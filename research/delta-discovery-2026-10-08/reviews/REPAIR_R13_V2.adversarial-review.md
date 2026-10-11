# Independent adversarial and fair-budget review — R13 v2

Reviewer: `/root/r13_v2_adversarial_review`  
Mode: independent read-only counterexample, hidden-cost and attribution review;
no editing or project/model execution.

Reviewed exact final bytes:

- math SHA256
  `c6d611ffe4476035a54d5cd1cf7584895dbbb2248d7d499be69b07e6300647b0`
- source SHA256
  `a607f442103b97c309ee1cc4fbdbe489cf4257b80387e9dfe6ec5cf954aaca62`

## Attacks and repairs checked

- The initial overreach from failure of a common affine decoder to failure of
  every decoder is removed. Arbitrary point recovery is excluded only when a
  same-information compatible-target set has positive diameter; otherwise a
  nonlinear piecewise decoder may exist.
- The counterexample uses individually invertible transitions, so the new
  obstruction is hidden transition identity rather than singular erasure.
  Reachability under identical retained information is explicitly required.
- The hidden-mode interface is correctly labelled as a restriction: an ordinary
  Delta implementation normally has the realized key, gate, decay, and value at
  update time.
- Exact algebra is distinguished from floating-point rank decisions. A finite or
  generated affine family, its storage/certification, and any mode label are
  charged rather than treated as free.
- A direct protected-value ledger remains the mandatory exact control. The final
  bytes also preserve the offset-free `d_k<d_v` exception, so no unconditional
  memory-cost superiority is claimed.
- Native tasks do not expose the hidden mode, compatible-target diameter, or
  ledger state; the empirical status is therefore unknown, not failed.

## Verdict

**FINAL-BYTE PASS for the scoped theorem/control; candidate admission NO.** No
mathematical blocker remains, but finite precision, restricted reachable sets,
and changing/multiple protected targets remain non-blocking boundaries. Park
after repair attempt 2/3 with candidate delta zero.

