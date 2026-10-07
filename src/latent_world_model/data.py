"""Exact target-token accounting over a retained token stream."""
import math
from pathlib import Path
import numpy as np
from .io import read_json, sha256_file, within


def count_targets(labels):
    return int(np.count_nonzero(np.asarray(labels) != -100))


def validate_corpus(manifest_path):
    manifest_path = Path(manifest_path)
    manifest = read_json(manifest_path)
    if manifest["format"] != "lwm-token-corpus-v1" or manifest["dtype"] != "<u4":
        raise ValueError("Unsupported corpus format")
    index = manifest_path.parent / "documents.jsonl"
    if not index.is_file() or sha256_file(index) != manifest["document_index_sha256"]:
        raise ValueError("Document index hash mismatch")
    for split, entry in manifest["files"].items():
        path = within(manifest_path.parent, entry["path"])
        if path.stat().st_size != entry["tokens"] * 4:
            raise ValueError(f"{split}: token count and file length differ")
        if sha256_file(path) != entry["sha256"]:
            raise ValueError(f"{split}: input hash mismatch")
    return manifest


class TokenBlocks:
    """Adjacent windows overlap by one input token; every target appears once.

    Targets are already shifted. Call the trainer's summed CE, never pass these
    targets to a HF model's labels argument (which would shift them again).
    """

    def __init__(self, manifest_path, split, seq_len, target_tokens=None):
        if not isinstance(seq_len, int) or seq_len <= 0:
            raise ValueError("seq_len must be positive")
        manifest_path = Path(manifest_path)
        manifest = read_json(manifest_path)
        entry = manifest["files"][split]
        self.path = within(manifest_path.parent, entry["path"])
        if self.path.stat().st_size != entry["tokens"] * 4:
            raise ValueError("Corpus size mismatch")
        available = entry["tokens"] - 1
        self.target_tokens = available if target_tokens is None else target_tokens
        if not isinstance(self.target_tokens, int) or not 0 < self.target_tokens <= available:
            raise ValueError(f"target_tokens must be in [1, {available}] available targets")
        self.seq_len = seq_len
        self.tokens = np.memmap(self.path, dtype="<u4", mode="r")

    def __len__(self):
        return math.ceil(self.target_tokens / self.seq_len)

    def __getitem__(self, index):
        if not isinstance(index, (int, np.integer)) or not 0 <= index < len(self):
            raise IndexError(index)
        start = int(index) * self.seq_len
        valid = min(self.seq_len, self.target_tokens - start)
        inputs = np.zeros(self.seq_len, dtype=np.int64)
        targets = np.full(self.seq_len, -100, dtype=np.int64)
        inputs[:valid] = self.tokens[start:start + valid]
        targets[:valid] = self.tokens[start + 1:start + valid + 1]
        return inputs, targets


def batch_at(dataset, order, offset, size):
    pairs = [dataset[int(i)] for i in order[offset:offset + size]]
    return np.stack([x for x, _ in pairs]), np.stack([y for _, y in pairs])
