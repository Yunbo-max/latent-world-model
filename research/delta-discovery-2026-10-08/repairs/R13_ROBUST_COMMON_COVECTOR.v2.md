# R13 — Robust common-covector transport under transition uncertainty (attempt 2)

## Status and lineage

- Parent: `R13_DYNAMIC_COVECTOR_PROTECTION.v1.md` (exact transport through one known realized affine step).
- Preserved v1 result: for `S^+=AS+B`, an affine decoder of `Q^T S` exists exactly when `ker A subseteq ker Q^T`; the minimum-norm decoder is generalized-inverse transport, exact overwrite can destroy an overlapping component, and a direct protected-value ledger dominates the declared fixed numerical endpoint.
- New failure type: **insufficient information about the realized transition**. Every candidate transition may be individually invertible while no single decoder works without knowing which transition occurred.
- Patch: quantify over an admissible family of affine maps, derive the exact simultaneous-factorization condition, then audit arbitrary nonlinear and set-valued decoders through an indistinguishability lower bound.
- Outcome: conditional theorem/control and bounded non-repairability result. It does not create a new updater or identify which fact remains valid. Park after attempt 2.

## 1. Formal object and information restriction

Let `S in R^{d_k x d_v}` and let an unobserved mode `i in {1,...,m}` select

\[
Z=A_iS+B_i,\qquad A_i\in\mathbb R^{d_k\times d_k},\quad
B_i\in\mathbb R^{d_k\times d_v}. \tag{1}
\]

The decoder observes `Z` and the admissible family `U={(A_i,B_i)}`, but not the realized mode. In ordinary Delta execution the realized key, gate, decay and value are normally causally present when the update is made; hiding the mode is therefore an explicit downstream retention/interface restriction, not a generic property of Delta. The protected old value is

\[
T(S)=Q^\top S+C_0,\qquad Q\in\mathbb R^{d_k\times p},\quad
C_0\in\mathbb R^{p\times d_v}. \tag{2}
\]

We first ask whether one affine, mode-blind decoder `g(Z)=XZ+C`, `X in R^{p x d_k}`, preserves (2) for every state and every admissible mode. This differs materially from v1: allowing `X_i,C_i` after revealing `i` gives the separate v1 problems and changes the information set.

For an infinite family whose actual affine hull is exactly known and finitely generated, the same analysis applies to one reference plus a basis of its differences. Using a larger containing span gives only a sufficient, potentially overconservative certificate. The finite presentation below is not a distributional guarantee.

## 2. Exact common-decoder theorem

Exact preservation requires

\[
X(A_iS+B_i)+C=Q^\top S+C_0
\quad\text{for every }S\text{ and }i. \tag{3}
\]

Matching the state coefficient and affine term gives

\[
XA_i=Q^\top\quad(i=1,\ldots,m),\qquad
X(B_i-B_1)=0\quad(i=2,\ldots,m),\qquad
C=C_0-XB_1. \tag{4}
\]

Define the horizontal block matrices

\[
\mathcal M=[A_1\;A_2\;\cdots\;A_m\;B_2-B_1\;\cdots\;B_m-B_1], \tag{5}
\]

\[
\mathcal N=[Q^\top\;Q^\top\;\cdots\;Q^\top\;0\;\cdots\;0]. \tag{6}
\]

The block widths in (5)--(6) are respectively `m` copies of `d_k` and `m-1` copies of `d_v`. Equation (4) is exactly

\[
X\mathcal M=\mathcal N. \tag{7}
\]

Hence a mode-blind exact affine decoder exists if and only if

\[
\ker\mathcal M\subseteq\ker\mathcal N, \tag{8}
\]

equivalently `row(N) subseteq row(M)`. When (8) holds, all common decoders are

\[
X=\mathcal N\mathcal M^\dagger+W(I-\mathcal M\mathcal M^\dagger), \tag{9}
\]

with arbitrary `W in R^{p x d_k}`, followed by the offset in (4). Necessity follows because every vector relation annihilated by `M` must also be annihilated by `N`; sufficiency follows from `N=N M^dagger M`. Equation (9) is the complete left-factor family.

For a nontrivial family this condition can be strictly stronger than applying v1 separately. Even if all `A_i` are invertible, (4) forces

\[
Q^\top A_i^{-1}=Q^\top A_j^{-1}\quad\text{for all }i,j, \tag{10}
\]

as well as common cancellation of the affine differences. Revealing the mode removes (10), but the mode label and its causal reliability must then be charged.

## 3. Delta counterexample without singular overwrite

Take `d_k=2`, `d_v=p=1`, `D=I`, `C_0=0`, `B_1=B_2=0`, gate `beta=1/2`, and two lawful unit keys `k_1=e_1`, `k_2=e_2`. The zero affine writes are realized by zero value vectors. Then

\[
A_1=I-\tfrac12 e_1e_1^\top=\operatorname{diag}(1/2,1),\qquad
A_2=I-\tfrac12 e_2e_2^\top=\operatorname{diag}(1,1/2). \tag{11}
\]

Both transitions are invertible and therefore each admits exact v1 transport. For `Q=(1,1)^T`, however, their unique transported rows are

\[
Q^\top A_1^{-1}=(2,1),\qquad Q^\top A_2^{-1}=(1,2), \tag{12}
\]

so no common decoder exists. This failure is caused by hidden transition identity, not erasure or numerical singularity.

The same post-state `z=(1,0)^T` is compatible with `S_1=A_1^{-1}z=(2,0)^T` and `S_2=A_2^{-1}z=(1,0)^T`. The protected old values are respectively `2` and `1`. The impossibility applies when both triples are reachable under the same retained decoder information; if their histories expose different lawful side information, that information must be included in the decoder input and costed. Under the declared mode-hidden interface, post-state and family alone do not determine the target.

## 4. Nonlinear and set-valued ambiguity lower bound

Let

\[
\mathcal C(z)=\{Q^\top S+C_0:\exists i,\ z=A_iS+B_i\} \tag{13}
\]

be the exact set of protected values compatible with an observed post-state. For any deterministic point decoder `g(z)` and any norm, if `t_1,t_2 in C(z)`, the triangle inequality gives

\[
\max\{\|g(z)-t_1\|,\|g(z)-t_2\|\}
\ge \tfrac12\|t_1-t_2\|. \tag{14}
\]

Therefore the minimax point-error radius is at least half the diameter of `C(z)`. Randomization cannot improve this worst-case expected-norm bound: apply the triangle inequality pointwise to the randomized output and take expectations. In the two-key example, every mode-blind point decoder has worst-case absolute error at least `1/2` at `z=(1,0)^T`.

Returning `C(z)` itself is an honest set-membership answer, but it preserves uncertainty rather than the old value; its representation and propagation cost must be counted. If a probability law over modes/states is supplied, `E||T||_F^2<infinity`, and squared loss replaces exact protection, the Bayes-optimal measurable square-integrable decoder is `E[T|Z]` and the minimum risk is

\[
\mathbb E\|T-\mathbb E[T\mid Z]\|_F^2
=\mathbb E\,\operatorname{tr}\operatorname{Cov}(\operatorname{vec}T\mid Z). \tag{15}
\]

This is a distribution-dependent estimation problem, not a repair of the exact invariant. Extra observations that identify the mode can reduce (13) or (15), but they change the visible information and must be matched in controls.

## 5. Old counterexample recheck and preserved conclusions

The v1 exact-overwrite counterexample remains valid mode by mode: if an `A_i` erases a direction seen by `Q^T`, not even a revealed mode can recover it without side information. The v2 counterexample is stronger in a different axis: every `A_i` in (11) is invertible, yet hiding which lawful Delta key was used makes the target unidentifiable from the post-state.

The v1 conditioning law also survives. If a common decoder exists near overwrite, its norm is at least the maximum of the mode-specific minimum norm needed along every retained protected component. Transition uncertainty can add inconsistency on top of this conditioning cost; it cannot remove the pole.

Neither theorem identifies semantic validity. Two worlds may have identical `Z,U,Q` and different truth about whether the protected association should still be used. Mode inference and fact-validity inference are separate obligations.

## 6. Construction, predictions, and failure boundary

The only exact construction supported by the theorem is a **certificate/control**:

1. form a finite generator family for the causally available transition uncertainty;
2. build `(M,N)` from (5)--(6);
3. test the algebraic row-space condition; in floating point, report the rank threshold, scaling, conditioning, and residual `||N(I-M^dagger M)||_F` as an approximate diagnostic rather than treating tolerance-zero as an exact proof;
4. when the exact condition holds, use the unique minimum-Frobenius-norm coefficient matrix `X=N M^dagger` and the offset in (4); this does not minimize a joint norm of `(X,C)` because `C=C_0-XB_1`;
5. when it fails, conclude only that no common affine decoder exists. Exact point recovery by an arbitrary decoder is ruled out exactly when some same-information reachable `C(z)` has positive diameter; otherwise a nonlinear piecewise decoder may still exist.

Distinguishing predictions:

- Individual invertibility is insufficient for common exact affine transport; the binary affine-feasibility property can be destroyed by an arbitrarily small family perturbation, although the residual itself need not be discontinuous away from rank changes.
- Revealing a correct mode label that determines the full `(A_i,B_i)` at the required time and precision reduces the problem to v1 and removes the two-key ambiguity, while an equally sized label independent of the mode does not; label acquisition, storage and reliability are charged.
- At fixed post-state, every mode-blind decoder has worst-case expected-norm error at least half the diameter of the same-information reachable set (13), not merely a penalty governed by one `A_i`'s condition number.
- A direct pre-update protected-value ledger remains exact across all modes and is unaffected by (8).

Falsifiers/boundaries:

- A mode-blind decoder that exactly recovers both targets in the same-post-state pair of section 3 would refute (14).
- If the realized transition is already causally observed, v2's uncertainty premise is false and only v1 applies.
- If the reachable state set is restricted, replace arbitrary `S` differences by the certified same-information reachable set; algebraically colliding histories that expose different retained information do not establish operational impossibility, and the full-space affine condition can be sufficient but not necessary.
- Approximate family generators, learned mode posteriors, and floating-point rank tests add estimation/numerical error; none is certified by the exact theorem.

## 7. Information, state, computation, and strongest controls

- **Direct protected-value ledger:** carry `T(S)` recurrently before the transition in `p d_v` scalars, charging its pre-read compute, precision and horizon. For this single fixed target it succeeds for every mode without identifying it. Persisting both changing `X` and unconstrained `C` costs `p d_k+p d_v` scalars and is larger. A decoder static or recomputed from already available family data has different amortization; when the offset is zero or cheaply recomputed, storing `X` alone costs `p d_k` and can be smaller if `d_k<d_v`. There is no unconditional state-cost dominance, and the comparison does not extend for free to a changing family of targets. The ledger remains the mandatory exact simple control.
- **Mode label plus v1 decoder:** costs the causal mode evidence/label and a way to compute or retain the relevant mode-specific decoder. It still fails for a singular mode violating v1's kernel condition.
- **Replay/checkpoint:** retains enough events/state to reconstruct the realized nonlinear path. Match event storage, precision, latency, and access.
- **Set-membership observer:** propagates the full compatible set under bounded uncertainty. It is the direct known-mechanism family for (13), with representation growth/outer-approximation costs.
- **Bayes estimator:** with a lawful prior and matched observations, compare the conditional mean and its irreducible conditional variance rather than claiming exact preservation.

Put `n=m d_k+(m-1)d_v`, so `M in R^{d_k x n}` and normally `n>=d_k`. A dense SVD-based pseudoinverse costs `O(d_k^2 n)` time and `O(d_k n)` working storage (cubic only when `n=Theta(d_k)`); iterative/rank-revealing alternatives retain conditioning and tolerance obligations. Explicitly retaining the finite family itself costs roughly `m(d_k^2+d_k d_v)` scalars unless it is generated from already available lower-dimensional causal data. A large uncertainty family can make certification and set propagation much more expensive than carrying the target. No state, compute, information, or precision advantage over the direct ledger has been established for the scoped setting.

## 8. Closest work and measurement

Common/unknown-input functional observers already study estimation of selected state functions across multiple or switching systems. Simultaneous matrix-equation and generalized-inverse literature covers common solutions. Set-membership filters propagate feasible state sets under bounded model/noise uncertainty. R13 v2 contributes only an explicit one-step block-kernel reduction and invertible two-key Delta counterexample inside this established territory; a bounded search does not support method-level originality.

LongMemEval `knowledge-update`, bAbI, and LAMBADA score endpoint answers, not hidden transition-mode identity, `(M,N)`, compatible-target diameter, or a protected-value ledger. Internal instrumentation could audit the theorem's premises but is not a native efficacy metric. No suitable existing native measurement object for the central internal certificate was located in this bounded repair, so method investment remains blocked.

## 9. Decision

R13 v2 changes the information condition and produces a real theorem: uncertainty over which invertible Delta step occurred can make the old protected value unidentifiable even though each step separately supports exact transport. The repair does not rescue the method. A direct ledger remains an exact control and is cheaper whenever a free offset is unavailable; the offset-free `d_k<d_v` regime is a real exception to that cost ordering, but the resulting common decoder still lies in known common-observer/simultaneous-equation territory and no native endpoint isolates the certificate.

Mathematics: conditionally accepted pending independent final-byte review. Contribution: useful Delta-specialized non-identifiability/control boundary; originality not established. Empirical effect: unknown. Candidate delta: zero. Park after attempt 2; no code or experiment is authorized or run.
