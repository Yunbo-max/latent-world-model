# New native measurement audit — provenance, re-read/revert, and causal memory pathways

Status: **new primary evidence, partial measurement progress only; no exhausted lineage reopened and no candidate added.** Read date: 2026-10-12. This audit concerns public papers and released artifact interfaces only. No project or upstream code was executed; no dataset/model was downloaded; no training, inference, scoring, GPU work, or experiment was performed.

## 1. When Old Facts Return (arXiv:2610.07715v1, 2026-10-06)

Primary paper: <https://arxiv.org/abs/2610.07715> and <https://arxiv.org/html/2610.07715v1>. Ancillary files are linked from the arXiv record, including `MANIFEST.json`, `data/scenarios.json`, `policy_contract.py`, `verify.py`, cached results, and a reference source snapshot.

### Formal object

The paper gives an observational non-identifiability construction. The same observed sequence

\[
(k,A,t_1),(k,B,t_2),(k,A,t_3)
\]

can arise from a re-read of stale (A) or a genuine later reversion to (A). A resolver that receives only key, value, and observation order sees the same record in both worlds although the correct current value differs. This is a concrete external instance of R14's observable-equivalence boundary.

### Released measurement object

The reported re-read benchmark selects 130 atomic transitions from 707 SWE-bench Lite/Verified issues. It evaluates a deliberately adversarial `A,B,A` observation pattern whose target remains (B). The reported aggregate results strongly separate an ordinary temporal-memory policy from a no-resurrection guard on this constructed re-read side. The manifest records paths, hashes, and byte counts for the released scenarios, policy contract, verifier, results, and reference source.

### What it establishes

- repeated observation time is not the same thing as authoritative change provenance;
- a “latest observed value wins” rule can resurrect stale facts;
- a no-resurrection rule repairs that one-sided adversary;
- without authoritative change evidence, the same observation history can also be a true revert, so no universal resolver exists.

### What it does not establish

- The released 130 cases are selected atomic transitions and cached extracted statements, not paired real histories containing both a re-read world and a true-revert world with identical observations.
- Genuine revert performance is not measured; the paper supplies the impossibility/policy counterexample instead.
- All counterfactual write/skip/release losses and randomized action propensities are not exposed.
- The aggregate study uses related model families for answer/write and judging and does not report paired significance for every comparison.
- The mechanism is an external temporal memory policy, not a Delta-state intervention or an internal overwrite-fiber label.

Decision: this is a valuable native-ish provenance stress test and a direct negative control, but it only partially closes R14's measurement gap. It does not shrink the observable equivalence class at deployment, does not identify a Delta-specific advantage, and does not justify attempt 4.

## 2. When Errors Become Memories (arXiv:2608.30198v1)

Primary paper: <https://arxiv.org/abs/2608.30198>.

The paper models multi-turn memory as a dynamic structural causal model over questions, answers, and stored memory. It defines controlled counterfactual trajectories and separates memory-entry effects, question-feedback effects, and their interaction using retention, natural-response, controlled-probe, and probability-preference outcomes.

This is closer to a mechanism-identifying evaluation than endpoint QA because it intervenes on pathways. It can inform how a wrong answer becomes a persistent external memory and can test whether an intervention enters through stored memory or later conversational feedback.

It still does not provide logged randomized Delta write/skip propensities, internal update actions, all potential action outcomes, or the joint Delta state needed by R02/R08/R14. Its memory is external and its interventions do not certify that an internal learned updater has identified factual validity. Decision: useful measurement template, not a native action-level Delta asset and not a reopening premise.

## 3. When to Remember, When to Abstain (arXiv:2610.07100v1)

Primary paper: <https://arxiv.org/abs/2610.07100>.

This work uses category-conditioned retention thresholds on synthetic personas. It is relevant to selective writing and abstention, especially because support rates differ by content category. Its lawful write-time inputs are the extractor-produced semantic category and confidence. Source support is an offline Gemini 2.5 Pro judge label used for evaluation and threshold/model selection, not an online validity oracle; repeated judging itself has a reported nonzero flip rate.

The dataset is synthetic and the problem is selective prediction rather than factual revision/reversion. The extra write-time category/confidence changes the available information budget, but it is weaker than a direct validity label. It is therefore a useful stronger-information baseline for R08/R14, not evidence that an updater can infer validity from the original Delta residual alone.

## 4. Delayed Supervision for Test-Time Language Models (arXiv:2609.32312v1)

Primary paper: <https://arxiv.org/abs/2609.32312>.

The paper-defined protocol uses later question-answer supervision on disposable test-time branches and evaluates delayed adaptation in TextWorld and long-context task families. No author implementation was pinned in this audit. The paper protocol shows that delayed outcomes can train an adaptation strategy under a changed information/timing protocol.

It does not expose native per-write randomized propensities or identify the causal value of an internal Delta update against matched direct action prediction. Slow parameters are trained and the deployment update object differs from the present internal-memory repair problem. It therefore remains a delayed-feedback neighbor/control rather than a new Delta candidate.

## 5. Native action and retention protocols

The audit also searched for one public protocol exposing a lawful tuple

\[
(H_t,A_t\in\{\text{write,skip,alternative}\},p_b(A_t\mid H_t),Y_{t+\tau},\text{old-skill retention},\text{later learning}).
\]

No inspected asset provides this tuple end to end.

### WritePolicyBench

Primary paper: <https://arxiv.org/abs/2602.02574>, Sections 4, 6, 9, and 11. Author repository: <https://github.com/edgardcham/WritePolicyBench>; the paper identifies release tag `v1.0` / short SHA `9cfc1f4`, and this audit pins the read repository to full commit `9cfc1f4979a91ee41ccebd320839186c2933ad2f`.

The native interface is unusually relevant: `writepolicybench/policy.py::WritePolicy.select(step, store)` returns memory actions defined in `writepolicybench/memory.py`, including `WRITE`, `MERGE`, `EXPIRE`, and `SKIP`; `writepolicybench/evaluator.py::run_policy_on_episode(...)` evaluates policies on frozen `data/episodes/*.jsonl` streams under a byte budget. Native endpoints include final retained-set F1, utility per KB, and write-only regret.

This makes it the best public action-interface neighbor found in the bounded audit. It remains a deterministic synthetic write-policy benchmark: it does not expose a behavior propensity `p_b(a|H)`, delayed external outcomes, or old model capability. A fixed random seed is not treatment randomization. It therefore improves the action and budget measurement inventory but cannot identify causal write-versus-skip benefit.

### MemoryBench

Primary paper: <https://arxiv.org/abs/2510.17281>, Sections 2.1--2.4, 3.2, and Appendix A.3. The v1 paper points to `LittleDinoC/MemoryBench-dataset`, `LittleDinoC/MemoryBench-code`, and the THUIR Hugging Face dataset. The current consolidated official organization repository is <https://github.com/THUIR/MemoryBench>; this audit pins that read to commit `247ba8c1e327fa297c0d57aaad0e3cbd66bac656` rather than claiming that the v1 paper itself fixed this SHA.

In the consolidated repository, `src/on-policy.py` generates feedback, unconditionally calls `memory_solver.agent.add_conversation_to_memory(...)`, and repeatedly measures held-out performance; `src/off-policy.py` replays recorded conversations and builds memory; `src/train_performance.py` measures degradation on prior training examples. This yields a useful future-task/retention curve for a complete external memory system.

The benchmark-level update action is nevertheless prescribed. Its “off-policy” mode is replay of recorded conversations, not causal off-policy evaluation. Random selection or ordering of training cases randomizes data, not the memory treatment. It supplies neither write/skip/alternative arms nor action propensities and does not maintain an immutable broad old-capability panel.

### WikiBigEdit

Primary paper: <https://arxiv.org/abs/2503.05683>, Sections 3.1--3.2, 4.1, and Appendix C.1. Author repository: <https://github.com/ExplainableML/WikiBigEdit>; this audit pins the read repository to commit `66b428560254c38755ab70068cb0b0179aa442e1`.

The release provides eight time steps from February through July 2024 and 502,382 samples. `EasyEdit_Experiments/run_lifelong_edit.py` applies the current time step's prescribed edits and then runs `past_eval`, with `hydra/experiments/base_config.yaml` carrying the experiment controls; native outcomes include current edit accuracy, retention of historical edits, locality, rephrase, multi-hop, and generalization measures.

This is a strong temporal editing/retention endpoint, but not a randomized update decision protocol. Shuffling or subsampling examples does not create treatment propensities, and the outcome is post-edit QA rather than naturally delayed external utility.

### Search over Self-Edit Strategies

Primary paper: <https://arxiv.org/abs/2601.14532>, Section 3.2. Author repository: <https://github.com/cheongalc/search-self-edit-strategies>; this audit pins the read repository to commit `49431ef761f81ae27fe7aae99e7593f1547e28c1`.

`squad/src/create_self_edits.py` samples multiple self-edit proposals using temperature/top-p, `squad/src/apply_self_edits.py` applies them separately and compares QA, and `squad/src/build_SFT_dataset.py` builds supervised data from top-ranked proposals. The protocol measures best-of-k proposal search and immediate QA gain. There is no designed skip arm; sampling temperature is not the propensity of the realized complex edit, and sequence log-probabilities are not recorded. Delayed outcomes, old capability, and future learning are absent.

### Open Bandit Dataset / Open Bandit Pipeline

Primary paper: <https://arxiv.org/abs/2008.07146>. Official repository: <https://github.com/st-tech/zr-obp>; this audit pins the read repository to commit `8cbd5fa4558b7ad2ba4781546d6604e4cc3e07c4`.

This asset is a positive control for the missing causal-log schema: `obp/dataset/real.py::OpenBanditDataset` emits `action`, `reward`, `pscore`, `context`, and `action_context` under random or Bayesian Thompson-sampling behavior policies. It identifies a one-step recommendation-policy value. Its action is apparel recommendation and its outcome is immediate click; it has no memory state, memory-update action, old-capability outcome, or later-learning endpoint. The causal fields cannot be spliced into unrelated memory benchmarks without invalidating identification.

SEAL, TTT, TemporalWiki, AToKe, MQuAKE-T, WISE/EasyEdit, and ENCORE were rechecked as neighbors. They contain proposal sampling, prescribed edits, or retention endpoints, but not a logged randomized memory-update action with positivity, propensity, and joint delayed outcomes. In particular, a generator's temperature/top-p is not automatically the behavior propensity of the implemented self-edit.

## 6. Measurement conclusion

| Required object | New evidence | Remaining gap |
|---|---|---|
| same observations, opposite semantic validity | explicit re-read versus true-revert impossibility construction | no paired native real-world record with both worlds and all action losses |
| authoritative provenance at write time | constructed offline source-support evaluation labels and a specification-level trusted-change input | no real benchmark of authoritative reverts; label/signal acquisition cost and fair access for direct baselines |
| causal memory pathway | controlled external-memory interventions | no internal Delta state/action intervention or randomized propensity log |
| delayed outcome | delayed QA supervision protocols | no isolation of delay-specific value versus ordinary QA/direct action prediction |
| native write action | WritePolicyBench exposes write/merge/expire/skip and byte-budget utility | deterministic synthetic stream; no propensity, external delay, or old-skill panel |
| temporal retention | MemoryBench and WikiBigEdit expose future-task or past-edit curves | update treatment prescribed; no write/skip causal contrast |
| valid propensity schema | Open Bandit Dataset exposes `pscore` and reward | recommendation domain, immediate click, no memory update or retention |
| native mechanism scorer | partial pathway/provenance diagnostics | no scorer for overwrite fibers, quotient state, syndrome width, or retain/revise causal action value |

The strongest new fact is not a new updater but a sharper measurement boundary: **observation order alone cannot distinguish stale re-reading from a genuine revert; an authoritative change event or another lawful causal signal is necessary.** The re-read asset can falsify naive recency policies, while the causal-pathway paper suggests how to localize error propagation. WritePolicyBench contributes the closest action API; MemoryBench/WikiBigEdit contribute retention curves; Open Bandit contributes a legitimate propensity schema. They arise from different data-generating processes and cannot be concatenated into a valid causal benchmark. None supplies the paired action-level counterfactual record required to reopen R14/R08/R02 or establish a Delta-specific contribution.

Reopen only if a primary asset provides one of the following:

1. paired same-observation re-read/revert histories with authoritative effective-change labels and action outcomes;
2. randomized or otherwise identified retain/revise/write/skip propensities plus delayed outcomes;
3. an internal-state intervention/scorer that distinguishes Delta overwrite/quotient/ledger mechanisms under matched access and cost.
