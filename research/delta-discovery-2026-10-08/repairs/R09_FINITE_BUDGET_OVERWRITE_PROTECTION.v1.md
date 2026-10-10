# R09 v1 — Finite-budget overwrite–protection Pareto certificate

Status: **conditional theory/control; parked, not a candidate**  
Parent lineage: `rejected/NOGO_CAP_02.md`, `rejected/IDENTIFIABILITY_PROJECTION_BOUNDARY.md`, and `rejected/RANK_REVEALING_CONSTRAINT_DELTA.md`  
Scope: mathematical/source review only; no model execution, training, inference, scoring, benchmark dispatch, or model/data download.

## 1. Original problem and concrete patch

The parent results proved two hard boundaries: exact overwrite makes the affine old-state path singular, and exact protection of a query span becomes infeasible or has norm proportional to `1/rho` when the new key approaches that span. Those statements are correct, but they leave the useful approximate regime unresolved. Treating “exactly protect and overwrite” versus “do nothing” as the only choices is a target mismatch.

This child keeps every old counterexample and asks a narrower question:

> At fixed causal information and a fixed desired correction fraction, what is the sharp tradeoff among current-key residual, protected-output displacement, and update energy; where does ordinary Delta lie; and when is a declared finite budget infeasible?

The patch changes the objective, not the available evidence. It does not infer which old facts remain valid, does not release a protected direction, and does not make a one-step certificate a long-horizon guarantee.

## 2. Formal object and information boundary

Let `S in R^{d x m}` be key-by-value, `k in R^d` a nonzero write key, `v in R^m`, and

`e = v-S^T k`.

For a general matrix edit `Delta S in R^{d x m}`, prescribe a correction fraction `gamma` by

`(Delta S)^T k = gamma e`.

The post-edit current-key residual is then `(1-gamma)e`. Full current-key correction is `gamma=1`; partial correction is permitted. A standard Delta write with direction `beta k e^T` realizes this same `gamma` only when `beta=gamma/||k||^2` is inside the declared gate range.

Let `G>=0` be a pre-action measurable protected-query covariance or declared quadratic metric. For example, with nonnegative weights and protected queries `q`,

`G = E[w(q) q q^T | F]`.

The quadratic protected **output displacement** and update energy are

`D(Delta S)=tr((Delta S)^T G Delta S)`,

`E(Delta S)=||Delta S||_F^2`.

If `Delta S=x e^T`, then `D=||e||^2 x^T G x` and `E=||e||^2||x||^2`. The metric is not free: a stored dense `G` costs `O(d^2)` state, a rank-`r` representation costs `O(dr)`, and both require a causal rule for estimating and releasing still-valid protected directions.

## 3. Representer theorem for the scalarized frontier

Fix `mu>0` and write `H_mu=G+mu I`, so `H_mu` is positive definite. Consider the general matrix problem

`min_{Delta S} tr((Delta S)^T H_mu Delta S)`

subject to `(Delta S)^T k=gamma e`.

Column-wise Lagrange stationarity gives `H_mu Delta S = k lambda^T`. Enforcing the constraint yields the unique solution

`Delta S_mu^* = [gamma H_mu^{-1}k /(k^T H_mu^{-1}k)] e^T`.

Thus the rank-one residual form is a consequence of the quadratic problem; it was not assumed. Its exact scalarized cost is

`C_mu^*(gamma)=gamma^2 ||e||^2 /(k^T H_mu^{-1}k)`.

For fixed nonzero `gamma,e`, the directions

`x_mu=gamma H_mu^{-1}k /(k^T H_mu^{-1}k)`

sweep the supported protection–energy frontier. If `0<mu_1<mu_2`, the two optimality inequalities imply

`||x_{mu_2}||^2 <= ||x_{mu_1}||^2`,

`x_{mu_1}^T G x_{mu_1} <= x_{mu_2}^T G x_{mu_2}`.

Increasing `mu` spends more protected displacement to reduce update energy. These are one-step geometric quantities, not semantic or recurrent guarantees.

## 4. Ordinary Delta is a frontier endpoint, not a dominated method

For the same correction `gamma`, ordinary Delta uses

`x_Delta=gamma k/||k||^2`.

This is the unique minimum-energy vector satisfying `k^T x=gamma`; therefore it is Pareto efficient. It must not be described as dominated. It is, however, generally suboptimal for the scalarized cost `x^T H_mu x`. Its exact scalarized-cost ratio is

`R_mu = [(k^T H_mu k)(k^T H_mu^{-1}k)]/||k||^4 >= 1`,

by Cauchy–Schwarz applied to `H_mu^{1/2}k` and `H_mu^{-1/2}k`. Equality holds exactly when `k` lies in one eigenspace of `H_mu` (equivalently of `G`). As `mu` tends to infinity, `x_mu` tends to `x_Delta`, the minimum-energy endpoint.

This ratio is a diagnostic for a weighted objective only. It does not prove lower total model loss, lower wall-clock cost, or better language performance.

## 5. Hard-protection and singular-metric limits

Let `P_0` project onto `ker(G)` and set `k_0=P_0 k`.

### 5.1 A zero-damage direction exists

If `k_0 != 0`, the minimum-energy zero-damage edit at correction `gamma` is

`x_0=gamma k_0/||k_0||^2`.

It has `x_0^T G x_0=0` and energy `gamma^2/||k_0||^2`. Under the finite direction-norm budget `||x||<=B`, zero-damage correction is feasible iff

`B ||k_0|| >= |gamma|`.

For full overwrite this recovers the parent `1/rho^2` energy blow-up as the unprotected component `rho=||k_0||` approaches zero.

### 5.2 No zero-damage direction exists

If `k_0=0`, then `k` lies in `range(G)`. Generalized Cauchy–Schwarz gives

`(k^T x)^2 <= (k^T G^dagger k)(x^T G x)`.

Hence the sharp minimum protected displacement at correction `gamma` is

`D_min/||e||^2 = gamma^2/(k^T G^dagger k)`,

attained by `x_0=gamma G^dagger k/(k^T G^dagger k)`. Exact hard protection is impossible for nonzero `gamma`.

The degenerate controls are explicit: when `G=0`, all edits have zero declared displacement and ordinary Delta is the minimum-energy choice; when `e=0`, no correction is needed and all displayed cost ratios involving `||e||` are operationally vacuous; when `k=0`, nonzero `gamma e` is infeasible.

## 6. A real finite-budget problem and its KKT certificate

A penalty is not itself a hard budget. For a declared update-direction budget `B`, solve

`min_x x^T G x` subject to `k^T x=gamma` and `||x||^2<=B^2`.

The problem is feasible iff `B>=|gamma|/||k||`. When `B>|gamma|/||k||`, relative Slater holds and its KKT equations are

`(G+mu I)x = nu k`,

`mu>=0`, `mu(||x||^2-B^2)=0`, `k^T x=gamma`.

Therefore every active-budget optimizer with `mu>0` is in the same `x_mu` family; `mu=0` describes a feasible minimum-damage endpoint, with the usual singular-case qualifications. At the boundary `B=|gamma|/||k||`, the feasible set is the singleton ordinary-Delta direction and is recovered as `mu` tends to infinity; a finite multiplier need not exist, and multipliers need not be unique in eigen-aligned degeneracies. This converts the old `rho=0`/`1/rho` diagnostic into a computable approximate-correction certificate without deleting it.

If both a displacement cap and an energy cap are imposed, feasibility is the convex QCQP

`max_x k^T x` subject to `x^T Gx<=C` and `||x||^2<=B^2`.

Its KKT direction is `(aG+bI)^dagger k` for nonnegative multipliers with the usual range and complementarity conditions. Solving that two-multiplier problem is classical trust-region/QCQP work; naming the caps does not create a new Delta mechanism.

For positive normalized caps `C,B^2`, its exact support value can also be written

`h(C,B^2)^2 = inf_{a,b>=0} (aC+bB^2) k^T(aG+bI)^dagger k`,

where `(a,b)!=(0,0)` and `k` must lie in `range(aG+bI)`; boundary cases are obtained by limits. Weighted Cauchy–Schwarz gives the upper bound and convex QCQP strong duality gives equality under the stated positive-cap/Slater conditions. A target correction `gamma` is feasible iff `|gamma|<=h(C,B^2)`. In particular `h(0,B^2)=B||P_0k||`, recovering the zero-damage condition above.

## 7. Soft correction corollary

For `lambda>0`, the unconstrained one-step surrogate

`min_{Delta S} ||e-(Delta S)^T k||^2 + lambda tr((Delta S)^T H_mu Delta S)`

has

`Delta S^* = [H_mu^{-1}k/(lambda+k^T H_mu^{-1}k)] e^T`.

The realized correction is `gamma=z/(lambda+z)` and the remaining residual fraction is `lambda/(lambda+z)`, where `z=k^T H_mu^{-1}k`. This is a ridge/proximal normal equation and a strong baseline, not a candidate contribution.

## 8. Old counterexamples and missing objectives revisited

1. **Exact overwrite versus reversibility remains.** With fixed `x`, the residual update is `S^+=(I-xk^T)S+xv^T`, and the matrix determinant lemma gives `det(I-xk^T)=1-k^T x=1-gamma`. Full correction remains singular; partial correction is invertible only when `gamma!=1`.
2. **Protected-span collision remains.** If a hard protected span contains `k`, then `k_0=0` and a nonzero exact correction has positive minimum damage. Orthogonal keys remain the success case.
3. **Semantic identifiability remains.** The same `(S,k,v,G)` can arise from a true revision or an encoder collision. The frontier chooses a geometric compromise but cannot decide which protected direction should be released.
4. **Displacement is not generally protected loss.** If a protected query has target `y(q)` and pre-edit residual `r(q)=S^Tq-y(q)`, then the squared-loss increment for `Delta S=xe^T` is

   `2(q^Tx) r(q)^T e + (q^Tx)^2 ||e||^2`.

   The linear cross moment can reverse the action sign. `G` alone is exact protected loss only under an explicit zero-cross-moment condition or when displacement itself is the declared objective.
5. **One-step is not future protection.** State-dependent future keys, gates, routing and readouts require the complete chronological Jacobian/costate object already analyzed in Step 2. A sampled `G` can also have an unsafe empirical nullspace out of sample.

## 9. Predictions, information/state cost, and strong comparisons

Predictions, not results:

- at matched correction, ordinary Delta is the minimum-energy endpoint and equals every scalarized optimum only for an eigen-aligned key;
- moving toward the protected nullspace decreases declared displacement while increasing update energy;
- zero-damage full correction becomes infeasible under budget exactly when `B||P_0k||<1`;
- any claimed escape from this boundary must relax correction/protection, change representation, or add information/state;
- a diagonal or low-rank approximation can miss the full-metric frontier, especially near small eigenvalues.

Strong same-information alternatives are ordinary Delta, hard QR/nullspace projection, ridge/soft projection, OWM/OGD/GEM-style projected updates, AlphaEdit/O-Edit, PDN, full/diagonal RLS, and GKA's finite iterative ridge solve. Dense inversion is `O(d^3)` naively; iterative products still need access to `G`; low-rank bases cost `O(dr)` state and application; updating which facts remain protected requires evidence or replay not supplied here.

bAbI, LAMBADA and LongMemEval can measure endpoint recall or knowledge-update answers, but do not expose the per-write protected covariance, correction fraction, action propensity, paired write/no-write outcome, or full future Jacobian. CounterFact/ZSRE-style prescribed-edit locality is a closer endpoint, but it is parameter editing with supplied targets and still does not natively identify this Delta fast-state frontier. The exact algebra is reviewable; natural-language usefulness has a measurement gap and empirical effect is unknown.

## 10. Nearest-work and disposition

The optimizer is the same normalized inverse-metric direction as the packet's D03 control and the full inverse-Gram theory behind PDN/RLS. Hard and soft protection are covered by OWM, AlphaEdit/O-Edit, OGD/GEM/EWC-type constraints, while GKA covers online ridge statistics and finite iterative solves. Implemented PDN uses a stable diagonal approximation rather than the paper's exact full inverse, which is an implementation distinction, not a new opening for this formula.

The bounded residual is an explicit Delta-specialized Pareto/conditioning theorem: a general-matrix representer result, ordinary-Delta equality/ratio certificate, hard-budget feasibility condition, and preservation of the exact-overwrite singularity. That is useful repair work, but it is not a distinct update mechanism and receives no D-number.

Counts remain **5 historical / 0 active / 0 scientifically admitted / 0 selected**. Mathematical correctness is conditional, contribution difference fails because of major mechanism collision, and experimental effectiveness is unknown.

Reopen only if a later child supplies at least one of:

1. a prefix-only, same-budget Delta-specific estimator of a dynamic/action-weighted `G` with a nontrivial approximation or regret theorem;
2. an information/state lower bound showing when every same-budget updater stays a quantified distance from the frontier;
3. a native causal object with pre-action protected queries, declared correction budgets, propensities and identifiable action outcomes.
