# Expanded text-model experiment design

Status: generated_unexecuted. Read together with ../../research/EXPERIMENT_DESIGN.md for the unchanged native assets, full denominators, development/confirmation split, failure retention and statistics. This file supersedes its five-arm inventory for the expanded matrix, while preserving that inventory as v0 controls. No benchmarks were added or substituted.

## Frozen source design

`configs/full_plan_experiments.json` names 13 engineering arms and seeds 17/29. `configs/full_*_{100m,1b,babi}.json` provide actual full stage configs. Standard expanded construction: d=256, memory16x256, L=256, semantic width128, exact history4096 tokens, two retrieved events/up to512 tokens, causal query32 tokens, fixed c=0.9 and K=4, beta=0.1. These are prospective development choices, not tuned optima.

| Arms | What the comparison resolves | Information / capacity caveat |
|---|---|---|
| memory_loop1/4, reset_loop1/4, memory_untied8 | Original v0 memory/depth alternatives and 2x2 interaction | Untied parameters/adapter calls and effective gradients differ; no exact cost match |
| full_loop1 vs full_loop4 | Fixed-forcing computation at identical retained raw history, query/access policy, nominal parameters | Runtime costs and finite-depth training differ |
| full_no_episodic vs full_loop4 | Added exact history access | Changes available information, not a pure compression improvement |
| full_no_plan vs full_loop4 | Explicit lower-width Z interface | Removes the bottleneck and changes active parameters; does not identify semantic meaning |
| full_no_stateaux vs full_loop4 | Direct compressed-state supervision | Additional observation of already eligible targets; disclose pair counts |
| full_transformer4 vs full_loop4 | Transformer recurrence vs global fixed-forcing contraction | Changes communication/model class; cannot attribute gain solely to a spectral bound |
| full_recency vs full_loop4 | Lexical selection vs simpler recency at equal raw budget | Same retained capacity/read limit/provenance, actual selected positions differ |
| full_retrieval_only vs full_no_stateaux | Persistent compressed state given equal raw-history access and beta=0 | Writer still runs but discards memory; active gradient and real cost differ |
| memory_loop4 vs full_transformer4 | Full known-mechanism extension with unconstrained recurrent core | Combined feature comparison, not causal attribution to one module |

No novelty/SOTA conclusion follows from these ablations. Strongest published baselines still require qualification before a new-method claim; historical discovery remains pending. Do not populate published-baseline rows with incomparable paper scores.

## Native coverage, budget and dispatch

Every arm/seed pretrains on the same fixed FineWeb-Edu/GPT-2 tokenizer stream at 100M or 1B eligible targets, evaluates the full LAMBADA5153 with its pretraining checkpoint, separately adapts on all20 bAbI tasks for1M answer/EOS targets, and evaluates bAbI20000. Evaluator answer labels and support metadata never enter model input, retrieval queries or event admission. In supervised training, each answer token is used as its target only after prediction, then becomes legitimate teacher-forced causal history for subsequent positions; all admitted training text has observed_text provenance. Defaults exclude generated raw positions; scored likelihood targets have distinct provenance. Empty-query fallback and omitted read positions are recorded.

13x2 runs cost **2.6B / 26B pretraining target observations**, plus **26M adaptation targets** per matrix, additional adaptation context, validation, inference, official replay, profiles and failures. The inherited five-arm subset costs1B/10B. Neither is an8h throughput promise. One user-stated2080Ti is the execution assumption; real VRAM/time/native environment capacity is pending. Full source does not launch anything.

Generate all26 arm/seed stage inventories with six cards each (pretrain, SFT, two evals and two official replays),44 paired-comparison cards and4 interaction cards: **204 dependency cards**. Invocation:

```bash
conda run -n lwm python scripts/run_matrix.py --design configs/full_plan_experiments.json --data-root data --output-root runs/full-plan --budget 100m
```

Use `--budget 1b` with its separately acquired corpus and separately admitted cumulative resources; do not auto-start it. A native comparison depends on official replay for all participating runs. Matrix cards are inner commands for Local's actual SSH/native harness, not a scheduler or verified dispatch packet.

## Statistics and interpretation

Pair exact native IDs, seed and inputs. `scoring compare` retains right-minus-left passage/bootstrap or episode-within-task bootstrap. `scoring interaction` implements `(M4-R4)-(M1-R1)` using one shared native resample across all four arms, preserving question counts within episodes and native task macro weighting. Do not subtract independently bootstrapped CIs. Report both seeds separately; two training repeats do not certify seed robustness.

The paired and interaction95% intervals are **exploratory, conditional on checkpoints**, with no multiplicity correction and no training-seed uncertainty. No simultaneous11-contrast,20-task or4-endpoint significance statement is authorized. Freeze any confirmatory family/effect criterion/repeats from real development evidence before confirmation; do not select configurations or omit contrasts using test outcomes. The first complete matrix supplies engineering evidence, not a prematurely declared scientific PASS.

## Costs and outcomes

Read train events/start/update/validation/failure, status/counters, evaluation manifest/predictions, native-replay.json and paired/factorial-bootstrap.json. `summarize_run` reports observed profile rates and last invocation's cumulative access snapshot, with future cost exclusions. New logs retain held-out head CE sum/pairs, main-only NLL, composite objective and parameters with present gradient tensors. This last field is not nonzero-gradient count or effective capacity.

Retrieved values are freshly embedded; selection/index work, CPU-GPU query synchronization, raw reads, storage/receipt serialization, parameter/activation device costs and all recomputation belong in total cost. `retrieval_cpu_seconds` covers CPU selector/tensor-preparation scope, not total transfer/attention time; total eval/training wall and GPU peaks cover the executed path. Fine-grained CUDA kernel timing is not supplied. `last_retrieval_trace` is last-call only; aggregate counts cover all calls. Peak RSS includes Python objects but is process high-water memory, not a per-store heap measurement.

Source acceptance requires actual software/native/identity checks before a science run. Implementation/asset failures remain invalid evidence; failures/zero or adverse benefits remain visible. Insufficient cumulative resources leave named pending comparisons; they do not justify shrinking native denominators or claiming a partial matrix complete.
