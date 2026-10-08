"""Authored Local checks for checkpoint byte identities; unexecuted by Web.

Real file replacement and deserialization stay in the fixture. Tokenizer doubles
only avoid external assets; these are software checks, never benchmark evidence.
"""
import hashlib
import json

import pytest
import torch

from lwm import checkpoint, generation, prepare, realization
from lwm.model import LatentWorldModel, ModelConfig


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _replace_after_load(monkeypatch, path, replacement):
    original = torch.load
    replaced = False

    def replace_once(file, *args, **kwargs):
        nonlocal replaced
        result = original(file, *args, **kwargs)
        name = getattr(file, "name", file)
        if str(name) == str(path) and not replaced:
            replaced = True
            checkpoint.save_checkpoint(path, replacement)
        return result

    monkeypatch.setattr(torch, "load", replace_once)


def test_checkpoint_digest_names_opened_bytes_after_atomic_path_replacement(tmp_path, monkeypatch):
    # Reopening the path to derive identity after load would name replacement B.
    path = tmp_path / "last.pt"
    checkpoint.save_checkpoint(path, {"version": "A", "value": torch.tensor([1.0])})
    expected = _sha(path)
    _replace_after_load(monkeypatch, path, {"version": "B", "value": torch.tensor([2.0])})
    loaded, digest = checkpoint.load_checkpoint_with_sha256(path)
    assert loaded["version"] == "A" and digest == expected
    assert digest != _sha(path)


def test_checkpoint_rejects_in_place_change_during_deserialization(tmp_path, monkeypatch):
    # A stable descriptor protects os.replace, but in-place edits must fail.
    path, other = tmp_path / "last.pt", tmp_path / "other.pt"
    checkpoint.save_checkpoint(path, {"version": "A"})
    checkpoint.save_checkpoint(other, {"version": "B"})
    changed_bytes = other.read_bytes()
    original = torch.load

    def mutate(file, *args, **kwargs):
        result = original(file, *args, **kwargs)
        path.write_bytes(changed_bytes)
        return result

    monkeypatch.setattr(torch, "load", mutate)
    with pytest.raises(ValueError, match="changed during loading"):
        checkpoint.load_checkpoint_with_sha256(path)


class _Tokenizer:
    eos_token_id = 0

    def encode(self, text, **kwargs):
        return [2, 3, 4, 5] if text else []

    def decode(self, tokens, **kwargs):
        return "fixture"


@pytest.mark.parametrize("entry", ["generation", "realization"])
def test_inference_outputs_keep_loaded_checkpoint_identity(tmp_path, monkeypatch, entry):
    # A late path hash either mislabels generated state or rejects a valid A plan.
    config = ModelConfig(vocab_size=19, d_model=16, n_heads=2, block_size=4,
        memory_slots=2, prelude_layers=1, core_layers=1, coda_layers=1,
        loop_steps=2, semantic_dim=8)
    model = LatentWorldModel(config).eval()
    tokenizer_identity = {"fixture": "same-tokenizer"}
    payload = {"model_config": config.to_dict(), "model_state": model.state_dict(),
               "corpus_provenance": {"tokenizer": tokenizer_identity}}
    path = tmp_path / "last.pt"
    checkpoint.save_checkpoint(path, payload)
    expected = _sha(path)
    replacement = dict(payload, model_state={name: tensor + 0.125 for name, tensor in payload["model_state"].items()})
    monkeypatch.setattr(prepare, "load_tokenizer", lambda path: _Tokenizer())
    monkeypatch.setattr(prepare, "tokenizer_identity", lambda path: tokenizer_identity)
    if entry == "realization":
        state = generation.ingest(model, generation.start_stream(model), [2, 3, 4, 5], -1)
        with torch.no_grad():
            plan, state = generation.plan_next(model, state)
        plan_path = tmp_path / "plan.pt"
        checkpoint.save_checkpoint(plan_path,
            realization.plan_snapshot(model, state, plan, expected, tokenizer_identity))
    _replace_after_load(monkeypatch, path, replacement)
    args = ["--checkpoint", str(path), "--tokenizer", str(tmp_path / "tokenizer"), "--device", "cpu"]
    if entry == "generation":
        state_path = tmp_path / "stream.pt"
        generation.main(args + ["--prompt", "fixture", "--max-new-tokens", "0", "--state-out", str(state_path)])
        saved = checkpoint.load_checkpoint(state_path)
        assert saved["model_checkpoint_sha256"] == expected
        with pytest.raises(ValueError, match="another checkpoint"):
            generation.main(args + ["--state-in", str(state_path), "--max-new-tokens", "0"])
    else:
        output = tmp_path / "realized"
        realization.main(args + ["--plan", str(plan_path), "--output", str(output)])
        assert json.loads((output / "manifest.json").read_text())["model_checkpoint_sha256"] == expected
    assert _sha(path) != expected
