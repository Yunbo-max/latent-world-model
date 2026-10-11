# R11 v2 source, collision, implementation, and measurement audit

Cutoff: 2026-10-11. Scope: exact ordered Delta composition, the adjacent order gap for the pure scalar-`beta` Delta map without an intervening decay matrix, factored/core SVD, query-weighted low-rank approximation, DeltaProduct, and native measurement feasibility. This is a bounded primary-source audit, not an exhaustive originality claim. The v2 factor theorem is not asserted for general gated/decayed Delta, KDA, or state-dependent updates.

## 1. Preserved lineage

- Parent repair: `repairs/R11_ORDER_GAP_COMPRESSION.v1.md`, SHA256 `38d5ba6cb4e897b602b9897c940468cdaab0b603f5e3d9055b3f98dc52e1929b`.
- Parent source audit: `sources/R11_ORDER_GAP_COMPRESSION_SOURCE_AUDIT.md`, SHA256 `dcf788d57146e87ffe7416d1e3f8567aeabf672051040dc84e2f64d79fb3a569`.
- Parent reviews: math `6e73d9731dc9262f35f9eed79753947ca53b7f7498b589770fc6fa92d6dac5ea`; source `ffe370d513d3f4de3e69f7e63b24e5df86a852378c3d966207027d8d36e15ba9`; adversarial `6872da1c923f81470d8bfb5ed4bb3b85a6487db5589b14608e821b9c6276249e`.

Those bytes and decisions are preserved. V2 requires new review because it changes the computational claim and jointly optimizes rank under selector uncertainty.

## 2. Exact ordered Delta and WY baseline

Primary work: Yang et al., “Parallelizing Linear Transformers with the Delta Rule over Sequence Length,” arXiv:2406.06484v6, 15 January 2025, especially the exact ordered Householder-product/WY-style chunk construction.

- Official full text: https://arxiv.org/abs/2406.06484 and https://arxiv.org/pdf/2406.06484v6 .
- Read depth reused from the parent audit: Section 2.2 for the Delta recurrence and Sections 3.1--3.2 for the exact order-preserving WY/chunk construction.
- Functional consequence: exact chronological composition is already available. R11 v2 is not needed to make an ordered Delta recurrence correct; it analyzes/compresses a counterfactual adjacent branch gap.

This remains the strongest non-oracle baseline. Any semantic correction must beat or complement retaining the observed order, not compare only against a commutative approximation.

## 3. DeltaProduct mechanism and fixed author interfaces

Primary work: Siems et al., “DeltaProduct: Improving State-Tracking in Linear RNNs via Householder Products,” arXiv:2502.10297v7, 22 October 2025, especially Section 4 equations defining multiple ordered `n_h` steps per token and Section 5.2/Figure 5 for permutation-group state tracking.

- Official full text: https://arxiv.org/abs/2502.10297 and https://arxiv.org/pdf/2502.10297v7 .
- Author-maintained FLA implementation, preserved pin: commit `a7880060012c862d58575ee23f613cafcd728d03`, `fla/layers/gated_deltaproduct.py`, blob `82d1a62ac228f3c80aa8818b6e0d0082ce6635b8`.
- Authors' task repository, preserved pin: `automl/DeltaProduct` commit `d62241a81d07aa32b1b65e7d17377f6a7cd0a5d8`; `README.md` blob `c316366630cf63fbd8cd74c27680a95fbc6d0bb5`; `state_tracking/src/generate_data.py` blob `66ca0701e1dd3508e1459d4b6d494b393e2091c5`; `state_tracking/src/main.py` blob `1e72f648fdda2a0114b263e7e01e7d63c8ac356f`; `state_tracking/src/utils.py` blob `4ef3b1cef867e6f190cf0defbaf443ece742aa65`.

The paper and code preserve ordered low-rank microsteps and use their product for expressivity. They do not provide R11's harmful-order semantic selector, but they are a decisive mechanism/control collision against treating a rank-two adjacent order effect as a new architecture.

## 4. Factored/core SVD collision

Primary work: Matthew Brand, “Fast Low-Rank Modifications of the Thin Singular Value Decomposition,” *Linear Algebra and its Applications* 415(1):20--30, 2006, DOI `10.1016/j.laa.2005.07.021`.

- Publisher record: https://www.sciencedirect.com/science/article/pii/S0024379505003812 .
- Author-institution technical report/full text: https://www.merl.com/publications/docs/TR2006-059.pdf ; MERL record `TR2006-059`, May 2006.
- Read depth: abstract and Section 2, equations (1)--(5), article pages 22--23 (MERL PDF pages 4--5). Brand explicitly reduces additive low-rank SVD modifications to extended orthogonal bases plus a small core `K`, then diagonalizes that core; rank-one updates are a specialization.

R11 v2 does not reuse Brand's streaming-update problem verbatim: it starts from a fresh rank-two Delta gap and a left query metric. Nevertheless, once `G^{1/2}K` is represented by two skinny factors, orthogonalize-the-factors and SVD-the-small-core is standard low-rank linear algebra. This is a **major computational collision**. The exact residual factorization and causal reconstruction are Delta-specific derivations, but the core-SVD solver is not a novel mechanism.

Classical Eckart--Young--Mirsky is used only for the best rank-`r` Frobenius tail after the declared left metric. No originality claim is attached to truncation.

## 5. Weighted low-rank boundary

The v1 objective uses a one-sided positive-semidefinite query metric:

`||G^(1/2)(K-C)||_F^2`.

After mapping to the weighted image, it is an ordinary Frobenius low-rank problem on the active range of `G`; its optimum follows from Eckart--Young--Mirsky. This should not be conflated with general elementwise weighted low-rank approximation, which can be harder.

For landscape context only, Nathan Srebro and Tommi Jaakkola, “Weighted Low-Rank Approximations,” ICML 2003, studies the broader elementwise-weighted problem. The R11 theorem does not depend on that paper, and the broader difficulty is not used to inflate R11's contribution.

## 6. Functional comparison

| Work/object | Ordered state mechanism | Low-rank computation | Selector information | Residual difference from R11 v2 |
|---|---|---|---|---|
| Yang et al. Delta/WY | exact chronological Delta composition | ordered compact chunk factors | none | no counterfactual semantic branch choice |
| DeltaProduct | multiple ordered Householder/Delta microsteps | product of low-rank transitions | learned sequence features, not a validity oracle | expressivity mechanism already uses order |
| Brand 2006 | general additive SVD modification | orthogonal skinny factors plus small core SVD | none | generic matrix computation, not Delta residual semantics |
| R11 v2 | counterfactual adjacent frozen-feature gap | exact two-key/two-residual factors and at-most `2 x 2` weighted core | externally estimated `p=P(z=+1|X)` | exact Delta factor/reconstruction and risk split; selector remains missing |

Adjudication: the ordered-update/ordered-low-rank expressivity mechanisms and the small-core numerical method are covered. The exact pure-Delta residual factorization and risk split remain a narrow derived theorem, not an established novel method. The uncaptured method-level problem is a semantic order decision, and R11 v2 supplies no lawful estimator or native measurement for it.

## 7. Native measurement and scorer status

The preserved `automl/DeltaProduct` author repository generates group word-problem sequences with cumulative group-product targets. Noncommuting groups such as S3/S4/A5/S5 can in principle test whether order is represented. `state_tracking/src/main.py` imports `sfirah.metrics::{token_accuracy,sequence_accuracy}`, and `state_tracking/src/utils.py` supplies cumulative prefix accuracy.

Readiness remains partial and unchanged from v1: the `sfirah` dependency revision and exact scorer denominator were not pinned in the inspected tree, and the repository generates data rather than publishing one fixed dataset. The paper's wider Chomsky-hierarchy assets were not present in the inspected author tree. No interface was executed.

More importantly, group multiplication labels legitimate order; it does not label when an observed write order should be reversed, suppressed, or revised. It exposes neither `K`, a prefix-causal `G`, nor counterfactual semantic branch labels. The parent source audit (SHA256 `dcf788d57146e87ffe7416d1e3f8567aeabf672051040dc84e2f64d79fb3a569`) recorded the same measurement mismatch for its already inspected bAbI/LAMBADA assets; v2 adds no new claim about those benchmarks. The mathematical core admits a future numerical algebra/engineering check only; that is not a native scientific benchmark and would not close semantic measurement.

No benchmark, dataset, case, label, metric, score, or empirical result is fabricated here.

## 8. Information and implementation boundary

Within the pure-Delta scope, the v2 algebra removes the dense-SVD requirement. Given a representation that applies `G` to two keys, it needs only two `G` matvecs, small Gram matrices, and an at-most `2 x 2` factorization. The chronological residual identity can reconstruct the common-prestate second residual from the post-first-write residual plus a retained first residual.

This does not make the method free:

- a dense `G` still costs quadratic key-side state and matvec work;
- a sketch must be prefix-lawful and its approximation error reviewed;
- one pending pair needs retained key/residual/gate state, while all-pairs or multi-swap variants need more;
- materializing or writing a rank-`r` correction into the full state costs `O(r d_k d_v)`;
- estimating the semantic posterior `p` remains the dominant unclosed information problem, and plug-in calibration error must be charged on retained core directions;
- a factored overlay must participate in later residual reads, and repeated edits require carry, merge, recompression, or materialization.

No R11-specific author implementation exists because R11 is a derived control, not a published method. The pinned FLA/DeltaProduct interfaces and Yang paper formulas are controls only and were not run.

## 9. Decision

Source status: sufficient to classify the small-core solver and ordered-update mechanism as known, but not an exhaustive search over every low-rank or continual-learning paper. Mathematical novelty of the exact Delta residual factorization is not equivalent to method novelty.

- Mathematical identity: derived; requires new exact-byte independent review.
- Closest-work distinction: Delta-specific factor/reconstruction remains a narrow theorem; computation and ordered mechanisms collide.
- Measurement: semantic selector and causal query metric remain unsupported by a pinned native object.
- Empirical effect: unknown; no execution.
- Candidate admission: `0`.
- Recommended disposition: park R11 after attempt 2.

A third attempt should reopen only for new causal information and a matched-budget Delta-specific consequence, not another factorization, rank threshold, or solver variant.
