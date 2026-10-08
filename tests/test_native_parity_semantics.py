"""Generated, unexecuted software contracts; fixtures are not native results."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path

import pytest

from lwm.native_parity import compare_babi_records, iter_export, run, verify_snapshot
from lwm.scoring import sha256_file


def records():
    # The text is the first act in the pinned ParlAI babi_all10k_test.yml.
    text = "John travelled to the hallway.\nMary journeyed to the bathroom.\nWhere is John?"
    row = {"id": "software-fixture", "native_text": text,
           "native_labels": ["hallway"], "native_reward": 0.0,
           "episode_done": True, "episode_index": 0, "episode_turn": 0}
    message = {"text": text, "labels": ["hallway"], "episode_done": True}
    return [row], [(1, message)]


def test_babi_record_comparison_preserves_exact_fields_and_default_zero_reward():
    rows, messages = records()
    assert compare_babi_records(rows, messages, "fixture") == {"examples": 1, "episodes": 1}


@pytest.mark.parametrize("field,value", [
    ("native_text", "changed"), ("native_labels", ["bathroom"]),
    ("native_reward", 1.0), ("episode_done", False),
    ("episode_index", 1), ("episode_turn", 1),
])
def test_babi_record_comparison_rejects_each_semantic_mismatch(field, value):
    rows, messages = records()
    rows[0][field] = value
    with pytest.raises(ValueError, match="fixture"):
        compare_babi_records(rows, messages, "fixture")


@pytest.mark.parametrize("delta", [-1, 1])
def test_babi_record_comparison_rejects_missing_or_extra_rows(delta):
    rows, messages = records()
    messages = [] if delta < 0 else messages + copy.deepcopy(messages)
    with pytest.raises(ValueError):
        compare_babi_records(rows, messages, "fixture")


@pytest.mark.parametrize("value", [float("nan"), float("inf"), True, "0"])
def test_babi_record_comparison_rejects_invalid_reward(value):
    rows, messages = records()
    messages[0][1]["reward"] = value
    with pytest.raises(ValueError):
        compare_babi_records(rows, messages, "fixture")


def test_babi_record_comparison_checks_multi_turn_episode_order():
    rows, messages = records()
    rows = rows + copy.deepcopy(rows) + copy.deepcopy(rows)
    messages = messages + copy.deepcopy(messages) + copy.deepcopy(messages)
    rows[0]["episode_done"] = messages[0][1]["episode_done"] = False
    rows[1]["episode_turn"] = 1
    rows[2]["episode_index"] = 1
    assert compare_babi_records(rows, messages, "fixture") == {"examples": 3, "episodes": 2}
    rows[2]["episode_index"] = 0
    with pytest.raises(ValueError, match="episode_index"):
        compare_babi_records(rows, messages, "fixture")


@pytest.mark.parametrize("text", [
    "text:a\ttext:b\tlabels:c\n",
    "text:a\tlabels:c\tepisode_done:False\n",
    "text:a\tlabels:c\tbroken\n",
    "\n",
])
def test_export_rejects_noncanonical_structure_before_native_parser(tmp_path, text):
    path = tmp_path / "invalid.txt"
    path.write_text(text)
    def must_not_parse(_):
        raise AssertionError("Malformed structure reached the native parser")
    with pytest.raises(ValueError):
        list(iter_export(path, must_not_parse))


def test_native_parity_failure_is_retained_without_success_receipt(tmp_path):
    output = tmp_path / "result"
    with pytest.raises(FileNotFoundError):
        run(tmp_path / "absent-data", tmp_path / "absent-exports",
            tmp_path / "absent-source", output)
    failure = json.loads((output / "failure.json").read_text())
    assert failure["status"] == "failed"
    assert failure["completed_tasks"] == []
    assert not (output / "babi-teacher-parity.json").exists()
    with pytest.raises(FileExistsError):
        run(tmp_path, tmp_path, tmp_path, output)


@pytest.mark.parametrize("ending", ["\n\n", "\n", "\n\n\n"])
def test_export_requires_exactly_one_final_episode_separator(tmp_path, ending):
    path = tmp_path / "export.txt"
    path.write_text("text:first\tlabels:a\ntext:second\tlabels:b\tepisode_done:True" + ending)
    def parser_fixture(line):
        # Test only iteration/separators. Actual escaping/parser parity is the
        # conditional full-native test, which imports the real pinned author.
        return {"episode_done": "episode_done:True" in line}
    if ending == "\n\n":
        assert [number for number, _ in iter_export(path, parser_fixture)] == [1, 2]
    else:
        with pytest.raises(ValueError, match="separator"):
            list(iter_export(path, parser_fixture))


@pytest.mark.parametrize("mutation", ["prepared", "export", "inventory"])
def test_final_snapshot_rejects_late_input_changes(tmp_path, mutation):
    # Real file I/O checks publication integrity, never native task coverage.
    exports = tmp_path / "exports"
    exports.mkdir()
    prepared = tmp_path / "prepared.jsonl"
    exported = exports / "task-1-test.txt"
    prepared.write_text("original prepared bytes")
    exported.write_text("original exported bytes")
    files = {path: sha256_file(path) for path in (prepared, exported)}
    expected = {exported.name}
    verify_snapshot(files, exports, expected)
    if mutation == "inventory":
        (exports / "unexpected.txt").write_text("extra")
    else:
        (prepared if mutation == "prepared" else exported).write_text("changed")
    with pytest.raises(ValueError, match="changed"):
        verify_snapshot(files, exports, expected)


def test_full_native_babi_teacher_exports_match_preparation_locally(tmp_path):
    names = ("LWM_NATIVE_BABI_DATA", "LWM_NATIVE_BABI_EXPORTS", "LWM_NATIVE_BABI_SOURCE")
    values = [os.environ.get(name) for name in names]
    if not all(values):
        pytest.skip("Full native preparation, all 60 author exports and pinned ParlAI source required")
    result = run(*(Path(value) for value in values), tmp_path / "native-parity")
    assert result["native_data_parity"] == "passed"
    assert result["examples"] == 220000
    assert len(result["completed_tasks"]) == 60
    assert result["model_adapter_parity"] == "pending_local"
