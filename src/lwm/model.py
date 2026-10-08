"""Exact finite-depth model from research/FULL_MODEL_PROPOSAL.md.

forward_segment rows predict the SAME input tokens, not tokens shifted again.
The writer sees a completed observed segment; the reader never sees its output.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import math
import time

import torch
from torch import Tensor, nn
from torch.nn import functional as F
from torch.utils.checkpoint import checkpoint

from .episodic import EpisodicStore, ORIGINS


@dataclass
class ModelConfig:
    vocab_size: int = 50257
    d_model: int = 256
    n_heads: int = 4
    ffn_mult: int = 4
    block_size: int = 256
    memory_slots: int = 16
    prelude_layers: int = 2
    core_layers: int = 2
    coda_layers: int = 1
    loop_steps: int = 4
    dropout: float = 0.0
    checkpoint_layers: bool = False
    memory_enabled: bool = True
    episodic_enabled: bool = False
    episodic_capacity_tokens: int = 4096
    episodic_read_tokens: int = 256
    episodic_top_k: int = 2
    episodic_query_tokens: int = 32
    episodic_policy: str = "lexical"
    episodic_include_generated: bool = False
    semantic_dim: int = 0
    dynamics: str = "transformer"
    contraction_bound: float = 0.9
    predictive_head: bool = False

    def __post_init__(self):
        for name in ("vocab_size", "d_model", "n_heads", "ffn_mult", "block_size",
                     "memory_slots", "prelude_layers", "core_layers", "coda_layers", "loop_steps"):
            if not isinstance(getattr(self, name), int) or getattr(self, name) <= 0:
                raise ValueError(f"{name} must be a positive integer")
        if self.d_model % self.n_heads:
            raise ValueError("d_model must be divisible by n_heads")
        if self.dropout != 0.0:
            raise ValueError("v0 defines dropout=0 for explicit train/generation parity")
        for name in ("episodic_capacity_tokens", "episodic_read_tokens", "episodic_top_k", "episodic_query_tokens"):
            if type(getattr(self, name)) is not int or getattr(self, name) <= 0:
                raise ValueError(f"{name} must be positive")
        if self.episodic_enabled and self.episodic_capacity_tokens < self.block_size:
            raise ValueError("Episodic capacity must admit a complete segment")
        if self.episodic_policy not in ("lexical", "recency"):
            raise ValueError("Unknown historical retrieval policy")
        if type(self.semantic_dim) is not int or not 0 <= self.semantic_dim < self.d_model:
            raise ValueError("semantic_dim is zero (v0) or a smaller positive width")
        if self.dynamics not in ("transformer", "contractive"):
            raise ValueError("Unknown workspace dynamics")
        if not math.isfinite(self.contraction_bound) or not 0 < self.contraction_bound < 1:
            raise ValueError("contraction_bound must be in (0,1)")

    def to_dict(self) -> dict:
        return asdict(self)


class RMSNorm(nn.Module):
    def __init__(self, width: int, eps: float = 1e-6):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(width))
        self.eps = eps

    def forward(self, x: Tensor) -> Tensor:
        normalized = x.float() * torch.rsqrt(x.float().square().mean(-1, keepdim=True) + self.eps)
        return normalized.to(x.dtype) * self.weight


class Attention(nn.Module):
    """Portable attention: no forced FlashAttention or BF16 requirement."""
    def __init__(self, config: ModelConfig):
        super().__init__()
        d = config.d_model
        self.heads = config.n_heads
        self.head_dim = d // self.heads
        self.q = nn.Linear(d, d, bias=False)
        self.k = nn.Linear(d, d, bias=False)
        self.v = nn.Linear(d, d, bias=False)
        self.out = nn.Linear(d, d, bias=False)

    def forward(self, query: Tensor, context: Tensor, causal: bool = False,
                key_mask: Tensor | None = None) -> Tensor:
        batch, length, width = query.shape
        def heads(value):
            return value.reshape(batch, -1, self.heads, self.head_dim).transpose(1, 2)
        q, k, v = heads(self.q(query)), heads(self.k(context)), heads(self.v(context))
        # FP32 scores/softmax avoid an FP16 QK overflow before softmax.
        with torch.autocast(device_type=query.device.type, enabled=False):
            scores = torch.matmul(q.float(), k.float().transpose(-1, -2)) / math.sqrt(self.head_dim)
            if key_mask is not None:
                scores = scores.masked_fill(~key_mask[:, None, None, :], float("-inf"))
            if causal:
                if query.size(1) != context.size(1):
                    raise ValueError("Causal self-attention requires equal query/key lengths")
                blocked = torch.ones(length, length, device=query.device, dtype=torch.bool).triu(1)
                scores = scores.masked_fill(blocked, float("-inf"))
            values = torch.matmul(scores.softmax(dim=-1), v.float())
        merged = values.to(q.dtype).transpose(1, 2).contiguous().reshape(batch, length, width)
        return self.out(merged)


class GatedMLP(nn.Module):
    def __init__(self, config: ModelConfig):
        super().__init__()
        width = config.d_model
        inner = width * config.ffn_mult
        self.a = nn.Linear(width, inner, bias=False)
        self.b = nn.Linear(width, inner, bias=False)
        self.out = nn.Linear(inner, width, bias=False)

    def forward(self, x: Tensor) -> Tensor:
        return self.out(F.silu(self.a(x)) * self.b(x))


class CausalBlock(nn.Module):
    def __init__(self, config: ModelConfig):
        super().__init__()
        self.norms = nn.ModuleList([RMSNorm(config.d_model) for _ in range(4)])
        self.attention = Attention(config)
        self.mlp = GatedMLP(config)

    def forward(self, x: Tensor) -> Tensor:
        normalized = self.norms[0](x)
        x = self.norms[1](x + self.attention(normalized, normalized, causal=True))
        return self.norms[3](x + self.mlp(self.norms[2](x)))


class CoreBlock(nn.Module):
    def __init__(self, config: ModelConfig):
        super().__init__()
        self.norms = nn.ModuleList([RMSNorm(config.d_model) for _ in range(6)])
        self.memory_norm = RMSNorm(config.d_model)
        self.self_attention = Attention(config)
        self.cross_attention = Attention(config)
        self.mlp = GatedMLP(config)

    def forward(self, x: Tensor, memory: Tensor, slots: Tensor) -> Tensor:
        normalized = self.norms[0](x)
        x = self.norms[1](x + self.self_attention(normalized, normalized, causal=True))
        x = self.norms[3](x + self.cross_attention(self.norms[2](x), self.memory_norm(memory + slots)))
        return self.norms[5](x + self.mlp(self.norms[4](x)))


class MemoryWriter(nn.Module):
    def __init__(self, config: ModelConfig):
        super().__init__()
        width = config.d_model
        self.query_norm = RMSNorm(width)
        self.evidence_norm = RMSNorm(width)
        self.update_norm = RMSNorm(width)
        self.proposal_norm = RMSNorm(width)
        self.old_gate_norm = RMSNorm(width)
        self.new_gate_norm = RMSNorm(width)
        self.attention = Attention(config)
        self.mlp = GatedMLP(config)
        self.proposal = nn.Linear(width, width, bias=False)
        self.gate = nn.Linear(2 * width, width, bias=True)

    def forward(self, memory: Tensor, evidence: Tensor, slots: Tensor) -> Tensor:
        context = self.attention(self.query_norm(memory + slots), self.evidence_norm(evidence))
        tentative = memory + context
        update = tentative + self.mlp(self.update_norm(tentative))
        # Keep persistent-state nonlinearities and the convex mixture in FP32;
        # half-rounded complementary weights need not sum to one after promotion.
        proposal = torch.tanh(self.proposal(self.proposal_norm(update)).float())
        gate = torch.sigmoid(self.gate(torch.cat((self.old_gate_norm(memory),
                                                  self.new_gate_norm(update)), dim=-1)).float())
        return (1 - gate) * memory.float() + gate * proposal


class EpisodicReader(nn.Module):
    """Position-specific historical attention; no union-of-future-queries edge."""
    def __init__(self, config):
        super().__init__()
        self.position = nn.Embedding(config.block_size, config.d_model)
        self.rank = nn.Embedding(config.episodic_top_k, config.d_model)
        self.origin = nn.Embedding(len(ORIGINS), config.d_model)
        self.attention = Attention(config)
        self.norm = RMSNorm(config.d_model)

    def forward(self, hidden, values, valid):
        length, budget, width = values.shape
        # A masked zero sentinel prevents all-masked softmax. Its output is
        # multiplied by zero for truly empty rows, not a learned null channel.
        active = valid.any(-1)
        mask = valid.clone()
        mask[~active, 0] = True
        context = self.attention(self.norm(hidden).reshape(length, 1, width),
                                 values, key_mask=mask).reshape(1, length, width)
        return context * active.reshape(1, length, 1)


class ContractiveWorkspace(nn.Module):
    """Restricted known tanh recurrence. Fixed forcing, no recurrent bypass."""
    def __init__(self, config):
        super().__init__()
        self.weight = nn.Parameter(torch.empty(config.d_model, config.d_model))
        nn.init.normal_(self.weight, std=0.02)
        self.bound = config.contraction_bound

    def matrix(self):
        weight = self.weight.float()
        return self.bound * weight / torch.linalg.vector_norm(weight).clamp_min(1.0)

    def forward(self, hidden, forcing, matrix):
        return torch.tanh(F.linear(hidden.float(), matrix) + forcing.float())


class LatentWorldModel(nn.Module):
    def __init__(self, config: ModelConfig):
        super().__init__()
        self.config = config
        self.embedding = nn.Embedding(config.vocab_size, config.d_model)
        self.position = nn.Embedding(config.block_size + 1, config.d_model)
        self.segment_start = nn.Parameter(torch.empty(config.d_model))
        self.memory_initial = nn.Parameter(torch.empty(config.memory_slots, config.d_model))
        self.slot_embedding = nn.Parameter(torch.empty(config.memory_slots, config.d_model))
        self.prelude = nn.ModuleList([CausalBlock(config) for _ in range(config.prelude_layers)])
        self.adapter = nn.Linear(2 * config.d_model, config.d_model, bias=False)
        self.core = nn.ModuleList([CoreBlock(config) for _ in range(config.core_layers)])
        self.coda = nn.ModuleList([CausalBlock(config) for _ in range(config.coda_layers)])
        self.output_norm = RMSNorm(config.d_model)
        self.writer = MemoryWriter(config)
        if config.episodic_enabled:
            self.episodic_reader = EpisodicReader(config)
        if config.semantic_dim:
            self.plan_projection = nn.Linear(config.d_model, config.semantic_dim)
            self.plan_lift = nn.Linear(config.semantic_dim, config.d_model)
        if config.dynamics == "contractive":
            self.contractive = ContractiveWorkspace(config)
        if config.predictive_head:
            # Mean-slot pooling is an explicit compressed-only finite target.
            self.future_projection = nn.Linear(config.d_model, config.d_model)
        self.audit = {}
        self.apply(self._initialize)
        nn.init.normal_(self.segment_start, std=0.02)
        nn.init.normal_(self.memory_initial, std=0.02)
        nn.init.normal_(self.slot_embedding, std=0.02)

    @staticmethod
    def _initialize(module):
        if isinstance(module, (nn.Linear, nn.Embedding)):
            nn.init.normal_(module.weight, std=0.02)
            if isinstance(module, nn.Linear) and module.bias is not None:
                nn.init.zeros_(module.bias)

    def initial_memory(self, batch_size: int) -> Tensor:
        if batch_size <= 0:
            raise ValueError("batch_size must be positive")
        return torch.tanh(self.memory_initial).unsqueeze(0).expand(batch_size, -1, -1)

    def _validate(self, tokens: Tensor, memory: Tensor, empty: bool = False):
        if tokens.ndim != 2 or tokens.dtype != torch.long:
            raise ValueError("tokens must be an unpadded [batch,length] torch.long tensor")
        lower = 0 if empty else 1
        upper = self.config.block_size - (1 if empty else 0)
        if not lower <= tokens.shape[1] <= upper:
            raise ValueError(f"Token length must be in [{lower},{upper}]")
        if tuple(memory.shape) != (tokens.size(0), self.config.memory_slots, self.config.d_model):
            raise ValueError("Memory shape does not match model and batch")
        if tokens.device != self.embedding.weight.device or memory.device != tokens.device:
            raise ValueError("Tokens, memory and model must share a device")

    def _call(self, module, *args):
        if self.config.checkpoint_layers and self.training and torch.is_grad_enabled():
            return checkpoint(module, *args, use_reentrant=False)
        return module(*args)

    def _encode(self, tokens: Tensor) -> Tensor:
        batch, length = tokens.shape
        start = self.segment_start.reshape(1, 1, -1).expand(batch, 1, -1)
        x = torch.cat((start, self.embedding(tokens)), dim=1)
        x = x + self.position(torch.arange(length + 1, device=tokens.device))[None]
        for block in self.prelude:
            x = self._call(block, x)
        return x

    def reset_audit(self):
        self.audit = {"retrieval_calls": 0, "query_positions": 0, "events_scanned": 0,
                      "index_tokens_scanned": 0, "events_selected": 0, "raw_tokens_read": 0,
                      "selected_tokens_omitted": 0, "last_retrieval_trace": [],
                      "retrieval_trace_scope": "last neural read only; cumulative access counts cover all calls",
                      "retrieval_cpu_seconds": 0.0, "retrieved_tensor_bytes_peak": 0,
                      "store_serialized_bytes_peak": 0, "store_receipt_count_peak": 0,
                      "reasoning_row_steps": 0, "contractive_last_step_residual": None}

    def _retrieved(self, tokens: Tensor, rows: int, episodic: EpisodicStore | None):
        if not self.config.episodic_enabled:
            return None
        if tokens.size(0) != 1 or episodic is None:
            raise ValueError("Exact-memory mode requires a single lane and explicit store")
        if episodic.capacity_tokens != self.config.episodic_capacity_tokens:
            raise ValueError("Episodic capacity/config mismatch")
        if not self.audit:
            self.reset_audit()
        started = time.perf_counter()
        known = tokens[0].detach().cpu().tolist()
        index = episodic.index(self.config.episodic_include_generated)
        self.audit["index_tokens_scanned"] += sum(len(event.tokens) for event in episodic.events)
        trace = []
        budget = self.config.episodic_read_tokens
        ids = torch.zeros(rows, budget, dtype=torch.long)
        positions = torch.zeros_like(ids)
        ranks = torch.zeros_like(ids)
        origins = torch.zeros_like(ids)
        valid = torch.zeros(rows, budget, dtype=torch.bool)
        for u in range(rows):
            query = known[max(0, u - self.config.episodic_query_tokens):u]
            selected, cost = episodic.retrieve(query, self.config.episodic_top_k, budget,
                self.config.episodic_policy, self.config.episodic_include_generated, index=index)
            trace.append({"prediction_row": u, "selections": cost.pop("selection_trace")})
            for key, value in cost.items():
                self.audit[key] += value
            if selected:
                payload = torch.tensor(selected, dtype=torch.long).T
                ids[u, :len(selected)], positions[u, :len(selected)], ranks[u, :len(selected)], origins[u, :len(selected)] = payload
                valid[u, :len(selected)] = True
        self.audit["retrieval_calls"] += 1
        self.audit["last_retrieval_trace"] = trace
        self.audit["query_positions"] += rows
        self.audit["retrieval_cpu_seconds"] += time.perf_counter() - started
        account = episodic.accounting()
        self.audit["store_serialized_bytes_peak"] = max(self.audit["store_serialized_bytes_peak"], account["serialized_cpu_bytes"])
        self.audit["store_receipt_count_peak"] = max(self.audit["store_receipt_count_peak"], account["receipt_count"])
        device = tokens.device
        ids, positions, ranks, origins, valid = (v.to(device) for v in (ids, positions, ranks, origins, valid))
        values = (self.embedding(ids) + self.episodic_reader.position(positions)
                  + self.episodic_reader.rank(ranks) + self.episodic_reader.origin(origins))
        values = values * valid[..., None]
        self.audit["retrieved_tensor_bytes_peak"] = max(self.audit["retrieved_tensor_bytes_peak"], values.numel() * values.element_size())
        return values, valid

    def _workspace(self, evidence: Tensor, memory: Tensor, tokens: Tensor,
                   episodic: EpisodicStore | None = None) -> Tensor:
        if not self.config.memory_enabled:
            memory = self.initial_memory(evidence.size(0))
        retrieved = self._retrieved(tokens, evidence.size(1), episodic)
        hidden = evidence
        if self.config.dynamics == "contractive":
            # Build forcing ONCE, independent of evolving hidden state.
            forcing = evidence
            if retrieved is not None:
                forcing = forcing + self.episodic_reader(forcing, *retrieved)
            for block in self.core:
                forcing = self._call(block, forcing, memory, self.slot_embedding)
            matrix = self.contractive.matrix()
            if not bool(torch.isfinite(matrix).all()) or not bool(torch.isfinite(forcing).all()):
                raise FloatingPointError("Nonfinite contractive matrix/forcing")
            hidden = torch.tanh(evidence.float())
            with torch.autocast(device_type=evidence.device.type, enabled=False):
                for _ in range(self.config.loop_steps):
                    previous = hidden
                    hidden = self.contractive(hidden, forcing, matrix)
            if not self.audit:
                self.reset_audit()
            self.audit["analytic_real_arithmetic_contraction_bound"] = self.config.contraction_bound
            self.audit["contractive_last_step_residual"] = float(torch.linalg.vector_norm((hidden - previous).detach()).item())
        else:
            for _ in range(self.config.loop_steps):
                hidden = self.adapter(torch.cat((hidden, evidence), dim=-1))
                if retrieved is not None:
                    hidden = hidden + self.episodic_reader(hidden, *retrieved)
                for block in self.core:
                    hidden = self._call(block, hidden, memory, self.slot_embedding)
        if not self.audit:
            self.reset_audit()
        self.audit["reasoning_row_steps"] += evidence.size(0) * evidence.size(1) * self.config.loop_steps
        return hidden

    def realize_plan(self, plan: Tensor, *, last_only: bool = False) -> Tensor:
        if not self.config.semantic_dim or plan.ndim != 3 or plan.size(-1) != self.config.semantic_dim:
            raise ValueError("Explicit [batch,rows,semantic_dim] plan required")
        if not 1 <= plan.size(1) <= self.config.block_size:
            raise ValueError("Invalid causal plan row count")
        return self._language(self.plan_lift(plan), last_only=last_only)

    def _language(self, hidden: Tensor, *, last_only: bool = False) -> Tensor:
        for block in self.coda:
            hidden = self._call(block, hidden)
        # RMSNorm and the vocabulary projection act independently at each
        # position. Keep the whole causal network, then project only the needed
        # row for next-token inference; training still reads every target row.
        if last_only:
            hidden = hidden[:, -1:]
        return F.linear(self.output_norm(hidden), self.embedding.weight)

    def _read(self, evidence: Tensor, memory: Tensor, tokens: Tensor,
              episodic: EpisodicStore | None = None, *, last_only: bool = False) -> Tensor:
        hidden = self._workspace(evidence, memory, tokens, episodic)
        if self.config.semantic_dim:
            plan = torch.tanh(self.plan_projection(hidden))
            return self.realize_plan(plan, last_only=last_only)
        return self._language(hidden, last_only=last_only)

    def predict_future(self, memory: Tensor) -> Tensor:
        if not self.config.predictive_head:
            raise ValueError("Compressed-state predictive head is disabled")
        return F.linear(torch.tanh(self.future_projection(memory.mean(1))), self.embedding.weight)

    def _write(self, evidence: Tensor, memory: Tensor) -> Tensor:
        # The ablation executes the writer but discards history. Parameter and
        # nominal writer compute inventories therefore remain explicit.
        result = self._call(self.writer, memory, evidence, self.slot_embedding)
        if not self.config.memory_enabled:
            return self.initial_memory(evidence.size(0))
        return result

    def forward_segment(self, tokens: Tensor, memory: Tensor, *,
                        episodic: EpisodicStore | None = None) -> tuple[Tensor, Tensor]:
        self._validate(tokens, memory)
        evidence = self._encode(tokens)
        logits = self._read(evidence[:, :-1], memory, tokens, episodic)
        next_memory = self._write(evidence[:, 1:], memory)
        return logits, next_memory

    def forward(self, tokens: Tensor, memory: Tensor, *, episodic: EpisodicStore | None = None) -> tuple[Tensor, Tensor]:
        return self.forward_segment(tokens, memory, episodic=episodic)

    def predict_prefix(self, prefix: Tensor, memory: Tensor, *,
                       episodic: EpisodicStore | None = None) -> Tensor:
        self._validate(prefix, memory, empty=True)
        return self._read(self._encode(prefix), memory, prefix, episodic, last_only=True)[:, -1]

    def plan_prefix(self, prefix: Tensor, memory: Tensor, *, episodic: EpisodicStore | None = None) -> Tensor:
        self._validate(prefix, memory, empty=True)
        if not self.config.semantic_dim:
            raise ValueError("This model has no separate plan interface")
        return torch.tanh(self.plan_projection(self._workspace(self._encode(prefix), memory, prefix, episodic)))

    def commit_segment(self, tokens: Tensor, memory: Tensor) -> Tensor:
        self._validate(tokens, memory)
        if tokens.size(1) != self.config.block_size:
            raise ValueError("Only a complete segment can be committed; retain partial prefixes")
        return self._write(self._encode(tokens)[:, 1:], memory)

