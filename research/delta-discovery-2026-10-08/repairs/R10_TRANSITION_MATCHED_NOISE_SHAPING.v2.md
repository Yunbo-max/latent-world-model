# R10 v2: transition-matched residual feedback — exact finite-horizon risk and the equal-state boundary

Status: repair attempt 2 of at most 3. Versioned child of `repairs/R10_EQUAL_BIT_TRANSPORTED_RESIDUAL.v1.md`; the parent bytes, counterexamples, reviews, and source record remain unchanged. This artifact contains mathematics and source/measurement reasoning only. No project code, software test, model execution, training, inference, scoring, or benchmark result was produced.

## 1. Original problem, exact failure, and preserved conclusions

R10 v1 established two facts that this child does not revoke.

1. If a stored pair `(W,C)` is consumed only through the decoded sum `L=W+C`, then its at-most `2^(b_W+b_C)` decoded values can be reproduced by a direct equal-cardinality state codebook. Splitting digits is therefore not a free capacity gain.
2. If the recurrent kernel sees only coarse `W` and uses `C` to alter later write timing, the method has changed the transition operator. It may exploit interface compatibility, but it no longer follows from the exact transported-sum identity and an arbitrary direct finite-state comparator can relabel the pair state.

The unclosed possibility was narrower: perhaps temporal correlation and the Delta transition make a transported feedback coefficient mathematically preferable even when no capacity claim is made. V1 mentioned correlated defects only as a failure boundary and did not derive the corresponding optimal feedback law. This child patches that omission.

The failure type remains **known-mechanism collision plus budget/target mismatch**, not incorrect v1 algebra. The retained exact finite-bit recurrence is still

\[
E_t=A_tE_{t-1}+d_t
\]

for a decoded transported split with residual-quantization defect `d_t`. The new result below concerns a different but explicit operator: feeding the previous quantization residual into the next proposal.

## 2. Formal object and update

First freeze an affine suffix and its quantizer interface:

\[
x_t=A_t x_{t-1}+b_t,
\qquad
z_t=A_t\hat x_{t-1}+b_t+F_t r_{t-1},
\qquad
\hat x_t=Q_t(z_t)=z_t-r_t. \tag{1}
\]

Here `x_t, \hat x_t, r_t \in R^d`, `A_t,F_t \in R^{d\times d}`, and `r_t` is the actual post-quantization residual of the deployed proposal. Set `e_t=x_t-\hat x_t`, `e_0=r_0`, and take `r_{-1}=0`. Subtraction gives the exact actual-update field

\[
e_t=A_t e_{t-1}-F_t r_{t-1}+r_t. \tag{2}
\]

No stochastic assumption is used in (2). For ordered products

\[
P_{u:i+1}=A_uA_{u-1}\cdots A_{i+1},\qquad P_{i:i+1}=I,
\]

induction yields

\[
e_u=r_u+\sum_{i=1}^{u}P_{u:i+1}(A_i-F_i)r_{i-1}. \tag{3}
\]

Thus `F_i=A_i` is not a heuristic coefficient: it cancels every older residual contribution in the frozen affine comparison and gives `e_u=r_u` for all `u`. For a Delta step,

\[
A_i=(I-\beta_i k_i k_i^\top)D_i,
\]

transition-matched feedback must preserve this order. Applying it to a residual is another Delta-like matrix-vector/matrix-state action; replacing it by the identity is exact only when the relevant residual directions satisfy `(A_i-I)r_{i-1}=0`.

## 3. Finite-horizon query-risk theorem

Let declared future linear reads be `C_u e_u`, and define

\[
\mathcal R(F_{1:T})=\mathbb E\sum_{u=1}^{T}\|C_u e_u\|_2^2. \tag{4}
\]

Assume, conditional on the frozen suffix, that residuals are zero mean and temporally uncorrelated,

\[
\mathbb E[r_i r_j^\top]=0\quad(i\ne j),
\qquad \mathbb E[r_i r_i^\top]=\Sigma_i\succeq0. \tag{5}
\]

For comparisons across different feedback matrices, additionally assume a common exogenous residual coupling: the joint residual law and hence every `\Sigma_i` are invariant to the compared `F_i`. A non-overloaded subtractive-dither model is one possible declared interface. Without this invariance, the following expression still evaluates risk for a fixed residual law, but its minimizer is only a conditional surrogate because the residual of a deterministic quantizer generally changes when `F` changes.

Substitution of (3) into (4) removes cross-time terms and gives

\[
\mathcal R
=\sum_{u=1}^{T}\operatorname{tr}(C_u\Sigma_u C_u^\top)
+\sum_{i=1}^{T}\operatorname{tr}\!\left[
G_i(A_i-F_i)\Sigma_{i-1}(A_i-F_i)^\top
\right], \tag{6}
\]

where

\[
G_i=\sum_{u=i}^{T}P_{u:i+1}^\top C_u^\top C_uP_{u:i+1}\succeq0. \tag{7}
\]

Consequently, under the common residual-law coupling, unrestricted transition-matched feedback `F_i=A_i` is a global minimizer of the declared quadratic risk. It is unique exactly on the jointly visible/noisy subspace: every minimizer satisfies

\[
G_i^{1/2}(A_i-F_i)\Sigma_{i-1}^{1/2}=0. \tag{8}
\]

If both `G_i` and `\Sigma_{i-1}` are positive definite, `F_i=A_i` is unique. If either is singular, feedback may differ from `A_i` on directions that are unexcited or invisible to the declared reads. This is a weighted least-squares projection, not a semantic-validity certificate.

For a scalar-restricted coefficient `F_i=f_i I`, expansion of (6) yields, when `tr(G_i\Sigma_{i-1})>0`,

\[
f_i^*=\frac{\operatorname{tr}(G_iA_i\Sigma_{i-1})}
{\operatorname{tr}(G_i\Sigma_{i-1})}. \tag{9}
\]

This may fall outside a hardware-imposed interval; a constrained scalar coefficient is its projection onto that interval because the objective is quadratic. Equation (9) also exposes the information burden: exact calibration needs a future readout Gramian and residual covariance, not only the current Delta key.

### Scalar stationary corollary

For constant `a` with `|a|<1`, scalar `f`, identity readout, and an `f`-invariant iid residual process of variance `\sigma^2`, the stationary risk is

\[
J(f)=\sigma^2\left[1+\frac{(a-f)^2}{1-a^2}\right]. \tag{10}
\]

Thus `f=a` attains `J(a)=\sigma^2`, while no feedback gives `J(0)=\sigma^2/(1-a^2)`. Unchanged unit feedback gives `J(1)=2\sigma^2/(1+a)` when `-1<a<1`; it is close to transition matching only near `a=1` and can be much worse for other poles.

## 4. Correlated residuals: the exact spectral boundary

Temporal correlation invalidates (6), rather than merely changing a constant. In the mean-square-stable scalar stationary case `|a|<1`, with a residual power spectrum `S_r(\omega)` held fixed across the compared coefficients and a nonnegative declared frequency weight `W(\omega)`, (2) has transfer function

\[
H_f(e^{i\omega})=
\frac{1-fe^{-i\omega}}{1-ae^{-i\omega}}. \tag{11}
\]

Define

\[
K_0=\frac1{2\pi}\int_{-\pi}^{\pi}
\frac{W(\omega)S_r(\omega)}{|1-ae^{-i\omega}|^2}\,d\omega,
\]

\[
K_1=\frac1{2\pi}\int_{-\pi}^{\pi}
\frac{W(\omega)S_r(\omega)\cos\omega}{|1-ae^{-i\omega}|^2}\,d\omega. \tag{12}
\]

When `0<K_0<\infty`, the risk is

\[
J(f)=K_0(1+f^2)-2K_1f,
\qquad f^*=K_1/K_0. \tag{13}
\]

White residuals with constant frequency weight give `K_1=aK_0`, recovering `f^*=a`. Residual energy concentrated near zero frequency drives `f^*` toward `1`; alternating/high-frequency residuals can move it toward `-1`. This is the cleanest falsifiable consequence of correlation. It also shows why a universal `F=A` claim would be false once the residual law and downstream frequency weighting change.

## 5. Finite residual storage restores the v1 defect

The optimality above assumes that the actual `r_{t-1}` is available. If only a quantized residual

\[
c_{t-1}=r_{t-1}-h_{t-1}
\]

is stored and (1) uses `F_t c_{t-1}`, then

\[
e_t=A_t e_{t-1}-F_t r_{t-1}+F_t h_{t-1}+r_t. \tag{14}
\]

For `F_t=A_t`, the mismatch `g_t=e_t-r_t` obeys

\[
g_t=A_tg_{t-1}+A_t h_{t-1}. \tag{15}
\]

Therefore finite residual coding simply creates a new transported defect. Exact cancellation on declared reads is recovered only when every injected `A_t h_{t-1}` vanishes after the relevant ordered propagation/readout; `h=0` is a sufficient full-state condition, but not necessary when the transition or declared reads have nullspaces. Achieving the full-state condition again costs an exact residual or an equivalent code. A purported gain must include residual bits, scales, lookup tables, feedback arithmetic, traffic, and saturation behavior.

The v1 cardinality theorem still applies: a finite pair state `(\hat x_t,c_t)` with at most `2^B` joint states can be relabeled as one `B`-bit finite-state code. This relabeling is an information-capacity control, not by itself an efficient static-codebook implementation or an equal-arithmetic/traffic baseline. A benefit over a *memoryless numeric quantizer* can be real, but it is then a transition/decoder-class benefit, not an information-capacity escape. Fair evaluation therefore needs both the direct `2^B`-state machine with the same metadata and allowed transition logic and computable matched-storage/traffic/operation predictors or quantizers that expose which interface restriction matters.

## 6. Old counterexamples and new failure boundaries

Old counterexamples remain:

- unchanged compensation does not transport the residual through `A_t`;
- an exact transported residual is another full state;
- decoded-sum split coding is contained in an equal-cardinality direct codebook;
- separate future reads of the pair leave the decoded-sum theorem but retain the finite-state relabeling bound.

New boundaries:

- equations (6)–(10) require a frozen/exogenous suffix and temporally uncorrelated residuals; deterministic rounding can violate both;
- comparing different feedback coefficients additionally requires an `F`-invariant residual coupling; with an ordinary deterministic quantizer, `r_t=z_t-Q_t(z_t)` is endogenous to `F_t`, so (6), (9), (10), and (13) are conditional surrogate optima rather than global deployed-quantizer optima;
- equation (13), not `f=a`, governs a declared correlated stationary scalar law;
- state-dependent keys/gates/values require the full nonlinear coupled Jacobian, so `A_t` from a frozen path is not a whole-network optimal controller;
- `G_i` uses future reads and cannot be a prefix-only deployment oracle without a lawful estimator and transfer assumption;
- saturation makes the residual law state dependent and can destabilize the feedback loop;
- an unrestricted full `F_t=A_t` action costs another transition of the residual, while a diagonal/scalar/rank-limited `F_t` is only a weighted projection;
- quadratic output risk does not identify which facts remain valid or authorize release/overwrite.

## 7. Predictions, controls, and measurement

Conditional predictions:

1. Under a non-overloaded subtractive-dither-like coupling that keeps the iid residual law fixed and a stable frozen scalar path, the risk curve in `f` is quadratic with minimum at the actual Delta pole `a`; unit feedback should lose increasingly as `a` departs from one.
2. Holding the pole and residual-law coupling fixed while shifting residual spectral mass from low to high frequency should move the best scalar coefficient from positive toward negative according to (13), not according to a fixed decay score.
3. Quantizing the residual should introduce the new propagated defect (15); any advantage should shrink with residual-code distortion and can reverse under saturation.
4. If an arbitrary equal-state finite-state comparator with the same transition metadata matches the split system, the observed benefit was due to a restricted numeric/interface comparator rather than extra retained information.

Strong controls are: direct equal-cardinality finite-state relabeling; optimized direct state quantization; no feedback; unit feedback; transition-matched feedback; stochastic/subtractive-dither quantization where lawful; DAMP/STEPQuant lifetime allocation; the recurrent-state residual/direction-memory operator; and the closest state-space/graph-filter quantitative error-feedback rule.

Existing downstream bAbI, LAMBADA, RULER, reasoning, and code-generation tasks can measure endpoint behavior of an implemented quantized recurrence, but they do not natively expose `r_t`, its spectrum, `G_i`, `F_i`, the equal-state transition class, or semantic validity. The public graph-filter work measures native graph-filter output noise, not Delta language-memory utility. Hence the theorem is mathematically falsifiable, but an affordable native Delta measurement object remains missing. No benchmark, sample, label, metric, or result is invented here.

## 8. Closest work and disposition

The mathematical mechanism is not new. Classical error-spectrum shaping in state-space digital filters already optimizes feedback of roundoff error. Zheng et al. derive explicit output-noise quadratics and closed-form diagonal feedback coefficients for deterministic/random/asynchronous graph filters; for diagonal `D` their displayed deterministic FIR term is `tr(GS^2)+tr(GD^2)-2tr(GSD)`, directly paralleling the weighted projection in (6)–(9). Ohno et al. analyze a static uniform quantizer with a strictly causal error-feedback filter, downstream output MSE, fixed quantization bits/dynamic range, negligible-overload assumptions, and frequency-domain filter optimization. The recent recurrent-state write-back paper covers coarse-visible residual and direction memory, while DAMP and STEPQuant cover persistence/readout-aware allocation.

What remains useful is a Delta-specific debugging theorem: transition-matched feedback exactly cancels old residual propagation on a frozen affine path, scalar restrictions are Gramian/covariance projections, and correlated residuals move the optimum by a weighted one-lag spectral ratio. This is a **known-mechanism specialization/control**, not an admitted method.

- Mathematical status: conditional theorem/control; requires independent final-byte review.
- Contribution status: major collision with state-space error-spectrum shaping and quantitative graph-filter error feedback, in addition to the v1 write-timing/allocation collisions.
- Empirical status: unknown; no execution occurred.
- Candidate admission: 0.
- Disposition: **park after repair attempt 2**.

Reopen a third attempt only with a genuinely Delta-specific consequence not already implied by general state-space error feedback—for example, a noncommuting low-rank feedback construction whose matched-total-cost advantage follows from the Delta factorization, together with a lawful prefix estimator and an existing native measurement object. Another scalar coefficient, residual bit split, or offline spectral fit is insufficient.
