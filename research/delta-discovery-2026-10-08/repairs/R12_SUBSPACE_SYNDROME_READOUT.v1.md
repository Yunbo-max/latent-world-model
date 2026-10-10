# R12 — Subspace-syndrome protected-readout recovery (attempt 1)

## Status and lineage

- Parent: `rejected/CHECKSUM_REVISION_SKETCH.md` (blob `20bc78d86035a9fb75874edcba0c27aa5dd0c3e5`).
- Parent failure retained: a causal checksum cannot create missing revision/coexistence identity or latest-truth evidence. Bloom/SimHash/Count-Min variants remain approximate dictionaries or frequency summaries, and the historical `A→B→A` counterexample is unchanged.
- Failure type repaired: **target/construction mismatch**. The parent asked a sketch to infer semantic validity. R12 asks the narrower observable question that a linear syndrome can answer: when does a checksum determine the effect of an already-observed numerical Delta edit on a declared protected-query family?
- Patch: replace semantic classification by exact functional recovery on an explicit admissible edit subspace, derive the necessary-and-sufficient nullspace condition, its noise/misspecification penalty, and the same-budget direct-statistic control.
- Outcome: useful conditional theorem/control, but generic linear inverse/sufficient-statistic mathematics. It does not identify whether an edit is beneficial, and it has no established advantage over directly storing protected outputs or subspace coordinates. Park after attempt 1; no active candidate.

## 1. Formal object

Let the key-by-value memory be `S∈R^{d_k×d_v}` and let `Δ` denote a numerical edit whose later protected-query effect is

\[
L_Q(\Delta)=Q^\top\Delta\in\mathbb R^{p\times d_v},
\qquad Q\in\mathbb R^{d_k\times p}.
\]

A fixed causal syndrome uses `H∈R^{d_k×m}` and stores

\[
Y=H^\top\Delta+N\in\mathbb R^{m\times d_v}, \tag{1}
\]

where `N` is measurement/quantization noise. No future answer, validity label, revision flag or identity oracle enters (1). Let the declared admissible left subspace be `U=col(B)` with full-column-rank `B∈R^{d_k×r}`; exact-model edits have `Δ=BA` for arbitrary `A∈R^{r×d_v}`.

The scientific question is not whether `Y` says which fact is true. It is whether one can compute `Q^TΔ` uniformly over the declared numerical edit class.

## 2. Exact functional-recovery theorem

Define

\[
M=H^\top B\in\mathbb R^{m\times r},\qquad C=Q^\top B\in\mathbb R^{p\times r}. \tag{2}
\]

There exists a decoder `R∈R^{p×m}` satisfying

\[
R H^\top\Delta=Q^\top\Delta\quad\text{for every }\Delta=BA \tag{3}
\]

if and only if

\[
\ker M\subseteq\ker C. \tag{4}
\]

Equivalently, `row(C)⊆row(M)`, or there exists `R` with `RM=C`. Necessity follows because two coefficient matrices differing by any column in `ker M` have the same syndrome and must have the same protected output. Sufficiency follows from the factorization

\[
R_0=C M^\dagger, \tag{5}
\]

because (4) implies `C=C M^†M`, hence `R_0M=C`.

Full recovery of `Δ` is the special case `C=I_r` in coefficient coordinates: it requires `rank(M)=r`, so necessarily `m≥r`. Functional recovery can be smaller: necessarily `rank(M)≥rank(C)`. If `H` may be freely designed with knowledge of `B,C`, a sketch whose `M` row space equals `row(C)` achieves `m=rank(C)` (including `m=0` when `C=0`). Such a designed `H` is only a reparameterized direct sufficient statistic, not an oblivious checksum. Thus the correct dimension is the protected functional rank, not automatically the ambient memory dimension and not automatically the semantic number of facts.

## 3. Indistinguishability and sharp deterministic lower bound

If (4) fails, choose `a∈ker M` with `Ca≠0` and any unit value direction `w`. The two legal edits

\[
\Delta_+=Ba w^\top,\qquad \Delta_-=-Ba w^\top \tag{6}
\]

produce the identical zero syndrome but protected outputs `±Ca w^T`. For every decoder `D(Y)`, the triangle inequality gives

\[
\max_{s\in\{+,-\}}
\|D(0)-Q^\top\Delta_s\|_F
\ge \|Ca\|_2\|w\|_2. \tag{7}
\]

Under the coordinate-invariant edit budget `||Ba||≤ρ`, the exact zero-syndrome hidden-class minimax radius is

\[
\sup_{a\in\ker M:\,\|Ba\|_2\le\rho}\|Ca\|_2. \tag{8}
\]

It is also a lower bound for any larger admissible problem containing these hidden edits. If the columns of `B` are orthonormal, (8) reduces to `ρ||C P_{ker M}||_2`. This is a numerical observability bound, not the parent's Bayes error for revision identity. Under worst-case expected norm, randomizing the decoder cannot improve the symmetric-pair lower bound without extra information.

## 4. Noise, conditioning, and model leakage

When (4) holds, (5) yields

\[
\widehat L=R_0Y,
\qquad
\|\widehat L-Q^\top\Delta\|_F\le \|R_0\|_2\|N\|_F \tag{9}
\]

for exact-model edits. The action of every exact decoder is fixed on `range(M)`; choosing zero action on `range(M)^⊥` makes (5) a minimum (not necessarily unique) operator-norm extension. Small retained singular values of `M` can amplify noise through `CM^†`; they do not matter when `C` annihilates the corresponding right-singular directions.

For misspecified edits `Δ=BA+E`, applying (5) to (1) gives the exact error identity

\[
\widehat L-Q^\top\Delta
=(R_0H^\top-Q^\top)E+R_0N, \tag{10}
\]

and therefore

\[
\|\widehat L-Q^\top\Delta\|_F
\le (\|R_0\|_2\|H\|_2+\|Q\|_2)\|E\|_F
+\|R_0\|_2\|N\|_F. \tag{11}
\]

An oblivious near-isometry for every vector in an unknown `r`-dimensional subspace is a stronger, different probabilistic contract, with its own ambient-dimension-capped lower bounds; it is not asymptotically larger than (4) in every regime. R12 makes no random-sketch success claim.

## 5. Delta specialization

For one frozen-feature Delta write

\[
\Delta=\beta k e^\top,\qquad e=v-S^\top k, \tag{12}
\]

the left subspace is `span{k}`. If `k` is causally observed, `H^Tk≠0`, and `N=0`, then one syndrome direction suffices to recover the numerical write:

\[
\Delta=k\frac{(H^\top k)^\top Y}{\|H^\top k\|_2^2}. \tag{13}
\]

This is not a new memory algorithm: the ordinary updater already has `k,e,β` at the write time, so storing the write or its protected outputs is at least as direct. For an accumulated edit `Δ=BA`, R12 helps only if a stable low-dimensional `B` is causally known and (4) remains well-conditioned. State-dependent future features, transport, and changing protected queries are not covered by a static syndrome unless their induced functionals continue to factor through `H^TB`; otherwise one must update the basis/decoder or retain more state.

## 6. Old counterexamples and semantic boundary

The old revision/coexistence no-go survives verbatim. Two semantic worlds can share the same numerical `Δ`, `Y`, `Q`, and all causal observables while differing in which value is currently true. Equations (3)–(13) reconstruct an edit effect; they do not label it beneficial, current, or obsolete. In particular, `A→B→A` remains indistinguishable from historical membership alone. Stable entity/version evidence, external correction markers, or future outcomes remain extra information.

Likewise, exact preservation of declared linear readouts does not imply preservation of a nonlinear downstream model or of future Delta recursion. Those require the full state Jacobian/transport conditions already retained elsewhere in the packet.

## 7. Information, state, and compute cost

- Syndrome state: `m d_v` scalars; fixed dense formation/update costs `O(m d_k d_v)` naively but rank-one Delta writes update it as `H^TΔ=β(H^Tk)e^T` in `O(md_k+md_v)`. A dense explicit `H` itself costs `m d_k` scalars unless it is fixed/implicit.
- Decoder: storing dense `R_0` costs `p m`; applying it costs `O(pmd_v)`.
- Admissible basis: a dense `B` costs `r d_k` unless supplied by the model; tracking a changing basis adds an unanalysed cost.
- Direct protected-statistic control: if `q=rank(C)` and `C=FG` is a rank factorization with `G∈R^{q×r}`, store `GA` using exactly `q d_v` scalars and reconstruct `CA=F(GA)`. This matches the minimum possible syndrome rank; storing `Q^TΔ` directly is the unreduced `p d_v` version. Designing `H` from `B,Q` merely changes coordinates of this direct statistic.
- Direct subspace-coordinate control: store `A` (or `B^†Δ`) using `r d_v` scalars. When `B` is known, it avoids an arbitrary `H` and can be better conditioned.

For a family `C_j=Q_j^TB`, let `W=span_j row(C_j)` and `s=dim(W)`. Choose `J∈R^{s×r}` with `row(J)=W`; then every `C_j=F_jJ`. Every exact common syndrome must have `W⊆row(M)` and hence `rank(M)≥s`, while directly storing `JA` uses `s d_v` scalars and reconstructs every `C_jA=F_j(JA)`. Therefore even a shared sketch for many known later functionals has no scalar-state advantage. Only an externally imposed/implicit `H`, an unknown-at-write query family covered by a separately justified subspace, or a demonstrated compute/layout benefit can leave a systems role.

These are scalar counts, not bit/information costs unless precision is matched. Storage/calibration of `B,Q,R_0`, changing-basis tracking, decoder quantization, and perturbations in `B,H,Q` are outside (10)–(11) and must be charged separately.

## 8. Predictions, falsifiers, and measurement boundary

Conditional predictions:

1. Exact protected-output reconstruction occurs exactly when (4) holds; violating it produces the paired failure (6)–(8).
2. With exact subspace membership, worst-case noise sensitivity follows `||CM^†||`; changing `H` while holding dimensions fixed can alter error through conditioning even when rank is unchanged.
3. With leakage `E`, error grows according to the observable operator in (10), not merely `||E||` or sketch width.

Falsifiers/stop conditions:

- A decoder achieving uniform exact recovery while (4) fails would refute the theorem's algebraic claim.
- If the chosen native task cannot expose `Q`, admissible `B`, or retained protected outputs, it cannot test the mechanism. LongMemEval/bAbI/LAMBADA endpoint scores do not supply these internal labels.
- Any advantage explained by more stored scalars, a privileged basis, future queries, semantic labels, or a hardware checksum unavailable to controls is not evidence for the proposed mechanism.

No project code, test, model, benchmark, scorer, training, inference, download, GPU job or synthetic evaluation was executed or created.

## 9. Decision

R12 salvages a precise theorem: a linear checksum is a sufficient statistic for declared protected edit effects iff the target functional annihilates every edit direction hidden by the sketch; otherwise a sharp symmetric indistinguishability pair remains. This is mathematically useful for deciding when a checksum is legitimate and when it is information-losing.

The mechanism is generic linear inverse/sufficient-statistic geometry. Direct protected-functional coordinates or subspace coordinates are same-width simple controls, while semantic revision remains unidentified. Park R12 after attempt 1 as a conditional theory/control. Reopen only if a real Delta workload supplies a stable causal `B`, an externally imposed or implicit syndrome interface with a compute/layout advantage over direct coordinates under equal precision, and a native measurement path for the claimed benefit.
