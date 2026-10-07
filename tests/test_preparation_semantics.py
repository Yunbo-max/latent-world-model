"""Local acceptance specifications; authored without executing project code.

Synthetic fixtures below check serialization, not benchmark qualification.
The release procedure must also verify the complete pinned native assets.
"""
import hashlib
import io
import tarfile

import pytest

from lwm.data import TokenCorpus
from lwm.prepare import (
    FineWebBuilder,
    content_key,
    encode_document,
    git_blob_sha1,
    iter_babi_examples,
    lambada_document,
    load_assets,
    safe_extract_archive,
    serialize_babi_sft,
    split_for_key,
    verify_asset,
)


class ByteTokenizer:
    """A deterministic fixture tokenizer, never a replacement for pinned GPT-2."""

    eos_token_id = 50256

    def encode(self, text, *, add_special_tokens=False, split_special_tokens=False):
        assert add_special_tokens is False
        if "<|endoftext|>" in text and not split_special_tokens:
            return [self.eos_token_id]
        return list(text.encode("utf-8"))


def test_asset_manifest_is_pinned_and_source_bound_is_complete():
    assets = load_assets()
    assert assets["tokenizer"]["revision"] == "607a30d783dfa663caf39e06633721c8d4cfcd7e"
    source = assets["fineweb"]
    assert len(source["files"]) == 14
    assert sum(f["bytes"] for f in source["files"]) == 28_518_193_415
    assert source["source_byte_limit"] == 30_000_000_000
    assert assets["babi"]["splits"]["test"]["examples"] == 20_000
    assert assets["lambada"]["examples"] == 5_153


def test_git_blob_identity_and_asset_content_tampering(tmp_path):
    path = tmp_path / "vocab.json"
    path.write_bytes(b"abc")
    expected = hashlib.sha1(b"blob 3\0abc").hexdigest()
    assert git_blob_sha1(path) == expected
    spec = {"path": "vocab.json", "bytes": 3, "git_blob_sha1": expected}
    identity = verify_asset(path, spec)
    assert identity["sha256"] == hashlib.sha256(b"abc").hexdigest()
    path.write_bytes(b"abd")
    with pytest.raises(ValueError, match="identity"):
        verify_asset(path, spec)


def test_content_hash_normalizes_only_the_split_key():
    assert content_key("Cafe\u0301\n story") == content_key("Caf\u00e9 story")
    assert split_for_key("0000000000000000" + "0" * 48) == "valid"
    assert split_for_key("0000000000000032" + "0" * 48) == "test"
    assert split_for_key("0000000000000064" + "0" * 48) == "train"
    assert encode_document(ByteTokenizer(), "a\n b") == [97, 10, 32, 98, 50256]


def test_literal_special_token_is_ordinary_text_with_one_appended_eos():
    ids = encode_document(ByteTokenizer(), "a <|endoftext|> b")
    assert ids[:-1] == list(b"a <|endoftext|> b")
    assert ids.count(50256) == 1


def rows_for_splits():
    groups = {name: [] for name in ("train", "valid", "test")}
    i = 0
    while any(len(group) < 3 for group in groups.values()):
        text = f"fixture document {i}"
        split = split_for_key(content_key(text))
        if len(groups[split]) < 3:
            groups[split].append({"id": f"source-{i}", "text": text})
        i += 1
    return [row for group in groups.values() for row in group]


def build_fixture(directory, train_tokens):
    budgets = {"train": train_tokens, "valid": 11, "test": 13}
    source = {"path": "fixed.parquet", "sha256": "a" * 64, "bytes": 1}
    with FineWebBuilder(directory, ByteTokenizer(), budgets, {"test_fixture": True}) as builder:
        for row_number, row in enumerate(rows_for_splits()):
            builder.add_row(row, source, row_number)
        builder.finish()
    return {split: TokenCorpus(directory / split) for split in budgets}


def test_exact_budgets_heldouts_and_nested_training_prefix(tmp_path):
    small = build_fixture(tmp_path / "small", 9)
    large = build_fixture(tmp_path / "large", 37)
    assert small["train"].ids.tolist() == large["train"].ids[:9].tolist()
    for split, count in (("train", 9), ("valid", 11), ("test", 13)):
        assert small[split].manifest["targets"] == count
    for split in ("valid", "test"):
        assert small[split].ids.tolist() == large[split].ids.tolist()
    sets = [{r["metadata"]["content_sha256"] for r in small[s].records}
            for s in ("train", "valid", "test")]
    assert all(not sets[a].intersection(sets[b]) for a, b in ((0, 1), (0, 2), (1, 2)))
    tail = small["train"].records[-1]["metadata"]
    assert tail["truncated_tail"] and not tail["terminal_eos_included"]


def test_dedup_and_incomplete_budget_never_publish_corpus(tmp_path):
    text = next(row["text"] for row in rows_for_splits()
                if split_for_key(content_key(row["text"])) == "train")
    source = {"path": "fixed.parquet", "sha256": "b" * 64, "bytes": 1}
    with pytest.raises(ValueError, match="Insufficient"):
        with FineWebBuilder(tmp_path / "incomplete", ByteTokenizer(),
                            {"train": 1000, "valid": 1, "test": 1}, {}) as builder:
            builder.add_row({"text": text}, source, 0)
            builder.add_row({"text": text + " "}, source, 1)
            assert builder.stats["duplicate_documents"] == 1
            builder.finish()
    assert not (tmp_path / "incomplete" / "train" / "manifest.json").exists()


def test_babi_teacher_turns_history_and_answer_only_loss(tmp_path):
    source = tmp_path / "qa8_train.txt"
    source.write_text(
        "1 Mary went to the kitchen.\n"
        "2 John went to the office.\n"
        "3 Where is Mary?\tkitchen\n"
        "4 Mary picked up the apple.\n"
        "5 What is Mary carrying?\tapple,milk\n"
        "1 Daniel went to the garden.\n"
        "2 Where is Daniel?\tgarden\n", encoding="utf-8")
    rows = list(iter_babi_examples(source, task_id=8, split="train", archive_sha256="c" * 64))
    assert len(rows) == 3
    first, second, third = rows
    assert first["episode_id"] == second["episode_id"] != third["episode_id"]
    assert not first["episode_done"] and second["episode_done"] and third["episode_done"]
    assert second["new_facts"] == ["Mary picked up the apple."]
    assert second["native_text"] == "Mary picked up the apple.\nWhat is Mary carrying?"
    assert "Where is Mary?" not in second["context"]
    assert "kitchen\n" not in second["context"]  # no preceding gold reply
    assert second["answer"] == "apple milk"
    ids, loss_start = serialize_babi_sft(ByteTokenizer(), second)
    assert ids[:loss_start] == list(second["context"].encode("utf-8"))
    assert ids[loss_start:] == list(b" apple milk") + [50256]


def test_babi_question_detection_uses_labels_and_rejects_unlabeled_tail(tmp_path):
    path = tmp_path / "qa1_test.txt"
    path.write_text("1 A fact?\n2 A request without question mark\tyes\n", encoding="utf-8")
    row, = list(iter_babi_examples(path, task_id=1, split="test", archive_sha256="d" * 64))
    assert row["new_facts"] == ["A fact?"]
    assert row["question"] == "A request without question mark"
    path.write_text("1 An unanswered fact.\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unlabeled"):
        list(iter_babi_examples(path, task_id=1, split="test", archive_sha256="d" * 64))


def test_lambada_preserves_literal_space_boundary_and_every_source_field():
    row = lambada_document({"text": "Some  words signs", "extra": "retained"}, 7, "e" * 64)
    assert row["context"] == "Some  words"
    assert row["target"] == " signs"
    assert row["source_document"] == {"text": "Some  words signs", "extra": "retained"}
    trailing = lambada_document({"text": "word "}, 8, "e" * 64)
    assert trailing["context"] == "word" and trailing["target"] == " "
    empty = lambada_document({"text": ""}, 9, "e" * 64)
    assert empty["text"] == "" and empty["target"] == " "


@pytest.mark.parametrize("kind,name", [("file", "../escape"), ("file", "/absolute"),
                                      ("symlink", "link"), ("hardlink", "link")])
def test_archive_rejects_escape_and_link_members(tmp_path, kind, name):
    archive = tmp_path / "bad.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        member = tarfile.TarInfo(name)
        if kind == "file":
            member.size = 1
            tar.addfile(member, io.BytesIO(b"x"))
        else:
            member.type = tarfile.SYMTYPE if kind == "symlink" else tarfile.LNKTYPE
            member.linkname = "../escape"
            tar.addfile(member)
    with pytest.raises(ValueError, match="Unsafe"):
        safe_extract_archive(archive, tmp_path / "unpacked", max_bytes=1024)
    assert not (tmp_path / "escape").exists()


def test_archive_checks_declared_total_before_extracting(tmp_path):
    archive = tmp_path / "large.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        member = tarfile.TarInfo("safe/file.txt")
        member.size = 4
        tar.addfile(member, io.BytesIO(b"data"))
    with pytest.raises(ValueError, match="limit"):
        safe_extract_archive(archive, tmp_path / "unpacked", max_bytes=3)
    assert not (tmp_path / "unpacked" / "safe" / "file.txt").exists()
