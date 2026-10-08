# Independent dynamics, plan and objective source review

Date: 2026-10-08. Reviewer: `/root/dynamics_spec_review`.
Role: independent Web source review; **generated_unexecuted**. No project code, imports, tests, training, inference or asset acquisition was executed. The integration writer owns all implementation edits and main publication. This reviewer writes only this review file.

Review scope: `src/lwm/model.py`, `src/lwm/realization.py`, `src/lwm/generation.py`, `src/lwm/train.py`, against `EXPANSION_SPEC.md` and `DYNAMICS_SPEC_REVIEW.md`; relevant `episodic.py`, `data.py`, `checkpoint.py` and authored tests were read to inspect call/state boundaries. This is source review, not a scientific or software acceptance result.

## Construction findings

### Contractive branch

`ContractiveWorkspace.matrix` derives the matrix from the current FP32 weight and current Frobenius vector norm, with a denominator clamped at one. There is no detached normalization or power-iteration approximation. `_workspace` creates retrieval and forcing once, uses any causal core/history processing before the recurrence, and then performs only the tanh affine recurrence with the same matrix and forcing for fixed K. Its nonlinear recurrence has no reader-attention, RMSNorm, or residual bypass. The old writer is outside the loop. The matrix and forcing have explicit nonfinite checks.

Autograd remains connected through the matrix normalization, every recurrence, forcing, plan, and realization; activation checkpointing wraps the ordinary core blocks without detaching state. The source therefore matches the reviewed real-arithmetic contraction construction. `contractive_last_step_residual` logs ||H_K-H_(K-1)||, not the separate fixed-point residual ||R(H_K)-H_K||. It performs no extra diagnostic recurrence and makes no readout/ground-truth or floating-point certificate claim. c remains a validated config constant in (0,1). Historical Q01 and adaptive stopping remain unimplemented and unqualified.

The contractive variant intentionally has a different communication structure: causal/core attention enters the forcing once, while subsequent steps are pointwise recurrent updates. The adapter and ordinary core modules are still registered; not all registered parameters are necessarily active in every branch. Parameter inventory and source path must not be read as a matched-effective-capacity theorem. Runtime gradient/norm/parity checks remain Local-pending.

### Latent plan and realization

The active factorization is `tanh(plan_projection(H)) -> plan_lift -> _language -> vocabulary logits`. `_language` receives only lifted plan values. No M, raw token sequence, prelude output, retrieval tensor or workspace bypass enters realization. Tied embedding **parameters** in the vocabulary projection are not a runtime raw-token/context bypass.

Training uses `_read` through `forward_segment`; online `predict_prefix` uses the same plan factorization. Real generation explicitly invokes `plan_next` and then `realize_plan`, rather than leaving the helper unused. Causal coda runs on the complete plan sequence before last-row-only norm/projection. This preserves the adopted complete-prefix dependency and same-token row convention.

The persisted snapshot stores explicit Z, model/config/tokenizer/checkpoint/source identities, plan digest, and the full stream context. Restore checks Z dimensions, finite floating values, boundedness, digest and all compatibility fields, then converts device/dtype explicitly. Realization CLI reconstructs the model and context identity, but does not re-run reader, writer or retrieval to reconstruct Z. It realizes one next-symbol distribution, not an unchanging sentence-level meaning or an invertible semantic codec.

Initial review found context hashing included `reasoning_clock` and `expression_clock`, unnecessarily invalidating reuse after compute-only/readout-only progress. The writer changed `context_identity` to omit these two counters while retaining them in the full stored context. Observation, prefix, memory, provenance, document/segment context and admitted receipts remain identity-bound. Source follow-up confirms this fix; changed evidence/prefix still causes a stale-plan rejection.

### Predictive state auxiliary objective

`predict_future` mean-pools the compressed slots, applies its own projection and tanh, and maps to the finite vocabulary using embedding weights. `window_objective` supplies cross entropy against the first real next-segment token from that head; it does not supply the token to `predict_future`, writer, memory or retrieval. The main helper computes auxiliary logits from incoming M before processing the next segment. A genuine previous complete segment and an eligible first target mask are required. The trainer resets memory/history at document boundaries and does not splice documents into a segment, so no successor target crosses EOS/document reset in the declared prepared corpus path.

The implementation deliberately uses `(main_CE_sum + beta*state_CE_sum)/main_target_count` at the actual accumulation boundary. The earlier specification review suggested per-pair normalization; `EXPANSION_SPEC.md` explicitly selected main-denominator normalization instead. This is mathematically lawful: the finite composite sum is a positive weighted combination of proper categorical losses, with effective auxiliary weight beta*N_pair/N_main. It must not be described as beta times a separately per-pair averaged loss. Main CE, auxiliary CE sum, pair count, beta, objective per main target and main-only NLL are separately logged.

Auxiliary labels are already main eligible targets. Their repeated supervision is explicit; they are not additional unique target tokens or extra history acquisition. No missing pair is invented. If mask[0] is true, the segment has at least one main target, so adding auxiliary to total_loss is safe. No available pair leaves auxiliary absent and pair_count zero.

Within a TBPTT window, M from a prior write remains connected to writer-exclusive parameters and gives the reviewed direct state-loss gradient path. At the first segment of a later window, detached M may still be evaluated by the auxiliary head, but its earlier writer gradient is truncated. This is a disclosed TBPTT limitation, not a defect in the categorical objective. The source does not estimate predictive mutual information, latent posterior KL, semantic reconstruction or a physical-action likelihood. Fixed K compute and capacity remain explicit constraints rather than arbitrary differentiable losses.

### v0 and end-to-end paths

All optional modules default off: episodic false, semantic_dim zero, Transformer dynamics, predictive_head false and state_prediction_weight zero. The old prelude/adapter/shared core/coda/writer equations and no-second-target-shift remain present. Additional key masks only apply when provided. New config defaults do not register optional plan, episodic, contractive or future-head parameters for v0. Initial checkpoint loading normalizes legacy ModelConfig before strict architecture/weight checks. Strict training resume remains source/config/corpus-bound, so an old executable checkpoint is not silently resumed under changed source; a reviewed weights-only child is the appropriate path.

`generate` creates functional branches and separately advances reasoning/output clocks; raw-event and compressed-state commits occur only as actual consumed tokens complete a segment. `ingest` checks stable chunk receipts before transitions. Score-continuation consumes targets as `scored_continuation`, retaining their conditional-likelihood origin rather than relabeling them observed external evidence. Training `history` persists exact stores across windows and serializes them at optimizer-boundary checkpoints. Ordinary evaluation retains main-text NLL comparability and uses the same model prefix path. These source connections exist; their runtime equivalence is unverified.

## Final expanded-state and acceptance-source follow-up

At the integration writer's request, reread the latest model, realization, generation, trainer, specification and the full expanded-resume fixture with its comparison helpers; inspected the expansion, episodic and generation acceptance source. No project code or tests were executed. This follow-up replaces the earlier binding for changed files.

- `prefix_sources` is appended per consumed token, committed into exact-event source locators, serialized and restored alongside origin labels. Generated tokens remain generated; anonymous input is explicitly anonymous. Source IDs describe provenance, not truth authentication. `restore_stream` rejects incomplete v2 records and limits missing-format legacy restore to v0; legacy missing provenance is conservatively generated/anonymous rather than observed evidence. The CLI persists and checks current model config/source identity in addition to checkpoint/tokenizer identity.
- Chunk replay digests now include the EOS boundary policy. Receipts survive across EOS for whole-chunk transactional retries; per-document event receipts reset separately. The specification reflects this lifecycle and the source checks replay before processing any token. The event store document ID and stream document clock are checked on restore.
- `_retrieved` builds one token-only lexical view per read and reuses it across causal prediction rows. Query slices still end strictly before the target row. Selected tokens are freshly embedded; no projected neural key cache or future query union was introduced. This optimization does not make forcing depend on evolving reasoning H.
- The persistent `auxiliary_target_observations` budget counter advances with completed windows, is serialized with counters, and resumes from the recorded value. It remains separate from seen/optimized main target counts. The old beta=0 path has zero auxiliary observations. In the expanded real-trainer fixture, document lengths 8 and 6, block size 2, window size 4 and budget 12 give pairs `1 + 2 + 1 = 4`: first document/window has a predecessor only for its second segment; the second window has an existing predecessor plus its own second segment; the next document resets and again has one eligible within-window predecessor. The paused checkpoint therefore has 1 and the terminal checkpoint 4. The cross-window head prediction uses detached M, so it counts supervised head exposure without claiming a historical writer gradient.
- `test_expanded_training_resume_preserves_events_and_auxiliary_budget` invokes the real trainer entry for full modules, pauses at a live-state optimizer boundary, resumes and compares model/optimizer/scaler/cursor/memory/history/RNG/counters against an uninterrupted run. The shared comparison excludes only wall time and explicit resume provenance. The expected source event receipts, document reset and auxiliary counts are coherent. This is a meaningful authored software acceptance fixture, not a passed execution result. The corresponding v0 fixture now explicitly expects auxiliary count zero.
- Prefix/teacher-forcing equality is conditional on equal store, provenance and parameters. Observed training text, scored likelihood prefixes and free-generated history have deliberately different origin policies; default retrieval excludes generated raw positions. The revised specification correctly avoids unconditional free-generation/teacher-forcing parity across these policy differences.
- Native evaluation resets model access counters per prediction row/example; per-example aggregation can sum those counters without summing repeated within-training-invocation snapshots. Its storage/cost records disclose lexical timing scope, raw reads/index scans, serialized state and process RSS separately. Complete native parity/results remain outside this source review.

No new unresolved Critical/Important source finding was identified in this final follow-up scope.

### Narrow integration-fix follow-up

Reread the subsequent concrete legacy-restore, validation-objective and resource-inventory changes without executing project code:

- Removing the format field from any payload retaining a v2 marker now raises `Missing stream format on a v2 payload; no legacy downgrade`, even with all extensions disabled. The new negative fixture constructs that exact disabled-extensions case. A genuine old v0 memory/prefix-only payload remains accepted and receives conservative generated/legacy-anonymous metadata. This closes the format-stripping route without treating unknown provenance as observed evidence.
- `validation_nll` now receives the actual auxiliary weight, collects main and state sums separately, retains main-only NLL/perplexity, and reports state CE per pair and the composite objective per main target. The actual training validation call passes `state_weight`. The authored validation fixture's first document has two block-4 segments (one eligible auxiliary pair), and its second document has one segment (zero after reset), so its expected pair count 1 is coherent. Audit snapshot/restore remains intact and no division occurs when pair count is zero.
- Training inventories parameter tensors with present `.grad` before `zero_grad`; its scope explicitly disclaims a nonzero-gradient count or effective-capacity proof. Allocated and reserved GPU peak memory are now separately logged, with CPU zero values. These are planned runtime measurements, not Web results.
- Reread the actual model's current fixed-forcing recurrence and realization path, and the related generation/test source after their hash changes. No new recurrent bypass, target access, objective-normalization or parameter-gradient detachment was introduced. The expanded resume auxiliary total remains 4 and v0 total remains 0.

No unresolved Critical/Important finding remains in this narrow follow-up. The updated hash binding below supersedes earlier changed-file bindings; test execution, numerical memory/norm verification and actual native/GPU acceptance remain pending.

## Source findings and follow-up

| Finding | Source severity and resolution |
|---|---|
| A plan became stale after an additional reasoning-clock increment with identical evidence | Important interface restriction. Addressed by excluding reasoning/expression-only counters from context identity; follow-up source inspected. |
| Validation reused training historical-access counters | Important cost-attribution confound. Addressed by snapshot/reset/restore around validation and separate validation historical_access; follow-up source inspected. |
| Restored M accepted finite unbounded/nonfloating tensors | Important restore-boundary integrity concern. Addressed: restore now requires floating, finite M with abs(M)<=1; source follow-up inspected. |
| Pre-generation --plan-out built an unused autograd graph | Minor avoidable memory/cost concern. Addressed by explicit no_grad around plan generation; source follow-up inspected. |
| Audit logs contain cumulative snapshots | Addressed by reset at actual invocation start and explicit historical_access_scope describing within-invocation cumulative counters excluding separately recorded validation. Collector must not sum snapshots; source label inspected. |

Validation success now restores training counters. If validation raises, the training invocation fails and retains its failure evidence; it must not claim that invocation completed. No expensive validation retry or silent budget reset is introduced here.

## Final source binding

The writer may still edit these files while implementing review feedback. The actual SHA256 binding and final resolution below will be filled only from re-read concrete bytes, not an assumed commit. GitHub exact-commit publication/readback is the integration writer's responsibility. Source review applies only to bound bytes and described equivalent changes; later functional edits require follow-up.

Final source conclusion: **no unresolved Critical/Important finding in the reviewed scope after the source fixes above**. This conclusion is conditional on the exact bytes below and is not a software pass. Binding recorded from actual file bytes after rereading the changed context/counter/restore/no-grad paths:

| File | SHA256 |
|---|---|
| `src/lwm/model.py` | `73c7a6cbcdc8a2617089ece8cd51a3f89638dd7b6fd9331464b33d0bef2b59e8` |
| `src/lwm/realization.py` | `e3447da48a982c454893cf01506e343e3b028979e41a90c944520efab276269a` |
| `src/lwm/generation.py` | `98e2a57b3a4024332a45879cfd533532938f1fb57782f3bd96f8058868fa1798` |
| `src/lwm/train.py` | `8e41f8e523c604e1e12531ed8c37fcf1cc1af10cc87c63f94123405b8401a2d6` |
| `rounds/full-plan-2026-10-08/EXPANSION_SPEC.md` | `03131f0453601ede4505afc9f1d38b60e3ebd3e0287bfcf2cc4ffea0d8abc5e0` |
| `tests/test_resume_semantics.py` | `6bb5f9cea404ba7081f7e5fab0422f109ee2a5b8c7d8c1f17460d17f74723b72` |
| `tests/test_expansion_semantics.py` | `384590e2701aa312cd70f4394b019f7539e0f021b983f0a885e26e2bc5970430` |
| `tests/test_episodic_semantics.py` | `832fd1f6b1df5d67eb4b4119309cfe671519c76f45275ffc813074fba61a5cf1` |
| `tests/test_generation_semantics.py` | `4a66cde8b7472ed64b59f848f955d851d2ad40988368226c4204cd1919b59b82` |
| `src/lwm/episodic.py` (supporting source) | `ea14eb243777532ddd7f729dd46857e19a19df698a6d5580b58d15bfe4ebedc1` |
| `src/lwm/evaluate.py` (cost/reset excerpts) | `ca141f364599a6b205386639be78f56ed42cfd462388a918355d0e9e94b6d5ce` |

This local source packet was populated through the integration writer's remote reads and edits rather than a local git checkout. No local commit was manufactured. Exact remote integration commit and byte readback remain the root writer's delivery record.

## Local acceptance remaining

Contractive current-norm/gradient/zero-weight and complete-prefix parity; semantic-plan no-reader/no-writer expression with compatible snapshots and clock-only reuse; eligible auxiliary denominator/target-path/writer-gradient checks including TBPTT boundaries; legacy v0 disabled-extensions parity; state/plan corruption rejection and mid-segment resume; native full bAbI/LAMBADA comparison and actual cost/RSS/GPU qualification remain pending. Authored fixtures are software acceptance proposals, not native benchmark outcomes. No test pass or empirical novelty/scientific benefit is asserted.
