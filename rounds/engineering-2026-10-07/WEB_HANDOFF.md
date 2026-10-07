# Web handoff: engineering-2026-10-07

Destination: https://github.com/Yunbo-max/latent-world-model, `main`. Exact publication SHA is supplied by the later delivery receipt; a file cannot contain its own future commit hash.

Status: **generated_unexecuted**. The requested full model mathematical construction, corresponding source and full experimental design are the delivery objective. Current source authoring does not claim a research-discovery selection, novelty, software pass, native qualification, GPU run or task score.

Start with [AGENTS](../../AGENTS.md), then [Local guide](../../LOCAL_AGENT_RUNBOOK.md), particularly its [asset acquisition](../../LOCAL_AGENT_RUNBOOK.md#download-datasets-and-models). Restore real host paths/resources and use the existing Local execution harness.

## Adopted construction and evidence map

- [Full mathematical specification](../../research/FULL_MODEL_PROPOSAL.md): persistent bounded memory, causal SEG/prelude, fixed-evidence shared core, coda, separate writer; exact targets, generating state machine, TBPTT limitations.
- [Author implementation audit](../../research/AUTHOR_IMPLEMENTATION_AUDIT.md): pinned Huginn/RMT source hazards and a source-only causal/gradient review.
- [Scope review](../../research/SCIENTIFIC_SCOPE_REVIEW.md): explicit engineering adaptation, not a faithful reproduction or fabricated original discovery.
- [Math-to-code map](../../research/MATH_TO_CODE.md): functions and meaningful Local checks.
- [Native asset/protocol audit](../../research/DATA_PROTOCOL_PROPOSAL.md), [asset manifest](../../configs/assets.json), [native environments](../../research/NATIVE_ENVIRONMENT.md).
- [Complete experimental design](../../research/EXPERIMENT_DESIGN.md), [matrix](../../configs/experiments.json), [implementation plan](../../docs/superpowers/plans/2026-10-07-latent-world-model.md).

## Source inventory

| Function | Source / commands |
|---|---|
| Model equations | `src/lwm/model.py` |
| Streaming observation / readout / branch state / generation CLI | `src/lwm/generation.py` |
| Immutable corpus + resumable cursor | `src/lwm/data.py` |
| Pinned source download + FineWeb/bAbI/LAMBADA prep | `src/lwm/prepare.py`, `configs/assets.json` |
| Single-device TBPTT + AMP + explicit budgets | `src/lwm/train.py`, 100M/1B/bAbI configs |
| Atomic full optimizer/RNG/state resume | `src/lwm/checkpoint.py` |
| Full native task inference and predictions | `src/lwm/evaluate.py` |
| Strict scoring, actual native replay, paired uncertainty | `src/lwm/scoring.py` |
| Full command matrix / observed profile summary | `scripts/run_matrix.py`, `scripts/summarize_run.py` |
| Local software acceptance | `tests/` — authored, not run by Web |

## Acceptance and known gaps

Local must obtain real assets; execute the complete software suite; verify native data/teacher/tokenizer/scorer parity; measure RTX2080Ti capacity and each necessary cost envelope; freeze the full cumulative resource plan; then execute the complete selected matrix. Exact source/config/scorer and actual IDs/denominators remain attached to every result.

100M/1B is per pretraining arm and seed. Five arms × two seeds multiply total compute, and bAbI adaptation is additional. Full 1B configurations exist, but unknown measured costs are not a promise to finish all runs in a day. The standard model's analytic parameter count is ~20.1M and must be checked on the actual instantiated source.

The model is a text predictive state, not a proven physical/causal world model. No KV cache is implemented; prefix recomputation makes generation semantics explicit but may be slow. Shallow writer capacity, finite memory, short BPTT credit and parameter-stale carried state are material limitations. Strongest-published baseline superiority and a new-method paper remain outside what this source packet establishes.

The old `research/method-batch.json` still has one unselected Q01 direction and unresolved discovery obligations. Its historical `CODE_READINESS.json` is not a green gate for this engineering route. Do not replace it with invented selection or test receipts.

This long task has been conducted in the active Work conversation. No independent hosted Goal ID, external scheduler, paid service or GPU job was created. Source publication and future Local execution are distinct.

Return real acceptance/experiment logs, E04 and exact GitHub result commit/packet as specified by the Local guide. Preserve failed and incomplete comparisons and the original cumulative budgets.
