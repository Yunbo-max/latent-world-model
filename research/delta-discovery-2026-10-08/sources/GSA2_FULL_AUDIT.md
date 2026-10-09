# Gated Slot Attention-2 primary-formula exclusion audit

Read scope: Li et al., *Gated Slot Attention-2: Two-Sided Associative Memory Correction in Linear Attention*, arXiv:2610.02816v1, submitted 2026-10-02; full HTML §§2--4 and Appendices A.1--A.2.  No author-designated source repository is linked by the arXiv record, so no code interface is claimed inspected.

## Exact mechanism

GSA2 closes a broad route that might otherwise be miscounted as a new Delta idea: “correct the key side as well as the value side using shared slots.”  Under the paper's value-by-key orientation, ordinary Delta minimizes

\[
\tfrac12\|v_t-Sk_t\|^2
\]

and performs value-side correction.  The complementary Oja update minimizes

\[
\tfrac12\|k_t-S^\top v_t\|^2
\]

with

\[
S_t=(I-\beta_tv_tv_t^\top)S_{t-1}+\beta_tv_tk_t^\top.
\]

OJA2 adds ordered channel decay and decoupled erase/write gates:

\[
S_t=
\left(I-v_t(b_t\odot v_t)^\top\right)
\operatorname{Diag}(\alpha_t)S_{t-1}
+v_t(c_t\odot k_t)^\top.
\]

GSA2 maintains a key-to-slot state \(S_t^{(1)}\in\mathbb R^{M\times D_k}\) and slot-to-value state \(S_t^{(2)}\in\mathbb R^{D_v\times M}\).  The shared slot vector \(w_t\) is the value/address connecting them: OJA2 corrects key-to-slot associations, while Gated Delta Rule-2 corrects slot-to-value associations.  The readout is a two-stage nonlinear map through the shared slots.  The paper derives WY/UT-style chunk accumulation for the ordered diagonal-plus-rank-one transitions.

## Collision consequences for this discovery batch

The following cannot receive a new D-number without a substantive residual beyond GSA2:

1. factorizing one key-value memory into key-slot and slot-value matrices;
2. applying a reverse/value-to-key Oja correction in addition to Delta correction;
3. decoupling erase and write gates on both sides;
4. using a shared latent slot as the interface between two corrections;
5. using two corrected memory stages or a two-layer Delta/Oja composition;
6. claiming efficient parallelism from the standard low-rank WY/UT product alone.

The paper's own ablations report that complementary OJA2/Delta2 stages outperform using the same correction on both stages; standalone OJA2 is not uniformly stronger than GDN2.  This is important: “bidirectional correction” is an architecture with empirical claims, not a theorem that every key collision is solved.

## Residual limitations, not automatic candidate licenses

GSA2 still has fixed slot/state capacity, learned routing ambiguity, and no formal revision-versus-coexistence identifier.  Its two stages add state and constant factors, and a shared slot can itself be a collision surface.  These are valid investigation points, but “improve routing,” “add more slots,” “protect slots,” or “add another correction stage” are already crowded routes.  A new candidate must derive a different observable, state invariant or failure separation and compare against the actual GSA2 two-sided recurrence.

The paper uses existing language/retrieval evaluations and reports results; none were rerun here.  This audit records formulas and exclusion boundaries only and makes no independent empirical claim.  No project code, test, model, benchmark, training, inference, scorer, download or GPU work was executed.
