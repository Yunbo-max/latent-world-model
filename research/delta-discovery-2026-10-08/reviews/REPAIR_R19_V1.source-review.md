# R19 v1 independent final-byte source, distinctness, and measurement review

- Reviewer: `/root/r19_final_source_review`
- Reviewed screen: `../repairs/R19_REPAIR_LINE_SCREEN.md`
- Screen SHA256: `e14b8689f9d544ed05f6a0c8b2e5018660bbc28adfc5e28808d67c73d57c6745`
- Reviewed artifact: `../repairs/R19_SWITCHED_PROTECTION_FIBER.v1.md`
- Artifact SHA256: `c589931307d5821b6abd3f4542c21fd6d5a98af5e43d2764cb3d7a22efa93bf6`
- Reviewed source audit: `../sources/R19_SWITCHED_PROTECTION_FIBER_SOURCE_AUDIT.md`
- Source-audit SHA256: `8056962e86bcf3a94ddcb2b3d1a41de7be88562f019b0654d4d3c9773da2ce6f`
- Verdict: **PASS — decisive switched-seminorm collision; changed-kernel Delta debugging corollary only; candidate delta zero**

The first source pass found a missing decisive neighbor and did not pass the earlier audit. The final bytes now inspect Baum, Liu, Qin and Stursberg, arXiv:2512.16338v1: §2.1 Definition 6/equations (15)--(19) use PSD seminorms and invariant kernels; §3.1 Lemma 1/equations (22)--(28) use a common kernel, cross-mode `P_new preceq beta P_old`, and dwell/leave conditions; §3.2 Theorem 2/equations (60)--(63) lifts a separating seminorm family to full-state contraction. This directly covers the R19 switched-seminorm, comparison-factor, and dwell-time skeleton.

The retained difference is consequently narrow: Baum et al. require the compared mode metrics to share the relevant kernel, whereas a Delta protection release may change it. R19 gives the resulting infinite-factor witness and the reset/side-ledger coordinate obligation. It is not a new switched-contraction framework, updater architecture, release-validity estimator, or originality-certified theorem family. Internal Step2/R08/R13/R18 already cover the fixed fiber, decision, dynamic readout, and complete-state quotient components.

Branicky, Della Rossa--Tanwani, and Veer--Poulakakis are correctly marked supportive rather than formula-level evidence; Baum and the fully inspected Hespanha--Morse PDF provide the formula evidence. The audit records its date, exact bounded query strings, fixed URLs, and non-exhaustive scope. No author-code interface is fabricated for a theorem-only result.

The fixed bAbI, LAMBADA, RULER, BABILong, LongMemEval, SEAL, and temporal-editing endpoints do not natively expose `P_sigma`, reset tangents, cross-kernel truth, or paired same-state mode interventions. Derived JVP/energy instrumentation would not be native evidence. The correct disposition is conditional theorem/control, park after attempt 1, zero active/admitted/selected increment, empirical effect unknown.
