# R10 v3 source, collision, implementation, and measurement audit

Cutoff: 2026-10-11. Scope: fixed low-rank residual carriers for Delta transitions, common invariant subspaces and switched reachability, exact/projected model reduction, error-feedback quantization, author interfaces, and native measurement. This is a bounded primary-source audit, not an exhaustive priority claim.

## 1. Preserved lineage

- Parent math artifact: `repairs/R10_TRANSITION_MATCHED_NOISE_SHAPING.v2.md`, SHA256 `3a9e0c3a185d0f1c0a5724b59a30063963794576f516e4f77ee3f63e71f21d08`.
- Parent source audit: `sources/R10_V2_TRANSITION_MATCHED_NOISE_SHAPING_SOURCE_AUDIT.md`, SHA256 `a09c1dd2dd1a14fa6436428f45e175468ad3dcd659ddeff5a99ac49c7f444781`.
- Preserved conclusion: transition-matched residual feedback is conditional on a common exogenous or feedback-invariant residual law; equal-total-state and overload boundaries remain; classical ESS/QEF/fixed-rate feedback and recurrent quantization are decisive controls.

No parent byte or review is overwritten or reused as v3 approval.

## 2. Common invariant subspaces and simultaneous block structure

Primary source:

- Guillaume O. Berger, Raphaël M. Jungers, and Zheming Wang, “Data-driven invariant subspace identification for black-box switched linear systems,” arXiv:2209.05320v1, 2022, https://arxiv.org/abs/2209.05320 .

Read depth: official full text, Proposition 1 and the displayed block-triangularization criterion. The source treats common invariant subspaces for a matrix family and their equivalent simultaneous block form. R10 v3's condition \(A_\omega U=UB_\omega\), or \((I-UU^\top)A_\omega U=0\), is exactly that established criterion in Delta coordinates.

Impact: decisive collision for the operator-level claim. The Delta expansion of the leakage and the explicit witness are specializations, not a new invariant-subspace mechanism.

## 3. Switched reachability and the minimal invariant hull

Primary source:

- Igor Pontes Duff, Sara Grundel, and Peter Benner, “New Gramians for Linear Switched Systems: Reachability, Observability, and Model Reduction,” arXiv:1806.00406v1, 2018, https://arxiv.org/abs/1806.00406 .

Read depth: official full text, Theorem 2 and Theorem 3. The reachability space is characterized as the smallest subspace containing the input ranges and invariant under every mode; the Gramian range realizes that reachable subspace under the paper's assumptions. This covers the closure skeleton of R10 v3 equation (11).

Primary corroborating source:

- Mert Baştuğ, Mihály Petreczky, Rafael Wisniewski, and John Leth, “Model Reduction of Linear Switched Systems by Restricting Discrete Dynamics,” arXiv:1409.1444v2, 2014, https://arxiv.org/abs/1409.1444 .

Read depth: official full text, Lemma 3 and Claim 1. The paper builds reduced switched realizations from reachable spaces for restricted switching sequences and proves behavior preservation on the declared language. This directly covers the idea that a restricted natural mode family may admit an exact smaller carrier, while unrestricted robustness may not.

Additional closest work:

- Philipp Schulze and Benjamin Unger, “Model reduction for linear systems with low-rank switching,” arXiv:1801.09445v1, 2018, https://arxiv.org/abs/1801.09445 . The paper replaces low-rank switching by an envelope system, reduces that system using standard methods, maps back, and supplies an output-error bound and quadratic-stability preservation under its stated sufficient assumptions. This is close to any claim that low-rank mode changes alone create a new reducible residual carrier.

Impact: the minimal carrier/invariant-hull theorem, restricted-mode escape, and projected-error interpretation all sit inside mature switched-system reduction. R10 v3 contributes a Delta-form instantiation and a sharp legal witness only.

## 4. Quantization and feedback neighbors retained from v2

The v2 exact-version reads remain current:

- P. P. Vaidyanathan, “On Error-Spectrum Shaping in State-Space Digital Filters,” IEEE TCAS 32(1):88–92, 1985, DOI `10.1109/TCS.1985.1085587`.
- Shuichi Ohno, Teruyuki Shiraki, M. Rizwan Tariq, and Masaaki Nagahara, “Rate-Distortion Analysis of Quantizers with Error Feedback,” arXiv:1609.01383, https://arxiv.org/abs/1609.01383 .
- Xue Xian Zheng et al., “Quantitative Error Feedback for Quantization Noise Reduction of Filtering over Graphs,” arXiv:2506.01404v2, https://arxiv.org/abs/2506.01404 .
- Ismail Erbas, Xavier Intes, and Vikas Pandey, “When Quantization Breaks Memory: Recurrent-State Write-Back in Low-Precision Temporal Inference,” arXiv:2609.04490v1, §§2.2–2.3 and Supplements S5/S8/S10, https://arxiv.org/abs/2609.04490 .
- Tao Zhang et al., “DAMP: Decay-Aware Mixed-Precision Recurrent-State Quantization,” arXiv:2608.27513v2.
- Bingchen Yao et al., “STEPQuant: When and Where Errors Matter in Delta-Rule Recurrent State Quantization,” arXiv:2609.38169v1.

Ohno covers strictly causal fixed-rate error-feedback filtering under a no-overload assumption; Zheng et al. cover optimized state-space/graph quantitative error feedback; recurrent write-back covers residual/direction memory; DAMP/STEPQuant cover persistence/readout-aware state quantization. None states the exact R10 v3 noncommuting witness, but the witness does not create a new capability outside those mechanism and model-reduction families.

## 5. Author interfaces and cost boundary

No new author implementation is claimed for the invariant-subspace theorems. They are mathematical sources, not software dependencies. The v2 bounded search found no confirmed author repository for Vaidyanathan, Zheng QEF, Ohno, DAMP, or arXiv:2609.04490.

Pinned relevant author interfaces were read statically:

- `fla-org/flash-linear-attention` at commit `a7880060012c862d58575ee23f613cafcd728d03`: `fla/ops/delta_rule/naive.py::delta_rule_recurrence` computes the current residual `v-S^T k` and applies the ordinary rank-one Delta write; `fla/ops/kda/naive.py::naive_recurrent_kda` applies exponential decay before the rank-one correction, confirming the actual ordered left transition \((I-\beta kk^\top)D\). Neither path exposes an independent low-rank quantization-residual carrier.
- `NVlabs/GatedDeltaNet` at commit `b53d6d3a161267432a79c1c04af69fa52bddc921`: `lit_gpt/gated_delta_rule_ops/chunk.py::{chunk_gated_delta_rule,chunk_gated_delta_rule_ref}` exposes the standard gated/decayed chunk update, not a common-invariant residual-carrier interface.
- `Dreamer-Toby/STEPQuant` at commit `61f24c9c2bc188b60a6c7525e7f86c7459bc737d`: `stepquant/calibration.py` performs offline calibration of recurrent traces and explicitly does not run quantized feedback in that collection path; `stepquant/quantization.py::QuantizationPlan` stores head/key bit and impact plans; `stepquant/kernels/writeback.py::{CapturedWrites,defer_writeback,WritebackGraph}` schedules bounded CUDA write-back. These are strong allocation/write-back controls, not a common-invariant low-rank carrier, and no code was executed here.

For a fixed dense basis, projected Delta transport requires \(U^\top D U\), \(U^\top k\), and reconstruction; a moving basis additionally stores/reads \(U_t\), transports \(A_tU_t\), and reorthogonalizes. A direct low-rank augmented controller with the same factors has the same interface. Any advantage must count model/basis metadata, recurrent bits, scales, overflow flags, bytes moved, and operations.

## 6. Functional comparison and distinctness

| Object | Exact mathematical object | Overlap with R10 v3 | Residual difference |
|---|---|---|---|
| Common invariant-subspace theory | matrix-family invariant carrier / simultaneous block form | exact fixed-carrier criterion | R10 writes the Delta-ordered leakage |
| Switched reachability | smallest common invariant span generated by injections/mode words | exact minimal-hull skeleton | R10 supplies a legal noncommuting rank-one witness |
| Restricted switched reduction | exact behavior on a declared switching language | restricted-prefix-family escape | no Delta semantics |
| Low-rank switching reduction | envelope-system reduction and output-error bounds | low-rank mode change does not imply a new reduction principle | different large-scale systems target |
| ESS/QEF/error feedback | stored quantization error shaped through a state-space filter | transported residual and weighted downstream error | R10 specializes the state transition to Delta |
| DAMP/STEPQuant/recurrent write-back | recurrent-state persistence, allocation, and residual write timing | adjacent quantized-memory mechanism | not the exact common-carrier theorem |
| R09/R16/R18 packet controls | robust carriers, active spectral closure, recursive quotient | internal theorem-level collision | different motivating failure line |

Adjudication: **major functional/theorem collision**. The v3 result is a useful repair closure and counterexample, but no new updater, representation class, or matched-cost capability survives.

## 7. Native measurement feasibility

- Existing bAbI, LAMBADA, RULER, reasoning, and code-task native scorers observe endpoint correctness, not invariant leakage, carrier width, residual tail rank, basis metadata/traffic, saturation, or matched finite-state capacity.
- Graph-filter QEF exposes output noise for its own state-space filter, but not semantic Delta memory or fact validity.
- STEPQuant is the closest public implementation path, but its released path is not an affordable native mechanism object for the retained single-RTX-2080-Ti setting, and endpoint scores would not isolate carrier closure from extra state and compute.
- A synthetic key-family leakage diagnostic or profiler would be informative engineering instrumentation, not an existing native natural benchmark. None was created or run.

Measurement status remains open. Empirical effect remains unknown.

## 8. Search record and bounded conclusion

Search date: 2026-10-11. Queries covered exact titles and combinations of `common invariant subspace matrix family`, `switched system reachable invariant subspace`, `low-rank switching model reduction`, `error feedback quantization state space`, and the already pinned Delta quantization works. Primary arXiv/full-text sources and the existing pinned author repository were used; summaries were not treated as full analysis.

Bounded conclusion: R10 v3 is mathematically correct if its fixed-basis, declared-mode-family, frozen-feature, and cost assumptions remain explicit. Its common-carrier and closure objects are established; the Delta leakage identity and noncommuting witness are a specialized debug theorem. Candidate delta is 0, attempt 3/3 is exhausted, and the line should be parked unless a natural causal restricted family, matched-total-cost advantage, controlled injection tail/saturation, and native measurement object are supplied together.
