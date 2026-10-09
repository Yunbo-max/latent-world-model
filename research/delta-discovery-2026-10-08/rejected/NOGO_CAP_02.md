# NOGO-CAP-02 — exact overwrite is incompatible with reversible retention

Disposition: **rejected control; not a candidate**.  The result closes an invalid escape route rather than proposing a new Delta mechanism.

## Formal object

Let the key-by-value state be (S\in\mathbb R^{d\times m}) with readout (o(q)=S^\top q).  Consider the more general affine single-step write

\[
S^+=AS+uv^\top,
\]

where (A\in\mathbb R^{d\times d}), (u,k\in\mathbb R^d), and (v\in\mathbb R^m).  Require exact overwrite at a unit key (k) for **every** prior state and value:

\[
(S^+)^\top k=v \quad \text{for all }S,v.
\]

Expanding gives

\[
S^\top A^\top k+v(u^\top k)=v.
\]

Because (S) and (v) vary independently, this holds exactly iff

\[
A^\top k=0,\qquad u^\top k=1.
\]

The first condition puts nonzero (k) in the kernel of (A^\top).  Hence (A) is singular.  No update in this affine class can provide unconditional exact overwrite and an invertible old-state path at the same time.

## Ordinary Delta specialization

For

\[
S^+=(I-\beta kk^\top)DS+\beta kv^\top
\]

with \\(\lVert k\rVert=1\\),

\[
v-(S^+)^\top k=(1-\beta)\bigl(v-(DS)^\top k\bigr).
\]

- If \\(\beta<1\\) and (D) is invertible, the old-state path can remain invertible, but arbitrary current-key error is only contracted, not exactly erased.
- If \\(\beta=1\\), current-key overwrite is exact.  The old-state map is singular.  When (D) is invertible, for every (a\in\mathbb R^m) the perturbation (\delta S=D^{-1}ka^\top) lies in its kernel.  Without invertibility, \\(\operatorname{rank}((I-kk^\top)D)\le d-1\\) still implies a nontrivial vector kernel, so left multiplication on \\(d\times m\\) states discards at least (m) real degrees of freedom.

This is a structural tradeoff, not a finite-bit statement.

## Simultaneous protected-query requirement

Let (Q=[q_1,\ldots,q_r]).  Exact preservation of all old readouts (S^\top Q), again for every (S,v), requires

\[
A^\top Q=Q,\qquad u^\top Q=0.
\]

If (k=Qc\in\operatorname{span}(Q)\setminus\{0\}), preservation implies both (A^\top k=k) and (u^\top k=0), whereas exact overwrite implies (A^\top k=0) and (u^\top k=1).  The requirements are infeasible.  A valid success case exposes the boundary: when (D=I) and every protected query is orthogonal to (k), (A=I-kk^\top, u=k) exactly overwrites (k) and preserves those protected readouts.  This is the known orthogonal-protection special case, not a new method.

## Finite-precision capacity statement

Only now impose finite precision: the post-state random variable (Z) belongs to a finite set \\(\Omega\\) with \\(|\Omega|\le 2^B\\).  Let finite-alphabet (M) denote the old behavioral equivalence class that must remain recoverable and finite-alphabet (V) the new value.  If a decoder using ((Z,K)), where (K) is the allowed key/context, recovers ((M,V)) with joint error at most \\(\epsilon\\), Fano's inequality gives

\[
B\ge H(M,V\mid K)-h_2(\epsilon)
-\epsilon\log_2(|\mathcal M||\mathcal V|-1).
\]

If (M,V) are mutually independent, uniform on their full respective alphabets, and independent of (K), then exact recovery gives

\[
B\ge \log_2|\mathcal M|+\log_2|\mathcal V|.
\]

Thus coexistence consumes additional code capacity under an explicit finite-state assumption.  A true revision may release the old behavioral class; a coexisting near-key fact may not.  This does **not** infer a finite-bit bound from real-valued finite dimension alone.

## Identifiability boundary

Suppose two histories induce the same (S), and the update receives the same ((k,v,\text{context})) in both worlds.  If their admissible post-state behavior sets are disjoint—for example, a protected old query must retain one output in the coexistence world but change to an unequal output in the revision world—every deterministic state-only updater produces the same (S^+) and cannot satisfy both requirements.  The words “revision” and “coexistence” alone do not guarantee this incompatibility in degenerate/equivalent cases.  Distinguishing entity, source, change or event identity in the context can break the premise; a raw residual cannot do so unconditionally.

## Escape-route audit

1. Saving the discarded direction or lost low-order bits adds a side channel/event memory.  Reversible RNNs explicitly pay this cost.
2. Taking \\(\beta<1\\) is the familiar approximate-correction/retention gate tradeoff, not exact overwrite.
3. Forgetting only within a predictive fiber is valid but is the predictive-quotient construction, not a new Delta-specific mechanism.
4. Maintaining a full inverse-Gram or QR factor returns to RLS/VLA, GKA/PDN, basis slots or an additional typically quadratic state.  A generic low-rank/approximate conflict certificate need not be quadratic, but then it requires its own approximation and failure analysis.

Accordingly, “reversible exact-overwrite Delta with no additional information or state” is impossible under the declared affine class.  A future candidate must explicitly choose approximate correction, a justified predictive equivalence class, or additional accessible information/state.

## Nearest sources and scope

- Matthew MacKay et al., *Reversible Recurrent Neural Networks*, NeurIPS 2018, especially the finite-precision lost-bits discussion: <https://arxiv.org/abs/1810.10999> and author code <https://github.com/matthewmackay/reversible-rnn>.
- Linzhe Zhang and Changming Xu, *What Can a Recurrent State Safely Forget?*, arXiv:2609.23366v1, predictive fibers/quotient and exact-corrector boundary: <https://arxiv.org/abs/2609.23366>.
- Xianyao Li et al., *Minimal Recurrent Behavioral Memory for Imitation under Partial Observability*, arXiv:2609.25757v1, behaviorally sufficient recurrent equivalence classes: <https://arxiv.org/abs/2609.25757>.
- Jianhai Zhang et al., *A Geometry-Based Capacity Theory for Finite-Feature Associative Memory*, arXiv:2610.09056v1, finite-feature noise and key/value geometry: <https://arxiv.org/abs/2610.09056>.

These sources support neighboring boundaries only; the list is bounded rather than exhaustive and does not establish originality of the elementary affine singularity proof, which is derived directly.  The result does not rule out restricted state manifolds, nonlinear or state-dependent updates, augmented side state, approximate overwrite, or recovery only modulo a justified predictive equivalence.  No project code, benchmark, training, inference or scorer was executed.
