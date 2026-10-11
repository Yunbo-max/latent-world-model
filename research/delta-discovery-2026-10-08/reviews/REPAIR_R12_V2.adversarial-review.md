# Independent adversarial and fair-budget review — R12 v2

Reviewer: \`/root/r12_v2_adversarial_review\`  
Mode: independent read-only counterexample, hidden-cost and attribution review;
no editing or project/model execution.

Reviewed exact final bytes:

- math SHA256
  \`4b7afa4ec82b770fa86e36435d0b4ae5173e4dc94186d161e592a4631175b916\`
- source SHA256
  \`3903fd6b35f4b1cff3fb844cf92aae354121b83e210f5787f77aace8f3499c9e\`

## Attacks and repairs checked

- Initial review rejected individual coefficient constancy as necessary. The
  final bytes correctly require only projected composite-transition constancy on
  syndrome fibers and treat coefficient constancy as a sufficient decomposition.
- Initial review rejected raw leakage magnitude as basis invariant. The final
  bytes restrict equation (12)--(13) to fixed \(H\), use orthonormal \(U\) for
  fair numerical comparison, and charge decoder conditioning and finite
  precision.
- Randomized rules are ruled out only for guaranteed/almost-sure exact recovery
  of both indistinguishable states; Bayesian approximate estimation under a prior
  is not excluded.
- Equation (8) is explicitly set-theoretic for an infinite/implicit key family;
  descriptor/certification and any full-state coefficient generator are charged.
- The decay/update order is scoped to the packet's formula. Reversed/pre-decay
  implementations require a new derivation.
- Keeping full \(S\) makes the syndrome an auxiliary ledger, not compression.
  Direct orthonormal coordinates are equal-width, while sparse/implicit compute
  differences require matched total-cost evidence.
- Native endpoint tasks cannot attribute gains to the internal fiber theorem.

## Verdict

**FINAL-BYTE PASS for the scoped theorem/control; candidate admission NO.**
Originality/distinctness is not established, empirical status is unknown, and
the justified disposition is park after attempt 2/3 with candidate delta zero.

