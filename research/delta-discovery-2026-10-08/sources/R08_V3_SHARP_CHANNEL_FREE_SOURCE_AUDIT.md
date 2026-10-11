# R08 v3 source, novelty and native-measurement audit — sharp channel-free release

Status: **source-supported conditional theorem/control; final-byte independent review pending**.  
Bound artifact: `repairs/R08_SHARP_CHANNEL_FREE_RELEASE.v3.md`, SHA256 `d7ec2b67693e42f2c0d8daffd9754a42f22926768369fefbc9d52dfc7dee673b`.  
Read cutoff: 2026-10-11. No code, benchmark, model, data or scorer was executed.

## 1. Reused verified source lineage

R08 v3 retains rather than replaces the exact source work in:

- `sources/REPAIR_R08_TEMPORAL_VALIDITY_SOURCE_AUDIT.md` (v1): BOCPD, belief-state POMDP/change detection, temporal misalignment, AToKe, StableEdit and RLEdit, including pinned author repositories/interfaces;
- `sources/R08_V2_ACTION_DEPENDENT_INFORMATION_SOURCE_AUDIT.md` (v2): Blackwell comparison, controlled-sensing POMDPs, costly/limited observation, EVSI and the native action-record gap;
- `sources/R05_V4_PREFIX_CONDITIONAL_SOURCE_AUDIT.md`: conditional partial identification, ambiguity-robust individualized policy and baseline-safe decision rules;
- `sources/R02_V2_CAUSAL_DR_QUOTIENT_SOURCE_AUDIT.md` and `sources/R15_INTERVENTION_RANK_SOURCE_AUDIT.md`: finite-action propensity correction, sequential OPE and the cost of changed future policies.

Those parent audits and reviews remain byte-preserved. This audit adds only the channel-free extremal bound and its exact collision status.

## 2. Formula-level attribution

### Expected value of sample/perfect information

Heath, Manolopoulou and Baio, *Efficient Monte Carlo Estimation of the Expected Value of Sample Information Using Moment Matching*, *Medical Decision Making* 38(2), 2018, DOI [`10.1177/0272989X17738515`](https://doi.org/10.1177/0272989X17738515), preprint [`arXiv:1611.01373v3`](https://arxiv.org/abs/1611.01373), §1 equation (1) and §2.4, defines EVSI as the expected optimized posterior net benefit minus optimized current net benefit and gives the two-treatment posterior incremental-net-benefit form. R08 v2 already established this direct mechanism collision.

Jackson et al., *Value of Information: Sensitivity Analysis and Research Design in Bayesian Evidence Synthesis*, *Journal of the American Statistical Association* 114(528), 2019, open author manuscript at [`PMC7034331`](https://pmc.ncbi.nlm.nih.gov/articles/PMC7034331/), §2 distinguishes EVPI (loss reduction if the uncertain quantity were learned perfectly) from EVSI (loss reduction from a specified additional dataset). This supports the label “perfect-information ceiling”; it does not supply the R08 affine absolute-margin simplification.

Rothery et al., *Value of Information Analytical Methods: Report 2 of the ISPOR Value of Information Analysis Emerging Good Practices Task Force*, *Value in Health* 23(3), 2020, DOI [`10.1016/j.jval.2020.01.004`](https://doi.org/10.1016/j.jval.2020.01.004), equations (3), (4) and (10), separately defines perfect-information utility, EVPI and EVSI and states the EVPI upper-bound relation. This is the direct established name for the v3 ceiling.

Kamenica and Gentzkow, *Bayesian Persuasion*, *American Economic Review* 101(6), 2011, DOI [`10.1257/aer.101.6.2590`](https://doi.org/10.1257/aer.101.6.2590), p. 2595 and Proposition 1, characterizes Bayes-plausible finite-support posterior distributions by the mean-prior condition and shows implementation by a signal. This directly supports finite-support laws; the math artifact's displayed measure kernels extend the construction to arbitrary posterior laws when general signal spaces are allowed. With a fixed alphabet, shared sensor, likelihood family or information budget, Bayes plausibility need not be the only constraint and the perfect-information value can be only an outer bound.

The v3 identity

`0 <= I_a <= [(1-p)|delta_a(0)|+p|delta_a(1)|-|delta_a(p)|]/2`

is proved directly by the endpoint chord inequality for the convex function `|u_a+w_a x|`. Perfect revelation attains the upper endpoint and an uninformative experiment attains the lower endpoint. This is the binary EVPI ceiling over the v2 EVSI object, not a new general value-of-information theorem.

### Blackwell and controlled sensing

Blackwell, *Equivalent Comparisons of Experiments*, *Annals of Mathematical Statistics* 24(2), 1953, DOI [`10.1214/aoms/1177729032`](https://doi.org/10.1214/aoms/1177729032), supplies the classic decision-problem ordering/garbling framework. Krishnamurthy, *POMDP Structural Results for Controlled Sensing*, [`arXiv:1701.00179v1`](https://arxiv.org/abs/1701.00179v1), §II equations (2)--(3), §II-A equation (6), and Theorem III.1 give the action-dependent Bayesian filter, Bellman object and value-function concavity. These are decisive prior mechanisms: uninformative and perfectly revealing experiments are extremal controls only after the prior, memory, state transition, costs and terminal decision problem are fixed.

Veeravalli, Fellouris and Moustakides, *Quickest Change Detection with Controlled Sensing*, [`arXiv:2310.17223v1`](https://arxiv.org/abs/2310.17223v1), §II Assumption 1 and equations (1)--(4), explicitly makes observation laws action-dependent. Bayraktar and Kravitz, *Quickest Detection with Discretely Controlled Observations*, [`arXiv:1212.4717v3`](https://arxiv.org/abs/1212.4717v3), §2 and §5, covers costly/limited observations and posterior-state dynamic control. R08 v3 cannot claim novelty for an unknown action-specific channel or a keep/query/release decision.

## 3. Partial identification and policy collision

Manski, *Nonparametric Bounds on Treatment Effects*, *American Economic Review* 80(2):319--323, 1990, develops worst-case bounds when counterfactual outcomes are not point identified. The exact R08 objects differ, but the move from a missing counterfactual channel to a sharp identified set rather than a point estimate is standard partial-identification logic.

The closest modern project-audited sources are more direct:

- Ben-Michael, *Partial identification via conditional linear programs: estimation and policy learning*, [`arXiv:2506.12215v2`](https://arxiv.org/html/2506.12215v2), §2.1 equations (1)--(2), §2.2, §3 and §4: conditional identified sets, policy learning, nuisance estimation and cross-fitting;
- D'Adamo, *Orthogonal Policy Learning Under Ambiguity*, [`arXiv:2111.10904v3`](https://arxiv.org/pdf/2111.10904), §§1--5: conditional partially identified effects, minimax criteria and individualized policy learning;
- Christensen, Moon and Schorfheide, *Optimal Decision Rules when Payoffs are Partially Identified*, [`arXiv:2204.11748`](https://arxiv.org/abs/2204.11748): minimax risk/regret over payoff identified sets;
- Kallus and Zhou, *Confounding-Robust Policy Improvement*, NeurIPS 2018, [paper PDF](https://proceedings.neurips.cc/paper/2018/file/3a09a524440d44d7f19870070a5ad42f-Paper.pdf), §3: baseline-relative robust policy improvement under uncertainty.

R05 v4 already maps these mechanisms to prefix-conditioned Delta gates. R08 v3 differs mathematically—its unknown is an EVSI Jensen gap over Bayes-plausible posterior laws, not `E[rZ]` over unknown validity/sensitivity coupling—but it is not method-level distinctness. It is another low-dimensional closed form inside the same mature partial-identification/robust-decision family.

Khan, Saveski and Ugander, *Off-policy Evaluation Beyond Overlap: Sharp Partial Identification Under Smoothness*, ICML/PMLR 2024, [`arXiv:2305.11812v2`](https://arxiv.org/abs/2305.11812), is the strongest direct no-overlap computational control. It derives sharp OPE bounds outside support under nonparametric smoothness and contrasts them with wider bounded-outcome/Manski bounds. The official repository was inspected at `skhan1998/lipschitz-ope@55c2bee4dc56b83b61bc946a529ff4692f21bf6f`: `ope_estimators.py::EstimatorBase` records `no_overlap=(pi_b==0)`; `compute_psi1_hat` handles overlap; `compute_psi2_bounds` bounds the unsupported part; and `ManskiEstimator`, `LipImputeEstimator`, `LipImputeBddRespEstimator`, and `MultiActionOPEEstimator` expose the corresponding controls. It does not implement Delta margins, but it directly blocks novelty for “sharp action-value bounds without overlap.”

## 4. Causal support and sequential-policy controls

Jiang and Li, *Doubly Robust Off-policy Value Evaluation for Reinforcement Learning*, ICML 2016, [PMLR 48 paper](https://proceedings.mlr.press/v48/jiang16.html), equations (4)--(10) and Theorem 1, extends doubly robust evaluation to sequential decisions with cumulative importance ratios. The project audits record that the author-linked implementation was not recoverable as immutable readable bytes; no third-party implementation is substituted.

Dudik, Langford and Li, *Doubly Robust Policy Evaluation and Learning*, ICML 2011, [`arXiv:1103.4601`](https://arxiv.org/abs/1103.4601), is the finite-action propensity/AIPW control. These results do not identify an action with zero support or an unobserved outcome object. They support R08 v3's requirement that a point claim needs consistency, action support/positivity, legitimate action-timed labels and adequate state adjustment; otherwise a sensitivity/identified set is required. Multistep policy changes require the sequential rather than one-step object.

Petersen et al., *Diagnosing and responding to violations in the positivity assumption*, *Statistical Methods in Medical Research* 21(1), 2012, DOI [`10.1177/0962280210386207`](https://doi.org/10.1177/0962280210386207), §2.3--2.3.1, explains that a never-observed action in a covariate stratum leaves the corresponding conditional outcome undefined and blocks nonparametric g-computation identification absent extra assumptions. This is the exact support boundary in R08's two-world example.

The two-world proof in the math artifact is internal and explicit: the behavior policy always keeps, both worlds induce the same complete observed keep-record law, but the unsupported release channel is respectively uninformative or perfectly revealing. It is an identification counterexample, not an empirical finding.

## 5. Delta, quotient and implementation boundaries

The R08 v3 calculation uses the Delta signed branch loss coefficients inherited from R07 and the v2 two-stage timing. It does not change DeltaNet/Gated DeltaNet/KDA/RWKV updates, construct a learned channel, or reduce the multistep state.

R18's prefix-causal recursive quotient is the direct control for claims about a smaller exact multistep sufficient state. Its source audit finds functional collisions with switched-system observability, common invariant subspaces, bisimulation/predictive equivalence and recurrent behavioral memory. R08 v3 therefore does not recount “belief plus a recursively closed margin module” as a new result.

No author implementation is expected for the elementary convex-chord proof. Existing pinned temporal-editing implementations remain as in v1/v2:

- AToKe author repository `Arvid-pku/ATOKE@a1b42e34e4130507220307ced3d681fb8719831f`, containing README and JSON assets but no audited executable native scorer;
- StableEdit `MINE-USTC/StableEdit@be5769232cf5ba160d8f011dfb9a6d0b5a2a6470`, including `editor/stableedit.py::{STABLEEDIT.__init__,predict_param_shifts,cache,run}` and `editor/base.py` sequential cache/apply flow;
- RLEdit `zhrli324/RLEdit@c6576a1e8e8a122c54d61ec5580ec7397e740a42`, including `editor/rledit.py::{RLEDIT.train,predict_param_shifts,update_hypernet,run}`.

These are strong sequential-edit controls but do not implement the R08 channel-free bound or supply its missing causal record.

## 6. Native measurement audit

The native record needed to distinguish the two worlds contains, before action, the visible prefix/belief and signed branch table; supported keep/release assignment or declared propensities; the action-specific signal; the correctly timed terminal loss/outcome; query/delay cost; and enough state to justify consistency/exchangeability. If the action changes later policies, it also needs the sequential action/propensity history.

AToKe supplies known old/current facts plus historical/current QA outcomes after prescribed edits. StableEdit and RLEdit supply sequential editor trajectories. bAbI, LAMBADA, RULER, BABILong and LongMemEval supply endpoint answer/token/long-context measurements. The audited native formats do not jointly expose randomized sensing actions, both signal kernels, pre-action Delta branch coefficients, query costs and identifiable keep/release action values. Endpoint success can measure a future implementation's behavior but cannot identify which v3 counterfactual world generated an unsupported action.

This is a measurement gap, not a negative benchmark result. No synthetic examples, labels, scores or outcomes are manufactured.

## 7. Claim ledger and disposition

| Claim | Mathematical status | Nearest-work status | Native status |
|---|---|---|---|
| sharp `[0,U_a]` channel-free information set | exact under binary affine terminal loss, fixed prior/state and all Bayes-plausible channels | binary EVPI/EVSI + convex order/Blackwell specialization | no native action-channel record |
| sharp action interval `[H-U_R,H+U_K]` | exact under independent rectangular actionwise channel ambiguity | partial-ID/robust decision specialization; R05 direct project neighbor | endpoint tasks do not identify it |
| same-record opposite-action worlds | exact unsupported-action counterexample | standard causal support/partial-ID boundary | not an experiment |
| `O(1)` analytical screen | true after prefix belief and branch coefficients are supplied | coefficient/JVP/evidence cost remains; direct robust Q is stronger control | unmeasured total cost |

Decision: mathematical contribution is a useful Delta-specific debugging closure, but method-level mechanisms are covered. Originality status is **known EVPI/EVSI, Blackwell, controlled sensing, partial identification and robust-policy collision; narrow signed-margin closed form only**. Candidate delta remains zero; empirical status unknown. After final-byte reviews R08 should exhaust attempt 3/3 and park. Reopening requires a native randomized action-level record or a non-rectangular Delta channel restriction that yields a provably tighter lawful bound and matched-total-cost advantage over direct robust action-value prediction.
