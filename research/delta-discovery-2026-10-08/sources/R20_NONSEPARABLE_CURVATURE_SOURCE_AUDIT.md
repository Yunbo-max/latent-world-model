# R20 nonseparable-curvature source, collision, and measurement audit

Read 10 October 2026. This is a bounded primary-source and fixed-interface audit, not a field-wide originality certificate. No implementation was run.

## 1. General curvature and tensor-preconditioning neighbors

Martens and Grosse, **Optimizing Neural Networks with Kronecker-factored Approximate Curvature**, ICML 2015, PMLR 37:2408--2417, approximate layerwise Fisher blocks by Kronecker products of activation and derivative factors and exploit the factorization for efficient inverse action. This is a decisive principle-level neighbor for two-sided query/value curvature. Under R20's exact all-output constraint, however, a *single* separable Kronecker factor cancels on the output side, as equation (13) shows; K-FAC does not by itself establish the nonseparable higher-rank constrained action.

Primary: <https://proceedings.mlr.press/v37/martens15.html>.

Author-maintained implementation pin: `tensorflow/kfac@ddad6375bbdebfae809bccfd3a5c3db073128764`; `kfac/python/ops/fisher_factors.py` exposes Fisher-factor covariance/inverse infrastructure and `kfac/python/ops/optimizer.py::KfacOptimizer` exposes the optimizer. The repository is now archived and is evidence for an author-maintained K-FAC interface, not necessarily the exact 2015 release bytes.

Gupta, Koren and Singer, **Shampoo: Preconditioned Stochastic Tensor Optimization**, ICML 2018, PMLR 80:1842--1850, maintains preconditioners along tensor modes rather than flattening the tensor. It is a strong separable/tensor-mode control and makes a generic claim of “left and right curvature” non-novel. It does not turn the R20 KKT witness into a Delta-specific method.

Primary: <https://proceedings.mlr.press/v80/gupta18a.html>.

The bounded search did not locate a reliably pinnable 2018 original author repository. A later author-related scalable implementation is fixed at `google-research/google-research@6e6b1ff7471be7ed884ff7ce0821c889a3a1b0c9`, `scalable_shampoo/jax/shampoo.py::{Preconditioner.statistics_from_grad,Preconditioner.preconditioned_grad,matrix_inverse_pth_root,Shampoo}`. Its file corresponds to the later scalable-Shampoo work and is not misrepresented as the original 2018 implementation.

The KKT/Schur-complement formula in R20 equation (8) is standard equality-constrained strictly convex quadratic optimization. R20 does not claim the solver, generalized natural-gradient projection, conjugate-gradient route, or Woodbury route as original.

Simoncini, **Computational Methods for Linear Matrix Equations**, SIAM Review 58(3), 2016, treats `AXE+DXB=C`, the identity `vec(AXB)=(B^T otimes A)vec(X)`, and multi-term equations `sum_i A_i X B_i=C`, together with projection/Krylov and low-rank-right-hand-side solvers. Consequently `lambda X + sum_u p_up_u^T XW_u = k mu^T` is a symmetric positive-definite multi-term generalized Sylvester equation, not a new numerical primitive.

Primary author PDF: <https://www.dm.unibo.it/~simoncin/sirev58-3_377.pdf>; DOI: <https://doi.org/10.1137/130912839>.

**CrispEdit, arXiv:2602.15823v2 / ICML 2026.** Its capability-preservation curvature and K-FAC eigenbasis projection are a major functional collision: full/Gauss--Newton-style capability curvature is compressed into activation/output factors, a nonseparable spectral mask acts on a matrix gradient, and sequential edits update cached curvature. It is parameter editing rather than a Delta fast-state exact-interpolation solve, so it is not equation-for-equation identical; it nevertheless removes any broad claim that output-sensitive curvature plus higher-rank matrix projection is new.

Pinned author repository `zarifikram/CrispEdit@09035f16695998f3a71ec6006245d99e8cc648c8`, inspected without execution. `crispedit.py::execute_ft` and `execute_ft_sequential` call `calculate_cov_cache_with_old_data`, `build_optimizer_with_cov_caches`, and cache refreshes. `easyeditor/models/crispedit/utils.py` blob `444eda1d82fcb0a321bec481a9cee8ed1b21f3d4` exposes the K-FAC `A/B` caches, eigenbasis/mask construction and optimizer assembly. `easyeditor/models/crispedit/projected_adam.py` blob `c9ebe09b86a590ac15c211b59a68b3ccb6f312e5` applies `U_B ((U_B^T grad U_A) odot M^T) U_A^T` before the Adam step and reprojects momentum after cache reset. This is static interface evidence, not a reproduction.

Paper: <https://arxiv.org/abs/2602.15823>.

## 2. Delta-family fixed interfaces

**Preconditioned DeltaNet (PDN), arXiv:2604.21100v1.** The paper's section 3 derives historical least squares with key Gram `G_t`, cross-covariance `C_t`, inverse `P_t`, and a Sherman--Morrison/preconditioned write-key update. The exact update is still one outer product with a key-side write direction. The practical path uses a diagonal stable preconditioner, which must not be conflated with the paper's non-diagonal inverse-Gram theory.

Pinned author commit: `ntumm120/preconditioned-deltanet@7bd753279af87b39114149a104c5bde9bf67145f`. Inspected interfaces already fixed in this packet: `3rdparty/flash-linear-attention/fla/ops/precond_gated_delta_rule/naive.py::naive_recurrent_precond_gated_delta_rule` and `fused_recurrent.py`. The recurrent autograd backward in the latter raises `NotImplementedError`; a separate chunk path exists. Static reading only.

Paper: <https://arxiv.org/abs/2604.21100>.

**Gated KalmaNet (GKA), arXiv:2511.21016v3.** The paper presents ridge/Kalman-style sufficient statistics and a finite Chebyshev approximation to the query solve. It is not an explicit exact dense Kalman inverse at every token.

Pinned author commit: `awslabs/hybrid-model-factory@774c1048afd826e35b9222a7116ffd0fc50bcad6`. Under `training/src/hmf/model/hybrid_zoo/layers/gated_kalmanet/ops/chebyshev/`, `gka_chebyshev_solve.py` exposes `latent_chebyshev`, `gka_chebyshev_gla`, and `torch_decoding_one_step`; `chebyshev_iteration.py` exposes `ChebyshevIteration`. These are query-solve/statistics controls, not a released R20 edit solver.

Paper: <https://arxiv.org/abs/2511.21016>.

**QED and Gated DeltaNet-2.** The packet's full-formula/code audits establish that both keep the left write direction `k`: QED changes the erase/read covector; GDN2 uses value-side erase/write gating but writes a rank-one update along `k`. They are controls for richer erase/value logic, not evidence that the R20 nonseparable KKT action is useful. See `QED_FULL_FORMULA_CODE_AUDIT_2026-10-09.md` and `PRIMARY_NEW.md` for exact paper/code pins and functions.

**DeltaProduct.** The fixed FLA interface at commit `a7880060012c862d58575ee23f613cafcd728d03`, `fla/layers/gated_deltaproduct.py::GatedDeltaProduct.forward`, expands a token into ordered learned rank-one microsteps. It is the strongest direct representation control because every rank-`r` R20 action can be decomposed into `r` rank-one writes. The separate authors' repository is fixed at `automl/DeltaProduct@d62241a81d07aa32b1b65e7d17377f6a7cd0a5d8` in the R11 audit.

## 3. What is actually distinct

The source-backed residual is narrow:

1. R09/PDN/D03 left-side curvature and a single separable two-sided factor produce the normalized rank-one exact edit.
2. A sum of differently oriented query and value factors can make the exact constrained optimum rank two or higher.
3. The R20 2-by-2 witness provides an exact best-rank-one excess `1/48`, so the effect is not removable by retuning a rank-one direction.

The witness's data-curvature contribution is one separable term; its nonseparability comes from the **sum** `lambda I + W otimes pp^T`. Thus the gap can be read as an exact isotropic-damping/curvature mismatch boundary and is not evidence for a newly observed query×value mechanism. More broadly, the Step2 recursive random-metric control already allows a general edit coordinate; taking `u=vec(X)` subsumes this local quadratic family. R20 contributes the exact equality-constrained action and rank-gap witness, not a new curvature family.

This is a scoped mathematical debugging result, not an originality-certified optimizer or architecture. Generic GGN/natural-gradient, K-FAC/Shampoo, KKT projection, multiple rank-one writes and direct low-rank action prediction cover the principal mechanism and alternatives. No source located in this bounded audit supplies a cheap prefix-causal R20 curvature estimator together with a matched-budget advantage, but absence from this search is not proof of absence.

## 4. Measurement feasibility and gap

- bAbI exposes synthetic answers/supporting facts, not `H`, KKT residuals or optimal edit rank.
- LAMBADA exposes final-word likelihood/accuracy, not edit curvature or paired actions.
- RULER/BABILong stress long-context retrieval, not a query×value Hessian oracle.
- LongMemEval exposes knowledge-update QA and evidence spans but not an internal optimal action, protected-query curvature, or same-state rank-one versus rank-r counterfactual.
- CITB exposes parameter-level continual-instruction-learning task matrices and aggregate retention/transfer signals such as BWT/FWT; these are endpoint task metrics, not fast-state curvature, KKT rank, or paired same-state action labels. FWT is not itself a same-budget sample/compute learning-speed certificate.
- TRACE exposes parameter-level task-sequence retention/general-capability endpoints including backward-transfer-style summaries. Its original multi-task large-model setting and judge-dependent components carry substantial resource/evaluation cost, and it still has no native `H`, exact-edit rank, or paired action counterfactual.

A future study could derive internal diagnostics from a model, but those would be newly instrumented measurements and cannot be called native benchmark fields. The strongest feasible native outcome comparison would be downstream task quality at matched total state/FLOPs against Delta, rank-r/multi-step Delta, PDN/GKA-style controls and a direct action predictor. This Web/math phase did not design a full executable experiment or run a scorer.

## 5. Audit disposition

The mathematics is worth retaining because it precisely limits R09's representer theorem and distinguishes separable from genuinely coupled curvature. The general machinery and strongest controls are already known, the dense cost is prohibitive, prefix-causal estimation is absent, and native mechanism measurement is missing. Therefore R20 is a parked conditional theorem/control with candidate delta zero and empirical status unknown.
