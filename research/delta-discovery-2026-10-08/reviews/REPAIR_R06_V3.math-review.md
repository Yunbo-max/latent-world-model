# Independent mathematical review — R06 v3

- Reviewer identity: `/root/r06_v3_math_review`
- Assignment: independently check dimensions, spectrum, product bounds, sampling competitive factor, residual/plasticity identity, edge cases and claimed scope.
- Artifact: `research/delta-discovery-2026-10-08/repairs/R06_SURVIVAL_MARGIN_PLASTICITY.v3.md`
- Artifact SHA256: `26fed27d5e5091c93bd8428c76b0dde5c7e6fd49dc930911247a90c311cd3ceb`
- Final-byte verdict: **PASS for the stated conditional theorem/control; not an empirical or novelty verdict.**

## Review reasoning

The final artifact correctly separates `d_k>=2`, `d_k=1`, and `k=0`. For `A=I-beta kk^T`, the displayed operator norm and minimum singular value follow from the exact eigenspaces. Repeated minimum-singular-value inequalities give the lower Frobenius product bound without any commutativity assumption; the upper product bound follows from nonexpansiveness. The endpoint examples establish sharpness.

The Kantorovich factor is valid only under the conditions the artifact now states: a nonempty positive-envelope finite frame, positive budget, fixed or prefix-measurable horizons, positive lower ratio, and inactive caps for both proportional designs. The artifact does not extend the result to active caps, semantic validity, action benefit, or full-network loss.

The identity `e_s^+=(1-rho_s)e_s` is dimensionally and algebraically correct. It establishes the advertised survival--plasticity tradeoff on the same rank-one factor. The uniform-horizon and infinite-product consequences are correctly conditional, and the multiple-microstep sentence is restricted to a fixed key/target and nonovershooting branch.

The full autoregressive Jacobian, post-factor decay, normalization/rescaling, and infinite-horizon limitations are explicitly separated from the frozen-memory result. Final source-precision wording in section 7 changes no mathematics.

## Corrections required during review

Earlier drafts needed explicit treatment of one-dimensional and zero-key cases, cap inactivity, horizon measurability, decay factors, the infinite-product condition, and the fixed-key scope of microsteps. Those corrections are present in the bound final bytes. No further mathematical edit is required.

This review does not admit a candidate and does not claim empirical benefit.
