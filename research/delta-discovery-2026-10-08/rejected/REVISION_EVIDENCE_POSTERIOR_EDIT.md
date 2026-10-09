# Revision-evidence posterior edit — Bayes gate plus known edit geometry

Disposition: **rejected as a distinct method; retained as a reviewed control**.  Extra causal evidence can lift the residual-only identifiability no-go, but the resulting construction decomposes into a standard Bayesian gate and known protected/ridge/slot editing.

## Identifiability supplied by observed evidence

Let \(H\in\{R,C\}\) denote true revision versus coexistence, let \(X\) contain the state, current write and observed prefix information, and permit an additional already-observed evidence variable \(Z\), such as a reliable entity identifier, correction marker, timestamp or provenance.  Given \(\pi(x)=P(H=R\mid X=x)\) and class-conditional densities, the posterior is, wherever the denominator is nonzero,

\[
\gamma(x,z)=P(R\mid x,z)
=\frac{\pi(x)p_R(z\mid x)}
{\pi(x)p_R(z\mid x)+(1-\pi(x))p_C(z\mid x)}.
\]

If \(Z\perp H\mid X\), the posterior equals the prefix prior and no new capability appears.  Under equal priors and symmetric 0--1 loss, the minimum classification error conditional on a fixed \(x\) is \((1-\operatorname{TV}(p_R(\cdot\mid x),p_C(\cdot\mid x)))/2\).  With unequal \(x\)-dependent priors, the general Bayes error instead integrates

\[
\min\{\pi(x)p_R(z\mid x),(1-\pi(x))p_C(z\mid x)\};
\]

an unconditional TV shortcut is invalid.  Perfect discrimination requires the two conditional evidence laws to be almost-everywhere disjoint on relevant \(x\).  An ID/timestamp pair achieves this only under an explicit data-generating assumption that identifiers are unique and markers are reliable.

For false-revision cost \(c_{R\mid C}\) and missed-revision cost \(c_{C\mid R}\), the standard Bayes action chooses revision when

\[
\gamma>
\frac{c_{R\mid C}}
{c_{R\mid C}+c_{C\mid R}}.
\]

These classification statements do not bound downstream language CE or memory accuracy.

## Posterior-weighted edit

Let \(S\in\mathbb R^{d\times m}\), let unit \(a\) be an externally identified old address, let unit \(k\) be the current key, and define

\[
e_a=v-S^\top a,
\qquad
e_k=v-S^\top k.
\]

For increment \(U=S^+-S\), consider the explicitly chosen quadratic risk

\[
\begin{aligned}
J_\gamma(U)
=&\ \gamma\|a^\top U-e_a^\top\|_2^2\\
&+(1-\gamma)\left(\|a^\top U\|_2^2+
\|k^\top U-e_k^\top\|_2^2\right)
+\lambda\|U\|_F^2.
\end{aligned}
\]

For \(\lambda>0\), the unique solution is

\[
U^*=\left[aa^\top+(1-\gamma)kk^\top+\lambda I\right]^{-1}
\left[\gamma a e_a^\top+(1-\gamma)k e_k^\top\right].
\]

The coefficient matrix is positive definite, dimensions agree, and the solution lies in \(\operatorname{span}\{a,k\}\), so a two-vector Gram/Woodbury solve suffices.  This is the Bayes action only for the stated hand-designed squared edit loss; it is not implied by a sequence likelihood or semantic correctness.

At \(\gamma=1\), finite \(\lambda\) gives the ridge fit \(U^*=a e_a^\top/(1+\lambda)\), reaching exact overwrite only as \(\lambda\to0\).  At \(\gamma=0\), finite \(\lambda\) gives a soft protection/write tradeoff.  If

\[
z=(I-aa^\top)k\ne0,
\]

then the \(\lambda\to0\) minimum-Frobenius-norm solution of the exact coexistence constraints \(a^\top U=0\), \(k^\top U=e_k^\top\) is the known protected write

\[
U_C=\frac{z e_k^\top}{\|z\|_2^2}.
\]

If \(k=\pm a\), coexistence is feasible only when \(e_k=0\); otherwise separate slots/addresses are required.  Near parallelism makes \(\|U_C\|_F\) and conditioning blow up.

## Collision and cost audit

- The posterior is an ordinary two-hypothesis Bayesian gate.  It becomes a collapsed BOCPD-style special case only after specifying run length, hazard and predictive likelihood; it is not the full BOCPD posterior.
- Likelihood-reweighted predictor mixtures are a strong functional neighbor, although this construction takes one action under posterior expected edit loss rather than maintaining equivalent multi-state dynamics.
- The \(\gamma=0,\lambda\to0\) endpoint is existing orthogonal/protected projection; finite \(\lambda\) is ridge/soft preconditioning.
- Reliable identity mapped to addresses becomes deterministic routing/slots.  Explicitly retaining both hypotheses becomes the already rejected multi-state mixture route.
- A single linear protected address does not guarantee preservation of related queries or a downstream nonlinear network.

The two-vector solve is \(O(dm+d)\) after its small Gram computation, but acquiring a stable old address \(a\) requires provenance/entity retrieval.  Maintaining \(M\) explicit addresses costs \(O(Md)\) plus indexing; address errors are outside the derivation.  Exact BOCPD run-length state grows with history unless truncated.

If \(\gamma\) is trained from a future teacher answer or suffix, the added information belongs to supervision and must be compared with an equally informed classifier, deterministic router, ordinary future CE and delayed semantic supervision.  The method cannot count label information as update-rule novelty.

## Measurement boundary and disposition

LongMemEval provides public knowledge-update QA and can assess final behavior, but its native labels do not identify every internal Delta write as revision/coexistence or certify \(\gamma\).  bAbI, LAMBADA and RULER likewise cannot identify the internal gate.  This is a mechanism-level measurement gap; no synthetic case, label or metric is introduced here.

All four regimes reduce to known boundaries: no new evidence leaves the TV no-go; perfect evidence becomes deterministic routing; probabilistic evidence gives a Bayesian gate plus known edit geometry; future evidence is extra supervision.  The control clarifies what information is missing, but it does not define a new Delta principle and receives no D-number.  No project code, test, benchmark, model, training, inference, scorer, data/model download or GPU work was executed.
