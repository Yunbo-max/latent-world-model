# D01 inspected evidence: one uncertain edit, retrospective mixture

Authoring worker: `/root/delta_edit_derivation`. Read-only inspection on 2026-10-08; no project execution. These are source notes, not a semantic review of D01.

## Gated DeltaNet

- Paper: https://arxiv.org/html/2412.06464v3 ; sections 2–3, Delta and gated-Delta recurrences/chunkwise construction. Paper uses value-by-key state; D01 consistently transposes it to key-by-value.
- Author code commit: `b53d6d3a161267432a79c1c04af69fa52bddc921`.
- File: `lit_gpt/gated_delta_net.py`, blob `daaeff4c365b34a48ee9f59e35c2db0664ec2bc8`.
- Interface inspected: `GatedDeltaNet.forward`, q/k/v convolution/projection, sigmoid beta, negative-log decay, normalization and `chunk_gated_delta_rule(... initial_state=..., output_final_state=...)`.
- Source boundary: subsequent same-input q/k/v/decay may be shared for an isolated layer, but upper-layer activations can depend on branch output. D01 does not assert exact compression for an ordinary branch-feedback multilayer network.

## AlphaEdit: already-known protection geometry

- Paper: https://arxiv.org/html/2410.02355v3 ; sections 3.1–3.3, equations 7–14, Appendix B.
- Author code commit: `b84624f44dfe8fc6cd9e41df916c44124a0c46dc`.
- File: `AlphaEdit/AlphaEdit_main.py`, blob `6cc07e798bbc91e91d04ef7195d255d22a9c36c5`.
- `apply_AlphaEdit_to_model(model,tok,requests,hparams,cache_template,cache_c,P)` uses a projected linear solve and later updates the cached key Gram matrix. Its requested target values are supervised edit inputs, not free inference evidence.
- Null-space projection protects the represented fixed linear key associations. Paper implementation thresholds small eigenvalues, so exact-null-space and numerical-threshold protection must be distinguished. This geometry is not D01's originality claim.

## Bayesian Online Changepoint Detection: already-known hypothesis recursion

- Paper: https://arxiv.org/html/0710.3742v1 ; section 2, equations 1–9, Algorithm 1.
- Inspected companion implementation, not claimed original authors' code: `hannawallach/changepoint-detection`, commit `bd9f3cb68b4b23894be52a0cdd15514e2edefa8f`, `src/changepoint_detection.py`, blob `c6b7bc5d652165d89898f621c8050d7fda6b125b`.
- `inference(x,beta,n=None)` tracks run-length probabilities and Dirichlet categorical statistics. The implementation takes the entire x array and infers alphabet size from it; D01 cannot copy that interface at inference. Its probabilities must use the already-fixed tokenizer and causal prefix only.
- Causal posterior prediction and likelihood-weighted model hypotheses are established ideas. The Delta rank-one retrospective representation is the residual construction being investigated.

## Bayesian memory neighbors

- Memory by Design: https://arxiv.org/html/2605.31163v1 ; sections 2–3 and Appendix D read. Mean/covariance Gaussian filtering is already a sequence-layer construction. Its auxiliary design model explicitly does not define the input-token likelihood. D01 instead defines two normalized causal token distributions; its posterior is a model-index posterior, not a covariance over associations.
- Voltic: https://arxiv.org/abs/2610.05700 , official indexed abstract retrieved, dated 2026-10-05. Separating volatility/stochasticity with input-dependent anisotropic uncertainty is a known nearby claim. Primary full HTML/abstract/PDF opens returned DisabledError in this worker. Full formula, algorithm and author-code collision audit remains open; third-party mathematical summaries were not used as primary evidence.
- Kalman Delta Networks `2609.07816`: root worker is inspecting the actual source. D01 must inherit that inspected source comparison before any originality clearance.

## Coverage and unresolved search

The above inspection rules out counting a covariance gain, a static protected projection, or a two-expert Bayesian mixture itself as a new mechanism. Exact low-rank compression is an algebraic identity; priority of its application to retrospective Delta editing remains unresolved. The decisive predictive reference is the identical explicit two-state mixture, not an inferior fixed gate. Ordinary contextual gating is a strong simpler alternative.

Native task coverage for genuine delayed revision/coexistence identification remains a measurement gap in this worker; no artificial benchmark, metric, labels or results were created.
