# Independent mathematical review — R15 v1

- Reviewer: `/root/r15_math`
- Assignment: independent derivation, counterexamples, and final exact-byte review
- Artifact: `repairs/R15_INTERVENTION_RANK_BOUND.v1.md`
- Artifact SHA256: `23dd9536139c1beb4858a0407c4e21c1f32e6750e6d85521bec9eeba1c6a9c53`
- Verdict: `PASS_CONDITIONAL`
- Execution: no project/upstream code, model, benchmark, training, inference, scorer, data/model download, GPU, or Docker.

## Checks actually performed

The reviewer independently derived the causal-support boundary, the linear/quadratic feature design, and the singular-Gram necessity argument. The coefficient dimension `1+r+r(r+1)/2`, the known-baseline reduction, the scalar three-level requirement, and the fact that binary write/no-write identifies only one endpoint contrast are correct for the stated unrestricted exact quadratic conditional-mean family.

The initial exact-byte review caught two local defects. First, `I_(d_v) tensor k` is only the memory-block injection, not automatically the complete augmented-state matrix. The final bytes now distinguish `B_S in R^(d_k d_v by d_v)` and embed it into `B in R^(n by d_v)`. Second, the Cramér--Rao statement needed a fixed-`F` stratum or a correctly specified shared model across `F`; the final bytes now state this scope and the information `N G/sigma^2` explicitly.

The fixed-suffix replay counterexample, `B^T lambda` action-gradient boundary, updater meta-gradient distinction, horizon/support counterexamples, and the `O(q^2)`, `O(KH)`, and `2^H` cost statements were also checked and found sound within their declared conditions.

The final integrated bytes additionally state the fourth-moment-equivalent feature integrability needed by the quadratic Gram, separate fixed recorded descendants from lawful common-random-number free-running pairing, and explicitly mark the result as a multivariate consolidation/generalization of the already-recorded `STEP2_PROJECTED_DELAYED_CREDIT.md` control.

## Non-blocking caveats and disposition

- Extra coefficient restrictions or shape constraints could change which functionals remain identified when `G` is singular; the iff theorem is for the declared unrestricted exact quadratic family.
- Equation (6) is a regular unbiased parametric information bound, not a universal finite-sample minimax guarantee and not a claim that an arbitrary continuous-`F` stratum supplies repeated samples.

The theorem is mathematically useful but does not define a new updater. Final disposition: retain as a conditional identifiability/control theorem, park after attempt 1, and add zero active, scientifically admitted, or selected candidates.
