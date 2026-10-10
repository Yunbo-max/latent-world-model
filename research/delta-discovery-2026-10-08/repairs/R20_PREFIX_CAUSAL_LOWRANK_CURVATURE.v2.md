# R20 v2 — prefix-causal low-rank curvature gives an exact constrained Delta solve

Status: **conditional theorem/control; substantive repair attempt 2; not an active D candidate**. This child preserves R20 v1 byte-for-byte and repairs its first deployment gap: the dense future-curvature oracle is replaced by a strictly prefix-measurable damped low-rank empirical curvature. The resulting solve is exact for the declared surrogate and can reproduce the v1 rank-two witness. It does **not** prove that past curvature predicts future harm, that the feature construction is cheaper than a direct action predictor, or that language-model behavior improves.

## 1. Parent problem, exact patch, and information law

Let

\[
X=\Delta S\in\mathbb R^{d_k\times d_v},\qquad X^\top k=e,
\]

with `k != 0`, and use column-major `x=vec(X)`, `n=d_k d_v`,

\[
A=I_{d_v}\otimes k^\top\in\mathbb R^{d_v\times n},\qquad Ax=e. \tag{1}
\]

R20 v1 allowed a dense local PSD operator which could depend on frozen future queries/Jacobians. The v2 patch instead declares a filtration `F_t` containing only the visible prefix and feedback legally available before write `t`, and constructs

\[
Z_t=[z_{t,1},\ldots,z_{t,r}]\in\mathbb R^{n\times r},\qquad
Z_t\ \text{is }\mathcal F_t\text{-measurable}, \tag{2}
\]

\[
\widehat H_t=\lambda I_n+Z_tZ_t^\top,\qquad \lambda>0. \tag{3}
\]

Columns may be retained prefix per-example **gradient** features, causal sketches, learned prefix features, or correctly factorized Jacobian curvature columns. These objects must not be conflated: a true GGN contribution has columns `J_i^T C_i^(1/2)` and satisfies `Z_i Z_i^T=J_i^T C_i J_i`, whereas a single observed gradient `g_i=J_i^T r_i` gives only the per-example gradient outer product `g_i g_i^T=J_i^T r_i r_i^T J_i` (the usual empirical-Fisher object when `g_i` is a log-likelihood score/NLL gradient), not a GGN contribution in general. Equation (2) defines features as columns; a data matrix that stores samples as rows would instead induce `Z^T Z`. Equation (2) forbids future suffixes, current/future answers not yet revealed, protected-fact validity oracles, and counterfactual outcomes of actions not taken. Causality makes the update deployable; it does not make `Hhat_t` an unbiased or calibrated estimator of the future-loss curvature. Any such transfer requires an additional stationarity, mixing, slow-drift, or explicit online-regret assumption.

The mathematical problem is

\[
\min_x\ \frac12x^\top\widehat H_t x\quad\text{subject to}\quad Ax=e. \tag{4}
\]

## 2. Exact projected Woodbury solution

Because `AA^T=||k||^2 I_(d_v)`, the Euclidean minimum-norm feasible point and the orthogonal projector onto `ker(A)` are

\[
x_0=A^\top(AA^\top)^{-1}e
=\operatorname{vec}\!\left(\frac{k e^\top}{\|k\|^2}\right), \tag{5}
\]

\[
P=I_n-A^\top(AA^\top)^{-1}A
=I_{d_v}\otimes\left(I_{d_k}-\frac{kk^\top}{\|k\|^2}\right). \tag{6}
\]

Thus `Ax0=e`, `AP=0`, `Px0=0`, and every feasible point is `x=x0+u` with `u in ker(A)`. Put

\[
B=PZ_t,\qquad c=Z_t^\top x_0,\qquad
C=\lambda I_r+Z_t^\top PZ_t=\lambda I_r+B^\top B. \tag{7}
\]

The tangent first-order condition is

\[
\lambda u+B(c+B^\top u)=0. \tag{8}
\]

Since `lambda>0`, `C` is positive definite. Solving (8) gives

\[
\boxed{x^\star=x_0-PZ_t(\lambda I_r+Z_t^\top PZ_t)^{-1}Z_t^\top x_0.} \tag{9}
\]

This is an exact equality-constrained low-rank solve, not an approximate inverse. Feasibility is immediate from `AP=0`. Moreover,

\[
Z_t^\top x^\star=\lambda C^{-1}c,\qquad
\widehat H_t x^\star
=\lambda x_0+\lambda(I-P)Z_tC^{-1}c\in\operatorname{range}(A^\top), \tag{10}
\]

so the KKT condition holds. Strict convexity makes the optimum unique.

The exact optimum and the improvement over normalized ordinary Delta `x0` are

\[
J^\star=\frac\lambda2\|x_0\|^2+\frac\lambda2c^\top C^{-1}c, \tag{11}
\]

\[
J(x_0)-J^\star
=\frac12c^\top\!\left[I-\lambda C^{-1}\right]c
=\frac12c^\top(Z_t^\top PZ_t)C^{-1}c\ge0. \tag{12}
\]

Thus the correction is nonzero only when the stored curvature coordinates overlap both the base edit (`c != 0`) and a feasible tangent direction (`PZ_t != 0`).

## 3. Factorized features and an implementable matrix form

Suppose each causal feature is stored as

\[
z_j=w_j\otimes p_j=\operatorname{vec}(p_jw_j^\top),
\quad p_j\in\mathbb R^{d_k},\ w_j\in\mathbb R^{d_v}. \tag{13}
\]

Then

\[
Z_tZ_t^\top=\sum_{j=1}^r(w_jw_j^\top)\otimes(p_jp_j^\top), \tag{14}
\]

which is the low-rank nonseparable query×value curvature family missing from the single-Kronecker cancellation in R20 v1. Define

\[
\bar p_j=\left(I-\frac{kk^\top}{\|k\|^2}\right)p_j. \tag{15}
\]

The small Gram and right-hand side are

\[
G_{ij}=(w_i^\top w_j)(\bar p_i^\top\bar p_j),\qquad
c_j=\frac{(w_j^\top e)(p_j^\top k)}{\|k\|^2}. \tag{16}
\]

After solving `(lambda I_r+G) alpha=c`, the exact edit is

\[
\boxed{X^\star=\frac{k e^\top}{\|k\|^2}
-\sum_{j=1}^r\alpha_j\bar p_jw_j^\top.} \tag{17}
\]

Each correction has `bar(p)_j^T k=0`, so it changes other-query responses without spoiling the exact current-key correction. Also

\[
\operatorname{rank}(X^\star)\le\min(d_k,d_v,r+1). \tag{18}
\]

No dense `n x n` matrix or projector is needed. Projecting features costs `O(r d_k)`; forming the two factor Grams and their Hadamard product costs `O(r^2(d_k+d_v))`; the SPD solve costs `O(r^3)` time and `O(r^2)` state. The edit can remain as `r+1` rank-one factors with `O(r(d_k+d_v))` state and per-query application `O(r(d_k+d_v))`, or be materialized in `O(r d_kd_v)` time. These counts exclude the cost of obtaining each `p_j,w_j`; that cost is part of the method and may dominate.

For unstructured `Z`, state is `O(nr)`, the Gram costs `O(nr^2)`, and the low-rank representation may be unattractive. When `r` is large, a primal/nullspace constrained iterative solve can be cheaper than the dual `r x r` solve.

## 4. Old counterexample recheck

The v1 witness has `lambda=1`, `k=e=(1,0)^T`, `p=(1,1)^T`, and

\[
H=I_4+W\otimes pp^\top,
\qquad W=\begin{bmatrix}2&1\\1&2\end{bmatrix}. \tag{19}
\]

Factor `W=LL^T` and take the two columns `z_j=l_j otimes p`. Then `ZZ^T=W otimes pp^T`, `r=2`, and (9)/(17) gives exactly

\[
X^\star=\begin{bmatrix}1&0\\-5/8&-1/8\end{bmatrix}. \tag{20}
\]

So v2 does not delete the old rank-two counterexample or change its objective. It supplies a compact representation and exact solve for it. What remains unsupported is whether a legal prefix supplies those two correct factors before the write.

## 5. Predictions, failure boundaries, and controls

Conditional, falsifiable predictions:

1. Relative to normalized Delta, improvement in the declared surrogate is exactly (12); it vanishes if `PZ=0` or `Z^T x0=0`.
2. The v1 rank advantage is recoverable with `r` at least the factor rank of the coupled curvature; too small a sketch loses it.
3. Under stable prefix-to-future curvature transfer, causal factors should improve future protected-query quadratic loss most when `G` has well-conditioned tangent directions coupled to `c`.
4. Under abrupt distribution or factual-validity shift, prefix curvature can point in the wrong direction even though (9) exactly minimizes the stale surrogate.

Failure and edge boundaries:

- `k=0,e!=0` is infeasible; `k=0,e=0` makes the constraint vacuous and `X=0` optimal, but formulas (5)--(6) are undefined.
- `e=0`, empty `Z`, `PZ=0`, or `Z^T x0=0` returns `X=0` or normalized Delta as appropriate.
- `lambda=0` can destroy coercivity and uniqueness; pseudoinverse range conditions are then required.
- Duplicate/dependent features are harmless for the solve because `C >= lambda I`, but waste state.
- Causal empirical Fisher/GGN factors estimate a declared past surrogate, not semantic truth, fact freshness, source identity, or the counterfactual future loss of an unchosen action.
- Saving old features is causal but they become stale as the model/state changes; recomputing current Jacobians on old examples needs replayed inputs/targets and backward/JVP/VJP cost. Neither path is free.
- A factorized feature assumption is a storage/computation restriction; arbitrary per-example gradients need not factor as one `w otimes p` without approximation.
- Full free-running future keys, gates, routing and updater state depend on the edit; this local surrogate does not replace the complete-state Jacobian results already in Step2.

Two exact adversarial boundaries show why surrogate optimality is not a future guarantee. First take `d_v=1,d_k=2`, scalar target `e=1`, `k=(1,1)`, and the stale feature `Z=sqrt(rho)(1,0)^T`. Then

\[
\widehat x=\frac{(\lambda,\lambda+\rho)^\top}{2\lambda+\rho}\longrightarrow(0,1)^\top. \tag{21}
\]

If future curvature has rotated from `diag(lambda+rho,lambda)` to `diag(lambda,lambda+rho)`, the future-optimal action tends to `(1,0)` while Euclidean Delta is `(1/2,1/2)`: the exact stale-surrogate minimizer can be worse than the simple baseline. Duplicate correlated features also scale `rho` and can create spurious rigidity unless normalization/forgetting is declared; those heuristics do not identify validity.

Second, again take scalar target `e=1`, with `k=(1,epsilon)` and the same stale protected first coordinate. If `rho >> lambda/epsilon^2`, the exact constrained action approaches `(0,1/epsilon)`, while Euclidean Delta has bounded norm. A trust region, damping lower bound or condition/norm rejection test is therefore a necessary safety control near protection--overwrite singularity; exact Woodbury algebra does not prevent the blow-up.

Strong same-information controls are: no-write and normalized Delta; diagonal/RMS/EWC-style empirical Fisher; hard `Z^T x=0` projection with a feasibility test; projected natural gradient/online Newton/RLS; K-FAC, Shampoo and sketched covariance; rank-`r` or `r` sequential Delta writes; matched-state L-BFGS (a compact-curvature control, not automatically equation-identical); a projected or nullspace constrained-CG solve; and a direct prefix network predicting the `r+1` action factors. The comparison must charge feature/Jacobian extraction, replay, sketch/window updates, Gram construction, solve, stored bytes, and query-time application. Formula (9) has no certified total-cost or regret advantage over these controls, and it is unfair to give only v2 backward/Jacobian information.

## 6. Measurement and disposition

Existing bAbI, LAMBADA, RULER, BABILong and LongMemEval endpoints can observe downstream prediction/retrieval but do not natively expose `Z`, future curvature, the constrained optimum, or a paired same-state counterfactual. CITB/TRACE provide continual-learning retention/transfer endpoints but operate primarily at parameter-update/task-sequence level and likewise do not label the fast-state curvature target. Internal KKT residual, surrogate gain (12), factor rank and curvature-transfer error would require derived instrumentation, not a claimed native benchmark outcome. No benchmark, label, metric or result was fabricated; no scorer or model was run.

M-FAC's pinned author implementation already maintains a sliding matrix of recent gradients and applies the inverse of a damped empirical Fisher via a small Gram/Woodbury computation. SENG implements sketched empirical-natural-gradient preconditioning, and WoodFisher recursively builds a damped empirical-Fisher inverse from gradient outer products. R20 v2 adds an exact Delta equality constraint and a factorized matrix-action form, but these are a standard projected low-rank quadratic consequence, not enough for method novelty. The prefix-vs-future transfer premise and matched-cost advantage remain open.

**Decision:** conditional mathematics accepted; park after substantive attempt 2 with zero candidate increment. Reopen the final allowed attempt only with (i) a lawful prefix-to-future approximation/regret guarantee under checkable assumptions, or (ii) a native measurable same-budget advantage over rank-`r` Delta, projected CG and direct action-factor prediction. Empirical effect remains unknown.
