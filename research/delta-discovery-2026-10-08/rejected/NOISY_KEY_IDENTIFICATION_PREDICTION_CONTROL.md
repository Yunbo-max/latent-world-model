# Noisy-key Delta: identification and prediction are different targets

Disposition: **known EIV/BC-LMS/IV control, not an admitted candidate**. No D-number. This is a conditional mathematical analysis, not evidence that this project's learned keys exhibit measurement noise. No project execution or experiment occurred.

## Probability object and observation contract

Use key-by-value state \(S,B\in\mathbb R^{d\times m}\). At each step observe \(k=x+\epsilon\) and \(v=B^\top x+\nu\); optionally also \(z=x+\delta\). Assume centered iid tuples over time, mutually independent \(x,\epsilon,\delta,\nu\) within a tuple, finite required moments, and \(C=\mathbb E[xx^\top]\succ0\), \(R=\mathbb E[\epsilon\epsilon^\top]\succeq0\), \(R'=\mathbb E[\delta\delta^\top]\succeq0\). Initialization is independent of subsequent tuples. These are fixed features and a stationary linear target; no decay, normalization, state-conditioned feature network or learned gate is silently included. Gaussianity is needed only for the Bayes readout and explicit scalar fourth-moment examples below.

There are two legitimate objectives: recover latent structural map \(B\), or minimize squared error predicting \(v\) from the observed query \(q\). They coincide for clean queries under this model, but generally differ for noisy queries. Neither objective by itself supplies event identity, revision labels or semantic truth.

## Normal equations and the actual recurrences

Ordinary Delta/LMS is

\[
S^+=S+\eta k(v-S^\top k)^\top.
\]

Expanding the population quadratic loss gives gradient \((C+R)S-CB\), since \(\mathbb E[kv^\top]=CB\). Consequently its population minimizer and mean fixed point are

\[
S_{\rm obs}=(C+R)^{-1}CB.
\]

For constant \(\eta\), iid independence gives the exact mean recursion about this fixed point, with transition \(I-\eta(C+R)\). Mean convergence requires \(0<\eta<2/\lambda_{\max}(C+R)\). This does not say individual constant-step iterates converge to a deterministic matrix; stochastic steady-state error remains.

If true \(R\) is supplied, subtracting its quadratic contribution gives

\[
L_{\rm corr}(S)=\tfrac12\mathbb E\|v-S^\top k\|^2-
\tfrac12\operatorname{tr}(S^\top RS),\qquad
\nabla L_{\rm corr}=C(S-B).
\]

The corresponding unbiased gradient estimator and deployed update are

\[
\widehat g=(kk^\top-R)S-kv^\top,\qquad
S^+=S+\eta\{k(v-S^\top k)^\top+RS\}.
\]

This is column-wise bias-compensated LMS, not a new Delta mechanism. The population Hessian is positive definite, whereas the sample Hessian \(H=kk^\top-R\) can be indefinite. For \(R=rI\), every direction orthogonal to \(k\) has sample transition multiplier \(1+\eta r\). Population convexity therefore does not imply sample nonexpansion or information retention. If a fixed misspecified \(\widehat R\) is used, the mean Hessian becomes \(C+R-\widehat R\) and, when invertible, the fixed point becomes \((C+R-\widehat R)^{-1}CB\). It can lose positive definiteness. A noisy online covariance estimate needs a separate joint analysis.

With a valid independent second view, the alternative moment and update are

\[
\mathbb E[z(v-S^\top k)^\top]=C(B-S),\qquad
S^+=S+\eta z(v-S^\top k)^\top.
\]

This is an IV moment iteration. Sample \(zk^\top\) is generally nonsymmetric, so this is not ordinary per-sample MSE descent. General instruments only give \(\mathbb E[zv^\top]=MB\), \(M=\mathbb E[zk^\top]\), when the exclusion moments hold. Full rank identifies \(B\), but stability additionally requires \(\rho(I-\eta M)<1\); full rank alone is insufficient. For instance \(M=-I\) is full rank and unstable for every positive step. In the paired independent-view specialization \(M=C\), mean stability is \(0<\eta<2/\lambda_{\max}(C)\).

In both modified recurrences \(R\) or \(z\) is an actual additional input. It cannot be inferred by naming a loss. Input-dependent normalization/gating changes weighted moments: \(\mathbb E[z\epsilon^\top]=0\) does not imply \(\mathbb E[\eta(k,z)z\epsilon^\top]=0\). Learned features, temporal correlation and endogenous state feedback likewise invalidate the iid proof unless analyzed anew. Decay changes the fixed point/objective and must retain its declared chronological order.

## Exact stability separation

For a single value column, put \(E=S-B\). Both corrected recurrences have form \(E^+=A E+\eta\xi\), with

\[
\begin{array}{c|c|c}
&A&\xi\\\hline
\mathrm{BC}&I-\eta(kk^\top-R)&k\nu+(R-k\epsilon^\top)B\\
\mathrm{IV}&I-\eta zk^\top&z\nu-z\epsilon^\top B
\end{array}
\]

Here \(\mathbb E[\xi]=0\); \(A\) and \(\xi\) may be correlated. The exact homogeneous second-moment operator is \(\mathcal T(Q)=\mathbb E[AQA^\top]\), with vectorized matrix \(\mathbb E[A\otimes A]\). Its spectral radius below one gives homogeneous mean-square asymptotic stability. Forced second moments also contain \(\eta\mathbb E[A\,\mathbb E[E] \xi^\top]\) and its transpose, plus \(\eta^2\mathbb E[\xi\xi^\top]\); one cannot discard these cross terms at arbitrary finite time. Under iid independence, finite forcing second moments and the stability conditions, they decay with the mean and leave a generally nonzero stationary covariance. No claim of exact constant-step parameter recovery is made.

An explicit analytic boundary uses independent scalar Gaussian \(x,\epsilon,\delta\) with variances \(c>0,r,r'\). BC has \(h=k^2-r\), so

\[
\mathbb E[h]=c,\qquad \mathbb E[h^2]=3c^2+4cr+2r^2.
\]

This follows by expanding \(\mathbb E[k^4]=3(c+r)^2\). IV has \(h=zk\); Isserlis' identity gives \(\mathbb E[h^2]=(c+r)(c+r')+2c^2\). Since the homogeneous squared multiplier is \(1-2\eta c+\eta^2\mathbb E[h^2]\), the exact strict scalar homogeneous mean-square ranges are

\[
0<\eta<\frac{2c}{3c^2+4cr+2r^2}\quad(\mathrm{BC}),\qquad
0<\eta<\frac{2c}{3c^2+c(r+r')+rr'}\quad(\mathrm{IV}).
\]

Both are narrower than the mean range \(0<\eta<2/c\). These are derived examples, not evaluated scores or claims that IV always dominates BC. They do not transfer to arbitrary normalized neural keys. The published BC-LMS source's apparent Eq. (14) versus (15) sign mismatch is recorded in the source audit; its displayed step-size bound is not imported here.

## Parameter debiasing can increase the intended prediction risk

For a fresh independent query/target pair distributed like \((k,v)\), define \(\mathcal R(S)=\mathbb E\|v-S^\top q\|^2\). The normal equations eliminate the cross term in completing the square:

\[
\mathcal R(S)-\mathcal R(S_{\rm obs})
=\operatorname{tr}[(S-S_{\rm obs})^\top(C+R)(S-S_{\rm obs})].
\]

Thus directly reading noisy \(q\) with recovered \(B\) has nonnegative excess risk. In the scalar case it is \(B^2r^2/(c+r)\), strictly positive for \(B r\ne0\). This statement needs only second moments and best-linear-predictor comparison, not Gaussianity. Under joint Gaussian assumptions the conditional mean is exactly

\[
\mathbb E[v\mid q]=B^\top C(C+R)^{-1}q=S_{\rm obs}^\top q,
\]

so the ordinary population Delta predictor is also Bayes optimal over all measurable square-integrable predictors. Reading \(B\) through the posterior-denoised \(\mathbb E[x\mid q]\) reproduces the same predictor; it supplies no stationary accuracy improvement theorem. At a clean query \(x\), by contrast, \(B^\top x\) is the correct conditional prediction and attenuation is harmful. Different query-noise conditions can justify different calibration, but their actual observation law must be provided.

This prevents treating a statistical estimation bias as an unconditional memory failure. Noise2Noise likewise preserves the input-conditioned target mean; it does not promise an unattenuated structural matrix.

## What a single observed stream cannot identify

In the nondegenerate scalar Gaussian case, let observed moments be \(u=\operatorname{Var}k>0\), \(w=\operatorname{Var}v>0\), \(g=\operatorname{Cov}(k,v)\ne0\), and \(uw>g^2\). For every

\[
a\in[g^2/w,u],\quad
\operatorname{Var}x=a,\quad B=g/a,\quad
\operatorname{Var}\epsilon=u-a,\quad
\operatorname{Var}\nu=w-g^2/a,
\]

independent centered Gaussian components generate the identical joint law of \((k,v)\). All variances are nonnegative and each covariance is \(g\). Therefore that observed law alone cannot select the latent \(B\) or \(R\), even though its optimal observed predictor \(g/u\) is identified. This is an explicit identification counterexample, not a general impossibility result once valid extra measurements/priors are supplied.

With genuinely independent paired views, \(\mathbb E[kz^\top]=C\), hence \(R=\mathbb E[kk^\top]-C\) is identifiable at the population level even for unequal view variances. The simpler formula \(\tfrac12\mathbb E[(k-z)(k-z)^\top]=R\) additionally requires equal covariances; unequal views give \((R+R')/2\). Nonzero relevant cross-view error moments can spoil these identities; independence is sufficient, not necessary, and dependence with vanishing relevant moments need not invalidate them. Deterministic projections, dropout views and paraphrases do not automatically meet the exclusion/independence conditions.

## Delta consequences, costs and feasible discrimination

An IV edit changes any fixed query output by \(\eta(q^\top z)e\), where \(e=v-S^\top k\); BC changes it by \(\eta(q^\top k)e+\eta S^\top Rq\). Neither creates protected associations or revision evidence. Future influence still propagates through the actual ordered future transitions; the full network requires Jacobians.

Ordinary and IV state/work cost are \(O(dm)\); IV needs another observed view and, if learned, its encoder and information access. BC adds \(RS\): \(O(d^2m)\) work plus \(O(d^2)\) covariance storage for dense known \(R\), or \(O(dm)\) work and \(O(d)\) storage for a diagonal approximation. Estimating dense paired moments adds \(O(d^2)\) work/state and conditioning error. These estimates exclude source acquisition, encoding and outer training, which must be charged separately. BC updates are affine and associatively scannable when features/covariance are frozen; this is not a throughput guarantee and estimating them from state reintroduces dependency. The existing 2080Ti/0.1B/1B context establishes no memory or runtime fit here.

Native bAbI/LAMBADA measure QA or final-word prediction, not latent-key/noise identification; neither supplies the independent repeated semantic-key measurement assumed above. The pinned Noise2Noise author paths provide a legitimate denoising control and PSNR scorer, not a test of revision protection or learned latent-key \(B\). Asset acquisition and execution remain pending. Strong simple alternatives are ordinary Delta/CE, the actual conditional predictor or teacher readout, BC-LMS, IV-LMS, and appropriately modeled TLS/denoising; they do not all optimize the same object. No new benchmark, label, metric, executable matrix or model code is proposed.

**Decision:** retain this result to fix the target definition and exclude plain covariance subtraction/paired-view IV from the originality pool. Reopening requires a natural source of extra observations, a specified deployed query law, and a recurrence or guarantee substantively beyond these known methods. Those conditions are missing for the current text interface; they do not block unrelated Delta mechanisms. See [primary/source audit](../sources/NOISY_KEY_EIV_SOURCE_AUDIT.md) and [exact-byte independent review](../reviews/NOISY_KEY_IDENTIFICATION_PREDICTION_CONTROL.review.md).
