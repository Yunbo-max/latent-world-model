# CHECKSUM-REVISION-SKETCH — compression cannot create revision identity

Disposition: **finite-memory corollary/control; not a candidate**.

Let \(H\in\{R,C\}\) denote true revision versus coexistence, and let \(W_t\) contain every allowed causal observable: observed history, current context/key/value and current recurrent state.  Any randomized causal sketch \(Y_t\) whose fresh randomness is independent of \(H\) conditional on \(W_{\le t}\) obeys

\[
H\longrightarrow W_{\le t}\longrightarrow Y_t.
\]

Data processing gives

\[
\operatorname{TV}(P_R^{Y},P_C^{Y})
\le \operatorname{TV}(P_R^{W},P_C^{W}),
\]

so the equal-prior Bayes error after sketching is at least \((1-\operatorname{TV}_W)/2\).  If the two worlds are causally observationally identical, the error remains at least \(1/2\).  Also \(I(H;Y\mid W)=0\), and a \(B\)-bit sketch has \(I(H;Y)\le\min\{I(H;W),B\}\).  This specializes the existing revision/collision TV no-go; random hashing creates no missing evidence.

## Strongest approximate-membership control

Suppose an externally meaningful, stable canonical identity fingerprint \(u\) is already available.  Maintain filters for identities and identity--value pairs, and declare

\[
\text{revision}\iff \operatorname{seen}(u)
\land\neg\operatorname{seen}(u,c(v)).
\]

Under ideal independent hashing, the usual occupancy approximation is

\[
p_{\rm FP}\approx(1-e^{-hn/m})^h.
\]

This rule detects a novel pair, not the latest valid value.  Different entities sharing \(u\) are deterministically conflated; contextual identity drift misses revisions; and \(A\to B\to A\) is missed because \((u,A)\) was seen historically.  Correct latestness needs a per-identity current value/version, deletion/epoch state or explicit event dictionary.

For SimHash with \(r\) independent Gaussian hyperplanes and angle \(\theta\), mismatch count is \(\operatorname{Binomial}(r,\theta/\pi)\).  A strict assumed gap \(\theta_R<\theta_C\) yields midpoint error at most

\[
\exp[-r(\theta_C-\theta_R)^2/(2\pi^2)]
\]

per comparison, plus a union factor over stored prototypes.  The geometric gap itself supplies the missing identity evidence, and storing/searching prototypes is approximate event memory.

Count-Min guarantees \(f_u\le\hat f_u\le f_u+\epsilon N\).  The theorem can certify singleton separation only with width \(\Theta(N)\): \(\epsilon N<1\) separates integer zero from one, while a robust half-unit margin needs \(\epsilon N<1/2\).  CountSketch has the same linear-width issue for constant singleton error against an \(ell_2\) tail.  Neither frequency sketch represents latest truth.

## Equivalence and cost

Without stable identity this is exactly the prior data-processing no-go.  With stable \(u\) or a proven angular margin, it is an evidence-conditioned gate plus an approximate dictionary, followed by known protected/ridge/slot edit geometry.  Costs include hash arrays/counters, projection seeds, stored signatures/indexes, version/expiry state, provenance, serialization and lookup traffic.  Fixed false-positive rate also makes memory grow with the planned number of distinct facts.

The only lead is learning an identity representation with a proved separation margin.  That is a new entity-resolution/metric-learning problem requiring supervision and nearest-work review, not a completed Delta recurrence.

No project code, test, model, benchmark, download or experiment was executed.
