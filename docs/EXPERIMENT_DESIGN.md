# Baseline qualification and conditional research design

Status: generated, unexecuted. This is a complete source/configuration specification
for the delivered existing-model base. It is not a completed 15-method G01 matrix
or a frozen candidate Gate A. The unclosed method obligations are explicit in
`CANDIDATE_AUDIT.md` and `CANDIDATE_COVERAGE.csv`.

## Compute and data interpretation

The user states RTX 2080 Ti. Plan one device, nominal 11 GB; exact driver, UUID,
available VRAM and throughput must come from the user's GPU host. Interpret 0.1B
and 1B as token budgets, not parameter counts. Main training uses FP32 master
weights, FP16 autocast/GradScaler, SDPA's available backend and gradient
checkpointing. No FlashAttention-2/BF16 dependency. Native Conda, no Docker.

| Configuration | Initialization | Tokens | Effective targets/update | Intended role |
|---|---|---:|---:|---|
| train_31m_100m | Scratch Llama, about 31.5M parameters | 100,000,000 | 16,384 nominal | First language-training baseline |
| train_31m_1b | Independent scratch run | 1,000,000,000 | 16,384 | Optional data-scale comparison |
| train_135m_100m | Scratch SmolLM2-sized Llama config | 100,000,000 | 16,384 | Capacity comparison after resource qualification |
| continue_smollm2_100m | Released pretrained SmolLM2-135M | 100,000,000 additional | 16,384 | Practical continued-training reference, not a compute-matched scratch control |
| Released SmolLM2-135M | Pretrained, no new training | 0 additional | n/a | Evaluator/model capability reference |

The 31M configurations use width 384, eight layers, six Q heads, two KV heads and
FFN width 1024 with tied vocabulary. Estimated parameter count is architectural,
not a measured runtime receipt; the trainer records the actual count.
The 135M config preserves the released 30-layer, width-576 configuration.

100M / 16,384 gives 6,104 optimizer updates after rounding up; 1B gives 61,036.
Exact token accounting masks the final incomplete block and weights accumulated
losses by the actual number of nonmasked targets. Groups containing a shuffled
partial block and the final incomplete group can have fewer targets than the
nominal update size. FP16 overflow retries do not
advance learned-token count. Logging separately retains attempted tokens.
Do not promise eight-hour completion. Once Local measures steady-state throughput
q, training-only time is approximately D/q; evaluate/checkpoint/preparation time
must be added. A 1B plan is roughly ten times the token work of 100M, not a free
extension. The scheduled learning-rate horizon is fixed at run creation.

FineWeb-Edu `sample-10BT` is a published input pool, not a request to download or
train all 10B tokens. The preparer streams a deterministic prefix at a full pinned
revision. Content-hash assignment sends 1% of documents to a training development
split, ensuring identical text cannot appear on both sides. The first 100M or 1B
training targets and 1M development targets are retained with EOS separators,
document identities and byte hashes. This internal development NLL is a training
diagnostic, never substituted for a released benchmark score. Benchmark overlap
with web pretraining remains unmeasured; report it rather than assert decontamination.

## Published language benchmarks

Source revisions, native task names and dataset identities are in
`configs/sources.json`. The implementation loads the pinned evaluator's actual
task configuration and changes only repository alias/revision/cache and the
explicit development split, not prompts, scoring or target extraction.

| Benchmark | Published evaluation split | Native primary quantity | Denominator | Entry |
|---|---|---|---|---|
| WikiText-2, document level | test | word perplexity; byte perplexity/bits-per-byte also retained | Native document inventory; word/byte weighting retained by scorer | `evaluation.py`, task `wikitext` |
| HellaSwag | validation | length-normalized multiple-choice accuracy | All 10,042 released validation records, verified locally | `evaluation.py`, task `hellaswag` |
| PIQA | validation | multiple-choice accuracy; normalized accuracy also retained | All 1,838 released validation records, verified locally | `evaluation.py`, task `piqa` |
| ARC-Easy | test | normalized multiple-choice accuracy | All 2,376 released test records, verified locally | `evaluation.py`, task `arc_easy` |

No `--limit` option is supplied. Evaluate zero-shot at context 512 and batch one
for all main models. Preserve full per-sample outputs, released row IDs/hashes,
native task config, labels, dataset fingerprints, counts and evaluator revision.
The source-generated adapter has not yet been qualified against official scorers.
Missing/changed denominators are an error; no skipped task becomes zero or an
omitted row. PIQA's pinned loader has external acquisition dependencies; the
native builder must complete and record their actual download checksums.
Scoring consumes a separately frozen preparation inventory. Before inference it
compares the exact task set, source/split/config, all processed sample hashes,
download identities and actual wrapper/evaluator software. Every predicted row ID
and document hash must match the frozen set. The four task inventories and their
native denominators still require initial Local qualification; a freshly observed
WikiText document count alone is not independent scorer-parity evidence.

For development, use published validation for ARC/WikiText. HellaSwag/PIQA's
labelled public split is already validation: once inspected, it is descriptive
evidence and cannot be renamed fresh confirmation. Use a separately predeclared
untouched benchmark/split for later confirmatory claims. Do not tune test outcomes.

## Existing latent-reasoning comparisons

Coconut is source-pinned to its author implementation. `assets.py` acquires the
repository and hashes code plus released ProsQA data. `coconut.py` creates CoT,
no-CoT and Coconut training configurations for ProsQA and GSM8K, preserving the
author's curriculum, data format and answer extraction. GSM8K uses the author's
augmented train/validation and released test processing, with its input revision
pinned in the upstream script. It is not silently mixed with FineWeb.

| Native task | Arms | Train/selection/held-out path | Metric/source |
|---|---|---|---|
| ProsQA | CoT, no-CoT, Coconut | `data/prosqa_train.json`, `prosqa_valid.json`, `prosqa_test.json` | Author `run.py` exact answer extraction and correct/total |
| GSM8K author protocol | CoT, no-CoT, Coconut initialized from actual CoT checkpoint | Author `gsm_icot.bash` preparation, then `gsm_train/valid/test.json` | Author `run.py` exact answer extraction and correct/total |

These baselines use GPT-2 and FP32 with `bf16=false`, one GPU, microbatch one and
gradient accumulation 128 to preserve 128 examples/update nominally. Because
the author loss averages variable-length microbatches, this is a resource-adapted
comparison, not an exact reproduction of 4x32-example gradient weighting. It is
also not token- or FLOP-matched to scratch pretraining. Report these axes separately.
The author runner's checkpoint resume does not retain optimizer/RNG state; a
restart is a documented training deviation, not exact continuation. Its data
mapping requests 32 processes; memory/CPU admission must reflect this or a reviewed
operational source patch is needed before launch. No silent monkeypatch is supplied.

Checkpoint selection uses development accuracy only; preserve epoch curves and
select the best qualifying checkpoint, ties to earliest epoch. For Coconut,
retain all checkpoints and select only fully latent final-stage checkpoints:
ProsQA epoch 36 onward, GSM8K epoch 13 onward. Earlier curriculum stages are not
interchangeable with the fixed final evaluation depth. Final test is once
per selected seed/checkpoint. Do not equate author default 25/50 epochs with an
eight-hour run or the 100M-token pretraining budget. Original native logs are the
score source; full prediction logging/parity receipts remain Local qualification
work because the author runner prints only example excerpts.

## Seeds, controls, resources and decisions

Use seed 17 for initial software/resource/baseline qualification. The proposed
replication seeds are 17, 29, 43, admitted only after per-run measured cost fits a
separately recorded finite Local budget. The configs do not launch all of them.
Resource calibration is not evidence of research benefit. Do not create 15
method runs from this list.

For any later architecture comparison, match tokenizer, data order, trained target
tokens, optimizer/tuning budget, training information and evaluation examples.
Report parameter count and measured train/inference time/peak memory. Parameter
matching alone is not compute matching; a loop needs a compute-matched control.
Mandatory controls for the central hypothesis include a shared phase-conditioned
transition, frozen-memory workspace, equal extra feed-forward depth and explicit
text/retrieval memory where relevant. They remain design obligations until
selection and contribution gates permit their implementations.

Report native task estimates and native standard errors; per-example paired
bootstrap and across-seed variability must be separately prespecified before any
candidate effect claim. Do not average perplexity and accuracy or treat training
seeds as independent benchmark items. A prospective effect threshold cannot be
set from inspected test gains. No numeric PASS/KILL threshold is invented here.

Local first restores host paths/authority, acquires inputs, runs meaningful
software/native acceptance, checks scorer parity and closes the remaining
scientific design obligations. Queue one GPU job at a time under Research
Autopilot's existing `run_harness.py`; task timeout and cumulative limits are
explicit and independent of the reporting cadence. The trainer pauses at its
23-hour per-invocation limit and checkpoints at update boundaries. An outer
hard limit must leave time for checkpointing, with lost in-flight work bounded
by the checkpoint interval. Local must reconcile attempts before resuming.
