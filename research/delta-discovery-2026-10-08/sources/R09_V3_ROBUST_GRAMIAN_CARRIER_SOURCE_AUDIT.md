# R09 v3 robust-Gramian-carrier source, code, distinctness, and measurement audit

Audit target: `repairs/R09_ROBUST_GRAMIAN_CARRIER.v3.md`. Cutoff: 2026-10-11. Scope is primary-source/formula, author-interface, internal-collision and native-measurement review. No code, model, data, test, training, inference, scoring or benchmark was executed.

## 1. Preserved lineage evidence

R09 v1 (`d0bfe49...`) and v2 (`aa78f4f...`) remain unchanged. Their source audits already pin original/parallel DeltaNet, PDN, KDN, OWM/GEM/A-GEM/OGD/EWC, AlphaEdit/O-Edit, RLS/QR-RLS, classical observability/energy Gramians, DDP/iLQR and the fixed native endpoints. V3 does not re-count those mechanisms.

The new atomic claim is limited to the minimum **common exact linear carrier** of a finite prefix-declared family of transported PSD factors and the Delta counterexample showing that this carrier can be full width even when every realized Gramian is rank one.

## 2. Decisive constrained-language and switched-system collision

Mert Bastug, Mihaly Petreczky, Rafael Wisniewski and John Leth, *Model Reduction of Linear Switched Systems by Restricting Discrete Dynamics*, arXiv:1409.1444v2, is the closest functional collision for a declared lawful mode family:

- Definition 8 and equation (12) define the unobservable subspace restricted to a regular language `L` of admissible mode words; equation (13) defines the associated suffix language;
- Lemma 4 identifies the quotient preserving `L`-equivalent input-output behavior;
- Algorithm 2 recursively constructs the relevant dual row spaces by automaton state.

R09 v3's `V_t^*` is the finite-horizon transported-output/row-space dual for a finite prefix-declared language. Its Gramian support notation and Delta witness are specializations, not a new observable-carrier or quotient mechanism. The paper referenced an author webpage for MATLAB material, but this audit found no immutable author-repository revision suitable for a code pin; none is fabricated.

Mihaly Petreczky, Laurent Bako and Jan H. van Schuppen, *Realization theory of discrete-time linear switched systems*, arXiv:1103.1343, gives the noncommutative mode-product realization setting and observability/rank minimality criteria, further blocking a priority claim for the common transported row space.

Igor Pontes Duff, Sara Grundel and Peter Benner, *New Gramians for Linear Switched Systems: Reachability, Observability, and Model Reduction*, arXiv:1806.00406v1 / IEEE TAC 2020, is the closest primary source.

- §2.2, Definition 1, equations (10a)--(10b) construct switched reachability/observability Gramians as sums of factor products over mode words.
- Equations (11a)--(11b) give generalized Lyapunov equations.
- Theorem 3 states `R=range(P)` and `O=range(Q)`.
- §4 uses global projection matrices shared across modes for reduced-order systems.

These are the generic Gramian counterparts of v3's factor-span/range identity and common carrier. V3 is finite-horizon, discrete and Delta-coordinate specialized; it cannot claim the Gramian range, switched observable space or common projection idea as new.

The paper also cites constrained-switching reachability/observability reduction and mode-dependent local/global projections. R18 v2 already reads that line for the exact prefix-lawful quotient; v3's common carrier is the PSD-Gramian dual specialization.

Philipp Schulze and Benjamin Unger, *Model reduction for linear systems with low-rank switching*, arXiv:1801.09445, studies low-rank changes between switched coefficient matrices through an envelope system and standard model reduction. It blocks the broad claim that low-rank switching creates a new reduced-state principle.

## 3. Low-rank Gramian/Lyapunov collision

Jing-Rebecca Li and Jacob White, *Low Rank Solution of Lyapunov Equations*, SIAM J. Matrix Anal. Appl. 24(1), DOI `10.1137/S0895479801384937`, develops Cholesky-factor ADI for low-rank Lyapunov solutions and relates low-rank factors to Krylov/invariant-subspace approximations. R09 v3's exact finite factor stack is simpler, but low-rank Gramian factorization and reduced solves are established numerical-linear-algebra controls.

Pontes Duff et al. explicitly note low-rank factorized solutions in the large-scale setting and cite generalized Lyapunov/Krylov methods. Thus a small realized Gramian or Woodbury solve is not itself a contribution.

## 4. Delta transition/code interfaces

Siems et al., *DeltaProduct: Increasing the Expressivity of DeltaNet Through Products of Householders*, arXiv:2502.10297 / NeurIPS 2025, explicitly characterizes Gated DeltaNet/RWKV-7 transitions as diagonal plus rank one and DeltaProduct as products of multiple generalized Householder factors. The primary author repository is pinned here at:

- `automl/DeltaProduct@d62241a81d07aa32b1b65e7d17377f6a7cd0a5d8`;
- README blob at that commit states that maintained integration is in Flash Linear Attention, documents `num_householder`, and distinguishes one versus multiple factors;
- repository folders `flash-linear-attention`, `state_tracking` and `language_modeling` are author-provided experimental interfaces.

Static inspection only. DeltaProduct expands the legal transition products but supplies neither the action-time future factor family nor a protection Gramian/core. It strengthens, rather than evades, the possibility that prefix-compatible transported factors span many directions.

R09 v2 already pins KDN author code `ngocbh/kalman-delta-networks@53e437be...`: KDN carries filtering uncertainty under a declared state-space model, not the future protected-query carrier. PDN/RLS remain inverse-metric controls.

## 5. Internal collisions and exact residue

- **R18 v2:** exact path-conditioned prefix-robust observable quotient, common invariant-subspace fixed point, minimum linear width and full-state-collapse examples. This is the strongest internal collision.
- **R16 v2:** exact active-core reduction under structured spectral conditions, plus dense-basis/full-width and hidden-transform-cost boundaries.
- **R11 v2:** factor-core compression logic and the obligation to charge transported-factor construction and coordinates.
- **R20 v3:** sharp spectral transfer under a lawful metric sandwich and impossibility of certifying that sandwich over unrestricted identical-prefix futures.
- **R09 v2:** transported Gramian, complete-state qualification and swapped-anisotropy minimax lower bound.

The only retained v3 residue is the concise Delta counterexample `A_i=I-beta e_i e_i^T`, `Q=11^T`, for which each `G_i` is rank one but the common exact carrier is `R^d`. This is a useful debugging theorem against an invalid rank-one-to-small-state inference. It is not a distinct algorithmic operation.

## 6. Native measurement audit

The packet-fixed LongMemEval, LongMemEval-v2, EvoMemBench, AToKE, SEAL, CounterFact/ZSRE/KnowEdit, bAbI, LAMBADA, RULER and BABILong assets expose downstream answer/token/edit endpoints. None jointly exposes, **before the write**:

1. complete state and a declared carrier;
2. an action-indexed guarantee/calibrated event that all relevant future key/query/Jacobian factors remain in it;
3. the protected PSD core or ambiguity set and grounded old/new validity;
4. randomized propensity or paired fixed-continuation outcomes;
5. native endpoint score plus matched bytes, traffic, FLOPs and latency for both the Gramian controller and a direct low-rank action/Q predictor.

Hidden-state logging or constructing factor labels would be custom instrumentation, not a native scorer. Realized future factors cannot be used to choose the earlier write without leakage. Existing endpoints can later falsify usefulness after an implementation, but cannot identify the v3 mechanism.

## 7. Cost and strongest same-information control

A width-`r` basis costs `O(dr)` state unless it is a fixed coordinate grouping or separately charged fast transform. A symmetric core costs `r(r+1)/2`; basis discovery/tracking, calibration, core update/factorization and complete-state derivatives must be charged. An explicit mode tree may be exponential and a merged common span may become full width. The physical write remains `O(dm)`.

The strongest same-information control is direct prediction/robust optimization of the coefficients in `span(k,V)`, or direct robust action/Q prediction, after charging the same basis/features. V3 establishes no matched-total-cost advantage over that control.

## 8. Bounded novelty conclusion

Primary-source and author-interface search through 2026-10-11 finds direct functional coverage by constrained-language observability/quotient construction, switched-system Gramian ranges/common projections, low-rank Lyapunov factors and low-rank switching, plus direct internal coverage by R18/R16/R11/R20. No inspected publication or fixed author implementation states verbatim the Delta-specific combination of the finite-family carrier and the exact `A_i=I-beta e_i e_i^T`, `Q=11^T` witness. This bounded absence is not priority evidence: the functional carrier is already covered and the witness is an elementary Delta specialization.

Decision: **source-supported conditional theorem/debug control; attempt 3/3 exhausted; candidate delta zero; empirical effect unknown**. Reopen only with the native causal object above or a materially different Delta structure proving a smaller lawful statistic and matched-cost advantage.
