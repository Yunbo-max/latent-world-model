"""Pinned model/source acquisition for Local preparation tasks."""
import argparse
from pathlib import Path
import subprocess
from .io import read_json, sha256_file, write_json


def acquire_model(name, source_path, directory, tokenizer_only=False):
    from huggingface_hub import snapshot_download
    sources = read_json(source_path)
    spec = sources["models"][name]
    directory = Path(directory).resolve() / name
    receipt_path = directory / "acquisition.json"
    if receipt_path.exists():
        existing = verify_assets(directory)
        if existing["repo"] != spec["repo"] or existing["revision"] != spec["revision"]:
            raise ValueError("Asset directory belongs to another revision; choose a new directory")
    required = list(spec["tokenizer_files"])
    if not tokenizer_only:
        required += spec["model_files"]
    snapshot_download(repo_id=spec["repo"], revision=spec["revision"],
                      allow_patterns=required, local_dir=directory, max_workers=2)
    inventory = {}
    for relative in required:
        path = directory / relative
        if not path.is_file() or path.stat().st_size == 0:
            raise ValueError(f"Missing required asset {path}")
        with path.open("rb") as stream:
            head = stream.read(128)
        if head.startswith(b"version https://git-lfs.github.com/spec/") or head.lstrip().lower().startswith(b"<!doctype html"):
            raise ValueError(f"Downloaded pointer or HTML instead of {path}")
        inventory[relative] = {"bytes": path.stat().st_size, "sha256": sha256_file(path)}
    # A later tokenizer-only request cannot invalidate a complete matching acquisition.
    if receipt_path.exists():
        for relative, entry in read_json(receipt_path)["files"].items():
            if sha256_file(directory / relative) != entry["sha256"]:
                raise ValueError("Asset integrity changed during acquisition; retain the old receipt")
            if relative not in inventory:
                inventory[relative] = entry
    write_json(receipt_path, {"repo": spec["repo"], "revision": spec["revision"],
               "files": inventory, "hash_scope": "actual acquired bytes; not an invented upstream checksum"})
    print(receipt_path, flush=True)


def verify_assets(directory):
    directory = Path(directory)
    receipt = read_json(directory / "acquisition.json")
    for relative, expected in receipt["files"].items():
        file = directory / relative
        if not file.is_file() or file.stat().st_size != expected["bytes"] or sha256_file(file) != expected["sha256"]:
            raise ValueError(f"Asset integrity mismatch: {file}; preserve this directory and reacquire into a new one")
    return receipt


def acquire_coconut(source_path, output):
    spec = read_json(source_path)["coconut"]
    output = Path(output).resolve()
    if not output.exists():
        output.mkdir(parents=True)
        subprocess.run(["git", "init", str(output)], check=True)
        subprocess.run(["git", "-C", str(output), "remote", "add", "origin", spec["url"]], check=True)
        subprocess.run(["git", "-C", str(output), "fetch", "--depth", "1", "origin", spec["revision"]], check=True)
        subprocess.run(["git", "-C", str(output), "checkout", "--detach", "FETCH_HEAD"], check=True)
    actual = subprocess.check_output(["git", "-C", str(output), "rev-parse", "HEAD"], text=True).strip()
    if actual != spec["revision"]:
        raise ValueError("Existing Coconut checkout has a different revision; preserve it")
    dirty_tracked = subprocess.check_output(["git", "-C", str(output), "diff", "HEAD", "--"], text=True)
    if dirty_tracked:
        raise ValueError("Existing Coconut author source has tracked modifications")
    inventory = {name: sha256_file(output / name) for name in spec["source_files"]}
    write_json(output.parent / "coconut-acquisition.json", {"source": spec, "files": inventory})
    print(output, flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["smollm2", "gpt2", "coconut", "verify"])
    parser.add_argument("--sources", default="configs/sources.json")
    parser.add_argument("--directory", default="assets")
    parser.add_argument("--tokenizer-only", action="store_true")
    args = parser.parse_args()
    if args.action == "coconut":
        acquire_coconut(args.sources, args.directory)
    elif args.action == "verify":
        print(verify_assets(args.directory))
    else:
        acquire_model(args.action, args.sources, args.directory, args.tokenizer_only)


if __name__ == "__main__":
    main()
