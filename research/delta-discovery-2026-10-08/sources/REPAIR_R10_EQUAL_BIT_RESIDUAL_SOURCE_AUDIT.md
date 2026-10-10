# R10 source, implementation, originality, and measurement audit

Cutoff: 2026-10-10. Scope: equal-total-bit transported residuals, coarse-visible error feedback, persistence/readout-weighted recurrent-state quantization. This is a bounded primary-source audit, not an exhaustive claim that no other work exists.

## 1. Lineage source retained

- Parent: rejected/D04_COMPENSATION_COLLISION.md, exact main blob 61bc4bc29f8724793ea9fed20a1d11c80c4e404b at parent commit ca384afc014e4222b47c9935677788b59635669d.
- Parent source record: sources/D03_D04_SOURCE_AUDIT.md (reused; not rewritten).
- Retained failure: unchanged feedback does not transport the residual through \(A_t\); exact transported compensation uses a second full state and had no equal-bit advantage.

## 2. Recurrent-state write-back paper

Primary full text:

- Ismail Erbas, Xavier Intes, Vikas Pandey, “When Quantization Breaks Memory: Recurrent-State Write-Back in Low-Precision Temporal Inference,” arXiv:2609.04490v1, 2026-09-03: https://arxiv.org/html/2609.04490v1
- Read depth: D2/D3 for §§2.2–2.3, S5, S8, S10, data/code availability.

Verified formulas and boundaries:

- S18–S19: \(q_t=Q_B(h_t+e_{t-1})\), followed by clipped residual \(e_t=\operatorname{clip}(h_t+e_{t-1}-q_t,-\Delta_B,+\Delta_B)\).
- S20–S23: \(q_t=Q_B(h_t+\rho_{t-1})\), \(u_t=h_t+\rho_{t-1}-q_t\), \(\rho_t=Q_{\rho,k}(u_t)\), and \(\Delta_{\rho,k}=\Delta_B/2^k\), with \(2^k\) uniformly spaced residual levels over the stated half-step interval.
- S5/S10 compare \((4+k)\)-bit visible state against a 4-bit visible state plus \(k\)-bit residual or direction memory. The paper explicitly interprets observed differences as operator/interface compatibility, not intrinsic superiority of auxiliary bits, and explicitly says storage matching does not match arithmetic, logic, routing, energy, or total-model memory.
- Crucially, the recurrence-visible state remains on the 4-bit grid; the auxiliary state changes when later 4-bit writes occur. This is equation (4) in the R10 card, not the transported \(W+C\) recurrence.
- The paper states code/checkpoints/data will be released upon acceptance and withholds links for double-blind review. No author implementation was available in this audit; no file/function mapping is claimed.

Impact: major collision for the auxiliary-feedback/operator route, while also supporting the R10 separation between interface-preserving feedback and fine decoded state.

## 3. DAMP

Primary full text:

- Tao Zhang et al., “DAMP: Decay-Aware Mixed-Precision Recurrent-State Quantization,” arXiv:2608.27513v2, 2026-09-30: https://arxiv.org/html/2608.27513v2
- Read depth: D2/D3 for §§3.1–3.3, 4.1–4.2, 5.1–5.2, Appendix A, limitations.

Verified mechanism:

- Eq. 2 keeps the actual GDN/KDA order \((I-\beta kk^\top)\Lambda S+\beta kv^\top\).
- Eqs. 8–13 derive accumulated quantization error \(\Delta S_t=A_t\Delta S_{t-1}+R_t\) and its ordered propagation.
- Eq. 14 measures per-key-channel local squared reconstruction error.
- Eq. 15 defines an accumulated-error risk score by multiplying local error by products of future learned decay over a finite calibration horizon.
- Under a fixed storage budget it stores selected high-risk channels in FP16 and the rest in INT8+scaling/reordering; the reported effective storage is 9.9 bits per state value.

Implementation status:

- The arXiv record and inspected full text provide method and kernel descriptions, but no author GitHub link was confirmed in the paper record or bounded repository search. No implementation file/function claim is made.

Impact: major functional collision with the persistence-weighted allocation half of R10. DAMP uses decay-only retention rather than the full query observability Gramian.

## 4. STEPQuant paper and author code

Primary full text:

- Bingchen Yao et al., “STEPQuant: When and Where Errors Matter in Delta-Rule Recurrent State Quantization,” arXiv:2609.38169v1, 2026-09-29: https://arxiv.org/html/2609.38169v1
- Read depth: D2/D3 for §§2–4, Appendix A–C, concurrent-work discussion.

Verified mechanism:

- Eq. 8 minimizes lifetime-weighted candidate-format distortion under a nominal bit budget.
- Eqs. 9–10 define one-step query/readout row impact through \(g_t=A_t^\top q_t\) and \(\omega_i=\mathbb E[g_{t,i}^2]\).
- Eqs. 11–14 define key-row/value-column dual-axis fitting; Eqs. 17–18 define architecture-specific calibrated distortions used by the allocation; FP16 pivots protect difficult units.
- Appendix B preserves the actual Delta order and separates persistence from spatial/readout impact.
- The paper explicitly identifies DAMP as concurrent work and distinguishes STEPQuant by combining lifetime allocation with one-step readout-aware dual-axis fitting. It does not instantiate the full finite-horizon observability Gramian in R10 equation (5).

Author repository and pinned inspection:

- Repository: https://github.com/Dreamer-Toby/STEPQuant
- Inspected commit: 61f24c9c2bc188b60a6c7525e7f86c7459bc737d (2026-10-01); tree ebdd3e3b828d4a32fe3b7db3b27a0f7575a599f3 from the prior connector receipt.
- stepquant/allocation.py, blob 8260a7ccb8cb3f7bd0a0d7568774b7c340b8d0e1: allocate_dp performs exact integer dynamic programming for GDN; allocate_lagrangian performs a feasible Lagrangian allocation plus discrete gain-per-bit repair for KDA.
- stepquant/calibration.py, blob fc279e859e2e464a5d1efd604b763e001fa78587: LayerStatistics.observe accumulates row impact and log decay; _distortions fits candidate formats; calibrate multiplies distortion by lifetime_weight, selects FP16 pivots, and calls the allocator. The module docstring says calibration uses recurrent traces without quantized feedback.
- stepquant/kernels/writeback.py, blob a024c2582cc17ab46e24bff3a185840f9d62b92a: defer_writeback, CapturedWrites, and WritebackGraph implement bounded asynchronous persistent write-back scheduling. This is actual serving-interface code, not proof of the paper's numerical results.
- README.md at the pinned commit reports the tested stack SGLang 0.5.12, PyTorch 2.11.0, Triton 3.7.1, and a four-GPU Qwen example. No command was executed in this Web/math phase.

Impact: STEPQuant is a decisive stronger collision within the same persistence-aware allocation family as DAMP. R10's separable KKT derivation is a simpler continuous relaxation of an allocation problem whose discrete lifetime-aware and one-step readout-aware version is already implemented. The full finite-horizon Gramian remains a theoretical residual, but it does not by itself rescue a distinct deployed method claim.

## 5. Functional comparison

| Object | Recurrence-visible state | Extra state / allocation | Essential effect | R10 relation |
|---|---|---|---|---|
| Transported split | decoded \(W+C\) | residual code | finer decoded codebook; exact only with exact residual | same-cardinality direct-codebook equivalent |
| 2609.04490 residual memory | coarse \(W\) | finite residual/direction memory | changes future coarse write timing | different operator; already covered |
| DAMP | mixed FP16/INT8 state | offline channel selector | local error × decay persistence | covers persistence allocation |
| STEPQuant | mixed 2/4/6/8/16-bit state | lifetime, row-impact, pivots, dual-axis scales | error magnitude × lifetime × one-step readout impact | stronger member of same allocation family |

Adjudication: exactly two distinct major functional families apply—auxiliary coarse-visible write timing and persistence/readout-aware bit allocation. The only retained R10 contribution is the scoped representation-equivalence/operator-boundary theorem. It is useful as a control and no-go result, not a method candidate.

## 6. Native measurement feasibility

- The write-back paper uses a fluorescence-lifetime GRU task and states its code/data are withheld pending acceptance. Its matched-storage results are not currently reusable as a public native Delta benchmark.
- STEPQuant releases task configs and graders for AIME 2026, GPQA-Diamond, LiveCodeBench v6, EvalPlus and other tasks, but the reported Qwen/Kimi path uses 27B/48B-class models and a four-GPU serving example. That is outside the retained single-RTX-2080-Ti background and cannot be presented as an affordable ready test here.
- Existing project bAbI/LAMBADA/RULER assets can compare downstream scores only after a legitimate implementation exists. They cannot prove the exact frozen-affine identity or distinguish decoded-codebook equivalence from operator-interface compatibility without native quantized-state instrumentation.
- No new benchmark, samples, labels, metric, result, or executable experiment matrix was created.

## 7. Search scope and unresolved evidence

Queries covered exact titles/identifiers plus combinations of recurrent-state quantization, error feedback, residual memory, matched storage, decay/lifetime allocation, key-row impact, and Delta-rule state write-back, through 2026-10-10. Primary full texts and the available STEPQuant author repository were inspected. This bounded audit does not claim exhaustive literature coverage.

Unresolved:

1. no public author code was confirmed for DAMP or arXiv:2609.04490;
2. no affordable native benchmark was found that separately identifies the R10 representation theorem and operator-compatibility effect;
3. no primary work was found in this bounded pass that gives the exact same-cardinality decoded-codebook theorem for transported Delta residuals, but the theorem alone remains a control and cannot override the two method-family collisions.

Decision: park R10 attempt 1; candidate count remains unchanged.

