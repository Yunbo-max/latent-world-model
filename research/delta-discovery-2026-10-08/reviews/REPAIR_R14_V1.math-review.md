# Independent mathematical review — R14 v1

- Reviewer identity: `/root/r14_math_derivation`
- Assignment: independent derivation and exact-byte recheck
- Artifact: `repairs/R14_POSTERIOR_PROVENANCE_WRITE.v1.md`
- Artifact SHA256: `9b08b160d5b0a28c6fcabb7d88ea5d1fadca373f370f580640be343aeb20dbca`
- Verdict: `PASS_CONDITIONAL`
- Execution: no project code, model, benchmark, training, inference, or scorer executed.

## Independent checks actually performed

The reviewer independently re-derived the minimum-Frobenius rank-one action, differentiated the posterior-averaged quadratic, and checked the positive-definite and singular pseudoinverse/range cases. Equations (2)–(4) have the declared dimensions and signs. The scalar wrong-slot specialization correctly produces the `(1-π_i)λ_i` term.

The reviewer separately recomputed the tensor-address normalization and confirmed that normalized address `k⊗π` yields the shared residual displacement in Eq. (5), while the Bayes action uses slot-specific residuals, signed terms, and curvature. The equality condition, two-slot counterexample, two-world and uniform-m-slot ambiguity floors, hard full-write risks, and the top-`B` gain rule were all checked. The revised text correctly distinguishes continuous shrinkage from literal abstention and states the `1/||k||²` scaling of Frobenius edit energy.

## Non-blocking scope caveats

- On any zero-posterior block, exact tensor/Bayes equality additionally requires `π_i r_i-bar c_i=0`; otherwise the tensor block is forced to zero while the signed local surrogate may prefer a nonzero action. This strengthens, rather than weakens, the non-equivalence result.
- The stated `O(m d_v²)` damage-matrix state assumes the online sufficient aggregates `barΛ_i` are streamed or directly predicted. Explicit materialization of every raw world-conditioned `Λ_{i|j}` would cost `O(m² d_v²)`.

These are estimator/interface conditions, not algebraic defects. The theorem remains conditional on a supplied calibrated posterior and declared local quadratic. It does not establish empirical benefit or scientific-admission novelty.

## Disposition

Mathematical correctness: conditional pass. Candidate status: no uplift; retain as a theorem/control and keep the architecture line parked.
