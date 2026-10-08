"""Unexecuted Local acceptance checks for actual training pause/resume behavior.

These tiny CPU/float32 fixtures are software checks, not experiments or benchmark
results. The Web author has not imported or executed this file/project.
Local command pending: python -m pytest tests/test_resume_semantics.py
"""

from copy import deepcopy
from pathlib import Path
import hashlib
import json
import random
import signal

import numpy as np
import pytest
import torch

from lwm import train
from lwm.checkpoint import capture_rng, load_checkpoint, restore_rng, save_checkpoint
from lwm.data import CorpusWriter


@pytest.fixture(autouse=True)
def isolated_cpu_runtime():
    """Keep tiny CPU operations repeatable and leave other tests' globals intact."""
    rng = capture_rng()
    threads = torch.get_num_threads()
    torch.set_num_threads(1)
    try:
        yield
    finally:
        restore_rng(rng)
        torch.set_num_threads(threads)


def _write_corpus(path, *, first_token=3):
    # EOS is token 2. Documents remain separate and contain no padding.
    # The pause at target 4 retains live first-document memory; target 8 closes
    # that document; budget 12 ends at offset 4 of the second document.
    with CorpusWriter(path, {"kind": "local-software-fixture", "eos_token_id": 2}) as writer:
        writer.add("first", [first_token, 4, 5, 6, 7, 8, 9, 2], loss_start=0)
        writer.add("second", [10, 11, 12, 13, 14, 2], loss_start=0)


@pytest.fixture
def training_case(tmp_path):
    config = {
        "stage": "software_acceptance",
        "model": {
            "vocab_size": 23,
            "d_model": 16,
            "n_heads": 2,
            "ffn_mult": 2,
            "block_size": 2,
            "memory_slots": 2,
            "prelude_layers": 1,
            "core_layers": 1,
            "coda_layers": 1,
            "loop_steps": 2,
            "dropout": 0.0,
            "checkpoint_layers": False,
            "memory_enabled": True,
        },
        "training": {
            "token_budget": 12,
            "unroll_segments": 2,
            "accumulate_targets": 4,
            "learning_rate": 0.001,
            "min_lr_ratio": 0.1,
            "warmup_tokens": 0,
            "weight_decay": 0.01,
            "clip_grad_norm": 1.0,
            "seed": 149,
            "precision": "float32",
            "repeat": False,
            "shuffle": False,
            "max_run_seconds": 600,
            "max_skipped_updates": 0,
            "checkpoint_every_updates": 1,
            "validation_every_updates": 100,
            "validation_targets": 4,
        },
    }
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")
    data_path = tmp_path / "corpus"
    _write_corpus(data_path)
    return {"config": config, "config_path": config_path, "data_path": data_path}


def _run(case, output, *, resume=None, max_updates=None, config_path=None, data_path=None):
    argv = [
        "--config", str(config_path or case["config_path"]),
        "--data", str(data_path or case["data_path"]),
        "--output", str(output),
        "--device", "cpu",
    ]
    if resume is not None:
        argv.extend(["--resume", str(resume)])
    if max_updates is not None:
        argv.extend(["--max-updates", str(max_updates)])
    train.main(argv)


def _assert_nested_equal(left, right, location="checkpoint"):
    if isinstance(left, torch.Tensor):
        assert isinstance(right, torch.Tensor), location
        torch.testing.assert_close(left, right, rtol=0, atol=0, msg=location)
    elif isinstance(left, dict):
        assert isinstance(right, dict) and left.keys() == right.keys(), location
        for key in left:
            _assert_nested_equal(left[key], right[key], f"{location}.{key}")
    elif isinstance(left, (tuple, list)):
        assert type(left) is type(right) and len(left) == len(right), location
        for index, (first, second) in enumerate(zip(left, right)):
            _assert_nested_equal(first, second, f"{location}[{index}]")
    else:
        assert left == right, location


def _assert_equivalent_training_state(first, second):
    # Wall time and explicit resume provenance are the only permitted differences.
    for field in set(first) | set(second):
        if field in {"resumed_from", "counters"}:
            continue
        _assert_nested_equal(first[field], second[field], field)
    first_counts = {key: value for key, value in first["counters"].items()
                    if key != "cumulative_seconds"}
    second_counts = {key: value for key, value in second["counters"].items()
                     if key != "cumulative_seconds"}
    _assert_nested_equal(first_counts, second_counts, "counters")


def _updates(output):
    events = [json.loads(line) for line in
              (output / "events.jsonl").read_text(encoding="utf-8").splitlines()]
    return [event for event in events if event["event"] == "update"]


@pytest.fixture
def paused_run(training_case, tmp_path):
    output = tmp_path / "paused"
    _run(training_case, output, max_updates=1)
    checkpoint = load_checkpoint(output / "last.pt")
    assert checkpoint["status"] == "paused"
    assert checkpoint["counters"]["updates"] == 1
    assert checkpoint["counters"]["seen_targets"] == 4
    assert checkpoint["memory"] is not None
    return output, checkpoint


def test_pause_resume_matches_uninterrupted_training_at_live_memory_boundary(
    training_case, paused_run, tmp_path
):
    # Catches omitted memory/cursor/AdamW state, lost targets, or changing the
    # optimizer grouping when a run is paused and resumed.
    resumed_output, paused = paused_run
    paused_path = resumed_output / "last.pt"
    paused_bytes = paused_path.read_bytes()
    assert paused["cursor"]["document_position"] == 0
    assert paused["cursor"]["token_offset"] == 4
    assert paused["memory"].shape == (1, 2, 16)
    assert not paused["memory"].requires_grad
    assert paused["counters"]["optimized_targets"] == 4
    assert paused["counters"]["input_tokens"] == 4
    assert paused["optimizer_state"]["state"], "the checkpoint must include AdamW moments"

    uninterrupted_output = tmp_path / "uninterrupted"
    _run(training_case, uninterrupted_output)
    _run(training_case, resumed_output, resume=paused_path)
    uninterrupted = load_checkpoint(uninterrupted_output / "last.pt")
    resumed = load_checkpoint(resumed_output / "last.pt")

    _assert_equivalent_training_state(uninterrupted, resumed)
    assert resumed["status"] == "completed_target_budget"
    assert {key: value for key, value in resumed["counters"].items()
            if key != "cumulative_seconds"} == {
        "seen_targets": 12,
        "optimized_targets": 12,
        "input_tokens": 12,
        "updates": 3,
        "skipped_updates": 0,
        "auxiliary_target_observations": 0,
    }
    assert resumed["cursor"]["document_position"] == 1
    assert resumed["cursor"]["token_offset"] == 4
    assert resumed["memory"] is not None
    assert [event["targets_this_update"] for event in _updates(resumed_output)] == [4, 4, 4]
    assert [event["targets_this_update"] for event in _updates(uninterrupted_output)] == [4, 4, 4]
    # The input checkpoint's identity must remain frozen even though this path
    # is replaced by subsequent checkpoints during the resumed invocation.
    assert resumed["resumed_from"] == {
        "path": str(paused_path.resolve()),
        "sha256": hashlib.sha256(paused_bytes).hexdigest(),
    }
    assert not (resumed_output / "run.lock").exists()


def test_expanded_training_resume_preserves_events_and_auxiliary_budget(training_case, tmp_path):
    """Real trainer CPU fixture; authored, not executed by Web."""
    config = deepcopy(training_case["config"])
    config["model"].update(episodic_enabled=True, episodic_capacity_tokens=4,
        episodic_read_tokens=4, episodic_top_k=2, episodic_query_tokens=2,
        semantic_dim=8, dynamics="contractive", contraction_bound=0.8, predictive_head=True)
    config["training"]["state_prediction_weight"] = 0.1
    path = tmp_path / "expanded.json"
    path.write_text(json.dumps(config), encoding="utf-8")
    paused_output, ordinary_output = tmp_path / "expanded-resumed", tmp_path / "expanded-ordinary"
    _run(training_case, paused_output, max_updates=1, config_path=path)
    paused_path = paused_output / "last.pt"
    paused = load_checkpoint(paused_path)
    assert paused["history"]["segments"] == 2
    assert len(paused["history"]["store"]["receipts"]) == 2
    assert paused["counters"]["auxiliary_target_observations"] == 1
    _run(training_case, ordinary_output, config_path=path)
    _run(training_case, paused_output, resume=paused_path, config_path=path)
    ordinary, resumed = load_checkpoint(ordinary_output / "last.pt"), load_checkpoint(paused_output / "last.pt")
    _assert_equivalent_training_state(ordinary, resumed)
    assert resumed["counters"]["seen_targets"] == 12
    assert resumed["counters"]["auxiliary_target_observations"] == 4
    assert resumed["history"]["segments"] == 2
    assert resumed["history"]["store"]["document_id"] != paused["history"]["store"]["document_id"]


def test_resume_restores_nondefault_saved_rng_streams(training_case, paused_run, tmp_path):
    # A deterministic, dropout-free run would accidentally pass an RNG equality
    # check even without restoration, because reinitialization repeats its draws.
    # Give a valid paused checkpoint distinct RNG states to test the real loader.
    _, paused = paused_run
    random.seed(991)
    np.random.seed(997)
    torch.manual_seed(1009)
    random.random()
    np.random.random(5)
    torch.rand(7)
    saved_rng = capture_rng()
    modified = deepcopy(paused)
    modified["rng"] = saved_rng
    checkpoint_path = tmp_path / "nondefault-rng.pt"
    save_checkpoint(checkpoint_path, modified)

    random.seed(3)
    np.random.seed(5)
    torch.manual_seed(7)
    output = tmp_path / "rng-resumed"
    _run(training_case, output, resume=checkpoint_path)

    # This v0 CPU path has no random operations after restoring the checkpoint.
    _assert_nested_equal(load_checkpoint(output / "last.pt")["rng"], saved_rng, "rng")


@pytest.mark.parametrize("incompatibility", ["configuration", "corpus", "source"])
def test_incompatible_resume_is_rejected_without_writing_a_run(
    training_case, paused_run, tmp_path, incompatibility
):
    # Catches resuming a different objective, token corpus, or source revision.
    paused_output, paused = paused_run
    original_path = paused_output / "last.pt"
    original_bytes = original_path.read_bytes()
    resume_path = original_path
    config_path = training_case["config_path"]
    data_path = training_case["data_path"]
    if incompatibility == "configuration":
        changed = deepcopy(training_case["config"])
        changed["training"]["learning_rate"] = 0.002
        config_path = tmp_path / "changed-config.json"
        config_path.write_text(json.dumps(changed), encoding="utf-8")
    elif incompatibility == "corpus":
        data_path = tmp_path / "different-corpus"
        _write_corpus(data_path, first_token=16)
    else:
        changed = deepcopy(paused)
        changed["source_identity"]["train.py"] = "0" * 64
        resume_path = tmp_path / "different-source.pt"
        save_checkpoint(resume_path, changed)

    output = tmp_path / "rejected-child"
    with pytest.raises(ValueError):
        _run(training_case, output, resume=resume_path,
             config_path=config_path, data_path=data_path)

    assert original_path.read_bytes() == original_bytes
    assert not (output / "last.pt").exists()
    assert not (output / "events.jsonl").exists()
    assert not (output / "run.lock").exists()


def test_older_checkpoint_cannot_overwrite_a_newer_output(
    training_case, paused_run, tmp_path
):
    # Catches loading an old/external checkpoint and silently rewinding a run.
    output, _ = paused_run
    checkpoint_path = output / "last.pt"
    older_path = tmp_path / "older.pt"
    older_path.write_bytes(checkpoint_path.read_bytes())
    _run(training_case, output, resume=checkpoint_path, max_updates=1)
    newer = load_checkpoint(checkpoint_path)
    assert newer["status"] == "paused"
    assert newer["counters"]["seen_targets"] == 8
    assert newer["counters"]["updates"] == 2
    preserved = {name: (output / name).read_bytes()
                 for name in ("last.pt", "events.jsonl", "status.json")}
    assert preserved["last.pt"] != older_path.read_bytes()

    with pytest.raises(ValueError):
        _run(training_case, output, resume=older_path)

    for name, contents in preserved.items():
        assert (output / name).read_bytes() == contents
    assert not (output / "run.lock").exists()


def test_completed_budget_cannot_be_resumed_as_a_fresh_run(training_case, tmp_path):
    # Catches an apparent successful resume that has no remaining work/checkpoint.
    output = tmp_path / "completed"
    _run(training_case, output)
    checkpoint_path = output / "last.pt"
    assert load_checkpoint(checkpoint_path)["status"] == "completed_target_budget"
    original_bytes = checkpoint_path.read_bytes()
    attempted_output = tmp_path / "completed-resume"

    with pytest.raises(ValueError):
        _run(training_case, attempted_output, resume=checkpoint_path)

    assert checkpoint_path.read_bytes() == original_bytes
    assert not (attempted_output / "last.pt").exists()
    assert not (attempted_output / "run.lock").exists()


def test_log_setup_failure_releases_lock_and_restores_handlers(training_case, tmp_path, monkeypatch):
    output = tmp_path / "log-open-failure"
    original_open = Path.open
    handlers = {sig: signal.getsignal(sig) for sig in (signal.SIGINT, signal.SIGTERM)}

    def deny_log_open(path, *args, **kwargs):
        if path == output / "events.jsonl":
            raise PermissionError("software fixture log failure")
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", deny_log_open)
    with pytest.raises(PermissionError, match="software fixture"):
        _run(training_case, output)
    assert not (output / "run.lock").exists()
    assert {sig: signal.getsignal(sig) for sig in handlers} == handlers


@pytest.mark.parametrize("maximum", [0, -1])
def test_max_updates_must_be_positive(training_case, tmp_path, maximum):
    # Catches a zero/negative feasibility limit silently performing an update.
    output = tmp_path / "invalid-limit"
    with pytest.raises(SystemExit) as error:
        _run(training_case, output, max_updates=maximum)
    assert error.value.code == 2
    assert not (output / "last.pt").exists()


def test_stop_request_waits_for_the_normal_accumulation_boundary(
    training_case, tmp_path, monkeypatch
):
    # Catches flushing partial gradients on SIGTERM, which changes AdamW updates
    # and makes a resumed run differ from an uninterrupted one.
    config = deepcopy(training_case["config"])
    config["training"]["accumulate_targets"] = 8
    config_path = tmp_path / "accumulate-eight.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")
    ordinary_output = tmp_path / "ordinary-boundary"
    _run(training_case, ordinary_output, config_path=config_path, max_updates=1)

    original_signal = train.signal.signal
    original_objective = train.window_objective
    installed_handlers = {}
    windows_seen = 0

    def record_real_handler(signum, handler):
        installed_handlers[signum] = handler
        return original_signal(signum, handler)

    def request_stop_after_first_real_window(*args, **kwargs):
        nonlocal windows_seen
        result = original_objective(*args, **kwargs)
        windows_seen += 1
        if windows_seen == 1:
            # Invoke the production handler; do not send an operating-system signal.
            installed_handlers[signal.SIGTERM](signal.SIGTERM, None)
        return result

    interrupted_output = tmp_path / "requested-stop"
    with monkeypatch.context() as patched:
        patched.setattr(train.signal, "signal", record_real_handler)
        patched.setattr(train, "window_objective", request_stop_after_first_real_window)
        _run(training_case, interrupted_output, config_path=config_path)

    ordinary = load_checkpoint(ordinary_output / "last.pt")
    interrupted = load_checkpoint(interrupted_output / "last.pt")
    _assert_equivalent_training_state(ordinary, interrupted)
    assert interrupted["status"] == "paused"
    assert interrupted["counters"]["seen_targets"] == 8
    assert interrupted["counters"]["optimized_targets"] == 8
    assert interrupted["counters"]["updates"] == 1
    assert [event["targets_this_update"] for event in _updates(interrupted_output)] == [8]
    assert not (interrupted_output / "run.lock").exists()

