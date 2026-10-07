# Engineering source review — 2026-10-07

**Status: source_reviewed / generated_unexecuted.** This records an independent read-only whole-packet review followed by bounded review of the integration fixes. No reviewer imported or executed the project, ran a test, obtained datasets/weights, or measured a GPU.

Scope: FULL_MODEL_PROPOSAL, all `src/lwm` modules, authored acceptance tests, all 15 model/stage configs, the experiment matrix and Local guide. The reviewer used the actual new working-tree files; the preexisting local HEAD alone did not contain them.

## Findings and source corrections

| Finding | Correction |
|---|---|
| A correction after AMP unscale and an overflowing FP32 global norm could escape expected update safety | Scale correction now precedes unscale; norm measurement uses FP64; nonfinite decoding/loss fails and AMP's detected nonfinite gradients retain its skip path |
| Half-rounded complementary gate weights could let persistent memory exceed its intended range | Writer gate/proposal nonlinearities and the persistent mixture are FP32; an unexecuted CUDA rounding-boundary regression is included |
| An old compatible checkpoint could overwrite newer output progress | Under-lock checkpoint identity checks; reject differing current output; use a new child directory for an older parent; freeze the resume-parent hash |
| An interruption could flush a partial accumulation and change AdamW updates | Signal/time requests wait for the natural accumulation boundary or a loss-free TBPTT boundary; deadline is explicitly soft |
| Setup failure could leave a lock or signal handlers behind | Cleanup encloses post-lock setup and nested finally blocks retain cleanup even if closing the log fails |
| Failed work lost input/target accounting since the last update | Failure events retain completed counters, pending accumulation and the current attempted window; incomplete work is an upper bound, never falsely counted as fully executed |
| Greedy decoding could turn nonfinite logits into apparently normal benchmark answers | Both generation and continuation scoring explicitly require finite logits |
| Text stream resume omitted sampling RNG | Serialized generator state, temperature and device-type compatibility are now part of stream resume |
| Separate native scorer environments could not import the project | Commands expose the repository's `src` path without installing incompatible model dependencies |
| Evaluation reporting omitted completion status, unscored IDs and timing scope | Manifests label checkpoint completion, retain failed/remaining IDs and distinguish setup/tokenization/whole-loop scope with first-example timing |

The whole-packet reviewer found no remaining critical or important correctness defect in the source it inspected after those fixes. A subsequent bounded review found the log-close cleanup edge above; the integration writer applied the nested-finally correction. This statement is a source-review conclusion, not a proof that executable tests pass.

## Properties inspected and limitations

The implementation follows the SEG target alignment, keeps old memory fixed throughout reader loops, preserves writer gradients across adjacent segments within each TBPTT window, and distinguishes document reset from gradient truncation. Data preparation/cursors preserve exact target budgets and document boundaries. Evaluation retains full selected native IDs/denominators and distinguishes local formula previews from actual official scorer replay.

Authored tests cover causal isolation, teacher/prefix correspondence, writer gradients, explicit truncation, functional state and EOS/commit boundaries, activation recomputation, gradient range, pinned preparation/scoring contracts, and actual training pause/resume semantics. These are software fixtures and assertions, not scientific results. CPU/FP32 resume equality does not establish cross-device or arbitrary nondeterministic CUDA bitwise equality; device type/GPU identity is now included in resume compatibility.

Still pending Local: actual package resolution/imports, complete assets, full bAbI author-teacher serialization parity, LAMBADA tokenizer/forward/scorer parity, every software check, CUDA FP16/checkpoint behavior, GPU fit/throughput, learning behavior and scientific conclusions. The full ParlAI environment card documents a concrete dependency conflict candidate and retains resolver qualification as pending; metrics-only replay cannot waive that obligation.

Static syntax/config/link checks are recorded separately in SOURCE_CHECKS.json. Exact GitHub byte readback is performed by the publishing session and reported with the delivered commit.
