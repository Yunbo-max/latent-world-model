# Independent mathematical review — R14 v2

Reviewer: `/root/r14_v2_math`  
Reviewed at: 2026-10-11T07:47:35+01:00  
Mode: independent read-only semantic mathematics review; no artifact editing and
no project/model code, test, training, inference, scoring or experiment.

Reviewed exact final bytes:

- `repairs/R14_CREDAL_PROVENANCE_WRITE.v2.md`
- SHA256 `073146ac7af184d9d39146911686af9b1de911688ed5a945d7f628ac5d5a6bbb`

## Checks

- Re-derived the two-slot Bayes action, Bayes risk, interval minimax solution and
  direct saddle inequality. The least-favourable posterior is the projection of
  `1/2` onto the certified interval.
- Re-derived the exact posterior-misspecification regret and checked dimensions,
  signs, endpoint behaviour and the invalid-certificate counterexample.
- Verified the hard one-touch action thresholds and the explicit warning that
  allowing `(1,1)` changes the action set and adds worst-case risk `lambda`.
- Verified the multi-slot Bayes action and robust value under the explicit
  uniform positivity condition `inf_{pi in Pi,i} h_i(pi)>0`.
- Confirmed that a polytopal ambiguity set yields a convex epigraph QCQP with
  vertex constraints, while the least-favourable posterior may be an interior
  mixture; it is not generally enough to maximize the reduced Bayes risk only
  over vertices.
- Confirmed that the `lambda -> 0` statement is restricted to fixed
  non-degenerate `0<p<1`, with posterior endpoints and `lambda=0` handled
  separately.

## Verdict

**CONDITIONAL PASS for the stated local quadratic theorem and controls.** The
math is correct on the bound bytes under the stated coverage, operational
identity and positive-curvature assumptions. This review does not establish the
external certificate, Delta-language applicability, originality, native
measurement, empirical benefit, candidate admission or selection.

