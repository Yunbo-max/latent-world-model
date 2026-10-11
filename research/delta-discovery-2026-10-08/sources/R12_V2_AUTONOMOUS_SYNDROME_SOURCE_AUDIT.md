# R12 v2 autonomous-syndrome closure — source, collision, interface, and measurement audit

Audit date: 2026-10-11  
Subject: \`../repairs/R12_AUTONOMOUS_SYNDROME_CLOSURE.v2.md\`  
Scope: primary-formula and static author-interface reading only. No project or
upstream code was executed; no model, benchmark, scorer, training, inference,
download, GPU job, synthetic case, or Docker action was run.

## 1. Frozen atomic claim

For fixed-prefix affine Delta transitions, a fixed syndrome \(H^\top S\) is an
autonomous exact recurrent state iff its kernel is forward invariant, equivalently
\(F^\top\operatorname{col}(H)\subseteq\operatorname{col}(H)\). For pure Delta,
every active key is either inside the retained subspace or orthogonal to it. In
orthonormal syndrome coordinates \(U\), the best one-step linear reduction has
exact worst-case leakage
\(|\beta|\|P_V k\|\|P_{V^\perp}k\|\). An unnormalized \(H\)-coordinate leakage
is scale dependent and must not be compared without decoder conditioning and
finite precision. None of these quantities identifies semantic validity.

## 2. Primary Delta source and released interface

Songlin Yang, Bailin Wang, Yu Zhang, Yikang Shen and Yoon Kim,
*Parallelizing Linear Transformers with the Delta Rule over Sequence Length*,
arXiv:2406.06484v3 (31 October 2024),
<https://arxiv.org/html/2406.06484v3>, §2.2 equations around the remove/write
update and §3.1 equations (3)--(4), were read in full HTML. The paper explicitly
computes the old value from the previous matrix state and writes the recurrence as
a generalized Householder right multiplication plus a rank-one write (the paper
uses the transposed value-by-key convention). It further notes that computing the
pseudo-value naively requires the previous state and derives an ordered WY
representation instead of replacing that state with an arbitrary checksum.

The paper links the Flash Linear Attention implementation. R12 v1 already pinned
the repository now canonical at
\`fla-org/flash-linear-attention@a7880060012c862d58575ee23f613cafcd728d03\`
and inspected \`fla/layers/delta_net.py\` plus
\`fla/ops/delta_rule/__init__.py\`: the available interfaces dispatch ordinary
recurrent/chunk Delta kernels with query/key/value/gate/state inputs; no
\(H,Y,L\) autonomous-syndrome interface was found at that pin. V2 reuses that
fixed interface evidence and does not claim a fresh code search or execution.

Source consequence: the hidden-state residual repaired by v2 is part of the actual
Delta recurrence, while exact ordered Delta/WY is the strongest direct baseline.
The v2 theorem is derived here; it is not attributed to the DeltaNet paper.

## 3. Decisive general-mechanism collision

George J. Pappas, *Bisimilar Linear Systems*, Automatica 39 (2003),
DOI 10.1016/j.automatica.2003.07.003, author-hosted full text, was read at
Definition 10, Theorem 16/equations (19)--(21), Corollary 17/equations (26)--(28),
and Theorem 21/equations (39)--(41).

- The paper represents a linear quotient by a surjective map \(z=Hx\).
- Theorem 16 characterizes preservation of quotient fibers by a controlled
  invariance condition on \(\ker H\).
- Corollary 17 extends the condition across discrete time.
- Theorem 21 establishes the general invariant-subspace fixed-point mechanism
  through a maximal invisible-kernel iteration. R12 equation (8) is the
  pure-Delta/common-map dual specialization, not Pappas's literal recursion.

R12 v2's condition \(\ker H^\top\subseteq\ker(H^\top F)\) is the
no-control, exact-same-input specialization of this established quotient/lumping
geometry. Its fixed-point construction for rank-one Delta maps is therefore a
Delta corollary, not a new invariant-quotient principle.

The packet's already-published R18 v1 is an even stronger internal collision:
it treats the complete recurrent state, exact global fibers, affine finite-horizon
quotients, nonlinear Jacobians, side-state rescue, and backward invisible-space
recursion. R12 v2 remains useful because it exposes the one-line pure-Delta
dichotomy and sharp leakage constant, but it cannot be counted as a distinct
method.

## 4. Relation to R12 v1 and other packet controls

| Record | Object | What survives | Why v2 is not a new candidate |
|---|---|---|---|
| R12 v1 | static \(H^\top\Delta\) functional recovery | nullspace factorization, hidden-edit minimax pair, noise/leakage bound | v2 adds recursive closure, not a new information source |
| R18 v1 | complete joint-state quotient/fiber invariance | full-state nonlinear and side-state obligations | strictly broader general mechanism |
| R01 v2/v3 | exact right quotients for declared credit families | direct sufficient-coordinate and transported-covector controls | same quotient principle on a different matrix side |
| DeltaNet/WY | exact ordered state recurrence | computes state-dependent old value without losing order | strongest direct implementation baseline |
| Direct \(U^\top S\) | coordinates of the invariant subspace | same state width and closure as any well-conditioned \(H\) | designed syndrome is a coordinate change |

The parent checksum no-go also survives: neither invariant closure nor small
leakage identifies revision/coexistence, entity identity, latest truth, or whether
a write should be released.

## 5. Novelty and distinctness verdict

- Mathematical status before independent review: complete conditional derivation
  for fixed-prefix affine coefficients; full state-dependent coefficients remain
  under R18/full-Jacobian scope.
- Mechanism novelty: decisive collision with invariant quotients/bisimulation and
  direct reduced coordinates.
- Delta-specific residual: equations (7), (8), and (13) in the paired artifact
  give an explicit active-key dichotomy, minimum reducing-space iteration, and
  sharp normalized one-step leakage for rank-one Delta transitions. For an
  infinite/implicit neural key family, equation (8) is set-theoretic unless a
  finite certified description or proof covers the full allowed family.
- Method distinctness: no. No new external evidence, updater, recurrence family,
  or same-budget advantage is introduced.
- Exact-formula priority: bounded search only; no exhaustive absence claim.

Disposition supported by sources: **conditional theory/debugging control; park
after attempt 2/3; candidate delta zero**.

## 6. Native measurement and fair-cost status

R12 v1 fixed LongMemEval at official commit
\`9e0b455f4ef0e2ab8f2e582289761153549043fc\`: its knowledge-update answer judge
and task/overall accuracy aggregator expose endpoint correctness, not internal
syndrome fibers. Existing fixed bAbI, LAMBADA, RULER and BABILong assets likewise
score answers/tokens/retrieval, not paired states with equal \(H^\top S\),
\(P_{V^\perp}k\), invariant-subspace dimension, or the leakage operator.

Accordingly:

- theorem verification is mathematical, not an endpoint benchmark result;
- behavioral endpoints may later compare implementations but cannot natively
  attribute a gain to the v2 mechanism;
- a custom hidden-state diagnostic would not close the current native-measurement
  obligation and was not created;
- matched cost must include full state if retained, or \(H/L\) representation,
  basis tracking, quantization scales, metadata, traffic and decoder work if the
  state is replaced; it must also include certification/description of an
  infinite key family and any full-state coefficient generator.

Strong same-information controls are exact Delta/WY, direct orthonormal reduced
coordinates \(U^\top S\), the R18 complete-state quotient/JVP analysis, and no
compression. Empirical effect is unknown, not failed.

