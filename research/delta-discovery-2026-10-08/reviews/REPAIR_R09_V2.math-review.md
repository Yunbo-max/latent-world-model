# R09 v2 independent final-byte mathematics review

- Reviewer: `/root/r09_v2_math`
- Artifact: `research/delta-discovery-2026-10-08/repairs/R09_DYNAMIC_PROTECTION_GRAMIAN.v2.md`
- Artifact SHA256: `aa78f4f15322ef501d14ce76d93e60e3544e2b07b16bebea7488eb308e11aacf`
- Assignment: independent read-only review; reviewer did not write the integrated artifact.
- Verdict: **PASS for the stated frozen/exogenous-suffix, rank-one/common-left-metric finite-horizon theorem/control; no candidate upgrade**.

## Checks

1. With `S,Delta S in R^{d x m}`, `x,k in R^d`, `e in R^m`, and `A,P,Q,G,H in R^{d x d}`, every constraint, propagation, trace, and inverse-metric expression is dimensionally valid.
2. `P_{t,h}=A_h...A_{t+1}` and `G_{j:H}=w_jQ_j+A_{j+1}^TG_{j+1:H}A_{j+1}` have the correct chronological/reverse noncommuting order.
3. For the declared left-side Euclidean value metric, substitution `Delta S=xe^T` yields `||e||^2 x^TGx`; the Lagrange optimum and minimum are correct for `mu>0,k!=0`.
4. The revised curvature scope is correct: retained rank one scalarizes each value-side factor to `e^TR_he`; after lifting to the general-matrix feasible set, varying `Q_h otimes R_h` can be nonseparable and higher rank.
5. The complete-state equation is a Gauss--Newton pullback, not mislabeled as the exact nonlinear Hessian. Costate-weighted dynamics curvature, linear/cross terms, free-running support changes, and omitted state remain explicit boundaries.
6. From `(1-epsilon)H preceq hat H preceq (1+epsilon)H`, the exact ratio and sharp Kantorovich bound `1/(1-epsilon^2)` are correct and explicitly attributed to R20 v3.
7. The swapped-anisotropy two-future construction has the correct feasible parameterization, unique minimax action `x=gamma k`, oracle cost, exact ratio `(M+m)^2/(4Mm)`, and randomization lower bound.
8. Full overwrite singularity, semidefinite/nullspace branches, semantic non-identifiability, and same-prefix impossibility are preserved.
9. Frozen row-space and complete-state storage/compute costs are now separated; the matrix-free path still pays horizon-wide batched JVP/VJP, injection, checkpoint/recomputation, tolerance, and calibration costs.

The final bytes establish only conditional mathematical correctness. They do not establish prefix estimability, semantic validity, free-running causal benefit, empirical efficacy, originality, or scientific admission. Attempt 2/3 parking and candidate delta zero are correct.
