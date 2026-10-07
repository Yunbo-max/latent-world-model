# Local Codex: start here

Read this file and `rounds/2026-10-07/WEB_HANDOFF.md` at the pinned delivery SHA.
The Web delivery contains generated source, not passing tests or measured GPU
performance. The architecture candidate stage remains blocked as documented in
`docs/CANDIDATE_AUDIT.md`; the existing-model base is ready for Local acceptance
work once host access and finite execution authority are restored.

## Host and execution ownership

The user's computer runs Local Codex and owns the authenticated delivery checkout.
The GPU host runs Python/Conda, the existing Research Autopilot runtime, workloads
and logs. Obtain the SSH alias and absolute host paths from the user's existing
local configuration; they are not supplied in this conversation. Do not guess a
host or request credentials in chat. Hardware is user-stated RTX 2080 Ti; one
device is the planning assumption. Read actual UUID, free VRAM, driver and RAM.

Except for the explicitly marked source-capture step, command cards below are **inner foreground commands for admitted tasks on
that host**, not permission to run them directly from a laptop or outside the
shared host harness. Use the attempt's staged project root as cwd, the real Conda
interpreter, and preserve the harness-assigned CUDA_VISIBLE_DEVICES. CPU-only
acquisition gets zero GPUs; model training/evaluation gets one exclusive GPU.
Use native Conda, no container runtime.

The current Web request authorizes code delivery, not starting a GPU queue from
this chat. Local must restore its actual finite execution scope and cumulative
budget. Report cadence is not a training timeout. Unknown timing/VRAM stays
unknown until measured; do not auto-run the optional 1B queue or all 15 ideas.

## Ordered command cards

1. Fetch the delivered commit into a clean compatible checkout; preserve live
   attempts and user edits. Read AGENTS, this guide and the round handoff.
2. Use the installed runtime's read-only `run_harness.py --inspect-host` command
   on the GPU host. Record SSH target, project/runtime/interpreter paths, GPU UUID,
   driver, CUDA, RAM, disk and actual allowed runtime in `runs/host/`.
3. Admit environment preparation and acquisition using source-pinned code/config
   refs. Preserve the resolved package/environment manifest.
4. Admit engineering tests and native resume/FP16 acceptance separately. Inspect
   failures, qualify the memory profile and retain actual logs. No scientific
   quality inference follows from these tests.
5. Prepare native benchmark inputs and official scorer parity. Bind actual
   sample manifests, labels, full native data/scorer inputs and software receipts
   in the runtime's existing scientific protocol before any baseline scoring run.
6. Admit the finite baseline train/eval work. Novel candidates remain blocked
   until math/selection/value/collision and complete G01 prerequisites close.
7. Collect logs/identities and return a source-linked E04 packet; preserve pending
   work and failed attempts. Do not claim a 15-method experiment completed.

## Native environment

Inspect and reuse a compatible environment first. If one must be created, the
reviewed command cards are:

```bash
conda create -n latent-world-model python=3.11 pip -y
conda run --no-capture-output -n latent-world-model python -m pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cu121
conda run --no-capture-output -n latent-world-model python -m pip install -r requirements.txt
conda run --no-capture-output -n latent-world-model python -m pip install --no-deps -e .
conda run --no-capture-output -n latent-world-model python -m pip check
```

`requirements.txt` is a requested version set, not a claim about an installed
environment. Capture `python -m pip freeze`, `conda list --explicit`, Python version,
`nvidia-smi` and torch/CUDA version in the host packet. PyTorch 2.5.1 cu121 is a
published wheel choice; the actual host driver must support it. Avoid optional
torchvision/tensorflow/vLLM/FlashAttention installs.

The examples below use `python` to mean that absolute admitted Conda interpreter.
Use `conda run --no-capture-output -n latent-world-model` if needed by the host.

## Preserve source identity across harness staging

On the clean, delivered checkout, before submitting tasks to the existing host
harness, capture tracked file hashes and the actual Git commit:

```bash
python scripts/capture_source.py --output runs/source-identity.json
```

This is controller-side read-only source inventory, not a GPU workload. Choose a
new receipt path for a later source revision. Stage all captured files into the
attempt workspace, preserving relative paths, plus this receipt and all declared
input artifacts. Set `LWM_SOURCE_IDENTITY` to the receipt's **absolute staged
path** in that task's environment. The wrapper verifies current bytes against it;
it never assumes the staged workspace has `.git`. Use `scripts/run.py` below so
imports resolve to the staged `src/` even when another checkout is editable-installed.

The commands are reviewed entry cards, not fabricated launch-ready harness plans:
Local must bind real source/input paths, admitted budgets and prepared native
contracts in the installed harness schema. Preparation and scoring use the same
source bundle and resolved environment. Environment receipts hash actual critical
package files, including Torch binaries; this startup I/O is additional to training.

## Download datasets and models

All input identities are in `configs/sources.json`. Source hashes in acquisition
receipts describe bytes actually downloaded; they are not fabricated upstream
checksums. Downloads are Local-only and must be admitted, bounded tasks.

**Main tokenizer/config/model reference.** Both scratch pretraining and the
pretrained reference use the pinned SmolLM2 tokenizer. Acquire the complete
small model once so the same directory can serve the pretrained reference:

```bash
python scripts/run.py latent_world_model.assets smollm2 --directory assets
python scripts/run.py latent_world_model.assets verify --directory assets/smollm2
```

This downloads the fixed revision's config, full safetensors weight file,
generation config, tokenizer JSON/config/special tokens, merges and vocabulary.
The repository reports roughly 272 MB for this model snapshot. The receipt is
`assets/smollm2/acquisition.json`. Existing matching caches are reused; changed
revisions/files fail rather than silently replacing an in-use asset.

**FineWeb-Edu training corpus.** No separate full 10B-token download is required.
The preparer streams the published pinned `sample-10BT` train split, records
document source IDs and hashes, writes the exact retained targets, and fails if
the source exhausts early:

```bash
python scripts/run.py latent_world_model.prepare --assets assets --tokens 100000000 --dev-tokens 1000000 --output data/fineweb-100m
```

Expected files: `train.bin`, `dev.bin`, `documents.jsonl`, `manifest.json`. Uint32
token files occupy about 404 MB total for this profile; raw network/cache and
document-index costs are additional and unmeasured. Internal development NLL is
not a published benchmark score. Repeated identical content has the same split.
Interrupted preparation leaves a uniquely named `.partial-*` directory for
inspection; restarting preparation rereads the stream through its cache and
does not falsely resume a token cursor. A complete matching corpus is reused.

Only when the separately admitted data-scale comparison is wanted:

```bash
python scripts/run.py latent_world_model.prepare --assets assets --tokens 1000000000 --dev-tokens 1000000 --output data/fineweb-1b
```

The 1B train token file is about 4 GB plus development/index/cache. It is not
downloaded or trained by selecting the 100M configuration.

**Four native language benchmark loaders/scorers.** The evaluator is already
installed from full Git SHA in requirements. The following invokes its native
task builders, including any external PIQA builder downloads, and retains the
actual split fingerprints, download checksums and full sample manifests:

```bash
python scripts/run.py latent_world_model.evaluation prepare --cache hf-cache --split-mode published --output runs/native-inputs/published
python scripts/run.py latent_world_model.evaluation prepare --cache hf-cache --split-mode development --output runs/native-inputs/development
```

The required inventories are WikiText-2 document-level test/validation,
HellaSwag validation, PIQA validation and ARC-Easy test/validation. Their exact
HF commits are frozen in sources.json. All native rows and labels are retained
through their loaders. In particular, downloading the 15 KB PIQA repository
alone is **not** downloading its examples: its external builder must succeed.
Inspect and preserve native checksums for those inputs before evaluation.
No dataset is replaced if access or download fails.
Freeze `dataset-inventory.json` and all four `*-samples.json` files after native
qualification, and bind their hashes in the admitted scoring plan. Scoring requires
`--native-inventory` and checks the same task set, split, processed sample hashes,
denominators, source and software before inference. HellaSwag/PIQA/ARC counts also
have released-count checks. WikiText document aggregation must be qualified against
the pinned native loader; do not substitute raw line counts for document counts.

**Coconut latent-reasoning baseline.** Acquire the pinned author code and GPT-2:

```bash
python scripts/run.py latent_world_model.assets coconut --directory vendor/coconut
python scripts/run.py latent_world_model.assets gpt2 --directory assets
python scripts/run.py latent_world_model.assets verify --directory assets/gpt2
```

GPT-2 acquisition includes one complete safetensors weight file and its tokenizer/
config files, not ONNX/TensorFlow duplicates. The full author checkout includes
the released ProsQA train/valid/test JSON files; source and data hashes are
recorded in `vendor/coconut-acquisition.json`. Disk size is recorded locally.

For GSM8K, run the inspected author's preparation script **from vendor/coconut**:

```bash
bash preprocessing/gsm_icot.bash
```

It fetches the author-linked train/valid/test text at commit
`e06a32ee5e4cd117171daeb4755d2a97ece62761`, applies their parser and writes
`data/gsm_train.json`, `gsm_valid.json`, `gsm_test.json`. Retain original source
identities, actual output hashes/counts and preparation logs; this is the author's
augmented training protocol, not a substitute dataset with the same name.
All source URLs, access and available disk must succeed before generating
dependent configs. There are no gated model licenses assumed here and no secrets
are written into commands.

## Acceptance and resource qualification

Engineering contract command:

```bash
python scripts/run.py pytest -m 'not native' -q
```

These array fixtures test shifting, coverage, integrity, partial groups, schedule
boundaries and rejected configurations; they are not research examples.

Native resume acceptance uses the actual prepared training corpus and pinned
tokenizer/config. Set LWM_NATIVE_CORPUS and LWM_ASSETS to their **absolute remote
paths** in the admitted task environment; then:

```bash
python scripts/run.py pytest -m native -q --basetemp runs/acceptance/pytest-temp
```

It compares four FP32 baseline updates with two updates plus resume plus two
updates, checking parameters, optimizer/scaler/RNG, data cursor, step count and
trained tokens. FP16 overflow/retry qualification remains separately pending.
Use a fresh basetemp per
attempt. It is a restart check on genuine training data, not a benchmark effect.
For deterministic CUDA acceptance, set CUBLAS_WORKSPACE_CONFIG=:4096:8 before
Python starts and preserve its value in the environment receipt.

Next qualify the *actual* FP16 31M configuration using a bounded first segment:

```bash
python scripts/run.py latent_world_model.training --config configs/train_31m_100m.json --assets assets --output runs/llama-31m-100m-s17 --max-updates 50
```

This trains real first-run updates and produces a resumable checkpoint; its cost
counts toward that baseline. It is not a completed 100M comparison. Inspect
steady-state time, actual GPU memory, FP16 scale/overflows, finite loss/gradients,
source/config identity and native restart evidence. Baseline quality must be
evaluated separately. Do not halve settings silently on OOM.

## Training, checkpointing and native evaluation

After scoped Local acceptance and execution admission, continue the same run:

```bash
python scripts/run.py latent_world_model.training --config configs/train_31m_100m.json --assets assets --output runs/llama-31m-100m-s17 --resume
```

The checkpoint stores FP32 model/optimizer/scaler, RNG, exact block position,
learned/attempted token counts and source/input identities. Existing output
without --resume is rejected. Source/config/data changes invalidate a resume.
The program writes immutable `checkpoint-<generation>.pt` files, then atomically
publishes the fsynced `checkpoint.json` pointer. The current and previous committed
generations are retained; an interrupted unpublished generation cannot replace
the current pointer. Logs carry invocation and committed-generation identities,
so replay after rollback is distinguishable. Resolve the pointer rather than
assuming a fixed checkpoint filename. Copy an explicitly selected
milestone checkpoint if a later protocol needs it. Checkpoint interval is 250
updates; power loss may replay the work since the last committed checkpoint.
At the exact token budget it exports `runs/llama-31m-100m-s17/model/` in ordinary
HF safetensors format. A paused run is not training-complete. Resume also checks
the actual resolved package versions and critical installed bytes; changing the
environment requires a reviewed new run, not a silent continuation.

Native full benchmark commands, each under its own admitted scientific task:

```bash
python scripts/run.py latent_world_model.evaluation run --native-inventory runs/native-inputs/published/dataset-inventory.json --model assets/smollm2 --cache hf-cache --output runs/eval/reference-smollm2-s17
python scripts/run.py latent_world_model.evaluation run --native-inventory runs/native-inputs/published/dataset-inventory.json --model runs/llama-31m-100m-s17/model --cache hf-cache --output runs/eval/llama-31m-100m-s17
```

The defaults are full published splits, zero-shot, 512 context, batch one and
seed 17. No quick subset substitutes for these four obligations. Outputs include
results.json, per-task sample/prediction files, dataset-inventory.json and
execution.json. Native harness metrics are not automatically an official-scorer
parity receipt or a scientific PASS; close those checks and E04 on the real host.

Optional configurations are `configs/train_31m_1b.json`,
`configs/train_135m_100m.json` and `configs/continue_smollm2_100m.json`.
Each needs a fresh output and its own source/cost qualification. Never resume a
100M cosine-schedule run under the 1B file, compare pretrained and scratch as
equal-compute models, or launch all optional runs merely because files exist.

## Coconut author-runner comparison

Generate complete native data-bound configs after acquisition:

```bash
python scripts/run.py latent_world_model.coconut configs --dataset prosqa --repository vendor/coconut --assets assets --output runs/coconut/prosqa-s17
python scripts/run.py latent_world_model.coconut configs --dataset gsm8k --repository vendor/coconut --assets assets --output runs/coconut/gsm8k-s17
```

`launch-cards.json` contains absolute inspected argv/config/data references.
Admit its foreground author runner through the existing harness, one GPU. It
requires `python -m torch.distributed.run --standalone --nnodes=1 --nproc_per_node=1`
even on one GPU. Set WANDB_MODE=disabled and TOKENIZERS_PARALLELISM=false. No
external W&B account or API key is needed. Reserve 32 preprocessing CPU workers
unless a separately reviewed operational patch changes the author source.

GSM Coconut requires the actual development-selected CoT checkpoint; its unbound
config is explicitly not launch-ready. Use the `bind` command with the actual
checkpoint file path to produce a new bound config. Example syntax, with
ACTUAL_CHECKPOINT replaced by the returned path (never an invented checkpoint):

```bash
python scripts/run.py latent_world_model.coconut bind --config runs/coconut/gsm8k-s17/coconut-train.yaml --checkpoint ACTUAL_CHECKPOINT --output runs/coconut/gsm8k-s17/coconut-bound.yaml
```

The same command with `--evaluation --repository vendor/coconut` produces the
held-out eval config. For Coconut it rejects early curriculum checkpoints:
ProsQA epoch 36 onward / GSM epoch 13 onward are eligible for fully latent eval.
Select best development accuracy within that final phase, ties earliest epoch.
CoT/no-CoT use their own development-selected checkpoints. Preserve all epoch
curves. Never choose checkpoints from test scores.

The resource-adapted author baseline uses FP32, one-example microbatches and
128-step accumulation; its variable-length loss weighting differs from the
author's four-GPU run. Its resume is weights/epoch only, not optimizer/RNG-exact.
It is not constrained by the main pretraining token budget and may span multiple
admitted windows. No claim of exact paper-score reproduction or 8-hour completion
is made. Native per-sample logging/scorer parity must be qualified before using
its outcome to pass a research gate.

## Debug and acceptance routing

| Observation | Inspect | Scoped action and recheck |
|---|---|---|
| CUDA/import/version error | Host receipt, resolved environment, requirements, full stderr | Repair the identified native environment; pip check and affected acceptance. No driver upgrade/container shortcut. |
| Model/data hash, missing split or HTML/LFS pointer | acquisition.json, corpus manifest, source revision, native builder log | Reacquire the same required asset through supported cache recovery; preserve the failed attempt. No substituted model/dataset. |
| OOM | hardware.json, peak allocated/reserved, live GPU contention, effective microbatch/context | Reconcile foreign use; review a result-affecting config change as a new run. Preserve global targets and full comparison requirements. |
| FP16 overflow | train.jsonl overflow records and scaler; FP32 native acceptance | Repeated overflows stop after eight consecutive failed groups. Investigate inputs/precision/LR under bounded development; do not count skipped updates. |
| Off-by-one or restart drift | data.py target shift, checkpoint cursor/RNG, native resume test | Repair the demonstrated cause, rerun the same semantic acceptance and invalidate affected results. |
| Native benchmark zero score/count mismatch | predictions, task config, retained native sample IDs and labels | Check tokenizer and evaluator semantics; replay qualified native scorer. Do not invent a replacement metric or delete failures. |
| Coconut early-stage checkpoint | bound config and author epoch/stage mapping | Select an actually retained eligible final-stage checkpoint using development scores; never relabel an early checkpoint. |
| Lost SSH/launch acknowledgment | Existing harness batch/attempt ID, PID/boot/start tuple, checkpoint/status | Reconcile the same task identity before resume. No duplicate raw training launch or cleared lock. |
| Time boundary | Actual elapsed time, outer task budget, checkpoint receipt | Checkpoint and retain partial status; carry forward only within remaining scoped authority. No budget reset or completed-comparison claim. |

## Return and next Web review

Collect small metadata and hashes inside an admitted CPU collection task:

```bash
python scripts/run.py latent_world_model.collect --runs runs --output runs/return/round-01
```

Use a new output for each return packet. The manifest retains raw prediction/sample
file hashes/host paths while leaving their potentially large contents on the host;
native_metrics.csv copies only native metric values. Retrieve packet/logs over the
existing SSH connection, verify hashes, retain actual source SHA/dirty-state,
failed attempts, environment, native scoring/E04 scope and unfinished comparisons.
Deliver small authorized result records back to this GitHub project using one
writer and read back the result commit. No HF output repo is confirmed: do not
upload weights or benchmark contents to an invented destination. Return the exact
GitHub commit and actual host artifact locators for the next Web review.
