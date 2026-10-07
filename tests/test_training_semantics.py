"""Unexecuted Local acceptance for objectives and RNG/atomic resume state."""
import random

import numpy as np
import torch
from torch.nn import functional as F

from lwm.checkpoint import capture_rng, restore_rng, save_checkpoint, load_checkpoint
from lwm.model import ModelConfig, LatentWorldModel
from lwm.train import clip_gradient_norm, window_objective


def test_window_objective_counts_only_eligible_targets():
    torch.manual_seed(11)
    model = LatentWorldModel(ModelConfig(vocab_size=23, d_model=16, n_heads=2,
        block_size=4, memory_slots=2, prelude_layers=1, core_layers=1,
        coda_layers=1, loop_steps=2))
    ids = torch.tensor([3, 4, 5, 6, 7, 8])
    mask = torch.tensor([False, False, False, True, True, True])
    memory = model.initial_memory(1)
    first, intermediate = model.forward_segment(ids[:4][None], memory)
    second, expected_memory = model.forward_segment(ids[4:][None], intermediate)
    expected = F.cross_entropy(first[:, 3].float(), ids[3:4], reduction="sum")
    expected = expected + F.cross_entropy(second[0].float(), ids[4:], reduction="sum")
    loss, actual_memory, count = window_objective(model, ids, mask, memory)
    assert count == 3
    torch.testing.assert_close(loss, expected)
    torch.testing.assert_close(actual_memory, expected_memory)
    loss.backward()
    assert any(p.grad is not None and bool(p.grad.abs().sum() > 0) for p in model.writer.parameters())


def test_checkpoint_restores_rng_and_primitive_state(tmp_path):
    random.seed(13)
    np.random.seed(13)
    torch.manual_seed(13)
    state = capture_rng()
    expected = (random.random(), np.random.random(), torch.rand(3))
    path = tmp_path / "last.pt"
    save_checkpoint(path, {"rng": state, "cursor": {"token_offset": 8},
                           "memory": torch.arange(4).float()})
    loaded = load_checkpoint(path)
    restore_rng(loaded["rng"])
    assert random.random() == expected[0]
    assert np.random.random() == expected[1]
    torch.testing.assert_close(torch.rand(3), expected[2])
    assert loaded["cursor"]["token_offset"] == 8


def test_large_finite_gradients_have_finite_norm_and_are_clipped():
    parameter = torch.nn.Parameter(torch.zeros(4))
    parameter.grad = torch.full_like(parameter, 1e30)
    norm = clip_gradient_norm([parameter], 1.0)
    assert bool(torch.isfinite(norm))
    torch.testing.assert_close(parameter.grad, torch.full_like(parameter, 0.5))


def test_nonfinite_gradients_are_left_for_amp_skip():
    parameter = torch.nn.Parameter(torch.zeros(2))
    parameter.grad = torch.tensor([float("inf"), 1.0])
    norm = clip_gradient_norm([parameter], 1.0)
    assert not bool(torch.isfinite(norm))
    assert parameter.grad[1].item() == 1.0
