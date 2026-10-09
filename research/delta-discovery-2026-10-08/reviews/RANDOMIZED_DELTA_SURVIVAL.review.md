# Independent review — RANDOMIZED-DELTA-SURVIVAL

Reviewer: `/root/qed_full_audit`.  Semantic review only; no file editing or execution.

Decision: **correct under explicit restrictions; reject as a distinct candidate and retain as a negative/numerical control**.

- The compensated Bernoulli mean and variance are correct as one-step conditional statements.  They do not imply equality of state-dependent network trajectories, logits or losses.
- The repeated-key relative-variance formula requires iid masks and \(\beta\ne1\); it concerns a homogeneous old-information component, not a full recurrence with additive writes.
- The uncompensated matched-mean MSE gap is correct for a fixed unit-key residual and does not rule out training regularization.
- Pathwise fixed-point preservation requires coupled erase/write coefficients.  Mere equality of their expectations preserves only the expected fixed point.
- The PSD exact-mean lemma is correct and is the strongest no-go: random erase range is almost surely contained in \(\operatorname{span}(k)\).
- Stochastic-rounding bounds require non-saturation, exact probabilities and an explicit grid.  Frozen affine propagation must use ordered products; a nonlinear network requires Jacobians.  The absorbing-zero result is scoped to a finite nonnegative grid.
- Direct collisions include Zoneout, recurrent update dropout, stochastic rounding, low-discrepancy recurrent-cache dither, LeapQuant and STEPQuant.

The remaining correlated/error-feedback lead lacks a concrete construction, readout guarantee and cost separation, so no active-candidate residual survives.
