# Rank-revealing constraint Delta

Disposition: **accepted exact algebraic diagnostic; rejected as a distinct method**.  The route reduces to rank-Greville/QR recursive least squares and hard protected projection.  No project code or experiment was executed.

## Formal causal state

Let \(S\in\mathbb R^{d\times m}\) read \(S^\top k\).  Accepted exact constraints are

\[
A^\top S=Y,qquad A=[a_1,\ldots,a_r]=QR,quad Q^\top Q=I_r.
\]

Write \(W=R^{-\top}Y\), so the constraints are \(Q^\top S=W\).  For a new observed pair \((k,v)\), compute

\[
z=Q^\top k,qquad u=(I-QQ^\top)k,qquad \rho=\|u\|.
\]

If \(\rho>0\), set \(q=u/\rho\) and update

\[
Q_+=[Q\ q],\qquad
R_+=\begin{bmatrix}R&z\\0&\rho\end{bmatrix},qquad
W_+=\begin{bmatrix}W\\(v-W^\top z)^\top/\rho\end{bmatrix}.
\]

If \(\rho=0\), the old constraints already imply \(v_{\rm implied}=W^\top z\).  The pair is either redundant when \(v=v_{\rm implied}\), or algebraically inconsistent when they differ.

## Minimum-change recurrence

Assume \(S\) satisfies the old constraints and let \(e=v-S^\top k\).  Solve

\[
\min_{\Delta S}{1\over2}\|\Delta S\|_F^2
\quad\text{s.t.}\quad Q^\top\Delta S=0,quad k^\top\Delta S=e^\top.
\]

For \(\rho>0\), the unique solution is

\[
\boxed{\Delta S^\star={u e^\top\over\|u\|^2}}.
\]

It exactly preserves every old key-span response and fits the new pair.  Its unavoidable norm is

\[
\|\Delta S^\star\|_F={\|e\|\over\rho}.
\]

At \(\rho=0\), exact fitting while preserving old constraints is feasible iff \(e=0\).  Near dependence forces the \(1/\rho\) amplification.  If decay is first applied, exact old-constraint restoration requires

\[
S^{\rm old}=\bar S+Q(W-Q^\top\bar S),
\]

which costs \(O(drm)\) and cancels decay on the protected span.

## Scope and counterexamples

Only \(r\le d\) independent hard key directions exist under a fixed linear readout.  Arbitrarily many dependent pairs remain possible if consistent, so this is not an unconditional finite-bit capacity theorem.  Finite precision additionally depends on the rank threshold and \(\sigma_{\min}(A)\).

The exact rank classifier does not identify semantics:

- history \((1,0)\), new pair \((1,1)\) gives \(\rho=0,e=1\) both when one fact was revised and when two entities collided in the encoder;
- \((e_1,0),(e_2,0),(e_1+e_2,1)\) is an impossible set of exact linear constraints, but does not specify which item to delete;
- \((e_1,0),(e_1+\epsilon e_2,1)\) requires state scale at least \(1/\epsilon\);
- \(k_3=e_1+e_2,v_3=v_1+v_2\) is a consistent dependent control and correctly needs no update.

## Closest work and disposition

The boxed update is the hard-nullspace OWM/protected-projection rule.  Rank-Greville/QR-RLS already provides the independent-observation update and the dependent least-squares compromise; see Staub and Steinmann, arXiv:2106.11594v1, §2.1--2.2, Theorems 4--5/Eqs.36 and 39.  Relaxing old constraints gives ordinary RLS/inverse-Gram geometry; PDN arXiv:2604.21100v1 §3.1 Eqs.3--5 uses exactly this historical regression object.  Routing a conflict to another row is sparse/slot memory, while retaining event identities for later downdates is event memory.

Prediction: in exact arithmetic the preserved-span and new-fit equalities hold, while edit norm scales as \(1/\rho\).  Any method avoiding this growth has relaxed a constraint or added information/state.  The route is retained as a geometric novelty/consistency diagnostic and receives no D-number.
