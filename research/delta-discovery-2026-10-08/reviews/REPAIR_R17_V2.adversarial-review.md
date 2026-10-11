# Independent final-byte adversarial review — R17 v2

- Reviewer: `codex-subagent:/root/r17v2_adversarial_review`
- Math SHA256: `c7f7843a9508dbb5cc6fdf9525e23dc311eff070f58b572bb133850722eb1438`
- Source-audit SHA256: `f8f7bd33008eda1750506833af5e5dff6be71d7f7bcaa60dbffac811e3929ea2`
- Verdict: **PASS_CONDITIONAL**
- Execution: static adversarial review only; no edits or project execution.

## Attack results

The final bytes explicitly restrict equations (3)--(14) to a frozen linear continuation and refuse to treat endogenous/free-running queries as covered without a full-state coupling or remainder argument. Calibration and deployment randomness are separated; mean leakage is not promoted to pathwise safety; probabilistic zero-score conclusions retain their `1-delta` scope.

The robust ball calculation, identical-prefix construction and finite-sample rare-event boundary survive attack. Boundedness alone returns the full isotropic worst case. Partial overwrite removes the exact kernel but creates reciprocal ill-conditioning and does not solve the unknown future-relevance coefficient. Direct ledgers, abstention, ordinary gating and R09 inverse-metric edits remain stronger same-information controls.

The corrected ambiguity-set notation is consistent. No remaining causal, mathematical, cost, collision or measurement defect was found under the declared assumptions.

## Adjudication

Park after attempt 2/3. Do not count as an active or scientifically admitted candidate; no empirical conclusion follows.
