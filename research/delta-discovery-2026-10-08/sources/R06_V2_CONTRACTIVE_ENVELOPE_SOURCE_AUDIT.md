# R06 v2 contractive-envelope source and novelty audit

Status: formula/code-interface and closest-work audit for R06 v2; no model or benchmark execution. Search/read cutoff: 2026-10-10 UTC. The dated search refreshed the named primary records and found no evidence that changes the retained mechanism disposition; it is not an exhaustive-priority claim.

## Reused exact primary sources

- **DeltaNet**, Schlag, Irie and Schmidhuber, [arXiv:2102.11174v3](https://arxiv.org/abs/2102.11174), section 4 equations 23--25 and appendix A.1. The paper supplies the residual Delta update used in R06 v2. Original 2021 code was not independently inspected in the retained packet.
- **Parallel DeltaNet**, Yang et al., [arXiv:2406.06484v6](https://arxiv.org/abs/2406.06484), sections 2--3. The paper gives the ordered generalized-Householder recurrence and WY form. The retained author library pin is FLA `07ca1e49ef6ca76a7f0dbc8d5ad040ab59434c38`. In `fla/ops/delta_rule/naive.py`, `delta_rule_recurrence(q,k,v,beta,initial_state,output_final_state)` accepts an initial state and can return the final state, whereas the helper `delta_rule_chunkwise(q,k,v,beta,chunk_size)` has no `initial_state` argument although it returns `(output,state)`. This distinguishes the two actual interfaces; no code was run.
- **Imberg et al., Optimal sampling in unbiased active learning**, AISTATS 2020, [PMLR 108](https://proceedings.mlr.press/v108/imberg20a.html), sections 2--3 and propositions 1--3. Positive inclusion probabilities, inverse-probability unbiased risk and variance-optimal PPS/influence allocation directly cover the sampling principle.
- **Kossen et al., Active Testing**, ICML 2021, [PMLR 139](https://proceedings.mlr.press/v139/kossen21a.html), sections 2.1--2.2 and 3.1, equations 5--6. Sequential randomized acquisition with an expensive label and a learned surrogate proposal is a direct strong baseline.
- **Amorim et al.**, JRSS A 2021, section 4.1.1 equations 8--9, and **Chen--Lumley**, 2021. Influence-function Neyman and multiwave two-phase allocation cover adaptive validation designs.
- **Hadad et al.**, PNAS 2021, and **Cook--Mishler--Ramdas**, CLeaR 2024, cover history-adapted propensity, AIPW and time-uniform inference obligations.
- **R20 v3 retained source audit** reads PROMISE, Iterative Hessian Sketch, Online Newton/dynamic regret and additional spectral-sketch work. R20 v3 already proves and records the `(M+m)^2/(4Mm)` Kantorovich transfer factor and an unrestricted same-prefix impossibility. R06 v2 reuses that inequality for scalar audit-envelope ratios rather than claiming a new inequality.

## What is actually new in this packet

The packet-specific result is the exact connection

`contractive frozen Delta product -> prefix envelope X_i -> rectangular minimax HT allocation -> sharp absence of finite clairvoyant competitive ratio without a lower continuation bound`.

The first arrow is a direct spectral-norm calculation; the middle optimization is generic robust Neyman/PPS; the sharp ratio is classical and already present internally. The connection is useful for debugging the R06 proxy claim but does not establish a distinct updater or sampling method.

## Author-code and semantic boundary

The FLA recurrence stores/updates the fast state and preserves the ordered product. It does not expose grounded audit labels, randomized audit propensity, a post-horizon causal influence target, or a proof that network features remain frozen. Therefore source inspection supports equation (1)'s recurrence only; it does not support the full scientific audit premise.

The no-expansion condition `0<=beta||k||^2<=2` is an explicit mathematical assumption. Learned beta/key normalization must be checked at the actual interface before any empirical use. Even when each frozen factor is nonexpansive, an edited autoregressive model can change later features and invalidate the frozen product as a full Jacobian.

## Native measurement gap and disposition

ROME/CounterFact, EvEdit, EasyEdit/KnowEdit, continuous editing and SEAL endpoints remain as recorded in R06 v1. They do not jointly supply grounded `Y`, prefix envelope `X`, post-horizon action-independent `Z`, randomized `pi`, or paired actions. Derived instrumentation would be a new protocol, not an already native scorer.

Closest-work disposition: **mechanism collision / retain as conditional theory-control**. No novelty pass, no candidate increment, and no empirical verdict. The only scientifically live residual is an externally justified, prefix-checkable two-sided continuation/residual law or a native matched-cost advantage over generic learned influence proposals.

