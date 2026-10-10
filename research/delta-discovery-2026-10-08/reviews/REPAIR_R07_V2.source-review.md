# R07 v2 final-byte source and novelty review

Reviewer identity: `/root/r07v2_sources` — independent source/novelty reviewer  
Review mode: read-only final-byte review; no project or upstream file was written, and no code, test, training, inference, benchmark scoring, data/model download, paid service, GPU job or Docker action was run.

## Bound artifacts

- Math artifact: `research/delta-discovery-2026-10-08/repairs/R07_COUPLED_DIRECTIONAL_MARGIN.v2.md`  
  SHA256: `4259fee0afb25db2624972efcbd7ed6658b5aec16af84163583b8c14b96fdee3`
- Source audit: `research/delta-discovery-2026-10-08/sources/R07_V2_COUPLED_DIRECTIONAL_MARGIN_SOURCE_AUDIT.md`  
  SHA256: `6689600f72bdbc42e8df30c888a1ce6023d5e342bae25f38a3cc9933a18fe8b5`

Both hashes were independently recomputed. A control-character scan is clean. The repaired gradient notation, both `\qquad` commands, remainder inequality and exact-Hessian/GGN-iLQR/full-DDP wording are present.

## Mathematical source check

**PASS.** Equations (3)–(6) correctly give the forward tangent and reverse costate forms of the first directional derivative, including `⟨G_{S,Y},beta k e^T⟩_F=beta k^T G_{S,Y}e`. Equations (7)–(10) correctly propagate the second state derivative and include the costate-weighted transition Hessian. The artifact distinguishes full DDP from GGN/iLQR approximations and records the extra `F_a`, `F_xa`, and `F_aa` terms for explicit later action dependence.

The remainder certificate and branch logic now handle indefinite curvature correctly. The full-write condition, clipped convex minimizer, endpoint branch, fixed-reference v1 reduction, and score-function first/second derivatives are correct under the stated assumptions.

## Primary-source and implementation check

**PASS for source fidelity.** Tassa, Erez and Todorov (IROS 2012) support the Bellman/local-Q/costate recursion and the full-DDP versus iLQG distinction. Amos et al. (NeurIPS 2018) and pinned `locuslab/mpc.pytorch@1fb5d416436e1b2d56494ac4c2cab9008c6413bb` support differentiable finite-horizon MPC and adjoint calculation. MAML and learned-optimizer work already cover differentiation of future loss through an inner/recurrent update. SEAL, TTT Ouroboros and HOPE are used with bounded claims; no third-party HOPE implementation is called author code, and no online Delta costate oracle is inferred.

No reviewed source supports claiming complete-state directional differentiation, Bellman/costate evaluation, future-loss meta-gradients, or delayed validation as a new R07 mechanism.

## Collision and residual decision

**MAJOR_COMPONENT_COLLISION / CONTROL_ONLY.** The complete-state finite-horizon derivative is standard adjoint sensitivity/DDP/iLQR/Bellman evaluation. The Delta-specific part is the rank-one initial contraction; the continuation calculation is general. Rank-one injection alone does not prove lower total state or compute than JVP/VJP, BPTT, DDP or RTRL.

R07 v1's signed truth/protection quadratic is correctly recovered as the affine fixed-reference limit. The full recurrence identifies omitted state paths and dynamics curvature, making this a useful debugging theorem and rejection/control certificate, not a distinct architecture or verified estimator.

Unclosed residuals are: a Delta-specific lower-cost theorem, a lawful prefix estimator outperforming direct action-value prediction at the same information, a free-running causal bridge, and action-level causal measurement.

## Native-measurement check

**PASS with an open measurement gap.** AToKe, SEAL continual evaluation, LongMemEval v1/v2, StreamingQA, CITB, TRACE, bAbI, LAMBADA, CounterFact/ROME and KnowEdit/EasyEdit can test endpoints. No pinned native interface jointly exposes the complete pre-action recurrent state, action-time tangent/costate/curvature, grounded validity, randomized propensity, paired potential outcomes, free-running distribution effect and matched byte/FLOP cost. The artifact therefore records a measurement gap, not a negative result, and invents no data, metric or result.

## Final disposition

- Mathematical correctness: **PASS for the declared local, smooth, fixed-policy finite-horizon object**.
- Source fidelity: **PASS**.
- Functional novelty: **not established; major-component collision**.
- Distinct architecture or estimator: **NO**.
- Native mechanism measurement: **OPEN GAP**.
- Empirical effect: **UNKNOWN; not executed**.
- Candidate status: **parked conditional control/theorem, attempt 2/3; not an active or scientifically admitted D candidate**.
- Count implication: **no change — 5 historical / 0 active / 0 scientifically admitted / 0 selected**.

This review is bounded rather than exhaustive priority certification. Within the checked sources, implementations and native assets, the final-byte artifact and source audit support their conservative conclusion.
