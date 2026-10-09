# Deferred correction debt — transported error feedback, not a distinct candidate

Disposition: **rejected as a distinct method; retained as a control**.  The exact affine bookkeeping is useful, but the mechanism is transported error feedback plus known safe projection/controllability.  It does not occupy D07.

## Exact bookkeeping under shared affine dynamics

Let an ideal reference state obey

\[
X_t=A_tX_{t-1}+B_t.
\]

Suppose an immediate protected write admits only \(G_t\), leaving inflow debt \(E_t=B_t-G_t\).  Maintain a deployed state \(M_t\) and debt \(R_t\).  The theorem in this section requires the ideal and deployed paths to share the same externally fixed \(A_t,B_t\); state-dependent features are treated only in the later nonlinear boundary.  Define

\[
Z_t=A_tR_{t-1}+E_t,\qquad T_t=C_t(Z_t),
\]
\[
M_t=A_tM_{t-1}+G_t+T_t,\qquad R_t=Z_t-T_t.
\]

If \(M_{t-1}+R_{t-1}=X_{t-1}\), then

\[
M_t+R_t=A_t(M_{t-1}+R_{t-1})+G_t+E_t=X_t.
\]

Thus the identity holds by induction, and the readout difference from the ideal reference is exactly

\[
q_t^\top(M_t-X_t)=-q_t^\top R_t.
\]

No future label is needed for this accounting: \(E_t\) is formed from the current observed write deficit and \(C_t\) is causal.  The construction does not solve the protection/correction conflict; it postpones the unmet component.

## Future-key repayment is error feedback

For a unit causal address \(h_t\) and \(0\le\eta\le1\), choose

\[
C_t(Z)=\eta h_th_t^\top Z.
\]

Then

\[
R_t=(I-\eta h_th_t^\top)Z_t,
\]

and

\[
\lVert R_t\rVert_F^2
=\lVert Z_t\rVert_F^2-(2\eta-\eta^2)
\lVert h_t^\top Z_t\rVert_2^2.
\]

Debt orthogonal to all accessible future addresses is never repaid.  When \(A_t=I\), the recursion is exactly the error-feedback pattern \(p=g+e\), compressed/applied update \(\Delta=C(p)\), and residual \(e'=p-\Delta\) of Karimireddy et al., ICML 2019, Algorithm 1: <https://proceedings.mlr.press/v97/karimireddy19a.html>.  General \(A_t\) merely transports the residual before applying error feedback.  Delayed/error-compensated updates and the project's previously rejected D04 already occupy this neighborhood.

## Reachability condition

For one debt \(E_\tau\), its ideal effect at horizon \(H\) is

\[
Y=P_{H,\tau+1}E_\tau.
\]

Fix the future transitions and repayment directions in advance and set \(P_{H,H+1}=I\).  If repayment at step \(s\) is restricted to a rank-one write \(u_sc_s^\top\), its horizon-\(H\) left direction is \(g_s=P_{H,s+1}u_s\).  With \(G_H=[g_\tau,\ldots,g_H]\), and with no sign, amplitude, gate or online constraint on the coefficient rows \(c_s^\top\), exact catch-up is possible iff

\[
\operatorname{col}(Y)\subseteq\operatorname{col}(G_H).
\]

The irreducible Frobenius residual is

\[
\lVert(I-G_HG_H^\dagger)Y\rVert_F,
\]

and minimum-norm coefficients are \(G_H^\dagger Y\).  A small nonzero singular value makes the required repayment ill-conditioned.  Offline optimal coefficients generally require future addresses; an online rule only sees them as they arrive and has no unconditional finite-horizon catch-up guarantee.  If a repayment changes later \(u_s\) or \(A_s\), this fixed-\(G_H\) criterion no longer applies without recomputing the nonlinear reachable set.

## Protected repayment

For protected queries \(Q_s\), a rank-one repayment must satisfy

\[
Q_s^\top u_sc_s^\top=0.
\]

If \(Q_s^\top u_s\ne0\), this forces \(c_s=0\).  Replacing the direction by

\[
u_s=\Pi_{\operatorname{Null}(Q_s^\top)}h_s
\]

and applying the minimum-residual projection returns to known protected-update geometry.  If \(u_s=0\) repayment is impossible; near-zero projected address gives poor conditioning.  Multiple directions/steps are a safe reachable-subspace construction, neighboring multi-step Delta and slots rather than a new principle.

## Stability boundary

For an orthogonal/under-relaxed projection and \(\lVert A_t\rVert_2\le\rho\le1\),

\[
\lVert R_t\rVert_F\le\rho\lVert R_{t-1}\rVert_F+\lVert E_t\rVert_F.
\]

If \(\rho<1\) and \(\lVert E_t\rVert_F\le G\), then \(\limsup_t\lVert R_t\rVert_F\le G/(1-\rho)\); at \(\rho=1\), debt can grow linearly.  With no new debt and the strong conditional persistent-excitation assumption \(\mathbb E[h_th_t^\top\mid Z_t]\succeq\mu I\), the conditional expected squared norm is upper-bounded by the previous squared norm times

\[
\rho^2[1-(2\eta-\eta^2)\mu].
\]

This assumption is not automatic and usually fails for a deterministic single address in dimension greater than one.  Without excitation there is no decay guarantee.  Oblique projectors, small reachable singular values and nonnormal transport can transiently amplify the debt.

## Nonlinear and semantic failure

If future features depend on the deployed state, the ideal branch follows \(F(M+R)\) while the actual branch follows \(F(M)\).  Linear transport is then only a Jacobian approximation with a second-order remainder; exactness requires a complete shadow trajectory or rewind/replay.

Without event/source identity, the same numeric debt can represent either a still-valid protected fact or an obsolete fact.  Repay/cancel actions can then conflict under identical observables.  With identity and old content, the mechanism becomes exact-event memory/replay.  Event-wise transported debt is also the already rejected influence-ledger/eligibility-trace route.

## Closest mechanisms and cost

DeltaProduct already performs several rank-one microsteps per token; debt repayment is structurally an additional microstep, although released DeltaProduct does not read a separate debt state.  Sparse Delta Memory/slots supply event-level storage.  Subtract-or-Replay makes exact amendment suffix-dependent and uses replay.  Full \(R\) adds \(O(d_kd_v)\) state.  Its transport/read is another \(O(d_kd_v)\) per token for ordinary diagonal-plus-rank-one Delta \(A_t\), but \(O(d_k^2d_v)\) for a generic dense \(A_t\).  An event factorization costs \(O(M(d_k+d_v))\) plus identities and inherits rank/event growth.

The strongest baselines are a full-matrix error-feedback state with identical information, a DeltaProduct extra microstep, and event replay.  The only distinctive prediction—that repayment rate follows the safe transported-key Gramian and its smallest singular value—is already implied by error feedback plus controllability.  No independent mechanism remains.

Primary neighboring sources include Karimireddy et al., ICML 2019 Algorithm 1; Stich and Karimireddy, JMLR 21(237), 2020 on delayed/error-feedback updates; DeltaProduct arXiv:2502.10297v3 §3 and the pinned `naive_recurrent_gated_delta_product` interface; and Bellec et al., Nature Communications 2020 Eqs. 20--21 for eligibility traces.  This record also reuses the project's pinned Sparse Delta interface and earlier D04 compensation audit.  These are bounded functional neighbors, not an exhaustive prior-art claim.  No project code, test, model, benchmark, training, inference or scorer was executed.
