# D07/WTSR full-formula and author-code collision audit

Disposition: **major functional collision with a narrow formula-level residual; inactive diagnostic/control, not a scientifically admitted candidate**.

The frozen claim is deliberately narrow.  For a token-level Delta write

\[
W_i=\beta_i k_i e_i^\top,\qquad
P_{i,h}=A_{i+h}\cdots A_{i+1},
\]

D07 directly penalizes the normalized realized-path state survival

\[
s_{i,h}=\frac{\|P_{i,h}W_i\|_F^2}{\|W_i\|_F^2}
=\|P_{i,h}k_i\|_2^2,
\qquad
\mathcal L_{\rm WTSR}=\mathbb E[(\rho_h^2-s_{i,h})_+^2].
\]

The loss appears only during training; deployment keeps the ordinary Delta recurrence, readout and state size.  The audit asks whether that exact combination, rather than the broader ideas of tracing a source or training retention, remains scientifically distinct.

## 1. Source contribution is already the same mathematical object

Lee et al., *How Linear Attention Remembers*, arXiv:2609.33093v1, §2.1--2.2, write a recurrent state as a transition plus a source write and define the contribution of source \(i\) at time \(t\) by

\[
C_i^{(t)}=(T_t\circ\cdots\circ T_{i+1})(C_i^{(i)}).
\]

For linear Delta transitions this is exactly \(P_{i,h}W_i\).  Their Eqs. 4--5 also separate survival in state from access by a query.  The analysis is explicitly conditioned on the observed/frozen forward trajectory; counterfactually changing an earlier write can change later features and requires replay.  D07 inherits the same restriction.  D07's normalized rank-one norm is therefore a specialization of an existing source-contribution object, not a new definition of memory.

RPMem, arXiv:2609.23466v1, Appendix E.1/E.4, independently decomposes a gated recurrent state into per-source coefficients on the observed gate path and names

\[
L_i(a)=w_{i,i+a}/w_{i,i}
\]

source survival.  Its recurrence is different from Delta and it does not use the D07 hinge, but it further removes any broad novelty claim for realized-path source survival.

## 2. Tabular ICL gives an exact same-key specialization and a simpler mechanism

Schnurr et al., *Adapting Linear-Time Architectures for Tabular In-Context Learning*, arXiv:2609.36337v1, §4.4, replace the Delta write rate by

\[
\beta_t^{\rm eff}=\beta_t\eta_t,
\qquad \eta_t=\frac{c}{t+c},
\]

with \(c=256\) in their reported configuration.  Appendix D.7 Eq. 10 gives the same-key source contribution

\[
C_i=\beta_i\prod_{t>i}(1-\beta_t).
\]

When \(D_t=I\), all later unit keys equal \(k_i\), and \(A_t=I-\beta_t k_i k_i^\top\), D07 reduces exactly to

\[
\sqrt{s_{i,h}}=\prod_{t=i+1}^{i+h}(1-\beta_t)=C_i/\beta_i.
\]

Thus even D07's normalized scalar is not new in this success case.  The surviving distinction is only that D07 propagates arbitrary ordered keys and optimizes their trace norm, whereas the paper uses a deterministic position schedule that changes both training and inference.

The paper-designated author repository was inspected without executing it:

- repository: <https://github.com/schnurrd/ICL-Architectures>
- pinned current commit: `0be576b8481e153ce7489aba6ad64e278c133c09`
- feature merge: `39eed45a38b8e80e89059a83c7970361251823a4`
- cleaned-paper commit: `c9d4f93d21a2ff5b5132c5035678097735c2d929`
- `PFNs/pfns/model/fla_patches.py`, blob `1743007b85af7fb0d41426b803f9639dcdb5a846`: `_apply_deltanet_beta_decay` returns `beta * t0 / (t0 + position)` and handles cached offsets/token grouping; `_deltanet_beta_decay_patch` applies it before the FLA kernels; `_maybe_patch_deltanet_with_stateless_recurrent` covers chunk, recurrent and stateless paths.
- `PFNs/pfns/model/backbones.py`, blob `76ad5255edafebc1031076e5696ba105fddba672`: validates DeltaNet-only use and threads position/token grouping.
- `PFNs/configs/fla/fla_config.py`, blob `d1c5e2108da0881111cfbdc71ce7134b73360ade`: exposes and wires the decay arguments.
- `PFNs/pfns/experiments/model_benchmarks/model_registry.py`, blob `b61ed4a3a5609a8e3f6a7e578f706f70e052d0ed`: registers `online_inverse` variants with \(t_0=256\).
- `PFNs/notebooks/deltanet_effective_beta_plots.ipynb`, blob `f119436d182f1dc56813fcc9a68a6e7147186de9`: diagnoses the same-key beta product, not an arbitrary-key ordered trace.

This code path is a stronger simple baseline than an unqualified survival regularizer because it implements a deployable retention intervention with no auxiliary loss.  D07 would need a formal separation in which arbitrary-key geometry matters and every scalar schedule fails.

## 3. Behavior-level supervision already targets the claimed function

Kim and Kothari, *Delayed Supervision for Test-Time Language Models*, arXiv:2609.32312v1, §3.1--3.3 and Eqs. 4--6, train event next-token prediction together with delayed semantic QA.  The probe branch is discarded, so the native inference recurrence remains unchanged.  Gradients traverse the original write, intervening transitions and readout, and the labels can distinguish retention from revision.  D07 uses less information, but it supervises only an internal norm that cannot tell whether a source is readable, correct or still valid.

REFINE, arXiv:2602.16704, provides another stronger behavioral alternative through next-sequence prediction and reinforced rollouts.  It is more expensive and does not identify a single source trace, but it prevents treating any long-horizon training objective as unique to D07.

## 4. Exact residual and why it is insufficient

No inspected source was found to reproduce the complete combination

\[
(\rho_h^2-\|A_{i+h}\cdots A_{i+1}k_i\|_2^2)_+^2
\]

for token-level Delta writes, arbitrary non-collinear keys, direct normalized-trace optimization, training-only use, and unchanged deployment recurrence.  This is a bounded no-exact-formula-collision result, not an originality result.

The residual is too narrow for scientific admission:

1. state norm is not query accessibility or semantic correctness;
2. normalization removes \(\beta_i\) and \(\|e_i\|\), so a tiny or irrelevant write can receive the same protection pressure as an important one;
3. the loss has no validity/revision signal and may preserve obsolete facts;
4. for one later key with overlap \(c\), a required residual ratio \(\epsilon\) implies
   \[
   s=1-\beta(2-\beta)c^2\le 1-(1-\epsilon^2)c^2,
   \]
   so strong same-address correction and strong source survival conflict;
5. sampled horizon traces add \(O(NHd)\) training work, while position-dependent write decay is cheaper;
6. there is no native scorer for the internal source norm, and generic QA accuracy cannot identify whether this proxy caused any gain.

## 5. Collision verdict and reopening conditions

The source-contribution object and observed-trajectory qualification are covered by *How Linear Attention Remembers* and RPMem.  The central retention function is addressed by Tabular ICL write-rate decay and delayed semantic supervision.  What remains is an implementation-level formula choice: direct arbitrary-key normalized-trace hinge.

D07 is therefore moved from the active pool to an **inactive source-tracing/retention diagnostic**.  Re-entry would require all of:

1. a formal arbitrary-key ordered-geometry separation where scalar decay cannot achieve the stated property;
2. a result showing the direct hinge solves that separation and is not reducible to equally informed delayed semantic supervision or ordinary future CE;
3. a causal revision-release signal that prevents preserving obsolete writes; and
4. distinct measurements for raw state survival and query-visible valid retention using existing public/native assets, or an explicit unresolved measurement gap.

This audit is bounded to the cited primary texts and pinned author-code paths.  It does not claim an exhaustive prior-art search or absolute non-originality.  No project code, test, model, benchmark, training, inference, scorer, data/model download or GPU job was executed.
