# R11 v2: pure-Delta factor-core order-gap decision — exact two-dimensional reduction and selector/compression split

Status: repair attempt 2 of at most 3. Versioned child of `repairs/R11_ORDER_GAP_COMPRESSION.v1.md`, SHA256 `38d5ba6cb4e897b602b9897c940468cdaab0b603f5e3d9055b3f98dc52e1929b`. The parent, its counterexamples, and all three reviews remain unchanged. This artifact contains mathematics, source comparison, and measurement feasibility only. It does not run project code, tests, models, training, inference, scoring, or benchmarks.

## 1. Original problem, exact failure, and patch

R11 v1 correctly proved that the frozen-feature adjacent Delta order gap has rank at most two and that a missing semantic order selector produces irreducible query risk. Its computational account was nevertheless too pessimistic: it wrote the optimum as a dense whitening and SVD of `G^{1/2}K`, even though the Delta gap has a stronger factorization that v1 did not expose. The failure is therefore a **missed algebraic/computational consequence**, not a sign error in v1 and not evidence that the semantic selector has become identifiable.

The patch has three parts.

1. Rewrite the exact order gap using the two keys and two residuals at one common pre-state.
2. Reduce every nonzero weighted singular component to an at-most `2 x 2` core, without forming `G^{1/2}` or a dense SVD.
3. Solve selector uncertainty and rank compression jointly, so information error and compression error are not conflated.

The repair preserves the old conclusion that exact ordered Delta/WY composition is the strongest no-oracle baseline and that low-rank algebra cannot supply evidence about whether chronology is semantically harmful.

Scope is deliberately narrow. Equations below apply to two **pure scalar-`beta` Delta** maps of the form (1), with no intervening left decay `D_t`, normalization, or state-dependent feature recomputation. A gated/decayed rule such as `(I-beta kk^T)D_tS+beta kv^T` generally has additional `D_t`- and state-dependent order terms and need not admit the two-key/two-residual factorization below.

## 2. Exact residual factorization

Let the common pre-state be `S in R^{d_k x d_v}` and define two frozen-feature Delta maps

\[
T_a(S)=S+\beta_a k_a\bigl(v_a-S^\top k_a\bigr)^\top,
\qquad a\in\{i,j\}. \tag{1}
\]

Write

\[
e_i=v_i-S^\top k_i,\qquad e_j=v_j-S^\top k_j,
\qquad c=k_i^\top k_j,\qquad \gamma=\beta_i\beta_j c. \tag{2}
\]

For `S_+=T_j(T_i(S))`, `S_-=T_i(T_j(S))`, direct substitution gives

\[
K:=S_+-S_-
=\gamma\left(k_i e_j^\top-k_j e_i^\top\right). \tag{3}
\]

For example, after the `i` write the residual of `j` is

\[
e_{j\mid i}=v_j-T_i(S)^\top k_j=e_j-\beta_i c e_i. \tag{4}
\]

Using (4) in the two ordered branches yields (3). This is equivalent to the affine-commutator expansion in v1 but exposes more structure. Define

\[
U=[k_i,\ k_j]\in\mathbb R^{d_k\times2},\qquad
V=\gamma[e_j,\ -e_i]\in\mathbb R^{d_v\times2}. \tag{5}
\]

Then

\[
K=UV^\top. \tag{6}
\]

Consequently `rank(K)<=2`, with exact degeneracies:

- `c=0`, `beta_i=0`, or `beta_j=0` implies `K=0`;
- collinear keys or collinear residual columns imply `rank(K)<=1`;
- `rank(K)=2` requires `gamma != 0`, `rank(U)=2`, and `rank(V)=2`;
- for `k_i=k_j=k`, equation (3) becomes `beta_i beta_j ||k||^2 k(v_j-v_i)^T`, reproducing the v1 affine same-key counterexample.

Equation (4) also repairs a hidden information-cost claim. If the chronological execution observes `e_i` and then `e_{j|i}`, the common-prestate residual is recoverable as

\[
e_j=e_{j\mid i}+\beta_i c e_i. \tag{7}
\]

Thus an adjacent-pair diagnostic need not reread the full pre-state. It must retain `(k_i,e_i,beta_i)` until `j` and pay vector inner-product/reconstruction cost. This is causal for the observed adjacent pair, but it does not predict the second event before it arrives and does not scale for free to all pairs in a long block.

## 3. Query-weighted optimum from a `2 x 2` core

Let `G>=0` be a declared, prefix-lawful query-risk matrix on key space. For now take a deterministic desired scalar `a` and solve

\[
\min_{\operatorname{rank}(C)\le r}
\left\|G^{1/2}(aK-C)\right\|_F^2. \tag{8}
\]

Set `X=G^{1/2}U`. Take compact rank-revealing factorizations

\[
X=Q_xR_x,\qquad V=Q_vR_v, \tag{9}
\]

where `Q_x in R^{d_k x q_x}` and `Q_v in R^{d_v x q_v}` have orthonormal columns, `q_x,q_v<=2`, and `R_x in R^{q_x x 2}`, `R_v in R^{q_v x 2}` have full row rank. Then

\[
G^{1/2}K=Q_xHQ_v^\top,\qquad H=R_xR_v^\top\in\mathbb R^{q_x\times q_v}. \tag{10}
\]

All nonzero weighted singular values of `K` are exactly the singular values of the at-most `2 x 2` matrix `H`. If `[aH]_r` is its best rank-`r` truncation, a canonical solution of (8) is

\[
C_r^*=U R_x^\dagger[aH]_rR_v^{\dagger\top}V^\top, \tag{11}
\]

because `R_xR_x^dagger=I_{q_x}` and `R_vR_v^dagger=I_{q_v}`. Its weighted image is `Q_x[aH]_rQ_v^T`, and

\[
\min (8)=\sum_{\ell>r}\sigma_\ell(aH)^2. \tag{12}
\]

The formula remains valid for singular `G` because the compact factorization drops its null-risk directions. Other optima may add `N` with `G^{1/2}N=0` only if the total rank constraint is still satisfied.

No explicit square root of `G` is needed. Small factors can be obtained from

\[
U^\top G U=R_x^\top R_x,\qquad V^\top V=R_v^\top R_v, \tag{13}
\]

using rank-revealing eigendecompositions or Cholesky-like factors of the two `2 x 2` Gram matrices. Therefore the exact weighted compression needs two applications of `G` to key vectors, vector inner products, and one at-most `2 x 2` SVD rather than a dense `d_k x d_v` SVD. A dense `G` still costs `O(d_k^2)` state and its two matvecs still cost `O(d_k^2)`; a lawful low-rank/query-sketch representation can reduce that cost, but the sketch and its estimation error must be counted separately.

If a one-pair correction is stored in factored rank-`r` form, storage is `O(r(d_k+d_v))` and a query-time correction can be applied without materializing a dense matrix. The nominal Delta memory `S` remains full-width. The overlay must also participate in every later residual `v-S^Tk`; repeated corrections grow its rank unless they are carried, merged, recompressed, or materialized, each with additional cost or approximation error. Materializing `C_r^*` into `S` costs `O(r d_k d_v)` arithmetic/writes, so a small core is not by itself a persistent-state or hardware-speed guarantee.

## 4. Joint selector and compression theorem

Let the physical order be observed, while a hidden binary semantic target `z in {+1,-1}` says which signed branch difference is desired. Conditional on allowed information `X`, assume

\[
p=P(z=+1\mid X),\qquad m=E[z\mid X]=2p-1, \tag{14}
\]

and that `K` and the same branch-independent `G` are `X`-measurable. Define

\[
\bar S=\frac{S_++S_-}{2},\qquad S_z=\bar S+\frac z2K. \tag{15}
\]

First consider a **centered representation budget**: an estimator `S_hat=bar S+C` with `rank(C)<=r`. Its conditional risk is

\[
\begin{aligned}
E\left[\left\|G^{1/2}\left(\frac z2K-C\right)\right\|_F^2\mid X\right]
&=p(1-p)\left\|G^{1/2}K\right\|_F^2\\
&\quad+\left\|\frac m2G^{1/2}K-G^{1/2}C\right\|_F^2. \tag{16}
\end{aligned}
\]

Applying Section 3 with `a=m/2` gives

\[
C_r^*=U R_x^\dagger\left[\frac m2H\right]_rR_v^{\dagger\top}V^\top, \tag{17}
\]

and the exact optimum

\[
\mathcal R_r^*
=p(1-p)\sum_\ell\sigma_\ell(H)^2
+\frac{m^2}{4}\sum_{\ell>r}\sigma_\ell(H)^2. \tag{18}
\]

The first term is selector-information error; the second is centered-representation compression error. They have different remedies. Tied singular values make the optimizing factors nonunique, although the risk is unique.

This centered theorem is not yet a same-budget deployed edit theorem. Suppose the actually executed physical branch has observed sign `s in {+1,-1}` and state

\[
S_s=\bar S+\frac s2K. \tag{19}
\]

If the allowed deployed edit is `Delta` with `rank(Delta)<=r`, the target displacement is `((z-s)/2)K`, not `zK/2`. The exact conditional identity becomes

\[
\begin{aligned}
E\left[\left\|G^{1/2}\left(\frac{z-s}{2}K-\Delta\right)\right\|_F^2\mid X\right]
&=p(1-p)\left\|G^{1/2}K\right\|_F^2\\
&\quad+\left\|\frac{m-s}{2}G^{1/2}K-G^{1/2}\Delta\right\|_F^2. \tag{20}
\end{aligned}
\]

Therefore the same physical edit budget gives

\[
\Delta_r^*=U R_x^\dagger\left[\frac{m-s}{2}H\right]_rR_v^{\dagger\top}V^\top, \tag{21}
\]

\[
\mathcal R_{r,\mathrm{phys}}^*
=p(1-p)\sum_\ell\sigma_\ell(H)^2
+\frac{(m-s)^2}{4}\sum_{\ell>r}\sigma_\ell(H)^2. \tag{22}
\]

The actual no-edit baseline is `Delta=0`, whose conditional risk is `(1-p)||G^{1/2}K||_F^2` when `s=+1`, and `p||G^{1/2}K||_F^2` when `s=-1`. By contrast, `C=0` in the centered theorem moves to the midpoint and generally requires a rank-at-most-two physical edit `-sK/2`; it is not a no-op.

Equations (17)--(22) use the true conditional mean `m`. If a plug-in estimate `m_hat=2p_hat-1` is used with the same top-`r` singular subspace, its physical-branch risk is

\[
p(1-p)\sum_\ell\sigma_\ell(H)^2
+\frac{(m-\widehat m)^2}{4}\sum_{\ell\le r}\sigma_\ell(H)^2
+\frac{(m-s)^2}{4}\sum_{\ell>r}\sigma_\ell(H)^2. \tag{23}
\]

Thus selector calibration error is paid on the retained core directions. Estimator training, state, latency, and transfer error must be charged exactly as for a direct same-information action predictor.

- If `p=1/2`, then `m=0`, `C_r^*=0`, and no rank budget can beat the irreducible risk `||G^{1/2}K||_F^2/4`.
- If `p` is `0` or `1`, selector uncertainty vanishes and (18) reduces to the observed-sign centered rank tail from v1.
- If `r>=rank(H)`, compression error vanishes, but selector uncertainty remains.
- For a centered rank-one representation, the geometric second-mode potential is `sigma_2(H)^2`; its actual compression penalty is `(m^2/4)sigma_2(H)^2` and therefore also vanishes when `m=0`. For a physical rank-one edit, replace `m` by `m-s`.

The centered theorem corrects the v1 separation between its oracle rank truncation and unrestricted Bayes conditional mean; the physical theorem corrects the update-budget base point. Neither identifies `p`, causal future validity, or a richer action such as suppressing a write, delaying it, changing the value, or protecting a subspace.

## 5. Predictions, counterexamples, and failure boundaries

Falsifiable mathematical predictions:

1. The up-to-two nonzero weighted singular values computed from a direct `G^{1/2}K` must equal those of `H`, up to numerical tolerance, whenever both are formed under the same frozen state and metric.
2. The geometric rank-one tail potential is nonzero exactly when `sigma_2(H)>0`; its risk coefficient can still vanish when the relevant conditional-mean scalar is zero. The geometric tail disappears under orthogonal keys, zero gates, collinear weighted keys, or collinear residual columns.
3. At fixed `H`, increasing selector certainty changes the centered optimum through both terms in (18): irreducible uncertainty falls as `p(1-p)`, while the value of centered rank grows as `(2p-1)^2`. The physical coefficient instead depends on the executed sign through `(m-s)^2`.
4. A same-information direct rank-`r` action predictor can match (21); the factor core claims exact computation and decomposition of risk, not extra semantic information.

Failure boundaries:

- Equations (1)--(23) are frozen-feature/local-state results for the pure Delta map (1). Endogenous future keys, gates, values, and queries require the complete recurrent Jacobian and may change both `K` and `G`.
- If the two semantic branches use different metrics `G_+` and `G_-`, equations (16) and (20) are not the correct common-metric bias-variance splits.
- `G` must be decision-time lawful and action invariant: a fixed query distribution, frozen path, or explicitly declared causal surrogate. If future queries or keys are generated from the chosen state, the true metric is action dependent and these equations are only a local surrogate. A realized future-query Gram, future answer, or old-fact-validity oracle is not deployable evidence.
- Equation (7) covers one adjacent chronological pair. Maintaining common-prestate residuals for many possible swaps requires extra retained events or recomputation; multiple swaps remain path-dependent because intermediate states change.
- An ill-conditioned `U^T G U` or `V^T V` makes factor recovery numerically sensitive even though the exact rank is at most two. Rank thresholds and finite precision must be declared.
- The binary reversed-order proxy is not a general harmful-overwrite model. Valid chronology may need no correction; harmful revision may require an action outside the two-branch span.

## 6. Information, state, and compute ledger

Required online information at the second event is: current `(k_j,v_j,beta_j)`, retained `(k_i,e_i,beta_i)`, the post-`i` residual `e_{j|i}`, a prefix-lawful representation or matvec interface for `G`, and either a declared `p` estimator or an oracle used only for analysis. Additional temporary state is `O(d_k+d_v)` for one pending pair plus the `G` representation. The `2 x 2` algebra is negligible compared with residual construction, `G` applications, or dense state writes.

The strongest same-information simple controls, all referenced to the actually executed branch, are:

1. exact observed chronological Delta recurrence with `Delta=0`;
2. exact ordered WY/chunk evaluation;
3. the direct scalar plug-in edit `((m_hat-s)/2)K` when the rank budget admits it;
4. direct rank-`r` prediction of the physical edit from the same `X`, same `G/p` estimator, and same carry/materialization budget;
5. DeltaProduct with matched state/compute as an ordered low-rank expressivity control, but only a same-information semantic control if it receives the same selector and metric observables.

Any comparison must charge retained residual/key traffic, the estimator and state for `G` and `p`, selector calibration error, overlay carry/merge/recompression or materialization, factor application, and any second branch. The small-core identity eliminates a dense SVD; it does not eliminate these costs.

## 7. Measurement feasibility and disposition

The inspected author group-state code defines cumulative group-product labels and invokes token/sequence accuracy, so it can in principle test order representation; the exact native scorer revision and denominator remain unpinned. It does not expose a harmful-versus-legitimate semantic selector, the internal common-prestate gap `K`, a causal query metric `G`, or paired counterfactual branches. Parent-audited bAbI/LAMBADA assets likewise do not natively supply those objects. Therefore the factor identity and risk decomposition admit a future numerical algebra/engineering check, but that would not be a native scientific benchmark or evidence for the semantic selector. No new benchmark, data, label, metric, result, or score is created here.

The repair is useful within its pure-Delta scope: the adjacent gap is not merely rank at most two; it is an exact two-key/two-residual product, its weighted optimum is an at-most `2 x 2` problem, and selector uncertainty plus rank loss obey the closed decompositions (18) and (22). The sequential reconstruction (7) is a Delta-specific identity and cost correction; no priority or method-novelty claim is made for it.

The method-level contribution remains insufficient. Small-core SVD of factored low-rank modifications and weighted low-rank truncation are classical; exact ordered Delta/WY and DeltaProduct already preserve order; and no causal selector or native semantic measurement has been supplied. This is a **corrected theorem/control**, not a new active architecture.

- Mathematical status: conditional, pending independent final-byte review.
- Contribution status: exact Delta factorization and cost correction; major generic low-rank-factorization and ordered-Delta collisions remain.
- Empirical status: unknown; no execution occurred.
- Candidate admission: `0`.
- Disposition: **park after repair attempt 2**.

Reopen a third attempt only with a prefix-lawful estimator of both the query metric and semantic selector, a matched-total-cost advantage over exact ordered Delta and a direct same-information action predictor, plus an existing native object that measures the claimed choice. A different `2 x 2` solver, rank threshold, or renamed gate is not a new delta.
