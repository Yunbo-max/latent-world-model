"""Pinned asset acquisition and complete corpus preparation for Local execution.

No network or model loading occurs at import time. The four CLI commands acquire
only the explicitly listed files; they never obtain model weights or a mutable
Hub revision. Native preparation is an auditable adapter, not a claim that the
official teacher/scorer replay or hardware qualification has already passed.
"""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import ExitStack
import hashlib
from importlib.metadata import version
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import sqlite3
import sys
import tarfile
import tempfile
import time
import unicodedata
from urllib.request import Request, urlopen

from .data import CorpusWriter, file_sha256


ASSET_MANIFEST_PATH = Path(__file__).resolve().parents[2] / "configs" / "assets.json"
EOS_TOKEN_ID = 50256
SPLITS = ("train", "valid", "test")
BABI_CONTEXT_POLICY = "all_observed_facts_then_current_question_no_prior_questions_or_answers"


def load_assets(path: str | Path | None = None) -> dict:
    """Read the public, versioned source manifest in the project checkout."""
    manifest_path = Path(path) if path is not None else ASSET_MANIFEST_PATH
    assets = json.loads(manifest_path.read_text(encoding="utf-8"))
    if assets.get("format") != "lwm-source-assets-v1":
        raise ValueError("Unsupported source asset manifest")
    for name in ("tokenizer", "fineweb", "lambada"):
        if not re.fullmatch(r"[0-9a-f]{40}", assets[name]["revision"]):
            raise ValueError(f"A full immutable Hub revision is required: {name}")
    files = assets["fineweb"]["files"]
    paths = [item["path"] for item in files]
    if paths != sorted(set(paths)):
        raise ValueError("FineWeb files must be unique and in canonical source order")
    if sum(item["bytes"] for item in files) > assets["fineweb"]["source_byte_limit"]:
        raise ValueError("Pinned FineWeb files exceed the source byte limit")
    return assets


def git_blob_sha1(path: str | Path) -> str:
    path = Path(path)
    digest = hashlib.sha1(f"blob {path.stat().st_size}\0".encode("ascii"))
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_asset(path: str | Path, specification: dict) -> dict:
    """Verify advertised content identity, then record an independent SHA-256."""
    path = Path(path)
    size = path.stat().st_size
    if "bytes" in specification and size != specification["bytes"]:
        raise ValueError(f"Asset byte-size identity mismatch: {specification.get('path', path.name)}")
    sha256 = file_sha256(path)
    if "sha256" in specification and sha256 != specification["sha256"]:
        raise ValueError(f"Asset SHA-256 identity mismatch: {specification.get('path', path.name)}")
    result = {"path": specification.get("path", path.name), "bytes": size, "sha256": sha256}
    if "git_blob_sha1" in specification:
        blob_sha1 = git_blob_sha1(path)
        if blob_sha1 != specification["git_blob_sha1"]:
            raise ValueError(f"Asset Git-blob identity mismatch: {specification.get('path', path.name)}")
        result["git_blob_sha1"] = blob_sha1
    if "sha256" not in specification and "git_blob_sha1" not in specification:
        raise ValueError("An expected source content digest is required")
    return result


def _write_json(path: Path, value: dict) -> None:
    temporary = path.with_name(path.name + ".partial")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
                         + "\n", encoding="utf-8")
    temporary.replace(path)


def _empty_destination(path: str | Path) -> Path:
    destination = Path(path)
    destination.mkdir(parents=True, exist_ok=True)
    if any(destination.iterdir()):
        raise FileExistsError(f"Destination must be empty; use a new output directory: {destination}")
    return destination


def _directory_bytes(path: Path) -> int:
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def _implementation_identity() -> dict:
    return {
        "prepare.py": file_sha256(Path(__file__)),
        "data.py": file_sha256(Path(__file__).with_name("data.py")),
        "assets.json": file_sha256(ASSET_MANIFEST_PATH),
        "python": sys.version,
        "packages": {name: version(name) for name in
                     ("transformers", "tokenizers", "huggingface-hub", "pyarrow", "numpy")},
        "execution_role": "local_asset_preparation",
        "native_adapter_parity": "not_established_by_preparation",
    }


def _download_hf(source: dict, specification: dict, cache: Path) -> tuple[Path, dict]:
    from huggingface_hub import hf_hub_download

    if not re.fullmatch(r"[0-9a-f]{40}", source["revision"]):
        raise ValueError("Refusing an unpinned Hub revision")
    path = Path(hf_hub_download(repo_id=source["repo_id"], repo_type=source["repo_type"],
                              revision=source["revision"], filename=specification["path"],
                              cache_dir=str(cache / "huggingface"), etag_timeout=30))
    return path, verify_asset(path, specification)


def _tokenizer_identity_from_files(path: Path) -> dict:
    specification = load_assets()["tokenizer"]
    expected_names = {item["path"] for item in specification["files"]}
    actual_names = {item.name for item in path.iterdir()}
    if actual_names != expected_names | {"preparation.json"}:
        raise ValueError("Tokenizer directory must contain exactly the pinned files and preparation.json")
    return {
        "repo_id": specification["repo_id"], "revision": specification["revision"],
        "class": specification["class"], "vocab_size": specification["vocab_size"],
        "eos_token_id": specification["eos_token_id"],
        "files": {item["path"]: verify_asset(path / item["path"], item)
                  for item in specification["files"]},
    }


def tokenizer_identity(path: str | Path) -> dict:
    """Return the verified identity shared by corpora, checkpoints and evaluation."""
    path = Path(path)
    actual = _tokenizer_identity_from_files(path)
    saved = json.loads((path / "preparation.json").read_text(encoding="utf-8"))
    if saved.get("format") != "lwm-tokenizer-preparation-v1" or saved.get("tokenizer") != actual:
        raise ValueError("Tokenizer preparation identity mismatch")
    return actual


def load_tokenizer(path: str | Path):
    """Load only the locally verified GPT-2 tokenizer, never pretrained weights.

    Native benchmark tokenization retains the default special-token policy.
    FineWeb explicitly opts into ordinary encoding in :func:`encode_document`.
    """
    from transformers import GPT2TokenizerFast

    identity = tokenizer_identity(path)
    tokenizer = GPT2TokenizerFast.from_pretrained(str(Path(path)), local_files_only=True,
                                                add_prefix_space=False)
    if (len(tokenizer) != identity["vocab_size"]
            or tokenizer.vocab_size != identity["vocab_size"]
            or tokenizer.eos_token_id != identity["eos_token_id"]
            or tokenizer.bos_token_id != identity["eos_token_id"]
            or tokenizer.convert_tokens_to_ids("<|endoftext|>") != identity["eos_token_id"]):
        raise ValueError("Loaded tokenizer mapping does not match the pinned identity")
    return tokenizer


def prepare_tokenizer(cache: str | Path, output: str | Path) -> dict:
    destination = _empty_destination(output)
    source = load_assets()["tokenizer"]
    measured = {}
    for specification in source["files"]:
        acquired, _ = _download_hf(source, specification, Path(cache))
        shutil.copyfile(acquired, destination / specification["path"])
        measured[specification["path"]] = verify_asset(destination / specification["path"], specification)
    identity = {"repo_id": source["repo_id"], "revision": source["revision"],
                "class": source["class"], "vocab_size": source["vocab_size"],
                "eos_token_id": source["eos_token_id"], "files": measured}
    manifest = {"format": "lwm-tokenizer-preparation-v1", "tokenizer": identity,
                "source_bytes_verified": sum(item["bytes"] for item in measured.values()),
                "implementation": _implementation_identity(),
                "license_record": source["license_record"]}
    _write_json(destination / "preparation.json", manifest)
    # Mapping qualification is part of preparation, not assumed from the constants.
    try:
        load_tokenizer(destination)
    except Exception:
        (destination / "preparation.json").unlink()
        raise
    return manifest


def content_key(text: str) -> str:
    normalized = " ".join(unicodedata.normalize("NFC", text).split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def split_for_key(key: str) -> str:
    bucket = int(key[:16], 16) % 10000
    return "valid" if bucket < 50 else "test" if bucket < 100 else "train"


def encode_document(tokenizer, text: str) -> list[int]:
    """Encode raw text without interpreting an in-text EOS spelling as a marker.

    transformers 4.46.3 forwards split_special_tokens to the fast backend's
    encode_special_tokens flag. tokenizers 0.20.3 then excludes registered
    special-token matches, leaving their literal bytes for ordinary BPE.
    """
    ids = tokenizer.encode(text, add_special_tokens=False, split_special_tokens=True)
    if EOS_TOKEN_ID in ids:
        raise ValueError("Ordinary document encoding unexpectedly emitted a special EOS token")
    return ids + [EOS_TOKEN_ID]


class FineWebBuilder:
    """Incremental deterministic splitter with a disk-backed exact dedup index.

    The target budgets are prefix lengths before any training-time shuffle.
    The final document is a true target prefix; an omitted EOS is never added
    merely to make a truncated document look complete.
    """
    def __init__(self, directory: str | Path, tokenizer, budgets: dict, provenance: dict):
        self.path = Path(directory)
        self.path.mkdir(parents=True, exist_ok=True)
        if set(budgets) != set(SPLITS) or any(type(value) is not int or value <= 0
                                            for value in budgets.values()):
            raise ValueError("Positive exact train, valid and test token budgets are required")
        self.tokenizer, self.budgets, self.provenance = tokenizer, dict(budgets), provenance
        self.counts = {split: 0 for split in SPLITS}
        self.stats = {"source_rows_seen": 0, "empty_documents": 0, "duplicate_documents": 0,
                      "already_full_split_documents": 0, "encoded_documents": 0,
                      "literal_special_token_documents": 0, "special_token_documents_dropped": 0}
        self.writers = {split: CorpusWriter(self.path / split,
                                           {**provenance, "split": split, "target_budget": budgets[split]})
                        for split in SPLITS}
        self.seen = sqlite3.connect(self.path / "content_hashes.sqlite")
        self.seen.execute("PRAGMA journal_mode=DELETE")
        self.seen.execute("PRAGMA cache_size=-16384")
        self.seen.execute("CREATE TABLE seen (content_hash BLOB PRIMARY KEY, split TEXT NOT NULL) WITHOUT ROWID")
        self.finished = self.closed = False

    @property
    def complete(self) -> bool:
        return all(self.counts[split] == self.budgets[split] for split in SPLITS)

    def add_row(self, row: dict, source: dict, row_number: int) -> None:
        if self.finished or self.closed:
            raise ValueError("FineWebBuilder is closed")
        self.stats["source_rows_seen"] += 1
        text = row.get("text")
        if not isinstance(text, str):
            raise ValueError(f"FineWeb text must be a string at {source['path']}:{row_number}")
        if not text.split():
            self.stats["empty_documents"] += 1
            return
        key = content_key(text)
        split = split_for_key(key)
        cursor = self.seen.execute("INSERT OR IGNORE INTO seen VALUES (?, ?)",
                                   (bytes.fromhex(key), split))
        if cursor.rowcount == 0:
            self.stats["duplicate_documents"] += 1
            return
        if self.stats["source_rows_seen"] % 10_000 == 0:
            self.seen.commit()
        remaining = self.budgets[split] - self.counts[split]
        if not remaining:
            self.stats["already_full_split_documents"] += 1
            return
        ids = encode_document(self.tokenizer, text)
        self.stats["encoded_documents"] += 1
        self.stats["literal_special_token_documents"] += int("<|endoftext|>" in text)
        kept = ids[:remaining]
        truncated = len(kept) != len(ids)
        identifier = f"fineweb-edu:{source['sha256']}:row:{row_number}"
        metadata = {"source_shard": source["path"], "source_sha256": source["sha256"],
                    "source_row": row_number, "native_id": row.get("id"),
                    "content_sha256": key, "split": split,
                    "original_target_tokens": len(ids), "truncated_tail": truncated,
                    "terminal_eos_included": not truncated,
                    "raw_text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()}
        self.writers[split].add(identifier, kept, loss_start=0, metadata=metadata)
        self.counts[split] += len(kept)

    def finish(self) -> None:
        if not self.complete:
            missing = {split: self.budgets[split] - self.counts[split] for split in SPLITS}
            raise ValueError(f"Insufficient unique source tokens; no repetition is allowed: {missing}")
        self.seen.commit()
        self.finished = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        self.seen.commit()
        self.seen.close()
        self.closed = True
        publish = exc_type is None and self.finished
        for writer in self.writers.values():
            writer.provenance["preparation_stats"] = dict(self.stats)
            writer.close(publish=publish)
        if exc_type is None and not self.finished:
            raise ValueError("FineWebBuilder.finish() must establish all exact budgets before publication")


def prepare_fineweb(tokenizer_path: str | Path, cache: str | Path, output: str | Path,
                    tokens: int, valid_tokens: int = 1_000_000,
                    test_tokens: int = 1_000_000) -> dict:
    import pyarrow.parquet as parquet

    if tokens not in (100_000_000, 1_000_000_000):
        raise ValueError("The frozen training budgets are 100000000 and 1000000000")
    destination = _empty_destination(output)
    tokenizer = load_tokenizer(tokenizer_path)
    identity = tokenizer_identity(tokenizer_path)
    source = load_assets()["fineweb"]
    acquired_sources = []
    budgets = {"train": tokens, "valid": valid_tokens, "test": test_tokens}
    provenance = {"dataset": "fineweb-edu", "repo_id": source["repo_id"],
                  "revision": source["revision"], "configuration": source["configuration"],
                  "native_split": source["native_split"], "tokenizer": identity,
                  "split_policy": source["split_policy"], "source_files": acquired_sources,
                  "implementation": _implementation_identity(),
                  "document_boundary": "index document boundary resets; chunk boundaries only detach",
                  "target_definition": "raw-text ordinary BPE plus EOS; exact prefix, no SEG or padding"}
    start = time.monotonic()
    with FineWebBuilder(destination, tokenizer, budgets, provenance) as builder:
        verified_source_bytes = 0
        for shard_index, specification in enumerate(source["files"]):
            if builder.complete and shard_index >= source["minimum_acquired_shards"]:
                break
            if verified_source_bytes + specification["bytes"] > source["source_byte_limit"]:
                raise ValueError("FineWeb source acquisition would exceed the 30 GB bound")
            print(f"Acquiring pinned FineWeb shard {specification['path']}", file=sys.stderr, flush=True)
            shard_path, measured = _download_hf(source, specification, Path(cache))
            verified_source_bytes += measured["bytes"]
            measured["rows_consumed"] = 0
            acquired_sources.append(measured)
            if builder.complete:
                measured["scan_status"] = "acquired_minimum_shard_not_needed_for_budgets"
                continue
            shard = parquet.ParquetFile(shard_path)
            available = shard.schema_arrow.names
            if "text" not in available:
                raise ValueError(f"Pinned FineWeb shard has no text column: {specification['path']}")
            columns = [name for name in ("text", "id") if name in available]
            measured["native_rows"] = shard.metadata.num_rows
            measured["schema"] = str(shard.schema_arrow)
            row_number = 0
            for batch in shard.iter_batches(batch_size=128, columns=columns, use_threads=False):
                for row in batch.to_pylist():
                    builder.add_row(row, measured, row_number)
                    row_number += 1
                    if builder.complete:
                        break
                if builder.complete:
                    break
            measured["rows_consumed"] = row_number
            measured["scan_status"] = "complete" if row_number == shard.metadata.num_rows else "budget_prefix"
            print(f"Exact target counts so far: {builder.counts}", file=sys.stderr, flush=True)
        builder.finish()
    split_manifests = {split: json.loads((destination / split / "manifest.json").read_text(encoding="utf-8"))
                       for split in SPLITS}
    manifest = {"format": "lwm-fineweb-preparation-v1", "dataset": "fineweb-edu",
                "tokenizer": identity, "source": {"repo_id": source["repo_id"],
                                                  "revision": source["revision"],
                                                  "files": acquired_sources},
                "budgets": budgets, "counts": dict(builder.counts), "stats": dict(builder.stats),
                "splits": {split: {"directory": split, "targets": item["targets"],
                                     "documents": item["documents"],
                                     "manifest_sha256": file_sha256(destination / split / "manifest.json")}
                           for split, item in split_manifests.items()},
                "source_bytes_verified": verified_source_bytes,
                "source_byte_limit": source["source_byte_limit"],
                "prepared_bytes_before_summary": _directory_bytes(destination),
                "content_hash_index_sha256": file_sha256(destination / "content_hashes.sqlite"),
                "elapsed_seconds": time.monotonic() - start,
                "disk_peak_bytes": None, "disk_peak_status": "not_sampled; measure in Local run harness",
                "split_policy": source["split_policy"], "implementation": provenance["implementation"],
                "license_record": source["license_record"],
                "nested_budget_contract": "train/100M is an ordered token prefix of train/1B before training shuffle",
                "contamination_audit": "exact normalized-content dedup only; near duplicates and benchmark overlap unqualified"}
    _write_json(destination / "preparation.json", manifest)
    return manifest


def _download_archive(source: dict, cache: Path) -> tuple[Path, dict]:
    cache.mkdir(parents=True, exist_ok=True)
    destination = cache / f"{source['sha256']}.tar.gz"
    expected = {"path": "babi.tar.gz", "sha256": source["sha256"]}
    if destination.exists():
        if destination.stat().st_size > source["download_byte_limit"]:
            raise ValueError("Cached archive exceeds the download byte limit")
        return destination, verify_asset(destination, expected)
    with tempfile.NamedTemporaryFile(dir=cache, prefix="babi-", suffix=".partial", delete=False) as created:
        temporary = Path(created.name)
    try:
        request = Request(source["url"], headers={"User-Agent": "lwm-pinned-asset-preparation/1"})
        with urlopen(request, timeout=60) as response, temporary.open("wb") as target:
            advertised = response.headers.get("Content-Length")
            if advertised is not None and int(advertised) > source["download_byte_limit"]:
                raise ValueError("Archive advertised size exceeds the download byte limit")
            count = 0
            for block in iter(lambda: response.read(1024 * 1024), b""):
                count += len(block)
                if count > source["download_byte_limit"]:
                    raise ValueError("Archive exceeds the download byte limit")
                target.write(block)
        measured = verify_asset(temporary, expected)
        temporary.replace(destination)
        return destination, measured
    finally:
        temporary.unlink(missing_ok=True)


def safe_extract_archive(archive: str | Path, destination: str | Path,
                         max_bytes: int) -> dict:
    """Preflight every member and manually copy regular files into an empty root."""
    destination = _empty_destination(destination)
    root = destination.resolve()
    with tarfile.open(archive, "r:gz") as source:
        members = source.getmembers()
        total = 0
        names = set()
        for member in members:
            path = PurePosixPath(member.name)
            if (path.is_absolute() or ".." in path.parts or "\\" in member.name
                    or "\0" in member.name or not (member.isfile() or member.isdir())):
                raise ValueError(f"Unsafe archive member: {member.name!r}")
            if not path.parts or path == PurePosixPath("."):
                if member.isdir():
                    continue
                raise ValueError("Unsafe empty archive member")
            canonical_name = path.as_posix()
            if canonical_name in names:
                raise ValueError(f"Unsafe duplicate archive member: {member.name!r}")
            names.add(canonical_name)
            target = root.joinpath(*path.parts)
            if not target.is_relative_to(root) or member.size < 0:
                raise ValueError(f"Unsafe archive path or size: {member.name!r}")
            if member.isfile():
                total += member.size
                if total > max_bytes:
                    raise ValueError("Archive uncompressed byte limit exceeded")
        extracted_files = 0
        for member in members:
            path = PurePosixPath(member.name)
            target = root.joinpath(*path.parts)
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            stream = source.extractfile(member)
            if stream is None:
                raise ValueError(f"Unreadable regular archive member: {member.name}")
            with stream, target.open("xb") as output:
                copied = 0
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    copied += len(block)
                    if copied > member.size:
                        raise ValueError("Archive member exceeds its declared byte size")
                    output.write(block)
            if copied != member.size:
                raise ValueError("Archive member byte-size mismatch")
            extracted_files += 1
    return {"extracted_files": extracted_files, "extracted_bytes": total,
            "extract_byte_limit": max_bytes, "archive_members": len(members)}


def iter_babi_examples(path: str | Path, *, task_id: int, split: str,
                       archive_sha256: str):
    """Parse the selected nosf files with the pinned teacher's labeled-act rules.

    Teacher text is incremental. ``native_text`` reproduces each act; ``context``
    is this adapter's full observed-fact history followed by the current question.
    Past questions and past labels are absent from both the persistent evidence
    serialization and its SFT counterpart. Unlabeled teacher acts are an explicit
    preparation error, never silently omitted from native coverage.
    """
    if task_id not in range(1, 21) or split not in SPLITS:
        raise ValueError("A native bAbI task 1..20 and train/valid/test split are required")
    facts, new_facts = [], []
    last_line_id = None
    episode = -1
    episode_turn = question_ordinal = 0
    reward = 0.0
    pending = None
    path = Path(path)
    with path.open("r", encoding="utf-8") as stream:
        for physical_line, raw in enumerate(stream, 1):
            line = raw.strip().replace("\\n", "\n")
            if not line:
                continue
            space = line.find(" ")
            line_id = int(line) if space == -1 else int(line[:space])
            fields = [field.strip() for field in line[space + 1:].split("\t")]
            boundary = last_line_id is None or line_id <= last_line_id
            if boundary:
                if new_facts:
                    raise ValueError(f"Unexpected unlabeled native teacher act before {path}:{physical_line}")
                if pending is not None:
                    pending["episode_done"] = True
                    yield pending
                    pending = None
                episode += 1
                episode_turn = 0
                facts, new_facts = [], []
                reward = 0.0
            last_line_id = line_id
            if len(fields) > 2 and fields[2]:
                # In the official nosf files this is reward, never supporting IDs.
                reward += float(fields[2])
            if len(fields) <= 1 or not fields[1]:
                facts.append(fields[0])
                new_facts.append(fields[0])
                continue
            labels = fields[1].split("|")
            if task_id in (8, 19):
                labels = [label.replace(",", " ") for label in labels]
            if len(labels) != 1:
                raise ValueError("Selected bAbI SFT protocol requires one native label per question")
            if pending is not None:
                yield pending
            identifier = f"babi:{archive_sha256}:task:{task_id}:split:{split}:question:{question_ordinal}"
            episode_id = f"babi:{archive_sha256}:task:{task_id}:split:{split}:episode:{episode}"
            question = fields[0]
            pending = {"id": identifier, "task_id": task_id, "split": split,
                       "episode_id": episode_id, "episode_index": episode,
                       "episode_turn": episode_turn, "episode_done": False,
                       "question_index": question_ordinal, "source_line": physical_line,
                       "source_line_id": line_id, "source_path": path.name,
                       "new_facts": list(new_facts), "question": question,
                       "native_text": "\n".join(new_facts + [question]),
                       "context": "\n".join(facts + [question]),
                       "answer": labels[0], "native_labels": labels,
                       "native_reward": reward,
                       "native_candidates_omitted": len(fields) > 3 and bool(fields[3]),
                       "context_policy": BABI_CONTEXT_POLICY}
            new_facts = []
            reward = 0.0
            episode_turn += 1
            question_ordinal += 1
    if new_facts:
        raise ValueError(f"Unexpected unlabeled native teacher act at EOF: {path}")
    if pending is not None:
        pending["episode_done"] = True
        yield pending


def serialize_babi_sft(tokenizer, example: dict) -> tuple[list[int], int]:
    """Supervise the leading-space answer tokens and EOS, with the full prompt."""
    prompt = example["context"]
    continuation = " " + example["answer"]
    prompt_ids = tokenizer.encode(prompt, add_special_tokens=False)
    answer_ids = tokenizer.encode(continuation, add_special_tokens=False)
    combined = tokenizer.encode(prompt + continuation, add_special_tokens=False)
    if combined != prompt_ids + answer_ids:
        raise ValueError(f"bAbI prompt/answer GPT-2 boundary mismatch: {example['id']}")
    if not answer_ids:
        raise ValueError(f"bAbI native answer has no tokenizer tokens: {example['id']}")
    return combined + [EOS_TOKEN_ID], len(prompt_ids)


def prepare_babi(tokenizer_path: str | Path, cache: str | Path, output: str | Path) -> dict:
    destination = _empty_destination(output)
    tokenizer = load_tokenizer(tokenizer_path)
    identity = tokenizer_identity(tokenizer_path)
    source = load_assets()["babi"]
    cache_path = Path(cache) / "babi"
    archive_path, archive_identity = _download_archive(source, cache_path)
    split_records = {}
    raw_sources = []
    start = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="babi-verified-", dir=cache_path) as temporary:
        extract = safe_extract_archive(archive_path, temporary, source["extract_byte_limit"])
        selected = Path(temporary) / source["selected_directory"]
        if not selected.is_dir():
            raise ValueError(f"Official archive lacks the selected directory: {source['selected_directory']}")
        provenance = {"dataset": "babi", "source_archive_sha256": source["sha256"],
                      "parlai_revision": source["parlai_revision"], "tokenizer": identity,
                      "context_policy": BABI_CONTEXT_POLICY, "answer_prefix": " ",
                      "loss_policy": "answer tokens including first leading-space token and final EOS only",
                      "adaptation_budget": "separate from pretraining target-token budget",
                      "implementation": _implementation_identity(), "source_files": raw_sources}
        # Publish both SFT manifests only after all 60 native files pass coverage.
        with ExitStack() as stack:
            writers = {split: stack.enter_context(CorpusWriter(destination / "sft" / split,
                                                               {**provenance, "split": split}))
                       for split in ("train", "valid")}
            for split in SPLITS:
                task_counts = {}
                jsonl_path = destination / f"{split}.jsonl"
                with jsonl_path.open("w", encoding="utf-8") as target:
                    for task_id in source["task_ids"]:
                        name = source["file_pattern"].format(task=task_id, split=split)
                        raw_path = selected / name
                        if not raw_path.is_file():
                            raise ValueError(f"Official archive lacks required native file: {name}")
                        source_record = {"path": f"{source['selected_directory']}/{name}",
                                         "sha256": file_sha256(raw_path), "bytes": raw_path.stat().st_size,
                                         "task_id": task_id, "split": split}
                        raw_sources.append(source_record)
                        examples = episodes = 0
                        for example in iter_babi_examples(raw_path, task_id=task_id, split=split,
                                                          archive_sha256=source["sha256"]):
                            example["source_path"] = source_record["path"]
                            example["source_sha256"] = source_record["sha256"]
                            target.write(json.dumps(example, ensure_ascii=False) + "\n")
                            examples += 1
                            episodes += int(example["episode_done"])
                            if split in writers:
                                ids, loss_start = serialize_babi_sft(tokenizer, example)
                                writers[split].add(example["id"], ids, loss_start=loss_start,
                                                   metadata={"task_id": task_id,
                                                             "episode_id": example["episode_id"],
                                                             "source_line": example["source_line"],
                                                             "source_sha256": source_record["sha256"],
                                                             "prompt_sha256": hashlib.sha256(example["context"].encode("utf-8")).hexdigest(),
                                                             "truncated_tail": False})
                        if examples == 0 or episodes == 0:
                            raise ValueError(f"Native bAbI task/split is empty: {task_id}/{split}")
                        if split == "test" and examples != 1000:
                            raise ValueError(f"Native bAbI task {task_id} test must contain all 1000 questions")
                        task_counts[str(task_id)] = {"examples": examples, "episodes": episodes,
                                                     "source_sha256": source_record["sha256"]}
                counts = {key: sum(item[key] for item in task_counts.values())
                          for key in ("examples", "episodes")}
                if counts != source["splits"][split]:
                    raise ValueError(f"Full native bAbI coverage mismatch for {split}: {counts}")
                split_records[split] = {"file": jsonl_path.name, "sha256": file_sha256(jsonl_path),
                                         **counts, "tasks": task_counts}
    manifest = {"format": "lwm-babi-preparation-v1", "dataset": "babi",
                "source": {"url": source["url"], "sha256": source["sha256"],
                           "bytes": archive_identity["bytes"], "parlai_revision": source["parlai_revision"],
                           "selected_directory": source["selected_directory"]},
                "tokenizer": identity, "splits": split_records,
                "source_files": raw_sources, "archive_extraction": extract,
                "source_bytes_verified": archive_identity["bytes"],
                "context_policy": BABI_CONTEXT_POLICY, "answer_prefix": " ",
                "teacher_text_policy": "native_text contains only new facts and current question; native labels/candidates never enter context",
                "sft": {"train": "sft/train", "valid": "sft/valid"},
                "sft_manifests": {split: file_sha256(destination / "sft" / split / "manifest.json")
                                  for split in ("train", "valid")},
                "native_examples_excluded": 0,
                "prepared_bytes_before_summary": _directory_bytes(destination),
                "elapsed_seconds": time.monotonic() - start,
                "implementation": provenance["implementation"],
                "license_record": source["license_record"],
                "adapter_qualification": "Source-authored parser; Local official teacher export and scorer parity still required."}
    _write_json(destination / "preparation.json", manifest)
    return manifest


def lambada_document(document: dict, row_number: int, source_sha256: str) -> dict:
    """Preserve the raw native document and the harness's literal-space boundary."""
    if not isinstance(document, dict) or not isinstance(document.get("text"), str):
        raise ValueError(f"LAMBADA row {row_number} must contain a text string")
    text = document["text"]
    pieces = text.split(" ")
    return {"id": f"lambada:{source_sha256}:{row_number}", "source_row": row_number,
            "text": text, "context": " ".join(pieces[:-1]), "target": " " + pieces[-1],
            "source_document": document}


def prepare_lambada(cache: str | Path, output: str | Path) -> dict:
    destination = _empty_destination(output)
    source = load_assets()["lambada"]
    source_path, source_identity = _download_hf(source, source["file"], Path(cache))
    # Retain the exact native bytes for official local-harness replay.
    shutil.copyfile(source_path, destination / "lambada_test.jsonl")
    verify_asset(destination / "lambada_test.jsonl", source["file"])
    counts = Counter()
    output_path = destination / "test.jsonl"
    with source_path.open("r", encoding="utf-8") as stream, output_path.open("w", encoding="utf-8") as target:
        for row_number, line in enumerate(stream):
            if not line.strip():
                raise ValueError(f"Blank physical line in the pinned native JSONL at {row_number}; no row is silently dropped")
            document = json.loads(line)
            example = lambada_document(document, row_number, source_identity["sha256"])
            counts["examples"] += 1
            counts["empty_text"] += int(example["text"] == "")
            counts["literal_special_token_text"] += int("<|endoftext|>" in example["text"])
            counts["extra_field_documents"] += int(set(document) != {"text"})
            target.write(json.dumps(example, ensure_ascii=False) + "\n")
    if counts["examples"] != source["examples"]:
        raise ValueError(f"LAMBADA requires the complete 5153 rows, found {counts['examples']}")
    manifest = {"format": "lwm-lambada-preparation-v1", "dataset": "lambada_openai",
                "source": {"repo_id": source["repo_id"], "revision": source["revision"],
                           **source_identity, "harness_revision": source["harness_revision"]},
                "splits": {"test": {"file": "test.jsonl", "sha256": file_sha256(output_path),
                                    "examples": counts["examples"]}},
                "native_file": "lambada_test.jsonl", "counts": dict(counts),
                "native_examples_excluded": 0,
                "context_policy": "' '.join(text.split(' ')[:-1])",
                "target_policy": "' ' + text.split(' ')[-1]",
                "source_bytes_verified": source_identity["bytes"],
                "prepared_bytes_before_summary": _directory_bytes(destination),
                "implementation": _implementation_identity(),
                "license_record": source["license_record"]}
    _write_json(destination / "preparation.json", manifest)
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Acquire pinned, hash-verified assets and prepare exact corpora. No model weights are downloaded.",
        epilog="Outputs must be empty/new. Run from the installed editable project checkout. Preparation is not native scorer qualification.")
    commands = parser.add_subparsers(dest="command", required=True)
    tokenizer = commands.add_parser("tokenizer", help="Acquire and verify the five pinned GPT-2 tokenizer files.")
    fineweb = commands.add_parser("fineweb", help="Prepare exact nested 100M/1B train prefixes and fixed disjoint heldouts.")
    babi = commands.add_parser("babi", help="Prepare all 20 native English 10k tasks plus answer-only train/valid SFT.")
    lambada = commands.add_parser("lambada", help="Prepare all 5153 pinned English test passages and preserve native JSONL.")
    for command in (tokenizer, fineweb, babi, lambada):
        command.add_argument("--cache", type=Path, required=True, help="Reusable source download cache.")
        command.add_argument("--output", type=Path, required=True, help="New or empty destination; never overwritten.")
    for command in (fineweb, babi):
        command.add_argument("--tokenizer", type=Path, required=True, help="Verified output of the tokenizer command.")
    fineweb.add_argument("--tokens", type=int, choices=(100_000_000, 1_000_000_000), required=True,
                         help="Exact nonpadding target count in train, including only actually consumed EOS.")
    fineweb.add_argument("--valid-tokens", type=int, default=1_000_000, help="Exact fixed validation target prefix (default 1000000).")
    fineweb.add_argument("--test-tokens", type=int, default=1_000_000, help="Exact fixed test target prefix (default 1000000).")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    if args.command == "tokenizer":
        manifest = prepare_tokenizer(args.cache, args.output)
    elif args.command == "fineweb":
        manifest = prepare_fineweb(args.tokenizer, args.cache, args.output,
                                  args.tokens, args.valid_tokens, args.test_tokens)
    elif args.command == "babi":
        manifest = prepare_babi(args.tokenizer, args.cache, args.output)
    else:
        manifest = prepare_lambada(args.cache, args.output)
    print(json.dumps({"output": str(args.output), "format": manifest["format"],
                      "preparation_sha256": file_sha256(args.output / "preparation.json")}, sort_keys=True))


if __name__ == "__main__":
    main()
