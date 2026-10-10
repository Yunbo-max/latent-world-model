# Independent adversarial review — R14 v1

- Reviewer identity: `/root/r14_adversarial`
- Artifact SHA256: `9b08b160d5b0a28c6fcabb7d88ea5d1fadca373f370f580640be343aeb20dbca`
- Source-audit SHA256: `1ce269bade6d255ab14cf8acd4cec530ee1e8de89fa21c3016ce448f88d55d37`
- Verdict: `PASS_CONDITIONAL; KILL_AS_CANDIDATE`
- Blockers: none
- Execution: no project code, model, benchmark, training, inference, or scorer executed.

## Attacks performed

The reviewer independently attacked the dimensions and normalization, the pseudoinverse edge, the shared-residual tensor equivalence claim, the two-slot and multi-slot lower bounds, the hard abstention rule, the top-`B` support selector, and the stated state/compute costs. It also challenged whether continuous shrinkage had been mislabeled as exact abstention and whether the displacement regularizer represented literal Frobenius energy. The final bytes explicitly fix both issues: exact abstention is attributed to Eq. (7), a touch price, or a threshold, and `τ_i` absorbs `1/||k||²` when it prices edit energy.

No remaining formula, source, or semantic blocker was found. The phrase that non-certain slots abstain as damage diverges is valid as the `λ→∞` limit and is consistent with the later finite-parameter qualification.

## Disposition

The repair removes the identity-oracle premise and yields a sound conditional decision rule and ambiguity floor. It still composes known Bayesian routing, routed memory, and protected quadratic controls, while a direct per-slot router is the stronger same-information implementation. Kill as an architecture candidate; retain the theorem/control and warning against posterior-mean tensor common-residual writes. Experimental effect remains unknown.
