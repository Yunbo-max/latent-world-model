# Independent adversarial review — R02 v2 final bytes

Reviewer: `/root/r02_v2_adversarial_review`  
Review date: 2026-10-10  
Artifact: `repairs/R02_CAUSAL_DR_QUOTIENT.v2.md`  
Exact final artifact SHA256: `255e687deff4c9f6ccde2130efc97e480e92f384fcadec8a905625d7033d921d`  
Source audit: `sources/R02_V2_CAUSAL_DR_QUOTIENT_SOURCE_AUDIT.md`  
Source-audit SHA256: `b2fa8474edf4c1f66ee551b5319157cbcd06baf2b10b4f225e3244b594338a81`

## Verdict

**PASS only as conditionally correct theory/debugging control.** No candidate admission, independent-method novelty, minimal recursive-width equality, stochastic-kernel certificate, empirical result, or state/sample/compute advantage is established.

## Final-byte adversarial checks

1. **One-step coarsening and DR language — PASS.** Equations (1)–(3) are correct under the declared full-history randomization/consistency assumptions and positive coarse propensity. The final text distinguishes structural full-history propensity sufficiency from accidental zero covariance. A learned nuisance still requires the usual fold/training sigma-field and persistent-dependence handling, already retained as a boundary rather than silently solved.

2. **Support and sequential sufficiency — PASS.** Equations (4)–(6) are explicitly strong sufficient conditions, not a necessity claim. Exact-ratio ledgers, exact quotient action values and marginalized ratios remain separate weaker routes. Quotient support is used together with exact target/behavior factorization; the artifact separately preserves hidden within-cell zero-support as a failure mode when that factorization is absent.

3. **Fixed-family lower bound — PASS.** Equation (9) is now restricted to a fixed declared finite scalar family, fixed right quotient and ambient local perturbations. It is stated only as `r >= r_F`, not as an existence or equality theorem. Prediction 4 also retains equality as requiring a recursively closed construction.

4. **Recursive fixed-point and stochastic-kernel gaps — PASS.** The final bytes state that next-quotient observables depending on `W` create an invariant-subspace/fixed-point problem. They also state that finitely many moments/Jacobians cannot certify equality of the stochastic kernels in (4); full relevant test-function separation or a justified parametric kernel family is required. The local tangent/global fiber distinction remains explicit.

5. **Minimax quantifiers and native realizability — PASS.** The full-width witness now has the correct order: first fix any sub-full `W`, then permit an adversarial lawful rank-one observable in its discarded direction. This proves only lack of a uniformly exact fixed right quotient over that formal class and explicitly does not prove native language-model realizability.

6. **R18 dimension comparison — PASS.** Monotonicity is claimed only when policy/transition observables are added to the same fixed scalar family. The artifact explicitly denies a universal dimension comparison with R18's complete-joint-state quotient.

7. **Ledger accounting — PASS.** Offline `O(T)` log storage, possible `O(1)` online ratio accumulation, analysis information/storage and recurrent model-state coordinates are separated. The text correctly says none of these makes the quotient Markov. Target propensity may in practice be recomputed rather than logged; this does not change the retained no-free-side-information conclusion.

8. **Collision/distinctness — PASS.** Hao et al. directly collide with the OPE state-abstraction mechanism, while R18 supplies recursive/global quotient geometry. The fixed Delta `XW` translation and covariance witness are useful lineage-specific diagnostics only. The artifact correctly retains `candidate_delta=0`, major functional collision, empirical unknown, and parked attempt 2/3.

## Required retained scope

- Treat equations (1)–(3) and the strong conditions (4)–(6) as conditional identification statements, not proof that a learned quotient satisfies them.
- Treat equations (8)–(9) as a fixed-`W`, fixed-family local lower bound. A state/time-dependent `W`, reachable-manifold restriction, global nonlinear quotient or arbitrary stochastic kernel needs a new derivation.
- “Compression may reduce overlap” should be read as degrading effective/represented overlap or hiding rare support, not changing the underlying logged behavior support by algebra alone; this wording is non-blocking because no overlap benefit is claimed.
- Any final-attempt reopening still requires a prefix-checkable recursively closed construction and matched-information advantage over Hao-style abstraction, R18/full-state sensitivity, exact-ratio ledgers and direct recurrent Q/policy prediction.

No project/upstream code, software tests, model execution, benchmark scoring, training, inference, data/model download, GPU work, paid service, or Docker was used.
