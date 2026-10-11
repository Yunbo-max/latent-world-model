# Independent final-byte mathematical review — R17 v2

- Reviewer: `codex-independent-math-reviewer-r17v2-final` (`/root/r17v2_math_review`)
- Assignment: independent semantic review of the causal predictive-leakage certificate, probability contract, partial-overwrite boundary, costs and disposition.
- Math artifact: `research/delta-discovery-2026-10-08/repairs/R17_CAUSAL_PREDICTIVE_LEAKAGE_CERTIFICATE.v2.md`
- Observed math SHA256: `c7f7843a9508dbb5cc6fdf9525e23dc311eff070f58b572bb133850722eb1438`
- Source audit: `research/delta-discovery-2026-10-08/sources/R17_CAUSAL_PREDICTIVE_LEAKAGE_SOURCE_AUDIT.v2.md`
- Observed source SHA256: `f8f7bd33008eda1750506833af5e5dff6be71d7f7bcaa60dbffac811e3929ea2`
- Verdict: **PASS_CONDITIONAL**
- Execution: static mathematics/source-consistency review only; no edits or project execution.

## Reasoning

Dimensions and the frozen-continuation scope are consistent. For an erased perturbation `ka^T`, the output loss is exactly `||a||^2 k^T G k`. The support function, common-kernel equivalence, spectral-ball maximizer and bounded-family worst case are exact.

The corrected sampling contract separates a fixed prefix stratum, calibration data and a fresh deployment suffix. The one-sided matrix-Bernstein radius states its centered-summand and variance conditions. Combining the calibration event with conditional Markov and a union bound correctly yields coverage at least `1-delta-alpha`; the artifact does not reuse the invalid pathwise mean substitution. The all-zero finite-sample boundary is correctly an upper-confidence-limit requirement `p_U(0^n)>=1-delta^(1/n)`.

The identical-prefix impossibility is valid. For partial overwrite, the Sherman--Morrison inverse, `1/(1-beta)` condition number, post-write residual, quadratic tradeoff and coefficient conditions are correct. Ledger state and prefix-varying basis costs are charged, and monotonicity is restricted to nested ambiguity sets.

## Adjudication

Accept only as a conditional theorem/debugging control. It does not establish semantic validity, recursive quotient closure, a cheaper prefix estimator, a matched-cost advantage or empirical benefit. Candidate, scientific-admission and selection increments remain zero.
