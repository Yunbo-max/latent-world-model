# R02 randomized-action credit — primary source and implementation audit

Scope: fixed formulas, assumptions, available author artifacts and native measurement relevance for `repairs/R02_RANDOMIZED_ACTION_CREDIT.v1.md`. Source overlap is not a claim that the Delta application has been empirically tested.

## 1. Contextual-bandit doubly robust estimation

**Dudík, Langford & Li, “Doubly Robust Policy Evaluation and Learning,” ICML 2011 / arXiv:1103.4601v2.**

- Full paper: https://arxiv.org/abs/1103.4601
- The estimator combines a reward model with inverse propensity correction. The finite-action R02 pseudo-outcome is the standard single-action AIPW/DR specialization, with loss replacing reward.
- Its validity depends on logged propensities/overlap and the stated sampling assumptions. It does not identify an individual unit's unobserved counterfactual sign.
- R02 therefore cannot claim the estimator or the general randomized-feedback idea as new.

## 2. Sequential doubly robust OPE

**Jiang & Li, “Doubly Robust Off-policy Value Evaluation for Reinforcement Learning,” ICML 2016, PMLR 48.**

- Paper: https://proceedings.mlr.press/v48/jiang16.html
- Algorithm 1 / Eq. (10) recursively corrects a model value by an importance-weighted temporal-difference residual. The paper's contextual-bandit special case is \(\widehat V(s)+\rho\{r-\widehat R(s,a)\}\), and its sequential form multiplies target/behavior action ratios along the trajectory.
- This supports the R02 distinction: one randomized current update followed by the same continuation policy needs only the initial-action correction; changing later policy requires sequential OPE and can incur product-ratio variance.
- The source does not confer a Delta-specific computational or statistical advantage.

## 3. Production implementation control

**Vowpal Wabbit**, repository snapshot `00196b35f63bcb8a6d66966e2b4cf67d6a2bd335` found during the audit.

- Repository: https://github.com/VowpalWabbit/vowpal_wabbit
- `python/docs/source/tutorials/off_policy_evaluation.md` documents direct-method, IPS and DR evaluation/training through `--cb_type`, and explains the partial-information problem and logged action propensities.
- This is an adjacent maintained implementation, not asserted to be the Dudík/Jiang authors' exact reference code and not a Delta implementation. It is a strong generic engineering baseline.

## 4. Missing-outcome / censoring correction

**Bang & Robins, “Doubly Robust Estimation in Missing Data and Causal Inference Models,” Biometrics 61(4), 2005, DOI:10.1111/j.1541-0420.2005.00377.x.**

- DOI: https://doi.org/10.1111/j.1541-0420.2005.00377.x
- This is the primary missing-data/AIPW basis for the R02 delayed-outcome correction. R02 uses the MAR/independent-censoring special case \(R\perp Y\mid H,A\) with \(c_a(H)>0\).
- The artifact separately requires fixed, cross-fitted or pre-action-predictable nuisance estimates; known randomization alone does not make an outcome model fit on the same evaluated response exactly unbiased.

## 5. SEAL nearest mechanism and actual interface

**Zweiger et al., “Self-Adapting Language Models,” arXiv:2506.10943; official repository `Continual-Intelligence/SEAL`, pinned observed commit `6d9c9f9ee392c6cc618e771f399d436d190f6ca4`.**

- Paper: https://arxiv.org/abs/2506.10943
- Repository: https://github.com/Continual-Intelligence/SEAL
- `general-knowledge/src/inner/TTT_server.py` blob `ffa2b8f3e04ce45a3b8737645fd7819c88f0096c`: `accuracy_and_texts` and `main`; the latter constructs `Trainer(...)`, calls `trainer.train()`, evaluates the adapter, and returns `baseline_accuracy`, `adapter_accuracy` and `gains`. The grading path calls GPT-4.
- `general-knowledge/src/query/query_server.py` blob `2ae312297d0852eae0f5f637f535c21412167944`: `send_round_trip` and `evaluate_completion` implement the downstream reward round trip.
- `general-knowledge/src/EM/build_SFT_dataset.py` blob `45e945502df9e3279d4867d6dfcdae7f62b6d220`: `_top_k` and `main` select metric-ranked self-edits for SFT data.
- `general-knowledge/src/continual/continual_self_edits.py` blob `24fc1506c20b9a1f7159e51db6818ccc1bfeb137`: `run_one_sequence` accumulates prior questions, reevaluates them after each update and progressively merges LoRA adapters, producing a lower-triangular accuracy matrix. This is relevant negative evidence for repeated edits and forgetting.
- SEAL supplies downstream post-update feedback for self-edits, but it does not establish the R02 randomized Delta action effect, retrospective source release, or guaranteed recursive improvement. Its model/hardware/service requirements are not compatible with the present no-execution/no-paid-service stage.

## 6. Native endpoint audit

**LongMemEval official repository**, pinned commit `9e0b455f4ef0e2ab8f2e582289761153549043fc`.

- Repository: https://github.com/xiaowu0162/LongMemEval
- The task includes timestamped dialogue history, evidence annotations and knowledge-update questions. It can test final answer behavior after changed information.
- `src/evaluation/evaluate_qa.py` blob `4732f3772b04a2b9069121ade304e6320494abc2`: `get_anscheck_prompt` plus the module main flow read hypothesis/reference data, call the judge and write `autoeval_label`; `model_zoo['gpt-4o']` is fixed to `gpt-4o-2024-08-06`.
- `src/evaluation/print_qa_metrics.py` blob `f1f68505865960188f239d0f8ccd0a10f8d7b906` has a module-level judge assertion and reports task-averaged, overall and abstention accuracy.
- The native path does not expose randomized internal update actions, logged propensities or both potential outcomes. It is an endpoint benchmark, not a native causal-action-credit scorer under current constraints.

bAbI and the project-pinned LAMBADA variant likewise lack update-action randomization and counterfactual outcomes. They cannot by themselves test the R02 identification claim.

## 7. Other nearest controls

- Thomas & Brunskill, “Data-Efficient Off-Policy Policy Evaluation for Reinforcement Learning,” arXiv:1604.00923 / ICML 2016, covers weighted DR/MAGIC-style general variance/MSE controls.
- Sun et al., “Learning to (Learn at Test Time),” ICML 2025, is a strong learned-state-update baseline, not a randomized action-value estimator.
- Nested Learning / HOPE, arXiv:2512.24695, is relevant at the high-level multi-timescale/self-modifying-memory layer. No official author implementation was verified here, so no implementation-level collision is claimed.

## 8. Audit decision and lawful residuals

The repair escapes the parent's passive-observation nonidentifiability only because the randomized action is new external evidence. The causal estimator, sequential extension and main overlap/variance tradeoffs are already established in contextual-bandit/OPE literature and implemented in general-purpose tooling.

Three Delta-specific residual research leads remain unproved:

1. use exact \(\Delta o(q)=\beta(q^\top k)e\) and the complete state Jacobian as a structured outcome model and prove a matched-budget variance/sample bound;
2. design a protection-aware behavior policy that keeps positivity while proving an old-query-damage bound;
3. prove a Delta state summary sufficient for sequential DR history with lower state/compute than the complete recurrent state.

Merely feeding Delta features into AIPW is not a distinct contribution. Disposition: **mathematics conditionally supported; major general-mechanism collision; native mechanism measurement gap; zero candidate admission.**

No project or source code was executed. Repository inspection was read-only.
