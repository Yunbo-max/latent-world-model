# Step 2 residual object: query-weighted finite-bit rate--distortion boundary

Date: 2026-10-12  
Status: `theorem/control`; `candidate_delta=0`; empirical effect unknown; no model code, training, inference, scoring, or experiment executed.  
Lineage: new Step-2 parent object. It is not a fourth revision of exhausted R17, R18, or R19. It changes the formal question from exact real-valued protection to lossy finite-bit preservation under a declared query task.

## 1. Scientific question

Suppose a Delta memory or side ledger must be represented by at most (B) bits. What query error is unavoidable, what part is caused by missing semantic evidence rather than bit precision, and when can a causal online quantizer keep that error bounded?

This is a useful capacity/debugging question. It is not evidence that a new updater exists. The derivation below shows that, under quadratic query loss, the proposed "semantic" compression reduces to task-based/indirect rate--distortion in the same observability metric already used by R17--R18; its coordinate-model zero-error lower bound numerically matches R19 after the quotient-coordinate identification. The retained contribution is a single Delta-specific bridge joining those three boundaries and making explicit the kernel compatibility required by this particular seminorm recursion.

## 2. Formal object and information contract

Let (S\in\mathbb R^{d_k\times d_v}) be the state that must be represented, (x=\operatorname{vec}(S)), and let (Z) be the stored code. A hard state budget means

\[
|\mathcal Z|\le 2^B,
\qquad I(x;Z)\le H(Z)\le B.
\]

The decoder produces (\widehat S(Z)). For a deployment query (q\in\mathbb R^{d_k}), the squared task loss is

\[
d(S,\widehat S;q)=\|(S-\widehat S)^Tq\|_2^2.
\]

For the fixed-Gram results below, \(q\sim\pi\) is independent of \((S,Z)\). More generally, it is sufficient that its conditional second moment is the same fixed matrix almost surely:

\[
\mathbb E[qq^T\mid S,Z]=G_\pi:=\mathbb E_\pi[qq^T]\quad\text{a.s.}
\]

Then

\[
D_\pi
=\mathbb E\,d(S,\widehat S;q)
=\mathbb E\,\operatorname{tr}\!\left[(S-\widehat S)^TG_\pi(S-\widehat S)\right]
=\mathbb E\|W_\pi^{1/2}(x-\widehat x)\|_2^2,
\]

where (W_\pi=I_{d_v}\otimes G_\pi). If \(\mathbb E[qq^T\mid S,Z]\) varies with the latent state, code, or action, this reduction to one fixed \(G_\pi\) is invalid; the joint or conditional second moment must be retained.

The encoder may see only an allowed observation (O), not the latent semantic state (x), future realized queries, hidden validity labels, or task-answer oracles. Codebook, query-law estimator, shared randomness, scaling, overflow rules, decoder state, and metadata all count toward information/state/compute cost.

## 3. Observation error separates from bit error

Let

\[
m(O)=\mathbb E[x\mid O].
\]

Assume \(\mathbb E\|x\|_2^2<\infty\), so this conditional mean exists in \(L_2\) and is an orthogonal projection in the weighted seminorm.

For every decoder (\widehat x=\widehat x(Z)) whose code is generated from (O) (allowing encoder randomness conditionally independent of (x) given (O)), conditional orthogonality gives

\[
\boxed{
D_\pi
=D_{\mathrm{obs}}
+\mathbb E\|W_\pi^{1/2}(m(O)-\widehat x)\|_2^2
}
\tag{1}
\]

with

\[
D_{\mathrm{obs}}
=\mathbb E\|W_\pi^{1/2}(x-m(O))\|_2^2.
\]

Thus no number of bits removes ambiguity about the declared state \(x\) that is not identified by the allowed observation. More bits can encode only its observable posterior statistic. External provenance, validity, or correct-action labels are charged by \(D_{\mathrm{obs}}\) only if they are represented in \(x\) and in the declared query distortion; if they are absent from that target, equation (1) does not measure them at all.

## 4. Gaussian Shannon lower bound

First suppose (x\sim\mathcal N(0,\Sigma)). Let the nonzero eigenvalues of

\[
W_\pi^{1/2}\Sigma W_\pi^{1/2}
\]

be (\lambda_1,\ldots,\lambda_r). Any single-state code with at most (2^B) messages is a special case of the broader Shannon coding problem, so its distortion obeys

\[
\boxed{
D_\pi^{\mathrm{one\mbox{-}state}}(B)
\ge D_{\mathrm{Sh}}(B)
=\sum_{j=1}^r\min(\lambda_j,\theta)
}
\tag{2}
\]

where (\theta\ge0) is chosen so that

\[
B=\frac12\sum_{j=1}^r\log_2^+\frac{\lambda_j}{\theta}.
\tag{3}
\]

This is a converse, not a claim that a one-token recurrent quantizer attains reverse water-filling.

For the indirect case, additionally assume ((x,O)) is jointly Gaussian, so (m(O)) is Gaussian. If (\bar\lambda_j) are the nonzero eigenvalues of

\[
W_\pi^{1/2}\operatorname{Cov}(m(O))W_\pi^{1/2},
\]

then (1)--(3) give

\[
\boxed{
D_\pi^{\mathrm{one\mbox{-}state}}(B)
\ge D_{\mathrm{obs}}+\sum_j\min(\bar\lambda_j,\bar\theta)
}
\tag{4}
\]

with (B=\frac12\sum_j\log_2^+(\bar\lambda_j/\bar\theta)). Covariance alone does not justify (4) for an arbitrary non-Gaussian posterior statistic; Gaussian reverse water-filling must not be silently exported beyond this assumption.

## 5. Constructive finite-precision upper bounds

Diagonalize the weighted observable statistic: for an orthogonal eigenbasis \(U\), write \(Y=U^TW_\pi^{1/2}m(O)\). Let coordinate \(Y_j\) be retained over a declared range \([-A_j,A_j]\). Allocate integer \(b_j\ge0\) bits with \(\sum_jb_j\le B\). For \(b_j\ge1\), nearest uniform quantization with \(2^{b_j}\) levels including both endpoints has spacing \(2A_j/(2^{b_j}-1)\), hence pointwise squared error at most

\[
\epsilon_j\le \frac{A_j^2}{(2^{b_j}-1)^2}.
\tag{5}
\]

For (b_j=0), use a declared constant reconstruction and charge its full second moment. Therefore, for bounded coordinates,

\[
D_\pi\le D_{\mathrm{obs}}+\sum_j\epsilon_j.
\tag{6}
\]

For \(Y_j\sim\mathcal N(0,\nu_j)\), clip at \(A_j=a_j\sqrt{\nu_j}\) and quantize the clipped value with endpoint levels. Writing \(Q(a)=\Pr[N(0,1)>a]\) and \(\phi\) for the standard normal density,

\[
\epsilon_j
\le
\frac{A_j^2}{(2^{b_j}-1)^2}
+2\nu_j\left[(1+a_j^2)Q(a_j)-a_j\phi(a_j)\right].
\tag{7}
\]

The second term is the exact clipping-tail second moment (\mathbb E[(|Y_j|-A_j)_+^2]). Equations (5)--(7) are explicit fixed-codebook upper bounds; they do not inherit asymptotic Shannon achievability for free.

## 6. Recursive propagation and the required kernel condition

Assume a lawful finite-dimensional observable statistic evolves as

\[
v_t=A_tv_{t-1}+g_t(O_t),
\qquad
\widehat v_t=Q_t(A_t\widehat v_{t-1}+g_t(O_t)).
\]

Let (e_t=v_t-\widehat v_t=A_te_{t-1}+\eta_t), and let (H_t\succeq0) be the current query/observability metric. A recursion in the previous seminorm requires

\[
\boxed{
\ker H_{t-1}\subseteq\ker(H_t^{1/2}A_t)
}
\tag{8}
\]

so that a direction previously assigned zero distortion cannot become visible at time (t). Under (8), define

\[
L_t=\|H_t^{1/2}A_tH_{t-1}^{\dagger/2}\|_2,
\qquad
\mathbb E\|H_t^{1/2}\eta_t\|_2^2\le\epsilon_t.
\]

Minkowski's inequality in (L_2) yields

\[
\sqrt{D_t}\le L_t\sqrt{D_{t-1}}+\sqrt{\epsilon_t},
\tag{9}
\]

and therefore

\[
\boxed{
\sqrt{D_T}
\le
\left(\prod_{j=1}^TL_j\right)\sqrt{D_0}
+\sum_{s=1}^T
\left(\prod_{j=s+1}^TL_j\right)\sqrt{\epsilon_s}
}.
\tag{10}
\]

If (8) fails, no bound depending only on (D_{t-1}) exists: choose (u\in\ker H_{t-1}) with (H_t^{1/2}A_tu\ne0), scale (e_{t-1}=cu), and obtain (D_{t-1}=0) but arbitrarily large next distortion. This is exactly the bridge-query failure mode. If (L_t>1) repeatedly, even small quantization errors can be amplified.

For a prefix-lawful construction, (H_t) must come from a fixed or causally predicted query family. Replacing it by the realized future query Gram is an unavailable oracle. A public upper envelope is safe but can collapse to the full-state metric.

## 7. Discrete lossy endpoint and R19

Let a quotient semantic state \(C=(C_1,\ldots,C_r)\) be uniform on \(\mathbb F_q^r\). The encoder must create \(Z\) from \(C\) before the query index is revealed: \(p(z\mid C,J)=p(z\mid C)\). Let \(J\) then be uniform on \(\{1,\ldots,r\}\) and independent of \((C,Z)\), and let the decoder produce \(\widehat C_J(Z,J)\) with average symbol error probability \(D\). Coordinate-wise Fano inequalities, conditional entropy subadditivity, and concavity give

\[
\boxed{
B\ge
r\left[
\log_2q-h_2(D)-D\log_2(q-1)
\right]
}.
\tag{11}
\]

At (D=0), this becomes (B\ge r\log_2q), recovering the same \(q^r\)-message numerical lower bound after identifying these \(r\) coordinates with R19's quotient reduction. R19's decoder side information and branch-target structure are additional assumptions, not implied by this coordinate model. If only (b) coordinates can be stored exactly and coordinate (i) is queried with probability (p_i), keeping the (b) largest-probability coordinates and guessing the rest gives

\[
D\le\left(1-\frac1q\right)\sum_{i\notin I_b}p_i,
\qquad b\log_2q\le B.
\tag{12}
\]

Better joint codes are ordinary (q)-ary lossy source codes. Allowing error in this quotient-coordinate model therefore leads to standard lossy coding; it does not by itself extend R19's full branch/decoder-side-information theorem or create a new updater.

## 8. Old counterexamples and failure boundaries

1. **Unidentified validity survives outside the declared distortion.** Two semantic worlds can have the same (O), code, query law, and \(x=\operatorname{vec}(S)\) but opposite correct write actions. Equation (1) does not see that external label unless it is added to the target/distortion; extra bits about \(x\) do not identify the world.
2. **Rare queries are deliberately sacrificed.** An average (G_\pi) can assign negligible weight to a rare but important direction. Distribution shift or worst-case protection needs a robust envelope, returning to R17--R18.
3. **Future bridges revive discarded directions.** Failure of (8) invalidates the recursive bound regardless of current reconstruction error.
4. **State-dependent queries need a joint model.** A fixed average Gram is wrong when the memory/action changes the future query distribution and thereby changes its conditional second moment.
5. **Side information changes the problem.** If queries or branch labels are visible only to the decoder, conditional/Wyner--Ziv or branch-code analysis is required.
6. **Finite range is substantive.** Overflow, clipping, precision, and saturation must be explicit; a real-valued state dimension is not a bit budget.
7. **Controlled dynamics are not static RDF.** If the code/action changes later state or observations, the object is controlled/nonanticipative rate--distortion, not equations (2)--(7) alone.

## 9. Nearest work and distinctness

- Task-based and indirect quantization already separate irreducible observation MMSE from excess coding MSE and design quantizers around the downstream task.
- Nonanticipative rate--distortion already treats causal encoder/channel/decoder realizations, partially observed Gauss--Markov sufficient statistics, SDP characterizations, and dynamic reverse water-filling.
- Goal-oriented quantization already weighs quantization by downstream decision loss.
- R17 already supplies the query/observability Gram and spectral-tail control; R18 supplies recursive quotient, robust fibers, and direct ledgers; R19 supplies the zero-error finite-state endpoint.

The only retained local delta is the explicit Delta matrix-to-query reduction plus equations (1), (4), (8)--(12) in one audit object. That is a useful theorem/control and a guard against conflating semantic uncertainty, bit distortion, and recursive bridge exposure. It is not a substantively distinct update mechanism and has no proved matched-cost advantage over a direct task-aware quantizer or quotient ledger.

## 10. Strong same-information controls

| Control | What it matches | Required discriminator |
|---|---|---|
| direct quantized ledger | same (B) bits, codebook and query weights | a smaller causal distortion bound or lower total state/traffic/compute |
| task-based vector quantizer | same observation and task loss | a Delta-specific attainable advantage, not merely the same weighted metric |
| causal/nonanticipative RDF filter | same causal observation process and distortion | an online construction or bound outside the generic solution class |
| R17 spectral gate | same future Gram but avoids storing an unsafe write | lossy storage must beat abstention/gating at equal capability and cost |
| R18 direct quotient/side code | same protected fibers and recurrence | compression must preserve required behavior with strictly less matched total cost |
| R19 exact syndrome | same finite alphabet at zero error | only a nonzero-error tradeoff remains, which must beat ordinary lossy coding |
| retrieval/external KV | same total bits and access budget | internal Delta storage must add measurable value beyond retaining the source |

## 11. Testable predictions and native measurement status

The theorem predicts that, within its assumptions:

1. query-weighted error follows the spectrum of (W_\pi^{1/2}\Sigma W_\pi^{1/2}), not unweighted Frobenius reconstruction;
2. increasing (B) cannot reduce the irreducible (D_{\mathrm{obs}});
3. a bridge query violating (8) can reveal arbitrarily large error despite zero prior seminorm error;
4. under a stable compatible recurrence, accumulated root-MSE is bounded by (10);
5. the zero-error finite-field endpoint recovers R19's same \(q^r\) numerical lower bound under the quotient-coordinate identification, not R19's full branch/side-information theorem.

Existing bAbI, LAMBADA, RULER, BABILong, LongMemEval, LongMemEval-V2, EvoMemBench, AToKE, and SEAL can measure downstream behavior of a future implementation, but their native scorers do not expose the latent/observable decomposition, actual stored bit alphabet, lawful prefix query Gram, codebook/metadata cost, compatibility condition (8), per-step quantization noise, or matched direct-ledger curve. An instrumented rate--distortion diagnostic would be derived rather than native evidence. No benchmark, labels, metric, case, or result is created here.

## 12. Decision

The mathematics supports a scoped finite-bit theorem/debugging control. The line does **not** become a candidate because its core mechanisms are already task-based/indirect and nonanticipative rate--distortion, while its Delta specialization collapses to the R17--R19 metric/quotient/syndrome controls. Reopen only if a prefix-causal Delta rank-one recurrence yields a proved attainable distortion or total-cost bound strictly better than direct task-aware quantization, generic causal RDF, and the strongest quotient ledger under identical bits, metadata, query information, and decoder capability.

Counts remain: 5 historical retired cards, 0 active candidates, 0 scientifically admitted, 0 selected. The 20/15 goal remains incomplete. Empirical effect remains unknown.
