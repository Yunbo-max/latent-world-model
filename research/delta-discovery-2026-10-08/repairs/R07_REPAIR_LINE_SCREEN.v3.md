# R07 repair-line screen v3 — factor-core joint action margin

Date: 2026-10-11  
Parent: `R07_COUPLED_DIRECTIONAL_MARGIN.v2.md`  
Attempt: 3/3  
Stage: Web mathematics, source collision and native-measurement feasibility only; no model execution.

## Preserved result and remaining defect

R07 v2 correctly replaces the v1 frozen-probe scalar with the complete-state first/second directional derivative of a declared fixed-policy, common-exogenous finite suffix. Its costate-weighted transition Hessian and Taylor remainder certificate remain the correct general local calculation. The unresolved practical defect is that this complete calculation is a generic JVP/VJP/DDP object, while v2 only observed—without deriving—whether Delta structure can reduce a multi-write action calculation.

## Bounded patches screened

| Patch | Consequence | Decision |
|---|---|---|
| A. Sum independently computed scalar R07 margins | Ignores cross terms between proposed writes. | Rejected by the exact joint Hessian below. |
| B. Frozen-affine Delta response core | For fixed proposed rank-one writes, fixed future Delta coefficients and quadratic reads, propagate only the proposed key factors and solve the exact joint box QP. | **Selected.** It closes the explicit multi-write gap and gives an auditable computation boundary. |
| C. Promote the core to a complete recurrent/free-running gate | Treat future keys, gates, routes, probes or losses as unaffected by the write. | Rejected. A scalar state-dependent-gate example reverses the first derivative; a prefix-valid perturbation envelope requires extra simultaneously calibrated information. |

## Decision

Patch B yields a real Delta-specific factorization and an exact `m`-action solve under a declared frozen affine suffix. For diagonal-plus-rank-one transitions, the key-side factors propagate in `O(H d_k m)` rather than propagating `m` dense memory tangents. The gain is conditional: future probes and coefficients still have to be available, value-side Gram and QP costs remain, and the result does not include feedback through keys/gates/routes/updater state.

The mechanism is weighted least squares/reduced-space QP plus low-rank Delta propagation; Delta/WY, DeltaProduct, DDP/iLQR/differentiable MPC and the packet's R11/R20 controls cover the main ingredients. The exact Hadamard response identity is retained as a narrow theorem/debugging baseline. It does not supply validity evidence, a lawful prefix future, a free-running causal effect, or a native mechanism scorer.

R07 therefore exhausts attempt 3/3 and is parked as a conditional theorem/control. Candidate, scientific-admission and selection deltas are zero; empirical effect remains unknown.
