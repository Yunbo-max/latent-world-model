# R07 v2 — complete-state finite-horizon directional action margin

Status: **conditional local theorem/debugging control; parked after attempt 2/3, not an active D candidate**. This versioned child of `R07_VALIDITY_TO_ACTION_MARGIN.v1.md` repairs the frozen-reference-path omission by differentiating a complete recurrent state through a declared finite suffix. It preserves the v1 truth/action counterexample and signed protection term. It does **not** identify a free-running causal effect, provide a prefix oracle, prove a novel updater, or establish empirical benefit.

## 1. Original problem, failure type and concrete patch

R07 v1 uses the exact surrogate

\[
\Delta_Y(a)=2a(c-Yb)+a^2h_Y
\]

for a fixed collection of linearized probes. That algebra is correct, but it cannot be silently promoted to a recurrent action value. A write can change future memory, updater state, gates, keys, routes, predictions and later losses. The failure type is **target/construction mismatch**: fixed-reference coefficients were being asked to answer a coupled-state question.

The patch keeps a scalar action `a` but expands the state and differentiates the complete declared suffix. Let

\[
x_0(a)=x^-+ad,\qquad
d=(\operatorname{vec}(U),0,\ldots,0),\qquad
U=\beta k e^\top,\qquad e=v-(S^-)^\top k,
\tag{1}
\]

where `x` contains `vec(S)` and every updater, router, belief, previous-action, pending-feedback and other recurrent coordinate needed by the future transition. The proposal `U` is fixed at action time; if it is recomputed as `a` changes, its derivatives must instead enter the action transition below.

For a fixed future policy and a common exogenous suffix `xi_1:H`, define

\[
x_{j+1}(a)=F_j(x_j(a),\xi_{j+1}),\qquad
J_Y(a)=r_Y(a)+\sum_{j=0}^{H-1}\ell_{Y,j}(x_j(a))+\phi_Y(x_H(a)).
\tag{2}
\]

`Y` may switch a declared new-target loss on or off, but it remains distinct from action utility. A future observed truth label can train or audit (2); it cannot be read before the action unless already in the filtration.

## 2. Exact first directional derivative on the declared suffix

Assume the displayed maps are twice continuously differentiable along the no-write path `a=0`. Write

\[
A_j=D_xF_j(x_j(0),\xi_{j+1}),\qquad
z_j=\left.\frac{d x_j(a)}{da}\right|_{a=0}.
\]

Because the injection (1) is affine,

\[
z_0=d,\qquad z_{j+1}=A_jz_j.
\tag{3}
\]

Let \(g_j=\nabla \ell_{Y,j}(x_j(0))\), \(g_H=\nabla \phi_Y(x_H(0))\), and define the costate

\[
\lambda_H=g_H,\qquad
\lambda_j=g_j+A_j^\top\lambda_{j+1}.
\tag{4}
\]

Then forward and reverse forms agree:

\[
\boxed{J_Y'(0)=r_Y'(0)+\sum_{j=0}^{H-1}g_j^\top z_j+g_H^\top z_H
=r_Y'(0)+\lambda_0^\top d.}
\tag{5}
\]

For a memory-only injection, reshape the memory block of `lambda_0` as `G_{S,Y}`. The Delta specialization is

\[
\lambda_0^\top d
=\langle G_{S,Y},\beta k e^\top\rangle_F
=\beta k^\top G_{S,Y}e.
\tag{6}
\]

This is a structured contraction, not a cheap oracle: computing `G_{S,Y}` still requires the complete suffix costate or a separately calibrated predictor.

If the action enters later transitions explicitly, `F_j=F_j(x_j,a,xi)`, equation (3) must be replaced by `z_{j+1}=F_{x,j}z_j+F_{a,j}`. Omitting that term is another frozen-action error.

## 3. Exact second directional derivative and the term frozen analysis loses

Let

\[
w_j=\left.\frac{d^2x_j(a)}{da^2}\right|_{a=0}.
\]

For the affine initial injection and action-independent suffix transition,

\[
w_0=0,\qquad
w_{j+1}=A_jw_j+D_x^2F_j[z_j,z_j].
\tag{7}
\]

Thus

\[
\boxed{
J_Y''(0)=r_Y''(0)+
\sum_{j=0}^{H-1}
\left(z_j^\top H_{\ell,j}z_j+g_j^\top w_j\right)
+z_H^\top H_\phi z_H+g_H^\top w_H.}
\tag{8}
\]

An equivalent reverse recursion is

\[
K_H=H_\phi,
\]

\[
K_j=H_{\ell,j}+A_j^\top K_{j+1}A_j
+\sum_i(\lambda_{j+1})_i\,H_{F_j^{(i)}},
\tag{9}
\]

which gives

\[
J_Y''(0)=r_Y''(0)+d^\top K_0d.
\tag{10}
\]

The last sum in (9) is the second derivative of the dynamics weighted by the next costate. A frozen-feature or Gauss--Newton/iLQR approximation can drop it; a full DDP/exact-Hessian calculation cannot. If `F` depends explicitly on `a`, equation (7) also needs `2F_{xa,j}z_j+F_{aa,j}`.

No positive-semidefinite claim follows for (8). The complete directional curvature can be positive, zero or negative, even when each pointwise squared loss has a positive-semidefinite Gauss--Newton term.

## 4. Safe local gate and exact reduction to R07 v1

Define the coupled finite-horizon local margin

\[
q_{Y,H}=-\frac12J_Y'(0),\qquad
h_{Y,H}=\frac12J_Y''(0).
\tag{11}
\]

If the third-order remainder obeys, simultaneously on the entire segment under consideration,

\[
J_Y(a)-J_Y(0)=-2q_{Y,H}a+h_{Y,H}a^2+R_{Y,H}(a),
\qquad |R_{Y,H}(a)|\le \frac{\kappa_{Y,H}}6a^3,
\tag{12}
\]

then simultaneous action-time-valid bounds

\[
q_{Y,H}\ge\underline q>0,\qquad
h_{Y,H}\le\overline h,\qquad
\kappa_{Y,H}\le\overline\kappa
\]

certify improvement of any `a in (0,1]` satisfying

\[
\boxed{2\underline q>a\overline h+\frac{a^2\overline\kappa}{6}.}
\tag{13}
\]

This direct inequality is valid even when `overline h` is negative. It avoids importing the convex `h>=0` branch from v1 into an indefinite coupled Hessian.

With zero remainder, `J'(0)<0` iff `q>0`. Hence if `q>0`, every sufficiently small positive step improves; if `q<0`, every sufficiently small positive step hurts. At the boundary `q=0`, the quadratic term decides: positive small steps improve iff `h<0`, tie when `h=0`, and hurt when `h>0`. The v1 iff statement relied on `h>=0`. Full write beats no-write iff `q>h/2`, for any sign of `h`. When `h>0`, the quadratic's continuous minimizer is `clip(q/h,0,1)` and full write is the continuous optimum iff `q>=h`. When `h<=0`, the quadratic is linear/concave and its minimum over `[0,1]` is at an endpoint; full write is chosen iff `h-2q<0`, with ties assigned to no-write.

In the v1 affine fixed-reference quadratic, `J'(0)=2(c-Yb)` and `J''(0)=2h_Y`, so (11)--(13) reduce exactly to its thresholds. Nothing in v1 is invalidated.

## 5. Old counterexamples and new failure boundaries

1. **Truth is still not action utility.** Two worlds can share `Y,b` and pointwise curvature but differ in signed protected cross loss or continuation cost, producing opposite actions.
2. **Dynamics curvature matters.** Let `x_0(a)=1+a`, `F(x)=x^2`, terminal loss `phi(y)=y`, and immediate action cost `r(a)=-2.5a`. Then `J(a)-J(0)=-0.5a+a^2`: an infinitesimal write helps but the full write hurts. Dropping `lambda F''` predicts only the misleading linear gain.
3. **Memory-only state can be wrong.** A write may leave the current readout unchanged but set a hidden updater/router coordinate that changes terminal loss. A derivative that tracks only `S` reports zero while the complete-state derivative is nonzero.
4. **Finite horizon can reverse later.** An `H`-step benefit can be overturned by a loss at `H+1`; a longer-horizon claim needs a valid discounted closed-loop tail bound, not a verbal appeal to stability.
5. **Indefinite curvature changes the branch logic.** For `Delta(a)=a-2a^2`, small steps hurt while the full action helps. Positive-semidefinite quadratic formulas cannot be reused without checking the complete Hessian.
6. **Discrete routes are nonsmooth.** Argmax, top-k routing and token sampling can have zero pathwise derivative almost everywhere yet change under a finite gate. Taylor certificates do not cross such boundaries.
7. **Multiple writes interact.** For an action vector, the Hessian has cross terms; adding independently computed scalar margins is generally wrong.
8. **Future policy optimization is different.** Equations (2)--(13) evaluate a fixed declared future policy/path. If later actions are reoptimized, the correct object is a Bellman `Q`; policy switches can make the value nonsmooth. Adding a separate continuation correction after already including the full suffix would double count it.
9. **No overlap, no causal free-running comparison.** If the action changes user/environment feedback or discrete future-token laws, a common-path derivative is not an identified total action effect without a reparameterized model, branch summation, randomization/OPE and overlap.

A minimal distributional sign reversal is: the common good path has cost `-epsilon a`, but the action makes a bad branch of cost `C` occur with probability `a`. The teacher-forced derivative is `-epsilon`; the expected free-running derivative is `C-epsilon`, which has the opposite sign when `C>epsilon`.

## 6. Distribution-sensitive derivative and information boundary

If an action-dependent trajectory law `p_a(tau)` is dominated by a common measure, has action-independent support, is differentiable, and permits differentiation under the integral, with total path loss `L(a,tau)` and score `s=partial_a log p_a(tau)`, then formally

\[
J'(a)=E_a[L_a+Ls],
\tag{14}
\]

\[
J''(a)=E_a[L_{aa}+2L_as+L(s^2+\partial_a^2\log p_a)].
\tag{15}
\]

A lawful common-noise reparameterization may absorb these terms into pathwise derivatives. Discrete sampling or environment response generally cannot be repaired by pretending the score terms are zero. Estimating (14)--(15) can have high variance and reopens R02/R03's randomization, OPE and free-running-law obligations.

Deployment-time use of (13) requires `underline q, overline h, overline kappa` and any tail bound to be measurable before the action and simultaneously calibrated. Computing them from the realized future is a retrospective diagnosis, not an online gate. A future truth label or a model-generated suffix is not new external evidence.

## 7. Computation, state and strongest simple alternatives

For one scalar action, (3) needs one forward JVP chain; (4)--(6) need a reverse VJP/costate chain; (7)--(10) need a directional second-order pass or Hessian-vector/forward-over-reverse calculation. Dense `K_j` need not be materialized, but activations must be stored or recomputed. With full feedback the initially rank-one memory tangent generally becomes dense across the joint state. Rank-one Delta therefore does not by itself prove lower asymptotic total cost than ordinary automatic differentiation.

Strong same-information controls are: no-write; standard Delta; R07 v1's fixed-reference gate; paired suffix rollout; a direct conditional action-value/advantage predictor; reverse VJP/BPTT with checkpointing; forward JVP/RTRL/e-prop-style sensitivity; DDP/exact-Hessian and iLQR/Gauss--Newton approximations; R08's Bellman/POMDP continuation object; and randomized sequential OPE when the action changes future laws. R07 v2 has value only as an auditable decomposition or rejection certificate if its prefix estimates are demonstrably cheaper or better calibrated than these controls. That advantage is not established.

## 8. Predictions, measurement and disposition

Conditional predictions, not results:

1. When future gates/keys/routes are state-dependent, the complete derivative will disagree with the frozen-reference coefficient exactly through omitted state paths and dynamics curvature.
2. Relative to the stated exact-cost-Hessian iLQR/Gauss--Newton approximation, the omitted curvature is sourced by the propagated costate-weighted `D^2F` contractions in (9), subject to cancellation across time and coordinates.
3. Fixed-policy finite-horizon gains will fail to predict free-running effects when action-dependent branching or omitted tail loss dominates.
4. A direct action-value predictor that matches or beats the decomposed certificate at equal information/state/compute removes the claimed practical need.

AToKe supplies time-conditioned old/current facts; SEAL supplies continual self-edit outcomes; CounterFact/ROME and KnowEdit/EasyEdit supply edit efficacy/generalization/locality endpoints. None of the pinned native interfaces jointly exposes pre-action complete-state tangents, exact directional Hessian, simultaneous remainder/tail bounds, randomized action propensity and paired free-running potential outcomes. They can test endpoint consequences only. The missing joint object is a measurement gap, not a negative experiment, and no data, label, metric, case, scorer or result is invented here.

The repair is mathematically useful but functionally collides with adjoint sensitivity, automatic differentiation, DDP/iLQR and Bellman policy evaluation. Its Delta-specific residue is equation (6), a rank-one initial contraction; the continuation computation remains general. Counts stay **5 historical / 0 active / 0 scientifically admitted / 0 selected**. Empirical effect is unknown and no code or experiment was run.

Reopen for attempt 3 only if at least one of these becomes available:

1. a lawful prefix-only estimator of `q,h,kappa` and the horizon tail with a proved same-information total-cost or calibration advantage over a direct action-value predictor;
2. a Delta-specific structural theorem that computes the complete directional margin with materially less state/compute than general JVP/VJP/DDP/RTRL;
3. a native randomized causal object joining old/new validity, pre-action margins, propensities and identifiable free-running action outcomes.
