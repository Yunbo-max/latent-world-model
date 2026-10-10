# R20 v3 — sharp spectral-transfer certificate and prefix impossibility

Status: **accepted only as a conditional theorem/no-go control; substantive repair attempt 3 exhausted; parked; not an active D candidate**. This versioned child preserves R20 v1 and v2 byte-for-byte. It repairs the loose transfer algebra in v2, then shows that the new premise is not certifiable from the legal prefix without an additional continuation law. No model, scorer, benchmark, training or inference job was run.

## 1. Original problem, patch, and formal object

R20 v2 lawfully replaced an oracle future curvature by the prefix-measurable surrogate

\[
\widehat H=\lambda I+ZZ^\top\succ0,\qquad
\widehat x=\arg\min_{Ax=e}\frac12x^\top\widehat Hx, \tag{1}
\]

and gave its exact projected-Woodbury solution. Its unresolved step was the implication “small prefix quadratic risk implies small future harm.” Exact solution of (1) does not prove that implication.

The v3 patch does not alter the action. It asks for the weakest explicit relative spectral premise under which the implication is true. Let

\[
\mathcal C_e=\{x:Ax=e\}\ne\varnothing,
\quad K=\ker A,
\quad L_e=\operatorname{span}(\mathcal C_e)
=K+\operatorname{span}\{\widehat x\}. \tag{2}
\]

For a declared future *homogeneous quadratic* risk with operator \(H\succ0\) on \(L_e\), define

\[
x_H=\arg\min_{x\in\mathcal C_e}\frac12x^\top Hx. \tag{3}
\]

The causal information law is unchanged: \(A,e,Z,\widehat H,\widehat x\) may be \(\mathcal F_t\)-measurable; a realized suffix, future answer, protected-fact validity oracle, or counterfactual outcome may not be used to choose the current write. The operator \(H\) is therefore an analysis object unless a separate prefix-checkable stochastic or drift law supplies a confidence statement about it.

## 2. Sharp competitive theorem

Assume that on \(L_e\)

\[
m\widehat H\preceq H\preceq M\widehat H,
\qquad 0<m\le M<\infty. \tag{4}
\]

Then

\[
\boxed{
\frac{\widehat x^\top H\widehat x}
{x_H^\top Hx_H}
\le \frac{(M+m)^2}{4Mm}.} \tag{5}
\]

This is sharper than the valid but loose chaining bound \(M/m\).

### Derivation

Whiten with \(y=\widehat H^{1/2}x\) and

\[
G=\widehat H^{-1/2}H\widehat H^{-1/2}. \tag{6}
\]

On \(\widehat H^{1/2}L_e\), (4) becomes \(mI\preceq G\preceq MI\). Because \(\widehat y=\widehat H^{1/2}\widehat x\) is the Euclidean minimum-norm point in the whitened affine feasible set, every feasible \(y\) satisfies

\[
u^\top y=\|\widehat y\|,
\qquad u=\widehat y/\|\widehat y\|, \tag{7}
\]

when \(e\ne0\). Minimizing \(y^\top Gy\) over the larger hyperplane in (7) gives

\[
x_H^\top Hx_H
\ge \frac{\|\widehat y\|^2}{u^\top G^{-1}u}. \tag{8}
\]

The numerator is \(\|\widehat y\|^2u^\top Gu\), hence the ratio is at most

\[
(u^\top Gu)(u^\top G^{-1}u). \tag{9}
\]

For an eigenvalue \(\gamma\in[m,M]\),

\[
(M-\gamma)(\gamma-m)\ge0
\Longrightarrow \gamma+\frac{Mm}{\gamma}\le M+m. \tag{10}
\]

Average (10) using the squared spectral coordinates of \(u\), then apply AM-GM:

\[
4Mm(u^\top Gu)(u^\top G^{-1}u)
\le(M+m)^2. \tag{11}
\]

Equations (8)--(11) prove (5).

The constant is sharp. Take \(\widehat H=I_2\), \(H=\operatorname{diag}(m,M)\), \(u=(1,1)^\top/\sqrt2\), and \(\mathcal C=\{x:u^\top x=1\}\). Then \(\widehat x=u\), the relaxed hyperplane in (8) is the actual feasible set, and equality holds in (11).

For a symmetric relative uncertainty radius

\[
(1-\delta)\widehat H\preceq H\preceq(1+\delta)\widehat H,
\qquad 0\le\delta<1, \tag{12}
\]

the sharp factor is

\[
\boxed{\frac{1}{1-\delta^2}.} \tag{13}
\]

The commonly written \((1+\delta)/(1-\delta)\) follows from loose endpoint chaining and is not sharp for this shared affine constraint.

## 3. Robust minimax consequence does not create a new action

Let \(\mathcal U_\delta\) contain all operators satisfying (12) on \(L_e\). For every feasible \(x\),

\[
\sup_{H\in\mathcal U_\delta}\frac12x^\top Hx
=\frac{1+\delta}{2}x^\top\widehat Hx. \tag{14}
\]

Therefore

\[
\arg\min_{x\in\mathcal C_e}\sup_{H\in\mathcal U_\delta}
\frac12x^\top Hx=\widehat x. \tag{15}
\]

Symmetric Loewner robustification leaves the v2 action exactly unchanged. It supplies a certificate if (12) is independently justified; it is not a new updater.

## 4. Why the domain must include the affine base point

A sandwich only on feasible differences \(K=\ker A\) is insufficient because it misses base--tangent cross terms. Let

\[
A=[1,0],\ e=1,\ \widehat H=I_2,\quad
H_b=\begin{bmatrix}b^2+\varepsilon&b\\b&1\end{bmatrix},
\quad \varepsilon>0. \tag{16}
\]

Feasible actions are \(x=(1,u)\). On \(K=\operatorname{span}(e_2)\), \(v^\top H_bv=v^\top\widehat Hv\), an apparent exact match. Yet

\[
x^\top H_bx=(u+b)^2+\varepsilon. \tag{17}
\]

The prefix optimum is \((1,0)\), the future optimum is \((1,-b)\), and the risk ratio is \((b^2+\varepsilon)/\varepsilon\), which is unbounded. Thus the weakest uniform linear domain for the homogeneous quadratic claim is

\[
L_e=K+\operatorname{span}\{x_0\}
=\operatorname{span}(\mathcal C_e), \tag{18}
\]

for any feasible base point \(x_0\). A posteriori, (5) only needs the two-action span \(\operatorname{span}\{\widehat x,x_H\}\), but that space depends on the unknown future and is not an action-time certificate. Uniformity over every possible target \(e\) generally expands the required domain to \(K+\operatorname{range}(A^\top)=\mathbb R^n\).

## 5. Same-prefix impossibility of certifying the premise

Suppose a deterministic prefix rule announces a nonvacuous \(\delta<1\) from \(\mathcal F_t\). Two continuations may share exactly that prefix and the same \(Z,\widehat H,\widehat x\), while having

\[
H_1=\widehat H,
\qquad H_2=\widehat H+\rho vv^\top, \tag{19}
\]

where \(v\in L_e\cap\operatorname{span}(Z)^\perp\) is unit length. Since \(\widehat H v=\lambda v\), the upper inequality in (12) for \(H_2\) requires

\[
\rho\le\delta\lambda. \tag{20}
\]

Choosing \(\rho>\delta\lambda\) violates the announced certificate without changing any prefix observation. If the low-rank sketch happens to span \(L_e\), the same impossibility follows from the indistinguishable continuation \(H_2=c\widehat H\) with \(c>1+\delta\). Hence no prefix-measurable function can soundly certify a fixed \(\delta<1\) over unrestricted continuations.

This is not a claim that transfer never occurs. It identifies the missing premise: a stated generative model, mixing/stationarity law, known drift/Lipschitz constants, or a time-uniform concentration result whose coverage and adaptive-write failure probability are explicit. Estimating \(\delta\) from the realized suffix is lawful evaluation but cannot gate the already-made write.

## 6. Loss-class and boundary checks

The theorem is exactly about the declared homogeneous quadratic. Curvature alone does not control a linear term. With feasible \((1,u)\), \(H=\widehat H=I\), and

\[
F_b(u)=\tfrac12(u-b)^2, \tag{21}
\]

the curvatures match perfectly, but the curvature-only action \(u=0\) has loss \(b^2/2\) while the future optimum has zero loss. A full local quadratic needs the tangent linear term, not only \(H\).

Nor does exact base-point curvature control a finite nonlinear edit. For

\[
F_b(u)=b(1-u^3)^2+\tfrac12u^2, \tag{22}
\]

we have \(F_b'(0)=0\) and \(F_b''(0)=1\) for every \(b\), but \(F_b(0)=b\) and \(F_b(1)=1/2\). A finite-action claim needs a trust region and a uniform remainder/Jacobian bound along the changed trajectory. The complete-state Jacobian results from Step2 remain necessary when future keys, gates, routing, or updater state depend on the edit.

Other exact boundaries:

- if \(e=0\), both positive-definite quadratic problems choose zero; the multiplicative ratio is written as an action equality rather than \(0/0\);
- if \(\dim L_e=1\) or \(m=M\), both actions coincide and the ratio is one;
- if \(m=0\), equivalently \(\delta\ge1\) in (12), no finite competitive factor follows; future optima may have zero risk;
- if \(\widehat H\) is singular, shared-nullspace, range, uniqueness, and tie-break conditions are required;
- factual validity, source freshness, causal identity, and unobserved counterfactual utility are not encoded by a curvature sandwich.

## 7. Cost, controls, measurement, and decision

V3 adds no state and no solve to v2. The deployed action remains the projected-Woodbury formula with the same feature extraction, sketch, \(r\times r\) solve, storage, and query costs. Any claimed certificate must additionally pay for the information that establishes its premises. The same-information controls remain normalized/rank-\(r\) Delta, projected CG, ONS/natural-gradient or empirical-Fisher variants, hard projection, matched-memory L-BFGS, and a direct prefix action-factor predictor.

Primary literature already contains spectral-approximation assumptions for sketched or subsampled curvature, constrained Hessian-sketch approximation theorems, and online Newton/dynamic-regret guarantees under explicit convexity, variation, or prediction-error assumptions. Those results support the conditional mathematics but also make “spectral transfer plus stale curvature” a strong known baseline rather than an originality claim. They do not supply the missing autoregressive prefix-to-future law for this Delta state.

Existing language/continual-learning benchmarks can measure downstream retention or prediction only after execution; they do not natively label \(H\), \(\delta\), the same-state counterfactual optimum, or factual validity. No native measurement closes the deployment premise at this stage.

**Decision:** mathematical correctness `accepted_conditional`; contribution difference `known certificate plus a useful Delta-specific no-go boundary, not a new method`; empirical effect `unknown_no_execution`. R20 has used all three substantive repair attempts and is now parked. It can reopen only if new external evidence yields a prefix-checkable continuation law with explicit coverage, or a native matched-total-cost advantage over the listed controls. Candidate, scientific-admission, and selection increments are all zero.
