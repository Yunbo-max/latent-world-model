# NOGO-DUAL-FRAME-04 — redundant frames cannot repair endogenous Delta forgetting

Disposition: **accepted no-go/finite-precision control; not a candidate**.

Let \(S\in\mathbb R^{d\times p}\), \(F\in\mathbb R^{r\times d}\) have full column rank, and \(G=F^\dagger=(F^\top F)^{-1}F^\top\), so \(GF=I\).  Store \(Z=FS\) and read

\[
o(q)=Z^\top G^\top q.
\]

The exact frame-coded Delta recurrence is

\[
\bar Z=FDGZ,\quad e=v-\bar Z^\top G^\top k,
\quad Z^+=\bar Z+\beta(Fk)e^\top.
\]

On the code subspace this is exactly \(F[(I-\beta kk^\top)DS+\beta kv^\top]\): encoded write is \(Fk\), encoded erase covector is \(G^\top k\), and no memory law changes.

## Redundancy dichotomy

The identity \(GF=I\) requires \(r\ge d\).  If \(r=d\), \(F\) is invertible and this is only a coordinate conjugacy, with no syndrome space.  If \(r>d\), the stored state grows from \(dp\) to \(rp\) scalars.  Legal codewords still have \(dp\) logical degrees of freedom; extra coordinates are physical redundancy rather than semantic capacity.

For any parity operator \(H\) with \(HF=0\), every endogenous Delta forgetting/interference perturbation is \(F\delta S\), hence

\[
HF\delta S=0.
\]

It remains a valid codeword.  A frame syndrome can detect off-code numerical corruption, not the recurrence's own altered state.

## Exogenous noise bound and its price

With independent encoded additive noise of variance \(\sigma^2\) per entry, one injected error transported by the actual frozen future product \(P\) has per-value-coordinate query variance

\[
\sigma^2q^\top P(F^\top F)^{-1}P^\top q.
\]

For unit-norm frame rows, \(\operatorname{tr}(F^\top F)=r\), so worst unit effective-direction variance is at least \(\sigma^2d/r\), with equality for a unit-norm tight frame.  The factor \(r/d\) reduction pays \(r/d\) more stored coefficients and more total frame energy; under fixed total energy it disappears.  The canonical dual is PSD-optimal only among exact linear left inverses under isotropic noise.

Known-coordinate erasures are exactly recoverable iff the retained-row subframe has rank \(d\); robustness is governed by its smallest singular value.  These are classical real-frame/error-correcting-code properties, not protection from Delta's semantic update.

At a fixed total \(B\)-bit budget, extra coefficients receive fewer bits.  Under a simple equal-range dithered model, a tight frame's variance relative to a square orthogonal code scales as

\[
\frac dr\,2^{2B(1/d-1/r)},
\]

which may be worse.  General rate-distortion conclusions still require a source model.

## Deployability and metric collapse

To retain a diagonal encoded decay for every diagonal \(D\), require \(FD=\widetilde DF\) with diagonal \(\widetilde D\).  Rowwise, arbitrary unequal diagonal entries force each row of \(F\) to support at most one original coordinate.  The only exact cheap frames are coordinate scalings/repetitions; a mixing frame needs dense decode--gate--encode work, typically \(O(rdp)\) per token.

For a positive-definite query Gramian \(W\), optimizing the frame operator \(M=F^\top F\) under \(\operatorname{tr}M=r\) gives

\[
M^*=\frac{rW^{1/2}}{\operatorname{tr}W^{1/2}},
\qquad
\min\operatorname{tr}(WM^{-1})=
\frac{(\operatorname{tr}\sqrt W)^2}{r}.
\]

This is query-aware transform/bit allocation and overlaps D05/STEPQuant/PDN.  If \(W\) is singular, the expression is only an unattained SPD infimum without a spectral floor.  Time-varying \(W_t\) additionally requires re-encoding old state.

Classical nearest work includes quantized/tight frames with erasures, numerically erasure-robust frames, and real-valued error-correcting codes.  The Delta-specific residual is fully covered by wider-state accounting and the existing quantization/metric controls.  No active candidate survives.

No project code, test, model, benchmark, download or experiment was executed.
