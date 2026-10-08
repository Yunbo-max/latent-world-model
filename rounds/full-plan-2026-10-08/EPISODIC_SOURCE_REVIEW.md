# Independent episodic SOURCE review

Reviewer: `/root/episodic_spec_review`. Date: 2026-10-08. Role: Web static source review only. No project code, imports, tests, native scorers or GPU work executed. Integration and publication belong to root. Status: `generated_unexecuted`; findings below are source-derived, not passing software evidence.

## Bound source snapshot

This is a working-tree review above parent `fba4653780e0b277a1fe7fdef47e3f20d33f2d53`, not a claim that these bytes already exist at a remote commit. The integration writer must record the final remote commit after exact readback. The initial review findings are retained below; the following bindings are the **final source reread** after their resolutions on 2026-10-08:

| File | SHA256 |
|---|---|
| `src/lwm/episodic.py` | `ea14eb243777532ddd7f729dd46857e19a19df698a6d5580b58d15bfe4ebedc1` |
| `src/lwm/model.py` | `27be3e0b571b207c62985e269f6e3e4ad33a6aa38fc9f508ef0eccc11201096d` |
| `src/lwm/generation.py` | `98e2a57b3a4024332a45879cfd533532938f1fb57782f3bd96f8058868fa1798` |
| `src/lwm/train.py` | `8e41f8e523c604e1e12531ed8c37fcf1cc1af10cc87c63f94123405b8401a2d6` |
| `src/lwm/evaluate.py` | `ca141f364599a6b205386639be78f56ed42cfd462388a918355d0e9e94b6d5ce` |
| `src/lwm/realization.py` | `e3447da48a982c454893cf01506e343e3b028979e41a90c944520efab276269a` |
| `tests/test_episodic_semantics.py` | `832fd1f6b1df5d67eb4b4119309cfe671519c76f45275ffc813074fba61a5cf1` |
| `tests/test_expansion_semantics.py` | `384590e2701aa312cd70f4394b019f7539e0f021b983f0a885e26e2bc5970430` |
| `EXPANSION_SPEC.md` | `03131f0453601ede4505afc9f1d38b60e3ebd3e0287bfcf2cc4ffea0d8abc5e0` |

Also inspected supporting `data.py` cursor and native `evaluate.py` call/cost excerpts to determine actual training/evaluation information paths. Any subsequent edits invalidate the bindings for changed files and require an explicit incremental review entry.

## Accepted source paths

1. **Strict target causality:** `_retrieved` slices `known[max(0,u-query_tokens):u]`. Teacher row u is obtained from `_encode(tokens)[:, :-1]`, whose u-th row depends on the same `tokens[:u]`. Prefix inference computes the full causal prefix before selecting its final output row. Copying the full segment to CPU does not itself create a model-visible future dependency; the selection slices exclude it.
2. **No union-of-future-queries edge:** selected embeddings have shape `[rows,budget,d]`; `EpisodicReader` treats rows as independent attention batch lanes `[rows,1,d]`. The neural reader cannot attend to another target's retrieval list. Causal core/coda can use earlier rows, whose information is also available now.
3. **Fresh differentiable consumption:** retained payloads are Python integer/origin tuples. `_retrieved` re-embeds IDs and adds position/rank/origin embeddings under current weights. Attention consumption occurs in `_workspace`, including actual training/prefix generation, not only in an unused helper. No learned selector gradient is claimed.
4. **Empty bank behavior:** false validity rows are given one zero sentinel key then their outputs are zeroed. This avoids an all-masked softmax, without adding an unmasked learned null channel. `_retrieved` requires batch=1 before row reshaping.
5. **Mixed source filtering:** `retrieve` removes generated token positions before lexical scoring and neural selection unless explicitly enabled; original within-event positions are preserved. `scored_continuation` is deliberately available as known likelihood-prefix history, distinguished from external input and generated tokens. It is not independent evidence.
6. **Event receipts and FIFO:** immutable append creates a new store, leaves raw data bounded by token capacity and keeps digest receipts after eviction. `check` verifies retained full token/origin equality as well as digest. Restored events must form the exact FIFO suffix and match their receipt digests. Digest equality after eviction remains conditional on collision resistance.
7. **Inference admission and branches:** `ingest` validates the entire token chunk and its explicit receipt before token transitions. `observe` checks segment identity before `commit_segment` and only appends afterward. State transitions replace rather than mutate the caller's memory/prefix/store values. Generation produces a returned branch with generated provenance, and scoring consumes each target only after scoring it.
8. **Training history:** `new_history`, `window_objective`, checkpoint history payload and `restore_history` connect the store to sequential text training. Histories survive TBPTT windows; true cursor document resets isolate histories. Loss-mask targets never enter the current segment's retrieval. The auxiliary next-segment target enters its loss only. Training restore checks store document identity, capacity and segment ordinal against the training ledger.
9. **CLI checkpoint identity:** generation CLI verifies checkpoint SHA256 and tokenizer identity before accepting stream state. Direct `restore_stream` is a lower-level structural loader; callers outside the CLI need the same outer identity contract.

## Initial findings, retained as review history

| ID / priority | Actual source finding | Required resolution |
|---|---|---|
| E01 / high | `restore_stream` accepts stream-v2 with absent `prefix_origins` and silently assigns `observed_text`; missing clocks/receipts default. A malformed snapshot can relabel generated partial tokens as observed. | Require all v2 structural/provenance/ledger fields; only permit legacy defaults for genuinely legacy v0/no-episodic states. Reject missing v2 origin data rather than repairing it. |
| E02 / high | `window_objective` invokes `forward_segment` and its belief writer before episodic `append/check`. Ordinal is presently always next, so normal cursor flow cannot replay an old ordinal, but the explicit pre-writer admission contract is absent from training. | Validate/stage raw tokens/origins and call `store.check(next_ordinal,...)` before the forward/writer path. Document that training windows without caller chunk IDs are new cursor observations, not replay-safe API ingestion. |
| E03 / medium | Public chunk receipts intentionally survive EOS; `test_document_reset_drops_raw_events_without_forgetting_chunk_retry` asserts this. Specification/reviewer text says receipt lifetime ends at document reset. | Retaining stream-global chunk receipts correctly supports retry of a chunk spanning EOS; disclose O(total accepted chunks in stream), separate it from per-document segment receipts, update lifetime/reset prose and count its bytes. |
| E04 / medium | Stream restore accepts arbitrary store document ID with a nonnegative document clock; no linkage is checked. Generation's ordinal is per document but segment_clock is global. | Validate the known generated `stream:{document_clock}` identity contract, or explicitly serialize a caller document identity and per-document segment clock. Verify receipt/clock compatibility, not shape alone. |
| E05 / medium | `LatentWorldModel.forward` has no `episodic` argument and delegates to a method that requires an explicit store for enabled mode. Calling the ordinary model module fails for this valid configuration. | Expose the same episodic keyword as `forward_segment`, or explicitly document and remove misleading unsupported generic-forward interface. |
| E06 / medium | Retrieval token budget takes ordered suffixes, but metrics report only scanned/selected/read totals; omitted-token counts and actual selected IDs/offsets are absent. | Report omitted accessible positions/events and provide auditable selection provenance/offsets or a digest/trace mode. Do not label all retained event contents as read. |
| E07 / medium | Native evaluator has total wall/GPU peaks but the reviewed cost excerpts export neither model retrieval audit nor process RSS. Training audit includes validation reads without a separate scope, and `retrieval_cpu_seconds` ends before JSON accounting/transfers/embedding/attention. | Export explicitly scoped retrieval counters and state/receipt bytes in native results, process RSS high water, and either separate validation from optimization audits or label accumulation scope. Keep end-to-end wall as inclusive cost; do not present lexical timer as all retrieval/device cost. |

No training-answer/future-token leak was identified in the reviewed causal read path. That finding does **not** resolve malformed restore, interface/cost gaps or replace Local semantic tests.

## Final reread: resolutions and decision

| ID | Source resolution actually reread | Decision |
|---|---|---|
| E01 | Stream-v2 requires memory/prefix/origins/source locators, store/receipts and every clock. Missing-format legacy restoration is rejected whenever episodic, semantic, contractive or predictive extensions are enabled. Legacy defaults therefore cannot downgrade expanded-state checks. | Resolved in source. |
| E02 | Complete training segments stage their raw IDs and call `store.check(next_ordinal,...)` before `forward_segment`/writer. Caller-less training remains cursor-consumed data; it does not claim public-ingest retry semantics. | Resolved in source. |
| E03 | EXPANSION_SPEC now separates per-document segment receipts from stream-lifetime public chunk receipts. EOS retains public IDs to verify whole-chunk retry. `stream_accounting` reports their count/serialized size; updated EPISODIC_SPEC_REVIEW matches. | Resolved by explicit, disclosed scope. |
| E04 | Restore validates store document identity equals `stream:{document_clock}` and per-document receipt ordinal cannot exceed global committed segment clock. Training restore still validates its own exact document/segment ledger. | Resolved within the declared structural contract; not an authenticated truth/provenance guarantee. |
| E05 | Generic `forward` exposes the episodic keyword and passes it through; the full-factorization authored fixture uses `model(...,episodic=...)`. | Resolved in source. |
| E06 | Retrieval reports selected-token omissions and event IDs/original offsets. Model audit keeps cumulative counts and explicitly named **last** retrieval trace. One raw lexical index is rebuilt per neural read and shared across target rows, preserving each row's strict prefix query. | Resolved; last trace is diagnostic, not claimed complete historical selection log. |
| E07 | Native rows reset/export audit, report prompt/output stream payloads, and aggregate accesses/lexical time plus process RSS. Train snapshots label their invocation-cumulative scope; validation resets its own audit then restores training audit. Native timing explicitly excludes device embeddings/attention/receipt work from lexical timer while total inference wall includes them. | Resolved for inclusive cost accounting; per-operator GPU timings are not separately claimed measured. |

Final generation CLI stream snapshots additionally persist/verify model config and source-file identity through `implementation_identity`, along with checkpoint/tokenizer, sampling device and temperature. Raw events now store per-token source locators and their digest incorporates those locators; explicit chunk retry digest incorporates EOS policy, preventing one ID being replayed under a different boundary interpretation. Raw/source fields are validated on restoration. Caller IDs remain unauthenticated metadata.

The original causal/read gradient conclusions survive the fixes: no target/future selection edge was found, row-isolated attention consumes fresh embeddings, generated token positions are filtered before lexical scoring, and current segment commits remain after reading. Existing episodic tests and new expansion fixtures were **read only**; they cover generic-forward/prefix parity, future isolation, malformed v2 origins, direct writer independence, full trainer/store restore and standalone realization. No test pass is inferred.

**Final decision:** accept these bound bytes for source delivery of the episodic engineering extension and its reviewed integration. No unresolved Critical/Important source finding remains within this review's scope. This is neither whole-project scientific acceptance nor a runtime result; all Local software/native/hardware/scientific checks remain pending. New edits require incremental review and new hash bindings.

### Final integration delta reread

The final hash table includes a further narrow source-only reread on 2026-10-08. `restore_stream` now rejects a missing format whenever any v2-only marker remains, even with extensions disabled; only genuinely historical v0 payloads without those markers may use legacy defaults. The authored `test_disabled_extension_stream_cannot_downgrade_to_legacy` explicitly covers rejection and the genuine legacy memory/prefix path; this fixture was read, not run.

Trainer update receipts additionally report CUDA allocator reserved high water separately from allocated high water. The gradient inventory is taken before `zero_grad` and is correctly labelled as tensors/elements whose gradient is present, not nonzero gradient or effective capacity. Validation takes the configured auxiliary weight, preserves main CE as text NLL, reports head CE sum/pair count/per-pair separately, and forms the weighted objective using the main-target denominator; it still restores training audit after its own isolated audit. The corresponding new validation bookkeeping fixture was read only. These changes preserve the reviewed causal and admission paths, add no target-dependent state input, and introduce no new Critical/Important finding within this review scope.

## Important conditional behavior to disclose

- Training treats corpus tokens as `observed_text`; native teacher-forced continuation uses `scored_continuation`; free generation labels predictions `generated` and defaults to excluding their raw positions from later episodic retrieval. Thus exact teacher/prefix parity holds at identical state/provenance. Across free-generation segment boundaries, changing token origins intentionally changes allowed retrieval even if token IDs happen to match. Avoid claiming unconditional train/free-generation selection equality.
- The compressed writer still incorporates generated-prefix segments into the **returned generation branch**. An external-only raw reader does not purify the compressed branch of generated content. The accepted contract is functional branch/provenance, not a posterior that contains external facts only.
- Terminal training segments may contain EOS and be processed transiently before document history is dropped. No subsequent training example can read that terminal history. Generation EOS discards partial prefix/raw segment history instead. Only equivalent eligible prefix/next-token predictions should be compared; terminal post-state parity is not promised.
- Frozen dataclasses prevent attribute reassignment but do not make underlying Torch tensors intrinsically immutable to callers. Internal transitions inspected here avoid in-place changes. External API callers must not mutate supplied state tensors in place.
- `serialized_cpu_bytes` measures JSON payload length, not Python heap bytes or RSS. Receipt growth and lexical scanning are real extra costs; raw-token capacity alone does not bound total stream memory.

## Local acceptance additions suggested to integration writer

Retain the existing unexecuted causal/gradient, receipt/conflict, mixed-origin, save/restore and branch tests. Add: missing v2 provenance rejection; malformed document ID/clock rejection; training pre-writer admission assertion; enabled generic-forward consumption; cross-EOS chunk retry and receipt-cost accounting; generated/observed/scored provenance policies across an actual segment boundary; native result includes scoped access counters. The existing future-suffix perturbation assertion covering rows `:3` after changing positions `2:` is mathematically correct: row 2 predicts target position 2 from positions <2.

The initial findings are resolved above at the final bound source snapshot. All software/native/hardware/scientific results remain Local-pending.
