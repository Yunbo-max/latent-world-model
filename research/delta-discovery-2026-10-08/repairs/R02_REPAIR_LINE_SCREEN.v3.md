# R02 repair-line screen v3 — quantitative approximate causal quotient

Date: 2026-10-10  
Parent: `R02_CAUSAL_DR_QUOTIENT.v2.md`  
Attempt: 3/3  
Stage: Web mathematics, primary-source comparison and native-measurement feasibility only; no model execution.

## Preserved result and exact remaining defect

R02 v2 correctly proves the exact quotient-only AIPW coarsening bias

\[
B_a(q)=\frac{\operatorname{Cov}(\mu_a(H),m_a(H)\mid q)}{\bar\mu_a(q)}
\]

and states strong exact sequential quotient conditions. Its remaining defect is practical but mathematical: exact fiber constancy is rarely checkable, while simply observing a small endpoint error gives no tolerance or horizon accumulation guarantee.

## Screened patches

| Patch | Mathematical consequence | Decision |
|---|---|---|
| A. Small reconstruction loss | Treat low `S -> SW -> S` error as causal/DR sufficiency. | Rejected. It neither bounds within-cell propensity–outcome covariance nor preserves target-reachable reward/value distinctions. |
| B. Quantitative two-part certificate | Bound one-step coarsening bias by within-cell conditional variances, and separately bound fixed-policy target-value abstraction error by uniform reward and transition defects; specialize the dynamic defect to Delta `q=SW`. | **Selected for full derivation.** It is a real scope repair and yields sharp/finite-horizon bounds, but not a full sequential-DR theorem. |
| C. Behavior-average defect | Estimate only average abstraction error under the logging policy. | Rejected as a generic guarantee. A rare behavior cell can have `O(delta)` average defect but `O(1)` target-policy value error; a concentrability factor exposes the missing cost. |

## Decision

Patch B replaces an all-or-nothing exact quotient claim with a quantitative debugging certificate. The one-step causal term and the dynamic state-abstraction term remain distinct estimands and are not added together as a claimed doubly robust guarantee. The certificate also reveals that its required fiber variation, uniform target-reachable defect, propensity ledger and side state may cost as much as full-history DR or direct recurrent value prediction.

Approximate homomorphism/bisimulation, simulation bounds and OPE state abstraction cover the main mechanism. The Delta residual is a precise coefficient-leakage decomposition for `q=SW`, not a new updater or a proved matched-cost advantage. R02 therefore reaches its bounded third attempt and is parked as a useful conditional control with candidate delta zero and empirical effect unknown.

