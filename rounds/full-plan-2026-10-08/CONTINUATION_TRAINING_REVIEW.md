# Independent continuation training/native review

Reviewer: `/root/expansion_training_review`, source-only Web review, 2026-10-08.
Status: `generated_unexecuted`; no project import, project code, software test,
GPU workload, dataset acquisition or upstream download was executed. Reads and
standard-library SHA256 were the only source-inspection operations. This review
does not adopt earlier review verdicts as its own evidence.

Reviewed contract: `AGENTS.md`, this round's `EXPANSION_SPEC.md` and
`IMPLEMENTATION_GOAL.md`; model, trainer, checkpoint, evaluation, native scoring,
matrix authoring and all `configs/full*` configuration bytes. Local runbook and
the adopted proposal/math map/experiment design provided integration obligations.

## Initial findings, sent to the integration writer

**Critical: none found in the reviewed initial bytes.** This is a bounded static
review, not a proof that software will execute or that the construction is novel.

**Important T1 — held-out auxiliary target quality is not evaluated.**
`train.validation_nll` calls `window_objective` with its default zero state weight
and consumes only the returned language loss. The auxiliary head is trained and
its training CE/pair count is logged, but validation cannot expose its held-out
CE or eligible-pair denominator. This prevents the proposed predictive-state
objective from having the same development diagnostics as the main object.
Repair: accept the selected weight, accumulate explicit main/state CE sums and
pair counts, return main CE per main target as the unchanged language NLL,
separately return state CE per eligible pair and the weighted objective per main
target. Pass the selected weight from the actual trainer validation call. Zero
pairs must produce an explicit absent value rather than division by zero.

**Important T2 — registered parameter count is being used without the promised
active-gradient inventory.** The start/evaluation manifests report total
parameters. Some branches deliberately leave registered modules unused (adapter
under contractive dynamics, predictive head at beta=0, writer in reset-memory
arms). The experiment design explicitly requires total and gradient-active
inventory. Repair: before zeroing optimizer gradients, record the number of
parameter tensors/elements whose `.grad` exists, distinguishing this from nonzero
gradient, identifiability or effective model capacity. Keep the total count and
the structural comparison warning.

**Important T3 — the preserved 2×2 interaction has no actual scoring card.**
The adopted v0 experimental design requires `(M4-R4)-(M1-R1)`, but initial
`scoring.py` exposes only two-arm `compare`, and the full matrix contains no
four-arm interaction job. All five v0 arms remain configured, so data are
available, but Local would need to author the missing statistic. Repair: add an
explicit four-run native-ID join and shared passage/within-task episode
bootstrap of the per-example four-arm interaction; require full native
denominators and completed immutable manifests, preserve seed uncertainty and
multiplicity limitations, and generate dependency cards after all four native
replays. This is an existing analysis obligation, not a new benchmark.

**Observation T4 — access counts are complete, selection trace is last-call
only.** `model.audit.last_retrieval_trace` is overwritten for each prefix/segment
read. Cumulative counts record raw reads/scans, but the trace in an update/example
cannot reconstruct all earlier selections in that interval. State this scope
explicitly in logs/runbook, or add a low-storage ordered digest/count of the
complete selection chain. This observation does not invalidate causality or
the reported total access counts.

## Independently checked mathematics and code paths

- `ContractiveWorkspace.matrix` computes
  `A=cW/max(1,||W||_F)` in FP32 without detaching its parameter dependence.
  Therefore `||A||_2 <= ||A||_F <= c` in real arithmetic. For fixed forcing,
  elementwise tanh is 1-Lipschitz, so the implemented recurrence is a global
  c-contraction in workspace. Forcing is built once outside the recurrence;
  no recurrent attention, normalization or residual bypass appears inside it.
  The real-arithmetic guarantee is not a floating-point roundoff certificate.
- The fixed forcing consumes causal evidence, previous compressed slots and
  earlier completed raw events. Each retrieval row uses `tokens[:u]`, not the
  row's target. The reader cannot consume the writer output of the same segment.
- The auxiliary distribution is a normalized vocabulary head from mean pooled
  post-write compressed memory. Only the subsequent segment's first existing
  eligible target contributes. That token enters CE after state/retrieval have
  already been defined; no new target is passed into writer or retrieval.
- `window_objective` adds `main_sum + beta*state_sum`; optimizer accumulation
  scales and finally corrects by the existing main eligible-target denominator.
  Auxiliary observations are counted separately and do not enlarge the main
  target budget. The complete within-window writer graph remains connected;
  the explicit TBPTT boundary truncates it once per window. This objective is
  a finite supervised surrogate, not conditional-mutual-information estimation,
  KL compression or a sufficiency proof.
- Native document resets rebuild history; terminal document history is discarded.
  No auxiliary pair is taken across documents. Partial budget-final training
  segments may yield transient numerical memory, but no future optimization
  continuation is admitted after the completed target budget.
- Checkpoints persist the store/segment clock with slots, data cursor,
  optimizer/scaler, RNG, config/source/data identities and counters at an
  optimizer boundary. Restore checks store/document/config/ordinal consistency;
  source/config/data mismatches and an already completed target budget fail.
  Run output lock, latest-parent checks and failure retention remain present.
- Plan training projects workspace through a narrow tanh plan then the separate
  language lift/coda/readout. Its token likelihood is ordinary categorical CE;
  this is not evidence of identified semantics or an annotated semantic codec.
- Native evaluation retains 20,000 bAbI and 5,153 LAMBADA denominators; scorer
  replay checks pinned source and ordered row identities. Paired bootstrap
  clusters bAbI questions within native episodes/tasks and LAMBADA by passage.
  The result is conditional on checkpoints, not training-seed uncertainty.
- The selected full matrix has 13 arms ×2 seeds: 2.6B/26B pretraining targets
  for the 100M/1B tier plus 26M answer/EOS adaptation targets per tier. Retrieval,
  context, validation/inference and failed attempts are separate real costs.
  Full/no-module/recency/retrieval-only config distinctions match their stated
  information and mechanism interventions; they are not parameter/FLOP matches.

## Initial SHA256 snapshot

These identify the reviewed initial source, before integration repairs.

| Path | SHA256 |
|---|---|
| `AGENTS.md` | `e6bcd6b0b1793cebf257bb83c648b27f0deda3750e7683aa46dc13674cf11b19` |
| `rounds/full-plan-2026-10-08/EXPANSION_SPEC.md` | `03131f0453601ede4505afc9f1d38b60e3ebd3e0287bfcf2cc4ffea0d8abc5e0` |
| `rounds/full-plan-2026-10-08/IMPLEMENTATION_GOAL.md` | `01bd58706b9a168b262a02b67a470be6929960059296483daa086f4c571f7a10` |
| `src/lwm/model.py` | `27be3e0b571b207c62985e269f6e3e4ad33a6aa38fc9f508ef0eccc11201096d` |
| `src/lwm/train.py` | `9a7c16512efd0c80b4581cccbda10f4355bcf5371717c1fa2985c9a62559df19` |
| `src/lwm/checkpoint.py` | `c1e0cbf73d53ca8cf4075caee942376f2b6c74e03984568f70362e1cc56bd1b6` |
| `src/lwm/evaluate.py` | `ca141f364599a6b205386639be78f56ed42cfd462388a918355d0e9e94b6d5ce` |
| `src/lwm/scoring.py` | `02f079f6cdaa3d14ccfdbef3f9973ab727f8bb8c94d96503a9e5c236f751004d` |
| `scripts/run_matrix.py` | `8a719c38f7b9702b867266b33632ba5c2b0a4f3924f5a36b9c58b6d836b5bbe6` |
| `configs/full_plan_experiments.json` | `3f87d477bbfa8f87113c3d6599735d597f7b3001bfec7146ae4f3589715eb7e4` |

The initial 25 `configs/full*` files additionally have an ordered whole-set
SHA256 of `c0b10360eab4dec4e24f6d4281a07e67e040cda9634b070bfa3ce0f99b6492e3`.
Construction: lexicographically sorted relative UTF-8 path, NUL, raw file bytes,
NUL, concatenated and hashed. This identifies every configuration reviewed.

## Follow-up on actual integration repairs

The writer changed source after receiving T1–T3. I separately re-read the actual
changed methods and the new authored acceptance cases; none was executed.

- **T1 resolved in source:** validation accepts the selected state weight and
  accumulates main CE separately from auxiliary CE/pairs. Main language NLL and
  perplexity retain their original denominator and meaning; state CE per pair
  and the weighted objective per main target are separate. Zero-pair state CE
  per pair is `None`. The real trainer passes its weight. The new validation
  fixture covers equal language NLL, composite denominator, audit restoration,
  and no cross-document state pair. Its imports/argument names match the code.
- **T2 resolved in source:** update captures `.grad`-present tensor/element counts
  before `zero_grad`; the log explicitly excludes nonzero-gradient or effective
  capacity interpretation. Reserved GPU peak is now recorded with allocated
  peak. Such measurements remain Local-produced, not Web resource receipts.
- **T3 resolved in source:** `factorial_bootstrap` strictly joins all four native
  ID sets, checks shared input/task/labels/episode or target identity, validates
  binary scores, forms per-example `M4-R4-M1+R1`, and resamples its shared
  episode/passage units. Point estimate and percentile interval use the same
  native macro/micro choice as the paired helper. `_index` rejects empty inputs;
  missing/duplicate/mismatched IDs fail. CLI invocation order matches the actual
  function signature and full-denominator/immutable-manifest checks are present.
  Four-arm cards depend on all four official replays for each task/seed. Added
  numeric fixtures verify interaction sign/extreme bound, zero interaction and
  missing-ID rejection; these fixtures are not native benchmark evidence.
- **T4 scope resolved in source:** `model.audit.retrieval_trace_scope` now says
  last neural read only, while cumulative access counts cover all calls. This
  removes an ambiguous all-trace interpretation without claiming complete
  trace retention.

No Critical/Important model, objective, resume, pairing or cost issue remains
from T1–T4 in the follow-up bytes below. A minor input-contract hardening
observation was sent to the writer: `_run_manifest` initially did not explicitly
reject non-test LAMBADA split metadata (the evaluator only produces test). The
writer should keep this explicit rejection and zero-GPU command intent visible;
neither native-replay dependency nor a completed-manifest field alone qualifies
model-adapter parity, training completion, novelty or scientific value.

### Follow-up SHA256 snapshot

| Path | SHA256 |
|---|---|
| `src/lwm/model.py` | `73c7a6cbcdc8a2617089ece8cd51a3f89638dd7b6fd9331464b33d0bef2b59e8` |
| `src/lwm/train.py` | `8e41f8e523c604e1e12531ed8c37fcf1cc1af10cc87c63f94123405b8401a2d6` |
| `src/lwm/checkpoint.py` | `c1e0cbf73d53ca8cf4075caee942376f2b6c74e03984568f70362e1cc56bd1b6` |
| `src/lwm/evaluate.py` | `ca141f364599a6b205386639be78f56ed42cfd462388a918355d0e9e94b6d5ce` |
| `src/lwm/scoring.py` | `e914b5e6b091b3e4e804c66e683c0a4ba2fd152e05290de114013cf313b9a234` |
| `scripts/run_matrix.py` | `19549ce4aa7345d67af08eca203c4ffa0da6a5ac4e2e6e78da235244b88d4bc3` |
| `configs/full_plan_experiments.json` | `3f87d477bbfa8f87113c3d6599735d597f7b3001bfec7146ae4f3589715eb7e4` |
| `tests/test_expansion_semantics.py` | `384590e2701aa312cd70f4394b019f7539e0f021b983f0a885e26e2bc5970430` |
| `tests/test_scoring_semantics.py` | `cccd67f345acd87818aeaedce5010f0cce3f8a571f95b74ec3cecab10d34d262` |

All Local software/native/hardware/scientific acceptance remains pending.

## Final narrowly scoped follow-up

Actual last delta separately read: `_run_manifest` now rejects unknown native
task/split, LAMBADA outside `test`, non-integer example counts and any incomplete
native denominator before either comparison path. Interaction argv now explicitly
uses `env CUDA_VISIBLE_DEVICES=` and retains `gpu_count=0`. The minor manifest
observation above is therefore resolved in source; no project invocation ran.

`COVERAGE.md`, this round's `EXPERIMENT_DESIGN.md` and `WEB_HANDOFF.md` were also
read for contract consistency. The full design's command count is
`13*2*6 + 11*2*2 + 2*2 = 204`; the target totals are `13*2*100M=2.6B` or
`13*2*1B=26B`, with `13*2*1M=26M` separately budgeted adaptation targets.
Costs, last-only trace scope, conditional statistics, pending Local execution
and unfinished broader scientific ideals remain explicit. A minor coverage-row
gate convention typo was sent to the writer: the actual `MemoryWriter` uses
`M'=(1-gate)*M+gate*proposal`.

Final changed-source SHA256:

| Path | SHA256 |
|---|---|
| `src/lwm/scoring.py` | `d3ff5d1989cd67e3b0e6d6a51c7ce5fb3bb4be87ca0df5062ebf59ac8c06cfe7` |
| `scripts/run_matrix.py` | `adab5e83d59933ff15e8d56429dabc0e054ec3427018b0751ad95557dc322687` |

These replace the preceding snapshot's scoring/matrix hashes. Other reviewed
model/trainer/checkpoint/evaluator bytes are unchanged by this final delta.
Final verdict: no remaining Critical/Important issue found within this source
review scope; runtime, native adapter, hardware and scientific results unverified.
