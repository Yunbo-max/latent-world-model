# SPD metric rescue of oblique Delta — exact coordinate equivalence control

Disposition: **rejected as a distinct method; retained as a metric-stability control**.

## Rank-one correction and existence theorem

Consider

\[
x^+=x+w(y-r^\top x),
\qquad A=I-wr^\top,
\qquad c=r^\top w.
\]

The addressed residual satisfies \(e^+=(1-c)e\).  A fixed SPD matrix \(H\) with

\[
A^\top H A\preceq H
\]

exists if and only if \(0<c\le2\).  Every such certificate satisfies

\[
Hw=\alpha r,
\qquad \alpha>0,
\]

and then

\[
H-A^\top H A=\alpha(2-c)rr^\top\succeq0.
\]

Necessity follows because every \(z\in\ker r^\top\) is fixed by \(A\); zero quadratic form under the PSD slack forces the slack to annihilate that subspace, hence \(Hw\in\operatorname{span}(r)\).  Positivity then forces \(c>0\), and the displayed slack forces \(c\le2\).

This explains the Euclidean oblique no-go: at \(H=I\), nonexpansiveness requires \(w\parallel r\).  A genuine oblique update can be nonexpansive only after changing the geometry.

## Construction and conditioning price

Let \(e=w/\|w\|\), decompose \(r=(c/\|w\|)e+r_\perp\), and set \(a=c/\|w\|^2\), \(b=r_\perp/\|w\|\).  A suitable SPD completion can be built from

\[
H=aee^\top+eb^\top+be^\top+rac{bb^\top}{a}
+\mu(I-ee^\top),
\]

with the orthogonal-complement coefficient chosen large enough for positive definiteness; it satisfies \(Hw=r\).  If \(\theta\) is the angle between \(w\) and \(r\), every such metric obeys the conditioning lower bound

\[
\kappa(H)\ge
\left(\frac{1+\sin\theta}{\cos\theta}\right)^2.
\]

Near-orthogonal erase/write directions therefore move the expansion problem into an ill-conditioned coordinate system rather than removing it.

## Executable form and exact equivalence

For fixed \(H\succ0\), choose

\[
w_t=
\frac{\beta_tH^{-1}k_t}{k_t^\top H^{-1}k_t},
\qquad0<\beta_t<2,
\]

and update

\[
S_t=(I-w_tk_t^\top)D_tS_{t-1}+w_tv_t^\top.
\]

The current-key residual contracts by \(1-\beta_t\), and the query effect is

\[
\Delta o(q)=
\beta_t\frac{q^\top H^{-1}k_t}{k_t^\top H^{-1}k_t}e_t^\top.
\]

If \(D_t^\top H D_t\preceq H\), the actual ordered homogeneous update is also \(H\)-nonexpansive.

But with \(Z=H^{1/2}S\) and \(\tilde k=H^{-1/2}k\), the recurrence becomes exactly

\[
Z^+=
\left(I-\beta
\frac{\tilde k\tilde k^\top}{\|\tilde k\|^2}\right)Z
+\beta\frac{\tilde k}{\|\tilde k\|^2}v^\top,
\]

and readout uses the transformed query \(H^{-1/2}q\).  Fixed-metric oblique Delta is therefore normalized/preconditioned Delta in whitened coordinates, not a new dynamics family.

## Time-varying metric boundary

Per-token local certificates \(A_t^\top H_tA_t\preceq H_t\) do not compose.  A valid telescoping path needs a cross-time inequality such as

\[
A_t^\top H_tA_t\preceq H_{t-1}
\]

and uniform bounds \(mI\preceq H_t\preceq MI\).  Otherwise shrinking the metric can manufacture a false stability claim.  Explicitly changing coordinates while preserving physical state requires transport \(H_t^{1/2}H_{t-1}^{-1/2}\), with dense cost up to \(O(d_k^2d_v)\).

Dense fixed \(H\) costs \(O(d_k^2)\) storage and solve/multiply work; diagonal forms are cheap but fall directly in the known diagonal-preconditioning family.  PDN, Bayesian/Kalman Delta, natural-gradient/proximal edits, OWM and QED already cover the principal preconditioned/protected geometry.  A future candidate would need a causal cross-time metric law with a non-equivalence and necessity result; none is supplied here.

The theorem is a useful bridge between the Euclidean oblique no-go and preconditioned Delta, but it is a coordinate-equivalence control.  No project code, test, model, benchmark, training, inference, scorer, download or GPU work was executed.
