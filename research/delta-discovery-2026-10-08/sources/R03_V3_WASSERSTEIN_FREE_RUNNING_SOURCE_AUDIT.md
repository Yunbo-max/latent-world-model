# R03 v3 Wasserstein free-running safety — source and collision audit

Audit date: 2026-10-10  
Artifact under audit: `repairs/R03_WASSERSTEIN_FREE_RUNNING_SAFETY.v3.md`  
Scope: primary-source/formula audit only; no reproduction or model execution.

## Frozen atomic claim

For complete free-running closed-loop state laws, a Wasserstein-Lipschitz reference kernel and uniformly bounded action-dependent kernel mismatch imply `delta_(h+1) <= kappa_h delta_h + epsilon_h`; a Lipschitz protected loss converts the unrolled law-distance bound into an expected-harm certificate. A rank-one Delta write can cheaply instantiate only the initial displacement under an explicit product metric. The recurrence and value consequences are generic established perturbation mathematics.

## Primary-source comparison

| Neighbor | Fixed material inspected | Mechanism overlap | Residual difference / decision |
|---|---|---|---|
| Rudolf & Schweizer, *Perturbation theory for Markov chains via Wasserstein distance* | arXiv:1503.04123; §2 Wasserstein ergodicity and ergodicity coefficient; §3.1 Theorem 3.1 and Corollary 3.2, especially the geometric initial-law plus kernel-perturbation bound; published Bernoulli 24(4A), DOI `10.3150/17-BEJ938` | Directly bounds nth-step law differences of perturbed Markov chains from Wasserstein contraction/ergodicity and transition discrepancy. | This is the strongest direct collision with the v3 recurrence. R03 only specializes the initial discrepancy to a Delta write and uses a finite nonhomogeneous horizon. |
| Asadi, Misra & Littman, *Lipschitz Continuity in Model-based Reinforcement Learning* | PMLR 80 (ICML 2018), official PDF; Definition 3/equations (3)--(4), Lemma 1, Theorem 1/equation (multi-step error), value-error section; official supplementary PDF for omitted proofs | Uses Kantorovich--Rubinstein duality and a Lipschitz transition model to accumulate one-step Wasserstein error geometrically, then bounds value error. | Covers the same compounding-error/value logic in RL. R03's closed-loop action-vs-no-write framing is an application, not a new principle. |
| Ferns, Panangaden & Precup, *Metrics for Finite Markov Decision Processes* | arXiv:1207.4114 (journal version of the finite-MDP bisimulation-metric line); fixed-point metric and value-difference bounds | Transition-law Wasserstein terms and reward differences define a bisimulation metric controlling value similarity. | Strong collision for choosing a state metric tied to future value; warns that an arbitrary hidden-state Euclidean metric is not automatically task meaningful. |
| Neufeld & Sester, *Bounding the Difference between the Values of Robust and Non-Robust Markov Decision Problems* | arXiv:2308.05520, version displayed 2026-03-22; Standing Assumptions 2.1--2.4, equation (2.4), Theorem 3.1/equation (3.1) | Bounds robust/nonrobust value differences linearly in a Wasserstein transition ambiguity radius under Lipschitz assumptions. | Direct robust-MDP/value-bound collision; R03 does not create a new robust-control objective. |
| Weed & Bach, *Sharp asymptotic and finite-sample rates of convergence of empirical measures in Wasserstein distance* | arXiv:1707.00087; finite-sample/asymptotic rates on compact metric spaces | Establishes dimension/metric-complexity-dependent empirical Wasserstein convergence. | Supports the measurement-cost warning: full-state empirical `W_1` is not a free finite-variance certificate. |
| Existing R03 v1/v2 packet | `R03_PROTECTION_AWARE_LOGGING.v1.md`; `R03_COUPLED_HORIZON_SAFETY.v2.md`; their exact-byte reviews/source audits | v1 supplies exact rank-one protected-query displacement and safe-design feasibility; v2 supplies full coupled-state same-path gain/tube conditions and the explicit free-running limitation. | v3 changes the comparison object to state laws and preserves all prior counterexamples outside its stronger kernel assumptions. |

## Formula facts checked

1. Rudolf--Schweizer's Corollary 3.2 has the same qualitative form as the homogeneous v3 law bound: a geometrically decaying initial-law term plus a geometric sum of kernel perturbations. Therefore the recurrence cannot be claimed as novel.
2. Asadi et al. Theorem 1 bounds n-step Wasserstein error by one-step error times a geometric sum of a Lipschitz constant. Their official PDF also states the Kantorovich--Rubinstein dual form used to pass from law distance to Lipschitz observables.
3. Neufeld--Sester explicitly require Lipschitz transition kernels and rewards and obtain a value-gap upper bound linear in the Wasserstein ambiguity radius. Their result is robust-control/value analysis, not Delta memory, but it covers the general value-consequence claim.
4. Bisimulation metrics make the metric/task relationship explicit. Merely selecting a state metric that makes `kappa` small is not enough; the protected loss must be Lipschitz in the same predeclared metric.
5. The exact rank-one formula belongs to the Delta lineage, but only bounds the immediate memory-block displacement. It does not reduce the dimension or complexity of later full-law certification.

## Implementation and code-interface status

These closest works are mathematical perturbation/value-bound papers; no author implementation is required to verify the closed-form recurrence. Asadi et al.'s official PMLR page supplies paper and supplementary proofs; the artifact does not attribute an implementation result to it. Existing R03 audits already pin the author implementations relevant to safe logging, SEAL, ACL/SRWM, and the Delta lineage. No third-party repository is presented as author code, and no source code was executed.

## Native measurement audit

The packet's pinned LongMemEval/LongMemEval-v2, SEAL continual, CITB, TRACE, bAbI, and LAMBADA assets measure endpoint accuracy/retention or task-level forgetting. They do not natively expose all of: the complete action-time Markov state, a declared metric, per-action transition kernels, simultaneous `kappa/epsilon` certificates, protected-validity labels, and paired free-running counterfactual laws. Endpoint evaluation can falsify a claimed performance benefit but cannot by itself validate the mechanism. This remains a measurement gap, not a fabricated negative result.

## Novelty and disposition

Verdict: **strong functional collision / retain as theory-control only**. The v3 patch is useful because it repairs a scope error and shows exactly what extra assumptions are needed to move from shared-path sensitivity to free-running expected harm. The generic recurrence, geometric accumulation, and value consequence are already covered. No evidence supports first/new/unique language, a new architecture, a new updater, or a same-budget statistical/computational advantage. Candidate delta remains zero; R03 is exhausted after attempt 3/3.

## Evidence limitations

- The bounded source audit is sufficient to reject a generic novelty claim; it is not an exhaustive proof that no narrower Delta theorem exists.
- Primary sources were read for their formulas/assumptions. No experimental reproduction was performed.
- The empirical behavior, tightness of certificates on language models, and feasibility under the project's later compute budget remain unknown.

