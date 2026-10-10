# Independent mathematical review — R08 v1

- Reviewer: `/root/r08_math_derivation`
- Assignment: independent final-byte rederivation and adversarial check; reviewer did not write the integrated artifact.
- Artifact: `research/delta-discovery-2026-10-08/repairs/R08_TEMPORAL_VALIDITY_RELEASE.v1.md`
- Artifact SHA256: `574a66f55b62c57cf08c2866ea16d6711dbc49d14c37c4d3c0dbe9b1bf19fd4a`
- Byte check: matched.
- Verdict: **PASS, conditional control only; no candidate upgrade**.

## Checks performed

1. Dimensions: `Delta S=a beta k e^T` is key-by-value; `q_v` and `h_v` are fully contracted scalars before mixing with a posterior.
2. Quadratic signs: `D_p(a)=h(p)a^2-2q(p)a`; beneficial positive small step iff `q(p)>0`; full write beats no-write iff `q(p)>h(p)/2`; full write is the constrained continuous optimum iff `q(p)>=h(p)`.
3. Binary posterior threshold: with `D(p)=B+pA`, release is `p<-B/A` for `A>0`, `p>-B/A` for `A<0`, and independent of `p` for `A=0`.
4. Counterexample: both worlds keep `p,Yb,h` fixed and change signed protection geometry; arithmetic and opposite actions are correct.
5. Robust endpoint result: for fixed branches and a sharp posterior interval, fixed-action risk is affine in `p`, so endpoints give the exact range. The artifact correctly refuses to call a Cartesian product of marginal intervals sharp.
6. One-step value of information: terminal Bayes risk is the minimum of affine losses and therefore concave; for an action-independent, no-time-transition observation, posterior martingality plus Jensen gives nonnegative information value.
7. Dynamic control: switching term `kappa(1-2a_{t-1})`, continuation difference `Gamma`, and the `+/-G` sufficient certificates have the correct signs. The state correctly includes memory/updater/run-length variables rather than belief alone.
8. Failure cases: information destruction, hysteresis, delayed-label leakage, action-conditioned e-process validity, and multi-fact state growth all preserve the relevant old counterexamples.

## Conditions and nonblocking clarifications

- The endpoint minimax stationary-point enumeration inherits R07's linear branch when curvature is zero.
- If “defer” consumes time while validity transitions, the posterior-martingale statement applies only after the appropriate prediction step; that case belongs in the Bellman section rather than the one-step static VoI result.
- Fixed-reference correctness does not establish free-running performance.

The reviewed contribution is an exact conditional bridge from temporal belief to signed Delta action margin plus a Bellman correction. It is not a novel filter, POMDP, change detector, or editing architecture.
