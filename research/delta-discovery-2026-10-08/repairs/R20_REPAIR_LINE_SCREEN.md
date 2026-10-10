# R20 repair-line screen — escaping the rank-one metric theorem

Scope: mathematical repair, primary-source/author-interface review, and native-measurement feasibility only. No project or upstream code, tests, model execution, training, inference, scoring, dataset/model download, GPU work, or Docker was used.

## Three bounded repair clues

| Parent line | Exact failure or open interface | Failure type | Preserved result | Concrete patch tested | Screen decision |
|---|---|---|---|---|---|
| `repairs/R09_FINITE_BUDGET_OVERWRITE_PROTECTION.v1.md`, `cards/D03.json`, and the value-coupled Gram already recorded in R17 | R09 proves a rank-one representer only for a left metric, and a single separable query×value Kronecker metric still cancels on the value side under the exact all-output constraint. That does not cover a sum of differently oriented query and value curvature factors. | assumption boundary plus target/geometry mismatch; R09 itself is not wrong | normalized inverse-left-metric Delta is still the unique optimum for left-only or single separable curvature | minimize a strictly convex nonseparable query×value quadratic subject to the exact Delta correction, derive the KKT/Schur solution, and test whether rank one remains sufficient | **selected for one bounded R20 child**: there is a minimal rank-two witness and an exact simultaneous-output-eigenbasis solver; generic KKT/GGN/Kronecker preconditioning are expected major collisions |
| `STEP2_COUPLED_UPDATER_STABILITY.md` and R19 | Stronger small-gain margin reduces closed-loop sensitivity, but the present packet does not quantify the learning-response tradeoff. | retained open consequence, not a derivation error | block-Jacobian and fixed-fiber stability conclusions remain correct | derive DC/frequency response and a stability–adaptation Pareto frontier | deferred: without an independently justified disturbance/feedback observable this is standard resolvent or H-infinity sensitivity, not yet a Delta-specific repair |
| `rejected/NOGO_CAP_02.md`, R10, R17, and R18 | Finite precision can turn a real-valued invertible partial overwrite into a practically irreversible channel. | assumption gap already covered by strong neighbors | equal-codebook, quotient and complete-state fiber controls remain correct | add repeated noisy observations and quantized write-back under an explicit stochastic law | not selected: the lawful patch is Kalman/RLS/EMA plus rate-distortion/quantized filtering, with no new same-budget Delta consequence identified |

## Decision

R20 performs substantive attempt 1 on the first line. The repair changes the risk geometry rather than renaming the gate: output coordinates may have different query-side curvatures, so the exact constrained action can require multiple left write directions. It does not infer factual validity, expose a prefix-causal future Hessian, or claim that a dense solve is useful.

The expected stopping condition is explicit. If the only retained result is a general equality-constrained quadratic projection, while K-FAC/Shampoo/GGN and existing Delta preconditioning or multi-step rank controls cover the mechanism at lower or comparable cost, R20 remains a theorem/control and contributes zero candidates. Reopening requires a causal structured curvature estimator plus a matched-total-cost advantage over rank-r Delta, constrained CG and a same-information direct action predictor.

