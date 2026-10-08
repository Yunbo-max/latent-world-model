"""Authored Local checks; these fixtures are not a scientific benchmark."""
from dataclasses import replace
from unittest.mock import patch
import pytest
import torch
from torch.nn import functional as F

from lwm.generation import start_stream, ingest, plan_next, next_logits, stream_payload, restore_stream
from lwm.model import LatentWorldModel, ModelConfig
from lwm.realization import plan_snapshot, restore_plan
from lwm.train import window_objective, new_history, history_payload, restore_history
from lwm.train import validation_nll
from lwm.data import CorpusWriter, TokenCorpus


def small(**extra):
    config = dict(vocab_size=29, d_model=16, n_heads=2, ffn_mult=2, block_size=4,
                  memory_slots=2, prelude_layers=1, core_layers=1, coda_layers=1,
                  loop_steps=3, episodic_enabled=True, episodic_capacity_tokens=8,
                  episodic_read_tokens=8, episodic_query_tokens=3, episodic_top_k=2,
                  semantic_dim=8, dynamics="contractive", predictive_head=True)
    config.update(extra)
    return LatentWorldModel(ModelConfig(**config))


@pytest.mark.parametrize("device", ["cpu", pytest.param("cuda", marks=pytest.mark.skipif(not torch.cuda.is_available(), reason="GPU qualification pending"))])
def test_full_factorization_teacher_prefix_and_future_isolation(device):
    torch.manual_seed(3)
    model = small().to(device).eval()
    state = ingest(model, start_stream(model), [2, 3, 4, 5], -1)
    tokens = torch.tensor([[6, 7, 8, 9]], device=device)
    teacher, _ = model(tokens, state.memory, episodic=state.episodic)
    for row in range(4):
        prefix = model.predict_prefix(tokens[:, :row], state.memory, episodic=state.episodic)
        torch.testing.assert_close(prefix, teacher[:, row], atol=3e-6, rtol=3e-5)
    changed = tokens.clone()
    changed[:, 2:] = torch.tensor([[17, 18]], device=device)
    altered, _ = model(changed, state.memory, episodic=state.episodic)
    torch.testing.assert_close(teacher[:, :3], altered[:, :3], atol=3e-6, rtol=3e-5)


def test_restored_plan_realizes_without_reader_writer_or_retrieval_and_rejects_stale():
    model = small().eval()
    state = ingest(model, start_stream(model), [2, 3, 4, 5, 6], -1)
    plan, planned_state = plan_next(model, state)
    snapshot = plan_snapshot(model, planned_state, plan, "fixture-checkpoint", {"fixture": "tokenizer"})
    restored = restore_plan(model, snapshot, "fixture-checkpoint", {"fixture": "tokenizer"}, current_state=state)
    with patch.object(model, "_workspace", side_effect=AssertionError("reader called")), \
         patch.object(model, "_write", side_effect=AssertionError("writer called")), \
         patch.object(model, "_retrieved", side_effect=AssertionError("retrieval called")):
        actual = model.realize_plan(restored, last_only=True)[:, -1]
    torch.testing.assert_close(actual, next_logits(model, state), atol=2e-6, rtol=2e-5)
    changed = ingest(model, state, [7], -1)
    with pytest.raises(ValueError, match="Stale"):
        restore_plan(model, snapshot, "fixture-checkpoint", {"fixture": "tokenizer"}, current_state=changed)


def test_global_contractive_parameterization_has_no_recurrent_bypass():
    torch.manual_seed(4)
    model = small()
    with torch.no_grad():
        model.contractive.weight.mul_(100)
    matrix = model.contractive.matrix()
    assert float(torch.linalg.vector_norm(matrix)) <= model.config.contraction_bound + 1e-6
    h1, h2, forcing = torch.randn(1, 3, 16), torch.randn(1, 3, 16), torch.randn(1, 3, 16)
    r1 = model.contractive(h1, forcing, matrix)
    r2 = model.contractive(h2, forcing, matrix)
    assert torch.linalg.vector_norm(r1 - r2) <= (model.config.contraction_bound + 1e-6) * torch.linalg.vector_norm(h1 - h2)
    r1.sum().backward()
    assert model.contractive.weight.grad is not None and torch.isfinite(model.contractive.weight.grad).all()


def test_predictive_ce_has_immediate_writer_path_and_separate_masked_denominator():
    torch.manual_seed(5)
    model = small()
    memory = model.initial_memory(1)
    _, written = model.forward_segment(torch.tensor([[2, 3, 4, 5]]), memory,
        episodic=new_history(model, "fixture")["store"])
    future_loss = F.cross_entropy(model.predict_future(written), torch.tensor([6]))
    future_loss.backward()
    assert model.writer.gate.weight.grad.abs().sum() > 0
    model.zero_grad(set_to_none=True)
    ids = torch.tensor([2, 3, 4, 5, 6, 7, 8, 9])
    mask = torch.tensor([False, False, False, False, True, True, True, True])
    diagnostics = {}
    history = new_history(model, "fixture")
    loss, _, count = window_objective(model, ids, mask, model.initial_memory(1),
        history=history, state_prediction_weight=0.1, diagnostics=diagnostics)
    assert count == 4 and diagnostics["state_pairs"] == 1
    assert abs(loss.item() - (diagnostics["main_ce_sum"] + 0.1 * diagnostics["state_ce_sum"])) < 2e-5
    restored = restore_history(model, history_payload(history))
    assert restored["store"] == history["store"] and restored["segments"] == 2
    masked_stats = {}
    window_objective(model, ids, torch.zeros(8, dtype=torch.bool), model.initial_memory(1),
        history=new_history(model, "masked"), state_prediction_weight=0.1, diagnostics=masked_stats)
    assert masked_stats["state_pairs"] == 0


def test_v2_stream_rejects_missing_generated_origin_and_clock_fields():
    model = small().eval()
    state = ingest(model, start_stream(model), [2, 3], -1, origin="generated")
    payload = stream_payload(state)
    payload.pop("prefix_origins")
    with pytest.raises(ValueError, match="Incomplete"):
        restore_stream(model, payload)


def test_disabled_extension_stream_cannot_downgrade_to_legacy():
    model = small(episodic_enabled=False, semantic_dim=0, dynamics="transformer", predictive_head=False).eval()
    state = ingest(model, start_stream(model), [2, 3], -1)
    payload = stream_payload(state)
    payload.pop("stream_format")
    with pytest.raises(ValueError, match="downgrade"):
        restore_stream(model, payload)
    genuine_v0 = {"memory": state.memory, "prefix": state.prefix}
    restored = restore_stream(model, genuine_v0)
    assert restored.prefix_origins == ("generated", "generated")


def test_writer_is_independent_of_reader_depth_with_full_modules():
    model = small()
    tokens = torch.tensor([[2, 3, 4, 5]])
    memory = model.initial_memory(1)
    first = model.commit_segment(tokens, memory)
    model.config.loop_steps = 7
    second = model.commit_segment(tokens, memory)
    torch.testing.assert_close(first, second, rtol=0, atol=0)


def test_validation_reports_head_ce_separately_and_restores_access_counters(tmp_path):
    # Non-evaluation training bookkeeping fixture: no benchmark score evidence.
    torch.manual_seed(7)
    model = small()
    directory = tmp_path / "validation-corpus"
    with CorpusWriter(directory, {"kind": "software-fixture"}) as writer:
        writer.add("first", [2, 3, 4, 5, 6, 7, 8, 9], loss_start=0)
        writer.add("second", [10, 11, 12, 13], loss_start=0)
    corpus = TokenCorpus(directory)
    model.reset_audit()
    model.audit["raw_tokens_read"] = 123
    expected_audit = dict(model.audit)
    main_only = validation_nll(model, corpus, "cpu", 12)
    composite = validation_nll(model, corpus, "cpu", 12, state_prediction_weight=0.1)
    assert composite["targets"] == 12 and composite["state_pairs"] == 1
    assert composite["nll_per_target"] == pytest.approx(main_only["nll_per_target"])
    assert composite["state_ce_sum"] > 0
    assert composite["objective_per_main_target"] == pytest.approx(
        composite["nll_per_target"] + 0.1 * composite["state_ce_sum"] / 12)
    assert model.audit == expected_audit and model.training
