# R20 v3 spectral-transfer source and novelty audit

Status: **primary-source/full-formula and author-code audit; no novelty pass**. This audit is scoped to the v3 residual: whether a prefix curvature approximation can lawfully certify future constrained quadratic risk or yield a distinct Delta method.

## 1. PROMISE: spectral approximation and stale/infrequent curvature are established baselines

Frangella, Tropp and Udell, *PROMISE: Preconditioned Stochastic Optimization Methods by Incorporating Scalable Curvature Estimates*, JMLR 25 (2024), full paper:

- Proposition 8 and equation (9) give a two-sided spectral approximation between a subsampled regularized GLM Hessian and the full regularized Hessian under explicit batch-size, coherence/effective-dimension and regularization conditions.
- Assumption 2 directly assumes each preconditioner is a \(\zeta\)-spectral approximation.
- The convergence analysis allows preconditioners to be updated infrequently; the paper's guarantee comes from declared statistical/regularity assumptions, not from observing a prefix alone.

Primary paper: https://www.jmlr.org/papers/volume25/23-0601/23-0601.pdf

Author repository pinned at commit `a1cfef7ab940224443a2deb5f75399f7605e29b1`:

- `opts/sketchysgd.py`, blob `548189c37c02b04c37d8f676bf84238e7b6849d7`, function `SketchySGD.step`: updates the preconditioner at a configured frequency, recalibrates the step on a sample, then applies `compute_direction`.
- `preconditioners/nystrom.py`, blob `0f9ee72f64edb7c1bac674f5d56f5200db2e0550`, functions `Nystrom.update_precond` and `compute_direction`: form a randomized rank-limited Nyström approximation and apply a damped inverse through its eigen factors.
- `config/sensitivity_exp_logistic.sh`, blob `7471ce1a0af2fe7d4840a6a850fc75a7af06d348`: the frequency sweep includes `100000`, documented as no update after the first preconditioner construction.

Pinned repository: https://github.com/udellgroup/PROMISE/tree/a1cfef7ab940224443a2deb5f75399f7605e29b1

Collision implication: relative spectral approximation plus stale/infrequently refreshed curvature is known optimization machinery. R20's Delta equality constraint and closed form are a specialization, not enough for a first-method claim.

## 2. Iterative Hessian Sketch: constrained sketch approximation is known

Pilanci and Wainwright, *Iterative Hessian Sketch: Fast and Accurate Solution Approximation for Constrained Least-Squares*, JMLR 17 (2016):

- Proposition 1 bounds a Hessian-sketch solution error by sketch quality quantities.
- Theorem 2 gives geometric approximation of the constrained least-squares solution under repeated good-sketch events.

Primary paper: https://www.jmlr.org/papers/volume17/14-460/14-460.pdf

Collision implication: constrained optimization with sketched curvature and a spectral/embedding premise is established. IHS does not analyze Delta fast weights or the same affine write constraint, but it blocks treating the v3 certificate pattern as intrinsically new.

## 3. Online Newton and predictive/dynamic regret

Hazan, Agarwal and Kale, *Logarithmic Regret Algorithms for Online Convex Optimization*:

- Figure 3 defines Online Newton Step using the accumulated outer-product matrix and metric projection.
- Theorem 2 gives logarithmic regret for exp-concave losses under the paper's bounded-domain assumptions.

Primary paper: https://www.cs.princeton.edu/~ehazan/papers/logregret.pdf

Chang and Shahrampour, *On Online Optimization: Dynamic Regret Analysis of Strongly Convex and Smooth Problems* (AAAI 2021):

- the paper states that unrestricted comparator movement makes sublinear dynamic regret impossible;
- its optimistic online Newton construction uses gradient/Hessian predictions;
- the regret bounds depend on prediction error, and the paper discusses stale gradient/Hessian predictions under its smooth strongly-convex assumptions.

Primary paper: https://ojs.aaai.org/index.php/AAAI/article/download/17151/16958

Collision implication: a regret-based repair is possible only after adding strong loss, variation and prediction assumptions, and then lands in an established online-optimization family. No Delta-specific regret or cost improvement was derived here.

## 4. Additional direct spectral-sketch collisions

The independent source reviewer found further primary collisions:

- Ye, Luo and Zhang, *Approximate Newton Methods and Their Local Convergence*, ICML 2017, section 3 equations (2)--(3) and Theorem 3, uses relative Loewner Hessian approximation to control approximate quadratic/Newton behavior: https://proceedings.mlr.press/v70/ye17a/ye17a.pdf .
- Roosta-Khorasani and Mahoney, *Sub-Sampled Newton Methods I*, equation (10), Lemmas 1--2 and Algorithms 3--4, establishes a restricted spectral approximation on the relevant cone/subspace under sampling assumptions: https://www.stat.berkeley.edu/~mmahoney/pubs/ssn_MathProg.pdf .
- Lacotte, Wang and Pilanci, *Adaptive Newton Sketch*, equations (5)--(7), event (13), Lemma 1, Theorem 1 and Algorithm 2, adapts sketch size using observable optimization progress: https://proceedings.mlr.press/v139/lacotte21a/lacotte21a.pdf . The author code is pinned at `pilancilab/Adaptive-Newton-Sketch@48570ede88fc07e8d91c6344524641b367cf0cce`; `newton_sketch.py` defines `SketchedNewtonLogisticRegression`, while `optim.py::run_sketched_newton` and `ada_m` enlarge the sketch and can fall back to the full Hessian.
- Na, Dereziński and Mahoney, *Hessian Averaging in Stochastic Newton Methods*, equation (4), section 1.2.1 equations (9)--(10) and Algorithm 1, analyzes averaging under a stationary-objective/martingale-noise regime: https://www.stat.berkeley.edu/~mmahoney/pubs/hessian_averaging_MathProg.pdf . Author code is pinned at `senna1128/Hessian-Averaging@e5f92962874e3f1c3b011d18c65de0f82adf9e4a`; the relevant interfaces are `required_func.py::{sto_weight_oracle_Newton,sketch_Newton,sto_weight_Sket_Newton}` and `main_func.py::Sketch_Main`.

These works certify a current or stationary target under explicit sampling/model assumptions. None turns an arbitrary unseen autoregressive suffix into an action-time observable future operator.

## 5. R20-specific residual and negative result

What remains specific and useful is narrow:

1. for the v2 affine Delta action, the shared-constraint competitive factor sharpens from the generic endpoint chain \(M/m\) to the Kantorovich constant \((M+m)^2/(4Mm)\);
2. the sandwich must cover the affine feasible span, not merely feasible differences, because base--tangent cross terms can dominate;
3. a low-rank prefix sketch can miss an arbitrary future direction, giving an exact same-prefix impossibility of a nontrivial deterministic certificate over unrestricted continuations.

The scalar inequality used in the derivation is proved directly in the v3 artifact, so no novelty is attributed to the classical Kantorovich inequality itself.

## 6. Author-code and interface relevance

PROMISE exposes precisely the operations relevant to the nearest collision: sampled curvature construction, a low-rank/damped inverse action, and configurable refresh frequency. It does not implement the R20 Delta equality constraint. Conversely, R20 v2/v3 does not provide PROMISE's statistical premises or a convergence theorem. The two mechanisms therefore overlap at curvature representation and inverse action but differ in constraint and application; the remaining difference is insufficient for scientific admission without a prefix-to-future law or matched-cost advantage.

## 7. Measurement feasibility and disposition

Public language and continual-learning benchmarks can measure downstream outcomes after the fact, but none of the already audited native interfaces labels the future operator \(H\), the smallest valid \(\delta\), or the same-state counterfactual constrained optimum. Derived instrumentation could estimate these quantities during a future authorized experiment, but it would not make them legal action-time inputs.

**Novelty verdict:** no method-level novelty pass. The sharp affine certificate and impossibility boundary are retained as a conditional theoretical contribution/control. R20 v3 remains parked with candidate increment zero and empirical effect unknown.
