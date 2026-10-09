# DeltaTTT primary-paper audit

Status: primary-paper formula audit complete; author implementation was not located in the bounded search recorded below.  This is a source/novelty audit, not an experimental reproduction.

## Fixed source

- Alex Cheng, Soham De, Debojyoti Dey, Ahmed Khaled, Tri Dao, *DeltaTTT: Layerwise Optimization for Nonlinear Recurrent Memory*, arXiv:2610.08553v1, submitted 2026-10-06: <https://arxiv.org/abs/2610.08553>
- Formula-bearing HTML read on 2026-10-09: <https://arxiv.org/html/2610.08553v1>

The bounded author/repository search on 2026-10-09 did not locate a repository that the paper itself identifies as its official implementation.  This is deliberately recorded as “not located”, not “does not exist”.

## Actual mathematical object

The paper starts from test-time training (TTT) memory,

\[
W_t=W_{t-1}-\eta_t\nabla_W\mathcal L(f_W(k_t),v_t),\qquad
o_t=f_{W_t}(q_t),
\]

and distinguishes serial TTT, whose gradient is evaluated at the evolving state, from a fixed-base form whose per-token gradients can be summed.  For a linear memory and squared reconstruction error, the serial rule is the usual Delta update; evaluating all gradients at a fixed base collapses it to linear attention (paper Eqs. 3--6).  This distinction matters: exact parallelization is not obtained by silently treating serial state-dependent gradients as independent.

DeltaTTT then uses the nonlinear two-layer memory

\[
f_{A,B}(x)=B\phi(Ax)
\]

with layer-local squared losses.  In the paper's post-update form (Eqs. 7--12),

\[
A_t=A_{t-1}+\alpha_t(v_t-A_{t-1}k_t)k_t^\top,
\]
\[
h_t=\phi(A_tk_t),
\]
\[
B_t=B_{t-1}+\beta_t(v_t-B_{t-1}h_t)h_t^\top,
\]
\[
o_t=B_t\phi(A_tq_t).
\]

The paper also specifies the pre-update alternative, in which the hidden target is computed from the prior first-layer state.  Both layer updates remain Delta-shaped and state dependent.  The contribution is therefore not “two independent linear memories”: the second update's key/hidden target is induced by the first evolving memory and a nonlinearity.  The paper derives chunkwise algorithms that preserve this nonlinear recurrent readout rather than replacing the serial rule by one global fixed-base sum.

## Claims and assumptions checked

- The paper's exactness claim concerns its derived chunkwise evaluation of the specified layerwise recurrent update, not exact equivalence between arbitrary serial TTT and a fixed-base approximation.
- The local targets and squared layer losses are explicit.  They are not evidence that any arbitrary auxiliary reconstruction loss improves language modelling.
- The reported 0.54B-parameter, 92.5B-token and RULER results are author experiments.  They were read as evidence of feasibility only; this project did not execute, score or reproduce them.
- “Nonlinear memory” here has a concrete two-layer parameter state `(A,B)`.  Merely putting an MLP before or after a Delta state is not automatically equivalent, but a candidate must show a mathematical difference rather than rely on the word nonlinear.

## Collision consequences for this discovery pool

DeltaTTT directly covers the broad idea “stack multiple Delta updates with layer-local prediction targets to obtain a nonlinear recurrent memory”.  Consequently, the following are baselines rather than countable new candidates:

1. adding a second Delta matrix whose key is the first matrix's hidden activation;
2. changing only pre- versus post-update hidden targets;
3. attaching local squared reconstruction targets to successive Delta layers;
4. claiming novelty solely from retaining a nonlinear readout while using exact chunkwise evaluation.

It does **not** directly implement the residual objects currently under review:

- D01's exact rank-one compression of one counterfactual full-state branch under a shared future affine recurrence and delayed Bayesian branch resolution;
- D03's transported future-query/observability metric used to choose a constrained current write direction;
- D06's proposed determinant/information-budget control object.

Those non-collisions are narrow.  They do not establish originality, and they do not remove the need for the separate recurrent-ensemble, optimal-control/query-aware, and online log-determinant audits.

## Interface and cost implications

The recurrent state contains two matrices, and each token performs two state-dependent Delta-like updates plus nonlinear feature evaluation.  A future implementation comparison therefore needs to account for both state matrices, both update paths and the chunkwise algorithm; comparing only the nominal asymptotic order of one matrix would hide the constant-factor and activation-storage costs.  No code interface is recorded because no author-designated implementation was found in the bounded search.

## Pool disposition

No candidate is added from DeltaTTT.  It strengthens the nearest-work exclusion boundary: “multi-layer/local-target/nonlinear Delta” is already an explicit 2026 method family.  The paper is too recent to infer community validation, and its empirical claims remain unreplicated here.
