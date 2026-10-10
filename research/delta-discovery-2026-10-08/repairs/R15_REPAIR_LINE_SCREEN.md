# R15 repair-line screen — intervention evidence before another updater

Scope: mathematical repair, primary-source/author-interface review, and native-measurement feasibility only. No project or upstream code, tests, model execution, training, inference, scoring, dataset/model download, GPU work, or Docker was used.

## Three bounded repair clues

| Parent line | Exact failure | Failure type | Preserved result | Concrete patch tested | Screen decision |
|---|---|---|---|---|---|
| `rejected/COUNTERFACTUAL_QUERY_WRITE_UTILITY.md` | Passive factual loss cannot identify the loss of an unchosen write/no-write action; fixed-suffix leave-one-write-out credit also collapses to ordinary future CE for write-local parameters. | information/estimand mismatch | frozen-path transport and the passive individual-effect no-go are correct | restrict edits to a finite action subspace, randomize action coordinates, and derive the exact intervention-rank needed to identify a linear or quadratic response surface | selected only as an R15 theorem/control; R02 and `STEP2_PROJECTED_DELAYED_CREDIT.md` already cover the estimator/mechanism, so no new method child is admitted |
| `rejected/NOGO_CAUSAL_POLYNOMIAL_FUTURE_PRODUCT.md` | A causal prefix does not reveal realized future propagation coefficients; polynomial extrapolation can reverse off support. | missing future information / target mismatch | a declared bounded coefficient set can support robust optimization | replace point extrapolation by a PSD interval or uncertainty set over projected action consequences | not selected: the robust action is the same generalized inverse/Pareto geometry already recorded in R09, while noncommutative ordered uncertainty returns to R11 and the full-Jacobian suffix gap remains |
| `rejected/EXACT_FLOW_IMPLICIT_DELTA_CONTROL.md` | exact scalar-flow discretization changes only the gate and is still ordinary implicit/ODE discretization | mechanism collision | exact flow removes a finite-step stability artifact | use the noncommuting generator `M=Lambda+kk^T` so decay and overwrite are solved jointly by `exp(-M tau)` | retain as an unqualified next lead only: it changes the operator when `Lambda` does not commute with `kk^T`, but a full exact-discretization/SSM/KDA/PDN formula-and-code audit is still missing |

## Decision

R15 performs one substantive revision of the counterfactual-action lineage. It adds an explicit structural assumption—an exact low-order response surface—and derives the intervention-rank and conditioning price needed to use it. This is a real mathematical repair of the vague “probe a few writes” idea, but it is not a new Delta updater: randomization, HT/AIPW, sequential DR, paired replay, horizon reversal, and action-space projection were already preserved in R02/R03/R06 and `STEP2_PROJECTED_DELAYED_CREDIT.md`.

The old parent bytes and counterexamples remain authoritative. R15 does not erase them, promote a diagnostic into a method, or use fixed-suffix replay as evidence about free-running causal value.
