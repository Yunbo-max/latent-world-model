# R02 v2 — causal quotient conditions for compressed sequential DR

Status: **conditional theorem/debugging control; parked after attempt 2/3, not an active D candidate**. This versioned child of `R02_RANDOMIZED_ACTION_CREDIT.v1.md` repairs its third residual lead. It proves what a compressed state must retain for one-step AIPW and sequential DR, specializes the conditions to a Delta right quotient, and preserves explicit failure witnesses. The general mechanism is already state abstraction for OPE; empirical benefit and a Delta-specific matched-cost advantage remain unknown.

## 1. Original problem, failure type, and patch

R02 v1 uses a full causal history

\[
H_t=(x_{\le t},S_{t-1},h^{\rm upd}_{t-1},k_t,v_t,\ldots)
\]

and randomized finite update action `A_t` with known behavior propensity `\mu_t(a\mid H_t)`. Its sequential estimator conditions on the full history. The residual proposal was to replace `H_t` by a compact summary `Q_t=\phi_t(H_t)`, particularly a Delta value-side quotient.

Failure type: **assumption/representation mismatch**, not a sign or dimension error in R02 v1. A summary sufficient for predicting one loss need not preserve conditional randomization, target/behavior action probabilities, or recursive future evolution. The patch is to state the exact causal quotient obligations and charge any retained propensity ledger or side state.

Throughout, actions use only the visible prefix and total action effects are evaluated under real later outcomes. No future target, validity oracle, self-generated judgment, or retrospective source identity is added.

## 2. One-step coarsening bias

Fix an action `a`. Let

\[
m_a(H)=\mathbb E[Y^a\mid H],\qquad
\mu_a(H)=\Pr(A=a\mid H),\qquad
\bar\mu_a(q)=\Pr(A=a\mid Q=q)=\mathbb E[\mu_a(H)\mid Q=q].
\]

Consider the quotient-only AIPW score with any fixed, cross-fitted, or pre-action-predictable nuisance `\widehat m_a(q)`:

\[
\psi_a^Q=\widehat m_a(Q)+
\frac{\mathbf 1\{A=a\}}{\bar\mu_a(Q)}
\{Y-\widehat m_a(Q)\}.
\tag{1}
\]

Consistency and randomization given the full history imply

\[
\begin{aligned}
\mathbb E[\psi_a^Q\mid Q=q]
&=\widehat m_a(q)+
\frac{\mathbb E[\mu_a(H)\{m_a(H)-\widehat m_a(q)\}\mid q]}
{\bar\mu_a(q)}\\
&=\mathbb E[m_a(H)\mid q]
+\frac{\operatorname{Cov}(\mu_a(H),m_a(H)\mid q)}{\bar\mu_a(q)}.
\end{aligned}
\tag{2}
\]

Thus quotient-only AIPW has conditional bias

\[
\boxed{B_a(q)=\operatorname{Cov}(\mu_a(H),m_a(H)\mid q)/\bar\mu_a(q).}
\tag{3}
\]

This exact identity is independent of the displayed nuisance value. It is zero under either strong branch:

1. **outcome sufficiency:** `m_a(H)=\bar m_a(Q)` almost surely;
2. **propensity sufficiency:** `\mu_a(H)=\bar\mu_a(Q)` almost surely.

Accidental zero covariance is weaker but not a stable structural guarantee. To preserve the usual two separate robustness branches for all laws in a declared class, the quotient/model class must be capable of representing the true action-specific outcome and behavior propensity. If the exact full-history propensity is logged and carried separately, the propensity branch can be restored, but that scalar sequence is an additional ledger and belongs in the state/information cost.

### Minimal witness

Let two equiprobable histories `h_0,h_1` share the same quotient. For action 1 set

\[
\mu_1(h_0)=3/4,\quad \mu_1(h_1)=1/4,
\qquad m_1(h_0)=1,\quad m_1(h_1)=0.
\]

Then `\bar\mu_1=1/2`, the target mean is `1/2`, but (2) gives `\mathbb E[\psi_1^Q\mid Q]=3/4` for every quotient-only nuisance. The bias `1/4` equals `(1/8)/(1/2)`. Full-history randomization remains valid; only the coarsening breaks the required conditional balance.

## 3. Sequential causal quotient

Let the target policy be `\pi_t(a\mid H_t)` and let

\[
G_t=\sum_{s=t}^{T}\gamma^{s-t}L_s,
\qquad
Q_t^\pi(H_t,a)=\mathbb E_\pi[G_t\mid H_t,A_t=a].
\]

A strong primitive sufficient condition for quotient-only sequential DR is that, for each `t` and action `a`, there exist quotient functions/kernels such that

\[
\begin{aligned}
\pi_t(a\mid H_t)&=\bar\pi_t(a\mid Q_t),\\
\mu_t(a\mid H_t)&=\bar\mu_t(a\mid Q_t),\\
\mathbb E[L_t\mid H_t,A_t=a]&=\bar r_t(Q_t,a),\\
\Pr(Q_{t+1}\in B\mid H_t,A_t=a)&=\bar P_t(B\mid Q_t,a)
\quad\text{for all measurable }B.
\end{aligned}
\tag{4}
\]

Together with consistency, sequential exchangeability, integrability, and target support

\[
\bar\pi_t(a\mid q)>0\Longrightarrow\bar\mu_t(a\mid q)>0,
\tag{5}
\]

(4) makes the quotient a controlled Markov abstraction for the declared loss and policies. Backward induction then gives

\[
Q_t^\pi(H_t,a)=\bar Q_t^\pi(Q_t,a),
\tag{6}
\]

so the full-history sequential DR identity descends to `Q_t` with exact ratios `\bar\pi_t/\bar\mu_t`.

These primitive conditions are sufficient, not claimed necessary. Estimator-specific weaker conditions exist: exact full-history ratios may be retained in a side ledger; an exact quotient action-value can supply the outcome branch; marginalized ratios can replace trajectory ratios under their own state-distribution conditions. What cannot be done is silently discard all of these objects and inherit the full-history proof.

### Recursive failure witness

Take two histories with the same `Q_t`, identical current loss and identical action propensities. Under one action, let their next-quotient laws differ and let the target continuation earn loss only in one next cell. Current outcome/propensity checks pass, but `Q_t^\pi` differs between the two histories. Hence a current-step sufficient readout is not a sequential sufficient state; action-conditioned transition closure is indispensable unless the future value itself is retained exactly.

## 4. Delta right-quotient specialization

Write the Delta memory perturbation as `X\in\mathbb R^{d_k\times d_v}` and choose an orthonormal `W\in\mathbb R^{d_v\times r}`. Retain

\[
\mathcal L_W(X)=XW,
\tag{7}
\]

along with every non-memory recurrent component explicitly included in the proposed quotient. The discarded tangent fiber is `\{E:EW=0\}`.

For any differentiable scalar object `f(X)`—a positive-action log behavior propensity, positive-action log target propensity, immediate conditional loss, action value, or recursively transported future credit—write its Frobenius covector as `C_f`. At a zero-probability boundary use the probability/logit itself rather than its log, and omit target-inactive actions:

\[
Df(X)[E]=\langle C_f,E\rangle_F.
\]

Local first-order factorization through `XW` holds iff

\[
\boxed{C_f=C_fWW^\top.}
\tag{8}
\]

Indeed, (8) annihilates every `E` with `EW=0`; conversely, a component `C_f(I-WW^\top)\ne0` supplies a discarded perturbation that changes `f` while leaving `XW` fixed.

For a **fixed declared finite family** of local scalar observables, the quotient must therefore cover the joint row span of:

- behavior-policy log-propensity covectors;
- target-policy log-propensity covectors;
- declared loss/action-value covectors;
- covectors produced by transporting declared future-value sensitivities through the complete coupled-state Jacobian;
- declared scalar test functions or moments of the action-conditioned next-quotient law.

Let this fixed family's joint row space have dimension `r_F`. Within fixed right quotients and ambient perturbations, every exact local quotient representing that family has width at least

\[
\boxed{r\ge r_F.}
\tag{9}
\]

Adding policy or transition observables to the **same fixed scalar family** cannot shrink its row-span lower bound and can make it strictly larger than its outcome-only subfamily. This is not a universal dimension comparison with R18's full joint-state quotient.

Equation (9) is a lower bound, not an existence/equality theorem. When next-quotient observables themselves depend on `W`, recursive closure is an invariant-subspace/fixed-point problem: a proposed `W` changes the scalarized transition objects whose covectors it must contain. A finite collection of moment/Jacobian tests also does not certify equality of stochastic kernels in (4); that requires all relevant measurable test functions or a separately justified parametric kernel family.

In a minimax formal class that permits, after any rank-`r<d_v` right quotient has been fixed, a lawful behavior/target logit or future scalar credit with arbitrary rank-one covector, choose `a\in\ker W^\top` and covector `ua^\top`. Two states share `XW` but have different propensities or values. Hence no sub-full fixed right quotient is uniformly exact over that class. This quantifier order does not prove that native language-model policies realize every witness.

Equation (8) is only a local tangent certificate. Exact nonlinear compression requires constancy on complete quotient fibers and forward invariance under every allowed action/input, as in R18's global congruence condition. Discrete routing switches and disconnected fibers are not certified by one Jacobian.

## 5. Information, state, and compute accounting

- The memory quotient costs `d_k r` real coordinates per retained matrix state, plus side recurrent state and the description/update of `W`.
- Retaining exact per-step behavior and target propensity scalars instead of policy factorization costs `O(T)` offline log storage per trajectory; online evaluation can maintain a cumulative ratio with an `O(1)` scalar accumulator when the estimator permits. These are analysis information/storage costs rather than recurrent model-state coordinates, and neither makes `Q_t` Markov.
- Learning transition/reward/value models on the quotient adds their parameter and inference cost. Verifying exact closure can require full-history comparisons or matrix-free JVP/VJP coverage of all threatened directions.
- Product ratios can still have exponential horizon variance. State compression may reduce nuisance complexity, but it can also reduce overlap, introduce bias, or erase rare action-relevant distinctions. No variance/sample advantage follows from dimension reduction alone.
- A direct recurrent Q/policy predictor, full logged history with sequential DR, marginalized-ratio OPE, or an explicit protected-value/propensity ledger are same-information controls. Any claimed savings must count all side state and source/continuation processing.

## 6. Old counterexample recheck and new failure boundaries

R02 v1's passive-observation no-go, lack of individual counterfactual signs, delayed-outcome MAR requirement, persistent-stream dependence, mediation, noncompliance, and horizon reversal all remain. Compression does not repair them.

Additional boundaries are:

1. **Within-cell confounding:** equation (3) is nonzero.
2. **Policy aliasing:** target or behavior probabilities vary inside a quotient cell, so quotient-only ratios are wrong.
3. **Transition aliasing:** current loss and policies factor, but the next quotient law does not.
4. **Support collapse:** aggregation hides a target-reachable action with zero behavior support in part of a cell.
5. **Ledger laundering:** exact ratios are retained externally but omitted from the advertised state/cost.
6. **Local/global gap:** all quotient Jacobian tests pass at a point while finite states in one fiber have different policies or returns.
7. **Full-width formal class:** after any sub-full fixed `W`, an allowed arbitrary rank-one policy/value covector supplies a distinguishing witness; native realizability remains unproved.

## 7. Distinguishing predictions, falsifiers, and measurement

Conditional predictions:

1. Quotient-only AIPW error should track the empirical within-cell propensity–outcome covariance from (3), not merely quotient reconstruction error.
2. Adding exact propensity coordinates can remove the one-step bias branch while leaving transition-aliasing error at longer horizons.
3. A quotient passing current-loss tests but failing action-conditioned next-quotient tests should agree at horizon one and diverge at longer horizons.
4. For a fixed declared scalar family, the joint transported causal-covector rank is a lower bound on local right-quotient width and can exceed the outcome-only subfamily rank; equality additionally requires a recursively closed quotient construction.

Falsifiers include a claimed exact quotient with a nonzero discarded policy/value covector, a pair of equal quotient states with different action-conditioned next-quotient law, or a state/cost advantage that disappears after charging ratio ledgers and transition/value models.

Open Bandit Pipeline-style logged bandit data can test generic one-step AIPW and abstraction bias, but it does not instantiate coupled Delta memory. LongMemEval, bAbI and LAMBADA measure endpoints and do not natively expose randomized Delta actions, propensities, quotient fibers, or both potential outcomes. No native benchmark reviewed here jointly measures the theorem and the proposed Delta compression; this remains a measurement gap, not a negative empirical result.

## 8. Closest work and disposition

Hao et al. (arXiv:2406.19531v3) directly study state abstraction for OPE. They define target-policy irrelevance, Markov state abstraction, behavior-policy/backward-transition irrelevance (including history-dependent behavior policies), and Fisher consistency of value, sequential/marginalized-IS and doubly robust estimators on abstract states. Li et al. (2006), Allen et al. (2021), MDP homomorphism/bisimulation, Jiang–Li sequential DR, MIS, and STAR are further strong controls. R18 already supplies this packet's full joint recursive quotient/fiber conditions.

The remaining Delta-specific content is the translation of these obligations into the fixed right quotient `XW`, the joint transported-covector width (9), and the explicit warning that propensity/value ledgers must be charged. That is a useful debug theorem and design screen, but not a substantively distinct updater or a proved state/sample/compute advantage.

Disposition: **mathematics conditionally supported; major functional collision; candidate delta zero; empirical effect unknown.** Reopen the final attempt only with a prefix-checkable Delta causal quotient plus a proved matched-information total-cost/statistical advantage over full-history/ratio-ledger DR, direct recurrent Q/policy prediction, recent OPE abstractions, and R18. Otherwise keep R02 as the randomized-action causal control.

No project code, tests, model execution, benchmark scoring, training, inference, data/model download, GPU work, paid service, or Docker was used.

