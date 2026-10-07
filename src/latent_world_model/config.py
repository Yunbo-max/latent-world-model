"""Explicit baseline-only configuration: unknown model mechanisms are rejected."""
import math
from pathlib import Path
from .io import read_json


def validate_train_config(config):
    if config.get("precision") not in {"fp16", "fp32"}:
        raise ValueError("precision must be fp16 or fp32 for this 2080 Ti profile")
    if config.get("model", {}).get("initialization") not in {"scratch", "pretrained"}:
        raise ValueError("Only existing Llama scratch/pretrained baselines are implemented")
    for key in ("total_tokens", "sequence_length", "micro_batch_size",
                "gradient_accumulation_steps", "checkpoint_every_updates",
                "dev_every_updates", "max_consecutive_overflows", "max_wall_seconds"):
        value = config.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ValueError(f"{key} must be a positive integer")
    if config["max_wall_seconds"] > 86400:
        raise ValueError("A Local cycle cannot exceed 24 hours")
    for key in ("learning_rate", "grad_clip"):
        if not math.isfinite(config[key]) or config[key] <= 0:
            raise ValueError(f"{key} must be finite and positive")
    if not 0 < config["warmup_fraction"] < 1 or not 0 <= config["min_lr_ratio"] <= 1:
        raise ValueError("Invalid learning-rate schedule")
    if not math.isfinite(config["weight_decay"]) or config["weight_decay"] < 0:
        raise ValueError("Invalid weight decay")
    if not isinstance(config["seed"], int) or config["seed"] < 0:
        raise ValueError("seed must be a nonnegative integer")
    if config.get("mechanism", "baseline") != "baseline":
        raise ValueError("Candidate implementations require repaired selection/contribution evidence")
    return config


def load_train_config(path):
    return validate_train_config(read_json(Path(path)))
