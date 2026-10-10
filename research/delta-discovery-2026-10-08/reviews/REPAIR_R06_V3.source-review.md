# Independent source, collision, and native-measurement review — R06 v3

- Reviewer identity: `/root/r06_v3_source_review`
- Assignment: check primary formula and author-interface support, closest-work collisions, novelty scope, and native measurement availability.
- Artifact SHA256: `26fed27d5e5091c93bd8428c76b0dde5c7e6fd49dc930911247a90c311cd3ceb`
- Source audit: `research/delta-discovery-2026-10-08/sources/R06_V3_SURVIVAL_MARGIN_SOURCE_AUDIT.md`
- Source-audit SHA256: `50d1c6adc7801e4244d104dfeec257114391f081cf9039605045274e4ff1f304`
- Final-byte verdict: **PASS for conditional source support and collision classification; FAIL for novel-updater/candidate admission.**

## Review reasoning

The final source audit accurately distinguishes the original DeltaNet residual recurrence from the pinned Parallel DeltaNet/FLA layer defaults. At the pinned FLA commit, L2 normalization and the sigmoid beta are layer defaults; the optional negative-eigenvalue setting doubles beta, while the low-level naive kernel consumes already-produced keys and beta. No global positive singular margin follows from an unconstrained finite-logit sigmoid.

Grazzi et al. directly cover the generalized-Householder `I-beta kk^T` spectral family and the negative-eigenvalue branch. i-ResNet and Residual Flows cover the general invertible/bi-Lipschitz residual mechanism. Imberg et al., Active Testing, and classical PPS/Neyman allocation cover adjacent inverse-probability and proposal-allocation mechanisms, but do not themselves prove the packet's independent-Bernoulli rectangular-robust factor. The remaining Delta-specific contribution is therefore a useful debugging theorem tying one exact rank-one singular factor to finite-horizon survival, audit allocation, and current-key residual plasticity—not a new architecture, estimator, or demonstrated capability.

Existing audited editing and temporal-memory assets do not natively expose the required joint tuple, enforced effective singular margin, paired update/no-update outcomes, or frozen-path/full-Jacobian comparison. Empirical effect remains unknown; no benchmark or result was manufactured.

## Required corrections resolved

The reviewer requested precise FLA interface wording and a narrower description of the Imberg/Active Testing relation. Both changes are present in the bound final artifact and source audit. No remaining source, collision, or measurement edit is required.
