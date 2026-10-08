# Second source audit, repairs and method explanation

Request: “你需要重新检查一遍，然后改正，然后跟我说下整个方法的思想”, 2026-10-08. Baseline main: fa75982cb9258047189651547381b4582b7eaec9; all115 remote blobs matched the local source before edits. Source status remains **generated_unexecuted**. No project imports, tests, asset downloads, training, inference, scoring or GPU workloads were executed by Web.

## Fresh independent scopes

| Actual reviewer | Source reviewed | Conclusion / bounded follow-up |
|---|---|---|
| /root/reaudit_model | model, episodic store, model/episodic/expansion fixtures and adopted spec | Confirmed one query-scan accounting defect and the successor-token wording ambiguity; repair/test deltas independently reread |
| /root/reaudit_training | trainer, data cursor, checkpoint/resume, masks/AMP/budgets/configs and training fixtures | No new demonstrated training/checkpoint blocker; method prose independently checked; runtime acceptance remains pending |
| /root/reaudit_stream | streaming generation, realization, serialization/provenance and fixtures | Confirmed accepted-temperature numerical edge; repair/device fixtures independently reread; no new supported-stream Important/Critical finding |
| /root/reaudit_eval | native preparation/parity/evaluation/scoring, matrix/config/runbook | No demonstrated Important/Critical evaluation/matrix defect; separate replay receipts remain an explicitly disclosed evidence-packaging limitation |

Reviews are source inspection, not executed behavior or a guarantee of bug freedom. Earlier review records retain their original byte/version bindings.

## Confirmed source changes

**Visible-candidate accounting.** The query loop in EpisodicStore.retrieve iterates the source-filtered index, but its events_scanned field previously counted every retained event. A retained all-generated event is valid and excluded by default, yet was billed as one scan per row. The counter now uses len(index). Index construction still separately bills all retained raw-token visits, including excluded positions. Predictions and selection order are unchanged.

Authored acceptance checks use mixed observed/generated events with cached and freshly built indexes, and a real neural read with only generated history. The latter expects three prediction rows, zero candidate scans, four index-token visits, no retrieved token and equality to an empty store. No benchmark scores are inferred from these fixtures.

**Finite positive-temperature sampling.** The public input check accepts any finite positive Python temperature and finite FP32 logits. Direct FP32 division can create infinities/NaNs at temperature1e-50 or with large finite logits at ordinary positive temperature, making softmax/multinomial fail. Sampling now subtracts the maximum in FP64, scales the resulting nonpositive vector, restores exact maxima/ties to zero, applies softmax, then casts probabilities to FP32 for the existing multinomial draw.

The maximum restoration is necessary for the pinned PyTorch2.5.1 CUDA scalar-division implementation: it can compute reciprocal(temperature) first, which overflows at the minimum positive Python double5e-324; without restoration, zero times infinity is NaN. Root independently read the primary kernel [BinaryDivTrueKernel.cu](https://github.com/pytorch/pytorch/blob/v2.5.1/aten/src/ATen/native/cuda/BinaryDivTrueKernel.cu), Git blob aa955a9c7e546ca351ca669b94c318a498360e6b. Negative infinities are legitimate zero-probability categories, and at least one maximum remains zero/positive mass. Finite FP32 subtraction cannot overflow after promotion to FP64.

CPU and CUDA regression cases were authored for1e-50,5e-324 and finite huge FP32 logits, with device-local tensors/generators. Only the upstream model-logit boundary is controlled; the real generate/multinomial/provenance/state operations remain under test. The greedy native matrix path is unchanged. Positive-temperature numerics have changed, so source-strict old stochastic snapshots stay pinned and cannot be silently resumed on this revision. Measure actual FP64 vector-transform cost locally.

Core regression source was authored before its repair, but no red/green run or TDD-pass evidence exists because Web is not the execution owner.

## Corrected explanation and handoff

- Auxiliary supervision predicts the next segment's first token only if that position is eligible. It does not scan past masked context for a later target. README/AGENTS now agree with the existing algorithm and EXPANSION_SPEC.
- The existing plan projection is affine with trainable bias. The exact equation now includes b_z in EXPANSION_SPEC, COVERAGE, MATH_TO_CODE and the explanation; no model parameter or computation was changed for this clarification.
- Persistent compressed M and temporary H are separated. M is not established as calibrated factual belief. Generated raw positions are excluded by default, but generated tokens still enter the returned branch's prefix and completed-segment compressed state.
- The output remains autoregressive. A saved causal Z sequence realizes one next-symbol distribution; it is not a complete sentence code. A new token triggers a new plan.
- WEB_HANDOFF now names its historical source/delivery/reviewer records as historical. Its former “present followup changes docs only” and “task remains enabled” sentences no longer misdescribe this foreground revision. Existing task state and scientific discovery gates were not mutated.

The [complete Chinese method explanation](../../research/METHOD_EXPLAINED.zh-CN.md) maps the actual M/S/P/H/Z objects, prefix-specific retrieval, fixed-forcing versus Transformer recurrence, gated writer, three counters, objectives, gradient windows, autoregressive expression and native comparison scope. It preserves the unfinished stronger scientific goals.

## Disclosed limits that did not justify another algorithm change

The trainer binds resume to train corpus/config/source but not to the optional validation-corpus identity. Each validation event records its actual fingerprint; the fixed matrix paths preserve the selected split. Switching or omitting validation on resume is a development-ledger limitation, not silently changed training state or a passed benchmark. Retain actual fingerprints and the fixed handoff inputs.

Comparison/interaction records bind completed evaluation files and preserve pending evaluator metadata, while native aggregation replay supplies separate hash-bound receipts/dependencies. The runbook requires retaining both. A separate replay cannot promote adapter/Teacher qualification to passed. No erroneous statistic or falsely passed qualification was demonstrated in the adopted DAG.

All actual CPU/CUDA passes, writer/auxiliary/nonempty-retrieval FP16 backward, GradScaler overflow/skip/resume, full native Teacher/tokenizer/model/scorer parity, GPU feasibility/cost and complete trained experiments remain pending. Fixed K, no adaptive readout certificate, unproved predictive sufficiency, unidentified sentence semantics and absence of physical-action dynamics remain explicit. This repair does not qualify novelty or the historical discovery batch.

## Local acceptance and publication

Read same-revision AGENTS, LOCAL_AGENT_RUNBOOK and WEB_HANDOFF first, preserve old live attempts on their pinned source, and run the complete suite through the existing Local execution owner:

~~~bash
conda run -n lwm python -m pytest -q
~~~

After a failure, use the targeted command in the handoff/runbook; do not repeat a passed whole suite merely to generate a narrower receipt. Inspect CUDA skips and actual logs, source/environment identity, device behavior and costs. No new assets, model weights, services or Docker are required by this repair.

Fresh standard-library AST/JSON/TOML parsing and report hash checks support source syntax/identity only. Main publication uses expected-parent non-force update and exact changed-file readback; the publishing session reports its concrete commit after success.

## Current changed source identities

| Path | SHA-256 |
|---|---|
| src/lwm/episodic.py | ecef5998c936bc6912ced9b41dfb68ed53aece4e467cb3fa1966cdcc7d28adce |
| src/lwm/generation.py | 9f51a0b00f48b3bb44b8a4cb23e3a0bc770906469daa0ee802dad3036b3105ad |
| tests/test_episodic_semantics.py | 674212e63742b7cd1d88eec5ce7dca538483907dea51f89767bb02af34443457 |
| tests/test_generation_semantics.py | 4ead43a301e464d319cb6f708a622094dfb427900d969f1568fbfe1f928930bb |
| research/METHOD_EXPLAINED.zh-CN.md | 01e71c40e1c4dba126a9e3e80480131598ea111c0f0a737377437d605276f43e |
