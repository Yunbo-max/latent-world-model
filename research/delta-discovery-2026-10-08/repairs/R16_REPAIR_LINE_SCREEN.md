# R16 repair-line screen — noncommuting decay and write

Scope: mathematical repair, primary-source/author-interface review, and native-measurement feasibility only. No project or upstream code, tests, model execution, training, inference, scoring, dataset/model download, GPU work, or Docker was used.

## Three bounded repair clues

| Parent line | Exact failure | Failure type | Preserved result | Concrete patch tested | Screen decision |
|---|---|---|---|---|---|
| `rejected/EXACT_FLOW_IMPLICIT_DELTA_CONTROL.md` | Its exact scalar residual flow only changes a scalar gate; with channel-dependent decay it omits the noncommuting joint generator. | assumption too narrow / mechanism collision | exact integration removes a finite-step artifact but does not add semantic evidence | solve the frozen simultaneous ODE with generator `M=Lambda+kk^T`, including its affine source, then ask whether an exact-write endpoint survives | selected as R16 theorem/control; the joint transition has a real Krylov-rank boundary, but the endpoint repair is known inverse-metric Delta and the dense transition loses KDA cost |
| `rejected/SYMMETRIC_SPLIT_DELTA_CONTROL.md` and `rejected/AFFINE_MAGNUS_COMMUTATOR_CONTROL.md` | Strang/Magnus corrections describe order error, but a homogeneous commutator alone omits the affine write-source error. | incomplete object / known numerical-analysis mechanism | the leading order gap is governed by noncommutation | derive both the homogeneous and affine second-order gaps and an exact two-dimensional leakage witness | retained inside R16; useful correction, not a separate method |
| `repairs/R09_FINITE_BUDGET_OVERWRITE_PROTECTION.v1.md` | A normalized inverse metric can hit the new key exactly, but it does not specify a new causal metric or recover reversibility. | known-mechanism collision / information gap | the finite-budget Pareto and singular exact-overwrite boundaries are correct | derive the metric induced by the joint flow endpoint | not selected: the endpoint controller is exactly R09's normalized inverse-metric update with `H=P_tau^{-1}` |

## Decision

R16 performs one substantive revision of the exact-flow lineage. The noncommuting generator genuinely changes the homogeneous transition: its departure from pure decay is confined to a Krylov subspace whose dimension can exceed one and can reach the full key dimension. But the natural simultaneous flow does not write the target exactly, while enforcing exact endpoint write converts it into the already-known normalized oblique Delta geometry after a dense transition.

The old parent bytes and counterexamples remain authoritative. R16 neither deletes the scalar-flow collision nor claims that KDA's declared decay-then-write recurrence is an approximation error. It tests a different frozen sub-token semantics, preserves the resulting theorem/control, and parks the line after attempt 1.
