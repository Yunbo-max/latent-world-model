# R09 v2 independent adversarial final-byte review

- Reviewer: `/root/r09_final_adversarial`
- Math artifact SHA256: `aa78f4f15322ef501d14ce76d93e60e3544e2b07b16bebea7488eb308e11aacf`
- Source artifact SHA256: `8894320661e2f608c28c6dc79e509b3902106b18a696e6e02e301cb5a4ff176d`
- Assignment: independent read-only attack on target scope, free-running validity, nonseparable curvature, prefix measurability, hidden costs, benchmark claims, and originality.
- Verdict: **PASS after two final-byte corrections; conditional control only, no candidate upgrade**.

The first review found two real defects: the general-matrix higher-rank conclusion was stated while a rank-one action remained fixed, and complete-state validity was invoked while only row-space costs were charged. The final bytes now:

1. show that retained rank one scalarizes value-side curvature, and restrict the nonseparable Kronecker/higher-rank conclusion to the lifted general-matrix feasible set;
2. separate frozen `d x d` cost from explicit `n x n` complete-state storage or matrix-free horizon-wide JVP/VJP, injection, checkpoint/recompute, solver-tolerance, and calibration costs.

All remaining attacks pass. The target is declared quadratic displacement, not semantic/full protected loss. Frozen suffix, complete-state Gauss--Newton, exact DDP, and action-dependent free-running regimes are not conflated. Conditional expectation needs a sufficient state and continuation law; realized suffix geometry is not treated as legal action-time input. The inverse-metric solution, spectral factor, two-future minimax proof, randomization bound, old counterexamples, and endpoint-only benchmark scope are consistent. The source audit exposes observability/Lyapunov, DDP/iLQR, PDN/RLS/editing, KDN, and exact R20 collisions. KDN's prefix-derived filtering covariance is not the suffix protected-query pullback, so the identical-prefix lower bound still applies; internal randomization is covered by the stated `E[s^2]` argument. The audit's bounded negative search is explicitly non-exhaustive and is not used to claim originality. No blocking defect remains, but empirical effect and novelty are not established.
