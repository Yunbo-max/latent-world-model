# R03 v3 exact-byte independent mathematical review

- Reviewer identity: `/root/r03_v3_math_review`
- Assignment: static review of the Markov/Wasserstein assumptions, recurrence and unrolling, Delta injection bound, Kantorovich--Rubinstein risk bound, discounted algebra, logging-simplex feasibility, counterexamples, and claim scope
- Artifact: `research/delta-discovery-2026-10-08/repairs/R03_WASSERSTEIN_FREE_RUNNING_SAFETY.v3.md`
- Exact final artifact SHA256: `9701f44391fc2d71154648cdfd4ab76bfac45a05e176bdd111a9b2f86a885ec6`
- Verdict: **PASS (conditional theory/control; candidate delta zero)**
- Mandatory revisions remaining: `none`

## Revision history and final-byte binding

The first review of artifact SHA256 `0b1db0a0e9790a88b62d23adc804dfec568168c61deb77e5b8c68eeb7fcd5591` returned **REVISE** for three linked issues: the memory-metric inequality was described in the opposite direction from equation (9), and a one-sided upper recurrence was twice interpreted as an actual positive distance floor and once as an empirical floor prediction.  The artifact was revised and reread at SHA256 `0f44c91f217835bd4b28556c2661ea86392dec293f028b37b04e615d3516e636`; that version passed those mathematical checks.  A later revision at SHA256 `bc3ea5f5e0bc8c3326ca1d3170771dc79ceefbb338e31fc16149dd487425ff28` replaced the degenerate conditional-coverage notation in equation (14) with an independent-calibration, uniform outer-coverage statement and passed rereview.  The final revision scopes prediction 1 to `\kappa_h\le\kappa<1` and uniformly bounded `L_h`, while retaining the exact `L_hP_{h:0}\delta_0` envelope without that bound.  The reviewer reread exact current bytes at SHA256 `9701f44391fc2d71154648cdfd4ab76bfac45a05e176bdd111a9b2f86a885ec6`; they preserve all prior corrections and the prediction now follows exactly from equations (7) and (10).

## 1. State spaces, kernels, and measurability

The time-inhomogeneous formulation is dimensionally coherent.  For each `h`, both `K_h^a` and `K_h^0` have common domain `\mathsf X_h` and codomain laws on `\mathsf X_{h+1}`.  The complete-state requirement is the right closure condition: if action-affected decoder, policy, retrieval, environment, or pending-feedback variables are omitted, equations (1)--(3) do not describe the actual free-running laws.

Polish spaces plus finite first moments suffice for the displayed `W_1` quantities.  A Lipschitz loss is Borel measurable and integrable under those laws once it is finite at one reference point.  The artifact also correctly requires decision-time availability of numerical certificates and does not treat realized suffixes as deployment information.  It now distinguishes deterministic structural bounds from bounds computed using an independent predeployment calibration object `\mathcal D`.

Equation (2) need not have `\kappa_h<1` for the finite-horizon recurrence; when it is at least one it is a Wasserstein Lipschitz coefficient rather than a contraction.  The artifact mostly preserves that distinction and explicitly adds strict contraction only in the homogeneous corollary.

## 2. One-step recurrence and product indices

The proof of equation (5) is valid.  The first term obeys

\[
W_1(\nu_h^aK_h^a,\nu_h^aK_h^0)
\le \int W_1(K_h^a(x),K_h^0(x))\,\nu_h^a(dx)
\le \varepsilon_{a,h},
\]

and the second obeys the push-forward contraction inequality implied by (2).  The latter can be proved either by integrating a coupling or by applying Kantorovich--Rubinstein duality to `K_h^0 f`.  No common realized path is required.

The unrolling indices are correct.  In particular, at `h=1`, equation (7) gives `\kappa_0\delta_{a,0}+\varepsilon_{a,0}`, and at `h=2` it gives `\kappa_1\kappa_0\delta_{a,0}+\kappa_1\varepsilon_{a,0}+\varepsilon_{a,1}`.  The empty-product convention in equation (6) is consistent.

## 3. Delta initial displacement

The rank-one Frobenius identity itself is correct:

\[
\|\Delta S_a\|_F
=|\alpha_a\beta|\,\|k\|_2\,\|e\|_2.
\]

The final prose immediately before equation (9) now explicitly assumes the inequality it uses:

\[
d_0(x_0^a,x_0^0)\le c_S\|\Delta S_a\|_F.
\]

This is sufficient because the action is assumed to change no other state component.  Equality in the pure Frobenius metric and the need to include all other changed components are correctly stated.

## 4. Loss transfer and discounted algebra

Equation (10) is a correct application of Kantorovich--Rubinstein duality.  Equation (11) correctly upper-bounds the signed increase by first taking the absolute per-horizon expectation difference.  It therefore supplies a sufficient, possibly conservative expectation certificate, not a pathwise guarantee or semantic-validity certificate.

Under the homogeneous assumptions, equation (12) is a valid upper bound.  Summing it with weights `\lambda^h` gives

\[
\sum_{h\ge0}\lambda^h\delta_{a,h}
\le {\delta_{a,0}\over1-\lambda\kappa}
+{\varepsilon_a\over1-\kappa}
\left({1\over1-\lambda}-{1\over1-\lambda\kappa}\right),
\]

so equation (13) is algebraically correct.

The final bytes now interpret the recurrence in the correct one-sided direction.  Positive `\varepsilon_a` does not imply that the actual `\delta_{a,h}` has a positive floor: the supremum kernel discrepancy may occur off occupancy or discrepancies can cancel.  Section 4.1 instead says that the **certificate envelope** approaches `\varepsilon_a/(1-\kappa)` and that the undiscounted sum of that envelope diverges; Section 6 repeats the distinction.  Predictions 2--3 are likewise predictions about the envelope and explicitly withhold an exact-effect claim without tightness or a lower bound.  Prediction 1 is valid as a geometrically decaying upper envelope under the homogeneous bounded-`L_h` assumptions of Section 4.1.

## 5. Logging simplex feasibility

Equation (14) is now a valid form of calibration coverage.  For a fixed true conditional-risk function `\Delta R_{a,H}(f)`, randomness comes from the independent calibration object `\mathcal D`; the event is simultaneous over the finite action set and the predeclared admissible-history class `\mathcal H_t`.  Therefore, on the outer event, the inequality remains valid after an online history `f` is selected or observed.  This is materially different from conditioning on an already observed `\mathcal F_t` when both the true conditional risk and computed bound are `\mathcal F_t`-measurable, which would reduce the alleged conditional probability to an indicator.  The alternative of one simultaneous anytime event over the joint online filtration is also correctly identified.

The uniform event requires the usual implicit measurability of the displayed supremum/event and a calibration procedure that genuinely supplies uniform rather than pointwise coverage.  Those are declared assumptions, not results silently inferred from a plug-in estimate.  The artifact appropriately does not claim that such a tight high-dimensional calibration object is available natively.

Equation (16) is exact for feasibility of the simplex plus lower-propensity constraints and the linear expected-cost budget.  The minimum achievable budget cost is obtained by putting `\epsilon_\mu` on every action and all residual mass `1-K\epsilon_\mu` on an action attaining `\min_a\bar U_a^W`.  Thus feasibility is equivalent to `K\epsilon_\mu\le1` and the displayed budget threshold (assuming a finite action set and finite costs).  The artifact correctly distinguishes this expected mixed-action budget from per-sampled-action safety.

The objective `\sum_a g_a/\mu_a` does not affect constraint feasibility; positivity makes it finite for finite `g_a`.  No additional convexity claim is needed for the stated result.

## 6. Failure boundaries and scope

The artifact correctly retains the following limitations:

- a point Jacobian or separately stable subsystem is not a uniform full-kernel coefficient;
- exact-match loss under a Euclidean hidden metric can invalidate the Lipschitz transfer;
- changing/scaling the metric cannot be evaluated without the compensating loss Lipschitz constant;
- full-state Wasserstein estimation can be statistically prohibitive;
- a structural upper certificate and sequential OPE estimate different objects;
- neither object identifies whether an old fact remains semantically valid;
- the online scalar recurrence does not account for the potentially dominant cost of constructing global coefficients.

These are legitimate failure boundaries, although most are conditional arguments rather than explicit numerical counterexamples.  That is sufficient for this control artifact.  The contribution/disposition language is appropriately narrow: the recurrence is established perturbation mathematics, the Delta part enters only through the initial rank-one displacement, no same-budget advantage is proved, measurement remains open, and candidate delta remains zero.

## 7. Final verdict

The exact final bytes support a conditionally correct finite-horizon Wasserstein perturbation certificate, its homogeneous discounted corollary, and the finite-action logging-feasibility boundary.  They do not prove the required coefficients exist cheaply for a neural closed loop, do not turn a certificate envelope into an observed effect, do not identify semantic validity, and do not establish a novel or admitted Delta method.  Parking R03 after attempt 3/3 with candidate delta zero is mathematically consistent.

No project code, tests, model execution, training, inference, benchmark scoring, data/model download, GPU work, Docker, paid API, or scientific experiment was performed.
