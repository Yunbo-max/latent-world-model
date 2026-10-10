# R11 — Query-risk order-gap compression (attempt 1)

## Status and lineage

- Parent: `rejected/AFFINE_MAGNUS_COMMUTATOR_CONTROL.md` (blob `c184a16121d5148fcc855b2564ed3174bec36788`).
- Failure being repaired: the parent correctly derived the affine order gap, but the proposed “commutator cancellation” target erased chronology. That is a **target mismatch**, not a dimensional error and not evidence that order effects are useless.
- Patch: preserve the signed chronological gap and ask only whether it can be compressed under an explicit rank and future-query-risk budget.
- Outcome: the conditional mathematics below is sound and falsifiable, but the construction is a generic weighted low-rank control; exact ordered Delta/WY composition and DeltaProduct already cover the main mechanism. Park as a theorem/control, not a new active architecture.
- Candidate accounting: historical candidates `5`; active `0`; scientifically admitted `0`; selected `0`.

## 1. Formal object

Let a frozen-feature Delta step be the affine map

\[
T_a(S)=A_aS+B_a,\qquad
A_a=I-\beta_a k_ak_a^\top,\quad B_a=\beta_a k_av_a^\top,
\]

with \(S\in\mathbb R^{d_k\times d_v}\), \(k_a\in\mathbb R^{d_k}\), \(v_a\in\mathbb R^{d_v}\). For two events \(i,j\), define

\[
S_+=T_j(T_i(S)),\quad S_-=T_i(T_j(S)),\quad
K=S_+-S_-.
\]

The parent established exactly

\[
K=[A_j,A_i]S+(A_j-I)B_i-(A_i-I)B_j. \tag{1}
\]

The physical sequence order is observed. Let \(z\in\{+1,-1\}\) instead encode the possibly hidden **semantic target**: retain that observed order effect (\(+1\)) or prefer the reversed/corrective branch (\(-1\)). With \(\bar S=(S_++S_-)/2\),

\[
S_z=\bar S+\frac z2K. \tag{2}
\]

Thus “remove \(K\)” is not chronology preservation. The repaired problem is to approximate the signed correction \(zK/2\).

## 2. Exact Delta specialization and rank

Writing \(c=k_j^\top k_i\), direct expansion of (1) gives

\[
K=\beta_i\beta_j\left[
c\{k_j(k_i^\top S)-k_i(k_j^\top S)\}
-k_j(k_j^\top k_i)v_i^\top+k_i(k_i^\top k_j)v_j^\top
\right]. \tag{3}
\]

Every term has its left factor in \(\operatorname{span}\{k_i,k_j\}\); hence

\[
\operatorname{rank}(K)\leq \dim\operatorname{span}\{k_i,k_j\}\leq2. \tag{4}
\]

For \(k_i=k_j=k\), the linear commutator vanishes but the affine gap remains

\[
K=\beta_i\beta_j\lVert k\rVert^2 k(v_j-v_i)^\top,
\]

which is rank one unless the target values agree. This rechecks the parent counterexample: commuting transitions do not imply commuting affine writes.

At the other extreme, \(k_i^\top k_j=0\) makes every term in (3) vanish, so orthogonal keys give \(K=0\). Equal-key and orthogonal-key limits are explicit rank boundaries, not evidence for a generic nonzero correction.

## 3. Query-risk optimal rank budget

Let \(G\succeq0\) be a causal estimate of future query Gram/risk on the key side. For an observed desired sign \(z\), choose a correction \(C\) of rank at most \(r\) by

\[
\min_{\operatorname{rank}(C)\le r}
\left\|G^{1/2}\left(\frac{zK}{2}-C\right)\right\|_F^2. \tag{5}
\]

If \(G\succ0\), set \(M=G^{1/2}zK/2\). Rank is invariant under multiplication by \(G^{1/2}\), so Eckart–Young–Mirsky gives

\[
C_r^*=G^{-1/2}[M]_r,\qquad
R_r^*=\sum_{\ell>r}\sigma_\ell(M)^2. \tag{6}
\]

For singular \(G\), a canonical optimum is \(C_r^*=G^{\dagger/2}[M]_r\) on \(\operatorname{range}(G)\). A null-risk addition \(N\) is allowed only when \(G^{1/2}N=0\) **and** \(\operatorname{rank}(C_r^*+N)\le r\); it is not an unrestricted degree of freedom. Equation (4) means an adjacent frozen-feature Delta swap is exactly representable with \(r=2\), while \(r=1\) loses exactly the second weighted singular component.

This is a conditional oracle construction: it requires the desired sign, the current state needed for \(K\), and a causal \(G\). Computing an SVD of the exact gap may cost more than simply retaining the ordered composition.

## 4. Selector impossibility is retained, not deleted

Suppose the allowed observable \(X\) does not reveal \(z\), with \(p=P(z=+1\mid X)\). Assume \(\bar S,K,G\) are \(X\)-measurable and the two branches are evaluated by the same \(G\). For any common estimator \(\widehat S(X)\), conditional squared query risk is minimized by the conditional mean

\[
\widehat S^*=\bar S+\frac{2p-1}{2}K, \tag{7}
\]

and its irreducible conditional risk is

\[
p(1-p)\lVert G^{1/2}K\rVert_F^2. \tag{8}
\]

At \(p=1/2\), the best common estimate is \(\bar S\) and the risk is \(\lVert G^{1/2}K\rVert_F^2/4\). Low-rank compression cannot manufacture a missing semantic selector. Sequence order itself is observed. Here \(z\) is only a **binary order-choice proxy**. General harmful-overwrite repair may instead suppress a write, change its target, protect a subspace, or wait for evidence; equations (7)–(8) do not claim to solve those larger action spaces.

## 5. Blocks and transported swap effects

For a block of affine maps in chronological order,

\[
A_{1:m}=A_m\cdots A_1,\qquad
B_{1:m}=\sum_{a=1}^m A_m\cdots A_{a+1}B_a. \tag{9}
\]

For the sign convention in (1), an adjacent swap at positions \(i,i+1\) obeys

\[
S_{\mathrm{final}}^{\mathrm{chronological}}-S_{\mathrm{final}}^{\mathrm{swapped}}
=P K_{i+1,i}(S_{i-1}),\qquad P=A_m\cdots A_{i+2}.
\]

Multiple swaps must be accumulated along a fixed swap path with intermediate states recomputed. A naive sum of gaps all evaluated at the original state is generally false.

## 6. Prediction, boundaries, and same-information controls

Predictions:

1. Under fixed features and a fixed causal \(G\), rank-\(r\) query error equals the tail in (6).
2. Rank one fails precisely when the second weighted singular value is nonzero; collinear keys collapse the adjacent gap to rank at most one (possibly zero).
3. A gate with exactly the same \(X\) and loss cannot beat the Bayes estimator (7). Improvement requires strictly richer causal information that changes \(P(z\mid X)\), or a separately stated constraint/loss for which (7) is no longer the comparator.

Failure boundaries:

- In a nonlinear network, future features change with the update; (1)–(9) are no longer a full causal effect and require the complete state Jacobian.
- A stale, noncausal, or branch-dependent \(G\) invalidates the common-metric optimum and the simple risk formula (8).
- Rank of the mathematical correction is not a hardware-cost guarantee.
- Only the branch difference is low rank: \(\bar S\) remains a full \(d_k\times d_v\) state and may require both branches or equivalent work. A dense \(G\) costs \(O(d_k^2)\) state, and dense left whitening can cost \(O(d_k^2d_v)\); no time or memory saving follows from rank \(r\) alone.
- Exact ordered recurrence or exact chunk composition dominates whenever it is affordable.

True same-oracle-information controls are direct rank-\(r\) SVD of the observed gap and the no-correction conditional mean (7). Exact sequential Delta and exact ordered affine/WY chunking are stronger non-oracle baselines. DeltaProduct is an ordered low-rank expressivity/parameterization control, not naturally a same-information control unless it is explicitly supplied the same \(K,G,z\) observables.

## 7. Decision

The repair salvages a useful result: chronology error has an exact query-weighted rank tail, and missing semantic order labels impose the irreducible risk (8). It does **not** establish a distinct model. Ordered Householder products and exact Delta chunking already preserve order; weighted truncated SVD is classical; and the semantic selector remains unidentifiable without extra evidence. Park R11 after attempt 1. Reopen only with a causal, same-budget estimator of \(G\) and selector information that yields a consequence not reducible to exact ordered composition or generic low-rank approximation. Empirical value remains unknown.
