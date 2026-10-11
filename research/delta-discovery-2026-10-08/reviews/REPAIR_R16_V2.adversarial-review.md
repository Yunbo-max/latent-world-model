# Independent adversarial and distinctness review — R16 v2

- Reviewer: /root/commutator_candidate
- Assignment: re-run adversarial review after correction of the dense-basis cost objection; inspect assumptions, edge cases, hidden computation/information, old counterexamples, controls, novelty, and measurement.
- Math artifact SHA256: e97793f06e6c10eb56bac6dd8913f3435fe604cb9c8de190a2b816d4ea6e43bb
- Source-audit SHA256: 4fc11ab72193f7e7f4a796ce2267424020c81e8650c6dfc374a2bf035449f488
- Digest status: both match the corrected final bytes.
- Verdict: **PASS_CONDITIONAL** as a theorem/control only.
- Execution: exact-byte static review only; no project/upstream code, tests, model execution, training, inference, scoring, benchmark dispatch, data/model download, GPU work, or Docker.

## Adversarial findings

The previous blocker is genuinely fixed. The artifact now separates the general symmetric active-spectrum identity from the fast coordinate-diagonal/tied-group interface. It explicitly charges dense projection/lifting, eigenspace discovery, storage, and base-exponential action, and restricts equation (15) accordingly.

The invariant-core construction, Vandermonde proof, functional-calculus identity, DPR1 secular equation, affine source, Duhamel bounds, and normalized-direction certificate are algebraically correct. The coordinate-group action costs \(O(dm+r^2m+r^2)\); distinct active rates with dense \(k\) give \(r=d\) and restore \(O(d^2m)\). Varying token bases do not provide fixed-rank exact scan closure.

No remaining edge condition invalidates the theorem, but implementation must still define small-component thresholds, near-tie grouping, representatives, sorting, discontinuous membership, eigenderivatives, backward gradients, and low-precision error. Exact small \(r\) is nongeneric for unconstrained floating per-channel rates and dense keys. The denominator certificate can be valid yet vacuous when its lower bound is tiny.

All decisive v1 failures survive: natural flow does not exact-write every initial state; endpoint normalization remains inverse-metric Delta; the old-state factor is singular; multi-group affine leakage can reach a query orthogonal to \(k\); full active spectrum removes the small-core gain; and one-token structure does not imply scan closure.

The result is not structurally distinct from its controls. DPR1 eigensolvers, low-rank matrix-function updates, expmv/rational Krylov, structured SSM actions, R09/RLS/PDN endpoint geometry, DeltaProduct, and CKDA cover its principal mechanisms. Grouped KDA must receive the same group partition, rates, \(k,v,\tau\), parameter restriction, and total computation. Otherwise an apparent benefit could come from tied-decay regularization, smoothing, or extra \(r^2m\) work.

Native endpoint tasks do not expose the true joint generator, active grouping, exact internal state action, semantic validity labels, and matched action cost. Frozen matrix fixtures would establish numerical consistency only.

## Verdict

The corrected bytes merit conditional mathematical acceptance, numerical-originality rejection, a narrow Delta-specific theorem residual, candidate delta zero, and park-after-attempt-2 disposition. Reopening as an architecture requires independent scientific justification of the joint generator, a consequence unavailable to grouped KDA/direct core action, a complete forward/backward/grouping/transform/storage budget, scalable sequence computation or an honestly recurrent claim, and a native measurement object.
