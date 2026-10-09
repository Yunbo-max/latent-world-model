# NOGO-CAUSAL-POLYNOMIAL-FUTURE-PRODUCT

Disposition: **scoped no-go/solver control; not a candidate**.

For

\[
S_t=A_tS_{t-1}+u_te_t^\top,
\qquad A_t=(I-\beta_tk_tk_t^\top)D_t,
\]

let \(P_{t,h}=A_{t+h}\cdots A_{t+1}\).  A deployed \(u_t\) is \(\mathcal F_t\)-measurable.  The Bayes-relevant quadratic future-risk object is

\[
G_t=\mathbb E\left[\sum_h\omega_hP_{t,h}^\top Q_{t,h}P_{t,h}\mid\mathcal F_t\right],
\]

not a realized future product that the causal updater cannot access.

## What a causal Krylov basis can approximate

For \(z=K_rc\) measurable at time \(t\), square-integrability gives the conditional projection identity

\[
\mathbb E[\|Pb-z\|^2\mid\mathcal F_t]
=\mathbb E[\|Pb-\mathbb E[Pb\mid\mathcal F_t]\|^2\mid\mathcal F_t]
+\|\mathbb E[Pb\mid\mathcal F_t]-z\|^2.
\]

Krylov approximation can reduce only the second term; conditional suffix uncertainty remains.  Even commuting future factors need not factor in expectation: with the same \(Z\sim\operatorname{Bernoulli}(1/2)\), \(A_1=A_2=ZI\) gives \(\mathbb E[A_2A_1]=I/2\) but \(\mathbb E[A_2]\mathbb E[A_1]=I/4\).

For a scalar-coefficient polynomial in one fixed nonzero square matrix \(B\), \([p(B),B]=0\), hence

\[
\|P-p(B)\|\ge\frac{\|[P,B]\|}{2\|B\|}
\]

in a submultiplicative operator norm.  This does not exclude multi-basis/noncommutative predictors; it proves that one aggregated operator loses generic order information.

If \(Q\) is prefix-measurable,

\[
\mathbb E[P^\top QP\mid\mathcal F_t]
=\bar P^\top Q\bar P+
\mathbb E[(P-\bar P)^\top Q(P-\bar P)\mid\mathcal F_t].
\]

For future-random \(Q_h\), the required object is directly the joint moment \(\mathbb E[P^\top Q_hP\mid\mathcal F_t]\); predicting only \(\bar P\) is insufficient.

## No free causal write rotation

For unit \(k\), current correction \(k^\top u=\beta\) implies \(\|u\|\ge|\beta|\), with equality only at ordinary \(u=\beta k\).  A deterministic worst-case example takes \(k=(e_1+e_2)/\sqrt2\) and two causally indistinguishable legal suffix erasures

\[
P_1=\operatorname{diag}(0,1),\qquad
P_2=\operatorname{diag}(1,0).
\]

Under \(k^\top u=1\) and \(\|u\|^2\le2\), at least one path has survival no greater than \(1/2\), attained by \(u=k\).  This is a deterministic/pathwise minimax statement; randomization against an oblivious adversary can change the expected game and is not covered.

If true and approximate factors are both nonexpansive in the same norm, telescoping gives

\[
\|A_h\cdots A_1-\hat A_h\cdots\hat A_1\|
\le\sum_j\|A_j-\hat A_j\|.
\]

This is an upper bound, not a guarantee of useful long-horizon prediction.

## Route collapse and cost

- realized suffix propagation is a forward-sensitivity/source trace;
- a causal predictor of \(G_t\) is the inactive D03 future-risk/teacher route;
- polynomial inverse action on \(G_t\) is a PDN/GKA-style solver;
- several current-token factors are DeltaProduct/multi-step Delta;
- diagonal polynomial gains are KDA/RWKV-style gating.

Dense degree-\(r\) Horner action costs \(O(rd^2d_v)\) for \(d_v\) right-hand sides; dense \(G\) itself costs \(O(d^2)\) state and exact solve \(O(d^3)\).  Explicit Krylov bases add \(O(rdd_v)\) storage.  Predicting \(H\) future factors costs at least \(O(Hd)\) outputs before the predictor and training target are counted.  General noncommutative word bases grow combinatorially without structure.

A prefix-identifiable latent suffix regime is a lead only.  No distinct deployed construction or nearest-work separation is supplied.

No project code, test, model, benchmark, download or experiment was executed.
