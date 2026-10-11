# R17 v3 residual-scaled spectral certificate — source, interface, collision and measurement audit

- Subject: `../repairs/R17_RESIDUAL_SCALED_SPECTRAL_CERTIFICATE.v3.md`
- Scope: bounded primary-source and actual-interface reading plus mathematical comparison and native-measurement feasibility. This is not exhaustive priority certification or empirical validation.
- Execution: static reading only; no project/upstream code, tests, model execution, training, inference, scoring, dataset/model download, GPU, Docker or paid service.

## Preserved v1/v2 evidence

The v1/v2 audits remain binding. Predictive fibers, task-sufficient quotients, conditional rate-distortion, robust observability, empirical observability Gramians, matrix concentration/confidence sequences, R09's transported future-query metric and direct protected-coordinate ledgers already cover the broad mechanisms. V3 does not relabel those reads as new novelty. Its new question is narrower: whether a lawful PSD upper certificate can be compressed one-sidedly and combined with the actual Delta residual without losing safety.

## Low-rank approximation collision

Halko, Martinsson and Tropp, *Finding Structure with Randomness*, arXiv:0909.4061v2 / SIAM Review 2011, separate the two-stage framework in Section 1.2, randomized Stage A intuition in Section 1.3, Stage A algorithms in Section 4, Stage B factorizations in Section 5, and deterministic/probabilistic error analysis in Sections 9--10. This supports efficient approximate factors but also confirms that a probabilistic approximation carries an explicit failure/error term. A factor alone is not a Loewner upper certificate.

The top-eigenspace residual `lambda_(r+1)` in v3 is the standard Eckart--Young--Mirsky spectral boundary. Therefore the rank/slack result is a specialization of classical matrix approximation, not an originality claim.

Ghashami, Liberty, Phillips and Woodruff, *Frequent Directions: Simple and Deterministic Matrix Sketching*, arXiv:1501.01711 / SIAM Journal on Computing 2016, prove a deterministic row-streaming covariance-sketch bound of the form `||A^T A-B^T B||_2 <= ||A-A_k||_F^2/(ell-k)` and space/error optimality in their model. It is a direct strong baseline for online Gram compression.

Actual author implementation inspected at `edoliberty/frequent-directions`, commit `691df9edb2ffbc2fdddc2cec3b703a3f1e438d4d`:

- `frequentDirections.py`, blob `4bb3500cbea9c81c21cbeea5cd5db60ac4006d3d`, class `FrequentDirections(d, ell)`, methods `append(vector)`, private SVD shrink `__rotate__()`, and `get()` returning an `ell x d` sketch;
- `exampleUsage.py`, blob `9d4b909082597d00cfade20b84b6dd8113565f40`, forms `B^T B` from the returned sketch.

This interface computes a covariance sketch; it does not emit R17's prefix-conditioned future-law coverage, semantic retain/revise labels, or native paired no-write outcomes. Turning its additive covariance error into v3's `epsilon I` is legitimate only when the published bound's assumptions and tail term are charged.

## Empirical-Gramian collision and actual interface

Powel and Morgansen, *Empirical Observability Gramian for Stochastic Observability of Nonlinear Systems*, arXiv:2006.07451v1, Section II-B equations (5)--(7), construct empirical observability Gramians from perturbed trajectories. Their Section III, Theorem 3 and equation (19), separately relate the small-perturbation Gramian to Fisher-information bounds under additive Gaussian measurement noise. R17 v2 already recorded this collision.

Christian Himpe's author-maintained `emgr` was inspected at commit `79c4355b7f064130fbfb08db18c178f9e297a5dd`. `py/emgr.py` exposes
`emgr(f,g,s,t,w,pr,nf,ut,us,xs,um,xm,dp)`; setting `w="o"` perturbs each state coordinate, accumulates output trajectories in `obsCache`, and returns `W += dp(obsCache.T,obsCache)` after time/scale normalization. The README identifies version 5.99 and supports empirical observability, cross, sensitivity, identifiability and joint Gramians, plus custom solvers and inner products.

This is a real trajectory-Gramian interface and a strong construction baseline. It still requires model/output trajectories and does not make the future Gram available from a deployment prefix or make output movement synonymous with factual harm.

## Delta and control collision

Equation (4) in v3 is the already-known Delta response `Delta o(q)=beta(q^T k)e` propagated through a frozen suffix and squared. Yang et al., *Parallelizing Linear Transformers with the Delta Rule over Sequence Length*, arXiv:2406.06484v6, Section 2.2, specify the gated Delta recurrence. The fixed author implementation `fla-org/flash-linear-attention@a7880060012c862d58575ee23f613cafcd728d03`, `fla/layers/delta_net.py`, creates `b_proj` when `use_beta` is enabled, applies `sigmoid()` to produce `beta` in `forward`, substitutes ones when disabled, and passes that scalar gate to the recurrent/chunk Delta kernels. Thus Delta recurrences already learn scalar write gates. R09 already derives inverse-metric editing under a future-query Gram. V3's safe-step formula is therefore a theorem/debugging composition, not a new updater family.

The direct dense score `k^T U k` is a strong same-information baseline when `U` is affordable. When only the current direction is needed, a model that directly issues/calibrates a scalar upper score for `(prefix,k)`, or a global/isotropic scalar upper bound, is cheaper and mandatory. The standard quadratic benefit-versus-interference gate is also a direct control. A low-rank factor is useful only when multiple directions are queried and its construction/coverage cost is lower. A direct ledger `B^T S` has additional `rm` real-valued state because it provides the stronger ability to retain values through an unsafe write; matched bits, precision, metadata, refresh traffic, predictor and calibration costs remain unresolved, and comparing float counts without the capability difference would be misleading.

## Statistical and causal limits

Tropp's matrix concentration and Howard et al.'s confidence-sequence results from v2 remain the relevant sources for fixed-time versus anytime coverage. Compression failure probability must be unioned with future-Gram coverage. Conformal Risk Control (Angelopoulos et al., arXiv:2208.02814) controls expected monotone risk under its exchangeability setup, but does not automatically provide a matrix Loewner upper prediction set for each realized suffix. None of these sources supplies semantic validity from model self-assessment.

## Native measurement audit

The previously fixed native assets remain unchanged: ParlAI bAbI `a29567f7ce76992fd1f03c51ba9e3b155a37ea51`; lm-eval LAMBADA `d6de81643928d653435c431bae19945d41d32520`; RULER `c3f5e3b4f87f97e048793bb510a3a6b19a46bf3a` with pipeline `e8bbff677ca2c239640dc90f93310dcf32408c93`; LongMemEval `9e0b455f4ef0e2ab8f2e582289761153549043fc`.

Their native scorers expose endpoint answers/tokens. They do not expose paired no-write continuations, the effective-query Gram, a prefix-issued PSD upper matrix, low-rank spectral residual, coverage failure event, or equal-budget protected ledger. An instrumented paired-action trace would be a new measurement object, so no native mechanism-identifying benchmark is claimed.

## Audit decision

- Mathematics: conditionally supported as an action-specific one-sided bound and safe gate.
- Broad originality: **REJECTED_MAJOR_COLLISION** with Delta gating, observability Gramians and classical/streaming low-rank approximation.
- Residual contribution: **PARTIAL_THEOREM_DELTA** — correct residual scaling, probability composition, and capability-aware certificate-versus-ledger boundary.
- Architecture candidate: not admitted.
- Native measurement: absent.
- Experimental effect: unknown; no execution.

R17 closes after attempt 3/3 as a useful theorem/control. Rank, sketch, threshold, confidence and eigensolver variants are not new repairs.
