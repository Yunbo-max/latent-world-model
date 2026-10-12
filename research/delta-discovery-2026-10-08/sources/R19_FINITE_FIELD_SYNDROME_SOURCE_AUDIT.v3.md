# R19 v3 finite-field syndrome release: source, collision, cost, and measurement audit

Scope: bounded primary-source reading plus reuse of fixed R19/R18 source records. No author/project code was executed; no data/model was downloaded; no test, training, inference, scoring, GPU work, paid service or Docker was used.

## 1. Fixed sources and actual use

| Source | Fixed identity / inspected scope | Consequence for R19 v3 |
|---|---|---|
| Meng and Ramamoorthy, *Quantum advantage in zero-error function computation with side information* | arXiv `2402.01549v4`; §I-A Definitions 1, 3 and 4; §VI Definitions 17 and 19 | Decisive broad collision. R19's state is the encoder source, `(Az,m)` is decoder side information, and `B_mz+b_m` is the requested function. The one-shot fixed-length object is graph coloring; graph-entropy/asymptotic variants are different claims. The quantum extension is not used. |
| Prashant Koulgi, Ertem Tuncel, Shankar L. Regunathan and Kenneth Rose, *On Zero-Error Source Coding With Decoder Side Information* | IEEE Transactions on Information Theory 49(1):99--111, January 2003, DOI `10.1109/TIT.2002.806154`; primary PDF §I states that fixed-length zero-error side-information codes are graph colorings and treats variable-length codes separately | Confirms that exact fixed-length coloring is established coding machinery and that variable-length claims cannot be imported into v3. |
| Yao and Jafar, *The Capacity of 3 User Linear Computation Broadcast* | arXiv `2206.10049v3`; §2 conditional-rank notation and §3.1 equations (1)--(7) for the general finite-field linear-computation-broadcast formulation | Structured collision. Mapping release branches to users with common side information `Az` is exact. The arbitrary-`M` common-side formula used by v3 is the artifact's elementary quotient specialization, not a theorem stated verbatim in this source; Sun--Jafar directly supports the two-branch case. |
| Sun and Jafar, *On the Capacity of Computation Broadcast* | arXiv `1903.07597v1`; §2.1 equations (1)--(3), §2.5.1 equations (16)--(19), Theorem 3 and Appendix equations (193)--(199) | For two branches with common side information, the exact linear-computation broadcast cost reduces to the same conditional rank. This supports collision, not Delta effectiveness. |
| Lee, Dimakis and Heath, *Index Coding with Coded Side-Information*; Byrne and Calderini, *Error Correction for Index Coding With Coded Side Information* | arXiv `1501.00077v1` and `1506.00785v2`; coded linear side-information/minrank scopes | Broader mechanism neighbors. They do not by themselves prove arbitrary nonlinear optimality for R19; the complete-multipartite clique proof supplies that special-case converse. |
| Ebrahimi and Jafari Siavoshani, *On Index Coding and Graph Homomorphism* | arXiv `1408.7019v1`, 2014-08-29; abstract and stated scalar/vector/nonlinear versus linear/minrank scope | Neighboring collision/control only. It shows that side-information coding already distinguishes nonlinear, scalar, vector and linear codes. R19 v3 does not claim the general index-coding problem or minrank formula. |
| Petreczky, Bako and van Schuppen, *Realization theory of discrete-time linear switched systems* | arXiv `1103.1343v2`; minimality via reachability/observability and generalized Hankel-rank scope, already fixed in R19 v2 | Stacking all branch/path reads and quotienting their common invisible subspace is switched-observability/minimal-realization machinery. V3's rank quotient is a one-event finite-field specialization, not a new realization principle. |
| Project R18 v2/v3 and R19 v2 records | `R18_PREFIX_CAUSAL_ROBUST_QUOTIENT.v2.md`, `R18_BOUNDED_FIBER_LEAKAGE_LEDGER.v3.md`, `R19_PREFIX_CAUSAL_BRANCH_CODE.v2.md`, their source audits and final-byte reviews | R18 already supplies the strong joint-row/direct-ledger comparison; R19 v2 already supplies the general finite graph object. V3 may retain only the exact structured collapse and no-advantage boundary. |

Primary search on 2026-10-12 used the exact queries `zero-error function computation side information linear finite field rank syndrome coding`, `index coding confusion graph chromatic number linear code side information`, `linear computation broadcast common side information conditional rank`, and the fixed arXiv identifiers above. The accessible primary records establish the general graph-coloring and linear-computation-broadcast collisions. The source search did not establish priority for the exact elementary complete-multipartite decomposition written in v3; no firstness claim is made.

## 2. What is derived here and what is already covered

The v3 graph has edge differences

\[
\ker A\setminus(\ker A\cap\ker B).
\]

Therefore each `A`-fiber is partitioned by cosets of `H=ker A intersect ker B`; vertices within a coset are nonadjacent and vertices in distinct cosets are adjacent. The graph is complete multipartite and its chromatic number equals the number of parts, `q^r`. A complement-row syndrome realizes those colors.

This proof is self-contained linear algebra plus the already-known confusion-graph coding equivalence. It is a useful exact specialization because it removes NP-hard coloring for the declared class. It is not a distinct function-computation theorem, index code, switched observer or Delta updater.

The strongest simple control is not the naive tuple of all branch outputs. It row-reduces the stacked target map and removes rows already recoverable from `Az`. That construction has the same width

\[
\operatorname{rank}([A;B])-\operatorname{rank}(A)
\]

and the same decoder factorization as the syndrome. R18's joint-row ledger is the identical information object. Thus a claim of lower state than direct storage would rely on an intentionally weak baseline.

## 3. Cost and information audit

The theorem charges:

- exact finite-field symbols and their bit representation;
- offline rank/basis/factorization work;
- retained matrices/codebook and per-branch decoder data;
- per-event encode and decode field operations;
- the genuinely observed post-write side information and branch label; and
- quantizer/range/overflow/error-protection metadata for any physical approximation.

General graph coloring can be hard; the structured class uses polynomial Gaussian elimination. That computational gain does not create a scientific method difference because the strong direct quotient uses the same elimination. Nonlinear or randomized exact encoders cannot beat the clique lower bound; approximate, block, variable-length or distribution-dependent coding changes the object and requires fresh analysis.

## 4. Native measurement feasibility

The fixed benchmark conclusion from v2 remains unchanged. LongMemEval, LongMemEval-V2, EvoMemBench, AToKE and SEAL can test downstream updating, retrieval, temporal conflict or forgetting endpoints. bAbI, LAMBADA, RULER and BABILong can test task accuracy or long-context retrieval. None natively supplies a finite-field hidden state, matrices `A,B_m`, quotient rank, exact syndrome bits, clique witness, or a matched-cost side-ledger mechanism label.

An instrumented algebraic diagnostic could verify the theorem on a declared finite object, but it would be a derived diagnostic rather than native benchmark evidence. It cannot establish downstream language-model benefit. Strong future behavioral controls remain the row-reduced direct signature/R18 ledger, full pre-write retention, no-write/fixed protection, R08 same-evidence release, full-history/time-conditioned KV, and same-capacity replay or external KV.

## 5. Decision

Mathematical status: exact conditional theorem for a one-shot noiseless finite-field linear/affine release.

Contribution status: tractable structured specialization and a sharp no-advantage boundary.

Novelty status: decisive collision with zero-error function computation plus major R18/switched-observability overlap; exact complete-multipartite derivation retained without priority claim.

Measurement status: native mechanism object absent.

Empirical status: unknown; no execution.

Disposition: R19 attempt 3/3 should be terminally parked with `candidate_delta=0`. The patch repairs tractability but proves equivalence to the strongest same-information baseline rather than a distinct updater.
