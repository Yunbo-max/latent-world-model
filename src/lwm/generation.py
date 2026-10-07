"""Functional stream state. Generated continuations operate on a caller branch."""
from __future__ import annotations

from dataclasses import dataclass
import math

import torch
from torch import Tensor

from .model import LatentWorldModel


@dataclass(frozen=True)
class StreamState:
    memory: Tensor
    prefix: Tensor

    def detached(self) -> "StreamState":
        return StreamState(self.memory.detach(), self.prefix.detach())


def start_stream(model: LatentWorldModel) -> StreamState:
    return StreamState(model.initial_memory(1), torch.empty(
        (1, 0), dtype=torch.long, device=model.embedding.weight.device))


def next_logits(model: LatentWorldModel, state: StreamState) -> Tensor:
    return model.predict_prefix(state.prefix, state.memory)


def observe(model: LatentWorldModel, state: StreamState, token_id: int,
            eos_token_id: int) -> StreamState:
    if not 0 <= token_id < model.config.vocab_size:
        raise ValueError("Token ID outside vocabulary")
    if token_id == eos_token_id:
        return start_stream(model)
    token = torch.tensor([[token_id]], dtype=torch.long, device=state.prefix.device)
    prefix = torch.cat((state.prefix, token), dim=1)
    if prefix.size(1) == model.config.block_size:
        return StreamState(model.commit_segment(prefix, state.memory), prefix[:, :0])
    if prefix.size(1) > model.config.block_size:
        raise ValueError("Uncommitted stream prefix exceeds segment length")
    return StreamState(state.memory, prefix)


@torch.no_grad()
def ingest(model: LatentWorldModel, state: StreamState, tokens: list[int],
           eos_token_id: int) -> StreamState:
    """Consume accepted observations without an unnecessary language readout."""
    for token in tokens:
        state = observe(model, state, int(token), eos_token_id)
    return state


@torch.no_grad()
def score_continuation(model: LatentWorldModel, state: StreamState,
                       tokens: list[int], eos_token_id: int,
                       trace: list[dict] | None = None) -> tuple[float, bool]:
    """Native loglikelihood primitive: sum target log-probabilities and greedy flag."""
    if not tokens:
        raise ValueError("Continuation must contain at least one token")
    total, greedy = 0.0, True
    for token in tokens:
        if not 0 <= token < model.config.vocab_size:
            raise ValueError("Continuation token outside vocabulary")
        logits = next_logits(model, state)[0].float()
        if not bool(torch.isfinite(logits).all()):
            raise FloatingPointError("Nonfinite continuation logits")
        probability = float(logits.log_softmax(-1)[token].item())
        argmax = int(logits.argmax().item())
        total += probability
        greedy = greedy and argmax == token
        if trace is not None:
            trace.append({"token_id": int(token), "log_probability": probability,
                          "argmax_token_id": argmax})
        state = observe(model, state, int(token), eos_token_id)
    return total, greedy


@torch.no_grad()
def generate(model: LatentWorldModel, state: StreamState, max_new_tokens: int,
             eos_token_id: int, temperature: float = 0.0,
             generator: torch.Generator | None = None) -> tuple[list[int], StreamState]:
    if max_new_tokens < 0 or not math.isfinite(temperature) or temperature < 0:
        raise ValueError("Generation limits must be nonnegative")
    if model.training:
        raise ValueError("Call model.eval() before generation")
    produced = []
    for _ in range(max_new_tokens):
        logits = next_logits(model, state)[0].float()
        if not bool(torch.isfinite(logits).all()):
            raise FloatingPointError("Nonfinite generation logits")
        if temperature == 0:
            token = int(logits.argmax().item())
        else:
            token = int(torch.multinomial((logits / temperature).softmax(-1), 1,
                                          generator=generator).item())
        produced.append(token)
        state = observe(model, state, token, eos_token_id)
        if token == eos_token_id:
            break
    return produced, state


def main(argv=None):
    import argparse
    import json
    from .checkpoint import load_checkpoint, save_checkpoint
    from .data import file_sha256
    from .model import ModelConfig
    from .prepare import load_tokenizer, tokenizer_identity

    parser = argparse.ArgumentParser(description="Generate from a trained checkpoint with resumable text-history state")
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--tokenizer", required=True)
    parser.add_argument("--prompt", default="")
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--max-new-tokens", type=int, default=64)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--state-in")
    parser.add_argument("--state-out")
    args = parser.parse_args(argv)
    checkpoint_data = load_checkpoint(args.checkpoint)
    model = LatentWorldModel(ModelConfig(**checkpoint_data["model_config"]))
    model.load_state_dict(checkpoint_data["model_state"], strict=True)
    model = model.to(args.device).eval()
    tokenizer = load_tokenizer(args.tokenizer)
    identity = tokenizer_identity(args.tokenizer)
    expected_tokenizer = checkpoint_data["corpus_provenance"].get("tokenizer")
    if expected_tokenizer != identity:
        raise ValueError("Checkpoint/tokenizer identity mismatch")
    checkpoint_hash = file_sha256(args.checkpoint)
    state = start_stream(model)
    random_generator = torch.Generator(device=args.device).manual_seed(args.seed)
    if args.state_in:
        saved = load_checkpoint(args.state_in)
        if saved.get("kind") != "text-stream" or saved["model_checkpoint_sha256"] != checkpoint_hash:
            raise ValueError("Stream state belongs to another checkpoint or format")
        if saved["tokenizer"] != identity:
            raise ValueError("Stream tokenizer differs")
        state = StreamState(saved["memory"].to(args.device), saved["prefix"].to(args.device))
        model._validate(state.prefix, state.memory, empty=True)
        if state.prefix.size(1) >= model.config.block_size:
            raise ValueError("Saved stream contains an uncommitted complete segment")
        if saved.get("sampling_device_type") != torch.device(args.device).type:
            raise ValueError("Sampling RNG resume requires the same device type")
        if saved.get("temperature") != args.temperature:
            raise ValueError("Resume must preserve the sampling temperature")
        random_generator.set_state(saved["sampling_rng"])
    # Supplied text is data, even if it literally spells the EOS marker.
    prompt_ids = tokenizer.encode(args.prompt, add_special_tokens=False, split_special_tokens=False)
    state = ingest(model, state, prompt_ids, eos_token_id=-1)
    tokens, continuation = generate(model, state, args.max_new_tokens, tokenizer.eos_token_id,
                                    args.temperature, random_generator)
    if args.state_out:
        save_checkpoint(args.state_out, {"kind": "text-stream", "model_checkpoint_sha256": checkpoint_hash,
            "tokenizer": identity, "memory": continuation.memory.detach().cpu(),
            "prefix": continuation.prefix.detach().cpu(), "state_semantics": "includes generated text history",
            "sampling_rng": random_generator.get_state().cpu(), "temperature": args.temperature,
            "sampling_device_type": torch.device(args.device).type})
    print(json.dumps({"text": tokenizer.decode(tokens, skip_special_tokens=True), "token_ids": tokens,
                      "checkpoint_sha256": checkpoint_hash, "state_out": args.state_out}, ensure_ascii=False))


if __name__ == "__main__":
    main()
