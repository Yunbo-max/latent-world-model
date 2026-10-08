# Expanded original-plan source handoff

Latest follow-up: read [CHECK_REVIEW](CHECK_REVIEW.md) at this same revision. The follow-up repairs checkpoint load/hash identity, weights-only tokenizer compatibility and the pinned empty-context prefix-token branch. Added acceptance cases are in test_checkpoint_identity_semantics.py, test_resume_semantics.py and test_scoring_semantics.py. All source is still generated_unexecuted. Earlier whole-tree/publication receipts below describe their historical commits; they do not certify this repair or replace Local checks.

Status: **generated_unexecuted**. Sole integration writer: root. Parent main restored: fba4653780e0b277a1fe7fdef47e3f20d33f2d53, descendant of the reopened6c799d9 checkpoint. All69 original blobs were read via pinned Git object URLs and their actual Git blob hashes checked. Existing unpublished expansion work was retained and statically rereviewed. Publication is non-force with expected-parent protection; exact final commit/readback is reported by the publishing session.

Read same-revision [AGENTS](../../AGENTS.md), [Local runbook](../../LOCAL_AGENT_RUNBOOK.md), [coverage](COVERAGE.md), [executable specification](EXPANSION_SPEC.md), [expanded design](EXPERIMENT_DESIGN.md), [math mapping](../../research/MATH_TO_CODE.md), and [native environments](../../research/NATIVE_ENVIRONMENT.md). Existing tokenizer/corpus/scorer/author acquisition commands in the runbook remain complete and unchanged; no new assets/weights/services are needed.

## Source delivered

Exact-event FIFO store/retrieval with per-token source/provenance, stable receipts and replay protection; causal neural consumption; optional separately persisted plan/realization; explicit three-clock stream state; optional globally contractive fixed-forcing workspace; proper compressed-state next-segment categorical supervision; full train/validation/checkpoint/generation/native evaluation wiring. v0 disabled-extension path/configs retained. [Coverage](COVERAGE.md) distinguishes actual constructs from broader unsolved theoretical ideals.

Current independently queried Web reviewers are `/root/episodic_spec_review`, `/root/dynamics_spec_review` and `/root/full_chain_review`. Their EPISODIC/DYNAMICS spec/source reports and INTEGRATION_SOURCE_REVIEW bind actual source bytes, with findings and resolutions retained. Inherited [state](CONTINUATION_STATE_REVIEW.md) and [training/native](CONTINUATION_TRAINING_REVIEW.md) draft reviews are historical supplied records, not live identity certification by this invocation. Their actual held-out head CE, gradient inventory and full-native four-arm interaction repairs are preserved and independently reread. No reviewer runs project code/tests. Source parsing/hash/link checks are not a software pass.

## Ordered Local acceptance

All following are authored inner commands, never executed by Web. Admit them through the already installed Local controller/SSH/native harness at the actual staged checkout. Retain actual stdout/stderr/status, source identities, skips and failures. No Docker/GPU work was started here.

1. Recover actual SSH/GPU/env/checkout/cumulative budgets. Acquire and verify all pinned inputs using the runbook's exact commands. Full bAbI Teacher environment/install/export remains qualification-pending, separately from metrics-only replay. Preserve all20/20000 and LAMBADA5153.
2. Run the complete software suite, then inspect actual skips and CUDA cases:

```bash
conda run -n lwm python -m pytest -q
conda run -n lwm python -m pytest tests/test_checkpoint_identity_semantics.py tests/test_episodic_semantics.py tests/test_expansion_semantics.py tests/test_resume_semantics.py tests/test_scoring_semantics.py -q
```

The second command is a focused diagnosis after a failure, not a redundant mandatory rerun after a complete pass. Required properties: strict future isolation, equal-store teacher/prefix rows, FIFO/evicted replay, mixed-origin/source retention, changed chunk rejection before writer, crossEOS chunk retries, branch isolation, full state restore, independent plan realization, contractive norm/gradient checks, main/aux mask/denominator/counter separation and uninterrupted/resumed trainer parity. Software fixtures are not scientific benchmarks.
3. Execute full native Teacher export parity and model/tokenizer/scorer parity using existing NATIVE_ENVIRONMENT/runbook commands. A replay receipt cannot replace adapter/forward qualification. Keep installation conflicts and skipped native cases pending until real resolution.
4. Profile the actual full branch with accepted native training inputs and its own output directory:

```bash
conda run -n lwm python -m lwm.train --config configs/full_loop4_100m.json --data data/fineweb-100m/train --validation data/fineweb-100m/valid --output runs/profile-full-loop4 --max-updates 10
conda run -n lwm python scripts/summarize_run.py runs/profile-full-loop4 --project-tokens 100000000
```

Measure the necessary different active architectures/access envelopes, total budget and all failed attempt costs before matrix admission. Do not infer13-arm time from a single branch. CPU history receipts grow with document/stream length despite bounded raw retention.
5. Generate the complete204-card matrix from the expanded design. Inspect its native environments/dependencies and freeze development selection/cumulative resource budget before actual dispatch:

```bash
conda run -n lwm python scripts/run_matrix.py --design configs/full_plan_experiments.json --data-root data --output-root runs/full-plan --budget 100m
```

Admit one GPU workload at a time; CPU replay/collection may proceed under actual shared bounds. Resume paused runs only with exact compatible source/config/assets; existing older-source active runs remain pinned. A new weights-only child is distinct from compatible training resume.
6. After real accepted training, exercise independent plan expression and stream resume:

```bash
conda run -n lwm python -m lwm.generation --checkpoint runs/full-plan/full_loop4-100m-seed17/pretrain/last.pt --tokenizer data/tokenizer --prompt 'The story begins' --observation-id demo-prompt-1 --max-new-tokens 0 --plan-out artifacts/text-plan.pt --state-out artifacts/text-state.pt
conda run -n lwm python -m lwm.realization --checkpoint runs/full-plan/full_loop4-100m-seed17/pretrain/last.pt --tokenizer data/tokenizer --plan artifacts/text-plan.pt --output artifacts/realized-plan
conda run -n lwm python -m lwm.generation --checkpoint runs/full-plan/full_loop4-100m-seed17/pretrain/last.pt --tokenizer data/tokenizer --state-in artifacts/text-state.pt --max-new-tokens 64 --state-out artifacts/text-state-next.pt
```

Create `artifacts` as part of actual accepted setup if absent. Plan snapshot realizes one next symbol from a full causal plan sequence; the final command demonstrates normal replanning as symbols change. It is not a frozen sentence-level semantic codec. Repeat the same prompt only with the same observation ID/content to verify a no-op; changed content under that ID must fail. Generation's branch retains generated provenance.
7. Native replay/paired/interaction cards produce complete hash-bound outputs. Return all seeds/tasks, original and expanded active parameter/cost inventories, aux counts, real failures and E04 review. Main/test selection rules, conditional intervals and unresolved originality in the design remain applicable. No paper efficacy claim follows from source delivery.

## Exact remaining limits

Software/native/GPU qualification and results remain pending Local. Predictive sufficiency, identified semantic meaning, action/world dynamics and historical Q01/adaptive stopping are not claimed achieved. BF16 snapshot hashing is outside the supported FP32/FP16 profile. No core algorithm is left as a TODO in the selected executable text construction. Source-delivery completion depends on final main readback; runtime qualification does not need to have occurred before this handoff.


## Publication identity

This packet is the exact commit containing this handoff; the publishing invocation supplies its concrete SHA after non-force expected-parent main update and byte-for-byte readback. All current reviewed source modules, configs and runbook are included. The existing task remains enabled until that expanded endpoint is verified; closure receipt is recorded separately afterward, never inferred from the old v0 closure.


## Verified expanded publication

The executable source/config packet is d8ee2a98208c9e4e68ceadae11c4fe4d2dc10564. This invocation read all111 files at that exact commit, then reconciled ace232e2fbdbcd0d250b049c6b4eeac82e3f6323 closure metadata. The present followup corrects reviewer attribution/bindings, gate notation, command64/204 counts and current handoff/status only; no executable source/config is replaced. Existing DELIVERY_RECEIPT.json is preserved. The same source task is already disabled and was independently queried; no duplicate task or second disable is issued. All Local acceptance and stronger unimplemented scientific ideals remain as listed above.
