# R16 v3 independent final-byte source and novelty review

- Reviewer: \`/root/counterfactual_source_audit\`
- Review date: 2026-10-11
- Artifact SHA256: \`48ec9e9e1c94191df3e8e5e8c87e810d4119d9d902ec61dd63e14d8c39ea0b4d\`
- Source-audit SHA256: \`e58768e3c40dc7ca8c26a7e0926a5b9a8b811b01401c83c543fdd99597407465\`
- Execution: static reading of primary sources, fixed author-code commits and repository mathematics only; no project execution.
- Verdict: **PASS; narrow theorem/debug residual only.**

Martin and Cundy, arXiv:1709.04057v2, section 1 and Algorithm 1 support the general associative affine-scan control, while section 2.1 exposes the dense matrix-composition cost. The final audit now correctly limits the pinned author implementation \`eamartin/parallelizing_linear_rnns@da10de34701313e5556d67f4df4aacb76983e20c\`: its header stores \`decays\` and \`impulses\` as \`n_steps × n_dims\` arrays and its CUDA kernel composes scalar pairs independently by coordinate. It is therefore an operational control only for the diagonal/elementwise special case, not a generic dense \(r\times r\) core implementation.

Yang et al., arXiv:2406.06484v6, and the pinned FLA author implementation \`fla-org/flash-linear-attention@a7880060012c862d58575ee23f613cafcd728d03\` support ordered Delta/WY as a direct control. The recorded \`prepare_wy_repr_fwd\`, \`recompute_w_u_fwd\` and chunk consumption interfaces are accurate. They do not make KDA's ordered decay/write equal to R16's simultaneous exponential.

Internal collision accounting passes: R10 already covers common invariant carriers and invariant hulls; R11 covers lazy low-rank overlays, additive rank growth, recompression and transported error; R12 covers finite-family closure and the future-bridge boundary. R16's supportable residual is restricted to its PSD-exponential sharp commuting rank-growth witness, the shared-carrier specialization and the natural-flow contraction certificate.

Those residuals do not establish a new updater, scan primitive, low-rank maintenance algorithm, semantic retain/revise mechanism, hardware advantage or architecture admission. Existing native tasks do not jointly expose the simultaneous generator, prefix-known carrier, exact correction ranks, recompression/backward errors, semantic validity and matched kernel traffic. Synthetic fixtures would verify identities, not scientific effect.

**Disposition:** accept as terminal conditional theorem/control, attempt 3/3 exhausted, candidate delta zero, empirical effect unknown.
