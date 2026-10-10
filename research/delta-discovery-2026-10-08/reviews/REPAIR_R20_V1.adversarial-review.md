# R20 v1 independent final-byte adversarial review

- Reviewer: `/root/r20_adversarial`
- Artifact SHA256: `481880030ff3ac535bc6137320bfc3939007e8efb9a1c8838df1d962e813f33e`
- Source-audit SHA256: `3c6032df1fbdc126ea397ba91ca355001e33f2b1132cc3c357c5bfea75308ad3`
- Verdict: **PASS — strictly for a parked conditional theorem/control; not candidate admission**.

The previous FAIL was bound to old bytes. Its incorrect KKT multiplier, rank-one wording, damping interpretation and measurement omissions are fixed; the old verdict is superseded by this new-hash review.

Independent recalculation confirms the general KKT solution, single-Kronecker cancellation and structural rank bound. For the 2x2 witness, `y*=(-5/8,-1/8)`, `J*=13/16`; the best feasible rank-one edit has `a=-2/3`, value `5/6`, and exact gap `1/48`. The corrected multiplier `(13/8,1/8)` is exact.

The artifact now says explicitly that the witness's nonseparability comes from the sum `lambda I + W otimes pp^T`, so isotropic damping/curvature mismatch is not packaged as a newly observed query×value mechanism. It also states that Step2's general `u=vec(X)` already covers this local quadratic family; R20 adds the constrained action, cancellation boundary and witness rather than a new curvature family.

CrispEdit is treated as a major functional collision; K-FAC, Shampoo, PDN, GKA, QED, GDN2, DeltaProduct, rank-r actions, constrained CG and direct prediction remain strong controls. Future-information access, absence of a prefix-causal estimator, dense/structured solve cost, KKT/constraint residual obligations and empirical uncertainty are disclosed. bAbI, LAMBADA, LongMemEval, CITB and TRACE expose only peripheral endpoints, not a native `H`, optimal rank or paired same-state counterfactual.

Simoncini's standard generalized Sylvester form is now recorded as `AXE+DXB=C`, with the correct vectorization identity. No blocking issue remains. The disposition must stay `conditional theorem/control; parked; candidate delta 0; empirical effect unknown`.
