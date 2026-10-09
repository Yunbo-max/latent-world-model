# Independent review — NOGO-DUAL-FRAME-04

Reviewer: `/root/checksum_revision_math`.  Semantic review only; no file editing or execution.

Decision: **accept as a scoped no-go/control; do not admit as a candidate**.

- Dimensions and exact encoded recurrence are correct.
- \(r=d\) is coordinate conjugacy; \(r>d\) is physically wider redundancy, not added logical semantic capacity while the state stays on the code subspace.
- The decisive syndrome result is correct: legal Delta perturbations are in \(\operatorname{range}(F)\) and are invisible to every parity check \(HF=0\).
- The \(d/r\) noise bound concerns the worst unit effective query direction under iid additive noise, not every fixed query.  Canonical-dual optimality is limited to exact linear left inverses under isotropic noise.
- Fixed-total-bit and erasure bounds require their stated quantizer/range/known-erasure assumptions.
- The query-aware optimum assumes \(W\succ0\); singular \(W\) gives an infimum unless a spectral floor is imposed.
- The arbitrary-diagonal-gate theorem is correct and leaves only monomial transforms or coordinate repetition; a dense frame hides substantial decode--gate--encode cost.

Classical tight-frame/erasure coding and the existing D05/STEPQuant/PDN controls cover the surviving numerical function.  No active-candidate residual remains.
