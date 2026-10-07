import math
import pytest
from latent_world_model.training import learning_rate, schedule_group
from latent_world_model.config import validate_train_config


def test_final_accumulation_group_has_exact_block_count():
    assert schedule_group(0, 21, 2, 4) == [(0, 2), (2, 2), (4, 2), (6, 2)]
    assert schedule_group(20, 21, 2, 4) == [(20, 1)]
    assert schedule_group(21, 21, 2, 4) == []


def test_learning_rate_boundaries():
    assert learning_rate(0, 1000, 0.01, 0.1, 0.1) > 0
    assert math.isclose(learning_rate(100, 1000, 0.01, 0.1, 0.1), 0.01)
    assert math.isclose(learning_rate(1000, 1000, 0.01, 0.1, 0.1), 0.001)


def test_reject_bf16_and_implicit_architecture(tmp_path):
    base = {"name": "fixture", "model": {"initialization": "scratch",
            "config": "configs/model_31m.json"}, "data_manifest": "data/manifest.json",
            "total_tokens": 100, "sequence_length": 8, "micro_batch_size": 1,
            "gradient_accumulation_steps": 2, "seed": 17, "precision": "bf16",
            "learning_rate": 0.001, "weight_decay": 0.1, "warmup_fraction": 0.01,
            "min_lr_ratio": 0.1, "grad_clip": 1.0, "checkpoint_every_updates": 10,
            "dev_every_updates": 10, "gradient_checkpointing": True,
            "max_consecutive_overflows": 8, "max_wall_seconds": 82800}
    with pytest.raises(ValueError, match="precision"):
        validate_train_config(base)
