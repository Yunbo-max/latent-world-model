"""Single-device, document-preserving TBPTT with exact target accounting.

This module is authored but has not been executed by Web. See Local runbook.
"""
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import random
import resource
import signal
import socket
import time

import numpy as np
import torch
from torch.nn import functional as F

from .checkpoint import capture_rng, restore_rng, save_checkpoint, load_checkpoint
from .data import TokenCorpus, CorpusCursor, canonical_hash, file_sha256
from .model import ModelConfig, LatentWorldModel
from .episodic import EpisodicStore


def new_history(model, document_id):
    return {"segments": 0, "document_id": document_id,
            "store": EpisodicStore(model.config.episodic_capacity_tokens, document_id)
                if model.config.episodic_enabled else None}


def history_payload(history):
    if history is None:
        return None
    return {"segments": history["segments"], "document_id": history["document_id"],
            "store": history["store"].state_dict() if history["store"] is not None else None}


def restore_history(model, payload):
    if payload is None:
        return None
    history = new_history(model, payload["document_id"])
    if type(payload["segments"]) is not int or payload["segments"] < 0:
        raise ValueError("Invalid training segment clock")
    history["segments"] = payload["segments"]
    if bool(payload["store"] is not None) != model.config.episodic_enabled:
        raise ValueError("Training store/model mismatch")
    if payload["store"] is not None:
        history["store"] = EpisodicStore.from_state_dict(payload["store"],
            vocab_size=model.config.vocab_size, event_length=model.config.block_size)
        if (history["store"].document_id != history["document_id"] or
                history["store"].capacity_tokens != model.config.episodic_capacity_tokens or
                history["store"].next_ordinal != history["segments"]):
            raise ValueError("Training history identity/config differs")
    return history


def window_objective(model, ids, loss_mask, memory, *, history=None,
                     state_prediction_weight=0.0, diagnostics=None):
    """Sum eligible NLLs; preserve writer graphs within this complete window."""
    total_loss, target_count = None, 0
    if not math.isfinite(state_prediction_weight) or state_prediction_weight < 0:
        raise ValueError("Nonnegative finite state prediction weight required")
    if state_prediction_weight and not model.config.predictive_head:
        raise ValueError("State prediction loss requires the normalized predictive head")
    if model.config.episodic_enabled and history is None:
        raise ValueError("Exact-memory training requires explicit persistent history")
    if diagnostics is None:
        diagnostics = {}
    diagnostics.update(main_ce_sum=0.0, state_ce_sum=0.0, state_pairs=0)
    for start in range(0, ids.numel(), model.config.block_size):
        segment = ids[start:start + model.config.block_size]
        mask = loss_mask[start:start + model.config.block_size]
        # This memory is the previous complete segment's post-write state.
        # The genuine next token enters ONLY this CE, never writer/retrieval.
        auxiliary = None
        if (state_prediction_weight and history is not None and history["segments"] > 0
                and bool(mask[0])):
            auxiliary = F.cross_entropy(model.predict_future(memory).float(), segment[:1], reduction="sum")
        store = history["store"] if history is not None else None
        if store is not None and segment.numel() == model.config.block_size:
            raw = segment.detach().cpu().tolist()
            store.check(store.next_ordinal, raw, ("observed_text",) * len(raw))
        logits, memory = model.forward_segment(segment[None], memory, episodic=store)
        count = int(mask.sum().item())
        if count:
            loss = F.cross_entropy(logits[0, mask].float(), segment[mask], reduction="sum")
            total_loss = loss if total_loss is None else total_loss + loss
            diagnostics["main_ce_sum"] += float(loss.detach().item())
            target_count += count
        if auxiliary is not None:
            total_loss = total_loss + state_prediction_weight * auxiliary
            diagnostics["state_ce_sum"] += float(auxiliary.detach().item())
            diagnostics["state_pairs"] += 1
        if history is not None and segment.numel() == model.config.block_size:
            if store is not None:
                raw = segment.detach().cpu().tolist()
                history["store"] = store.append(store.next_ordinal, raw, ("observed_text",) * len(raw))
            history["segments"] += 1
    return total_loss, memory, target_count


@torch.no_grad()
def validation_nll(model, corpus, device, max_targets, state_prediction_weight=0.0):
    model.eval()
    training_audit = model.audit.copy()
    model.reset_audit()
    cursor = CorpusCursor(corpus, seed=0, shuffle=False)
    memory, nll, targets, history = None, 0.0, 0, None
    state_ce_sum, state_pairs = 0.0, 0
    while not cursor.exhausted and targets < max_targets:
        window = cursor.take_window(model.config.block_size * 4, max_targets=max_targets - targets)
        if window.reset_before:
            memory = model.initial_memory(1)
            history = new_history(model, f"validation:{window.epoch}:{window.document_id}")
        ids = torch.tensor(window.ids, dtype=torch.long, device=device)
        mask = torch.tensor(window.loss_mask, dtype=torch.bool, device=device)
        stats = {}
        loss, memory, count = window_objective(model, ids, mask, memory, history=history,
            state_prediction_weight=state_prediction_weight, diagnostics=stats)
        state_ce_sum += stats["state_ce_sum"]
        state_pairs += stats["state_pairs"]
        if loss is not None:
            # Main NLL remains directly comparable to beta=0/v0. The head's
            # held-out proper CE is a separate diagnostic, never text NLL.
            nll += stats["main_ce_sum"]
            targets += count
        if window.ended_document:
            memory = None
            history = None
    validation_audit = model.audit.copy()
    model.audit = training_audit
    model.train()
    if not targets:
        raise ValueError("Validation corpus contains no eligible targets")
    mean = nll / targets
    try:
        perplexity = math.exp(mean)
    except OverflowError:
        perplexity = None
    return {"nll_per_target": mean, "perplexity_per_token": perplexity,
            "perplexity_overflow": perplexity is None,
            "targets": targets, "corpus_fingerprint": corpus.fingerprint,
            "state_ce_sum": state_ce_sum, "state_pairs": state_pairs,
            "state_ce_per_pair": state_ce_sum / state_pairs if state_pairs else None,
            "state_prediction_weight": state_prediction_weight,
            "objective_per_main_target": (nll + state_prediction_weight * state_ce_sum) / targets,
            "historical_access": validation_audit,
            "scope": "development likelihood; not a benchmark or confirmation result"}


def learning_rate(training, consumed):
    base = float(training["learning_rate"])
    warmup = int(training["warmup_tokens"])
    budget = int(training["token_budget"])
    if warmup and consumed < warmup:
        return base * max(1, consumed) / warmup
    progress = min(1.0, max(0.0, (consumed - warmup) / max(1, budget - warmup)))
    floor = float(training["min_lr_ratio"])
    return base * (floor + (1 - floor) * 0.5 * (1 + math.cos(math.pi * progress)))


def source_identity():
    identity = {path.name: file_sha256(path) for path in sorted(Path(__file__).parent.glob("*.py"))}
    identity["torch_runtime"] = str(torch.__version__)
    identity["numpy_runtime"] = str(np.__version__)
    identity["cuda_runtime"] = str(torch.version.cuda)
    identity["pyproject.toml"] = file_sha256(Path(__file__).resolve().parents[2] / "pyproject.toml")
    return identity


def clip_gradient_norm(parameters, maximum):
    """Measure in FP64 so finite FP32 gradients cannot overflow the norm.

    Leave nonfinite gradients intact: GradScaler has already recorded them
    during unscale and must skip that step. The FP32 caller instead fails.
    """
    gradients = [p.grad for p in parameters if p.grad is not None]
    if not gradients:
        raise RuntimeError("Optimizer boundary has no gradients")
    norm = torch.linalg.vector_norm(torch.stack([
        torch.linalg.vector_norm(gradient.double()) for gradient in gradients]))
    if bool(torch.isfinite(norm)):
        factor = (float(maximum) / (norm + 1e-6)).clamp(max=1.0)
        for gradient in gradients:
            gradient.mul_(factor.to(dtype=gradient.dtype, device=gradient.device))
    return norm


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--data", required=True, help="Prepared TokenCorpus directory")
    parser.add_argument("--validation", help="Prepared held-out TokenCorpus directory")
    parser.add_argument("--output", required=True)
    parser.add_argument("--resume")
    parser.add_argument("--init-checkpoint", help="Weights-only start for separately budgeted SFT")
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--max-updates", type=int, help="Finite feasibility run; never a completed training claim")
    args = parser.parse_args(argv)
    if args.max_updates is not None and args.max_updates <= 0:
        parser.error("--max-updates must be positive")
    if args.resume and args.init_checkpoint:
        parser.error("Choose resume or weights-only initialization")
    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    training = config["training"]
    model_config = ModelConfig(**config["model"])
    state_weight = float(training.get("state_prediction_weight", 0.0))
    if not math.isfinite(state_weight) or state_weight < 0 or (state_weight and not model_config.predictive_head):
        raise ValueError("Invalid compressed-state objective configuration")
    if training["unroll_segments"] < 2:
        raise ValueError("The independent writer requires unroll_segments >= 2")
    if training["token_budget"] <= 0 or training["accumulate_targets"] <= 0:
        raise ValueError("Positive token and accumulation budgets required")
    if not 0 < training["max_run_seconds"] <= 86400:
        raise ValueError("Each Local invocation must have a finite limit <=24 hours")
    if training["precision"] not in ("float32", "float16"):
        raise ValueError("v0 supports float32 or CUDA float16; no implicit BF16 requirement")
    device = torch.device(args.device)
    if device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable; perform Local environment acceptance")
    if device.type != "cuda" and training["precision"] == "float16":
        raise ValueError("FP16 profile requires CUDA")
    random.seed(training["seed"])
    np.random.seed(training["seed"])
    torch.manual_seed(training["seed"])
    if device.type == "cuda":
        torch.cuda.manual_seed_all(training["seed"])
        torch.backends.cuda.matmul.allow_tf32 = False
        torch.cuda.reset_peak_memory_stats(device)
    corpus = TokenCorpus(args.data)
    validation = TokenCorpus(args.validation) if args.validation else None
    if not training["repeat"] and training["token_budget"] > corpus.manifest["targets"]:
        raise ValueError("Token budget exceeds unique eligible targets; explicit repeat policy required")
    model = LatentWorldModel(model_config).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=training["learning_rate"],
        betas=(0.9, 0.95), weight_decay=training["weight_decay"], foreach=False)
    scaler = torch.amp.GradScaler("cuda", enabled=training["precision"] == "float16")
    cursor = CorpusCursor(corpus, seed=training["seed"], shuffle=training["shuffle"],
                          repeat=training["repeat"])
    counters = {"seen_targets": 0, "optimized_targets": 0, "input_tokens": 0,
                "updates": 0, "skipped_updates": 0, "cumulative_seconds": 0.0,
                "auxiliary_target_observations": 0}
    memory, history = None, None
    identity = source_identity()
    identity["execution_device_type"] = device.type
    identity["execution_gpu_name"] = torch.cuda.get_device_name(device) if device.type == "cuda" else None
    identity["execution_gpu_capability"] = list(torch.cuda.get_device_capability(device)) if device.type == "cuda" else None
    initialization = None
    resume_identity = None
    if args.init_checkpoint:
        initial = load_checkpoint(args.init_checkpoint)
        # Initialization across data domains must preserve the architecture.
        if ModelConfig(**initial["model_config"]).to_dict() != model_config.to_dict():
            raise ValueError("Initialization architecture differs from target configuration")
        model.load_state_dict(initial["model_state"], strict=True)
        initialization = {"path": str(Path(args.init_checkpoint).resolve()),
                          "sha256": file_sha256(Path(args.init_checkpoint))}
    if args.resume:
        resume_identity = {"path": str(Path(args.resume).resolve()),
                           "sha256": file_sha256(Path(args.resume))}
        state = load_checkpoint(args.resume)
        if file_sha256(Path(args.resume)) != resume_identity["sha256"]:
            raise ValueError("Resume checkpoint changed while loading")
        if (state["config"] != config or state["corpus_fingerprint"] != corpus.fingerprint
                or state["source_identity"] != identity):
            raise ValueError("Resume config, corpus or source differs; create a reviewed child run")
        model.load_state_dict(state["model_state"], strict=True)
        optimizer.load_state_dict(state["optimizer_state"])
        scaler.load_state_dict(state["scaler_state"])
        cursor.load_state_dict(state["cursor"])
        counters = state["counters"]
        counters.setdefault("auxiliary_target_observations", 0)
        if counters["seen_targets"] >= training["token_budget"]:
            raise ValueError("Checkpoint already completed its target budget; use evaluation or a child run")
        initialization = state.get("initial_checkpoint")
        memory = state["memory"].to(device) if state["memory"] is not None else None
        history = restore_history(model, state.get("history"))
        if memory is not None and history is None:
            if model.config.episodic_enabled or state_weight:
                raise ValueError("Expanded-state checkpoint lacks its historical ledger")
            history = new_history(model, "legacy-v0-continuation")
        restore_rng(state["rng"])
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    lock = output / "run.lock"
    try:
        descriptor = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as error:
        raise RuntimeError("Output is locked; reconcile host/PID before removing any stale lock") from error
    log = None
    prior_handlers = {}
    try:
        with os.fdopen(descriptor, "w") as stream:
            json.dump({"pid": os.getpid(), "host": socket.gethostname(), "started": time.time()}, stream)
        latest = output / "last.pt"
        has_history = any((output / name).exists() for name in ("events.jsonl", "status.json"))
        if not args.resume and (latest.exists() or has_history):
            raise FileExistsError("Existing run: explicitly resume or choose a new output directory")
        if args.resume:
            if file_sha256(Path(args.resume)) != resume_identity["sha256"]:
                raise ValueError("Resume checkpoint changed before acquiring the output lock")
            if latest.exists() and file_sha256(latest) != resume_identity["sha256"]:
                raise ValueError("Output contains a different checkpoint; use its latest checkpoint or a new child directory")
            if not latest.exists() and has_history:
                raise ValueError("Output has history but no checkpoint; preserve it and choose a new child directory")
        started = time.monotonic()
        prior_seconds = counters["cumulative_seconds"]
        start_updates = counters["updates"]
        stop_requested = False
        def request_stop(signum, frame):
            nonlocal stop_requested
            stop_requested = True
        for sig in (signal.SIGINT, signal.SIGTERM):
            prior_handlers[sig] = signal.signal(sig, request_stop)
        log = (output / "events.jsonl").open("a", encoding="utf-8")
        def event(kind, **values):
            log.write(json.dumps({"event": kind, "time": time.time(), **values}, allow_nan=False) + "\n")
            log.flush()
        def persist(status):
            counters["cumulative_seconds"] = prior_seconds + time.monotonic() - started
            payload = {"model_config": model_config.to_dict(), "model_state": model.state_dict(),
                       "config": config, "corpus_fingerprint": corpus.fingerprint,
                       "corpus_provenance": corpus.manifest["provenance"],
                       "optimizer_state": optimizer.state_dict(), "scaler_state": scaler.state_dict(),
                       "cursor": cursor.state_dict(), "memory": memory.detach().cpu() if memory is not None else None,
                       "history": history_payload(history),
                       "rng": capture_rng(), "counters": counters.copy(), "source_identity": identity,
                       "status": status, "initial_checkpoint": initialization,
                       "resumed_from": resume_identity}
            save_checkpoint(output / "last.pt", payload)
            (output / "status.json").write_text(json.dumps({"status": status, **counters,
                "target_budget": training["token_budget"], "config_hash": canonical_hash(config)}, indent=2) + "\n")
        accumulated = 0
        loss_sum = 0.0
        objective_stats = {"main_ce_sum": 0.0, "state_ce_sum": 0.0, "state_pairs": 0}
        attempted_window = None
        model.train()
        optimizer.zero_grad(set_to_none=True)
        event("start", config=config, source_identity=identity, corpus=corpus.fingerprint,
              parameters=sum(p.numel() for p in model.parameters()), device=str(device),
              gpu=torch.cuda.get_device_name(device) if device.type == "cuda" else None,
              gpu_total_memory_bytes=torch.cuda.get_device_properties(device).total_memory if device.type == "cuda" else None,
              gpu_capability=list(torch.cuda.get_device_capability(device)) if device.type == "cuda" else None,
              resumed=bool(args.resume), generated_source_status="Local execution begun")
        model.reset_audit()
        try:
            while counters["seen_targets"] < training["token_budget"]:
                if cursor.exhausted:
                    raise RuntimeError("Corpus exhausted before target budget; no implicit epoch repetition")
                cursor_before = cursor.state_dict()
                attempted_window = None
                window = cursor.take_window(model_config.block_size * training["unroll_segments"],
                    max_targets=training["token_budget"] - counters["seen_targets"])
                attempted_window = {"cursor_before": cursor_before,
                    "document_id": window.document_id, "epoch": window.epoch,
                    "input_tokens": len(window.ids), "eligible_targets": int(window.loss_mask.sum()),
                    "forward_completed": False, "backward_completed": False,
                    "included_in_counters": False}
                if window.reset_before:
                    memory = model.initial_memory(1)
                    history = new_history(model, f"train:{window.epoch}:{window.document_id}")
                if memory is None:
                    raise RuntimeError("Cursor/memory state inconsistent at a continuation window")
                ids = torch.tensor(window.ids, dtype=torch.long, device=device)
                mask = torch.tensor(window.loss_mask, dtype=torch.bool, device=device)
                with torch.autocast(device_type=device.type, dtype=torch.float16,
                                    enabled=training["precision"] == "float16"):
                    window_stats = {}
                    loss, next_memory, count = window_objective(model, ids, mask, memory,
                        history=history, state_prediction_weight=state_weight, diagnostics=window_stats)
                for key in objective_stats:
                    objective_stats[key] += window_stats[key]
                attempted_window["forward_completed"] = True
                if loss is not None:
                    if not bool(torch.isfinite(loss)):
                        raise FloatingPointError("Nonfinite loss; retain log and last accepted checkpoint")
                    scaler.scale(loss / training["accumulate_targets"]).backward()
                    attempted_window["backward_completed"] = True
                    loss_sum += float(loss.detach().item())
                    accumulated += count
                # Exactly the explicit TBPTT boundary, never an inner segment boundary.
                memory = None if window.ended_document else next_memory.detach()
                if window.ended_document:
                    history = None
                counters["seen_targets"] += count
                counters["input_tokens"] += len(window.ids)
                counters["auxiliary_target_observations"] += window_stats["state_pairs"]
                attempted_window["included_in_counters"] = True
                final_budget = counters["seen_targets"] == training["token_budget"]
                time_limit = time.monotonic() - started >= training["max_run_seconds"]
                # A stop request must not create a different AdamW grouping.
                # Finish the normal accumulation boundary; the deadline is soft.
                should_step = accumulated >= training["accumulate_targets"] or final_budget
                if should_step and accumulated:
                    correction = training["accumulate_targets"] / accumulated
                    for parameter in model.parameters():
                        if parameter.grad is not None:
                            parameter.grad.mul_(correction)
                    # Correct while still scaled, so AMP also detects overflow
                    # introduced by the last partial accumulation's correction.
                    scaler.unscale_(optimizer)
                    norm = clip_gradient_norm(model.parameters(), training["clip_grad_norm"])
                    old_scale = scaler.get_scale()
                    if not bool(torch.isfinite(norm)) and not scaler.is_enabled():
                        raise FloatingPointError("Nonfinite FP32 gradients")
                    lr = learning_rate(training, counters["seen_targets"])
                    for group in optimizer.param_groups:
                        group["lr"] = lr
                    scaler.step(optimizer)
                    scaler.update()
                    skipped = scaler.get_scale() < old_scale
                    counters["updates"] += 1
                    counters["skipped_updates"] += int(skipped)
                    if not skipped:
                        counters["optimized_targets"] += accumulated
                    gradient_parameters = [p for p in model.parameters() if p.grad is not None]
                    gradient_tensor_count = len(gradient_parameters)
                    gradient_element_count = sum(p.numel() for p in gradient_parameters)
                    optimizer.zero_grad(set_to_none=True)
                    event("update", **counters, targets_this_update=accumulated,
                          nll=objective_stats["main_ce_sum"] / accumulated,
                          objective_per_main_target=loss_sum / accumulated,
                          state_prediction_weight=state_weight, **objective_stats,
                          parameters_with_gradient_tensor=gradient_element_count,
                          parameter_tensors_with_gradient=gradient_tensor_count,
                          gradient_inventory_scope="grad is present before zero_grad; not nonzero-gradient count or effective-capacity proof",
                          historical_access=model.audit.copy(),
                          historical_access_scope="cumulative within this invocation; excludes separately recorded validation; do not sum snapshots",
                          cpu_process_peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
                          gradient_norm=float(norm) if bool(torch.isfinite(norm)) else None,
                          lr=lr, scale=scaler.get_scale(), skipped=skipped,
                          elapsed_seconds=time.monotonic() - started,
                          peak_memory_bytes=torch.cuda.max_memory_allocated(device) if device.type == "cuda" else 0,
                          peak_reserved_memory_bytes=torch.cuda.max_memory_reserved(device) if device.type == "cuda" else 0)
                    accumulated, loss_sum = 0, 0.0
                    objective_stats = {"main_ce_sum": 0.0, "state_ce_sum": 0.0, "state_pairs": 0}
                    if counters["skipped_updates"] > training["max_skipped_updates"]:
                        persist("numerical_failure")
                        raise FloatingPointError("Skipped-update allowance exceeded; review precision/LR")
                    if counters["updates"] % training["checkpoint_every_updates"] == 0:
                        persist("running")
                    if validation and counters["updates"] % training["validation_every_updates"] == 0:
                        event("validation", **validation_nll(model, validation, device,
                                                             training["validation_targets"], state_weight))
                max_updates = args.max_updates is not None and counters["updates"] - start_updates >= args.max_updates
                if final_budget or ((stop_requested or time_limit or max_updates) and accumulated == 0):
                    status = "completed_target_budget" if final_budget else "paused"
                    persist(status)
                    event("stop", status=status, **counters)
                    print(json.dumps({"status": status, "checkpoint": str(output / "last.pt"), **counters}))
                    break
        except BaseException as error:
            event("failure", error_type=type(error).__name__, message=str(error),
                  counters=counters, accumulated_targets=accumulated,
                  accumulated_nll=loss_sum, attempted_window=attempted_window,
                  elapsed_seconds=time.monotonic() - started,
                  exposure_note="Counters cover completed windows; an incomplete attempted window is an upper bound, not claimed fully executed exposure. Hard kills require the external attempt ledger.",
                  checkpoint_policy="Resume last persisted optimizer boundary; preserve failed work logs")
            raise
    finally:
        try:
            if log is not None:
                log.close()
        finally:
            try:
                for sig, handler in prior_handlers.items():
                    signal.signal(sig, handler)
            finally:
                lock.unlink(missing_ok=True)


if __name__ == "__main__":
    main()

