# Martingale innovation release for protected Delta memory

Disposition: **mathematically valid sequential-change control; rejected as a distinct Delta method**.  This is a read-only derivation and source audit; no code, data, test, scorer or experiment was run.

## Causal statistical object

For a protected association \(j\), let \(\mathcal G_t\) contain only information observed before outcome \(Y_t\).  Under the still-valid null and a predictable alternative,

\[
H_0:Y_t\mid\mathcal G_t\sim p_t,\qquad q_t\ll p_t,
\]

define

\[
B_t={q_t(Y_t\mid\mathcal G_t)\over p_t(Y_t\mid\mathcal G_t)},
\qquad M_t=\prod_{s\le t}B_s.
\]

Because \(p_t,q_t\) are fixed before \(Y_t\), \(\mathbb E_0[B_t\mid\mathcal G_t]=1\).  Thus \(M_t\) is a nonnegative martingale and the stopping time

\[
\tau_\alpha=\inf\{t:M_t\ge1/\alpha\}
\]

satisfies Ville's bound \(P_0(\tau_\alpha<\infty)\le\alpha\).  A moment version follows from a predictable conditional CGF bound:

\[
\mathbb E[e^{\lambda_tX_t}\mid\mathcal G_t]\le e^{\psi_t(\lambda_t)},
\qquad E_t=\prod_s e^{\lambda_sX_s-\psi_s(\lambda_s)}.
\]

Choosing \(\lambda_t\) after observing \(X_t\), or repeatedly inspecting fixed-time e-values in a finer filtration, invalidates this argument.

## Delta coupling and exact guarantee

Let \(u_t^C\) be an already defined protected/coexistence direction and \(u_t^R=\beta_tk_t\) the ordinary revision write.  With the absorbing release bit

\[
R_t=\mathbf1\{\max_{s\le t}E_s\ge1/\alpha\},
\]

one can deploy

\[
S_t=\bar S_t+[(1-R_t)u_t^C+R_tu_t^R]
(v_t-\bar S_t^\top k_t)^\top.
\]

Under a valid item-level null, the probability that this hard release ever fires is at most \(\alpha\).  That is the entire formal guarantee.  It does not prove that \(u^C\) preserves all useful queries, that \(u^R\) repairs semantics, or that delayed release repays blocked writes.  Soft release before threshold has no corresponding zero/one false-release guarantee.

Unknown change time can be handled by a proper mixture \(E_t=\sum_\nu\pi_\nu L_t^{(\nu)}\), paying a \(-\log\pi_\nu\) delay term.  An unrestricted sum over restarts instead gives an e-detector/average-run-length guarantee, not permanent false-alarm probability control.  Across \(J\) associations and restarts, wealth or \(\alpha\) must be allocated globally.

Under a post-change law \(q\), expected log wealth accumulates KL divergence.  For a Gaussian mean shift \(\delta\) with variance \(\sigma^2\), the first-order delay scale is

\[
{2\sigma^2\over\delta^2}\log{1\over\alpha\pi_\nu}.
\]

This is a falsifiable amplitude--delay prediction, not a semantic-memory theorem.

## Why it does not solve the Delta problem

If a revision world and a collision/coexistence world induce the same allowed causal key/value/residual law, every adapted e-process and stopping time has the same distribution in both worlds.  Low false release in the coexistence world then also means low revision detection.  Stable identity, source, version or other observed evidence is necessary to separate them.

Furthermore,

\[
\log M_t=\sum_s[\log q_s(Y_s)-\log p_s(Y_s)]
\]

is a prequential future-CE difference.  When it is an exact Bayes factor, posterior odds are prior odds times \(M_t\), so the resulting gate is the already recorded Bayesian posterior edit followed by known protected/ridge/slot geometry.  A generic e-process is not even a posterior probability.

Ordinary Delta reconstruction residual is not automatically a valid innovation: its key, direction and target may all be constructed after observing the same token.  A legal detector needs a genuine pre-outcome predictor or a later observed outcome.  Topic drift or predictor misspecification can otherwise trigger release without any fact revision.

## Closest work and disposition

This route is directly covered by anytime-valid testing and sequential change detection: Howard et al., arXiv:1808.03204v8 §2; Vovk et al., PMLR 152 (2021), *Retrain or not retrain*; Shin, Ramdas and Rinaldo, arXiv:2203.03532v4; Bhattacharyya and Ramdas, arXiv:2609.27179v1; and Adams--MacKay BOCPD, arXiv:0710.3742v1.  These works distinguish PFA, ARL, restart mixtures, filtration and detection delay.  The Delta attachment contributes no new statistical object and no new edit geometry.

Prediction: a calibrated null can satisfy the anytime bound and a separated change can show the stated delay scaling, but indistinguishable revision/collision worlds must cross at the same rate.  The strongest simple alternatives are matched-information future CE, CUSUM/e-detectors, BOCPD and the existing Bayesian edit gate.  No D-number is assigned.
