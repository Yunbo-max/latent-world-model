# D01 decisive collision and equivalence audit

Reviewer: `/root/d01_lowrank_collision`.  Scope: primary-paper mathematics and static author-code reading; no project code, model, test, benchmark or experiment was executed.

Disposition: **major functional collision; the narrow exact one-event rank-one state factorization is not scientifically admitted**.  Preserve D01 as an equivalence control and conditional lemma, but remove it from the active candidate pool.  This is `REROUTE_MECHANISM`, not a claim that one prior paper reproduces every Delta-specific formula.

## Exact reparameterization

Let the two explicit branch states be

\[
S_t^C,\qquad S_t^R=S_t^C+l_te^\top.
\]

At one uncertain event,

\[
S_\tau^R-S_\tau^C=(u_R-u_C)e^\top=l_\tau e^\top.
\]

If all subsequent steps share the same affine recurrence

\[
S_j^h=A_jS_{j-1}^h+B_j,
\]

then

\[
S_j^R-S_j^C=A_j(S_{j-1}^R-S_{j-1}^C)
=(A_jl_{j-1})e^\top,
\]

so (l_j=A_jl_{j-1}).  Under exactly these assumptions,

\[
(S_t^C,S_t^R,\pi_t)\longleftrightarrow(S_t^C,l_t,e,\pi_t)
\]

is a reversible change of coordinates.  Reconstructing (S_t^R) yields exactly the two explicit token readouts, likelihood ratio, posterior branch weights and mixture distribution.

The advertised retrospective term is also an identity.  With

\[
M_t=S_t^C+\pi_tl_te^\top,
\]

one obtains

\[
M_t=A_tM_{t-1}+B_t+(\pi_t-\pi_{t-1})l_te^\top.
\]

For nonlinear token readouts (M_t) cannot replace the two branch probabilities; both readouts still have to be computed.  The correction term therefore adds no new predictive behavior beyond the explicit mixture.

## Direct functional neighbors

### Mixture of Delta rules

Wilson, Nassar and Gold, *A Mixture of Delta-Rules Approximation to Bayesian Inference in Change-Point Problems*, PLOS Computational Biology 2013, DOI <https://doi.org/10.1371/journal.pcbi.1003150>, maintains multiple Delta predictors, recursively updates posterior node weights from observation likelihood and mixes their predictions.  The 2018 correction <https://doi.org/10.1371/journal.pcbi.1006210> must be read with it; the corrected equations/figure claims supersede the affected original material.

Author repository `d-r-b-o-b/2013WilsonEtAlPLoSCB`, commit `16f265808d7854cda6d19ecc48b5a7bf11fe1ad8`, `simulate.m` blob `c9c68e9742b6b7bc03df3d5bc8e72814552bc58e`, exposes the actual sequence `U` update, likelihood `lk`, prior transition, normalized posterior weights and posterior-weighted mean.  It covers the multiple-Delta-hypothesis and later-evidence reweighting function; it does not use D01's matrix rank-one difference coordinates.

### Particle-filter RNNs

Ma et al., *Particle Filter Recurrent Neural Networks*, AAAI 2020 / arXiv:1905.12885v2, uses multiple recurrent latent particles with shared parameters, observation-likelihood weight updates and soft resampling.  Author repository `Yusufma03/pfrnns`, audited commit `0a76d52a857f06d4128bbc7601c616d714b25734`, `pfrnns.py` blob `827ce93e2e184bd874628c72c48e8a56c7c7a05b`, implements this in `PFLSTMCell.forward`, `PFGRUCell.forward` and `PFRNNBaseCell.resampling`.  This directly covers recurrent hypothesis states plus future-observation reweighting, although D01's normalized token likelihood is a cleaner observation model.

### Rank-one ensemble parameterizations

Wen, Tran and Ba, *BatchEnsemble*, ICLR 2020 / arXiv:2002.06715v2, parameterizes a member by \\(W'_k=W\circ(r_ks_k^\top)\\).  The `google/edward2` implementation at commit `d79d6a54d0cd0be4bffb9b3d5101e409fcf3b253`, `edward2/tensorflow/layers/dense.py` blob `6b503279632a4f2f0f9f0f477dc183c0bf995251`, applies per-member factors around a shared kernel.  This is multiplicative slow-weight rather than D01's additive fast-state difference, but it already covers the broad claim “compress an ensemble with a shared base and rank-one member factors”.

Voltic's Gaussian mean/covariance, diagonal and low-rank uncertainty states differ from a discrete two-policy token mixture; it is not an exact collision.  It nevertheless covers broad claims based only on uncertainty-modulated Delta writes or low-rank auxiliary state; see `VOLTIC_D01_FULL_AUDIT.md`.

## Residual and failure boundary

The only narrow residual found is:

> one uncertain rank-one Delta edit, branch-independent subsequent affine coefficients, an exact base-plus-rank-one representation, and two actual token-probability readouts.

It reduces state storage from about \\(2d_kd_v\\) to \\(d_kd_v+d_k+d_v+1\\), but changes neither the represented predictions nor the required two likelihood evaluations.  It breaks as an exact factorization when:

1. downstream features depend on branch outputs, so later (A_j,B_j) differ;
2. several independent uncertain events create up to \\(2^m\\) trajectories or growing rank;
3. the causal input lacks source/entity/change identity needed to distinguish revision from a near-key coexisting fact.

The strongest baseline is two explicit complete Delta states with the same causal token-likelihood Bayesian mixture: it is prediction-identical under D01's assumptions and continues to support branch-dependent future features.  A (K=2) PF-RNN without resampling is the broader recurrent-belief baseline.

## Exact-byte inputs reviewed

- `cards/D01.json`: `25658efd8c2be27abd54d6472f84a4c0562e48b97ebd913884857d07792f7a15`
- `sources/D01-sources.md`: `8f47fcaaa544c924ce127b35d7e5455e0542de97de548f6928c011e0eefc8235`
- `sources/VOLTIC_D01_FULL_AUDIT.md`: `fda858acb73b1af92ea279fb69b0060b4d2838e82487ef3e40fdaf4f1397bade`

The bounded audit supports removal from the active pool.  It does not establish exhaustive absence of a literal formula duplicate and does not support “first” or “fully new” language.
