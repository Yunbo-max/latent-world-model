# R20 v2 independent final-byte mathematical review

Reviewer: `/root/r20_math`. Assignment: independently verify the corrected exact-byte prefix-causal low-rank curvature artifact and unchanged screen, including the empirical-Fisher/GGN distinction, projected Woodbury derivation, both adversarial counterexamples, formula numbering, complexity, controls, and disposition. The reviewer did not author or modify repository files and did not run project/model code, tests, training, inference, scoring, or experiments.

- Artifact: `research/delta-discovery-2026-10-08/repairs/R20_PREFIX_CAUSAL_LOWRANK_CURVATURE.v2.md`
- Exact reviewed SHA256: `dfe5b8b1cde3c0798432411e76178f5dc87925cae4510856df1862c5a1cf367c`
- Screen: `research/delta-discovery-2026-10-08/repairs/R20_REPAIR_LINE_SCREEN.v2.md`
- Exact reviewed screen SHA256: `b70b3f7e1d8a80ccfa22975eaedf22f9177f98ce1813e75c8a5dbc09ae0c307b`
- Verdict: **PASS / conditional mathematics accepted / theorem-control only / park after substantive attempt 2 / zero candidate admission**.

## Supersession notice

The earlier FAIL review bound to artifact SHA256 `1fd846cd8c7cf7bb7ce353ff56c681c7f0bd13d8e2334bb7206eebae4e081c2c` remains historical and must not be used as the current review. The corrected bytes now qualify a generic observed loss-gradient outer product separately from the usual empirical Fisher for log-likelihood score/NLL gradients, and both adversarial constructions explicitly set the scalar target `e=1`.

## Independent mathematical check

With column-major `x=vec(X)`, `n=d_kd_v`, and `k!=0`, `A=I_(d_v) otimes k^T` has shape `d_v x n`, `AA^T=||k||^2I_(d_v)`, and `x0=A^T(AA^T)^(-1)e=vec(k e^T/||k||^2)` is the Euclidean minimum-norm feasible action. The displayed `P=I-A^T(AA^T)^(-1)A=I_(d_v) otimes (I-kk^T/||k||^2)` is the symmetric orthogonal projector onto `ker A`; therefore `Ax0=e`, `AP=0`, and `Px0=0`.

For `Hhat=lambda I+ZZ^T`, `lambda>0`, define `B=PZ`, `c=Z^Tx0`, and `C=lambda I+Z^TPZ=lambda I+B^TB`. Parameterizing feasible actions as `x=x0+u`, `u in ker A`, gives the tangent equation `lambda u+B(c+B^Tu)=0` and the unique solution `x*=x0-PZ C^(-1)c`. All dimensions agree. Feasibility follows from `AP=0`. Direct substitution gives `Z^Tx*=lambda C^(-1)c` and `Hhat x*=lambda x0+lambda(I-P)ZC^(-1)c in range(A^T)`, which is exactly the equality-constrained KKT condition. Strict convexity gives uniqueness.

Equations (11)--(12) are exact: `J*=lambda||x0||^2/2 + lambda c^TC^(-1)c/2` and `J(x0)-J*=c^T(Z^TPZ)C^(-1)c/2 >= 0`. The final inequality holds because `Z^TPZ` is PSD and commutes with `C=lambda I+Z^TPZ`.

For factored columns `z_j=w_j otimes p_j=vec(p_jw_j^T)`, equations (14)--(17) are dimensionally and algebraically correct. Every correction left factor is orthogonal to `k`, so the exact current-key constraint is preserved. The rank bound `rank(X*)<=min(d_k,d_v,r+1)` follows immediately.

The empirical-Fisher/GGN distinction is now scoped correctly. A GGN factor has columns `J_i^T C_i^(1/2)` and product `J_i^T C_iJ_i`. An arbitrary observed loss gradient yields a per-example gradient outer product `J_i^Tr_ir_i^TJ_i`; it is the usual empirical-Fisher object when the gradient is a log-likelihood score/NLL gradient, and it is not generally the GGN. The column-versus-row data-matrix warning is also correct.

Factoring the v1 witness `W=LL^T` and taking `z_j=l_j otimes p` gives `ZZ^T=W otimes pp^T`; equations (9)/(17) recover exactly `[[1,0],[-5/8,-1/8]]`. Thus v2 changes the information/solver structure, not the v1 objective or counterexample.

## Adversarial boundaries, complexity, and disposition

Both adversarial examples are complete. For `d_v=1,e=1,k=(1,1)` and stale curvature `diag(lambda+rho,lambda)`, the exact action tends to `(0,1)`; after curvature rotation, the future optimum tends to `(1,0)` and the stale optimum can be worse than Euclidean Delta. For `e=1,k=(1,epsilon)` and `rho >> lambda/epsilon^2`, the exact action tends to `(0,1/epsilon)` while normalized Delta remains bounded.

Formula numbering (1)--(21) is sequential. The factorized and unstructured cost accounts are sound and explicitly exclude, then separately charge, feature extraction. Edge cases, replay/staleness, nonfactorable gradients and full free-running dependence are retained. Prefix measurability establishes legality only, not future predictive validity or factual correctness.

M-FAC, SENG, WoodFisher, projected natural-gradient/online-Newton/RLS, rank-r Delta, constrained CG, L-BFGS and direct action-factor prediction cover the principal mechanism and budget controls. No regret, total-cost, native-measurement or empirical advantage is established. Retain R20 v2 as a conditional theorem/control, park after attempt 2, keep empirical effect unknown, and leave candidate counts unchanged.
