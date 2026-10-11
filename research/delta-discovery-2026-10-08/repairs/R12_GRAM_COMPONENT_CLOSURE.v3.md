# R12 v3 — Gram-component closure for a declared Delta key family

## Status

Repair attempt 3/3. The mathematical result below is a conditional exact theorem and constructive certificate. It is **not** evidence of empirical benefit, semantic revision truth, originality of the general invariant-subspace idea, or scientific admission of a method.

## 1. Original problem and exact patch

Let the Delta memory be `S\in\mathbb R^{d_k\times d_v}`. A pure left Delta step with nonzero strength is

\[
S^+ = F_i S+\beta_i k_i v^T,\qquad
F_i=I-\beta_i k_i k_i^T,\qquad \beta_i\ne0.
\]

For protected queries `Q\in\mathbb R^{d_k\times r}`, v2 asked for a reduced syndrome `Y=U^T S` whose state is autonomous and still determines `Q^T S`. Its exact condition was joint invariance of `V=\operatorname{col}(U)` under all `F_i`.

**Patch.** Evaluate v2's already-defined least invariant fixed point under the narrower assumption that the admissible nonzero keys form a fixed, finite, externally declared family

\[
\mathcal K=\{k_1,\ldots,k_n\}\subset\mathbb R^{d_k},
\]

known before compression. Coefficients and chosen indices may vary causally, but no key outside this family may occur. Moreover, the selected index, `\beta_i`, and `v` must be externally visible or computable from the retained state/prefix without consulting discarded coordinates. Zero keys and operators that can occur only with `\beta=0` can be removed. Exactness is required for every ambient `S` and every allowed operator sequence, not merely one realized reachable trajectory. The task is to express that unique inclusion-minimal fixed point as an explicit graph component certificate and compute its dimension.

This is a deliberately narrower, checkable condition. It removes neither the same-information baseline nor the need to charge the declared dictionary.

## 2. Non-orthogonality graph

Set the protected seed subspace explicitly to

\[
V_0=\operatorname{col}(Q).
\]

Build the undirected graph `G=(\{1,\ldots,n\},E)` with

\[
\{i,j\}\in E \iff k_i^T k_j\ne0.
\]

A vertex is seeded when `P_{V_0}k_i\ne0`, equivalently when `k_i` is not orthogonal to `V_0`. Let `R` be the union of every connected component containing at least one seed, and define

\[
V_\star=V_0+\operatorname{span}\{k_i:i\in R\}.
\]

## 3. Theorem: exact least jointly invariant carrier

**Theorem.** Under the fixed finite-family assumptions above, `V_\star` is the unique inclusion-minimal linear subspace `V` satisfying

\[
V_0\subseteq V,\qquad F_i^T V\subseteq V\quad\text{for every }i.
\]

Because each `F_i` is symmetric, the transpose can be omitted.

### Proof

**Step 1: one-factor dichotomy.** For any subspace `V`, invariance under `F_i` is equivalent to invariance under `k_i k_i^T`, because `\beta_i\ne0` and

\[
k_i k_i^T x=\beta_i^{-1}(x-F_i x).
\]

If `V` is invariant and some `x\in V` has `k_i^Tx\ne0`, then

\[
k_i=(k_i^Tx)^{-1}k_i k_i^T x\in V.
\]

Otherwise `k_i^Tx=0` for all `x\in V`, hence `k_i\perp V`. Thus every invariant `V` obeys

\[
k_i\in V\quad\text{or}\quad k_i\perp V. \tag{1}
\]

Conversely, either alternative in (1) makes `k_i k_i^T V\subseteq V`, so (1) is also sufficient.

**Step 2: every feasible subspace contains all selected components.** Let `V` contain `V_0` and be invariant under every `F_i`. If `i` is a seed, `k_i\not\perp V_0\subseteq V`; by (1), `k_i\in V`. If `k_i\in V` and `k_i^Tk_j\ne0`, then `k_j\not\perp V`, so (1) forces `k_j\in V`. Induction along a path shows `k_j\in V` for every `j` in a seeded connected component. Therefore `V_\star\subseteq V`.

**Step 3: `V_\star` is feasible.** If `i\in R`, then `k_i\in V_\star`, so (1) gives invariance. If `i\notin R`, its component contains no seed, hence `k_i\perp V_0`; it also has zero inner product with every `k_j`, `j\in R`, because otherwise there would be an edge joining its component to `R`. Thus `k_i\perp V_\star`, and (1) again gives invariance. Therefore every `F_i` preserves `V_\star`.

Steps 2 and 3 prove feasibility and inclusion-minimality; an inclusion-minimal feasible subspace is consequently unique. `\square`

## 4. Closed recurrence and dimension certificate

Let `U\in\mathbb R^{d_k\times m_\star}` have orthonormal columns spanning `V_\star`, where

\[
m_\star=\dim V_\star=\operatorname{rank}[Q\;K_R].
\]

Define `Y=U^TS\in\mathbb R^{m_\star\times d_v}` and `h_i=U^Tk_i`. Since `V_\star` is invariant,

\[
Y^+=(I-\beta_i h_i h_i^T)Y+\beta_i h_i v^T. \tag{2}
\]

For `i\notin R`, `h_i=0`, so the excluded component cannot change the protected reduced state. Because `V_0\subseteq V_\star`, there is a fixed matrix `C=U^TQ` with

\[
Q^TS=C^TY.
\]

Equation (2) is therefore an exact autonomous recursion for all allowed key sequences. It also shows the real object: direct coordinates of `S` in the least jointly invariant carrier, not an additional independent checksum.

## 5. Old counterexamples rechecked

1. **v1 static-but-not-recursive failure.** A static `H` that omits a key overlapping its span is not closed. The graph construction adds that key and all non-orthogonally connected keys, so this particular algebraic failure is repaired for the declared family.
2. **v2 full-span collapse.** If every graph component touching `V_0` spans all of `\mathbb R^{d_k}`, then `m_\star=d_k`; the construction correctly collapses to full Delta and offers no compression.
3. **semantic ambiguity.** Two worlds can have the same keys and reduced state but disagree about whether a fact is obsolete. The theorem does not decide protection versus release and does not repair that identifiability failure.
4. **same-information equivalence.** Storing `Y=U^TS` is exactly storing the direct reduced memory coordinates. The v1 objection survives: no candidate novelty or advantage follows from calling them syndromes.

## 6. New failure boundary: the future bridge counterexample

The finite family must be declared before information is discarded. A prefix-only adaptive graph is not future-safe.

Take `d_k=2`, `V_0=\operatorname{span}(e_1)`. An early key `k_a=e_2` is initially orthogonal to `V_0`, so a prefix-only reducer may omit its write. Later a bridge key `k_b=e_1+e_2` arrives. Now `k_b` is seeded and is non-orthogonal to `k_a`, so the least closure for the enlarged family contains both coordinates. But the old `e_2` write has already been discarded. Two full histories with equal retained `e_1` state and different discarded `e_2` values are indistinguishable to the reducer, yet yield different protected outcomes after the bridge step.

Therefore no prefix-only expansion rule can reconstruct the missing state for all such histories without retaining full state, a sufficient ledger, or equivalent side information. This is an information-loss statement, not merely a poor graph algorithm.

## 7. Approximation is a separate claim

Replacing `k_i^Tk_j\ne0` by a numerical threshold is not an exact theorem. For a current subspace `V`, the one-step cross-boundary operator has norm

\[
\|P_V F_i P_{V^\perp}\|_2
=|\beta_i|\,\|P_Vk_i\|_2\,\|P_{V^\perp}k_i\|_2.
\]

Small pairwise Gram entries alone do not bound a long ordered product without horizon, strength, accumulation, and conditioning assumptions. Accordingly v3 makes no universal approximate-closure guarantee.

More explicitly, for an orthonormal `U`, put `a_t=U^Tk_t`, `b_t=(I-UU^T)k_t`, and let `e_t` be the difference between the true reduced state and a recursion that drops the orthogonal coordinates. Then

\[
e_t=(I-\beta_ta_ta_t^T)e_{t-1}-\beta_ta_tb_t^TS_{t-1}.
\]

Hence, if `\|S_{t-1}\|_F\le\rho_{t-1}`, `\delta_t=|\beta_t|\|a_t\|\|b_t\|`, and `\lambda_t=\|I-\beta_ta_ta_t^T\|_2`,

\[
\|e_T\|_F\le
\Big(\prod_{u=1}^T\lambda_u\Big)\|e_0\|_F+
\sum_{t=1}^T\Big(\prod_{u=t+1}^T\lambda_u\Big)\delta_t\rho_{t-1}.
\]

Even uniformly small *pairwise* key overlaps need not make `\delta_t` small. For `V=\operatorname{span}(e_1,\ldots,e_r)` and
`k=(2r)^{-1/2}\sum_{j=1}^r e_j+2^{-1/2}e_{r+1}`, each overlap with the displayed generators tends to zero as `r` grows, but `\|P_Vk\|\|P_{V^\perp}k\|=1/2`, its maximum for a unit key. A useful threshold theorem therefore needs basis-level or Gram-conditioning control, not edge thresholding alone.

## 8. Predictions and falsifiers

- Exact prediction: a declared family has a proper autonomous protected carrier iff `\operatorname{rank}[Q\;K_R]<d_k`.
- Structural prediction: adding a single bridge key can merge components and discontinuously increase `m_\star`.
- No-benefit prediction: when the seeded components span the full key space, any exact method implementing this carrier has full-state dimension.
- Falsifier: an allowed key outside the declared family, a nonzero numerical inner product treated as zero, or a non-scalar left operator not preserving `V_\star` invalidates exact closure.
- Selector boundary: if a key/gate/value is chosen using discarded coordinates, two full states with the same `Y` can choose different operators, so `Y` is not autonomous unless that selector also factors through `Y` (or is supplied externally).
- Numerical boundary: exact graph edges are discontinuous. With `k_1=e_1` and `k_2=\varepsilon e_1+e_2`, every nonzero `\varepsilon` connects the vertices although `\varepsilon=0` does not.
- Empirical status: all performance, robustness and numerical claims remain unknown.

## 9. Information, state and computation cost

- Required side information: the complete admissible key dictionary (or an externally certified equivalent family), `Q`, the chosen numerical zero/precision convention, and the basis `U`. Storing an unshared dense dictionary costs `nd_k` numbers.
- Offline naive cost: seed cross-products cost `O(nd_kr_0)` for protected rank `r_0`; all pairwise Gram products cost `O(n^2d_k)` arithmetic and `O(n^2)` dense storage before sparsity. A sparse representation costs `O(n+|E|)` topology plus edge weights; component discovery costs `O(n+|E|)`. Rank-revealing QR/SVD on `[Q\;K_R]` and basis construction must also be charged.
- Runtime state: `m_\star d_v` numbers for `Y`, dense basis cost `d_km_\star`, decoder cost `m_\star r`, and optional cached coordinates `h_i` cost `nm_\star`.
- Runtime update: (2) is `O(m_\star d_v)` per write only after the key identity and `h_i` are supplied or cached. Otherwise projecting `k_i` adds `O(d_km_\star)`. Total cost includes key-ID lookup/certification, dictionary and basis traffic, precision, and amortization horizon.
- A scalar identity term preserves every subspace, but a factor `\alpha_i I-\gamma_i k_i k_i^T` forces the key dichotomy only when `\gamma_i\ne0`; a zero operator imposes no key condition. A general left decay/preconditioner `D_i` requires joint invariance under the complete `F_i^T` and can enlarge the closure; the graph theorem alone does not cover it.

## 10. Same-information strong controls

1. Full Delta/WY recurrence with the same key sequence.
2. Direct reduced memory `Y=U^TS` using the identical `U`; this is algebraically identical to the claimed syndrome state and is the decisive simplicity baseline.
3. Fixed orthogonal blocks/slots or sparse routing supplied with the same declared dictionary and total state budget.
4. Numerical rank/projection truncation with leakage measured rather than claimed exact.

The v3 contribution is only the finite-family component certificate and its sharp online limitation. It is not a separate architecture unless a future construction exhibits a non-equivalent state/update or a matched-cost advantage.

## 11. Measurement feasibility

Existing endpoint tasks such as RULER or BABILong can compare long-range answers, while LongMemEval's update/temporal questions are the closest endpoint proxy. But their native data and scorers do not expose the model's internal keys, the declared admissible family, Gram components, `m_\star`, paired equal-`Y` full states, or the intervention needed to attribute success to exact closure. bAbI's usual per-question reset cannot measure persistent cross-question recursion, and LAMBADA measures final-word prediction rather than this mechanism. A paid model judge required by a pinned evaluation is not silently replaced in this no-new-paid-service stage.

Using held-out or future test keys to build the graph would leak future information. The family must be an ex-ante structural object, or the graph can be used only as a development/post-hoc analysis. Observed keys certify only the observed subfamily unless membership of future keys is independently guaranteed.

The theorem is directly checkable on an externally supplied linear key family by native linear-algebra identities, but that is a mathematical fixture, not an existing native language benchmark. A mechanism-identifying public record remains missing. No benchmark, label, metric or result is invented here.

## 12. Nearest-work and decision

The general language is a specialization of common invariant/reducing-subspace and exact-abstraction/bisimulation ideas. Rank-one Delta structure turns joint invariance into the dichotomy (1), and a finite family turns propagation into graph connectivity. The source audit must not claim priority for the general theorem or a first method.

**Decision:** conditionally accept the exact finite-family theorem as a useful Delta-specific control/certificate; park R12 after attempt 3/3. Candidate delta remains zero because the executable reduced state is identical to the direct-coordinate baseline, the declared-family cost is material, native mechanism measurement is absent, and unseen bridge keys defeat online expansion.

