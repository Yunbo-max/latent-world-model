# R20 v2 source and nearest-work audit

Audit date: 2026-10-10. Scope is formula/author-interface and measurement feasibility; no upstream or project code was executed.

## Pinned primary mechanisms and author interfaces

### M-FAC

- Paper: Frantar, Kurtic and Alistarh, *M-FAC: Efficient Matrix-Free Approximations of Second-Order Information*, NeurIPS 2021, [proceedings page](https://proceedings.neurips.cc/paper/2021/hash/b4a528955b84f584974e92d025a75d1f-Abstract.html), [arXiv:2107.03356](https://arxiv.org/abs/2107.03356).
- Author repository: [`IST-DASLab/M-FAC`](https://github.com/IST-DASLab/M-FAC) pinned at commit [`8116367fb537b48484e2e4bde24f11f42b117f8a`](https://github.com/IST-DASLab/M-FAC/commit/8116367fb537b48484e2e4bde24f11f42b117f8a).
- Inspected bytes: [`optim.py`](https://github.com/IST-DASLab/M-FAC/blob/8116367fb537b48484e2e4bde24f11f42b117f8a/optim.py), blob `eca73f46afc38e3a57dd660f48a1f912723302eb`; [`README.md`](https://github.com/IST-DASLab/M-FAC/blob/8116367fb537b48484e2e4bde24f11f42b117f8a/README.md), blob `3a711d440c8b6ee22957806264512edb7f95656e`.
- Actual interface: `HInvFastUpMulti` stores a sliding `m x d` gradient matrix, builds `GG^T`, and `mul` applies the inverse of a damped empirical-Fisher approximation without materializing a dense `d x d` inverse. `update` replaces the oldest gradient; `MFAC.step` calls `update_mul` on the current flattened gradient. `HInvSlow` is explicitly a naive Woodbury correctness reference.
- Collision: prefix gradient windows plus small-Gram damped inverse products are already implemented. R20 v2's residual is the exact `X^T k=e` constraint, the tangent projector, and factorized Delta action—not low-rank empirical-Fisher inversion itself.

### SENG

- Paper: Yang et al., *Sketchy Empirical Natural Gradient Methods for Deep Learning*, [arXiv:2006.05924](https://arxiv.org/abs/2006.05924).
- Author repository: [`yangorwell/SENG`](https://github.com/yangorwell/SENG) pinned at commit [`e33f907d03e2b2099ecd452b485d85f07609672a`](https://github.com/yangorwell/SENG/commit/e33f907d03e2b2099ecd452b485d85f07609672a).
- Inspected bytes: [`Pytorch/cifar10/seng.py`](https://github.com/yangorwell/SENG/blob/e33f907d03e2b2099ecd452b485d85f07609672a/Pytorch/cifar10/seng.py), blob `97cef23e7383eb38b5c34e6a7289c99e44473363`.
- Actual interface: `SENG` periodically computes empirical-Fisher inverse blocks, exposes damping/update-frequency/subsampling/column-sketch controls, and `_precond` uses the displayed `g/k - U^T(kI+UU^T)^-1Ug/k` Woodbury form. It operates as a parameter-gradient preconditioner, not an exact Delta overwrite solver.
- Collision: sketching the empirical Fisher and solving in a smaller sample/feature space are known mechanisms. A different sketch distribution alone is not a R20 candidate.

### WoodFisher

- Paper: Singh and Alistarh, *WoodFisher: Efficient Second-Order Approximation for Neural Network Compression*, NeurIPS 2020, [proceedings page](https://proceedings.neurips.cc/paper/2020/hash/d1ff1ec86b62cd5f3903ff19c3a326b2-Abstract.html), [arXiv:2004.14340](https://arxiv.org/abs/2004.14340).
- Author repository: [`IST-DASLab/WoodFisher`](https://github.com/IST-DASLab/WoodFisher) pinned at commit [`d4b1a968947d9850ebf6b67935165e9453495962`](https://github.com/IST-DASLab/WoodFisher/commit/d4b1a968947d9850ebf6b67935165e9453495962).
- Inspected bytes: [`pruners/woodfisher.py`](https://github.com/IST-DASLab/WoodFisher/blob/d4b1a968947d9850ebf6b67935165e9453495962/pruners/woodfisher.py), blob `96c876145e3ca68cf276427658167896cb539817`.
- Actual interface: `_compute_sample_fisher` flattens first-order gradients; `_compute_woodburry_fisher_inverse` recursively updates a damped inverse from sampled gradient outer products and then extracts inverse-diagonal statistics for pruning.
- Collision: recursive empirical-Fisher/Woodbury construction is established. WoodFisher's target is parameter pruning, so it does not itself impose the Delta current-key equality constraint.

### Empirical-Fisher limitation

- Wu et al., *An Improved Empirical Fisher Approximation for Natural Gradient Descent*, NeurIPS 2024, [proceedings page](https://proceedings.neurips.cc/paper_files/paper/2024/hash/5a51762759bdeee8e2242669a66dc54a-Abstract-Conference.html).
- Relevance: the paper distinguishes exact Fisher, empirical Fisher and generalized Gauss--Newton objects. A general per-example loss-gradient outer product is not automatically an empirical Fisher; for an observed-label log-likelihood/NLL score it is the usual empirical-Fisher surrogate, and it still need not equal the GGN. This directly blocks any inference from “prefix-causal gradient features” to “accurate future curvature” without extra assumptions and validation.

### Past-gradient projection controls

- OGD: Farajtabar et al., *Orthogonal Gradient Descent for Continual Learning*, AISTATS 2020, [PMLR paper](https://proceedings.mlr.press/v108/farajtabar20a.html), projects updates away from stored past gradient directions.
- GEM: Lopez-Paz and Ranzato, *Gradient Episodic Memory for Continual Learning*, NeurIPS 2017, [paper](https://papers.nips.cc/paper_files/paper/2017/hash/f87522788a2be2d171666752f97ddebb-Abstract.html), uses episodic gradients and constrained projection.
- SketchOGD: Min, Wright, Bernstein and Azizan, *SketchOGD: Memory-Efficient Continual Learning*, arXiv:2305.16424v2 (2025-03-10), [abstract/version record](https://arxiv.org/abs/2305.16424), maintains fixed-budget sketches of past gradient subspaces before orthogonal projection.
- Collision: `||Z^T x||^2` is a soft past-feature protection penalty and approaches a hard projection only in a qualified singular limit. Fixed-budget past-gradient sketching/projection is therefore already a strong direct control; R20 v2 must not claim the sketch or protection principle as novel.

## Reused R20 v1 audits

The v1 audit remains binding for KKT/equality-constrained quadratic projection, GGN/natural gradient, K-FAC, Shampoo, generalized Sylvester/Krylov solves, CrispEdit, PDN, Gated Kalman attention, DeltaProduct, QED and GDN2. In particular:

- a single separable Kronecker metric cancels on the value side under the exact all-output constraint;
- general nonseparable curvature and equality-constrained quadratic solves are known mathematics;
- multiple/sequential Delta writes and direct low-rank action prediction are mandatory controls;
- R20 v2 does not inherit a novelty pass from v1 merely because the information law changed.

## Source-supported distinction and unresolved residual

Supported distinction: R20 v2 combines a prefix-only damped low-rank curvature with the exact fast-state constraint `X^T k=e`, and derives a tangent-projected Woodbury solution whose factorized columns are legal multi-direction Delta actions. The exact formula and v1 witness recovery are project derivations; the low-rank inverse mechanism is not new.

Unresolved residual: no inspected source supplies a theorem that a fixed-size past gradient or properly factorized GGN sketch predicts the post-write future-query damage under a changing autoregressive Delta state, nor a matched-total-cost advantage over direct prediction of the same `r+1` action factors. Observed-gradient empirical Fisher and GGN must remain distinct. This transfer problem is the scientific bottleneck, not the small linear solve.

## Native measurement feasibility

The existing benchmark audit remains unchanged. bAbI/LAMBADA/RULER/BABILong/LongMemEval can measure downstream task behavior but do not natively expose the target curvature, the optimal constrained action, or paired same-state counterfactual writes. CITB/TRACE provide retention/transfer/task-sequence outcomes but are parameter-level continual-learning endpoints and still lack a native fast-state `Z` or KKT target. Therefore curvature-transfer error, surrogate gap and action rank require derived instrumentation; they are measurement gaps, not fabricated benchmark metrics or results.

## Audit decision

Mechanism collision is major: M-FAC, SENG and WoodFisher cover prefix/past gradient outer products, damped low-rank empirical curvature, sketching and Woodbury inversion; v1 sources cover the constrained quadratic, curvature and Delta baselines. The exact constrained factorized corollary is useful debugging mathematics, but originality and same-budget utility are not established. Source verdict: **conditional control; park after attempt 2; zero candidate increment; empirical effect unknown**.
