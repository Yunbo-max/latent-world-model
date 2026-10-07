"""Immutable token documents and a serializable, document-preserving cursor."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import random

import numpy as np


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False).encode("utf-8")).hexdigest()


class CorpusWriter:
    """Publish manifest last. A directory without a manifest is incomplete."""
    def __init__(self, directory: str | Path, provenance: dict):
        self.path = Path(directory)
        self.path.mkdir(parents=True, exist_ok=True)
        if any(self.path.iterdir()):
            raise FileExistsError(f"Corpus destination must be empty: {self.path}")
        self.provenance = provenance
        self.tokens = (self.path / "tokens.bin").open("wb")
        self.index = (self.path / "index.jsonl").open("w", encoding="utf-8")
        self.token_count = self.document_count = self.target_count = 0
        self.closed = False

    def add(self, document_id: str, ids: list[int], loss_start: int = 0,
            metadata: dict | None = None) -> None:
        if self.closed:
            raise ValueError("CorpusWriter is closed")
        if not ids or not 0 <= loss_start <= len(ids):
            raise ValueError("Nonempty document and valid loss_start required")
        if min(ids) < 0 or max(ids) > 65535:
            raise ValueError("Token IDs must fit the declared uint16 format")
        record = {"id": str(document_id), "start": self.token_count,
                  "length": len(ids), "loss_start": loss_start}
        if metadata:
            record["metadata"] = metadata
        self.tokens.write(np.asarray(ids, dtype="<u2").tobytes())
        self.index.write(json.dumps(record, ensure_ascii=False) + "\n")
        self.token_count += len(ids)
        self.target_count += len(ids) - loss_start
        self.document_count += 1

    def close(self, publish: bool = True) -> None:
        if self.closed:
            return
        self.tokens.close()
        self.index.close()
        self.closed = True
        if publish:
            manifest = {"format": "lwm-token-documents-v1", "dtype": "<u2",
                        "tokens": self.token_count, "documents": self.document_count,
                        "targets": self.target_count, "provenance": self.provenance,
                        "files": {name: file_sha256(self.path / name)
                                  for name in ("tokens.bin", "index.jsonl")}}
            (self.path / "manifest.json").write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        self.close(publish=exc_type is None)


class TokenCorpus:
    def __init__(self, directory: str | Path, verify: bool = True):
        self.path = Path(directory)
        self.manifest = json.loads((self.path / "manifest.json").read_text(encoding="utf-8"))
        if self.manifest.get("format") != "lwm-token-documents-v1":
            raise ValueError("Unsupported corpus format")
        if self.manifest.get("dtype") != "<u2":
            raise ValueError("Corpus dtype must be little-endian uint16")
        if verify:
            for name in ("tokens.bin", "index.jsonl"):
                if file_sha256(self.path / name) != self.manifest["files"][name]:
                    raise ValueError(f"Corpus hash mismatch: {name}")
        self.fingerprint = canonical_hash(self.manifest)
        self.records = [json.loads(line) for line in
                        (self.path / "index.jsonl").read_text(encoding="utf-8").splitlines()]
        offset = targets = 0
        for record in self.records:
            if record["start"] != offset or record["length"] <= 0:
                raise ValueError("Corpus index must be contiguous nonempty documents")
            if not 0 <= record["loss_start"] <= record["length"]:
                raise ValueError("Invalid loss range")
            offset += record["length"]
            targets += record["length"] - record["loss_start"]
        if (offset != self.manifest["tokens"] or targets != self.manifest["targets"]
                or len(self.records) != self.manifest["documents"]
                or (self.path / "tokens.bin").stat().st_size != offset * 2):
            raise ValueError("Corpus count/byte-size mismatch")
        if not offset:
            raise ValueError("Corpus has no tokens")
        self.ids = np.memmap(self.path / "tokens.bin", dtype="<u2", mode="r")

    def document(self, index: int) -> np.ndarray:
        record = self.records[index]
        return self.ids[record["start"]:record["start"] + record["length"]]


@dataclass
class TokenWindow:
    ids: np.ndarray
    loss_mask: np.ndarray
    reset_before: bool
    ended_document: bool
    document_id: str
    epoch: int


class CorpusCursor:
    def __init__(self, corpus: TokenCorpus, seed: int, shuffle: bool = True,
                 repeat: bool = False):
        self.corpus, self.seed, self.shuffle, self.repeat = corpus, seed, shuffle, repeat
        self.epoch = self.document_position = self.token_offset = 0
        self._make_order()

    def _make_order(self):
        self.order = list(range(len(self.corpus.records)))
        if self.shuffle:
            random.Random(self.seed + self.epoch).shuffle(self.order)

    @property
    def exhausted(self) -> bool:
        return self.document_position == len(self.order) and not self.repeat

    def state_dict(self) -> dict:
        return {"corpus": self.corpus.fingerprint, "seed": self.seed,
                "shuffle": self.shuffle, "repeat": self.repeat, "epoch": self.epoch,
                "document_position": self.document_position, "token_offset": self.token_offset}

    def load_state_dict(self, state: dict) -> None:
        for key, expected in (("corpus", self.corpus.fingerprint), ("seed", self.seed),
                              ("shuffle", self.shuffle), ("repeat", self.repeat)):
            if state[key] != expected:
                raise ValueError(f"Resume cursor mismatch: {key}")
        self.epoch = int(state["epoch"])
        self.document_position = int(state["document_position"])
        self.token_offset = int(state["token_offset"])
        if self.epoch < 0 or not 0 <= self.document_position <= len(self.corpus.records):
            raise ValueError("Invalid cursor position")
        self._make_order()
        if self.document_position == len(self.order):
            valid = self.token_offset == 0
        else:
            valid = 0 <= self.token_offset < self.corpus.records[
                self.order[self.document_position]]["length"]
        if not valid:
            raise ValueError("Invalid cursor token offset")

    def take_window(self, max_length: int, max_targets: int | None = None) -> TokenWindow:
        if max_length <= 0 or (max_targets is not None and max_targets <= 0):
            raise ValueError("Positive window and target limits required")
        if self.document_position == len(self.order):
            if not self.repeat:
                raise StopIteration
            self.epoch += 1
            self.document_position = 0
            self._make_order()
        record_index = self.order[self.document_position]
        record = self.corpus.records[record_index]
        start = self.token_offset
        end = min(record["length"], start + max_length)
        mask = np.arange(start, end) >= record["loss_start"]
        if max_targets is not None and int(mask.sum()) > max_targets:
            end = start + int(np.flatnonzero(mask)[max_targets - 1]) + 1
            mask = mask[:end - start]
        ids = np.asarray(self.corpus.document(record_index)[start:end], dtype=np.int64).copy()
        ended = end == record["length"]
        self.token_offset = end
        if ended:
            self.document_position += 1
            self.token_offset = 0
        return TokenWindow(ids, mask, start == 0, ended, record["id"], self.epoch)
