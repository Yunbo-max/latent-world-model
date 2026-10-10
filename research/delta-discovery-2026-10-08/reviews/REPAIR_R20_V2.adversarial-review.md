# R20 v2 independent final-byte adversarial review

Reviewer: `/root/r20_adversarial`. Scope: independent read-only review; no repository edits or model/software execution.

- Artifact: `research/delta-discovery-2026-10-08/repairs/R20_PREFIX_CAUSAL_LOWRANK_CURVATURE.v2.md`
- Exact reviewed SHA256: `dfe5b8b1cde3c0798432411e76178f5dc87925cae4510856df1862c5a1cf367c`
- Screen: `research/delta-discovery-2026-10-08/repairs/R20_REPAIR_LINE_SCREEN.v2.md`
- Exact reviewed screen SHA256: `b70b3f7e1d8a80ccfa22975eaedf22f9177f98ce1813e75c8a5dbc09ae0c307b`
- Verdict: **PASS, scoped to a parked conditional theorem/control only; candidate increment zero.**

The exact projected Woodbury derivation, feasibility, KKT identity, optimum value and nonnegative declared-surrogate improvement check algebraically. The factorized feature orientation, Gram, matrix action, rank bound and exact recovery of the v1 rank-two witness are consistent.

The final bytes correctly require every feature to be measurable before the action and exclude unrevealed answers, future traces, validity oracles and unobserved counterfactuals. They also expose the unavoidable choice between causal-but-stale stored features and costly replay/recomputation with old inputs and targets.

The two precision fixes are present: a generic `g_i g_i^T` is a per-example gradient outer product and becomes the usual empirical-Fisher object only for an NLL/log-likelihood score, while GGN requires `J_i^T C_i J_i`; both scalar counterexamples explicitly set `e=1`.

The rotated-curvature example correctly proves that an exact stale-surrogate minimizer can be worse than Euclidean Delta under drift. The `k=(1,epsilon)` example correctly produces an approximately `1/epsilon`-norm action when `rho >> lambda/epsilon^2`, so damping, trust-region, norm or condition checks remain necessary. Prefix-only features also cannot distinguish two worlds with the same prefix and opposite future validity.

State/compute accounting explicitly charges feature extraction and distinguishes factorized from unstructured storage. Mandatory controls include diagonal Fisher/EWC, hard projection, projected natural gradient/ONS/RLS, K-FAC/Shampoo/sketches, rank-r Delta, L-BFGS, constrained CG, replay and direct factor prediction. Native tasks expose endpoints, not fast-state curvature or paired actions.

The surviving result is therefore limited but valid: a prefix-causal exact constrained low-rank quadratic identity plus explicit failure boundaries. M-FAC, SENG, WoodFisher, natural-gradient projection and existing R20/Step2 machinery create major collisions; future-validity transfer and matched-total-cost advantage remain unresolved. Final disposition: `conditional theorem/control; substantive attempt 2; parked; zero candidate increment; empirical effect unknown`.
