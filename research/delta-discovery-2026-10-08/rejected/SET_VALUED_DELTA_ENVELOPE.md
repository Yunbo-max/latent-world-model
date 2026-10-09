# Set-valued Delta envelope: feasible-map control and branching boundary

Disposition: **rejected as a distinct candidate; retained as a set-membership control**. Mathematics/source analysis only; no model, benchmark, test, download or experiment was run.

## Exact causal object

Let \(S\in\mathbb R^{d_k\times d_v}\), \(s=\operatorname{vec}(S)\), and

\[
H_t=I_{d_v}\otimes k_t^\top,
\qquad H_ts=v_t.
\]

For a bounded residual model, maintain

\[
\mathcal C_t^- =F_t\mathcal C_{t-1}+b_t\oplus\mathcal W_t,
\qquad
\mathcal C_t=\mathcal C_t^-\cap
\{s:\|H_ts-v_t\|_{R_t^{-1}}\le1\}.
\]

The actual ordered Delta transition

\[
S_t=A_tS_{t-1}+B_t,
\quad A_t=(I-\beta_tk_tk_t^\top)D_t,
\quad B_t=\beta_tk_tv_t^\top
\]

corresponds to \(F_t=I_{d_v}\otimes A_t\) and \(b_t=\operatorname{vec}(B_t)\). This is precisely a time-varying feasible-parameter-set recursion. When \(D=I\) and \(\beta=\|k\|^{-2}\), the Delta transition already projects every prior map onto the current measurement hyperplane, so the post-update intersection is redundant.

## Ellipsoidal approximation

For \(\mathcal E(c,P)=\{c+P^{1/2}u:\|u\|\le1\}\), an outer prediction through process ellipsoid \(\mathcal E(0,Q)\) is

\[
c^-=Fc+b,
\qquad
P^-=(1+\rho^{-1})FPF^\top+(1+\rho)Q,
\quad \rho>0.
\]

Combining the prior quadratic \(g_0\) and measurement quadratic \(g_1\), any \(\lambda\in[0,1]\) gives the S-procedure outer ellipsoid defined by

\[
A_\lambda=(1-\lambda)(P^-)^{-1}+\lambda H^\top R^{-1}H,
\]

\[
b_\lambda=(1-\lambda)(P^-)^{-1}c^-+\lambda H^\top R^{-1}v,
\qquad c_\lambda=A_\lambda^{-1}b_\lambda,
\]

and shape \((1-d_\lambda)A_\lambda^{-1}\), where completing the square defines

\[
d_\lambda=(1-\lambda)c^{-\top}(P^-)^{-1}c^-
+\lambda v^\top R^{-1}v-b_\lambda^\top A_\lambda^{-1}b_\lambda.
\]

This is classical outer-bounding ellipsoid/set-membership filtering, not a new Delta recurrence.

For a query \(q\), \(G_q=I_{d_v}\otimes q^\top\) maps the feasible set to output set \(\mathcal O(q)=G_q\mathcal C\). The ellipsoid gives center \(G_qc\), shape \(G_qPG_q^\top\), and directional support

\[
h_{\mathcal O(q)}(z)=z^\top G_qc+sqrt{z^\top G_qPG_q^\top z}.
\]

Returning a center, robust choice, sample or abstention is a downstream decision; the set does not create a unique language output.

## What the set cannot identify

If revision and coexistence worlds have identical causal observables, every causal deterministic set recursion produces the same set and every randomized one the same state distribution. A conflict relaxation score may detect inconsistency but cannot say why it occurred.

A single fixed linear map cannot point-read two different values at one identical address. Exact deferred semantics therefore needs a nonconvex union

\[
\mathcal C_t^{\rm revise}\cup\mathcal C_t^{\rm coexist}.
\]

Replacing this union by one convex ellipsoid/polytope introduces interpolated maps that correspond to neither hypothesis. With \(m\) unresolved binary decisions, exact branching can require \(2^m\) components. Pruning/merging is an approximation; a weighted union is ordinary multiple-model/Bayesian filtering.

Noiseless consistency itself is standard. With \(K=[k_i]\) and \(V=[v_i]\), a map satisfying \(S^\top K=V\) exists iff \(Vz=0\) for every \(z\in\ker K\), and is unique only when the key span is full. In unseen key directions an unbounded version space gives no bounded prediction.

## State, assumptions and costs

Let \(n=d_kd_v\). An exact polytope/SOC representation accumulates active constraints and needs LP/SOCP support queries. A full ellipsoid has \(O(n^2)\) state and naive \(O(n^3)\) updates; per-value blocks cost \(O(d_vd_k^2)\), while diagonal/low-rank forms sacrifice correlations and coverage tightness. A union multiplies these costs by its component count.

Learned \(Q,R\) can be inflated to avoid infeasibility, so an unknown-but-bounded coverage claim requires externally meaningful, past-calibrated bounds. Pure text provides no such noise process automatically. A robust CE built from logit intervals is trainable, but it does not prove distribution-free coverage.

## Closest work and measurement gap

The direct collisions are foundational set-membership recursion (Bertsekas & Rhodes, IEEE TAC 1971, DOI 10.1109/TAC.1971.1099674), recursive feasible-parameter sets and bounding ellipsoids, set-membership NLMS/optimal bounding spheroids (Gollamudi et al., IEEE SPL 1998, DOI 10.1109/97.668945), version spaces (Mitchell, IJCAI 1977), and multiple-model filters. Modern uncertainty-aware linear-attention work, including Kalman Linear Attention, Preconditioned DeltaNet and Kalman Delta Networks, further occupies mean/covariance approximations.

LongMemEval, MINTEval and MemConflict can test downstream update/conflict behavior but do not supply per-step latent maps or verified \(Q/R\) bounds, so they cannot establish set coverage. bAbI/LAMBADA likewise do not measure the proposed geometry. The route should not invent a benchmark or scorer.

**Ruling:** a convex feasible set can express uncertainty but cannot create missing identity or preserve discrete revision/coexistence branches without a union whose cost grows. The mechanism is classical set-membership filtering plus known approximation choices; no D-number is assigned.
