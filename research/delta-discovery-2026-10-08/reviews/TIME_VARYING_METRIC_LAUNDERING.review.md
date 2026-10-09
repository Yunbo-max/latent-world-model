# Independent review — TIME-VARYING-METRIC-LAUNDERING

Reviewers: `/root/rank_innovation_audit` and `/root/reciprocal_cycle_audit`. Independent semantic mathematical reviews only; no file editing or project execution.

Decision: **accept as a scoped no-go and merge into D06 / `LYAPUNOV_OBLIQUE_METRIC`; reject as an independent candidate**.

- The pullback identity is exact only for invertible transitions. Singular exact overwrite cannot support an SPD equality.
- Without uniform coercivity, a moving metric can certify a vanishing or exploding scalar trajectory as isometric. It therefore proves neither Euclidean stability nor retention.
- With \(mI\preceq H_t\preceq MI\), the one-sided cross-time inequality supplies only an upper product bound. A separate lower inequality is required for \(\sigma_{\min}\) retention.
- For rank-one updates, determinant shrinkage proves volume loss; it must not be mislabeled Euclidean contraction. Repeated volume contraction forces determinant/geometric-mean metric blow-up, not necessarily every eigenvalue.
- Exact normalized overwrite or a zero decay channel makes the actual Delta transition singular, so inverse transport is undefined; a pseudoinverse semimetric cannot satisfy uniform positive coercivity.
- Multiple-Lyapunov and contracting-RNN results impose switching/closure and uniform-metric conditions; arbitrary prefix-wise inverse transport is only a coordinate identity.
- Deployment either leaves the recurrence unchanged, becomes an unstable coordinate transform, collapses to RLS/PDN preconditioning, or returns to known dynamical-isometry/retention controls.

The reviews specifically checked invertibility, scalar counterexamples, determinant language, uniform-envelope telescoping, lower-singular-value conditions, causal/post-hoc metric selection, numerical cost and nearest-work boundaries. No D-number is warranted.
