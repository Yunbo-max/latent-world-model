# R17 v3 — residual-scaled low-rank spectral certificate for a Delta write

Status: **conditional theorem/debugging control; parked after the final substantive attempt 3/3; not an active D candidate**. This versioned child preserves the exact bytes, counterexamples and reviews of R17 v1/v2. It repairs one remaining target mismatch: v2 bounded an arbitrary erased perturbation `ka^T`, whereas an actual gated Delta action has the prefix-known perturbation `beta k e^T`, with residual `e=v-Sbar^T k`. It also compresses a lawful one-sided future-Gram certificate without losing its upper-bound direction. The result is a causal, computable safe-step rule and a sharp rank-versus-slack boundary. It does not identify which future changes are harmful, construct the prefix certificate, or establish novelty over standard Delta gating, observability Gramians and low-rank matrix sketches.

## 1. Lineage, convention and actual action

Work after any declared decay and before the current write. Let

\[
\bar S\in\mathbb R^{d\times m},\quad \|k\|_2=1,\quad
e=v-\bar S^\top k\in\mathbb R^m . \tag{1}
\]

A gated Delta update is

\[
S^+(\beta)=\bar S+\beta k e^\top,
\qquad 0\le\beta\le1. \tag{2}
\]

For a frozen continuation `omega`, define effective covectors
`x_{u,omega}=P_{u,omega}^T q_{u,omega}`, nonnegative weights `w_u`, and

\[
G_\omega=\sum_u w_u x_{u,\omega}x_{u,\omega}^\top\succeq0. \tag{3}
\]

Relative to the no-write branch with the same exogenous continuation, the exact weighted output-change energy is

\[
\begin{aligned}
\mathcal I_\omega(\beta)
&=\sum_u w_u\|q_{u,\omega}^\top P_{u,\omega}(S^+(\beta)-\bar S)\|_2^2\\
&=\beta^2\|e\|_2^2 k^\top G_\omega k. \tag{4}
\end{aligned}
\]

This is not the v1/v2 all-state decodability claim. It is an action-specific frozen-path interference identity. It is prefix-computable except for the future Gram. If future inputs, keys, gates or queries react to the action, (4) needs a common-exogenous coupling plus the full state Jacobian/remainder; it is not a free-running nonlinear guarantee. For an invertible pre-decay map `D`, the corresponding old-state lost direction is `D^{-1}k`, exactly as in v1/v2. If `D` is singular, a pseudoinverse substitution is insufficient: the complete preimage/kernel from v1 equation (4) must be retained.

## 2. Prefix-valid one-sided certificate and composition

Let `F_t` be the information available before choosing `beta`. Suppose a prefix-measurable PSD matrix `U_t` satisfies the v2 contract

\[
\Pr(G_\omega\preceq U_t\mid\mathcal F_t)\ge1-\delta. \tag{5}
\]

Now compress `U_t`. Let `L_t in R^(d x r)` and `epsilon_t>=0` be prefix-measurable and satisfy

\[
U_t\preceq C_t:=L_tL_t^\top+\epsilon_t I. \tag{6}
\]

Then, on the event in (5),

\[
\boxed{\mathcal I_\omega(\beta)
\le\beta^2\|e\|_2^2
\left(\|L_t^\top k\|_2^2+\epsilon_t\|k\|_2^2\right).} \tag{7}
\]

Proof: (5) and (6) give `G_omega <= C_t`; apply the quadratic form in direction `k` and multiply by the nonnegative factor `beta^2||e||^2`. No independence is needed.

If `L_t,epsilon_t` are already measurable in the decision sigma-field `F_t`, (6) is a deterministic condition given `F_t`. For a randomized compressor, instead let `F_t^0` denote the pre-compression information, draw compressor randomness after `F_t^0`, and require (6) with conditional failure probability at most `eta` relative to `F_t^0`. The realized factor and residual then enter the enlarged decision field `F_t=sigma(F_t^0,L_t,epsilon_t)` before choosing `beta`. A union bound with the future-Gram failure event gives coverage at least `1-delta-eta`; no independence is required, and randomized compression error may not be omitted. A two-sided norm approximation `||U_t-L_tL_t^T||_2<=epsilon_t` implies (6), but a low-rank approximation without a certified residual does not.

The crucial correction from v2 is the factor `||e||^2`. A certificate of the direction alone is insufficient for the actual action. Conversely, when `e=0`, the update changes no state and (7) is exactly zero even if `k^T U_t k` is large.

## 3. Exact spectral construction and rank/slack boundary

Let the eigenvalues of a fixed `U_t` be

\[
\lambda_1\ge\cdots\ge\lambda_d\ge0,
\quad U_t=\sum_{i=1}^d\lambda_i u_i u_i^\top . \tag{8}
\]

For `0<=r<d`, choose

\[
L_r=[\sqrt{\lambda_1}u_1,\ldots,\sqrt{\lambda_r}u_r],
\qquad \epsilon_r=\lambda_{r+1}. \tag{9}
\]

Because

\[
U_t-L_rL_r^\top=\sum_{i>r}\lambda_i u_i u_i^\top
\preceq\lambda_{r+1}I, \tag{10}
\]

(6) holds. The corresponding score is

\[
c_r(k)=\sum_{i=1}^r\lambda_i(u_i^\top k)^2
+\lambda_{r+1}\|k\|_2^2. \tag{11}
\]

The residual radius `lambda_(r+1)` is the smallest possible spectral-norm error of any rank-`r` approximation to `U_t` (Eckart--Young--Mirsky). Therefore no rank-`r` factor can uniformly replace the isotropic remainder in (11) by a smaller spectral residual without extra structure. This is a representation boundary, not a claim that truncated eigenspaces are a new algorithm.

A slightly tighter exact eigen-tail upper matrix is

\[
\widetilde C_r=L_rL_r^\top+\lambda_{r+1}(I-U_rU_r^\top), \tag{12}
\]

where `U_r=[u_1,...,u_r]`; its tail dominates every `lambda_i, i>r`. Equation (12) needs the same basis and avoids adding `lambda_(r+1)` on the retained subspace. The simpler (11) remains valid for arbitrary certified low-rank factors.

## 4. Computable safe gate

For a declared frozen-path interference budget `tau>=0`, define

\[
s_t=\|e\|_2^2\left(\|L_t^\top k\|_2^2+\epsilon_t\|k\|_2^2\right). \tag{13}
\]

The largest gate certified by (7), conditional on an already-issued lawful certificate, is

\[
\boxed{\beta_{\rm safe}=
\begin{cases}
1,&s_t=0,\\
\min\{1,\sqrt{\tau/s_t}\},&s_t>0.
\end{cases}} \tag{14}
\]

On the joint certificate event, `I_omega(beta_safe)<=tau`. This is an actual prefix-only **gate after** a lawful certificate has been issued: `k`, `e`, `L_t`, `epsilon_t` and `tau` are known when the write is chosen. It is not a construction of (5). Marginal calibration, exchangeability, or stationarity alone does not establish pointwise conditional Loewner coverage for every high-dimensional prefix stratum. The gate is also only a safety throttle. It does not prove that spending the full budget improves prediction, or that a change counted by (4) is harmful rather than a desired revision.

The same-information simple controls remain mandatory:

1. ordinary scalar Delta gating using the exact dense score `k^T U_t k`;
2. a prefix model that directly issues and calibrates only a scalar upper score for the current `(prefix,k)`, or a global/isotropic scalar upper bound, avoiding a dense matrix or factor when no other direction is queried;
3. the low-rank score (13) with abstention when unsafe;
4. the ordinary scalar quadratic comparator, for `lambda>=0` and `c_t>=0`,
   `J(beta)=||e||^2[(1-beta)^2+lambda beta^2 c_t]`, whose constrained minimizer on `beta in [0,1]` for `e!=0` is `beta*=1/(1+lambda c_t)`;
5. direct storage of protected coordinates `B_t^T Sbar` when preservation rather than throttling is required;
6. R09's inverse-metric rank-one edit when the write direction, not only `beta`, may change.

In float-count terms only, the low-rank certificate can use less state than a direct ledger: `L_t,epsilon_t` use `dr+1` real scalars and each score costs `O(dr)`, whereas a rank-`r` direct ledger also stores `B_t^T Sbar in R^(r x m)`. This is not matched-bit or matched-total-cost accounting. Precision, normalization/scales, basis metadata, refresh state and traffic, predictor parameters/activations, calibration storage, and enough numerical margin to preserve the one-sided inequality must all be charged. Equation (12) also requires an explicitly normalized eigenbasis. The two objects are not equivalent capabilities: the certificate merely decides or shrinks a write; the ledger retains protected coordinates through an unsafe write. Claiming an `rm` float saving as a preservation advantage would be false.

## 5. Old counterexamples and new failure boundaries

- **Identical-prefix worlds survive with the correct probability qualifier.** In v2's worlds `G^(0)=e_2e_2^T` and `G^(1)=e_1e_1^T` with `k=e_1`, a deterministic robust common upper bound has score at least one. Under (5), if the harmful world has conditional mass `pi`, any common certificate with score below one fails with probability at least `pi`; the score-at-least-one conclusion follows when `delta<pi` or uniform coverage is required. If `delta>=pi`, the contract may legally discard that world. Compression never identifies which world occurred.
- **Isotropic uncertainty gives no directional low-rank gain.** If `U_t=gamma I`, then the low-rank-factor-plus-isotropic-tail construction has tail radius `gamma` and no directional slack reduction. The matrix is nevertheless storage-compact as one scalar. Diagonal, block, Toeplitz or shared-basis full-rank certificates may also be compact; low algebraic rank is not the only compact structure.
- **Low-rank success case.** If a valid `U_t` has rank at most `r`, then `epsilon_r=0` and (11) is exact. This is the clean exact case for the particular low-rank-plus-isotropic-residual family, and it relies on the certificate already being lawful.
- **Slow spectral decay.** A large `lambda_(r+1)` makes (14) vacuous even if the leading subspace is accurate. Approximation quality in Frobenius norm alone is not sufficient for a one-sided per-direction guarantee.
- **Residual scaling is action-specific.** Small `||e||` makes the actual update harmless under (4), but does not restore v1 quotient decodability for arbitrary old-state pairs. Large `||e||` tightens the gate.
- **Semantic mismatch remains.** `G_omega` weights output movement, not factual harm. A correct revision can have large energy. Removing intended revision queries from `G_omega` requires a validity/protection label that the prefix does not supply.
- **Nonlinear and adaptive paths remain outside the theorem.** A frozen Gram can miss state-dependent future features and compensating channels. Full-state Jacobian or paired intervention evidence is still required.

Thus the old counterexamples are not deleted; the target is narrowed to a computable action-level certificate.

## 6. Construction cost and statistical obligations

If `U_t` is explicitly dense, its eigendecomposition is `O(d^3)` and storage is `O(d^2)`, so compressing it after construction may not save training cost. Randomized SVD and streaming sketches can maintain `O(dr)` real-valued summaries, but their spectral residual, failure probability and precision/metadata cost must be included in (6)--(7). Frequent Directions supplies a deterministic covariance-sketch error, but its published bound is additive and depends on the unretained Frobenius tail; it does not itself supply the prefix-valid future-law coverage (5).

Producing the trajectory Gram still requires effective future covectors or an equivalent instrumented interface during training/calibration. A network that predicts `L_t,epsilon_t` from a prefix adds parameters, compute and a one-sided calibration problem. Reusing a fixed global factor removes per-prefix cost but can be too conservative under heterogeneous continuations. None of these costs may be hidden behind the word “certificate.”

The gate uses no future token, target, answer, factual-validity oracle or post-write outcome at deployment. This artifact supplies no deployed procedure that establishes (5). Historical future trajectories may train/calibrate a proposed certificate only under an explicit sampling/coverage contract; exchangeability, stationarity or time-uniform concentration can support particular marginal, stratum-specific or anytime statements but cannot be silently upgraded to pointwise conditional Loewner coverage. Distribution shift reopens coverage.

## 7. Distinguishing predictions and native-measurement boundary

Conditional predictions are exact:

1. Holding `k` and the certificate fixed, the certified interference scales as `beta^2||e||^2`; halving `beta` quarters the frozen-path bound.
2. For an exact rank-`r` `U_t`, the tail term vanishes; for isotropic `U_t`, no rank below `d` improves the score.
3. If an approximate factor omits a valid spectral residual, there exists a tail eigenvector `k` for which its reported score is too small by the omitted eigenvalue.
4. Under (5)--(6), any observed violation of (7) implies a failed coverage event, a convention/order mismatch, an endogenous continuation, numerical error, or an incorrect implementation—not evidence that the algebraic bound was merely loose.

The fixed bAbI, LAMBADA, RULER and LongMemEval interfaces expose endpoint targets/scores. They do not expose paired no-write continuations, `G_omega`, `U_t`, its one-sided coverage event, the spectral residual, or an equal-budget direct ledger. They can compare downstream behavior after a future implementation, but cannot natively identify whether (7) or (14) caused a difference. An instrumented paired-action trace would measure the mechanism, but that would be a new benchmark object and is not created here.

## 8. Nearest work and final disposition

The ingredients are already mature: Delta's residual-scaled rank-one response, observability Gramians, robust upper metrics, eigentruncation/Eckart--Young--Mirsky, randomized low-rank approximation, Frequent Directions, and scalar trust-region/gating rules. The retained Delta-specific contribution is a clean debugging bridge: it composes v2's lawful future-Gram coverage with a one-sided spectral compression and the actual residual to produce the explicit safe gate (14), while stating exactly why this is cheaper than a ledger only because it offers a weaker capability.

That is a useful theorem/control, not a scientifically admitted method. The prefix certificate is still externally assumed, the mechanism is heavily covered, the direct dense-score gate is a stronger simple comparator when affordable, semantic validity is missing, and no native mechanism scorer exists. Actual effect remains unknown.

**Decision:** park and close R17 after substantive attempt 3/3. Add zero active, scientifically admitted or selected candidates. Reopen only with genuinely new information or evidence: an author-visible deployed prefix law with calibrated one-sided coverage, a matched-total-cost advantage beyond direct dense gating and direct protected coordinates, and a native mechanism-identifying measurement. Changing rank, sketch size, threshold, confidence level or eigensolver is not a new repair.
