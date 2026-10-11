# R10 v2 source, implementation, collision, and measurement audit

Cutoff: 2026-10-11. Scope: transition-matched quantization-residual feedback, state-space error-spectrum shaping, graph-filter quantitative error feedback, equal-total-state comparison, and Delta-specific measurement feasibility. This is a bounded primary-source audit, not an exhaustive claim that no other work exists.

## 1. Preserved lineage

- Parent repair: `repairs/R10_EQUAL_BIT_TRANSPORTED_RESIDUAL.v1.md`, SHA256 `76ed51db1a0848a234f6e0d8176ff974a48371ad27d55d56c82d3961c0164763`.
- Parent source audit: `sources/REPAIR_R10_EQUAL_BIT_RESIDUAL_SOURCE_AUDIT.md`, SHA256 `310d36ac4942281fc44eaffd9116b3a9042f0e7acffb4d8be0a9ef8603552758`.
- Preserved result: decoded-sum split coding has no equal-cardinality capacity advantage; coarse-visible feedback is a different operator; DAMP/STEPQuant and recurrent-state residual/direction memory remain direct controls/collisions.

No old artifact or review is overwritten or reused as approval for v2.

## 2. Quantitative error feedback for graph filters

Primary work:

- Xue Xian Zheng, Weihang Liu, Xin Lou, Stefan Vlaski, and Tareq Al-Naffouri, “Quantitative Error Feedback for Quantization Noise Reduction of Filtering over Graphs,” arXiv:2506.01404v2, revised 2026-05-11; accepted by IEEE Transactions on Signal Processing, DOI `10.1109/TSP.2026.3664752`.
- Official arXiv record/full text: https://arxiv.org/abs/2506.01404 and https://arxiv.org/html/2506.01404v2 .
- Closely related conference version: Xue Xian Zheng and Tareq Al-Naffouri, “Error Feedback Approach for Quantization Noise Reduction of Distributed Graph Filters,” arXiv:2412.05651 / ICASSP 2025; official institutional full text: https://repository.kaust.edu.sa/bitstreams/93c2245b-884b-4114-8712-0fec4b1280d8/download .

Read depth and exact scope:

- D2/D3 for the arXiv v2 abstract, Introduction/related work, state-space recursion in Eq. (1), deterministic FIR/IIR setup in Eqs. (2)–(3), and the paper’s stated deterministic/random/asynchronous coefficient optimization.
- The institutional full-text capture of the conference version exposes Section 3.1 and Proposition 1. For deterministic FIR, the displayed output-noise contribution has the form

  `sigma_(k-1)^2/N * { tr(G S^2) + tr(G D^2) - 2 tr(G S D) }`,

  where diagonal `D` weights the locally stored quantization error. For `D=diag(d)` and positive diagonal weights, differentiating this quadratic gives the coordinate solution `d_i=(GS)_(ii)/G_(ii)` on nondegenerate coordinates. This is the same weighted-projection structure as R10 v2 equation (9), not an independent Delta novelty.
- The v2 paper explicitly connects the construction to classical error-spectrum shaping in state-space digital filters and says it supplies closed-form feedback coefficients for deterministic, random-graph, and asynchronous cases.

Implementation status:

- The bounded GitHub repository search by both exact titles and principal mechanism returned no confirmed author repository. No file/function mapping or execution claim is made.
- Absence of confirmed public code is an implementation unknown, not evidence that the paper’s mathematical mechanism is absent.

Impact: **decisive major functional collision** for R10 v2’s feedback-coefficient optimization. The graph operator is not Delta, but the state-space objective, stored residual, output-noise quadratic, and coefficient optimization cover the contribution skeleton.

## 3. Classical state-space error-spectrum shaping

Primary historical work:

- P. P. Vaidyanathan, “On Error-Spectrum Shaping in State-Space Digital Filters,” IEEE Transactions on Circuits and Systems 32(1):88–92, 1985, DOI `10.1109/TCS.1985.1085587`.
- The verified bibliographic abstract states that the method applies diagonal second-order error feedback to arbitrary-order state-space structures and optimizes noise behavior jointly with the realization.
- The 2025/2026 Zheng et al. papers cite the broader classical line, including first- and higher-order feedback, coordinate transformation, and roundoff-noise minimization.

Read depth: D1/D2 for bibliographic identity and abstract; the exact old IEEE formula was not used to justify any R10 equation. R10’s algebra was derived independently, while the historical source establishes that the mechanism family is mature. The newer Zheng et al. full formula supplies the decisive functional comparison.

Impact: reinforces that scalar/vector residual feedback and spectral noise shaping cannot be claimed as a new Delta mechanism merely by substituting the Delta transition matrix.

## 4. Fixed-rate error-feedback quantization

Primary work:

- Shuichi Ohno, Teruyuki Shiraki, M. Rizwan Tariq, and Masaaki Nagahara, “Rate-Distortion Analysis of Quantizers with Error Feedback,” arXiv:1609.01383, 2016: https://arxiv.org/abs/1609.01383 .

Read depth and scope: D2/D3 for the official abstract and paper formulation. It models a static uniform quantizer with a strictly causal error-feedback filter, declares negligible overload, minimizes downstream mean-squared quantization error, parameterizes the optimal frequency response, and relates achievable MSE to the number of quantization bits; practical filters are then approximated by Yule–Walker and LMI methods. This directly covers the frequency-weighted noise-shaping and fixed-rate/dynamic-range skeleton adjacent to R10 v2 Sections 4–5. The overload assumption is a limitation, not a free guarantee.

Implementation status: a bounded GitHub search by exact title, arXiv identifier, authors, and mechanism returned no confirmed author repository. This is recorded as an implementation unknown and is not used to weaken the mathematical collision.

Impact: decisive additional collision for any claim that the weighted scalar spectral ratio, bit-aware feedback filtering, or saturation/rate boundary is new. R10 retains only the explicit Delta-transition specialization and equal-state comparator boundary.

## 5. Reused nearest work from v1

The following v1 reads remain current and are reused at the exact versions recorded there:

- Ismail Erbas, Xavier Intes, and Vikas Pandey, “When Quantization Breaks Memory: Recurrent-State Write-Back in Low-Precision Temporal Inference,” arXiv:2609.04490v1, §§2.2–2.3 and Supplement S5/S8/S10. Its recurrence-visible word remains coarse while residual/direction memory alters write timing. Code/data were withheld in the inspected version.
- Tao Zhang et al., “DAMP: Decay-Aware Mixed-Precision Recurrent-State Quantization,” arXiv:2608.27513v2, Eqs. (2), (8)–(15). It covers decay-persistence allocation; no confirmed author code in the bounded v1 audit.
- Bingchen Yao et al., “STEPQuant: When and Where Errors Matter in Delta-Rule Recurrent State Quantization,” arXiv:2609.38169v1 and author repository `Dreamer-Toby/STEPQuant` at commit `61f24c9c2bc188b60a6c7525e7f86c7459bc737d`. `allocation.py`, `calibration.py`, and `kernels/writeback.py` cover discrete allocation, lifetime/readout calibration, pivots, dual-axis formats, and persistent serving write-back.

These works do not state the exact R10 v2 finite-horizon identity, but the identity is a specialization/control inside a heavily covered mechanism family, not sufficient evidence for a new method.

## 6. Functional comparison

| Work/object | State transition | Feedback/allocation object | Mathematical overlap with R10 v2 | Residual difference |
|---|---|---|---|---|
| R10 v2 | frozen Delta affine `A_t` | previous quantization residual through `F_t` | exact error transfer; conditional Gramian/covariance and spectral projection under an `F`-invariant residual-law coupling | Delta factorization, residual-endogeneity warning, and explicit equal-state boundary |
| Classical ESS | general state-space digital filter | first/higher-order roundoff-error feedback | same noise-shaping family | hardware/filter realization emphasis |
| Ohno et al. 2016 | static uniform quantizer plus downstream LTI system | strictly causal error-feedback filter under fixed bits/range | frequency-weighted output MSE and rate–distortion optimization | LTI quantizer/filter setting, not Delta memory semantics |
| Zheng et al. QEF | deterministic/random/asynchronous graph state-space recursion | optimized diagonal feedback | explicit quadratic output-noise minimization and closed-form weights | graph communication rather than Delta memory |
| 2609.04490 | coarse recurrent visible state | residual/direction write-back | causal residual memory and write-timing effect | no transition-matched full `A_t` claim |
| DAMP/STEPQuant | Delta/KDA/GDN state | offline persistence/readout-aware formats | future consequence weighting and bit allocation | not online residual-feedback coefficient optimization |

Adjudication: the exact Delta specialization is mathematically useful, but the core operator and objective are covered by at least three functional families: general state-space/graph error-spectrum shaping, fixed-rate error-feedback quantization, and recurrent-state coarse-visible feedback. DAMP/STEPQuant add an adjacent allocation family. Under the collision contract this is a known-mechanism specialization/control, not an active candidate.

## 7. Author interfaces and computational boundary

No author implementation was confirmed for Vaidyanathan 1985, Zheng et al. QEF, DAMP, or arXiv:2609.04490 within this bounded pass. STEPQuant remains the only pinned author implementation among the immediate R10 neighbors.

For Delta,

`A_t r = D_t r - beta_t k_t (k_t^T D_t r)`

can be applied without forming a dense matrix, but it still costs another residual-state transition and full residual traffic unless `F_t` is restricted. A scalar/diagonal/rank-limited `F_t` is only a weighted approximation. This computational specialization is not itself a new capability and currently lacks a theorem showing matched-total-cost dominance over direct state coding or known QEF/ESS implementations.

The R10 coefficient optimum is also conditional on comparing feedback choices under a common exogenous residual process (or an equivalent `F`-invariant covariance/spectrum). Ordinary deterministic quantization makes the residual endogenous to the feedback input; the inspected nearest work does not remove that deployment boundary for Delta.

## 8. Native measurement feasibility

- Graph-filter QEF has its own native filter-output noise objective, but this does not measure semantic Delta memory, fact validity, or language-model endpoint quality.
- The v1 downstream assets—bAbI, LAMBADA, RULER, reasoning, and code tasks—can measure task endpoints only after a legitimate quantized recurrence exists. They do not natively expose quantization residual spectra, feedback matrices, future readout Gramians, equal-state transition classes, or source validity.
- STEPQuant’s released path remains too large to count as an affordable ready test on the retained single-RTX-2080-Ti background, and its endpoint scores would not by themselves separate representation capacity from operator compatibility.
- No new benchmark, case, label, metric, result, or executable experiment design was created.

Measurement status: a falsifiable mathematical control exists, but an affordable native Delta object that isolates its mechanism remains missing.

## 9. Search record and decision

Search date/cutoff: 2026-10-11. Query families included exact titles and combinations of `state-space error feedback quantization`, `error spectrum shaping`, `closed-form feedback coefficient`, `graph filter quantization noise`, `fixed-rate error-feedback quantizer`, `Delta recurrent state residual`, and GitHub repository searches for both Zheng titles. Primary arXiv/KAUST/IEEE bibliographic sources and the already pinned STEPQuant author repository were used. Search results were deduplicated by underlying work; arXiv:2412.05651 is treated as the conference predecessor of the extended 2506.01404 line, not a separate collision count.

No collision-free Delta-specific method remains after this pass. R10 v2 should be parked after attempt 2 with candidate delta zero. A third attempt requires new evidence for a noncommuting low-rank Delta feedback construction with lawful prefix estimation, matched total storage/traffic/compute advantage, and an existing native measurement object; another scalar/diagonal coefficient or residual bit split would repeat known ESS/QEF.
