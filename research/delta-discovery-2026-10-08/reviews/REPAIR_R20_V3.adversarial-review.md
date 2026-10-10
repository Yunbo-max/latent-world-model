# Independent adversarial review — R20 v3

Reviewer: `/root/r20_adversarial`  
Assignment: search for domain, measurability, semidefinite, linear-term, nonlinear and low-rank counterexamples; reviewer did not author repository files.  
Artifact: `research/delta-discovery-2026-10-08/repairs/R20_SPECTRAL_TRANSFER_CERTIFICATE.v3.md`  
Artifact SHA256: `9fff175d5a25aa905ba1cc8efa11ae5d6bf56a1f66539619f4f0ba7481aedde7`

## Verdict

**Conditional theorem/no-go survives; method repair fails and must be parked.** Candidate, scientific-admission and selection increments are zero.

## Counterexample audit

1. **Tangent-only failure.** With feasible \(x=(1,u)\), \(\widehat H=I\), and
   \[
   H_b=\begin{bmatrix}b^2+\varepsilon&b\\b&1\end{bmatrix},
   \]
   the metrics agree exactly on \(\ker A\), but the prefix and future optima are \(u=0\) and \(u=-b\); the risk ratio \((b^2+\varepsilon)/\varepsilon\) is unbounded. The final artifact correctly requires the affine feasible span.
2. **Loss linear term.** Even when \(H=\widehat H\), the future loss \((u-b)^2/2\) reverses the action through its tangent linear term. The artifact correctly limits the theorem to homogeneous quadratics.
3. **Nonlinear remainder.** The family \(b(1-u^3)^2+u^2/2\) matches the local derivative and Hessian at zero for every \(b\) but has an unbounded finite-action gap. The artifact correctly retains the complete-state Jacobian/trust-region requirement.
4. **Missed direction.** If \(v\perp\operatorname{span}(Z)\), the indistinguishable continuation \(H_2=\widehat H+\rho vv^\top\) violates any announced \(\delta<\rho/\lambda\). Low rank plus damping does not create a transfer certificate.
5. **Semidefinite boundary.** At \(\delta\ge1\) a relevant future optimum may have zero risk and no finite multiplicative factor exists. Strict lower transfer is inconsistent with such a relevant null direction.
6. **Measurability.** A suffix-estimated \(\delta\) is post-hoc evaluation, not a legal current-action input. Identical-prefix future worlds prove the deterministic prefix impossibility.

## Hidden-cost and equivalence check

V3 changes no action relative to v2 and adds no deployable estimator. Any stochastic certificate would require separately priced assumptions, samples, confidence coverage and adaptive-write failure accounting. The symmetric robust set is an analysis wrapper around the existing action.

## Final assessment

All decisive counterexamples are retained rather than removed. The artifact makes no performance or originality claim and exhausts the third repair attempt. Disposition `park_final_attempt_as_theorem_no_go_control` is supported.
