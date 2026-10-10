# R13 — Dynamic covector transport for protected Delta readouts (attempt 1)

## Status and lineage

- Parent: `STEP2_COUPLED_UPDATER_STABILITY.md`, especially the open boundary for dynamic protected readouts `L_t`.
- Retained parent result: fixed-readout protection requires neutral retained coordinates; strict whole-state contraction cannot preserve every nonzero protected distinction. The parent explicitly did not certify rotating, transported, or released protection spaces.
- Failure type repaired: **insufficient structural assumptions plus target mismatch**. A fixed `L` was used to discuss a time-varying ordered recurrence. R13 instead asks when an affine protected observable can be transported exactly through the realized Delta transition.
- Patch: derive a necessary-and-sufficient row-space condition, the complete decoder family, the exact-overwrite obstruction, a near-overwrite conditioning law, and the extra state needed to cancel the affine write.
- Outcome: conditional theorem/control. The algebra is a Delta specialization of classical linear-system observability, generalized inverses, adjoint transport, and reversible-recurrence limits. It does not identify which memories deserve protection or establish a new updater. Park after attempt 1 unless a native workload supplies causal protected covectors and a same-budget advantage over replay/direct ledgers.

## 1. Formal object

Let the key-by-value memory obey the realized affine transition

\[
S_t=A_tS_{t-1}+B_t,
\qquad S_t\in\mathbb R^{d_k\times d_v},
\tag{1}
\]

with a declared protected covector matrix `Q_{t-1}\in\mathbb R^{d_k\times p}`. The old protected numerical readout is `Q_{t-1}^\top S_{t-1}`. We allow the future reader to use a transported covector `Q_t` and an affine offset `C_t\in\mathbb R^{p\times d_v}`:

\[
Y_t=Q_t^\top S_t+C_t. \tag{2}
\]

The pathwise protection question is whether, for every possible `S_{t-1}` in the declared linear state space,

\[
Q_t^\top S_t+C_t
=Q_{t-1}^\top S_{t-1}+C_{t-1}. \tag{3}
\]

The same `A_t,B_t` are held fixed across the state alternatives quantified in (3), and must be known from causal, already realized quantities. This is exact for exogenous/frozen coefficients. If keys, gates, values, or updater state depend on `S_{t-1}`, the full recurrence is not one global affine map over those alternatives and only the local Jacobian statement in section 6 applies. Equation (3) is required over the full declared linear state space; a smaller known reachable affine subspace can weaken the kernel condition below by restricting the admissible state differences. It is numerical equality along this affine interface, not a statement that the protected fact remains true, that the model's nonlinear query generator will emit `Q_t`, or that a counterfactual deletion leaves future features unchanged.

## 2. One-step exact transport theorem

Substituting (1) into (3) and matching the coefficient of arbitrary `S_{t-1}` gives

\[
Q_t^\top A_t=Q_{t-1}^\top, \qquad
C_t=C_{t-1}-Q_t^\top B_t. \tag{4}
\]

Therefore exact affine transport exists if and only if

\[
\ker A_t\subseteq\ker Q_{t-1}^\top,
\tag{5}
\]

equivalently `row(Q_{t-1}^T)\subseteq row(A_t)`. When (5) holds, every solution is

\[
Q_t^\top
=Q_{t-1}^\top A_t^\dagger
+Z_t(I-A_tA_t^\dagger), \tag{6}
\]

for arbitrary `Z_t\in\mathbb R^{p\times d_k}`, followed by the offset update in (4). Necessity follows because any state perturbation in `ker A_t` disappears from `S_t` and hence cannot remain visible to any later linear readout. Sufficiency follows from the generalized-inverse identity `Q_{t-1}^T=Q_{t-1}^TA_t^\dagger A_t` under (5). The term in `Z_t` spans the left nullspace freedom and vanishes after multiplication by `A_t`.

The minimum-Frobenius-norm transported covector is `Q_{t-1}^TA_t^\dagger`. Thus exact transport through a poorly conditioned retained singular direction necessarily magnifies the reader. If `A_t=U_r\Sigma_rV_r^T` and a row component of `Q_{t-1}^T` along `v_i^T` has magnitude `a_i`, the corresponding minimum-norm coefficient in `Q_t^T` has magnitude `|a_i|/\sigma_i`. This is an exact conditioning cost, not merely an upper bound.

For a horizon product `P_{T:1}=A_T\cdots A_1`, final-time recovery of the initial protected readout with one offset exists iff

\[
\ker P_{T:1}\subseteq\ker Q_0^\top. \tag{7}
\]

Condition (7) also guarantees that an algebraic intermediate-reader sequence exists *ex post*: after selecting a final decoder `Q_T`, define `Q_t^T=Q_T^TA_T\cdots A_{t+1}`. Then `Q_t^TA_t=Q_{t-1}^T`. What (7) does not provide is a bounded-norm decoder sequence or an online causal construction: a forward procedure may need future-aware choices among the nullspace freedoms in (6), and near-singular factorizations can make intermediate readers ill-conditioned.

## 3. Delta specialization and exact-overwrite boundary

For the ordered Delta transition

\[
A_t=(I-\beta_tk_tk_t^\top)D_t,
\qquad B_t=\beta_tk_tv_t^\top, \tag{8}
\]

assume in this section that `D_t` is invertible. Put

\[
\delta_t=1-\beta_t\lVert k_t\rVert_2^2. \tag{9}
\]

If `\delta_t\ne0`, `A_t` is invertible and the transported covector is unique:

\[
Q_t^\top
=Q_{t-1}^\top D_t^{-1}
\left(I+{\beta_t\over\delta_t}k_tk_t^\top\right). \tag{10}
\]

The component `Q_{t-1}^TD_t^{-1}k_t` is amplified by `1/|\delta_t|`. Orthogonality to that component removes this particular near-overwrite pole, but transport can still be ill-conditioned through `D_t^{-1}`; total sensitivity is governed by the singular spectrum of `A_t`, not `\delta_t` alone.

At exact overwrite `\delta_t=0`,

\[
\ker A_t=\operatorname{span}(D_t^{-1}k_t), \tag{11}
\]

so exact transport exists precisely when

\[
Q_{t-1}^\top D_t^{-1}k_t=0. \tag{12}
\]

If (12) fails, choose a state difference `\Delta S_{t-1}=D_t^{-1}k_t w^T`. The two old states have different protected outputs but map to the same post-transition state under the same `(A_t,B_t)`. No later reader, checksum, updater state that did not already store this difference, or fresh internal randomness can recover it when subsequent exogenous observations are held fixed. New external evidence correlated with the erased distinction changes the information set and is outside this impossibility claim.

The offset in (4) cancels the known numerical write:

\[
C_t=C_{t-1}-\beta_t(Q_t^\top k_t)v_t^\top. \tag{13}
\]

It costs `p d_v` persistent scalars for `p` protected outputs unless recomputed from a retained event ledger. The offset is not free semantic evidence; it merely subtracts a known affine contribution.

## 4. Offset-free protection is strictly narrower

If the deployed interface permits only a raw readout `Q_t^TS_t` and no offset, (4) additionally requires

\[
Q_t^\top B_t=0. \tag{14}
\]

For `\beta_t>0` and nonzero `v_t`, this is `Q_t^Tk_t=0`. Under (8) with invertible `D_t`, (10) gives

\[
Q_t^\top k_t
=\delta_t^{-1}Q_{t-1}^\top D_t^{-1}k_t. \tag{15}
\]

Therefore, under this section's assumptions `D_t` invertible, `\beta_t>0`, and `v_t\ne0`, an offset-free exact transported readout exists iff (12) holds, even when `A_t` itself is invertible. In that case the unique admissible protected covector is simply

\[
Q_t^\top=Q_{t-1}^\top D_t^{-1}. \tag{16}
\]

Equation (15) proves this when `\delta_t\ne0`. At `\delta_t=0`, condition (12) makes the full solution family `Q_t^T=Q_{t-1}^TD_t^{-1}+a_tk_t^T` with `a_t\in\mathbb R^p`; imposing `Q_t^Tk_t=0` forces `a_t=0` because `k_t\ne0`. Thus (16) also holds at the singular endpoint.

Thus invertibility of the state transition is not enough for a raw protected readout: the current write contaminates it unless the protected direction is orthogonal to the write key after undoing decay. An affine ledger can remove contamination when the old component was not destroyed; it cannot undo the singular loss in (11).

## 5. Noise, approximate transport, and a sharp local test

Suppose the observed post-state is `\widetilde S_t=S_t+N_t` and the offset has error `E_t`. Any exact transported reader incurs

\[
\widetilde Y_t-Y_{t-1}=Q_t^\top N_t+E_t, \qquad
\lVert\widetilde Y_t-Y_{t-1}\rVert_F
\le\lVert Q_t\rVert_2\lVert N_t\rVert_F+\lVert E_t\rVert_F. \tag{17}
\]

For an impossible old covector, the best one-step linear approximation solves

\[
\min_X\lVert XA_t-Q_{t-1}^\top\rVert_F,
\tag{18}
\]

whose minimum is

\[
\lVert Q_{t-1}^\top(I-A_t^\dagger A_t)\rVert_F. \tag{19}
\]

Equation (19) is the exact Euclidean Frobenius row-space residual in the chosen coordinates. It is zero exactly under (5), but by itself is neither semantic information loss nor expected downstream harm and changes under rescaling. Regularizing the inverse can trade reader norm against this residual, but that is ordinary Tikhonov/truncated-SVD estimation and must be compared with the same-budget direct ledger or replay.

## 6. Full-network and coupled-updater boundary

For a differentiable complete recurrent state `z_t=F_t(z_{t-1})`, the first-order tangent obeys the homogeneous equation `\delta z_t=J_t\delta z_{t-1}`. Replacing `A_t` by the full Jacobian `J_t` in the homogeneous parts of (4)--(7) gives the exact covector-transport condition for differentials at the realized point and only a first-order statement for finite perturbations; the affine offset ledger (4) does not arise from this Jacobian-only tangent recurrence. Conventional VJP/adjoint propagation maps a future covector backward as `Q_{t-1}=J_t^TQ_t`; R13 instead starts with the old covector and must solve the inverse/least-squares problem `J_t^TQ_t=Q_{t-1}`, which a VJP does not provide for free. Using only the memory block while keys, gates, queries or updater state depend on memory omits cross-block terms and does not certify the full model.

This is a local pathwise statement. Removing or changing a write can change later `J_t`; exact finite counterfactual protection then needs replay or a complete shadow trajectory. A transported numerical covector also does not prove that the model's endogenous query network can generate it within the same information and compute budget.

## 7. Old counterexamples, predictions, and failure boundary

The parent's semantic counterexamples survive. Two worlds can share identical `S,A,B,Q,C` while differing in whether the protected association is still valid. R13 preserves whichever numerical functional was declared; it cannot decide whether to retain or release it.

Conditional predictions:

1. Exact affine readout preservation succeeds exactly under (5), with the decoder family (6).
2. A Delta overwrite destroys every protected component with nonzero overlap (12); two old states differing only in that component become indistinguishable after one step.
3. Before overwrite, transported-reader norm and finite-precision sensitivity scale as `1/|\delta_t|` for the overlapping component.
4. Removing the offset causes an additional, exact orthogonality requirement (12), not merely a softer numerical penalty.

Falsifiers and stop conditions:

- Recovery of an old component outside `row(A_t)` from no retained side information would refute the linear-algebra claim.
- A claimed protection gain that uses stored offsets, old states, raw events, future queries, more precision, or replay must charge the same information and cost to controls.
- Endpoint QA alone cannot establish (5), conditioning, or semantic correctness without the internal transition/readout records.

## 8. Same-information controls, costs, and measurement

- **Direct protected-value ledger:** if the sole target is to retain the already-declared numerical matrix `Y_{t-1}`, carry that matrix unchanged in `p d_v` side scalars. This is functionally complete for R13's current endpoint and is cheaper and more stable than persisting both `Q_t` and `C_t`; no additional same-budget downstream operation has been established for the transported representation.
- **Replay/checkpoint:** retain events and checkpoints, then recompute the actual nonlinear path. It targets finite counterfactual behavior rather than a pathwise linear observable, but it is a fair comparator only after matching retained events, precision, storage, latency, and future-feature access.
- **Adjoint/JVP-VJP:** transport a loss covector backward for sensitivity or compute a local VJP. This is established and targets gradients, not a persistent protected semantic object.
- **Projection/ridge protection:** constrain the write so that a fixed query is not changed. This alters the update and may make a desired correction infeasible; R13 instead diagnoses whether a realized transition permits the reader itself to move.
- **Reversible recurrence with retained bits:** prevents information destruction by changing the architecture and paying side storage. It is an appropriate comparator near singular forgetting only when bit precision, retained side state, latency, and access are explicitly matched.

Persisting R13 directly costs `p d_k` scalars for `Q_t` plus `p d_v` for `C_t`; recomputing them instead must charge `Q_0`, all needed transitions/events, history storage, and latency. Dense inversion is `O(d_k^3)` if recomputed. With dense `D_t^{-1}`, applying the explicit rank-one formula to `p` covectors is `O(pd_k^2)` naively; when `D_t` is diagonal or scalar it falls to `O(pd_k)` plus elementwise scaling and inner products. Maintaining a changing dense inverse by Sherman--Morrison is `O(d_k^2)` once the base inverse is available. Offsets cost `O(pd_v)` per rank-one update after `Q_t^Tk_t` is known. Under ordinary floating-point representation and a fixed absolute preservation tolerance, near-singular equal-bit accounting must also charge mantissa precision growing logarithmically with the amplification factor, including `1/|\delta_t|` and ill-conditioning in `D_t`; this is not an unconditional lower bound under arbitrary rescaling or symbolic representation. Full-Jacobian transport cannot generally form a dense inverse; iterative solves/JVPs still require conditioning and convergence evidence.

LongMemEval's `knowledge-update` QA can measure final answer behavior, but its native scorer does not expose `A_t`, `Q_t`, singular values, offset ledgers, or paired pre/post state equality. Analytic trace instrumentation could check R13's premises but would not itself be a native efficacy score. bAbI and LAMBADA likewise do not natively score this internal certificate. No benchmark, label, case, metric, code, test, model run, training, inference, download or GPU job is created here.

## 9. Decision

R13 repairs the fixed-protection target mismatch by deriving the exact moving-reader certificate. The useful result is a trilemma: a protected component crossing a singular overwrite must either be orthogonal to the erased direction, be retained in side information before erasure, or be lost; before singularity, exact transport can require arbitrarily large reader norm. An affine offset cancels known write contamination but costs the same order of state as directly carrying the protected output.

This is generic row-space/generalized-inverse mathematics and classical functional-observer/adjoint/reversibility territory. It is a sharper Delta control, not an admitted new method. For the declared fixed numerical invariant, a direct `p d_v` value ledger strictly dominates persisting `Q_t,C_t`; no method-level residual remains. Park after attempt 1. Reopen only if a causal selector for the initial protected object and its validity exists, a downstream operation unavailable to the cheaper direct ledger is formalized, the transported representation wins under matched state/precision/compute/access, and a native endpoint can distinguish the claimed benefit.
