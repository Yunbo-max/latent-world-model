# Independent KDN source reading for D03 review

Reader: /root/delta_math_review_b, 2026-10-08 UTC, Web mathematical/source inspection only. No project code, scorer, or oracle was executed.

The primary PDF at https://arxiv.org/pdf/2609.07816 resolves to arXiv2609.07816v2, dated29 September2026, as its page0 footer states. The v1 HTML/PDF locators failed in this reading; do not mislabel the inspected formulas as v1.

## Formal object and exact versus approximation

In §§3.1–3.2, memory is the posterior mean of a latent key-by-value Gaussian map. Conditional on supplied transition, noise and key quantities, independent process/observation noise gives the Kalman prediction Phat=D P D^T+Omega and mean Shat=D S. The residual e=v−Shat^T k is written with gain kappa=Phat k/(r+k^T Phat k); posterior covariance is (I−kappa k^T)Phat. This follows ordinary Gaussian conditioning, not future-query risk minimization.

In §4.1, a diagonal predictive covariance gives the exact one-step posterior mean conditional on that diagonal prior. Reverse-KL projection onto diagonal Gaussian laws retains this mean, and gives posterior diagonal entries p_i=(phat_i^-1+k_i²/r)^-1. This is not the dense filter's exact posterior after a sequence of approximating projections. Information scaling mu multiplies the posterior precision increment after forming the current gain; it changes later writes without changing the already-formed current write.

For D03, a matrix of conditional future transported query sensitivity is not posterior covariance. Both lead to variable write directions and normalized matrix-vector gains; merely using a matrix-valued gain is already covered. The remaining proposed distinction must be the estimand, causal predictor/targets, and the resulting ordered-transport risk—not a renamed Kalman preconditioner.

## Actual author source pin

Repository ngocbh/kalman-delta-networks, literalmain commit53e437be8591521a508bb6a04cd5b26594a3d5ec. Exact Git blob0e1d77dac63a350c659825cfa393969b4e51c958 at lit_gpt/kdn_ops/diag_kdn_naive.py was read through the GitHub connector. Full author bytes are retained in scratch as KDN_AUTHOR_NAIVE_PINNED.txt solely for reading and identity checks, and are not part of the published mathematical packet. Its Git object identity was recomputed from exact bytes; SHA25687876ebe27fb175685548b7d8d59ad83e5c3e04164be78b4366f2a7ea226327d. The published packet retains this source locator, audit, and compact source manifest rather than a vendored code copy.

- diag_kdn_gain_naive inputs k/alpha/omega[B,T,H,K], r[B,T,H], positive initial_precision scalar/[H]/[B,H]/[B,H,K], positive per-head info_scale; gains[B,T,H,K], optional finalprecision[B,H,K].
- The recurrence predicts covariance using alpha² and omega, forms normalized gain, and then applies the information-scaled coordinate posterior update. Default info_scale is K.
- naive_recurrent_diag_kdn also accepts q[B,T,H,K], v[B,T,H,V], optional memory[B,H,K,V]. It decays memory, reads the current-key innovation, updates with the gain, then reads output with q; final state includes both memory and precision for continuation.
- The oracle computes float32 unless any input/state is float64; q/v output is cast to v's dtype. Normalization/projection frontends are outside this oracle.
- A separate private chunk oracle composes per-coordinate Mobius maps in actual order and uses the affine-memory WY transform. Thus KDN offers an existing practical parallel gain baseline; D03 cannot claim its dense learned metric has the same scan structure without proof.
- I inspected only this recurrence oracle, not the complete production kernels or layer frontend. No performance, correctness-test, or hardware-compatibility claim follows.

The author README identifies release qualification on H200, Python3.11, PyTorch2.8/CUDA12.8/BF16. This is author-stated release scope, not evidence of RTX2080Ti compatibility. Such compatibility is pending future Local acceptance and is out of this mathematical stage.

Primary locators: https://arxiv.org/pdf/2609.07816 ; https://github.com/ngocbh/kalman-delta-networks/blob/53e437be8591521a508bb6a04cd5b26594a3d5ec/lit_gpt/kdn_ops/diag_kdn_naive.py .

