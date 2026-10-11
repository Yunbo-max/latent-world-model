# R11 v3 source, implementation, collision, and measurement audit

Cutoff: 2026-10-11. Scope: pure-Delta affine transport, lazy low-rank correction overlays, repeated order-gap injections, skinny-factor recompression, exact ordered Delta/WY and DeltaProduct controls, and native measurement feasibility. This is a bounded primary-source audit, not an exhaustive originality claim. No source interface was executed.

## 1. Preserved evidence and new claim

V1 and v2 bytes, source audits, counterexamples, and reviews remain unchanged. V3 changes one cost claim: later residual participation does not by itself increase the rank of a single overlay when both paths share fixed pure-Delta coefficients. It adds the repeated-injection capacity bound, corrected-prestate `MC` term, and transported recompression error. Those changed claims require new review.

## 2. Exact ordered Delta/WY collision

Primary source: Yang et al., “Parallelizing Linear Transformers with the Delta Rule over Sequence Length,” arXiv:2406.06484v6, 15 January 2025, full text `https://arxiv.org/pdf/2406.06484v6`.

- Section 2.2 gives the Delta recurrence.
- Section 3.1 equation (3) gives its additive pseudo-value form.
- Section 3.2 equations (4)--(5) unroll ordered products and affine contributions.

That ordered affine superposition already implies `C_t=A_tC_{t-1}+E_t` for a common frozen-feature comparison. V3's lazy factor transport is a direct Delta specialization, not a new recurrence.

Pinned author implementation: `fla-org/flash-linear-attention` commit `a7880060012c862d58575ee23f613cafcd728d03`.

- `fla/ops/delta_rule/naive.py`, blob `d1f65a859a9cf74b98e71fbd9eb18c2165f9822a`, `delta_rule_recurrence` forms `v-S^Tk`, applies the rank-one write, and reads `q^TS`.
- `fla/ops/delta_rule/wy_fast.py`, blob `672bf0ec84dc9aa9e7fcda6a1bd8cb4f123c5f78`, `prepare_wy_repr_fwd` and `recompute_w_u_fwd` construct the exact ordered chunk representation.
- `fla/ops/delta_rule/chunk.py`, blob `de56d867b01e7974d58bad306b8aba28b5d02830`, calls that WY preparation and exposes a full recurrent state.
- `fla/layers/delta_net.py`, blob `6f34aba3fa77367162d75b4937db46b1cd8007b2`, selects recurrent/chunk implementations and passes the full recurrent state.

The inspected interface has no separate semantic-selector or low-rank correction-overlay API. That absence is an interface observation, not evidence that the generic algebra is novel.

## 3. DeltaProduct collision

Primary source: Siems et al., “DeltaProduct: Improving State-Tracking in Linear RNNs via Householder Products,” arXiv:2502.10297v7, 22 October 2025, full text `https://arxiv.org/pdf/2502.10297v7`.

Section 4 equation (3) composes multiple sequential gradient/Householder steps into an ordered transition product and affine sum. It directly covers propagation through repeated low-rank Delta transitions.

Pinned FLA implementation at the same commit:

- `fla/layers/gated_deltaproduct.py`, blob `82d1a62ac228f3c80aa8818b6e0d0082ce6635b8`, exposes `num_householder`, flattens the ordered microsteps, and uses full recurrent state;
- `fla/ops/gated_delta_product/chunk_ref.py`, blob `3e78eee82a4083c1fe00466e5de20adcfc1e1a87`, reshapes token-by-microstep inputs and delegates to ordered Delta/gated-Delta chunk routines.

The author task repository remains `automl/DeltaProduct` commit `d62241a81d07aa32b1b65e7d17377f6a7cd0a5d8`. Neither inspected implementation supplies harmful-order semantic labels or a counterfactual correction selector.

## 4. Incremental low-rank maintenance collision

Primary source: Matthew Brand, “Fast Low-Rank Modifications of the Thin Singular Value Decomposition,” *Linear Algebra and its Applications* 415(1):20--30, 2006, DOI `10.1016/j.laa.2005.07.021`; MERL full text `https://www.merl.com/publications/docs/TR2006-059.pdf`.

Section 2 equations (1)--(5), article pages 22--23 / PDF pages 4--5, reduce an additive low-rank modification to extended skinny orthogonal bases and a small core. Section 6, PDF pages 14--15, discusses streaming rank-increasing updates, immediate truncation, lost variance, and order/adversary sensitivity. This is a direct computation collision for append/merge/recompress. V3's sharp legal Delta block witness and `MC` correction are specialized theorem/debug content, not a distinct low-rank solver.

## 5. Functional comparison

| Object | Closest established mechanism | V3 residual | Decision |
|---|---|---|---|
| passive overlay transport | Yang Delta/WY ordered affine recurrence | explicit residual/query coupling and factor cost | direct specialization |
| multiple ordered transitions | DeltaProduct ordered microsteps | semantic correction interpretation | mechanism collision |
| append/merge/recompress | Brand skinny bases plus small-core SVD | sharp Delta gap rank witness | generic computation collision |
| selector and query metric | none of these sources supplies validity evidence | lawful `p` and transported `G` still missing | information gap |
| repeated corrected-state gap | affine branch difference `K(S+C)=K(S)+MC` | explicit R11 bookkeeping correction | narrow theorem only |

Adjudication: **major functional collision** for the mechanism and computation. No inspected source is claimed to state the exact R11 block witness verbatim, and no priority claim is made. The surviving contribution is a conditional Delta-specific control theorem.

## 6. Measurement feasibility

The pinned DeltaProduct group-state scripts generate sequences with cumulative group-product targets, import/call token and sequence accuracy, and expose cumulative-prefix accuracy. They can test whether legitimate noncommutative order is represented and whether endpoint state tracking degrades with length. The `sfirah` dependency revision and exact scorer denominator remain unpinned, and the author repository generates data rather than publishing one immutable dataset.

It does not expose:

- the internal adjacent gap `K` or overlay factors;
- exact corrected-versus-base state equality;
- overlay rank, truncation tail, or recompression error;
- a harmful-versus-legitimate chronology label;
- paired counterfactual order branches or a lawful future-query metric.

Parent-audited bAbI and LAMBADA are endpoint controls only. Packet-reused source records also pin `xiaowu0162/LongMemEval@9e0b455f4ef0e2ab8f2e582289761153549043fc` and `Arvid-pku/ATOKE@a1b42e34e4130507220307ced3d681fb8719831f` as answer-level update/temporal-editing endpoints; they were not newly requalified in this round. Those prescribed-update tasks still do not natively provide R11's hidden adjacent-state selector, both internal branches, or factor ledger. Therefore no inspected native object jointly identifies the theorem's mechanism and semantic utility. A synthetic algebra check would be engineering instrumentation, not a native scientific benchmark; none was created or run.

## 7. Cost and implementation boundary

The exact overlay can avoid dense materialization only in the common fixed-coefficient/shadow-path scope. It pays factor state and bandwidth on every later residual/query. Each independent injection appends factors; exact dependence removal or lossy recompression uses QR/core-SVD machinery; dense materialization can be preferable depending on traffic. A direct same-information action predictor or scalar R11 edit using the identical overlay engine receives the same benefit.

If future features/selectors depend on the corrected memory, the shadow partition is not the counterfactual uncorrected trajectory. General recurrent Jacobians need not preserve matrix rank. A realized future-query Gram remains an oracle at decision time unless supplied by a declared prefix-lawful source.

## 8. Bounded conclusion

The source record supports v3's conditional correction: one passive overlay stays low rank; repeated independent new gaps can force cumulative rank; generic recompression is known. It does not support a new updater, semantic selector, matched-total-cost advantage, native measurement claim, or empirical benefit.

- Source/collision status: major mechanism and computation collision; narrow theorem residue only.
- Measurement status: endpoint tasks located, mechanism-identifying object absent.
- Empirical status: unknown; no execution.
- Candidate delta/admission: `0`.
- Disposition: park R11 after attempt 3/3 exhausted.
