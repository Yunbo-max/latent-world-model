# R15 v2 repair-line screen — derive response order before choosing probes

Scope: mathematical repair, primary-source/author-interface review, and native-measurement feasibility only. No project or upstream code, tests, model execution, training, inference, scoring, dataset/model download, GPU work, or Docker was used.

## Why v1 can be reopened once

R15 v1 made the quadratic response surface explicit, but did not derive it from the coupled Delta continuation. The source review therefore allowed attempt 2 only if full dynamics yielded a checkable low-order law or a matched-information advantage over direct response/Q estimation. The present patch attacks the first condition directly: derive the action-response degree from the actual continuation map, then decide whether a quadratic intervention design is lawful.

## Three bounded repair choices

| Choice | Exact patch | Preserved v1 result | Outcome |
|---|---|---|---|
| Assume another quadratic response | none; repeats v1 | full lifted-Gram iff theorem | rejected as no new delta |
| Local Taylor/DDP model | replace exact global polynomial by a radius-`rho` quadratic surrogate plus an explicit third-derivative regret bound | action-space gradient/Hessian and direct-action controls | useful local control, but already covered by DDP/GGN and project Step2 |
| Coupled polynomial-degree audit | propagate the degree of `z -> x_h(z)` through the abstract Delta recurrence and prove an explicit scalar counterexample | v1 intervention-rank theorem becomes a degree-indexed theorem only for a saturated black-box polynomial family | selected for R15 v2 |

## Decision

R15 v2 derives an affine-quadratic sufficient closure regime and an equally exact failure witness: one algebraically admissible state-dependent scalar Delta key turns a scalar current write into a degree-six terminal loss. More generally, repeated scalar Delta feedback can raise degree as `2*3^H`. If that response is treated as an unrestricted black-box degree-`m` polynomial, its saturated lift has `binom(r+m,m)` features; the fixed structured recurrence need not have that many unknown parameters. This is a real repair of v1's missing structural premise.

The result remains a theorem/debugging control, not a new updater. Affine continuation plus degree-at-most-two loss is one checkable sufficient closure regime; nonlinear maps can also cancel or preserve a quadratic invariant. In the affine regime the same object is standard LQR/DDP/response-surface design, and direct action/Q estimation or model derivatives use the same information. Outside a certified closure, saturated black-box intervention design can become large and local quadratic control requires a declared trust region and derivative bound. Candidate counts therefore remain unchanged unless later work supplies a prefix-checkable closure certificate with a Delta-specific matched-cost advantage and a native action-response measurement object.
