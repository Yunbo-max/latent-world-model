# R03 v2 独立数学审查

- Reviewer assignment: `/root/r03_v2_math_review`
- Artifact: `research/delta-discovery-2026-10-08/repairs/R03_COUPLED_HORIZON_SAFETY.v2.md`
- Final artifact SHA256: `4c083cba9b45ebb27d82996aff894836ec832b993632e9992645b3a865fb5761`
- Decision: **ACCEPT — conditional mathematical control; not a candidate**
- Mode: static mathematics only; no code/tests/models/experiments/downloads.

## Review history

Initial exact-byte review of SHA256 `02613789f29d53940d0bdf95775f16dbd551316e69697ff55c6fb76e33af1464` returned **REVISE**. It found five scoped semantic gaps:

1. the Lipschitz display compared the same query and therefore did not yet cover an endogenous query generator;
2. tube, gain and residual constants used by a deployed action rule were not explicitly required to be decision-time measurable simultaneous bounds;
3. the propensity-weighted constraint controlled randomized-action expectation, not every realized action;
4. the floor-simplex condition `0<epsilon_mu<=1/K` was missing;
5. PSD output metrics, nonnegative risk budget and common query/target reference law needed to be explicit.

The integration writer repaired all five without deleting the counterexamples or loosening the claim: endogenous queries now use an augmented state/composite observable; free-running distribution change remains outside the pathwise theorem; deployable constants are `F_t`-measurable simultaneous bounds; expectation and actionwise safety are separated; the simplex/PSD/shared-law conditions are stated.

## Final checks

The reviewer re-hashed and reread final bytes. Accepted under the declared conditions:

1. `eta_x=vec(alpha beta k e^T)` has the stated dimensions and Frobenius norm.
2. `Gamma_h=prod_{j=t+1}^{t+h} gamma_j` has correct indexing from the post-action state; the finite/infinite geometric bounds follow.
3. The hybrid certificate correctly uses `w_0 d_{a,0}` and does not freeze later endogenous queries.
4. The horizon risk inequality is ordinary Cauchy--Schwarz in the shared-law direct-sum Hilbert space; the threshold is sufficient for `M_h>=0`, `rho_H>=0`, `B>=0`.
5. The protected-fiber recurrence and its distinction between `delta p=0` and persistent protected-coordinate injection are correct under uniform compatible-norm bounds.
6. `A=D=1/2,B=C=3/5` has joint eigenvalue `11/10`, so separate block stability is insufficient.
7. For finite nonnegative action costs and `0<epsilon_mu<=1/K`, the stated minimum floor-simplex cost is necessary and sufficient for feasibility.
8. The randomized budget controls conditional expected harm only; actionwise safety requires every supported action to meet its own bound.

Non-blocking precision limits retained by the review: the unified `g_h` notation is shorthand for the composite map when queries are endogenous; binary `U_0=0` semantically means `bar U_{0,H}=0`; the `b_H/U_1,H` write-probability statement is the binary zero-baseline-cost case and is capped by `1-epsilon_mu`. Uniform tube/gain certification may cost more than rollout/full Jacobian; pathwise safety does not identify free-running total effect.

Final verdict: **conditional mathematics accepted; no originality, same-budget advantage, semantic validity, empirical benefit or scientific admission established.** Counts remain 5 historical / 0 active / 0 admitted / 0 selected.
