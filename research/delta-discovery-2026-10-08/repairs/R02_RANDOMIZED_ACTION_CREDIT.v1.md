# R02 v1 — randomized Delta action credit

Status: **conditional causal identification control; not an active D candidate**. This is a versioned child of `rejected/COUNTERFACTUAL_QUERY_WRITE_UTILITY.md`. It repairs one precise failure by adding randomized external evidence. It does not repair retrospective source deletion, semantic truth identification, or long-run self-improvement.

## 1. Original failure, type, and retained result

The parent diagnostic computes a frozen-path leave-one-write-out contribution. For write-local parameters its exact utility gradient is ordinary future cross-entropy, and after contributions mix in a fixed aggregate state it cannot selectively release an old source without identity, traces, or replay.

Failure type: **information/estimand mismatch**, not an algebraic failure. Passive observation gives only the realized branch. A predictor trained from it cannot generally identify the counterfactual loss of not writing. The retained correct result is the query-visible transport formula and the passive-observation no-go for individual historical deletion.

Patch: at training/evaluation time, randomize among a finite set of fully specified, same-information Delta update actions and log the propensity. Judge each realized action by a delayed *real* future loss under a fixed continuation policy. This changes the information set; it is not a relabeling of the old estimator.

## 2. Formal object and information boundary

At decision time (i), let the causal history

\[
H_i=(x_{\le i},S_{i-1},h^{\rm upd}_{i-1},k_i,v_i)
\]

contain only the visible prefix, current full memory and updater state. It excludes future tokens, answers, old-fact-validity oracles, ideal edits and future model judgments.

Let \(\mathcal A\) be finite. Each \(a\in\mathcal A\) is a complete coupled-state map \(F_a:H_i\mapsto Z_i^a=(S_i^a,h_i^{\rm upd,a},\ldots)\), with \(S_i^a\in\mathbb R^{d_k\times d_v}\). In the binary control the non-memory components are unchanged at intervention time:

\[
S_i^0=\bar S_i=D_iS_{i-1},\qquad
S_i^1=\bar S_i+\beta_i k_i e_i^\top,
\quad e_i=v_i-\bar S_i^\top k_i,
\qquad
Z_i^a=F_a(H_i)=(S_i^a,h_{i-1}^{\rm upd},\ldots).
\]

All later coupled variables evolve under the common continuation policy \(\kappa\).

Protected, ridge or learned updates may be additional actions only if they use the same visible information and total resource accounting. Draw

\[
A_i\sim \mu_i(\cdot\mid H_i),\qquad
\mu_i(a\mid H_i)\ge\epsilon>0,
\]

and log the exact propensity. After the intervention, use one fixed continuation policy \(\kappa\) for \(H\) steps. The potential delayed loss is

\[
Y_i^a=\sum_{h=1}^{H}w_h\,\ell_{i+h}^{(a,\kappa)}.
\]

Lower is better. The object is the total action effect, including action-induced future keys, queries, gates, memories and updater states under \(\kappa\). It is not a frozen-Jacobian direct path and not the value of deleting a historical source.

## 3. Identification and computable estimator

Assume: (i) consistency \(Y_i=Y_i^{A_i}\); (ii) designed conditional randomization \(A_i\perp\{Y_i^a\}_{a\in\mathcal A}\mid H_i\); (iii) positivity; (iv) a well-defined common continuation policy and horizon; and (v) reset/disjoint experimental units, or a correctly specified sequential martingale treatment of a persistent stream.

For the displayed finite-sample conditional-unbiasedness identities, nuisance predictions are fixed independently of the evaluated outcome, obtained by sample splitting/cross-fitting, or—in an adaptive stream—predictable from the pre-action filtration. This condition covers \(\widehat m_a\), any estimated censoring law \(\widehat c_a\), and sequential \(\widehat Q_t,\widehat V_t\). A target policy learned from the same log must likewise be evaluated on held-out/cross-fitted units or by an otherwise valid adaptive-policy evaluation argument.

Define

\[
m_a(H)=\mathbb E[Y\mid H,A=a],\qquad
\psi_a=\widehat m_a(H)+
\frac{\mathbf 1\{A=a\}}{\mu_a(H)}
\bigl(Y-\widehat m_a(H)\bigr).
\]

Because the propensity is known from the randomizer,

\[
\begin{aligned}
\mathbb E[\psi_a\mid H]
&=\widehat m_a(H)+
\frac{\Pr(A=a\mid H)}{\mu_a(H)}
\{m_a(H)-\widehat m_a(H)\}\\
&=m_a(H)=\mathbb E[Y^a\mid H].
\end{aligned}
\]

For binary actions, the AIPW loss-effect pseudo-outcome is

\[
\Gamma=\widehat m_1(H)-\widehat m_0(H)
+\frac{A}{p(H)}\{Y-\widehat m_1(H)\}
-\frac{1-A}{1-p(H)}\{Y-\widehat m_0(H)\},
\]

so \(\mathbb E[\Gamma\mid H]=m_1(H)-m_0(H)\). Cross-fitted estimates may train a future *frozen* action policy. With known propensity, unbiasedness of the population action value does not require a correct outcome model; calling an estimated-propensity version exactly unbiased would be wrong.

If at analysis time only \(R=\mathbf 1\{D\le C\}\) outcomes have arrived, let \(c_a(H)=\Pr(R=1\mid H,A=a)\). Under conditional independent censoring and positivity,

\[
\psi_a^D=\widehat m_a(H)+
\frac{\mathbf 1\{A=a\}R}{\mu_a(H)c_a(H)}
\{Y-\widehat m_a(H)\}.
\]

Correct \((\mu,c)\) makes this unbiased for any outcome model; a correct outcome model also kills the augmentation mean under delay-MAR. Outcome-dependent unobserved delay is not identified. Waiting for all finite-delay outcomes avoids the censoring model.

## 4. Overlap, variance, horizon and sequential scope

For independent/reset one-decision units with complete outcomes and binary actions, write \(\sigma_a^2(H)=\operatorname{Var}(Y^a\mid H)\). The efficient-influence variance is

\[
\operatorname{Var}\{m_1(H)-m_0(H)\}
+\mathbb E\left[\frac{\sigma_1^2(H)}{p(H)}+
\frac{\sigma_0^2(H)}{1-p(H)}\right].
\]

With independent censoring the residual denominators become \(pc_1\) and \((1-p)c_0\). This i.i.d. expression is not the variance of an overlapping persistent stream: there one needs a valid martingale/dependence analysis, predictable quadratic variation and any cross-window covariance terms. In either case rare write/no-write arms or late outcomes can make the estimator unusably noisy. Randomization creates evidence but spends samples and deliberately takes some inferior actions.

The one-decision result is valid when only \(A_i\) is intervened and the same mapping \(\kappa\) governs every later action, even though future histories depend on \(A_i\). If a different target policy \(\pi\) is evaluated later, one-step AIPW is invalid. Sequential DR instead uses

\[
\rho_{i:t}=\prod_{s=i}^{t}\frac{\pi_s(A_s\mid H_s)}{\mu_s(A_s\mid H_s)}
\]

Define the target-policy loss functions

\[
Q_t^\pi(h,a)=\mathbb E_\pi\!\left[\sum_{s=t}^{T}\gamma^{s-t}L_s\mid H_t=h,A_t=a\right],
\qquad
V_t^\pi(h)=\sum_a\pi_t(a\mid h)Q_t^\pi(h,a),
\]

with \(V_{T+1}=0\). The sequential DR estimator is

\[
\widehat V_{{\rm DR},i}^{\pi}
=\widehat V_i(H_i)+
\sum_{t=i}^{T}\gamma^{t-i}\rho_{i:t}
\{L_t+\gamma\widehat V_{t+1}(H_{t+1})-
\widehat Q_t(H_t,A_t)\}.
\]

It additionally requires sequential exchangeability and positivity at every target-reachable history. Correct behavior ratios give unbiasedness for arbitrary fixed, cross-fitted or pre-action-predictable \(\widehat Q\); exact target \(Q,V\) makes each temporal-difference residual conditionally mean-zero for predictable weights, subject to the usual support and integrability conditions. Product ratios can have exponential horizon variance. When \(\pi_{s>i}=\mu_{s>i}=\kappa\) pointwise, later factors are one and only the initial intervention ratio remains, which is the precise reduction to initial-action AIPW.

A finite \(H\) defines a finite-horizon estimand and is not itself biased. It does not prove long-run benefit. For the convention \(\sum_{h=1}^{\infty}\gamma^{h-1}\ell_{i+h}\), if \(|\ell|\le L\), the worst-case action-effect tail after \(H\) is at most

\[
\frac{2L\gamma^{H}}{1-\gamma}.
\]

Without discounting or a full coupled-state tail condition, two worlds can agree through \(H\) and reverse at \(H+1\). Contraction of \(S\) alone is insufficient.

## 5. Old counterexample recheck and new falsifiers

The parent no-go survives for retrospective source credit: randomized units identify population action values, not the sign of an unobserved counterfactual for one historical write, and they do not reconstruct a mixed source.

Concrete boundaries:

1. **No overlap.** If \(p(H)=1\), two worlds can share all observed \(Y^1\) and choose arbitrary \(Y^0\).
2. **No individual sign.** Two populations can have the same randomized marginals of \(Y^1,Y^0\) but different within-unit pairings and therefore different individual effect signs.
3. **Post-action mediation.** If a later update \(B=f(A)\), the contrast is the total effect through \(B\); a controlled direct effect needs another intervention and overlap.
4. **Persistent interference.** Treating every overlapping token write as an i.i.d. row violates the unit assumption. Use reset episodes/windows or a fully specified sequential regime with dependence-aware inference.
5. **Informative delay.** If missingness depends on unobserved potential loss, IPCW/AIPW does not identify the target without extra assumptions or observables.
6. **Noncompliance.** Random assignment \(Z\) with a different executed action identifies intention-to-treat, not the action effect absent instrumental-variable assumptions.
7. **Horizon reversal.** Equal losses through \(H\) and opposite loss at \(H+1\) falsify any unqualified long-run claim.

## 6. What this can and cannot establish

| Claim level | Evidence required | Status of this construction |
|---|---|---|
| Training-time causal value of a finite update action | randomized logged actions, real delayed outcomes, overlap | identified under the stated assumptions |
| Learned frozen update policy | held-out/interventional action value versus same-information controls | possible; not measured |
| Deployment-time memory adaptation | execute the frozen policy on causal inputs | recurrence may adapt; policy itself is not improving |
| Deployment-time updater improvement | continued external feedback plus legal online policy update and sequential evaluation | not supplied by this artifact |
| Cross-new-task learning efficiency / RSI | native new-task evidence at matched state, compute and feedback | not established |
| Retrospective source release or semantic truth | identity/trace/replay or additional validity evidence | not identified |

The strongest same-information controls are randomized difference in means, direct outcome regression/future CE, IPS/SNIPS, AIPW/DR, SWITCH, a generic contextual-bandit policy learner, sequential DR for changed continuations, delayed supervision/direct action prediction, and—where lawful—a training-only paired twin-state replay on an identical exogenous suffix. Fixed Delta and no-write remain endpoints.

## 7. Costs and native measurement gaps

The construction needs logged action propensities, real delayed outcomes and enough samples in every action/context region. The action set, outcome model and exploration all consume budget; sequential ratios and long delays magnify variance. Exact paired cloning avoids propensity variance but costs at least two forward branches and is only causal when the suffix is exogenous or replayable.

LongMemEval contains knowledge-update cases and timestamped histories, so it can measure final QA behavior. It does not natively provide randomized Delta-action propensities, repeated potential outcomes or an internal update-credit scorer; its official judge also uses an external model service. bAbI and LAMBADA likewise measure endpoint behavior, not this causal mechanism. Therefore native mechanism measurement remains open; no benchmark, label, metric or result is invented here.

## 8. Distinctness and disposition

This repair is mathematically different from passive source attribution because it adds a randomized intervention. The identification machinery itself is established contextual-bandit AIPW/DR and sequential off-policy evaluation. SEAL also evaluates candidate self-edits through downstream post-update performance, though with a different parameter/LoRA mechanism and without this particular randomized Delta-action logging protocol.

What remains Delta-specific is only the finite action interface \(F_a\) and the separation between total nonlinear action effect and frozen-path write attribution. There is no proved Delta-specific variance, sample, state or compute advantage over generic DR/direct regression, no repaired source deletion, and no native empirical evidence. Consequently R02 v1 is retained as a **causal logging/training/evaluation control**, contributes zero active candidates, and should be reopened only if a rank-one Delta structure yields a provably cheaper estimator or a lawful exact paired-branch construction at matched total resources.

No project code, tests, model execution, benchmark scoring, training, inference, data/model download, GPU work or Docker was used.
