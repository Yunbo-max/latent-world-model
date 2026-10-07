"""Local software acceptance only; these fixtures are not scientific benchmarks."""
import json

import numpy as np

from lwm.data import CorpusWriter, TokenCorpus, CorpusCursor


def corpus(tmp_path):
    with CorpusWriter(tmp_path, {"tokenizer_revision": "test-fixture"}) as writer:
        writer.add("a", [3, 4, 5, 2], loss_start=0)
        writer.add("b", [8, 9, 10, 11, 2], loss_start=3)
    return TokenCorpus(tmp_path)


def test_cursor_resume_and_target_budget_preserve_context(tmp_path):
    source = corpus(tmp_path)
    cursor = CorpusCursor(source, seed=7, shuffle=False)
    first = cursor.take_window(3, max_targets=2)
    assert first.ids.tolist() == [3, 4]
    assert first.reset_before and not first.ended_document
    restored = CorpusCursor(source, seed=7, shuffle=False)
    restored.load_state_dict(json.loads(json.dumps(cursor.state_dict())))
    for c in (cursor, restored):
        rest = c.take_window(8, max_targets=1)
        assert rest.ids.tolist() == [5]
        assert not rest.reset_before
        assert c.take_window(8).ids.tolist() == [2]
        supervised = c.take_window(8, max_targets=1)
        assert supervised.ids.tolist() == [8, 9, 10, 11]
        assert supervised.loss_mask.tolist() == [False, False, False, True]
        assert supervised.reset_before and not supervised.ended_document


def test_cursor_never_joins_documents(tmp_path):
    cursor = CorpusCursor(corpus(tmp_path), seed=7, shuffle=False)
    assert cursor.take_window(100).ids.tolist() == [3, 4, 5, 2]
    assert cursor.take_window(100).ids.tolist() == [8, 9, 10, 11, 2]
    assert cursor.exhausted


def test_manifest_detects_changed_token_bytes(tmp_path):
    corpus(tmp_path)
    with (tmp_path / "tokens.bin").open("r+b") as f:
        f.write(np.array([99], dtype="<u2").tobytes())
    import pytest
    with pytest.raises(ValueError, match="hash"):
        TokenCorpus(tmp_path)
