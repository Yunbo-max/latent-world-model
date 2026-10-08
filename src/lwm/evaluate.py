"""Complete native bAbI/LAMBADA inference, authored but not executed.

Source status: generated_unexecuted. Runtime receipts are created only by an
actual invocation. Official scorer replay and model-adapter qualification are
separate: a local numerical preview never grants native parity.

Every bAbI question starts a fresh stream containing its complete prepared
facts/current-question context, exactly as in SFT. This is independent question
evaluation, not an assertion that the native teacher's incremental state path
has been qualified. No previous answer or question enters the context.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import importlib.metadata
import json
import math
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time
import traceback

from .scoring import (
    SOURCE_STATUS, aggregate_babi, aggregate_lambada, babi_exact_match,
    encode_hf_pair, lambada_context_target, load_dataset, replay_native,
    row_fingerprint, sha256_file, validate_predictions, write_json,
)


def _source_identity() -> dict:
    root = Path(__file__).resolve().parents[2]
    paths = sorted((root / "src" / "lwm").glob("*.py"))
    for relative in ("pyproject.toml", "research/DATA_PROTOCOL_PROPOSAL.md",
                     "research/FULL_MODEL_PROPOSAL.md", "configs/assets.json"):
        candidate = root / relative
        if candidate.is_file():
            paths.append(candidate)
    files = {str(path.relative_to(root)): sha256_file(path) for path in paths}
    git = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],
                         text=True, capture_output=True, check=False)
    return {"root": str(root), "git_head": git.stdout.strip() if git.returncode == 0 else None,
            "files_sha256": files, "files_fingerprint": row_fingerprint(files)}


def _runtime_versions() -> dict:
    versions = {"python": platform.python_version(), "platform": platform.platform()}
    for name in ("torch", "numpy", "transformers", "tokenizers", "huggingface-hub"):
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = None
    return versions


def _checkpoint_contract(checkpoint: dict, tokenizer: dict, task: str) -> None:
    required = {"model_config", "model_state", "config", "corpus_fingerprint",
                "corpus_provenance", "counters"}
    missing = required - checkpoint.keys()
    if missing:
        raise ValueError(f"Checkpoint lacks evaluation provenance fields: {sorted(missing)}")
    if any(not isinstance(checkpoint[name], dict) for name in
           ("model_config", "model_state", "config", "corpus_provenance", "counters")):
        raise ValueError("Checkpoint model/config/provenance/counters must be dictionaries")
    if not isinstance(checkpoint["corpus_fingerprint"], str) or not checkpoint["corpus_fingerprint"]:
        raise ValueError("Missing checkpoint corpus identity")
    if checkpoint["corpus_provenance"].get("tokenizer") != tokenizer:
        raise ValueError("Checkpoint/tokenizer byte identities differ")
    stage = checkpoint["config"].get("stage")
    if stage not in ("pretrain", "sft_babi"):
        raise ValueError("Checkpoint must explicitly identify pretrain or sft_babi stage")
    if task == "lambada" and stage != "pretrain":
        raise ValueError("Native zero-shot LAMBADA requires the pretraining checkpoint before bAbI adaptation")
    if checkpoint["model_config"].get("vocab_size") != tokenizer["vocab_size"]:
        raise ValueError("Checkpoint vocabulary differs from the verified tokenizer")


def _validate_trace(trace: list[dict], tokens: list[int], ll: float, greedy: bool) -> None:
    if len(trace) != len(tokens) or not math.isfinite(ll) or type(greedy) is not bool:
        raise ValueError("Incomplete or non-finite LAMBADA token-likelihood trace")
    for expected, item in zip(tokens, trace, strict=True):
        if item.get("token_id") != expected or type(item.get("argmax_token_id")) is not int:
            raise ValueError("LAMBADA trace target/argmax alignment differs")
        probability = item.get("log_probability")
        if type(probability) not in (int, float) or not math.isfinite(probability) or probability > 1e-7:
            raise ValueError("Invalid LAMBADA target token log probability")
    # Same ordered sum/boolean conjunction as score_continuation, no rounding.
    if sum(item["log_probability"] for item in trace) != ll:
        raise ValueError("LAMBADA example likelihood differs from its token trace")
    if all(item["argmax_token_id"] == item["token_id"] for item in trace) != greedy:
        raise ValueError("LAMBADA greedy flag differs from its token trace")


def _prediction(model, tokenizer, row: dict, task: str, max_new_tokens: int) -> dict:
    from .generation import generate, ingest, score_continuation, start_stream, stream_accounting

    model.reset_audit()

    base = {"id": row["id"], "task": task, "input_sha256": row_fingerprint(row),
            "context_truncated": False, "state_reset": True}
    tokenization_started = time.perf_counter()
    if task == "lambada":
        context, target = lambada_context_target(row["text"])
        pair = encode_hf_pair(tokenizer, context, target)
        base["tokenization_wall_seconds"] = time.perf_counter() - tokenization_started
        # Native text can literally encode token 50256. It is observed data,
        # never an artificial document boundary; -1 cannot be a vocabulary ID.
        state = ingest(model, start_stream(model), pair["context_token_ids"], eos_token_id=-1,
                       observation_id=f"lambada:{row['id']}:context")
        base["prompt_state_storage"] = stream_accounting(state)
        trace: list[dict] = []
        ll, greedy = score_continuation(model, state, pair["target_token_ids"],
                                        eos_token_id=-1, trace=trace)
        _validate_trace(trace, pair["target_token_ids"], ll, greedy)
        return {**base, **pair, "source_row": row["source_row"], "historical_access": model.audit.copy(),
                "log_likelihood": ll, "is_greedy": greedy, "token_trace": trace,
                "context_token_count": len(pair["context_token_ids"]),
                "target_token_count": len(pair["target_token_ids"]),
                "generation_truncated": False,
                "literal_eos_input_tokens": pair["context_token_ids"].count(tokenizer.eos_token_id),
                "literal_eos_target_tokens": pair["target_token_ids"].count(tokenizer.eos_token_id)}

    context = row["context"]
    tokens = list(tokenizer.encode(context, add_special_tokens=False,
                                   split_special_tokens=False, truncation=False))
    base["tokenization_wall_seconds"] = time.perf_counter() - tokenization_started
    if not tokens:
        raise ValueError(f"Empty native bAbI context: {row['id']}")
    state = ingest(model, start_stream(model), tokens, eos_token_id=-1,
                   observation_id=f"babi:{row['id']}:context")
    base["prompt_state_storage"] = stream_accounting(state)
    produced, branch = generate(model, state, max_new_tokens, tokenizer.eos_token_id,
                           temperature=0.0)
    base["output_state_storage"] = stream_accounting(branch)
    stopped = bool(produced and produced[-1] == tokenizer.eos_token_id)
    answer_tokens = produced[:-1] if stopped else produced
    prediction = tokenizer.decode(answer_tokens, skip_special_tokens=False,
                                  clean_up_tokenization_spaces=False)
    if not isinstance(prediction, str):
        # Keep the denominator; an invalid answer is scored as an empty error.
        prediction = ""
    return {**base, "historical_access": model.audit.copy(), "task_id": row["task_id"], "episode_id": row["episode_id"],
            "episode_turn": row["episode_turn"], "episode_done": row["episode_done"],
            "source_line": row.get("source_line"), "context": context,
            "context_token_ids": tokens, "context_token_count": len(tokens),
            "native_labels": row["native_labels"], "prediction": prediction,
            "prediction_token_ids": produced,
            "exact_match": babi_exact_match(prediction, row["native_labels"]),
            "stopped_on_eos": stopped, "generation_truncated": not stopped,
            "generated_token_count": len(produced),
            "literal_eos_input_tokens": tokens.count(tokenizer.eos_token_id)}


def run(args: argparse.Namespace) -> dict:
    """Execute only on explicit CLI invocation; never reuse an output directory."""
    import torch

    from .checkpoint import load_checkpoint
    from .model import LatentWorldModel, ModelConfig
    from .prepare import load_tokenizer, tokenizer_identity

    if args.loops is not None and args.loops <= 0:
        raise ValueError("--loops must be positive")
    if args.max_new_tokens <= 0:
        raise ValueError("--max-new-tokens must be positive")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    manifest = {"format": "lwm-evaluation-v1", "source_status": SOURCE_STATUS,
                "execution_status": "running", "started_at_utc": datetime.now(timezone.utc).isoformat(),
                "task": args.task, "split": args.split, "argv": sys.argv,
                "cwd": str(Path.cwd()), "runtime_versions": _runtime_versions()}
    predictions = []
    dataset = None
    current_id = None
    try:
        source = _source_identity()
        dataset = load_dataset(args.data, args.task, args.split)
        identity = tokenizer_identity(args.tokenizer)
        tokenizer = load_tokenizer(args.tokenizer)
        declared_tokenizer = dataset.manifest.get("tokenizer")
        if declared_tokenizer is not None and declared_tokenizer != identity:
            raise ValueError("Prepared native data and evaluation tokenizer identities differ")
        checkpoint_path = args.checkpoint.resolve()
        checkpoint_sha = sha256_file(checkpoint_path)
        checkpoint = load_checkpoint(checkpoint_path, map_location="cpu")
        _checkpoint_contract(checkpoint, identity, args.task)
        training_config = checkpoint["config"]
        original_model_config = ModelConfig(**checkpoint["model_config"]).to_dict()
        evaluation_model_config = dict(original_model_config)
        if args.loops is not None:
            evaluation_model_config["loop_steps"] = args.loops
        if args.memory_reset:
            evaluation_model_config["memory_enabled"] = False
        evaluation_model_config["checkpoint_layers"] = False
        model_config = ModelConfig(**evaluation_model_config)
        device = torch.device(args.device)
        if device.type not in ("cpu", "cuda"):
            raise ValueError("This evaluation adapter supports explicit cpu or cuda devices")
        if device.type == "cuda" and not torch.cuda.is_available():
            raise RuntimeError("Requested CUDA is unavailable; evaluation will not fall back to CPU")
        model = LatentWorldModel(model_config)
        model.load_state_dict(checkpoint["model_state"], strict=True)
        # Peak includes the actual model placement and all inference work.
        if device.type == "cuda":
            torch.cuda.synchronize(device)
            torch.cuda.reset_peak_memory_stats(device)
        model = model.to(device).eval()
        manifest.update({
            "source": source, "checkpoint": {"path": str(checkpoint_path), "sha256": checkpoint_sha,
                "bytes": checkpoint_path.stat().st_size, "model_config": original_model_config,
                "config": training_config, "config_sha256": row_fingerprint(training_config),
                "status": checkpoint.get("status"),
                "completed_target_budget": checkpoint.get("status") == "completed_target_budget"
                    and checkpoint["counters"].get("seen_targets") == training_config.get("training", {}).get("token_budget"),
                "corpus_fingerprint": checkpoint["corpus_fingerprint"],
                "corpus_provenance": checkpoint["corpus_provenance"], "counters": checkpoint["counters"],
                "training_status": checkpoint.get("status"), "source_identity": checkpoint.get("source_identity"),
                "initial_checkpoint": checkpoint.get("initial_checkpoint")},
            "tokenizer": identity, "tokenizer_sha256": row_fingerprint(identity),
            "data_path": str(dataset.path), "data_sha256": dataset.sha256,
            "data_preparation": dataset.manifest,
            "data_preparation_sha256": sha256_file(dataset.manifest_path) if dataset.manifest_path else None,
            "examples": len(dataset.rows), "effective_model_config": model_config.to_dict(),
            "parameters": sum(parameter.numel() for parameter in model.parameters()),
            "settings": {"loops_override": args.loops, "memory_reset": args.memory_reset,
                         "max_new_tokens": args.max_new_tokens if args.task == "babi" else None,
                         "temperature": 0.0, "num_fewshot": 0, "batch_size": 1,
                         "dtype": str(next(model.parameters()).dtype), "device": str(device),
                         "prefix_vocabulary_projection": "last_position_only_after_full_coda",
                         "kv_cache": False,
                         "float32_matmul_precision": torch.get_float32_matmul_precision(),
                         "cuda_matmul_allow_tf32": torch.backends.cuda.matmul.allow_tf32,
                         "deterministic_algorithms": torch.are_deterministic_algorithms_enabled(),
                         "context_truncation": "none; stream all tokens across model segments",
                         "input_eos_policy": "literal native token is data; reset disabled with sentinel -1",
                         "state_policy": "fresh stream per complete prepared question" if args.task == "babi" else "fresh stream per native passage",
                         "babi_answer_policy": "greedy until EOS or fixed cap; no answer extraction",
                         "sft_answer_prefix": " "},
        })
        if device.type == "cuda":
            manifest["device"] = {"name": torch.cuda.get_device_name(device),
                                  "total_memory_bytes": torch.cuda.get_device_properties(device).total_memory,
                                  "cuda_runtime": torch.version.cuda}
            torch.cuda.synchronize(device)
        inference_started = time.perf_counter()
        setup_seconds = inference_started - started
        predictions_path = output / "predictions.jsonl"
        with predictions_path.open("x", encoding="utf-8") as stream, torch.inference_mode():
            for row in dataset.rows:
                current_id = row["id"]
                if device.type == "cuda":
                    torch.cuda.synchronize(device)
                example_started = time.perf_counter()
                prediction = _prediction(model, tokenizer, row, args.task, args.max_new_tokens)
                if device.type == "cuda":
                    torch.cuda.synchronize(device)
                prediction["wall_seconds"] = time.perf_counter() - example_started
                stream.write(json.dumps(prediction, ensure_ascii=False, allow_nan=False) + "\n")
                stream.flush()
                predictions.append(prediction)
                current_id = None
        if device.type == "cuda":
            torch.cuda.synchronize(device)
        inference_seconds = time.perf_counter() - inference_started
        ordered = validate_predictions(dataset.rows, predictions, args.task)
        metrics = aggregate_babi(ordered) if args.task == "babi" else aggregate_lambada(ordered)
        if metrics["examples"] != len(dataset.rows):
            raise ValueError("Scoring changed the complete native denominator")
        qualification = {"native_aggregation_replay": "pending_local", "model_adapter_parity": "pending_local",
                         "native_teacher_serialization_parity": "pending_local" if args.task == "babi" else "not_applicable",
                         "scientific_gate": "not_assessed"}
        metric_origin = "local_native_formula_preview"
        if args.native_source is not None:
            replay = replay_native(dataset, ordered, args.native_source)
            write_json(output / "native-replay.json", replay)
            metrics = replay["metrics"]
            qualification["native_aggregation_replay"] = replay["native_aggregation_replay"]
            metric_origin = "pinned_official_scorer_replay"
        # A concurrently replaced latest.pt, data file, tokenizer, or source is
        # not an immutable result identity. Fail rather than publish a receipt.
        if sha256_file(checkpoint_path) != checkpoint_sha or sha256_file(dataset.path) != dataset.sha256:
            raise ValueError("Checkpoint or dataset changed during evaluation")
        if tokenizer_identity(args.tokenizer) != identity or _source_identity() != source:
            raise ValueError("Tokenizer or implementation changed during evaluation")
        if dataset.manifest_path and sha256_file(dataset.manifest_path) != manifest["data_preparation_sha256"]:
            raise ValueError("Data preparation manifest changed during evaluation")
        metrics["metric_origin"] = metric_origin
        write_json(output / "metrics.json", metrics)
        usage = {"inference_wall_seconds": inference_seconds,
                 "inference_timing_scope": "complete row loop, including tokenization, synchronization and prediction serialization",
                 "setup_wall_seconds": setup_seconds,
                 "tokenization_wall_seconds": sum(row["tokenization_wall_seconds"] for row in ordered),
                 "warmup_policy": "no separate warmup; first example included and reported separately",
                 "first_example_wall_seconds": ordered[0]["wall_seconds"],
                 "total_wall_seconds": time.perf_counter() - started,
                 "context_tokens": sum(row["context_token_count"] for row in ordered),
                 "scored_target_tokens": sum(row.get("target_token_count", 0) for row in ordered),
                 "generated_tokens": sum(row.get("generated_token_count", 0) for row in ordered),
                 "max_context_tokens": max(row["context_token_count"] for row in ordered),
                 "max_context_plus_target_tokens": max(row["context_token_count"] + row.get("target_token_count", 0) for row in ordered),
                 "context_truncations": sum(row["context_truncated"] for row in ordered),
                 "generation_truncations": sum(row["generation_truncated"] for row in ordered),
                 "examples_per_second": len(ordered) / inference_seconds,
                 "gpu_peak_allocated_bytes": torch.cuda.max_memory_allocated(device) if device.type == "cuda" else None,
                 "gpu_peak_reserved_bytes": torch.cuda.max_memory_reserved(device) if device.type == "cuda" else None,
                 "cpu_process_peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
                 "historical_raw_tokens_read": sum(row.get("historical_access", {}).get("raw_tokens_read", 0) for row in ordered),
                 "historical_index_tokens_scanned": sum(row.get("historical_access", {}).get("index_tokens_scanned", 0) for row in ordered),
                 "retrieval_cpu_seconds": sum(row.get("historical_access", {}).get("retrieval_cpu_seconds", 0.0) for row in ordered),
                 "retrieval_timing_scope": "prefix D2H, lexical index/selection, CPU packing; GPU H2D/embedding/attention and receipts are in total inference wall time",
                 "gpu_memory_status": "measured_in_process" if device.type == "cuda" else "not_applicable_cpu"}
        manifest.update({"execution_status": "completed", "completed_at_utc": datetime.now(timezone.utc).isoformat(),
                         "predictions_sha256": sha256_file(predictions_path),
                         "metrics_sha256": sha256_file(output / "metrics.json"),
                         "qualification": qualification, "measurements": usage,
                         "examples_excluded": 0, "prediction_ids_verified": True})
        write_json(output / "manifest.json", manifest)
        return manifest
    except BaseException as error:
        manifest.update({"execution_status": "failed", "examples_completed": len(predictions),
                         "failed_current_id": current_id,
                         "unscored_ids": [row["id"] for row in dataset.rows[len(predictions):]] if dataset else None,
                         "inventory_scope": "remaining IDs in native order; null when native dataset loading failed",
                         "total_wall_seconds": time.perf_counter() - started,
                         "error_type": type(error).__name__, "error": str(error),
                         "qualification": {"native_aggregation_replay": "not_qualified",
                                           "model_adapter_parity": "pending_local"}})
        if not (output / "manifest.json").exists():
            write_json(output / "manifest.json", manifest)
        (output / "failure.txt").write_text(traceback.format_exc(), encoding="utf-8")
        raise


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", required=True, type=Path)
    parser.add_argument("--tokenizer", required=True, type=Path)
    parser.add_argument("--task", required=True, choices=("babi", "lambada"))
    parser.add_argument("--data", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--loops", type=int)
    parser.add_argument("--memory-reset", action="store_true")
    parser.add_argument("--split", default="test", choices=("valid", "test"))
    parser.add_argument("--max-new-tokens", type=int, default=32)
    parser.add_argument("--native-source", type=Path,
                        help="Pinned ParlAI/harness checkout to actually replay official scoring")
    result = run(parser.parse_args(argv))
    print(json.dumps({"execution_status": result["execution_status"], "task": result["task"],
                      "examples": result["examples"], "qualification": result["qualification"]},
                     sort_keys=True))


if __name__ == "__main__":
    main()

