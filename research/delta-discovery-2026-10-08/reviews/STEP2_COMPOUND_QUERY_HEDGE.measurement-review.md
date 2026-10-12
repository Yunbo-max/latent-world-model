# Measurement review — compound query hedge v1

Binding: `main@fd320bc4a51c9e41b4c8ceab488e8be28d3b1f2e`; assignment `compound-query-hedge-measurement-001`; reviewer identity `/root/compound_query_hedge_measurement`; workflow `rsi-simple@0.3.0-simple.9`. This review was produced read-only; no experiment or benchmark construction occurred.

## Verdict

No already pinned native asset measures the required causal object. A valid object must jointly expose a query index/metric withheld from the stage-1 filtration, a byte-identical hashed immutable snapshot, a later native reveal, append-only and fresh-recode arms on the same lawful history, equal final payload including metadata, full archive/read/write/compute accounting, and one official scorer.

## Native interface mapping

| Asset | Useful native interface | Decisive missing field |
|---|---|---|
| WritePolicyBench | `WritePolicy.select(step, store)`; WRITE/MERGE/EXPIRE/SKIP; native byte model | no metric reveal, immutable layered code, raw-archive or full rewrite/compute ledger |
| AToKE-ME | historical/current-relative and explicit questions; native temporal scores | future prompts coexist in one record; masking is non-native; no byte snapshot or matched recode |
| LongMemEval-V2 | `Memory.insert` and `query`; accuracy and latency | backend may mutate/rebuild; no frozen bytes, reveal schedule or equal-payload arms |
| EvoMemBench | evolving in-/cross-episode suites | heterogeneous scorers; no common byte state or causal reveal |
| MemoryBench | future/old-task retention curves | prescribed update/replay, not the required query-reveal treatment |
| WikiBigEdit | temporal edit, retention/locality/generalization outcomes | prescribed editing; no immutable prefix or matched progressive/fresh resources |
| Open Bandit Dataset | action, reward, propensity and context | no memory snapshot, query metric, retention or reconstruction object |

WritePolicyBench is closest on actions/bytes; LongMemEval-V2 on insert/query/latency; AToKE-ME on future-query records. Combining them would splice different data-generating processes and scorers, thereby inventing a benchmark.

## Missing released unit

A sufficient native record would contain

\[
(H_1,W_1,Z_1^{\rm hash},B_1,\tau_{\rm freeze},
W_2,\tau_{\rm reveal},A_2,\widehat Y_2,Y_2^*)
\]

with `Z_1=f(H_1,W_1)` serialized before `W_2` enters the lawful information set. Progressive decoding may use only `Z_1` plus `A_2`; fresh recoding receives the same lawful history and final payload; both use the same official scorer and sample IDs.

The minimum resource vector is `(D1,D2,persistent bits,written bits,archive bits,raw reads,encode/decode cost)`, with query descriptors, codebooks, basis/Gram data, framing, checksums, adaptive parameters, write amplification, latency and scratch memory separately visible.

## Decision

Keep the object as theorem/control, candidate delta zero and empirical effect unknown. No native experiment should be dispatched. Reopen measurement only if a primary released asset supplies the prefix-causal snapshot/reveal contract, or a benchmark officially adds it with native samples, budget and scorer.
