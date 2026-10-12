# Step 2 residual object: irreversible query-shift refinement tax

Date: 2026-10-12  
Status: `theorem/control under source and independent review`; `candidate_delta=0`; empirical effect unknown; no model code, training, inference, scoring, or experiment executed.  
Lineage: new temporal coding parent after `STEP2_QUERY_WEIGHTED_RATE_DISTORTION_2026-10-12.md`. It is not a fourth repair of R17--R19.

## 1. Important problem and exact patch

The previous query-weighted rate--distortion object asks how accurately a declared Delta state can be represented at a fixed bit budget for one declared query law. It does not answer the next online question:

> If the query law changes after a prefix-optimal compressed description has already been made durable, can appended bits reuse that description as efficiently as a fresh code designed for the new query law?

The patch changes the **action and timing**, not merely the loss name. Stage-1 bits are immutable; stage 2 may append bits but may not rewrite them. A matched fresh-code baseline may spend the same total bits after the new query law is known. This is a successive-refinement problem with stage-dependent query distortion.

The retained conclusion is deliberately narrow. A sharp Gaussian witness proves an irreversible rate tax under orthogonal query shift. A general positive result requires the usual Markov-compatible test channels. Neither result constructs a semantic retain-versus-revise oracle or a new Delta updater.

## 2. Formal object

Let `x=vec(S)` be the declared memory state. For query law `pi_j`, let

\[
W_j=I_{d_v}\otimes G_j,\qquad G_j=\mathbb E_{q\sim\pi_j}[qq^T],
\]

and define `d_j(x,xhat)=(x-xhat)^T W_j(x-xhat)`. A two-stage block code observes `X^n` and emits

\[
M_1=f_1(X^n),\quad |\mathcal M_1|\le 2^{nR_1},
\qquad
M_2=f_2(X^n),\quad |\mathcal M_2|\le 2^{n\Delta}.
\]

Decoder 1 uses only `M_1`; decoder 2 uses `(M_1,M_2)`. The first message is not replaceable after the second metric is selected or revealed. Define the total-rate successive-refinement boundary

\[
R_{\rm sr}(D_1,D_2;d_1,d_2)
=\inf I(X;\widehat X_1,\widehat X_2)
\]

over joint test channels satisfying

\[
\mathbb E d_j(X,\widehat X_j)\le D_j,
\qquad I(X;\widehat X_1)\le R_{d_1}(D_1).
\]

The **query-shift refinement tax** is

\[
\mathcal T=R_{\rm sr}(D_1,D_2;d_1,d_2)-R_{d_2}(D_2)\ge0. \tag{1}
\]

Equation (1) is an established successive-refinement rate-loss object specialized to Delta query metrics. It is not claimed as a new information-theoretic region.

The classical boundary permits `d_1` and `d_2` to differ while both are fixed for joint code design. The stricter online variant additionally requires `M_1` to be measurable before `W_2` is revealed; a family/minimax or Bayesian criterion must then be declared, and the description of `W_2` must be public side information or charged. The orthogonal theorem below does not need that stronger uncertainty assumption: its no-slack tax holds even when the future orthogonal metric is known at stage 1. Unknown future metrics can only further restrict the first encoder, not weaken this witness.

## 3. Sharp orthogonal-query theorem

Consider i.i.d. pairs

\[
(A_i,B_i)\sim\mathcal N(0,\sigma^2 I_2),\qquad i=1,\ldots,n,
\]

with stage distortions

\[
d_1((a,b),\widehat a)=(a-\widehat a)^2,
\qquad
d_2((a,b),\widehat b)=(b-\widehat b)^2. \tag{2}
\]

These are two orthogonal rank-one query metrics on the same state. Let the stage-1 decoder attain distortion `D_1`, and define its unused information budget

\[
\epsilon_n
=R_1-\frac12\log_2\frac{\sigma^2}{D_1}\ge0, \qquad 0<D_1\le\sigma^2. \tag{3}
\]

for any feasible finite-block code (and with the usual asymptotic interpretation on the rate--distortion boundary). Then every immutable-prefix two-stage code with an additional `Delta` bits per source pair satisfies the exact converse

\[
D_2\ge \sigma^2 2^{-2(\Delta+\epsilon_n)}. \tag{4}
\]

In particular, if stage 1 is asymptotically point-to-point optimal,

\[
D_1=\sigma^2 2^{-2R_1}+o(1),
\]

then `epsilon_n=o(1)` and

\[
(D_2^{\rm progressive})^*= \sigma^2 2^{-2\Delta},
\qquad
(D_2^{\rm fresh})^*=\sigma^2 2^{-2(R_1+\Delta)}. \tag{5}
\]

where the stars denote Shannon infima/asymptotically achievable boundaries. Thus the optimal progressive distortion is worse by the sharp multiplicative factor `2^(2R_1)`, or equivalently the total-rate tax is `R_1` bits per source pair.

### Proof

Write rates in bits. Since `M_1` has at most `nR_1` bits,

\[
\begin{aligned}
nR_1
&\ge H(M_1)\\
&\ge I(A^n,B^n;M_1)\\
&=I(A^n;M_1)+I(B^n;M_1\mid A^n). \tag{6}
\end{aligned}
\]

The scalar Gaussian rate--distortion converse applied to the stage-1 reconstruction gives

\[
I(A^n;M_1)\ge \frac n2\log_2\frac{\sigma^2}{D_1}. \tag{7}
\]

Combining (3), (6), and (7),

\[
I(B^n;M_1\mid A^n)\le n\epsilon_n. \tag{8}
\]

Because `A^n` and `B^n` are independent,

\[
I(B^n;M_1)\le I(B^n;M_1\mid A^n)\le n\epsilon_n. \tag{9}
\]

The appended message contributes at most `nDelta` further bits, so

\[
I(B^n;M_1,M_2)
\le I(B^n;M_1)+H(M_2)
\le n(\epsilon_n+\Delta). \tag{10}
\]

Applying the scalar Gaussian converse to the stage-2 reconstruction yields (4). A fresh total-rate code can ignore `A^n` and attain the Gaussian distortion-rate function for `B^n`, which gives (5). Equality is approached by an optimal stage-1 Gaussian code for `A^n` and an independent optimal appended code for `B^n`. More generally, the stage-1 slack `epsilon_n` can be assigned to a successively refinable Gaussian description of `B^n`, so the displayed converse is sharp on the Shannon boundary. This proves sharpness.

At exact finite-block RDF equality, `epsilon_n=0`, the same chain forces both

\[
I(B^n;M_1\mid A^n)=0,
\qquad
I(B^n;M_1)=0. \tag{11}
\]

For a sequence of codes approaching the RDF boundary, the corresponding statement is per-symbol leakage tending to zero. It is not an exact finite-block zero-leakage claim.

## 4. What the old counterexamples now say

The earlier fixed-metric capacity theorem remains correct. Its failure was a target mismatch: it did not price irreversible bits after task rotation. The patch does not delete any old counterexample.

- If `R_1=0`, the tax vanishes.
- If `D_1>=sigma^2`, the first task lies in its zero-rate region and the logarithm in (3) must be replaced by its positive part; the stated positive-rate witness is then inapplicable. If `D_1=0`, finite rate cannot attain the target.
- If the second query metric equals the first and only requests a finer distortion, the Gaussian squared-error source is successively refinable; the orthogonal witness does not apply.
- If the first message has rate or distortion slack, (4) shows exactly how much information can be hedged toward a future orthogonal query.
- If old bits may be replaced rather than only appended, the fresh-code baseline is implementable and the tax disappears as a coding constraint, though re-encoding compute and traffic must be charged.
- Knowing the future orthogonal metric before stage 1 does not remove the no-slack result: a stage-1 message on the point-to-point boundary has no remaining rate for the independent coordinate. It permits only an explicit stage-1 distortion/rate tradeoff.

## 5. General positive condition and boundary

For memoryless sources and single-letter stage distortions under the standard rate--distortion attainment and regularity assumptions, zero tax at both point-to-point boundaries requires both the rate ordering

\[
R_{d_1}(D_1)\le R_{d_2}(D_2)
\]

and compatible optimal test channels. In this attained two-stage setting, a sufficient-and-necessary asymptotic condition is the existence of reconstructions with

\[
X\longrightarrow \widehat X_2\longrightarrow \widehat X_1, \tag{12}
\]

while each marginal attains its own rate--distortion optimum. If the infima are not attained, this statement must instead be formulated using closures or approximating sequences. Under a fixed Gaussian quadratic distortion the attained condition holds. Under changing query metrics it must be checked; a shared source distribution alone is insufficient.

For Delta memory, a checkable sufficient special case is a common eigenbasis in which the stage-1 optimal Gaussian test channel is a stochastic degradation of the stage-2 optimum. Mere commutation of `W_1` and `W_2`, nesting of query subspaces, or monotonicity of trace is not by itself enough: the active water-filling allocations must also be compatible.

On the asymptotic Gaussian Shannon boundary, a two-coordinate specialization makes this allocation condition explicit. Suppose stage 1 uses an RDF-achieving Gaussian test channel and spends

\[
R_1=\frac12\log_2\frac{\sigma_A^2}{D_1}
\]

on coordinate `A`, while the final metric has positive coordinate weights `a,b`. The RDF-achieving stage-1 channel leaves a Gaussian posterior innovation of variance `D_1`; progressive refinement therefore sees conditional weighted variances `aD_1` and `b sigma_B^2`, while a fresh code sees `a sigma_A^2` and `b sigma_B^2`. Both use ordinary reverse water-filling. On this Shannon boundary, they attain the same final distortion exactly when some fresh optimum allocates at least `R_1` bits to `A`, so the old layer can be embedded in the fresh optimum. If every fresh optimum allocates less than `R_1` to `A`, the prefix has overcommitted rate and the gap is strict. The pure orthogonal shift is the extremal case: the fresh allocation to `A` is zero. This is not asserted for an arbitrary finite-block code that merely reports the same numerical rate and distortion.

## 6. Delta interpretation and computable prediction

Choose two orthogonal key directions and one value coordinate inside `vec(S)`. Then (2) is induced by two rank-one query Gramians. The theorem predicts:

1. an append-only compressed Delta memory can be optimal for the current query family yet maximally unhelpful after orthogonal query rotation;
2. the gap from fresh re-encoding grows with the rate already committed to now-irrelevant query directions;
3. near-compatible query paths should show a smaller tax, while high active-subspace turnover should increase it;
4. reserving universal bits can reduce future tax only by paying visible current-stage distortion or extra rate.

The natural diagnostic is the excess total rate

\[
\widehat{\mathcal T}
=R_{\rm progressive}(D_1,D_2)-R_{\rm fresh}(D_2), \tag{13}
\]

at identical source blocks, bit accounting, query metrics and decoder class. Principal angles between active query-weighted covariance eigenspaces are a conditioning variable, not a substitute for measuring (12).

## 7. Information, state, and compute ledger

The theorem is asymptotic and information-theoretic. A consuming construction must separately charge:

- first and appended payload bits;
- framing, codebook, query-Gram/eigenbasis and stage metadata;
- encoder search, re-encoding, decoder and state-migration compute;
- precision, overflow/failure probability and finite-block redundancy;
- storage or traffic for the original state if fresh re-encoding needs it;
- whether stage 2 can revisit the original source block at all; if it cannot, the fresh comparator must be restricted to the same retained state or the archive/read cost must be charged;
- any hedge capacity reserved for unknown future queries.

The strongest same-information controls are:

1. full fresh re-encoding after query shift with identical total bits;
2. a standard successive-refinement code using the exact stage distortions;
3. a single universal/minimax query metric fixed at stage 1;
4. independent per-query-subspace coders with the same aggregate bits;
5. the direct quotient/ledger controls of R18--R19;
6. uncompressed Delta state at matched total memory/traffic where feasible.

No float-count saving or low-rank label establishes a matched-bit or matched-total-cost benefit.

## 8. Closest-work and contribution status

Classical successive refinement already asks whether an optimal first description can remain part of an optimal later description; its Markov compatibility theorem, full rate region with two possibly different distortion measures, abstract-source extensions and vector Gaussian individual-distortion analysis directly cover the main object. Rate--distortion formulations of database search already combine a scalable search layer, query side information and a reconstruction enhancement layer under different layer distortions. Task-based and indirect rate--distortion cover query-weighted fidelity. The orthogonal theorem above is therefore a transparent Delta-coordinate witness and debugging boundary, not a firstness claim.

The residual scientific value is:

- a sharp no-slack inequality (4) tying current point-to-point optimality to future query flexibility;
- an explicit Delta query-Gram witness for irreversible compression under task rotation;
- a matched-rate diagnostic and clear reopen condition.

This is insufficient for a new method card. Reopening candidate construction requires a lawful prefix-causal code or state mechanism that obtains a strict matched-bit/metadata/compute advantage over standard two-distortion successive refinement, scalable query-side-information coding, fresh re-encoding, universal/runtime-distortion coding and direct ledgers on a native object that actually changes query tasks. The residual online/compound case must explicitly distinguish a `W_2` unknown at stage 1 from the classical jointly designed pair `(d_1,d_2)`.

## 9. Measurement feasibility and failure boundary

Ordinary language-memory endpoints report answer accuracy or loss, not an immutable first-stage bitstream, appended payload, fresh-code comparator, query metric, code metadata and re-encoding cost. They therefore cannot identify (12) without an already public protocol exposing those fields. Synthetic orthogonal Gaussian coordinates would demonstrate the theorem but would be a constructed diagnostic, not an authorized native benchmark result.

Failure boundaries:

- non-Gaussian or finite-block sources require their own rate region and redundancy terms;
- zero eigenvalues make distortion a seminorm and require an explicit quotient;
- state evolution between stages requires causal/nonanticipative coding, not the frozen-source proof;
- shared randomness must be conditioned on and any decoder side information must be charged; otherwise the mutual-information ledger changes;
- correlation between old and new coordinates can make part of the new query predictable from the old description; the hard loss applies to the independent innovation, not automatically to the whole new coordinate;
- data-dependent routing can change the metric after seeing encoded state and must be included in the filtration;
- semantic validity remains unidentifiable without external evidence;
- a practical learned codec may fail far above the Shannon boundary, so the theorem predicts no empirical gain by itself.

Current disposition: retain as a theorem/debug control pending exact-byte independent review and source closure. Candidate, scientific-admission and selection increments remain zero; empirical effect is unknown.
