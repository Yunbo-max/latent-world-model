# R20 v1 — nonseparable query×value curvature can force a higher-rank exact Delta edit

Status: **conditional theorem/control; parked after substantive attempt 1; not an active D candidate**. This versioned child repairs an assumption boundary in R09/D03. R09's rank-one theorem remains correct for a left metric, and even a single separable two-sided metric reduces to the same form. R20 shows what changes for a nonseparable sum of query- and value-curvature factors. It does not provide a causal estimator of that curvature, a cheaper algorithm, factual-validity evidence, or an experiment.

## 1. Formal object and patch

Let the key-by-value state edit be

\[
X=\Delta S\in\mathbb R^{d_k\times d_v},
\qquad X^\top k=e, \tag{1}
\]

where `k != 0` and `e` is the desired current residual correction. With column-major `x=vec(X)` define

\[
A=I_{d_v}\otimes k^\top,
\qquad Ax=e. \tag{2}
\]

R09 minimizes a left-metric displacement. R20 instead takes the locally quadratic displacement energy

\[
J(X)=\frac12\langle X,\mathcal H(X)\rangle_F,
\qquad
\mathcal H(X)=\lambda X+\sum_{u=1}^U p_up_u^\top XW_u, \tag{3}
\]

where `lambda>0`, `p_u in R^(d_k)`, and each symmetric `W_u` is positive semidefinite. In vector form,

\[
H=\lambda I_{d_kd_v}+\sum_u W_u\otimes(p_up_u^\top)\succ0. \tag{4}
\]

The `p_u` can be frozen future query/Jacobian directions and the `W_u` output-space GGN factors. That interpretation is only a local/frozen-path construction; equation (3) is the actual mathematical object.

## 2. Exact constrained solution

For

\[
\min_x\ \frac12x^\top Hx\quad\text{subject to}\quad Ax=e, \tag{5}
\]

the KKT equations are

\[
Hx=A^\top\mu,\qquad Ax=e. \tag{6}
\]

Because `H` is positive definite and `A` has full row rank when `k != 0`,

\[
M=AH^{-1}A^\top\succ0. \tag{7}
\]

Indeed `A^T z=z\otimes k` is nonzero for every nonzero `z`. Therefore the unique optimum and its value are

\[
\boxed{x^\star=H^{-1}A^\top(AH^{-1}A^\top)^{-1}e},\qquad
\boxed{J^\star=\frac12e^\top(AH^{-1}A^\top)^{-1}e}. \tag{8}
\]

Equation (8) is a Schur-complement equality-constrained quadratic projection. It is not presented as a new optimizer.

The solution has a finite structural range. Let

\[
\mathcal U=\operatorname{span}\{k,p_1,\ldots,p_U\}. \tag{9}
\]

Projecting the matrix KKT equation `Hcal(X*)=k mu^T` onto `U^perp` leaves `lambda X_perp=0`; hence every column of `X*` lies in `U`, and

\[
\operatorname{rank}(X^\star)\leq\min(d_v,d_k,U+1). \tag{10}
\]

This bound does not make the solve cheap: the output directions can still be coupled.

## 3. Why separable curvature does not repair R09

Suppose the entire metric is one Kronecker product

\[
H=W\otimes G,qquad W\succ0,\ G\succ0. \tag{11}
\]

Then

\[
AH^{-1}A^\top=(k^\top G^{-1}k)W^{-1}, \tag{12}
\]

and substitution in (8) cancels `W`:

\[
\boxed{X^\star=
\frac{G^{-1}k}{k^\top G^{-1}k}e^\top.} \tag{13}
\]

Thus a separable two-sided/K-FAC coordinate change is still rank one under the exact all-output constraint. R09 is the `W=I` case. Merely adding a right preconditioner, without nonseparable curvature or a different constraint, is not a repair.

For `e != 0`, every feasible rank-one matrix must have the form

\[
X=ae^\top,\qquad k^\top a=1. \tag{14}
\]

Therefore rank one is optimal exactly when the unrestricted-rank **constrained** optimum has the form `X*=ae^T` with `k^T a=1`. Nonseparability permits but does not by itself guarantee higher rank.

## 4. Minimal exact rank-two witness

Take

\[
d_k=d_v=2,\quad k=(1,0)^\top,\quad e=(1,0)^\top,
\quad p=(1,1)^\top,\quad
W=\begin{bmatrix}2&1\\1&2\end{bmatrix},\quad\lambda=1. \tag{15}
\]

The constraint fixes the first row of `X` to `e^T`; write the second row as `y^T`. Then

\[
J(y)=\frac12(1+\|y\|_2^2)
+\frac12(e+y)^\top W(e+y). \tag{16}
\]

Stationarity gives

\[
(I+W)y=-We,
\qquad y^\star=(-5/8,-1/8)^\top. \tag{17}
\]

Hence

\[
X^\star=\begin{bmatrix}1&0\\-5/8&-1/8\end{bmatrix},
\qquad \det X^\star=-1/8,
\qquad J^\star=13/16. \tag{18}
\]

The unique optimum has rank two. Direct substitution gives `Hx*=A^T(13/8,1/8)^T` and `Ax*=e`.

The ordinary normalized Delta edit `X_Delta=[[1,0],[0,0]]` has objective `3/2`, an excess `11/16`. More strongly, any feasible rank-one edit has second row `(a,0)`; minimizing over `a` gives `a=-2/3`, objective `5/6`, and a strict best-rank-one excess

\[
J_{\rm rank1}-J^\star=\frac1{48}. \tag{19}
\]

The witness therefore rules out the explanation that a different rank-one scaling always absorbs value-coupled curvature.

## 5. A computable special case and the general cost

If all `W_u` are simultaneously orthogonally diagonalizable,

\[
W_u=U\operatorname{diag}(w_{u1},\ldots,w_{ud_v})U^\top, \tag{20}
\]

put `Z=XU` and `r=U^T e`. The problem splits into output modes with

\[
G_j=\lambda I+\sum_u w_{uj}p_up_u^\top,
\qquad
z_j^\star=r_j\frac{G_j^{-1}k}{k^\top G_j^{-1}k}. \tag{21}
\]

Different active modes produce higher rank precisely when their normalized vectors `G_j^(-1)k` are not collinear. This is an exact intermediate construction, not an approximation.

For general noncommuting dense `W_u`, let `n=d_kd_v`. A dense representation costs `O(n^2)` state and a direct factorization `O(n^3)`. A structured Hessian-vector product

\[
Y\mapsto\lambda Y+\sum_up_up_u^\top YW_u \tag{22}
\]

costs approximately `O(U(d_kd_v+d_v^2))` with dense `W_u`, plus storage for the factors. One can solve a nullspace SPD system on `(d_k-1)d_v` variables, or apply `H^(-1)` to the `d_v` Schur right-hand sides and solve a `d_v`-dimensional Schur system. Low-rank `W_u` admits Woodbury structure, but its advantage disappears as the aggregate value rank grows. Approximate iterative solves must report both KKT and constraint residuals.

The result is not an economical updater by itself. A rank-`r` solution is also a sum of `r` rank-one writes, so multi-step Delta/DeltaProduct is a direct matched-information representation control.

## 6. Old-result recheck, predictions, and failure boundaries

Preserved conclusions:

- R09's inverse-left-metric representer theorem is correct in its declared separable scope.
- D03's future-response/GGN interpretation is a strong principle-level neighbor. More strongly, the Step2 recursive random-metric control already permits a general edit coordinate `u`; taking `u=vec(X)` subsumes the full local quadratic family. R20 adds only the exact equality-constrained action and the rank-gap witness, not a new curvature family.
- R17 already records a value-coupled Gram for quotient/decodability. R20 changes the question to a minimum-curvature exact edit; it does not recertify R17 as a method.
- For any probe `q`, `Delta o(q)=q^T X` remains exact. Unlike rank-one Delta, a higher-rank action can change different output directions at different queries rather than keeping every response in `span(e)`.

Conditional predictions:

1. The gap from rank-one controls should track heterogeneity of normalized output-mode directions, not key-Gram conditioning alone.
2. The gap vanishes for isotropic/separable value curvature or when every active output mode yields a collinear normalized direction.
3. A rank-`r` factorization with enough left directions can match the dense oracle; rank one cannot match the witness in (15)--(19).
4. Any claimed benefit must survive same-information rank-`r` Delta, constrained CG, and a direct action predictor at matched total state and FLOPs.

Failure boundaries:

- `d_k=1`, `d_v=1`, `e=0`, or collinear modal directions give no rank benefit;
- `lambda=0` requires range conditions and pseudoinverses and may lose uniqueness;
- a true local loss with nonzero current gradient also has a linear term; the pure quadratic is exact only for a displacement-energy objective or under an appropriate stationary/zero-cross-term condition;
- frozen `p_u,W_u` omit the dependence of future keys, gates, routing and updater state on `X`; full free-running differentiation may change the operator;
- an exact Hessian can be indefinite, whereas the GGN/PSD object in (3) is a local surrogate;
- no deployment-time future target, truth oracle, protected-fact label or revision-validity label is licensed by this derivation;
- higher mathematical rank alone does not imply better language-model behavior.

## 7. Controls, measurement, and disposition

Strong same-information controls are ordinary normalized Delta; R09/D03/PDN left-preconditioned rank-one edits; a single Kronecker/K-FAC or Shampoo-style separable preconditioner; rank-`r` or multiple sequential Delta writes including DeltaProduct; a matrix-free constrained-CG/Schur oracle; and a direct predictor of `X` or its low-rank factors. PDN's full theory modifies the key-side inverse Gram and its practical implementation is diagonal; GKA maintains `H/U` statistics and uses a finite Chebyshev query solve; QED and GDN2 retain a single left write direction `k`. None of these facts makes R20's dense action useful.

The fixed bAbI, LAMBADA, RULER, BABILong and LongMemEval endpoints can measure downstream prediction or retrieval but do not expose the true operator `H`, an optimal KKT edit, a rank-gap label, or paired same-state actions. CITB and TRACE add continual-learning task-sequence endpoints such as retention/transfer/BWT/FWT or general-capability deltas, but concern parameter-level continual learning and still do not expose a fast-state `H`, KKT/rank necessity, or paired same-state action. TRACE's original multi-task, large-model and judge components also make it a costly endpoint rather than a native mechanism scorer. Derived internal instrumentation would be a new measurement, not a native benchmark result. No benchmark, label, case, metric or outcome was fabricated, and no scorer was run.

Generic equality-constrained quadratic/KKT projection, GGN/natural-gradient curvature, generalized Sylvester equations, K-FAC, Shampoo and CrispEdit already cover the mathematical machinery or close functionality. Existing Delta preconditioning and multi-step rank controls cover the strongest simple alternatives. The retained value is a sharp debugging boundary: **right curvature cancels when the complete metric is separable, while a nonseparable sum can make the exact minimum-curvature edit provably higher rank**. The regularized operator `lambda I + W otimes pp^T` in the witness is already such a sum unless it happens to refactor; exact damping itself can break a factored approximation, so the rank gap is not by itself a new mechanism.

**Decision:** conditional mathematics accepted, but park after substantive attempt 1 with zero candidate increment. Reopen only with a prefix-causal structured estimator of the coupled curvature, a certified low-cost solve or regret/approximation theorem that beats rank-`r` Delta/direct predictors at matched total budget, and a native measurable consequence. Empirical effect remains unknown.

