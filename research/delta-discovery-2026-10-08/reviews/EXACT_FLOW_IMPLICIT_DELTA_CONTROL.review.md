# Independent review — EXACT-FLOW-IMPLICIT-DELTA-CONTROL

Reviewers: `/root/flow_delta_math` and `/root/flow_delta_audit`. Read-only semantic/source review; no editing or project execution.

Decision: **reject as a candidate; retain only as an exact-flow/proximal baseline**.

- Both reviewers independently derived (c_F=(1-e^{-\tau\|k\|^2})/\|k\|^2) and (c_P=\eta/(1+\eta\|k\|^2)), and verified that they multiply the same rank-one Delta residual.
- Unit-key softplus/exponential parameterizations reproduce the ordinary sigmoid gate exactly, including its derivative.
- EFLA is a direct exact-flow primary collision; Longhorn is a direct implicit-proximal mathematical collision. NLMS/passive-aggressive methods cover the hard-projection limit.
- The route adds no new address, evidence, state invariant, or output path. It cannot distinguish revision from collision and does not change ordered future propagation.
- Stable evaluation and scalar-gate training behavior are useful implementation controls, not scientific novelty.

No candidate ID is assigned. Reopening requires a genuinely different causal object, such as a justified noncommuting simultaneous generator, followed by a new tractability and nearest-work audit.
