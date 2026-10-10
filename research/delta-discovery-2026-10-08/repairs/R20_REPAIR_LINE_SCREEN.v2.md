# R20 v2 repair-line screen — replacing the dense future oracle

Scope: mathematical/source review only; no project code, tests, model execution, training, inference, scoring, dataset/model download, GPU work, or Docker.

| Repair clue | Exact remaining failure | Patch tested | Result |
|---|---|---|---|
| causal low-rank curvature | v1's dense/frozen future curvature is unavailable at deployment and its solve is too expensive | require `Z_t` to be prefix-measurable and use `Hhat=lambda I+ZZ^T`; derive the exact projected Woodbury solution and factorized query×value form | **selected attempt 2**; exact mathematics and v1 witness recovery, but past-to-future transfer is unproved and M-FAC/SENG/WoodFisher are major mechanism collisions |
| R01 credit quotient final attempt | exact quotient conditions are conditional and generic lumping/MOR neighbors are strong | learn a time-varying causal covector span with a certified approximation bound | deferred; no new observable or Delta-specific total-cost theorem is presently available |
| R14 provenance posterior | latent identity posterior is not identifiable from the current prefix and routed slots dominate posterior-mean writes | add causally observed provenance/revision evidence | deferred; without a new lawful evidence channel this changes the problem statement rather than repairing the estimator |

The chosen patch is substantive: it changes the information law and reduces the dense `d_k d_v` curvature solve to a prefix-maintained rank-`r` system while preserving the exact overwrite constraint and old counterexample. It does not equate deployment legality with predictive validity. The final R20 attempt remains reserved for a checkable transfer/regret theorem or a native same-budget consequence; repeating Woodbury with a different sketch does not qualify.
