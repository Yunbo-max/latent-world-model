# Independent source/closest-work review — R03 v3 final bytes

Reviewer: `/root/r03_v3_source_review`  
Review date: 2026-10-10  
Math artifact: `research/delta-discovery-2026-10-08/repairs/R03_WASSERSTEIN_FREE_RUNNING_SAFETY.v3.md`  
Math artifact SHA256: `9701f44391fc2d71154648cdfd4ab76bfac45a05e176bdd111a9b2f86a885ec6`  
Source audit: `research/delta-discovery-2026-10-08/sources/R03_V3_WASSERSTEIN_FREE_RUNNING_SOURCE_AUDIT.md`  
Source-audit SHA256: `7a27bdd8ee84a66a62d89d1f7dd77f5ab94e759d432fb3f88e63edae9118f998`

## Verdict

**PASS for the bounded source/collision audit and theory-control disposition.** The exact final bytes correctly classify the law-distance recurrence, geometric accumulation, and Lipschitz expected-loss consequence as established perturbation machinery. This is not an exhaustive priority search, an empirical-validation pass, or evidence that the proposed certificate is useful or affordable for a language model.

## Primary-source findings

1. **Rudolf--Schweizer is the direct generic collision.** In arXiv:1503.04123, Proposition 2.1 gives contractivity through the generalized Dobrushin/Wasserstein ergodicity coefficient. Theorem 3.1 decomposes the nth-step discrepancy into an initial-law term and accumulated one-step kernel perturbations under Wasserstein ergodicity and a Lyapunov condition. Corollary 3.2 gives the uniform-kernel-error specialization
   \[
   W(p_n,\widetilde p_n)\le C\left(\rho^nW(p_0,\widetilde p_0)+(1-\rho^n)\frac{\gamma}{1-\rho}\right).
   \]
   R03 v3's time-inhomogeneous one-step recursion is a simpler triangle/contractivity specialization, not a new perturbation principle. The source audit is also appropriately cautious: Rudolf--Schweizer analyze homogeneous chains and an ergodicity envelope, whereas R03 writes a finite-horizon nonhomogeneous recursion.

2. **Asadi--Misra--Littman covers the same compounding-error/value logic in model-based RL.** The official PMLR 80 paper defines Wasserstein distance and Kantorovich--Rubinstein duality in Eqs. (3)--(4), proves a Lipschitz transition operator in Lemma 1, and in Theorem 1 bounds n-step prediction error by one-step error times a geometric sum of transition Lipschitz factors. Their result is stated for a fixed action sequence and their particular Lipschitz model class. R03 instead absorbs policy, updater, retrieval, and environment variables into a closed-loop Markov state, but that reframing does not create a new propagation mechanism.

3. **Ferns--Panangaden--Precup is a strong metric/task-alignment collision.** arXiv:1207.4114 defines bisimulation metrics using immediate-reward discrepancies and Wasserstein/Kantorovich distances between transition laws, then bounds optimal-value differences through the metric. This supports R03's warning that an arbitrary hidden-state metric with a small contraction factor is scientifically insufficient unless the protected loss/value is controlled in that same metric. The R03 artifact does not claim that the Ferns metric is identical to its chosen product metric.

4. **Neufeld--Sester directly covers Wasserstein transition ambiguity to value-gap control.** In arXiv:2308.05520, Theorem 3.1 assumes the paper's Lipschitz reward/kernel conditions and bounds the robust-versus-nonrobust value difference linearly in the Wasserstein-ball radius, with dependence on discount and Lipschitz constants. This is a robust-MDP result rather than a Delta-memory result, but it rules out novelty for the general claim that Wasserstein kernel discrepancy plus Lipschitz structure yields a value/risk bound.

5. **Weed--Bach supports only the bounded statistical-cost warning, not an impossibility claim.** arXiv:1707.00087 proves finite-sample and asymptotic empirical-Wasserstein rates on compact metric spaces in terms of intrinsic/Wasserstein dimension; for regular d-dimensional measures the characteristic rate is approximately `n^{-1/d}` in the relevant regime. R03's wording--full-state empirical `W_1` *can* be prohibitive without additional structure--is supported. The source does not justify a universal curse for every structured, low-dimensional, discrete, or parametric state law, and the artifact does not make that stronger claim.

## Formula and assumption boundary

- The source-supported generic step is `delta_(h+1) <= kappa_h delta_h + epsilon_h`, provided `kappa_h` is a valid Wasserstein Lipschitz coefficient for the complete reference kernel and `epsilon_h` uniformly controls the action/reference kernel discrepancy. The unrolled product/sum and discounted homogeneous corollary are elementary consequences. The revised final bytes correctly call the persistent-forcing limit a **certificate-envelope** plateau, not a lower bound on the actual law distance; cancellations or loose one-step bounds may make the true gap smaller.
- The final Prediction 1 is now scoped correctly: geometric decay of the protected-loss envelope requires both `kappa_h <= kappa < 1` and a uniform observable bound `L_h <= L`. Without the latter, Kantorovich--Rubinstein yields only the exact factor `L_h P_(h:0) delta_0`, which need not decay even when the state-law distance does. This narrowing agrees with the cited Lipschitz/value-bound literature and does not change novelty.
- Kantorovich--Rubinstein duality supports conversion to an expectation gap only for observables Lipschitz in the same declared metric. It does not certify discontinuous exact-match loss under an arbitrary Euclidean hidden-state metric.
- The cited literature does not supply R03's action-time simultaneous confidence event, complete neural closed-loop coefficients, or native language-model state metric. Those remain assumptions/measurement gaps, not source-backed available estimators.
- The revised Eq. (14) now states an outer-probability uniform event over an independent calibration object and the declared history/action class, with an anytime joint-filtration event allowed as an alternative. This correctly avoids treating an already `F_t`-measurable inequality as a nondegenerate conditional-coverage probability. It is an explicit additional assumption rather than a guarantee attributed to any of the five checked perturbation papers, so it does not alter the collision or novelty decision.
- Rudolf--Schweizer's Lyapunov-weighted and ergodicity assumptions are not silently inherited as if identical to R03's finite-horizon uniform assumptions. Conversely, R03's simpler assumptions do not improve their general theorem.
- The rank-one Delta equality is lineage-specific only at the immediate memory displacement. The revised metric premise now states the required upper bound `d_0(x_0^a,x_0^0) <= c_S ||Delta S_a||_F`, so its direction agrees with Eq. (9). None of the checked sources implies that subsequent law propagation remains rank one, cheap, or Delta-specific.

## Novelty, implementation, and measurement decision

The supported residual is narrow: an audit specialization that composes (i) an immediate Delta rank-one write norm, (ii) a generic full-law Wasserstein perturbation envelope, and (iii) the already established propensity-floor/expected-harm feasibility calculation from earlier R03 versions. The five primary sources are sufficient to reject novelty for the generic recurrence, geometric accumulation, metric-to-value link, and Wasserstein statistical-cost claim. They do not exhaustively prove that no narrower Delta theorem exists; accordingly, the artifact avoids first/new/unique language.

The closest sources are theorem papers, and R03 attributes no executable result or author-code behavior to them. The absence of an implementation read therefore does not weaken the formula collision. Existing benchmark statements are correctly bounded as a native measurement gap: endpoint retention/accuracy does not by itself expose a complete action-time Markov state, per-action kernels, simultaneous contraction/mismatch bounds, or paired free-running counterfactual laws. No benchmark outcome or negative empirical result is inferred.

The artifact's `candidate delta = 0`, `park after attempt 3/3`, and `empirical status = unknown` follow from the strong functional collision plus the unclosed same-information/state/compute and native-measurement obligations. The theorem may remain a useful control even though it does not qualify as a new candidate.

## Final disposition

- `source_status`: `primary_sources_supported_final_bytes`
- `novelty_status`: `major_functional_collision_theory_control_only`
- `residual_status`: `delta_injection_to_generic_law_certificate_specialization`
- `implementation_status`: `no_implementation_claim; theorem_interfaces_only`
- `measurement_status`: `native_closed_loop_certificate_gap`
- `candidate_admission`: `0`
- `empirical_status`: `unknown_not_executed`
- `mandatory_revisions`: `none`

No project/source code, model, benchmark scorer, training, inference, dataset/model download, GPU workload, paid service, or Docker was executed.
