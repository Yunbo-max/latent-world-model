# Independent source and novelty review — R16 v1

- Reviewer: /root/r16_sources
- Math artifact SHA256: 737f49385a232bdf9261c0fe7bec10955d0856ac7315e71ea226d7c78895d7d6
- Source audit SHA256: 442beb38d5f4c09a82f1c13488122e12a1bcf307e1500319de6cac3db0ccf3ca
- Mathematical/source verdict: PASS_CONDITIONAL
- Novelty verdict: INCONCLUSIVE_EXPAND_SEARCH
- Disposition: parked theorem/control; not an active or admitted candidate
- Execution: static mathematical/source review only; no model execution, training, scoring, or data/model download.

The exact ZOH derivation, ordering, signs, endpoint-constrained patch, limiting cases, rank bound, two-dimensional determinant witness, leakage witness, split commutator term, and affine-source discrepancy are internally correct under the declared frozen-generator ODE. The construction does not naturally guarantee endpoint overwrite; the KKT repair is exact but collapses to known normalized inverse-metric/RLS/PDN-style geometry.

The final audit adequately pins paper versions, sections/equations, and author-code commit/path/blob/function for KDA, EFLA, PDN, Longhorn, S4/S5, plus relevant low-rank matrix-function and diagonal-plus-rank-one eigensolver work. It correctly distinguishes:

- KDA's ordered decay/write recurrence;
- EFLA's pure rank-one or commuting scalar-decay flow;
- PDN's full inverse-Gram theory from its practical diagonal preconditioner;
- Longhorn's proximal recurrence and elementwise approximation;
- S4/S5 fixed-generator exact discretization;
- established Krylov/matrix-function and DPR1 eigensolver machinery.

No identical ML recurrence was established in the bounded search, but exact ZOH and its computational ingredients are established mechanisms. Novelty therefore remains unresolved. Reopen only with an independently justified joint ODE plus a structured exact or certified-approximate action with matched-budget benefit, or new causal evidence unavailable to the controls.
