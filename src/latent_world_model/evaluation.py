"""Use lm-evaluation-harness task definitions and scorers without rewriting them."""
import argparse
import copy
from pathlib import Path
import time
from .io import canonical_hash, git_identity, read_json, sha256_file, within, write_json
from .environment import environment_identity


def native_tasks(sources_path, cache_dir, split_mode="published"):
    from lm_eval.tasks import TaskManager
    from lm_eval.api.task import ConfigurableTask
    if split_mode not in {"published", "development"}:
        raise ValueError(split_mode)
    sources = read_json(sources_path)
    manager = TaskManager()
    tasks = {}
    for name, spec in sources["benchmarks"].items():
        # Version-pinned internal API is source-inspected at lm-eval v0.4.8.
        config = copy.deepcopy(manager._get_config(name))
        config["dataset_path"] = spec["repo"]
        if config.get("dataset_name") != spec["config"]:
            raise ValueError(f"Native dataset config changed for {name}")
        config["dataset_kwargs"] = {**(config.get("dataset_kwargs") or {}),
                                    "revision": spec["revision"], "cache_dir": str(cache_dir)}
        if split_mode == "development":
            # ARC/WikiText validation is the published development split. HellaSwag
            # and PIQA already use validation: it can never later be fresh confirmation.
            config["test_split"] = None
            config["validation_split"] = spec["development_split"]
        selected = config.get("test_split") or config.get("validation_split")
        if selected != spec[f"{split_mode}_split"]:
            raise ValueError(f"Native selected split changed for {name}")
        tasks[name] = ConfigurableTask(config=config)
    return tasks


def retain_native_inventory(tasks, output, sources_path, split_mode, environment):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    source_hash = sha256_file(sources_path)
    sources = read_json(sources_path)
    inventory = {"format": "lwm-native-inventory-v2", "source_config_sha256": source_hash,
                 "split_mode": split_mode, "tasks": {},
                 "source": git_identity(Path(__file__).resolve().parents[2]),
                 "software": {key: environment[key] for key in ("python", "packages", "resolved_versions")}}
    if inventory["source"]["status"]:
        raise ValueError("Commit wrapper source before preparing or scoring native inputs")
    if set(tasks) != set(sources["evaluator"]["task_names"]):
        raise ValueError("Native task set differs from the full declared comparison")
    for name, task in tasks.items():
        documents = task.eval_docs
        rows = []
        for index, document in enumerate(documents):
            rows.append({"native_row_index": index, "native_id": document.get("id", document.get("ind")),
                         "doc_sha256": canonical_hash(document)})
        expected_counts = {"hellaswag": 10042, "piqa": 1838, "arc_easy": 2376 if split_mode == "published" else 570}
        if not rows or (name in expected_counts and len(rows) != expected_counts[name]):
            raise ValueError(f"Incomplete released split for {name}: {len(rows)}")
        write_json(output / f"{name}-samples.json", {"task": name, "scope": split_mode,
                   "denominator": len(rows), "source_config_sha256": source_hash, "samples": rows})
        inventory["tasks"][name] = {"denominator": len(rows), "sample_manifest": f"{name}-samples.json",
                           "dataset_source": sources["benchmarks"][name],
                           "selected_split": sources["benchmarks"][name][f"{split_mode}_split"],
                           "sample_manifest_sha256": sha256_file(output / f"{name}-samples.json"),
                           "dataset_fingerprints": {split: data._fingerprint for split, data in task.dataset.items()},
                           "download_checksums": {split: data.info.download_checksums
                                                  for split, data in task.dataset.items()}}
    write_json(output / "dataset-inventory.json", inventory)
    return inventory


def prepare_native(sources, cache, output, split_mode):
    output = Path(output)
    if output.exists() and any(output.iterdir()):
        raise ValueError("Preserve frozen native inputs; preparation output must be new")
    environment = environment_identity(read_json(sources)["evaluator"])
    tasks = native_tasks(sources, cache, split_mode)
    return retain_native_inventory(tasks, output, sources, split_mode, environment)


def compare_inventories(expected, actual):
    if canonical_hash(expected) != canonical_hash(actual):
        raise ValueError("Native inventory differs from the frozen acquisition contract; retain both attempts")


def validate_predictions(records, rows):
    if len(records) != len(rows):
        raise ValueError("Incomplete native prediction denominator")
    expected = {row["native_row_index"]: row["doc_sha256"] for row in rows}
    seen = set()
    for record in records:
        index = record["doc_id"]
        if index not in expected or index in seen or canonical_hash(record["doc"]) != expected[index]:
            raise ValueError("Prediction row identity differs from frozen native sample")
        seen.add(index)
    if seen != set(expected):
        raise ValueError("Missing native prediction row")


def evaluate(model_path, sources, cache, output, split_mode, seed, native_inventory, max_length=512):
    import torch
    from lm_eval import evaluator
    from lm_eval.models.huggingface import HFLM
    from transformers import AutoModelForCausalLM, AutoTokenizer
    output = Path(output).resolve()
    if output.exists() and any(output.iterdir()):
        raise ValueError("Evaluation output must be new; never overwrite prior predictions")
    output.mkdir(parents=True, exist_ok=True)
    native_inventory = Path(native_inventory).resolve()
    expected = read_json(native_inventory)
    expected_rows = {}
    for name, entry in expected["tasks"].items():
        path = within(native_inventory.parent, entry["sample_manifest"])
        if sha256_file(path) != entry["sample_manifest_sha256"]:
            raise ValueError(f"Frozen sample manifest changed for {name}")
        expected_rows[name] = read_json(path)["samples"]
    environment = environment_identity(read_json(sources)["evaluator"])
    tasks = native_tasks(sources, cache, split_mode)
    inventory = retain_native_inventory(tasks, output, sources, split_mode, environment)
    compare_inventories(expected, inventory)  # Before loading the model or performing inference.
    model_path = Path(model_path).resolve()
    if not (model_path / "model.safetensors").is_file() and not (model_path / "model.safetensors.index.json").is_file():
        raise ValueError("A complete local HF checkpoint is required; no implicit model download")
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(model_path, local_files_only=True,
                                                torch_dtype=torch.float16, attn_implementation="sdpa")
    if max_length > model.config.max_position_embeddings:
        raise ValueError("Requested context exceeds model maximum")
    model.to("cuda").eval()
    wrapped = HFLM(pretrained=model, tokenizer=tokenizer, batch_size=1, device="cuda",
                   max_length=max_length, add_bos_token=False)
    started = time.monotonic()
    torch.cuda.reset_peak_memory_stats()
    # No --limit, modified answer extraction, task averaging or replacement scorer.
    results = evaluator.simple_evaluate(model=wrapped, tasks=list(tasks.values()),
        num_fewshot=0, batch_size=1, device="cuda", limit=None, log_samples=True,
        bootstrap_iters=1000, random_seed=seed, numpy_random_seed=seed,
        torch_random_seed=seed, fewshot_random_seed=seed)
    from lm_eval.utils import handle_non_serializable
    import json
    samples = json.loads(json.dumps(results.pop("samples"), default=handle_non_serializable))
    for name, records in samples.items():
        if name not in tasks:
            raise ValueError(f"Unexpected native task {name}")
        write_json(output / f"{name}-predictions.json", records)
    if set(samples) != set(tasks) or set(results["results"]) != set(tasks):
        raise ValueError("Missing or unexpected native prediction/metric task")
    for name, records in samples.items():
        validate_predictions(records, expected_rows[name])
    # Native result configs contain source functions; upstream provides a JSON converter.
    serializable = json.loads(json.dumps(results, default=handle_non_serializable))
    write_json(output / "results.json", serializable)
    model_files = {str(p.relative_to(model_path)): sha256_file(p) for p in sorted(model_path.iterdir())
                   if p.is_file() and (p.suffix in {".safetensors", ".json", ".txt"})}
    write_json(output / "execution.json", {"model_files": model_files,
        "source": git_identity(Path(__file__).resolve().parents[2]), "environment": environment,
        "frozen_native_inventory_sha256": sha256_file(native_inventory),
        "sources_sha256": sha256_file(sources), "split_mode": split_mode,
        "seed": seed, "max_length": max_length, "num_fewshot": 0,
        "wall_seconds": time.monotonic() - started,
        "peak_allocated_bytes": torch.cuda.max_memory_allocated(),
        "scientific_result_verified": False,
        "qualification": "native harness run; independent official-scorer parity/E04 still required"})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["prepare", "run"])
    parser.add_argument("--sources", default="configs/sources.json")
    parser.add_argument("--cache", default="hf-cache")
    parser.add_argument("--output", required=True)
    parser.add_argument("--model")
    parser.add_argument("--native-inventory", help="Previously frozen dataset-inventory.json; required for run")
    parser.add_argument("--split-mode", choices=["published", "development"], default="published")
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--max-length", type=int, default=512)
    args = parser.parse_args()
    if args.action == "prepare":
        prepare_native(args.sources, args.cache, args.output, args.split_mode)
    elif not args.model or not args.native_inventory:
        parser.error("run requires --model and --native-inventory")
    else:
        evaluate(args.model, args.sources, args.cache, args.output, args.split_mode, args.seed,
                 args.native_inventory, args.max_length)


if __name__ == "__main__":
    main()
