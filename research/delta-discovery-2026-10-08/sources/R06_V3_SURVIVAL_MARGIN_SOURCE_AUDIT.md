# R06 v3 survival-margin source and novelty audit

Status: primary-paper/formula/author-interface audit for the third bounded R06 repair; no code or benchmark execution. Search/read cutoff: 2026-10-10 UTC.

## Reused primary sources and exact scope

- **[DeltaNet / fast-weight programmer](https://arxiv.org/abs/2102.11174)**, Schlag, Irie and Schmidhuber, arXiv:2102.11174v3, section 4 equations 23--25 and appendix A.1. This is the retained source for the residual correction update. It supports the recurrence, not the new audit target or a positive survival floor. Its feature normalization is not unconditionally the unit-L2 assumption used by the simplest v3 parameterization.
- **[Parallelizing Linear Transformers with the Delta Rule](https://arxiv.org/abs/2406.06484)**, Yang et al., arXiv:2406.06484v6 / NeurIPS 2024, sections 2--3. The retained implementation pin is FLA commit `07ca1e49ef6ca76a7f0dbc8d5ad040ab59434c38`, including [`fla/ops/delta_rule/naive.py`](https://github.com/fla-org/flash-linear-attention/blob/07ca1e49ef6ca76a7f0dbc8d5ad040ab59434c38/fla/ops/delta_rule/naive.py) and [`fla/layers/delta_net.py`](https://github.com/fla-org/flash-linear-attention/blob/07ca1e49ef6ca76a7f0dbc8d5ad040ab59434c38/fla/layers/delta_net.py). At that pin the **layer defaults** are `qk_norm='l2'`, `allow_neg_eigval=False`, and learned `beta=sigmoid(...)`; enabling `allow_neg_eigval=True` multiplies beta by two. `naive.py` consumes already-produced keys and beta rather than normalizing them itself. A pointwise sigmoid beta below one still does not certify a uniform positive distance from one, and these layer defaults are not asserted as invariants of every kernel or configuration.
- **[Unlocking State-Tracking in Linear RNNs Through Negative Eigenvalues](https://arxiv.org/abs/2411.12537)**, Grazzi et al., arXiv:2411.12537v5 / ICLR 2025, directly analyzes products of identity-minus-vector-outer-product matrices with eigenvalues in `[-1,1]`. Its [author repository](https://github.com/automl/unlocking_state_tracking) and the FLA interface expose the `2*sigmoid` beta option for negative eigenvalues. This is the closest Delta-specific collision for the exact rank-one spectrum and upper branch; it does not supply the excluded margin band or audit-influence claim.
- **[Invertible Residual Networks](https://proceedings.mlr.press/v97/behrmann19a.html)**, Behrmann et al., arXiv:1811.00995 / ICML 2019, theorem 1 and lemma 2. It proves that `I+g` is invertible when `Lip(g)<1` and supplies forward/inverse Lipschitz bounds. The paper links the [`jhjacobsen/invertible-resnet`](https://github.com/jhjacobsen/invertible-resnet) implementation. This directly covers the general residual-invertibility/bi-Lipschitz mechanism; R06 v3 uses the exact spectrum of a linear rank-one Delta factor rather than claiming a new invertibility principle.
- **[Residual Flows](https://arxiv.org/abs/1906.02735)**, Chen et al., NeurIPS 2019. It retains Lipschitz-constrained invertible residual blocks and emphasizes the expressivity/computation implications. It is a strong mechanism control, not evidence that Delta audit survival improves.
- **[Optimal sampling in unbiased active learning](https://proceedings.mlr.press/v108/imberg20a.html)**, Imberg et al., AISTATS 2020; **[Active Testing](https://proceedings.mlr.press/v139/kossen21a.html)**, Kossen et al., ICML 2021. These establish adjacent inverse-probability and proposal-allocation families: Imberg's optimum generally scales with the square root of a conditional second loss moment, while Active Testing uses oracle or learned proposals inside its LURE protocol. They do not prove R06's independent-Bernoulli rectangular-robust HT factor; that factor is the packet's own conditional derivation. R06 nevertheless inherits rather than reclaims the broader sampling principle.

## Actual formula/interface distinction

For `A=I-beta kk^T` and key dimension at least two, the exact minimum singular value is `min(1,|1-beta||k||^2|)`; in one dimension it is simply `|1-beta||k||^2|`. R06 v3's proposed cap `beta=(1-eta)sigmoid(g)` assumes unit-normalized keys and is not asserted to exist in the pinned FLA bytes. Existing beta sigmoid supplies `0<beta<1` per realized finite logit, but without a finite logit bound it supplies no global `eta>0`. If an implementation rescales beta inside a kernel or does not normalize the key exactly, the certificate must use the effective `rho=beta||k||^2` at that interface. Allowing both sides of the admissible set requires an explicit branch or other gap-preserving parameterization because `[0,1-eta] union [1+eta,2]` is disconnected.

The author code supports the recurrence interface only. It does not expose grounded `Y`, post-horizon action-independent `Z`, randomized external audit propensities, paired action outcomes, or a complete-network singular certificate. No source is treated as empirical support for the proposed audit behavior.

## Collision and residual contribution

The functional skeleton is directly covered:

`general residual invertibility / bi-Lipschitz margin + Delta generalized-Householder eigenvalue control + known PPS/Neyman allocation`.

The packet-specific residual is an exact rank-one Delta identity: the factor that lower-bounds survival also lower-bounds the remaining current-key residual, so a finite-horizon audit certificate pays an explicit plasticity cost and decays as a product of margins. This is useful as a theorem/debugging control but does not establish a distinct architecture, objective, estimator or scientific capability.

## Native measurement gap

The editing/temporal-memory assets already audited in R06 v1/v2 measure endpoint behavior after updates. They do not natively expose the joint tuple `(Y_i,X_i,Z_i,pi_i)`, an enforced effective singular margin, paired update/no-update outcomes, or a frozen-path/full-Jacobian comparison. No benchmark, label, case, metric, scorer or result is created here.

## Disposition

**PASS for conditional source support and direct-collision classification; not a novelty pass.** The repair should be parked after attempt 3/3 unless a complete-state margin or native matched-cost audit object changes the information and measurement problem. Empirical effect is unknown.
