"""Artifact identities and crash-safe small metadata writes."""
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def read_json(path):
    with Path(path).open(encoding="utf-8") as stream:
        return json.load(stream)


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8") as stream:
        temporary = Path(stream.name)
        json.dump(value, stream, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)
    fsync_directory(path.parent)


def fsync_directory(path):
    descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def resolve_checkpoint(directory):
    directory = Path(directory)
    receipt = read_json(directory / "checkpoint.json")
    path = within(directory, receipt["path"])
    if not path.is_file() or sha256_file(path) != receipt["sha256"]:
        raise ValueError("Checkpoint hash mismatch; preserve this attempt")
    return path


def append_jsonl(path, value):
    with Path(path).open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(value, sort_keys=True, allow_nan=False) + "\n")
        stream.flush()


def git_identity(root, source_manifest=None, allow_staged=True):
    root = Path(root).resolve()
    source_manifest = (source_manifest or os.environ.get("LWM_SOURCE_IDENTITY")) if allow_staged else None
    if source_manifest:
        expected = read_json(source_manifest)
        if expected["status"] or expected["format"] != "lwm-source-v1":
            raise ValueError("Source capture must come from a clean committed checkout")
        for relative, digest in expected["files"].items():
            if sha256_file(within(root, relative)) != digest:
                raise ValueError(f"Staged source integrity mismatch: {relative}")
        for folder in ("src", "scripts", "tests"):
            for path in (root / folder).rglob("*.py"):
                if str(path.relative_to(root)) not in expected["files"]:
                    raise ValueError(f"Uncaptured Python source: {path}")
        return expected
    def git(*args):
        return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()
    files = subprocess.check_output(["git", "-C", str(root), "ls-files", "-z"]).decode().split("\0")
    return {"format": "lwm-source-v1", "commit": git("rev-parse", "HEAD"),
            "status": git("status", "--porcelain"),
            "files": {name: sha256_file(within(root, name)) for name in files if name}}


def within(root, relative):
    root = Path(root).resolve()
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError(f"Path escapes artifact root: {relative}")
    return path
