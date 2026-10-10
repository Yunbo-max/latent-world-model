# R14 v1 — posterior provenance write and the identity-ambiguity floor

Lineage parent: `rejected/PROVENANCE_TENSOR_DELTA.md` (identity-oracle control). Substantive attempt 1 of at most 3. This artifact is mathematics/source review only; no project code or experiment was executed.

## 1. Original problem, exact patch and status vocabulary

The parent binds semantic key `k` to a supplied provenance code `c`. Its equations are correct, but the code already decides whether an observation revises an existing entity/version or belongs elsewhere. The proposed patch does not pretend that a Delta residual reveals identity. It replaces the oracle by a causal belief

\[
\pi_i=\Pr(J=i\mid\mathcal F_t),\qquad i=1,\ldots,m,
\]

where `J` is the latent identity/slot and `F_t` contains all causally observed decision variables, including the visible prefix, declared metadata, current `k,v`, slot state and any protection summary. A posterior is an input produced by a separately specified and calibrated likelihood/router; a current target is not silently reused as a ground-truth identity label.

The mathematical result below is exact for its declared local quadratic decision. Contribution difference and empirical effect are separate: the construction is not automatically novel, and no efficacy is known without execution.

## 2. Formal object and causal action class

Maintain `m` ordinary key-by-value Delta slots

\[
S_i\in\mathbb R^{d_k\times d_v},\quad y_i=S_i^\top k,\quad r_i=v-y_i,
\]

for an observed nonzero key `k` and target `v`. Restrict the current edit to the minimum-Frobenius rank-one action that changes the written-key readout by `a_i∈R^{d_v}`:

\[
\Delta S_i={k\over\lVert k\rVert^2}a_i^\top,
\qquad
(S_i+\Delta S_i)^\top k=y_i+a_i.
\]

Let `Λ_{i|j}⪰0` and `c_{i|j}∈R^{d_v}` be prefix-measurable quadratic and signed linear consequences of changing slot `i` in identity world `j`, and let `τ_i≥0` be a displacement regularizer. If it represents literal Frobenius edit energy, its coefficient includes the factor `1/||k||²` because `||ΔS_i||_F²=||a_i||²/||k||²`. A generic local protected-risk change has the form `2c_{i|j}^Ta_i+a_i^TΛ_{i|j}a_i`; omitting the signed term would control displacement, not the change in squared loss. One legal frozen-query contribution to its quadratic part is

\[
\Lambda_{i\mid j}={\mathbb E[(q^\top k)^2\mid\mathcal F_t,J=j]\over\lVert k\rVert^4}V_{i\mid j},
\qquad V_{i\mid j}\succeq0,
\]

because the edit changes a future read by `(q^T k/||k||²)a_i`. This interpretation is conditional: endogenous future queries require the complete state Jacobian or a separately justified bound.

For identity world `J=j`, declare the local loss

\[
L_j(a)=\lVert r_j-a_j\rVert^2
+\sum_i\left(2c_{i\mid j}^\top a_i+a_i^\top\Lambda_{i\mid j} a_i\right)
+\sum_i\tau_i\lVert a_i\rVert^2.
\]

Taking the conditional expectation gives the separable Bayes risk

\[
\bar c_i=\sum_j\pi_jc_{i\mid j},\qquad
\bar\Lambda_i=\sum_j\pi_j\Lambda_{i\mid j},
\]

\[
\mathcal R(a\mid\mathcal F_t)
=\sum_i\left[
\pi_i\lVert r_i-a_i\rVert^2
+2\bar c_i^\top a_i
+a_i^\top\bar\Lambda_i a_i
+\tau_i\lVert a_i\rVert^2
\right]. \tag{1}
\]

This is a local decision surrogate, not a claim that truth, long-horizon utility, or the posterior is natively observed.

## 3. Bayes-optimal posterior write

Define

\[
H_i=\pi_i I+\bar\Lambda_i+\tau_iI.
\]

When `H_i` is positive definite, differentiating (1) yields

\[
H_i a_i^\star=\pi_i r_i-\bar c_i,
\qquad
a_i^\star=H_i^{-1}(\pi_i r_i-\bar c_i). \tag{2}
\]

For singular `H_i`, the minimizers exist exactly when `π_i r_i-\bar c_i∈range(H_i)` and are `H_i^†(π_i r_i-\bar c_i)+z`, `z∈ker(H_i)`; the minimum-norm action sets `z=0`. If this range condition fails, the declared quadratic is unbounded below along a zero-curvature direction and is not a legal risk certificate.

The simpler wrong-slot-displacement model used below is the explicit special case `c_{i|j}=0`, `Λ_{i|i}=0`, and `Λ_{i|j}=Λ_i` for `j≠i`. Then `\barΛ_i=(1-π_i)Λ_i`. With scalar `Λ_i=λ_i I`,

\[
a_i^\star={\pi_i\over \pi_i+(1-\pi_i)\lambda_i+\tau_i}\,r_i. \tag{3}
\]

Thus a one-hot posterior and zero regularizer recover ordinary routed full-step Delta. Ambiguous identity yields confidence- and damage-dependent shrinkage; as wrong-slot damage diverges, non-certain slots abstain. This is the concrete repaired action.

The minimum risk can be written without hidden labels. Completing the square gives

\[
\mathcal R_{\min}
=\sum_i\left[
\pi_i\lVert r_i\rVert^2
-(\pi_i r_i-\bar c_i)^\top H_i^\dagger(\pi_i r_i-\bar c_i)
\right], \tag{4}
\]

under the range condition. Equation (4) separates unavoidable identity uncertainty from the loss reduced by the selected action.

## 4. Why a soft tensor tag is generally not this action

Reshape the tensor memory into the same slots and use the posterior itself as a dense address `u=k⊗π`. A normalized full-step lifted Delta write uses `β=1/(||k||²||π||²)` and shared residual

\[
\bar r=v-\sum_j\pi_jy_j.
\]

Its blockwise written-key displacements are

\[
a_i^{\rm tensor}={\pi_i\over\lVert\pi\rVert^2}\bar r. \tag{5}
\]

All slot actions in (5) share one residual direction and a fixed relative scale. Equation (2) instead depends on each slot residual and signed world-averaged consequence. With an arbitrary scalar gate, write `a_i^{tensor}=ηπ_i\bar r`; equality requires

\[
H_i\,\eta\pi_i\bar r=\pi_i r_i-\bar c_i
\quad\text{for every active }i, \tag{5a}
\]

which is not implied by posterior calibration. One scalar cannot in general create the independent `H_i^{-1}(π_ir_i-\bar c_i)` directions.

A minimal counterexample is `m=2`, scalar values, unit key, `y_1=y_2=0`, `v=1`, `π=(1/2,1/2)`, `Λ_1=Λ_2=1`, and `τ_i=0`. Equation (2) gives `a_1=a_2=1/2` and risk `1/2`. Normalized full-step tensor Delta gives `a_1=a_2=1` and risk `1`; no-write also has risk `1`. Therefore replacing a one-hot identity code by its posterior mean is not the Bayes repair.

## 5. Sharp two-world ambiguity floor

For two scalar slots with `y_1=y_2=0`, `v=1`, posterior `(p,1-p)`, wrong-slot damage `λ>0`, and zero regularizer, every measurable action `(a_1,a_2)` has conditional risk at least

\[
R_\star(p,\lambda)
={p\lambda(1-p)\over p+\lambda(1-p)}
+{(1-p)\lambda p\over (1-p)+\lambda p}. \tag{6}
\]

This follows by independently completing the two scalar squares and is attained by (3). For `0<p<1`, `R_*(p,λ)>0`: no deterministic or randomized internal update can simultaneously emulate the two identity-oracle actions under the same observable posterior and declared loss. Internal randomization cannot beat (6), because (1) is convex and Jensen's inequality maps a randomized action to its conditional mean without larger risk.

The bound is scoped. It vanishes when identity becomes certain, wrong-slot damage is zero, or a later observation changes the posterior. It does not prove that semantic identity is universally unknowable; it proves that a memory geometry cannot manufacture absent evidence.

For `m` observationally indistinguishable slots with `π_i=1/m`, common scalar wrong-slot damage `λ`, and common residual `r`, (3) gives

\[
a_i^\star={r\over1+(m-1)\lambda},\qquad
\mathcal R_{\min}={ (m-1)\lambda\over1+(m-1)\lambda}\lVert r\rVert^2. \tag{6a}
\]

An identity oracle has zero risk in this simplified loss, so (6a) is the exact ambiguity price. It approaches the no-write risk as either the number of indistinguishable slots or wrong-slot damage grows.

If at most one slot may be fully written, the three simple actions have risks

\[
R(\text{write 1})=(1-p)(1+\lambda),\quad
R(\text{write 2})=p(1+\lambda),\quad
R(\text{no write})=1. \tag{7}
\]

Hence a hard router should write the maximum-posterior slot only when `(1+λ)min(p,1-p)<1`; otherwise it should abstain. This gives a falsifiable difference between top-1 routing and the continuous Bayes action.

## 6. Equal-write-count budget and the stronger direct router

Let `b_i=π_i r_i-\bar c_i`. Completing the square shows that enabling slot `i` reduces (1) relative to `a_i=0` by

\[
G_i=b_i^\top H_i^\dagger b_i, \tag{8}
\]

provided the range condition holds. Therefore, if at most `B` slots may be touched and each touch has equal cost, the exact optimizer of the declared separable risk chooses the `B` largest positive `G_i` and applies (2) only there. With a fixed touch price `ζ`, it additionally abstains whenever `G_i≤ζ`. The optimal support is generally not the top-`B` posterior: residual, signed protection cost and curvature matter.

This is also the strongest same-information baseline. A standard soft/hard router that reads each candidate slot, computes its own residual and solves the per-slot ridge/QP implements (2)/(8) directly. Beating only the shared-residual tensor write in (5) is not evidence for a distinct method. Exact scoring normally reads all `m` residuals, costing `O(m d_kd_v)` even if only `B` writes are materialized; shortlist routing lowers compute but loses the global top-`B` guarantee.

## 7. Old counterexample recheck and failure boundaries

- **Parent collision preserved.** If `π` is one-hot, (2) is an ordinary routed Delta slot. The tensor representation adds no distinct recurrence.
- **No identity from residual.** Two worlds can share `F_t,k,v,{S_i}` and require different slots. They produce the same action and incur (6). A learned router may reduce uncertainty only through real statistical evidence and calibration.
- **Posterior shift.** A likelihood or router trained under a different source/version process can make (2) confidently wrong. Equation (2) is Bayes-optimal only for the supplied posterior and declared loss.
- **Signed consequences and shared slots.** The scalar lower bound assumes zero signed cross-term and that the intended slot's old contents are fully releasable. Real squared-loss change generally has `c_{i|j}≠0`, and a slot may hold several still-valid facts even when `J=i`; those cases require the general (1), not the simplified `(1-π_i)Λ_i` form.
- **Cross-slot coupling.** If the consequence contains `a_i^TK_{i\ell|j}a_\ell`, the separable formula is replaced by one joint block positive-semidefinite quadratic program. Calling the per-slot shrinker exact would then be false.
- **Long horizon.** `Λ_{i|j},c_{i|j}` derived from frozen queries are not exact free-running certificates. State-dependent gates, keys and queries require the complete joint Jacobian or empirical evaluation.
- **Unmodelled new identity.** If `J` may be outside the existing slots, the posterior needs an explicit new-slot hypothesis. Renormalizing over old slots forces corruption.
- **Capacity.** Adding slots or unique events consumes state; uncertainty-aware routing does not evade finite-precision capacity or retrieval indexing.
- **Loss mismatch.** Quadratic endpoint protection does not decide factual validity, causal utility, or later-new-task learning efficiency.

## 8. Information, state and compute cost

The memory state is `m d_k d_v` scalars plus `m` posterior weights and router/likelihood state. Dense evaluation of (2) reads all slots and costs `O(m d_k d_v)`; after support selection, writing `B` slots costs `O(Bd_kd_v)`. Full `d_v×d_v` damage matrices cost `O(m d_v²)` state and up to `O(m d_v³)` dense solve work; scalar, diagonal or cached-factor costs are cheaper approximations and must be identified as such.

The same information must be supplied to all controls. The strongest simple implementation is direct routed slots with (2), not a tensor state. An explicit event/version store plus a latest-version pointer is stronger when exact provenance metadata exists; a product-key or sparse memory is the scalable retrieval control. Plain no-write, top-1 routed Delta, posterior-mean tensor Delta, and direct posterior-weighted slots form the minimum comparison set.

## 9. Distinguishing predictions and native measurement gap

Under calibrated posteriors and the declared local loss:

1. uncertainty raises the irreducible risk according to (4)/(6), even when all slot memories have enough numeric capacity;
2. higher wrong-slot damage shrinks continuous diffuse-posterior writes toward zero; an exact abstention region requires the hard full-write choice in (7), a touch price as in (8), or an explicit threshold;
3. posterior-mean tensor Delta can be worse than both (2) and no-write at high ambiguity;
4. one-hot identity collapses all repaired actions to routed ordinary Delta.

Existing bAbI/LAMBADA/RULER/LongMemEval endpoints do not natively expose latent source/version identity, calibrated `π`, wrong-slot potential outcomes, or `Λ_i`. Model-edit benchmarks can score efficacy/locality after a prescribed edit, but do not by themselves identify the pre-action identity posterior or the Bayes risk in (1). No benchmark, label, metric or result is invented here.

## 10. Contribution and disposition

The repair succeeds mathematically: it removes the identity oracle, derives the correct local action, and proves a sharp ambiguity floor. It does **not** yield a new Delta architecture. It is a multi-slot specialization of the already reviewed `REVISION_EVIDENCE_POSTERIOR_EDIT` control and composes ordinary Bayesian routing with the protected quadratic geometry already bounded in R07/R09. The implementation is direct Bayesian decision over known routed slots; the tensor lift is strictly unnecessary. The result is retained as a conditional theorem/control and as a warning against substituting a posterior-mean tag into tensor Delta. Empirical effect remains unknown.

Reopen only if a causal Delta-specific sufficient statistic estimates identity and protection at lower matched state/compute than a direct router, or if a natural native task exposes calibrated provenance and action consequences that distinguish this theorem from generic routing.
