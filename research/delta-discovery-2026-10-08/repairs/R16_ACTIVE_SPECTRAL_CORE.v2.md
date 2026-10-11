# R16 v2 — active-spectrum exact core and certified grouping

Status: **conditional theorem/control; parked after attempt 2, not an active D candidate**. This versioned child preserves R16_NONCOMMUTING_JOINT_FLOW.v1.md. It gives an exact active-spectrum reduction for symmetric decay, and repairs v1's computation statement only under an explicit structured-basis condition. It does not repair the known exact-write collision or supply causal revision evidence.

## 1. Formal object and repaired question

Use the same frozen joint flow as v1:

\[
\dot S=-(\Lambda+kk^\top)S+kv^\top,
\qquad \Lambda=\Lambda^\top\succeq0,
\qquad S\in\mathbb R^{d\times m},\quad \tau>0,\quad k\ne0. \tag{1}
\]

The \(k=0\) branch is pure decay and has no normalized write direction. The assumptions \(k\ne0,\tau>0\) are required only when the normalized endpoint is used.

Let

\[
M=\Lambda+kk^\top,\quad
E_\tau=e^{-\tau M},\quad
p_\tau(x)=\begin{cases}(1-e^{-\tau x})/x,&x>0,\\ \tau,&x=0,\end{cases}
\quad P_\tau=p_\tau(M),\quad F_\tau=P_\tau k. \tag{2}
\]

Then the natural flow is \(S_\tau=E_\tau S_0+F_\tau v^\top\). The v1 endpoint controller is

\[
g_\tau=\frac{P_\tau k}{k^\top P_\tau k},\qquad
S^+=E_\tau S_0+g_\tau(v-S_0^\top E_\tau k)^\top. \tag{3}
\]

V1 proved that the matrix-function correction is supported on the \(\Lambda\)-Krylov space of \(k\), which can have dimension \(d\). V2 asks the narrower constructive question: **when is that support exactly a small, identifiable invariant core, and what error is paid if the spectrum is grouped to make it small?**

## 2. Active-spectrum decomposition

Let the spectral decomposition of \(\Lambda\) be

\[
\Lambda=\sum_{j=1}^{J}\lambda_j\Pi_j. \tag{4}
\]

The \(\lambda_j\) are distinct and the \(\Pi_j\) are orthogonal projectors. Define

\[
\mathcal A=\{j:\|\Pi_jk\|>0\},\qquad r=|\mathcal A|. \tag{5}
\]

For \(j\in\mathcal A\), set

\[
c_j=\|\Pi_jk\|,\qquad u_j=\Pi_jk/c_j,\qquad
U=[u_j]_{j\in\mathcal A},\qquad
D=\operatorname{diag}(\lambda_j)_{j\in\mathcal A},\qquad
c=(c_j)_{j\in\mathcal A}. \tag{6}
\]

The columns of \(U\) are orthonormal, \(k=Uc\), and \(\Lambda U=UD\). Since the active eigenvalues are distinct, the Vandermonde matrix built from \(1,\lambda_j,\ldots,\lambda_j^{r-1}\) is nonsingular. Hence

\[
\mathcal K(\Lambda,k)
=\operatorname{span}\{k,\Lambda k,\ldots\}
=\operatorname{span}\{u_j:j\in\mathcal A\},\qquad
\dim\mathcal K=r. \tag{7}
\]

This is the smallest \(\Lambda\)-invariant subspace containing \(k\). It is an exact representation-class lower bound: any exact construction that confines the correction to a \(\Lambda\)-invariant active subspace containing \(k\) needs dimension at least \(r\). It is not a universal lower bound against every algorithm. For a general symmetric \(\Lambda\), the vectors \(u_j\) can be dense and discovering the projectors may itself require a full eigendecomposition; exact dimension reduction alone is not a cheap implementation.

## 3. Exact small-core theorem

Define the \(r\times r\) symmetric diagonal-plus-rank-one core

\[
B=D+cc^\top. \tag{8}
\]

The spaces \(\operatorname{range}(U)\) and its orthogonal complement reduce both \(\Lambda\) and \(M\); on them, \(M\) acts as \(B\) and \(\Lambda\), respectively. Therefore, for every analytic function \(f\) defined on their spectra,

\[
f(M)=f(\Lambda)+U\bigl[f(B)-f(D)\bigr]U^\top. \tag{9}
\]

In particular,

\[
E_\tau=e^{-\tau\Lambda}
+U\bigl[e^{-\tau B}-e^{-\tau D}\bigr]U^\top, \tag{10}
\]

\[
P_\tau=p_\tau(\Lambda)
+U\bigl[p_\tau(B)-p_\tau(D)\bigr]U^\top,\qquad
F_\tau=U p_\tau(B)c. \tag{11}
\]

Consequently the exact-write direction is computed entirely inside the active core:

\[
g_\tau=
U\frac{p_\tau(B)c}{c^\top p_\tau(B)c}. \tag{12}
\]

The rank of \(E_\tau-e^{-\tau\Lambda}\) is at most \(r\), but need not equal \(r\). Formula (9), rather than rank alone, is the constructive result.

For the scalar special case \(\Lambda=\lambda I\), \(r=1\) and

\[
E_\tau=e^{-\tau\lambda}\left[I+
\bigl(e^{-\tau\|k\|^2}-1\bigr)\frac{kk^\top}{\|k\|^2}\right],
\qquad g_\tau=\frac{k}{\|k\|^2}. \tag{13}
\]

Thus the cheapest exact case collapses to ordinary normalized Delta/scalar-flow territory, exactly as the v1 collision predicted.

## 4. Exact sequential cost and its structured-basis boundary

The core \(B=D+cc^\top\) is DPR1. Its eigenvalues solve

\[
1+\sum_{j=1}^{r}\frac{c_j^2}{\lambda_j-\mu}=0, \tag{14}
\]

and its eigenvectors are proportional to \((D-\mu I)^{-1}c\), with the usual deflation treatment. A forward-stable DPR1 eigensolver computes each eigenpair in \(O(r)\), hence all core eigenpairs in \(O(r^2)\). A generic dense core routine would instead cost \(O(r^3)\).

For an arbitrary symmetric \(\Lambda\), orthogonal eigenspaces need not be coordinate-sparse. A dense \(U\) makes projection/lifting cost \(O(drm)\); discovering and storing a general eigenbasis can cost \(O(d^3)\) and \(O(d^2)\). Applying \(e^{-\tau\Lambda}\) to \(S\) can itself cost \(O(d^2m)\). V2 does not call this case efficient.

The fast claim requires one of two declared structures:

1. \(\Lambda\) is diagonal in the deployed coordinates, with tied values defining coordinate groups; or
2. a fixed eigenbasis with a separately charged fast transform is supplied, and its transform cost replaces the coordinate projection/lifting cost below.

In the first KDA-style case, the \(u_j\) have disjoint coordinate-group support, so forming \(U^\top S\) and lifting \(U(\cdot)\) together costs \(O(dm)\), not \(O(drm)\). The active groups and base action \(e^{-\tau\Lambda}S\) are available by elementwise operations. Applying the dense core eigenbasis to \(r\times m\) data costs \(O(r^2m)\). The exact sequential action then costs

\[
O(dm+r^2m+r^2). \tag{15}
\]

This stores \(S\), the coordinate-group description, and an \(r\times r\) core. Fixed/small \(r\), or more generally \(r^2=O(d)\), recovers \(O(dm)\) asymptotics for the coordinate-diagonal interface. If diagonal \(\Lambda\) has distinct coordinate values and every coordinate of \(k\) is nonzero, then \(r=d\), the core eigenbasis is generically dense, and application returns to \(O(d^2m)\). DPR1 structure sharpens generic dense \(O(d^3)\) formation to \(O(d^2)\), but does not recover KDA's \(O(dm)\) recurrence in that worst case. A claimed non-coordinate fast basis must report its forward, backward, storage, and discovery/amortization costs rather than silently using (15).

Affine maps still compose associatively. However, token-dependent \(U_t\) and \(B_t\) need not share a basis, and products of their low-rank corrections need not keep fixed rank. Formula (15) is an exact **sequential recurrent** result, not a compact exact chunk-scan theorem.

## 5. Certified grouping for a general spectrum

Let \(\widetilde\Lambda\succeq0\) group nearby decay eigenvalues, define

\[
\delta=\|\Lambda-\widetilde\Lambda\|_2,\qquad
\widetilde M=\widetilde\Lambda+kk^\top, \tag{16}
\]

and put tildes on the corresponding \(E,P,F,g\). The Duhamel identity and contractivity of PSD exponentials give

\[
\|E_\tau-\widetilde E_\tau\|_2\le \tau\delta,\qquad
\|P_\tau-\widetilde P_\tau\|_2\le \frac{\tau^2}{2}\delta,\qquad
\|F_\tau-\widetilde F_\tau\|_2\le \frac{\tau^2}{2}\delta\|k\|. \tag{17}
\]

Thus

\[
\|S_\tau-\widetilde S_\tau\|_F
\le \tau\delta\|S_0\|_F
+\frac{\tau^2}{2}\delta\|k\|\|v\|. \tag{18}
\]

For the normalized endpoint, let \(a=k^\top P_\tau k\), \(\widetilde a=k^\top\widetilde P_\tau k\), and assume the explicit conditioning certificate \(a,\widetilde a\ge a_{\min}>0\). Then

\[
\|g_\tau-\widetilde g_\tau\|_2
\le
\frac{\tau^2\delta\|k\|}{2a_{\min}}
+\frac{\tau^3\delta\|k\|^3}{2a_{\min}^2}. \tag{19}
\]

The denominator certificate is essential. Without it, grouping error can be magnified by endpoint normalization. One computable sufficient bound is \(a_{\min}=p_\tau(L)\|k\|^2\) for any declared \(L\ge\max(\|M\|_2,\|\widetilde M\|_2)\), because \(p_\tau\) is positive and decreasing on \([0,\infty)\).

The bounds above hold for symmetric PSD operators whether or not their basis is cheap. Realizing them at the cost in (15) additionally requires coordinate-diagonal grouping or a separately charged fast fixed basis. Grouping changes the generator; it is not a free approximation to the original per-channel KDA semantics. It must be compared with grouped KDA and a direct grouped exponential action at the same \(r\), tolerance, transform/storage burden, and total cost. Adaptive grouping, active-set thresholds, and gradients through membership remain implementation costs, not consequences of the norm certificate.

## 6. Old counterexamples and collisions rechecked

1. **Natural flow still misses exact overwrite.** \(E_\tau\) is invertible positive definite for finite \(\tau\), so \(k^\top E_\tau\ne0\); \(E_\tau S+F_\tau v^\top\) cannot equal \(v\) at the key for every initial \(S\). The state-dependent endpoint control remains necessary.
2. **Endpoint geometry is unchanged.** Equation (12) is still v1's normalized inverse-metric/oblique Delta and therefore still collides with R09/PDN/RLS. Structure repairs computation, not functional novelty.
3. **Exact overwrite remains irreversible.** The old-state factor \((I-g_\tau k^\top)E_\tau\) is singular because \(k^\top g_\tau=1\).
4. **Orthogonal-query leakage remains.** When \(r>1\), \(F_\tau=Up_\tau(B)c\) is generally not parallel to \(k=Uc\); a query orthogonal to \(k\) may still see the affine write. This is geometry, not evidence of semantic benefit.
5. **Dense-basis cost survives.** Small \(r\) alone does not imply \(O(dm)\) when the active eigenvectors are dense or must be discovered.
6. **Worst case survives.** Distinct active decays give \(r=d\), eliminating the small-core advantage.
7. **Scan closure remains absent.** Different token cores do not generally compose into a fixed \(r\)-core representation.

## 7. Same-information controls, predictions, and measurement

Mandatory controls are: ordered KDA; grouped KDA; ordinary normalized Delta; R09/PDN/RLS; direct discrete implementation of the same \(E_\tau,g_\tau\); fixed-generator DPLR/structured-SSM kernels; polynomial/rational Krylov or exponential-action approximations with explicit tolerance; and matched-step DeltaProduct/multistep Delta.

Falsifiable conditional predictions are:

- exact dense and active-core implementations agree up to numerical error when their declared \(\Lambda,k,\tau\) match;
- correction dimension tracks the number \(r\) of active distinct decay values, while recurrent cost additionally tracks basis transform/discovery structure rather than merely rank-one \(kk^\top\);
- grouping error obeys (17)–(19) when the stated PSD and denominator conditions hold;
- at identical \(E_\tau,g_\tau\), an ODE narrative and a direct discrete implementation are functionally identical;
- grouped joint flow can only beat grouped KDA empirically if the simultaneous-generator semantics matter, not merely because it receives extra rank or computation.

Existing bAbI, LAMBADA, RULER, and LongMemEval endpoints do not natively expose a true sub-token generator, active spectral groups, exact internal action, or validity labels for protected/revised associations. They can measure downstream endpoints but cannot by themselves identify (1) or certify protection/release. No benchmark, label, metric, or result is invented.

## 8. Disposition

R16 v2 repairs a real gap: under \(r\) active spectral groups, the noncommuting joint flow and its affine source reduce exactly to an \(r\times r\) DPR1 core, and approximate grouping has a finite error certificate. With coordinate-diagonal tied groups this is an exact structured sequential action; with a general symmetric generator the dense basis and its discovery must be charged. It also corrects v1's coarse generic formation statement: diagonal-plus-rank-one eigendecomposition is \(O(d^2)\), although dense application remains \(O(d^2m)\).

The repair does not establish a distinct updater. The scientific generator is still assumed, exact-write remains known normalized inverse-metric Delta, direct discrete action is identical, fixed-rank scan closure is missing, and no new causal information resolves retain versus revise. Empirical effect is unknown.

**Decision:** park after substantive attempt 2/3 as a conditional theorem/control. Add zero active, scientifically admitted, or selected candidates. Reopen only under the conditions in R16_REPAIR_LINE_SCREEN.v2.md.
