# Retroactive rollback Delta: exact restricted algebra and replay boundary

Disposition: **rejected as a distinct method; retained as a rollback trilemma/control**. This is mathematics and source analysis only. No project code, test, benchmark, download, model execution or GPU work was performed.

## Ordered affine object

For the repository's key-by-value convention,

\[
S_t=A_tS_{t-1}+B_t,\qquad
A_t=(I-\beta_tk_tk_t^\top)D_t,\qquad
B_t=\beta_tk_tv_t^\top .
\]

For \(b\ge a\), define \(P_{b:a}=A_b\cdots A_a\) and

\[
Q_{b:a}=\sum_{j=a}^b A_b\cdots A_{j+1}B_j.
\]

Then \(S_b=P_{b:a}S_{a-1}+Q_{b:a}\). Interval summaries form the ordered affine monoid

\[
(P_R,Q_R)\circ(P_L,Q_L)
=(P_RP_L,\;P_RQ_L+Q_R).
\]

This gives three different operations which must not be conflated:

1. Removing only \(B_\tau\) under a frozen suffix gives
   \(S_T^{-B_\tau}=S_T-P_{T:\tau+1}B_\tau\).
2. Replacing only the value gives
   \(S_T'-S_T=P_{T:\tau+1}\beta_\tau k_\tau(v_\tau'-v_\tau)^\top\).
3. Deleting the complete transaction, hence replacing \((A_\tau,B_\tau)\) by \((I,0)\), gives

\[
S_T^{-\tau}=S_T-P_{T:\tau+1}R_\tau,
\qquad
R_\tau=S_\tau-S_{\tau-1}.
\]

The third identity is exact only if every later affine map stays fixed. It needs the realized event receipt or the pre-event state, plus the ordered suffix.

## Native causal omission

If removing event \(\tau\) changes later hidden features, later maps also change. For two paths

\[
S_t^\pm=A_t^\pm S_{t-1}^\pm+B_t^\pm,
\]

the difference obeys

\[
\Delta_t=A_t^+\Delta_{t-1}+F_t,
\qquad
F_t=(A_t^+-A_t^-)S_{t-1}^-+(B_t^+-B_t^-).
\]

Hence

\[
\Delta_T=P^+_{T:\tau+1}\Delta_\tau
+\sum_{s=\tau+1}^T P^+_{T:s+1}F_s.
\]

Transporting the old receipt alone is exact iff the forcing sum vanishes. In a state-dependent network this generally requires checkpoint-and-replay; a Jacobian transport is only a local influence approximation. This formula directly collides with *Exact Record Omission in Delta Attention: A Transport Criterion, Its Cost, and a Replay Certificate*, arXiv:2609.06872v3, Theorem 1 and §§VI-D/G/J: https://arxiv.org/abs/2609.06872 .

## Inversion is neither deletion nor numerically safe

The transition is invertible only if

\[
\det D_t\ne0,
\qquad
1-\beta_t\|k_t\|^2\ne0.
\]

Then

\[
A_t^{-1}=D_t^{-1}
\left(I+{\beta_t\over1-\beta_t\|k_t\|^2}k_tk_t^\top\right).
\]

For unit \(k\), the exact overwrite \(\beta=1\) is singular and \(\kappa_2(I-\beta kk^\top)=1/(1-\beta)\) for \(0\le\beta<1\). Applying an old inverse to the present is also not middle deletion because the maps do not commute. Chronological deletion must undo the suffix, skip the selected event, then replay the suffix.

## Finite-precision information lower bound

Even scalar addition shows why arbitrary stable-ID rollback needs history. Let

\[
S_t=S_{t-1}+b_t,\qquad b_t\in\{0,1\}.
\]

If current state plus a compressed receipt \(C\) can answer deletion of every event ID \(i\), then

\[
b_i=S_T-S_T^{-i}.
\]

All \(T\) bits can be reconstructed from the deletion oracle. Since \(S_T\) has only \(T+1\) values, \(C\) requires at least \(T-\log_2(T+1)\) bits in the worst case. This is explicitly a finite-precision/robust-storage statement, not a claim about ideal real numbers.

## Implementable controls and costs

- **Checkpoint and replay:** retain event identity, raw input or \((k,v,\beta,D)\), model/config/RNG provenance, and periodic full states. Exact deterministic semantics cost replay from the preceding checkpoint.
- **Affine segment tree:** store \((P,Q)\) at each node and replace a deleted leaf by \((I,0)\). It gives logarithmic node recompositions only when later leaves remain valid, with dense \(O(T(d_k^2+d_kd_v))\) storage and expensive dense merges.
- **Per-event transported trace:** update one state-sized receipt for each rollbackable event; exact frozen-path rollback costs state proportional to the number of named events.
- **RLS/QR downdate:** valid for an order-independent least-squares objective, not for a generic order-dependent Delta recurrence; it still needs the deleted payload and becomes ill-conditioned at the downdate boundary.

The 2026 record-omission paper already contains the Delta-specific transport criterion, replay certificate and deployment cost trade-off. Generic retroactive sequence composition is classical: Demaine, Iacono and Langerman, *Retroactive Data Structures*, ACM TALG 3(2), 2007, DOI 10.1145/1240233.1240236. Reversible recurrent computation likewise retains lost information; it does not provide arbitrary history-free deletion.

## Semantic and measurement boundary

Frozen-trace omission, native model replay, causal regeneration of outputs/actions, and semantic deletion of paraphrases or consequences are different objects. Only the first has the simple receipt formula. Stable event identity and provenance are extra information, not something inferred from the compressed current state.

bAbI, LAMBADA and ordinary language-model accuracy contain no native deletion request or replay-defined reference state. Model-editing benchmarks measure behavioral efficacy/locality, not exact recurrent-state equality. No native benchmark suitable for this algebraic claim was established; do not manufacture one.

**Ruling:** exact fixed-trace rollback is known affine transport; exact state-dependent rollback is replay. Under finite precision, arbitrary named deletion, noninvertible/state-dependent ordered writes and constant latent state cannot all be retained. No D-number is assigned.
