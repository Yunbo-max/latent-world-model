# Follow-up source review and repairs

Historical delivery: fa75982cb9258047189651547381b4582b7eaec9. The source hashes below bind that first repair packet; later changes are recorded in [RECHECK_REVIEW](RECHECK_REVIEW.md), which is the current follow-up entry.

User request: "你检查下", 2026-10-08. Audit baseline: main `48f249bc4b9baee81b208dbcb9fb299f56e8e91a`; all 113 remote file blobs matched the review snapshot before edits. This report is at the commit containing it. Status: **generated_unexecuted**. No project imports, software tests, training, inference, native scoring, downloads or GPU jobs were executed by Web.

## Findings and source repairs

| Finding | Concrete trigger / consequence | Repair |
|---|---|---|
| Important: checkpoint load/hash race | Generation and standalone realization loaded A, then hashed the `last.pt` path after a trainer could atomically publish B. A-derived memory or Z could then be labeled SHA(B), defeating later identity checks. Weights-only initialization had the same provenance gap. | `checkpoint.load_checkpoint_with_sha256` holds one unbuffered file descriptor, streams hashes before and after deserialization, and returns the loaded payload plus its actual SHA. Atomic replacement retains A and SHA(A); persistent in-place changes reject. Generation, realization, initialization, resume and evaluation use that identity. Existing latest-path resume/evaluation checks remain. No whole-checkpoint byte buffer is added. |
| Medium: incompatible tokenizer initialization | Equal architecture/vocabulary size does not imply equal token-ID meanings. Initializing embedding/readout rows from tokenizer A and later labeling the checkpoint as corpus tokenizer B could silently corrupt identity. | `train.main` compares initial and target tokenizer identities before weight loading. Different identities or missing asymmetry reject; equal identities and both-absent software fixtures remain allowed. FineWeb-to-bAbI transfer under the shared pinned tokenizer is retained. |
| P2 bounded scoring edge case | With empty context and a continuation already starting with EOS, the helper added a second EOS and counted the first as a target. The pinned harness moves the existing prefix into context. No current full LAMBADA matrix impact was established. | `scoring.encode_hf_pair` adopts the existing-prefix branch from pinned TemplateLM and keeps empty-target rejection. Primary source independently reread: lm-evaluation-harness `d6de81643928d653435c431bae19945d41d32520`, `lm_eval/api/model.py`, lines 455–464. |
| Documentation precision | "Labels never enter history" can be read as forbidding previous supervised answer tokens. | Design now distinguishes excluded evaluator/support metadata from ordinary causal teacher-forced training history. The algorithm/provenance policy is unchanged. |

Fresh independent read-only reviewers were `/root/check_state`, `/root/check_training` and `/root/check_evaluation`. They inspected the initial findings and relevant repair deltas. The checkpoint helper additionally uses unbuffered FileIO to prevent a stale BufferedReader cache hiding an in-place change. No remaining Critical/Important source finding was identified within these bounded reviews. This is not a runtime pass or a general proof of bug freedom.

## What the source audit supports

Actual call chains connect event retrieval to neural consumption, causal prefixes to workspace/plan/readout, completed-segment writer commits to persistence, and main/auxiliary objectives to training and validation. Writer graphs remain connected within TBPTT windows. Fixed-forcing contraction matches its conditional real-arithmetic bound. The 13-arm/two-seed native matrix retains 204 dependency cards and full bAbI/LAMBADA denominators. No core algorithm was left as a placeholder in the selected text construction.

The narrower executable text construction and original theoretical goals remain distinct. Fixed K remains; adaptive stopping/output-error certificates, predictive sufficiency, identified sentence semantics/invertible codec, calibrated belief and action/physical-world dynamics are not implemented or established. The original discovery/novelty batch remains unqualified. Closing this source task does not close those scientific goals.

## Local acceptance

Core regression cases were authored before the repair source, but **not executed**, so no red/green or TDD-pass claim is made. New cases exercise real atomic checkpoint replacement, persistent in-place changes, both CPU generation/realization entry points, incompatible and matching tokenizer initialization, and the existing-prefix token boundary. Zero-weight/current-norm gradients and CUDA FP16 main/readout forward/backward cases were added to expansion acceptance. The latter single-segment fixture has an empty retrieval store and does not qualify writer/auxiliary or nonempty-retrieval gradients. Tokenizer doubles avoid external assets only; checkpoint deserialization/file replacement and model/trainer/CLI behavior remain real software fixtures, not scientific evaluation.

Read the same-revision AGENTS, runbook and handoff, then run the complete suite through the existing Local execution owner:

```bash
conda run -n lwm python -m pytest -q
```

Only after a failure, the focused diagnosis is:

```bash
conda run -n lwm python -m pytest tests/test_checkpoint_identity_semantics.py tests/test_resume_semantics.py tests/test_scoring_semantics.py tests/test_expansion_semantics.py -q
```

Retain stdout/stderr/exit status, actual skips and source/environment identities. Native Teacher/tokenizer/model/scorer qualification, actual GradScaler overflow/skip/resume behavior, CUDA device acceptance, profile/cumulative cost and the complete experimental matrix still need real Local evidence. An authored CUDA test skipped on CPU does not qualify CUDA. The two streaming hashes add actual I/O time; measure it within setup/checkpoint costs. Preserve old live runs/snapshots on their original source; do not silently resume them on changed source hashes.

Fresh standard-library AST/JSON/TOML parsing of the repaired source found no syntax errors. Those checks never import the project. Main publication requires expected-parent reconciliation and exact-file readback; its concrete SHA is reported by the publishing session after verification.

## Repaired source identities (SHA-256)

| Path | SHA-256 |
|---|---|
| src/lwm/checkpoint.py | ec4d435acd1efae555d2bc131704aea33e0f5d73cc6a7707a5c8838defabd585 |
| src/lwm/generation.py | 06d145dd6e836ca0c8c5599bbf0f017155b0dfeaa96674426c4a65c36af5b496 |
| src/lwm/realization.py | 2bb65947e5c8d61176205eeca0b6cf5fbfc192916c6ef661e13d87d4da582534 |
| src/lwm/train.py | 40305fd712b42b7db7a9de14e595dceeaf3869f2fdaf28c43ea55f169a21b2d1 |
| src/lwm/evaluate.py | 347dcdc180f058ca6bb328205f7cba90df649ed6b499248e5e88b543cf414ba9 |
| src/lwm/scoring.py | 57d0f279091646c88a3f9344b37262d678ed0ee15838f996651a90c0d7ed1188 |
| tests/test_checkpoint_identity_semantics.py | a4598113d0267c4f2f56b447388e52274a8066473d6644211c9bae094525e978 |
| tests/test_resume_semantics.py | c306940ed24e7ebff65309fdd97fd29b57bb978ff466afcf0cc3f57bd2448b8d |
| tests/test_scoring_semantics.py | 5001bdcb66de5a1034ac5426740a5e78d25533c3e681d75ccb5f38b5777835be |
| tests/test_expansion_semantics.py | 2f6db4c8bfc4fc9e474835170e6caa361db7dadce94a98c6389c61ef76cee1ef |
