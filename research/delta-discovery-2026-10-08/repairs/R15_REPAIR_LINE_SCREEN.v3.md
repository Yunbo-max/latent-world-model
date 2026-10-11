# R15 v3 repair-line screen — finite jets do not certify a nontrivial positive-radius guarantee

Scope: mathematical repair, primary-source/interface review, and native-measurement feasibility only. No project or upstream code, tests, model execution, training, inference, scoring, dataset/model download, GPU work, Docker, or paid service was used.

## Why v2 can be reopened once

R15 v2 replaced the unjustified global quadratic-response premise by two valid objects: an exact polynomial degree audit and a local Taylor regret bound. It nevertheless left the central deployment premise open: can a prefix-time updater infer a positive trust radius or a finite derivative envelope from the same local response information? Attempt 3 attacks that premise directly. It preserves v1's causal-support theorem and v2's degree-growth witness, then tests whether a finite response jet can certify the missing radius without extra observations or assumptions.

## Three bounded repair choices

| Choice | Exact patch | Preserved result | Decision |
|---|---|---|---|
| Learn a radius from the current residual or Hessian | infer a radius from local quantities already available at the action point | v2 Taylor model | rejected: a finite jet contains no information about the first omitted term |
| Use trial outcomes and an acceptance ratio | evaluate branch-consistent trial actions and shrink/expand a trust region from model agreement | v1 randomized-action and v2 local-model objects | valid generic trust-region/regularization control, but it consumes new counterfactual or simulator outcomes and is not a prefix-only certificate |
| Prove the finite-jet boundary | construct two polynomial continuation responses with the same derivatives through order `p` at the current action but incompatible optimal actions, then add the exact uniform-remainder condition that repairs the guarantee | v1/v2 assumptions, costs, and counterexamples | selected for R15 v3 |

## Decision

For every finite order `p` and every positive radius `rho`, the two responses `Y_+(z)=C+c(u^Tz)^(p+1)` and `Y_-(z)=C-c(u^Tz)^(p+1)` have identical `p`-jets at the current action; choosing `C>=c rho^(p+1)` also makes both losses nonnegative. Yet any deterministic or randomized rule using only that common jet has a nonzero worst-world regret. Thus the jet alone cannot certify a nontrivial, scale-free optimizer guarantee on a fixed positive radius. A known uniform `(p+1)`-derivative envelope repairs the statement and yields the standard `2 M rho^(p+1)/(p+1)!` surrogate-optimizer bound, while an exact polynomial degree cap at most `p` removes the ambiguity altogether. A known global loss range/lower bound gives only a possibly loose finite fallback and does not identify an improving direction.

This exhausts the third substantive R15 repair attempt. The result is a useful terminal theorem/debugging control: a lawful positive radius needs extra structural assumptions or post-action validation outcomes. High-order Taylor regularization, trust-region acceptance, exact polynomial interpolation, direct action/Q optimization, and the existing R15 causal design are the same-information or extra-information controls. No Delta-specific updater, matched-cost advantage, or native mechanism-identifying record survives. Candidate delta remains zero; empirical effect is unknown.
