"""Local software acceptance checks; authored but not executed in the Web role.

These tiny deterministic fixtures check mathematical/software semantics only.
They are not training runs, benchmark examples, or scientific evidence.
Local command pending: python -m pytest tests/test_model_semantics.py
"""

import math
from unittest.mock import patch

import pytest
import torch
from torch.nn import functional as F

from lwm.model import LatentWorldModel, ModelConfig


def _model(*, loop_steps=2):
    # The test seed controls initialization, not any scientific experiment.
    torch.manual_seed(417)
    model = LatentWorldModel(
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
            loop_steps=loop_steps,
            dropout=0.0,
            checkpoint_layers=False,
            memory_enabled=True,
        )
    )
    return model.eval()


@pytest.fixture
def model():
    return _model()


def _tokens():
    return torch.tensor([[2, 7, 4, 13], [3, 9, 1, 5]], dtype=torch.long)


def _likelihood_loss(logits, tokens):
    # Row i already predicts token i. A second label shift would be a bug.
    return F.cross_entropy(logits.reshape(-1, logits.shape[-1]), tokens.reshape(-1))


def _assert_nonzero_finite(gradient):
    assert gradient is not None, "the required gradient path is disconnected"
    assert torch.isfinite(gradient).all(), "the required gradient is nonfinite"
    assert torch.count_nonzero(gradient).item() > 0, "the required gradient is zero"


def test_activation_recomputation_preserves_two_segment_loss_and_gradients():
    ordinary = _model().train()
    recomputed = _model().train()
    recomputed.load_state_dict(ordinary.state_dict())
    recomputed.config.checkpoint_layers = True
    tokens = _tokens()
    losses = []
    for current in (ordinary, recomputed):
        first, memory = current.forward_segment(tokens, current.initial_memory(2))
        second, _ = current.forward_segment(tokens.flip(1), memory)
        loss = _likelihood_loss(first, tokens) + _likelihood_loss(second, tokens.flip(1))
        loss.backward()
        losses.append(loss.detach())
    torch.testing.assert_close(losses[0], losses[1])
    for (name, first), (other_name, second) in zip(ordinary.named_parameters(), recomputed.named_parameters(), strict=True):
        assert name == other_name
        assert (first.grad is None) == (second.grad is None), name
        if first.grad is not None:
            torch.testing.assert_close(first.grad, second.grad, msg=name)
    _assert_nonzero_finite(recomputed.writer.proposal.weight.grad)


@pytest.mark.skipif(not torch.cuda.is_available(), reason="Local CUDA device is unavailable")
def test_amp_writer_does_not_round_complementary_gate_weights_out_of_bounds():
    model = _model().cuda()
    memory = torch.ones(1, model.config.memory_slots, model.config.d_model, device="cuda")
    evidence = torch.zeros(1, model.config.block_size, model.config.d_model, device="cuda")
    # This valid gate is a rounding boundary where FP16 (1-g) can become 1.
    probability = 2.0 ** -12
    gate_logit = math.log(probability / (1 - probability))
    with patch.object(model.writer.gate, "forward", return_value=torch.full_like(memory, gate_logit, dtype=torch.float16)), \
         patch.object(model.writer.proposal, "forward", return_value=torch.full_like(memory, 20, dtype=torch.float16)), \
         torch.no_grad(), torch.autocast("cuda", dtype=torch.float16):
        updated = model.writer(memory, evidence, model.slot_embedding)
    assert updated.dtype == torch.float32
    assert bool(torch.isfinite(updated).all())
    assert float(updated.max()) <= 1.0 + 1e-7
    assert float(updated.min()) >= -1.0 - 1e-7


@pytest.mark.parametrize("target_position", [0, 1, 2, 3])
def test_prediction_cannot_see_its_target_or_future_tokens(model, target_position):
    # Catches a missing causal mask, target leakage, or reading freshly written memory.
    tokens = _tokens()
    changed = tokens.clone()
    changed[:, target_position:] = (changed[:, target_position:] + 5) % 19
    memory = model.initial_memory(batch_size=2)

    with torch.no_grad():
        original_logits, _ = model.forward_segment(tokens, memory)
        changed_logits, _ = model.forward_segment(changed, memory)

    torch.testing.assert_close(
        original_logits[:, : target_position + 1],
        changed_logits[:, : target_position + 1],
        rtol=1e-5,
        atol=1e-6,
    )


@pytest.mark.parametrize("length", [1, 3, 4])
def test_teacher_forcing_matches_every_prefix_including_empty(model, length):
    # Catches an extra conventional label shift and a missing segment-start row.
    tokens = _tokens()[:, :length]
    memory = model.initial_memory(batch_size=2)

    with torch.no_grad():
        logits, _ = model.forward_segment(tokens, memory)
        assert logits.shape == (2, length, 19)
        assert torch.isfinite(logits).all()
        for position in range(length):
            prefix_logits = model.predict_prefix(tokens[:, :position], memory)
            assert prefix_logits.shape == (2, 19)
            torch.testing.assert_close(
                prefix_logits, logits[:, position], rtol=1e-5, atol=1e-6
            )


def test_next_prediction_uses_the_last_observed_prefix_token(model):
    # Catches a shared off-by-one bug in both teacher forcing and prefix prediction.
    prefix = _tokens()[:, :3]
    changed = prefix.clone()
    changed[:, -1] = torch.tensor([15, 16])
    memory = model.initial_memory(batch_size=2)

    with torch.no_grad():
        original_logits = model.predict_prefix(prefix, memory)
        changed_logits = model.predict_prefix(changed, memory)

    assert not torch.allclose(original_logits, changed_logits, rtol=1e-6, atol=1e-7)


@pytest.mark.parametrize("prefix_length", [0, 1, 3])
@pytest.mark.parametrize("loop_steps,memory_enabled", [(1, True), (4, True), (4, False)])
@pytest.mark.parametrize("device", ["cpu", pytest.param("cuda", marks=pytest.mark.skipif(
    not torch.cuda.is_available(), reason="Local CUDA device is unavailable"))])
def test_prefix_projects_only_next_position_without_changing_logits(prefix_length, loop_steps, memory_enabled, device):
    # Catches restoring the discarded prefix-wide vocabulary projection, slicing
    # before causal coda, or truncating the teacher-forcing supervision rows.
    model = _model(loop_steps=loop_steps).to(device)
    model.config.memory_enabled = memory_enabled
    tokens = _tokens().to(device)
    memory = model.initial_memory(2)
    projected_shapes = []
    handle = model.output_norm.register_forward_pre_hook(
        lambda module, inputs: projected_shapes.append(tuple(inputs[0].shape)))
    try:
        with torch.no_grad():
            prefix = model.predict_prefix(tokens[:, :prefix_length], memory)
            teacher, _ = model.forward_segment(tokens, memory)
    finally:
        handle.remove()
    assert projected_shapes == [(2, 1, 16), (2, 4, 16)]
    torch.testing.assert_close(prefix, teacher[:, prefix_length], rtol=1e-5, atol=1e-6)


def test_prefix_projection_preserves_parameter_gradients():
    # Catches a detached last state or dropping its earlier causal dependencies.
    reference, prefix_model = _model(), _model()
    tokens = _tokens()
    full, _ = reference.forward_segment(tokens, reference.initial_memory(2))
    one = prefix_model.predict_prefix(tokens[:, :3], prefix_model.initial_memory(2))
    F.cross_entropy(full[:, 3], tokens[:, 3]).backward()
    F.cross_entropy(one, tokens[:, 3]).backward()
    for (name, first), (other, second) in zip(reference.named_parameters(), prefix_model.named_parameters(), strict=True):
        assert name == other
        assert (first.grad is None) == (second.grad is None), name
        if first.grad is not None:
            torch.testing.assert_close(first.grad, second.grad, rtol=1e-4, atol=2e-6, msg=name)
    _assert_nonzero_finite(prefix_model.embedding.weight.grad)


def test_teacher_forcing_and_explicit_commit_agree_at_segment_boundary(model):
    # Catches using stale memory, a missing write, or an extra token at the boundary.
    first_tokens = _tokens()
    second_tokens = torch.tensor([[6, 11, 8], [10, 12, 14]], dtype=torch.long)
    initial_memory = model.initial_memory(batch_size=2)

    with torch.no_grad():
        _, teacher_memory = model.forward_segment(first_tokens, initial_memory)
        committed_memory = model.commit_segment(first_tokens, initial_memory)
        second_logits, _ = model.forward_segment(second_tokens, teacher_memory)
        torch.testing.assert_close(teacher_memory, committed_memory)
        for position in range(second_tokens.shape[1]):
            prefix_logits = model.predict_prefix(
                second_tokens[:, :position], committed_memory
            )
            torch.testing.assert_close(
                prefix_logits, second_logits[:, position], rtol=1e-5, atol=1e-6
            )


def test_initial_memory_is_learned_and_receives_likelihood_gradient(model):
    # Catches detached/copied initialization and a reader that ignores memory.
    memory = model.initial_memory(batch_size=2)
    assert memory.shape == (2, 3, 16)
    assert memory.requires_grad
    parameters = tuple(model.parameters())
    initialization_gradients = torch.autograd.grad(
        memory.sum(), parameters, allow_unused=True, retain_graph=True
    )
    learned_initialization = [
        parameter
        for parameter, gradient in zip(parameters, initialization_gradients)
        if gradient is not None
    ]
    assert learned_initialization, "initial_memory must depend on model parameters"

    logits, _ = model.forward_segment(_tokens(), memory)
    gradients = torch.autograd.grad(
        _likelihood_loss(logits, _tokens()),
        learned_initialization,
        allow_unused=True,
    )
    present = [gradient for gradient in gradients if gradient is not None]
    assert present, "likelihood must reach the learned memory initialization"
    for gradient in present:
        assert torch.isfinite(gradient).all()
    assert any(torch.count_nonzero(gradient).item() > 0 for gradient in present)


def test_second_segment_likelihood_trains_the_previous_segment_writer(model):
    # Catches a detach inside the writer/segment API or loss on only the current write.
    memory = model.initial_memory(batch_size=2)
    _, first_written_memory = model.forward_segment(_tokens(), memory)
    first_written_memory.retain_grad()
    second_tokens = torch.tensor([[6, 11, 8], [10, 12, 14]], dtype=torch.long)

    second_logits, _ = model.forward_segment(second_tokens, first_written_memory)
    _likelihood_loss(second_logits, second_tokens).backward()

    _assert_nonzero_finite(first_written_memory.grad)
    writer_gradients = [parameter.grad for parameter in model.writer.parameters()]
    present = [gradient for gradient in writer_gradients if gradient is not None]
    assert present, "the earlier writer must receive the next-segment loss"
    for gradient in present:
        assert torch.isfinite(gradient).all()
    assert any(torch.count_nonzero(gradient).item() > 0 for gradient in present)


def test_detaching_boundary_memory_blocks_the_previous_writer_graph(model):
    # Catches hidden model state retaining a graph across the explicit TBPTT boundary.
    memory = model.initial_memory(batch_size=2)
    _, first_written_memory = model.forward_segment(_tokens(), memory)
    first_written_memory.retain_grad()
    detached_memory = first_written_memory.detach().requires_grad_(True)
    second_tokens = torch.tensor([[6, 11, 8], [10, 12, 14]], dtype=torch.long)

    second_logits, _ = model.forward_segment(second_tokens, detached_memory)
    _likelihood_loss(second_logits, second_tokens).backward()

    _assert_nonzero_finite(detached_memory.grad)
    assert first_written_memory.grad is None
    assert all(parameter.grad is None for parameter in model.writer.parameters())


def test_reader_iteration_count_does_not_change_the_committed_memory():
    # Catches a writer that consumes recurrent reader state or writes on every loop.
    shallow = _model(loop_steps=1)
    deep = _model(loop_steps=4)
    deep.load_state_dict(shallow.state_dict(), strict=True)
    memory = shallow.initial_memory(batch_size=2)

    with torch.no_grad():
        shallow_commit = shallow.commit_segment(_tokens(), memory)
        deep_commit = deep.commit_segment(_tokens(), memory)
        _, shallow_forward_memory = shallow.forward_segment(_tokens(), memory)
        _, deep_forward_memory = deep.forward_segment(_tokens(), memory)

    torch.testing.assert_close(shallow_commit, deep_commit, rtol=0, atol=0)
    torch.testing.assert_close(shallow_forward_memory, shallow_commit)
    torch.testing.assert_close(deep_forward_memory, shallow_commit)


def test_writer_consumes_the_final_observed_token(model):
    # Catches using prediction rows E[:, :L] instead of observed rows E[:, 1:L+1].
    original = _tokens()
    changed = original.clone()
    changed[:, -1] = torch.tensor([15, 16])
    memory = model.initial_memory(batch_size=2)

    with torch.no_grad():
        original_memory = model.commit_segment(original, memory)
        changed_memory = model.commit_segment(changed, memory)

    assert not torch.allclose(original_memory, changed_memory, rtol=1e-6, atol=1e-7)


@pytest.mark.parametrize("operation", ["forward_segment", "predict_prefix", "commit_segment"])
def test_public_model_operations_leave_caller_memory_unchanged(model, operation):
    # Catches in-place memory writes that corrupt other prefixes or unroll graphs.
    memory = model.initial_memory(batch_size=2).detach().clone()
    before = memory.clone()
    tokens = _tokens()
    if operation == "predict_prefix":
        tokens = tokens[:, :2]

    with torch.no_grad():
        getattr(model, operation)(tokens, memory)

    torch.testing.assert_close(memory, before, rtol=0, atol=0)


@pytest.mark.parametrize("operation", ["forward_segment", "commit_segment"])
def test_observed_segment_apis_reject_empty_segments(model, operation):
    # Catches undefined empty writer attention or silently treating SEG as data.
    empty_tokens = torch.empty((2, 0), dtype=torch.long)
    memory = model.initial_memory(batch_size=2)

    with pytest.raises(ValueError):
        getattr(model, operation)(empty_tokens, memory)


@pytest.mark.parametrize("length", [1, 2, 3])
def test_commit_rejects_an_unfinished_prefix(model, length):
    # Catches premature persistent writes that change the specified segmentation.
    memory = model.initial_memory(batch_size=2)

    with pytest.raises(ValueError):
        model.commit_segment(_tokens()[:, :length], memory)


def test_full_prefix_requires_a_commit_before_the_next_prediction(model):
    # Catches keeping block_size tokens in a prefix instead of crossing the boundary.
    memory = model.initial_memory(batch_size=2)

    with pytest.raises(ValueError):
        model.predict_prefix(_tokens(), memory)
