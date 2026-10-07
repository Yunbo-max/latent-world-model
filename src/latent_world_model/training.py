"""Single-GPU baseline trainer with token accounting and resumable state.

No model architecture is reimplemented here: the forward pass is Transformers'
released LlamaForCausalLM. Generated on Web; runtime acceptance is pending.
"""
import argparse
import fcntl
import math
import os
from pathlib import Path
import random
import signal
import time
import uuid
import numpy as np
from .config import load_train_config, validate_train_config
from .data import TokenBlocks, batch_at, validate_corpus
from .io import (append_jsonl, canonical_hash, fsync_directory, git_identity,
                 read_json, resolve_checkpoint, sha256_file, within, write_json)
from .environment import environment_identity


def learning_rate(tokens, total, peak, warmup_fraction, min_ratio):
    warmup = max(1, round(total * warmup_fraction))
    if tokens < warmup:
        return peak * (tokens + 1) / warmup
    fraction = min(1.0, max(0.0, (tokens - warmup) / max(1, total - warmup)))
    return peak * (min_ratio + (1 - min_ratio) * 0.5 * (1 + math.cos(math.pi * fraction)))


def schedule_group(offset, length, micro_batch, accumulation):
    group = []
    for _ in range(accumulation):
        if offset >= length:
            break
        count = min(micro_batch, length - offset)
        group.append((offset, count))
        offset += count
    return group


def initialize_model(config, assets_dir, root):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, LlamaConfig, LlamaForCausalLM
    assets_dir = Path(assets_dir)
    tokenizer = AutoTokenizer.from_pretrained(assets_dir / "smollm2", local_files_only=True)
    if config["model"]["initialization"] == "scratch":
        model_config = LlamaConfig(**read_json(Path(root) / config["model"]["config"]))
        model_config._attn_implementation = "sdpa"
        model = LlamaForCausalLM(model_config)
    else:
        model = AutoModelForCausalLM.from_pretrained(assets_dir / "smollm2", local_files_only=True,
                                                    torch_dtype=torch.float32, attn_implementation="sdpa")
    if model.config.vocab_size != len(tokenizer):
        raise ValueError("Model vocabulary and tokenizer differ")
    if config["sequence_length"] > model.config.max_position_embeddings:
        raise ValueError("Sequence length exceeds model configuration")
    model.config.use_cache = False
    if config["gradient_checkpointing"]:
        model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    return model, tokenizer


def rng_state(torch):
    return {"python": random.getstate(), "numpy": np.random.get_state(),
            "torch": torch.get_rng_state(), "cuda": torch.cuda.get_rng_state_all()}


def restore_rng(torch, state):
    random.setstate(state["python"])
    np.random.set_state(state["numpy"])
    torch.set_rng_state(state["torch"])
    torch.cuda.set_rng_state_all(state["cuda"])


def save_checkpoint(directory, model, optimizer, scaler, state, config, identities, torch, invocation_id):
    directory = Path(directory)
    generation = uuid.uuid4().hex
    final = directory / f"checkpoint-{generation}.pt"
    temporary = final.with_suffix(".pt.partial")
    previous = read_json(directory / "checkpoint.json") if (directory / "checkpoint.json").exists() else None
    snapshot = {"format": "lwm-training-state-v1", "model": model.state_dict(),
                "optimizer": optimizer.state_dict(), "scaler": scaler.state_dict(),
                "rng": rng_state(torch), "state": state, "config": config,
                "identities": identities}
    torch.save(snapshot, temporary)
    with temporary.open("rb") as stream:
        os.fsync(stream.fileno())
    os.replace(temporary, final)
    fsync_directory(directory)
    receipt = {"path": final.name, "generation": generation, "state": dict(state),
               "invocation_id": invocation_id, "sha256": sha256_file(final),
               "config_hash": canonical_hash(config),
               "previous": {k: v for k, v in previous.items() if k != "previous"} if previous else None}
    # This single durable pointer replacement is the publication commit point.
    write_json(directory / "checkpoint.json", receipt)
    if previous and previous.get("previous"):
        obsolete = within(directory, previous["previous"]["path"])
        obsolete.unlink(missing_ok=True)
        fsync_directory(directory)
    return generation


def dev_loss(model, dataset, batch_size, device, use_amp):
    import torch
    import torch.nn.functional as F
    model.eval()
    numerator, denominator = 0.0, 0
    order = np.arange(len(dataset))
    with torch.no_grad():
        for start in range(0, len(dataset), batch_size):
            x, y = batch_at(dataset, order, start, batch_size)
            x = torch.from_numpy(x).to(device)
            y = torch.from_numpy(y).to(device)
            with torch.autocast("cuda", dtype=torch.float16, enabled=use_amp):
                logits = model(input_ids=x, use_cache=False).logits
                loss = F.cross_entropy(logits.float().reshape(-1, logits.size(-1)),
                                       y.reshape(-1), ignore_index=-100, reduction="sum")
            numerator += loss.item()
            denominator += int((y != -100).sum().item())
    model.train()
    return {"nll": numerator / denominator, "targets": denominator,
            "scope": "training-development split; not a published benchmark score"}


def train(config, root, assets_dir, output, resume=False, max_updates=None, device="cuda"):
    import torch
    import torch.nn.functional as F
    validate_train_config(config)
    root, output = Path(root).resolve(), Path(output).resolve()
    if device != "cuda" or not torch.cuda.is_available():
        raise RuntimeError("Training is configured for the admitted CUDA device on the GPU host")
    if torch.cuda.device_count() != 1:
        raise RuntimeError("Expose exactly one admitted GPU; do not change CUDA_VISIBLE_DEVICES inside this program")
    if max_updates is not None and max_updates <= 0:
        raise ValueError("max_updates must be positive; it is an acceptance/feasibility cap, not a new budget")
    output.mkdir(parents=True, exist_ok=True)
    with (output / "writer.lock").open("a+") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise RuntimeError("This output directory already has an active writer") from error
        return _train_locked(config, root, assets_dir, output, resume, max_updates, torch, F)


def _train_locked(config, root, assets_dir, output, resume, max_updates, torch, F):
    started = time.monotonic()
    interrupted = {"value": False}
    handlers = {}
    for sig in (signal.SIGTERM, signal.SIGINT):
        handlers[sig] = signal.signal(sig, lambda *_: interrupted.update(value=True))
    try:
        pointer = output / "checkpoint.json"
        if pointer.exists() and not resume:
            raise ValueError("Checkpoint exists: use --resume or a fresh output directory")
        if resume and not pointer.exists():
            raise ValueError("--resume requires an existing checkpoint")
        if not resume and (output / "config.json").exists():
            raise ValueError("Prior run metadata exists without a checkpoint; preserve the attempt and choose a new output")
        random.seed(config["seed"])
        np.random.seed(config["seed"])
        torch.manual_seed(config["seed"])
        torch.cuda.manual_seed_all(config["seed"])
        torch.backends.cuda.matmul.allow_tf32 = False
        torch.backends.cudnn.allow_tf32 = False
        manifest_path = root / config["data_manifest"]
        manifest = validate_corpus(manifest_path)
        sources = read_json(root / "configs/sources.json")
        from .assets import verify_assets
        model_receipt = verify_assets(Path(assets_dir) / "smollm2")
        expected = sources["models"]["smollm2"]
        if model_receipt["repo"] != expected["repo"] or model_receipt["revision"] != expected["revision"]:
            raise ValueError("Model acquisition revision does not match pinned source")
        if manifest["tokenizer"] != expected:
            raise ValueError("Corpus tokenizer identity does not match model input identity")
        identities = {"corpus_sha256": sha256_file(manifest_path), "source": git_identity(root),
                      "environment": environment_identity(),
                      "model_assets_sha256": sha256_file(Path(assets_dir) / "smollm2/acquisition.json"),
                      "model_config_sha256": (sha256_file(root / config["model"]["config"])
                        if config["model"]["initialization"] == "scratch" else None)}
        if identities["source"]["status"]:
            raise ValueError("Commit source changes before training; no untracked or modified source runs")
        train_data = TokenBlocks(manifest_path, "train", config["sequence_length"], config["total_tokens"])
        dev_data = TokenBlocks(manifest_path, "dev", config["sequence_length"])
        order = np.random.default_rng(config["seed"]).permutation(len(train_data))
        model, tokenizer = initialize_model(config, assets_dir, root)
        model.to("cuda")
        optimizer = torch.optim.AdamW(model.parameters(), lr=config["learning_rate"],
                                       betas=(0.9, 0.95), weight_decay=config["weight_decay"])
        amp = config["precision"] == "fp16"
        scaler = torch.amp.GradScaler("cuda", enabled=amp)
        state = {"next_block": 0, "trained_tokens": 0, "optimizer_steps": 0,
                 "attempted_tokens": 0, "overflows": 0, "elapsed_seconds": 0.0}
        invocation_id = uuid.uuid4().hex
        parent_generation = None
        if resume:
            checkpoint = resolve_checkpoint(output)
            parent_generation = read_json(pointer)["generation"]
            saved = torch.load(checkpoint, map_location="cpu", weights_only=False)
            if saved["config"] != config or saved["identities"] != identities:
                raise ValueError("Resume would change config/source/input identity; a new protocol/run is required")
            model.load_state_dict(saved["model"], strict=True)
            optimizer.load_state_dict(saved["optimizer"])
            scaler.load_state_dict(saved["scaler"])
            state = saved["state"]
            restore_rng(torch, saved["rng"])
            del saved
        append_jsonl(output / "train.jsonl", {"event": "invocation", "invocation_id": invocation_id,
                     "resume_generation": parent_generation, "initial_state": dict(state)})
        write_json(output / "config.json", config)
        write_json(output / "source.json", identities)
        write_json(output / "hardware.json", {"name": torch.cuda.get_device_name(0),
             "capability": list(torch.cuda.get_device_capability(0)),
             "total_memory": torch.cuda.get_device_properties(0).total_memory,
             "torch": torch.__version__, "cuda": torch.version.cuda,
             "parameters": sum(p.numel() for p in model.parameters()),
             "precision": config["precision"], "one_gpu": True})
        torch.cuda.reset_peak_memory_stats()
        model.train()
        initial_steps = state["optimizer_steps"]
        previous_elapsed = state["elapsed_seconds"]
        consecutive_overflows = 0
        while state["next_block"] < len(train_data):
            if interrupted["value"] or time.monotonic() - started >= config["max_wall_seconds"]:
                break
            if max_updates is not None and state["optimizer_steps"] - initial_steps >= max_updates:
                break
            group = schedule_group(state["next_block"], len(train_data),
                                   config["micro_batch_size"], config["gradient_accumulation_steps"])
            batches = [batch_at(train_data, order, start, count) for start, count in group]
            group_tokens = sum(int(np.count_nonzero(y != -100)) for _, y in batches)
            lr = learning_rate(state["trained_tokens"], config["total_tokens"], config["learning_rate"],
                               config["warmup_fraction"], config["min_lr_ratio"])
            for parameters in optimizer.param_groups:
                parameters["lr"] = lr
            optimizer.zero_grad(set_to_none=True)
            nll_sum = 0.0
            step_started = time.monotonic()
            for x, y in batches:
                x = torch.from_numpy(x).to("cuda")
                y = torch.from_numpy(y).to("cuda")
                with torch.autocast("cuda", dtype=torch.float16, enabled=amp):
                    logits = model(input_ids=x, use_cache=False).logits
                    loss_sum = F.cross_entropy(logits.float().reshape(-1, logits.size(-1)),
                                               y.reshape(-1), ignore_index=-100, reduction="sum")
                if not torch.isfinite(loss_sum):
                    raise FloatingPointError("Nonfinite loss; keep failed attempt, do not silently change precision")
                nll_sum += float(loss_sum.detach())
                scaler.scale(loss_sum / group_tokens).backward()
                del logits, loss_sum, x, y
            scaler.unscale_(optimizer)
            norm = torch.nn.utils.clip_grad_norm_(model.parameters(), config["grad_clip"],
                                                  error_if_nonfinite=not amp)
            old_scale = scaler.get_scale()
            scaler.step(optimizer)
            scaler.update()
            state["attempted_tokens"] += group_tokens
            overflow = amp and scaler.get_scale() < old_scale
            if overflow:
                state["overflows"] += 1
                consecutive_overflows += 1
                append_jsonl(output / "train.jsonl", {"event": "fp16_overflow", "state": dict(state),
                                                       "invocation_id": invocation_id,
                                                       "committed_generation": parent_generation,
                                                       "new_scale": scaler.get_scale()})
                if consecutive_overflows >= config["max_consecutive_overflows"]:
                    raise FloatingPointError("Consecutive FP16 overflows exceeded bound; qualification required")
                continue  # retry the same data group; never count it as learned tokens
            consecutive_overflows = 0
            state["next_block"] += sum(count for _, count in group)
            state["trained_tokens"] += group_tokens
            state["optimizer_steps"] += 1
            torch.cuda.synchronize()
            elapsed_step = time.monotonic() - step_started
            state["elapsed_seconds"] = previous_elapsed + time.monotonic() - started
            record = {"event": "update", **state, "nll": nll_sum / group_tokens, "lr": lr,
                      "invocation_id": invocation_id, "committed_generation": parent_generation,
                      "grad_norm": float(norm), "step_seconds": elapsed_step,
                      "tokens_per_second": group_tokens / elapsed_step,
                      "peak_allocated_bytes": torch.cuda.max_memory_allocated(),
                      "peak_reserved_bytes": torch.cuda.max_memory_reserved()}
            append_jsonl(output / "train.jsonl", record)
            if state["optimizer_steps"] % 10 == 0:
                print(record, flush=True)
            if state["optimizer_steps"] % config["dev_every_updates"] == 0:
                record_dev = dev_loss(model, dev_data, config["micro_batch_size"], "cuda", amp)
                append_jsonl(output / "dev.jsonl", {"optimizer_steps": state["optimizer_steps"],
                             "invocation_id": invocation_id, "committed_generation": parent_generation, **record_dev})
            if state["optimizer_steps"] % config["checkpoint_every_updates"] == 0:
                state["elapsed_seconds"] = previous_elapsed + time.monotonic() - started
                parent_generation = save_checkpoint(output, model, optimizer, scaler, state, config,
                                                     identities, torch, invocation_id)
        state["elapsed_seconds"] = previous_elapsed + time.monotonic() - started
        parent_generation = save_checkpoint(output, model, optimizer, scaler, state, config,
                                             identities, torch, invocation_id)
        completed = state["trained_tokens"] == config["total_tokens"]
        if completed:
            model.save_pretrained(output / "model", safe_serialization=True)
            tokenizer.save_pretrained(output / "model")
        write_json(output / "status.json", {"status": "training_complete" if completed else "paused",
                   "invocation_id": invocation_id, "committed_generation": parent_generation,
                   "state": state, "scientific_result_verified": False,
                   "reason": "token budget reached" if completed else "signal, wall limit or acceptance update cap"})
        return state
    finally:
        for sig, handler in handlers.items():
            signal.signal(sig, handler)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--root", default=".")
    parser.add_argument("--assets", default="assets")
    parser.add_argument("--output", required=True)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--max-updates", type=int)
    args = parser.parse_args()
    train(load_train_config(args.config), args.root, args.assets, args.output, args.resume, args.max_updates)


if __name__ == "__main__":
    main()
