# Independent source and novelty review — R09 v1

- Reviewer: `/root/r09_source_audit`
- Assignment: independently verify primary-paper formulas, author-code ownership and pins, native measurement claims, and closest-work disposition; reviewer did not write the integrated source audit.
- Artifact: `research/delta-discovery-2026-10-08/sources/REPAIR_R09_OVERWRITE_PROTECTION_SOURCE_AUDIT.md`
- Artifact SHA256: `c74e96dcc7c19f9b9fd8a1e261f839b5c81002cf9340fa8452adc20a24408c01`
- Byte check: matched.
- Verdict: **PASS; major mechanism collision, bounded theorem/control only, no candidate upgrade**.

## Checks performed

1. AlphaEdit ownership is correctly separated: `experiments/evaluate.py::get_project` constructs the covariance/SVD nullspace projector, while `AlphaEdit/AlphaEdit_main.py::apply_AlphaEdit_to_model` consumes that projector, forms the supplied-target residual, performs the projected solve, and updates cached covariance.
2. AlphaEdit+ is correctly recorded as Findings of ACL 2026, Anthology `2026.findings-acl.728`, DOI `10.18653/v1/2026.findings-acl.728`. Its equations 1--2 give the AlphaEdit Tikhonov objective/solution and equation 7 adds optimized projector perturbation, conflict-weighted prior-edit constraints, and smoothing.
3. The author-code pin `zjh-vinky/AlphaEdit_plus@b4fe675ad638fe9fef5046ea3300536d09bd6ddf` contains the named interfaces `apply_AlphaEditPlus_to_model`, `solve_delta_closed_form`, `objective_value`, and `build_lambda_p` with the stated roles.
4. DeltaNet, PDN, Gated KalmanNet, OWM, GEM/EWC/A-GEM/OGD, Rank-Greville/QR-RLS, and the native measurement assets are described within the limits of the inspected papers and implementations.
5. The main mechanism is already substantially covered by inverse-Gram/preconditioned least squares and nullspace/soft-conflict editing. The residual contribution is therefore limited to the Delta-specialized Pareto ratio, equality cases, singular endpoints, and exact infeasibility certificate.

Disposition: park R09 as a conditional static-theory control. It receives no D-number and changes none of the active, admitted, selected, or readiness counts. Empirical effect remains unknown.
