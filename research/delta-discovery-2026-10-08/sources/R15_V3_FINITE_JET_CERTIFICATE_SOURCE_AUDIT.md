# R15 v3 finite-jet certificate boundary — primary-source, author-interface, novelty, and measurement audit

- Math artifact: `repairs/R15_FINITE_JET_CERTIFICATE_BOUNDARY.v3.md`
- Artifact SHA256: `13cab85d2629935d453b53e8e4d9664d389db94805f8e927f51ebe47f053c2b0`
- Scope: bounded collision/feasibility audit, not exhaustive priority certification or empirical validation.
- Execution: no project/upstream code, model, benchmark, training, inference, scorer, data/model download, GPU, Docker, or paid service.
- Search date: 2026-10-11. Queries covered high-order Taylor regularization, derivative-Lipschitz remainder conditions, probabilistically accurate trust-region models, exact Delta interfaces, and the already-pinned R15 causal/measurement controls.

## 1. Exact contribution of v3

V1 established the support and lifted-design requirements for a declared quadratic causal response. V2 derived a polynomial degree upper bound, an abstract scalar Delta degree-growth witness, and a local Taylor regret certificate conditional on a uniform third-derivative bound. V3 does not propose another action estimator. It proves by an explicit polynomial pair that derivatives through any finite order at the current action do not themselves certify a nontrivial scale-free optimizer guarantee on a positive trust radius. It then states sufficient repairs: a uniform first-omitted-derivative envelope, a true degree cap, a possibly loose range/lower-bound fallback, or new trial outcomes.

The pair and its deterministic/randomized regret lower bounds are derived in the artifact; no external theorem is invoked to manufacture them. The source question is whether the repaired positive mechanism is already standard and whether any released Delta interface supplies the missing global certificate.

## 2. High-order Taylor and trust-region collision

Cartis, Gould & Toint, *Improved second-order evaluation complexity for unconstrained nonlinear optimization using high-order regularized models*, arXiv:1708.04044, §2 Eqs. (2.2)–(2.8) and Algorithm 2.1, assumes a globally Lipschitz `p`-th derivative, defines the order-`p` Taylor model, gives a one-sided function bound plus gradient/Hessian model-error bounds, adds a `||s||^(p+1)` regularizer, and accepts/rejects trial steps using the ratio of actual objective decrease to unregularized Taylor-model decrease. This covers the same established high-order Taylor/regularization regime and demonstrates that a smoothness envelope and trial evaluation are real assumptions/information, not consequences of a finite jet. R15's compact-ball absolute remainder and two-sided optimizer-regret sandwich are derived in the artifact under its stated bounded `(p+1)`-derivative assumption; they are not attributed verbatim to Cartis et al.

Cartis, Gould & Toint, *Universal regularization methods — varying the power, the smoothness and the accuracy*, arXiv:1811.07057, studies Taylor models whose guarantees vary with model accuracy and available smoothness. It is a close control for weakening or mis-specifying the derivative regularity; it does not provide a Delta-specific prefix certificate.

Bandeira, Scheinberg & Vicente, *Convergence of trust-region methods based on probabilistic models*, arXiv:1304.2808, studies a deterministic objective evaluated without noise and requires random models that satisfy stated approximation quality with probability at least one half inside a trust-region framework. This covers probabilistic model-quality validation as a generic route; the probability concerns model accuracy, not noisy real-outcome validation. It does not make an unvalidated local Delta jet globally accurate.

Consequently, the positive side of R15 v3 collides with established high-order regularization/trust-region machinery. The negative finite-jet pair is retained as a packet-specific theorem boundary, not advertised as priority novelty.

## 3. Delta paper and pinned author interface

Yang et al., *Parallelizing Linear Transformers with the Delta Rule over Sequence Length*, arXiv:2406.06484v6, §2.2 and §3.3, specifies the Delta recurrence and feature normalization. The pinned author implementation `fla-org/flash-linear-attention@a7880060012c862d58575ee23f613cafcd728d03`, `fla/layers/delta_net.py`, derives `q`, `k`, `v`, and sigmoid-or-unit `beta` from hidden states and dispatches recurrent/chunk Delta operators; the default query/key normalization is L2. `fla/ops/delta_rule/__init__.py` blob `8c8459c46fbc1de6dd3647a38d9870500d44aad2` exports the chunk and recurrent operators.

Neither the paper nor these interfaces expose a certified global `(p+1)`-derivative envelope, action trust radius, randomized branch outcomes, propensity log, or free-running counterfactual oracle. The affine immediate write geometry does not bound the coupled continuation's first omitted derivative. As in v2, the scalar `S -> S-S^3` recurrence is an abstract algebra witness, not a literal claim about the normalized pinned FLA model.

## 4. Preserved causal, polynomial, and action controls

The exact versions and sections already retained in the v1/v2 source audits remain applicable:

- Box–Wilson response surfaces, Pukelsheim optimal design, Allen-Zhu et al. finite linear-feature design, Bhat–Amballa polynomial bandits, and Volterra identification cover exact polynomial fitting, feature-rank, conditioning, and coefficient growth.
- Dudík et al. 2011 and Jiang–Li 2016 cover finite/sequential propensity-corrected evaluation; MIPS/OffCEM show that low-dimensional action embeddings need additional response structure.
- TTT Ouroboros at `lingjivoo/ttt-ouroboros@f7811f878679864e686c84abcd83dd05efdc0417` exposes finite dose menus, Recorded Replay, and later Settlement. These are finite trial/validation controls, not a uniform prefix derivative certificate.
- Internal `STEP2_PROJECTED_DELAYED_CREDIT.md` and `STEP2_RECURSIVE_RANDOM_METRIC_CONTROL.md` already cover action-space pullbacks, DDP/iLQR/GGN, direct action predictors, and fixed-suffix/free-running mismatch.

No source converts local derivatives into the missing causal outcomes or semantic-validity evidence.

## 5. Native measurement feasibility

- Open Bandit Pipeline has logged actions, contexts, rewards, and propensities, but no Delta state/action jet or coupled response.
- Ouroboros can compare its finite declared doses and later real-text Settlement, but does not provide arbitrary free-running potential outcomes or a certified supremum derivative bound on an action ball.
- LongMemEval, bAbI, LAMBADA, and RULER measure endpoints and do not natively expose the joint object `(prefix, action jet, uniform remainder envelope, randomized branch-consistent outcomes)`.

Thus a finite-dose residual can refute a declared local model after outcomes are acquired, but the reviewed assets cannot validate the claimed zero-outcome prefix certificate. The packet invents no benchmark, intervention label, derivative oracle, scorer, or result.

## 6. Audit decision

- Mathematical/source consistency: supported for the stated compact action ball, common-prefix/admissible-class condition, smoothness/degree assumptions, nonnegative-loss baseline option, and branch law.
- Functional novelty: `TERMINAL_THEOREM_DEBUG_CONTROL`; the proposed positive repair family has a `MAJOR_HIGH_ORDER_OPTIMIZATION_COLLISION`. This does not claim that the cited optimization papers state the explicit finite-jet lower-bound pair.
- Architecture candidate: not admitted.
- Native measurement: joint mechanism-identifying object absent in reviewed assets.
- Experimental effect: unknown; no execution.
- Lineage decision: attempt 3/3 exhausted and parked. Reopen only with changed causal information or a genuinely Delta-specific, prefix-lawful structural envelope that beats identical high-order/direct-action controls at matched total cost and has a native measurement object.

The v3 theorem is useful because it prevents a false repair—estimating a safe radius from a finite local jet—but it does not produce a new updater.
