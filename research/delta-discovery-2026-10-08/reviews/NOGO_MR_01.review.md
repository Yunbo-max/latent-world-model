# NOGO-MR-01 independent review

- Artifact: `research/delta-discovery-2026-10-08/rejected/NOGO_MR_01.md`
- SHA256: `12e7bebba8e234c968ee6911580cbff07663c7ded188e70f385c486a9e63b06d`
- Reviewer: `/root/d06_closest_audit`, independent of derivation worker `/root/minimax_retention_nogo`
- Outcome: **ACCEPT as a scoped no-go/control result; not a candidate**

The reviewer checked the singular-value maximin upper bound, the equality structure, the zero/full erase boundaries, the distinction between the erase submap and the full ordered `ED` factor, the reversed-order contraction condition, and the frozen-affine/nonlinear boundary. Two review passes required the artifact to replace ambiguous minimax/correction language, state dimensions and real-domain assumptions, separate `G` from the full factor, and remove an unsupported universal claim about nonnormal condition numbers. The final exact bytes incorporate those changes.

Accepted scope: fixed `k,beta`, square linear old-state difference map, the same current-key residual-contraction constraint for every old state, and global minimum singular value as the metric. The result does not imply semantic, query-distribution, finite-precision, nonlinear-network or task optimality. No code, test, scorer or experiment was executed.
