"""Exact finite-depth model from research/FULL_MODEL_PROPOSAL.md.

forward_segment rows predict the SAME input tokens, not tokens shifted again.
The writer sees a completed observed segment; the reader never sees its output.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import math

import torch
from torch import Tensor, nn
from torch.nn import functional as F
from torch.utils.checkpoint import checkpoint


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

    def __post_init__(self):
        for name in ("vocab_size", "d_model", "n_heads", "ffn_mult", "block_size",
                     "memory_slots", "prelude_layers", "core_layers", "coda_layers", "loop_steps"):
            if not isinstance(getattr(self, name), int) or getattr(self, name) <= 0:
                raise ValueError(f"{name} must be a positive integer")
        if self.d_model % self.n_heads:
            raise ValueError("d_model must be divisible by n_heads")
        if self.dropout != 0.0:
            raise ValueError("v0 defines dropout=0 for explicit train/generation parity")

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

    def forward(self, query: Tensor, context: Tensor, causal: bool = False) -> Tensor:
        batch, length, width = query.shape
        def heads(value):
            return value.reshape(batch, -1, self.heads, self.head_dim).transpose(1, 2)
        q, k, v = heads(self.q(query)), heads(self.k(context)), heads(self.v(context))
        # FP32 scores/softmax avoid an FP16 QK overflow before softmax.
        with torch.autocast(device_type=query.device.type, enabled=False):
            scores = torch.matmul(q.float(), k.float().transpose(-1, -2)) / math.sqrt(self.head_dim)
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

    def _read(self, evidence: Tensor, memory: Tensor) -> Tensor:
        if not self.config.memory_enabled:
            memory = self.initial_memory(evidence.size(0))
        hidden = evidence
        for _ in range(self.config.loop_steps):
            hidden = self.adapter(torch.cat((hidden, evidence), dim=-1))
            for block in self.core:
                hidden = self._call(block, hidden, memory, self.slot_embedding)
        for block in self.coda:
            hidden = self._call(block, hidden)
        return F.linear(self.output_norm(hidden), self.embedding.weight)

    def _write(self, evidence: Tensor, memory: Tensor) -> Tensor:
        # The ablation executes the writer but discards history. Parameter and
        # nominal writer compute inventories therefore remain explicit.
        result = self._call(self.writer, memory, evidence, self.slot_embedding)
        if not self.config.memory_enabled:
            return self.initial_memory(evidence.size(0))
        return result

    def forward_segment(self, tokens: Tensor, memory: Tensor) -> tuple[Tensor, Tensor]:
        self._validate(tokens, memory)
        evidence = self._encode(tokens)
        logits = self._read(evidence[:, :-1], memory)
        next_memory = self._write(evidence[:, 1:], memory)
        return logits, next_memory

    def forward(self, tokens: Tensor, memory: Tensor) -> tuple[Tensor, Tensor]:
        return self.forward_segment(tokens, memory)

    def predict_prefix(self, prefix: Tensor, memory: Tensor) -> Tensor:
        self._validate(prefix, memory, empty=True)
        return self._read(self._encode(prefix), memory)[:, -1]

    def commit_segment(self, tokens: Tensor, memory: Tensor) -> Tensor:
        self._validate(tokens, memory)
        if tokens.size(1) != self.config.block_size:
            raise ValueError("Only a complete segment can be committed; retain partial prefixes")
        return self._write(self._encode(tokens)[:, 1:], memory)
