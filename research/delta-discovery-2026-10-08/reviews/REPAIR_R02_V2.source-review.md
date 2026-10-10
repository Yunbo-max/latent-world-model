# Independent source/closest-work review — R02 v2 final bytes

Reviewer: `/root/r02_v2_source_review`  
Review date: 2026-10-10  
Math artifact: `research/delta-discovery-2026-10-08/repairs/R02_CAUSAL_DR_QUOTIENT.v2.md`  
Math artifact SHA256: `255e687deff4c9f6ccde2130efc97e480e92f384fcadec8a905625d7033d921d`  
Source audit: `research/delta-discovery-2026-10-08/sources/R02_V2_CAUSAL_DR_QUOTIENT_SOURCE_AUDIT.md`  
Source-audit SHA256: `b2fa8474edf4c1f66ee551b5319157cbcd06baf2b10b4f225e3244b594338a81`

## Verdict

**PASS for the bounded source/collision audit and `CONTROL_ONLY` disposition.** The prior two source-precision findings are resolved in these exact final bytes. This is not a field-wide priority certification, author-code reproduction, or empirical-validation pass.

## Primary-source findings

1. **Sequential DR is represented correctly.** Jiang and Li (ICML 2016) give contextual-bandit DR in Eq. (8), recursive step-wise IS in Eq. (9), and recursive sequential DR in Eq. (10). Their discussion requires the evaluated policy and fitted reward/value objects to be independent of evaluation samples (or fitted through an appropriate independent/cross-fitted construction). R02 v2 retains this estimator and asks when its state-dependent objects descend to a quotient; it does not claim a new DR estimator.

2. **Hao et al. are a direct functional collision.** In arXiv:2406.19531v3, Definition 1 is target-policy irrelevance; Definition 2 requires reward and abstract-next-state Markov structure; Definition 5 imposes reward/transition model irrelevance; Definition 6 and Eqs. (6)–(8) impose behavior-policy and backward-transition irrelevance, including the history-dependent behavior-policy refinement. Lemma F.2 and Theorem 4 cover Fisher consistency of value-based, SIS, MIS, and doubly robust OPE after the stated abstractions. The final audit now correctly says that Theorem 4 explicitly invokes Assumptions 1–3—boundedness, coverage and stationarity—and separates nuisance-estimator assumptions used in finite-sample/MSE analysis.

3. **The implementation interfaces are accurately summarized.** Hao et al. Appendix B specifies a forward encoder with reward, transition, target-Q and anti-collapse/diversity losses, and a backward encoder with behavior, inverse, density-ratio and smoothness losses. The paper's Appendix C links the author repository `pufffs/state-abstraction`.

4. **The collision has a bounded scope.** Hao et al.'s main setup is a finite-state, stationary ground MDP, although the refined behavior policy after iterative abstraction may depend on abstract history. It does not state R02's exact one-step covariance identity, fixed-right-factor Delta tangent condition, or fixed-family transported-covector width lower bound. Those pieces remain valid lineage-specific diagnostics, not a new general compressed-OPE method.

5. **Classical and OPE-specific controls are correctly characterized.** Li, Walsh and Littman organize abstractions by policy/value/model invariances, including reward and transition preservation. Allen et al. learn Markov abstractions using inverse-model and density-ratio structure. STAR is an OPE framework based on abstract reward processes. Xie–Ma–Wang replace trajectory ratios with state-marginal ratios under MDP assumptions and establish polynomial-horizon error behavior under their stated conditions.

6. **Pavse–Hanna is now explicitly included.** arXiv:2212.07486 / AAAI 2023 directly combines state abstraction with MIS, proves consistency and conditional variance benefits, and identifies reward/transition conditions needed for abstract-ratio estimation. This source strengthens the functional-collision verdict and closes the prior close-source omission.

## Author-code availability

Hao et al. Appendix C links `https://github.com/pufffs/state-abstraction`. On the review date that URL returned HTTP 404, and public GitHub search did not expose a readable repository or immutable replacement. The final audit correctly treats Appendix B as a paper-level interface and records author implementation bytes as unavailable. No third-party repository can close that gap.

The fixed Vowpal Wabbit, SEAL, LongMemEval, MIPS/OffCEM and Open Bandit Pipeline implementation evidence is inherited from the already bound R02 v1/R15 audits. R02 v2 makes no new execution or reproduction claim from those records.

## Novelty and measurement decision

The supported residual is narrow: the Delta fixed-right-quotient translation, its local fixed-family joint propensity/value/transported-credit row-span lower bound, and explicit accounting for retained ratio information. The final artifact also correctly limits Eq. (9) to a lower bound rather than an existence/equality theorem, distinguishes scalar moment closure from full kernel equality, and restricts the full-width witness to a minimax formal class without claiming native realizability.

The general scientific mechanism—compressing state while preserving policy, reward/value, transition and ratio objects for OPE—is directly covered by Hao et al., Pavse–Hanna, STAR, MIS and classical abstraction/homomorphism work. `MAJOR_FUNCTIONAL_COLLISION / CONTROL_ONLY`, architecture admission `0`, and empirical effect `unknown` are supported.

Open Bandit data exposes contexts, actions, rewards and behavior propensities, so it can measure generic one-step abstraction/AIPW behavior. It has no coupled recurrent Delta state or action-conditioned Delta transition. LongMemEval, bAbI and LAMBADA are endpoint tasks without randomized internal update actions, logged quotient propensities, quotient-fiber labels, or paired potential outcomes. The native Delta mechanism-measurement gap is supported; no experiment or new intervention protocol was designed or run.

## Final disposition

- `source_status`: `primary_sources_supported_final_bytes`
- `novelty_status`: `major_functional_collision_control_only`
- `author_code_status`: `paper_link_verified_but_repository_unavailable_2026-10-10`
- `measurement_status`: `native_delta_causal_quotient_gap`
- `candidate_admission`: `0`
- `empirical_status`: `unknown_not_executed`
- `mandatory_revisions`: `none`

No project/source code, model, benchmark scorer, training, inference, data/model download, GPU workload, paid service, or Docker was executed.
