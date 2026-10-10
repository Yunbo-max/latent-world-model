# R02 v3 final-byte independent adversarial review

- Reviewer: `/root/r02v3_adversarial`
- Assignment: attack the one-step and finite-horizon bounds, observational-equivalence and rare-occupancy witnesses, DR/model distinction, hidden side-state, cost accounting, old-counterexample survival and candidate disposition.
- Artifact: `repairs/R02_APPROXIMATE_CAUSAL_DYNAMIC_QUOTIENT.v3.md`
- Exact artifact SHA256: `5d6d1894eeec0d5bd4ecb72c22cfeeefbadaa50e7ee8cc7ab5030280a3ef75c6`
- Verdict: **PASS — conditional theorem/debugging control only**
- Mandatory revisions remaining: none

## Adversarial findings

The sharp one-step bound cannot be strengthened under the stated moment information: aligned two-point fibers attain Cauchy--Schwarz, including the retained v2 witness. Zero covariance is only law-specific cancellation and does not establish outcome, propensity or dynamic sufficiency. The two-world example genuinely preserves the quotient-level binary `(A,Y)` distribution while changing the intervention mean; revealing hidden history or exact history-specific propensities would distinguish the worlds, but that is extra information and ledger cost.

The finite-horizon recurrence uses the correct TV/span constant and discount order under uniform target-reachable defects. Its rare-state witness defeats behavior-average calibration: an `O(delta)` behavior defect can coexist with `O(1)` target error, requiring uniform coverage or an explicit concentrability price. The artifact does not conflate this model/value guarantee with sequential DR; ratio approximation, pointwise overlap, product-ratio amplification, occupancy shift and nuisance remainders remain open.

The corrected fiber condition fixes both projected memory `q` and retained side state `z`; lawful `z` dependence is no longer mislabeled as hidden leakage. `AEW=0` removes only the direct projected term. State-dependent gate/key/value/routing coefficients can still transmit discarded memory, and the derivative is local rather than a global closure certificate. Small Euclidean distance between distinct deterministic states still permits TV distance one.

All material old failures remain: hidden support, continuation aliasing, ratio-ledger limits, local-versus-global leakage, behavior/target occupancy mismatch and identical-prefix hidden-fiber ambiguity. Information accounting includes `W`, `z`, exact propensity/cumulative-ratio ledgers, nuisance models and fiber/Jacobian coverage. Uniform certification may cost at least direct full-state prediction.

Approximate homomorphism, bisimulation/simulation, OPE state abstraction, sequential DR, MIS/STAR and packet-internal R18/R03 cover the main mechanism. Public endpoint benchmarks do not jointly expose the mechanism variables. Reopening requires new prefix-estimable certificates, complete-state treatment, estimator-specific DR math if claimed, matched-cost advantage and a native measurement object. Therefore `candidate_delta=0`, empirical effect unknown, attempt 3/3 exhausted and parked. No counterexample was removed to manufacture a pass, and no code or experiment was executed.
