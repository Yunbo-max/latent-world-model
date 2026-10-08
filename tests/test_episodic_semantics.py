"""Local software acceptance, not scientific evaluation. Web has not run it."""
import pytest
import torch

from lwm.episodic import EpisodicStore
from lwm.model import ModelConfig, LatentWorldModel
from lwm.generation import start_stream, ingest, generate, next_logits, stream_payload, restore_stream


def tiny(**extra):
    return LatentWorldModel(ModelConfig(vocab_size=31, d_model=16, n_heads=2,
        ffn_mult=2, block_size=4, memory_slots=2, prelude_layers=1, core_layers=1,
        coda_layers=1, loop_steps=2, episodic_enabled=True, episodic_capacity_tokens=8,
        episodic_read_tokens=8, episodic_top_k=2, episodic_query_tokens=3, **extra))


def test_evicted_identity_replay_cannot_resurrect_or_conflict():
    store = EpisodicStore(4)
    origins = ("observed_text",) * 4
    store = store.append(0, (1, 2, 3, 4), origins).append(1, (5, 6, 7, 8), origins)
    assert store.evicted_events == 1 and [e.ordinal for e in store.events] == [1]
    assert store.append(0, (1, 2, 3, 4), origins) is store
    with pytest.raises(ValueError, match="Conflicting"):
        store.append(0, (1, 2, 3, 9), origins)
    with pytest.raises(ValueError, match="consecutive"):
        store.append(3, (1, 2, 3, 4), origins)
    restored = EpisodicStore.from_state_dict(store.state_dict(), vocab_size=31, event_length=4)
    assert restored == store


def test_mixed_provenance_filters_generated_positions_before_ranking():
    store = EpisodicStore(8).append(0, (1, 2, 3, 4),
        ("observed_text", "generated", "observed_text", "generated"))
    selected, _ = store.retrieve([2], 2, 8, "lexical")
    assert [item[0] for item in selected] == [1, 3]
    assert [item[1] for item in selected] == [0, 2]
    all_selected, _ = store.retrieve([2], 2, 8, "lexical", include_generated=True)
    assert [item[0] for item in all_selected] == [1, 2, 3, 4]


@pytest.mark.parametrize("cached", [False, True])
@pytest.mark.parametrize("include_generated,scans,wanted", [
    (False, 1, [1, 3]), (True, 2, [1, 3, 2, 4]),
])
def test_query_scan_cost_counts_only_candidates_visible_under_source_policy(cached, include_generated, scans, wanted):
    # Catches billing filtered-out events on every query, while still billing
    # the raw tokens visited once when constructing the source-filtered index.
    store = EpisodicStore(8).append(0, (1, 3), ("observed_text",) * 2)
    store = store.append(1, (2, 4), ("generated",) * 2)
    index = store.index(include_generated) if cached else None
    selected, cost = store.retrieve([1], 2, 8, "lexical", include_generated, index=index)
    assert [item[0] for item in selected] == wanted
    assert cost["events_scanned"] == scans
    assert cost["index_tokens_scanned"] == (0 if cached else 4)


def test_generated_only_history_has_no_per_row_query_scans():
    model = tiny().eval()
    prefix = torch.tensor([[1, 2]])
    memory = model.initial_memory(1)
    store = EpisodicStore(8).append(0, (3, 4, 5, 6), ("generated",) * 4)
    model.reset_audit()
    actual = model.predict_prefix(prefix, memory, episodic=store)
    assert model.audit["query_positions"] == 3
    assert model.audit["events_scanned"] == 0
    assert model.audit["index_tokens_scanned"] == 4
    assert model.audit["raw_tokens_read"] == 0
    expected = model.predict_prefix(prefix, memory, episodic=EpisodicStore(8))
    torch.testing.assert_close(actual, expected)


def test_causal_retrieval_teacher_prefix_parity_and_real_gradient():
    torch.manual_seed(7)
    model = tiny().eval()
    store = EpisodicStore(8).append(0, (2, 4, 6, 8), ("observed_text",) * 4)
    memory = model.initial_memory(1)
    tokens = torch.tensor([[2, 3, 5, 7]])
    logits, _ = model.forward_segment(tokens, memory, episodic=store)
    for u in range(4):
        prefix = model.predict_prefix(tokens[:, :u], memory, episodic=store)
        torch.testing.assert_close(prefix, logits[:, u], atol=2e-6, rtol=2e-5)
    changed = tokens.clone()
    changed[:, 2:] = torch.tensor([[11, 13]])
    altered, _ = model.forward_segment(changed, memory, episodic=store)
    torch.testing.assert_close(altered[:, :3], logits[:, :3], atol=2e-6, rtol=2e-5)
    empty_logits, _ = model.forward_segment(tokens, memory, episodic=EpisodicStore(8))
    assert not torch.allclose(logits, empty_logits)
    logits.square().sum().backward()
    assert model.episodic_reader.attention.v.weight.grad.abs().sum() > 0


def test_identified_chunk_retry_is_atomic_across_commits_and_partial_restore():
    model = tiny().eval()
    initial = start_stream(model)
    ids = [1, 2, 3, 4, 5, 6]
    state = ingest(model, initial, ids, -1, observation_id="source:chunk-0")
    assert len(state.episodic.events) == 1 and state.prefix.tolist() == [[5, 6]]
    duplicate = ingest(model, state, ids, -1, observation_id="source:chunk-0")
    assert duplicate is state
    with pytest.raises(ValueError, match="Conflicting"):
        ingest(model, state, ids + [7], -1, observation_id="source:chunk-0")
    with pytest.raises(ValueError):
        ingest(model, state, [1, 999], -1, observation_id="bad")
    assert state.prefix.tolist() == [[5, 6]] and initial.prefix.numel() == 0
    restored = restore_stream(model, stream_payload(state))
    torch.testing.assert_close(next_logits(model, restored), next_logits(model, state))
    assert restored.episodic == state.episodic and restored.chunk_receipts == state.chunk_receipts


def test_generation_branch_never_relabels_generated_history_as_observation():
    model = tiny().eval()
    state = ingest(model, start_stream(model), [1, 2, 3], -1, observation_id="prompt")
    _, branch = generate(model, state, 2, eos_token_id=-1)
    assert state.prefix.tolist() == [[1, 2, 3]] and not state.episodic.events
    assert "generated" in branch.episodic.events[0].origins
    assert branch.observation_clock == state.observation_clock
    assert branch.expression_clock == state.expression_clock + 2
    assert branch.reasoning_clock == state.reasoning_clock + 2 * model.config.loop_steps


def test_document_reset_drops_raw_events_without_forgetting_chunk_retry():
    model = tiny().eval()
    state = ingest(model, start_stream(model), [1, 2, 3, 4, 30], 30, observation_id="doc0")
    assert not state.episodic.events and state.episodic.next_ordinal == 0
    assert state.document_clock == 1
    assert ingest(model, state, [1, 2, 3, 4, 30], 30, observation_id="doc0") is state
