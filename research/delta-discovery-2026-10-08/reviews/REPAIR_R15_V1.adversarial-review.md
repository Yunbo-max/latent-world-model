# Independent adversarial review — R15 v1

- Reviewer: `/root/r15_adversarial`
- Artifact: `repairs/R15_INTERVENTION_RANK_BOUND.v1.md`
- Artifact SHA256: `23dd9536139c1beb4858a0407c4e21c1f32e6750e6d85521bec9eeba1c6a9c53`
- Verdict: `PASS_CONDITIONAL_CONTROL; PARK_NOT_CANDIDATE`
- Execution: read-only mathematical/source inspection; no code, model, benchmark, training, inference, scorer, data/model download, GPU, or Docker.

## Attacks and corrections

The first exact-byte audit returned `REVISE`. It found that the quadratic feature Gram requires fourth-order-equivalent action moments, that a noisy paired baseline cancels rather than literally reveals the intercept, and that fixed recorded descendants had been conflated with lawful common-random-number free-running pairing. It also required the packet to acknowledge that the scalar Gram condition, action-space projection, finite-horizon/free-running boundary, OPE support, and Ouroboros collision were already recorded in `STEP2_PROJECTED_DELAYED_CREDIT.md` and `STEP2_RECURSIVE_RANDOM_METRIC_CONTROL.md`.

All four corrections are present in the final bytes. The reviewer rechecked support/exchangeability, augmented-state dimensions, the full-rank iff proof, `q` and action-count wording, the scalar binary endpoint limitation, horizon tail, sequential positivity/OPE, action/meta-gradient distinction, `O(KH)` one-time replay, and `2^H` exhaustive binary-sequence cost.

## Surviving counterexamples and collision

- With no overlap, two worlds share all factual observations and disagree on the unchosen action.
- Randomized arm marginals do not identify a historical unit's individual-effect sign.
- Finite horizon can reverse at the next step; the discounted bounded-loss tail is the only unconditional finite-H protection stated.
- Fixed factual post-action feedback cannot lawfully be reused across counterfactual branches.
- The multivariate intervention-rank theorem is generic response-surface design and a consolidation/generalization of project controls, not a new Delta mechanism.

## Final decision

The conditional theorem/control is correct and useful for ruling out under-probed learned updaters. It neither supplies a new updater nor proves empirical benefit. Park after attempt 1, preserve R02/Step2 as the primary mechanism lineage, and add zero active/admitted/selected candidates.
