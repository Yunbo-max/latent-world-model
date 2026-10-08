# Web handoff: sigma-review-2026-10-08

Destination: `Yunbo-max/latent-world-model`, literal `main`. Parent inspected: `a8a86cf359ac0d8598ac7b2fa6465ffa120718ae`; all 61 parent files were recovered and checked against their remote Git blob IDs. The publication receipt supplies this round's exact new commit after readback.

**Status: generated_unexecuted.** This is the user-requested continuation and Sigma reading round, preserving the [complete initial packet](../engineering-2026-10-07/WEB_HANDOFF.md). Experiments remain Local-owned. No project tests, imports, model/data downloads, training, inference or native scoring were executed by Web. No separate Goal service or GPU job is claimed.

## Decision and concrete delta

Read [SIGMA_REVIEW](../../research/SIGMA_REVIEW.md) for source locators, publication availability, the model/objective boundary, exact row-selection derivation, hardware/budget accounting and falsifiers. This round retains the adopted text predictive-state construction. It adds no new scientific candidate or artificial discovery qualification.

- `src/lwm/model.py`: `predict_prefix` selects the final hidden position after the full coda, before final RMSNorm/vocabulary projection. Training keeps all target rows; writer, state, parameter names/shapes and data contract are unchanged.
- `src/lwm/evaluate.py`: evaluation settings explicitly record the prefix projection policy and absence of KV caching.
- `tests/test_model_semantics.py`: source for output/allocation-contract and gradient parity acceptance. No runtime pass is claimed.
- [FULL_MODEL_PROPOSAL](../../research/FULL_MODEL_PROPOSAL.md), [MATH_TO_CODE](../../research/MATH_TO_CODE.md), [EXPERIMENT_DESIGN](../../research/EXPERIMENT_DESIGN.md): exact mapping, cost limitations and prospective selection ledger.
- [SOURCE_REVIEW](SOURCE_REVIEW.md) and [SOURCE_CHECKS](SOURCE_CHECKS.json): actual scoped source review and static-only verification, created before publication. Prior receipts remain at their original paths/revisions.

## Local Codex: start here

At the delivered commit, read [AGENTS](../../AGENTS.md), [LOCAL_AGENT_RUNBOOK](../../LOCAL_AGENT_RUNBOOK.md), especially [Download datasets and models](../../LOCAL_AGENT_RUNBOOK.md#download-datasets-and-models), and this handoff. Reuse the user's actual SSH/native execution harness, installed Conda and cumulative limits. Restore real host paths; no host locator was available to Web.

Follow the existing ordered cards: qualify environment and pinned complete assets → full software and native acceptance → finite training profile → admit complete cumulative matrix cost → train/evaluate/replay → E04 and result return. New source requires its own actual acceptance. Preserve older live workspaces and checkpoints; moving main cannot retarget a running job. A changed source fingerprint must not be bypassed to resume training.

The existing setup/data commands and asset revisions remain sufficient. No additional Sigma checkpoint, model or dataset is downloaded. Model weights from an older run can be evaluated as fixed weights if their existing checkpoint/tokenizer contract passes; retain both training-source and evaluation-source identities. This does not authorize relabeling the old training run with the new revision.

Run the complete authored suite through Local's admitted execution task:

```bash
conda run -n lwm python -m pytest
```

If the new path fails, inspect the two prefix tests, causal/teacher parity tests, `_read` and SIGMA_REVIEW §3. Do not delete the numerical comparison or move slicing ahead of attention. Tests checking tiny integer tensors are software checks, not scientific evaluation. Actual CUDA numerical qualification and peak memory/latency remain pending.

## Complete experiment obligations

The supplied five arms × seeds 17/29, full 20 bAbI tasks and all 5,153 LAMBADA passages remain selected. Primary inference uses the depth each arm trained with; decoder temperature is zero. Record actual development choices before test access as specified by EXPERIMENT_DESIGN §8. For optional inference-depth sensitivity, freeze and report the entire declared group; never select the best test setting as the primary result.

Generate the same complete 100M command inventory after acceptance:

```bash
conda run -n lwm python scripts/run_matrix.py --data-root data --output-root runs/matrix --budget 100m
```

The script writes 40 cards and launches nothing. Local binds real interpreters/paths, dependency receipts and resource admission. Each 100M arm/seed consumes 100M pretraining targets: the whole matrix consumes 1B, plus adaptation/profile/failed work. The separate 1B-per-run design totals 10B pretraining exposures and stays conditional on actual resources. Native scorer environments, bAbI teacher qualification and contamination limitations retain their pending status.

## Return evidence and uncompleted work

Return tests/native parity, actual hardware/profile, checkpoint/attempt inventory, all native predictions/replays and denominators, every arm/seed and failed attempt, cost/selection ledger and E04. Use a unique result path beneath this round, with execution commit and dirty diff, input/config/output hashes and real host/attempt locators. Transfer declared artifacts over the existing SSH path and verify bytes; retain large data/weights outside Git. Publish appropriate small result summaries to the already authorized repository, preserve concurrent main work and read back the exact commit.

Still pending: Local environment/assets, executed semantic tests, complete native teacher/tokenizer/scorer qualification, GPU fit/throughput, cumulative budget admission, training and scientific results. The historical Q01/20→15 discovery obligations remain unfinished separately. Report the actual result repo/commit/packet locator for the next Web review.
