# R08 v1 — Temporal-validity release with action margins

Status: **conditional theory/control; parked, not a candidate**  
Parent lineage: `rejected/REVISION_EVIDENCE_POSTERIOR_EDIT.md`, `rejected/MARTINGALE_RELEASE_CONTROL.md`, and `repairs/R07_VALIDITY_TO_ACTION_MARGIN.v1.md`  
Scope: mathematical/source review only; no model execution, training, inference, scoring, or benchmark dispatch.

## 1. Problem and the failed step

The old line estimated whether an old fact is still valid and then used that posterior, or a sequential evidence threshold, as if it were the sign of a release/write decision. That implication is false. A validity posterior describes a hidden state; an action must instead minimize loss after accounting for Delta interference, protection geometry, future information, and state changes.

The repair does not delete the old counterexamples. It asks the narrower question:

> Under what explicit conditions can temporal validity be converted into a release/retain/query action, and when must the updater defer to a dynamic state-value calculation?

## 2. Formal object and information boundary

Let `V_t in {0,1}` mean that the old fact is still valid (`1`) or obsolete (`0`). The pre-action filtration is `F_t`, and

`p_t = P(V_t=1 | F_t)`.

For a general two-state transition with `s_1=P(V_t=1|V_{t-1}=1)` and `s_0=P(V_t=1|V_{t-1}=0)`, the prediction step is

`p_t^- = s_1 p_{t-1} + s_0(1-p_{t-1})`.

For an absorbing obsolescence/revision prior with hazard `eta_t`, this reduces to

`p_t^- = (1-eta_t) p_{t-1}`.

Given an action-independent observation `Z_t` with declared likelihoods `g_v(z)=p(Z_t=z | V_t=v,F_{t-1})`, the Bayes update is

`p_t = p_t^- g_1(Z_t) / [p_t^- g_1(Z_t) + (1-p_t^-) g_0(Z_t)]`.

This filter is meaningful only if the likelihood conditions include any selection/action mechanism that changes which observations arrive. A same-write action `a_t` must be `F_t`-measurable. A later label can train a policy offline or affect a later action, but cannot retroactively gate `a_t`.

## 3. Patch: posterior plus signed action geometry

Let `a in [0,1]` denote release/write strength along a fixed Delta direction

`Delta S(a) = a beta k e^T`, with `S in R^{d_k x d_v}`.

Conditioned on `V=v`, use the fixed-reference R07 quadratic action increment

`D_v(a) = h_v a^2 - 2 q_v a`,

where `h_v >= 0` and `q_v = Yb_v-c_v` are fully contracted scalars. The posterior-weighted increment is

`D_p(a) = (1-p)D_0(a) + pD_1(a) = h(p)a^2 - 2q(p)a`,

with

`h(p)=(1-p)h_0+ph_1`,  `q(p)=(1-p)q_0+pq_1`.

Therefore, when `h(p)>0`,

`a*(p)=clip(q(p)/h(p),0,1)`.

The exact fixed-reference statements are:

- a beneficial positive infinitesimal step exists iff `q(p)>0`;
- full release beats retain/no-write iff `q(p)>h(p)/2`;
- full release is the constrained continuous optimum iff `q(p)>=h(p)`.

For binary full release versus retain,

`D(p)=D_p(1)=B+pA`,

where `B=h_0-2q_0` and `A=(h_1-h_0)-2(q_1-q_0)`. Release iff `D(p)<0`. Hence:

- if `A>0`, release iff `p < -B/A`;
- if `A<0`, release iff `p > -B/A`;
- if `A=0`, the action does not depend on `p`.

The intuitive rule “release when validity is low” occurs only when `D_0<0<D_1`. A posterior threshold is not unconditional.

This affine threshold is only for fixed binary/full actions. If release and protected directions each optimize their own continuous amplitude, their clipped quadratic values are piecewise rational functions of `p`; their comparison need not have one crossing.

## 4. Old counterexample revisited

Fix `p=0.2`, `Yb=1`, `h_0=h_1=1`, and `c_0=0`. Then `q_0=1`.

- World A: `c_1=1`, so `q_1=0`, `q(p)=0.8`, and `D_p(1)=-0.6`; full release is beneficial.
- World B: `c_1=6`, so `q_1=-5`, `q(p)=-0.2`, and `D_p(1)=1.4`; release is harmful.

The validity posterior and the nominal write signal are identical, while protection geometry changes the optimal action. Thus a `p`-only gate is not identified. A necessary-and-sufficient policy-level condition is that all histories with the same `p` share at least one Bayes-optimal action; a stronger sufficient condition is that branch losses depend on history only through `p`.

## 5. Robust endpoint certificate

Assume branch pairs `(q_v,h_v)` are fixed and `p` belongs to a sharp identified interval `[l,u]`. For fixed `a`, `D_p(a)` is affine in `p`, so

`max_{p in [l,u]} D_p(a) = max{D_l(a),D_u(a)}`.

The interval has a strict robust benefit exactly when this maximum is negative. In particular:

- some positive robust step exists iff `q(l)>0` and `q(u)>0`;
- full write is robust iff `min_{r in {l,u}} [q(r)-h(r)/2] > 0`.

A minimax `a` can be found by checking the endpoint quadratics' constrained minima, `a=0,1`, and their in-range intersection `a=2(q_l-q_u)/(h_l-h_u)` when defined. This endpoint statement is sharp only for a joint achievable set. Independently combining marginal confidence intervals is conservative and need not be sharp; simultaneous coverage and joint feasibility must be stated.

## 6. Query/defer value in the one-step problem

Let `L_R(p)` and `L_K(p)` be affine posterior risks for release and keep, and

`R(p)=min{L_R(p),L_K(p)}`.

`R` is concave. For an action-independent observation channel `j`, posterior `P'_j`, and cost `kappa_j`, the martingale property `E[P'_j | p]=p` and Jensen's inequality give

`VoI_j(p)=R(p)-E[R(P'_j)|p] >= 0`.

Query/defer is worthwhile in this one-step model iff `VoI_j(p)>kappa_j`. If all posterior realizations choose the same terminal action, `VoI_j=0`. This is ordinary Bayesian value of information specialized to the Delta action margin, not a new Delta mechanism.

## 7. Dynamic repair and failure of the myopic threshold

When an action changes memory, updater state, observation availability, or future cost, belief alone is generally not sufficient. Let

`z_t=(p_t,S_t,u_t,a_{t-1},r_t,...)`

contain all sufficient memory/updater/run-length variables. For binary release `a=1` and keep `a=0`, define the immediate release-minus-keep margin `delta_t(z)` and switching cost `kappa 1[a != a_{t-1}]`. The exact Bellman comparison is

`J_t(z)=min_a { L_t^a(z)+E[J_{t+1}(F_a(z,V,Z))] }`,

and release is preferred exactly when

`delta_t(z) + kappa(1-2a_{t-1}) + Gamma_t(z) < 0`,

where

`Gamma_t(z) = E[J_{t+1}(z') | z,a=1] - E[J_{t+1}(z') | z,a=0]`.

The R07/static threshold is exact only when the continuation difference is zero and no omitted state-dependent cost remains, or when a separately proved monotone-POMDP/optimal-stopping theorem supplies the threshold structure. If `|Gamma_t(z)|<=G`, then

- release is certified when `delta_t + switch + G < 0`;
- keep is certified when `delta_t + switch - G > 0`;
- otherwise defer or solve/approximate the dynamic program.

Two minimal failures remain:

1. **Information destruction.** At `p=1/2`, release has immediate gain `epsilon in (0,1/2)` but destroys the diagnostic signal; the terminal indistinguishability loss is `1/2`. Keeping yields a perfect next observation and zero terminal loss. Myopic release costs `1/2-epsilon>0`, while dynamic keep costs zero.
2. **Hysteresis.** With immediate release margin `-0.1` and switching cost `0.2`, the total margin is `-0.1+0.2(1-2a_{t-1})`: keep is optimal from `a_{t-1}=0`, release from `a_{t-1}=1`, at identical `p`.

## 8. Sequential evidence is not action utility

A nonnegative e-process can survive adaptive actions only relative to the actual filtration and only when, for every predictable action/selection rule,

`E[M_t | F_{t-1}] <= M_{t-1}`.

Its likelihood or test-martingale construction must condition on action-dependent missingness and feedback. Ville's inequality then controls an evidence event under the null “old fact remains valid”; it does not prove that release has positive utility. If `g_0=g_1`, evidence cannot move the posterior; only the hazard prior changes it.

## 9. Information, state, and computational cost

- A two-state action-independent filter is `O(1)` time/state per tracked item, plus retrieval/indexing.
- Exact Bayesian online change-point filtering over run length grows linearly with the data so far per step; pruning/truncation changes this to an approximation with an effective-run-length cost.
- The dynamic object is a POMDP over belief and Delta/updater state and can be much more expensive than the original update.
- Estimating `q_v,h_v` requires the signed protection/reference contractions from R07; their JVP/residual access may dominate a standard Delta write.
- A direct same-information predictor of conditional action advantage is the strongest simple alternative to “estimate validity, then map validity to action.”
- With multiple correlated protected facts, a joint belief can grow exponentially in their count and simultaneous writes add Hessian cross terms; independent per-fact filters are an extra approximation.

## 10. Native measurement and falsifiable predictions

AToKe provides supplied temporal transitions plus old/current QA and historical/current reliability-style scores. It can test whether a method preserves historical facts and applies current facts after a known edit. It does **not** natively identify observation likelihoods, hazards, query costs, Delta pre-action `(q,h)`, action propensities, paired write/no-write outcomes, or `Gamma_t`.

Predictions, not results:

- A calibrated validity posterior should still choose the wrong action when protection geometry flips `q` at fixed `p`.
- A myopic threshold should lose when release censors later evidence or creates large continuation cost.
- Robust endpoint abstention should concentrate on histories whose validity interval or action margin straddles zero.
- If a direct action-advantage predictor matches or beats the decomposed filter at equal information/state/compute, the temporal-validity decomposition has no independent practical value.

No existing native asset read in this phase measures all four claims; this is a measurement gap, not an experimental failure.

## 11. Nearest-work and disposition

The repaired mathematics is a specialization of cost-sensitive Bayes decisions, Bayesian online change-point filtering, value of information, sequential evidence, and POMDP/quickest-change control. Temporal model editing already supplies time-conditioned old/new facts and routing objectives. The residual contribution here is the explicit bridge from a temporal-validity belief to R07's signed Delta action margin, its exact endpoint certificate, and the Bellman correction that shows when the bridge is insufficient.

This is useful theory/control but not currently a distinct method candidate. Counts remain 5 historical, 0 active, 0 scientifically admitted, 0 selected. Empirical effect is unknown.

Reopen only if at least one of the following is supplied:

1. a prefix-only sufficient statistic for `(p,q,h,Gamma)` with a proved same-budget advantage over a direct action-advantage predictor;
2. a Delta-specific structural theorem that makes `Gamma` or the optimal threshold computable with materially less state than the general POMDP/change-point baseline;
3. a native causal object with old/new validity, pre-action margins, randomized propensities, and paired/identifiable action outcomes.
