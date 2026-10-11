# R15 v2 coupled-response degree — primary-source, author-interface, novelty, and measurement audit

- Math artifact: `repairs/R15_COUPLED_RESPONSE_DEGREE.v2.md`
- Artifact SHA256: `786bc749464ec9d400690fd279d1768a353f8917f8a68a5fa7d8c9ac9edf0ff7`
- Scope: bounded collision/feasibility audit, not exhaustive priority certification or empirical validation.
- Execution: no project/upstream code, model, benchmark, training, inference, scorer, data/model download, GPU, Docker, or paid service.

## 1. What changed relative to v1

V1 assumed an exact quadratic conditional response and then correctly applied lifted linear regression/response-surface design. V2 does not present another estimator. It derives when that assumption follows from the continuation: polynomial maps compose multiplicatively in degree; affine continuation plus degree-at-most-two loss closes at degree at most two; one algebraically admissible state-dependent scalar Delta step can instead give `S -> S-S^3` and degree-six terminal loss. The source question is therefore whether this closure/failure theorem supplies a new Delta method or only a debugging boundary.

## 2. Delta formula and actual author interface

- Yang et al., *Parallelizing Linear Transformers with the Delta Rule over Sequence Length*, arXiv:2406.06484v6, §2.2 (Delta update) and §3.3 (feature-map normalization), specifies the Delta recurrence and ordered low-rank computation. It supports the algebra used by the witness but does not claim that a current write has a globally quadratic free-running value.
- The author implementation `fla-org/flash-linear-attention@a7880060012c862d58575ee23f613cafcd728d03`, `fla/layers/delta_net.py`, constructs `q`, `k`, `v`, and—when `use_beta=True`—sigmoid `beta` from hidden states; `use_beta=False` instead supplies ones. It dispatches `fused_recurrent_delta_rule` or `chunk_delta_rule`. The default `qk_norm='l2'` and nonlinear hidden-state feature path do not supply the affine-continuation premise needed for exact quadratic closure. `fla/ops/delta_rule/__init__.py` blob `8c8459c46fbc1de6dd3647a38d9870500d44aad2` exports `chunk_delta_rule`, `fused_chunk_delta_rule`, and `fused_recurrent_delta_rule`; it contains no intervention-rank, response-degree, propensity, or branch-outcome interface.
- The scalar witness is an abstract unnormalised state-dependent Delta-rule-algebra recurrence, not a claim that pinned FLA/Parallel DeltaNet literally sets `k=S` or realizes the `2*3^H` path. It proves only non-implication: the bare Delta algebra does not force a low-order action response.

## 3. Polynomial response and experimental-design collisions

The degree-composition inequality and monomial count `binom(r+m,m)` are standard polynomial algebra. Once the degree-`m` response is lifted to `psi_m`, the full-rank Gram iff argument is ordinary linear-model estimability, already covered in the v1 source audit by Box--Wilson response-surface methodology, Pukelsheim optimal design, and Allen-Zhu et al. 2017 finite linear-feature design.

Additional primary controls checked for the v2 scope:

- Bhat & Amballa, *Identifying near-optimal decisions in linear-in-parameter bandit models with continuous decision sets*, UAI 2022 / PMLR 180, abstract and the polynomial-specialized algorithm, treats a known nonlinear feature map and specializes the decision problem to univariate polynomial mean reward. This directly covers treating polynomial action response as linear-in-parameter design rather than a Delta-specific learner.
- Dalla Libera, Carli & Pillonetto, *A novel Multiplicative Polynomial Kernel for Volterra series identification*, arXiv:1905.07960, §2.1 (distinct monomial features and least squares), §2.2, and §3.1–3.2 (high-degree polynomial-kernel limitations and multiplicative kernel), treats polynomial/Volterra nonlinear system identification and coefficient-growth/regularization. It is a mechanism neighbor for high-order response fitting, not evidence that R15's scalar counterexample appeared there.
- Sidorov et al., *Volterra black-box models identification methods: direct collocation vs least squares*, arXiv:2310.19382, abstract, §1 and §2, describes parameter growth and truncated Volterra-kernel identification. It supports the generic nature of the saturated feature-count warning, not a Delta-specific lower bound.

The exact `2*3^H` scalar-degree witness is useful packet-specific derivation work, but it is only a counterexample inside the unconstrained Delta algebra. Degree alone does not imply `q_m` unknown parameters: a fixed structured recurrence can be known or low dimensional, and optimizer identification can be easier than full coefficient recovery. The underlying polynomial-composition and lifted-regression mechanisms are established mathematics. No originality or priority claim is made for the witness theorem.

## 4. Local quadratic/DDP collision

Equation (11) is the action-space pullback of a continuation gradient/Hessian. Its Taylor remainder and two-epsilon decision-regret sandwich are standard local optimization facts. `STEP2_RECURSIVE_RANDOM_METRIC_CONTROL.md` already records the complete-Jacobian Hessian/GGN pullback, DDP/iLQR controls, and the fixed-suffix/free-running gap. `STEP2_PROJECTED_DELAYED_CREDIT.md` already records `B^T lambda`, action-space quadratic control, finite-horizon tails, and the stronger same-information direct action predictor.

Accordingly, one VJP plus directional HVPs may be a useful computational route under model access, but it is not a new causal estimator or a capability unavailable to direct DDP/iLQR/GGN/constrained action optimization. A learned Q/action predictor with the same prefix information remains the deployment comparator; model derivatives add an internal-model assumption rather than external counterfactual evidence.

## 5. Causal and free-running controls preserved from v1

Dudik et al. 2011 and Jiang & Li 2016 remain the primary AIPW/sequential-DR controls, with the exact sections/equations retained in `R15_INTERVENTION_RANK_SOURCE_AUDIT.md`. Saito & Joachims MIPS/OffCEM remain the structured-action warning that embeddings need additional outcome structure. TTT Ouroboros `lingjivoo/ttt-ouroboros@f7811f878679864e686c84abcd83dd05efdc0417` remains the strongest finite-dose/Recorded-Replay/Settlement implementation control: `README.md`, `scripts/preq_obs.py` (`--settle-alpha-grid`), `scripts/horizon.py` (recorded replay), `scripts/deferred.py` (defer/settle), and `ttt_pt/parallel_probe.py` (`score_fast_weight_branches`, fixed doses). None turns a fixed descendant into a lawful free-running counterfactual, and none makes a polynomial world model correct from one factual branch.

## 6. Native measurement feasibility

- Open Bandit Pipeline exposes actions, rewards, contexts, propensities, and generic OPE estimators at the pinned files/commit recorded in `R15_INTERVENTION_RANK_SOURCE_AUDIT.md`, but not internal Delta writes or coupled response derivatives.
- Ouroboros exposes finite alpha/dose menus, Recorded Replay, and later real-text Settlement. Dose-fit residuals are measurable on its controlled branch, but no native field gives arbitrary free-running potential outcomes or exact polynomial coefficients.
- LongMemEval (pinned scorer files in the v1 audit), bAbI, LAMBADA, and RULER (existing project benchmark audits) measure endpoints. They do not natively log the action coordinate, randomized support, branch-consistent outcomes, or a response-degree certificate.

No reviewed native asset closes the joint measurement object. The packet does not invent actions, coefficients, labels, metrics, or results.

## 7. Audit decision

- Mathematical/source consistency: supported for the explicit polynomial, smoothness, branch, and moment assumptions.
- Functional novelty: `THEOREM_DEBUG_CONTROL / MAJOR_MECHANISM_COLLISION`.
- Architecture candidate: not admitted.
- Experimental effect: unknown; no execution.
- Reopen condition: a lawful prefix-measurable closure or trust-radius certificate, a Delta-specific action unavailable to same-information direct optimization/Q prediction, a matched-total-cost advantage, and a native branch-consistent action-response measurement object.

R15 v2 is a substantive assumption-debugging repair, but it does not overcome v1's method collision. Candidate delta remains zero.
