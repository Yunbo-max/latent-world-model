# Latent World Model Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans for implementation and the scoped dispatching-parallel-agents workflow for independent source review. Research Autopilot's Web role applies: author complete source and meaningful acceptance checks; do not run project code/tests here. User has already requested implementation and GitHub delivery.

**Goal:** Deliver the full text predictive latent-state model, training/inference/native evaluation source, and a reproducible RTX 2080 Ti experimental design.

**Architecture:** A causal prelude embeds a segment with an internal segment-start vector. A shared recurrent reader repeatedly reads fixed evidence and previous-segment memory, followed by a language coda. A separate writer consumes the completed observed segment exactly once and provides memory to the next segment.

**Tech Stack:** Python, PyTorch, NumPy, pinned Hugging Face tokenizer/data assets; native Conda on the execution host, no container requirement.

**Spec:** `research/FULL_MODEL_PROPOSAL.md`; source comparison in `research/AUTHOR_IMPLEMENTATION_AUDIT.md`; data protocol in `research/DATA_PROTOCOL_PROPOSAL.md`.

## Global Constraints

- The owner's actual goal is a complete model scheme, then corresponding code and experiment design based on existing models/code. This is an explicitly described engineering composition, not a claimed faithful reproduction or original research result.
- Preserve the earlier discovery batch and its unresolved obligations. Do not change its verifier or falsely report selection, scientific acceptance, or novelty.
- `generated_unexecuted` is the source-delivery status. Tests, GPU fit/throughput and native-scoring parity require Local execution.
- Predict every actual token, including the first and EOS, without observing that token in its prediction row. No additional conventional shifted-label transformation is allowed on `forward_segment` output.
- Keep memory fixed throughout the reader's internal iterations. Writes occur only when an observed segment closes. Partial generation prefixes do not write persistent memory.
- Backpropagate through at least two adjacent segments when learning the writer; detach at the unroll boundary. Do not claim full-document gradients under truncated BPTT.
- Treat 100M/1B as training target-token budgets, with EOS counted and padding/segment vectors excluded. Record actual processed, optimized and skipped token counts separately.
- Model size and microbatch settings are engineering starting points, not measured fit or throughput claims.

## Review Focus

1. Changing a future token must not change earlier token logits.
2. Prefix generation and teacher-forced logits must agree with dropout disabled, including segment boundaries and an empty prefix.
3. A next-segment loss must produce a nonzero finite writer gradient; no graph crosses the declared truncation boundary.
4. A paused partial prefix must not cause a duplicate memory write, and EOS/document boundaries must reset the correct state.
5. Resume must preserve data cursor, memory, RNG, token counts and optimizer/scaler state; incompatible configuration/assets must fail explicitly.

## Task 1: Model and mathematical mapping

Files: `src/lwm/model.py`, `src/lwm/generation.py`, `tests/test_model_semantics.py`, `research/MATH_TO_CODE.md`.

Interfaces:
- `ModelConfig` defines vocabulary, dimensions, heads, segment length, memory slots, layer/loop counts and memory ablation.
- `LatentWorldModel.initial_memory(batch_size)` returns differentiable learned initialization.
- `forward_segment(tokens[B,L], memory[B,S,d])` returns `(logits[B,L,V], next_memory[B,S,d])`; output row i predicts input token i using the internal SEG row and preceding tokens.
- `predict_prefix(prefix[B,u], memory)` supports `0 <= u < block_size` and returns `[B,V]` next-token logits.
- `commit_segment(tokens, memory)` returns new memory without mutating caller state.

- [x] Write semantic acceptance tests for the five risks above; keep tests visibly unexecuted.
- [x] Implement explicit causal attention, fixed-memory cross attention, input reinjection, shared core, tied readout and functional writer.
- [x] Implement streaming observation/prediction with exactly-once segment commits and EOS reset.
- [x] Review formulas against each source function; Local later runs `pytest tests/test_model_semantics.py` through its execution harness.

## Task 2: Versioned assets and document data

Files: `src/lwm/data.py`, `src/lwm/prepare.py`, `configs/assets.json`, `tests/test_data_semantics.py`.

Interfaces: source preparation writes token documents and a manifest with immutable upstream identities, tokenizer fingerprint, byte hashes, split assignment and exact counts. The training reader preserves document boundaries and serializes its cursor.

- [x] Implement acquisition of complete pinned required files, integrity checks and deterministic preparation; never fetch mutable latest implicitly.
- [x] Preserve first-token/EOS targets and exact nested token prefixes. Keep document-content-hash splits disjoint.
- [x] Implement native bAbI and LAMBADA schema adapters against the reviewed author protocol.
- [x] Write Local acceptance checks for corpus identities, counts, native example parity and complete released ID coverage.

## Task 3: Training and resumable checkpoints

Files: `src/lwm/train.py`, `src/lwm/checkpoint.py`, `configs/*.json`, `tests/test_training_semantics.py`.

Interfaces: `python -m lwm.train --config CONFIG --data DATA_DIR --output RUN_DIR [--resume CHECKPOINT]` uses the model/data contracts above.

- [x] Implement bounded segment unrolling, token-weighted gradient accumulation, FP16 GradScaler, clipping, AdamW, schedule and exact target budget.
- [x] Save atomic versioned checkpoints with optimizer, scaler, data cursor, memory, CPU/CUDA/Python/NumPy RNG and effective configuration.
- [x] Implement held-out document likelihood, peak-memory/throughput measurement and finite loss/gradient failure reporting.
- [x] Keep pretraining and benchmark supervised training budgets and run identities separate.

## Task 4: Native evaluation and experimental design

Files: `src/lwm/evaluate.py`, `scripts/run_matrix.py`, `research/EXPERIMENT_DESIGN.md`, `configs/experiments.json`.

- [x] Cover every selected bAbI task and the full selected LAMBADA split with native scoring and strict prediction/ID/denominator checks.
- [x] Define memory × internal-depth comparisons plus an equal-core-application-depth control with measured cost; distinguish matched-token and matched-cost questions.
- [x] Retain per-example predictions/losses, per-task metrics, actual cost and failed/unscored inventories.
- [x] Prespecify paired uncertainty, training-repeat limitations, development-only selection, confirmation and resource-dependent launch conditions.

## Task 5: Local handoff and GitHub integration

Files: `README.md`, `AGENTS.md`, `LOCAL_AGENT_RUNBOOK.md`, `rounds/engineering-2026-10-07/WEB_HANDOFF.md`, research checkpoint.

- [x] Write exact asset, setup, acceptance, train/eval, resume and collection commands; identify unresolved host paths/access in a concrete restoration step.
- [x] Source-review all interfaces, parse authored Python/configs without executing the project, and review generated tests independently.
- [x] Preserve research history and report separate source-delivery/scientific/hosted-task statuses.
- [ ] Publishing-session action: update main with an expected parent and read back exact-version bytes; the final delivery receipt reports the actual commit only after this succeeds.

Checked entries mean source authored and source-reviewed only. The 61 test functions are unexecuted; no software/native/empirical pass is implied. The publishing-session step is verified against the resulting commit after this file is committed, so its final receipt lives in the delivery message.
