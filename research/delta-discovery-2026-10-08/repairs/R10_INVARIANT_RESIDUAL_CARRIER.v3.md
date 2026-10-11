# R10 v3: invariant residual carrier — exact closure, leakage, and a noncommuting full-width boundary

Recorded: 2026-10-11. This is a versioned child of `R10_TRANSITION_MATCHED_NOISE_SHAPING.v2.md` and the third substantive R10 repair attempt. Parent bytes, counterexamples, source audits, and reviews remain unchanged. Scope is frozen-feature Delta-state mathematics; empirical effect is unknown and no execution was performed.

## 1. Original problem and exact patch

R10 v2 transports a quantization residual through the full Delta transition

\[
A_t=(I-\beta_t k_tk_t^\top)D_t\in\mathbb R^{d\times d},
\]

which can be applied as \(A_tr=D_tr-\beta_tk_t(k_t^\top D_tr)\) but still costs a full-width residual state and its traffic. The attempted patch is a fixed rank-\(r\) carrier

\[
R_t\approx U C_t,\qquad U\in\mathbb R^{d\times r},\quad U^\top U=I_r,
\]

where columns of \(R_t\) may correspond to value coordinates. This directly tests whether the v2 residual can be compressed without changing the transition or borrowing future queries.

## 2. Exact carrier criterion

Let \(P=UU^\top\). There exists a coordinate transition \(B_t\in\mathbb R^{r\times r}\) satisfying

\[
A_t U=U B_t
\]

for every carrier coordinate if and only if

\[
L_t:=(I-P)A_tU=0. \tag{1}
\]

When (1) holds, the unique orthogonal projected core is

\[
B_t=U^\top A_tU. \tag{2}
\]

For a family \(\Omega\) of prefix-legal modes, one fixed exact carrier requires (1) for every \(\omega\in\Omega\): \(\operatorname{range}(U)\) must be a common invariant subspace. For one realized coordinate \(c\), \(L_tc=0\) is enough; that pathwise fact must not be promoted to invariance for every residual.

For a nonorthonormal full-column basis, the corresponding formulas use \(P=UU^\dagger\) and \(B=U^\dagger AU\). Conditioning of \(U^\top U\) then becomes an additional numerical cost.

## 3. Delta-order-preserving core and leakage

Substituting the actual ordered Delta transition gives

\[
B_t=U^\top D_tU-\beta_t(U^\top k_t)(k_t^\top D_tU), \tag{3}
\]

\[
L_t=(I-P)D_tU-\beta_t(I-P)k_t(k_t^\top D_tU). \tag{4}
\]

Equation (4) retains the required order: \(D_t\) acts before the rank-one erase. If \(D_tU\subseteq\operatorname{range}(U)\), then

\[
L_t=-\beta_t(I-P)k_t(k_t^\top D_tU),
\]

and

\[
\|L_t\|_2=|\beta_t|\,\|(I-P)k_t\|_2\,\|k_t^\top D_tU\|_2. \tag{5}
\]

For \(\beta_t\ne0\), exactness in this restricted case holds if and only if either \(k_t\in\operatorname{range}(U)\) or \(k_t^\top D_tU=0\). Without \(D_t\)-invariance, the two terms in (4) may cancel; treating their separate vanishing as necessary would be wrong. A safe general bound is

\[
\|L_t\|_2\le \|(I-P)D_tU\|_2+|\beta_t|\,\|(I-P)k_t\|_2\,\|k_t^\top D_tU\|_2. \tag{6}
\]

## 4. Exact approximate-carrier error recurrence

Let the full residual obey

\[
R_t=A_tR_{t-1}+Z_t,
\]

and let the compressed recursion be

\[
C_t=B_tC_{t-1}+U^\top Z_t,\qquad \widehat R_t=UC_t.
\]

With \(E_t=R_t-\widehat R_t\), direct substitution yields the exact identity

\[
E_t=A_tE_{t-1}+L_tC_{t-1}+(I-P)Z_t. \tag{7}
\]

Writing \(\Phi_{t:i}=A_tA_{t-1}\cdots A_i\) and \(\Phi_{t:t+1}=I\),

\[
E_t=\Phi_{t:1}E_0+\sum_{i=1}^t\Phi_{t:i+1}\left[L_iC_{i-1}+(I-P)Z_i\right]. \tag{8}
\]

Therefore, with \(a_j=\|A_j\|_2\),

\[
\|E_t\|_2\le
\left(\prod_{j=1}^t a_j\right)\|E_0\|_2+
\sum_{i=1}^t\left(\prod_{j=i+1}^t a_j\right)
\left(\|L_i\|_2\|C_{i-1}\|_2+\|(I-P)Z_i\|_2\right). \tag{9}
\]

If \(a_j\le\rho<1\), \(\|L_j\|\le\epsilon\), \(\|C_j\|\le M\), and \(\|(I-P)Z_j\|\le\delta\), then

\[
\|E_t\|\le \rho^t\|E_0\|+(\epsilon M+\delta)\frac{1-\rho^t}{1-\rho}. \tag{10}
\]

At \(\rho=1\), the corresponding bound is linear in \(t\). Delta form alone does not imply contraction. Coordinate quantization contributes a decoded defect inside (7); ambient elementwise quantization may leave the carrier immediately and belongs in \((I-P)Z_t\).

## 5. Minimal exact carrier and noncommuting full-width witness

For an initial column span \(V_0\), a declared legal mode family \(\Omega\), and a declared family \(\mathcal Z\) of admissible injection column spans, first define the seed

\[
V_{\rm seed}=\operatorname{span}\left(V_0\cup\bigcup_{Z\in\mathcal Z}\operatorname{range}(Z)\right).
\]

The minimal fixed exact carrier for those reachable affine residual trajectories is the invariant hull

\[
\mathcal K=\operatorname{span}\{A_{\omega_h}\cdots A_{\omega_1}v:
v\in V_{\rm seed},\ h\ge0,\ \omega_j\in\Omega\}. \tag{11}
\]

Taking \(U\) as a basis of \(\mathcal K\) gives exact fixed compression of the declared reachable trajectories, and the minimum width is \(\dim\mathcal K\). A larger carrier containing \(\mathcal K\) is exact for every coordinate in that larger carrier only if it is itself common invariant. If injections are unrestricted, their seed span is already full and no nontrivial exact carrier follows.

The hull can be full even though each Delta correction is rank one. Let \(d\ge2\), \(D=I_d\), \(\beta\in(0,1]\), \(a>0\), \(v=\mathbf1_d\), and

\[
k_i=\frac{e_i+a\mathbf1_d}{\|e_i+a\mathbf1_d\|},\qquad
A_i=I-\beta k_ik_i^\top,\quad i=1,\ldots,d. \tag{12}
\]

The unnormalized key matrix is \(I+a\mathbf1\mathbf1^\top\), whose determinant is \(1+ad>0\); hence the keys span \(\mathbb R^d\). Also \(k_i^\top v>0\). If a fixed carrier contains \(v\) and is invariant under every \(A_i\), then

\[
v-A_iv=\beta k_i(k_i^\top v)\in\operatorname{range}(U),
\]

so every \(k_i\) lies in the carrier and \(r=d\). For \(i\ne j\), these keys are nonorthogonal and noncollinear, and

\[
[A_i,A_j]=\beta^2(k_i^\top k_j)(k_ik_j^\top-k_jk_i^\top)\ne0. \tag{13}
\]

Thus a legal noncommuting rank-one Delta family can force a full-width robust common carrier. This is a worst-case common-carrier statement, not a claim that every realized sequence needs width \(d\).

## 6. Old counterexamples rechecked and new failure boundaries

1. **v1 same-bit boundary remains.** A finite tuple \((W,U,C,\text{metadata})\) is an augmented finite-state code. A direct controller with the same total state and transition can simulate it; naming \(C\) a residual does not create capacity.
2. **v2 residual-law boundary remains.** Deterministic clipping/rounding makes defects endogenous to feedback. Equations (7)–(10) are pathwise, but covariance/spectral optima still require an exogenous or policy-invariant law.
3. **New defects need not stay low rank.** For
   \[
   X=\begin{bmatrix}0.2&0.4\\0.4&0.8\end{bmatrix},
   \quad Q(X)=\begin{bmatrix}0&0\\0&1\end{bmatrix},
   \]
   \(X\) has rank one whereas \(X-Q(X)\) has determinant \(-0.20\) and rank two. Rank-one Delta transport preserves the rank of an existing factor only up to singular loss; it does not make newly injected elementwise quantization residuals low rank.
4. **Moving bases are an escape, not a free result.** A thin QR of \(A_tU_{t-1}=U_tR_t\) can transport a rank-\(r\) column space exactly along one realized path. But \(U_t\) is then runtime state: storing/reading it costs \(O(dr)\), applying \(A_tU\) costs \(O(dr)\), and reorthogonalization costs about \(O(dr^2)\). A direct low-rank augmented-state baseline gets the same factors and operations.
5. **Prefix lawfulness.** A fixed carrier may be outer-trained or derived from a declared ex ante mode set. Choosing it from future keys, future query Gramians, residual spectra, or the realized suffix leaks future information. Expanding after an unseen key does not undo leakage already incurred without retaining the missing state/history.
6. **Frozen-path scope.** \(A_t\) is only the held-feature left-state transition. In the full network, memory perturbations alter later \(k,q,v,\beta,D\), updater state, and possibly the basis. Claims beyond the frozen path require the full coupled Jacobian plus nonlinear remainder.

## 7. Costed comparison and predictions

The carrier stores \(r\) coordinates per residual column only if \(U\) is fixed and shared. Dense projection/reconstruction costs \(O(dr)\) per column; for token-varying diagonal \(D_t\), forming a generic dense \(U^\top D_tU\) costs \(O(dr^2)\) and applying the core to \(m\) residual columns costs \(O(r^2m)\). A moving dense basis additionally carries \(dr\) values plus gauges/scales and QR updates. Exact full residual Delta transport is only \(O(d)\) per column because \(A_tr=D_tr-\beta k(k^\top D_tr)\). Therefore lower state width does not imply lower traffic or compute.

Required same-information controls are: direct projected residual with the same \(U\); direct low-rank augmented recurrent state with the same factors; same-total-bit main-state/full-residual coding including scales and saturation metadata; classical dithered/error-feedback quantization; and low-rank truncation under the same rank and compute budget.

Falsifiable conditional predictions are limited:

- leakage is zero precisely under (1), and under \(D_t\)-invariance follows the factorized test (5);
- for a declared mode family, required exact width equals the invariant-hull dimension (11);
- when \(\rho<1\), bounded leakage/injection produces the floor in (10), while \(\rho\ge1\) has no such conclusion;
- a moving-basis method can beat a fixed carrier only after charging basis state, traffic, factor quantization, saturation, and basis-update cost.

## 8. Nearest work, measurement, and disposition

Common invariant subspaces, switched reachability/invariant hulls, projection/model reduction, and dynamic compensator/state augmentation are established. The exact carrier theorem strongly collides internally with R09 robust carriers and R16/R18 spectral/quotient closure. Classical error-spectrum shaping, fixed-rate error feedback, graph quantitative error feedback, recurrent residual write-back, DAMP, and STEPQuant already cover the adjacent quantization mechanisms. The Delta specialization and explicit noncommuting witness are useful debugging results, not evidence of a new updater.

Existing bAbI, LAMBADA, RULER, reasoning, and code-task native scores measure endpoints but do not expose carrier containment, residual tail rank, basis bytes/traffic, saturation, matched augmented-state capacity, or fact validity. STEPQuant remains the closest pinned author interface, but its released path is not an affordable native mechanism object for the retained single-RTX-2080-Ti background. No benchmark, label, metric, case, or result was invented.

**Disposition:** conditional mathematics accepted as a boundary/debug theorem; contribution has major common-invariant-subspace/model-reduction and internal R09/R16/R18 collisions; measurement remains open; empirical effect is unknown; candidate delta is 0. R10 is parked after attempt 3/3. Reopen only with a natural prefix-lawful restricted mode family whose small carrier is proved, a matched-total-storage/traffic/compute advantage over direct projected/augmented state, controlled new-defect tail and saturation, and a native measurement object.
