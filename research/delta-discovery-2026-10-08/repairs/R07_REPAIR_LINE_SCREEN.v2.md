# R07 repair-line screen v2 — coupled finite-horizon directional margin

Date: 2026-10-11  
Parent: `R07_VALIDITY_TO_ACTION_MARGIN.v1.md`  
Attempt: 2/3  
Stage: Web mathematics, primary-source comparison and native-measurement feasibility only; no model execution.

## Preserved result and exact remaining defect

R07 v1 correctly proves that a truth label `Y` does not by itself determine whether a proposed Delta write should be taken. On its declared fixed-reference quadratic surrogate, the decision additionally depends on signed new-target benefit, signed protected-target cross loss, and curvature. Its exact thresholds and counterexamples remain valid.

The unclosed defect is a target/construction mismatch: v1 freezes the reference probes and future path. In a real recurrent updater, the write changes memory, future gates/keys/routes, updater state, later losses, and sometimes the law of future tokens or feedback. Reusing the v1 scalar coefficients as a free-running action value would omit continuation derivatives.

## Screened patches

| Patch | Mathematical consequence | Decision |
|---|---|---|
| A. Add a heuristic horizon multiplier | Multiply the v1 margin by a learned persistence scalar. | Rejected. It neither restores omitted state derivatives nor controls distribution shift, and is equivalent to an uncalibrated action-value predictor. |
| B. Complete-state directional Taylor certificate | Put memory and every updater/router/ledger coordinate in one state; propagate first and second directional tangents through a fixed-policy, common-exogenous finite suffix; derive exact local derivatives and a uniform-remainder gate. | **Selected for full derivation.** It is the minimal mathematical repair of the frozen-path omission and exposes the exact dynamics-curvature term. |
| C. Call the result an exact Bellman/free-running gate | Treat the fixed suffix derivative as the optimal or stochastic free-running action value. | Rejected. Future policy switches, discrete routing/sampling, action-dependent environment responses, missing overlap, and tail loss require additional Bellman, score-function/OPE, or model evidence. |

## Decision

Patch B supplies a correct coupled-state local certificate and reduces exactly to R07 v1 in the affine/quadratic fixed-reference limit. It also shows why the repair is not yet a method: the required forward tangents, reverse costate and directional curvature are standard automatic differentiation/DDP objects; rank-one Delta injection saves the initial direction but not the generally dense continuation computation. The same-information direct action-value predictor, paired rollout, DDP/iLQR and RTRL/BPTT remain stronger simple controls.

This is therefore a useful second-attempt debug/control. It is not prefix-deployable without additional calibrated simultaneous bounds, not a free-running causal effect, and not scientifically admitted. Candidate delta is zero and empirical effect remains unknown.
