# R09 source, implementation, originality, and native-measurement audit

Artifacts: `repairs/R09_FINITE_BUDGET_OVERWRITE_PROTECTION.v1.md` and its parent controls.  
Audit scope: primary formulas and fixed author interfaces; no imported/executed code, model/data download, training, inference, scoring, or benchmark run.

## 1. Direct mechanism collisions

### Original and Parallel DeltaNet

- Schlag et al., *Linear Transformers Are Secretly Fast Weight Programmers*, arXiv:2102.11174v3, §4 Eqs. 23–25: residual Delta write `S^+=S+beta k(v-S^Tk)^T`.
- Yang et al., *Parallelizing Linear Transformers with the Delta Rule over Sequence Length*, arXiv:2406.06484v6, §§2–3: generalized Householder products and WY/chunkwise realization.
- Fixed author-library interface already pinned in the packet: `fla-org/flash-linear-attention@07ca1e49ef6ca76a7f0dbc8d5ad040ab59434c38`, `fla/ops/delta_rule/naive.py::{delta_rule_recurrence,chunkwise}`.

R09's `x_Delta` is this recurrence at matched correction. The minimum-energy endpoint is a baseline, not a proposed method.

### Preconditioned DeltaNet (PDN)

- Tumma, Loo and Rus, *Preconditioned DeltaNet: Curvature-aware Sequence Modeling for Linear Recurrences*, arXiv:2604.21100v1 (22 April 2026), §§2.3–3.5, Theorem 3.1, Apps. C.1–C.3/E.3/F.1.3.
- Full theory uses `P=(lambda I+sum kk^T)^{-1}` and a normalized preconditioned write key, recovering historical ridge under its exact assumptions. This is the same normalized inverse-metric direction as R09.
- The practical stable model is different: it keeps a diagonal accumulator, applies a bounded log-space squash, and omits the exact Sherman–Morrison normalization.
- Fixed author commit `ntumm120/preconditioned-deltanet@7bd753279af87b39114149a104c5bde9bf67145f`; `3rdparty/flash-linear-attention/fla/ops/precond_gated_delta_rule/naive.py::naive_recurrent_precond_gated_delta_rule` and `fused_recurrent.py`. The recurrent backward in the latter explicitly raises `NotImplementedError`; a separate chunk path exists. No code was run.

Conclusion: exact R09 optimizer has a major functional collision with PDN/RLS theory. The diagonal/full distinction bounds implementation claims but does not establish originality.

### Gated KalmaNet (GKA)

- Peng et al., *Gated KalmaNet: A Fading Memory Layer Through Test-Time Ridge Regression*, arXiv:2511.21016v3 (17 May 2026), §4.1 Algorithm 1, §4.2, Apps. B/C/J.
- It maintains `H/U` statistics and applies a finite Chebyshev solve to `(H+lambda I)` at query time. A finite iteration is approximate; it is not a per-token exact Kalman inverse.
- Fixed author commit `awslabs/hybrid-model-factory@774c1048afd826e35b9222a7116ffd0fc50bcad6`; `.../gated_kalmanet/ops/chebyshev/gka_chebyshev_solve.py::{latent_chebyshev,gka_chebyshev_gla,torch_decoding_one_step}` and `chebyshev_iteration.py::ChebyshevIteration`.

Conclusion: covariance/ridge state and iterative inverse application are strong direct baselines. R09 does not supply a cheaper solver.

## 2. Hard/soft protection and sequential editing

### OWM and continual-learning projections

- Zeng et al., *Continual Learning of Context-dependent Processing in Neural Networks*, arXiv:1810.01256v3, Methods Eqs. 1–2: `P=I-A(A^TA+alpha I)^{-1}A^T` plus recursive covariance-inverse updates. For positive ridge this is a soft operator, not an exact idempotent nullspace projector.
- Fixed interface `beijixiong3510/OWM@a5c59d7b569e3228374ce57a696647646fde6ea2`, `OWM_CNN/owm.py::Appr.train_epoch`, nested `pro_weight`.
- GEM/A-GEM/OGD/EWC already cover constrained/proximal protection of previous tasks or output-Jacobian directions. Their parameter-level task/replay state is not a per-token Delta implementation, but the projection, half-space and quadratic-penalty primitives are direct functional neighbors.
- Fixed interfaces: `facebookresearch/GradientEpisodicMemory@34c6b8e9a0607db7567301c48b727430d20bee7e`, `model/gem.py::{store_grad,overwrite_grad,project2cone2,Net.observe}` and `model/ewc.py::Net.observe`; `facebookresearch/agem@45421499483b28935491251e9e821c55e8b3c089`, `model/model.py::create_stochastic_gem_ops`; `MehdiAbbanaBennani/continual-learning-ogdplus@b633f2c5949f6ea165e2e76aab3d043065d770a8`, `ogd/tools.py::{orthonormalize,project_vec}`. Static interface inspection only.

### AlphaEdit and O-Edit

- Fang et al., *AlphaEdit: Null-Space Constrained Knowledge Editing for Language Models*, arXiv:2410.02355v4, §3.1 Eq. 7, §3.2 Eqs. 8–10, §3.3 Eqs. 11–15. It projects perturbations into an approximate nullspace of preserved-key covariance and adds previous-edit covariance in a normal equation.
- Fixed author commit `jianghoucheng/AlphaEdit@b84624f44dfe8fc6cd9e41df916c44124a0c46dc`; `experiments/evaluate.py::get_project` (blob `2b154d9a2b6d3568d6b246b044b59ca270c09e9c`) uses covariance, SVD and `S < nullspace_threshold` to construct `P`. `AlphaEdit/AlphaEdit_main.py::apply_AlphaEdit_to_model` receives that `P`, computes the supplied-target residual and projected linear solve, then updates the cached key covariance. The tree also contains native CounterFact/ZSRE/MQuAKE evaluation utilities. Static inspection only.
- Cai and Cao, *O-Edit: Orthogonal Subspace Editing for Language Model Sequential Editing*, arXiv:2410.11469, §§2–4, Eqs. 24/26 and Algorithms 1–2: accumulated edit and implicit-knowledge directions are orthogonalized. No confirmed author repository was established in this bounded audit; no third-party interface is promoted to author code.

### AlphaEdit+ — direct hard-to-soft conflict repair

- Liu et al., *AlphaEdit+: Model Editing in the Presence of Conflicting and Inconsistent Knowledge*, Findings of ACL 2026, Anthology ID `2026.findings-acl.728`, DOI `10.18653/v1/2026.findings-acl.728`, Eqs. 1–2 and 7. It directly starts from preserved/prior-edit interference plus Tikhonov least squares, then relaxes the hard nullspace with an optimized projector perturbation and conflict-weighted previous-edit constraints.
- Fixed author repository `zjh-vinky/AlphaEdit_plus@b4fe675ad638fe9fef5046ea3300536d09bd6ddf`; `AlphaEdit_plus/AlphaEditPlus_main.py::{apply_AlphaEditPlus_to_model,solve_delta_closed_form,objective_value,build_lambda_p}` implements the supplied-target closed-form solve, projector search/objective and previous-key weighting; `experiments/evaluate.py` constructs the base projector and dispatches evaluation. Static interface inspection only.

Conclusion: R09's move from a hard infeasibility statement to a soft conflict/energy tradeoff has a particularly direct current collision. The exact Delta frontier/equality certificate remains a bounded theoretical specialization, not a distinct algorithm.

Conclusion: the hard-nullspace endpoint, soft relaxation, sequential protected covariance and orthogonalized edit directions are covered. These methods receive prescribed edit targets and do not identify whether an old fact remains valid.

### Rank-Greville / QR-RLS

Staub and Steinmann, arXiv:2106.11594v1, §2.1–2.2, Theorems 4–5 and Eqs. 36/39, cover rank-deficient recursive least squares and dependent-observation compromise. The parent `RANK_REVEALING_CONSTRAINT_DELTA` already derived `||Delta S||=||e||/rho`. R09's zero-damage energy `||e||^2/rho^2` is that boundary squared, not a new mechanism.

## 3. Claim-by-claim status

| R09 claim | Mathematical/source status | Contribution status |
|---|---|---|
| general-matrix optimum becomes rank-one residual edit | direct Lagrange representer result | useful derivation; classical constrained quadratic optimization |
| `x_mu` inverse-metric frontier | exact for declared static `G` and correction | D03/PDN/RLS/soft projection collision |
| ordinary-Delta scalarized ratio `R_mu>=1` | Cauchy–Schwarz/Kantorovich-type corollary; equality condition explicit | bounded diagnostic residual, not a new updater |
| hard-budget feasibility and nullspace endpoint | exact under declared norm/displacement objective | hard projection/QR-RLS/AlphaEdit collision |
| soft correction closed form | ridge/proximal normal equation | fully known baseline |
| semantic protection or dynamic forgetting reduction | not implied by the theorem | requires validity evidence and full future path; open |

## 4. Native measurement boundary

- LongMemEval at author commit `9e0b455f4ef0e2ab8f2e582289761153549043fc` has knowledge-update endpoint QA but no per-write protected-query covariance, correction budget, propensity, or paired action outcome.
- CounterFact/ZSRE through the pinned AlphaEdit implementation can measure prescribed-target efficacy/locality, but concern parameter editing rather than Delta fast-state adaptation and do not natively expose R09's internal frontier.
- AToKe at author commit `a1b42e34e4130507220307ced3d681fb8719831f` provides temporal old/new questions but no `G`, write budget, action propensity or paired write/no-write outcome.
- bAbI and `lambada_openai` retain their existing native scorer definitions; they can measure endpoint recall/completion but cannot identify the internal geometric claim.
- SEAL's continuous self-edit setting is parameter SFT/LoRA with a different information/compute object.

The formulas can be verified without a new benchmark. Any claim that the certificate predicts or reduces natural-language forgetting still has a measurement gap. No result is fabricated from endpoint accuracy.

## 5. Audit disposition

- Mathematical correctness: suitable for independent exact-byte review after integration.
- Originality/contribution: **major mechanism collision**; retain only the Delta-specialized Pareto/equality/infeasibility theorem.
- Implementation: full-metric state/solve is not supplied; PDN's diagonal implementation is not the exact theorem; no code was executed.
- Experimental effect: unknown.
- Candidate accounting: no D-number, no active/admitted/selected increment.

Reopen only for a same-budget dynamic estimator/lower bound or a native causal protected-action object that survives the listed baselines.
