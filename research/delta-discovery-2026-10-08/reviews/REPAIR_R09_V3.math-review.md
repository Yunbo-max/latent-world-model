# Independent final-byte mathematics review — R09 v3

Reviewer identity: `/root/r09_v3_final_math_review`  
Final artifact: `repairs/R09_ROBUST_GRAMIAN_CARRIER.v3.md`  
Final artifact SHA256: `fa1c525afdf34646c750373eb45ce2e62c33881d846ea0cab63331744cf01415`  
Verdict: **PASS for the scoped conditional theorem/debug control; not method admission**

## Preserved correction history

The first exact-byte review of SHA256 `20e7d3c0c5c077b6b4925cb1146f97eeddb8e962825fa5d6fb1bd7bf86f1e8c2` failed on two local claims: equation (10) omitted the adjoint on a potentially nonsymmetric decay, and `mu=0` was said to always destroy uniqueness. The integration writer changed the adjoint action to

`D_j^T U-beta_j D_j^T k_j(k_j^T U)`,

restricted the `O(s^2)` decay-core claim to scalar/diagonal or explicitly two-sided-fast structure, and changed the semidefinite claim to “uniqueness need not hold.” The final bytes above were independently reread and rehashed.

## Final reasoning

- Dimensions and chronological product order in equations (1)--(10) are consistent.
- `range(G^omega)=span_h range(Z_h^omega)` and the common-carrier minimality follow from the PSD kernel/range identity.
- The mode-tree recursion is a valid finite constrained-language support recursion.
- The active-span reduction, rank-one core update, known-core inverse action, and stated conditional costs are correct after charging basis, coordinates, stage metrics and solve.
- For `mu>0`, the robust maximum of quadratic forms is strongly convex; projection onto `span(k,V_t^*)` preserves feasibility and Gramian terms while strictly removing orthogonal energy.
- In the counterexample, `Z=11^T-beta I` has eigenvalues `d-beta` and `-beta` with multiplicity `d-1`; `0<beta<1` gives invertible Delta factors, rank-one realized Gramians and common exact width `d`.
- The `mu=0`, feasibility, stability, diagonal-decay and approximate-versus-exact boundaries are correctly qualified.

Disposition supported: conditional theorem/debug control; attempt 3/3 exhausted and parked; candidate delta `0`; empirical effect unknown; no execution.
