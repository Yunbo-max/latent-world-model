# STEP2 repair: active evidence before a Delta write

Date: 2026-10-12  
Lineage: child of the R14 provenance-identifiability boundary and the bounded-repair synthesis; this is not a fourth repair attempt under the old information set.  
Status: accepted scoped theorem/control; mechanism-level collision; not a candidate. Empirical effect unknown.

## 1. Original failure and the legal patch

R14 proved a genuine information obstruction: two worlds can expose the same prefix and current Delta residual while disagreeing about whether the observation is a valid revision or a conflicting duplicate. Any updater measurable only with respect to that common information must take the same action in both worlds.

The patch changes the information pattern instead of deleting the counterexample. Before committing a write, the updater may select one bounded, legal external probe `a`, pay cost `c_a`, observe `Y ~ P_H^a`, and then choose how much of the normalized Delta update to apply. Here `H=1` means that the proposed fact is valid and should be written; `H=0` means that the protected incumbent should be retained. Future gold answers, hidden task labels, or model self-generated repetitions of the same prefix are not legal probes.

## 2. Formal object and immediate Delta stakes

Let

\[
S\in\mathbb R^{d_k\times d_v},\qquad k\ne 0,\qquad e=v-S^\top k,
\]

and define the normalized update direction

\[
U=\frac{k e^\top}{k^\top k},\qquad S_b=S+bU,\qquad 0\le b\le 1.
\]

Then `S_b^T k = S^T k + b e`; hence the squared missed-update stake under a positive-semidefinite metric `M_new` is

\[
A=e^\top M_{\rm new}e.
\]

For a quadratic protected-query metric `G_old` with output metric `M_old`, the pure displacement stake is

\[
B=\frac{k^\top G_{\rm old}k}{(k^\top k)^2}\,e^\top M_{\rm old}e.
\]

The more general declared protected set is important because a displacement-only argument can omit a linear term. For pairs `(q_j,t_j)` with residual `r_j=S^Tq_j-t_j`, weight `w_j`, and PSD metric `M_j`, let

\[
J_{\rm old}(S)=\frac12\sum_jw_j\|r_j\|_{M_j}^2.
\]

Direct expansion gives

\[
J_{\rm old}(S+bU)-J_{\rm old}(S)
=bA_{\rm old}+\frac12b^2C_{\rm old},
\]

where

\[
A_{\rm old}=\sum_jw_j\frac{k^\top q_j}{k^\top k}e^\top M_jr_j,
\qquad
C_{\rm old}=\sum_jw_j\frac{(k^\top q_j)^2}{(k^\top k)^2}e^\top M_je\ge0.
\]

Thus the binary loss below is an exact scoped model when the incumbent is locally correct and the protected residuals are centered so that the relevant linear term is absent, or when `B` is explicitly defined as the charged displacement loss. It is not a universal replacement for the general expansion.

## 3. One-probe Bayes decision

Let the prior be `pi=P(H=1|F)`. Probe `a` has conditional densities `p_h^a(y)` with respect to a common dominating measure. The posterior is

\[
p_a(y)=\frac{\pi p_1^a(y)}{\pi p_1^a(y)+(1-\pi)p_0^a(y)}.
\]

Use the scoped loss

\[
L(H,b)=HA(1-b)^2+(1-H)Bb^2.
\]

Conditioned on posterior `p`, differentiating the quadratic posterior risk yields the exact soft action

\[
b^*(p)=\frac{pA}{pA+(1-p)B}
\]

and Bayes envelope

\[
r(p)=\frac{p(1-p)AB}{pA+(1-p)B}.
\]

The repaired update is therefore

\[
S^+=S+b^*(p_a(Y))U.
\]

For a hard write/no-write decision, write iff

\[
p\ge \frac{B}{A+B},
\]

or, for `0<pi<1` and `A,B>0`, iff

\[
\frac{p_1^a(y)}{p_0^a(y)}\ge\frac{(1-\pi)B}{\pi A}.
\]

The posterior form remains the safe statement at boundary priors or zero densities; extended likelihood ratios are required otherwise.

The exact hard Bayes risk of probe `a` is

\[
R_a^{\rm hard}=\int\min\{\pi A p_1^a(y),(1-\pi)B p_0^a(y)\}\,d\mu_a(y)+c_a.
\]

For soft actions, the optimal one-probe policy is

\[
a^*\in\arg\min_a\{c_a+\mathbb E[r(p_a(Y))]\}.
\]

## 4. Value of information and the repaired conclusion

Posterior means obey `E[p_a(Y)]=pi`. Moreover, for `A,B>0`,

\[
r''(p)=-\frac{2A^2B^2}{[B+(A-B)p]^3}<0.
\]

Consequently Jensen gives

\[
\mathbb E[r(p_a(Y))]\le r(\pi),
\]

with strict inequality for every genuinely informative probe whose posterior is nonconstant. Thus any such probe has strictly positive gross value for the soft action; it is worthwhile after cost exactly when

\[
r(\pi)-\mathbb E[r(p_a(Y))]>c_a.
\]

The earlier phrase “informative but zero decision value” is valid only for the separate hard-action, piecewise-affine envelope when every posterior realization stays on the same side of the write threshold. It is false for the interior soft quadratic decision above.

If experiment `a_2` is a garbling of `a_1`, Blackwell's comparison implies that `a_1` is weakly better for every downstream decision problem before acquisition costs. This is classical decision theory, not a Delta novelty claim.

### Symmetric binary channel

For `A=B=C`, `pi=1/2`, and a binary symmetric probe with error `epsilon`, no probing costs `C/4`, while probing costs

\[
C\epsilon(1-\epsilon)+c.
\]

The probe is useful exactly when

\[
c<C(1/2-\epsilon)^2.
\]

### Minimax variants

Without a prior and without a probe, equalizing the two state losses gives

\[
b_{\rm mm}=\frac{\sqrt A}{\sqrt A+\sqrt B},\qquad
R_{\rm mm}=\frac{AB}{(\sqrt A+\sqrt B)^2}.
\]

For a fixed probe,

\[
\inf_{b(\cdot)}\max_{h\in\{0,1\}}
\mathbb E_{P_h^a}L(h,b(Y))+c_a
\]

equals a least-favourable-prior Bayes problem under the usual compactness and convexification conditions. If randomized probe selection is allowed, the probe set must also be convexified; one may not silently exchange minimization over probes with maximization over priors.

## 5. Old counterexample, predictions, and failure boundaries

The R14 same-prefix information obstruction can be weakened, and positive expected decision value is possible, only when some legal action has `P_0^a != P_1^a`. Distinct laws do not imply exact identification for every outcome: overlapping supports leave ambiguous realizations, while exact per-outcome identification requires disjoint support or an equivalent guarantee. If every allowed probe has identical conditional law, the old impossibility returns unchanged. The derivation predicts larger probe value when the posterior moves toward different actions and when the immediate stakes `A,B` are large relative to cost.

It can still fail when: the channel model is misspecified; nominally distinct sources are correlated or copied; a probe changes the world and therefore requires a POMDP/intervention model; archive access quietly adds unmatched information or storage; finite-precision metadata costs are ignored; a locally valid write harms unrelated capabilities; or recurrent feature changes make the immediate quadratic stakes a poor proxy. Full nonlinear downstream claims still require the complete state Jacobian.

## 6. Information, state, and computation cost

The construction adds an explicit probe selector, a calibrated likelihood or posterior model, probe cost, and one observation before the write. Evaluating a finite action set requires estimating each action's posterior-risk expectation—by exact integration when available or by sampling/approximation otherwise—plus channel-model calibration, in addition to the original Delta update. Archive retrieval, source authentication, repeated querying, and calibration data are counted as information and compute; they are not free improvements under a same-budget comparison.

## 7. Strong same-information and added-information controls

Required same-information controls are the no-probe posterior Bayes amplitude, the best fixed probe, the hard likelihood-ratio gate, and generic Bayesian experimental design/controlled sensing with the identical loss and cost. RIME retrieve-before-consolidate, SAGE novelty/write gates, paired post-edit validation, and abstain/no-update/archive/fresh re-encoding are system or added-information controls unless they can be instantiated with exactly matched visible information and total cost. A learned selector must beat each applicable control under an explicit matched budget.

## 8. Native measurement coverage

LoCoMo can measure endpoint long-conversation QA/F1 and evidence-retrieval diagnostics, with supporting dialogue IDs where supplied. LongMemEval and LongMemEval-S provide timestamped sessions, QA, and evidence-session analysis. Neither benchmark natively exposes a selectable authenticated pre-write probe or matched counterfactual write/skip outcome.

CounterFact and zsRE can compare edit and no-edit controls and collateral locality at matched edit budget, including efficacy and paraphrase/generalization. They do not natively provide old-fact validity, provenance labels, a protected old-capability panel, calibrated probe channels/costs, or the Delta stakes `A,B`.

No inspected native benchmark jointly supplies pre-commit action-dependent evidence, revision-validity labels, matched write/skip effects, protected old-capability queries, and channel/cost calibration. Gold answers and future tokens may supervise offline estimation but cannot be exposed as deployable evidence. The empirical effect therefore remains unknown; no experiment was executed.

## 9. Nearest-work and disposition

Controlled sensing, Blackwell comparison of experiments, and decision-directed active learning cover the acquisition-and-decision skeleton. RIME, REALM, and SAGE provide close memory-system controls for evidence retrieval, reconsolidation, and pre-write gating. The residual contribution is the transparent mapping from a normalized Delta direction to stakes `(A,B)`, the exact immediate-loss expansion, and a closed-form debugging baseline.

This is a positive repair of R14's information gap, but not a new updater family. It is retained as a scoped theorem/control. Candidate, scientific-admission, and selection counts do not change.
