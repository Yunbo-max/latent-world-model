# R14 v2 repair-line screen — from a point posterior to a certified posterior set

Scope: mathematical/source/measurement review only. No model code, benchmark execution, training, inference, scoring, data download or GPU job was run.

## Bounded clues for substantive attempt 2

| Clue | Exact remaining defect in v1 | Patch considered | Decision |
|---|---|---|---|
| Posterior misspecification | v1 assumes a single calibrated causal posterior `p=P(J=1|F_t)` is supplied. A shifted or miscalibrated router can make its Bayes action confidently harmful. | replace the point posterior by an externally certified, prefix-measurable interval `p in [ell,u]`; derive the exact minimax continuous write, exact misspecification regret and a hard write/abstain control | **selected**: changes the information object and yields a falsifiable theorem without erasing v1 |
| Acquire more identity evidence | the interval may be too wide to support a useful write | query/retrieve before acting and price the value of information | not selected: changes the information set, latency and budget; it is the R08/EVSI/controlled-sensing family |
| Add an unknown/new slot | the true identity may be absent from all existing slots | add an explicit `J=empty` action and allocation/eviction rule | not selected: changes state, capacity and action space; it must be compared with an event store/open-world router under equal memory |

The selected patch does not claim to identify provenance. It asks what the safest local action is when a valid set of posterior beliefs is available. If no new evidence exists, a legal certificate may be `[0,1]`; that is a result, not a reason to hide the ambiguity.

## Lineage and state transition

- parent byte record: `repairs/R14_POSTERIOR_PROVENANCE_WRITE.v1.md`;
- parent source/reviews remain unchanged and authoritative for the point-posterior theorem;
- child: `repairs/R14_CREDAL_PROVENANCE_WRITE.v2.md`;
- attempt: 2 of at most 3;
- success condition: a correct robust decision theorem or a Delta-specific residual not already implemented by a direct minimax router;
- observed outcome: the theorem is exact, but the implementation is precisely a direct robust router and the interval itself needs external evidence. The line is therefore parked as a conditional theory/control, not upgraded to a candidate.

