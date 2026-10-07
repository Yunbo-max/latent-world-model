"""Source-authored engineering contracts; Local execution is required."""
import copy
import pytest
from latent_world_model.assets import acquire_model
from latent_world_model.io import read_json, sha256_file, write_json, resolve_checkpoint
from latent_world_model.evaluation import compare_inventories, validate_predictions


@pytest.mark.parametrize("changed", ["tokenizer.json", "model.safetensors"])
@pytest.mark.parametrize("tokenizer_only", [False, True])
def test_reacquisition_rejects_changed_receipted_bytes(tmp_path, monkeypatch, changed, tokenizer_only):
    import huggingface_hub
    directory = tmp_path / "assets/smollm2"
    directory.mkdir(parents=True)
    names = ["tokenizer.json", "model.safetensors"]
    for name in names:
        (directory / name).write_bytes(b"original fixture")
    receipt = {"repo": "fixture", "revision": "1" * 40, "files": {
        n: {"bytes": (directory / n).stat().st_size, "sha256": sha256_file(directory / n)} for n in names}}
    write_json(directory / "acquisition.json", receipt)
    write_json(tmp_path / "sources.json", {"models": {"smollm2": {
        **receipt, "tokenizer_files": names[:1], "model_files": names[1:]}}})
    (directory / changed).write_bytes(b"changed fixture!")
    def unexpected_download(**_):
        pytest.fail("Corruption must be detected before acquisition")
    monkeypatch.setattr(huggingface_hub, "snapshot_download", unexpected_download)
    with pytest.raises(ValueError, match="integrity"):
        acquire_model("smollm2", tmp_path / "sources.json", tmp_path / "assets", tokenizer_only)
    assert read_json(directory / "acquisition.json") == receipt


def test_unpublished_checkpoint_generation_does_not_replace_committed_state(tmp_path):
    committed = tmp_path / "checkpoint-committed.pt"
    committed.write_bytes(b"committed fixture")
    write_json(tmp_path / "checkpoint.json", {"path": committed.name, "sha256": sha256_file(committed)})
    (tmp_path / "checkpoint-unpublished.pt").write_bytes(b"interrupted later save")
    assert resolve_checkpoint(tmp_path) == committed
    committed.write_bytes(b"corrupted")
    with pytest.raises(ValueError, match="hash"):
        resolve_checkpoint(tmp_path)


def test_frozen_inventory_rejects_changed_or_missing_task():
    frozen = {"format": "lwm-native-inventory-v2", "tasks": {"task": {"denominator": 2}},
              "source_config_sha256": "fixture", "split_mode": "published"}
    for changed in [{**frozen, "tasks": {}}, {**frozen, "split_mode": "development"}]:
        with pytest.raises(ValueError, match="inventory"):
            compare_inventories(frozen, changed)
    changed = copy.deepcopy(frozen)
    changed["tasks"]["task"]["denominator"] = 1
    with pytest.raises(ValueError, match="inventory"):
        compare_inventories(frozen, changed)


def test_prediction_ids_and_documents_must_match_frozen_rows():
    from latent_world_model.io import canonical_hash
    rows = [{"native_row_index": i, "doc_sha256": canonical_hash({"x": i})} for i in range(2)]
    records = [{"doc_id": i, "doc": {"x": i}} for i in range(2)]
    validate_predictions(records, rows)
    for invalid in [records[:1], [records[0], records[0]], [records[1], {"doc_id": 0, "doc": {"x": 99}}]]:
        with pytest.raises(ValueError):
            validate_predictions(invalid, rows)
