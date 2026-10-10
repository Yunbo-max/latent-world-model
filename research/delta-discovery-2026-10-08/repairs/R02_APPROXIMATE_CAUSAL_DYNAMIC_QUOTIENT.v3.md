# R02 v3 — quantitative approximate causal and dynamic quotient certificate

Status: **conditional theorem/debugging control; parked after attempt 3/3, not an active D candidate**. This versioned child of `R02_CAUSAL_DR_QUOTIENT.v2.md` replaces exact quotient sufficiency by explicit tolerances. It preserves the old counterexamples, proves a sharp one-step coarsening-bias bound, derives a separate finite-horizon target-value abstraction bound, and identifies the exact Delta coefficient leakage for `q=SW`. It does **not** prove an approximate sequential-DR estimator guarantee, a prefix-only certificate, novelty, or empirical benefit.

## 1. Original problem, failure type, and patch

R02 v2 gives two exact results:

1. quotient-only AIPW bias is a within-cell propensity–outcome covariance divided by the coarse propensity;
2. exact sequential DR descends under policy, reward/value and action-conditioned quotient-transition closure.

The remaining defect is **assumption/checkability mismatch**, not an algebra error. Exact fiber constancy is too strong to treat as a practical certificate, but a small memory reconstruction error is unrelated to causal balance or target-policy continuation error. The patch is intentionally two-part:

- quantify the already exact one-step AIPW coarsening identity;
- separately quantify fixed-policy value error from reward and quotient-transition defects.

These two bounds answer different questions. Combining them mechanically would omit quotient behavior/target ratio errors, pointwise overlap, product-ratio amplification, occupancy shift and nuisance-estimation remainders, so it would not be a sequential-DR theorem.

## 2. Sharp one-step quotient-AIPW bias bound

Fix action `a` and quotient cell `Q=q`. Retain the v2 notation

\[
m_a(H)=\mathbb E[Y^a\mid H],\quad
\mu_a(H)=\Pr(A=a\mid H),\quad
p_a(q)=\bar\mu_a(q)=\mathbb E[\mu_a(H)\mid q]>0.
\]

For any fixed, cross-fitted, or pre-action-predictable quotient nuisance, v2 proves

\[
B_a(q)=\mathbb E[\psi_a^Q\mid q]-\mathbb E[m_a(H)\mid q]
=\frac{\operatorname{Cov}(\mu_a(H),m_a(H)\mid q)}{p_a(q)}.
\tag{1}
\]

If both conditional second moments are finite, conditional Cauchy–Schwarz gives

\[
\boxed{
|B_a(q)|\le
\frac{\sigma_{\mu,a}(q)\,\sigma_{m,a}(q)}{p_a(q)}.}
\tag{2}
\]

Under coarse overlap `p_a(q)>=epsilon>0`, the denominator may be replaced by `epsilon`. If additionally
`mu_a in [mu_L,mu_U]` and `m_a in [m_L,m_U]` within the cell, the conditional Grüss inequality gives the alternative

\[
|B_a(q)|\le
\frac{(\mu_U-\mu_L)(m_U-m_L)}{4p_a(q)}.
\tag{3}
\]

Equation (2) is sharp. Let two histories in the same quotient cell be equiprobable, with

\[
\mu_a=p\pm\delta,\qquad m_a=m_0\pm\eta,
\]

using aligned signs and legal probability/outcome ranges. Then covariance is `delta eta`, the two conditional standard deviations are `delta` and `eta`, and equality holds in (2). The v2 witness `p=1/2`, `delta=1/4`, `m_0=1/2`, `eta=1/2` remains an equality case with bias `1/4`; no counterexample was deleted.

### What the bound does not identify

The quantities in (2) are generally not functions of a single observed quotient prefix. A quotient-only observational distribution can leave the target mean unidentified. For example, let hidden equiprobable histories `h_0,h_1` share one `q`, with behavior propensities `1/4,3/4`. In world A take Bernoulli action-1 outcome means `(0,1)`; in world B take `(1,2/3)`. In both worlds

\[
\Pr(A=1)=1/2,\qquad
\mathbb E[\mu_1(H)m_1(H)]=3/8,
\]

so the quotient-level joint law of binary `(A,Y)` can be identical after setting action-0 outcomes identically. Yet the target action-1 means are respectively `1/2` and `5/6`. Repeated randomized coverage with the hidden/full history, an environment model, or additional structural assumptions is needed to estimate the within-fiber variation.

Coarse positivity `p_a(q)>0` also does not repair pointwise support: a target-active history inside the cell may still have `mu_a(H)=0`.

## 3. Finite-horizon target-value abstraction bound

This section concerns model-based target-policy value approximation, not DR estimator bias.

Let `q_t=phi_t(H_t)` and require the target policy itself to factor exactly,

\[
\pi_t(a\mid H_t)=\bar\pi_t(a\mid q_t).
\tag{4}
\]

Let `r_t(h,a)=E[L_t|h,a]`, let `P_t^phi(.|h,a)` be the pushforward law of `q_{t+1}` under the real next-history kernel, and choose abstract objects `bar r_t(q,a)` and `bar P_t(.|q,a)`. Assume `0<=r_t,bar r_t<=R_t`, discount `gamma in [0,1]`, and define conventional total variation

\[
d_{TV}(P,Q)=\sup_B|P(B)-Q(B)|=\tfrac12\|P-Q\|_1.
\]

Hence `|E_P f-E_Q f|<=span(f)d_TV(P,Q)`. Define uniform, target-reachable defects

\[
\epsilon_{r,t}=\sup_{h,a}|r_t(h,a)-\bar r_t(\phi_t(h),a)|,
\]

\[
\epsilon_{P,t}=\sup_{h,a}d_{TV}
\left(P_t^\phi(\cdot\mid h,a),
\bar P_t(\cdot\mid\phi_t(h),a)\right),
\tag{5}
\]

where the suprema need only cover histories/actions reachable under the declared target and comparison domain. Let

\[
M_t=\sum_{u=t}^T\gamma^{u-t}R_u,\qquad
\Delta_t=\sup_h|V_t(h)-\bar V_t(\phi_t(h))|.
\]

Use the terminal convention `M_{T+1}=Delta_{T+1}=0`.

Subtracting the two Bellman recursions and adding/subtracting the pushforward expectation gives

\[
\boxed{
\Delta_t\le \epsilon_{r,t}+\gamma\Delta_{t+1}
+\gamma M_{t+1}\epsilon_{P,t}.}
\tag{6}
\]

The last term uses `span(bar V_{t+1})<=M_{t+1}`. Expanding the recurrence yields

\[
\boxed{
\Delta_t\le
\sum_{s=t}^T\gamma^{s-t}\epsilon_{r,s}
+\sum_{s=t}^{T-1}\gamma^{s-t+1}M_{s+1}\epsilon_{P,s}.}
\tag{7}
\]

If signed losses rather than nonnegative bounded losses are used, replace `M_t` by a valid span or sup-norm bound and keep the associated TV convention explicit.

### Why behavior-average defects are insufficient

Let `Q` be constant. At `t=0`, an action produces hidden `U=1`; otherwise `U=0`. The behavior chooses that action with probability `delta>0`, while the target always chooses it. At `t=1`, set terminal loss `L_1=U`. Both policies factor through constant `Q`, and the pushforward next-`Q` kernel is identical. If the abstract terminal loss is the behavior mean `delta`, then the behavior-average absolute defect is `2delta(1-delta)=O(delta)`, whereas the terminal-step target value error is `1-delta=O(1)` (or `gamma(1-delta)` when viewed one discounted step earlier). A uniform target-reachable bound or an explicit occupancy/concentrability factor—here of order `1/delta`—is indispensable.

## 4. Delta right-quotient dynamic leakage

Let the Delta memory be `S in R^{d_k x d_v}` and choose an orthonormal `W in R^{d_v x r}`. Retain `q=SW`. For an action-dependent Delta step

\[
S^+=A(h,a)S+\beta(h,a)k(h,a)v(h,a)^T,
\qquad A=(I-\beta kk^T)D,
\]

right projection gives the exact identity

\[
\boxed{
q^+=A(h,a)q+\beta(h,a)k(h,a)v_W(h,a)^T,
\qquad v_W=W^Tv.}
\tag{8}
\]

Thus the discarded component of `v` does not directly enter `q^+`. But this algebra is a recursive quotient only if `A,beta,k,v_W` and every other recurrent side state factor through the declared `(q,z,a)`. If a gate, key, decay, route or value feature depends on discarded components of `S`, equal `q` states can still have different `q^+`.

For a deterministic abstract update `bar f_t(q,z,a)`, define the uniform leakage

\[
\epsilon_{F,t}=\sup_{h,a}
\left\|A(h,a)q+\beta(h,a)k(h,a)v_W(h,a)^T
-\bar f_t(q,z,a)\right\|.
\tag{9}
\]

Under a lawful same-side-state coupling and an `L_{t+1}`-Lipschitz abstract continuation value, (6) has the metric analogue

\[
\Delta_t\le\epsilon_{r,t}+\gamma\Delta_{t+1}
+\gamma L_{t+1}\epsilon_{F,t}.
\tag{10}
\]

For stochastic updates, replace the last defect by a Wasserstein-1 distance under the same value-Lipschitz condition. Without Lipschitz regularity use a TV/span formulation such as (6). Small Euclidean leakage does not imply small TV: distinct deterministic Dirac next states have conventional TV distance one.

The exact deterministic fiber diameter, with every retained side coordinate held fixed, is

\[
\eta_t(q,z,a)=\sup_{\substack{h,h':\,S(h)W=S(h')W=q\\z(h)=z(h')=z}}
\|f_W(h,a)-f_W(h',a)\|
\tag{11}
\]

vanishes iff the declared deterministic next-quotient map is constant on the complete `(q,z)` fiber. Choosing a cell representative gives a defect no larger than `eta_t`, but computing it usually requires full-fiber or repeated-history access. Omitting `z` from the fiber would incorrectly classify lawful side-state dependence as quotient leakage.

For a discarded tangent `E` with `EW=0`, differentiating the projected update yields

\[
Df_W(S)[E]
=(DA(S)[E])q
+D[\beta k v_W^T](S)[E],
\tag{12}
\]

because the direct term `A(S)EW` vanishes. With state-independent coefficients the local leakage is zero; state-derived gates/keys/values supply the hidden-fiber terms. Equation (12) is local only. It does not certify finite-fiber constancy, disconnected fibers or discrete routing boundaries, and it requires the complete coupled state of R18 rather than `SW` alone.

## 5. Old counterexamples and new failure boundaries

1. **Old one-step witness survives:** it is an equality case of (2), not removed by approximation.
2. **Accidental covariance cancellation:** zero covariance can occur while both propensity and outcome vary inside a cell; it is not structural factorization and is unstable under distribution shift.
3. **Old recursive witness survives:** current loss and policy checks do not imply continuation-value closure. Equations (6), (9) or a terminal defect expose it only when measured over target-reachable fibers.
4. **Pointwise support can be hidden:** coarse overlap does not imply history-level target support.
5. **Estimator/model distinction:** (6)–(10) bound target-value abstraction, not sequential-DR bias. The latter additionally needs behavior/target ratio control, overlap, estimator remainder analysis and dependence handling.
6. **Average-to-target shift:** behavior-average defects require an explicit occupancy/concentrability price.
7. **Norm/TV mismatch:** small deterministic state error has TV one unless a metric/Lipschitz route is used.
8. **Local/global gap:** equation (12) can vanish at one point while nonlinear fibers or routing switches differ globally.
9. **Prefix non-identification:** the same visible prefix/quotient can be followed by different lawful hidden fibers or suffix laws, so the defect bounds are not deployment-time oracles without extra evidence.

## 6. Information, state and compute accounting

- `q=SW` costs `d_k r` real coordinates, plus `W`, its update/description, and every retained non-memory recurrent state.
- Exact target/behavior propensities or cumulative ratios are additional ledgers; they do not make `q` Markov.
- Estimating conditional variances, uniform fiber defects, TV/Wasserstein distances or high-confidence bounds needs repeated action coverage, full-history labels, a structural environment model, or a calibration population.
- Reward, transition and value models add parameters and inference cost. Fiber suprema or Jacobian coverage can be more expensive than direct full-state prediction.
- Strong same-information controls are full-history sequential DR with exact logged ratios, direct recurrent Q/policy prediction, marginalized-ratio OPE, Hao-style learned OPE abstraction, R18 full-joint quotient/JVP auditing, and no compression with an explicit sufficient ledger.

No lower state, sample or total compute cost follows from equations (2), (7) or (10).

## 7. Predictions, falsifiers and measurement

Conditional predictions:

1. With other terms controlled, quotient AIPW error scales with the conditional covariance and is bounded by (2), not by memory reconstruction loss.
2. Exact propensity ledgers can remove one ratio-coarsening branch while leaving dynamic/terminal aliasing unchanged.
3. Under fixed quotient policy and calibrated uniform defects, horizon error obeys the ordered accumulation (7); behavior-average calibration alone can fail by the rare-cell construction.
4. For `q=SW`, hidden-state dependence enters projected dynamics through coefficient derivatives in (12), not through a direct `AEW` term.

Falsifiers include violation of (2) with correct positive propensity and second moments; violation of (7) under its uniform bounded-loss assumptions; a claimed Euclidean-to-TV implication for distinct deterministic next states; or a claimed prefix-only certificate that uses unobserved future/fiber information.

Open Bandit Pipeline-style logged data can test the one-step generic abstraction effect if the finer history remains available. They do not instantiate Delta quotient dynamics. LongMemEval, bAbI and LAMBADA provide endpoint tasks but no randomized internal actions, exact propensities, quotient fibers, uniform transition defects or paired target-policy continuations. The joint native measurement object remains absent; this is a measurement gap, not an empirical failure.

## 8. Closest work and disposition

Jiang–Li supplies sequential DR; Hao et al. directly supply OPE state-abstraction conditions and consistency results; STAR and marginalized-importance methods are same-problem controls. Classical approximate homomorphism, bisimulation metrics and simulation/value perturbation bounds cover the quantitative reward/transition part. R01 and R18 already cover transported credit and complete-state quotient leakage inside this packet.

The substantive repair delta over v2 is a sharp tolerance and accumulation audit plus the exact Delta coefficient-leakage decomposition. It does not produce a prefix-estimable quotient, a lower-cost estimator or a novel updater. The two bound families have no newly proved necessary interaction beyond being separate obligations of the same compressed causal state.

Disposition: **mathematics conditionally supported; major functional collision; candidate delta zero; empirical effect unknown; lineage exhausted and parked after attempt 3/3.** Reopen only with a lawful prefix-estimable upper-confidence certificate for the displayed defects and a matched-information total-cost or statistical advantage over full-history ratio-ledger DR, direct recurrent value/policy prediction, recent OPE abstractions and R18.

No project code, tests, model execution, benchmark scoring, training, inference, data/model download, GPU work, paid service, or Docker was used.

