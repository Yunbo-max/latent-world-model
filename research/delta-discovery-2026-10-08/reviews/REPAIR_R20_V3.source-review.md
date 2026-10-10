# Independent source and novelty review — R20 v3

Reviewer: `/root/r20_sources`  
Assignment: primary full-formula, actual author-code, collision, measurement and novelty audit; reviewer did not author repository files.  
Artifact: `research/delta-discovery-2026-10-08/repairs/R20_SPECTRAL_TRANSFER_CERTIFICATE.v3.md`  
Artifact SHA256: `9fff175d5a25aa905ba1cc8efa11ae5d6bf56a1f66539619f4f0ba7481aedde7`  
Source audit: `research/delta-discovery-2026-10-08/sources/R20_V3_SPECTRAL_TRANSFER_SOURCE_AUDIT.md`

## Verdict

**CONDITIONAL-MATH PASS; NOVELTY/CANDIDATE FAIL; PARK.** The source record supports using a spectral sandwich as an explicit assumption. It does not support inferring that sandwich from an arbitrary Delta prefix.

## Primary-source findings

1. Ye--Luo--Zhang, subsampled Newton, Iterative Hessian Sketch and Adaptive Newton Sketch already use relative Loewner/sketch approximation to transfer an approximate quadratic or Hessian into optimization guarantees under stated sampling and regularity assumptions.
2. PROMISE explicitly assumes spectral approximation and implements sampled, damped low-rank curvature with infrequent refresh. Its pinned author code exposes the curvature update and inverse action that form the closest stale-curvature mechanism collision.
3. Hessian averaging supplies a stationary-objective/martingale-noise route; online Newton and dynamic-regret work supplies convexity, feedback, path-variation or prediction-error routes. Those assumptions are materially stronger than prefix measurability.
4. M-FAC/SENG/WoodFisher and OGD/GEM/SketchOGD from the v2 audit remain direct controls for past-gradient small-Gram inversion or projection. Empirical Fisher must not be described as GGN without the appropriate factorization.

## Scope correction

The robust identity reviewed here is the **absolute worst-case homogeneous quadratic cost** over a symmetric Loewner interval. It does not imply that minimax regret, a competitive-ratio objective with another comparator, a linear-term loss, or nonlinear future dynamics select the same action.

The sharp affine constant in the artifact is independently established by the math review; none of the searched source collisions makes that constant a deployable update rule. The information problem has merely moved into the premise \(m\widehat H\preceq H\preceq M\widehat H\).

## Measurement and novelty

Generalized-eigenvalue coverage, future/surrogate cost ratio, drift/path length, sketch rank and staleness are derived diagnostics. The already audited native Delta/language endpoints do not expose the true future \(H\), smallest valid radius, or same-state counterfactual optimum. No result was fabricated.

Final status: useful conditional theorem and prefix-impossibility control; zero candidate increment; reopen only with a lawful online certificate or explicit measurable drift/stationarity premise.
