# R08 source, implementation, originality, and native-measurement audit

Artifact: `repairs/R08_TEMPORAL_VALIDITY_RELEASE.v1.md`  
Audit status: primary/full-formula evidence read; implementation and native-object gaps stated explicitly.

## 1. Bayesian online change-point detection

Adams and MacKay, *Bayesian Online Changepoint Detection*, arXiv:0710.3742v1 (19 October 2007), https://arxiv.org/abs/0710.3742.

- Read object: full paper equations (1)–(16) and Algorithm 1, including the hazard/growth/change recursion in equations (4)–(6).
- Relevant content: posterior over run length, hazard-driven growth/change probabilities, recursive message passing, and posterior predictive mixture.
- Cost stated by the paper: at time `t`, the exact recursion costs `O(t)` time and `O(t)` memory, hence `O(T^2)` cumulative time through horizon `T`; tail truncation is a heuristic whose per-step cost is tied to the retained/effective run-length support, not an unconditional constant.
- Collision: R08's hazard/predict/update filter is standard change-point Bayes filtering. The paper does not contain the R07 Delta action margins or prove that a validity posterior equals write utility.
- Author implementation: no official code interface was established from the paper record in this audit; no third-party implementation is treated as author code.

## 2. Bayesian sequential detection as a POMDP

V. Krishnamurthy, *Bayesian Sequential Detection with Phase-Distributed Change Time and Nonlinear Penalty — A POMDP Approach*, arXiv:1011.5298v4 (13 June 2011), https://arxiv.org/abs/1011.5298.

- Read object: belief-state formulation and structural threshold/switching-curve results.
- Relevant content: posterior belief is the information state for the stated POMDP; monotonicity and switching-curve/threshold structure require explicit assumptions.
- Collision/boundary: R08's Bellman correction and belief-state control are POMDP mechanisms. A scalar posterior threshold is not automatic once action affects transition, observations, memory, or switching cost.
- No code claim is made.

## 3. Quickest change detection coupled to control

T. Banerjee, M. Liu, and J. P. How, *Quickest Change Detection Approach to Optimal Control in Markov Decision Processes with Model Changes*, arXiv:1609.06757v2 (1 March 2017), https://arxiv.org/abs/1609.06757.

- Read object: full paper problem formulation and two-threshold strategy.
- Relevant content: detection and reward/control interact; treating them independently can incur long-run loss, motivating a coupled control policy.
- Collision/boundary: the release/query/control interaction is known in change-detection control. R08's Delta-specific residual is only the action-margin bridge and its exact conditional certificate.

For general quickest-change context, also checked V. V. Veeravalli and T. Banerjee, *Quickest Change Detection*, arXiv:1210.5552v1, https://arxiv.org/abs/1210.5552.

## 4. Temporal knowledge editing and AToKe

X. Yin, J. Jiang, L. Yang, and X. Wan, *History Matters: Temporal Knowledge Editing in Large Language Model*, arXiv:2312.05497v3 (14 December 2023), https://arxiv.org/abs/2312.05497; AAAI 2024, DOI 10.1609/aaai.v38i17.29912.

- Read object: paper description of intrinsic errors versus outdated knowledge, temporal edit setting, and historical/current evaluation.
- Author repository fixed at commit `a1b42e34e4130507220307ced3d681fb8719831f`: https://github.com/Arvid-pku/ATOKE/tree/a1b42e34e4130507220307ced3d681fb8719831f.
- Repository interface at that commit: README plus `AToKe-EE.json`, `AToKe-ME.json`, and `AToKe-SE.json`; no model/evaluator implementation file was present.
- Fixed blobs read: README `3821549dfaa06a3b67b3605a27a33e1d209f2d98`; EE `5c96c1476ad9623be05356508d13f6b64f4d3e93`; ME `f4c976c887717b6a91f60996227c64374605158e`; SE `e74b9789b739a872cf902e16956f882f2ec931fa`.
- Data fields read include `requested_rewrite`, `time_true`, `time_new`, `history_evaluation`, `answer`, `new_answer`, and aliases. The README describes historical/current reliability and generality-style scores.
- Paper-defined native metrics are HRS/HES for historical relative/explicit-time questions and CRS/CES/CES-P for current relative/explicit-time/paraphrase questions; multiple editing reports per-edit means plus final `HES*`, while the extend editing split has no historical HRS/HES. The fixed repository has no executable native scorer/editor, so only the published metric definitions and QA fields—not an audited scorer implementation—are available for reuse.
- Native capability: supplied temporal transitions with historical and current questions/answers can measure behavior after a known update.
- Missing object: no uncertain causal evidence stream, declared likelihood/hazard, optional query cost, Delta pre-action `(q,h)`, randomized propensity, paired write/no-write outcome, or Bellman continuation value.

Therefore AToKe is a useful temporal-behavior asset, not a native estimator of R08's causal action advantage.

## 5. Direct temporal-action and sequential-editing neighbors

**Mitigating Temporal Misalignment by Discarding Outdated Facts.** Zhang and Choi, EMNLP 2023, arXiv:2305.14824v3, https://arxiv.org/abs/2305.14824, predicts a fact-duration distribution and uses the probability that duration is below the query/model time gap to trigger retrieval/discarding, including a 0.5 threshold in its adaptive inference. This directly covers temporal-validity posterior to thresholded downstream action. It does not contain a sequential evidence filter, Delta protection geometry, or action-dependent Bellman state, so those remain the narrower residual. The author repository was checked at commit `893a0e76982c46197b51ff27cedf1a7249911065`: https://github.com/mikejqzhang/mitigating_misalignment/tree/893a0e76982c46197b51ff27cedf1a7249911065. Its tree contains only a README saying code is forthcoming; no training/evaluator function or native scorer was available to audit.

**StableEdit.** Ma et al., *More Edits, More Stable: Understanding the Lifelong Normalization in Sequential Model Editing*, arXiv:2605.11836v2 (21 July 2026), https://arxiv.org/abs/2605.11836. The author repository was read at commit `be5769232cf5ba160d8f011dfb9a6d0b5a2a6470`: https://github.com/MINE-USTC/StableEdit/tree/be5769232cf5ba160d8f011dfb9a6d0b5a2a6470. `editor/stableedit.py` blob `921747983117e76ad0bebc30c4848e22bb97ec54` exposes `STABLEEDIT.__init__`, `predict_param_shifts`, `cache`, and `run`; `editor/base.py` blob `b41bc15c2104a3c96941b1e888f37a72406422ba` performs sequential cache/predict/apply evaluation. The repository calls running-statistics/whitening abstractions plus a ridge solve; the paper proves asymptotic orthogonality and bounded norms only under its stated assumptions. It has no temporal-validity likelihood or release/query gate.

**RLEdit.** Li et al., *Reinforced Lifelong Editing for Language Models*, arXiv:2502.05759v4 (7 September 2025), https://arxiv.org/abs/2502.05759, maps sequential editing to an MDP whose supplied edit sample includes its target and learns update direction/magnitude from edit/locality and trajectory-return objectives. The author repository was checked at commit `c6576a1e8e8a122c54d61ec5580ec7397e740a42`: https://github.com/zhrli324/RLEdit/tree/c6576a1e8e8a122c54d61ec5580ec7397e740a42. `editor/rledit.py` exposes `RLEDIT.train`, `predict_param_shifts`, `update_hypernet`, and `run`; it always processes a prescribed edit sequence and has no latent validity posterior or skip/release evidence filter. R08 therefore cannot claim to be the first sequential, controlled, or RL editor.

## 6. Lineage collisions retained

R08 inherits the fixed source work in `sources/REPAIR_R07_VALIDITY_TO_ACTION_SOURCE_AUDIT.md`, including the distinction between known protected/orthogonal edit geometry and a new action-value theorem. It also preserves the old source conclusions in:

- `rejected/REVISION_EVIDENCE_POSTERIOR_EDIT.md` and its review: static posterior decision plus protected/ridge/slot edit geometry is known composition;
- `rejected/MARTINGALE_RELEASE_CONTROL.md` and its review: an e-process can control an evidence event but not the utility sign of release.

The current audit adds a sharper dynamic conclusion: once release changes subsequent evidence or memory, the correct comparator is a belief-and-memory POMDP/change-detection controller, not a static posterior gate.

## 7. Claim-by-claim status

| Claim | Mathematical status | Originality status | Native measurement status |
|---|---|---|---|
| `D_p(a)=h(p)a^2-2q(p)a` | exact under fixed-reference R07 quadratic and posterior mixture | Delta specialization of conditional Bayes risk | `(q,h)` absent from AToKe |
| full-write posterior threshold | exact only for fixed branch costs; direction depends on `A` | standard cost-sensitive Bayes rule | posterior calibration not natively supplied |
| endpoint robust certificate | exact for a sharp joint interval and fixed branches | robust-decision specialization | no joint identified set supplied |
| one-step query VoI | follows from concavity/Jensen for action-independent observations | standard Bayesian value of information | query action/cost absent |
| Bellman `Gamma` correction | exact once `z_t` is sufficient | standard POMDP/control object | continuation/action propensities absent |
| e-process false-release evidence control | valid only under the true action-conditioned filtration | standard sequential inference | action-dependent likelihood absent |

## 8. Audit disposition

- Mathematical correctness: conditional, suitable for independent final-byte review.
- Contribution difference: useful Delta-specific diagnostic/control bridge, but nearest mechanisms cover the filter, threshold, query, and dynamic-control primitives.
- Experimental state: unknown; no execution was performed.
- Candidate accounting: no upgrade; keep as parked theory/control.
