# R02 v3 approximate causal/dynamic quotient — source, implementation, novelty and measurement audit

Audit date: 2026-10-10  
Scope: `repairs/R02_APPROXIMATE_CAUSAL_DYNAMIC_QUOTIENT.v3.md`; bounded formula/code collision audit, not empirical validation or exhaustive priority certification.

## 1. Preserved causal/OPE sources

**Jiang & Li, “Doubly Robust Off-policy Value Evaluation for Reinforcement Learning,” ICML 2016.**

- Primary paper: https://proceedings.mlr.press/v48/jiang16.html
- Eq. (8) is contextual-bandit DR and Eqs. (9)–(10) give the sequential recurrence with target/behavior ratios. R02 v3 does not modify that estimator.
- The v3 conditional-covariance identity descends from v2 and ordinary Cauchy–Schwarz/Grüss bounds. It is explicitly restricted to one action and quotient cell; it is not claimed as a new sequential-DR robustness theorem.

**Hao, Su, Hu, Szabó, Zhao & Shi, “Off-policy Evaluation with Deeply-abstracted States,” arXiv:2406.19531v3.**

- Full paper: https://arxiv.org/abs/2406.19531
- The v2 audit read Definition 1 (target-policy irrelevance), Definition 2 (reward and abstract-next-state Markov properties), Definitions 5–6 and Eqs. (6)–(8) (reward/transition, behavior-policy and backward-transition irrelevance), plus Lemma F.2 and Theorem 4 on consistency of abstract-state value, SIS/MIS and DR estimators.
- Appendix B's forward encoder already uses reward, transition, target-Q and anti-collapse objectives; the backward encoder uses behavior, ratio/inverse and smoothness terms. These are direct controls for any claim that merely learning a low-dimensional OPE state is new.
- The paper-linked author repository `pufffs/state-abstraction` was unavailable through the GitHub API on the audit date, so no immutable function-level implementation claim is made. This remains a source gap, not evidence against the paper.

Hao et al. is the closest OPE-specific collision. R02 v3's equations (2) and (6)–(12) are a lineage-specific error audit, not a new general abstraction estimator.

## 2. Strongest full-formula collision: approximate information states

**Subramanian, Sinha, Seraj & Mahajan, “Approximate Information State for Approximate Planning and Reinforcement Learning in Partially Observed Systems,” JMLR 2022.**

- Primary full paper: https://jmlr.org/papers/volume23/20-1165/20-1165.pdf
- Definition 7 (pp. 14–15) defines an approximate information state through an immediate-reward defect and an integral-probability-metric defect for the next compressed state. Eq. (10) gives the IPM dual expectation bound.
- Theorem 9 and Eqs. (14)–(17) recursively propagate those two defects into value/action-value error and a greedy-policy performance bound. Its finite-horizon indexing, lack of the v3 discount notation and IPM gauge differ, but the functional recurrence `current reward defect + continuation-function gauge times transition defect + next-step error` directly covers the main mechanism of R02 v3 equations (6)–(7).

**Pinned author implementation:** `info-structures/ais@d2eca3b5d19d28c0225253e35f01fd256c6a2f43`.

- `src/networks.py` implements LSTM history encoders `rho_net_lowdim`, `rho_net_moddim`, `rho_net_highdim` and reward/next-observation predictors `psi_net_*`; the high-dimensional `psi` variants include `psi_net_highdim_MMD` and `psi_net_highdim_KL`.
- `src/main.py` exposes `--AIS_state_size`, `--IPM` (its help lists `KL` and `MMD`, with default `MMD`, but argparse imposes no `choices` constraint) and `--lmbda`, then combines reward prediction, next-observation/IPM proxy and policy losses in `total_loss`.
- This is direct author-code evidence for learning a compressed recurrent state using reward and transition-observation defects. It is not Delta, OPE or DR, and it does not implement the v3 one-step covariance identity; nevertheless it blocks treating the quantitative dynamic quotient mechanism as new.

This formula-level and code-level collision is stronger than a generic “simulation lemma” resemblance.

## 3. Full-formula approximate-abstraction collision

**Abel, Hershkowitz & Littman, “Near Optimal Behavior via Approximate State Abstraction,” ICML 2016.**

- Primary PMLR paper: https://proceedings.mlr.press/v48/abel16.html
- Definition 9, Eq. (9), aggregates states whose declared action-dependent scalar differs by at most `epsilon`.
- Definition 13, Eq. (25), is the approximate-model abstraction: within a cell, per-action rewards and aggregate transition probabilities to every abstract state are within `epsilon`.
- Lemma 2, Eq. (26), turns those reward/transition tolerances into an explicit value/suboptimality bound. Its constants and optimal-policy setting differ from R02 v3's fixed-policy finite-horizon telescoping bound, but the functional mechanism—quantitative reward/transition abstraction error implying bounded value error—is directly covered.
- The paper's Theorem 1 and Eqs. (10)–(12) also give bounded-loss guarantees for approximate `Q*` abstraction. Thus “relax exact quotient equality to epsilon and bound value loss” is established prior work.

**Pinned author implementation:** `david-abel/state_abstraction@a8a8157e4fceea6bf1e8a1da3632b3c29cf6e260`.

- `Workspace and Code/stateAbstraction/src/stateAbstractor/StateAbstractor.java` exposes `phi(State,State)`, greedily groups ground states in `setupGroupingsOfGroundStatesIntoAbstractStates`, and constructs the abstract transition/reward objects in `setupAbstractDomainAndAbstractRewardFunctionAndAbstractTerminalFunction`.
- The implementation averages ground transitions and rewards within each cluster using `getSteadyStateWeighting`, then solves/exports an abstract policy back to the ground MDP. It is a concrete strong baseline for state aggregation plus abstract model construction, though not an OPE estimator or Delta memory implementation.
- `src/experiments/EpsilonExperiments.java` and the domain generators provide the paper's epsilon/compression experiments. The repositories were inspected statically at the pinned commits. No project/upstream code, bundled model asset, software test, benchmark, training, inference or scorer was executed; no separate dataset/model acquisition or experiment was initiated.

The author code confirms that the generic approximate-abstraction construction is not merely an abstract citation. It does not supply the v3 Delta coefficient-derivative identity, but that identity alone is not a distinct estimator or updater.

## 4. Bisimulation, simulation and state-aggregation controls

**Ferns, Panangaden & Precup, “Metrics for Finite Markov Decision Processes.”**

- Primary record/full paper: https://arxiv.org/abs/1207.4114
- It defines quantitative bisimulation/state-similarity metrics from reward and transition differences and relates those distances to value differences. The Wasserstein/Lipschitz branch in R02 v3 is in this established family.

**Li, Walsh & Littman, “Towards a Unified Theory of State Abstraction for MDPs,” 2006.**

- Primary PDF: https://rbr.cs.umass.edu/aimath06/proceedings/P21.pdf
- Exact policy/value/model abstractions and homomorphism-style reward/transition closure already frame the zero-defect limit used by R02 v2/v3.

Classical simulation-lemma/value-perturbation arguments also telescope one-step reward and transition errors over a horizon. R02 v3 keeps its proof self-contained and states its total-variation convention, so no identity is borrowed without conditions; novelty is nevertheless a major collision.

## 5. OPE-specific ratio/abstraction controls

- **STAR / Abstract Reward Processes:** Chaudhari et al., arXiv:2410.02172, https://arxiv.org/abs/2410.02172.
- **Marginalized IS:** Xie, Ma & Wang, arXiv:1906.03393, https://arxiv.org/abs/1906.03393.
- **State abstraction with MIS:** Pavse & Hanna, arXiv:2212.07486, https://arxiv.org/abs/2212.07486.

These works prevent treating compact state plus valid OPE ratios as a new residual by itself. R02 v3 correctly refuses to add its one-step covariance bound to its model-based value bound and call the result approximate DR.

## 6. Internal Delta lineage and distinctness

- R02 v1 supplies randomized finite Delta actions, logged propensities, AIPW/sequential-DR identification and delayed-outcome boundaries.
- R02 v2 supplies the exact quotient coarsening-bias identity and exact causal quotient conditions.
- R01 v3 supplies transported-credit right-quotient width conditions.
- R18 supplies complete-state global fibers, recursive closure, local joint-state Jacobians and side-code costs.
- R02 v3 adds a sharp conditional-variance tolerance, a separately scoped finite-horizon value-error recurrence, and the exact observation that the direct `A E W` term vanishes while hidden-state dependence survives through coefficient derivatives.

This is a useful debugging specialization. The first two mechanisms are established; the Delta derivative is narrow and gives no prefix-checkable construction or matched-cost gain. Distinct architecture/method contribution is therefore zero.

## 7. Native measurement feasibility

- The fixed Open Bandit Dataset/OBP evidence inherited from the R02 v1/v2 and R15 audits exposes recorded contexts, actions, rewards and behavior propensities. Treating recorded context as the fine covariate can instantiate a generic one-step coarsening/AIPW check, but the native asset does not expose hidden full histories, recurrent Delta fibers or coupled next-state dynamics.
- LongMemEval, bAbI and LAMBADA are endpoint tasks. They do not natively record randomized internal update actions, exact propensities, quotient-fiber pairs, target-reachable uniform reward/transition defects, or paired continuations.
- The AIS and Abel implementations use synthetic/POMDP or finite-MDP environments and their own value/performance evaluation. They establish generic constructions, not a native Delta self-update measurement object.

No reviewed native asset jointly measures the v3 causal and dynamic quantities. This is a measurement gap, not a negative result. No benchmark, label, case, metric or result was manufactured.

## 8. Audit decision

- Mathematical source support: conditional, subject to independent final-byte review.
- Functional novelty: **MAJOR_FUNCTIONAL_COLLISION / CONTROL_ONLY**.
- Architecture candidate: not admitted.
- Empirical effect: unknown; no execution.
- Attempt status: 3/3 exhausted after final-byte review; park unless a lawful prefix-estimable upper-confidence certificate and matched-information advantage are supplied.

The cited repositories were inspected statically at pinned commits. No project/upstream code, bundled model asset, software test, benchmark, training, inference or scorer was executed; no separate dataset/model acquisition, GPU job, paid service, Docker action or experiment was initiated.

