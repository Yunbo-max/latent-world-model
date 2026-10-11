# R09 v3 — Prefix-robust Gramian carrier and full-width boundary

Status: **conditional theorem/debug control; substantive attempt 3/3 exhausted; parked, not a candidate**  
Parent: `repairs/R09_DYNAMIC_PROTECTION_GRAMIAN.v2.md` (preserved unchanged on literal `main`)  
Scope: mathematics, source, distinctness and native-measurement review only. No model code, software test, training, inference, scoring, benchmark dispatch, or model/data download.

## 1. Original problem, precise failure, and patch

R09 v2 repaired the static v1 metric by deriving the exact transported finite-horizon protection Gramian for a declared frozen suffix. It also proved that an unrestricted prefix cannot identify the future anisotropy. The earliest remaining premise was narrower:

> Can the diagonal-plus-rank-one structure of Delta transitions make the action-relevant future geometry exactly low dimensional, even when the realized future mode is unknown at action time?

The tempting repair was to retain a small future-key/query span and solve the inverse-metric edit there. That proposal had two gaps. First, a realized low-rank Gramian need not admit a small **common** carrier over all prefix-compatible futures. Second, span containment alone does not identify the PSD anisotropy inside that span.

This child patches the target again: it characterizes the minimum exact common linear carrier for a declared finite family of prefix-compatible suffixes, gives the exact reduced robust action problem, and constructs a standard rank-one Delta family in which every realized Gramian has rank one while the common carrier is all of `R^d`. This is a useful capacity/identifiability boundary, not a new updater.

## 2. Declared future family and transported factors

Fix action time `t`, row dimension `d`, nonzero current key `k`, correction `gamma`, and energy regularizer `mu>0`. Let `Omega_t` be a **prefix-declared** finite set of lawful future modes. For each `omega in Omega_t`, the frozen perturbation suffix is

`Delta S_h = P^omega_{t,h} Delta S_t`,

where `P^omega_{t,t}=I` and chronological products are not commuted. At stage `h`, factor the declared PSD row metric as

`Q_h^omega = U_h^omega (U_h^omega)^T`,

and take strictly positive weights `w_h^omega` for retained stages. Define transported factors

`Z_h^omega = sqrt(w_h^omega) (P^omega_{t,h})^T U_h^omega`.  (1)

Then the v2 dynamic Gramian is

`G^omega = sum_h Z_h^omega (Z_h^omega)^T`.  (2)

Zero-weight stages may simply be removed. A different factorization of the same `Q_h^omega` does not change the column span in the results below.

## 3. Exact minimum common carrier

For each fixed mode,

`range(G^omega) = span_h range(Z_h^omega)`.  (3)

Indeed, for any `y`,

`y^T G^omega y = sum_h ||(Z_h^omega)^T y||^2`.

Therefore

`ker(G^omega)=intersection_h ker((Z_h^omega)^T)`,

and taking orthogonal complements proves (3).

Define the common transported-factor carrier

`V_t^* = span_{omega in Omega_t, h} range(Z_h^omega)`,

`r_t^* = dim(V_t^*)`.  (4)

Let `V` have orthonormal columns. The following are equivalent:

1. `G^omega = V V^T G^omega V V^T` for every `omega`;
2. `range(G^omega) subseteq range(V)` for every `omega`;
3. `V_t^* subseteq range(V)`.

Hence `r_t^*` is the minimum dimension of an exact **common linear Gramian carrier**. This is a representation-class statement. It is not a finite-bit capacity theorem and does not rule out a nonlinear action-specific statistic.

For a finite mode tree the carrier can be computed backward. At node `eta`, with lawful outgoing edges `a`,

`V_eta^* = span(range(U_eta), union_a A_{eta,a}^T V_{eta a}^*)`.  (5)

Path-dependent node spaces must be retained when the switching language is constrained. Replacing the tree by an unconstrained rectangular mode hull is a safe but possibly larger carrier, exactly as in R18.

### 3.1 Exact active-span specialization and the v2 cost correction

For one realized no-decay suffix, write

`A_j=I-beta_j k_j k_j^T`, `Q_h=C_h C_h^T`,

and let `V=span({k_{t+1:H}} union_h range(C_h))` have orthonormal basis `U in R^{d x s}`. With `k_j=U a_j` and `Q_h=U Qbar_h U^T`, `V` reduces every symmetric `A_j` and

`A_j=U(I_s-beta_j a_j a_j^T)U^T+Pi_perp`,

`P_{t,h}=U Pbar_{t,h}U^T+Pi_perp`, `G=U Gbar U^T`.  (5a)

The core obeys the exact backward recursion

`Gbar_j=w_j Qbar_j+Abar_{j+1}^T Gbar_{j+1} Abar_{j+1}`.  (5b)

For `Abar=I-beta a a^T` and `g=Gbar a`,

`Abar^T Gbar Abar = Gbar-beta(a g^T+g a^T)+beta^2(a^T g)aa^T`.  (5c)

Thus, once a lawful basis and suffix coordinates are available, a pure-Delta dense core update is `O(s^2)` per step, not `O(s^3)`. In full space the same structure gives `O(Hd^2)`, correcting v2's generic `O(Hd^3)` upper bound for this special recurrence. Forming stage metrics, discovering/orthogonalizing the basis, projecting raw vectors, and representing future uncertainty remain separate costs.

For a known core, decompose the current key as `k=Ua+b`, with `b=Pi_perp k`. Then

`(mu I+U Gbar U^T)^{-1}k = U(mu I_s+Gbar)^{-1}a+mu^{-1}b`,

and the normalized equality-constrained solution is

`x*=gamma y/[a^T(mu I_s+Gbar)^{-1}a+mu^{-1}||b||^2]`,  (5d)

where `y` is the preceding inverse action. Given dense `U`, the state is `O(ds+s^2)`, backward work is `O(Hs^2)` for rank-one Delta factors plus stage-metric formation, one dense solve is `O(s^3)`, and projection/lifting is `O(ds)`. Incremental QR and `O(ds)` coordinate extraction per raw vector must be charged; a dense basis can erase the practical saving.

If `mu=0`, uniqueness need not hold. When `P_ker(G) k != 0`, a zero-protection-damage feasible direction exists and the minimum-Euclidean-norm one is `gamma P_ker(G)k/||P_ker(G)k||^2`; otherwise the v1 pseudoinverse/range branch applies. If `k=0` and `gamma!=0`, the constraint is infeasible; `gamma=0` (or an operational residual `e=0`) is degenerate.

## 4. Exact robust action reduction

Consider the declared robust rank-one write direction problem

`min_x max_{omega in Omega_t} x^T (G^omega + mu I) x`

subject to `k^T x = gamma`.  (6)

Let

`L_t = span({k} union V_t^*)`.

For any feasible `x`, let `x_L` be its orthogonal projection onto `L_t`. Because `k in L_t`, `k^T x_L=gamma`. Because every `G^omega` has range in `V_t^*`,

`x_L^T G^omega x_L = x^T G^omega x`,

while `||x_L||<=||x||`. Since `mu>0`, every component orthogonal to `L_t` strictly increases every objective unless it is zero. Therefore the unique minimizer of (6) lies in `L_t`.

If `W_t` is an orthonormal basis of `L_t`, (6) reduces exactly to the `ell_t`-dimensional convex problem

`min_y max_omega y^T [W_t^T G^omega W_t + mu I] y`

subject to `(W_t^T k)^T y=gamma`,  (7)

where `ell_t <= min(d,r_t^*+1)`. For one known mode, (7) is the v2 normalized inverse-metric closed form. For several modes it is a robust convex QCQP; the carrier does not remove the need to represent the mode ambiguity or its inner PSD cores.

## 5. Delta rank-one counterexample: realized rank one, common width `d`

Let `d>=2`, let `q=1_d`, choose `0<beta<1`, and let the legal future mode `i in {1,...,d}` use the standard no-decay Delta transition

`A_i = I - beta e_i e_i^T`.  (8)

Each `A_i` is invertible because `beta<1`. Use one rank-one terminal metric `Q=q q^T`. The transported factor is

`z_i=A_i^T q=q-beta e_i`,

and the realized Gramian is

`G_i=z_i z_i^T`,

which has rank one. However, the matrix with columns `z_i` is

`Z = 1_d 1_d^T - beta I`.

Its eigenvalue on `span(1_d)` is `d-beta` and its `d-1` orthogonal eigenvalues are `-beta`. Thus `Z` is nonsingular and

`span_i range(G_i)=R^d`, `r_t^*=d`.  (9)

So diagonal-plus-rank-one Delta structure and rank-one stage loss do **not** imply a small prefix-robust exact carrier. A family of individually rank-one futures can require full width before the future key is known. The example uses partial, invertible Delta factors; it does not rely on the singular full-overwrite endpoint.

The example is exact-width, not an approximate-rank impossibility. The singular values of `Z` are `d-beta` and `beta` repeated `d-1` times, so an approximation may discard directions only under an explicit absolute/relative error and action-regret certificate. That returns to R20's spectral-transfer premise.

## 6. Why a small carrier still does not determine the write

Suppose a lawful prefix supplies an exact orthonormal carrier `V` of width `r`, so

`G^omega=V C^omega V^T`.

The action still depends on the core `C^omega`. Two prefix-compatible PSD cores with swapped anisotropy inside the same `V` reproduce the v2 opposite-direction/minimax construction. Therefore span containment without a prefix-lawful core, ambiguity set, or direct action value is insufficient.

For one known core, Woodbury gives

`(mu I+V C V^T)^{-1}k`

from `V^T k` and an `r x r` solve. This is established low-rank inverse/Lyapunov geometry. For an ambiguity set of cores, (7) is a generic robust QCQP. A direct predictor of the same `ell_t` action coefficients, or direct robust action/Q prediction, is the strongest same-information alternative.

## 7. Delta transition structure and actual cost

For the project recurrence

`A_j=(I-beta_j k_j k_j^T)D_j`,

the backward factor action is

`A_j^T U = D_j^T U - beta_j D_j^T k_j (k_j^T U)`.  (10)

For the project's real diagonal decay, `D_j^T=D_j` and this application costs `O(d r)` for an `r`-column factor. A broader structured `D_j` needs an explicitly fast adjoint action. For an exact core reduction with decay, the chosen carrier must also be a common reducing subspace of every `D_j`; one may not commute `D_j` with the rank-one factor. In that case

`Abar_j=(I-beta_j a_j a_j^T)Dbar_j`.

The `O(s^2)` step survives for scalar/diagonal `Dbar_j`, or another declared structure supporting the two-sided core update at that cost; a generic dense core decay costs `O(s^3)`. If the initial key/query span is not decay-invariant, its closure under all `D_j` is required and can become all of `R^d`, as in R16's active-spectrum/Krylov boundary. A formally full-rank stage metric does not always force full active width: a shared scalar base such as `Q_h=alpha_h I` yields `c Pi_perp+U Gbar U^T`, hence a scalar-base-plus-core solve. No such claim holds for a generic anisotropic full-rank metric.

Even with the exact rank-one update algebra, the full prefix-robust object is not free:

- an exact basis costs `O(d r_t^*)` state and basis discovery/orthogonalization;
- every core costs up to `O((r_t^*)^2)` per mode/state, with generic factorization/solve up to `O((r_t^*)^3)`;
- an explicit mode tree can grow exponentially in horizon, while merging to one common span may saturate at `d`;
- constrained switching requires node-specific carriers rather than an unpaired rectangular union;
- free-running keys, gates, routes and readouts require the complete-state Jacobian and cost terms, not only (10);
- the actual memory write still costs `O(dm)`.

The algebraic span/rank identities hold for arbitrary real gates, including singular or expansive factors. Stability or non-expansion is a separate condition; for a normalized pure factor it requires, for example, `0<=beta_j||k_j||^2<=2`.

DeltaProduct's multiple generalized Householder factors enlarge the transition product class; they do not supply the missing prefix-lawful future family or prevent common-span growth.

## 8. Old counterexamples and v2 results rechecked

1. **Static frontier remains.** R09 v1's finite-budget correction/protection/energy frontier is unchanged for every declared `G`.
2. **Full overwrite remains singular.** At current correction `gamma=1`, `det(I-xk^T)=0`; the carrier does not restore reversibility.
3. **Protection collision remains.** If correction and protected directions overlap, the old infeasibility/`1/rho^2` energy boundary remains.
4. **The v2 Gramian remains conditional.** Equations (1)--(2) require a frozen/exogenous declared suffix or the qualified complete-state local object.
5. **The v2 identical-prefix anisotropy lower bound remains.** A common span can still hide different cores and different oracle actions.
6. **Semantic validity remains unidentified.** The carrier records sensitivity geometry, not whether an old fact remains true or a new assertion is grounded.
7. **Nonseparable value curvature remains outside the rank-one closed form.** Lifting to a general matrix action with heterogeneous value-side factors can require a higher-rank solve.
8. **R20 transfer remains the approximate control.** Approximate containment or approximate cores require a spectral/additive error premise; prefix reconstruction error alone is insufficient.

## 9. Closest work and distinctness

The main theorem is a finite-horizon, Delta-coordinate specialization of established switched-system observability-space and Gramian-range machinery. Linear switched-system Gramians already encode observable spaces; low-rank Lyapunov/Gramian methods and global projection are established; low-rank switching and products of Householder transitions are established. Internally:

- R18 v2 already gives the prefix-robust observable quotient and its possible collapse to full state;
- R16 v2 gives an exact active-core reduction plus the full-width/dense-basis boundary for a different joint-flow target;
- R20 v3 gives the sharp spectral transfer and identical-prefix impossibility for approximate metrics;
- R09 v2 already gives the dynamic Gramian and swapped-anisotropy minimax control.

The retained residue is a compact exact theorem and a particularly sharp Delta counterexample: every realized future Gramian can be rank one while the lawful common carrier is full width. This is useful for debugging claims that "rank-one Delta implies low-rank protection state," but it does not create a distinct updater.

## 10. Measurement, predictions, and disposition

Conditional predictions, not results:

- if a lawful prefix supplies a small exact carrier and its core/ambiguity set, the robust action can be solved entirely in `span(k,V_t^*)`;
- the carrier dimension grows monotonically when lawful future modes or protected factors are added;
- the family (8)--(9) forces full exact width despite rank-one realized Gramians;
- approximate savings require an explicit tail/spectral certificate and must be compared at matched state/FLOPs with direct low-rank action prediction.

The reviewed native assets expose downstream endpoint scores but not, before each write, a declared carrier, future factor-containment event, action-indexed core, propensity or paired outcome. They cannot identify this mechanism. Custom hidden-state instrumentation would not be a native scorer.

**Decision:** attempt 3/3 succeeds only as a conditional theorem/debug control. Major switched-observability, low-rank Gramian, R18, R16 and R20 collisions remain; matched-cost and native-measurement obligations remain open; empirical effect is unknown because no execution occurred. Add zero active, scientifically admitted, or selected candidates and park the R09 lineage as exhausted.

Reopen only with either (i) a native randomized action-level record carrying a lawful pre-action factor-containment/core object and matched-cost comparator, or (ii) a non-R16/R18/R20 Delta structure that proves a strictly smaller lawful carrier/action statistic and a matched-total-cost advantage over direct robust action prediction.
