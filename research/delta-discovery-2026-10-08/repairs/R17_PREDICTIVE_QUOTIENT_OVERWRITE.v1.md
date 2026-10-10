# R17 v1 — predictive-quotient decodability after exact Delta overwrite

Status: **conditional theorem/control; parked after attempt 1, not an active D candidate**. This versioned child of `rejected/NOGO_CAP_02.md` and `repairs/R10_EQUAL_BIT_TRANSPORTED_RESIDUAL.v1.md` changes the retention target from the full old state to a declared future-behavior quotient. It proves the exact condition under which that old quotient remains decodable from the overwritten state, plus a quotient-level finite-bit lower bound. This does not by itself make the deployed update semantics preserving: identity on the predictive quotient additionally requires an actual decoder/subtraction contract or direct equality of the relevant pre/post behavior. General predictive-fiber, task-sufficient compression and conditional rate-distortion mechanisms are known; the remaining result is a concrete Delta specialization, not an established new architecture.

## 1. Formal object, original problem, and patch

Let `S in R^(d x m)` be key-by-value memory. At the current step, with unit key `k`, exact Delta overwrite after a fixed left transition `D` is

\[
S^+=(I-kk^\top)DS+kv^\top . \tag{1}
\]

The affine old-state map is

\[
A=(I-kk^\top)D. \tag{2}
\]

`NOGO_CAP_02` correctly proves that `A` is singular and, when `D` is invertible,

\[
\ker(A\cdot)=\mathcal N_k
=\{D^{-1}ka^\top:a\in\mathbb R^m\}. \tag{3}
\]

Without invertibility the exact kernel is still

\[
\mathcal N_k=\{E\in\mathbb R^{d\times m}:DE\text{ has every column in }\operatorname{span}(k)\}, \tag{4}
\]

which may also contain `ker D` directions. The old no-go asked to recover every old-state distinction. R17 instead declares a lawful future-observation operator

\[
\mathcal O(E)=\big(q_u^\top P_uE\big)_{u\in\mathcal U}, \tag{5}
\]

where `q_u` is the allowed future query and

\[
P_u=P_{u:t+1}=A_uA_{u-1}\cdots A_{t+1},
\qquad P_{t:t+1}=I. \tag{5a}
\]

Thus `P_u` is the fixed, correctly ordered suffix after the current write and excludes the current `D` in (1). Crucially, `O` describes the counterfactual old behavior of the state entering the overwrite. Defining it only on the already-overwritten state would make every direction in `ker A` invisible by construction and turn the safety test into a tautology. Equation (5) is a frozen affine reference. If future keys, gates, queries, retrieval or inputs respond to the edited state, the full nonlinear comparison or its local Jacobian is required; (5) is not a whole-network identity.

Two states are predictively equivalent for this declared family iff their difference lies in `ker O`. The patch asks only whether their old quotient remains decodable after exact overwrite. It does not prove that `T` acts as identity on the quotient, that the actual downstream path uses the factor decoder, that the intended new write has been subtracted, or that the declared old behavior is numerically unchanged. It also does not infer which facts remain valid, choose the future query family, or gain access to future tokens at deployment.

## 2. Exact quotient-decodability theorem

Let `T(S)=AS+kv^T` with fixed `k,v,D`. The overwritten state is sufficient to recover the declared old-state quotient—equivalently, no two predictively distinct old states are identified by the overwrite—iff

\[
\boxed{\ker(A\cdot)\subseteq\ker\mathcal O.} \tag{6}
\]

Proof. If (6) holds and `T(S_1)=T(S_2)`, then `A(S_1-S_2)=0`, hence `O(S_1-S_2)=0`; the two old states were already predictively equivalent. Conversely, if some `E in ker(A·)` has `O(E) != 0`, then `S` and `S+E` have different declared future behavior but `T(S)=T(S+E)`, so the quotient is not recoverable from the overwritten state. In finite dimensions the kernel inclusion is also equivalent to a linear factorization `O=H(A·)` for some decoder `H`. This is both necessary and sufficient for the fixed declared behavior to be recoverable after this write. It should not be confused with a recursively closed quotient state: iterating one quotient recurrence additionally requires `A ker(O) subseteq ker(O)` (or the corresponding time-varying congruence).

For invertible `D`, substitute (3) into (5). Because `a` is arbitrary, (6) is equivalent to

\[
\boxed{q_u^\top P_uD^{-1}k=0\quad\text{for every allowed }u.} \tag{7}
\]

This formula depends on the state domain used in (5). If the comparison object is the post-decay, pre-overwrite state `\bar S=DS`, then its erased subspace is `{ka^T}` and the natural no-current-write suffix operator is `q_u^T P_u \bar E`; the same theorem becomes

\[
q_u^\top P_uk=0\quad\forall u. \tag{8}
\]

Equations (7) and (8) are not interchangeable conventions: the `D^{-1}` appears only when `O` acts directly on the pre-decay state. If a pre-decay counterfactual includes the current decay inside its observation operator, `D` cancels and yields (8).

For nonnegative scalar weights `w_u`, let `U_+={u:w_u>0}`, let `O_+` be (5) restricted to `U_+`, and define the finite-horizon observability Gramian on that support,

\[
G=\sum_{u\in\mathcal U}w_uP_u^\top q_uq_u^\top P_u\succeq0. \tag{9}
\]

For a lost perturbation `E=D^{-1}ka^T`, its exact weighted squared output is

\[
\sum_uw_u\|q_u^\top P_uE\|_2^2
=\|a\|_2^2\,k^\top D^{-\top}GD^{-1}k. \tag{10}
\]

Thus, for the positive-weight read family,

\[
\boxed{k^\top D^{-\top}GD^{-1}k=0}
\quad\Longleftrightarrow\quad
\mathcal N_k\subseteq\ker\mathcal O_+. \tag{11}
\]

with the analogous `k^TGk=0` in the post-decay convention. To identify this with the original unweighted `O`, every declared read must have positive weight; a zero-weight read is outside `O_+` and cannot be certified by `G`. Positive semidefiniteness is essential: a zero quadratic form then means the direction lies in `ker G`. With value-space weights `W_u succeq 0`, define the weighted column operator `O_W(E)=(W_u^{1/2}E^TP_u^Tq_u)_u`; its full matrix Gram is `sum_u W_u otimes (P_u^Tq_uq_u^TP_u)`. Annihilation of every vectorized lost matrix is equivalent to decodability relative to `O_W`. Equivalence to the original unweighted value read requires each declared `W_u` to be positive definite, or positive definite on the value subspace being protected; merely nonzero singular `W_u` can hide output directions in its kernel. Restricted value perturbations may therefore be invisible even when the full lost value space is not. Equation (10) quantifies the exact visible loss in the common scalar-weight case; it is not merely a binary rank argument.

## 3. Old counterexamples and success cases

### Success case

Take `D=I` and a fixed suffix with every effective query `P_u^Tq_u` orthogonal to `k`. Exact overwrite removes `{ka^T}`, but (8) holds. The projector therefore leaves the old-state component of every declared linear read unchanged; the affine contribution of the intended new write must still be handled separately. This recovers the known orthogonal-protection special case and generalizes it only to an explicitly propagated finite query family.

### Minimal failure

Take `d=m=1`, `D=P=q=k=1`. The overwrite maps every old scalar state to `v`, while the declared future read is the old scalar itself. Here `G=1`, (10) is `a^2`, and two predictively distinct states are identified. Renaming full-state recovery as a quotient does not remove this counterexample.

Zero mean query is not a rescue. With `D=P=I`, `k=e_1`, and future query equally likely to be `+e_1` or `-e_1`, `E[q]=0` but `G=e_1e_1^T`; the erased direction remains fully visible in squared risk. Likewise, a query initially orthogonal to `k` can make the old quotient nondecodable when the transported covector `P_u^Tq_u` aligns with `D^-1k`.

### Partial overwrite

For unit `k` and `0<=beta<1`, the old-state factor `(I-beta kk^T)D` is invertible whenever `D` is invertible. There is then no exact algebraic lost subspace of the form (3); the issue becomes attenuation, conditioning and finite distortion rather than exact quotient identification. The R17 theorem is an exact-overwrite boundary, not a proof that softer gates preserve useful information well.

### Singular decay

If `D` is singular, checking only the `k` direction is insufficient. Every element of (4), including any additional decay kernel, must lie in `ker O`. A pseudoinverse expression alone would omit possible lost directions.

## 4. Conditional rate-distortion bound for the retained quotient

Now impose an explicit finite-state budget. Let finite or standard-Borel random variable `Q` denote the declared predictive quotient of the old history, `K` the side information legally available to both encoder and decoder, and `Z` the stored post-update code with at most `2^B` values. Let `Qhat=g(Z,K)` be the reconstructed quotient and `d(Q,Qhat)` a declared distortion. If `E[d(Q,Qhat)]<=delta`, then

\[
B\ge H(Z\mid K)\ge I(Q;Z\mid K)\ge I(Q;\widehat Q\mid K)
\ge R_{Q\mid K}(\delta), \tag{12}
\]

where

\[
R_{Q\mid K}(\delta)
=\inf_{p(\widehat q\mid q,k):\,\mathbb E d(Q,\widehat Q)\le\delta}
I(Q;\widehat Q\mid K). \tag{13}
\]

The first inequality uses the finite code cardinality; the middle inequality is conditional data processing. For a discrete quotient reproduced exactly,

\[
\boxed{B\ge H(Q\mid K).} \tag{14}
\]

For continuous `Q`, (14) is not a valid finite-bit zero-distortion claim in general; the rate-distortion object (13), or an explicit quantized quotient, must be used. With nonzero classification error, the earlier Fano form remains available after replacing the full old behavior class by the declared quotient alphabet.

This corrects the scope of the parent capacity statement. Predictively irrelevant old distinctions need not be encoded, but every retained quotient still has an information cost under an explicit source, decoder, side-information and distortion contract. Neither real-valued dimension alone nor an unnamed future-query distribution supplies this bound.

## 5. Equal-budget recheck and strongest simple alternative

Suppose a proposed split memory `(W,C)` is consumed only through a decoded quotient `Qhat=f(W,C,K)`, and all codebooks, scales, routing metadata and side information are charged equally. The pair has at most `2^(B_W+B_C)` states. Relabeling each pair by one direct code produces the same `Qhat` with `B_W+B_C` bits. Therefore R10's same-cardinality representation theorem survives unchanged on the quotient: a split representation has no information-theoretic advantage over the direct quotient code solely because it is split.

The strongest simple comparator is consequently a direct sufficient-coordinate or direct quotient encoder, plus ordinary Delta on whatever residual state remains. For the fixed linear operator (5), choose a matrix `B` whose columns span `{P_u^Tq_u:u in U}` and store `B^TS` (or store the stacked effective reads directly). Any more elaborate updater must show a matched-total-cost benefit beyond this direct representation. If future computation reads split components separately or changes its transition as a function of them, it is a different operator class and needs a new derivation rather than the quotient code claim.

## 6. Information, computation, predictions, and measurement boundary

The theorem itself needs a declared suffix family. Materializing a horizon-`H` Gramian costs `O(Hd^2)` naive work and `O(d^2)` state; checking individual effective queries can instead use suffix-vector products but still requires the future operator. A rank-`r` direct quotient stores `O(rm)` values plus `O(dr)` basis/metadata unless the basis is fixed or generated. Increasing the horizon adds PSD Gram terms and can only shrink its kernel, so decodability for one finite horizon does not imply it for a longer or unrestricted future.

State-dependent suffixes require the full joint state, update and readout map. Another state component may carry a direction erased from this memory block, or endogenous coefficients may amplify a direction that the frozen memory path misses. Globally, the exact condition is the set-theoretic factorization `T(s)=T(s') => F_future(s)=F_future(s')`. Locally, `ker J_T subseteq ker J_F` is necessary; sufficiency needs regularity and constancy on connected fibers, not a Jacobian kernel check alone. These analyses inherit the full-Jacobian, replay and approximation costs already recorded in the project.

Equality of the complete `O` output is sufficient for preserving any downstream loss that depends only on `O`, but it need not be necessary for a loss-only quotient because the loss may identify additional outputs. The PSD Gram above is exact for weighted squared output difference. A Hessian/GGN Gram for a nonlinear loss is only local and second order; a nonzero first-order term must still be retained, so it is not an exact global safety certificate.

Distinguishing predictions are conditional:

1. If (11) is exactly zero, perturbations inside the overwrite kernel cannot change any positive-weight declared frozen-path read; any measured difference on that family must come from an undeclared/zero-weight query, nonlinear/state-dependent path, numerical error or changed information.
2. If (11) is positive, there exists a lost value direction whose declared future output changes by exactly (10); no decoder using only the overwritten state can recover it without side information.
3. Changing the allowed future-query family can turn the same overwrite from quotient-decodable to nondecodable. This is expected target dependence, not evidence that the writer learned semantic validity.
4. At the same quotient, side information and total bit budget, a split code cannot beat the best direct code by representation cardinality alone.

bAbI and LAMBADA expose endpoint answers/tokens, not the frozen suffix operator, counterfactual pre-overwrite state, quotient class or `G`. RULER and LongMemEval expose broader long-context/query endpoints and LongMemEval supplies evidence annotations, but neither natively labels the exact Delta-erasure quotient or its conditional rate-distortion source. They can test downstream behavior after an implementation exists; they cannot by themselves verify (6), identify why a fact was forgotten, or separate a quotient benefit from extra retrieval/state. No native internal scorer was established, and no benchmark, label, metric or result is invented.

## 7. Nearest work and disposition

The mechanisms closest to this result are predictive fibers/quotients for recurrent states, task-sufficient or regret-profile compression, classical conditional rate-distortion and information bottleneck, predictive-state representations, and observable-preserving lumping. R01-v2, R12, R13 and `STEP2_OBSERVED_PREDICTIVE_TARGET.md` already record closely related quotient, sufficient-coordinate and functional-observer controls. R17's retained contribution is narrower: it explicitly identifies the exact Delta-overwrite kernel, maps it to a finite future-query Gramian, and shows precisely when the old quotient is still linearly decodable despite the state singularity. It does not promote recoverability to semantic identity preservation.

That diagnostic is useful for debugging an overly strong no-go, but it does not supply a causal query law, a deployed quotient decoder, revision-validity evidence, a cheap online quotient, an implementation advantage, or empirical effectiveness. If the source audit finds the full specialization already stated in primary work, even the theorem-level residual disappears.

**Decision:** park after substantive attempt 1. Add zero active, scientifically admitted, or selected candidates. Reopen only with a lawful prefix-only mechanism that identifies a small stable quotient, computes or certifies it below the cost of direct sufficient-coordinate storage, and yields a distinct matched-information prediction on a native measurable object. Changing the horizon, query weights, basis or distortion threshold alone is not a new repair.
