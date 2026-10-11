# Independent mathematical review — R13 v2

Reviewer: `/root/r13_v2_math_review`  
Mode: independent read-only semantic mathematics review; no artifact editing and
no project/model code, test, training, inference, scoring or experiment.

Reviewed exact final bytes:

- `repairs/R13_ROBUST_COMMON_COVECTOR.v2.md`
- SHA256 `c6d611ffe4476035a54d5cd1cf7584895dbbb2248d7d499be69b07e6300647b0`
- paired source SHA256
  `a607f442103b97c309ee1cc4fbdbe489cf4257b80387e9dfe6ec5cf954aaca62`

## Checks

- Verified dimensions, coefficient matching, the block equation `X M=N`, the
  kernel/row-space condition, and the complete pseudoinverse solution family.
- Verified the two-mode invertible Delta counterexample and its same-post-state,
  different-protected-value witness.
- Verified the deterministic and randomized half-diameter lower bounds under the
  declared same-information reachability condition.
- Verified the conditional-variance Bayes-risk identity after restricting it to
  finite second moments and measurable square-integrable decoders.
- Verified that `N M†` is claimed only as the unique minimum-Frobenius-norm
  coefficient matrix, not as a joint optimum over the affine offset.
- Verified that the exact theorem is separated from floating-rank diagnostics and
  that the SVD, family-storage, decoder-state, and direct-ledger costs are not
  presented as unconditional dominance.

## Verdict

**PASS for the stated conditional common-affine-decoder theorem and
indistinguishability control.** This does not establish originality, empirical
benefit, candidate admission, native measurement readiness, or selection. The
hidden realized mode, certified reachable set, and fixed protected target remain
explicit scientific restrictions.

