# R11 source and collision audit

## Fixed sources read

1. Yang et al., *Parallelizing Linear Transformers with the Delta Rule over Sequence Length*, arXiv:2406.06484v6 (15 January 2025), especially the exact ordered Householder-product/WY-style chunk formulation. The paper's stated contribution is sequence-parallel Delta evaluation, not cancellation of noncommutativity.
2. Siems et al., *DeltaProduct: Improving State-Tracking in Linear RNNs via Householder Products*, arXiv:2502.10297v7 (22 October 2025), §4 equations for multiple ordered Delta steps per token and §5.1 implementation note. The product order is the mechanism that raises transition rank/expressivity.
3. Author-maintained FLA implementation at commit `a7880060012c862d58575ee23f613cafcd728d03`, `fla/layers/gated_deltaproduct.py`, blob `82d1a62ac228f3c80aa8818b6e0d0082ce6635b8`, read 10 October 2026. `GatedDeltaProduct.forward` expands each token to `num_householder` ordered keys/values/betas; chunk mode calls `chunk_gated_delta_product`, while recurrent inference flattens the ordered microsteps and calls `fused_recurrent_gated_delta_rule`. This is implementation evidence for preserving order, not for a semantic harmful-order detector.
4. Authors' `automl/DeltaProduct` repository at commit `d62241a81d07aa32b1b65e7d17377f6a7cd0a5d8`: `README.md` blob `c316366630cf63fbd8cd74c27680a95fbc6d0bb5`; `state_tracking/src/generate_data.py` blob `66ca0701e1dd3508e1459d4b6d494b393e2091c5`; `state_tracking/src/main.py` blob `1e72f648fdda2a0114b263e7e01e7d63c8ac356f`; and `state_tracking/src/utils.py` blob `4ef3b1cef867e6f190cf0defbaf443ece742aa65`, all read 10 October 2026. This audit inspected interfaces only and ran no entry point.
5. Eckart–Young–Mirsky theorem, used only as a classical low-rank baseline after left whitening by \(G^{1/2}\); no originality claim is attached to (6).

## Collision conclusion

- Exact chronological affine composition is already the correct algebraic baseline in Yang et al.
- Multiple ordered generalized Householder updates are the central mechanism of DeltaProduct; an adjacent rank-two order gap is therefore not a distinct architecture.
- Query-weighted truncation is generic low-rank approximation. The residual theorem may be useful as analysis/control, but it does not clear mechanism novelty.
- Neither source supplies the missing causal signal that labels an observed order effect as harmful overwrite versus valid chronology. That residual problem is real but remains unconstructed here.

## Native measurement feasibility

The fixed author code exposes generated group word-problem state tracking. `generate_data.py` writes seed/input/target CSV data with cumulative group-product targets; the defensible noncommuting cases are permutation groups such as S3/S4/A5/S5. `main.py` routes scoring through `compute_metrics` and imports `sfirah.metrics::{token_accuracy,sequence_accuracy}`, while `utils.py` supplies cumulative sequence accuracy. Readiness is only partial: the `sfirah` dependency revision and exact scorer denominator were not pinned here, and the repository generates data rather than releasing a fixed dataset. The paper reports Chomsky-hierarchy experiments, but those task/scorer files were not present in the inspected author tree; parity/modular tasks would not directly isolate noncommuting order effects anyway.

These group tasks can test ordered noncommuting expressivity, but they do not identify harmful-versus-legitimate chronology or validate a causal future-query Gram. bAbI/LAMBADA likewise do not expose the internal oracle gap \(K\), its weighted singular tail, or selector labels. Therefore (6) needs paired orders and query weights that the inspected native assets do not provide; the semantic claim retains a measurement gap. No benchmark, label, result, or score is fabricated in this audit.

## State of evidence

- mathematical identity/conditional optimum: derived;
- nearest-mechanism distinction: sufficient collision/control evidence to park this repair, but not an exhaustive novelty adjudication;
- empirical effect: unknown;
- originality: not established as a method;
- recommended status: parked R11 repair, not candidate.
