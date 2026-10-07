"""Local-only acquisition of a deterministic published-corpus training prefix."""
import argparse
import hashlib
import os
from pathlib import Path
import uuid
import numpy as np
from .io import canonical_hash, read_json, sha256_file, write_json
from .data import validate_corpus


def prepare(source_path, assets_dir, output_dir, target_tokens, dev_tokens=1_000_000):
    from datasets import load_dataset
    from transformers import AutoTokenizer
    if target_tokens <= 0 or dev_tokens <= 0:
        raise ValueError("Token budgets must be positive")
    sources = read_json(source_path)
    source = sources["training_dataset"]
    tokenizer_source = sources["models"]["smollm2"]
    request = {"source": source, "tokenizer": tokenizer_source,
               "target_tokens": target_tokens, "dev_tokens": dev_tokens,
               "split_rule": "sha256(text_utf8) mod 1000 < 10 is dev; else train"}
    output_dir = Path(output_dir).resolve()
    manifest_path = output_dir / "manifest.json"
    if manifest_path.exists():
        old = validate_corpus(manifest_path)
        if old["request_hash"] != canonical_hash(request):
            raise ValueError("Existing corpus has a different preparation request; choose a new output")
        return manifest_path
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValueError("Output is nonempty without a complete manifest; preserve it and choose a new output")
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_dir.parent / (output_dir.name + ".partial-" + uuid.uuid4().hex[:12])
    temporary.mkdir()
    model_dir = Path(assets_dir) / "smollm2"
    tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
    from .assets import verify_assets
    receipt = verify_assets(model_dir)
    if receipt["revision"] != tokenizer_source["revision"] or receipt["repo"] != tokenizer_source["repo"]:
        raise ValueError("Tokenizer acquisition identity differs from configured source")
    dataset = load_dataset(source["repo"], name=source["config"], split=source["split"],
                           revision=source["revision"], streaming=True)
    limits = {"train": target_tokens + 1, "dev": dev_tokens + 1}
    counts = {"train": 0, "dev": 0}
    documents = {"train": 0, "dev": 0}
    streams = {split: (temporary / f"{split}.bin").open("wb") for split in limits}
    scanned = 0
    try:
        with (temporary / "documents.jsonl").open("w", encoding="utf-8") as index:
            for row in dataset:
                scanned += 1
                text = row["text"]
                digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
                split = "dev" if int(digest, 16) % 1000 < 10 else "train"
                if counts[split] >= limits[split]:
                    continue
                ids = tokenizer.encode(text, add_special_tokens=False) + [tokenizer.eos_token_id]
                remaining = limits[split] - counts[split]
                kept = ids[:remaining]
                if ids and (min(ids) < 0 or max(ids) >= len(tokenizer)):
                    raise ValueError("Tokenizer ID is out of vocabulary")
                np.asarray(kept, dtype="<u4").tofile(streams[split])
                index.write(__import__("json").dumps({"source_id": row.get("id"), "text_sha256": digest,
                    "split": split, "offset": counts[split], "tokens": len(kept),
                    "original_tokens": len(ids)}, sort_keys=True) + "\n")
                counts[split] += len(kept)
                documents[split] += 1
                if scanned % 1000 == 0:
                    print({"scanned": scanned, "written_tokens": counts}, flush=True)
                if all(counts[s] == limits[s] for s in limits):
                    break
    finally:
        for stream in streams.values():
            stream.flush()
            os.fsync(stream.fileno())
            stream.close()
    if counts != limits:
        raise ValueError(f"Published stream exhausted before requested budget: {counts}; partial data retained")
    manifest = {"format": "lwm-token-corpus-v1", "dtype": "<u4",
                "request_hash": canonical_hash(request), "request": request,
                "tokenizer": tokenizer_source, "scanned_documents": scanned,
                "document_counts": documents, "files": {
                    s: {"path": f"{s}.bin", "tokens": counts[s],
                        "sha256": sha256_file(temporary / f"{s}.bin")} for s in counts},
                "document_index_sha256": sha256_file(temporary / "documents.jsonl")}
    write_json(temporary / "manifest.json", manifest)
    if output_dir.exists():
        output_dir.rmdir()  # only the previously checked empty directory
    os.replace(temporary, output_dir)
    print(manifest_path, flush=True)
    return manifest_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", default="configs/sources.json")
    parser.add_argument("--assets", default="assets")
    parser.add_argument("--output", required=True)
    parser.add_argument("--tokens", type=int, required=True)
    parser.add_argument("--dev-tokens", type=int, default=1_000_000)
    args = parser.parse_args()
    prepare(args.sources, args.assets, args.output, args.tokens, args.dev_tokens)


if __name__ == "__main__":
    main()
