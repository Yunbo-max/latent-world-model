# Finite source-delivery review — 2026-10-08

Status: **generated_unexecuted**. This packet closes a concrete native-data acceptance interface gap; it does not convert the adopted autoregressive model to Sigma diffusion. Parent main restored and checked: `cb98c6c6a668e35930d382771d06e6d6067a9f9b`. All 65 baseline file blobs matched the exact remote tree before changes. Publication uses the actual expected parent, non-force update, then exact-commit file readback.

## Delivered change and source evidence

The earlier runbook required full bAbI Teacher-export comparison but had no executable comparator. `src/lwm/native_parity.py` now compares all 60 task/split exports against prepared records: 220,000 questions and 68,928 episodes across train/valid/test. It checks exact ordinal text, labels, reward, episode boundaries/index/turn, native task denominators, clean pinned author source, file hashes and final inventory. It retains failure evidence, refuses output-directory reuse and publishes success only after all tasks pass. A data-parity receipt does not qualify the model adapter, scorer or full exporter environment.

Pinned author source inspected: ParlAI `a29567f7ce76992fd1f03c51ba9e3b155a37ea51`, `parlai/utils/misc.py`, `parlai/scripts/convert_data_to_parlai_format.py`, `parlai/tasks/babi/agents.py`. The checker uses the actual author's `str_to_msg`; canonical omitted False and blank episode separators follow the exporter. An explicit `episode_done:False` is rejected because upstream parsing uses `bool(value)`.

An independent read-only reviewer found two publication-integrity gaps: previously consumed prepared files could change late, and an extra export could appear after the initial inventory. Both were fixed with final snapshot verification. Follow-up source review found no remaining Critical/Important issue; canonical separators and late mutations now have authored regression cases. Neither reviewer nor integrator executed project code, imports or tests.

Static validation in this run: standard-library AST parsing of 20 Python files, JSON parsing of 24 existing JSON files, and TOML parsing of one file; 73 test functions counted statically (63 prior + 10 new). These are syntax/source observations, not passing software tests. Prior source review remains in the [Sigma packet](../sigma-review-2026-10-08/WEB_HANDOFF.md) and [initial full packet](../engineering-2026-10-07/WEB_HANDOFF.md); unchanged legacy source was not represented as a new exhaustive line-by-line audit.

## Delivery and remaining qualification

| Area | Implemented | Source-reviewed | Local still required |
|---|---|---|---|
| Mathematical model | Causal prelude, persistent memory, shared recurrent reader, coda/readout, separate writer | Adopted derivation and math-to-code map; prior independent causal/gradient review retained | Numerical/gradient contracts, instantiated parameter count |
| Training and streaming | Target alignment, document resets, TBPTT, complete-segment commit, strict checkpoint/cursor resume | Source contracts reviewed; current source unchanged | All software tests, resume/interrupt acceptance |
| Assets and native parity | Fixed asset identities, acquisition/preparation; new full bAbI export comparator | Pinned author parser/exporter and independent new-code review | Actual downloads, full Teacher installation/export, all 60-file parity and LAMBADA tokenizer/adapter acceptance |
| Evaluation | Full bAbI 20,000 and LAMBADA 5,153 inference, native scorer replay, paired comparison | Existing full protocol review retained | Actual inference, native replay and statistical results |
| Experimental design | Five arms × two seeds; 100M/1B per arm/seed; adaptation separate | Budget, selection/confirmation, failure and stop rules retained | RTX 2080 Ti memory/time measurements; admit 1B extension only from actual evidence |

The full matrices cost 1B or 10B pretraining target tokens respectively; bAbI adaptation/context/evaluation are additional. No test success, native qualification, GPU feasibility, speed or scientific conclusion is claimed. The historical 20→15 originality/discovery obligations remain unfinished and no gate/verifier is changed.

## Local entry and exact next actions

Read [AGENTS](../../AGENTS.md), [runbook](../../LOCAL_AGENT_RUNBOOK.md), [native environments](../../research/NATIVE_ENVIRONMENT.md), [model proposal](../../research/FULL_MODEL_PROPOSAL.md), [math mapping](../../research/MATH_TO_CODE.md) and [experiment design](../../research/EXPERIMENT_DESIGN.md) at this same delivered revision.

1. Restore the real Local host, record runtime/source identity and acquire pinned inputs through the runbook. Run the authored software suite and retain failures/skips; skips are not native qualification.
2. Attempt the documented complete Python 3.8 author Teacher environment with its unmodified dependency rules. The known openai/litellm candidate conflict remains unresolved until an actual resolver/import/export receipt exists. Do not replace this with metrics-only qualification.
3. Produce all 60 real author exports, then use the separate Python 3.11 `lwm-parlai` environment for:

```bash
env CUDA_VISIBLE_DEVICES="" PYTHONPATH="$PWD/src" \
  conda run -n lwm-parlai python -m lwm.native_parity \
  --data data/babi --exports assets/babi/native \
  --native-source external/ParlAI \
  --output artifacts/babi-teacher-parity
```

Success creates `babi-teacher-parity.json`; failure creates `failure.json` and exits nonzero. Use a new output path for a deliberate retry. Keep separate exporter installation/import/export receipts. Optional native acceptance-test environment variables are documented in the native environment card. Complete model-adapter, tokenizer and scorer qualification separately.

4. Measure resources before admitting the experiment matrix; follow the existing lock/resume/debug/result-return instructions. Adding a module changes the all-source checkpoint identity: use the complete new revision for new runs; do not bypass incompatible-source resume guards for an older checkpoint.
5. Return exact revision, environment/install logs, test results including skips, native parity/replay receipts, resource costs and any failures. Source delivery ends here after publication verification; it does not wait for experiments or create a new monitoring task.
