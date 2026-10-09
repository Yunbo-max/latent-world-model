# Step 2 re-entry: joint validity and future-query geometry

Status: **conditional theoretical/target-construction lead, not an admitted method or originality claim**. This reopens the problem definition rather than adding a renamed module. The noisy-key result already shows why the intended deployment query law must define the target; structural recovery is not automatically better prediction. Mathematics/source review only, no project execution or experiment design.

## Natural question and exact object

When a putative edit may be valid or invalid, can a posterior scalar edit gate be optimal if validity correlates with which future queries matter? This is a falsifiable conditional question; no observed project failure is asserted. It is distinct from whether any causal evidence can identify validity at all: existing indistinguishability results still apply within their conditions.

Let \(\mathcal F\) be all causally available deployment information before deciding an edit. Vectorize the full deployed state as \(s\in\mathbb R^n\). Consider edit \(\delta\in\mathbb R^n\), fixed \(\mathcal F\)-measurable proposed valid edit \(u\), latent validity \(r\in\{0,1\}\), and future output sensitivity \(J\in\mathbb R^{\ell\times n}\). The conditional joint law of \((r,J)\) may be dependent. Require finite relevant moments and a joint conditional law fixed independently of the proposed decision; if the edit changes future sampling, validity or feature laws, this frozen-law objective omits those effects. For affine future outputs, suppose the desired output correction really is \(Jr u\). The exact quadratic decision problem is

\[
L(\delta\mid\mathcal F)
=\mathbb E[\|J(\delta-r u)\|^2\mid\mathcal F]+\lambda\|\delta\|^2,
\qquad \lambda>0.
\]

Here validity is a probability object, not an online oracle. The assumption that a valid branch wants the same state edit \(u\), and an invalid branch wants zero, is explicit. Other desired output corrections \(b\) instead give \(h=\mathbb E[J^\top b\mid\mathcal F]\). Label availability is a separate condition. No future query, answer, \(r\) or realized \(J\) is granted to the deployer merely by writing a conditional expectation.

## Continuous derivation and separability condition

Define

\[
H=J^\top J,\quad G=\mathbb E[H\mid\mathcal F],\quad
G_r=\mathbb E[rH\mid\mathcal F],\quad
p=\mathbb E[r\mid\mathcal F],\quad M=G+\lambda I.
\]

Expand the square, using \(r^2=r\):

\[
L(\delta)=\delta^\top M\delta-2\delta^\top G_r u+u^\top G_r u.
\]

Thus \(\nabla L=2M\delta-2G_r u\), \(M\succ0\), and the unique optimizer is

\[
\boxed{\delta_*=(G+\lambda I)^{-1}G_r u.}
\]

A separate posterior gate and averaged metric assumes \(G_r=pG\), leading to \(\delta_{\rm sep}=M^{-1}pG u\). At \(\lambda=0\) and \(G\succ0\), this is simply \(pu\). Completing the square yields the exact excess risk

\[
L(\delta_{\rm sep})-L(\delta_*)
=u^\top(G_r-pG)M^{-1}(G_r-pG)u.
\]

Therefore equivalence for this edit holds **iff** \((G_r-pG)u=0\). Conditional independence is sufficient but unnecessary; only the relevant conditional mixed moment must factor. This is the precise residual question left by a Bayes gate plus mean future metric. Marginal calibration of \(p\) and \(G\) alone cannot determine it.

An analytic counterexample, not a new benchmark or measured result: scalar \(u\ne0\), equal-probability branches with \((r,H)=(1,4)\) and \((0,1)\), \(\lambda=0\). Then \(G=5/2\), \(G_r=2\), \(p=1/2\), so \(\delta_*=4u/5\) but \(\delta_{\rm sep}=u/2\). Their excess is \(9u^2/40\). If \(H\) is the same in both branches, the factorization is exact and the proposed coupling adds no benefit. The contrast tests a condition, not a promise of empirical improvement.

Because \(0\le r\le1\), \(0\preceq G_r\preceq G\preceq M\). Hence \(T=M^{-1/2}G_rM^{-1/2}\) has eigenvalues in \([0,1]\), and \(\delta_*=M^{-1/2}TM^{1/2}u\) is contractive in the \(M\)-norm. This does not guarantee Euclidean contraction, factual retention, or a stable deployed recurrent transition; conditioning can amplify ordinary norms. A stronger claim must analyze that recurrence and information access separately.

If only edits in a specified linear subspace are realizable, write \(\delta=Wa\). The correct optimizer is \(a_*=(W^\top MW)^{-1}W^\top G_r u\) when \(W\) has independent columns. An unconstrained full-state solution cannot be promoted to a rank-one Delta write without proving that interface is realizable.

## Why full state sensitivity matters

For key-by-value Delta, set \(\bar S=D S\), \(e=v-\bar S^\top k\), \(S^+=\bar S+\beta k e^\top\). Permit features/gates/decay to depend differentiably on the previous full state and current input. Holding the input fixed, the exact differential is

\[
\begin{aligned}
dS^+={}&(I-\beta kk^\top)\{D\,dS+(dD)S\}\\
&+(d\beta)k e^\top+\beta(dk)e^\top
+\beta k(dv)^\top-\beta k(dk)^\top\bar S.
\end{aligned}
\]

The last four feature/gate terms and the \(dD\) term vanish when the relevant directional derivatives vanish, as under frozen state-independent features; state dependence alone need not make each term nonzero, and cancellation is possible. This preserves decay/rank-one order. If the full state has other coordinates, this is one block of its Jacobian, not the entire Jacobian. For \(s_t=f_t(s_{t-1},x_t)\), the derivative of a future output is its readout Jacobian times the **chronological product of full \(D_s f_t\)**, including all paths. Frozen-feature ordered products are exact finite-edit propagators only for the corresponding affine graph.

For a nonlinear differentiable model, \(J\delta\) is a local first-order surrogate. If the future map has Hessian norm at most \(B_2\) throughout the segment, its remainder norm is at most \(B_2\|\delta\|^2/2\). Without a bounded neighborhood, the quadratic optimizer has no global certificate; discrete retrieval/switches may lack this derivative entirely. The surrogate's validity must be checked separately, not renamed as exact semantic protection. Likewise a branch-dependent desired correction not of form \(Jr u\) requires the general mixed moment \(\mathbb E[J^\top b]\).

## Finite sufficient moments and the diffusion boundary

Under the stated quadratic object, the decision depends only on \(G\) and \(h=G_r u\); the constant target-risk term does not affect the minimizer. A full conditional diffusion sampler has **no mathematical necessity for this decision** when these moments are otherwise available. Direct causal prediction of \(G,h\), a simple joint conditional model, ordinary future CE or teacher supervision are strong alternatives, with different available labels/objects clearly separated.

Given genuine conditional joint samples \((r_i,J_i)\), sample averages of \(H_i\) and \(r_iH_i u\) are unbiased moment estimators. Independently sampling validity and query geometry changes the target to \(pG u\) and destroys the coupling. If \(\widehat G\succeq0\), \(\widehat\delta=(\widehat G+\lambda I)^{-1}\widehat h\) obeys

\[
\|\widehat\delta-\delta_*\|
\le\lambda^{-1}\{\|\widehat h-h\|+\|\widehat G-G\|\|\delta_*\|\}.
\]

This follows by subtracting the two normal equations, not by assuming a trained sampler is correct. Bias, conditional-law mismatch and model cost remain. With \(\lambda=0\), require \(G\succ0\) for the exact optimizer and an invertible \(\widehat G\) with a supplied bound \(0<\gamma\le\lambda_{\min}(\widehat G)\); replace \(\lambda\) by \(\gamma\) in this perturbation bound. A bound on exact \(G\) alone does not bound the estimated inverse. Nonquadratic loss, large nonlinear edits, multimodal actions or chance constraints can require distributional information beyond these moments; they do not by themselves establish diffusion as the necessary estimator.

No sampling, fitting, autodiff or linear solve was executed. Exact dense \(G\) storage costs \(O(n^2)\), and a generic dense solve costs \(O(n^3)\); even forming \(J\) may be prohibitive. Matrix-free products use \(J^\top J a\), but need their own computation/approximation/source audit. A conditional moment predictor requires legitimate training information and estimation validation. Future traces/validity labels may be used only as declared training/scoring supervision, never leaked into deployment. These mathematical assets do not constitute a model implementation or an executable experiment matrix.

## Repositioning and unresolved obligations

The useful theoretical result is the exact **mixed-moment separability condition**, together with the endogenous-Jacobian and finite-moment boundary. It can remain a valuable target/representation result even if the deployed update eventually uses known components; a new deployed recurrence or new causal evidence is not required for every kind of scientific contribution. Its originality and importance still need their own obligations. This normal-equation derivation is not itself claimed new.

Closest existing packet objects are D01/posterior editing and D03/observability or Gauss–Newton metrics. Their previous collision verdicts remain historical and scoped, rather than forbidding every conditional combination. Compare the actual **joint** moment against an explicitly factorized baseline and an equally informed joint Bayesian decision/teacher baseline. D01-style mixtures and Bayesian models are not inherently factorized: evaluating branch-conditioned future risk already preserves the dependence. Existing weighted-Bayes normal equations (MELO Proposition 1) and APO function-space proximal metrics cover foundational principles; the Delta-specific residual, importance and source separation remain unresolved. See the independent review for exact primary locators; no new theorem or candidate originality is claimed. The current native QA assets do not directly label edit validity or expose the relevant mixed moment. LongMemEval knowledge-update is a natural endpoint lead, but its official judge/cost and label limitations remain as recorded; no substitute scorer or synthetic branch label is introduced.

Next lawful work: establish a real task/observation contract for \(r,b,J\), read nearest-work formulas and native asset interfaces, decide whether the mixed-moment distinction is already covered, and close local-surrogate/estimator tractability. If those obligations cannot close, retain this theory lead rather than adding a D-card. **Pool remains 5 historical / 0 active / 0 admitted / 0 selected; 20/15 targets are unchanged.**
