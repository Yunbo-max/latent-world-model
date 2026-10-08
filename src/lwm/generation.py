"""Functional stream state, exact event receipts, and independent clocks."""
from __future__ import annotations

from dataclasses import dataclass, replace
import math
import torch
from torch import Tensor
from .model import LatentWorldModel
from .episodic import EpisodicStore, ORIGINS, payload_digest


@dataclass(frozen=True)
class StreamState:
    memory: Tensor
    prefix: Tensor
    prefix_origins: tuple[str, ...] = ()
    prefix_sources: tuple[str, ...] = ()
    episodic: EpisodicStore | None = None
    chunk_receipts: tuple[tuple[str, str], ...] = ()
    document_clock: int = 0
    observation_clock: int = 0
    reasoning_clock: int = 0
    expression_clock: int = 0
    segment_clock: int = 0

    def detached(self) -> "StreamState":
        return replace(self, memory=self.memory.detach(), prefix=self.prefix.detach())


def start_stream(model: LatentWorldModel) -> StreamState:
    store = EpisodicStore(model.config.episodic_capacity_tokens) if model.config.episodic_enabled else None
    return StreamState(model.initial_memory(1), torch.empty(
        (1, 0), dtype=torch.long, device=model.embedding.weight.device), episodic=store)


def next_logits(model: LatentWorldModel, state: StreamState) -> Tensor:
    return model.predict_prefix(state.prefix, state.memory, episodic=state.episodic)


def plan_next(model: LatentWorldModel, state: StreamState) -> tuple[Tensor, StreamState]:
    """Advance only reasoning: evidence/store/prefix remain unchanged."""
    plan = model.plan_prefix(state.prefix, state.memory, episodic=state.episodic)
    return plan, replace(state, reasoning_clock=state.reasoning_clock + model.config.loop_steps)


def stream_accounting(state):
    import json
    return {"tensor_state_bytes": state.memory.numel() * state.memory.element_size()
                + state.prefix.numel() * state.prefix.element_size(),
            "chunk_receipt_count": len(state.chunk_receipts),
            "chunk_receipt_serialized_bytes": len(json.dumps(state.chunk_receipts).encode()),
            "episodic": state.episodic.accounting() if state.episodic else None,
            "scope": "serialized payload/tensor bytes; Python heap included only in process RSS"}


def observe(model: LatentWorldModel, state: StreamState, token_id: int,
            eos_token_id: int, origin: str = "observed_text", source_id: str = "anonymous") -> StreamState:
    if (type(token_id) is not int or not 0 <= token_id < model.config.vocab_size or origin not in ORIGINS
            or not isinstance(source_id, str) or not source_id or type(eos_token_id) is not int):
        raise ValueError("Invalid token ID/origin")
    state = replace(state, observation_clock=state.observation_clock + int(origin == "observed_text"),
                    expression_clock=state.expression_clock + int(origin == "generated"))
    if token_id == eos_token_id:
        fresh = start_stream(model)
        doc = state.document_clock + 1
        store = EpisodicStore(model.config.episodic_capacity_tokens, f"stream:{doc}") if state.episodic else None
        return replace(state, memory=fresh.memory, prefix=fresh.prefix, prefix_origins=(), prefix_sources=(),
                       episodic=store, document_clock=doc)
    token = torch.tensor([[token_id]], dtype=torch.long, device=state.prefix.device)
    prefix = torch.cat((state.prefix, token), dim=1)
    origins = state.prefix_origins + (origin,)
    sources = state.prefix_sources + (source_id,)
    if prefix.size(1) == model.config.block_size:
        store = state.episodic
        raw = prefix[0].detach().cpu().tolist() if store is not None else None
        ordinal = store.next_ordinal if store is not None else None
        if store is not None:
            store.check(ordinal, raw, origins, sources)  # admission precedes writer
        memory = model.commit_segment(prefix, state.memory)
        if store is not None:
            store = store.append(ordinal, raw, origins, sources)
        return replace(state, memory=memory, prefix=prefix[:, :0], prefix_origins=(), prefix_sources=(),
                       episodic=store, segment_clock=state.segment_clock + 1)
    if prefix.size(1) > model.config.block_size:
        raise ValueError("Uncommitted stream prefix exceeds segment length")
    return replace(state, prefix=prefix, prefix_origins=origins, prefix_sources=sources)


@torch.no_grad()
def ingest(model: LatentWorldModel, state: StreamState, tokens: list[int],
           eos_token_id: int, *, observation_id: str | None = None,
           origin: str = "observed_text") -> StreamState:
    """Transactional immutable acceptance; stable-ID retries are verified no-ops.

    Without caller identity even identical text is new input. An ID is a source
    locator, not a credential proving factual truth. Receipts grow with history.
    """
    if type(eos_token_id) is not int or origin not in ORIGINS or any(type(t) is not int or not 0 <= t < model.config.vocab_size for t in tokens):
        raise ValueError("Invalid input tokens/origin")
    if not tokens:
        if observation_id is not None:
            raise ValueError("Identified observations must be nonempty")
        return state
    if observation_id is not None and (not isinstance(observation_id, str) or not observation_id):
        raise ValueError("Nonempty caller observation identity required")
    from .data import canonical_hash
    digest = canonical_hash({"format": "lwm-chunk-v1", "payload": payload_digest(tokens, (origin,) * len(tokens)),
                             "eos_token_id": eos_token_id})
    if observation_id is not None:
        for identity, previous in state.chunk_receipts:
            if identity == observation_id:
                if digest != previous:
                    raise ValueError("Conflicting payload for consumed observation ID")
                return state
    # All transitions are functional: failure cannot partially accept the chunk.
    for token in tokens:
        state = observe(model, state, token, eos_token_id, origin, observation_id or "anonymous")
    if observation_id is not None:
        state = replace(state, chunk_receipts=state.chunk_receipts + ((observation_id, digest),))
    return state


def stream_payload(state: StreamState) -> dict:
    return {"stream_format": "lwm-stream-v2", "memory": state.memory.detach().cpu(),
            "prefix": state.prefix.detach().cpu(), "prefix_origins": list(state.prefix_origins),
            "prefix_sources": list(state.prefix_sources),
            "episodic": state.episodic.state_dict() if state.episodic else None,
            "chunk_receipts": [list(r) for r in state.chunk_receipts],
            **{name: getattr(state, name) for name in ("document_clock", "observation_clock", "reasoning_clock",
                                                      "expression_clock", "segment_clock")}}


def restore_stream(model: LatentWorldModel, saved: dict) -> StreamState:
    device = model.embedding.weight.device
    if saved.get("stream_format") not in (None, "lwm-stream-v2"):
        raise ValueError("Unknown stream state format")
    v2_markers = {"model_config", "source_identity", "prefix_origins", "prefix_sources", "episodic",
                  "chunk_receipts", "document_clock", "observation_clock", "reasoning_clock", "expression_clock", "segment_clock"}
    if saved.get("stream_format") is None and v2_markers.intersection(saved):
        raise ValueError("Missing stream format on a v2 payload; no legacy downgrade")
    if saved.get("stream_format") is None and (model.config.episodic_enabled or model.config.semantic_dim
            or model.config.dynamics != "transformer" or model.config.predictive_head):
        raise ValueError("Legacy stream state is only compatible with v0")
    if saved.get("stream_format") == "lwm-stream-v2":
        required = {"memory", "prefix", "prefix_origins", "prefix_sources", "episodic", "chunk_receipts", "document_clock",
                    "observation_clock", "reasoning_clock", "expression_clock", "segment_clock"}
        if not required.issubset(saved):
            raise ValueError("Incomplete v2 stream payload")
    memory, prefix = saved["memory"].to(device), saved["prefix"].to(device)
    model._validate(prefix, memory, empty=True)
    if (prefix.size(0) != 1 or not memory.is_floating_point() or not bool(torch.isfinite(memory).all())
            or bool((memory.abs() > 1).any()) or bool((prefix < 0).any()) or bool((prefix >= model.config.vocab_size).any())):
        raise ValueError("Invalid stream tensors")
    origins = tuple(saved.get("prefix_origins", ["generated"] * prefix.size(1)))
    if len(origins) != prefix.size(1) or any(o not in ORIGINS for o in origins):
        raise ValueError("Invalid partial-prefix provenance")
    sources = tuple(saved.get("prefix_sources", ["legacy-anonymous"] * prefix.size(1)))
    if len(sources) != prefix.size(1) or any(not isinstance(s, str) or not s for s in sources):
        raise ValueError("Invalid partial-prefix source locators")
    raw_store = saved.get("episodic")
    if bool(raw_store is not None) != model.config.episodic_enabled:
        raise ValueError("Saved episodic state/model mismatch")
    store = EpisodicStore.from_state_dict(raw_store, vocab_size=model.config.vocab_size,
        event_length=model.config.block_size) if raw_store is not None else None
    if store is not None and store.capacity_tokens != model.config.episodic_capacity_tokens:
        raise ValueError("Saved exact-memory capacity differs")
    receipts = tuple(tuple(r) for r in saved.get("chunk_receipts", []))
    if (any(len(r) != 2 or not isinstance(r[0], str) or not r[0] or not isinstance(r[1], str)
            or len(r[1]) != 64 or any(c not in "0123456789abcdef" for c in r[1]) for r in receipts)
            or len({r[0] for r in receipts}) != len(receipts)):
        raise ValueError("Invalid chunk replay receipts")
    clocks = {name: saved.get(name, 0) for name in ("document_clock", "observation_clock", "reasoning_clock", "expression_clock", "segment_clock")}
    if any(type(v) is not int or v < 0 for v in clocks.values()):
        raise ValueError("Invalid three-clock counters")
    if store is not None and (store.document_id != f"stream:{clocks['document_clock']}"
                              or store.next_ordinal > clocks["segment_clock"]):
        raise ValueError("Episodic document/segment clock differs")
    return StreamState(memory=memory, prefix=prefix, prefix_origins=origins, prefix_sources=sources,
                       episodic=store, chunk_receipts=receipts, **clocks)


@torch.no_grad()
def score_continuation(model: LatentWorldModel, state: StreamState,
                       tokens: list[int], eos_token_id: int,
                       trace: list[dict] | None = None) -> tuple[float, bool]:
    """Native sum of target log probabilities; conditional targets are history."""
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
        # A known likelihood-prefix target is neither external evidence nor a
        # generated fact. Its source remains distinct if a segment is committed.
        state = observe(model, state, int(token), eos_token_id, "scored_continuation")
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
        if model.config.semantic_dim:
            plan, state = plan_next(model, state)
            logits = model.realize_plan(plan, last_only=True)[0, -1].float()
        else:
            logits = next_logits(model, state)[0].float()
            state = replace(state, reasoning_clock=state.reasoning_clock + model.config.loop_steps)
        if not bool(torch.isfinite(logits).all()):
            raise FloatingPointError("Nonfinite generation logits")
        if temperature == 0:
            token = int(logits.argmax().item())
        else:
            token = int(torch.multinomial((logits / temperature).softmax(-1), 1,
                                          generator=generator).item())
        produced.append(token)
        state = observe(model, state, token, eos_token_id, "generated")
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
    from .realization import implementation_identity

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
    parser.add_argument("--observation-id", help="Replay-safe caller identity for the prompt chunk")
    parser.add_argument("--plan-out", help="Save an explicit pre-generation plan for independent realization")
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
        if saved.get("stream_format") == "lwm-stream-v2":
            if saved.get("model_config") != model.config.to_dict() or saved.get("source_identity") != implementation_identity():
                raise ValueError("Stream model configuration/source differs")
        state = restore_stream(model, saved)
        if saved.get("sampling_device_type") != torch.device(args.device).type:
            raise ValueError("Sampling RNG resume requires the same device type")
        if saved.get("temperature") != args.temperature:
            raise ValueError("Resume must preserve the sampling temperature")
        random_generator.set_state(saved["sampling_rng"])
    # Supplied text is data, even if it literally spells the EOS marker.
    prompt_ids = tokenizer.encode(args.prompt, add_special_tokens=False, split_special_tokens=False)
    state = ingest(model, state, prompt_ids, eos_token_id=-1, observation_id=args.observation_id)
    if args.plan_out:
        from .realization import plan_snapshot
        with torch.no_grad():
            plan, state = plan_next(model, state)
        save_checkpoint(args.plan_out, plan_snapshot(model, state, plan, checkpoint_hash, identity))
    tokens, continuation = generate(model, state, args.max_new_tokens, tokenizer.eos_token_id,
                                    args.temperature, random_generator)
    if args.state_out:
        save_checkpoint(args.state_out, {"kind": "text-stream", "model_checkpoint_sha256": checkpoint_hash,
            "tokenizer": identity, **stream_payload(continuation),
            "model_config": model.config.to_dict(), "source_identity": implementation_identity(),
            "state_semantics": "functional branch; generated provenance retained",
            "sampling_rng": random_generator.get_state().cpu(), "temperature": args.temperature,
            "sampling_device_type": torch.device(args.device).type})
    print(json.dumps({"text": tokenizer.decode(tokens, skip_special_tokens=True), "token_ids": tokens,
                      "checkpoint_sha256": checkpoint_hash, "state_out": args.state_out}, ensure_ascii=False))


if __name__ == "__main__":
    main()

