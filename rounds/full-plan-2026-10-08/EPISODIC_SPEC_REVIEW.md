# Independent review: causal exact-event memory specification

Date: 2026-10-08. Reviewer identity: `/root/episodic_spec_review` (queryable through the host collaboration registry). Reviewed baseline supplied by integration writer: `fba4653780e0b277a1fe7fdef47e3f20d33f2d53`; read the checkout's AGENTS, expanded IMPLEMENTATION_GOAL, adopted FULL_MODEL_PROPOSAL, MATHEMATICAL_DESIGN, SCIENTIFIC_SCOPE_REVIEW, SIGMA_REVIEW and model source. Status: specification/source review, `generated_unexecuted`; no project code, imports, tests, environment setup, training or asset acquisition executed. This reviewer writes only this file and does not integrate or push.

## Decision and scope

Accept a bounded, immutable token-event store with deterministic lexical retrieval and a differentiable neural reader as a **known-mechanism engineering extension**, provided the conditions below are implemented. This decision qualifies a concrete causal predictive model, not originality, posterior calibration, predictive sufficiency, factual truth, or task benefit. Independent source review of its eventual implementation remains necessary.

The sources support non-differentiable historical retrieval followed by trainable attention, historical-only memory updates and FIFO capacity management. They do **not** supply this exact lexical event store, identity protocol, provenance policy or raw-token reader unchanged. Those are explicit implementation choices. No discovered paper is represented as the project's new mathematical contribution.

## Executable mathematical contract

For one identified document/stream, let completed segments be `X_0,...,X_{s-1}` and current target token be `x_{s,j}`. `M_s` is the compressed state after the completed segments; `B_s` contains only retained immutable events from those segments. Event identity is `(stream_id, segment_ordinal)`, not a hash of token content: independent events can have identical content.

An event contains identity, immutable token tuple, **per-token** declared source origin (`observed_text`, `generated`, or `scored_continuation`), and source locator/version where available. The raw-payload capacity bounds both retained events and retained tokens; admission rejects events longer than the admissible per-event length, rather than silently truncating an event while calling it exact. FIFO eviction removes oldest complete events, not individual tokens from otherwise supposedly exact events. Segment digest receipts persist across the current document; public caller chunk receipts persist across the entire stream, including EOS, to verify whole-chunk retry atomically. **Total** memory is therefore O(number of consumed current-document segments plus identified stream chunks), not a constant-memory model. This is an explicit change from the initial high-watermark-only proposal, made to permit conflict checking after raw-token eviction.

For each supervised target position, use only its known prefix:

\[
 q_{s,j}=Q(x_{s,\max(0,j-w):j}),\qquad
 A_{s,j}=\operatorname{TopK}_{e\in B_s,\,eligible(e)}
      \bigl(score(q_{s,j},e),tie(e)\bigr).
\]

`Q` is a declared bounded token-set/term-count transform. A transparent overlap score is `|terms(q) intersect terms(e)|`; call it lexical overlap, **not BM25**, unless the actual BM25 formula, tokenizer, corpus-statistics scope and tie rule are implemented. Deterministic ties may use recency then ordinal. The empty-query and no-match policy must be explicit; using a declared recent-event fallback is causal but is a different retrieval policy whose selections must be logged. PAD/SEG/EOS and any ignored frequent token IDs must be specified independently of test answers.

Retrieve at most `k` events and at most `r` token positions under a fixed policy. If the neural read budget covers only a prefix or selected positions of a stored event, the store is exact but the **reader's access is partial**; record omitted token counts and offsets. Prefer configuring `r >= k * max_event_tokens` to avoid accidental truncation. Encode selected positions as

\[
 v_{e,a}=Emb_\theta(e.tokens[a])+Pos(a)+EventRank(e)+Origin(e.origins[a]),
\]

with an explicit event-position/order representation or an order-sensitive event encoder. Plain raw token embeddings with attention alone are permutation invariant in their memory key/value order; storing ordered tokens does not mean the reader can distinguish their order. `EventRank` can be bounded retrieved-rank metadata, not an unbounded learned ordinal table. Metadata must be available from history without privileged answer annotations.

For position-specific selected keys/values, one possible consumed read is

\[
 c_j=W_o\sum_{a\in A_{s,j}}
   softmax_a\!\left((W_q h_j)^T(W_kv_a)/\sqrt d\right)W_vv_a.
\]

Add/gate this result into the actual reader before recurrent computation or in each recurrent block; specify the chosen site. The attention source for position `j` is only `A_{s,j}`. Never flatten the union of selections for every current position into an unrestricted shared memory: another position's query could depend on tokens unavailable at `j`. Empty selection must produce a defined zero read or masked null item, with no all-masked softmax NaN.

### Causal and teacher-prefix argument

Let `F_{s,j}` denote the sigma-field generated by completed observed segments, permitted provenance, the current prefix `x_{s,<j}`, fixed parameters, and independent computational randomness. `M_s`, `B_s`, `q_{s,j}`, the selected tokens and their neural embeddings are `F_{s,j}`-measurable. The causal prelude and reader position `j` depend only on earlier/current known-prefix rows; by composition their logits are `F_{s,j}`-measurable. Therefore the categorical prediction of `x_{s,j}` cannot depend on its target or later tokens. Training loss may subsequently use the target; that does not authorize passing it to retrieval or read state.

In this repository `forward_segment(tokens,memory)` predicts the **same** token positions from `[SEG,tokens[:-1]]`; query for row `j` is `tokens[:j]`, not `tokens[:j+1]`. `predict_prefix(tokens[:j],memory)` must choose exactly the same event IDs, offsets and origin policy as teacher row `j`, with fixed weights/state. Current-segment raw tokens are committed **after** reader prediction of that segment; they cannot enter its own memory bank. LongMem's sequence-level causality alone does not repair a query constructed from a full teacher-forcing segment.

### Likelihood and gradient

The concrete model is

\[
 p_\theta(x_{1:N})=\prod_i p_\theta(x_i\mid M_i,B_i,x_{<i}),\quad
 L_{CE}=-\sum_i\log p_\theta(x_i\mid M_i,B_i,x_{<i}).
\]

The deterministic `M_i,B_i` histories introduce no random latent density or ELBO/KL by themselves. Since the token-ID overlap selector is independent of learned weights, CE gives ordinary gradients through **current** token embeddings/projections/read attention and the reachable compressed writer, with no selector gradient. Re-embed stored token IDs using current parameters; do not cache detached learned embeddings indefinitely while claiming fresh full gradients. No target-labelled retrieval training is required. Existing sequential text and true document boundaries suffice; TBPTT truncates writer gradients but must not discard the bank's forward history accidentally.

## Mandatory objections and resolutions before implementation

| Issue | Required resolution |
|---|---|
| Duplicate replay can update compressed belief twice even if the event store is idempotent | Check admission identity **before both** compressed writer and event-store mutation; one transactional commit boundary. Reader loops never advance admission state. |
| A high-water mark cannot verify token equality for an already evicted event | Accepted integration decision: retain consumed-event SHA256 receipts through the current document and public-chunk receipts across the entire stream. Retained duplicates compare full immutable tokens/provenance/source locators; evicted duplicates compare canonical digests. The latter is computationally checked under collision resistance, not mathematically exact content equality. Reject any mismatch. Receipt count and serialized/RSS bytes grow with history and must be measured. |
| Watermark can suppress a never-consumed out-of-order event | Enforce sequential internal segment ordinals and persist the next ordinal; stale receipt IDs cannot mutate. Public caller chunk IDs live in a separate namespace and may have arbitrary values; admission receipts, not lexical ID ordering, determine whether already consumed. Reset with a distinct document identity and delete the old document's receipt table only under the declared reset policy. |
| Provenance and memory clocks can disagree | The adopted integration supports origins per token, including mixed external/generated segments. External-only retrieval must mask generated positions even inside selected mixed events: either score/filter only external positions or reject mixed events as a declared stricter policy. Origin embeddings do not by themselves prevent access. Generated rollouts are separate branches or explicitly generated-origin history; their content is never relabelled independent evidence. |
| Completion/EOS/partial prefix mismatch | Retain incomplete prefixes in serialized state, including origin metadata; preserve the existing complete non-EOS commit contract. Do not flush a short terminal segment into future bank reads unless an explicitly separate finalization contract is adopted. Training's final segment may be ephemeral if no future read occurs. |
| Restore can silently change selected history | Persist token tuples/origins, identity, source, FIFO order, next internal ordinal, complete consumed receipts, capacities, retrieval policy/version, tokenizer/model/config identity and current partial prefix/origins. Reject mismatched identities/configuration; reconstruction cannot fetch unrelated external context. |
| Public chunk retry mutates a partial prefix twice | Check public `ingest(observation_id=...)` receipt before changing any prefix/origin/writer/segment state. Canonical digest includes ordered token IDs, per-token origins and applicable source metadata; persist its schema/version and distinguish chunk IDs from segment IDs. Stage all resulting state and commit atomically: validation failure cannot leave a partially accepted chunk or a receipt for work not performed. |
| API caller can forge external event truth | Origin is input metadata, not independent verification. Exact token storage proves retention of admitted input, not its factual correctness. Native evaluator constructs events from allowed problem history and never from answers/support labels. |

## Information and cost accounting

Adding raw historical access expands the compressed-only model's available information. Compare full versus compressed-only as an **information/access ablation**, not pure compute improvement. Compare full K=1 versus K=4 with identical event banks, same per-position selector policy and read budgets to isolate internal computation. Include a fixed-depth retrieved-memory control or explicitly limit the conclusion to an engineering ablation. Match target-token training exposure; memory-read/replayed tokens are separate context-access counts, not extra target tokens. Report cross-document memory resets.

Record scanned events, scanned token/term counts, selected events, requested/read/omitted tokens, CPU retrieval wall time, actual CPU RSS (Python object accounting is not just `4*token_count`), device transfer/embedding/attention time, GPU peak bytes, total wall time, raw-event serialization bytes, **receipt count/serialization bytes and hashing/admission time**. If selecting per target requires moving prefixes GPU-to-CPU, synchronization and transfer belong in total cost. A naive selector scanning `C` retained tokens for each of `L` target positions costs approximately `O(L*C)` lexical work per segment; bounded raw payload is neither constant-total-memory nor constant-time retrieval. No 2080 Ti fit or throughput claim follows from this review.

## Required Local acceptance cases (not executed here)

1. Teacher row/prefix inference event IDs, token offsets and logits agree within declared numerical tolerance, including `j=0`, empty bank, unmatched query and capacity eviction.
2. Perturb target and future suffix without changing the allowed prefix: earlier selections/logits do not change. The current segment is absent from its own bank.
3. Demonstrate actual reader consumption through changed historical tokens at fixed IDs in separate valid runs; verify differentiable embedding/read parameters receive gradients. This is a software semantic check, not task performance evidence.
4. Retained identical duplicate produces no writer/store/clock change; retained and evicted content/origin conflicts reject; identical evicted replay cannot resurrect memory; skipped internal ordinal rejects. Public chunk retry spanning segment boundaries leaves every state/clock unchanged. Save/restore preserves those decisions.
5. Generated-origin events cannot appear in external-only selections. Mixed-origin partial prefixes and EOS behavior follow their defined policy.
6. Serialize/restore mid-prefix and post-eviction produces the same next selections and logits; config/tokenizer/source mismatch rejects. Document reset removes bank, segment receipts, ordinal and compressed state together, while keeping public caller chunk receipts for whole-chunk replay. Invalid public chunk, including invalid token/origin/ID after a valid prefix, leaves all input state unchanged.

## Primary sources actually inspected

- **Memorizing Transformers**, arXiv `2203.08913v1`, §§3.1–3.2: [primary full text](https://arxiv.org/html/2203.08913v1). Examined per-token non-differentiable memory retrieval, trainable attention fusion, old-item removal, document reset and cached-representation staleness. It stores learned key/value representations, not raw token events or lexical overlap; neither its result nor its resource measurements transfer to this implementation.
- **LongMem**, NeurIPS 2023 camera-ready, §§2.1 and 2.3: [primary PDF](https://proceedings.neurips.cc/paper_files/paper/2023/file/ebd82705f44793b6f9ade5a669d0f0bf-Paper-Conference.pdf). Examined segment-after-read memory updates and per-token retrieved fusion. Published memory encodes previous segments with a frozen backbone; proposed raw-ID re-embedding uses a different cost/gradient path.
- **Author LongMem code**, verified repository main pin `b7f3c6b8db7471eb507971451f63f67e21c49ebf` via GitHub commit API on 2026-10-08: [dynamic_memory_with_chunk.py](https://github.com/Victorwz/LongMem/blob/b7f3c6b8db7471eb507971451f63f67e21c49ebf/fairseq/fairseq/modules/dynamic_memory_with_chunk.py), full source read (`External_Memory`, `reset`, `add_index`, `retrieve`). Uses chunk-averaged FAISS keys and returns selected key/value tensors. [joint_multihead_attention_sum.py](https://github.com/Victorwz/LongMem/blob/b7f3c6b8db7471eb507971451f63f67e21c49ebf/fairseq/fairseq/modules/joint_multihead_attention_sum.py), inspected `forward` and active `joint_multi_head_attention_forward` consumption/fusion; not executed. Do not copy its device-specific storage code as a portable CPU implementation.
- **TRIME** author [README](https://github.com/princeton-nlp/TRIME), inspected its BM25 batching and external-memory training description as adjacent lexical-memory precedent only; no exact source pin/reproduction established and no TRIME loss adopted. In-batch other-segment memory has different information access from this strictly historical contract.

Remaining implementation verification is owned by a separately identified source reviewer after the integration writer supplies actual diff. All Local software/native/hardware/scientific acceptance remains pending.
