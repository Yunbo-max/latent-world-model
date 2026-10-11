# Independent source and novelty review — R14 v3

- Reviewer identity: `/root/r14_v3_sources`
- Assignment: independent primary-source, closest-work, and novelty review
- Artifact reviewed: `R14_OBSERVABLE_EQUIVALENCE_CLOSURE.v3.md`
- Artifact SHA256: `7656047affe4d7866358cb5b3a568ea27d5effad427b6d93c9cdf45a55c5aa81`
- Source audit reviewed: `R14_V3_OBSERVABLE_EQUIVALENCE_SOURCE_AUDIT.md`
- Source-audit SHA256: `804720519bb026bcb15a5aff66947b2933062c5c6a109c1d1d6b1e2477369261`
- Review status: final exact-byte review

## Verdict

**PASS for source support as a scoped theorem/debug control; FAIL for a novel method or candidate. No blocking source defect.** `candidate_delta=0`, `novel_method_supported=false`, `useful_theory_control=true`, `native_measurement_supported=false`; empirical effect is unknown. Park attempt 3/3.

## Source support and collisions

1. Barber, arXiv:2004.09477v3, Definition 1 equation (3) and Theorems 1–2; EJS 14(2):3487–3524, DOI 10.1214/20-EJS1749, is the closest primary collision for distribution-free confidence intervals for conditional Bernoulli probabilities. Its lower bound is in a nonatomic i.i.d. random-covariate setting, not the sequential endogenous-prefix setting of R14.
2. Barber–Candès–Ramdas–Tibshirani, arXiv:1903.04684v2, section 2.2 Proposition 1 and section 3, establishes limits on exact/object-conditional predictive coverage. It concerns response prediction sets, not posterior-parameter intervals.
3. Vovk, arXiv:1209.2673v2, sections 2 and 5 and Proposition 1, supports that standard inductive conformal validity is exchangeability-based and unconditional; it does not provide tokenwise provenance-posterior coverage.
4. Tibshirani et al., NeurIPS 2019, section 3 Definition 1, Lemmas 2–3 and Theorem 2, requires weighted exchangeability and likelihood-ratio assumptions under covariate shift. It remains a prediction-set result rather than an R14 provenance certificate.
5. Polyanskiy–Wu, arXiv:1902.05616v2, section 1 and the proof of Theorem 1, equations (20)–(21); Annals of Statistics 54(1):1–24 (2026), DOI 10.1214/25-AOS2498, is a modern Le Cam/two-point indistinguishability precedent. It supports the general principle, not R14's exact common-submeasure factor.
6. The R14 v2 Qiu–Luedtke Gamma-minimax and credal-decision sources remain the correct robust-Bayes collision. The v3 two-slot closed form is a Delta-specific specialization, not a new decision-theory family.

## Required caveats

- None of the cited conditional-coverage papers directly proves the sequential endogenous-prefix theorem. The finite two-world lemma is self-contained and was reviewed on its own derivation.
- Conformal coverage cannot be repurposed as calibrated coverage of `P(J=1 | O)` without the relevant exchangeability or shift and target-class assumptions.
- Le Cam provides precedent for indistinguishability. The factors `(1-TV) lambda/(1+lambda)` and `(1-2 alpha-TV)_+`, the hard-randomization boundary, and the equality constructions depend on the artifact's derivation and math review.
- No priority or “first” claim is supported.
- No inspected native benchmark exposes paired identical-observation/opposite-identity worlds together with every action's counterfactual loss.

## Novelty disposition

The Delta-slot constants and closure of the certificate-oracle gap are useful project-specific theorem specializations. Conditional-coverage impossibility, TV data processing, two-point minimax lower bounds, and robust-Bayes routing are established theory. The strongest implementation control remains the direct same-information minimax router. Retain this artifact as a theorem/control, not architecture or updater novelty.
