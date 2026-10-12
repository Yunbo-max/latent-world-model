# Source and native-measurement audit: shadow catch-up / crossed-world Delta object

Date: 2026-10-12  
Scope: primary-source, formula/interface, and measurement-neighbor audit. No project/model code or experiment was run.  
Decision: source collisions are material; retain only a scoped lead/control with `candidate_delta=0`.

## 1. Primary papers checked at fixed public versions

The arXiv paper versions below are fixed. SafeCommit and MemTX author repositories were pinned at their observed public heads, but were not inspected at file/function byte level in this pass; CounterMem has no released author code at v1; the CMA supplementary kit was not pinned or executed. Accordingly, this is a bounded paper/formula and repository-availability audit, not author-code interface verification or implementation closure.

### SafeCommit

- Paper: Mayur Akewar and Ravi Ranjan, *SafeCommit: Certifying When Memory-Grounded Agents May Safely Act*, arXiv:2608.04289v1, submitted 2026-08-04. <https://arxiv.org/html/2608.04289v1>
- Public code linked by the paper: <https://github.com/akewarmayur/SafeCommit/tree/146708eba8d6c768544330d20ed98047a3cc73dc> (public head observed 2026-10-12; file/function inspection not completed here).
- Formula/interface locations read: §2.1 evidence/actions/worlds, Eqs. (1)--(4); §2.3 uncertified region and conformal action certificate, Eqs. (5)--(7); §2.4 safety-equivalence signatures, Eq. (8); §3.3 certified action set, Eqs. (10)--(11); §3.4 certificate-shrinking probes, Eqs. (12)--(13), Algorithm 1; §3.5 staged/reversible probes and complexity; §4.1 controlled JSONL protocol.
- Exact overlap: explicit `commit / probe / fallback`, calibrated plausible-world sets, action-specific probe value, staged reversible mutation, and conservative fallback already exist. The paper explicitly treats staged diffs/sandboxed execution as effect-revealing probes.
- Scope boundary: its controlled benchmark has known latent worlds, deterministic probes, and true-world support in the main experiment. It is not an internal Delta write/skip paired-outcome protocol, and its proof-of-concept evaluation explicitly does not claim deployed-agent validation.

### MemTX

- Paper: Xiaoyang Li et al., *MemTX: Transactional Belief Commit for Stateful Agent Memory*, arXiv:2607.23929v2, revised 2026-07-28. <https://arxiv.org/html/2607.23929v2>
- Public repository linked by the paper: <https://github.com/lxy1134/MEMTX_/tree/4e1124ccd5fd384857463020e3497aa73ec93be6> (public revision observed 2026-10-12; file/function inspection not completed here).
- Formula/interface locations read: §1 lifecycle and contribution summary; §3 protocol; paper-linked implementation and conformance-suite descriptions.
- Exact overlap: records carry evidence, permissions, provenance, and validity; writes are staged in snapshot-isolated transactions; validate-and-commit gates irreversible actions; retraction triggers typed cascading repair. This directly covers the generic “shadow/stage then validate” architecture-level story.
- Scope boundary: it is middleware over structured persistent records and tool effects, not a low-rank Delta state propagator. Its purpose-built conformance suite does not identify a Delta internal write effect, future learning efficiency, or a same-cost comparison against a rank-one pending ledger.

### CounterMem

- Paper: Hongji Pu, Ruixiang Tang, Yongfeng Zhang, *CounterMem: World-Model-Verified Counterfactual Memory for Language Agents*, arXiv:2609.31874v1, submitted 2026-09-25. <https://arxiv.org/html/2609.31874v1>
- Code status at the read version: the paper states that code will be released upon acceptance; no author repository is linked on the arXiv page.
- Formula/interface locations read: §3.2 at most \(K=4\) local alternatives, Eq. (1); §3.3 copy/reset evaluation and improvement \(\Delta(a')\), Eq. (2); record tuple and applicability conditions; Appendix B.4 retrieval/selection, Eqs. (7)--(9); algorithm lines for construction, freezing, and DQN selection.
- Exact overlap: local alternatives are evaluated from a copy or reset of the same state using executable tests/proof checkers/solvers; checked improvements and reuse conditions are stored; a learned selector chooses a retrieved record or skip. This is already a reset-based counterfactual-memory construction and later-use policy.
- Important negative evidence: the paper reports that applying verified corrections to unsuitable decisions can reverse gains. It also reports task-run token reductions while excluding offline selector-training cost, so the latter cannot establish matched-total-cost superiority.
- Scope boundary: the action is a task-level local alternative rather than an internal Delta write. Source-state verification identifies local checked improvement, not transport to arbitrary later Delta queries. The paper freezes memory and selector during held-out evaluation; it is not deployment-time recursive updater improvement.

### Counterfactual Memory Audit (CMA)

- Paper: Jiajie Zhang, Yankai Xiang, Changhao Chen, *Memory That Changes Action Is Not Memory That Guides It: Counterfactual Auditing of History-Conditioned Robot Policies*, arXiv:2609.27247v1, submitted 2026-09-23. <https://arxiv.org/abs/2609.27247v1>
- Full-text locations read: introduction and protocol definition; lawful histories reconverging to a verified-identical present; frozen-policy common randomness; crossing each saved action under both worlds; sensitivity, signed faithfulness, matched-world physical value, and per-pair reliability.
- Exact overlap: CMA already supplies the core measurement idea that action change under different memories is insufficient. It crosses histories and saved actions at an identical present to test whether memory causes the warranted decision.
- Native evidence: all audited Put Back pairs changed action, yet only 20/64 were fully reliable; later Swap actions all changed but selected the same branch. These are direct warnings against using action sensitivity as faithfulness.
- Scope boundary: CMA is a robot-policy evaluation protocol, not a Delta write rule. The scalar Delta crossed-loss identity in the companion derivation is a special-case analytical reduction of a crossed audit, not a claim to invent crossed-world evaluation.

### Additional direct primary neighbors (bounded abstract/full-text mechanism checks)

- *Delayed Supervision for Test-Time Language Models*, arXiv:2609.32312v1, studies disposable delayed branches for LaCT, DeltaNet, and RWKV-7 under a delayed-QA objective, while explicitly leaving delay-versus-general-QA attribution open. <https://arxiv.org/abs/2609.32312v1>
- *Forgetting Without Restarting*, arXiv:2609.04875v1, formalizes exact counterfactual suffixes for deterministic transitions using checkpoint/replay and gives the associated recomputation lower bound. <https://arxiv.org/abs/2609.04875v1>
- *What Eviction Destroys*, arXiv:2609.08279v1, uses per-question restoration counterfactuals on LongMemEval-S to measure what removed memory supported. <https://arxiv.org/abs/2609.08279v1>
- *MemAudit*, arXiv:2605.23723v1, performs post-hoc counterfactual memory-influence auditing with an anomaly graph. <https://arxiv.org/abs/2605.23723v1>
- *ChronoMem*, arXiv:2607.27773v2, stores whole-memory snapshots per write and evaluates semantic rollback/post-exposure counterfactuals. <https://arxiv.org/abs/2607.27773v2>

These papers further crowd delayed-branch, replay, restore, influence-audit, and rollback narratives. None of the bounded abstract/full-text mechanism checks above establishes the exact low-rank shared-affine Delta audit as a new updater or supplies the missing same-DGP joint protocol.

## 2. Internal nearest-work collision

| Internal object | Overlap with the new lead | Residual left after comparison |
|---|---|---|
| R08 v2/v3 | Bayes envelope, EVSI, controlled sensing, abstain/commit boundary | a particular lawful paired-loss channel under shared suffix; no new decision principle |
| R11 v3 | exact fixed-coefficient low-rank overlay closure and rank growth | use of the overlay as a causal audit branch; no new algebraic updater |
| R02 | randomized action credit, OPE/DR, causal quotient | paired full-information outcome can avoid propensity only under strong common-exogenous assumptions |
| R15 | counterfactual finite-action value and trial outcomes | reset/twin creates a real outcome; transfer beyond the checked state remains unidentified |
| direct ledger/control | retain factors plus evidence/provenance and decide later | same state order as independently committable shadows; must be matched explicitly |

This file does not reopen any exhausted lineage. It records a new parent measurement object and assigns its inherited components to their existing baselines.

## 3. Native measurement mapping

| Required claim | Native/public object currently available | What it measures | Missing piece |
|---|---|---|---|
| local write-vs-skip effect from same state | CounterMem-style resettable executable evaluator | checked local alternative outcome | not an internal Delta action; reset/evaluator costs; no old-retention/later-learning panel |
| history-conditioned decision faithfulness | CMA crossed histories/actions | sensitivity, faithfulness, matched-world utility, reliability | robot memory; no Delta state/cost interface |
| safe staged release | SafeCommit controlled benchmark | unsafe commit, task success, coverage, fallback, probes | known/synthetic latent worlds; no internal write potential outcomes |
| structured belief lifecycle/repair | MemTX conformance suite | action gating, cascading repair, downstream harm | structured records, not Delta; custom suite; no learning-efficiency endpoint |
| delayed full-information shadow loss | common external teacher-forced suffix | both branch predictions under shared target | paired fixed-suffix/model-based contrast; free-running closed-loop total effect not identified |
| later transfer value | CounterMem reuse selector/outcomes | usefulness of checked records on held-out tasks | action/applicability mechanism differs; offline selector cost and internal Delta retention absent |

No single audited object jointly contains: (i) internal Delta write/skip/partial action, (ii) paired branch or a valid assignment/propensity mechanism, (iii) delayed external outcome, (iv) old-capability retention, (v) later-learning efficiency, (vi) native scorer, and (vii) complete state/FLOP/latency/evaluator cost. Cross-dataset stitching would mix data-generating processes and would not identify the requested causal vector.

### Additional native repositories inspected

| Asset | Pinned revision | Useful native fields/metrics | Why it still does not identify per-update effect |
|---|---|---|---|
| [AgentMemoryBench](https://github.com/solomoon313/AgentMemoryBench) | `9dfda8dede15bf16518524e4614ed89344795413` (code-body commit `3af370d4acb4590736ae0be9decb2d4b43aa2a97`) | runner/scorers expose online CSR/LG/SL, replay FR/ASR, transfer TG/FTG, repair ER/RG/NR | `update_memory(task, history, result)` is procedurally invoked; no randomized write/skip/merge action or logged `pscore`/behavior probability |
| [MemoryArena](https://github.com/ZexueHe/MemoryArena) | `6cd9de14b71915e39ac742a20dc33785e14b6aab`; arXiv:2602.16313v2 | records expose `id`, `questions[]`, `answers[]`, `backgrounds`; native success/process score, `SR@k`, latency | memory store is system-internal; no uniform structured update action, random assignment, or propensity |
| [Evo-Memory](https://github.com/zhaosnw/evo_mem) | `10486d80a2a59903d543dd1e0438505b08ec2275`; arXiv:2511.20857v2 | streaming controls include `seed`, `num_streams`, `save_trajectories`; accuracy/success/progress/step efficiency | seed randomizes stream/order, not the memory action; no per-step action propensity or separate retention panel |
| [UMA / Ledger-QA](https://github.com/ictnlp/unified-memory-agent) | `90f8d900481bf16693d17d9bc7f4dcc76c7afd4b`; arXiv:2602.18493v2 | Add/Update/Delete/Retrieve/List/UpdateCore and future-QA reward; outputs `responses_*.jsonl`, `evaluated_*.jsonl` | public evaluation outputs do not establish a logged full action distribution; policy sampling during RL is not automatically an identifiable evaluation log |
| [WritePolicyBench](https://github.com/edgardcham/WritePolicyBench) | `9cfc1f4979a91ee41ccebd320839186c2933ad2f`; arXiv:2602.02574 | supervised write/merge/expire/skip labels; interface provenance is inherited from `STEP2_NEW_NATIVE_MEASUREMENT_AUDIT_2026-10-12.md` | labels are not randomized interventions and there is no delayed causal outcome panel |
| [Open Bandit Dataset](https://github.com/st-tech/zr-obp) | `8cbd5fa4558b7ad2ba4781546d6604e4cc3e07c4` | `context`, `action_context`, `action`, `reward`, `pscore` in recommendation | valid only for its own one-step recommendation DGP; cannot donate propensity to a memory benchmark |

The minimal lawful future protocol must predeclare the estimand, randomization unit, eligible update event, and outcome horizon. Before each event it records the pre-action history, state/version, policy version, assigned arm and realized action (including skip and any partial-write arm), then logs the assignment probability immediately. Sequential identification requires the stated exchangeability/randomization mechanism, positivity, consistency, an interference scope, censoring/attrition handling, and the product of trajectory propensities rather than only a final action probability. Outcomes must come from the same DGP: future-window loss, a fixed non-mutating old-capability panel, and a defined later-learning-efficiency measure such as loss per sample or time-to-threshold on a fixed new-task stream. State, compute, latency, reset/evaluator, and storage costs must be matched. Randomizing only the whole updater estimates a policy-level total effect, not the marginal effect of a particular write.

## 4. Code/interface availability status

- SafeCommit: public code is linked by the paper and its observed public head was pinned above; only paper-level controller semantics and repository availability were checked here, not a file/function interface.
- MemTX: public repository is linked by the paper and its observed public revision was pinned above; only paper-level lifecycle/transaction semantics and repository availability were checked here, not a file/function interface.
- CounterMem: no public author code at v1; the paper explicitly defers release until acceptance. Formula and pseudocode review is possible, implementation verification is not.
- CMA: the paper reports a supplementary recomputation kit, but this audit used the public full text and did not execute any artifact.

Availability is not evidence of correctness, originality, or suitability. No source code was run in this mathematical stage.

## 5. Novelty and contribution decision

The full combination is strongly crowded:

- `commit / probe / fallback` and action-directed evidence acquisition: SafeCommit and standard controlled sensing;
- stage/validate/commit/retract/provenance: MemTX and transactional memory;
- copy/reset local counterfactual checks plus later selection: CounterMem;
- crossed-history/crossed-action faithfulness audit: CMA;
- rank-one shadow propagation: internal R11 v3 and standard influence/eligibility machinery.

The residual relative to this bounded inspected set is a compact Delta-specific audit theorem: under a shared affine suffix, a rank-one candidate can be propagated without duplicating the full state, and under shared-query squared loss a crossed audit reduces to an explicit alignment term. That result can be useful for debugging and for specifying exactly when a low-rank-factor-state paired model-based contrast exists. It is not, on present evidence, a new updater, an originality result, or a scientifically admitted candidate.

## 6. Reopen conditions

Promotion beyond `lead/control` requires all of the following relevant to the claimed contribution:

1. a lawful native protocol that exposes the exact estimand (fixed-suffix controlled contrast, nested skip-suffix audit, or closed-loop total effect) rather than mixing them;
2. a proof or measurement that the Delta-specific low-rank audit is strictly cheaper at matched precision and actionability than a direct pending ledger/full twin;
3. source review showing the claimed interface is not already covered under a rename by SafeCommit/MemTX/CounterMem/CMA or the delayed-supervision, replay/unlearning, restore-audit, MemAudit, and ChronoMem families;
4. old-retention and later-learning outcomes from the same data-generating process, or an explicit transport theorem;
5. fresh exact-byte math, source, adversarial, and measurement reviews before any candidate promotion.

Until those conditions hold: `candidate_delta=0`, `scientific_admission_delta=0`, `selection_delta=0`, experiment unknown.

