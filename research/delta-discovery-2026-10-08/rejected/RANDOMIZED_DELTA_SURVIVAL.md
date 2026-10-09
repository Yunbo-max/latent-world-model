# RANDOMIZED-DELTA-SURVIVAL — unbiased random survival is variance, not memory

Disposition: **mathematically valid no-go/numerical control; not a candidate**.

Let

\[
\bar S_t=D_tS_{t-1},\quad e_t=v_t-\bar S_t^\top k_t,
\quad G_t=\beta_tk_te_t^\top,
\]

with unit \(k_t\).  For \(Z_t\mid\mathcal F_t\sim\operatorname{Bernoulli}(p_t)\), independent of the pre-mask information,

\[
\widehat S_t=\bar S_t+\frac{Z_t}{p_t}G_t
\]

is one-step conditionally unbiased, but

\[
\mathbb E[\|\widehat S_t-S_t^{\rm Delta}\|_F^2\mid\mathcal F_t]
=\frac{1-p_t}{p_t}\|G_t\|_F^2.
\]

This says nothing about an end-to-end network whose later features/tokens depend on the random state.

## Exact repeated-key counterexample

With fixed key, \(D=\alpha I\), fixed \(\beta,p\), and iid masks, an old key component is multiplied by

\[
R=\alpha(1-\beta Z/p).
\]

Then

\[
\mathbb ER=\alpha(1-\beta),\qquad
\mathbb ER^2=\alpha^2\left[(1-\beta)^2+rac{\beta^2(1-p)}p\right].
\]

For \(\beta\ne1\), the product's relative variance is

\[
\frac{\operatorname{Var}(\prod_{i=1}^nR_i)}
{\mathbb E[\prod_{i=1}^nR_i]^2}
=\left[1+\frac{\beta^2(1-p)}{p(1-\beta)^2}\right]^n-1.
\]

Thus larger second-moment “survival” is an exponentially broad path distribution, not a more reliable memory.  Pathwise nonexpansion already fails when \(p<\beta/2\), and mean contraction is insufficient for second-moment stability.

Without \(1/p\) compensation, \(\bar S+ZG\) has the same mean as deterministic Delta with \(\beta'=p\beta\).  Its expected current-key target MSE exceeds the matched deterministic gate by

\[
p(1-p)\beta^2\|e\|^2.
\]

Any benefit is therefore training regularization/update dropout, not a new deterministic memory law.

## Fixed point and direction no-go

For

\[
S^+=S-c_Zkk^\top S+d_Zkv^\top,
\]

an already-correct association \(S^\top k=v\) is preserved pathwise for every \(v\) iff \(c_Z=d_Z\) almost surely.  Independently random erase/write injects noise at the desired fixed point.

More strongly, if \(M_Z\succeq0\) and \(\mathbb EM_Z=\beta kk^\top\), then every \(u\perp k\) has

\[
0=\mathbb E[u^\top M_Zu].
\]

Nonnegativity forces \(M_Zu=0\) almost surely.  Hence \(M_Z=\gamma_Zkk^\top\) almost surely: an exact-mean PSD random erase cannot spread damage into other directions.  Signed/oblique escape routes add zero-mean cross-query noise and need a separate stability argument.

## Finite-precision exception and its limit

Standard stochastic rounding between adjacent grid points is unbiased and has conditional variance at most \(\Delta^2/4\) only without clipping/overflow and with exact probabilities.  On a frozen affine path its errors propagate through the actual ordered products.  In a finite nonnegative grid with minimum positive \(\mu\), \(0<a<1\), and absorbing zero,

\[
x_t=Q(ax_{t-1}),\qquad
\Pr(x_t>0)\le a^tx_0/\mu.
\]

So expectation can be carried by rarer survivor paths while a typical single trajectory is absorbed.  Limited random bits can also bias nominal stochastic rounding.

## Closest work and cost

Zoneout and recurrent update dropout directly cover Bernoulli state/update masking.  Stochastic rounding is classical.  Low-Discrepancy Dither for Quantized Recurrent State Caches (arXiv:2609.39185v1), LeapQuant (2609.38166) and STEPQuant (2609.38169) are closer recurrent/Delta-state numerical baselines: they address feedback of quantization error and structured precision/dither rather than claim random survival as semantic memory.

Compensated masks require RNG/branch state and can amplify active steps by \(1/p\); entrywise rounding requires state-wide decisions and resume-safe randomness.  Ensembles, antithetic copies and error-feedback add state and fall into already excluded routes.

Reopen only with a concrete single-state correlated schedule that preserves the Delta fixed point, has a query-level bound better than a deterministic matched-cost gate and low-discrepancy baselines, and fully accounts for extra state/kernel cost.  No such construction is supplied.

No project code, test, model, benchmark, download or experiment was executed.
