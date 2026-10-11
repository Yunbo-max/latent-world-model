# R14 v3 — observable-equivalence closure for provenance certificates

Lineage parents: `repairs/R14_POSTERIOR_PROVENANCE_WRITE.v1.md` and `repairs/R14_CREDAL_PROVENANCE_WRITE.v2.md`. Substantive attempt 3 of 3. This is a mathematics/source review artifact; no project code or experiment was executed.

## 1. Original problem and concrete patch

V1 derives the exact local Bayes write when a causal provenance posterior is supplied. V2 replaces a potentially wrong point posterior by a valid prefix-measurable interval and derives its exact minimax write. The remaining gap is earlier than both optimizations: can the existing causal record support a nontrivial valid interval at all?

The v3 patch models the **whole observable experiment**. Let `O` contain everything lawfully available before the write: visible prefix, current Delta states, current key/value, declared metadata, router/calibration state, protection summaries, retained calibration observations and any algorithmic random seed. Hidden identity is not included. Two worlds `theta in {1,2}` induce observable laws `Q_1,Q_2` on `O` but require different slots. Define

\[
  \delta=\operatorname{TV}(Q_1,Q_2)\in[0,1].                 \tag{1}
\]

The extreme identity targets are

\[
 p_1=\Pr_1(J=1\mid O)=1,\qquad p_2=\Pr_2(J=1\mid O)=0.     \tag{2}
\]

This is a legal subfamily of the open research problem: both worlds may generate nearly identical visible records while provenance differs. Any claimed universal updater or certificate must also handle this subfamily. Randomized algorithms are covered by adjoining an independent common random seed to `O`, which does not change (1).

## 2. Certificate-collapse lemma

Let a prefix-measurable procedure output an interval `C(O) subseteq [0,1]`. Require the same advertised coverage in both worlds,

\[
 Q_1\{1\in C(O)\}\ge 1-\alpha,
 \qquad
 Q_2\{0\in C(O)\}\ge 1-\alpha.                            \tag{3}
\]

For any event `A`, total variation gives `Q_1(A)>=Q_2(A)-delta`. Hence

\[
 Q_1\{0\in C\}\ge1-\alpha-\delta.
\]

Combining this with the first inequality in (3) and using the union bound,

\[
 Q_1\bigl\{\{0,1\}\subseteq C(O)\bigr\}
 \ge (1-2\alpha-\delta)_+.                                \tag{4}
\]

The symmetric argument gives the same lower bound under `Q_2`. Because `C(O)` is an interval contained in `[0,1]`, containing both endpoints means

\[
 \boxed{C(O)=[0,1]}
\]

on the event in (4). Thus exact observational equivalence (`delta=0`) plus high uniform coverage forces the uninformative full posterior interval with probability at least `1-2alpha`. In the special exact-equivalence case where `O` is the same single atom in both worlds and the certificate is deterministic, any `alpha<1` that demands coverage in both worlds forces `[0,1]` outright.

The same event bound gives, under either world,

\[
 \mathbb E_\theta[\operatorname{width} C(O)]
 \ge (1-2\alpha-\delta)_+.                         \tag{4a}
\]

The constant is sharp as a TV-only statement: an experiment may have common mass `1-delta` and disjoint identity-revealing mass `delta`; on the common symbol a randomized certificate can allocate its two miscoverage budgets and otherwise return `[0,1]`.

This lemma is narrower than a general conformal impossibility theorem and stronger for the declared binary witness: it needs no asymptotics or nonatomic covariate space. It says only that coverage cannot reveal a hidden distinction absent from the observable experiment.

## 3. Sharp decision-risk floor

Use the same normalized two-slot local losses as v2, for `lambda>0`:

\[
 L_1(a)=(1-a_1)^2+\lambda a_2^2,
 \qquad
 L_2(a)=(1-a_2)^2+\lambda a_1^2.                            \tag{5}
\]

Let `a(O)` be any measurable updater, including any nonlinear or randomized Delta controller using the declared observable record. Let `mu=Q_1\wedge Q_2` be the common submeasure, whose mass is

\[
 \mu(\Omega)=1-\operatorname{TV}(Q_1,Q_2)=1-\delta.         \tag{6}
\]

Nonnegativity of (5) gives

\[
\begin{aligned}
 {1\over2}\{\mathbb E_1L_1(a(O))+\mathbb E_2L_2(a(O))\}
 &\ge {1\over2}\int\{L_1(a(o))+L_2(a(o))\}\,d\mu(o).      \tag{7}
\end{aligned}
\]

For every fixed action,

\[
 {L_1(a)+L_2(a)\over2}
 ={(1-a_1)^2+(1-a_2)^2+\lambda(a_1^2+a_2^2)\over2}
 \ge {\lambda\over1+\lambda},                              \tag{8}
\]

with equality only at `a_1=a_2=1/(1+lambda)`. Combining (6)--(8),

\[
 \boxed{
 \inf_a\max_{\theta\in\{1,2\}}\mathbb E_\theta
 L_\theta(a(O))
 \ge (1-\delta){\lambda\over1+\lambda}.}                  \tag{9}
\]

Equation (9) is a Le-Cam-style lower bound specialized to the Delta slot loss. It applies to the full updater, not merely to a procedure that commits to using its reported interval.

When `delta=0`, the constant action

\[
 a_1=a_2={1\over1+\lambda}                                 \tag{10}
\]

attains equality in both worlds, so

\[
 \min_a\max\{L_1(a),L_2(a)\}={\lambda\over1+\lambda}.     \tag{11}
\]

This is exactly the v2 continuous robust action for `C=[0,1]`. The identity oracle has zero loss, so (11) is the exact price of the missing distinction. Randomization cannot improve it **within the convex continuous action class**: conditional averaging of an action does not increase either convex quadratic loss.

For a constant deterministic hard one-touch action from `{(0,0),(1,0),(0,1)}`, the corresponding worst-case losses under exact equivalence are `1,1+lambda,1+lambda`; no-write is minimax among those three constant actions. If randomized hard actions are admitted—or an identically distributed nuisance coordinate in `O` is used to implement the same mixture—the action class is nonconvex and mixing can help when `lambda<1`: the exact minimax value becomes

\[
 \min\left\{1,{1+\lambda\over2}\right\},                 \tag{11a}
\]

attained either by no-write or by an equal lottery over the two full writes. Thus the prior v2 distinction between continuous shrinkage and hard abstention is not cosmetic, and a blanket “randomization never helps” statement would be false outside the convex continuous class.

## 4. Why a derived Delta statistic cannot escape

For any measurable statistic `T=T(O)`—residual, gradient, hidden state, tensor tag, uncertainty score or learned router output—the data-processing inequality gives

\[
 \operatorname{TV}(Q_1\circ T^{-1},Q_2\circ T^{-1})
 \le \operatorname{TV}(Q_1,Q_2)=\delta.                    \tag{12}
\]

Therefore a deterministic repackaging of the same record cannot increase the distinguishability used in (4) or reduce the lower bound by creating evidence. A statistic can still improve computation or approximate an already-identifiable likelihood ratio; it cannot turn observational equivalence into provenance information.

An added timestamp, entity identifier, external correction signal, delayed label or active query changes the observable experiment and may increase total variation. That can legitimately lower (9), but the extra channel, calibration assumptions, state, latency and labels must be given to the direct Bayes/minimax router as well. If evidence laws remain equal conditional on the existing record, no value is added. If they separate, the best same-information action is still the direct Bayes decision from v1; Delta geometry alone is not the source of identification.

## 5. Old counterexamples and failure boundaries

- **V1 preserved.** Given a valid point posterior and declared quadratic loss, its per-slot Bayes normal equations remain correct.
- **V2 preserved.** Given a valid posterior set, its least-favourable-posterior action and misspecification identity remain correct. V3 evaluates when that set must be uninformative.
- **Invalid certificates remain dangerous.** The v2 `p=0.1`, asserted `[0.9,1]`, `lambda=1` counterexample is untouched.
- **The bound is a subfamily lower bound, not universal pessimism.** If `delta` is large because lawful evidence distinguishes the worlds, (9) weakens. At `delta=1` it is vacuous.
- **Total variation is not a complete performance formula.** For `0<delta<1`, (9) is a lower bound; equality needs additional structure on the overlapping and distinguishable parts.
- **The TV lower bound is nevertheless sharp over experiments.** A common observation of mass `1-delta` plus disjoint identity-revealing observations of mass `delta` attains (9) by using (10) on the common part and the oracle action on the disjoint part.
- **Closed-world identity remains explicit.** A genuinely new/absent identity, duplicated fact or distributed fact requires a larger latent/action model.
- **Local loss remains explicit.** Wrong residual, interference cost, Hessian or future Jacobian can invalidate the action prescription; v3 does not robustify them.
- **No semantic-validity claim.** The theorem distinguishes information from geometry. It does not decide whether a fact is true, current or useful.

## 6. Information, state, compute and same-information controls

The theorem charges all retained calibration data and router state inside `O`; hiding them outside the comparison would make (1) meaningless. Computing the exact total variation between rich generative worlds is generally intractable, so `delta` is a theoretical identifiability parameter, not a deployment score. Any empirical surrogate requires its own assumptions and labels.

Strong controls are:

1. the direct v1 Bayes router using the same posterior/evidence;
2. the direct v2 minimax router using the same certified set;
3. no-write and hard one-touch routing;
4. an explicit event/version ledger when identifiers exist;
5. a likelihood-ratio or direct action predictor using exactly the same `O`;
6. an information-acquisition policy under the same labels, latency and compute.

No Delta-specific implementation can beat (9) on the declared two-world observable experiment. A later computational claim would have to show a matched-total-cost advantage in approximating the same decision, not relabel missing information as memory geometry.

## 7. Distinguishing predictions and native measurement gap

The result predicts:

1. as observable laws approach each other, uniformly valid provenance intervals must frequently include both endpoints;
2. the conditional average loss on the common observable mass is at least `lambda/(1+lambda)`, yielding the global lower bound (9);
3. at exact equivalence, the v2 symmetric continuous write is minimax and a deterministic hard full-write/no-write controller abstains (while randomized hard policies obey the separate boundary (11a));
4. any reported gain from a new statistic must trace to new information, a distributional assumption, or a different loss/action budget.

Existing bAbI, LAMBADA, RULER and LongMemEval endpoints do not natively provide paired observationally identical worlds with opposite internal slot identity, calibrated tokenwise provenance intervals, or all counterfactual write losses. Model-edit datasets prescribe an edit and measure efficacy/locality, but do not expose the pre-action hidden identity experiment in (1). They can test end behavior after a chosen method is implemented; they cannot natively identify this mechanism or estimate its sharp counterfactual floor. No benchmark, label, case, metric or result is invented here.

## 8. Contribution and terminal disposition

Attempt 3 supplies a real repair result: v2's external-certificate gap is converted into a finite binary coverage-collapse lemma, and the same observable overlap yields a sharp Delta-slot minimax lower bound. It proves exactly when the full credal interval and its symmetric action are forced, and it records the lawful escape route—change the observable experiment or assumptions.

The result is not a new updater. Conditional-coverage impossibility, two-point/Le-Cam lower bounds, data processing and minimax Bayes decisions are established theory; the contribution is their exact R14 specialization and closure of an otherwise implicit oracle gap. The strongest implementation is the already-known direct minimax router.

Final status after attempt 3 of 3: scoped mathematics retained; mechanism novelty insufficient; native mechanism measurement absent; empirical effect unknown; candidate delta 0. Park R14 with the repair budget exhausted. Reopen only if new lawful evidence or assumptions change `Q_1,Q_2`, and a Delta-specific statistic or implementation then beats the same-information direct router under matched total cost.
