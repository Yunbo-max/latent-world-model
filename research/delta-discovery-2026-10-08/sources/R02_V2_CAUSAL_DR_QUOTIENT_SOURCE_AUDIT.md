# R02 v2 causal quotient — primary-source, implementation, novelty, and measurement audit

Audit date: 2026-10-10  
Scope: `repairs/R02_CAUSAL_DR_QUOTIENT.v2.md`; bounded collision/feasibility audit, not empirical validation or exhaustive priority certification.

## 1. Sequential DR and full-history conditioning

**Jiang & Li, “Doubly Robust Off-policy Value Evaluation for Reinforcement Learning,” ICML 2016, PMLR 48.**

- Primary paper: https://proceedings.mlr.press/v48/jiang16.html
- Eq. (8) gives contextual-bandit DR; Eqs. (9)–(10) give the recursive sequential estimator. The paper explicitly forms per-step target/behavior ratios and states the independence requirement for an evaluated policy/outcome model.
- R02 v2 does not alter this estimator. It asks when all state-dependent objects in it descend to a quotient.

## 2. Direct OPE state-abstraction collision

**Hao, Su, Hu, Szabó, Zhao & Shi, “Off-policy Evaluation with Deeply-abstracted States,” arXiv:2406.19531v3 (2025 revision).**

- Full paper: https://arxiv.org/abs/2406.19531
- Definition 1 requires target-policy irrelevance on abstraction fibers. Definition 2 requires reward and abstract-next-state Markov properties. Definition 5 gives reward/transition model irrelevance.
- Definition 6 and Eqs. (6)–(8) require behavior-policy and backward-transition irrelevance, explicitly extending the behavior policy to depend on abstract histories after iterative compression.
- Lemma F.2 and Theorem 4 establish Fisher consistency of value-based, sequential IS, marginalized IS, and doubly robust estimators on the paper's abstract state. Theorem 4 explicitly invokes Assumptions 1–3 (boundedness, coverage and stationarity); the paper's nuisance-function conditions enter its separate finite-sample/MSE analysis and are not silently added to that theorem.
- Appendix B gives the actual proposed interfaces: a forward encoder trained with reward, transition, target-Q and anti-collapse losses; a backward encoder trained with behavior, ratio/inverse and smoothness terms. Appendix C links the author repository `pufffs/state-abstraction`.
- On 2026-10-10, the official linked GitHub repository returned 404 through the GitHub API and public search did not expose readable source bytes. Therefore the formulas and Appendix interfaces were read, but an immutable author-code commit/file/function audit is unavailable. This is recorded as an implementation-source gap, not replaced with third-party code.

This paper is a major direct collision. The Delta right-quotient translation and local width formula are narrower diagnostics, not a new general compressed-OPE mechanism.

## 3. Classical abstraction controls

**Li, Walsh & Littman, “Towards a Unified Theory of State Abstraction for MDPs,” 2006.**

- Primary PDF: https://rbr.cs.umass.edu/aimath06/proceedings/P21.pdf
- The paper organizes state abstractions by which rewards, transitions, policies or values remain invariant. R02 v2's joint quotient obligations are an OPE/Delta specialization of this established abstraction question.

**Allen, Parikh & Konidaris, “Learning Markov State Abstractions for Deep Reinforcement Learning,” 2021.**

- Primary paper: https://cs.brown.edu/people/gdk/pubs/markov_state_abstractions_ws.pdf
- It gives learned Markov-state abstraction conditions using inverse/density-ratio structure. Hao et al. explicitly adapt these conditions for OPE and history-dependent behavior policies.

MDP homomorphism/bisimulation literature likewise requires reward/output agreement and action-conditioned transition agreement on abstraction cells. R02 v2's recursive closure is not a new homomorphism theorem.

## 4. OPE-specific abstraction and ratio controls

**Chaudhari, Deshpande, Castro da Silva & Thomas, “Abstract Reward Processes: Leveraging State Abstraction for Consistent Off-Policy Evaluation,” NeurIPS 2024 / arXiv:2410.02172.**

- Primary paper: https://arxiv.org/abs/2410.02172
- STAR builds abstract reward processes for consistent OPE and is a direct same-problem abstraction baseline.

**Xie, Ma & Wang, “Towards Optimal Off-Policy Evaluation for Reinforcement Learning with Marginalized Importance Sampling,” NeurIPS 2019 / arXiv:1906.03393.**

- Primary paper: https://arxiv.org/abs/1906.03393
- MIS replaces full trajectory ratios with state-marginal ratios under MDP structure and obtains polynomial rather than generic exponential horizon dependence under its assumptions. It is a stronger control than merely advertising a compact sequential history.

**Pavse & Hanna, “Scaling Marginalized Importance Sampling to High-Dimensional State Spaces via State Abstraction,” arXiv:2212.07486 / AAAI 2023.**

- Primary paper: https://arxiv.org/abs/2212.07486
- This work directly combines state abstraction with marginalized importance sampling and is therefore another close control on the proposed compressed-OPE residual. Its presence strengthens the functional-collision verdict.

**Hao et al., 2024/2025**, above, additionally derive backward-model irrelevance specifically so SIS/MIS/DR objects remain identifiable after abstraction. This subsumes the broad residual proposed by R02 v1.

## 5. Existing implementation controls

R02 v1 already pinned and inspected:

- `VowpalWabbit/vowpal_wabbit@00196b35f63bcb8a6d66966e2b4cf67d6a2bd335`, `python/docs/source/tutorials/off_policy_evaluation.md`, for DM/IPS/DR and logged propensities;
- `Continual-Intelligence/SEAL@6d9c9f9ee392c6cc618e771f399d436d190f6ca4`, including `general-knowledge/src/inner/TTT_server.py`, `query/query_server.py`, `EM/build_SFT_dataset.py`, and `continual/continual_self_edits.py`, for post-update downstream feedback and repeated-edit forgetting;
- `xiaowu0162/LongMemEval@9e0b455f4ef0e2ab8f2e582289761153549043fc`, native QA scorer files, for endpoint measurement only.

R15 additionally pinned author implementations for MIPS/OffCEM and Open Bandit Pipeline. Those methods show that low-dimensional action/context structure yields valid borrowing only under explicit irrelevance/local-correctness assumptions. They do not provide a Delta-specific causal quotient for free.

## 6. Internal lineage and distinctness

- R02 v1 supplies randomized Delta actions, AIPW, delayed outcomes, sequential DR, overlap and horizon boundaries.
- R18 supplies exact global fibers, local joint-state Jacobian closure, recursive quotient maps, and side-code costs.
- R01 v3 supplies transported credit covectors and the minimum fixed-right-quotient width for a declared scalar-credit family.
- R02 v2 adds the exact one-step coarsening-bias identity and joins policy-propensity covectors to the recursively transported Delta quotient. This is a useful lineage-specific debugging delta, not an independent method.

## 7. Native measurement feasibility

- Open Bandit Dataset/OBP contains contexts, finite actions, rewards and propensities and can test generic bandit AIPW/abstraction effects. It has no recurrent Delta state or coupled future transition.
- LongMemEval contains knowledge-update endpoint questions but no randomized internal update actions, logged quotient propensities, paired potential outcomes, or quotient-fiber annotations.
- bAbI and LAMBADA are endpoint tasks with the same mechanism gap.

No reviewed native asset jointly exposes full/quotient Delta state, randomized update actions, exact propensities, action-conditioned quotient transitions, and real delayed potential outcomes. A future empirical protocol would therefore require a new intervention layer; none is designed or run here.

## 8. Audit decision

- Mathematical source support: conditional, pending independent final-byte review.
- Functional novelty: **MAJOR_FUNCTIONAL_COLLISION / CONTROL_ONLY**.
- Architecture candidate: not admitted.
- Empirical effect: unknown; no execution.
- Author-code gap: Hao et al.'s linked repository was unavailable at the audit date; formulas and Appendix interfaces were read, immutable source bytes were not.
- Reopen condition: a lawful prefix-checkable Delta causal quotient with a matched-information total state/compute or statistical advantage over full-history/ratio-ledger DR, direct recurrent Q/policy prediction, Hao et al.'s OPE abstraction, STAR/MIS, and R18.

No project/upstream code, model, benchmark, training, inference, scorer, data/model download, GPU, paid service, or Docker was executed.
