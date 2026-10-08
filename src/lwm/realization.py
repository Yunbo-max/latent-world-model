"""Persisted token-plan interface; realization never invokes reader or writer.

This is a learned continuous text plan, not an identified semantic codec.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import torch

from .checkpoint import save_checkpoint, load_checkpoint
from .data import canonical_hash, file_sha256
from .generation import stream_payload, restore_stream
from .model import ModelConfig, LatentWorldModel


def tensor_digest(value):
    value = value.detach().cpu().contiguous()
    return canonical_hash({"shape": list(value.shape), "dtype": str(value.dtype),
        "bytes_sha256": hashlib.sha256(value.numpy().tobytes()).hexdigest()})


def implementation_identity():
    return {path.name: file_sha256(path) for path in sorted(Path(__file__).parent.glob("*.py"))}


def context_identity(state):
    payload = stream_payload(state)
    payload["memory"] = tensor_digest(payload["memory"])
    payload["prefix"] = tensor_digest(payload["prefix"])
    # Compute/readout clocks do not change the admitted evidence or prefix.
    payload.pop("reasoning_clock")
    payload.pop("expression_clock")
    return canonical_hash(payload)


def plan_snapshot(model, state, plan, checkpoint_sha256, tokenizer):
    if not model.config.semantic_dim or tuple(plan.shape) != (1, state.prefix.size(1) + 1, model.config.semantic_dim):
        raise ValueError("Plan/context dimensions differ")
    if not bool(torch.isfinite(plan).all()) or bool((plan.abs() > 1).any()):
        raise ValueError("Invalid bounded plan")
    return {"kind": "lwm-text-plan-v1", "model_checkpoint_sha256": checkpoint_sha256,
            "tokenizer": tokenizer, "model_config": model.config.to_dict(),
            "source_identity": implementation_identity(), "context": stream_payload(state),
            "context_sha256": context_identity(state), "plan": plan.detach().cpu(),
            "plan_sha256": tensor_digest(plan), "semantics": "per-token text-prediction bottleneck; no sentence/action semantics"}


def restore_plan(model, snapshot, checkpoint_sha256, tokenizer, *, current_state=None):
    if (snapshot.get("kind") != "lwm-text-plan-v1" or snapshot["model_checkpoint_sha256"] != checkpoint_sha256
            or snapshot["tokenizer"] != tokenizer or snapshot["model_config"] != model.config.to_dict()
            or snapshot["source_identity"] != implementation_identity()):
        raise ValueError("Plan model/tokenizer/source identity mismatch")
    context = restore_stream(model, snapshot["context"])
    if context_identity(context) != snapshot["context_sha256"]:
        raise ValueError("Plan context identity differs")
    if current_state is not None and context_identity(current_state) != snapshot["context_sha256"]:
        raise ValueError("Stale plan for a changed observation/prefix")
    plan = snapshot["plan"]
    if (tensor_digest(plan) != snapshot["plan_sha256"] or tuple(plan.shape) !=
            (1, context.prefix.size(1) + 1, model.config.semantic_dim)
            or not plan.is_floating_point() or not bool(torch.isfinite(plan).all())
            or bool((plan.abs() > 1).any())):
        raise ValueError("Plan payload identity/shape differs")
    # Explicit expression-device/dtype conversion; no replanning on load.
    return plan.to(device=model.embedding.weight.device, dtype=model.embedding.weight.dtype)


def main(argv=None):
    import argparse
    import json
    from .prepare import load_tokenizer, tokenizer_identity
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--tokenizer", required=True)
    parser.add_argument("--plan", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--device", default="cuda")
    args = parser.parse_args(argv)
    checkpoint = load_checkpoint(args.checkpoint)
    model = LatentWorldModel(ModelConfig(**checkpoint["model_config"]))
    model.load_state_dict(checkpoint["model_state"], strict=True)
    model = model.to(args.device).eval()
    tokenizer = load_tokenizer(args.tokenizer)
    identity = tokenizer_identity(args.tokenizer)
    if checkpoint["corpus_provenance"]["tokenizer"] != identity:
        raise ValueError("Tokenizer/checkpoint differs")
    checkpoint_hash = file_sha256(args.checkpoint)
    snapshot = load_checkpoint(args.plan)
    plan = restore_plan(model, snapshot, checkpoint_hash, identity)
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=False)
    with torch.inference_mode():
        logits = model.realize_plan(plan, last_only=True)[0, -1].float()
    if not bool(torch.isfinite(logits).all()):
        raise FloatingPointError("Nonfinite realization logits")
    token = int(logits.argmax().item())
    save_checkpoint(output / "logits.pt", {"logits": logits.cpu(), "plan_sha256": snapshot["plan_sha256"]})
    result = {"token_id": token, "text": tokenizer.decode([token], clean_up_tokenization_spaces=False),
              "model_checkpoint_sha256": checkpoint_hash, "plan_sha256": snapshot["plan_sha256"],
              "context_sha256": snapshot["context_sha256"], "reader_calls": 0,
              "writer_calls": 0, "retrieval_calls": 0, "scope": "one next-symbol realization from restored plan"}
    (output / "manifest.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
