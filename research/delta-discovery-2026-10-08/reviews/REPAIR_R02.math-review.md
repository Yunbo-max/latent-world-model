# R02 v1 independent mathematical review

- Reviewer: `/root/r02_counterfactual_math`
- Assignment: independent dimension, identification, variance, sequential-scope, counterexample and cost review; read-only
- Artifact: `research/delta-discovery-2026-10-08/repairs/R02_RANDOMIZED_ACTION_CREDIT.v1.md`
- Verified artifact SHA256: `b3460e4b433cd7b56302f3587cc7664f39cd9858f4c273401da68f54e49686da`
- Verdict: **PASS — ACCEPTED_CONDITIONAL_CAUSAL_CONTROL**
- Candidate admission: `0`

## Checks and corrections actually performed

The first reviewed draft was not passed. The reviewer required: an explicit sequential-DR equation and terminal condition; restriction of the efficient-influence variance to independent/reset units; dependence-aware scope for persistent streams; an explicit discount convention for the tail bound; removal of a false Delta-specific-theorem implication; and a dimensionally consistent coupled-state action map. The final artifact incorporates every correction and was rehashed before this review.

On the bound bytes:

1. \(S_i^0,S_i^1\in\mathbb R^{d_k\times d_v}\), while \(F_a\) returns the full coupled tuple \(Z_i^a\); the codomain is consistent.
2. Known-propensity finite-action AIPW and the binary conditional-effect pseudo-outcome are correct under consistency, randomization and positivity.
3. The delayed-outcome correction is valid under delay-MAR and censoring positivity, with the two stated robustness alternatives. Informative unobserved delay remains unidentified.
4. The displayed efficient-influence variance is correctly limited to independent/reset one-decision units. Persistent streams are explicitly routed to martingale/dependence-aware inference.
5. The total-effect interpretation under a common continuation policy is correct. The sequential-DR cumulative-ratio loss estimator, terminal value and target-reachable exchangeability/positivity conditions are stated, and the reduction to a single initial ratio when later policies coincide is sound.
6. Under the stated convention \(\sum_{h\ge1}\gamma^{h-1}\ell_{i+h}\) and \(|\ell|\le L\), the action-effect tail bound \(2L\gamma^H/(1-\gamma)\) is correct.
7. The no-overlap, individual-sign, mediation, persistent-interference, informative-delay, noncompliance and horizon-reversal counterexamples all survive.
8. The final nuisance condition correctly scopes finite-sample unbiasedness to fixed, cross-fitted or pre-action-predictable outcome/censoring/value estimates and separately evaluated learned target policies.

## Final distinction

The repair genuinely escapes the passive-observation no-go by adding randomized external evidence, but the estimator is generic causal/OPE machinery instantiated with Delta actions. It does not recover historical source identity or prove a Delta-specific statistical advantage. Native measurement, sample efficiency and empirical effect remain unknown. No further mathematical edits are required for this scoped control.

No files were edited by the reviewer and no project code, tests, models, data, scoring or experiments were executed.
