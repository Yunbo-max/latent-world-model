# Independent adversarial review — R03 v3

Reviewer: `/root/r03_v3_adversarial_review`  
Review date: 2026-10-10  
Artifact: `repairs/R03_WASSERSTEIN_FREE_RUNNING_SAFETY.v3.md`  
Exact artifact SHA256: `9701f44391fc2d71154648cdfd4ab76bfac45a05e176bdd111a9b2f86a885ec6`  
Source audit: `sources/R03_V3_WASSERSTEIN_FREE_RUNNING_SOURCE_AUDIT.md`  
Exact source-audit SHA256: `7a27bdd8ee84a66a62d89d1f7dd77f5ab94e759d432fb3f88e63edae9118f998`

## Verdict

**PASS only as conditionally correct theory/control.** The final bytes' memory-metric comparison, outer-coverage statement, Wasserstein recurrence, unrolling, Lipschitz-loss conversion, homogeneous discounted sum, envelope predictions, and collision disposition survive the adversarial attacks. This pass does not admit a candidate or establish novelty, native measurability, empirical effectiveness, or a matched-cost advantage.

## Revision history closed in the final bytes

The first reviewed bytes used an ambiguous metric-comparison direction before (9) and a degenerate conditional confidence statement in (14). Intermediate bytes repaired those issues but still described geometric protected-loss decay without controlling `L_h`. The final artifact now:

- assumes the required upper comparison `d_0(x_0^a,x_0^0) <= c_S ||Delta S_a||_F` for the deterministic memory-only case;
- places coverage probability over an independent predeployment calibration object, uniformly over a declared history class, and explicitly rejects self-conditioning on `F_t`;
- states prediction 1 for the **certified envelope** under both `kappa_h<=kappa<1` and `L_h<=L`, while retaining `L_h P_(h:0) delta_0` when no uniform loss bound exists.

No blocking mathematical defect remains in the reviewed scope.

## Attacks that the current bytes withstand

1. **Corrected Delta injection bound — PASS.** The revised text now states the upper comparison actually required, `d_0(x_0^a,x_0^0) <= c_S ||Delta S_a||_F`, for a deterministic memory-only displacement. Together with the rank-one Frobenius identity this implies (9). It correctly excludes stochastic writes and any action that also changes updater/routing/policy/feedback state from the cheap specialization.

2. **Kernel integration inequality — PASS.** On Polish spaces with finite first moments, (3) implies `W_1(nu K^a,nu K^0) <= int W_1(K^a(x),K^0(x)) nu(dx) <= epsilon`; (2) lifts to `W_1(mu K^0,nu K^0) <= kappa W_1(mu,nu)`. The triangle argument in (5) is sound. Routine measurability of the kernels/cost is implicit in the Markov-kernel/Polish setup.

3. **Non-Markov omitted state — PASS as a declared failure boundary.** If a hidden action-affected variable controls later tokens or environment responses, the observed state need not admit the kernels in (1), and the theorem is inapplicable. The artifact explicitly requires a complete closed-loop state and says the old objection returns if it is omitted.

4. **Changing metrics across time — PASS.** Equations (2), (4), and the product indices consistently use `d_h` on inputs and `d_(h+1)` on outputs. Metric rescaling cannot manufacture safety because the same predeclared metric must also support the loss Lipschitz constant.

5. **Persistent forcing — PASS after revision.** Equation (12) is an upper envelope, not a lower bound on the actual distance. The revised text correctly says that positive persistent forcing makes this undiscounted certificate diverge, while cancellations or loose one-step bounds can leave the actual gap smaller.

6. **Discontinuous protected loss — PASS as a boundary.** A bounded exact-match loss need not be Lipschitz in the chosen hidden-state metric; switching to a discrete metric can destroy useful contraction. The artifact does not silently apply Kantorovich--Rubinstein duality outside the Lipschitz class.

7. **Random initial laws — conditionally PASS.** The general theorem starts from arbitrary finite-first-moment `nu_0^a,nu_0^0`. Only the cheap Delta specialization is restricted to a deterministic pre-action state. A stochastic write/dropout/action requires a genuine coupling or direct `W_1` bound and does not inherit (9).

8. **Expected versus actionwise safety — PASS.** Equations (11) and (15) concern signed expected-loss increase and an expected-harm budget. The text correctly denies a realized-action maximum and notes that per-action safety plus positivity can be infeasible.

9. **Corrected calibration coverage — PASS.** Equation (14) now places probability over an independent predeployment calibration object and requires uniform simultaneous coverage over a declared history class. This avoids conditioning on the sigma-field that already contains the computed bound and true conditional target. The text also explicitly identifies the invalid self-conditioned alternative. This remains an assumed certificate/coverage construction, not evidence that a useful one is available.

10. **Empirical certificate leakage and hidden cost — PASS as unresolved feasibility, not a solution.** Sample endpoint `W_1`, realized future targets, or counterfactual suffixes do not yield an action-time uniform bound on (2)--(3). The artifact identifies leakage, high-dimensional estimation, simultaneous coverage, global neural certification, and simulator access as costs. It proves no same-budget advantage.

11. **Equivalence/collision — PASS.** The generic mechanism is a standard Markov-kernel perturbation/simulation/value bound. The source audit appropriately treats Rudolf--Schweizer, Asadi--Misra--Littman, bisimulation metrics, and Wasserstein robust MDPs as strong functional collisions. The Delta contribution is limited to immediate rank-one displacement bookkeeping and does not justify candidate admission.

## Required retained disposition after repair

`candidate_delta=0`; conditional theory/control only; measurement gap; empirical unknown; no novelty or matched-cost advantage; R03 parked and exhausted after attempt 3/3. No software execution, model run, benchmark scoring, training, inference, dataset/model download, GPU work, paid API, or Docker was used in this review.
