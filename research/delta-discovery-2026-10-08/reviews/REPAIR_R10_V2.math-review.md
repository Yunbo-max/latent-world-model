# Independent mathematical review — R10 v2

- Reviewer identity: `/root/r10_v2_math_review`
- Assignment: dimension, order, finite-horizon risk, uniqueness, scalar stationary/spectral formulas, finite residual coding, and limiting cases; read-only; no project execution.
- Final artifact: `repairs/R10_TRANSITION_MATCHED_NOISE_SHAPING.v2.md`
- Final artifact SHA256: `3a9e0c3a185d0f1c0a5724b59a30063963794576f516e4f77ee3f63e71f21d08`
- Source audit SHA256 observed: `a09c1dd2dd1a14fa6436428f45e175468ad3dcd659ddeff5a99ac49c7f444781`
- Verdict: **PASS as a conditional theorem/debugging control; not method admission.**

## Review reasoning

The first review of SHA256 `f4cc8bbe...` returned REVISE: the actual residual `r_t=z_t-Q_t(z_t)` generally changes with feedback `F`, so zero mean and temporal decorrelation alone did not justify optimizing `F` while holding `Sigma_t` or `S_r` fixed. The final artifact now explicitly assumes a common exogenous / `F`-invariant residual law for cross-feedback comparisons and downgrades deterministic deployed quantization to a conditional surrogate. It also corrects the overstrong statement that exact cancellation requires `h=0`: propagated/readout nullspaces can annihilate `A_t h_{t-1}`.

On the final bytes, equations (2)–(15) were rechecked. Dimensions, ordered products, trace-risk decomposition, positive-definite and singular uniqueness statements, scalar trace projection, the `|a|<1` stationary result, one-lag spectral ratio, and finite residual defect recurrence are consistent. The explicit capacity-versus-implementation qualifier does not change the proof.

## Conditions that remain open

- full state-dependent nonlinear Delta dynamics need the coupled Jacobian;
- future Gramian/spectrum are not lawful prefix deployment oracles;
- deterministic saturation/endogenous residual laws can change the optimum;
- conditional quadratic risk is not semantic validity or empirical benefit.

