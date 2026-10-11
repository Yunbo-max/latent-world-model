# R17 v2 causal predictive-leakage certificate — source, collision and measurement audit

- Math artifact: `repairs/R17_CAUSAL_PREDICTIVE_LEAKAGE_CERTIFICATE.v2.md`
- Math artifact SHA256: `c7f7843a9508dbb5cc6fdf9525e23dc311eff070f58b572bb133850722eb1438`
- Preserved v1 audit: `sources/R17_PREDICTIVE_QUOTIENT_SOURCE_AUDIT.md`, SHA256 `2b94f1e9c3ec3d8753e045462fbb81cdc57db3f41a38ea249182c5ff73279ba2`.
- Scope: bounded primary-source and nearest-work audit; not exhaustive priority certification or empirical validation.
- Execution: static source reading and mathematics only; no project/upstream execution, model, benchmark, training, inference, scorer, data/model download, GPU, Docker or paid service.

## 1. Preserved R17 v1 controls

The v1 audit remains binding. Predictive fibers/quotients, linear-system observation quotients and bisimulation, task-sufficient/regret quotients, information bottleneck, predictive rate-distortion, conditional rate-distortion and predictive-state representations already cover the broad idea that only future-relevant distinctions need retention. R17 v2 does not claim this principle as new. It changes the legal information interface from a realized suffix to an `F_t`-measurable uncertainty contract.

## 2. Matrix concentration and confidence sequences

Joel Tropp, *User-Friendly Tail Bounds for Sums of Random Matrices*, arXiv:1004.4389 / Foundations of Computational Mathematics 2012, proves matrix Chernoff, Hoeffding, Bernstein and Freedman inequalities for independent or martingale self-adjoint sums. Theorem 6.1 is the matrix-Bernstein family used for the one-sided mean bound in equations (17)--(20). It does **not** say that the next realized Gram is Loewner-bounded by the estimated mean.

Howard, Ramdas, McAuliffe and Sekhon, *Time-uniform, nonparametric, nonasymptotic confidence sequences*, arXiv:1810.08240 / Annals of Statistics 2021, develop confidence sequences via nonnegative supermartingales. Section 4.3, especially Corollary 3 and the subsequent covariance-confidence construction, gives matrix-martingale maximum-eigenvalue and covariance applications. This is the correct family when the certificate is inspected repeatedly or stopped adaptively. A fixed-time matrix-Bernstein radius cannot be silently reused as an anytime guarantee.

Powel and Morgansen, *Empirical Observability Gramian for Stochastic Observability of Nonlinear Systems*, arXiv:2006.07451v1, Section II-B equations (5)--(7), define the empirical observability Gramian from perturbed trajectories; Section III, Theorem 3 and equation (19), connect its derivative to Fisher information; Section IV treats stochastic processes. This is a direct control for learning an observation-energy object from trajectories. It does not provide R17's future semantic-validity label or make an empirical mean Gram a pathwise suffix bound.

These sources substantially cover the statistical machinery. R17's residual is only the exact mapping from the Delta overwrite kernel to the scalar quadratic form that must be certified, plus the explicit warning that mean-Gram confidence is not a pathwise future-Gram certificate.

## 3. Robust unobservability and robust optimization collision

Ian R. Petersen, *Robust Unobservability for Uncertain Linear Systems With Structured Uncertainty*, IEEE Transactions on Automatic Control 52(8), 2007, DOI 10.1109/TAC.2007.902751, asks when a state is unobservable for all admissible uncertainty values and constructs a robust unobservability function and unobservable cone. Only the publisher abstract/metadata was available in this bounded audit, so this is a concept-level closest-work inference, not a claim that Petersen states equations (7)--(9). The common-kernel condition is still a direct finite-horizon linear robust-unobservability specialization, not a new concept.

Support functions over PSD/norm-bounded ambiguity sets are standard robust/DRO operations. Equation (11) is a packet-level exact calculation for the Delta erased direction; its rank-one maximizer is elementary and leaves no architectural novelty. If the ambiguity set is broadened to arbitrary future Grams, the certificate becomes vacuous exactly as robust optimization predicts.

## 4. Dynamic-Gramian and direct-ledger collision

Internal R09 v2 already derives the transported future-query Gramian and the inverse-metric rank-one edit minimizing a quadratic protection cost. If R17 v2 optimizes the write direction under `U_t`, it becomes R09 with an upper metric. The distinct retained point is diagnostic: R17 certifies whether *exact overwrite's fixed erased direction* is safely invisible, and distinguishes expected from pathwise certification.

Internal R12/R18 and classical quotient/functional-observer theory cover recursive closed coordinates. R17 v2 does not claim recursive closure. Its equal-information comparator is a direct basis `B_t` for the union observable span and a ledger `B_t^T S`; absent a matched recurring-cost advantage, a more elaborate memory representation cannot claim benefit from relabeling alone.

## 5. Partial overwrite and intervention branches

For `beta<1`, equation (31) is a Sherman--Morrison specialization and equations (32)--(33) are ordinary quadratic shrinkage. Learned or fixed Delta gates, ridge/RLS/Kalman updates and PDN are mandatory controls. No candidate novelty survives.

Randomized probes could identify whether an erased direction affects later outcomes, but that changes information and consumes interventions. Causal experimental design and internal R02/R15 are the nearest controls. V2 therefore does not hide probes inside an observational certificate.

## 6. Benchmark and author-interface boundary

This audit reuses the fixed asset revisions recorded in `R18_RECURSIVE_JOINT_QUOTIENT_SOURCE_AUDIT.md` Section 5: ParlAI bAbI `a29567f7ce76992fd1f03c51ba9e3b155a37ea51`; lm-eval LAMBADA `d6de81643928d653435c431bae19945d41d32520`; RULER `c3f5e3b4f87f97e048793bb510a3a6b19a46bf3a` plus pipeline `e8bbff677ca2c239640dc90f93310dcf32408c93`; and LongMemEval `9e0b455f4ef0e2ab8f2e582289761153549043fc`. These interfaces provide prompts, targets and endpoint scorers. They do not provide the frozen effective-query Gram, prefix sigma-field, counterfactual overwritten state, Loewner prediction-set coverage, or equal-budget protected ledger. Endpoint accuracy may reveal a behavioral difference after implementation, but it cannot identify whether equations (13), (18) or (22) were the mechanism.

No native mechanism-identifying benchmark was located in this bounded, fixed-asset packet audit. Creating instrumented Delta traces would be a future experiment-design obligation and is outside this mathematical pass.

## 7. Audit decision

- Mathematical mechanism: conditionally supported as a robust/statistical certificate.
- Broad originality: **REJECTED_MAJOR_COLLISION** with robust observability, matrix concentration/confidence sequences, predictive quotients and R09.
- Delta-specific residual: **PARTIAL_THEOREM_DELTA** — exact erased-direction support and mean/pathwise distinction.
- Architecture candidate: not admitted.
- Native measurement: absent.
- Experimental effect: unknown; no execution.

R17 v2 is retained as a useful debugging theorem/control. Reopening needs a prefix-valid deployed-law construction, matched-total-cost advantage over direct sufficient-coordinate storage, and a native measurement object; threshold or estimator variants alone are not distinct methods.
