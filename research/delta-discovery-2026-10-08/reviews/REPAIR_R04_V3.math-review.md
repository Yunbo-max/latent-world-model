# Independent math review — R04 v3

- Reviewer: `/root/r04_v3_math_review`
- Assignment: independent read-only rederivation of R04 v3 final bytes
- Artifact: `research/delta-discovery-2026-10-08/repairs/R04_CONSOLIDATION_DYNAMICS.v3.md`
- Final artifact SHA256: `eb4ddfd81c947bf6fc176a1863f1618f3d095fc2366850c9964f0524384d8093`
- Boundary: no file edits by reviewer; no project/author code, model, test, training, inference or scoring execution
- Verdict: **PASS conditional mathematics; not a candidate/originality/empirical verdict**

## Independent rederivation

1. With column-stacked `vec`, `B_s,B_f` have shape `dm x p`, `T_T` has shape `dm x p`, and `(I_m tensor q_i^T)T_i=L_i` has shape `m x p`. The vectorization and output map are consistent.
2. Starting from the v2 difference recurrence gives `delta W_t=A_t delta W_{t-1}+E_t(I-D_t)C_s` and `delta W_0=C_s-C_f`. Ordered expansion yields the two terms in Eq.(3); exact interface matching removes only the initial mismatch term and gives Eq.(4).
3. Expanding Eq.(5) gives `z^T K z+2g^Tz`. Because `lambda>0` and `H_0` is positive definite, `K` is positive definite, so Eq.(7) and improvement `-g^T K^{-1}g` are correct.
4. For an orthonormal null-space basis `N`, Eq.(8) is the correct restricted normal equation. The conditioning statement is then basis meaningful.
5. Direct scalar differentiation reproduces Eq.(9). With `z in [0,1]`, positive migration occurs exactly when `p>alpha^T`. The multi-horizon sign in Eq.(11) is correct for nonnegative weights.
6. The still-valid/obsolete worlds are now correctly separated: without regularization their actions are `1/0`; with positive regularization they are positive shrinkage/zero.
7. The distinguishing prediction was repaired: a factorized gate is guaranteed worse only when it changes the Bayes action on a positive-probability conditional set. Correlation alone need not change the action.
8. The normal equation is exact only for a fixed conditional joint law. If the action changes future queries or feedback arrival, it is explicitly scoped as a frozen-law surrogate.

## Corrections required and applied before PASS

- Replaced the incorrect claim that the regularized still-valid world requires `z=1`.
- Added the fixed conditional-law assumption, column-stacked `vec`, orthonormal protection basis and nonnegative horizon weights.
- Removed the implication that the scalar threshold is Delta-specific.
- Weakened the prediction from “dependence implies strict advantage” to the correct Bayes-action-change condition.

## Unclosed conditions

- Full nonlinear closed-loop comparison requires complete state Jacobian/score terms.
- A local slow-parameter Jacobian does not guarantee finite-edit representability.
- Estimating `G,g` requires legal future feedback; observational logs require overlap/randomization or sequential identification assumptions.
- Approximate low-rank/diagonal/iterative solves have unquantified conditioning and direction error.
- `p>alpha^T` is a generic survival decision boundary instantiated in this Delta interface, not standalone novelty.
- Originality, native mechanism measurement and effect remain unverified.

Disposition supported by review: park R04 after its third bounded repair; no active/scientific/selected candidate increment.
