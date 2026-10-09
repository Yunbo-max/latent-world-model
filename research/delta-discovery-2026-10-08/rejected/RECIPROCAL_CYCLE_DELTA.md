# Reciprocal-cycle Delta: exact construction and identifiability boundary

Disposition: **rejected as a distinct method; retained as a bidirectional-memory control**.  This record is mathematical/source analysis only.  No project code, model, benchmark, download, test or GPU job was executed.

## Causal construction

Use key-by-value forward state and value-by-key reverse state

\[
S_t\in\mathbb R^{d_k\times d_v},\quad S_t^\top k\in\mathbb R^{d_v},
\qquad
R_t\in\mathbb R^{d_v\times d_k},\quad R_t^\top v\in\mathbb R^{d_k}.
\]

After the actual ordered decays \(\bar S_t=D_t^kS_{t-1}\), \(\bar R_t=D_t^vR_{t-1}\), define

\[
e_t^v=v_t-\bar S_t^\top k_t,qquad e_t^k=k_t-\bar R_t^\top v_t
\]

and the most direct reciprocal update

\[
S_t=\bar S_t+\beta_t k_t(e_t^v)^\top,qquad
R_t=\bar R_t+\gamma_t v_t(e_t^k)^\top.
\]

A non-decorative cycle objective can be written before the write.  Let

\[
a=\bar S^\top k,\quad b=\bar R^\top v,
\quad c^k=k-\bar R^\top a,quad c^v=v-\bar S^\top b.
\]

For

\[
\mathcal L={1\over2}\|e^v\|^2+{\lambda\over2}\|e^k\|^2
+{\mu\over2}\|c^k\|^2+{\nu\over2}\|c^v\|^2,
\]

direct differentiation gives

\[
-\nabla_S\mathcal L=k(e^v)^\top+\mu k(Rc^k)^\top+\nu b(c^v)^\top,
\]

\[
-\nabla_R\mathcal L=\lambda v(e^k)^\top+\mu a(c^k)^\top+\nu v(Sc^v)^\top.
\]

Thus the proposal has an actual finite-rank recurrence, not merely a named loss.  It doubles persistent state to \(2d_kd_v\) for independent \(S,R\), and the full cycle version adds several matrix--vector products and outer products per token.

## Two decisive degeneracies

For unit \(k,v\) and full interpolation \(\beta=\gamma=1\),

\[
S_t^\top k_t=v_t,\qquad R_t^\top v_t=k_t,
\]

so the post-write cycles satisfy

\[
R_t^\top S_t^\top k_t=k_t,qquad S_t^\top R_t^\top v_t=v_t
\]

regardless of whether the pair is a true revision, a second fact or an encoder collision.  Current-pair post-write cycle consistency is therefore an interpolation tautology.

More generally, every reciprocal state and cycle score is a causal function of the observed history \(H_t=((k_1,v_1),\ldots,(k_t,v_t))\).  Consider two latent worlds with the same \(H_t\): in one, \((k_a,u)\to(k_b,v)\) is a revision of one entity; in the other, the two pairs are distinct facts whose learned keys collide.  The correct actions are overwrite and coexist, but \(S_t,R_t\) and every cycle score are identical.  Fresh internal randomness cannot add the missing identity evidence.  This is the existing revision--collision data-processing boundary in a bidirectional coordinate system.

## Bijection and capacity boundary

If a tied construction requires exact forward and reverse recall,

\[
S^\top k_i=v_i,qquad Sv_i=k_i,
\]

then for all \(i,j\),

\[
\langle k_i,k_j\rangle
=\langle Sv_i,k_j\rangle
=\langle v_i,S^\top k_j\rangle
=\langle v_i,v_j\rangle.
\]

Thus the key and value Gram matrices must agree.  More generally exact cycles require a bijection between the represented key and value subspaces.  For two keys sharing one value,

\[
\min_u\sum_{i=1}^2\|u-k_i\|^2={1\over2}\|k_1-k_2\|^2.
\]

Cycle error diagnoses non-injectivity or conditioning; it does not say whether either association is obsolete.  Independent \(S,R\) removes the tied-Gram restriction by paying twice the state, but does not remove the semantic ambiguity.

## Closest work and disposition

- Kosko's bidirectional associative memory already uses a matrix and its transpose for heteroassociative round-trip recall: *Bidirectional Associative Memories*, IEEE TSMC 18(1), 1988, DOI 10.1109/21.87054.
- GSA2, arXiv:2610.02816v1, §§3.1--3.2 Eqs.7--13, explicitly combines value-to-key OJA2 correction and slot-to-value Delta2 correction through shared slots.
- DeltaProduct, arXiv:2502.10297v7 §4, already covers multiple rank-one correction directions per token.
- Exact forward/reverse ridge maps are ordinary two-sided regression; improving their solve with RLS/PDN/GKA does not create identity information.

Distinguishing prediction: any claimed revision benefit should vanish when compared with an equal-state bidirectional Delta/GSA2 baseline, and cycle evidence should fail for many-to-one values or identical observed histories with different latent semantics.  A surviving benefit from stable entity/source/version inputs would be attributable to that new causal observable, not reciprocity.

The construction is therefore not assigned a D-number.
