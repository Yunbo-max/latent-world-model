# R17 v2 — causal predictive-leakage certificate for exact Delta overwrite

Status: **conditional theorem/debugging control; parked after attempt 2/3, not an active D candidate**. This versioned child preserves `R17_PREDICTIVE_QUOTIENT_OVERWRITE.v1.md` and repairs its earliest interface defect: the realized future query family is not available when the write is chosen. The replacement is a prefix-measurable uncertainty contract. It yields exact robust and conditional-expectation leakage bounds, plus an impossibility boundary when indistinguishable futures disagree. It does not infer which knowledge remains valid, provide future evidence, or establish an advantage over direct sufficient-coordinate storage.

## 1. Formal object and causal interface

Work in the post-decay, pre-overwrite convention. Let `Sbar in R^(d x m)`, let `k in R^d` be unit norm, and apply exact overwrite

\[
T(\bar S)=(I-kk^\top)\bar S+kv^\top . \tag{1}
\]

The erased old-state perturbations are

\[
E=ka^\top,\qquad a\in\mathbb R^m. \tag{2}
\]

For a frozen continuation `omega`, define effective future covectors `x_{u,omega}=P_{u,omega}^Tq_{u,omega}`, nonnegative weights `w_u>=0`, and the PSD finite-horizon Gram

\[
G_\omega=\sum_u w_u x_{u,\omega}x_{u,\omega}^\top\succeq0. \tag{3}
\]

Exactly as in v1, the weighted output energy lost by (1) is

\[
L_\omega(E)=\sum_uw_u\|q_{u,\omega}^\top P_{u,\omega}E\|_2^2
=\|a\|_2^2 k^\top G_\omega k. \tag{4}
\]

If the comparison begins before an invertible decay `D`, replace `k` everywhere in (2)--(4) by `h=D^{-1}k`. The two conventions must not be mixed.

Equations (3)--(14) concern a declared frozen linear continuation. If `P_{u,omega}` or `q_{u,omega}` changes with the overwritten state or chosen action, they do not bound the full nonlinear free-running trajectory without an additional common-exogenous coupling, complete-state Jacobian/reachability calculation, or certified Lipschitz remainder.

Let `F_t` be the information available immediately before the write. A lawful deployment certificate, ambiguity set, or policy must be `F_t`-measurable. The realized suffix, future targets, and future factual-validity labels are not in `F_t`.

## 2. Exact robust certificate

Let \(\mathcal G_t\) be an `F_t`-measurable nonempty set of admissible future Grams and define its support in the erased direction

\[
\rho_t(k)=\sup_{G\in\mathcal G_t}k^\top Gk. \tag{5}
\]

Then the worst-case lost output energy is exactly

\[
\sup_{G\in\mathcal G_t}L_G(ka^\top)=\|a\|_2^2\rho_t(k). \tag{6}
\]

Consequently, exact quotient invisibility for every admitted continuation holds iff

\[
\boxed{\rho_t(k)=0}. \tag{7}
\]

Because every `G` is PSD, (7) is equivalent to

\[
k\in\bigcap_{G\in\mathcal G_t}\ker G. \tag{8}
\]

Writing

\[
\mathcal V_t=\operatorname{span}\!\left(\bigcup_{G\in\mathcal G_t}\operatorname{range}G\right), \tag{9}
\]

the universally invisible space is `V_t^perp`. This identifies the strongest direct control: retain coordinates on `V_t` explicitly. If `B_t` is a basis of `V_t` and `r=dim(V_t)`, storing `B_t^T Sbar` costs `rm` state. A prefix-varying basis additionally costs `dr` numbers unless the same shared generator/interface supplies it without duplication. A split or renamed memory has no cardinality advantage over that fully charged ledger merely because its internal representation differs.

For the spectral-norm ambiguity ball

\[
\mathcal G_t^{\rm sp}=\{G\succeq0:\|G-\widehat G_t\|_2\le\epsilon_t\},
\qquad \widehat G_t\succeq0, \tag{10}
\]

the support is exact:

\[
\boxed{\rho_t(k)=k^\top\widehat G_tk+\epsilon_t\|k\|_2^2}. \tag{11}
\]

The upper bound follows from the operator norm. Equality is attained by

\[
G=\widehat G_t+\epsilon_t\frac{kk^\top}{\|k\|_2^2}, \tag{12}
\]

which is PSD and lies in the ball. Thus any positive isotropic uncertainty radius destroys a nonzero exact-zero certificate. It can still certify a tolerance, but it cannot manufacture exact preservation from uncertain continuation geometry.

More generally, if a prefix-issued random matrix `U_t` satisfies

\[
\Pr(G_\omega\preceq U_t\mid\mathcal F_t)\ge1-\delta, \tag{13}
\]

then with the same conditional probability

\[
L_\omega(ka^\top)\le\|a\|_2^2k^\top U_tk. \tag{14}
\]

Equation (13), not the name “uncertainty estimate,” is the safety assumption. A posterior credible matrix, average Gram, or calibration curve is not automatically a Loewner upper prediction set.

An assumption-free bounded-family specialization shows why this is restrictive. If the prefix reveals only

\[
\|x_{u,\omega}\|_2\le L,
\qquad \sum_u w_u\le W, \tag{15}
\]

then `0 <= G_omega <= WL^2 I`, and

\[
\sup_\omega k^\top G_\omega k=WL^2\|k\|_2^2. \tag{16}
\]

The bound is attained by one admitted suffix covector parallel to `k`. Thus boundedness alone gives the full isotropic worst case; a useful certificate requires more structure than a norm bound.

## 3. Expected leakage is not realized leakage

Let `Z_t` be a fixed prefix stratum. Let a calibration sigma-field `H_n` contain past episode Grams `G_1,...,G_n`, sampled conditionally independently given `Z_t`, and let the deployment suffix Gram be a fresh conditionally independent draw from the same continuation law. Assume

\[
0\preceq G_i\preceq RI,
\qquad M_t=\mathbb E[G_\omega\mid Z_t]. \tag{17}
\]

Let `Ghat_n=n^{-1} sum_i G_i`. A valid one-sided matrix-Bernstein radius `epsilon_{n,delta}` yields

\[
\Pr\!\left(M_t\preceq\widehat G_n+\epsilon_{n,\delta}I\right)\ge1-\delta. \tag{18}
\]

For example, applying matrix Bernstein to `X_i=M_t-G_i`, with `lambda_max(X_i)<=R` and `||sum_i E[X_i^2|Z_t]||<=nR^2`, gives the conservative radius

\[
\epsilon_{n,\delta}
=R\sqrt{\frac{2\log(d/\delta)}{n}}
+\frac{2R\log(d/\delta)}{3n}, \tag{19}
\]

under the bounded independent assumptions above. Therefore, with probability at least `1-delta` over the historical sample,

\[
\mathbb E[L_\omega(ka^\top)\mid Z_t]
\le \|a\|_2^2 k^\top(\widehat G_n+\epsilon_{n,\delta}I)k. \tag{20}
\]

This is an **expected-leakage** statement. It does not imply

\[
G_\omega\preceq\widehat G_n+\epsilon_{n,\delta}I \tag{21}
\]

for the next realized suffix. Matrix concentration estimates the conditional mean; it does not convert a random future Gram into its mean.

One generic realized-tail consequence is possible but weaker. Since

\[
Y_\omega=k^\top G_\omega k\ge0, \tag{22}
\]

conditional Markov gives, for `0<alpha<1`,

\[
\Pr\!\left(
Y_\omega\le\frac{k^\top M_tk}{\alpha}
\middle|Z_t\right)\ge1-\alpha. \tag{23}
\]

On the calibration event (18), combine the mean bound (20) with conditional Markov (23). A union bound over calibration-sample randomness and the fresh deployment suffix gives joint coverage at least `1-delta-alpha`:

\[
L_\omega(ka^\top)
\le \frac{\|a\|_2^2}{\alpha}
k^\top(\widehat G_n+\epsilon_{n,\delta}I)k. \tag{24}
\]

A sharper pathwise result requires a genuine conditional quantile/prediction-set model, bounded-tail assumption, or a deterministic ambiguity set. Optional stopping requires a time-uniform confidence sequence rather than repeated use of a fixed-time bound. Distribution shift, prefix-stratum misspecification, endogenous future queries, or action-dependent continuations invalidate (17)--(24) unless represented explicitly.

Finite samples cannot certify exact zero without a support assumption. After `n` observed zero Grams, consider a compatible law that emits

\[
G=R\frac{kk^\top}{\|k\|_2^2}
\quad\text{with probability }p,
\qquad G=0\text{ otherwise}. \tag{25}
\]

The all-zero history has probability `(1-p)^n`. Hence every distribution-free `(1-delta)` upper confidence bound `p_U` must satisfy

\[
p_U(0^n)\ge1-\delta^{1/n}; \tag{26}
\]

equivalently, ruling out event mass above `eta` requires at least

\[
n\ge\frac{\log\delta}{\log(1-\eta)}
\approx \eta^{-1}\log(1/\delta). \tag{27}
\]

No finite `n` proves `p=0` without structural support or a margin premise.

## 4. Identical-prefix impossibility

Take `d=2`, `k=e_1`, and two continuation worlds sharing exactly the same `F_t`:

\[
G^{(0)}=e_2e_2^\top,
\qquad
G^{(1)}=e_1e_1^\top. \tag{28}
\]

The write is harmless in world 0 and loses unit output energy per `||a||^2` in world 1. Any deterministic prefix-only rule takes the same action in both worlds. Any uniform PSD upper certificate must dominate both admitted Grams, so its erased-direction score obeys

\[
k^\top U_tk\ge1. \tag{29}
\]

A point prediction that reports zero is simply invalid in world 1. Randomizing the write cannot supply the missing world identity; it only mixes its losses. External probes, delayed feedback, or a justified continuation law change the information set and must be separately budgeted.

This preserves the old v1 scalar failure rather than deleting it. The repair states exactly which additional assumption makes a nontrivial certificate possible.

## 5. Partial overwrite boundary

For `0<=beta<1`, the old-state factor is

\[
A_\beta=I-\beta kk^\top, \tag{30}
\]

with eigenvalue `1-beta` along `k`, so it is invertible and

\[
A_\beta^{-1}=I+\frac{\beta}{1-\beta}kk^\top. \tag{31}
\]

There is no exact lost quotient direction, but inverse noise on the `k` component is amplified by `1/(1-beta)`. For the standard Delta residual `e=v-Sbar^Tk`, the post-write residual is `(1-beta)e`, while the perturbation to another query `q` is `beta(q^Tk)e`. For `c_new,c_old>=0` and `c_new+c_old>0`, a quadratic one-step tradeoff

\[
J(\beta)=c_{\rm new}(1-\beta)^2+c_{\rm old}\beta^2 \tag{32}
\]

has the familiar optimum

\[
\beta^*=\frac{c_{\rm new}}{c_{\rm new}+c_{\rm old}}. \tag{33}
\]

This is ordinary gated shrinkage/ridge geometry, not a new quotient mechanism. The unknown `c_old` is exactly the future-relevance problem above; choosing `beta<1` softens but does not solve it.

## 6. Costs, controls, and falsifiable consequences

A full dense `U_t` costs `O(d^2)` state and a quadratic form costs `O(d^2)`. Low-rank factors reduce this only if their construction and approximation error are charged. A scalar certificate for one fixed `k` is cheaper, but must be recomputed when the key changes and cannot choose a different protected direction. Computing historical `G_i` still requires the declared suffix covectors or an equivalent author-provided interface; learned surrogates add estimation and calibration obligations.

The strongest same-information controls are:

1. abstain from exact overwrite when the certified score exceeds the tolerance;
2. store `B_t^T Sbar` directly for the robust observable span (9);
3. use ordinary partial Delta gating with the same certified scalar;
4. if optimizing the write direction under a PSD metric, compare with R09's closed-form inverse-metric edit, because that is the same geometry.

Conditional predictions are concrete:

- If a deterministic all-suffix upper bound `U_t` satisfies `k^TU_tk=0`, every admitted suffix has zero frozen-path leakage. Under the probabilistic certificate (13), the same conclusion holds only with conditional probability at least `1-delta`.
- Under (17)--(20), the empirical upper bound controls conditional **mean** leakage; rare realized suffixes can violate the numerical mean bound.
- Enlarging a nested ambiguity/confidence set raises its support score monotonically and can only reduce the set of exact-safe keys; unrelated confidence procedures need not be ordered.
- Two identical-prefix worlds of (28) force any uniform safe rule to behave conservatively unless new information distinguishes them.

bAbI, LAMBADA, RULER and LongMemEval expose endpoint behavior, not `F_t`, the realized effective-query Gram, a calibrated PSD prediction set, the overwritten counterfactual state, or the direct-ledger state. They cannot natively verify coverage (13), distinguish mean from pathwise protection, or attribute a forgotten answer to the erased quotient. Synthetic instrumented traces could test the theorem later, but that would be a new measurement object, not an existing native benchmark. No data, metric, label or result is invented here.

## 7. Nearest work and disposition

The mathematical skeleton is covered by robust unobservability/observability, predictive-state quotients, uncertainty-set support functions, matrix concentration/confidence sequences, conditional rate-distortion, and R09's dynamic protection Gramian. R17's retained Delta-specific value is diagnostic: it maps exact overwrite to one erased direction and shows precisely what a lawful prefix certificate must upper-bound, while separating expected from realized leakage.

That is useful repair, not an architecture candidate. The certificate needs an externally justified continuation law or ambiguity set, can be vacuous under broad uncertainty, and does not beat the direct sufficient-coordinate ledger. Semantic retain-versus-revise validity and empirical effectiveness remain unknown.

**Decision:** park after substantive attempt 2/3. Add zero active, scientifically admitted or selected candidates. Reopen only when a prefix-valid certificate is constructed and calibrated for the deployed continuation law, costs less than an equal-information direct ledger, and supports a native mechanism-identifying measurement. Merely changing `delta`, the horizon, the norm ball, the gate threshold or the Gram estimator is not a new repair.
