# R02 repair-line screen v2 — compressed sequential-DR state

Date: 2026-10-10  
Parent: `R02_RANDOMIZED_ACTION_CREDIT.v1.md`  
Attempt: 2/3  
Stage: Web mathematics and source audit only; no model execution.

## Preserved result and exact remaining defect

R02 v1 correctly repairs passive counterfactual non-identification by adding randomized, propensity-logged Delta actions and real delayed outcomes. Its third reopen condition asked whether a compressed Delta state could remain sufficient for sequential doubly robust (DR) evaluation at lower state/compute cost.

The unresolved step is not the DR identity. It is whether a proposed quotient retains every object the identity conditions on: target and behavior action probabilities, conditional future loss, and the action-conditioned law of the next quotient. Preserving only a future-loss readout is insufficient in general.

## Screened patches

| Patch | Mathematical consequence | Decision |
|---|---|---|
| A. Outcome-only Delta quotient | Preserve only the conditional delayed-loss predictor on `XW`. | Rejected as a generic DR repair. Coarsening can destroy sequential exchangeability; the one-step bias is exactly a within-cell propensity–outcome covariance divided by the coarse propensity. |
| B. Joint causal quotient | Require target/behavior policies and outcome/value objects to factor through the quotient, plus action-conditioned recursive transition closure; alternatively charge an exact propensity-ratio ledger as extra state. | **Selected for full derivation.** It gives exact positive conditions, counterexamples, and a Delta right-quotient rank boundary. |
| C. Learned compact recurrent summary without exact conditions | Train a recurrent encoder and check endpoint accuracy. | Kept only as an unverified approximation lead. It does not establish OPE identification, double robustness, or lower total cost; a direct recurrent Q/policy model is the same-information control. |

## Decision

Patch B repairs the mathematical scope but collides directly with Markov state abstraction, policy/behavior irrelevance, bisimulation/homomorphism, and recent OPE-specific abstraction work. The Delta specialization is a useful audit: a right quotient must include policy-propensity and recursively transported value/transition covectors, so it can be strictly wider than an outcome-only quotient and can be full-width. This is attempt 2/3, retained as theory/control with candidate delta zero.

