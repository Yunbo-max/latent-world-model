# Independent mathematical review — R12 v2

Reviewer: \`/root/r12_v2_math_review\`  
Mode: independent read-only semantic mathematics review; no artifact editing and
no project/model code, test, training, inference, scoring or experiment.

Reviewed exact final bytes:

- \`repairs/R12_AUTONOMOUS_SYNDROME_CLOSURE.v2.md\`
- SHA256 \`4b7afa4ec82b770fa86e36435d0b4ae5173e4dc94186d161e592a4631175b916\`
- paired source SHA256
  \`3903fd6b35f4b1cff3fb844cf92aae354121b83e210f5787f77aace8f3499c9e\`

## Checks

- Verified all dimensions and the order
  \(F=(I-\beta kk^\top)D\), including the \(D^\top\) term in the residual form.
- Verified the same-fiber, kernel, row-space, adjoint-invariant-subspace and
  factorization equivalences in equation (3), plus the protected-readout
  factorization in equation (5).
- Verified the pure-Delta dichotomy
  \(H^\top k=0\) or \(k\in\operatorname{col}(H)\), and the inclusion-minimal
  fixed point for an allowed active-key family.
- Verified the paired same-syndrome/different-next-syndrome counterexample.
- Verified the exact fixed-\(H\) operator-norm minimax identity, rank-one leakage
  factorization, and reduced-state error recurrence.
- Verified the final corrections: composite transition fiber constancy is the
  general necessary-and-sufficient condition; individual coefficient constancy
  is only sufficient. Orthonormal coordinates remove arbitrary basis scaling.
  An infinite key family leaves a valid set-theoretic fixed point but needs a
  separate computable certification.

## Verdict

**PASS for the stated conditional fixed-affine theorem/debugging control.**
The review does not establish originality, empirical benefit, candidate
admission, native measurement readiness or selection.

