# R20 v1 independent final-byte mathematical rereview

Reviewer: `/root/r20_math`. Assignment: independently verify the corrected exact-byte R20 artifact and unchanged screen, including dimensions, KKT/Schur solution, separable cancellation, the complete 2x2 witness, structural range/rank bound, simultaneous diagonalization, costs, controls, and failure boundaries. The reviewer did not author repository bytes, modify files, or run project/model code, tests, training, inference, scoring, or experiments.

- Artifact: `../repairs/R20_NONSEPARABLE_CURVATURE_EDIT.v1.md`
- Exact reviewed SHA256: `481880030ff3ac535bc6137320bfc3939007e8efb9a1c8838df1d962e813f33e`
- Screen: `../repairs/R20_REPAIR_LINE_SCREEN.md`
- Exact reviewed screen SHA256: `d13fd7abcc42f2b3af25472f5f448691459abb42d1b995ab3304ddec2164d24a`
- Verdict: **PASS / conditional mathematics accepted / theorem-control only / park / zero candidate admission**.

Any review bound to the earlier artifact SHA256 `11abeb7e491954ef5992b282b2d84166203b4a4a3df54ae9a009dc919a26cad8` is stale. It repeated the incorrect witness multiplier `(13/8,0)`; the corrected bytes and this rereview use `(13/8,1/8)`.

With column-major `x=vec(X)`, `A=I_(d_v) otimes k^T` has the declared shape and satisfies `Ax=X^T k`. Symmetric PSD `W_u` and `lambda>0` give the stated SPD operator. For `k!=0`, `A` has full row rank, so the KKT/Schur solution and optimal value in equation (8) are unique and correct. Projecting the matrix KKT equation onto `span{k,p_1,...,p_U}^perp` proves the range and rank bound.

For a fully separable metric `H=W otimes G`, direct Kronecker algebra cancels the right factor and gives `X*=G^(-1)k e^T/(k^T G^(-1)k)`. For `e!=0`, every feasible rank-one matrix can be rescaled to `X=ae^T`, `k^Ta=1`; the revised text correctly compares this class with the unrestricted-rank constrained optimum.

For the witness,

`H=[[3,2,1,1],[2,3,1,1],[1,1,3,2],[1,1,2,3]]`,

`x*=(1,-5/8,0,-1/8)^T`, and `A=[[1,0,0,0],[0,0,1,0]]`. Direct multiplication gives

`Hx*=(13/8,0,1/8,0)^T=A^T(13/8,1/8)^T`,

and `Ax*=e`. Thus `det(X*)=-1/8`, `rank(X*)=2`, and `J*=13/16`. Ordinary normalized Delta has value `3/2`; the best feasible rank-one edit has second row `(-2/3,0)`, value `5/6`, and strict excess `1/48`. All final-byte witness claims agree.

The simultaneous-output-eigenbasis decomposition follows by `Z=XU`, `r=U^Te`; active modes separate with `G_j=lambda I+sum_u w_(uj)p_up_u^T`. Higher rank occurs only when active normalized left directions are noncollinear, so nonseparability is not overclaimed as sufficient.

The Step2 subsumption statement is accurate: its general local edit coordinate can be `u=vec(X)`. R20 contributes the exact equality-constrained action, separable-cancellation boundary and rank-gap witness, not a new curvature family. Dense and structured costs, nullspace/Schur routes, iterative residual obligations, rank-r controls, frozen-path scope, missing linear term for a nonstationary true loss, indefinite-Hessian boundary, and causal/semantic information gaps are correctly recorded.

The corrected bytes establish a valid but narrow theorem/control. Generic constrained quadratic/GGN machinery, Step2's general coordinate, and rank-r/iterative/direct-prediction controls prevent candidate admission. Park after attempt 1, keep empirical effect unknown, and retain counts `5 historical / 0 active / 0 scientifically admitted / 0 selected`.

