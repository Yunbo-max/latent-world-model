# Source-only delivery review

Scope: the existing-model base at local revision `dd092ce`, followed by the
repair diff in this delivery. A fresh read-only reviewer inspected the source
and pinned upstream APIs. No project imports, tests, dataset/model acquisition,
inference or GPU workload ran during review.

| Finding | Severity | Source repair |
|---|---|---|
| Replacing checkpoint bytes before metadata could invalidate the sole restart point | Important | Immutable generations; fsynced atomic publication pointer; retain current and previous committed generations |
| Reacquisition could bless changed files by replacing their receipt | Important | Verify every old receipted file before any download; verify preserved bytes afterward; reject corruption with the old receipt retained |
| Evaluation ignored its prepared sample manifest and compared counts only to a fresh load | Important | Require frozen inventory; compare task/split/source/software/sample/checksum identities before inference; check all native row IDs and hashes in predictions |
| Requested versions were recorded without binding actual executed software | Important | Hash installed critical package files and verify imported package locations; enforce installed evaluator VCS revision; bind environment to resume and scoring |
| Harness staging may omit Git metadata and editable installs may import another checkout | Integration | Capture actual clean Git source; stage all captured files; verify them; launch through staged `scripts/run.py` |
| Missing document-index hash check and ambiguous replay logs | Minor | Verify document evidence hash; tag logs with invocation and committed generation |
| Resume acceptance omitted token/optimizer/scaler/RNG assertions | Minor | Add those assertions; explicitly keep FP16 overflow acceptance pending |
| Source capture could inherit a stale source-manifest environment variable | Minor | Capture explicitly forces live Git inspection |

The repair re-review found the four Important findings addressed in source and
no new Important/Critical source regression. The final minor source-capture
change explicitly disables staged-manifest reuse; docs now describe the pointer,
frozen native inventory and staged launcher.

Pinned lm-eval source confirms that prediction `doc_id` enumerates processed
`task.eval_docs` and logged `doc` is that processed document. Pinned Coconut
source confirms torchrun, FP32 with bf16=false, and final fully latent selection
eligibility (ProsQA checkpoint 36+, GSM checkpoint 13+).

Authored engineering contracts cover asset corruption, interrupted unpublished
checkpoint state, frozen inventory mismatch and native row identity, as well as
the earlier data/schedule/native-restart contracts. They have **not run**. Readiness
is `generated_unexecuted`, source reviewed. This is neither passing TDD nor runtime
acceptance. CUDA fit, wall time, exact restart, FP16 retry, installation, source
staging, native scorer parity and scientific comparison remain Local obligations.

The mathematical selection validator's retained failure is unrelated to these
software repairs. Candidate count implemented/verified remains zero; no baseline
delivery or source review clears the original architecture's research gates.
