# R13 — Minimum erasure ledger for bounded protected-readout transport (attempt 3)

## Status and lineage

- Parent v1, R13_DYNAMIC_COVECTOR_PROTECTION.v1.md, proved exact affine transport through one known realized step, the singular-overwrite obstruction, and reciprocal conditioning near overwrite.
- Parent v2, R13_ROBUST_COMMON_COVECTOR.v2.md, proved that a hidden realized mode can make one common decoder impossible even when every mode is invertible.
- This is substantive repair attempt **3/3**.
- v1's whole protected-value ledger was only a coarse control. The patch derives the minimum additional linear state required for the quotient actually erased by the realized step, plus an exact spectral-cut construction.
- Intended contribution: conditional theorem/debug control. It is a one-step specialization of functional observation and packet-internal R18/R12 sufficient-coordinate results, not a distinct updater.

## 1. Formal object and information boundary

Let
\[
Z=AS+B,\qquad
S,Z,B\in\mathbb R^{d_k\times d_v},\quad
A\in\mathbb R^{d_k\times d_k}
\tag{1}
\]
be one causally realized affine memory step. The declared pre-step protected object is
\[
T(S)=Q^\top S+C_0,\qquad
Q\in\mathbb R^{d_k\times p},\quad
C_0\in\mathbb R^{p\times d_v}.
\tag{2}
\]

Before applying (1), a linear encoder may retain
\[
H=L^\top S\in\mathbb R^{s\times d_v},
\qquad L\in\mathbb R^{d_k\times s}.
\tag{3}
\]
After the step, an affine decoder uses
\[
g(Z,H)=XZ+KH+C,
\qquad X\in\mathbb R^{p\times d_k},\quad
K\in\mathbb R^{p\times s}.
\tag{4}
\]

The realized \((A,B,Q)\) are fixed over all state alternatives and known at the required time. This is v1's revealed-step interface, not v2's hidden-mode interface. The ledger is written before the destructive step. Exactness is required over the declared full linear state space:
\[
g(AS+B,L^\top S)=Q^\top S+C_0
\quad\text{for every }S.
\tag{5}
\]

A certified reachable affine subspace may replace the full space by its admissible difference space, but it must be fixed from the same retained prefix information. The theorem preserves a declared numerical functional. It does not identify which fact remains valid and grants no future query, target, evaluator answer, or suffix oracle.

## 2. Minimum exact linear side-ledger theorem

Coefficient and offset matching in (5) give
\[
XA+KL^\top=Q^\top,\qquad C=C_0-XB.
\tag{6}
\]

Let \(N\in\mathbb R^{d_k\times r_0}\) have orthonormal columns spanning \(\ker A\), and let
\[
P_{\ker A}=NN^\top=I-A^\dagger A.
\tag{7}
\]
Define
\[
\ell_\star
=\operatorname{rank}(Q^\top N)
=\operatorname{rank}(Q^\top P_{\ker A}).
\tag{8}
\]

**Theorem 1.** Among ledgers of the columnwise linear form (3), the minimum number of retained rows allowing exact recovery is exactly \(\ell_\star\). Even if an unrestricted real-linear encoder may mix all \(d_v\) columns after vectorization, the minimum number of retained real scalar coordinates is \(d_v\ell_\star\).

### Necessity

Multiplying (6) by \(N\) yields
\[
K(L^\top N)=Q^\top N.
\tag{9}
\]
Hence
\[
s\ge \operatorname{rank}(Q^\top N)=\ell_\star.
\tag{10}
\]

For an unrestricted vectorized linear code, the post-map and target map are
\[
I_{d_v}\otimes A,\qquad I_{d_v}\otimes Q^\top.
\tag{11}
\]
The restriction of the target to the post-map kernel has rank
\[
\operatorname{rank}\!\left(
(I_{d_v}\otimes Q^\top)
\big|_{\mathbb R^{d_v}\otimes\ker A}
\right)
=d_v\,\operatorname{rank}(Q^\top N).
\tag{12}
\]
Any exact linear side code must separate that quotient, proving the scalar lower bound.

### Attainment

Take a thin SVD
\[
Q^\top N=U_\ell\Sigma_\ell V_\ell^\top,
\qquad \ell=\ell_\star.
\tag{13}
\]
Set
\[
L=NV_\ell,\qquad K=U_\ell\Sigma_\ell.
\tag{14}
\]
Then
\[
KL^\top=Q^\top NN^\top=Q^\top P_{\ker A}.
\tag{15}
\]
Put
\[
M=Q^\top-KL^\top,\qquad X=MA^\dagger.
\tag{16}
\]
Because \(MN=0\), every row of \(M\) lies in the row space of \(A\), so
\[
XA=MA^\dagger A=M.
\tag{17}
\]
Together with \(C=C_0-XB\), equations (14)--(17) attain (6).

The exact extra state is therefore the protected image of the directions erased by the transition. It does not make \(A\) reversible or retain unrelated coordinates.

## 3. Rank-budget tail and its boundary

For a side-row budget \(s<\ell_\star\), consider
\[
\min_{\substack{X,K,L\\ \operatorname{rank}(KL^\top)\le s}}
\left\|Q^\top-XA-KL^\top\right\|_F.
\tag{18}
\]
Let
\[
G=Q^\top P_{\ker A}.
\tag{19}
\]
Right multiplication by \(P_{\ker A}\) lower-bounds every feasible residual by the best rank-\(s\) approximation error of \(G\). Conversely, if \(G_s\) is the rank-\(s\) truncated SVD of \(G\), then
\[
X=(Q^\top-G_s)A^\dagger,\qquad KL^\top=G_s
\tag{20}
\]
attains the lower bound. Therefore
\[
\min (18)=
\left(\sum_{j>s}\sigma_j(G)^2\right)^{1/2}.
\tag{21}
\]

Equation (21) is an exact coefficient-space statement, not a semantic-loss bound. A state-space claim additionally needs a certified norm bound, for example
\[
\|(G-G_s)S\|_F
\le \|G-G_s\|_2\,\|S\|_F.
\tag{22}
\]
Without such a bound, arbitrarily small coefficient residual can accompany arbitrarily large endpoint ambiguity after rescaling \(S\).

The lower bound is for real-linear encoders. It is not an unconditional finite-bit bound and does not cover pathological discontinuous encodings of many reals into one real. A finite-precision claim must specify quantizer, range, tolerance, and noise.

## 4. Stable spectral-cut construction

The exact no-ledger decoder can be badly conditioned even when \(A\) is invertible. Let
\[
A=W\Sigma V^\top
\tag{23}
\]
be an SVD and fix a declared threshold \(\tau>0\). Let \((V_H,W_H,\Sigma_H)\) contain singular directions with \(\sigma_i\ge\tau\), and define
\[
P_L=I-V_HV_H^\top.
\tag{24}
\]
Set
\[
X_\tau
=Q^\top V_H\Sigma_H^{-1}W_H^\top,
\qquad
G_\tau=Q^\top P_L.
\tag{25}
\]
Then
\[
X_\tau A+G_\tau=Q^\top,\qquad
\|X_\tau\|_2\le \frac{\|Q\|_2}{\tau}.
\tag{26}
\]

Factoring \(G_\tau=KL^\top\) as in (13)--(14) gives an exact hybrid decoder: protected high-singular content is read from \(Z\), while only the protected low-singular quotient is retained before the step. For this declared spectral-cut decoder class, its exact side width is
\[
\ell_\tau=\operatorname{rank}(Q^\top P_L).
\tag{27}
\]
If \(X\) is fixed to \(X_\tau\), or the decoder is explicitly forbidden to use the low-singular directions, a smaller side budget has the Eckart--Young tail for \(G_\tau\). This is not the unconstrained optimum in (18): with free \(X\), an invertible but ill-conditioned \(A\) still permits zero-ledger exact inversion.

This does not prove a universal optimal \(\tau\). It exposes a state/noise tradeoff: increasing \(\tau\) bounds inverse amplification but can increase side state. Using the normalized SVD factorization from (13)--(14), if post-state and ledger errors are \(E_Z,E_H\), then
\[
\|\widehat T-T\|_F
\le \|X_\tau\|_2\|E_Z\|_F
+\|K\|_2\|E_H\|_F
+\text{declared truncation bias}.
\tag{28}
\]
The normalization matters because rescaling \(L\) and \(K\) changes a ledger-noise model. Choosing \(\tau\) from test labels, future noise, or an unobserved suffix would be leakage; it must come from causal calibration or an explicit numerical contract.

## 5. Delta specialization

For
\[
A=(I-\beta kk^\top)D,\qquad B=\beta kv^\top,
\tag{29}
\]
assume \(D\) is invertible and set
\[
\delta=1-\beta\|k\|_2^2.
\tag{30}
\]

If \(\delta\ne0\), then \(A\) is invertible, \(\ell_\star=0\), and v1's exact transported decoder exists. Zero extra state does not remove its \(1/|\delta|\) conditioning.

At exact overwrite, \(\delta=0\), and
\[
\ker A=\operatorname{span}(D^{-1}k).
\tag{31}
\]
For
\[
n=\frac{D^{-1}k}{\|D^{-1}k\|_2},
\tag{32}
\]
we have
\[
\ell_\star=\operatorname{rank}(Q^\top n).
\tag{33}
\]
Because \(Q^\top n\) has one column, \(\ell_\star=0\) when the protected family is orthogonal to the erased direction and \(\ell_\star=1\) otherwise. In the overlapping case, exactly one \(d_v\)-vector,
\[
H=n^\top S,
\tag{34}
\]
is necessary and sufficient, regardless of \(p\).

Thus the coarse full-value ledger \(Q^\top S\) costs \(p\,d_v\) scalars, while the optimal lost-coordinate ledger costs \(d_v\) scalars for one exact rank-one overwrite when \(p>1\). This is still a same-information direct ledger, not new evidence and not a validity rule.

## 6. Horizon and switching boundaries

Suppose the complete product and accumulated affine offset are fixed across all compared states and known before the ledger is encoded:
\[
Z_T=P S_0+b,\qquad P=A_TA_{T-1}\cdots A_1.
\tag{35}
\]
Then the pre-horizon minimum linear ledger width for recovering \(Q_0^\top S_0\) is
\[
\operatorname{rank}(Q_0^\top N_P),
\qquad \operatorname{col}(N_P)=\ker P.
\tag{36}
\]
This is generally noncausal online if the suffix is unknown when the ledger decision is made. It is therefore only a known-horizon control unless a lawful causal generator or robust prefix tree is supplied; R18 covers the latter threat model.

For pure no-decay partial Delta modes
\[
A_i=I-\beta_i k_i k_i^\top,\qquad
0<\beta_i\|k_i\|_2^2<1,
\tag{37}
\]
revealed-mode no-ledger covector transport obeys \(q_{t+1}=A_i^{-T}q_t\). Under arbitrary switching, \(\|q_t\|\) is uniformly bounded for every sequence if and only if
\[
q_0\in\bigcap_i k_i^\perp.
\tag{38}
\]
Sufficiency holds because every \(A_i^{-T}\) fixes that intersection. For necessity, decompose \(q_0\) against a mode with \(k_i^\top q_0\ne0\); repeatedly selecting that mode grows the parallel component geometrically. This is an elementary common-fixed-subspace/JSR specialization, not a new switching method. It also eliminates that mode's affine write contribution to the protected readout.

## 7. Old counterexamples rechecked

1. **Exact overwrite without side state:** Theorem 1 preserves v1's impossibility whenever \(Q^\top\ker A\ne\{0\}\); it quantifies the missing quotient.
2. **Hidden mode:** v2's same-\(Z\), different-target invertible-mode pair survives. The present construction requires the realized step or its sufficient label.
3. **Semantic validity:** identical retained numerical inputs with opposite truth status still induce the same ledger and decoder output.
4. **Full nonlinear network:** the affine theorem is exact only for the declared memory transition/readout. End-to-end effects still require the complete state Jacobian.
5. **Near overwrite:** the spectral cut exposes rather than removes inverse-conditioning cost.

## 8. State, information, and computation cost

Per item, the optimal exact ledger retains \(\ell_\star d_v\) real scalars; the spectral version retains \(\ell_\tau d_v\). If coefficients cannot be regenerated from already available transition metadata, storage additionally includes:

- \(L\): \(d_k\ell\) scalars;
- \(K\): \(p\ell\) scalars;
- \(X\): \(p d_k\) scalars;
- the offset and threshold/factorization metadata.

Online work includes the pre-read \(L^\top S\), post-read \(XZ\), and ledger term \(KH\), with corresponding memory traffic and latency. Setup includes a kernel/SVD or structured equivalent and must be amortized over a declared reuse horizon. Precision of the basis, ledger, and decoder is part of the budget. A fair comparison must match visible prefix, mode evidence, retained bytes, coefficient storage, bandwidth, setup amortization, online FLOPs, latency, and access rights.

Strong same-information controls are the identical optimal lost-coordinate ledger, the full \(Q^\top S\) ledger, revealed-mode v1 transport, full Delta/no compression, matched replay/checkpoint or external KV, R18's direct quotient, set-membership observation, and a Bayes conditional mean under the same lawful prior and observations.

## 9. Falsifiable predictions and measurement gap

- Extra state changes discontinuously when \(Q^\top\ker A\) changes rank.
- A rank-one exact overwrite with nonzero overlap needs one \(d_v\)-vector, not \(p\) vectors.
- As a retained singular value approaches zero, exact no-ledger decoder norm diverges; moving that direction into the ledger caps amplification at the chosen threshold.
- Below the ledger rank, the optimal coefficient residual follows the singular-value tail in (21).

Pinned bAbI, LAMBADA, RULER, BABILong, and LongMemEval assets measure endpoint behavior only. They do not natively expose \(A,Q,\ker A,\ell_\star\), same-post-state counterfactual targets, ledger bytes, or validity labels. They may later falsify an implementation's downstream claim, but cannot attribute benefit to this mechanism. Matrix/SVD traces are derived theorem diagnostics, not native efficacy evidence. Empirical effect is **unknown**; no model run or score was performed.

## 10. Contribution and disposition

The useful repair is a sharper control:
\[
\boxed{\ell_\star=\operatorname{rank}(Q^\top N)}
\]
with explicit attainment, cross-column scalar accounting, rank-budget tail, spectral-cut tradeoff, and the exact one-vector Delta-overwrite corollary.

Mechanism-level novelty is not established. Generalized inverses, minimum/functional observers, low-rank approximation, reversible side information, and packet-internal R18/R12/R19 cover the mechanism family. This third substantive attempt is exhausted. R13 is parked with candidate delta zero, no scientific admission, and empirical effect unknown.
