# R13 source and collision audit — dynamic covector transport

## Frozen atomic claim

For a realized affine memory transition `S_t=A_tS_{t-1}+B_t`, the old declared linear readout can be represented at the new state by `Q_t^T S_t+C_t` for every prior state exactly when `ker(A_t) subset ker(Q_{t-1}^T)`. Near a singular Delta overwrite, exact transport of an overlapping protected component requires a reader norm growing as the reciprocal retained singular value; at the singular overwrite the component is unrecoverable without side information. This is a conditional certificate and obstruction, not a semantic gate or a new updater.

## Fixed sources read

| Source | Fixed locator | Material actually used | Boundary |
|---|---|---|---|
| Penrose, *A generalized inverse for matrices* (1955) | DOI `10.1017/S0305004100030401` | Generalized inverse as the classical solution device for consistent linear matrix equations; R13 applies it to `X A=C`. | Does not supply a Delta-specific novelty claim. |
| Luenberger, *Observers for multivariable systems* (1966); Roman & Bullock, *Design of minimal order stable observers for linear functions of the state via realization theory* (1975) | DOI `10.1109/TAC.1966.1098323` (metadata/abstract and accessible opening discussion read); DOI `10.1109/TAC.1975.1101061` (abstract/metadata read) | Functional/reduced-order observer literature studies dynamic estimation of declared linear state functions, including minimum-order realizations. | Strong conceptual collision, not a claim that the papers contain R13's one-step known-post-state factorization verbatim. |
| Giles & Pierce, *An Introduction to the Adjoint Approach to Design* (2000) | DOI `10.1023/A:1011430410075`, section 2.2, pp. 394--395 | The linearized direct equation `Au=f` and adjoint equation `A^Tv=g` establish transposed sensitivity transport; this is the nearest computational interpretation of the full-Jacobian extension. | Conventional adjoints propagate a future covector backward; R13 instead solves an inverse equation from an old covector. Neither supplies semantic validity. |
| MacKay et al., *Reversible Recurrent Neural Networks* (NeurIPS 2018) | proceedings paper read; author repository located but code bytes not used for a mechanism claim | Perfect reversibility forbids forgetting; controlled forgetting requires retained side bits. | Architecture-level comparator, not the same deployed state transition. |
| Yang et al., *Parallelizing Linear Transformers with the Delta Rule over Sequence Length* | arXiv `2406.06484` | Ordered Delta recurrence and chunk/recurrent equivalence. | No moving protected-reader theorem claimed here. |
| *How Linear Attention Remembers* | arXiv `2609.33093v1`, sections 2.1--2.2, equations (1)--(4) | Separates storage from access and transports contributions through ordered linear transitions on a fixed forward path. | Aggregate contribution transport is not semantic identification or finite counterfactual replay. |
| Flash Linear Attention author implementation | `fla-org/flash-linear-attention@a7880060012c862d58575ee23f613cafcd728d03` | `fla/layers/delta_net.py` dispatches `chunk_delta_rule` or `fused_recurrent_delta_rule`; `fla/ops/delta_rule/naive.py::delta_rule_recurrence` materializes `S <- S + k[beta(v-S^T k)]^T`, emits `q^T S`, and exposes only final recurrent state through the standard interface. | The implementation has no transported `Q_t`, offset ledger, inverse, protected-subspace oracle, or certificate output. |

## Formula/interface readback

At the pinned FLA commit, the naive reference first computes `_v = v - (S*k).sum(-2)`, scales it by `beta`, then updates `S = S + k outer _v`; output is an einsum of `q` with the post-update state. The layer obtains `q,k,v,beta` from the current hidden state and returns a cacheable recurrent state. Therefore R13 is not a hidden restatement of an exposed author-code option: it is an analysis of whether a separately declared old linear functional can be decoded from the realized post-state.

## Functional collision map

| R13 ingredient | Closest established mechanism | Residual difference | Audit disposition |
|---|---|---|---|
| Solve `Q_t^T A_t=Q_{t-1}^T` | generalized inverse / linear systems | Delta rank-one specialization and overwrite boundary | mathematical specialization, not standalone method novelty |
| Preserve only declared linear functionals | functional observers / minimum-order realization | R13 gives a one-step exact decoder and singular Delta boundary, not an observer synthesis result | direct conceptual collision; retain only as a specialized diagnostic |
| Transport a covector through dynamics | adjoint/VJP transport | persistent declared state readout rather than loss gradient | same algebraic family; contribution difference is interpretive/theorem-level only |
| Avoid information loss | reversible RNN plus side bits | R13 leaves update unchanged and diagnoses recoverability | strong comparator; reversibility is more constructive but pays architecture/state |
| Carry affine offset | checksum/ledger/augmented state | exact cancellation of known write term | side-information bookkeeping; direct value ledger is simpler for the narrow target |
| Delta near-overwrite law | Sherman--Morrison / singular-value conditioning | explicit `1/|1-beta||k||^2|` protected-reader amplification | useful Delta diagnostic; originality not established |

## Search scope and negative evidence

On 2026-10-10 this bounded audit searched the exact functional objects rather than only the proposed name. Query families included `time varying linear functional observer`, `minimum order observer linear function state`, `XA=C generalized inverse solution`, `covector transport inverse adjoint`, `reversible recurrent side bits forgetting`, `linear attention contribution transport`, and `DeltaNet recurrent state implementation`. Citation expansion covered the primary generalized-inverse, functional-observer, adjoint, reversible-recurrence, Delta, and contribution-transport sources above. This is one bounded batch, not two saturated nearest-neighbor rounds. No inspected source established R13 as a new architecture. Conversely, no source read in this batch was found to state the exact Delta overwrite trilemma with the affine-offset cost in the same notation. Absence in this bounded search is not evidence of priority.

## Measurement and evidence boundary

Native endpoint QA (including knowledge-update subsets) can test final answer behavior but does not reveal `A_t`, declared `Q_t`, singular values, or the side-information ledger. At LongMemEval official repository commit `9e0b455f4ef0e2ab8f2e582289761153549043fc`, `src/evaluation/evaluate_qa.py` evaluates `knowledge-update` answers with an answer-level yes/no LLM judge; it does not inspect R13's internal objects. Thus it cannot verify the internal iff condition or conditioning law without instrumentation. R13 also assumes the protected covector is already available causally; identifying which fact is valid remains the unresolved semantic problem.

## Verdict

- Mathematical-source support: sufficient for a conditional control theorem, subject to independent byte-bound review.
- Mechanism originality: **not established**; the construction lies in generalized-inverse, adjoint, and reversible-memory territory.
- Empirical status: unknown and untested.
- Pool action: park as a repaired theoretical boundary, do not count as an active or admitted candidate.
- Reopen only with a causal selector for the initial protected object and its validity, a downstream operation unavailable to direct protected-value ledgers, a matched-state/precision/compute/access advantage, and an endpoint or internal protocol that can distinguish the certificate.
