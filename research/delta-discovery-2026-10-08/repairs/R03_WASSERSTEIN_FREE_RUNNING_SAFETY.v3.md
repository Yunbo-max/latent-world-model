# R03 v3 — Wasserstein free-running safety certificate (final repair attempt)

Date: 2026-10-10  
Lineage parent: `R03_COUPLED_HORIZON_SAFETY.v2.md`  
Attempt: 3/3  
Contribution type: conditional theory/control  
Execution boundary: symbolic mathematics and source reading only.

## 1. Original problem, exact failure, and patch

R03 v2 correctly bounds coupled memory/updater trajectories when the write and no-write systems are driven by the same future exogenous path. The failed step is to interpret that pathwise bound as free-running safety when the write can change generated tokens, queries, retrieval, policy choices, environment responses, or delayed feedback. In that setting the two suffix laws differ, so a shared-suffix Jacobian/tube does not by itself bound the total distributional effect.

Failure type: **target/construction mismatch**. The patch replaces pathwise comparison by a perturbation bound between the full closed-loop laws. It preserves v1's exact Delta injection geometry and v2's requirement that every action-affected state be included, but uses a Wasserstein/Dobrushin coefficient to propagate probability-law differences.

## 2. Formal object and information boundary

For each horizon step `h=0,1,...`, let `(\mathsf X_h,d_h)` be a Polish metric state space. A state contains all variables needed to make the future closed loop Markov: Delta memory, updater state/statistics, decoder/query/policy state, environment/retrieval state, and pending feedback. Let `\nu_h^a` and `\nu_h^0` be the laws after action `a` and no-write `0`, respectively. Their transitions are Markov kernels

\[
\nu_{h+1}^a=\nu_h^a K_h^a,
\qquad
\nu_{h+1}^0=\nu_h^0 K_h^0.
\tag{1}
\]

The action is measurable with respect to the decision-time history `\mathcal F_t`. Future realized tokens, answers, protected-validity labels, and counterfactual suffixes are unavailable at deployment. Every numerical certificate below must therefore be available at `\mathcal F_t`, obtained either as a deterministic structural bound or from an independent predeployment calibration object `\mathcal D`. When calibration is used, coverage is an outer probability over `\mathcal D` (or an anytime joint-filtration event), not a conditional probability given the already observed `\mathcal F_t`. A retrospective plug-in value is only a diagnostic.

Assume finite first moments and, on an action-time declared coverage event, constants `\kappa_h,\varepsilon_h\ge0` satisfying

\[
W_{1,d_{h+1}}\!\left(K_h^0(x,\cdot),K_h^0(y,\cdot)\right)
\le \kappa_h d_h(x,y),
\tag{2}
\]

for all relevant `x,y`, and

\[
\sup_x W_{1,d_{h+1}}\!\left(K_h^a(x,\cdot),K_h^0(x,\cdot)\right)
\le \varepsilon_{a,h}.
\tag{3}
\]

Equation (2) is a Wasserstein contraction/Lipschitz coefficient for the complete reference closed loop. Equation (3) is a per-step forcing term for action-dependent policies or environments. If, after the initial write, both systems truly use the same kernel, then `\varepsilon_{a,h}=0`; sharing a code path while feeding different omitted hidden variables is not enough.

Define

\[
\delta_{a,h}=W_{1,d_h}(\nu_h^a,\nu_h^0).
\tag{4}
\]

## 3. Free-running distribution recurrence

Triangle inequality gives

\[
\begin{aligned}
\delta_{a,h+1}
&=W_1(\nu_h^aK_h^a,\nu_h^0K_h^0)\\
&\le W_1(\nu_h^aK_h^a,\nu_h^aK_h^0)
   +W_1(\nu_h^aK_h^0,\nu_h^0K_h^0)\\
&\le \varepsilon_{a,h}+\kappa_h\delta_{a,h}.
\end{aligned}
\tag{5}
\]

The first inequality uses a common intermediate law. The second uses convexity/integration of (3) for the first term and the kernel Lipschitz coefficient (2) for the second. No common future sample path is required.

For `h>j`, write

\[
P_{h:j}=\prod_{r=j}^{h-1}\kappa_r,
\qquad P_{j:j}=1.
\tag{6}
\]

Induction yields

\[
\boxed{
\delta_{a,h}
\le P_{h:0}\delta_{a,0}
+\sum_{j=0}^{h-1}P_{h:j+1}\varepsilon_{a,j}}
\tag{7}
\]

with an empty sum at `h=0`. This is the precise distribution-level replacement for v2's same-path gain product.

### 3.1 Delta-specific initial displacement

If the pre-action state is deterministic, the action changes only the memory block, and the state metric on such a memory-only displacement is upper-bounded by its Frobenius norm with factor `c_S`,

\[
d_0(x_0^a,x_0^0)\le c_S\|\Delta S_a\|_F,
\]

then post-decay Delta

\[
\Delta S_a=\alpha_a\beta k e^\top,
\qquad e=v-\bar S^\top k,
\tag{8}
\]

gives

\[
\delta_{a,0}=d_0(x_0^a,x_0^0)
\le c_S|\alpha_a\beta|\,\|k\|\,\|e\|.
\tag{9}
\]

Equality holds only when the chosen state metric is exactly the memory Frobenius distance and no other state is changed. If the action also changes updater statistics, routing, policy state, or feedback queues, those components must be included in `\delta_{a,0}`. Thus rank-one structure helps only at the injection boundary; it does not make the later law rank one.

## 4. From law distance to protected risk

Let `\ell_h:\mathsf X_h\to\mathbb R` be the actual protected loss at horizon `h`, including the state-generated query and target interface. Suppose it is `L_h`-Lipschitz in `d_h`. Kantorovich--Rubinstein duality gives

\[
\left|\mathbb E_{\nu_h^a}\ell_h-
\mathbb E_{\nu_h^0}\ell_h\right|
\le L_h\delta_{a,h}.
\tag{10}
\]

For nonnegative declared weights `w_h`, a sufficient finite-horizon bound on the increase of expected protected loss is therefore

\[
\begin{aligned}
\Delta R_{a,H}
&:=\sum_{h=0}^{H}w_h
\left(\mathbb E_{\nu_h^a}\ell_h-
\mathbb E_{\nu_h^0}\ell_h\right)\\
&\le \sum_{h=0}^{H}w_hL_h
\left(P_{h:0}\delta_{a,0}
+\sum_{j=0}^{h-1}P_{h:j+1}\varepsilon_{a,j}\right)
=:U_{a,H}^{W}.
\end{aligned}
\tag{11}
\]

This controls an expectation difference, not a realized-action maximum and not semantic validity. A bounded but discontinuous exact-match loss need not be Lipschitz in a hidden-state Euclidean metric; choosing a discrete metric makes (10) valid but can make the contraction coefficient useless. The metric/loss pair is part of the scientific claim and cannot be selected after seeing outcomes.

### 4.1 Homogeneous discounted corollary

If `\kappa_h\le\kappa<1`, `\varepsilon_{a,h}\le\varepsilon_a`, `L_h\le L`, and `w_h=\lambda^h` with `0\le\lambda<1`, then

\[
\delta_{a,h}\le \kappa^h\delta_{a,0}
+\varepsilon_a\frac{1-\kappa^h}{1-\kappa},
\tag{12}
\]

and

\[
U_{a,\infty}^{W}
\le L\left[
\frac{\delta_{a,0}}{1-\lambda\kappa}
+\frac{\varepsilon_a}{1-\kappa}
\left(\frac{1}{1-\lambda}-\frac{1}{1-\lambda\kappa}\right)
\right].
\tag{13}
\]

When `\varepsilon_a>0`, the **certificate envelope** in (12) approaches `\varepsilon_a/(1-\kappa)`, so its undiscounted infinite sum diverges. This is not a lower bound on the actual state-law gap: cancellations or loose one-step bounds may make the true gap smaller. The justified conclusion is that contraction alone cannot certify vanishing cumulative harm in the presence of persistent bounded forcing.

## 5. Safe logging feasibility after the patch

Suppose action-time simultaneous bounds are deterministic structural bounds, or are functions of an independent calibration object `\mathcal D` satisfying the uniform outer-coverage statement

\[
\Pr_{\mathcal D}\!\left\{
\Delta R_{a,H}(f)\le\bar U_{a,H}^{W}(f;\mathcal D)
\ \forall a,\ \forall f\in\mathcal H_t
\right\}\ge1-\delta,
\tag{14}
\]

where `\mathcal H_t` is the declared class of admissible decision histories. An alternative anytime construction may replace (14) by one simultaneous event over the joint online filtration. Writing a conditional probability given `\mathcal F_t` when both the true conditional risk and the already computed bound are `\mathcal F_t`-measurable would be degenerate and is not a valid coverage claim.

The same safe-design problem from R03 v1/v2 may use `\bar U^W`:

\[
\min_{\mu}\sum_a\frac{g_a}{\mu_a}
\quad\text{s.t.}\quad
\sum_a\mu_a=1,
\quad \mu_a\ge\epsilon_\mu,
\quad \sum_a\mu_a\bar U_{a,H}^{W}\le b_H.
\tag{15}
\]

For `K` actions and finite nonnegative costs, feasibility is equivalent to

\[
K\epsilon_\mu\le1,
\qquad
b_H\ge\epsilon_\mu\sum_a\bar U_{a,H}^{W}
+(1-K\epsilon_\mu)\min_a\bar U_{a,H}^{W}.
\tag{16}
\]

This is still a conditional expected-harm budget under the coverage event. If every sampled action must itself be safe, then every action with positive propensity must satisfy its own bound; positivity can make that impossible. The optimization is generic safe experimental design, not a new Delta algorithm.

## 6. Old counterexamples rechecked and new failure boundaries

1. **The v2 shared-suffix objection is repaired only under (1)--(3).** Different free-running suffix laws are now compared directly. If the declared state omits action-affected decoder/environment variables, however, `K_h^a` is not the true closed-loop kernel and the old objection returns.
2. **A local Jacobian is insufficient.** Equation (2) is uniform over the covered state set and distributions. A point derivative, bounded gate, or separate stability of memory/updater blocks does not certify it.
3. **Persistent forcing defeats this undiscounted certificate.** Even with `\kappa<1`, constant `\varepsilon>0` makes the upper envelope in (12) approach a nonzero plateau and makes its undiscounted cumulative bound infinite. It does not prove a positive lower bound on the true distance.
4. **Metric laundering is invalid.** Rescaling or learning a metric can shrink `\delta` while enlarging the loss Lipschitz constant. Only the product appearing in (10)--(11), with a predeclared metric and loss, has meaning.
5. **Semantic validity remains unidentified.** Two worlds may induce the same observable closed-loop law while disagreeing on whether an old fact is still true. No Wasserstein certificate creates the missing external evidence.
6. **High-dimensional estimation can be prohibitive.** Empirical Wasserstein distances have dimension-dependent rates without extra structure. Sliced/projected/entropic surrogates change the metric or introduce bias and require a new theorem; they cannot silently replace `W_1` in (5).
7. **Loose global constants can stop learning.** Neural policy/environment Lipschitz bounds may be so large that every nonbaseline action is forced to the propensity floor. This is safe-but-uninformative, not evidence of successful updating.
8. **Endpoint OPE and structural certificates answer different questions.** Sequential DR can estimate a total policy/action effect under its own overlap and nuisance conditions, but it does not provide a pre-action worst-case certificate. Conversely, (11) can be computed from structural bounds without identifying the actual treatment effect and can be very loose.

## 7. Computability, state, and information cost

The cheap part is the Delta injection bound (9), requiring the already available `k,e,alpha,beta`. The expensive part is certifying the complete closed-loop coefficients:

- known analytic component kernels can sometimes yield `\kappa_h` and `\varepsilon_{a,h}` by composition/coupling;
- generic neural policies, routing, retrieval, and environment responses require global or high-confidence local certificates over a forward-reachable set;
- empirical full-state `W_1` estimation is statistically and computationally costly in high dimension;
- exact action-dependent kernels can require a simulator or model unavailable at deployment;
- simultaneous coverage across actions and horizons adds calibration cost.

The stored online state of the recurrence itself is `O(1)` per action/horizon step once all constants are supplied, but the certificate-construction cost is not `O(1)`. No same-budget advantage over direct rollout, interval/Lipschitz propagation, robust-MDP planning, or sequential OPE has been proved.

Strong controls are: no-write; standard Delta; R03 v1/v2; full coupled rollout; generic Markov/Wasserstein perturbation bounds; bisimulation/robust-MDP value bounds; full Jacobian or interval-bound propagation; safe optimal design; and sequential DR/OPE under randomized finite actions.

## 8. Distinctive predictions and falsifiers

Conditional predictions:

1. With a common post-action kernel (`epsilon=0`), `kappa_h <= kappa < 1`, and a uniform protected-loss Lipschitz bound `L_h <= L`, the certified expected protected-loss envelope decays geometrically from the Delta injection scale. Without the uniform `L_h` bound, only the exact product `L_h P_{h:0} delta_0` is certified and it need not decay.
2. With persistent action-dependent forcing, the certified upper envelope approaches a plateau and its undiscounted budget eventually becomes noncertifiable even when every one-step map is contractive. An actual positive gap floor additionally requires tightness or a separate lower-bound assumption.
3. Increasing key/residual norm raises only the initial Delta term in this envelope; if the certified forcing terms dominate, reducing the write magnitude will not proportionally reduce the long-horizon certificate. This is an envelope prediction, not a claim about the exact effect without tightness.
4. If a same-information rollout or generic robust bound is tighter at equal total cost, the Delta specialization has no practical certificate advantage.

Falsifiers:

- any covered action/horizon whose measured expected loss gap exceeds a valid simultaneous `\bar U^W` falsifies the claimed constants/closure;
- inability to define an action-time closed Markov state or predeclare a loss-compatible metric blocks the certificate;
- `\kappa_h`/`\varepsilon_h` estimates that require realized future targets or counterfactual suffixes are leakage, not deployment certificates;
- failure to beat generic controls at matched information/state/compute removes the method claim even if the theorem remains correct.

## 9. Closest work and residual contribution

The core recurrence is established Markov perturbation mathematics. Rudolf--Schweizer give Wasserstein perturbation bounds for Markov chains under ergodicity and kernel discrepancy. Asadi--Misra--Littman derive geometric multi-step Wasserstein model-error accumulation and value bounds for Lipschitz model-based RL. Ferns--Panangaden--Precup relate Wasserstein/bisimulation metrics to MDP value differences. Neufeld--Sester give Wasserstein-ambiguity robust-versus-nonrobust MDP value bounds. These are stronger than a claim that (5)--(13) constitute a new generic safety mechanism.

Residual contribution: a narrow Delta audit specialization that connects (i) the rank-one immediate write norm, (ii) a full free-running law perturbation certificate, and (iii) the already known positivity-versus-harm feasibility boundary. This repairs the v2 scope error and supplies a useful theorem/control, but it does not establish novelty, a new architecture, a learned updater, or same-budget practical superiority.

## 10. Native measurement status

LongMemEval/LongMemEval-v2, SEAL continual editing, CITB/TRACE, bAbI, and LAMBADA expose endpoint accuracy/retention or task-level forgetting, not an action-time closed state metric, full transition-kernel discrepancy, simultaneous contraction certificate, protected-validity label, and paired counterfactual law. Existing tasks can test an endpoint consequence but do not natively identify the mechanism in (2)--(14). The measurement gap remains; no benchmark, label, scorer, or result is invented here.

## 11. Disposition

- Mathematical status: **conditionally correct** under the declared complete Markov state, finite first moments, simultaneous action-time bounds, and Lipschitz protected loss; pending independent review of these exact bytes.
- Contribution status: **Delta-specialized control/theorem; main mechanism covered by Markov perturbation, Lipschitz model-error, bisimulation, and robust-MDP work**.
- Measurement status: **gap**.
- Empirical status: **unknown; not executed**.
- Candidate delta: **0**.
- Lineage decision: **park after attempt 3/3**. Reopening requires a genuinely new scientific object outside this exhausted repair line, such as a native closed-loop certificate with a proved same-budget Delta-specific advantage; it cannot be another renaming of generic Wasserstein/robust-control machinery.

