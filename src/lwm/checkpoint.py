"""Atomic trusted-project checkpoints, with an explicit resume contract."""
from __future__ import annotations

import os
import hashlib
from pathlib import Path
import random
import tempfile

import numpy as np
import torch


def capture_rng() -> dict:
    numpy_state = np.random.get_state()
    return {"python": random.getstate(), "numpy": {
        "name": numpy_state[0], "keys": numpy_state[1].tolist(),
        "position": int(numpy_state[2]), "has_gauss": int(numpy_state[3]),
        "cached_gaussian": float(numpy_state[4])},
        "torch": torch.get_rng_state(),
        "cuda": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else []}


def restore_rng(state: dict) -> None:
    random.setstate(state["python"])
    value = state["numpy"]
    np.random.set_state((value["name"], np.asarray(value["keys"], dtype=np.uint32),
                         value["position"], value["has_gauss"], value["cached_gaussian"]))
    torch.set_rng_state(state["torch"].cpu())
    if state["cuda"]:
        if not torch.cuda.is_available() or len(state["cuda"]) != torch.cuda.device_count():
            raise ValueError("CUDA RNG inventory differs from checkpoint")
        torch.cuda.set_rng_state_all([item.cpu() for item in state["cuda"]])


def save_checkpoint(path: str | Path, payload: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(handle, "wb") as stream:
            torch.save({"format": "lwm-checkpoint-v1", **payload}, stream)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def _stream_sha256(stream) -> str:
    stream.seek(0)
    digest = hashlib.sha256()
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
        digest.update(chunk)
    return digest.hexdigest()


def load_checkpoint_with_sha256(path: str | Path, map_location="cpu") -> tuple[dict, str]:
    """Bind payload and digest to one opened file, despite atomic path replacement.

    The writer publishes with os.replace. Holding its original file descriptor
    avoids reopening a newer checkpoint for identity. Streaming checks on both
    sides of deserialization reject unsupported in-place edits without buffering
    an additional whole checkpoint in CPU memory.
    """
    # Unbuffered reads make the second digest observe the inode's current bytes,
    # rather than a BufferedReader cache after an unsupported in-place edit.
    with Path(path).open("rb", buffering=0) as stream:
        digest = _stream_sha256(stream)
        stream.seek(0)
        value = torch.load(stream, map_location=map_location, weights_only=True)
        if _stream_sha256(stream) != digest:
            raise ValueError("Checkpoint changed during loading")
    if value.get("format") != "lwm-checkpoint-v1":
        raise ValueError("Unsupported checkpoint format")
    return value, digest


def load_checkpoint(path: str | Path, map_location="cpu") -> dict:
    return load_checkpoint_with_sha256(path, map_location=map_location)[0]
