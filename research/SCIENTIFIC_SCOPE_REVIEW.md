# Scientific scope review: full model delivery

Date: 2026-10-07. Independent review of the files at local project commit `9c93007773b1a3b290fde0d3d475f01f02d5d97f`, plus the primary sources identified below. This review executes no project code or tests and downloads no model or dataset. It is neither a passed research gate nor an experimental result.

## Recommendation

**Deliver a complete, explicitly disclosed engineering composition of Recurrent Memory Transformer (RMT) and Huginn's recurrent-depth architecture. New scientific discovery is not necessary to meet the user's stated functional requirements.** The composition must be described as an adaptation of established mechanisms, not an unchanged reproduction, a verified new method, or an empirically validated world model.

The user's actual requirements, as restored by the supervising conversation, are a full mathematical scheme followed by model/training/evaluation code and experiment design, grounded in actual existing models. The target includes persistent latent state, internal computation before language emission, and a separate language readout. The user has not requested a new paper or twenty original model inventions. The request also explicitly corrects the idea that future Local test results are needed before Web can finish a justified source delivery.

`BACKGROUND_GOAL.md` item 3, `method-batch.json`, and the checkpoint preserve an assistant-introduced discovery route. Preserve that history, with its unfinished 20-to-15 obligation still pending, rather than declaring it completed or overwriting its evidence. A stored assistant-authored workflow is not an independent human instruction. Record the engineering scope and its provenance openly in the integration writer's project records; do not edit the verifier, fabricate a selection, or label this composition a reproduction in order to obtain a green check.

This is a substantive route decision, not a weaker scientific claim: code delivery can be completed while originality, empirical benefit, and the old discovery lineage remain unresolved. If the user later elects a new-method research contribution, that separate lineage resumes its real mathematical/source/selection obligations. Nothing in this review closes them.

## What the existing evidence actually establishes

| Object | Finding | Consequence |
|---|---|---|
| Full-model target | Three operational requirements are present; no final architecture or explicit demand for a novel theorem is recorded in the user instructions supplied to this review. | Choose and disclose a complete engineering construction. |
| Q01 | The affine adjoint identity and Neumann-tail bound are correct under the card's stated assumptions. They concern one scalar's distance from an affine fixed-point readout. | Retain as a conditional mathematical note. It neither defines the full model nor supplies a necessary stopping rule. |
| Q01 qualification | The recorded code check reports one card, zero mathematical reviews, zero selected methods, and a selection deficit. | Do not claim selection, code readiness, or novelty. This review does not fabricate its missing JSON review or substitute for a full pool. |
| Earlier mathematical notes | They correctly separate observation, internal computation, and output; distinguish compression from approximation error; reject repeated likelihood counting; and identify posterior/causal-identification limitations. | Carry these constraints into the actual full-model interfaces. They do not prove that new discovery is necessary. |
| Discovery counts | One conditional partial construction exists; no qualified twenty-model pool exists. | The old batch remains at its actual counts. The engineering composition is not twenty candidates and is not added to that pool to repair a quota. |
| Resources | An RTX 2080 Ti is user-stated; available memory, host configuration, and throughput are unmeasured. Token quantities remain an interpretation rather than a frozen data contract. | Author a small configurable source implementation and a Local qualification plan; make no runtime or capability promise. |

Q01's bound follows directly from `(I-A)(h*-h)=r`, `(I-A)^T u=c`, and the geometric tail of the convergent adjoint series. The card appropriately disclaims nonlinear-neural applicability and answer correctness. No part of the proposed engineering construction needs to assert contraction, use that certificate, or turn fixed-point agreement into a correctness guarantee. Consequently, Q01's unfinished novelty investigation is not a scientific dependency of the engineering composition.

## Source-grounded model choice

| Source inspected | What it supplies | What it does not supply unchanged |
|---|---|---|
| RMT paper, §3; author `modeling_rmt/language_modeling.py` at `9d0ebe1778687995697fe68e886bc1dcf0e45e1c` | Actual language-model implementation with read-memory prefix, token segment, write-memory suffix, and suffix-state transfer to the next segment. | A separately controlled repeated latent-depth core; an API that preserves memory between all caller invocations. The supplied wrapper initializes its memory at each forward call. |
| Huginn paper, §3; author `recpre/raven_modeling_minimal.py` at `1ea7220ec7eb42d13e89db0663df254d0bcdc28e` | Prelude, repeatedly applied shared core with input reinjection, coda, vocabulary head, and explicit recurrence count. | RMT's bounded learned memory across observation segments. KV caching is not a proof of that memory semantics. |
| AVF paper, equations 6–13 and Algorithm 1; author `lib/models/srnn.py` and `util/train_val.py` at `f1032d62761c498e5206c0a2b07a012c8223b3de` | Persistent recurrent/latent state; repeated inference for one fixed observation; separate generation and external-step operations. | A released language implementation: the inspected SRNN config supports speech Gaussian and music Bernoulli outputs. Categorical text emissions, tokenization, and a query readout would be an explicit adaptation. |
| Recurrent Looped Transformer author README, observed at repository head `b323cbc6e349237b755600b13f2d9bde73e82ff3` | A nearby persistent decoder-state idea; recurrence runs through prompt and response tokens. | A free silent iteration count before a token. The documented main recurrence has fixed decoder work per token. Its name alone does not satisfy the required internal clock. This review did not inspect its implementation and does not adopt it. |

RMT plus Huginn is the preferred engineering path because both inspected mechanisms already operate on language-model representations. AVF is a coherent alternative if the owner prioritizes an explicitly probabilistic latent state over the simpler text-model implementation. Neither has established task performance for this exact project.

No exact unchanged released model was verified here to meet all the stronger requirements simultaneously: bounded persistent state, independently controlled silent iteration, language training, and the required evidence/readout separation. The recommendation therefore does not claim such a reproduction exists. Conversely, the absence of that exact package does not make an original research contribution necessary; transparent integration is sufficient for source engineering.

## A source-grounded alternative construction, not the adopted implementation specification

This section records the reviewer's RMT-suffix alternative. The integration writer selected the separate-writer construction in FULL_MODEL_PROPOSAL.md after causal/gradient review; that file is authoritative for implementation, including its internal SEG and unshifted target contract. The alternative below is retained as reasoning history and must not be combined with that specification's label, initialization or memory semantics. Its sizes and iteration counts are configurations, not independent research candidates.

Let `x_t` be the next externally accepted observation segment, `M_{t-1}` an `m × d` persistent memory array, and `K_t ≥ 1` the number of internal iterations. All segments belong to an explicitly identified stream; reset memory at true stream boundaries. Let `Emb`, `P`, `R`, `C`, and `W` respectively denote token embedding, causal prelude, shared causal recurrent core, causal coda, and vocabulary projection. The source-inspired ingest construction is

\[
U_t=[M_{t-1};\operatorname{Emb}(x_t);M_{t-1}],\qquad E_t=P(U_t),
\]

\[
H_{t,0}=\sigma\xi_t,\quad \xi_t\sim\mathcal N(0,I),\qquad
H_{t,k+1}=R_\theta(H_{t,k},E_t),\quad 0\le k<K_t,
\]

\[
O_t=C(H_{t,K_t}),\qquad
M_t=O_t[\text{write-memory rows}],\qquad
\ell_{t,j}=W O_t[\text{token row }j].
\]

The recurrent core contains the Huginn-style adapter applied to `[H;E]` followed by shared causal transformer blocks. Every inner iteration uses the **same** `E_t`; the outer memory assignment occurs once after ingest. Initialization noise is an explicitly recorded computational input independent of observations. Training and inference must use the same declared initializer policy; deterministic evaluation may fix its seed. A zero initializer is an implementation option, not a proved equivalent trajectory.

The read and write memory roles follow the actual RMT concatenation of the previous memory at both ends, rather than an invented undocumented write rule. All causal blocks must use the same valid-token and causal visibility contract. A token position cannot attend to later token positions or the write suffix. A write position may attend to the accepted full current segment. Across a new segment, memory may legitimately summarize every observation in the preceding segment.

**Causality argument.** At the start of a segment, each prefix memory row depends only on prior accepted observations and model randomness. One causal block at position `j` depends only on rows at or before `j`; composing prelude blocks, repeated core blocks, and coda blocks preserves this property by induction. Therefore token logits do not see future observation tokens through the suffix even though suffix rows produce the next persistent state. This argument fails if the implementation uses an incorrect mask or reuses suffix content as a prefix within the same segment. Mask correctness is consequently a necessary Local semantic check.

**Language objective.** Flatten consecutive segments within a real document/stream and use ordinary next-token cross entropy on eligible targets:

\[
\mathcal L(\theta)=\mathbb E_{K,\xi}
\left[-\frac{1}{N_{\rm valid}}
\sum_{i\in\mathcal I_{\rm valid}}
\log\operatorname{softmax}(\ell_i)_{x_{i+1}}\right].
\]

Memory-token rows are excluded from the target denominator. The last token of a segment may predict the first token of the next segment in the same stream. Cross-document targets and padding are masked. Memory is passed forward in value; cross-segment gradient propagation is enabled through a declared finite training window. Detaching memory truncates the learning gradient, not the forward state, and must be recorded as such. The same applies to detaching early internal iterations: this is a surrogate/truncated gradient, not the full derivative of the unrolled objective.

Use one fixed finite `K` for the first source configuration or an explicitly declared training distribution over `K`. Larger inference `K` is an exposed compute option, with no assumed monotone accuracy benefit or convergence theorem. A shared core reduces parameter duplication, but its repeated evaluation still consumes time and activation memory.

**Query and language output.** Freeze the accepted evidence memory `M_t` during an answer. For output position `j`, form a read-only branch from `M_t`, the query `Q`, and the already generated output prefix `y_{<j}`. Run the same prelude/core/coda with `K_{Q,j}` internal steps and sample/read the next-token logits. Do not commit this branch's suffix to the evidence memory. Thus changing `K_{Q,j}` changes internal computation without forcing extra emitted tokens. A separate API operation may ingest a later genuine observation. Storing the fact that the assistant previously said something is possible as a labelled event, but it must not silently become evidence that the content is true.

Serialization stores `M_t`, stream identity, model/tokenizer/config identity, and the point in the accepted observation stream. Query working state and generation caches have separate lifetimes. The source implementation should expose actual `ingest`, `answer`, `save_state`, `load_state`, and `reset` behavior, not merely rename the transformer's ordinary KV cache as persistent world state.

**Generative/predictive meaning.** This is a deterministic recurrent predictive state with a categorical language observation model. It can predict future language and update memory after observations. It does not identify a calibrated Bayesian posterior, a physical state, or a causal intervention model. Those stronger meanings require extra assumptions/data and cannot be obtained by naming `M_t` a world state. An imagined generated future belongs to a separate rollout branch; it is not an externally observed state transition.

**Prediction and falsifier.** The architecture permits information from earlier segments to influence later outputs even after their raw token buffers are discarded, and permits multiple core evaluations before the same single output position. Those are source-verifiable functional properties. The practical hypothesis is that learned memory plus repeated computation helps on some native history-dependent tasks under a fair total-cost comparison. A correctly implemented model can fail that hypothesis: memory may discard necessary facts, the core may ignore memory, or extra iterations may harm accuracy. A memory reset comparison, an equal-information fixed-depth comparison, and an iteration-count comparison are discriminating controls, not additional novel methods. Exact benchmarks, native scorers, full coverage, and budgets belong in the eventual complete design; this review does not freeze an empirical queue.

## Integration consequences from actual source, not guessed interfaces

1. RMT's `process_input` uses plural `inputs_embeds`, sends `input_ids=None`, and expects `hidden_states` as a layer tuple. The inspected Huginn interface uses singular `input_embeds`, accesses `input_ids.shape`, and returns a different recurrent output structure. A blind RMT wrapper around that file is incorrect. Provide an explicitly reviewed adapter or implement the pinned mathematical construction with matched interfaces.
2. Huginn returns `latent_states = x.clone().detach()`. Using that returned field as learned recurrent memory would sever gradient flow across observation segments. RMT instead reads the differentiable final hidden-state suffix; the integration must intentionally preserve that path within the declared BPTT window.
3. In the inspected Huginn implementation, a scalar `num_steps` is interpreted entirely as no-gradient iterations. Training must deliberately select differentiable iterations; simply passing `K=4` is insufficient.
4. Huginn's inspected `forward` sets `prepared_attn_mask=None` while the mask compilation call is commented out. Causal attention remains in the attention block, but that does not supply requested padding, document, or stream isolation. These masks must actually be implemented and exercised in Local acceptance.
5. RMT's `RecurrentWrapper.forward` initializes `memory_state=None` each invocation. Persistent state between calls needs the lower-level cell interface or an explicit stateful wrapper. Its `manage_gradients` assigns a detached tensor only to a local variable; do not assume that call truncates the caller's memory graph.
6. The repositories differ in positional treatment, output conventions, loss shifting, cache layout, and gradient controls. Copying an evaluation loss without aligning its label contract risks double shifting or omitted segment-boundary targets. Preserve a derivation-to-source map for the integrated implementation.

These are concrete source-authoring tasks, not reasons to demand future experiment results before writing code. Local must validate the exact resulting bytes. No source inspection here is claimed as a passed software test.

## 2080 Ti and actual delivery blockers

The construction has no mathematical dependence on billion-parameter weights. For example, a width-256 reference configuration with 8,192 tied vocabulary embeddings, one prelude block, two shared core blocks, one coda block, and a `2d → d` adapter is approximately 6.5 million parameters for a gated FFN width of `4d`. This is an analytic illustration of scalable parameterization, not an asserted measured parameter count or a chosen training recipe. With conventional FP32 weights, gradients, and two Adam moments, those parameter/optimizer tensors alone are about `16P` bytes; activations, attention, workspace, and the unrolled training window are additional. Actual fit and speed depend on those quantities and must be measured on the real host.

Author finite conservative configurations and an exact Local resource probe; do not promise that a published large Huginn training configuration fits this card or that 0.1B/1B tokens will produce a capable assistant. A small language model can implement the requested architecture while still failing to learn useful persistent reasoning. That is an empirical limitation to report, not a reason to replace the architecture with an unrelated ordinary small-LM pipeline.

The remaining **source-delivery** work is concrete: finish the mask/gradient/state integration; choose and pin the tokenizer and real training corpus; fix segment/document/label contracts; inspect the selected native benchmark data/protocol/scorer; implement complete required comparison and result-collection paths; and provide the project-specific Local runbook and acquisition/integrity instructions. None of these needs fabricated novelty or a claim that the old selection gate passed.

The **execution** blockers remain the absent usable training-host connection, unmeasured device/runtime capacity, missing asset acquisition/qualification, and the exact Local software and native-scorer checks. LongMemEval is only a candidate task in the old record; its model-judged native scorer is not interchangeable with exact match, and its rows have not been inspected by this reviewer. HF publication is not performed; an unknown HF output destination blocks such publication, not authoring source for the already authorized GitHub repository.

The integration writer can therefore continue immediately toward the full engineering source and complete pending design within the user's existing request. Document the scope distinction before delivery, preserve the old discovery records as pending, mark the source `generated_unexecuted`, and report actual native acceptance/results later. Do not use a synthetic twenty-item candidate list as a substitute for this work.

## Reading record and source locators

Canonical skill applied: `e0/remote-skills/skill-6ac68a8f6ff481919a700388dd326f62`. Read its entry, workflow harness, relevant research-policy sections, method-verification contract, and mathematical-analysis contract. The route judgment uses their express allowance for legitimate non-method outcomes and scope-specific applicability, together with the higher-priority actual user scope supplied by the supervisor. It does not change their standards for a new discovery claim.

- [RMT primary paper](https://papers.neurips.cc/paper_files/paper/2022/file/47e288629a6996a17ce50b90a056a0e1-Paper-Conference.pdf), especially §3 and the read/write memory diagram. [Author language-model implementation](https://github.com/booydar/recurrent-memory-transformer/blob/9d0ebe1778687995697fe68e886bc1dcf0e45e1c/modeling_rmt/language_modeling.py), read all 195 lines; Git blob `ea0908d51b4b84b3d364e2f511ee7d7703aec4b6`.
- [Huginn primary paper v1](https://arxiv.org/html/2502.05171v1), architecture section. [Author minimal implementation](https://github.com/seal-rg/recurrent-pretraining/blob/1ea7220ec7eb42d13e89db0663df254d0bcdc28e/recpre/raven_modeling_minimal.py), inspected attention/cache excerpts and forward/core/iteration interfaces; Git blob `0e83a0766644df9113a8923f43350c6a1b5a182c`. This is not a full training-repository review.
- [AVF primary paper](https://proceedings.neurips.cc/paper/2018/file/060afc8a563aaccd288f98b7c8723b61-Paper.pdf), equations 6–13 and Algorithm 1. [SRNN source](https://github.com/joelouismarino/amortized-variational-filtering/blob/f1032d62761c498e5206c0a2b07a012c8223b3de/lib/models/srnn.py), full returned source; blob `b7f696fc102c4c55a4fcf5fa586416b145b6e846`. [Training loop](https://github.com/joelouismarino/amortized-variational-filtering/blob/f1032d62761c498e5206c0a2b07a012c8223b3de/util/train_val.py), inference/generation/step sections; blob `63bfd37258b7408da6ca644902479b029436da10`.
- [RLT author README](https://github.com/yifanzhang-pro/recurrent-looped-tranformer/blob/b323cbc6e349237b755600b13f2d9bde73e82ff3/README.md), observed source blob `02681f724cf9de433524b17bc58e3e57f03783d0`. Read as a nearby architecture description only, not a verified reproduction or primary result audit.

This review writes only this file. It does not update the checkpoint, method pool, gate report, Git history, or remote repository. Publication and project-state reconciliation remain with the single integration writer.
