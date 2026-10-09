# Provenance tensor Delta: identity-oracle control

Disposition: **rejected as a distinct candidate; retained as a provenance-conditioned control**. This record contains only mathematics/source analysis; no code or experiment was executed.

## Causal construction

Let a semantic key \(k_t\in\mathbb R^{d_k}\) and an already observed source/entity/version/event code \(c_t\in\mathbb R^{d_c}\) form the lifted address

\[
u_t=k_t\otimes c_t\in\mathbb R^{d_kd_c}.
\]

For \(M_t\in\mathbb R^{d_kd_c\times d_v}\), use ordinary ordered Delta:

\[
\bar M_t=D_tM_{t-1},\quad
e_t=v_t-\bar M_t^\top u_t,\quad
M_t=\bar M_t+\beta_tu_te_t^\top.
\]

Read with a semantic query and role code:

\[
\hat v(q,r)=M_t^\top(q\otimes r).
\]

The code must be produced from already observed context/metadata. A dataset-supplied stable ID is extra information access and must be supplied identically to all controls. Plain next-token CE can train this path but cannot certify that a learned code represents stable identity.

## Exact interference law

Relative to the post-decay state, one write changes an arbitrary query by

\[
\Delta\hat v(q,r)
=\beta_t(q^\top k_t)(r^\top c_t)e_t.
\]

Thus the interference kernel is the product of semantic and role similarities. At the written address,

\[
e_t^+=(1-\beta_t\|k_t\|^2\|c_t\|^2)e_t.
\]

Exact overwrite requires \(\beta_t\|k_t\|^2\|c_t\|^2=1\), and repeated fixed-address correction is stable for a factor in \((0,2)\).

For two unit lifted addresses with overlap

\[
\rho=(k_a^\top k_b)(c_a^\top c_b),
\]

two full writes from zero leave the old read

\[
M_2^\top u_a=(1-\rho^2)v_a+\rho v_b.
\]

Same tag/address implements revision; orthogonal tags implement coexistence; intermediate tag overlap gives partial corruption. The recurrence performs whichever identity decision the tagger has already made—it does not decide revision versus coexistence.

For many addresses \(U=[k_i\otimes c_i]\),

\[
U^\top U=(K^\top K)\circ(C^\top C),
\qquad
\operatorname{rank}U\le\operatorname{rank}K\operatorname{rank}C.
\]

One-pass Delta still does not compute the joint inverse-Gram interpolation for correlated addresses.

## Routed-slot equivalence and the missing index

Reshape \(M\) into \(d_c\) ordinary memories. With one-hot \(c=e_j\), writing \(k\otimes e_j\) updates only slice \(j\). The proposal is exactly independent Delta slots plus a router, up to coordinate permutation.

Unique event tags solve overwrite only by changing the relation from \(k\mapsto v\) to \((k,\mathrm{eventID})\mapsto v\). A query must still supply the event ID. Selecting the latest version needs an entity-to-current-version pointer; arbitrary event retrieval needs an ID-to-slot index or content search. Dense semantic hashes remove the explicit index only by reintroducing collisions.

Exact pairwise orthogonal tags require \(N\le d_c\). For random unit tags,

\[
\mathbb E[c_i^\top c_j]=0,
\qquad
\mathbb E[(c_i^\top c_j)^2]\approx {1\over d_c},
\]

so under additional independence assumptions aggregate RMS crosstalk grows like the square root of the number of interfering writes divided by \(d_c\). The Welch bound forces nonzero coherence when \(N>d_c\). These are approximation/capacity trade-offs, not an identity mechanism.

## Future-path and cost limits

For frozen future lifted features,

\[
\delta\hat v_\tau(x)=
\beta_t x^\top A_\tau\cdots A_{t+1}u_t e_t,
\quad A_s=(I-\beta_su_su_s^\top)D_s.
\]

The product similarity is an immediate law, not an unconditional long-horizon invariant. Dense learned mixing can destroy tag isolation; the full state-dependent network requires Jacobian analysis.

Dense lifted state and arithmetic cost \(O(d_kd_cd_v)\). One-hot routing reduces active read/write cost to \(O(d_kd_v)\) but retains \(d_c\) full memories. With one unique tag per event, this costs \(O(Nd_kd_v)\), usually worse than an indexed event store \(O(N(d_k+d_v+\text{metadata}))\).

## Closest work and measurement gap

The construction is classical tensor-product binding plus ordinary Delta. Smolensky's Tensor Product Representations bind roles and fillers by outer products. Schlag et al., *Learning Associative Inference Using Fast Weight Memory* (ICLR 2021, arXiv:2011.07831), use a third-order tensor addressed by \(k_1\otimes k_2\), read the old value and write a residual outer product—an almost literal mechanism collision. *Linear Transformers Are Secretly Fast Weight Programmers* places Delta over learned feature maps, so \(\phi(k,c)=k\otimes c\) is a feature choice. HRR/VSA cover compressed quasiorthogonal binding and its cleanup/crosstalk trade-off. Product-key and Sparse Delta Memory supply the stronger indexed/sparse alternatives when tags become event IDs.

bAbI, LAMBADA and RULER do not natively score provenance-code correctness, identity routing, or revision-versus-coexistence decisions. A new identity-labelled benchmark would be outside scope. Any later comparison must give the same metadata to ordinary routed Delta slots, explicit event memory and product-key/sparse baselines.

**Ruling:** provenance suppresses interference after identity is known. The tensor lift cannot infer that identity and is directly covered by TPR/FWM/VSA plus routed Delta slots. No D-number is assigned.
