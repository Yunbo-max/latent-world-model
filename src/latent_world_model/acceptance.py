"""Meaningful Local acceptance on acquired native training data, not benchmark scores."""
from pathlib import Path
import copy
from .config import load_train_config
from .io import read_json, resolve_checkpoint, write_json


def state_equal(a, b):
    import torch
    import numpy as np
    if isinstance(a, torch.Tensor):
        return isinstance(b, torch.Tensor) and torch.equal(a, b)
    if isinstance(a, np.ndarray):
        return isinstance(b, np.ndarray) and np.array_equal(a, b)
    if isinstance(a, dict):
        return isinstance(b, dict) and a.keys() == b.keys() and all(state_equal(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)):
        return type(a) is type(b) and len(a) == len(b) and all(state_equal(x, y) for x, y in zip(a, b))
    return a == b


def verify_resume(corpus, assets, output):
    import torch
    from .training import train
    root = Path(__file__).resolve().parents[2]
    config = copy.deepcopy(load_train_config(root / "configs/train_31m_100m.json"))
    available = read_json(corpus)["files"]["train"]["tokens"] - 1
    config.update({"data_manifest": str(corpus.resolve()), "total_tokens": min(8192, available),
        "sequence_length": 128, "micro_batch_size": 1, "gradient_accumulation_steps": 2,
        "precision": "fp32", "gradient_checkpointing": False,
        "checkpoint_every_updates": 100, "dev_every_updates": 100})
    if config["total_tokens"] < 1024:
        raise ValueError("Native acceptance needs at least 1024 released training targets")
    full = train(config, root, assets, output / "uninterrupted", max_updates=4)
    train(config, root, assets, output / "resumed", max_updates=2)
    resumed = train(config, root, assets, output / "resumed", resume=True, max_updates=2)
    a = torch.load(resolve_checkpoint(output / "uninterrupted"), map_location="cpu", weights_only=False)
    b = torch.load(resolve_checkpoint(output / "resumed"), map_location="cpu", weights_only=False)
    difference = max((a["model"][key] - b["model"][key]).abs().max().item() for key in a["model"])
    result = {"same_data_position": full["next_block"] == resumed["next_block"],
              "same_optimizer_steps": full["optimizer_steps"] == resumed["optimizer_steps"],
              "same_trained_tokens": full["trained_tokens"] == resumed["trained_tokens"],
              "same_optimizer": state_equal(a["optimizer"], b["optimizer"]),
              "same_scaler": state_equal(a["scaler"], b["scaler"]),
              "same_rng": state_equal(a["rng"], b["rng"]),
              "fp16_overflow_acceptance": "pending; this test is FP32",
              "max_parameter_difference": difference,
              "scope": "FP32 deterministic restart on released training blocks, no quality claim"}
    write_json(output / "resume-acceptance.json", result)
    return result
