# Independent review — RETROACTIVE-ROLLBACK-DELTA

Reviewer: `/root/rollback_delta_audit`. Semantic/source review only; no file editing or project execution.

Decision: **kill as a new recurrence; retain as a restricted exact control**.

- The ordered affine composition and frozen-suffix receipt formula are dimensionally and chronologically correct.
- Deleting the full event is not the same as removing its additive value injection, nor as applying its inverse to the present.
- When later features change, the missing forcing sum is decisive; exactness requires a counterfactual replay unless that sum is proven zero.
- Exact current-state-only deletion is impossible for singular overwrites. Near-singular reverse maps are numerically unsafe.
- A stable event ID and receipt/log are additional provenance. Supporting arbitrary IDs in finite precision has history-sized worst-case information cost.
- The closest direct collision is arXiv:2609.06872v3, which already supplies the Delta-specific transport theorem, replay certificate, sequential deletion/replacement and practical checkpoint trade-offs.
- Affine segment trees collide with retroactive data structures; RLS/QR downdates solve a different, order-independent objective.

The retained result is a trilemma/no-go boundary, not a candidate: exact native rollback requires provenance plus replay/retroactive storage; otherwise the guarantee is restricted to frozen traces or local approximation.
