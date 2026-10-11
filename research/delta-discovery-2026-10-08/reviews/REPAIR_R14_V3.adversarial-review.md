# Independent adversarial and fair-budget review — R14 v3

Reviewer: `/root/r14_v3_adversarial`  
Mode: independent read-only counterexample, randomized-action, hidden-information and fair-budget review; no editing or project/model execution.

Reviewed exact final bytes:

- `repairs/R14_OBSERVABLE_EQUIVALENCE_CLOSURE.v3.md`
- SHA256 `7656047affe4d7866358cb5b3a568ea27d5effad427b6d93c9cdf45a55c5aa81`

## Attacks checked

- The certificate-collapse claim is restricted to endpoint posteriors and the stated uniform two-world coverage; it does not upgrade marginal calibration or a Bayesian credible set into tokenwise validity.
- The same-single-atom condition is explicit for the deterministic `[0,1]` conclusion.
- The artifact distinguishes a constant deterministic hard action from a mixed hard policy. Its value `min{1,(1+lambda)/2}` is correct, so it does not make the false claim that randomization is always useless.
- The TV lower bound is labeled a sharp lower bound rather than the exact value for every pair of observation laws.
- The common-mass conditional average loss and the global `(1-delta)` factor are stated separately.
- All calibration/router state and common algorithmic randomness are included in `O`; an identifier, delayed label, active query or world-correlated state is charged as extra evidence.
- Open-world identities, misspecified cost/Hessian/Jacobian, semantic validity and native counterfactual measurement remain outside the theorem.

## Verdict

**PASS as a scoped terminal theorem/control; no blocker.** Fair same-information controls face the same lower bound. A new evidence channel changes the experiment and must be costed equally. Candidate admission remains `NO`, `candidate_delta=0`, and empirical effect is unknown.
