# Web handoff: 2026-10-07

Delivery target: `Yunbo-max/latent-world-model`, literal `main`. The external
delivery receipt supplies the exact commit after publication; this file does
not fabricate its own future SHA.

## Scope and current state

The user requested implementation based on existing code/models and GitHub delivery,
then specified RTX 2080 Ti and 0.1B / 1B data. Interpret the latter as tokens.
The repository was empty. This work delivers an existing-model training,
native-evaluation and latent-baseline preparation codebase with explicit inputs
and Local entry points. It does **not** complete the novel 15-method implementation
or its G01 scientific matrix. The skill requires prerequisites that the inherited
conversation's table does not provide.

No scientific project code/tests, model/data downloads, training, inference or
evaluation have run on Web. Status is `generated_unexecuted`; source inspection,
source metadata retrieval and read-only evidence validation are distinct.
No scientific results, code_verified/design_verified flags or method success
counts are supplied. The real `verify_methods.py --before code --candidate C16`
report fails on missing retained mathematical pool/selection evidence.

## Reading map

- [Local runbook](../../LOCAL_AGENT_RUNBOOK.md): host restoration, acquisition,
  acceptance, inner commands, debug and return steps.
- [Input inventory](../../LOCAL_AGENT_RUNBOOK.md#download-datasets-and-models) and
  [full source pins](../../configs/sources.json).
- [Implementation plan](../../docs/IMPLEMENTATION_PLAN.md).
- [Candidate audit](../../docs/CANDIDATE_AUDIT.md) and
  [per-candidate coverage](../../docs/CANDIDATE_COVERAGE.csv).
- [Baseline design](../../docs/EXPERIMENT_DESIGN.md).
- [Literature / code review record](../../docs/SOURCE_REVIEW.md).
- [Independent delivery source review and repairs](../../docs/DELIVERY_REVIEW.md).
- [Progress checkpoint](workflow-checkpoint.json).
- [Evidence batch](../../evidence/method-batch.json); retained boundary report
  [selection check](../../evidence/method-boundary-report.json).

## Concrete implementation

`src/latent_world_model/` contains input acquisition, deterministic tokenization,
the existing-model trainer, native evaluator wrapper, Coconut author-config
generator, exact-resume acceptance and result collector. All main model forwards
are the released Transformers implementation. There is no nominal C16/C20 file
with a renamed baseline inside it.

Tests under `tests/` target data shift/count integrity, incomplete batches,
schedule/config checks, acquisition and evaluation identity, interrupted checkpoint
publication, and native checkpoint continuation. They are authored,
not executed. Source-level review cannot establish CUDA fit, convergence,
benchmark scorer parity or exact runtime determinism.
The existing host harness must stage the captured source bundle and receipt,
then run through `scripts/run.py`; the runbook gives the exact source-identity
step and required `LWM_SOURCE_IDENTITY` environment binding.

## Local obligations

Restore the actual host and current finite execution authority; do not infer a
GPU launch grant from this Web code-delivery request. Follow AGENTS and the runbook,
using one host harness. Acquire and verify complete inputs; run meaningful
software acceptance and inspect FP16 memory/throughput on actual training data.
Preserve the true environment, source/config/dataset identities and every failed
attempt. Bind actual outputs in the existing runtime's admitted native plans.

The four language tasks have source-complete adapters but await native loader/
scorer qualification. Coconut has source-pinned author training/evaluation paths;
its resource-adapted loss weighting, final-stage checkpoint selection, incomplete
optimizer resume and per-example logging limitations must remain explicit.

Do not implement C01–C20 until mathematical cards, semantic reviews, structural
distinctness/ranking, applicable Parent/Gate 0 and collision/IPCG obligations
close. World/action and multimodal evaluation have not been supplied by a text
benchmark. Preserve those gaps and continue the same research lineage, without
padding a fresh candidate list or passing a gate from this handoff.

HF is currently an **input** source only. The user has not chosen an output Hub
repository or explicitly declined one; that choice is pending when weights/results
need publication. No HF upload is authorized or attempted. Do not block baseline
source reading or ordinary GitHub code delivery on an invented HF destination.

Return the actual tested/executed commit, logs, native manifests/predictions and
scorer/E04 coverage, hardware measurements, incomplete comparisons and a read-back
GitHub result locator. Code delivery, runtime activity and scientific evidence
must be reported separately.
