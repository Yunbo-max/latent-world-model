# R07 v2 independent final-byte mathematics review

- reviewer identity: `/root/r07v2_math`
- assignment: independent read-only review of final R07 v2 bytes; no integration/file write
- artifact: `research/delta-discovery-2026-10-08/repairs/R07_COUPLED_DIRECTIONAL_MARGIN.v2.md`
- exact SHA256: `4259fee0afb25db2624972efcbd7ed6658b5aec16af84163583b8c14b96fdee3`
- verdict: **PASS for the stated complete-state, fixed-policy/common-suffix, finite-horizon local directional theorem and debugging-control scope**

The reviewer re-read every current artifact byte after the final presentation fixes. The hash matches independently, the control-character scan is empty, and both `\qquad` commands render correctly.

Final checks:

1. With `x in R^n`, `d,z_j,w_j,lambda_j in R^n`, and `A_j,K_j,H_{ell,j} in R^{n x n}`, the Frobenius contraction `⟨G_S,beta k e^T⟩=beta k^T G_S e` is dimensionally correct for `S in R^{d_k x d_v}`.
2. The forward tangent `z_{j+1}=A_j z_j`, costate recursion, and equality `J'(0)=r'(0)+lambda_0^T d` have the correct order and signs. Explicit later action dependence is correctly identified as requiring `F_a`.
3. The second-tangent and reverse-Hessian recursions agree. The costate-weighted transition Hessian is required; the stated `2F_xa z+F_aa` additions are correct when suffix transitions depend explicitly on the action.
4. `q=-J'/2` and `h=J''/2` reproduce `-2qa+ha^2`. Equation (13) is a valid sufficient-decrease certificate from simultaneous Taylor bounds. Full write beats no-write exactly when `q>h/2` in the exact quadratic, for either sign of `h`.
5. The branch logic is complete: for `h>0`, use `clip(q/h,0,1)`; for `h<=0`, the constrained minimum lies at an endpoint. At `q=0`, the sign of `h` correctly decides sufficiently small positive actions.
6. In the affine fixed-reference limit, `J'(0)=2(c-Yb)` and `J''(0)=2h_Y`, so the v1 thresholds and truth/action counterexample are recovered.
7. The dynamics-curvature and indefinite-curvature examples have the stated signs. State omission, finite-horizon tail, nonsmooth routing, multiple-action cross terms, Bellman policy switching and free-running distribution shift remain explicit failure boundaries.
8. Equations (14)–(15) are the correct score-function first and second derivatives under the stated common domination, action-independent support, differentiability and interchange assumptions. Common-path derivatives are not called free-running causal effects.
9. The JVP/VJP/directional-second-order construction avoids materializing a dense Hessian but charges activation storage or recomputation and complete-state feedback. It does not infer a total-cost advantage from the rank-one injection.
10. Realized suffix quantities are retrospective/training objects unless replaced by simultaneously calibrated prefix-measurable bounds. Native joint measurement and empirical benefit remain unknown.

This review establishes conditional mathematical correctness only. It does not establish originality, prefix-time estimability, free-running identification, native measurement, empirical efficacy, or candidate admission. The collision with adjoint sensitivity, automatic differentiation, DDP/iLQR and Bellman policy evaluation supports the parked-control disposition and zero count increment.
