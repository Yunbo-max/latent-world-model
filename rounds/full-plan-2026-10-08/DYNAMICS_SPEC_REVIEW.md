# Independent dynamics, expression and objective specification review

Date: 2026-10-08. Reviewer identity: `/root/dynamics_spec_review`.
Scope: independent mathematical/source review of the full-plan engineering extension, based on baseline `fba4653780e0b277a1fe7fdef47e3f20d33f2d53` and the current original-plan instructions. Status: **reviewed construction, generated_unexecuted**. No project imports, tests, training, inference or asset downloads were executed. This review writes only this file; the sole integration writer owns implementation and publication. It does not qualify historical Q01 or original-method discovery.

## Decision

The following constructions are mathematically executable known-mechanism adaptations: (i) a bounded, globally contractive **optional** workspace with fixed forcing; (ii) an explicit lower-dimensional latent plan and separately callable language realization; (iii) a proper finite-vocabulary prediction loss from the post-write compressed state. They can be implemented without invented action labels, an ELBO for deterministic vectors, a sufficiency claim, or an adaptive stopping claim.

The baseline finite-K Transformer path must remain available. The contractive path changes the model class substantially and is an ablation/comparator, not a proof that its predictions improve. A latent plan is an interface object, not an identified semantic representation. The reviewed targets below cover the lawful text-only realization of the original intent; they do not supply a physical world transition or a Bayes posterior.

## 1. Fixed-forcing contractive workspace

For prediction position i, construct causal forcing B_i once, using the prelude prefix E_{0:i}, the previously committed compressed state M, and retrieved **already observed** exact events D_i. B may use arbitrary neural layers, including causal attention, provided its inputs and retrieved records are fixed throughout this reasoning call and do not depend on the evolving workspace H^(r). Repeated query-dependent retrieval driven by H changes the operator and invalidates the following proof.

Let W in R^{d x d} be trainable, choose a config constant 0<c<1, and define

\[
s(W)=\max(1,\|W\|_F),\qquad A(W)=cW/s(W),
\]
\[
H_i^{(0)}=\tanh(E_i),\qquad
H_i^{(r+1)}=\tanh(A(W)H_i^{(r)}+B_i),\quad r=0,\ldots,K-1.
\]

For row-vector tensor code, transpose the multiplication consistently. The ordinary Euclidean norm on each position and the Frobenius norm on the full workspace produce the same bound because the recurrent map acts pointwise in position. Since tanh is 1-Lipschitz and ||W||_2 <= ||W||_F,

\[
\|R_B(H)-R_B(H')\|_F
\le \|A\|_2\|H-H'\|_F
\le c\|H-H'\|_F.
\]

The finite-dimensional complete state space admits a unique fixed point H*(B), and

\[
\|H^{(K)}-H^*\|_F\le c^K\|H^{(0)}-H^*\|_F.
\]

Each iterate after initialization lies in [-1,1]. For a tensor of N elements, the coarse state bound is 2 sqrt(N) c^K. A posteriori, with delta_K=||R_B(H^(K))-H^(K)||_F,

\[
\|H^{(K)}-H^*\|_F\le\delta_K/(1-c).
\]

This is a state-space bound for the exact mathematical map. It is not a whole-vocabulary output-error certificate, a correctness bound, or the historical affine adjoint certificate. If computing delta_K entails an additional recurrence, count it as a diagnostic call separately from the K prediction calls. ||H^(K)-H^(K-1)|| and delta_K are distinct quantities and must have distinct log names.

### Required implementation conditions

- Normalize from the **current** W on every applicable forward, using the actual Frobenius norm, not a stale optimizer-time cache, a spectral radius, or a power-iteration lower estimate. The normalization should remain in the autograd graph.
- Do not put residual addition, RMSNorm, arbitrary MLP, attention depending on H, or a learned unbounded gate inside R_B after its tanh and still claim c-contraction. Such additions require a different global bound.
- c must be finite, strictly between zero and one, and restored from compatible config/checkpoint state. No parameter update, state write, sampling noise, or forcing re-selection occurs between recurrent steps.
- A causal forcing path ensures causal H at every step. The pointwise recurrence does not create new communication between positions as r grows; cross-position information comes from forcing. This capacity change must remain explicit when comparing with the Transformer core.
- FP32 computation reduces routine numerical error but is not directed-rounding or interval arithmetic. Log `analytic_real_arithmetic_bound` and measured residuals; do not label computed values as certified floating-point upper bounds. Handle nonfinite parameters/forcing explicitly.
- Fixed K remains the only admitted compute policy. Do not enable adaptive stop from this review; Q01 selection, originality and neural applicability remain pending.

### Source and training gradient

Miller and Hardt, *Stable Recurrent Models*, arXiv:1805.10369v4, §2.2 and Appendix A.2.1, explicitly analyze tanh(Wh+Ux) with ||W||_2<1. Their experimental implementation projects singular values after updates (§4/Appendix), whereas this extension uses a conservative differentiable Frobenius rescaling. This is a disclosed parameterization adaptation, not their exact code or a new stability theorem.

For finite K the model is an ordinary differentiable unroll. Backpropagation differentiates tanh, W/s(W), forcing, and all earlier workspace steps; do not silently detach recurrence. The max boundary ||W||_F=1 has the usual subgradient convention. At W=0 the denominator is one; implementations must avoid a NaN gradient from an unnecessary square-root-of-zero construction. The norm primitive and clamp/max choice require Local software checks. Contraction concerns workspace derivatives only; it does not bound forcing/writer parameter gradients globally.

The writer continues its separately defined update and has **no** new contraction guarantee. Persistent memory is not forced to contract with c across observation time. Thus memory can retain information while workspace contracts for a fixed query; this realizes the original separation without proving that memory has learned long-term recall. The same-mode spectral incompatibility in the original notes remains conditional, not a universal architecture theorem.

## 2. Explicit latent plan and independent expression interface

For each causal prediction row define width d_z<d and a real interface

\[
Z_i=\tanh(W_z H_i^{(K)}+b_z),\qquad
T_i=W_{\rm up}Z_i+W_{\rm prev}e(x_{i-1}),
\]
\[
O_i=G_\omega(T_{0:i}),\qquad p(x_i\mid\text{available past})=\operatorname{softmax}(O_i).
\]

G may be a separately parameterized causal coda and vocabulary projection. At segment start use an internal SEG representation as the previous-symbol input. The previous-symbol rows are `[SEG, x_1,...,x_(ell-1)]` when labels are `[x_1,...,x_ell]`; an off-by-one exposing x_i directly is prohibited. If the realizer only accepts Z with no previous-symbol channel, the equations simplify and the interface is stricter. The full original memory/retrieval information must pass through Z; no direct reader/E/M/retrieval bypass is allowed. The previous-symbol channel provides expression context and must be disclosed; it precludes describing Z as the sole source of all linguistic context.

Required API behavior:

1. `plan_prefix(prefix, state)` returns an explicit causal Z sequence plus enough immutable schema/config/source/state information to identify which context it represents. It does not mutate belief, events, consumed identities or observation counters.
2. `realize_plan(plan, previous_symbols)` executes only the language realization module, with no hidden callback to reader/writer/retrieval. Repeated expression calls on the same snapshot are independently possible.
3. Ordinary training `forward_segment`, prefix prediction, generation and evaluation actually use this factorization when enabled. An unused standalone helper is not interface implementation.
4. Snapshot persistence must restore dimensions, dtype, model/config compatibility, state identity and causal prefix association. A stale plan must not be silently used after the observation state/prefix has changed. Device conversion may be explicit; hidden lost-context reconstruction may not.
5. Preserve the original direct-coda mode for a matched ablation. Post-coda last-row selection remains legal only after all causal row mixing; slicing the plan or coda input early changes the model function.

This is a **token-conditioned text plan**. Each next-symbol context may require a new planning call. It does not deliver a frozen sentence-level semantic goal generating arbitrary paraphrases without replanning, semantic annotations, an invertible codec, or cross-lingual meaning invariance. Conditional sequence decoders with a latent summary and previous-symbol context are established (Cho et al., arXiv:1406.1078v3, §2.2). Gisting is a closer modern example of forcing information through an explicit hidden bottleneck and reusing its activations: its paper §3 and author `make_gist_mask`/`GistActivations` code provide concrete attention-access boundaries. Neither paper is reproduced here.

Smaller continuous width is a dimensional/storage constraint; it is not a proven information-theoretic compression rate. Arbitrary continuous coordinates do not imply a finite bit-capacity without precision/quantization constraints. CE alone leaves Z's coordinates unidentifiable under invertible transformations absorbed by the decoder. Calling the module semantic describes its intended role; it does not establish semantic quality.

## 3. Lawful objectives with available text supervision

### Main realization/prediction loss

The exact normalized conditional model above gives

\[
\mathcal L_{\rm text}=-N_{\rm tok}^{-1}\sum_{t,i}\log p_\theta(x_{t,i}\mid M_{t-1},D_{t,i},x_{t,<i}).
\]

This one CE trains reader, forcing, plan, realization and any differentiable selected-record encoding. There is no separate realization-loss necessity: adding an identical CE under another name just changes its weight. Discrete deterministic retrieval selection has no pathwise selection gradient; selected event token embeddings/reader may still receive ordinary CE gradient. Report that distinction instead of pretending the retriever is trained end-to-end.

### Direct compressed-state future prediction

For a completed non-EOS segment t with an actual following segment in the **same document**, let the discrete random target Y_t=x_(t+1,1) be the first real next token. Define

\[
q_\eta(y\mid M_t)=\operatorname{softmax}(W_f\operatorname{vec}(M_t)+b_f)[y],
\]
\[
\mathcal L_{\rm state}=-N_{\rm pair}^{-1}\sum_{t\in\mathcal A}\log q_\eta(Y_t\mid M_t),
\qquad\mathcal L=\mathcal L_{\rm text}+\beta\mathcal L_{\rm state},\quad\beta\ge0.
\]

Pooling instead of flattening is legal only if the actual head and dimensions are specified. The target must enter **only** the loss. The head sees M_t, not Y_t, next-segment encoding, answer annotations, or exact-event retrieval. Exclude EOS/reset/document boundaries, missing genuine successors, and incompatible stream identities. No available pairs means a scalar zero contribution and pair_count=0, not division by zero or fabricated target.

For fixed deterministic M and a finite conditional vocabulary distribution with positive q support,

\[
\mathbb E[-\log q(Y\mid M)]
=H(Y\mid M)+\mathbb E_M\operatorname{KL}(p(Y\mid M)\Vert q(Y\mid M)).
\]

Thus this is a proper supervised prediction objective. Its optimization favors a predictively useful compressed state within its limited target and model class; it does **not** estimate I(F;history|state), enforce full future sufficiency, or guarantee long-term information retention. This identity is elementary likelihood theory and a local derivation, not a new named loss.

For writer parameters psi,

\[
\partial_\psi\mathcal L_{\rm state}
=(\partial_{M_t}\mathcal L_{\rm state})(\partial_\psi U_\psi(M_{t-1},X_t)).
\]

So it provides an immediate post-write learning path in addition to subsequent-segment CE. M_t must not be detached before this loss. Within-window state gradients remain intact; TBPTT still cuts earlier history and the usual parameter-staleness caveat remains. A separate head optimized against a future token does not require or justify a posterior distribution over deterministic M.

Use beta=0 for CE baseline and a documented finite positive value for a prospective development arm (for example beta=0.1 as a choice, not a theorem). Log main CE, auxiliary CE, beta, pair denominator and auxiliary target observations separately. These target observations should already be genuine next segments in the declared window/data view; do not acquire extra undeclared future context. Accounting must disclose repeated supervision of a target also present in main CE and any additional target access, rather than silently changing the 100M/1B token definition.

### Compression, reasoning and compute

- **Compression:** enforce finite memory-slot dimensions and bounded event/token capacity as explicit architectural/resource constraints. Log exact state/index/storage bytes and precision. There is no justified generic KL for a deterministic state. An L2 state penalty is not information compression and is not required here.
- **Reasoning accuracy:** main CE is the available supervised accuracy objective for finite internal computation. A residual-only auxiliary loss can encourage an uninformative fixed point and is not an accuracy surrogate without more justification; do not add it just to fill a coverage row.
- **Compute:** with config-fixed K, a penalty lambda*K is constant in trainable parameters and cannot teach adaptive computation. Use a hard depth budget and prospectively compare K=1/4/8 including all forcing, retrieval, diagnostic and realization costs. A learned stopping policy would need its own probability object, training estimator and qualified gate; it is intentionally not introduced by this review.
- **Expression:** train the separate language factorization with the same exact text likelihood. No invented semantic labels, action/transition targets, entropy-monotonicity target, or reconstruction ELBO is admitted.

These are executable constraints and estimators, not loss names standing in for completed work. They meet the lawful text-data construction while keeping unidentifiable original ideals explicitly separate.

## 4. Integration and prospective acceptance

The implementation writer should map the following obligations to actual symbols and commands after code exists. Local executes them; this review provides no passes.

| Contract | Required Local check and comparison |
|---|---|
| Causal forcing and plan | Future-token mutation leaves all earlier logits/retrieval identities unchanged; segmented teacher-forcing rows agree with real prefix prediction within stated dtype tolerances. |
| Fixed evidence and clocks | Extra planning/reasoning/realization calls leave belief/events/consumed identities unchanged; committing the same source event is idempotent; generated material keeps generated provenance. |
| Contractive path | Confirm current rescaled matrix Frobenius upper value is <=c within diagnostic tolerance; compare two workspaces with identical forcing; count any extra residual calls. Numerical checks support software semantics, not the real-arithmetic proof or science. |
| Auxiliary gradient | Direct post-write state loss produces actual nonzero writer-exclusive parameter gradients on a valid same-document pair; target value cannot affect writer/head inputs; EOS/missing pairs are excluded. |
| Independent expression | Restore a plan snapshot and call only realization; instrument reader/writer/retrieval entry points to establish they are not called; reject stale/incompatible plan metadata. |
| State restore | Mid-segment prompt/output source marks, committed belief/events, plan compatibility, counters and budgets restore together. Native eval branches copy all state and never share mutable stores. |
| Model comparisons | Preserve v0, exact-memory off, plan off, auxiliary beta=0 and unconstrained-versus-contractive/fixed-K arms. Cost comparisons must include different model-class/parameter/representation effects. |

All native data, scorers and full denominators remain those already adopted: bAbI all 20 tasks / 20000 and LAMBADA 5153. This review proposes no replacement benchmark, no hand-made scientific fixture and no GPU-fit claim. Full matrix budget is cumulative over arms/seeds; the 100M/1B unit remains per-arm/seed target-token exposure. Independent scientific evidence, native parity, software passes and 2080 Ti acceptance all remain Local-pending.

## 5. Primary reading and author-source record

- Miller and Hardt, [Stable Recurrent Models, arXiv:1805.10369v4](https://arxiv.org/pdf/1805.10369), §2.2, Appendix A.2.1 and stability projection description. Read the actual paper stability equations. The paper names underlying PyTorch language-model/TCN code but this reviewer did not discover a pinned dedicated release of their spectral-projection modification; no exact author implementation reproduction is claimed.
- Geiping et al., [Huginn / recurrent depth paper, arXiv:2502.05171](https://arxiv.org/abs/2502.05171), existing project primary reading reused. Independently read actual author [recpre/model_dynamic.py](https://github.com/seal-rg/recurrent-pretraining/blob/1ea7220ec7eb42d13e89db0663df254d0bcdc28e/recpre/model_dynamic.py), Git blob `e8ef88e6148463ce0723ad0c9676073c5a9f447c`: `RecurrentGPT`, adapter/core/coda initialization, `iterate_forward`, `core_block_forward`. The author's no-grad recurrence prefix is explicit; this extension retains full finite-K gradient and therefore is not identical training.
- Mu et al., [Learning to Compress Prompts with Gist Tokens, arXiv:2304.08467v3](https://arxiv.org/html/2304.08467v3), §3 and Appendix A. Independently read full author [`src/data/gist.py`](https://github.com/jayelm/gisting/blob/3be0d062b6bdfd3caf51843bbc60261a0855f876/src/data/gist.py), blob `1062487124d2cacce6c4a5556a3e6fbf7ede3d5b`, and [`src/gist_caching.py`](https://github.com/jayelm/gisting/blob/3be0d062b6bdfd3caf51843bbc60261a0855f876/src/gist_caching.py), blob `a96160dc03ce493d4c9c6fbc6f623d24b470af2f`. These enforce attention-access boundaries and explicit reuse of hidden/KV activations. This extension's lower-width Z factorization is an adaptation, not Gisting's mask or cached-transformer reproduction.
- Cho et al., [RNN Encoder-Decoder, arXiv:1406.1078v3](https://arxiv.org/pdf/1406.1078), §2.2 equations for decoding from a continuous summary and previous symbols. Actual primary paper read; no exact author-code reproduction claimed.
- Engdahl et al., [BDH-CQ, arXiv:2608.09888v1](https://arxiv.org/html/2608.09888v1), §3.2–3.3 equations 1–4. The actual paper states memory/workspace separation and says exact update/dimensions remain proprietary. This prevents treating high-level separation as established originality; it also prevents pretending there is a inspected open full system for faithful reproduction.
- Marino et al., [A General Method for Amortizing Variational Filtering, arXiv:1811.05090](https://arxiv.org/abs/1811.05090), project prior paper/code audit reused from `research/SCIENTIFIC_SCOPE_REVIEW.md`. Its stochastic filtering objects are distinct from the deterministic state likelihood chosen here; no AVF ELBO is copied without its distributions.

Some initial browser opens returned DisabledError; later primary-paper opens and GitHub connector reads above succeeded. Reading receipts establish source access, not execution. Author-code overlap, known statistical objectives and the exact restrictions above must remain visible in the integrated proposal, README and handoff.
