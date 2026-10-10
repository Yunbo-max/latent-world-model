# R20 v2 independent final-byte source review

Reviewer: `/root/r20_sources`. Assignment: independently inspect primary papers and pinned author interfaces, then review the exact artifact, source audit and screen without editing repository files or executing project/model code.

- Artifact SHA256: `dfe5b8b1cde3c0798432411e76178f5dc87925cae4510856df1862c5a1cf367c`
- Source-audit SHA256: `cfab7352929684c72bb70793b9c13fac71e23c9a79b0a445ab57a228adfbe23f`
- Screen SHA256: `b70b3f7e1d8a80ccfa22975eaedf22f9177f98ce1813e75c8a5dbc09ae0c307b`
- Verdict: **PASS for source scope and park disposition only**.

M-FAC, SENG and WoodFisher adequately establish the collision for past-gradient empirical-curvature sketches, damped small-Gram/Woodbury inversion and matrix-free inverse products. The audit correctly distinguishes a general per-example gradient outer product, the usual observed-label empirical Fisher for NLL/log-likelihood scores, and GGN; it does not infer future curvature from prefix gradients.

OGD, GEM and SketchOGD—including the corrected Min–Wright–Bernstein–Azizan arXiv:2305.16424v2 record—adequately cover past-gradient constraint/projection and fixed-budget sketch controls. No additional source omission is blocking the conservative disposition.

The exact current-key Delta equality constraint and factorized action remain a narrow interface-level distinction, but the projected Woodbury formula is standard and D03/Step2 already subsumes the general edit coordinate. Native benchmarks do not expose the fast-state curvature target, KKT optimum or same-state counterfactual; the stated measurement gap is valid.

Supported disposition: **conditional theorem/control; park after substantive attempt 2; zero candidate increment; empirical effect unknown**. This PASS validates source coverage and disposition only; it does not establish originality, prefix-to-future curvature transfer, same-budget utility or experimental success.
