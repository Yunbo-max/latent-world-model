# R07 v3 independent source, implementation and collision review

- Reviewer identity: `/root/r07v3_sources`
- Assignment: independent read-only final-byte source, implementation and novelty review; no project/upstream write or execution.
- Math artifact SHA256: `a455e43a40d3be167f1712db3ef515945597e8868c97a11d16b33ebf8fbe9e80`
- Source audit SHA256: `83808934ddbaa0e15f15e2065b6e4c6d819fb535b028ca9679a50b86f02fca80`
- Verdict: **PASS for the declared frozen-affine simultaneous-proposal subcase; MAJOR_COMPONENT_COLLISION / CONTROL_ONLY; not a distinct updater or admitted candidate.**

## Findings

The final bytes correctly derive `Delta S_t=Z_t Diag(a)E^T`, `Delta o_t=E Diag(Z_t^Tq_t)a` and

`H=R+sum_t (c_tc_t^T) odot (E^T W_t E)`.

The half-quadratic normalization, PSD condition, box-separability scope, feedback counterexample and conditional perturbation recursion all check. The recursion is not presented as an identified prefix certificate.

Primary-source and static-interface locators are faithful within their bounded use:

- Yang et al. arXiv:2406.06484v6 supports the Delta recurrence and ordered compact WY/UT treatment. The audit correctly avoids extending that exact kernel to arbitrary interleaved diagonal `D_t`.
- Siems et al. arXiv:2502.10297v7 and the pinned FLA/task interfaces support ordered Householder microsteps and state tracking. Those later residuals are recomputed; R07 v3's simultaneous fixed bank is an assumption boundary, not novelty.
- Tassa--Erez--Todorov, Amos et al., condensed MPC and Khatri--Rao/Schur Gram sources cover joint quadratic action optimization, box-QP/KKT machinery, state elimination and the Hadamard Gram identity.

The cost accounting is conservative. `O(Hd_km)` is only skinny-factor transport/contraction; dense residual construction up to `O(md_kd_v)`, proposal projections, no-action suffix/probes, value-metric Gram work, `O(Hm^2)` accumulation, `O(m^2)` state, QP tolerance/factorization and the selected rank-`m` application are separately charged. No matched-total-cost advantage is established.

## Collision and disposition

Weighted least squares, Schur/Hadamard/Khatri--Rao Grams, condensed affine MPC, box QPs and ordered Delta/Householder products are established. The residual contribution is a useful Delta-coordinate specialization and sharp sign-reversal boundary, not a new architecture, estimator or lawful online controller. Existing endpoints can test downstream behavior but not natively identify the joint internal action object.

Attempt 3/3 is exhausted and parked. Reopen only for a prefix-valid Delta-specific factorization of the full coupled derivative including coefficient feedback with nonvacuous calibration and matched-cost advantage, or a native randomized multi-action causal record. Candidate/count delta is zero; empirical effect is unknown.
