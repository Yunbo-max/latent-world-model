# R19 v1 independent final-byte mathematics review

- Reviewer: `/root/r19_final_math_review`
- Assignment: independent rederivation of PSD domination, sharp cross-mode factor, switched-product order, dwell-time consequence, released-coordinate rank, affine injection recursion, and nonlinear/branch scope
- Reviewed artifact: `../repairs/R19_SWITCHED_PROTECTION_FIBER.v1.md`
- Artifact SHA256: `c589931307d5821b6abd3f4542c21fd6d5a98af5e43d2764cb3d7a22efa93bf6`
- Verdict: **PASS — conditional mathematics accepted; theorem/control only; parked; zero candidate admission**

The first pass found two substantive defects and did not pass the earlier bytes: the product omitted a possible same-mode reset factor, and the released-ledger row-space construction mixed coefficient and state spaces. The final artifact fixes both. Equation (9a) makes same-mode reset the identity; any nontrivial same-mode reset must contribute its own comparison factor. With orthonormal `K`, the rank factorization `B=DQ` and code `C=QK^T` have correct dimensions and recover `Bz` from an old-kernel perturbation `h=Kz`.

The reviewer independently confirmed that finite PSD domination in (5) is equivalent to the kernel inclusion and that (6) is its sharp generalized-Rayleigh factor on `range(P_sigma)`. For the additive code, (13c) is exact because `ker(P+C^T C)=ker P cap ker C`; consequently finite `mu,nu` exist precisely when this joint kernel is killed by the new measured reset. The lower bound `p>=rank(B)` follows from `B=D_c(CK)` for an exact linear decoder and is attained by the `Q` coordinates under the explicitly scoped local linear assumptions.

The ordered product, average-dwell corollary, two-dimensional release witness, and affine unrolling (16) were also checked. The nonlinear statement is correctly restricted to local/common positive-margin branches unless complete finite-state reset and hybrid relations are certified. No mathematical error remains, but semantic release validity, originality, matched-budget advantage, native measurement, and empirical effect remain unproved.
