# Step 2 residual object: compound query hedge before demand reveal

Date: 2026-10-12  
Status: `classical theorem/control`; `candidate_delta=0`; empirical effect unknown; no model code, training, inference, scoring, benchmark construction, or experiment executed.  
Lineage: new parent object opened by the unresolved online clause in `STEP2_QUERY_SHIFT_SUCCESSIVE_REFINEMENT_2026-10-12.md`; it is not a fourth repair of R01--R20.

## 1. Problem, failure type, and patch

The preceding orthogonal query-shift theorem allowed the two distortion measures to be fixed when the layered code was designed. Its remaining question was genuinely temporal: what if the future query is absent from the first-stage filtration and is revealed only before an append-only second message?

The patch is to formalize that object rather than reuse a jointly designed two-distortion code. The first message must hedge across the declared query family. This changes the information pattern, but it does **not** create a new mechanism: after source audit, the object is the classical single-user lossy caching/prefetching problem. The useful output is therefore an exact Gaussian specialization and a Delta-facing cost boundary.

## 2. Formal object

Let

\[
X=(X_1,\ldots,X_m),\qquad X_j\stackrel{\mathrm{ind}}\sim\mathcal N(0,\sigma^2),
\]

and take `n` i.i.d. copies. Before the query index exists in the encoder's filtration, the stage-1 encoder emits

\[
M_0=f_0(X_1^n,\ldots,X_m^n),\qquad |\mathcal M_0|\le 2^{nR}.
\]

For the Bayesian criterion, `J` is independent of the source block and any code randomness with `P[J=j]=p_j`; for the minimax criterion it is a fixed, external, non-source-dependent index. After `J in {1,...,m}` is revealed to both second-stage encoder and decoder, the encoder emits

\[
M_J=f_J(X_1^n,\ldots,X_m^n,J),\qquad |\mathcal M_J|\le 2^{n\Delta},
\]

and the decoder produces `Xhat_J^n=g_J(M_0,M_J,J)`. The first message is immutable. The source block is available to the second encoder; a retained-state-only variant is strictly weaker and must be analyzed separately. Query identity is treated as public side information; otherwise its description cost must be charged.

For a Delta state, `X_j` represents an orthogonal query-visible coordinate of `vec(S)`. General correlated coordinates reduce to the rate--distortion--cache region and do not inherit the independent-coordinate closed form below.

## 3. Exact independent-Gaussian converse

Define the per-coordinate information placed in the first message

\[
a_j^{(n)}=\frac1n I(X_j^n;M_0).
\]

Independence implies

\[
\sum_{j=1}^m I(X_j^n;M_0)
\le I(X_1^n,\ldots,X_m^n;M_0)
\le H(M_0)\le nR. \tag{1}
\]

Indeed, conditional subadditivity gives
`H(X_1^n,...,X_m^n|M_0) <= sum_j H(X_j^n|M_0)`, while the unconditional entropy is additive. After demand `j`,

\[
I(X_j^n;M_0,M_j)
\le I(X_j^n;M_0)+H(M_j)
\le n(a_j^{(n)}+\Delta). \tag{2}
\]

The scalar Gaussian rate--distortion converse therefore gives

\[
D_j^{(n)}
=\frac1n\mathbb E\lVert X_j^n-\widehat X_j^n\rVert_2^2
\ge \sigma^2 2^{-2(a_j^{(n)}+\Delta)}. \tag{3}
\]

Equations (1)--(3) are valid for arbitrary, possibly joint and nonlinear first-stage codes. Shared randomness does not improve the bound after conditioning on it and must be available symmetrically.

## 4. Minimax theorem and achievability

For worst-case demand, (1) ensures `min_j a_j^(n) <= R/m`; hence

\[
\max_j D_j^{(n)}\ge \sigma^2 2^{-2(\Delta+R/m)}. \tag{4}
\]

The Shannon boundary is achievable: independently describe every coordinate at first-stage rate `R/m`, then, after `J` is revealed, append `Delta` Gaussian successive-refinement bits for `X_J`. Consequently

\[
D_{\max}^*(R,\Delta)
=\sigma^2 2^{-2(\Delta+R/m)}. \tag{5}
\]

A query-aware fresh encoder with the same final payload `R+Delta` can spend every bit on the requested coordinate:

\[
D_{\rm fresh}^*(R,\Delta)
=\sigma^2 2^{-2(R+\Delta)}. \tag{6}
\]

Thus an immutable query-agnostic prefix pays the exact worst-case rate tax

\[
\mathcal T_{\rm minimax}=R\left(1-\frac1m\right), \tag{7}
\]

or distortion factor `2^(2R(1-1/m))`, relative to fresh query-aware re-encoding. This is the inverted independent-source rate--distortion--cache formula, not a new coding theorem.

## 5. Bayesian query prior

If `P[J=j]=p_j` is declared before stage 1 and expected distortion is the objective, weighting (3) and minimizing under (1) gives the global causal optimum

\[
\min_{r_j\ge0,\ \sum_jr_j\le R}
\sigma^2 2^{-2\Delta}\sum_j p_j2^{-2r_j}. \tag{8}
\]

KKT conditions give reverse water-filling over query probabilities:

\[
r_j^*=\frac12\left[\log_2\left(\frac{p_j}{c}\right)\right]_+,
\qquad
\sum_j\frac12\left[\log_2\left(\frac{p_j}{c}\right)\right]_+=R, \tag{9}
\]

where `c` is chosen by the displayed rate equation for `R>0`; when `R=0`, any `c>=max_j p_j` works. The bracket means zero allocation when `p_j<=c`. The optimum is

\[
D_{\rm Bayes}^*(R,\Delta)
=\sigma^2 2^{-2\Delta}\sum_j\min\{p_j,c\}. \tag{10}
\]

For uniform demand, (9) reduces to `r_j=R/m` and (10) equals (5). A zero-probability coordinate receives no stage-1 rate. The Bayesian allocation is also an established lossy-caching object; it is retained as a strong baseline rather than counted as a candidate.

## 6. Counterexamples, edge cases, and scope

- `m=1` or `R=0`: the hedge tax in (7) vanishes.
- `Delta=0`: the cache alone must serve the revealed query; (5) remains valid.
- Correlated coordinates: a cached common component can help several queries, so equal per-coordinate allocation need not be optimal. The general conditional rate--distortion expression is required.
- Nonidentical variances, distortions, or query costs: the water level changes; (5) is not portable without re-derivation.
- If `J` leaks into the stage-1 filtration, this is no longer the declared problem.
- If the first message can be replaced, fresh coding removes the information-theoretic tax, but archive reads, rewrite traffic, latency, metadata and compute must still be charged.
- If the stage-2 encoder lacks the original source and sees only retained state, the achievability above may fail; it remains a lower bound inherited from the stronger encoder.
- In the extreme retained-message-only model, `M_j` is a function of `(M_0,J)` and cannot add information about `X_j^n` beyond `M_0`; the apparent `Delta`-bit refinement is then informationally useless by data processing.
- An adversary that observes the realized `M_0` before choosing `J(M_0)` defines a stronger adaptive criterion than `max_j E[D_j]`; (5) does not claim to solve it.
- Finite blocklength adds redundancy and failure probability. The equalities here are asymptotic Shannon boundaries.
- Query correctness or fact validity is not identified by `J`; this theorem does not provide a retain-versus-revise oracle.

## 7. Information, state, and compute ledger

Any consuming system must report at least

\[
(D_1,D_2,\text{persistent bits},\text{written bits},
\text{archive bits},\text{raw reads},\text{encode/decode cost}).
\]

Payload must include query descriptors, basis/Gram matrices, codebooks, dictionaries, framing, checksums and adaptive parameters. Cumulative writes, overwritten bytes, garbage collection, write amplification, peak scratch memory and device must not be hidden. Raw-history and retained-state-only regimes are separate comparisons.

The rates `R` and `Delta` above are bits per `m`-coordinate source vector per sample. Quoting them per scalar silently multiplies the aggregate budget by `m` and invalidates (5)--(7).

Strong same-information controls are: (i) fresh query-aware re-encoding at equal final payload; (ii) the optimal single-user lossy cache code; (iii) independent per-query Gaussian layers; (iv) one robust code for the declared metric family; (v) direct query-weighted quotient/ledger storage; and (vi) no-update, last-k and merge policies for deployment context.

## 8. Closest work and disposition

Timo, Saeedi Bidokhti, Wigger and Geiger formalize exactly a cache message produced before an arbitrary request and a request-specific delivery message afterwards. Their single-user informational region is a conditional rate--distortion minimization; for identical independent sources and symmetric distortions they give

\[
R(D,C)=[R_X(D)-C/m]^+,
\]

with the explicit prescription to cache `C/m` bits from every source. Setting `C=R`, delivery rate `Delta`, and Gaussian `R_X(D)=0.5 log2(sigma^2/D)` gives (5) exactly. Their work also treats correlated and multivariate Gaussian sources. Timo et al. explicitly identify prior Gaussian average-performance caching with demand probabilities; this blocks novelty of introducing the `p_j` objective, while (8)--(10) are independently derived here and were not formula-matched to that paper in this audit. Universal/runtime-distortion coding is adjacent but different: there the distortion is known to the encoder when its one message is formed, whereas here the immutable cache precedes query reveal.

Therefore the patch succeeds mathematically but collides functionally with established lossy caching/prefetching. The result is a precise Delta-facing theorem/debug control, not a new updater or math-card candidate. Candidate, scientific-admission and selection increments are all zero. Empirical effect remains unknown.

## 9. Measurement status and reopen condition

No already pinned native asset jointly provides a byte-hashed immutable stage-1 snapshot, a query metric withheld until a native reveal event, an append-only and a fresh-recode arm at equal total payload, common official scoring, and full archive/read/write/compute accounting. WritePolicyBench is closest on actions and byte budget; LongMemEval-V2 on insert/query/latency; AToKE-ME on future-query records. Splicing them would create a new benchmark, which this phase does not authorize.

Reopen only if either:

1. a public native object supplies that causal snapshot/reveal contract and shows a residual not explained by the optimal lossy-cache baseline; or
2. a lawful Delta state mechanism exploits a declared structural restriction (for example correlated query sufficient statistics) and proves a strict matched-bit, matched-metadata and matched-compute advantage over the general rate--distortion--cache solution or its strongest direct implementation.

Current disposition: close `compound_query_hedge v1` as a classical theorem/control. Do not promote it to the active pool.
