# Source review: 2026-10-08 continuation

Status: `generated_unexecuted`. Reviewed against exact recovered remote parent `a8a86cf359ac0d8598ac7b2fa6465ffa120718ae`. The local comparison snapshot was `933ce78`; it is a transport/review snapshot, not GitHub ancestry and is not published as such.

## Independent scopes actually completed

| Reviewer | Scope | Observed result |
|---|---|---|
| `/root/sigma_source_audit` | Primary release sources; bounded author/GitHub/HF discovery | Co-lead's October 7 pending-release announcement verified. No Sigma source commit/weights/scorer qualified. |
| `/root/sigma_resource_review` | Paper training/resources, evaluation/uncertainty, relevant appendices; current experiment design/runbook | Retain scratch-model matrix; distinguish full history, training seeds, native units and actual cost. Recommendations addressed in SIGMA_REVIEW/EXPERIMENT_DESIGN. |
| `/root/readout_review` | Exact product/test diff and the row-selection proof; edge cases, dtype, teacher/writer interfaces | No Critical/Important source blockers. Mathematical slice placement and full training default confirmed. |
| `/root/readout_review`, bounded follow-up | Added CPU/CUDA parametrization of actual prefix test | Model/tokens/device-derived memory aligned; CUDA skips explicit. No new Critical/Important source blockers. |

The root independently inspected the relevant source and primary release/paper sections before integration. These are source-review findings, not test or scientific-pass receipts. Paper release facts were not delegated to the code reviewer as assumed correctness.

## Addressed findings and limits

The inference head previously projected every prefix row and discarded all but the last. The new slice occurs only after every coda block; final RMSNorm acts on each row independently. `_read` defaults to full output, so `forward_segment` retains every supervised target. Parameter names/shapes, writer, stream boundaries and training objective have no change. See [SIGMA_REVIEW](../../research/SIGMA_REVIEW.md) for the proof and cost calculation.

Two test functions were authored before the product edit. The row-count and output comparison now includes CPU/CUDA FP32, empty/short/max fixture prefix, K=1/4 and reset/memory profiles. Parameter-gradient equivalence is authored for CPU FP32. All remain unexecuted; this is not a completed TDD red/green cycle. Existing teacher/causal, carried-memory, commit, EOS, functional-state and resume tests retain their separate role.

The new reset fixture starts from initial memory, so it does not independently prove rejection of a different carried history; this unchanged branch remains covered by the broader state/ablation obligations. AMP prefix parity is not qualified and is not the current evaluation dtype. The CUDA tests must actually execute on Local; skipped cases are not hardware acceptance.

The paper review prompted an accounting audit, not a claim of novel architecture or a licensed author-code port. No Sigma implementation is imported. Operator-level FLOP/tensor estimates are distinguished from measured end-to-end throughput and allocator peaks. Per-module GPU timing has not been added; current evaluator reports complete row-loop/setup/tokenization timing and actual peak allocation/reservation. If a future bottleneck claim needs finer timing, it requires a bounded measurement with instrumentation overhead reported.

All five arms, both training seeds, 100M/1B budgets and the complete bAbI/LAMBADA data/scorer contracts remain. Development-selection records will be created from actual Local attempts before test access. No hypothetical runs or future results were inserted.

## Verification boundary

[SOURCE_CHECKS.json](SOURCE_CHECKS.json) records Python AST/JSON/TOML parsing, local file-link checking, preserved asset/config identities and source hashes. `git diff --check` verifies whitespace only. No project module was imported, no authored assertion was run, and no dataset/model/GPU/native workload was executed. Publication has its own exact remote-commit readback, reported after the push; this document cannot contain its future commit SHA.

No historical Q01 readiness/verifier result is changed. Local software/native/resource acceptance, complete experiments and scientific conclusions remain pending.
