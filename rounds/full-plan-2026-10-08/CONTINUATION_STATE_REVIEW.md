> Publisher attribution note: preserved inherited draft review. This publishing invocation does not certify the named worker as a currently live/queryable context. Its source findings are retained; current independent review and exact byte bindings are provided by EPISODIC_SOURCE_REVIEW, DYNAMICS_SOURCE_REVIEW and INTEGRATION_SOURCE_REVIEW.

# Independent continuation, history and realization source review

Reviewer: `/root/expansion_integrity_review`, independently queryable in this Work invocation. Status: `generated_unexecuted`, static source review only. No project import, project code, test, training, model download or GPU invocation was executed. This record reviews the actual draft bytes below, not the conclusions of earlier reviews. No publication authority was used.

## Verdict

No Critical or Important defect was identified in the inspected standard model/training/generation paths. This is a bounded source judgment, not a software pass, native parity receipt, hardware acceptance or scientific validity claim. Local acceptance remains pending. A source change invalidates this review's corresponding input digest until re-reviewed.

The implementation is the finite engineering construction described by EXPANSION_SPEC: exact retained tokens plus compressed slots, lexical/recency retrieval, a narrow token-prediction plan, and fixed-depth reasoning. It does not establish predictive sufficiency, identified semantics, faithful independent sentence decoding, autonomous action/world dynamics or novelty. The deliberately narrower mathematical claims in the specification are necessary to interpreting the code.

## Checked information and state paths

1. **No current/future target in retrieval query.** `model._retrieved` selects each row independently using `known[max(0,u-q):u]`. The supplied store is prior completed history; it does not union later-row queries into earlier-row attention. `_encode` prelude and `_language` coda are causal. `forward_segment` drops the last evidence row before reading, preserving the same-position prediction contract.
2. **The history is consumed by the model.** Selected raw IDs, original positions, selected-event rank and origin are freshly embedded. The pointwise `EpisodicReader` attention affects the actual reader hidden state or fixed contractive forcing. A zero sentinel makes empty attention finite and its result is multiplied by zero. Selection is nondifferentiable; the fresh embedding/attention path is differentiable. Store append happens after the current segment's model call in `train.window_objective`; the successor-token label only enters its separate CE.
3. **Writer separation is real.** `commit_segment` calls `_write(_encode(tokens)[:,1:], memory)` without reader/retrieval/plan input. Both reader dynamics keep the admitted store fixed across K. Generated output is observed only after its distribution has been obtained. Reader depth therefore cannot rewrite the prior observation in this functional path.
4. **Identities, replay and eviction have actual code.** Episodic ordinals must be consecutive, receipts verify token/origin/source digests, and replayed evicted events cannot be reinserted. FIFO evicts entire events when raw capacity is exceeded. Identified chunks verify their complete digest before token transitions; receipts survive EOS, so a retry spanning a reset is a no-op. Anonymous identical text remains a new input. Sources are locators, not proof of truth.
5. **Origins remain distinct.** Stream prefix, events and persisted payload retain per-token origin/source. Generated raw positions are filtered before lexical ranking by default, including mixed-origin events. Scored continuation tokens enter only after their own likelihood has been evaluated, and are labelled `scored_continuation`. Native bAbI ingest consumes context, then generates; LAMBADA ingest consumes context, then sequentially scores the target. Future labels are not passed to ingest as evidence in those adapters.
6. **Restore has meaningful validation.** `restore_stream` validates tensor shapes, finite bounded memory, token bounds, prefix provenance, capacity/config, unique chunk IDs and digest syntax, nonnegative clocks, and document/segment consistency. `EpisodicStore.from_state_dict` validates each retained payload against its receipt, full segment length, token bounds and ordered FIFO suffix. Historical evicted receipt digests cannot authenticate lost token contents; this is an unavoidable disclosed receipt-only boundary, not a claim of evidence authenticity. Missing-format legacy state is restricted to disabled-extension v0.
7. **Plan realization is a connected bottleneck.** Enabled training reads `tanh(plan_projection(workspace))` through `realize_plan`; enabled generation uses `plan_next` then `realize_plan`. The callable realization path receives only the plan, projects it to language width, applies the causal coda and shared vocabulary parameters, and never calls reader/writer/retrieval. `plan_snapshot`/`restore_plan` bind checkpoint, tokenizer, config, implementation, context and plan content. The CLI restores the plan and writes actual next-symbol logits/token. This is independent realization of a complete causal per-token plan sequence, not an independently identified semantic language codec or one frozen plan yielding an entire sentence.
8. **Three clocks have an explicit functional transition.** Observed text increments the observation clock, emitted output increments expression, and `plan_next`/generation increments reasoning. Completed segments and documents have separate counters. `next_logits` is a pure read and `score_continuation` does not return its temporary branch; their actual computation is recorded in `model.audit.reasoning_row_steps`. Consumers must not use stream reasoning_clock alone as total inference cost. The audit/cost interface is the appropriate source for that quantity.

## Minor item and concrete remedy

**M1 — plan digests assume a NumPy-supported tensor dtype.** `realization.tensor_digest` calls `value.numpy().tobytes()` after making a CPU contiguous tensor, while snapshot validation permits any floating dtype and the public model can be explicitly converted to bfloat16. PyTorch-to-NumPy conversion commonly does not support bfloat16, so such a valid-looking snapshot request can fail before persistence. Current delivered CLI/default model is FP32 and training uses FP16 autocast with FP32 parameters; no impact on those specified paths was found. Remedy: hash a contiguous `uint8` view of tensor storage while retaining the original dtype/shape metadata, or explicitly reject/document unsupported plan/state dtypes at the interface. This is not a claim that bfloat16 GPU execution is supported on 2080Ti. Local should qualify any dtype it actually adopts.

No mandatory correctness repair is requested from this bounded review. Optional Local probes supplement the authored cases: source/payload mismatch rejection, caller-ID replay after intervening input and after multiple EOS resets, event-receipt conflict after eviction, and explicit clock/cost interpretation. Their results must be collected by Local; this reviewer did not execute them.

## Exact input SHA256

The following are reviewed input bytes, not a remote-commit certification:

| Path | SHA256 |
|---|---|
| AGENTS.md | `e6bcd6b0b1793cebf257bb83c648b27f0deda3750e7683aa46dc13674cf11b19` |
| rounds/full-plan-2026-10-08/EXPANSION_SPEC.md | `03131f0453601ede4505afc9f1d38b60e3ebd3e0287bfcf2cc4ffea0d8abc5e0` |
| rounds/full-plan-2026-10-08/IMPLEMENTATION_GOAL.md | `01bd58706b9a168b262a02b67a470be6929960059296483daa086f4c571f7a10` |
| src/lwm/episodic.py | `ea14eb243777532ddd7f729dd46857e19a19df698a6d5580b58d15bfe4ebedc1` |
| src/lwm/generation.py | `264c9fb9437f73fddaf459d61b18e29e724d83be208bda8ccc00484f20bc44ac` |
| src/lwm/realization.py | `e3447da48a982c454893cf01506e343e3b028979e41a90c944520efab276269a` |
| src/lwm/model.py | `27be3e0b571b207c62985e269f6e3e4ad33a6aa38fc9f508ef0eccc11201096d` |
| src/lwm/train.py (history/window-objective scope) | `818b572480343d65a7a9f7a9bf6c50e43e9f6ba2cd7b29e986a1630fb49de0be` |
| src/lwm/evaluate.py | `ca141f364599a6b205386639be78f56ed42cfd462388a918355d0e9e94b6d5ce` |
| tests/test_expansion_semantics.py | `6a0afdb1bbd2d5132f5ca196e56f3620d7d88248a4d0ca3c1179afc79efd29fd` |
| tests/test_episodic_semantics.py | `832fd1f6b1df5d67eb4b4119309cfe671519c76f45275ffc813074fba61a5cf1` |

Acceptance fixtures were read to identify authored coverage and gaps, not run. The trainer changed during review from `9a7c16512efd0c80b4581cccbda10f4355bcf5371717c1fa2985c9a62559df19` to the recorded current digest; its history/window-objective section was reread and is unchanged in the reviewed causal path. The full trainer is outside this review's independent approval scope. The root integration writer must reconcile these hashes against the exact delivered main bytes; no git metadata existed in this local draft directory at review time.
