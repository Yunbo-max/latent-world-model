# R02 v3 final-byte independent mathematical review

- Reviewer: `/root/r02v3_math`
- Assignment: independently check the quotient-AIPW identity and sharp bounds, finite-horizon value recurrence and TV constants, counterexamples, Delta dimensions/derivative, complete fiber condition, costs and theorem scope.
- Artifact: `repairs/R02_APPROXIMATE_CAUSAL_DYNAMIC_QUOTIENT.v3.md`
- Exact artifact SHA256: `5d6d1894eeec0d5bd4ecb72c22cfeeefbadaa50e7ee8cc7ab5030280a3ef75c6`
- Verdict: **PASS — conditional theorem/debugging control**
- Mandatory revisions remaining: none

## Checks

Conditioning on the nuisance-training sigma-field when needed, the identity

\[
B_a(q)=\frac{\operatorname{Cov}(\mu_a(H),m_a(H)\mid q)}{p_a(q)}
\]

is exact under the stated full-history randomization, consistency, coarse positivity, and fixed/cross-fitted/pre-action-predictable quotient nuisance. Conditional Cauchy--Schwarz gives `|B|<=sigma_mu sigma_m/p`; conditional Grüss gives the stated range product divided by `4p`. The two-point aligned construction attains equality, and the old v2 witness remains an equality case. The two-world construction has the same quotient-level binary `(A,Y)` law but target means `1/2` and `5/6`, so the non-identifiability conclusion is valid.

With conventional `d_TV=sup_B=1/2||.||_1`, `|E_P f-E_Q f|<=span(f)d_TV`. Under the declared target-policy factorization and target-reachable uniform reward/transition defects, Bellman insertion gives

\[
\Delta_t\le\epsilon_{r,t}+\gamma\Delta_{t+1}+\gamma M_{t+1}\epsilon_{P,t},
\]

with `M_(T+1)=Delta_(T+1)=0`; the unrolled exponents and range are correct. The rare-action example correctly has behavior-average defect `2 delta(1-delta)` but target error `1-delta` (or `gamma(1-delta)` one step earlier). These equations are a target-value abstraction bound, not an approximate sequential-DR theorem.

All Delta dimensions and order are correct for `S in R^(d_k x d_v)`, `W in R^(d_v x r)`, `q=SW`, and `v_W=W^T v`. The projected update is `q+=Aq+beta k v_W^T`. For discarded `E` with `EW=0`, the direct `A(S)EW` term vanishes while coefficient derivatives remain. The corrected diameter fixes every declared retained coordinate by requiring the same `(q,z)` fiber. The metric/Wasserstein branch correctly needs Lipschitz continuation values and does not infer TV closeness from Euclidean closeness.

## Boundaries and disposition

The old failures remain: zero covariance need not imply factorization; coarse overlap need not imply history-level support; current reward/policy agreement need not imply continuation closure; behavior-average defects need occupancy control; a local zero derivative does not imply global fiber closure. The accounting charges `W`, side state, ratio ledgers, nuisance models and calibration/fiber access. No state, sample or total-compute advantage follows.

Unclosed are a lawful prefix-estimable confidence certificate, history-level support or another valid identification route, estimator-specific sequential-DR bias/variance, global complete-state closure, native mechanism measurement, and matched-information advantage. Empirical effect is unknown. The supported state is `math_status=conditionally_supported`, `candidate_delta=0`, and park after attempt 3/3. No code, test, model, benchmark, training, inference or experiment was executed.
