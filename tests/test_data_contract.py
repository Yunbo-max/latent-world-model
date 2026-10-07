"""Engineering fixtures only: these arrays are never benchmark examples."""
import numpy as np
import pytest
from latent_world_model.data import TokenBlocks, count_targets, validate_corpus
from latent_world_model.io import sha256_file, write_json


def make_corpus(tmp_path, count=21):
    path = tmp_path / "tokens.bin"
    np.arange(count, dtype="<u4").tofile(path)
    (tmp_path / "documents.jsonl").write_text('{"fixture": true}\n')
    write_json(tmp_path / "manifest.json", {
        "format": "lwm-token-corpus-v1", "dtype": "<u4",
        "document_index_sha256": sha256_file(tmp_path / "documents.jsonl"),
        "files": {"train": {"path": "tokens.bin", "tokens": count,
                            "sha256": sha256_file(path)}},
        "tokenizer": {"repo": "fixture", "revision": "0" * 40},
    })
    return tmp_path / "manifest.json"


def test_blocks_shift_once_and_cover_every_target(tmp_path):
    manifest = make_corpus(tmp_path)
    blocks = TokenBlocks(manifest, "train", seq_len=8, target_tokens=19)
    pairs = [blocks[i] for i in range(len(blocks))]
    targets = [y[y != -100].tolist() for _, y in pairs]
    assert sum(targets, []) == list(range(1, 20))
    for x, y in pairs:
        valid = y != -100
        assert np.array_equal(y[valid], x[valid] + 1)
    assert count_targets(pairs[-1][1]) == 3


def test_nondivisible_token_budget_and_exhaustion(tmp_path):
    manifest = make_corpus(tmp_path)
    blocks = TokenBlocks(manifest, "train", seq_len=8, target_tokens=20)
    assert len(blocks) == 3
    assert count_targets(blocks[2][1]) == 4
    with pytest.raises(ValueError, match="available"):
        TokenBlocks(manifest, "train", seq_len=8, target_tokens=21)
    with pytest.raises(IndexError):
        blocks[3]


def test_mutated_input_fails_integrity(tmp_path):
    manifest = make_corpus(tmp_path)
    validate_corpus(manifest)
    with (tmp_path / "tokens.bin").open("r+b") as stream:
        stream.write(b"xxxx")
    with pytest.raises(ValueError, match="hash"):
        validate_corpus(manifest)


def test_invalid_block_size_and_budget(tmp_path):
    manifest = make_corpus(tmp_path)
    for seq, budget in [(0, 10), (8, 0), (-1, 5)]:
        with pytest.raises(ValueError):
            TokenBlocks(manifest, "train", seq_len=seq, target_tokens=budget)
