# R01 repair-line screen v3 — final bounded attempt

Date: 2026-10-10  
Parent: `R01_VALUE_SPAN_AND_CREDIT_QUOTIENT.v2.md`  
Attempt: 3/3  
Stage: Web mathematics and source audit only; no model execution.

## Preserved result and exact remaining defect

R01 v2 correctly characterized a **fixed** right quotient `L_W(X)=XW`: for the scalar-gated Delta tangent

\[
J_j[X]=A_jX+K_j\langle G_j,X\rangle_F,
\]

exact one-step closure requires the gate covector and requested credits to lie in the chosen value-side span. Its unresolved step was not algebraic correctness, but the choice of `W`: taking the raw union of all local gate/loss row spaces can be unnecessarily large, while choosing it causally from a prefix cannot in general anticipate arbitrary future credits.

## Three screened patches

| Patch | Mathematical delta | Decision |
|---|---|---|
| A. Transported-adjoint minimal right quotient | Back-propagate each declared future scalar credit by the exact adjoints `J_j^*`, then take the row span of the transported covectors. This produces an exact minimal-width theorem within the class `X -> XW` and a same-prefix full-width impossibility result. | **Selected for full derivation.** |
| B. Online expanding `W` with incremental QR | Add future row directions when observed. | Rejected. A quotient retained before expansion cannot reconstruct discarded components of `X`; exact repair needs the full state/replay. This is a storage policy, not a repaired sufficient statistic, and collapses into R18/general observability bookkeeping. |
| C. Learned prefix predictor of `W` | Predict which future value directions will matter. | Rejected as a distinct mathematical candidate. Without a checkable continuation-support law it is approximate prediction of future credit, with no exact coverage guarantee; the same information can train a direct action/credit predictor. |

## Why A is the only evidence-bearing final attempt

Patch A directly answers the v2 over-approximation defect and yields a falsifiable rank quantity. It does not delete the earlier counterexample. Instead, it proves that a smaller exact quotient exists only relative to a declared future credit family, and that unrestricted legal suffixes force full value width. The likely scientific disposition is therefore a useful Delta specialization/control theorem, not a new architecture.

