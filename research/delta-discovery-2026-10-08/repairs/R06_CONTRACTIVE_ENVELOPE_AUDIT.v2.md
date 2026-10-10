# R06 v2 — contractive-envelope selective audit

Status: **conditional theorem/control; substantive repair attempt 2; not an active candidate; no experiment executed**. This child preserves R06 v1 and its reviews byte-for-byte. It repairs only the unresolved claim that a legal prefix-only Delta sensitivity proxy might support an efficiency or regret guarantee.

## 1. Original problem and exact patch

R06 v1 estimates a finite-log moment

\[
m_T=T^{-1}\sum_{i=1}^T Y_i Z_i
\]

from randomized external audits, where `Y_i in [0,1]` is a grounded label and `Z_i` is an action-independent post-horizon sensitivity. It correctly states that a write-time audit policy cannot use a future-dependent `Z_i`; it may use only a prefix-measurable proxy `X_i`. What remained unproved was whether such a proxy has any principled allocation guarantee.

The v2 patch restricts the propagation law instead of pretending the future is observed. For the original Delta recurrence in key-by-value convention,

\[
S_s=(I-\beta_s k_s k_s^\top)S_{s-1}+\beta_s k_s v_s^\top,
\qquad A_s=I-\beta_s k_s k_s^\top, \tag{1}
\]

let the current write displacement be

\[
U_i=\beta_i k_i e_i^\top,
\qquad e_i=v_i-S_{i-1}^\top k_i. \tag{2}
\]

On a declared frozen-feature, same-future-input path through horizon `H`, its homogeneous propagated displacement is

\[
\widetilde U_{i,H}=P_{i,H}U_i,
\qquad P_{i,H}=A_HA_{H-1}\cdots A_{i+1}. \tag{3}
\]

This is not the full closed-loop network Jacobian. If the edit changes later keys, gates, routing, tokens or updater state, equation (3) is only a frozen-path analysis object and the complete-state Jacobian remains necessary.

## 2. A legal prefix envelope

Assume for every future factor on the declared path

\[
0\le \beta_s\|k_s\|_2^2\le 2. \tag{4}
\]

The eigenvalues of the symmetric rank-one factor `A_s` are `1` on `k_s^perp` and `1-beta_s||k_s||^2` on `span(k_s)`. Hence

\[
\|A_s\|_2\le 1,
\qquad \|P_{i,H}\|_2\le 1. \tag{5}
\]

Define the realized frozen-path influence magnitude and prefix envelope

\[
Z_i=\|P_{i,H}U_i\|_F,
\qquad X_i=\|U_i\|_F
=|\beta_i|\|k_i\|_2\|e_i\|_2. \tag{6}
\]

Then

\[
0\le Z_i\le X_i. \tag{7}
\]

`X_i` is prefix measurable and costs only norms already available around the Delta write. It is an upper envelope, not an estimate of factual validity, signed action benefit, or full nonlinear future loss.

## 3. Robust audit allocation is exactly solvable

Consider independent Bernoulli auditing with propensities `pi_i`, an expected audit budget

\[
\sum_i \pi_i=B,
\qquad 0<\pi_i\le 1, \tag{8}
\]

and HT second-moment term

\[
J(\pi;Y,Z)=\sum_i\frac{Y_i^2Z_i^2}{\pi_i}. \tag{9}
\]

Over the rectangular uncertainty set `0<=Y_i<=1`, `0<=Z_i<=X_i`, the coordinatewise supremum is attained at `Y_i=1,Z_i=X_i`. Restrict first to the estimand support `X_i>0`; when `X_i=0`, equation (7) forces `Z_i=0`, so that event contributes zero to this moment. Ignoring inactive caps for the moment, the robust design is therefore

\[
\min_{\pi_i>0,\ \sum_i\pi_i=B}
\sum_i\frac{X_i^2}{\pi_i}. \tag{10}
\]

Cauchy--Schwarz gives

\[
\left(\sum_iX_i\right)^2
\le \left(\sum_i\frac{X_i^2}{\pi_i}\right)
\left(\sum_i\pi_i\right), \tag{11}
\]

with equality exactly when

\[
\boxed{\pi_i^{\rm env}=
B\frac{X_i}{\sum_jX_j}}. \tag{12}
\]

The minimax value is `(sum_i X_i)^2/B`. With a positivity floor and cap, let `I_+={i:X_i>0}` and `I_0={i:X_i=0}`. While `B<=|I_+|+|I_0|epsilon`, KKT gives, uniquely on `I_+`,

\[
\pi_i^{\rm env}=\operatorname{clip}_{[\epsilon,1]}(cX_i),
\quad i\in I_+, \qquad
\pi_i^{\rm env}=\epsilon,
\quad i\in I_0, \tag{13}
\]

where `c` is chosen to meet the feasible budget. If that budget exceeds `|I_+|+|I_0|epsilon`, every positive-envelope coordinate is already capped at one and the excess must be assigned arbitrarily among zero-envelope coordinates; the optimum is then generally non-unique. If all `X_i=0`, every feasible allocation is optimal. Exact fixed-size sampling still needs PPS/rejective design and second-order inclusion probabilities; (9)--(13) are finite-frame Bernoulli-design statements, not a causal one-pass normalization rule over an unknown future stream.

Against uniform `pi_i=B/T` on a frame of `T` positive-envelope events in the no-cap regime, the worst-case second-moment improvement factor is

\[
\frac{J_{\rm unif}^{\rm worst}}
{J_{\rm env}^{\rm worst}}
=\frac{T\sum_iX_i^2}{(\sum_iX_i)^2}
=1+\operatorname{CV}(X)^2. \tag{14}
\]

Thus the allocation has a precise benefit only when prefix envelope magnitudes are heterogeneous. This is a ratio of worst-case HT second-moment terms, not in general a ratio of conditional variances. This is robust Neyman allocation specialized by the Delta contraction envelope, not a new sampling principle.

## 4. Sharp price of using the envelope

If realized `Z_i` were visible before auditing, `sum_i Z_i>0`, and caps were inactive, an active-support oracle allowing zero propensity on known-zero contributions would use `pi_i^Z=BZ_i/sum_jZ_j` and achieve

\[
J^*(Z)=\frac{(\sum_iZ_i)^2}{B}. \tag{15}
\]

Under the strict positivity condition in (8), this is an infimum approached as the propensities of known-zero contributions tend to zero; a positive floor instead produces the corresponding clipped oracle and a larger value. If every `Z_i=0`, both `J^*(Z)` and the ratio below are left undefined because the entire moment is zero.

For `X_i>0`, write `r_i=Z_i/X_i` and `w_i=X_i/sum_jX_j`. The envelope/oracle ratio is

\[
R=\frac{J(\pi^{\rm env};Z)}{J^*(Z)}
=\frac{\sum_iw_ir_i^2}{(\sum_iw_ir_i)^2}. \tag{16}
\]

If an independently justified continuation law gives the two-sided guarantee

\[
0<\alpha\le r_i\le1 \quad\text{for every eligible }i, \tag{17}
\]

then `(1-r)(r-alpha)>=0` implies `r+alpha/r<=1+alpha`. Define tilted weights `q_i=w_ir_i/(sum_jw_jr_j)`. Under `q`, equation (16) equals `(sum_iq_ir_i)(sum_iq_i/r_i)`. Applying the scalar Kantorovich inequality to `r_i in [alpha,1]` yields the sharp bound

\[
\boxed{R\le\frac{(1+\alpha)^2}{4\alpha}}. \tag{18}
\]

Equality is achievable with two ratio values at the endpoints and the corresponding extremal weights. This is the same classical spectral/ratio inequality already used in R20 v3; its application here does not establish novelty.

Contraction alone supplies only `r_i<=1`, not a positive lower bound. With weights `w_1=1-delta,w_2=delta` and ratios `r_1=0,r_2=1`, equation (16) gives `R=1/delta`, which diverges as `delta->0`. Therefore

\[
\boxed{\sup_{0\le Z_i\le X_i}R=\infty.} \tag{19}
\]

The prefix envelope is minimax for its declared worst-case rectangle, yet can have unbounded realized regret relative to a clairvoyant future-sensitive allocator. These are not contradictory objectives.

## 5. Same-prefix witness and old counterexamples

Take `U_i` with left factor parallel to a future normalized key `k`. With `beta=1`, the next factor `A=I-kk^T` annihilates that component, so `Z_i=0`. A continuation whose later keys are orthogonal to the same left factor preserves it, so `Z_i=X_i`. Both continuations can share the entire action-time prefix and the same `X_i`. No prefix-only rule can infer a positive universal `alpha` over unrestricted continuations.

This preserves every R06 v1 boundary:

1. `Y` is factual validity, not the ideal write action; R07's signed benefit/protection/curvature bridge is still required.
2. If returned audits affect later updates or observations, the target policy changes and single-step HT/AIPW remains invalid without a firewall or sequential OPE.
3. For AIPW, the realized residual amplitude is `|Y_i-q_i|Z_i`. It may vanish while `X_i>0`, so a two-sided ratio is even less plausible without explicit residual calibration.
4. Unknown full-network feature changes are not absorbed into `P`; a frozen path is not a closed-loop guarantee.
5. A positive floor over an unbounded stream remains incompatible with a fixed total number of audits.

## 6. Prediction, falsifier, cost and strong controls

Distinguishing prediction: at matched expected audit count, envelope PPS should reduce the worst-case HT second-moment term relative to uniform sampling in proportion to `1+CV(X)^2` only when the frozen-path envelope is the relevant uncertainty description. Its realized advantage over a learned residual/influence proposal should collapse when future Delta factors strongly and unevenly attenuate current writes.

Falsifier/boundary: if an eligible trace violates (4), if edits materially change future features, or if a matched-information learned proposal predicts `|Y-q|Z` substantially better than `X`, the certificate does not justify envelope allocation. A measured endpoint gain would not repair those premises.

Information and state: computing `X_i=|beta_i|||k_i||||e_i||` is `O(d_k+d_v)` once `k_i,e_i` exist. Equation (12) is an offline finite-frame allocation because its normalization uses all frame values `X_j`; prefix measurability of each score does not make that normalization causal. A declared online PPS/reservoir construction may require a first pass or state scaling with the retained sample, and no total implementation-cost guarantee is claimed here. External-label cost remains `B`; post-horizon `Z` still requires declared instrumentation.

Mandatory same-information controls are uniform HT/AIPW, generic learned influence/Neyman allocation, fixed-size PPS/rejective sampling, direct prediction of residual influence or action advantage, R07/R08 action controls, and the no-write/fixed-Delta baselines. The direct learned proposal is strictly more flexible; v2 offers a robust certificate, not a demonstrated accuracy or total-cost advantage.

## 7. Source, measurement and disposition

The recurrence and actual author implementation interface are already pinned in the packet: DeltaNet 2102.11174v3 equations 23--25; Parallel DeltaNet 2406.06484v6; FLA commit `07ca1e49ef6ca76a7f0dbc8d5ad040ab59434c38`, `fla/ops/delta_rule/naive.py::delta_rule_recurrence/chunkwise`. R06 v1 already reads optimal unbiased active learning, active testing, two-phase validation, adaptive AIPW and Neyman/influence allocation. R20 v3 already records the sharp Kantorovich factor and the prefix-to-future impossibility pattern. Consequently the robust allocator, ratio inequality and same-prefix witness are controls/theory, not a method-level originality pass.

Existing edit/temporal-memory benchmarks can measure downstream behavior after the fact but do not natively expose `(Y_i,X_i,Z_i,pi_i)`, an action-time continuation lower bound, or same-state counterfactual audit outcomes. No new benchmark, labels, scorer, metric or result is created here.

Decision: **mathematical correctness conditional on the frozen contractive path; contribution is a useful Delta-specialized robust-allocation theorem plus an impossibility boundary; empirical effect unknown; candidate increment zero.** R06 has used two of three allowed substantive attempts. Reopen once more only with a genuine prefix-checkable two-sided continuation/residual law, a native randomized audit object, or a matched-total-cost advantage over the listed generic proposals.

