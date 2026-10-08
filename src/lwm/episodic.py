"""Immutable exact-token events, bounded raw history, and replay receipts.

No neural keys or future labels. Raw history is bounded; digest receipts grow
with consumed events and are accounted separately. Generated source, unexecuted.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import hashlib
import json


ORIGINS = ("observed_text", "generated", "scored_continuation")


def payload_digest(tokens, origins, sources=None) -> str:
    if not tokens or len(tokens) != len(origins):
        raise ValueError("Nonempty tokens with one origin per token required")
    if any(type(t) is not int or t < 0 for t in tokens) or any(o not in ORIGINS for o in origins):
        raise ValueError("Invalid token/origin payload")
    sources = tuple(sources) if sources is not None else ("unspecified",) * len(tokens)
    if len(sources) != len(tokens) or any(not isinstance(s, str) or not s for s in sources):
        raise ValueError("One nonempty source locator per token required")
    payload = {"canonicalization": "lwm-event-v1", "tokens": list(tokens), "origins": list(origins), "sources": list(sources)}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


@dataclass(frozen=True)
class Event:
    ordinal: int
    tokens: tuple[int, ...]
    origins: tuple[str, ...]
    digest: str
    sources: tuple[str, ...]


@dataclass(frozen=True)
class EpisodicStore:
    capacity_tokens: int
    document_id: str = "stream:0"
    events: tuple[Event, ...] = ()
    receipts: tuple[str, ...] = ()
    evicted_events: int = 0

    def __post_init__(self):
        if type(self.capacity_tokens) is not int or self.capacity_tokens <= 0:
            raise ValueError("Positive exact-token capacity required")
        if not isinstance(self.document_id, str) or not self.document_id:
            raise ValueError("Nonempty document identity required")

    @property
    def next_ordinal(self):
        return len(self.receipts)

    def check(self, ordinal: int, tokens, origins, sources=None) -> bool:
        """Return True for a verified replay, before any writer invocation."""
        sources = tuple(sources) if sources is not None else (self.document_id,) * len(tokens)
        digest = payload_digest(tokens, origins, sources)
        if type(ordinal) is not int or not 0 <= ordinal <= self.next_ordinal:
            raise ValueError("Events must be admitted in consecutive ordinal order")
        if ordinal < self.next_ordinal:
            if self.receipts[ordinal] != digest:
                raise ValueError("Conflicting payload for a consumed event identity")
            for event in self.events:
                if event.ordinal == ordinal and (event.tokens != tuple(tokens) or event.origins != tuple(origins) or event.sources != sources):
                    raise ValueError("Retained event payload differs despite its digest")
            return True
        return False

    def append(self, ordinal: int, tokens, origins, sources=None) -> "EpisodicStore":
        sources = tuple(sources) if sources is not None else (self.document_id,) * len(tokens)
        if self.check(ordinal, tokens, origins, sources):
            return self
        if len(tokens) > self.capacity_tokens:
            raise ValueError("Capacity must admit one complete event")
        event = Event(ordinal, tuple(tokens), tuple(origins), payload_digest(tokens, origins, sources), sources)
        events = self.events + (event,)
        evicted = self.evicted_events
        retained = sum(len(e.tokens) for e in events)
        while retained > self.capacity_tokens:
            retained -= len(events[0].tokens)
            events = events[1:]
            evicted += 1
        return EpisodicStore(self.capacity_tokens, self.document_id, events,
                             self.receipts + (event.digest,), evicted)

    def index(self, include_generated=False):
        """Build one immutable lexical view per neural read, shared across rows."""
        result = []
        for event in self.events:
            visible = tuple((token, pos, ORIGINS.index(origin)) for pos, (token, origin) in
                enumerate(zip(event.tokens, event.origins, strict=True))
                if include_generated or origin != "generated")
            if visible:
                result.append((event.ordinal, visible, frozenset(t for t, _, _ in visible)))
        return tuple(result)

    def retrieve(self, query, top_k: int, token_budget: int, policy: str,
                 include_generated: bool = False, *, index=None) -> tuple[list[tuple[int, int, int, int]], dict]:
        """Return (token, original position, selected-event rank, origin index).

        Exact brute-force lexical scan, explicitly billed. No hidden answer index.
        Empty/zero-overlap queries fall back to recency. Mixed events filter each
        generated token BEFORE ranking/selection; they are never external facts.
        """
        if top_k <= 0 or token_budget <= 0 or policy not in ("lexical", "recency"):
            raise ValueError("Invalid retrieval limits/policy")
        known = set(query)
        candidates = []
        built = index is None
        index = self.index(include_generated) if built else index
        for ordinal, visible, terms in index:
            score = len(known.intersection(terms)) if policy == "lexical" else 0
            candidates.append((score, ordinal, visible))
        candidates.sort(key=lambda entry: (entry[0], entry[1]), reverse=True)
        result = []
        used_events = 0
        omitted = 0
        trace = []
        for rank, (_, ordinal, visible) in enumerate(candidates[:top_k]):
            remaining = token_budget - len(result)
            if not remaining:
                omitted += len(visible)
                continue
            # Keep an exact ordered suffix if a selected event exceeds budget.
            selected = visible[-remaining:]
            result.extend((token, pos, rank, origin) for token, pos, origin in selected)
            omitted += len(visible) - len(selected)
            trace.append({"event_id": f"{self.document_id}:{ordinal}",
                          "positions": [pos for _, pos, _ in selected]})
            used_events += 1
        return result, {"events_scanned": len(self.events),
                        "index_tokens_scanned": sum(len(e.tokens) for e in self.events) if built else 0,
                        "events_selected": used_events, "raw_tokens_read": len(result),
                        "selected_tokens_omitted": omitted, "selection_trace": trace}

    def state_dict(self) -> dict:
        return {"format": "lwm-episodic-v1", "capacity_tokens": self.capacity_tokens,
                "document_id": self.document_id, "events": [asdict(e) for e in self.events],
                "receipts": list(self.receipts), "evicted_events": self.evicted_events}

    @classmethod
    def from_state_dict(cls, state: dict, *, vocab_size: int, event_length: int) -> "EpisodicStore":
        if state.get("format") != "lwm-episodic-v1":
            raise ValueError("Unknown episodic state format")
        receipts = tuple(state["receipts"])
        if any(not isinstance(d, str) or len(d) != 64 or any(c not in "0123456789abcdef" for c in d) for d in receipts):
            raise ValueError("Invalid receipt digest")
        events = []
        for raw in state["events"]:
            event = Event(raw["ordinal"], tuple(raw["tokens"]), tuple(raw["origins"]), raw["digest"], tuple(raw["sources"]))
            if (type(event.ordinal) is not int or not 0 <= event.ordinal < len(receipts)
                    or len(event.tokens) != event_length or any(t >= vocab_size for t in event.tokens)
                    or payload_digest(event.tokens, event.origins, event.sources) != event.digest
                    or receipts[event.ordinal] != event.digest):
                raise ValueError("Invalid retained event identity/content")
            events.append(event)
        evicted = state["evicted_events"]
        if type(evicted) is not int or evicted < 0 or evicted + len(events) != len(receipts):
            raise ValueError("Event/eviction ledger differs")
        if [e.ordinal for e in events] != list(range(evicted, len(receipts))):
            raise ValueError("Retained events must be an ordered FIFO suffix")
        store = cls(state["capacity_tokens"], state["document_id"], tuple(events), receipts, evicted)
        if sum(len(e.tokens) for e in events) > store.capacity_tokens:
            raise ValueError("Restored raw history exceeds capacity")
        return store

    def accounting(self) -> dict:
        return {"retained_events": len(self.events), "retained_raw_tokens": sum(len(e.tokens) for e in self.events),
                "receipt_count": len(self.receipts), "evicted_events": self.evicted_events,
                "serialized_cpu_bytes": len(json.dumps(self.state_dict(), separators=(",", ":")).encode()),
                "memory_scope": "JSON payload bytes, not Python heap/RSS; receipts grow with document history"}
