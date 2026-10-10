# R10 v1 independent final-byte source and measurement review

- Reviewer: /root/r10_source_review
- Scope: primary sources, author implementation, originality collision, native measurement
- Source artifact: research/delta-discovery-2026-10-08/sources/REPAIR_R10_EQUAL_BIT_RESIDUAL_SOURCE_AUDIT.md
- Source SHA256: 310d36ac4942281fc44eaffd9116b3a9042f0e7acffb4d8be0a9ef8603552758
- Linked math SHA256: 76ed51db1a0848a234f6e0d8176ff974a48371ad27d55d56c82d3961c0164763
- Outcome: PASS

The initial review returned REVISE because a carriage-return byte corrupted \(\rho_t\), STEPQuant equation roles were conflated, collision-family counting was ambiguous, and the audit risked equating STEPQuant's one-step row impact with the full finite-horizon Gramian.

The final-byte review verified:

- arXiv:2609.04490v1 S18–S23, its 4-bit recurrence-visible state, matched stored-bit comparison, operator/interface interpretation, hardware-cost disclaimer, and withheld code/data status;
- DAMP arXiv:2608.27513v2 equation order, Eqs. 8–15 error/risk construction, 9.9-bit FP16/INT8+SR allocation, and absence of confirmed public author implementation in the bounded audit;
- STEPQuant arXiv:2609.38169v1 Eq. 8 allocation, Eqs. 9–10 one-step row impact, Eqs. 11–14 dual-axis fitting, Eqs. 17–18 calibrated distortions, and its explicit distinction from DAMP;
- author repository commit 61f24c9c2bc188b60a6c7525e7f86c7459bc737d and the inspected allocation, calibration, and writeback blob/function mappings;
- exactly two distinct collision families: coarse-visible auxiliary write timing, and persistence/readout-aware allocation; DAMP and STEPQuant are members of the same second family;
- STEPQuant does not instantiate R10's complete finite-horizon observability Gramian, but this theoretical residual alone does not yield a distinct deployed method;
- public benchmark interfaces exist, yet the 27B/48B four-GPU route is not demonstrated feasible on the retained single RTX 2080 Ti, and existing bAbI/LAMBADA/RULER endpoints do not identify the theorem/operator mechanism by themselves.

No source, collision-counting, or benchmark-feasibility correction remains. PASS does not convert the control into a candidate or a measured result.

