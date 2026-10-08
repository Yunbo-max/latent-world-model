# Project instructions

Before setup, acceptance, execution or repair, read these files at the **same delivered Git commit**:

1. [LOCAL_AGENT_RUNBOOK.md](LOCAL_AGENT_RUNBOOK.md), especially [input acquisition](LOCAL_AGENT_RUNBOOK.md#download-datasets-and-models).
2. [Current Web handoff](rounds/full-plan-2026-10-08/WEB_HANDOFF.md), including COVERAGE.md, EXPANSION_SPEC.md and EXPERIMENT_DESIGN.md at the same revision.
3. [Adopted mathematical specification](research/FULL_MODEL_PROPOSAL.md), [math-to-code map](research/MATH_TO_CODE.md), and [complete experiment design](research/EXPERIMENT_DESIGN.md).

User scope: complete the full original-plan engineered construction, not just the old v0: exact episodic history/query consumption, plan/realization, three clocks, lawful optional dynamics and supervised state objective, integrated train/generate/resume/native matrix. Adopt rounds/full-plan-2026-10-08/EXPANSION_SPEC.md together with the preserved v0 FULL_MODEL_PROPOSAL. This remains a text predictive latent-state model with persistent memory, independently controlled internal recurrent computation and a separate language readout, based on existing models. RTX 2080 Ti is user-stated. Data profiles are 100M/1B **pretraining target tokens per model run**, not parameter counts. The current construction is an explicitly disclosed engineering adaptation; do not claim a faithful Huginn/RMT reproduction, novelty or validated world dynamics.

Research Autopilot role split applies. Web authors and reviews source as `generated_unexecuted`; Local executes actual environment/software/native acceptance and experiments through the existing admitted SSH/native harness. Do not run a second competing background controller or use a written task file as a launch receipt. No Docker requirement.

Preserve history: the old discovery batch in `research/method-batch.json` and Q01 readiness report remain unfinished. They are not fabricated qualifications for this engineering source. If pursuing a new scientific contribution, resume their real mathematical, selection, originality and experimental obligations. Do not edit a verifier or manufacture receipts to make it pass.

Critical implementation contracts:

- `forward_segment(tokens,memory)` predicts the **same** token positions; do not shift targets again. Internal SEG carries the segment-first prediction.
- Reader loops do not write memory. Only a completed non-EOS segment is publicly committed; partial prefixes stay in the serialized state.
- Prefix inference computes the complete causal hidden sequence, then projects only the last position to the vocabulary. Do not slice before coda or truncate teacher-forcing targets. Read the equivalence proof in research/SIGMA_REVIEW.md before changing this path.
- Writer needs subsequent-segment loss through an untruncated within-window graph. Do not detach each segment. Keep document resets and TBPTT detaches distinct.
- Preserve pinned asset bytes, native bAbI/LAMBADA IDs/scorers and full denominators. Software fixtures are not scientific evaluation.
- Keep pretraining and bAbI adaptation target/context budgets distinct. Report all arms/seeds, actual elapsed cost, skipped optimization and failed attempts.
- Resume only compatible checkpoint/data/config/source; reconcile real host/PID and lock before retrying a lost launch. Never silently overwrite a live run or reset accumulated budgets.

GitHub destination is `Yunbo-max/latent-world-model`, branch `main`, already authorized by the owner. Use one integration writer and expected-parent updates, preserve concurrent work, and read back actual files at the exact remote commit. No HF output destination or training-host connection was supplied to Web; do not invent either or upload weights/data elsewhere.

Full-plan contracts:
- Follow-up checkpoint/input integrity review: read rounds/full-plan-2026-10-08/CHECK_REVIEW.md. Checkpoint payloads and hashes come from the same opened descriptor; weights-only initialization also requires equal tokenizer identities. New source and tests remain generated_unexecuted; old live runs and source-bound stream/plan snapshots stay pinned to their original implementation.
- Read IMPLEMENTATION_GOAL, EXPANSION_SPEC, COVERAGE and current experiment/review files at the same commit; stronger ideals are not executable/theorem claims.
- For target row u query only tokens[:u] and prior completed events. Never use a target/future suffix, support labels or evaluator answers in retrieval. Use current learned embeddings and per-row selected memory, not a cross-row unrestricted union.
- Event identity is document+ordinal, public input identity a separate caller chunk ID. Validate admission before writer; identical stable-ID retries are no-ops, conflicts reject. Chunk receipts survive EOS; document segment receipts do not. Count O(history) receipts and actual RSS/cost.
- Keep observed_text, generated and scored_continuation per-token provenance/source. Generated content is not external evidence. Teacher-prefix parity requires the same store/provenance; it is not a claim that all different source policies coincide.
- Plan realization receives only Z; save/restore binds context/source/config/tokenizer/checkpoint. Missing-format legacy stream state is v0 only; no source-identity downgrade or silent migration.
- Contractive branch requires fixed forcing, current differentiable matrix norm and no h-dependent attention/norm/residual bypass. Bound is real arithmetic; residual is diagnostic, never Q01/readout truth certificate. Fixed K remains adopted.
- State CE predicts the next segment's first token only when that position is eligible, from previous post-write M; it never scans forward past masked context for a later target. The target is used only in loss. Main denominator remains main target count; auxiliary observations are separately counted repeated labels. Preserve within-window writer gradients and cross-document resets.
- Matrix 13 arms x2 seeds:2.6B/26B pretraining targets plus26M adaptation per tier. Do not claim parameter/cost matching for architectural removals/replacements. All tests/native/GPU experiments are pending Local; do not execute project code/tests as Web or assign them to reviewers.

Expanded construction contracts: exact CPU store is appended only after prediction/complete admission; per-row query ends before target; no query union across future rows. Stable chunk receipts are checked before prefix/writer mutation and persist across EOS. Raw retention is bounded but receipts grow. Generated/scored/observed origins and source locators remain distinct. Optional plan realization consumes only persisted Z, with no reader callback. Fixed-forcing contraction has a real-arithmetic state bound, no output/roundoff/adaptive guarantee. Auxiliary CE is normalized by main target count and eligible pairs are logged separately; held-out main NLL is never the composite loss.

Second audit: read rounds/full-plan-2026-10-08/RECHECK_REVIEW.md and research/METHOD_EXPLAINED.zh-CN.md at this revision. Query scan counts bill visible index candidates; separate index construction still visits retained raw tokens. Positive-temperature sampling centers and scales in FP64, preserving maxima under CUDA reciprocal overflow; actual CPU/CUDA tests remain pending Local. Generated raw-position filtering does not remove generated content from the compressed continuation M.

Use configs/full_plan_experiments.json for the current13-arm/2-seed full matrix, retaining all v0 controls. Budget totals2.6B/26B pretraining plus26M separately counted adaptation targets. Native full denominators and paired/four-arm interaction are required. The current independently queried source reviews are EPISODIC_SOURCE_REVIEW, DYNAMICS_SOURCE_REVIEW and INTEGRATION_SOURCE_REVIEW in the full-plan round; inherited CONTINUATION reports are historical draft records; Local tests/native/GPU evidence remain pending. Historical original-method gates and Q01 remain unchanged.
