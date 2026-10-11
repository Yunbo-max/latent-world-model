# Independent final-byte mathematics review — R18 v2

- Reviewer: `/root/r18v2_math_derivation`
- Artifact: `research/delta-discovery-2026-10-08/repairs/R18_PREFIX_CAUSAL_ROBUST_QUOTIENT.v2.md`
- Reviewed SHA256: `df90d64c215268d83d3a499be9e527a994a69d8b8d4a7969fbeffb8618e5f813`
- Verdict: **PASS, conditional theorem/control; not candidate admission**

The first exact-byte review failed because the edge-read convention had an inconsistent leaf base, the recursive quotient was not constructed explicitly, and the constrained all-horizon automaton fixed point was missing. The bound artifact was revised and independently re-read at the SHA above.

The final bytes pass the following checks:

1. Edge timing and the base case are consistent: an edge read occurs before its transition and a true leaf with no outgoing read has invisible space `R^n`. The paired-path witness preserves transition/read pairing; rectangularizing the marginals is only a conservative sufficient certificate.
2. The quotient descent is dimensionally correct: `C_e=Cbar_e Q_parent`, `Q_child J_e=Jbar_e Q_parent`, and therefore the affine quotient recursion follows. Its minimum linear width is the row rank of the complete lawful descendant-read operator.
3. The finite-automaton operator is monotone descending and reaches the greatest state-indexed invariant family after at most `n|A|` total strict dimension drops. The stationary common-subspace recurrence is the one-state rectangular specialization.
4. The current-update/reference ordering is correct. With current linear part `A_t` and reference entrance `P_t`, exact affine recoverability is `ker A_t subseteq ker(O_T P_t)`, equivalently `O_T P_t=L A_t`.
5. If `K_t` spans `ker A_t`, the exact real-linear side-ledger width is `rank(O_T P_t K_t)`. The proposed `M=U^T O_TP_t` attainment is valid on the lost subspace.
6. The tree is prefix measurable and fixed across each current-update fiber; coverage is prefix conditional and simultaneous. Finite-tree, all-horizon, nonlinear, discrete-routing and same-labelled-word scopes are separated.

No mathematical correction remains for the stated affine-tree theorem. This does not prove semantic validity, empirical improvement, global nonlinear safety, originality or a cost advantage over the direct ledger/automaton control.

Final disposition supported: attempt 2/3 parked, `candidate_delta=0`, empirical effect unknown.
