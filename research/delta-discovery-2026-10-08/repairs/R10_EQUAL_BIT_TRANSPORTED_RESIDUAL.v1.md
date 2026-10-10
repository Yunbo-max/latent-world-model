# R10: equal-bit transported residual — radix equivalence and operator boundary

Status: repair attempt 1 of at most 3. Lineage child of `rejected/D04_COMPENSATION_COLLISION.md`; the parent bytes, counterexample, and review remain unchanged. This artifact is mathematics/source review only. No model code, software test, training, inference, scoring, or benchmark result was produced.

## 1. Original problem, failure type, and retained result

D04 correctly separated two updates for a frozen affine Delta state

\[
S_t^\star=A_tS_{t-1}^\star+B_t,
\qquad A_t=(I-\beta_tk_tk_t^\top)D_t.
\]

An **unchanged** carried residual,

\[
Z_t=A_tW_{t-1}+B_t+C_{t-1},\quad W_t=Q(Z_t),\quad C_t=Z_t-W_t,
\]

has lifted state (L_t=W_t+C_t) satisfying

\[
L_t=A_tL_{t-1}+B_t+(I-A_t)C_{t-1},
\]

so it does not generally recover the original affine trajectory. A **transported** residual,

\[
Z_t=A_t(W_{t-1}+C_{t-1})+B_t,
\quad W_t=Q_W(Z_t),
\quad C_t=Z_t-W_t,
\]

does give (L_t=Z_t=A_tL_{t-1}+B_t) in exact arithmetic. The retained conclusion is therefore conditional but correct: the residual must undergo the same transition if the goal is exact recovery of the frozen affine trajectory.

The parent failed as a candidate for a different reason: exact (C_t) is another full state, while a finite-width (C_t) had no same-total-bit advantage, allocation rule, or closest-work audit. This is a **budget/target mismatch**, not an algebraic failure of the transported identity.

## 2. Patch

This child closes the missing equal-bit question rather than deleting the old counterexample:

1. quantize the transported residual under an explicit total code budget;
2. compare its decoded recurrence state with the strongest direct quantizer having the same number of codes;
3. derive the remaining future-loss-weighted bit-allocation problem;
4. distinguish that representation problem from auxiliary feedback that deliberately keeps only (W_t) visible to the recurrence.

The patch changes neither the available information nor the reference trajectory. It therefore cannot manufacture a capacity gain by hiding extra precision in (C_t).

## 3. Formal object and exact error recurrence

Apply the representation argument first to one scalar coordinate. Let its finite alphabets be \(\mathcal W\) and \(\mathcal C\), with \(|\mathcal W|\le 2^{b_W}\), \(|\mathcal C|\le 2^{b_C}\), and \(b=b_W+b_C\) stored bits per scalar. A product-coded state with \(n\) scalar entries then has at most \(2^{nb}\) joint codes. The matrix recurrence below applies the scalar encoders componentwise:

\[
Z_t=A_tL_{t-1}+B_t,\qquad
W_t=Q_W(Z_t),\qquad
C_t=Q_C(Z_t-W_t),\qquad
L_t=W_t+C_t.
\]

Write the residual-quantization defect as

\[
d_t=(Z_t-W_t)-C_t.
\]

Then (L_t=Z_t-d_t). With (E_t=S_t^\star-L_t), subtraction from the reference recurrence gives the exact frozen-coefficient identity

\[
E_t=A_tE_{t-1}+d_t. \tag{1}
\]

For (P_{t:i}=A_tA_{t-1}\cdots A_i), with (P_{t:t+1}=I),

\[
E_t=P_{t:1}E_0+\sum_{i=1}^tP_{t:i+1}d_i. \tag{2}
\]

No independence, zero mean, or contraction is needed for (1)–(2). If \(\|A_j\|_2\le\rho<1\) and \(\|d_i\|_F\le\eta\), the parent bound follows:

\[
\|E_t\|_F\le \rho^t\|E_0\|_F+\eta\frac{1-\rho^t}{1-\rho}.
\]

This is a numerical state-error statement only. State-dependent keys, gates, or values require the full nonlinear Jacobian; semantic retention does not follow.

## 4. Same-cardinality representation theorem

Define the decoded pair codebook

\[
\mathcal L=\{w+c:w\in\mathcal W,\ c\in\mathcal C\}.
\]

Assume every future transition, read, and loss consumes the pair only through \(L_t=W_t+C_t\). Also hold the encoder/decoder, time index, and any external side information fixed and shared; adaptive scales, lookup tables, or codebook metadata must either be supplied equally to the direct comparator or counted in the joint state/budget. Under those conditions, every pair encoder \(x\mapsto(W(x),C(x))\) induces a direct encoder \(x\mapsto L(x)\in\mathcal L\). Moreover

\[
|\mathcal L|\le |\mathcal W||\mathcal C|\le 2^b. \tag{3}
\]

Therefore a direct \(b\)-bit state quantizer whose codebook is exactly \(\mathcal L\) can reproduce the split encoder's decoded value at every point, including every clipping and rounding choice. More generally, the admissible direct \(b\)-bit encoder class contains this split-induced mapping. Hence, for any jointly specified source distribution and expected-distortion objective, or any jointly specified worst-case distortion objective, the optimum over the direct class cannot be worse than the fixed split encoder. This statement does not claim that a distribution-optimized direct codebook is no worse at every individual point; such an optimizer may trade error among points.

This is a representation equivalence, not a claim that all encoders have equal arithmetic, packing, bandwidth, finite-arithmetic order, overflow behavior, or hardware cost. Duplicate sums or boundary clipping can make \(|\mathcal L|<2^b\), so the split may use the nominal bit budget less efficiently. If future computation reads \(W\) and \(C\) separately, then equal decoded sums can retain different hidden pair states and the theorem no longer applies.

### Nested uniform-grid corollary

Let the coarse lattice be \(\Delta\mathbb Z\). Let (M=2^{b_C}), \(\delta=\Delta/M\), and let the residual digit set contain one complete centered residue system modulo (M). Away from saturation and with consistent tie handling,

\[
\Delta\mathbb Z+\delta\mathcal J=\delta\mathbb Z.
\]

Thus, locally and away from saturation, a coarse word plus a \(b_C\)-bit residual digit is a mixed-radix encoding of a finer uniform lattice with step \(\delta\). The equal-cardinality finite conclusion follows from the theorem above, not from the infinite-lattice identity alone. Finite rails require explicit endpoint handling and may introduce duplicate codes; the lattice equality is not asserted outside the no-clipping nested-grid condition.

### Old counterexample recheck

The D04 counterexample remains intact. Transporting (C) is necessary for the exact lifted identity, but after finite coding the only recurrence-visible object is (L), whose codebook obeys (3). The patch therefore repairs the missing equal-budget analysis but does not rescue the method claim.

## 5. Operator boundary: visible-state feedback is a different method class

Suppose instead the recurrent kernel sees only a coarse state (W_{t-1}), while an auxiliary residual changes the next proposal:

\[
W_t=Q_W\!\left(F_t(W_{t-1})+C_{t-1}\right),\qquad
C_t=Q_C\!\left(F_t(W_{t-1})+C_{t-1}-W_t\right). \tag{4}
\]

Equation (4) can accumulate sub-threshold changes and alter when a coarse transition fires. It is not equivalent to propagating \(L_{t-1}=W_{t-1}+C_{t-1}\) through \(F_t\), except under special affine/interface identities. Its potential advantage over a *restricted finer-numeric-visible-state baseline* is therefore an **operator-compatibility/noise-shaping** effect: it preserves the coarse values on which the trained kernel operates while using auxiliary memory to alter future write timing. At the more general finite-state level, however, the pair \((W,C)\) can itself be relabeled as one \(b\)-bit code and simulated by a direct finite-state machine. Equation (4) therefore does not evade the total-state cardinality bound.

This distinction explains why matched storage does not contradict the representation theorem. A direct ((b_W+b_C))-bit visible state changes the kernel inputs; (4) retains a (b_W)-bit visible interface. The two methods have different transitions and may have different performance, but (4) cannot claim exact recovery of the original full-precision trajectory from the transported-residual proof.

## 6. Future-query risk and bit allocation

For fixed future coefficients and read queries (q_u), define the frozen-path output risk

\[
\mathcal R=\mathbb E\sum_{u=1}^T\|q_u^\top E_u\|_2^2.
\]

Assume here that the reference and deployed trajectories start from the same decoded state, \(E_0=0\). Substituting (2) produces diagonal injection terms and cross terms. If, additionally, the vectorized defects \(\operatorname{vec}(d_i)\) are zero-mean and have zero cross-covariance for \(i\ne j\), conditional on the frozen path, then the cross terms vanish and

\[
\mathcal R
=\sum_{i=1}^T\mathbb E\,\langle d_i,G_i d_i\rangle_F,
\qquad
G_i=\sum_{u=i}^T P_{u:i+1}^\top q_uq_u^\top P_{u:i+1}. \tag{5}
\]

Without \(E_0=0\), an initial-error term \(\sum_u\|q_u^\top P_{u:1}E_0\|_2^2\) and its applicable cross terms must be retained. Without the stochastic assumptions, (5) is not exact; correlated deterministic quantization defects retain cross terms. \(G_i\) is a finite-horizon frozen-path observability/risk operator, not a semantic-validity oracle.

Under the further separable high-rate model

\[
\mathbb E[d_j^2]\approx c_j2^{-2b_j},\qquad a_j=w_jc_j\ge0,
\]

where (w_j) summarizes the applicable diagonalized future-risk weight, the continuous relaxation is

\[
\min_{b_j\ge0}\sum_j a_j2^{-2b_j}
\quad\text{s.t.}\quad \sum_jb_j\le B. \tag{6}
\]

KKT stationarity on active coordinates yields

\[
b_j^\star=\left[\frac12\log_2\frac{a_j}{\tau}\right]_+,
\tag{7}
\]

with \(\tau\) chosen to meet the active budget when at least one \(a_j>0\). If all \(a_j=0\), every feasible allocation has the same objective and the optimizer is non-unique. Integer formats, finite codebooks, pivots, group scales, and per-format overhead turn (6) into a discrete knapsack/dynamic-programming problem; (7) is not an exact discrete allocator.

This derivation supplies a computable allocation control but not a distinct contribution: DAMP already combines local state-quantization error with decay-based persistence, and STEPQuant already optimizes lifetime-weighted candidate distortions under a nominal bit budget and adds query/readout-sensitive row weighting.

## 7. Predictions, failure boundaries, and strongest controls

Distinguishing predictions if the two operator classes are kept separate:

1. A transported split whose full future computation consumes the pair only through \(W+C\) cannot beat a direct encoder using the same decoded codebook under the same specified objective; any difference must come from implementation, arithmetic, unmatched side information, or a different codebook search.
2. A coarse-visible feedback method may beat a finer visible-state quantizer on a model trained for the coarse interface, especially when many proposals are consistently sub-threshold; this advantage should depend on run direction/persistence and can reverse after training the kernel for the finer interface.
3. Persistence-weighted allocation helps only when calibration ranks future error consequence stably enough; it can fail under distribution shift, correlated defects, state-dependent transition changes, or large unmodeled scale/metadata costs.

Failure boundaries:

- saturation, duplicate code sums, and inconsistent rounding break the simple nested-lattice corollary but not the cardinality bound (3);
- recurrence from (W) rather than (W+C) leaves the transported identity;
- separate future reads of \(W,C\), adaptive metadata not counted in the budget, or unmatched side information leave the decoded-state equivalence theorem;
- state-dependent (A_t,B_t,q_t) invalidate the frozen-path propagation as a whole-network equality;
- biased/correlated defects invalidate the diagonal risk decomposition;
- high-rate distortion laws are assumptions, not low-bit guarantees;
- bit count alone does not equal bandwidth, arithmetic, routing, energy, or latency.

Strong same-information controls are: (i) a direct quantizer with the exact decoded codebook \(\mathcal L\); (ii) an optimized direct (2^b)-code state quantizer; (iii) ordinary coarse write-back; (iv) unchanged error feedback; (v) stochastic rounding; (vi) DAMP/STEPQuant-style lifetime-aware mixed precision; and (vii) training each actual visible-state interface rather than evaluating only post-training swaps.

## 8. Information, state, computation, and measurement

The transported split has at most (b_W+b_C) stored bits per scalar plus scale/metadata. Decoding requires the two-code read and addition; transporting the decoded residual through Delta costs another state-like update if implemented separately. The exact unquantized residual restores the full-precision trajectory only by retaining a full residual state.

The auxiliary-feedback operator keeps a coarse recurrence-visible word plus (b_C) auxiliary bits and extra proposal/write logic. It may preserve a trained interface but does not have the same recurrence as a direct finer state.

Existing bAbI, LAMBADA, RULER, reasoning, and code-generation tasks can measure downstream task accuracy under an already implemented native quantized interface. They do not by themselves identify representation equivalence, exact frozen-path state error, or the cause of an operator-compatibility gain. The public STEPQuant path requires large Qwen/Kimi checkpoints and a multi-GPU SGLang stack, so it is not a demonstrated affordable native test for the project's single-RTX-2080-Ti background. No new benchmark, case, label, metric, or result is created here.

## 9. Status and disposition

- Mathematical status: the finite-residual error recursion, same-cardinality representation theorem, nested-grid corollary, operator separation, and conditional water-filling relaxation are accepted only subject to independent exact-byte review.
- Contribution status: the same-budget allocation mechanism has major functional collisions with DAMP and STEPQuant; the auxiliary-feedback operator is already represented by published residual/direction-memory write-back. The remaining clean result is a useful no-free-lunch/equivalence boundary, not an admitted new method.
- Empirical status: unknown; no execution occurred.
- Candidate admission: 0.
- Disposition: **park after repair attempt 1**.

Reopen only with a Delta-specific result that escapes the decoded-codebook equivalence and the DAMP/STEPQuant collision under actual equal total storage/traffic—for example, a provable rate advantage from a non-product entropy/sparsity constraint, or a correlated-noise-shaping theorem with a distinct observable prediction and feasible native measurement. A renamed residual, different bit split, or another decay-weighted score is insufficient.

