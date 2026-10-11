# R09 v2 — Dynamic protection Gramian and prefix minimax boundary

Status: **mathematically accepted only as a conditional theorem/control; parked, not a candidate**  
Parent: `repairs/R09_FINITE_BUDGET_OVERWRITE_PROTECTION.v1.md` (preserved byte-for-byte on literal main)  
Substantive repair attempt: **2 of at most 3**  
Scope: mathematics and source review only. No model execution, training, inference, scoring, benchmark dispatch, or model/data download.

## 1. Original problem, failure type, and patch

R09 v1 solved the sharp *one-step static* tradeoff between current-key correction, a declared protected quadratic, and update energy. Its formulas were correct, but its metric `G` did not say how a current edit reaches later queries. Calling that object long-horizon protection would be a **target/construction mismatch**.

This child keeps every v1 result and counterexample. It patches the target by deriving the exact finite-horizon quadratic for a frozen linearized suffix, then asks what remains possible when that future metric must be estimated from the legal prefix. The repair yields:

1. an exact transported protection Gramian and backward recursion;
2. the v1 normalized inverse-metric frontier with that dynamic metric;
3. a sharp estimator-transfer factor, already overlapping R20 v3;
4. an exact identical-prefix two-future minimax lower bound.

The patch does not identify which facts remain valid, reveal an unseen suffix, or turn retrospective suffix geometry into an online signal.

## 2. Formal object and exact transported loss

Let `S_t in R^{d x m}`, nonzero write key `k in R^d`, residual `e=v-S_t^T k in R^m`, and restrict the current edit to

`Delta S_t = x e^T`, with `k^T x = gamma`.

Then `(Delta S_t)^T k=gamma e`, so the current-key residual becomes `(1-gamma)e`. This rank-one form is not assumed to be a new mechanism: v1 proved that it contains the optimum for a common left-side quadratic.

For a declared frozen suffix, suppose row perturbations evolve as

`Delta S_h = P_{t,h} Delta S_t`,

where `P_{t,t}=I` and, if `Delta S_j=A_j Delta S_{j-1}`, then

`P_{t,h}=A_h A_{h-1} ... A_{t+1}`.

Let `Q_h succeq 0` be a declared stage query/curvature metric on the row space and `w_h>=0`. This is a **left-side separable, Euclidean value-space** loss. The future quadratic displacement is

`D_{t:H}(x)=sum_{h=t}^H w_h tr(Delta S_h^T Q_h Delta S_h)`

`            =||e||^2 x^T G_{t:H} x`,

with the exact finite-horizon transported Gramian

`G_{t:H}=sum_{h=t}^H w_h P_{t,h}^T Q_h P_{t,h} succeq 0`.  (1)

For a single protected query `q_h`, take `Q_h=q_h q_h^T`; then the stage term is exactly `||Delta S_h^T q_h||^2`. With `G_{H:H}=w_H Q_H`, the recursion is

`G_{j:H}=w_j Q_j + A_{j+1}^T G_{j+1:H} A_{j+1}`.  (2)

The multiplication order in (1)--(2) follows the actual forward perturbation order and cannot be commuted.

If the rank-one restriction is retained, a value-side term `tr(Delta S_h^T Q_h Delta S_h R_h)` reduces to the scalar weight `e^T R_h e` times a left quadratic in `x`. But if the action is lifted back to v1's general-matrix feasible set `(Delta S_t)^T k=gamma e`, varying/non-proportional `R_h` generally produces a nonseparable Kronecker-sum quadratic in `vec(Delta S_t)`. Its constrained optimum need not equal `x e^T`; it falls back to R20 v1's general higher-rank edit. Thus the rank-one reduction here is exact for the declared rank-one action/common left metric, not for an arbitrary general-matrix future Hessian.

### Complete-state qualification

Equations (1)--(2) are exact only for the declared frozen linear system. If the edit changes later keys, gates, routing, updater state, token law, or environment feedback, lift to the complete state `z`. If `B_t(e)x` injects the edit into `delta z_t`, `J_{t,h}` is the complete-state Jacobian, and `C_h succeq 0` is the stage metric, the local Gauss--Newton object is

`G^GN_{t:H}=B_t(e)^T [sum_h w_h J_{t,h}^T C_h J_{t,h}] B_t(e)`.  (3)

Exact second-order loss additionally contains costate-weighted dynamics curvature and linear/cross terms; R07 v2 already derived that boundary. Thus (3) is not a full nonlinear guarantee.

## 3. Dynamic frontier: exact conditional solve

Add energy regularization `mu>0` and define

`H_t=G_{t:H}+mu I succ 0`.

The unique solution of

`min_x x^T H_t x  subject to k^T x=gamma`

is

`x*_t = gamma H_t^{-1}k/(k^T H_t^{-1}k)`,  (4)

with cost

`gamma^2/(k^T H_t^{-1}k)`

before multiplication by `||e||^2`. The proof is the one-constraint Lagrange calculation from v1. Therefore v1's ordinary-Delta endpoint, hard-budget frontier, singular nullspace limits, and two-cap dual remain valid after replacing static `G` by the correctly transported `G_{t:H}`.

This is a conditional offline/frozen-suffix optimum. It is deployable only if `H_t`, or a lawful prefix estimator of it, is actually available before the write.

## 4. Random future and the causal information boundary

If future transitions and stage metrics are random but exogenous to the current action, and the declared state is sufficient, the prefix-conditional expected metric is

`bar G_t = E[sum_h w_h P_{t,h}^T Q_h P_{t,h} | F_t]`.  (5)

Under a Markov/sufficient-state law its backward form is the conditional Lyapunov/Bellman recursion

`bar G_j = E[w_j Q_j + A_{j+1}^T bar G_{j+1} A_{j+1} | F_j]`.  (6)

Equations (5)--(6) are analysis identities, not free observations. Estimating them needs an explicit continuation law, state, samples, or externally grounded feedback. If the action changes the future law, a fixed conditional expectation is wrong: the action-indexed transition, observation, and policy state belong in a Bellman/action-value object. Model-generated suffixes are not new external evidence.

## 5. Estimator error: sharp transfer, but no new mechanism

Let `hat H_t succ 0` be a prefix-measurable surrogate and `hat x` its normalized inverse-metric action. If, on the affine feasible span,

`(1-epsilon) H_t preceq hat H_t preceq (1+epsilon) H_t`, `0<=epsilon<1`,  (7)

then

`(hat x^T H_t hat x)/(x*_t^T H_t x*_t) <= 1/(1-epsilon^2)`.  (8)

To see this, rewrite (7) as

`[1/(1+epsilon)] hat H_t preceq H_t preceq [1/(1-epsilon)] hat H_t`

and apply the shared-affine-constraint Kantorovich bound

`(M+m)^2/(4Mm)`

with `m=1/(1+epsilon)` and `M=1/(1-epsilon)`. The constant in (8) is sharp. This is exactly the spectral-transfer theorem already retained in R20 v3, now specialized to the R09 dynamic Gramian. It is a required control, not a distinct contribution.

Equivalently, with `M_0=H_t^{-1/2} hat H_t H_t^{-1/2}` and `a=H_t^{-1/2}k`, the exact ratio is

`rho=[(a^T M_0^{-2}a)(a^Ta)]/(a^T M_0^{-1}a)^2`;  (9)

the eigenvalues of `M_0^{-1}` lie in `[1/(1+epsilon),1/(1-epsilon)]`, yielding (8). The sandwich must hold on the full affine feasible span used by the action; controlling only feasible differences can miss base--tangent cross terms.

The premise is the scientific burden. A small in-prefix reconstruction error does not imply (7) for an unrestricted future.

## 6. Exact identical-prefix minimax lower bound

The missing premise admits a quantitative counterexample. Let `d=2`, `||k||=1`,

`k=(1,1)^T/sqrt(2)`, `gamma!=0`, and `M>m>0`.

Two futures share the exact same legal prefix but have

`H_1=diag(M,m)`, `H_2=diag(m,M)`.  (10)

Every deterministic prefix-only rule must choose the same feasible vector in both worlds. Write

`x=(gamma/sqrt(2)+s, gamma/sqrt(2)-s)^T`.

The two costs are

`C_1(s)=M(gamma/sqrt(2)+s)^2+m(gamma/sqrt(2)-s)^2`,

`C_2(s)=m(gamma/sqrt(2)+s)^2+M(gamma/sqrt(2)-s)^2`.

Their maximum equals

`(M+m)(gamma^2/2+s^2)+sqrt(2)|gamma|(M-m)|s|`,

so it is uniquely minimized at `s=0`. The minimax prefix action is therefore

`x_rob=gamma k`,

the ordinary normalized Delta direction. Each future-specific oracle has cost

`C_i*=gamma^2/(k^T H_i^{-1}k)=2 gamma^2 M m/(M+m)`.

Hence every deterministic prefix-only rule has worst-future competitive ratio at least

`boxed[(M+m)^2/(4Mm)]`,  (11)

and ordinary Delta attains it on this family. Randomization cannot improve the worst expected ratio: the maximum is at least the average of the two expected costs, which is `(M+m)(gamma^2/2+E[s^2])`.

This does not say that future-aware preconditioning is useless. It says that without a continuation premise, directional anisotropy can be swapped behind an identical prefix and the robust solution collapses to ordinary Delta.

## 7. Old counterexamples rechecked

1. **Exact overwrite singularity remains.** For `gamma=1`, `det(I-xk^T)=1-k^Tx=0`; a dynamic metric does not invert the affine old-state map.
2. **Protected-span collision remains.** If the write constraint overlaps a protected nullspace requirement, feasibility and the `1/rho^2` blow-up from v1 are unchanged.
3. **Semantic validity remains unidentified.** `G_{t:H}` weights declared future sensitivity; it does not reveal whether an old fact is still true or whether a revision is grounded.
4. **Displacement is not full loss.** A true loss change may include a linear cross term, indefinite curvature, higher-order remainder, and action-dependent support.
5. **Frozen suffix is not free-running dynamics.** Complete Jacobians and, for exact second order, costate/dynamics-curvature terms are required.
6. **Estimator accuracy is not prefix-identifiable over unrestricted futures.** Equations (10)--(11) preserve and sharpen the same-prefix counterexample rather than deleting it.
7. **Nonseparable value curvature remains outside the closed form.** A sum of different `Q_h otimes R_h` terms need not preserve the `x e^T` representer; the general constrained solve may require higher rank.

## 8. Predictions, failure boundaries, and strongest alternatives

Conditional predictions, not results:

- when protected queries align with future high-gain singular directions, (4) rotates the write away from them and lowers the declared finite-horizon quadratic relative to ordinary Delta;
- if `G_{t:H}` is nearly isotropic on the feasible span, (4) approaches ordinary normalized Delta;
- if the spectral distortion is `epsilon`, no advantage claim should exceed the sharp transfer envelope (8);
- under the swapped identical-prefix family, richer deterministic prefix computation cannot beat (11) without new information or a valid continuation law.

Failure boundaries include `mu=0` with unmatched nullspaces, nonlinear/discrete route switches, action-dependent future laws, unbounded horizons without a tail certificate, and hidden state omitted from the Jacobian.

Strong same-information alternatives are ordinary Delta; v1's static inverse metric; R20 v3's projected spectral-transfer control; R07 v2 complete-state directional margin; a direct prefix action-value/factor predictor; low-rank/sketched Gramian plus Woodbury; generic Lyapunov/Riccati or DDP/iLQR calculation; and no-write. At equal information and total cost, a direct predictor that matches (4) removes the practical need for the explicit Gramian.

## 9. Information, state, computation, and measurement

For the frozen row-space system, an exact dense `d x d` Gramian costs `O(d^2)` state. Generic dense backward recursion and solve cost up to `O(H d^3)` and `O(d^3)` respectively. For the complete-state lift (3), an explicit `n x n` state Gramian costs `O(n^2)` storage; forming only its projected `d x d` action metric matrix-free still pays for horizon-wide batched JVP/VJP passes, application of `B_t(e)`, activation checkpointing or recomputation, solver tolerances, and calibration. Low-rank `Q_h`, iterative solves, or sketches can reduce these costs, but no Delta-specific improvement theorem is established. A random-law version also pays for the continuation model and calibration data. All costs must be matched against direct action prediction and ordinary Delta.

LongMemEval, CounterFact/ZSRE, AToKe, SEAL, bAbI, and LAMBADA can expose downstream endpoint changes under executed policies. Their reviewed native formats do not jointly expose the pre-write complete state, action-indexed future transitions, stage metrics, paired write/no-write futures, propensity, and matched-cost oracle needed to identify (5), verify (7), or estimate competitive regret. This is a measurement gap, not an experimental failure.

## 10. Decision and reopening rule

The repair is successful as mathematics: it replaces the static target by the exact finite-horizon transported quadratic and gives a sharp causal limitation. The contribution difference is not sufficient for a new candidate. Observability/energy Gramians, Lyapunov/Riccati recursions, DDP/iLQR, inverse-Gram preconditioning, and R20's spectral certificate already cover the main machinery. Empirical effect is **unknown; no execution**.

R09 v2 is parked after attempt 2/3. Counts remain **5 historical / 0 active / 0 scientifically admitted / 0 selected**.

Reopen attempt 3 only if at least one new delta is supplied:

1. a prefix-only Delta-specific estimator of the action-relevant dynamic Gramian with simultaneous coverage and lower matched state/FLOPs than direct action-value prediction or general JVP/VJP/DDP;
2. a structural theorem proving a smaller sufficient state or a sharper bound than R20 for the actual Delta recurrence;
3. a native causal record containing pre-action state/geometry, action propensity, grounded validity, and identifiable paired or off-policy future outcomes.
