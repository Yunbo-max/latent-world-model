# R15 v1 — finite-action intervention rank for Delta update credit

Status: **conditional identifiability/lower-bound control; parked, not an active D candidate**. This is a versioned theorem child of `rejected/COUNTERFACTUAL_QUERY_WRITE_UTILITY.md`, screened in `R15_REPAIR_LINE_SCREEN.md`. It repairs an imprecise finite-probe idea by stating exactly which causal action values and response coefficients can be identified. The estimator/mechanism is already covered by R02 and generic experimental design/OPE; no candidate uplift follows.

## 1. Original problem, patch, and information boundary

Let the complete augmented pre-action state be `x in R^n`, including Delta memory, updater state, pending feedback, and any state needed by the declared continuation. A current action coordinate `z in R^r` changes the next state by

\[
x^+(z)=x^+(0)+Bz,\qquad B\in\mathbb R^{n\times r}.
\]

For a fixed key and freely chosen value-amplitude vector, the memory block has \(n_S=d_kd_v\) and

\[
B_S=I_{d_v}\otimes k\in\mathbb R^{d_kd_v\times d_v}.
\]

If the action changes no other immediate state, the augmented injection is \(B=[B_S^\top,0^\top]^\top\in\mathbb R^{n\times d_v}\).

Let \(\mathcal F\) be the actual causal prefix and logged pre-action randomness. Let \(Y(z)\) be a scalar delayed loss obtained after executing `z` and then following one fully specified continuation policy for a declared horizon. Deployment may not observe future tokens, answers, old-fact validity, ideal edits, or counterfactual environment responses.

The parent failed because one factual branch does not determine an unchosen branch. R15's patch is deliberately narrower: randomize over declared action coordinates and, only when stated, assume the conditional mean is exactly linear or quadratic in those coordinates. Low-dimensional injection alone is not such an assumption.

## 2. Causal support theorem and no-interpolation counterexample

Assume consistency, conditional randomization

\[
Z\perp\{Y(z):z\in\mathcal A\}\mid\mathcal F,
\]

positive logged propensity on every action being compared, lawful reset units or dependence-aware inference, branch-consistent real outcomes, and correct treatment of delay/censoring. Then \(\mu(z,\mathcal F)=\mathbb E[Y(z)\mid\mathcal F]\) is identified on the randomized support. HT/AIPW or, under changed later policies, sequential DR/OPE are the generic estimators already written in R02.

Finite \(r\) does not identify unseen actions. Even for \(r=1\), a deterministic logger with `Z=0` cannot distinguish

\[
\mu_0(z)=0,\qquad \mu_1(z)=cz,
\]

because both agree on the observed action and disagree on any untried write. Thus the action subspace reduces the domain; it does not create counterfactual evidence or justify interpolation.

## 3. Exact response-surface rank theorem

Add the explicit structural model

\[
\mathbb E[Y\mid\mathcal F,z]
=\alpha+b^\top z+\frac12 z^\top H z,
\qquad H=H^\top.
\tag{1}
\]

Let `svec` contain the independent symmetric entries with whatever fixed scaling makes its dot product reproduce the quadratic term, and define

\[
\phi(z)=\bigl(1,z,\operatorname{svec}(zz^\top)\bigr),
\qquad q=1+r+\frac{r(r+1)}2.
\tag{2}
\]

Writing (1) as \(\theta^\top\phi(z)\), define the conditional design Gram

\[
G(\mathcal F)=\mathbb E[\phi(Z)\phi(Z)^\top\mid\mathcal F].
\tag{3}
\]

**Theorem.** Under the exact model and \(\mathbb E[\|\phi(Z)\|^2+Y^2\mid\mathcal F]<\infty\), the full conditional coefficient vector is identified iff `G(F)` has rank `q`. These moments are automatic for bounded finite action support and bounded outcomes. If the intercept is known independently, or canceled by observing lawful paired differences, delete the intercept column and require rank

\[
r+\frac{r(r+1)}2.
\tag{4}
\]

Sufficiency follows from the conditional normal equations. For necessity, if `d` is nonzero in `ker G`, then

\[
\mathbb E[(d^\top\phi(Z))^2\mid\mathcal F]=d^\top Gd=0,
\]

so \(\theta\) and \(\theta+d\) agree almost surely on the logging support. Whenever an alternative \(z_*\) has \(d^\top\phi(z_*)\ne0\), the two observationally identical worlds assign it different loss. No estimator can identify that extrapolated value from this log.

For a linear response with known baseline, identification reduces to

\[
\operatorname{rank}\mathbb E[ZZ^\top\mid\mathcal F]=r.
\tag{5}
\]

For an arbitrary quadratic response, at least `q` independent feature rows are required, hence at least `q` action levels when the intercept is unknown. In the scalar gate case, a known baseline plus two distinct nonzero amplitudes can identify slope and curvature. Binary write/no-write identifies only one endpoint contrast; it cannot separate slope, curvature, or the optimal fractional gate and cannot discover a new write direction.

This theorem is more precise than counting arms alone: repeated actions do not repair rank deficiency, and a formally sufficient number of nearly collinear feature rows can be statistically unusable.

## 4. Conditioning and finite-budget price

Within a fixed \(\mathcal F\) stratum, or under a correctly specified shared parametric model across \(\mathcal F\), assume homoskedastic Gaussian noise with variance \(\sigma^2\) and `N` independent/reset observations from the stated random design. The Fisher information is \(NG/\sigma^2\). For an identified query action,

\[
\operatorname{Var}\{\widehat\mu(z)\}
\ge \frac{\sigma^2}{N}\phi(z)^\top G^{-1}\phi(z)
\tag{6}
\]

for regular unbiased estimation in the exact linear model. Small action dimension reduces coefficient count, but a poorly conditioned design still consumes the sample budget. Maintaining a dense empirical Gram/inverse costs `O(q^2)` state and generic dense updates cost `O(q^2)` per observation; direct finite-arm means are cheaper when only the logged arms matter. Standard D/G-optimal response-surface design is therefore a required strong control.

## 5. Fixed-suffix replay, free-running effect, and meta-gradient

A cloned state replayed under an identical recorded/teacher-forced post-action suffix \(\xi\) computes the controlled contrast

\[
L(z;\xi)-L(0;\xi).
\tag{7}
\]

It is not the free-running total effect if the action changes future tokens, queries, retrieval, feedback, or later policies. A minimal example sets the post-action state `x=z`, lets the action-generated future token be `T=z`, and uses loss `(x-T)^2`. Both free-running actions have zero loss, while teacher-forcing the baseline suffix `T=0` assigns loss `z^2` to the write. Fixing an action descendant changes the estimand.

By contrast, common-random-number pairing may hold only genuinely exogenous noise fixed while allowing each branch to generate its own endogenous tokens, queries, and feedback. When a lawful simulator/environment supplies both branch-consistent marginals, that design can estimate a paired free-running total effect. It is invalid to reuse the factual branch's post-action response in the counterfactual branch merely because both began from the same state.

For a write-local parameter and fixed suffix, the baseline branch is parameter-independent, so the gradient of (7) is just the ordinary future-loss gradient. Paired replay can reduce variance or validate a candidate, but it is not a novel training signal.

Likewise, the one-time action gradient

\[
g_z=B^\top\lambda^+
\tag{8}
\]

does not identify a shared updater's meta-gradient. Shared parameters alter actions at many future states and can alter the trajectory law; their gradient includes all action-path derivatives, state/initialization terms, and—when the distribution is parameter-dependent—score/distribution terms. Finite current-action regression cannot replace those objects without additional interventions or a correct full model.

## 6. Old counterexamples and new failure boundaries

The parent counterexample survives outside randomized support. Additional exact boundaries are:

1. **No overlap.** If only write is logged, worlds with the same `Y(1)` and arbitrary `Y(0)` are observationally identical.
2. **Hidden assignment.** If an unrecorded variable selects the action, identical `(A,Y)` laws can represent a true action effect or pure confounding. Randomization must be conditional on the recorded filtration.
3. **Individual signs.** Randomized arm marginals identify population contrasts, not the coupling of both potential outcomes for one historical write.
4. **Horizon reversal.** Two systems may agree for every action through `H` and reverse at `H+1`. With `|ell|<=L` and discounted convention `sum gamma^(h-1) ell_h`, only the action-difference tail bound `2L gamma^H/(1-gamma)` follows.
5. **Cross-world feedback.** Reusing the factual user's, tool's, or environment's response in a counterfactual branch is invalid unless it is genuinely exogenous to the action.
6. **Sequential support.** Randomizing only the initial action identifies its induced trajectory under one common later policy. Evaluating a different later policy requires sequential positivity/OPE; worst-case importance weights can grow as `epsilon^(-H)`.
7. **Branch cost.** One-time `K`-arm replay costs `O(KH)` forward work plus complete-state snapshots. Enumerating arbitrary binary interventions at every one of `H` decisions has `2^H` branches absent additional structure.

## 7. Nearest work, controls, measurement, and disposition

The required same-information controls are randomized arm means, HT/AIPW, sequential DR/OPE, lawful paired replay, ordinary future CE/autodiff, a direct Q/action predictor, and standard linear/quadratic response-surface optimal design. TTT Ouroboros already supplies Fixed Generation, Recorded Replay, paired one-update analysis, and delayed real-data Settlement in an author implementation; R02 already records finite randomized Delta actions, propensities, AIPW, sequential DR, horizon reversal, and paired replay.

This packet also preserves a decisive internal collision: `STEP2_PROJECTED_DELAYED_CREDIT.md` already contains \(B=I\otimes k\), \(B^\top\lambda\), action-span summary lower bounds, the scalar paired-baseline quadratic model, the conditional Gram-rank criterion, the baseline-plus-two-nonzero-level requirement, binary endpoint nonidentifiability, finite-horizon/free-running counterexamples, OPE support, and the Ouroboros collision. `STEP2_RECURSIVE_RANDOM_METRIC_CONTROL.md` separately covers action-space Hessian/GGN pullbacks and fixed-suffix/free-running mismatch. R15 therefore consolidates and generalizes those controls to an explicit multivariate response-surface theorem; it does not claim the rank idea as a newly discovered residual mechanism.

bAbI, LAMBADA, RULER, and LongMemEval measure endpoint behavior but do not natively expose randomized Delta actions, propensities, both branch-consistent outcomes, or response-surface coefficients. Agent environments can provide outcomes, but lawful paired branches require reset/simulator semantics and matched feedback/branch cost. No benchmark, label, metric, or result is invented here.

**Disposition:** the exact intervention-rank theorem and its conditioning/cost boundary pass as a useful control. They do not define a new updater and are generic experimental-design mathematics. R15 is parked after substantive attempt 1, contributes zero active/admitted/selected candidates, and may reopen only if full coupled/free-running Delta dynamics imply a verifiable exact low-order/low-rank response law or a same-information, same-support, matched-budget advantage over direct response/Q estimation. Empirical effect remains unknown.
