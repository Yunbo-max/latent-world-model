# Independent review — ORTHOGONAL-VALUE-ROTATION-CONTROL

Reviewer: `/root/orthogonal_value_audit`. Semantic/source review only; no editing or project execution.

Decision: **kill as a general memory update; retain the isometric-editability theorem and normalized-value comparator**.

- Exact orthogonal editing while fixing protected outputs is possible iff the old and target columns have the same Gram matrix.
- A generic target, unequal norm, zero-to-nonzero write, or full protected span is infeasible.
- Householder is rank one but globally reflects every output sharing its active value direction; closest proper rotation is generally rank two.
- The key-local exact construction equals a full-step Delta update and therefore has identical cross-query interference.
- A state-dependent target-matching choice is a singular row replacement, not a reversible orthogonal state map.
- Orthogonal/unitary RNNs, Procrustes/Householder geometry, null-space editing, GSA2/QED and especially MOSE cover the broad stability/editing rationale.

The remaining result is a failure boundary: norm preservation does not imply association preservation, and protected-span rank consumes value-side editability. It is not a distinct candidate.
