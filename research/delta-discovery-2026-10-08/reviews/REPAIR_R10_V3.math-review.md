# Independent mathematical review — R10 v3

Reviewer: `/root/r10_math`  
Artifact: `research/delta-discovery-2026-10-08/repairs/R10_INVARIANT_RESIDUAL_CARRIER.v3.md`  
Verified artifact SHA256: `45308be5fbe91a9faff92e08fe3acec7f976cca4c3959b59a92fdf4e674a5c47`  
Decision: **PASS as a conditional boundary/debug theorem; not a method candidate.**

The reviewer independently recomputed the hash and checked dimensions, operator order, recurrence algebra, the affine invariant hull, the witness, costs, and scope.

## Findings

- `A_t` is \(d\times d\), `U` is \(d\times r\), `B_t` is \(r\times r\), `L_t` is \(d\times r\), `R,E,Z` are \(d\times m\), and `C` is \(r\times m\); all displayed products are valid.
- \((I-UU^\top)A_tU=0\) is exactly the fixed-carrier invariance condition. Equations (3)–(4) preserve \((I-\beta kk^\top)D\); no illegal commute occurs. The factorized norm and zero alternatives in the \(D_tU\subseteq U\) case are correct.
- Direct substitution verifies equation (7). Ordered products in (8), the norm bound (9), and the conditional geometric floor (10) are correct; contraction is assumed, not inferred.
- The corrected seed includes the initial residual and every declared admissible injection range. Its mode-word closure is the minimal exact carrier for the declared reachable affine trajectories. Unrestricted injections immediately make the seed full-dimensional.
- For \(d\ge2\), the keys in equation (12) span \(\mathbb R^d\), have nonzero overlap with \(v\), force all key directions into an invariant carrier, and have the nonzero commutator in (13). The result is explicitly worst-case/common-carrier, not a typical-trajectory lower bound.
- The rank-one-to-rank-two rounding example is arithmetically correct. The revised cost accounting includes generic \(O(dr^2)\) core formation, \(O(r^2m)\) core application, moving-basis traffic, and QR.

Minor interpretation: ambient quantization contributes its off-carrier component through \((I-P)Z_t\); the in-carrier part is absorbed into coordinate dynamics. The equations already implement this.

Final disposition: mathematics is conditionally accepted only as an R10 attempt-3 closure. Candidate delta remains 0; empirical benefit is untested; park after 3/3.
