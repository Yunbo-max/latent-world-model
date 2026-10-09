# Pseudospectral / Kreiss transient Delta control

Disposition: **rejected as a distinct candidate; retained as a scoped transient-growth diagnostic**. Mathematics/source analysis only; no project execution.

## Correct object and vacuous standard case

For frozen features, old-state perturbations obey

\[
E_t=A_tE_{t-1},\qquad
A_t=(I-\beta_tk_tk_t^\top)D_t.
\]

If (D_t) is diagonal contractive and (0\le\beta_t\|k_t\|^2\le2), then

\[
\|A_t\|_2\le1,
\qquad
\|A_t\cdots A_s\|_2\le1.
\]

For the discrete Kreiss constant

\[
K(A)=\sup_{|z|>1}(|z|-1)\|(zI-A)^{-1}\|_2,
\]

the Neumann bound plus the (z\to\infty) limit gives (K(A_t)=1). A per-token Kreiss penalty is therefore constant on the standard legal Delta/GDN path. It cannot diagnose forgetting: nonexpansion is not information retention.

## Why the time-varying extension fails

Kreiss theory controls powers of one fixed matrix, not a token-varying ordered product. Per-factor spectra, singular values and Kreiss constants do not determine order. With (N=e_1e_2^\top), (N^2=0), and

\[
A_\pm=a(I\pm mN),\quad 0<a<1,
\]

the two factors have matched local spectral data, yet

\[
A_-A_+=a^2I,
\qquad A_+^2=a^2(I+2mN).
\]

Only the actual product distinguishes cancellation from shear. In a nonlinear network the relevant quantity is the full state Jacobian, not merely the frozen (A_t) path.

Executable replacements all collapse to known controls:

- recent-window (\max_h\|A_t\cdots A_{t-h+1}\|_2): product/Jacobian spectral regularization;
- a recent-window monodromy Kreiss constant: certifies periodic repetition of that window, not the unseen suffix;
- (A^\top H A\preceq\gamma^2H) uniformly over tokens: common/path-complete Lyapunov or joint-spectral-radius control; whitening is spectral norm/preconditioning;
- future expected product risk: D03 future-observability with worst-case operator weighting;
- unconstrained time-varying (H_t): the already rejected metric-laundering loophole.

Pseudospectral analysis remains useful for oblique QED/GDN2 factors where (\rho(A)<1<\|A\|_2), but it only diagnoses repeated local shear. Suppressing that shear can also remove useful non-normal computation.

## Sources, cost and measurement

Apkarian--Noll (arXiv:1910.12572) covers Kreiss optimization; Mitchell (SIAM J. Matrix Anal. Appl. 2020, DOI 10.1137/19M1275127) gives expensive global algorithms; Ahmadi et al. cover joint spectral radius/path-complete Lyapunov functions; Kerg et al. show useful non-normal RNN transients. PDN/RLS occupy the surviving preconditioned implementation; QED supplies the oblique shear case.

Exact dense Kreiss optimization is far above Delta's fused recurrence cost; a complex grid still needs repeated resolvent/singular-vector solves and is not a certificate. Direct product/JVP norm estimation is the stronger simple baseline. bAbI, LAMBADA or generic recall scores cannot identify this internal mechanism, so the measurement gap remains.

**Ruling:** vacuous on standard normalized Delta and noncompositional on the time-varying path; no D-number.
