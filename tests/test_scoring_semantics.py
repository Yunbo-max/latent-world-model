"""Authored acceptance contracts; generated_unexecuted, not native qualification.

The text fixture is an actual pinned ParlAI example. Numeric rows below are
engineering aggregation inputs, never advertised as benchmark observations.
Full native LAMBADA/ParlAI checks are conditional on explicitly supplied assets.
"""
from __future__ import annotations

import json
import math
import os
from pathlib import Path

import pytest

from lwm.scoring import (
    LAMBADA_SHA256,
    aggregate_babi,
    aggregate_lambada,
    babi_exact_match,
    lambada_context_target,
    load_dataset,
    normalize_answer,
    paired_bootstrap,
    factorial_bootstrap,
    replay_native,
    validate_predictions,
)


# Source: ParlAI a29567f7ce76992fd1f03c51ba9e3b155a37ea51,
# parlai/tasks/babi/test/babi_all10k_test.yml, first actual test act.
BABI_NATIVE_CONTEXT = (
    "John travelled to the hallway.\n"
    "Mary journeyed to the bathroom.\n"
    "Where is John?"
)


def test_parlai_normalization_accepts_formatting_of_actual_native_answer():
    """Catches removal, rather than replacement, of native punctuation."""
    assert normalize_answer("The HALLWAY.") == "hallway"
    assert babi_exact_match("The HALLWAY.", ["hallway"]) == 1
    assert babi_exact_match("bathroom", ["hallway"]) == 0
    assert babi_exact_match("", ["hallway"]) == 0
    assert babi_exact_match(None, ["hallway"]) == 0


def test_parlai_normalization_replaces_punctuation_without_reordering():
    """A list sorter or substring scorer must not receive credit."""
    # Reuses tokens from the source-cited act; this is a scorer contract only.
    assert normalize_answer("hallway,bathroom") == "hallway bathroom"
    assert babi_exact_match("bathroom hallway", ["hallway bathroom"]) == 0
    assert babi_exact_match("hallway bathroom", ["hallway"]) == 0


def test_lambada_native_perplexity_uses_mean_example_ll_not_subtoken_count():
    """Changing to token-weighted normalization must fail this numeric case."""
    rows = [
        {"log_likelihood": -math.log(2), "is_greedy": True,
         "target_token_count": 1},
        {"log_likelihood": -math.log(8), "is_greedy": False,
         "target_token_count": 3},
    ]
    result = aggregate_lambada(rows)
    assert result["acc"] == 0.5
    assert result["perplexity"] == pytest.approx(4.0)
    assert result["examples"] == 2


def test_babi_numeric_summary_uses_strict_five_percent_failure_boundary():
    # Numerical aggregation fixture only: never a native benchmark substitute.
    rows = [{"task_id": task, "exact_match": int(index >= ({1: 1, 2: 2}.get(task, 0)))}
            for task in range(1, 21) for index in range(20)]
    result = aggregate_babi(rows)
    assert result["macro_accuracy"] == pytest.approx(0.9925)
    assert result["mean_error"] == pytest.approx(0.0075)
    assert result["failed_tasks_error_gt_0_05"] == 1
    with pytest.raises(ValueError):
        aggregate_babi([row for row in rows if row["task_id"] != 20])


@pytest.mark.parametrize("row", [
    {"log_likelihood": float("nan"), "is_greedy": True},
    {"log_likelihood": float("inf"), "is_greedy": True},
    {"log_likelihood": -1.0, "is_greedy": "false"},
    {"log_likelihood": True, "is_greedy": True},
])
def test_lambada_rejects_coercible_invalid_native_outputs(row):
    with pytest.raises(ValueError):
        aggregate_lambada([row])


def test_lambada_perplexity_overflow_is_not_clipped_to_a_finite_result():
    result = aggregate_lambada([
        {"log_likelihood": -1000.0, "is_greedy": False},
    ])
    assert result["perplexity"] is None
    assert result["perplexity_status"] == "overflow"


def test_lambada_rejects_an_empty_denominator():
    with pytest.raises(ValueError):
        aggregate_lambada([])


def _engineering_rows():
    # Pure numeric paired-analysis input, not a substitute bAbI dataset.
    return [
        {"id": "engineering:a", "task": "babi", "task_id": 1,
         "episode_id": "engineering:episode-1", "input_sha256": "a" * 64,
         "exact_match": 0, "native_labels": ["hallway"]},
        {"id": "engineering:b", "task": "babi", "task_id": 1,
         "episode_id": "engineering:episode-1", "input_sha256": "b" * 64,
         "exact_match": 1, "native_labels": ["hallway"]},
        {"id": "engineering:c", "task": "babi", "task_id": 1,
         "episode_id": "engineering:episode-2", "input_sha256": "c" * 64,
         "exact_match": 0, "native_labels": ["hallway"]},
    ]


def test_paired_bootstrap_keeps_questions_nested_within_native_episode():
    left = _engineering_rows()
    right = [{**row, "exact_match": 1} for row in left]
    result = paired_bootstrap(left, right, "babi", iterations=100, seed=3)
    assert result["resampling_unit"] == "episode_within_task"
    assert result["clusters"] == 2
    assert result["examples"] == 3
    assert result["delta_right_minus_left"] == pytest.approx(2 / 3)


def test_factorial_interaction_uses_shared_units_and_correct_sign():
    # Algebra/aggregation fixture, not generated benchmark observations.
    base = _engineering_rows()
    ones = [{**row, "exact_match": 1} for row in base]
    zeros = [{**row, "exact_match": 0} for row in base]
    result = factorial_bootstrap(ones, zeros, zeros, ones, "babi", iterations=100, seed=3)
    assert result["interaction"] == 2
    assert result["confidence_interval"] == [2, 2]
    assert result["clusters"] == 2 and result["examples"] == 3
    null = factorial_bootstrap(base, base, base, base, "babi", iterations=100, seed=3)
    assert null["interaction"] == 0 and null["confidence_interval"] == [0, 0]
    with pytest.raises(ValueError):
        factorial_bootstrap(ones, zeros[:-1], zeros, ones, "babi", iterations=100)


@pytest.mark.parametrize("fault", ["missing", "duplicate", "input", "episode"])
def test_paired_comparison_rejects_incomplete_or_different_examples(fault):
    left = _engineering_rows()
    right = [dict(row) for row in left]
    if fault == "missing":
        right.pop()
    elif fault == "duplicate":
        right.append(dict(right[0]))
    elif fault == "input":
        right[0]["input_sha256"] = "d" * 64
    else:
        right[0]["episode_id"] = "different"
    with pytest.raises(ValueError):
        paired_bootstrap(left, right, "babi", iterations=10, seed=1)


def test_prediction_join_never_shrinks_denominator_on_missing_or_extra_ids():
    from lwm.scoring import row_fingerprint

    native = [{"id": "engineering:a", "context": BABI_NATIVE_CONTEXT}]
    correct = [{"id": "engineering:a", "task": "babi",
                "input_sha256": row_fingerprint(native[0])}]
    assert len(validate_predictions(native, correct, "babi")) == 1
    with pytest.raises(ValueError):
        validate_predictions(native, [], "babi")
    with pytest.raises(ValueError):
        validate_predictions(native, correct + correct, "babi")
    with pytest.raises(ValueError):
        validate_predictions(native, [{**correct[0], "id": "extra"}], "babi")


def test_lambada_split_on_real_full_native_source_is_qualified_locally():
    location = os.environ.get("LWM_NATIVE_LAMBADA_DATA")
    if not location:
        pytest.skip("pending Local: set LWM_NATIVE_LAMBADA_DATA to pinned full data")
    dataset = load_dataset(Path(location), "lambada")
    assert len(dataset.rows) == 5153
    assert dataset.manifest["source"]["sha256"] == LAMBADA_SHA256
    row = dataset.rows[0]
    context, target = lambada_context_target(row["text"])
    # Row 0 target confirmed by the actual HF dataset row preview cited in
    # research/DATA_PROTOCOL_PROPOSAL.md section 6, not an invented passage.
    assert target == " signs"
    assert context.endswith("I don't care about")
    assert context + target == row["text"]


@pytest.mark.parametrize("encoded,context_ids,target_ids", [
    ([0, 7, 8], [0], [7, 8]),
    ([7, 8], [0], [7, 8]),
])
def test_empty_context_does_not_score_an_existing_prefix_token(encoded, context_ids, target_ids):
    # Software token-boundary fixture, not scientific benchmark input. Adding a
    # second prefix and scoring the first as a target would violate TemplateLM.
    from lwm.scoring import encode_hf_pair

    class Tokenizer:
        eos_token_id = 0

        def encode(self, text, **kwargs):
            return encoded

    actual = encode_hf_pair(Tokenizer(), "", "fixture")
    assert actual["context_token_ids"] == context_ids
    assert actual["target_token_ids"] == target_ids


def test_empty_context_with_only_prefix_is_rejected_as_empty_target():
    from lwm.scoring import encode_hf_pair

    class Tokenizer:
        eos_token_id = 0

        def encode(self, text, **kwargs):
            return [0]

    with pytest.raises(ValueError, match="empty context/target"):
        encode_hf_pair(Tokenizer(), "", "fixture")


def test_real_native_lambada_pairs_match_the_pinned_harness_token_boundary():
    """Pending Local test: actual source rows, tokenizer bytes and author code."""
    paths = {name: os.environ.get(f"LWM_NATIVE_LAMBADA_{name.upper()}")
             for name in ("data", "source", "tokenizer")}
    if not all(paths.values()):
        pytest.skip("pending Local: supply LWM_NATIVE_LAMBADA_DATA/SOURCE/TOKENIZER")
    import importlib
    import inspect
    import sys

    from lwm.prepare import load_tokenizer
    from lwm.scoring import encode_hf_pair, verify_native_source

    source = Path(verify_native_source(paths["source"], "lambada")["path"])
    dataset = load_dataset(paths["data"], "lambada")
    tokenizer = load_tokenizer(paths["tokenizer"])
    old_path = list(sys.path)
    sys.path.insert(0, str(source))
    try:
        official = importlib.import_module("lm_eval.api.model").TemplateLM
        assert Path(inspect.getfile(official)).resolve().is_relative_to(source)

        class NativeTokenizerAdapter:
            # The pinned causal TemplateLM pair helper only requires tok_encode
            # and backend. It does not load model weights or invoke a forward.
            backend = "causal"

            @staticmethod
            def tok_encode(text, **kwargs):
                return tokenizer.encode(text, add_special_tokens=False,
                                        split_special_tokens=False, truncation=False)

        for row in dataset.rows:
            context, target = lambada_context_target(row["text"])
            assert context, "A native empty context needs a separate upstream prefix-token qualification"
            expected_context, expected_target = official._encode_pair(
                NativeTokenizerAdapter(), context, target)
            actual = encode_hf_pair(tokenizer, context, target)
            assert actual["context_token_ids"] == expected_context
            assert actual["target_token_ids"] == expected_target
    finally:
        sys.path[:] = old_path


@pytest.mark.parametrize("task,env_prefix", [
    ("babi", "LWM_NATIVE_BABI"), ("lambada", "LWM_NATIVE_LAMBADA"),
])
def test_pinned_official_scorer_replay_requires_complete_actual_assets(task, env_prefix):
    """This cannot pass from handcrafted fixtures or an absent native checkout."""
    paths = {name: os.environ.get(f"{env_prefix}_{name.upper()}")
             for name in ("data", "predictions", "source")}
    if not all(paths.values()):
        pytest.skip(f"pending Local: supply {env_prefix}_DATA/PREDICTIONS/SOURCE")
    dataset = load_dataset(Path(paths["data"]), task)
    predictions = [json.loads(line) for line in
                   Path(paths["predictions"]).read_text().splitlines()]
    result = replay_native(dataset, predictions, Path(paths["source"]))
    assert result["native_aggregation_replay"] == "passed"
    assert result["examples"] == len(dataset.rows)
    assert result["model_adapter_parity"] == "pending_local"
