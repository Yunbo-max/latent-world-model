# R14 v3 repair-line screen — observable-equivalence closure

Scope: mathematics, primary-source and native-measurement feasibility only. No project code, benchmark, training, inference, scoring, data/model download or GPU work was executed.

## Bounded clues for substantive attempt 3

| Clue | Exact remaining defect after v2 | Patch tested | Decision |
|---|---|---|---|
| Lawful tokenwise provenance certificate | v2 assumes an externally valid interval for `p=P(J=1|F_t)` but does not show when such an interval can be nontrivial | put the entire causal record, calibration state and updater randomness into one observable `O`; compare two latent worlds by total variation and derive the coverage and decision-risk consequences | **selected**: this directly tests whether the remaining information gap can be repaired without adding an oracle |
| Robustify every quadratic coefficient | v2 only robustifies `p`, not residual, interference cost, Hessian or future Jacobian | place all coefficients in an ambiguity set and solve a generic robust QCQP | not selected: it is ordinary robust optimization, increases specification burden and still cannot identify provenance |
| Add an unknown/new slot or acquire evidence | closed-world routing can corrupt an absent identity | add allocation or an active query | not selected: both change state/information/latency and must be compared with an event store or controlled sensing under the same budget; R08 already covers value of information |

## Selected test and success condition

The selected child asks whether any prefix-measurable certificate or Delta statistic can distinguish two worlds that generate the same, or nearly the same, observable record but require opposite slots. Success as a repair would require either:

1. a nontrivial valid certificate derived from the existing observable law; or
2. a Delta-specific action with smaller worst-case risk than the direct same-information minimax router.

The derivation in `R14_OBSERVABLE_EQUIVALENCE_CLOSURE.v3.md` shows that neither is possible under the declared two-world family. Uniform certificate validity forces the full interval on the common observable mass, and every updater pays a sharp Le-Cam-style risk floor. At exact observational equivalence the v2 full-interval action attains the floor, so the direct minimax router is already optimal.

## Lineage disposition

- parents preserved byte-for-byte: `R14_POSTERIOR_PROVENANCE_WRITE.v1.md` and `R14_CREDAL_PROVENANCE_WRITE.v2.md`;
- this is substantive attempt 3 of 3;
- retained delta: a sharp observable-equivalence certificate-collapse lemma, an approximate-TV minimax risk lower bound, and a data-processing boundary for any derived Delta statistic;
- contribution status: useful terminal theorem/debug control, not a new updater;
- candidate delta: 0;
- empirical status: unknown; no execution was authorized or performed;
- disposition: park R14 with the lineage exhausted.

Reopen only after a genuinely new causal evidence channel, a stated distributional assumption supporting conditional validity, or a native action-level record changes the observable experiment. Such information must be supplied at the same state/compute/latency cost to the direct Bayes/minimax router and other controls.
