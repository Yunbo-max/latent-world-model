"""Unexecuted Local software checks for the functional streaming interface.

Fixtures are tiny software examples, never scientific evaluation results.
Local command pending: python -m pytest tests/test_generation_semantics.py
"""

from unittest.mock import patch

import pytest
import torch

from lwm.generation import generate, next_logits, observe, score_continuation, start_stream
from lwm.model import LatentWorldModel, ModelConfig


EOS = 0


def _model(device="cpu"):
    torch.manual_seed(613)
    return LatentWorldModel(
        ModelConfig(
            vocab_size=19,
            d_model=16,
            n_heads=4,
            ffn_mult=2,
            block_size=4,
            memory_slots=3,
            prelude_layers=1,
            core_layers=1,
            coda_layers=1,
            loop_steps=2,
            dropout=0.0,
            checkpoint_layers=False,
            memory_enabled=True,
        )
    ).to(device).eval()


@pytest.fixture
def model():
    return _model()


def test_new_stream_predicts_from_an_empty_prefix(model):
    # Catches requiring a user-supplied BOS token or dropping the first-token target.
    state = start_stream(model)

    assert state.prefix.shape == (1, 0)
    assert state.prefix.dtype == torch.long
    assert state.memory.shape == (1, 3, 16)
    actual = next_logits(model, state)
    expected = model.predict_prefix(state.prefix, model.initial_memory(batch_size=1))

    assert actual.shape == (1, 19)
    assert torch.isfinite(actual).all()
    torch.testing.assert_close(actual, expected, rtol=1e-5, atol=1e-6)


def test_partial_observation_and_repeated_prediction_do_not_commit(model):
    # The spy delegates to the real writer; commit call count is part of the contract.
    # Catches speculative writes and mutation of a state retained by the caller.
    original = start_stream(model)
    original_memory = original.memory.detach().clone()
    original_prefix = original.prefix.clone()

    with patch.object(model, "commit_segment", wraps=model.commit_segment) as commit:
        state = observe(model, original, 2, eos_token_id=EOS)
        first_prediction = next_logits(model, state)
        second_prediction = next_logits(model, state)
        assert commit.call_count == 0

    torch.testing.assert_close(state.prefix, torch.tensor([[2]], dtype=torch.long))
    torch.testing.assert_close(state.memory, original_memory, rtol=0, atol=0)
    torch.testing.assert_close(original.memory, original_memory, rtol=0, atol=0)
    torch.testing.assert_close(original.prefix, original_prefix, rtol=0, atol=0)
    torch.testing.assert_close(first_prediction, second_prediction, rtol=0, atol=0)


def test_a_full_non_eos_segment_is_committed_exactly_once(model):
    # Catches early, duplicate, omitted, or delayed writes at a full-block boundary.
    initial = start_stream(model)
    first_tokens = torch.tensor([[2, 3, 5, 7]], dtype=torch.long)
    second_tokens = torch.tensor([[9, 10, 11, 12]], dtype=torch.long)
    expected_first_memory = model.commit_segment(first_tokens, initial.memory)
    expected_second_memory = model.commit_segment(second_tokens, expected_first_memory)
    initial_memory = initial.memory.detach().clone()

    with patch.object(model, "commit_segment", wraps=model.commit_segment) as commit:
        state = initial
        for token_id in [2, 3, 5]:
            state = observe(model, state, token_id, eos_token_id=EOS)
            next_logits(model, state)
        partial_state = state
        partial_prefix = partial_state.prefix.clone()
        assert commit.call_count == 0

        state = observe(model, state, 7, eos_token_id=EOS)
        assert commit.call_count == 1
        assert state.prefix.shape == (1, 0)
        torch.testing.assert_close(state.memory, expected_first_memory)
        torch.testing.assert_close(partial_state.prefix, partial_prefix, rtol=0, atol=0)
        torch.testing.assert_close(partial_state.memory, initial_memory, rtol=0, atol=0)

        next_logits(model, state)
        next_logits(model, state)
        state = observe(model, state, 9, eos_token_id=EOS)
        next_logits(model, state)
        assert commit.call_count == 1
        torch.testing.assert_close(state.memory, expected_first_memory)

        for token_id in [10, 11, 12]:
            state = observe(model, state, token_id, eos_token_id=EOS)
        assert commit.call_count == 2
        assert state.prefix.shape == (1, 0)
        torch.testing.assert_close(state.memory, expected_second_memory)

    torch.testing.assert_close(initial.memory, initial_memory, rtol=0, atol=0)
    assert initial.prefix.shape == (1, 0)


def test_stream_matches_teacher_forcing_on_both_sides_of_a_boundary(model):
    # Catches prefix indexing and stale-memory errors in the actual generation helpers.
    state = start_stream(model)
    teacher_memory = model.initial_memory(batch_size=1)
    segments = [
        torch.tensor([[2, 5, 7, 3]], dtype=torch.long),
        torch.tensor([[11, 4, 1]], dtype=torch.long),
    ]

    with torch.no_grad():
        for tokens in segments:
            teacher_logits, following_memory = model.forward_segment(tokens, teacher_memory)
            for position, token_id in enumerate(tokens[0].tolist()):
                torch.testing.assert_close(
                    next_logits(model, state),
                    teacher_logits[:, position],
                    rtol=1e-5,
                    atol=1e-6,
                )
                state = observe(model, state, token_id, eos_token_id=EOS)
            teacher_memory = following_memory


@pytest.mark.parametrize("partial_tokens", [[], [8, 6], [8, 6, 4]])
def test_eos_resets_memory_and_prefix_without_committing(model, partial_tokens):
    # Catches carrying document history forward or committing EOS at block capacity.
    state = start_stream(model)
    for token_id in [2, 3, 5, 7, *partial_tokens]:
        state = observe(model, state, token_id, eos_token_id=EOS)
    previous_memory = state.memory.detach().clone()
    previous_prefix = state.prefix.clone()

    with patch.object(model, "commit_segment", wraps=model.commit_segment) as commit:
        # Prediction precedes observation, so EOS remains a normal scored target.
        assert torch.isfinite(next_logits(model, state)[:, EOS]).all()
        reset = observe(model, state, EOS, eos_token_id=EOS)
        assert commit.call_count == 0

    fresh = start_stream(model)
    assert reset.prefix.shape == (1, 0)
    torch.testing.assert_close(reset.memory, fresh.memory, rtol=0, atol=0)
    torch.testing.assert_close(next_logits(model, reset), next_logits(model, fresh))
    torch.testing.assert_close(state.memory, previous_memory, rtol=0, atol=0)
    torch.testing.assert_close(state.prefix, previous_prefix, rtol=0, atol=0)


@pytest.mark.skipif(not torch.cuda.is_available(), reason="Local CUDA device is unavailable")
def test_stream_state_and_observed_tokens_follow_the_model_device():
    # Catches hard-coded CPU allocations that fail on the intended execution host.
    model = _model(device="cuda")
    state = start_stream(model)
    for token_id in [2, 3, 5, 7, 9]:
        state = observe(model, state, token_id, eos_token_id=EOS)
        assert state.prefix.device == next(model.parameters()).device
        assert state.memory.device == next(model.parameters()).device
        assert next_logits(model, state).device == next(model.parameters()).device


@pytest.mark.parametrize("bad_value", [float("nan"), float("inf"), float("-inf")])
def test_nonfinite_logits_cannot_be_reported_as_a_normal_answer(model, bad_value):
    logits = torch.zeros(1, model.config.vocab_size)
    logits[0, 3] = bad_value
    state = start_stream(model)
    with patch.object(model, "predict_prefix", return_value=logits):
        with pytest.raises(FloatingPointError, match="Nonfinite"):
            generate(model, state, 2, EOS)
        with pytest.raises(FloatingPointError, match="Nonfinite"):
            score_continuation(model, state, [4], EOS)
