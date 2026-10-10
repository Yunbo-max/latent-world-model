# R12 source and collision audit — subspace-syndrome protected readouts

Snapshot: 2026-10-10. Scope: full scientific/formula reading where accessible, plus actual public interface inspection for the Delta implementation family. This is bounded collision evidence, not an exhaustive novelty claim.

## Frozen atomic claim

For numerical edits restricted to a declared left subspace, a fixed linear syndrome determines a declared protected-query functional iff the target annihilates the syndrome nullspace on that subspace. The remaining claims are conditioning and same-budget consequences. R12 does **not** claim semantic revision identification, sparse recovery, arbitrary-query norm sketching, or a new Delta recurrence.

## Primary neighbors read

1. **Nelson & Nguyen, “Lower bounds for oblivious subspace embeddings,” arXiv:1308.3280v1 (2013).** Definition, §1 Contribution I, §2 Corollary 5 and Theorem 6 read: for `ε,δ∈(0,1/3)`, an oblivious embedding of every vector in a `d`-dimensional subspace has the ambient-capped lower bound `m=Ω(min{n,(d+log(1/δ))/ε²})`, with additional sparsity tradeoffs. This is a stronger randomized near-isometry contract than R12's fixed-functional exact factorization, but it blocks any suggestion that a tiny oblivious checksum preserves arbitrary unknown subspaces for free. It is not asymptotically larger in every regime. No author code interface is advertised on the paper page; none is used.

2. **Li, Wang & Woodruff, “Tight Bounds for the Subspace Sketch Problem with Applications,” arXiv:1904.05543v3 (2019).** Definition 1.1 and the full HTML statement were read. For an `n×d` matrix with `O(log(nd))`-bit entries, the randomized data structure answers each norm query with `(1±ε)` accuracy; when `p` is not a positive even integer and `d=Ω(log(1/ε))`, the paper proves `\widetilde Ω(ε^{-2}d)` bits, while positive even `p` has different structure. This is an adjacent rhetoric guard, not a functional collision with exact fixed-linear-functional recovery. No released author implementation is required for the theoretical bound and none is claimed here.

3. **Candès, Romberg & Tao, “Stable Signal Recovery from Incomplete and Inaccurate Measurements,” arXiv:math/0503066v2 (2005).** Theorems 1–2 and proof geometry read in the HTML full text: stable recovery from noisy underdetermined measurements requires the paper's uniform-uncertainty/restricted-isometry-style hypotheses plus sparsity or approximation-tail structure, with error controlled by noise and approximation tail. R12's fixed-subspace pseudoinverse bound is the elementary linear-subspace case, not a new compressed-sensing decoder. No code claim is used.

4. **Parrini et al., “Neural in-memory checksums,” Phil. Trans. R. Soc. A 383:20230399 (2025), DOI 10.1098/rsta.2023.0399.** Published abstract and metadata only (D1) were read. Its checksums detect/correct hardware-memory/computation faults in in-memory inference. **Parrini et al., “Error Detection and Correction Codes for Safe In-Memory Computations,” arXiv:2404.09818 / ETS 2024, is a related precursor with a different title and author list, not the frozen journal article's arXiv version.** These are terminology/fault-model neighbors, not formula-level collisions and not support for semantic revision.

5. **Yang et al., “Parallelizing Linear Transformers with the Delta Rule over Sequence Length,” arXiv:2406.06484 (NeurIPS 2024), and Flash Linear Attention commit `a7880060012c862d58575ee23f613cafcd728d03` (inspected 2026-10-10).** The paper's recurrent Delta update is an ordered rank-one erase/write map. At the pinned code commit, `fla/layers/delta_net.py` imports and dispatches `chunk_delta_rule` / `fused_recurrent_delta_rule`; `fla/ops/delta_rule/__init__.py` exports recurrent/chunk kernels. The inspected interfaces expose ordinary query/key/value/gate and state paths, not an `H,Y,R` syndrome/decoder interface. This statement is scoped to the pin because the repository is fast-moving. R12's rank-one syndrome update follows algebraically from the recurrence; it is not an executed result.

## Search families and result

Queries covered: “linear sketch subspace embedding lower bounds exact recovery,” “subspace sketch query lower bound,” “stable signal recovery incomplete noisy measurements,” “neural memory checksum error correction,” and “DeltaNet official implementation delta rule.” Backward/forward citation saturation was not attempted in this bounded repair. Exact theorem priority therefore remains `INCONCLUSIVE_EXPAND_SEARCH`; candidate admission is nevertheless blocked by the elementary factorization and same-width direct-statistic control.

## Functional comparison

| Work family | Object | Required structure | What it covers | Residual for R12 |
|---|---|---|---|---|
| OSE/subspace sketches | preserve norms for all vectors in a subspace | random embedding, dimension/error probability | sketch dimension and sparsity lower bounds | R12 asks one fixed linear functional, a weaker elementary quotient condition |
| Compressed sensing | recover sparse/compressible signals from noisy measurements | sparsity/RIP or related assumptions | exact/stable inverse problems | R12's known-subspace pseudoinverse case is simpler and already classical |
| Hardware neural checksums | detect/correct numerical memory/compute faults | fault model and redundant codes | hardware reliability | does not identify semantic validity or query interference |
| DeltaNet/WY | exact ordered rank-one memory update | causal keys/values/gates | actual memory recurrence and parallelization | no syndrome/protected-functional mechanism in released interface |
| Direct protected statistics | store a rank basis of `Q^TB` | declared `B,Q` | exact target at `rank(Q^TB)d_v` state | same-width sufficient statistic; designed syndrome is only a coordinate change |

## Novelty and source verdict

- Mathematical correctness can be reviewed independently from novelty.
- The nullspace factorization is classical linear algebra/sufficient-statistic geometry; the noise result is a pseudoinverse conditioning bound.
- Delta specialization is a transparent rank-one update identity. It does not define a new recurrence, recover semantic identity, or improve the known information bound.
- For a known family of later query functionals, storing coordinates in a matrix basis `J` for their joint row space (`JA`) is a direct sufficient statistic with the same minimum scalar width as any exact syndrome. A possible residual systems question exists only for an externally imposed/implicit `H`, unknown-at-write queries covered by a justified subspace, or a demonstrated compute/layout benefit. No natural task, author implementation, native scorer, or equal-precision advantage has been established.

Verdict: **PARK as conditional theorem/control; no method-candidate admission.** Exact-priority coverage is `INCONCLUSIVE_EXPAND_SEARCH`, not a novelty kill. Empirical value is unknown, not failed.

## Native measurement readiness

At LongMemEval official repository commit `9e0b455f4ef0e2ab8f2e582289761153549043fc`, `src/evaluation/evaluate_qa.py` has a `knowledge-update` answer-correctness judge and `print_qa_metrics.py` aggregates task/overall accuracy. These files do not expose internal `B,Q,N`, decoder condition number, or per-write protected effect. bAbI and LAMBADA were not re-audited in R12 and should not be treated as mechanism-ready assets. This is a preliminary measurement-gap note, not native readiness. No substitute cases, labels, or metric were created; no scorer was run.
