# Local Codex: execution and acceptance guide

**Source status: generated_unexecuted.** Web authored the files and reviewed their semantics; no project tests, asset downloads, training, inference or benchmark runs were executed. Use this guide at the commit identified in the delivery receipt. Do not treat the current source packet as measured GPU fit, a passed native evaluation or a new-method claim.

Current expanded handoff: [full-plan-2026-10-08](rounds/full-plan-2026-10-08/WEB_HANDOFF.md). Read its adopted specification, coverage and experiment design at the same commit. The v0 commands below remain usable controls; the full-plan supplement at the end gives the expanded source acceptance and actual new endpoints. All commands remain unexecuted by Web.

Prior v0 increment: [sigma-review-2026-10-08](rounds/sigma-review-2026-10-08/WEB_HANDOFF.md), followed by [delivery review](rounds/delivery-review-2026-10-08/WEB_HANDOFF.md). Those historical acceptance scopes remain alongside the original guide below. The Sigma optimization changes only last-position vocabulary projection placement; the present full-plan extension adds explicitly configured modules. Source-strict training resume rejects a changed revision: preserve active runs at their pinned source. No Sigma weights or additional corpus are required.

## Restore the actual execution context

On the user's computer, recover the already configured GPU SSH alias, authenticated delivery checkout, remote project directory, Conda installation and current cumulative resource limits. No such host locator was available to Web. Verify the remote `nvidia-smi` inventory, available VRAM, competing processes, driver, CPU/RAM/disk and ownership before native work. The design assumes one visible device; the user named RTX 2080 Ti, but the actual count/availability must come from that host.

Fetch the exact delivered commit into an isolated compatible checkout, preserve live attempts and local changes, and read AGENTS plus the round handoff. Stage that same source onto the real GPU host using the existing Local SSH/file-transfer workflow; do not copy Web scratch paths into a remote command. Record both roots and the exact execution commit/dirty diff. No remote agent/GitHub credentials are required on the GPU machine merely to execute code.

All commands below are **inner task commands** on the GPU host, with working directory equal to the actual staged project root. Local submits them to its existing `run_harness.py`/SSH execution owner with real resource bounds, not a second shell daemon. Preparation/scoring tasks request zero GPU; training/inference request one accepted device. The outer task must preserve logs, native exit status, actual PID/session/host identity and cumulative budgets. Resolve the installed harness version and CLI from its real guidance; this project does not invent a runtime alias or a fake launch ID.

## Native environment

Use a dedicated Conda environment. Inspect the exact installed Conda and driver before choosing the sourced CUDA wheel; the following is the authored CUDA 12.1 profile, not an installation receipt:

```bash
conda create -n lwm python=3.11 pip=24.3.1 -y
conda run -n lwm python -m pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cu121
conda run -n lwm python -m pip install -e '.[test]'
conda run -n lwm python -m pip check
conda run -n lwm python -m pip freeze
```

The PyTorch wheel command is sourced from [official previous-version installation instructions](https://docs.pytorch.org/get-started/previous-versions/). `pyproject.toml` pins direct project dependencies. Retain the actual `pip freeze`, Python/PyTorch/CUDA/driver outputs and installation logs; this is not a solved universal transitive lock. A dependency/CUDA failure blocks execution and requires a source-supported native environment repair. Do not silently upgrade the entire stack or use Docker.

Official score replay uses the separately sourced environments and installation cards in [NATIVE_ENVIRONMENT.md](research/NATIVE_ENVIRONMENT.md). Preserve their native revision and actual dependency resolution independently of the model environment.

## Download datasets and models

The model trains from scratch: **no pretrained model weights are required**. The tokenizer is the pinned GPT-2 tokenizer only. All upstream repositories, revisions, required files and hashes are in [configs/assets.json](configs/assets.json) and [DATA_PROTOCOL_PROPOSAL.md](research/DATA_PROTOCOL_PROPOSAL.md).

The commands below acquire complete selected files via the supported Hub SDK or checksum-verified author archive. They preserve source caches; prepared output directories must be new/empty. Reuse a complete previously verified preparation rather than overwriting it. An interrupted preparation has no complete manifest and is not valid input; preserve its evidence, then prepare into a new output directory. The source cache may be reused. Do not delete a cache used by another live task.

```bash
conda run -n lwm python -m lwm.prepare tokenizer --cache assets/cache --output data/tokenizer
conda run -n lwm python -m lwm.prepare fineweb --tokenizer data/tokenizer --cache assets/cache --output data/fineweb-100m --tokens 100000000
conda run -n lwm python -m lwm.prepare babi --tokenizer data/tokenizer --cache assets/cache --output data/babi
conda run -n lwm python -m lwm.prepare lambada --cache assets/cache --output data/lambada
```

For the separately admitted 1B profile:

```bash
conda run -n lwm python -m lwm.prepare fineweb --tokenizer data/tokenizer --cache assets/cache --output data/fineweb-1b --tokens 1000000000
```

FineWeb preparation downloads at least the first two pinned Parquet shards (4,305,041,546 bytes), then additional listed shards only as required. All 14 total 28,518,193,415 bytes, within a 30 GB source-byte cap. Plan at least 50 GB input/preparation disk plus separate Conda/checkpoint/results capacity, then measure actual availability and peaks. The 1B token binary itself is 2 GB, excluding indexes/heldouts. Source sizes do not predict total experiment storage.

Required outputs:

| Asset | Complete local paths | Qualification |
|---|---|---|
| tokenizer | `data/tokenizer/{config.json,merges.txt,tokenizer.json,tokenizer_config.json,vocab.json,preparation.json}` | Exact five upstream Git blob IDs, actual SHA256, vocab=50257/EOS=50256; no weights |
| FineWeb | `data/fineweb-100m/{train,valid,test}/{tokens.bin,index.jsonl,manifest.json}` plus `preparation.json`/content hash index | Exact 100M train, 1M valid, 1M test targets; source SHA256/bytes; no split hash overlap; same deterministic prefix rules for 1B |
| bAbI | `data/babi/{train,valid,test}.jsonl`, `preparation.json`, `sft/{train,valid}` token corpora | 20 tasks; train179998/valid20002/test20000 questions and expected episode totals; labels/candidates excluded from context |
| LAMBADA | `data/lambada/lambada_test.jsonl`, `test.jsonl`, `preparation.json` | Original fixed SHA256 and 5153 native rows; prepared ID/order/text parity |

Preprocessing ordinary FineWeb text sets `split_special_tokens=True`; native benchmark text uses the official default tokenization. Source document boundaries, final EOS and budget-truncated tails are explicit. Corpus loading verifies its token/index byte hashes. Local must additionally compare actual native bAbI parser output against the author teacher export and actual LAMBADA token boundaries against the pinned harness on its real rows; writing a hash manifest does not prove native semantics.

## Software and native-interface acceptance

Run the complete authored software suite, retaining the command, actual exit status and full stdout/stderr:

```bash
conda run -n lwm python -m pytest
```

The important properties are causal target isolation; teacher/prefix equality including boundaries; writer gradient from later segments; explicit detach; bounded/functional memory; exactly-once commit/EOS behavior; corpus counts; and uninterrupted-versus-resumed optimization with a live partial document. These tests are ordinary software checks, not scientific task results. A static parse from Web did not execute them.

The current increment adds `test_prefix_projects_only_next_position_without_changing_logits` (empty/short/maximum fixture prefixes, K=1/4, memory/reset) and `test_prefix_projection_preserves_parameter_gradients`. The first checks that only one row reaches the final projection while all teacher-forcing rows remain; the second compares the derivative of the same last-token objective. The complete suite remains required. For diagnosis after a failure, the focused entry is:

```bash
conda run -n lwm python -m pytest tests/test_model_semantics.py -k prefix
```

These are authored acceptance cases, not a Web red/green test receipt. Record actual test results and numerical tolerances on the accepted software/device profile. The analytical reduction of one output tensor is not a measured peak-memory or latency result.

The projection-parity case is parameterized over CPU and CUDA in FP32, matching the current evaluator's dtype. CUDA skips due to an unavailable device do not qualify the user's GPU path. The new gradient comparison remains CPU FP32; no AMP prefix-parity claim is made.

Then complete the native data/teacher/scorer acceptance cards in DATA_PROTOCOL_PROPOSAL and NATIVE_ENVIRONMENT. After all 60 author exports exist, the exact full-row command is `python -m lwm.native_parity --data data/babi --exports assets/babi/native --native-source external/ParlAI --output artifacts/babi-teacher-parity`, run under the Python 3.11 `lwm-parlai` interpreter with `PYTHONPATH="$PWD/src"` and zero GPU as shown in NATIVE_ENVIRONMENT. Preserve its success or failure receipt; this comparison does not replace full-teacher installation/export logs. The bAbI author export commands operate on all 20 tasks and all native splits. Verify native_text/labels/episode boundaries by released file/order, not just a few invented cases. For LAMBADA verify full 5153 ID coverage and actual multi-subtoken targets, whitespace movement, no left truncation and correct greedy flags. Official aggregate replay alone cannot prove the model adapter generated correct LLs.

Expected stage evidence: input preparation identities, actual software log, native export/parser comparison, tokenizer/target parity, installed environment and a review tying those logs to this source commit. Keep each missing check pending. Do not fill in passed booleans from these instructions.

## Measure the real GPU before the matrix

After acceptance, run a finite profile on the actual native training corpus in a separate output directory:

```bash
conda run -n lwm python -m lwm.train --config configs/memory_loop4_100m.json --data data/fineweb-100m/train --validation data/fineweb-100m/valid --output runs/profile-memory-loop4 --max-updates 10
conda run -n lwm python scripts/summarize_run.py runs/profile-memory-loop4 --project-tokens 100000000
```

Expected status is `paused`, not completed training. Actual events record parameter count, GPU/capability/VRAM, peak allocation, elapsed seconds, processed/optimized targets and numerical skips. The summarizer excludes the first two updates and extrapolates the remaining observed rate; its projection excludes later validation, saves, evaluation, failures and other arms. Repeat only the profiles needed to resolve different memory/compute envelopes, then freeze the complete cumulative cost. Do not claim that a small profile proves an entire 1B run fits its time budget.

If OOM occurs, first distinguish external occupancy from intrinsic workload memory. Checkpoint/microbatch/accumulation changes may be profile repairs; L/m/d/U/K changes alter the model or learning and require a versioned design. Keep all comparison obligations and cumulative profile cost.

## Train and evaluate one complete arm

The following cards exercise the complete standard 100M arm. They are not a substitute for the full comparison matrix:

```bash
conda run -n lwm python -m lwm.train --config configs/memory_loop4_100m.json --data data/fineweb-100m/train --validation data/fineweb-100m/valid --output runs/memory-loop4-100m
conda run -n lwm python -m lwm.evaluate --checkpoint runs/memory-loop4-100m/last.pt --tokenizer data/tokenizer --task lambada --data data/lambada --output results/memory-loop4-100m-lambada --device cuda
conda run -n lwm python -m lwm.train --config configs/memory_loop4_babi.json --data data/babi/sft/train --validation data/babi/sft/valid --init-checkpoint runs/memory-loop4-100m/last.pt --output runs/memory-loop4-babi
conda run -n lwm python -m lwm.evaluate --checkpoint runs/memory-loop4-babi/last.pt --tokenizer data/tokenizer --task babi --data data/babi --output results/memory-loop4-babi --device cuda
```

Before using a checkpoint as a completed arm, inspect `status.json` and `last.pt` counters: `completed_target_budget`, exact seen target budget, optimized targets and all numerical skips must be consistent. A successful process exit after `paused` does not mean training completed. The default fixed-budget checkpoint, not best test performance, is the primary comparison point.

Before the first test evaluation, preserve the actual development ledger and frozen selection record required by EXPERIMENT_DESIGN §8. Primary settings are already fixed by the matrix; do not use optional K sensitivity to select a better test row. Record no extra tuning if none occurred, rather than inventing development runs.

The bAbI stage has its own 1M answer/EOS target budget and repeated native-train policy. Its much larger context exposure is reported separately; do not call the total training cost 100M. LAMBADA uses the pretraining checkpoint and is never used to tune it.

For a generated text continuation after real training:

```bash
conda run -n lwm python -m lwm.generation --checkpoint runs/memory-loop4-100m/last.pt --tokenizer data/tokenizer --prompt 'The story begins' --max-new-tokens 64 --state-out runs/text-stream.pt
```

`--state-in runs/text-stream.pt` resumes the saved partial prefix, memory and sampling RNG with the identical checkpoint/tokenizer, temperature and device type. On resume the saved RNG supersedes `--seed`. This state contains generated text history. To preserve an external-evidence-only state, use the functional API and retain the pre-generation input state; the generation branch never modifies it in place. A finite maximum output length bounds generation; EOS availability is not an almost-sure termination proof.

## Resume, logs and result collection

Resume a paused compatible run with the same config/corpus/source:

```bash
conda run -n lwm python -m lwm.train --config configs/memory_loop4_100m.json --data data/fineweb-100m/train --validation data/fineweb-100m/valid --output runs/memory-loop4-100m --resume runs/memory-loop4-100m/last.pt
```

Checkpoint contains optimizer/scaler, learned weights, data cursor, detached numerical memory, RNG, exact source/config/corpus and cumulative counters. It is written atomically when no accumulated gradients are pending. SIGINT/SIGTERM requests a save after the next normal accumulation update (or a loss-free TBPTT boundary), so interruption does not change AdamW grouping. Hard kill may leave only the previous accepted checkpoint. Preserve failed work logs and its cost. Failure events distinguish completed-window counters from an incomplete attempted window; the latter is an exposure upper bound. A saved boundary can replay work lost after it, so account for failed/repeated elapsed cost outside the checkpoint in the real harness ledger.

Each invocation has a soft time limit of at most 24 hours; finishing its normal accumulation boundary can exceed that deadline. The outer harness supplies a bounded hard-stop grace and preserves the prior checkpoint if termination is forced. This is not a fresh total-budget grant. Local retains the original cumulative allocation across invocations. The output lock records actual host/PID/start time. On stale lock, interrupted SSH or lost launch response, check that same host/process/attempt before removing anything or launching again. Never delete a lock solely because the chat lost context. An existing output directory only accepts its current checkpoint as the resume parent; an older checkpoint requires a new child output directory.

Events are `RUN/events.jsonl`; latest checkpoint `RUN/last.pt`; state `RUN/status.json`. Actual outer harness attempt stdout/stderr/receipt paths come from its real returned identity. Prediction/scoring output filenames are listed in the evaluator's `manifest.json`/result files. Keep raw predictions, target traces, failed/unscored inventories, native replay logs and every seed.

## Full matrix, official replay and comparisons

Generate the complete dependency-aware command inventory for all five arms and both seeds:

```bash
conda run -n lwm python scripts/run_matrix.py --data-root data --output-root runs/matrix --budget 100m
```

This creates 60 command cards (pretraining, SFT, LAMBADA, bAbI and both native replays for each arm/seed) and effective seed-specific configs. It launches nothing. Local supplies the exact native interpreter path and admits each card through the existing execution harness after software/native/resource qualification. Pause dependent cards when a training card is incomplete; continue independent admitted work within the same remaining budget. A requested 1B expansion uses `--budget 1b`, its separately prepared corpus and the same coverage, with measured cost and resource approval already in force.

Native scorer sources and installation are specified in NATIVE_ENVIRONMENT. After predictions exist, invoke actual official aggregation replay:

```bash
env CUDA_VISIBLE_DEVICES="" PYTHONPATH="$PWD/src" conda run -n lwm-parlai python -m lwm.scoring replay --task babi --data data/babi --predictions results/memory-loop4-babi/predictions.jsonl --native-source external/ParlAI --output results/memory-loop4-babi-native
env CUDA_VISIBLE_DEVICES="" PYTHONPATH="$PWD/src" conda run -n lwm-lmeval python -m lwm.scoring replay --task lambada --data data/lambada --predictions results/memory-loop4-100m-lambada/predictions.jsonl --native-source external/lm-evaluation-harness --output results/memory-loop4-lambada-native
```

The replay verifies the actual native checkout/import location and full IDs/denominators. Its result only qualifies the checked aggregation; model forward/tokenizer/teacher parity and scientific interpretation remain separate evidence.

Use `python -m lwm.scoring compare --left LEFT/predictions.jsonl --right RIGHT/predictions.jsonl --output COMPARISON_DIR` in the model environment for paired passage/episode bootstrap, with real completed output directories substituted from the command manifest. It checks run/input identities and reports its limited conditional-on-checkpoint uncertainty. Report both seeds and all20 per-task results; a bootstrap cannot manufacture independent training repeats or remove selection bias.

## Failure routing and return packet

| Observed failure | Read first | Repair boundary |
|---|---|---|
| Import/CUDA/version | setup stderr, environment freeze, `pyproject.toml`, actual driver/device | Repair identified native environment; no unrecorded broad upgrade |
| Missing shard/hash/source schema | prepare stderr, `configs/assets.json`, source cache and preparation manifests | Reacquire same immutable bytes; no replacement corpus or swallowed bad rows |
| Target/mask/writer gradient | failing software test, `model.py`, `train.window_objective`, MATH_TO_CODE | Repair actual formula/implementation discrepancy, then rerun affected and full acceptance |
| Checkpoint/cursor mismatch | last.pt source/config/data identities, `checkpoint.py`, `data.CorpusCursor` | Preserve old attempt; reviewed child run for changed semantics, not force resume |
| Native score/denominator | `prepare.iter_babi_examples`, `scoring.load_dataset`, actual author export/replay | No ID exclusions, denominator shrinking or custom replacement scoring |
| Numerical failure/slow/OOM | actual update/profile/device logs | Distinguish optimization, resource conflict and model size; preserve all budgets/controls |
| Poor valid/test results | implementation/native qualification, all arms, split and training exposure | Complete E04 before a mechanism verdict; do not tune on test or hide negative runs |

Return a packet with execution commit and dirty diff, environment/assets/source identities, actual host/attempt locators, tests/native parity, complete run inventory, raw predictions/native reports, paired analyses, costs and failed attempts, E04, and exact remaining obligations. Transfer declared files back over SSH with byte-hash verification. Commit appropriate source/results summaries to the already authorized GitHub destination using one writer and exact readback; keep large data, weights, secrets and raw copyrighted corpora out of Git. No HF output destination has been provided.

The user-facing return must distinguish **source delivered / software passed / native qualified / executed / scientifically supported**, and report which of those actually have receipts. The next Web continuation starts from this exact returned packet, not a recollection of an earlier success message.



## Full original-plan supplement

The current engineering spec is rounds/full-plan-2026-10-08/EXPANSION_SPEC.md; COVERAGE.md and EXPERIMENT_DESIGN.md identify exact formulas and interpretation limits. Preserve the v0 controls. Reuse the exact same asset files/acquisition steps above; the extension requires no new dataset, checkpoint weights, action labels, semantic annotations or paid scorer. All software/GPU/native qualification is still pending. The complete ParlAI Teacher candidate in NATIVE_ENVIRONMENT must really install and export all60 task/split files before full teacher parity; metrics-only replay never substitutes.

After the main environment exists, run the full suite and these focused tests under Local's execution owner, recording skips and actual stdout/stderr/exit status. CUDA skips cannot certify device behavior:

```bash
conda run -n lwm python -m pytest
conda run -n lwm python -m pytest tests/test_episodic_semantics.py tests/test_expansion_semantics.py tests/test_resume_semantics.py
```

Accept event FIFO/replay/conflicts, stable identified chunk transactions spanning EOS, partial-prefix origins/sources, generated-position exclusion, actual neural retrieval consumption/gradient, teacher-prefix future isolation, plan snapshot source/context binding, realization with no reader/writer/retrieval, legal norm/current-gradient path, writer independence from K, eligible state-loss normalization and full expanded trainer interruption equality. These CPU fixtures are finite software checks. Verify same-provenance CPU/CUDA FP32 parity and actual FP16 finite-profile behavior independently; the real-arithmetic contraction bound is not a floating-point error certificate. Rejection of malformed/downgraded/mismatched state is expected behavior, not a recovery reason to discard evidence.

Finite actual-native-corpus profile, in a fresh directory:

```bash
conda run -n lwm python -m lwm.train --config configs/full_loop4_100m.json --data data/fineweb-100m/train --validation data/fineweb-100m/valid --output runs/profile-full-loop4 --max-updates 10
conda run -n lwm python scripts/summarize_run.py runs/profile-full-loop4 --project-tokens 100000000
```

Record GPU model/count/driver, total and active parameters, allocated/reserved peaks, CPU RSS, all event/receipt bytes, per-invocation cumulative historical_access snapshots, separate validation audit and total elapsed wall. Do not sum cumulative snapshots. Audit CPU timing is the indexing/ranking subinterval; CPU transfers, admission SHA256, serialization, fresh embeddings and GPU attention are included in total wall, not that narrow subinterval. Profile the different envelopes needed for admission (Transformer loop, full retrieval, no-plan, K=1) before freezing matrix cost. Capacity/read-budget increases change workload. No fit or completion-time claim is made for 2080Ti.

Author a complete command DAG, with GPU disabled for official replays and comparisons. It does not launch anything:

```bash
conda run -n lwm python scripts/run_matrix.py --design configs/full_plan_experiments.json --data-root data --output-root runs/full-plan --budget 100m
```

The 13-arm/two-seed design gives200 dependency cards:52 training cards,52 full inference cards,52 native replay cards and44 comparison cards. Each tier is26 pretraining runs:2.6B targets for100M or26B for1B, plus26M adaptation targets, extra input/retrieval exposure and actual profile/failure costs. Run one admitted GPU job at a time with the existing owner, retain incomplete/failed dependency status, and continue independent admitted work. A tier1B manifest uses a distinct output root such as runs/full-plan-1b, its separately prepared corpus and a separately admitted total budget. No implicit second-tier launch.

Every completed arm/seed must have full native20000/5153 predictions, native replay and declared comparison obligations. run_matrix includes source-root/interpreter replay commands and right-minus-left comparisons; resolve each actual argv and dependency through the existing Local harness. Source/config/output paths in a manifest are not launch receipts. Comparisons use conditional-on-checkpoint paired episode/passage bootstrap; report both seeds and every predeclared contrast, including failures, not only a best seed or selected tasks.

Explicit state/plan interface after an accepted actual full checkpoint exists (replace path with the exact selected completed or finite-profile checkpoint and record that scope):

```bash
conda run -n lwm python -m lwm.generation --checkpoint runs/full-plan/full_loop4-100m-seed17/pretrain/last.pt --tokenizer data/tokenizer --prompt 'The story begins' --observation-id user-chunk-001 --max-new-tokens 0 --plan-out runs/full-plan/plan.pt --state-out runs/full-plan/stream.pt
conda run -n lwm python -m lwm.realization --checkpoint runs/full-plan/full_loop4-100m-seed17/pretrain/last.pt --tokenizer data/tokenizer --plan runs/full-plan/plan.pt --output results/full-plan-realization --device cuda
conda run -n lwm python -m lwm.generation --checkpoint runs/full-plan/full_loop4-100m-seed17/pretrain/last.pt --tokenizer data/tokenizer --state-in runs/full-plan/stream.pt --prompt 'The story begins' --observation-id user-chunk-001 --max-new-tokens 64 --state-out runs/full-plan/continued.pt
```

The repeated identified prompt is a verified no-op before generation; changing payload under that ID rejects. Anonymous repeated text is new input. Public receipts survive EOS for stream lifetime; document segment events/receipts reset with compressed state. A prompt source locator is not truth authentication. Plans retain a complete causal per-token plan sequence and realize one next-symbol distribution without replanning, not a complete sentence from an identified semantic code. Generation replans for each emitted token and advances reasoning/expression separately. Reader-only calls do not commit observations. New-v2 saved streams bind source/config/checkpoint/tokenizer and sampling policy/device/RNG; missing-format legacy states are only admitted by disabled-extension v0. Changes to implementation require explicit migration/new branch, not silent resume. Generated tokens retain their source in the continuation state and are filtered out of raw retrieval by default; the compressed continuation still summarizes generated text. Preserve the original functional state to retain external-only history.

For training resume use the manifest's exact effective config, corpus, output and current last.pt. History payload includes exact events/receipt ledger and segment clock, alongside slots/cursor/RNG/optimizer/scaler. Loss beta and predictive head must match; auxiliary_target_observations counts repeated existing eligible labels separately from seen/optimized target budgets. This does not charge or expose future labels to the reader. No cross-document state-loss pair is created. Local reports software/native/GPU qualification separately from completed target budget and scientific validity, retaining all actual failure evidence and costs.

## Full original-plan supplement

The current ordered entry is rounds/full-plan-2026-10-08/WEB_HANDOFF.md, with its COVERAGE/EXPANSION_SPEC/EXPERIMENT_DESIGN. All original input/scorer acquisition commands above remain mandatory. No extra dataset or weights are required. The expanded source introduces episodic.py and realization.py and wires them into existing training/validation/generation/evaluation/checkpoint paths.

Run the entire software suite at the exact accepted revision. Focused debug files are test_episodic_semantics.py, test_expansion_semantics.py, test_resume_semantics.py and test_scoring_semantics.py; fixtures do not replace native benchmarks. New acceptance includes future-isolated retrieval, replay after eviction/EOS, partial-prefix provenance restore, plan no-reader realization, current-matrix contraction, eligible aux denominator/validation and real-trainer resumed state parity. CPU/CUDA paths are separately qualified; skips cannot pass the GPU route.

Use the full handoff's exact profile/manifest/plan/resume commands. The full matrix --design configs/full_plan_experiments.json yields204 dependent cards:13 arms x2 seeds x6 stage/replay cards,11 paired contrasts x2 seeds x2 tasks, plus4 factorial interaction cards. No card runs automatically. Budget2.6B/26B pretraining targets plus26M adaptation targets and all other costs. Old40-card/five-arm descriptions above apply only to legacy v0 stages; current v0 generator also includes native-replay and interaction cards.

Collect per-run events/status/last.pt identities, evaluation manifests/predictions, native-replay.json, paired-bootstrap.json and factorial-bootstrap.json. Respect log scopes: training access counters are invocation cumulative, selection trace is last-call, validation access and head CE/pair counts are separate, process RSS is high-water. parameters_with_gradient_tensor means p.grad exists before zero_grad; not necessarily nonzero. Main NLL remains independent of beta. Total elapsed cost includes transfer/hash/admission/attention overhead; fine-grained kernel timing is not supplied.

Three clocks distinguish observed evidence, internal reader steps and generated output; next_logits/likelihood scoring are pure reads/temporary branches, so semantic counters are not all-call profiling. Use model.audit and real harness wall/resource receipts for cost. The raw event bank is bounded, but event/chunk receipts grow and must be budgeted. Default retrieval excludes generated raw positions; provenance is declared input origin, not factual authentication.

Contractive analysis is an exact-real-arithmetic state bound with fixed forcing, not a floating-point output certificate. Semantic plan is a per-token continuous bottleneck. No sentence/action/ELBO/adaptive TODO is assigned to Local; those broader ideals remain separate unresolved research. Supported runtime profile is FP32 models/FP16 autocast, not BF16 plan persistence.
