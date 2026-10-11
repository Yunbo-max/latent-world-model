# R19 v2 independent mathematics review

- Reviewer identity: `/root/r19_v2_math`
- Assignment: independently rederive the final artifact's finite zero-error theorem, metric bound, nonlinear witnesses, linear quotient rank, all-path extension, costs, and disposition.
- Artifact: `repairs/R19_PREFIX_CAUSAL_BRANCH_CODE.v2.md`
- Reviewed SHA256: `0d771029d39677e8077b7c23d761c90b2c9ffaecf03b81781a078ec8561ed105`
- Verdict: **PASS; no blocking correction**

## Reasoning

The first submitted byte version failed because its loopless graph omitted two same-state branches with one visible label but unequal targets. The final artifact adds condition (F), declares every violation infeasible for any code size, and uses (F) for `x=y` while proper coloring handles `x!=y`. This makes the coloring necessity and sufficiency proof exact for the declared finite, one-shot, fixed-length, zero-error object.

The no-code metric-radius lower bound is `Delta_0/2`; the final text translates it only to `Delta_0^2/4` for a unit-weight squared-`d_g` loss and does not infer an arbitrary switched-energy bound. The K2 and K4 witnesses, including the explicit lawfulness of both K4 branches, rederive correctly.

For kernel coordinates `Kz`, post-write observation `Az`, code `CKz`, and release rows `B_m`, exact mode-specific linear decoding is equivalent to `ker A intersect ker(CK) subseteq intersect_m ker B_m`. The minimum additional width is `rank([A;B_1;...;B_M])-rank(A)`, attained by a row-space complement; full-column-rank `K` makes the chosen code rows realizable. The all-path form correctly uses the joint row span and subtracts the already visible `row(A)`.

The branch-divergence example has gain `a/epsilon+rho`, so its unbounded cross-branch ratio is valid even though each branch derivative is contractive. Finite-alphabet, precision, coloring complexity, decoder metadata, and complete-state augmentation limitations are explicit. Parking after attempt 2 with `candidate_delta=0` and empirical effect unknown is mathematically supported.
