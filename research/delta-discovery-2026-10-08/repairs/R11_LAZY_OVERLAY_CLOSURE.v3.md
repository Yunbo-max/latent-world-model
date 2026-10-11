# R11 v3: lazy order-gap overlay closure and sharp cumulative-rank boundary

Status: repair attempt 3 of 3. Versioned child of `repairs/R11_FACTOR_CORE_ORDER_GAP.v2.md` (SHA256 `452b5753a732a6b9d868ecf2d3647a9d6efcc5f8c0c8fd6932b58342847d0b63`) and `repairs/R11_ORDER_GAP_COMPRESSION.v1.md` (SHA256 `38d5ba6cb4e897b602b9897c940468cdaab0b603f5e3d9055b3f98dc52e1929b`). Parent bytes, counterexamples, and reviews remain unchanged. This artifact is mathematics/source/measurement analysis only; no project code, model, test, training, inference, scorer, benchmark, data, or download was run.

## 1. Exact failure and patch

V2 correctly factors one pure-Delta adjacent order gap into a two-key/two-residual product and reduces its weighted truncation to an at-most `2 x 2` core. It also correctly warns that a correction must participate in every later residual. Its cost statement is nevertheless too broad: a **single** rank-`r` correction carried through later fixed-feature pure-Delta maps does not grow rank and does not require materialization or recompression.

The repair distinguishes four objects that v2 partially conflated:

1. passive propagation of one existing overlay;
2. injection of additional semantic corrections;
3. lossy fixed-rank recompression of their accumulated sum;
4. the full closed-loop difference when later features, selectors, or query metrics depend on the chosen state.

The retained result is an exact closure/capacity theorem and a correction to the cost ledger. It does not provide the missing semantic selector or a lawful future-query oracle.

## 2. Single-overlay closure is exact

Let

\[
T_t(S)=A_tS+B_t,\qquad
A_t=I-\beta_tk_tk_t^\top,\qquad
B_t=\beta_tk_tv_t^\top,                                      \tag{1}
\]

with `S in R^{d_k x d_v}`. Assume that the base and corrected paths use the same realized `(k_t,v_t,beta_t)`; equivalently these coefficients are held fixed and action invariant for the comparison. If the corrected state is `S+C`, then

\[
T_t(S+C)-T_t(S)=A_tC.                                        \tag{2}
\]

For `C=LR^T`, `L in R^{d_k x r}`, `R in R^{d_v x r}`, exact lazy propagation is

\[
L\leftarrow A_tL=L-\beta_tk_t(k_t^\top L),\qquad R\leftarrow R. \tag{3}
\]

Hence `rank(A_tC)<=rank(C)`; when `A_t` is invertible the rank is preserved. The overlay changes the residual and query output by

\[
e_t^{\rm corrected}=e_t^{\rm base}-C^\top k_t,
\qquad \Delta o(q)=C^\top q=R(L^\top q).                     \tag{4}
\]

The overlay therefore cannot be ignored by later writes, but it need not be materialized. Its state is `O(r(d_k+d_v))`; (3) costs `O(rd_k)` per fixed-coefficient write; a query correction costs `O(r(d_k+d_v))`. The full base state remains dense, and these are arithmetic identities rather than hardware speed claims.

For unit `k_t`, eigenvalues of `A_t` are `1` off the key and `1-beta_t` along it. More generally, if

\[
0\le \beta_t\|k_t\|^2\le2,                                  \tag{5}
\]

then `||A_t||_2<=1`, so a passive overlay is nonexpansive in Frobenius norm. At `beta_t||k_t||^2=1`, its key-aligned left factor can be annihilated. Stability is therefore not retention.

## 3. Repeated injections and exact variation of constants

Let `E_t` be a new correction inserted after map `t`. Under a common fixed coefficient path,

\[
C_t=A_tC_{t-1}+E_t,                                          \tag{6}
\]

and, with `Phi_{b:a}=A_b...A_a` and empty products equal to identity,

\[
C_T=\Phi_{T:1}C_0+\sum_{u=1}^T\Phi_{T:u+1}E_u.              \tag{7}
\]

Thus

\[
\operatorname{rank}(C_T)\le
\min\left(d_k,d_v,\operatorname{rank}(C_0)+\sum_u\operatorname{rank}(E_u)\right). \tag{8}
\]

Passive propagation is not the source of rank growth; linearly independent **new injections** are. Shared left carriers or a shared right-residual span are genuine low-rank closure cases.

## 4. A new order gap depends on the corrected pre-state

For one adjacent pair, write the two affine branches as

\[
T_s(S)=P_sS+b_s,\qquad s\in\{+1,-1\},                       \tag{9}
\]

and set `\bar P=(P_++P_-)/2`. Define

\[
K(S)=T_+(S)-T_-(S)=MS+d,\qquad M=P_+-P_-.                  \tag{10}
\]

For pure Delta, `K(S)=gamma(k_i e_j^T-k_j e_i^T)` as in v2 and

\[
M=\beta_i\beta_j(k_i^\top k_j)(k_jk_i^\top-k_ik_j^\top).   \tag{11}
\]

Therefore an existing overlay changes the next gap:

\[
K(S+C)=K(S)+MC.                                              \tag{12}
\]

This is the term a naive independent-injection account omits. Let `m=E[z|X]` and let the v2 physical edit scalar be `a=(m-s)/2`. Evaluating the edit on the actual corrected pre-state gives

\[
\begin{aligned}
C_{\rm post}
&=P_sC+aK(S+C)\\
&=(P_s+aM)C+aK(S)\\
&=\left(\bar P+\frac m2M\right)C+\frac{m-s}{2}K(S).        \tag{13}
\end{aligned}
\]

Equation (13) assumes the full scalar edit `aK(S+C)` is admitted, for example because the rank budget contains the gap. For a truncated rank-r core, the truncation subspace can depend on the corrected state and metric, and the same homogeneous identity need not hold. For `m=+1` or `m=-1`, the full-edit homogeneous operator is exactly `P_+` or `P_-`. If one instead injects only `aK(S)` while propagating by `P_s`, the omitted local term is `aMC`. When `m` and the injection schedule are held fixed/action invariant for this comparison, equation (13) remains an affine left-transport-plus-rank-at-most-two-injection recurrence, so (7)--(8) apply with the appropriate homogeneous factors. If the selector changes with the corrected state, the later closed-loop boundary applies instead. In neither case does (13) make repeated repairs independent.

## 5. Sharp rank and query-capacity boundary

The `2m` worst-case bound for `m` genuine R11 gaps is attainable. Allocate each pair `p` to a disjoint two-dimensional key block with basis `(e_{2p-1},e_{2p})` and value block `(f_{2p-1},f_{2p})`. Choose

\[
k_i=e_{2p-1},\quad k_j=e_{2p-1}+e_{2p},\quad
e_j=f_{2p-1},\quad e_i=-f_{2p},\quad \beta_i=\beta_j=1.     \tag{14}
\]

Then `k_i^Tk_j=1` and the gap block is

\[
K_p=k_ie_j^\top-k_je_i^\top
=\begin{bmatrix}1&1\\0&1\end{bmatrix},                    \tag{15}
\]

which has rank two. Orthogonal later blocks preserve earlier left blocks, so the accumulated block-diagonal gap has rank `2m` up to ambient dimension. Consequently no universal fixed-rank exact overlay handles more than `floor(r/2)` independent rank-two pair corrections.

This is a worst-case boundary, not a prevalence claim. If all injections share one right vector, arbitrarily many can remain rank one.

For a declared future query subspace `W` with orthogonal projector `P_W`, an overlay `C_hat` reproduces `C^Tq` for every `q in W` iff it satisfies `P_W C_hat=P_WC`. The minimum feasible rank is

\[
r_{\min}(W,C)=\operatorname{rank}(P_WC).                    \tag{16}
\]

The lower bound follows from `rank(P_W C_hat)<=rank(C_hat)` and the upper bound is attained by `C_hat=P_WC`. For a PSD query metric `G`, exact zero weighted error requires minimum rank

\[
r_{\min}(G,C)=\operatorname{rank}(G^{1/2}C),                \tag{17}
\]

and for rank `r<r_min` the best weighted error is

\[
\sum_{\ell>r}\sigma_\ell(G^{1/2}C)^2.                     \tag{18}
\]

Equations (16)--(18) generalize v2's one-gap `2 x 2` tail to the accumulated overlay; computing the optimum from skinny factors is generic low-rank maintenance, not a new R11 mechanism.

## 6. Recompression error is transported

Suppose an action-invariant injection schedule is held fixed and a deployed rank-r approximation performs

\[
\widehat C_t=\Pi_r(A_t\widehat C_{t-1}+E_t),\qquad
D_t=(I-\Pi_r)(A_t\widehat C_{t-1}+E_t).                     \tag{19}
\]

With exact `C_t` from (6), error `F_t=C_t-C_hat_t` obeys

\[
F_t=A_tF_{t-1}+D_t,\qquad
F_T=\Phi_{T:1}F_0+\sum_{u=1}^T\Phi_{T:u+1}D_u.             \tag{20}
\]

Locally optimal truncations need not minimize horizon loss: discarded components can add coherently after transport. Under (5), `||F_T||_F<=||F_0||_F+sum_u||D_u||_F`; with exact initialization `F_0=0`, this reduces to the discarded-tail sum. Without a bounded-product/contraction condition the errors can be amplified.

If later injections, selectors, or features consume the approximate memory, they need not be common between exact and approximate paths. Equation (20) then acquires injection-difference and feature-path terms. A full closed-loop guarantee needs the complete recurrent Jacobian or explicit Lipschitz/tube assumptions.

For fixed future coefficients and isotropic squared value error, a horizon query family induces a transported left metric

\[
G_{t:H}=\sum_{\tau=t}^H w_\tau
\Phi_{\tau:t+1}^\top q_\tau q_\tau^\top\Phi_{\tau:t+1}.     \tag{21}
\]

At decision time, the realized future `q_tau` and products are an oracle unless supplied by a declared prefix-lawful predictor/ambiguity set. A general language-loss Hessian acts on `vec(C)` and need not factor as `G tensor I`; (21) is a stated quadratic surrogate, not a full-network optimum.

## 7. Information, state, compute, and controls

An exact factor ledger appends columns for each new injection and propagates all current left factors. With accumulated rank `R`, state and read traffic are `O(R(d_k+d_v))`, propagation is `O(Rd_k)` per fixed-feature map, and query correction is `O(R(d_k+d_v))`. Exact merging can remove linear dependence; lossy recompression needs QR/small-core SVD and exposes (20). Dense materialization costs `O(Rd_kd_v)` arithmetic/writes but avoids recurring factor reads. These costs, selector state/calibration, `G` estimation, and additional overlay capacity must be matched.

Strong same-information controls are:

1. exact chronological Delta or exact ordered WY with no semantic edit;
2. the same `m_hat` scalar edit `((m_hat-s)/2)K` carried by the identical overlay engine;
3. a direct rank-r action predictor using the same `X`, selector, metric, and carry/recompression budget;
4. generic skinny-factor merge/recompression;
5. full materialization when memory traffic makes a factor overlay slower.

The R11 factor core supplies analytic bookkeeping, not additional semantic evidence or an unconditional total-cost advantage.

## 8. Predictions, falsifiers, and failure boundaries

Predictions/checks for a future lawful evaluation:

1. With identical frozen coefficients, a single rank-r overlay never exceeds rank r; direct state differencing must equal the lazy factors from (3).
2. With two independent block constructions from (14), exact accumulated rank is four; a rank-two implementation must incur the tail in (18).
3. Shared right residuals can keep many corrections rank one, falsifying any claim that correction count alone determines rank.
4. Setting `beta||k||^2=1` annihilates a key-aligned overlay direction.
5. Omitting `aMC` in a repeated corrected-state order decision produces a discrepancy exactly equal to that term under the fixed affine assumptions.

Boundaries:

- the exact closure concerns a shadow/base partition driven by the same realized coefficients; it is not the counterfactual uncorrected trajectory when the network recomputes future features from the chosen state;
- state-dependent keys, values, gates, selectors, metrics, or injection schedules require the full coupled difference/Jacobian and can map a rank-one perturbation to full matrix rank;
- a fixed current-query Gram is only its declared surrogate; it does not certify future semantic utility;
- no native task inspected supplies hidden harmful-versus-legitimate chronology, both counterfactual branches, lawful `G`, and internal overlay rank together;
- finite precision, factor thresholds, QR/recompression, memory bandwidth, and full-state reads remain unmeasured.

## 9. Disposition

Attempt 3 repairs a real overstatement and adds a sharp conditional capacity theorem. Passive pure-Delta propagation preserves low rank exactly; repeated independent semantic repairs, not residual participation itself, can force rank to grow by two per pair; and corrected-state repeated decisions must retain the `MC` term.

The method-level contribution still fails. Ordered affine Delta/WY and DeltaProduct cover the transport; incremental low-rank factor/core maintenance covers merge and recompression; the selector, prefix-lawful transported metric, matched-total-cost advantage, and native semantic measurement remain missing. The surviving result is a Delta-specific theorem/debug control, not a new updater.

- Mathematical status: conditional exact closure/capacity theorem, pending independent final-byte review.
- Contribution status: narrow Delta specialization with major ordered-recurrence and low-rank-maintenance collisions.
- Empirical status: unknown; no execution occurred.
- Candidate admission/delta: `0`.
- Disposition: **park R11 after attempt 3/3 exhausted**.

Reopen only if one package supplies lawful semantic selector information, a prefix-causal transported query object, a matched-total-cost advantage over the direct controls above, and a native mechanism-identifying record. Another factorization, rank threshold, or recompression rule is not a new scientific delta.
