# R16 v1 — noncommuting joint-flow boundary for Delta memory

Status: **conditional theorem/control; parked after attempt 1, not an active D candidate**. This versioned child of rejected/EXACT_FLOW_IMPLICIT_DELTA_CONTROL.md and rejected/AFFINE_MAGNUS_COMMUTATOR_CONTROL.md replaces a scalar commuting flow by the full frozen channel-decay/write generator. It finds a real Krylov-rank boundary, but its exact-write endpoint collapses to R09/PDN/RLS-style normalized inverse-metric Delta and its exact transition is generally dense.

## 1. Formal object, original failure, and concrete patch

Let \(S\in\mathbb R^{d\times m}\) be key-by-value memory, \(k\in\mathbb R^d\) a nonzero frozen key, \(v\in\mathbb R^m\) a frozen target, \(\Lambda=\Lambda^\top\succeq0\) a declared channel-decay generator, and \(\tau>0\) a declared token duration. The residual is \(e=v-S^\top k\).

The parent exact-flow control treated residual correction as a scalar autonomous flow and could only change the gate. R16 tests a simultaneous frozen flow:

\[
\dot S=-\Lambda S+k(v-S^\top k)^\top
=-(\Lambda+kk^\top)S+kv^\top. \tag{1}
\]

This is an additional modeling assumption. KDA's discrete decay-then-write recurrence already has a precise chronology; (1) is not a correction to an algebraic error in KDA. Define

\[
M=\Lambda+kk^\top,\quad E_\tau=e^{-\tau M},\quad
P_\tau=\int_0^\tau e^{-sM}\,ds=\tau\varphi_1(-\tau M),\quad
F_\tau=P_\tau k. \tag{2}
\]

Because \(M\succeq0\), \(P_\tau\succ0\). Variation of constants gives

\[
S_\tau=E_\tau S_0+F_\tau v^\top. \tag{3}
\]

## 2. The natural joint flow does not exactly write

\[
S_\tau^\top k=S_0^\top E_\tau k+a_\tau v,\qquad
a_\tau=k^\top P_\tau k>0. \tag{4}
\]

This is generally not \(v\). In one dimension with \(k=1\) and \(\Lambda=\lambda>0\),

\[
s_\tau=e^{-(\lambda+1)\tau}s_0+
\frac{1-e^{-(\lambda+1)\tau}}{\lambda+1}v, \tag{5}
\]

so even the infinite-time limit is \(v/(\lambda+1)\). If \(\Lambda\succ0\), Sherman--Morrison gives

\[
k^\top M^{-1}k=\frac{r}{1+r}<1,\qquad
r=k^\top\Lambda^{-1}k. \tag{6}
\]

Simultaneous decay changes the fixed point into a shrinkage solution. Calling (3) an exact overwrite would be false.

## 3. Exact endpoint patch and exact collision

To force \(S^{+\top}k=v\), the forcing must depend on the initial state:

\[
u_\tau=\frac{v-S_0^\top E_\tau k}{a_\tau},\qquad
g_\tau=\frac{P_\tau k}{k^\top P_\tau k}. \tag{7}
\]

Use this constant control in \(\dot S=-MS+ku_\tau^\top\). Then

\[
S^+=E_\tau S_0+g_\tau(v-S_0^\top E_\tau k)^\top
=(I-g_\tau k^\top)E_\tau S_0+g_\tau v^\top, \tag{8}
\]

and \(k^\top g_\tau=1\). For any query \(q\),

\[
o^+(q)=S_0^\top E_\tau q+
(q^\top g_\tau)(v-S_0^\top E_\tau k). \tag{9}
\]

This patch is the unique solution of

\[
\min_\Delta\operatorname{tr}(\Delta^\top P_\tau^{-1}\Delta)
\quad\text{s.t.}\quad
\Delta^\top k=v-(E_\tau S_0)^\top k. \tag{10}
\]

Thus it is exactly R09's normalized inverse-metric/oblique Delta with \(H=P_\tau^{-1}\). Its limits expose the collision:

\[
g_\tau\to\frac{k}{\|k\|^2}\quad(\tau\downarrow0),\qquad
g_\tau\to\frac{\Lambda^{-1}k}{k^\top\Lambda^{-1}k}
\quad(\tau\to\infty,\ \Lambda\succ0). \tag{11}
\]

The old-state factor \((I-g_\tau k^\top)E_\tau\) is singular, so exact overwrite still destroys one old-state direction. If the pre-update residual \(e_0=v-S_0^\top k\ne0\), then \(u_\tau\sim e_0/(\tau\|k\|^2)\) as \(\tau\downarrow0\); when \(e_0=0\) it can remain \(O(1)\). The generic nonzero-residual case therefore exposes an endpoint projection, not a mild realization of the original autonomous flow.

## 4. The genuine noncommuting theorem

Let

\[
\mathcal K=\operatorname{span}\{k,\Lambda k,\ldots,\Lambda^{d-1}k\},
\qquad r_K=\dim\mathcal K. \tag{12}
\]

For symmetric \(\Lambda\), both \(\Lambda\) and \(M\) leave \(\mathcal K\) invariant, while \(M=\Lambda\) on \(\mathcal K^\perp\). Therefore

\[
\operatorname{rank}(E_\tau-e^{-\tau\Lambda})\le r_K. \tag{13}
\]

If \(\Lambda k\parallel k\), then \(r_K=1\) and the result reduces to the scalar-gate control. Noncommutation can immediately exceed rank one. In two dimensions let \(a=\|k\|^2\), \(u=k/\sqrt a\), choose unit \(w\perp u\), and set \(c=u^\top\Lambda w\ne0\). Taylor expansion gives

\[
\det(E_\tau-e^{-\tau\Lambda})
=-\frac{a^2c^2}{12}\tau^4+O(\tau^5), \tag{14}
\]

so the difference has rank two for sufficiently small nonzero \(\tau\). With distinct diagonal entries and all coordinates of \(k\) nonzero, \(r_K=d\); there is no fixed rank-one correction guarantee.

A leakage witness takes \(S_0=0\), \(v\ne0\), \(\Lambda=\operatorname{diag}(0,1)\), \(k=(1,1)^\top/\sqrt2\), and \(q=(1,-1)^\top/\sqrt2\). Although \(q^\top k=0\),

\[
q^\top F_\tau=\frac{\tau^2}{4}+O(\tau^3)>0. \tag{15}
\]

Thus the joint source contributes \(q^\top F_\tau v^\top\ne0\), whereas the correction-subflow source \(F_K\parallel k\) contributes zero at the same query. This is geometry, not evidence that the association was obsolete or safe to release.

## 5. Ordered split comparison must include the affine source

Let \(C=e^{-\tau kk^\top}\) and \(D=e^{-\tau\Lambda}\). For the decay-then-correction split with homogeneous factor \(CD\),

\[
E_\tau-CD=\frac{\tau^2}{2}[\Lambda,kk^\top]+O(\tau^3). \tag{16}
\]

If \(F_K=\int_0^\tau e^{-s kk^\top}k\,ds\) is the correction-subflow source, then

\[
F_\tau-F_K=-\frac{\tau^2}{2}\Lambda k+O(\tau^3). \tag{17}
\]

A homogeneous commutator alone is incomplete. R11 already covers signed frozen-feature order gaps; Strang/Magnus and exponential integrators cover the generic construction. R16's residual is the Krylov-rank and endpoint-collision statement.

## 6. Computation, state, scan, and information cost

The affine maps compose associatively, so noncommutation does not prevent exact scan. The obstacle is structure: token-dependent \(M=\Lambda+kk^\top\) generally yields dense \(E_\tau\), and products do not remain diagonal-plus-rank-one.

- Generic dense exponential/eigendecomposition formation is \(O(d^3)\).
- Storing \(E_\tau\) costs \(O(d^2)\); applying it to \(S\) costs \(O(d^2m)\), versus the \(O(dm)\) diagonal-plus-rank-one recurrence.
- A \(p\)-step polynomial/Krylov action can cost about \(O(pdm)\), but is approximate, needs an error contract, and must be compared with multistep/DeltaProduct controls. Worst-case Krylov dimension is \(d\).
- A direct discrete implementation of the same \(E_\tau,g_\tau\) is identical, so the ODE story supplies no separate advantage.

No new causal information is introduced. The same prefix, \(k,v,\Lambda,\tau\), and state cannot decide true revision versus still-valid collision. Contractivity of \(E_\tau\) is stability, not retention, and the oblique projection can have norm above one.

## 7. Predictions, controls, and measurement

Conditional predictions and falsifiers are:

1. The split difference reduces to scalar-gate behavior when \(\Lambda k\parallel k\) and grows locally with commutator/Krylov structure.
2. Orthogonal-query leakage such as (15) appears even when ordinary one-step Delta predicts zero direct displacement.
3. At matched \(E_\tau,g_\tau\), joint-flow and direct discrete inverse-metric implementations must be identical.
4. Any claim of reversible exact endpoint writing is falsified by the singular factor in (8).

Required same-information controls are KDA's ordered recurrence, Delta/NLMS, PDN/RLS or R09, the direct dense affine map, Strang/Magnus/exponential-action approximations, and matched-step DeltaProduct/Krylov approximations.

bAbI, LAMBADA, RULER, and LongMemEval measure endpoints but do not natively expose a ground-truth sub-token generator, exact internal \(E_\tau,F_\tau\), or validity labels for leaked associations. They cannot alone distinguish (1) from split semantics or certify protection/release. No benchmark, label, metric, or result is invented.

## 8. Disposition

R16 preserves a useful theorem: noncommuting joint decay/write differs from pure decay on a Krylov subspace that can be higher-rank, and the affine source has its own second-order gap. But the natural flow misses exact write, the endpoint repair is known inverse-metric Delta, and the exact transition is generally dense and loses KDA's compact diagonal-plus-rank-one application/scan structure. This is not a universal lower bound against every structured exact-action algorithm. Empirical effect remains unknown.

**Decision:** park after substantive attempt 1. Add zero active, scientifically admitted, or selected candidates. Reopen only if the simultaneous ODE is independently justified and a structured exact or certified approximate action yields a matched-information, matched-budget advantage over KDA/PDN/direct exponential-action controls, or if new causal evidence resolves revision versus collision.
