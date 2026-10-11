# R14 v2 — credal provenance write, exact minimax action and misspecification regret

Lineage parent: `repairs/R14_POSTERIOR_PROVENANCE_WRITE.v1.md`. Substantive attempt 2 of at most 3. This is a mathematics/source review artifact; no project code or experiment was executed.

## 1. Original problem, concrete patch and scope

R14 v1 correctly solved a declared local quadratic decision when a single causal identity posterior is known. Its unresolved assumption is consequential: the deployed router supplies an estimate, not the oracle `p=P(J=1|F_t)`. Ordinary marginal calibration does not imply that every token-level posterior is correct, and a shifted router can make the v1 action confidently harmful.

The v2 patch replaces the supplied point posterior by an externally certified set

\[
  p_t=\Pr(J=1\mid\mathcal F_t)\in[\ell_t,u_t],
  \qquad 0\leq\ell_t\leq u_t\leq1,                 \tag{1}
\]

where both endpoints are measurable before the write. The certificate may come from a separately justified conditional-coverage, conformal, Bayesian or distributionally robust procedure. This artifact does **not** manufacture that certificate from the Delta residual and does not treat a future identity label as deployment information.

The theorem below is deliberately narrow: two existing slots, a unique latent identity, scalar common normalized residual, symmetric positive wrong-slot cost, and one local step. It is not a theorem about open-world identities, distributed facts, unknown future curvature or repeated nonlinear self-modification.

## 2. Formal object and fixed-posterior Bayes action

Normalize the common written-key residual to one. Let `a_i` be the amount written to slot `i`, and let `lambda>0` be the cost of changing the wrong slot. In identity world `J=1` or `J=2`, respectively,

\[
L_1(a)=(1-a_1)^2+\lambda a_2^2,
\qquad
L_2(a)=(1-a_2)^2+\lambda a_1^2.                   \tag{2}
\]

At posterior `p`, the conditional risk is

\[
\begin{aligned}
R_p(a)
&=pL_1(a)+(1-p)L_2(a)\\
&=1-2\{pa_1+(1-p)a_2\}+h_1(p)a_1^2+h_2(p)a_2^2, \tag{3}\\
h_1(p)&=\lambda+(1-\lambda)p,\qquad
h_2(p)=1+(\lambda-1)p.
\end{aligned}
\]

Because `h_i(p)>=min(1,lambda)>0`, (3) is strictly convex. Its unique Bayes action and risk are

\[
a_1^\star(p)={p\over h_1(p)},\qquad
a_2^\star(p)={1-p\over h_2(p)},                  \tag{4}
\]

\[
R^\star(p)
=1-{p^2\over h_1(p)}-{(1-p)^2\over h_2(p)}
={\lambda p(1-p)\over h_1(p)}
+{\lambda p(1-p)\over h_2(p)}.                  \tag{5}
\]

These are the two-slot specialization of v1, but v2 no longer assumes the argument `p` is known exactly.

## 3. Exact minimax action for an interval posterior

Consider the robust decision

\[
\min_{a\in\mathbb R^2}\max_{p\in[\ell,u]}R_p(a). \tag{6}
\]

For each fixed `a`, `R_p(a)` is affine in `p`, so its maximum is attained at an endpoint. For each `p`, it is uniformly coercive in `a`:

\[
R_p(a)\geq \min(1,\lambda)\lVert a\rVert_2^2
-2(|a_1|+|a_2|)+1.                              \tag{7}
\]

Hence a minimizer exists; minimax exchange follows either by restricting to a compact sublevel set and applying the convex--concave minimax theorem, or directly from the epigraph KKT system for `R_ell(a)<=t` and `R_u(a)<=t`.

The Bayes envelope `R^*(p)=inf_a R_p(a)` is concave because it is an infimum of affine functions of `p`. It is symmetric under `p -> 1-p`, hence it is nondecreasing on `[0,1/2]` and nonincreasing on `[1/2,1]`. Define the least-favourable posterior

\[
\widehat p=\operatorname{Proj}_{[\ell,u]}(1/2)
=\begin{cases}
u,&u<1/2,\\
1/2,&\ell\leq1/2\leq u,\\
\ell,&\ell>1/2.
\end{cases}                                      \tag{8}
\]

Then the exact saddle result is

\[
\boxed{
\min_a\max_{p\in[\ell,u]}R_p(a)=R^\star(\widehat p),
\qquad a^{\rm rob}=a^\star(\widehat p).}
                                                            \tag{9}
\]

A direct saddle check prevents a common overstatement. If the interval lies to the right of `1/2`, the envelope slope at `ell` is nonpositive, so the affine risk of `a^*(ell)` is worst at `ell`; the left-side case is symmetric. If the interval crosses `1/2`, then `a_1=a_2=1/(1+lambda)` and its risk is constant in `p`. Thus (9) is not merely a lower bound obtained by swapping min and max.

The operational rule is simple: clamp `1/2` to the posterior interval and apply the v1 shrinkage at that least-favourable point. When `[ell,u]=[0,1]`, the action is symmetric rather than magical:

\[
a_1^{\rm rob}=a_2^{\rm rob}={1\over1+\lambda},\qquad
R_{\rm rob}={\lambda\over1+\lambda}.             \tag{10}
\]

This robustifies the local decision but does not identify `J`.

## 4. Exact cost of posterior misspecification

Suppose the true posterior is `p` but an updater executes the point-posterior action `a^*(q)`. Completing the two squares gives the exact excess risk

\[
R_p(a^\star(q))-R^\star(p)
=h_1(p)[a_1^\star(q)-a_1^\star(p)]^2
+h_2(p)[a_2^\star(q)-a_2^\star(p)]^2.            \tag{11}
\]

The action differences are

\[
a_1^\star(q)-a_1^\star(p)
={\lambda(q-p)\over h_1(q)h_1(p)},\qquad
a_2^\star(q)-a_2^\star(p)
=-{\lambda(q-p)\over h_2(q)h_2(p)},              \tag{12}
\]

so

\[
\boxed{
R_p(a^\star(q))-R^\star(p)
=\lambda^2(p-q)^2
\left[
{1\over h_1(p)h_1(q)^2}
+{1\over h_2(p)h_2(q)^2}
\right].}                                        \tag{13}
\]

Equation (13) is a model-internal diagnostic, not a universal calibration guarantee. It is locally quadratic in posterior error, but its coefficient can be large near the `O(1/lambda)` boundary layer when wrong-slot cost is extreme. If the interval misses the true posterior, (9) gives no real-world protection. For example, with `lambda=1`, true `p=0.1` and asserted interval `[0.9,1]`, the rule uses `q=0.9`, incurs regret `1.28`, and is worse than no-write risk `1`.

## 5. Hard one-touch control and abstention

Continuous robust shrinkage does not generally abstain. To obtain an exact abstention rule, explicitly change the action class to at most one full slot write:

\[
\mathcal A_{\rm hard}=\{(0,0),(1,0),(0,1)\}.     \tag{14}
\]

The interval worst-case risks are

\[
1,\qquad (1-\ell)(1+\lambda),\qquad u(1+\lambda). \tag{15}
\]

Therefore the robust hard controller chooses their minimum. Equivalently, slot 1 is optimal when

\[
\ell\geq{\lambda\over1+\lambda},\qquad \ell+u\geq1,
\]

slot 2 is optimal when

\[
u\leq{1\over1+\lambda},\qquad \ell+u\leq1,
\]

and no-write is optimal when

\[
\ell\leq{\lambda\over1+\lambda},\qquad
u\geq{1\over1+\lambda},                          \tag{16}
\]

with ties on boundaries. The one-touch budget is essential: if `(1,1)` is allowed, its risk `lambda` must also enter (15) and dominates no-write when `lambda<1`.

## 6. Multi-slot credal extension and its exact limit

For `m` slots, unique identity `J=j`, and loss

\[
L_j(a)=(1-a_j)^2+\sum_{i\ne j}\lambda_{ji}a_i^2,
\]

let `pi` range over a compact convex credal set `Pi` in the probability simplex. Then

\[
R_\pi(a)=1-2\sum_i\pi_i a_i+\sum_i h_i(\pi)a_i^2,
\quad
h_i(\pi)=\pi_i+\sum_{j\ne i}\pi_j\lambda_{ji}.   \tag{17}
\]

Under the explicit uniform-curvature condition

\[
\inf_{\pi\in\Pi,\,i} h_i(\pi)>0,
\]

the fixed-`pi` Bayes actions and the robust value are

\[
a_i^\star(\pi)={\pi_i\over h_i(\pi)},\qquad
R^\star(\pi)=1-\sum_i{\pi_i^2\over h_i(\pi)},    \tag{18}
\]

\[
\min_a\max_{\pi\in\Pi}R_\pi(a)
=\max_{\pi\in\Pi}R^\star(\pi).                 \tag{19}
\]

If `Pi` is a polytope, the primal epigraph has one convex quadratic constraint per extreme posterior; it is a convex QCQP, not necessarily a linear QP. The least-favourable posterior can be an **interior mixture of active vertices**. It is wrong to maximize (18) only over vertices; the two-slot interval crossing `1/2` is already a counterexample. In the symmetric common-`lambda` full simplex, symmetry gives the uniform least-favourable posterior and

\[
a_i^{\rm rob}={1\over1+\lambda(m-1)},\qquad
R_{\rm rob}={\lambda(m-1)\over1+\lambda(m-1)}.   \tag{20}
\]

This is a generic credal Bayes decision over routed slots. It is not a new Delta recurrence.

## 7. Old counterexamples and new failure boundaries

- **Identity ambiguity remains.** Two worlds with the same `F_t` can require different slots. A wider posterior set changes the safe action; it does not create missing evidence.
- **Certificate validity is external.** Marginal calibration is not tokenwise conditional coverage. All robust claims are conditional on the true `p` lying in `[ell,u]` under deployment shift.
- **Identity must be operational.** The theorem assumes one unique slot is correct and that this identity determines (2). Duplicated, complementary or distributed facts need a different latent/action model.
- **Open-world support is absent.** If `J=empty` has positive probability, renormalizing over two old slots forces corruption. A new-slot action changes capacity and is not silently included.
- **Only posterior uncertainty is robustified.** Wrong `lambda`, wrong residual, signed linear protection terms, cross-slot Hessian terms or wrong future propagation can make the action arbitrarily poor.
- **Single-step only.** Local minimax risk does not imply time consistency, stable repeated updates or improved future learning. Endogenous gates/queries require the full joint Jacobian or an empirical test.
- **Extreme costs.** For a fixed nondegenerate posterior `0<p<1`, as `lambda->0` wrong writes are free and both continuous writes approach one; exact endpoint posteriors keep the impossible slot at zero, and at `lambda=0` uniform coercivity and uniqueness fail. As `lambda->infinity`, every non-certain posterior approaches no-write risk, while exact endpoint identity still permits a full write.

## 8. Information, state, compute and strong controls

The robust action needs the same slot residuals and cost model as v1 plus a certified interval or credal-set description. The certificate generator has its own labels, samples, calibration state and shift assumptions; none is free. Two slots add only constant decision work. For `m` slots and a polytope with `K` extreme posteriors, an exact generic controller solves a convex epigraph QCQP with `K` quadratic constraints; special symmetry yields closed form.

Strong same-information controls are:

1. the direct minimax per-slot router solving (6) or (19) — algebraically identical to this repair;
2. the hard one-touch router using (15), plus no-write;
3. a direct action/loss predictor using the same `F_t` and budget, which need not predict provenance;
4. robust optimization over the full uncertain quadratic coefficients `(b,H)`, rather than only `p`;
5. an explicit event/version ledger when provenance metadata is genuinely available.

Active evidence acquisition and new-slot allocation are informative adjacent controls, but they change the information/state budget and are not counted as R14 v2.

## 9. Distinguishing predictions and measurement gap

Conditional on a valid certificate and the local model, v2 predicts:

1. intervals crossing `1/2` induce the symmetric minimax action (10), regardless of the point estimate;
2. intervals wholly on one side use the endpoint closest to `1/2`, not the midpoint;
3. posterior misspecification loss follows the exact quadratic law (13);
4. the hard one-touch rule develops the abstention region (16), while continuous robust shrinkage generally does not;
5. an invalid confident interval can be worse than no-write, as the explicit `p=0.1`, `[0.9,1]`, `lambda=1` counterexample shows.

Existing bAbI, LAMBADA, RULER and LongMemEval assets score end-to-end answers or language loss, but do not expose the correct internal slot, tokenwise posterior coverage, wrong-slot potential outcomes or counterfactual loss for every action. Model-edit datasets can measure efficacy/locality after a prescribed edit, yet do not natively identify the pre-action provenance posterior or its interval. Therefore the theorem's key mechanism presently has a measurement gap; no labels, cases, metric or result are invented here.

## 10. Contribution and disposition

The patch is mathematically successful: it removes v1's exact-point-posterior assumption, yields an exact minimax write, quantifies misspecification regret, and separates continuous shrinkage from hard abstention. It also produces useful debugging boundaries for invalid certificates, open-world identities and multi-slot credal sets.

The contribution does **not** establish a new updater. Credal/robust Bayes and distributionally robust optimization already prescribe worst-case expected loss over a set of plausible laws; posterior-based decision regret and robust minimax regret are established; and the strongest implementation is the direct minimax router itself. Delta contributes the concrete slot-write interpretation, not a distinct optimization mechanism.

Status after substantive attempt 2: conditional mathematics accepted; contribution difference insufficient for a candidate; native measurement unclosed; empirical effect unknown. Park R14 with candidate delta 0. Reopen only if a prefix-measurable natural certificate has demonstrated deployment coverage at matched cost, Delta structure provides a strict computational/statistical advantage over the direct robust router, or a public native task exposes provenance and action-level consequences.

