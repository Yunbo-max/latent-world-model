# R15 intervention-rank — primary-source, author-interface, novelty, and measurement audit

- Math artifact: `repairs/R15_INTERVENTION_RANK_BOUND.v1.md`
- Artifact SHA256: `23dd9536139c1beb4858a0407c4e21c1f32e6750e6d85521bec9eeba1c6a9c53`
- Scope: bounded collision/feasibility audit, not exhaustive priority certification or empirical validation.
- Execution: no project/upstream code, model, benchmark, training, inference, scorer, data/model download, GPU, Docker, or paid service.

## 1. Response-surface and design collision

R15 lifts an exact quadratic action response into ordinary linear features `phi(z)=(1,z,svec(zz^T))`. Full-rank information/Gram iff full coefficient identification, a nullspace pair of observationally identical coefficients, condition-number variance, and D/G-optimal design are standard response-surface/optimal-design objects rather than a Delta invention.

- Box & Wilson, *On the Experimental Attainment of Optimum Conditions*, JRSS B 1951, DOI `10.1111/j.2517-6161.1951.tb00067.x`, is the primary response-surface origin.
- Pukelsheim, *Optimal Design of Experiments*, SIAM, Chapter 3, relates information-matrix rank to parameter estimability/identifiability.
- Allen-Zhu et al., *Near-Optimal Design of Experiments via Regret Minimization*, ICML 2017, §1 Eqs. (1)–(2), Theorem 1.1 and §2 Eq. (6), is a modern primary control for finite linear-feature design and prediction-variance criteria.

The R15 theorem is still useful as a precise Delta action-budget boundary, but its mathematical mechanism is standard lifted linear regression. If only the probed arms matter, direct arm means require no quadratic extrapolation. If the exact quadratic model is accepted, ordinary OLS/WLS on the same features plus D/G-optimal design is the direct same-information baseline.

## 2. Causal/OPE collision and low-dimensional action warnings

- Dudík, Langford & Li, *Doubly Robust Policy Evaluation and Learning*, ICML 2011 / arXiv:1103.4601, covers finite-action propensity correction and DR/AIPW.
- Jiang & Li, *Doubly Robust Off-policy Value Evaluation for Reinforcement Learning*, ICML 2016, Eqs. (4)–(10) and Theorem 1, covers sequential DR and cumulative importance ratios. It supports R15's separation between one randomized initial action under one common continuation and evaluation of a changed later policy; horizon-product variance remains.
- Saito & Joachims, *Off-Policy Evaluation for Large Action Spaces via Embeddings*, ICML 2022, Assumptions 3.1–3.2, Propositions 3.3–3.4 and Theorems 3.5–3.7, and OffCEM, ICML 2023, Eq. (4), Assumption 3.1, Proposition 3.2 and Theorem 3.3, are strong structured-action controls. They confirm that a low-dimensional action embedding does not by itself create support: borrowing across actions requires additional no-direct-effect/local-correctness structure.

Author implementations were read at fixed identities:

- `usaito/icml2022-mips@08d65ce04d597d2f7660bfb6da93bf77c86f8b1b`, `src/real/ope.py` blob `cdb43eac531e93a3e88f862d1c48f890b347d0e0`, interfaces `MIPS._estimate_w_x_e`, `_estimate_round_rewards`, and `estimate_policy_value`.
- `usaito/icml2023-offcem@100e325f973f9ccb2bb87d8aa23a2e375de6830a`, `src/real/ope.py` blob `ee132575ce92d1dff716ab892cda77e15913ddd6`, interfaces `train_pairwise_model`, `train_reward_model_via_two_stage`, `OffCEM._estimate_round_rewards`, and `estimate_policy_value`.
- `st-tech/zr-obp@8cbd5fa4558b7ad2ba4781546d6604e4cc3e07c4`: `obp/ope/estimators_embed.py` blob `e9b38ee9b981ade6ccee0098b7a46319c4d92d43`, `estimators.py` blob `58ee77bddd35c67c8575d8995b7f5665eeb950a0`, `meta.py` blob `6eff8bf49d52804942b43478a0a5fbf381239f69`, and `dataset/real.py` blob `0edc09f93067443c0c3f1832ca84042d5a1dac82` expose MIPS/replay/IPW/DM/DR/OPE and real logged action/reward/propensity/context fields.

These controls reinforce, rather than repair, the original no-overlap counterexample. R15's exact polynomial closure is an extra assumption, not a consequence of `x+=Bz`.

## 3. Paired-write and Delta implementation collisions

*Self-Generated Feedback Destabilizes Test-Time Training* (arXiv:2610.05076v1) already uses Fixed Generation, Recorded Replay, paired one-update comparisons, gradient-conflict diagnostics, and delayed independent-real-text Settlement. Its author repository was read at `lingjivoo/ttt-ouroboros@f7811f878679864e686c84abcd83dd05efdc0417`:

- `ttt_pt/parallel_probe.py` blob `0ec200cafa25eee087f9ae830026150dbf8872a8`: `score_fast_weight_branches`, `score_block_settlement`, and default finite doses `(0.5,1.0)`;
- `ttt_pt/block_inner.py` blob `6a1c685c0c2057d3905c8b2312b2560e7cd3dee7`: `settle_on_external` verifies the fast-weight version and commits the scored delta;
- `scripts/deferred.py` blob `81687b3b992ddfe86ea2eb0561b529a828726380`: `defer_update`, `defer_seq`, and `settle` maintain pending/accepted state and evaluate later real text;
- `scripts/preq_obs.py` blob `9d020882b65b6002b2028d481f41308e655f5075`: `settle_risk` enumerates a fixed alpha grid from a common base.

This is a strong collision for finite dose menus and independent future-evidence acceptance. It does not identify an untried dose or justify fixing an endogenous post-action descendant. R15's final bytes correctly distinguish recorded/teacher-forced suffix contrasts from lawful common-random-number pairing that holds only exogenous randomness fixed and lets both branches generate branch-consistent endogenous descendants.

The FLA implementation control `fla-org/flash-linear-attention@a7880060012c862d58575ee23f613cafcd728d03`, `fla/layers/delta_net.py` and `fla/ops/delta_rule/__init__.py`, exposes recurrent/chunk Delta updates but no propensity logger or response-surface/OPE interface. Thus `B_S=I_(d_v) tensor k` is only an action parameterization; it supplies no causal evidence.

*How Linear Attention Remembers* (arXiv:2609.33093v1), §2.1–2.3 Eqs. (1)–(5) and Appendix D.1, provides fixed-trajectory write transport and state/write interventions while warning that aggregate state does not uniquely recover sources. It is an attribution diagnostic, not a substitute for free-running action randomization.

## 4. Internal lineage collision

R15 is not the first appearance of its scalar facts inside this packet. `STEP2_PROJECTED_DELAYED_CREDIT.md` already derives the `B^T lambda` projection, action-span summary lower bound, scalar quadratic delayed-outcome model, conditional Gram criterion, baseline plus two nonzero levels, binary endpoint limitation, horizon/free-running counterexamples, OPE support, and Ouroboros collision. `STEP2_RECURSIVE_RANDOM_METRIC_CONTROL.md` separately covers action-space Hessian/GGN pullbacks and fixed-suffix/free-running mismatch. R02 already supplies randomized finite Delta actions, AIPW, sequential DR, delay/horizon conditions, and paired replay.

R15's legitimate delta is organizational and mathematical: it consolidates those facts into a multivariate exact response-surface iff/lower-bound theorem with conditioning and budget accounting. That is a retained control/theory contribution, not an independent updater or newly uncovered mechanism.

## 5. Native measurement feasibility

- Open Bandit Dataset/OBP natively logs finite recommendation actions, rewards, propensities, contexts and action features, so it can validate generic IPS/DR/MIPS estimators. Its actions are not Delta writes and it does not instantiate coupled free-running memory dynamics.
- Ouroboros provides real-text NLL, WebShop outcome paths, and Settlement branch scoring for finite candidate writes. It lacks arbitrary response-surface truth and does not turn recorded-suffix scores into free-running potential outcomes.
- LongMemEval at `xiaowu0162/LongMemEval@9e0b455f4ef0e2ab8f2e582289761153549043fc`, `src/evaluation/evaluate_qa.py` blob `4732f3772b04a2b9069121ade304e6320494abc2` and `print_qa_metrics.py` blob `f1f68505865960188f239d0f8ccd0a10f8d7b906`, measures QA endpoints but not randomized internal actions, propensities, paired branch-consistent outcomes, or polynomial coefficients.
- bAbI, LAMBADA, and RULER are likewise endpoint tasks. They cannot certify R15's mechanism without an added intervention protocol, which would be a new derived measurement rather than a native label.

No native asset reviewed here jointly exposes the prefix, randomized Delta action, lawful branch outcomes, exact response coefficients, and long-run free-running value. The measurement gap is real; no benchmark, metric, label, or result was invented.

## 6. Audit decision

- Mathematical/source consistency: supported for the stated exact conditional model and causal assumptions.
- Functional novelty: `MAJOR_FUNCTIONAL_COLLISION / CONTROL_ONLY`.
- Architecture candidate: not admitted.
- Experimental effect: unknown; no execution.
- Reopen condition: a checkable exact low-order/low-rank law derived from the full coupled/free-running Delta dynamics, or a matched-support/information/budget statistical or computational advantage over arm means, OLS/WLS optimal design, AIPW/sequential DR, direct Q prediction, and Settlement.

This bounded audit does not claim exhaustive literature priority. It is sufficient to prevent candidate duplication and to preserve the intervention-rank boundary as a reviewed control.
