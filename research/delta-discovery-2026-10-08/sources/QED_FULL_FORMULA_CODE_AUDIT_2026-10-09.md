# QED full-formula and public-code audit

Primary source: Gupta, Das and Gupta, *The Query Knows What to Forget: A Second Erase Direction for Linear Attention*, arXiv:2608.13668v1, submitted 2026-08-13.  Read on 2026-10-09: full HTML/PDF §§2--7 and Appendix A.  The arXiv record still exposes only v1.  Public GitHub repository/code searches over the exact arXiv ID, title, mechanism/ablation names and distinctive parameterization did not locate an author-designated implementation.  This is an availability result, not proof that private or future code does not exist.

## Exact orientation and ordered recurrence

QED uses key-by-value state

\[
S_t\in\mathbb R^{K\times V},\qquad o_t=S_t^\top q_t,
\]

with normalized \(q_t,k_t\in\mathbb R^K\).  Decay occurs before the rank-one edit:

\[
\bar S_t=D_tS_{t-1},\quad D_t=\operatorname{Diag}(e^{g_t}),\qquad
S_t=(I-k_ta_t^\top)\bar S_t+k_t(w_t\odot v_t)^\top .
\]

Thus the actual homogeneous transition is \((I-k_ta_t^\top)D_t\); the factors cannot be exchanged.

GDN-2 uses \(a_t=b_t\odot k_t\).  QED changes only this erase/read covector:

\[
a_t=b_t\odot k_t+\lambda_h d_t,
\qquad
d_t=P_{k_t}^{\perp}(b_t\odot q_t)
=b_t\odot q_t-k_t[k_t^\top(b_t\odot q_t)].
\]

The left write direction remains \(k_t\); QED is one rank-one update, not a second write along \(q_t\) and not a rank-two transition.  Relative to GDN-2,

\[
S_t^{\rm QED}-S_t^{\rm GDN2}
=-\lambda_hk_t(\bar S_t^\top d_t)^\top,
\]

and for the current query

\[
o_t^{\rm QED}-o_t^{\rm GDN2}
=-\lambda_h(q_t^\top k_t)\bar S_t^\top d_t.
\]

Consequently, the immediate correction is zero when \(q_t^\top k_t=0\), and every probe \(x\perp k_t\) still sees zero direct edit.  QED samples old state along a gated query-derived direction and injects a negative correction along the editable key direction.  It does not identify target versus still-useful interference, so signed cancellation is not a monotone semantic-error theorem.

## Stability scope

Because \(d_t^\top k_t=0\), the query term does not change the nontrivial eigenvalue \(1-a_t^\top k_t\).  It does not follow that the factor is Euclidean-nonexpansive.  Write \(a=ck+su\), with unit \(k,u\) and \(u\perp k\).  In the \([k,u]\) basis,

\[
I-ka^\top=
\begin{bmatrix}1-c&-s\\0&1\end{bmatrix},
\qquad
\|(I-ka^\top)u\|^2=1+s^2.
\]

Any nonzero oblique component therefore has singular norm above one even though the eigenvalue is unchanged.  Adding the ordered, noncommuting \(D_t\) does not repair this inference.  QED gives neither a global contraction nor an ordered-product/Lyapunov theorem.

The paper itself reports that the projection safeguard was nearly inactive in the two unprojected trained models: the observed nontrivial eigenvalue stayed in \([-0.011,0.985]\), and counterfactual projection changed it by less than \(10^{-3}\).  Gate and projection necessity were inconsistent across the two seeds.  These are the authors' bounded empirical observations, not results reproduced here.

## Parameter and cost claims

Appendix A sets

\[
\lambda_h=0.25\,\sigma(\theta_h),
\]

one scalar per layer/head, initialized with \(\theta_h=-2\), with a tenfold learning-rate multiplier.  Setting \(\lambda_h=0\) exactly recovers GDN-2.  State remains \(O(KV)\), and constructing \(d_t\) adds \(O(K)\) arithmetic.  The paper states one extra dot product and subtraction per token/head and structural compatibility with the GDN-2 kernel.  It provides no public kernel, chunk/WY derivation, wall-clock table or memory table, so implementation-level fusion/throughput is unavailable rather than verified.

## Exclusion boundary

Already occupied by QED and therefore baseline-only here:

1. a current-query-derived second erase/read direction;
2. projection of that direction into the current key's orthogonal complement;
3. channel-wise gating of the query correction;
4. a bounded learned scalar strength per head;
5. sampling \(\bar S_t^\top d_t\) and writing its negative along \(k_t\);
6. keeping a single rank-one fixed-state recurrence;
7. query, fixed-random, ungated and unprojected ablations.

QED does not by itself close routes that change the left write direction, use stable source identity, derive a full ordered-product invariant, or introduce a different causal observable.  Those routes still require their own nearest-work and necessity audits.

No repository code, software test, training, inference, benchmark scoring, asset download or GPU job was executed.
