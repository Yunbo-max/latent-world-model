# R02 v2 final-byte independent mathematical review

- Reviewer identity: `/root/r02_v2_math_review`
- Assignment: final-byte review of the one-step AIPW identity, sequential causal quotient, fixed-family Delta right-quotient lower bound, invariant-subspace and stochastic-kernel caveats, minimax quantifiers, counterexamples, dimensions and ledger accounting
- Artifact: `research/delta-discovery-2026-10-08/repairs/R02_CAUSAL_DR_QUOTIENT.v2.md`
- Exact final artifact SHA256: `255e687deff4c9f6ccde2130efc97e480e92f384fcadec8a905625d7033d921d`
- Verdict: **PASS (conditional theorem/debugging control)**
- Mandatory revisions remaining: `none`

## 1. One-step AIPW coarsening identity

Condition on the nuisance-training sigma-field when the nuisance is random. Full-history consistency and randomization imply

\[
\mathbb E\!\left[
 \frac{\mathbf 1\{A=a\}}{\bar\mu_a(q)}
 (Y-\widehat m_a(q))\middle|Q=q\right]
=\frac{\mathbb E[\mu_a(H)(m_a(H)-\widehat m_a(q))\mid q]}
 {\bar\mu_a(q)}.
\]

Using `E[mu_a(H)|q]=bar mu_a(q)`, the augmentation cancels for every fixed quotient nuisance and leaves

\[
\mathbb E[\psi_a^Q\mid q]
=\frac{\mathbb E[\mu_a(H)m_a(H)\mid q]}{\bar\mu_a(q)}
=\mathbb E[m_a(H)\mid q]
 +\frac{\operatorname{Cov}(\mu_a(H),m_a(H)\mid q)}{\bar\mu_a(q)}.
\]

Equations (2)--(3) are therefore exact whenever the coarse propensity is positive. Either outcome sufficiency or propensity sufficiency makes the covariance zero; accidental zero covariance is correctly classified as a weaker, law-specific cancellation.

The two-history witness is correct: `bar mu=1/2`, `E[m]=1/2`, `E[mu m]=3/8`, and `Cov(mu,m)=1/8`, so the quotient score has mean `3/4` and bias `1/4`, independently of the displayed nuisance value. The witness violates only quotient-level balance, not the assumed full-history randomization.

## 2. Sequential quotient sufficiency and failure witness

Equation (4) gives a valid strong primitive sufficient condition for an expected finite-horizon return:

1. target and behavior policies descend to `Q_t`;
2. the conditional mean current loss descends to `(Q_t,A_t)`;
3. the action-conditioned law of `Q_{t+1}` descends to `(Q_t,A_t)`.

With consistency, sequential exchangeability, target support and integrability, backward induction yields `Q_t^pi(H_t,a)=bar Q_t^pi(Q_t,a)`. The sequential DR identity can then use quotient Bellman functions and exact quotient ratios. For an additive expected return, separate factorization of the conditional mean loss and the next-quotient marginal kernel is sufficient; a joint loss/next-state distribution is not required for this expectation claim.

The artifact correctly labels these conditions sufficient rather than necessary. Exact full-history ratios stored separately, an exact quotient action value, or a valid marginalized-ratio construction can support weaker estimator-specific results. Its recursive witness is sound: current loss and policy factorization do not prevent two aliased histories from having different next-quotient laws and different continuation values.

## 3. Fixed-family Delta right-quotient lower bound

The dimensions and multiplication order are valid:

- `X,E,C_f` are `d_k x d_v`;
- `W` is `d_v x r` with orthonormal columns;
- `XW` is `d_k x r`;
- the discarded tangent fiber is `{E:EW=0}`.

For the linear quotient `L_W:E -> EW`, the Frobenius-orthogonal complement of its kernel is `{GW^T}`. Hence a scalar derivative annihilates every discarded tangent iff every row of `C_f` belongs to `range(W)`, equivalently

\[
C_f=C_fWW^T.
\]

The converse can be witnessed explicitly by `E=C_f(I-WW^T)`: it satisfies `EW=0` and

\[
\langle C_f,E\rangle_F
=\|C_f(I-WW^T)\|_F^2>0
\]

whenever the discarded component is nonzero. Equation (8) is therefore an exact first-order iff for each declared differentiable scalar object.

The revised quantifiers in equations (8)--(9) are correct. For one **fixed declared finite scalar family**, let `R_F` be the span of all rows of its policy, loss/value, transported-credit and declared transition-test covectors. If a single fixed right quotient represents every member locally, then `R_F subseteq range(W)`, so `r>=dim(R_F)=r_F`. Adding more observables to that same family cannot shrink the row-span lower bound. The artifact now correctly avoids comparing this value-side bound universally with R18's different full joint-state quotient.

Equation (9) is only a lower bound. The revision correctly withholds an existence/equality claim because next-quotient observables can themselves depend on `W`; recursive closure then becomes an invariant-subspace/fixed-point obligation. It also correctly separates finitely many scalar moment/Jacobian constraints from equality of stochastic kernels: finite tests imply full kernel equality only under an independently justified measure-determining test class or parametric kernel family.

The positive-action log-propensity domain is now explicit. At zero-probability boundaries the use of probability/logit covectors or omission of target-inactive actions avoids applying a logarithmic derivative outside its domain.

## 4. Minimax witness and quantifier order

The final artifact states the needed adversarial order:

1. first fix an arbitrary rank-`r<d_v` right quotient `W`;
2. then allow the declared minimax class to choose a lawful scalar policy logit or future credit with rank-one covector `u a^T`, where nonzero `a in ker(W^T)`;
3. perturb with `E=u a^T`, which obeys `EW=0` while changing that scalar object.

Therefore no one sub-full fixed `W` is uniformly exact over that formal class. This does not say that one fixed rank-one witness defeats every possible `W`, and it does not assert that a native language model realizes all witnesses. Both scope limitations are now explicit, so the formal full-width boundary is valid.

## 5. Information and ledger accounting

The revised accounting distinguishes model state from analysis records correctly:

- `XW` costs `d_k r` real coordinates, plus all retained recurrent side state and the representation/update of `W`;
- storing exact per-step behavior and target propensity scalars costs `O(T)` offline records per trajectory;
- an online estimator may maintain only an `O(1)` cumulative-ratio accumulator when its recurrence permits, but this neither makes `Q_t` Markov nor removes the source/logging obligation;
- quotient reward, transition and value models carry their own parameter, inference and verification costs;
- full-history DR, exact ratio ledgers, marginalized-ratio OPE and direct recurrent Q/policy prediction remain appropriate matched-information controls.

The artifact also correctly declines to infer variance or sample gains from dimensional compression. Product-ratio variance, history-specific support failure, quotient bias and rare action-relevant distinctions survive.

## 6. Counterexamples, local/global scope and disposition

- The within-cell example proves quotient AIPW bias without invalidating full-history randomization.
- The recursive example proves that current-step sufficiency need not be sequential sufficiency.
- A nonzero discarded policy/value covector falsifies local first-order factorization.
- Finite scalar transition tests do not establish equality of action-conditioned stochastic kernels.
- Pointwise Jacobian coverage does not establish nonlinear fiber constancy, forward congruence, discrete-route stability or disconnected-fiber equivalence.
- External ratio/value ledgers cannot be omitted from information/storage comparisons merely because they are not recurrent model coordinates.

The final bytes support a conditional theorem and design/debugging screen only. They do not prove a novel OPE mechanism, an exact nonlinear causal quotient, a Delta-specific matched-cost advantage, native benchmark measurability, candidate admission or empirical success. Parking R02 v2 after attempt 2/3 with candidate delta zero is mathematically consistent.

No project code, tests, model execution, benchmark scoring, training, inference or scientific experiment was executed for this review.
