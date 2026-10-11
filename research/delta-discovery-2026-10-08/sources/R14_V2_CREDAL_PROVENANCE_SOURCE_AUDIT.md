# R14 v2 credal-provenance source, implementation and novelty audit

Audit date: 2026-10-11. Scope: primary papers, author repositories and pinned project records. No repository code, model, benchmark, training, inference or scorer was executed.

## Decision

The repaired two-slot theorem is correct under its explicit model, but its mechanism is directly covered by robust Bayes/credal decision making and minimax/DRO. Posterior error causing decision regret is also established. The residual contribution is an exact Delta-slot specialization with a closed-form least-favourable posterior, an exact misspecification-regret identity, and a warning that continuous robust shrinkage is not the same as hard abstention. Retain it as a theorem/control; do not claim a novel architecture.

## Primary sources and author interfaces inspected

| Source | Fixed version / formula or interface inspected | Coverage and residual |
|---|---|---|
| Qiu & Luedtke, *Adversarial Meta-Learning of Gamma-Minimax Estimators That Leverage Prior Knowledge* | arXiv:2012.05465v6 (31 Aug 2023), Sec. 2 Eq. (1) and Sec. 3.3 Eq. (2); Electronic Journal of Statistics 17 (2023) | defines the Gamma-minimax decision `argmin_d sup_{pi in Gamma} r(d,pi)` and the saddle/least-favourable-prior condition. This is the most direct generic collision for R14's posterior-set minimax and prevents presenting the least-favourable posterior principle as Delta-specific. |
| Chen, Berrett, Damoulas & Caprio, *Bulk-Calibrated Credal Ambiguity Sets* | arXiv:2601.21324v2 (11 Jun 2026), Sec. 1 Eq. (upper expectation), Sec. 2.1 definition and Theorem 2.1; PMLR 306 (ICML 2026) | explicitly equates credal upper expectation with worst-case expected loss and minimizes it; Theorem 2.1 gives a closed-form mean-plus-sup robust risk. This directly covers the decision principle behind R14 v2, though not its two-slot formula. |
| Chen et al. author code | `MengqiChenMC/credal-ambiguity-sets-code-repo` commit `506c17fc28e87619e4532afeff8389083e578557` (13 May 2026); `credal_dro/lv_dro.py::{lv_objective,sup_fx_over_bulk,truncated_expectation}`, `credal_dro/lv_bulk_set.py::dkw_select_threshold`, `credal_dro/optimise.py`; CLI `credaldro` | implements/calibrates generic credal-DRO objectives for newsvendor, housing and CivilComments. It does not implement a Delta provenance router and is not evidence that R14 works in language memory. |
| Agarwal & Zhang, *Minimax Regret Optimization for Robust ML under Distribution Shift* | PMLR 178 (COLT 2022), Eqs. (1)--(3), Proposition 1 | separates worst-case raw risk from worst-case regret and optimizes regret uniformly over a distribution family. It is a strong collision for any broad “robust decision under posterior shift” claim; R14's contribution is only its exact local quadratic specialization. |
| Perez-Lebel et al., *Decision from Suboptimal Classifiers: Excess Risk Pre- and Post-Calibration* | arXiv:2503.18025v1 / PMLR 258 (AISTATS 2025), Secs. 2.2--3.2, Eqs. (4)--(11), Props. 3.1--3.2 | derives decisions from posterior probabilities and quantifies decision regret from approximate/miscalibrated probabilities. It does not give R14's continuous two-slot Delta action, but removes novelty from the general posterior-error-to-regret premise. |
| Perez-Lebel et al. author code | `aperezlebel/decision_suboptimal_classifiers`, default branch `temp-orphan`, commit `647cf8eb4296eeefd178025c953d7ae473f68598` (10 Mar 2025); `decision/xp/regrets.py::{compute_regret_CL,compute_V_min,compute_regret_GL_LB,compute_regret_GL_UB}` | operationalizes calibration/grouping-regret analysis for batch classifiers, not online Delta slots. Its existence supports the general decision-regret baseline, not R14 efficacy. |
| Zhou & Zhu, *Calibrating Decision Robustness via Inverse Conformal Risk Control* | arXiv:2510.07750v3 (10 Jun 2026), Sec. 2 Eqs. (1)--(3), Assumptions 3.1--3.2, Definition 3.3 Eqs. (5)--(6), Theorem 3.4 Eq. (7) | formalizes robust actions over an uncertainty set and separately certifies miscoverage/regret. Its finite-sample statement depends on exchangeability and bounded loss; therefore R14 may call an interval a coverage certificate only when the certificate's sampling conditions are actually supplied. A Bayesian credible interval or marginal calibration curve is not automatically such a certificate. |
| Zhou & Zhu author code | `wbzhou2001/Inverse-Conformal-Risk-Control` commit `d36ce4d39e9cb24006ba961b939dbefbb2ed8cd6` (31 May 2026); `model/icrc.py::InverseConformalRiskControl.{compute,estimate}`, `model/creme.py::CREME`, `optimization/lp.py::LinearProgramming.{solve,robust_solve,obj}` | implements robust linear decisions, regret/coverage estimates and post-hoc selection. It is a calibration/control interface, not a Delta-slot implementation or evidence of tokenwise conditional coverage. |
| Yamao et al., *Robust Decision-Focused Learning via Worst-Case Regret Minimization* | PMLR 337 (UAI 2026), Secs. 4.1--4.3; author repository commit `d3122144c97b39c7a5165023803fcee1bfc0fcc3`, `src/optmodel/robust_oracle.py::{EllipsoidUncertaintySet.worst_case_cost,RobustRegretDataset}`, `src/optmodel/dro_wasserstein.py::{DROWassersteinLoss.__call__,evaluate_dro_objective_exact}` | uses uncertainty-set worst-case regret and Wasserstein DRO for decision-focused learning. It is a strong neighbouring control but not an exact formula collision: its target is worst-case regret, whereas R14 minimizes worst-case raw local risk over a posterior set. |
| R14 v1 and project controls | `R14_POSTERIOR_PROVENANCE_WRITE.v1.md`; R05/R07/R08/R09 records | v1 supplies the point-posterior action and ambiguity floor; R07/R09 supply protected quadratic geometry; R08 covers information acquisition; R05 covers partial identification. V2 may not recount these components as a new architecture. |

## Formula-level collision

R14 v2 solves

\[
\min_a\sup_{p\in[\ell,u]}\mathbb E_{J\sim p}[L_J(a)],
\]

which is exactly a credal upper-expectation/DRO decision over a binary law set. Its least-favourable posterior and shrinkage are closed-form because the action loss is a separable quadratic. In multiple slots, the generic problem is an epigraph convex QCQP, and the least-favourable posterior can be an interior mixture of active extreme points. Neither the credal set nor minimax optimization is a new Delta mechanism.

## What remains specific and useful

1. Exact two-slot result `p_hat=Proj_[ell,u](1/2)` and the resulting routed Delta displacement.
2. Exact posterior-misspecification regret, including its sensitivity near high-cost certainty boundaries.
3. Separation of continuous minimax shrinkage from a one-touch hard abstention controller.
4. Explicit counterexample showing that an invalid confident interval may be worse than no-write.
5. A precise statement that robust action selection does not solve provenance identification.

These are theorem/diagnostic contributions. They do not justify “first”, “fully novel”, recursive self-improvement, or empirical superiority.

## Source and implementation gaps

- The inspected credal/DRO implementations calibrate generic distributional ambiguity, not conditional tokenwise provenance intervals.
- Marginal calibration or a held-out reliability curve is not automatically a deployment-time certificate for `P(J|F_t)`.
- Any finite-sample use of the word `certificate` must state the construction and its conditions (for example exchangeability and bounded loss in inverse conformal risk control); otherwise the interval is only an asserted ambiguity set.
- No inspected author repository supplies a native Delta-memory slot-identity benchmark or a scorer for all counterfactual writes.
- The project therefore cannot infer empirical benefit from these sources and must retain the measurement gap.

## Final source verdict

`source_supported=true` for the general robust-decision framing and `math_residual_supported=true` for the exact specialization after independent derivation review. `novel_method_supported=false`; `native_measurement_supported=false`; `experiment_status=unknown`; `candidate_delta=0`.

