# Latent World Model

Research preparation for **one RTX 2080 Ti**, using existing model code and
**100M / 1B training-token configurations**.

**Current delivery: generated, unexecuted baseline source.** Training, evaluation
and project tests have not run on Web. The original 20-candidate / top-15 table
does not yet pass Research Autopilot's mathematical distinctness, selection and
contribution requirements. **No original architecture candidate is implemented
or qualified in this revision.** See [the audit](docs/CANDIDATE_AUDIT.md).

## Local Codex: start here

Read the [Local runbook](LOCAL_AGENT_RUNBOOK.md) and
[current round handoff](rounds/2026-10-07/WEB_HANDOFF.md) at the delivered commit.
The [download inventory](LOCAL_AGENT_RUNBOOK.md#download-datasets-and-models)
contains pinned model/data/scorer acquisition commands. Local execution uses the
user's existing Research Autopilot host harness and native Conda environment.

## Included source

| Component | Implementation |
|---|---|
| Existing model | Transformers Llama; SmolLM2 tokenizer/config and pretrained reference |
| Main configuration | Approx. 31.5M parameters, 512 context, 100M targets, FP16 autocast |
| Optional comparisons | Independent 1B-token run, 135M scratch model, pretrained continued training |
| Data | Version-pinned FineWeb-Edu stream; document-disjoint development split and exact token accounting |
| Training | Gradient accumulation/checkpointing, optimizer/RNG/cursor resume, overflow accounting, HF export |
| Native language evaluation | Full WikiText-2, HellaSwag, PIQA and ARC-Easy via pinned lm-evaluation-harness |
| Existing latent-reasoning baseline | Pinned Coconut author code; ProsQA/GSM8K CoT, no-CoT and Coconut config generation |
| Handoff | Source pins, hardware assumptions, meaningful Local acceptance tests, collection and debug commands |

The pretrained reference has vastly more prior training than a 100M-token scratch
run; it is a practical reference, not an equal-compute architecture control.
Coconut's supervised native protocol is also a separate comparison. Neither
language loss nor those baselines prove counterfactual world modelling.

The delivered baseline specification is in
[EXPERIMENT_DESIGN.md](docs/EXPERIMENT_DESIGN.md). The unfinished scientific
candidate obligations are listed individually in
[CANDIDATE_COVERAGE.csv](docs/CANDIDATE_COVERAGE.csv).

The project has no Docker requirement, invented benchmark or automatic paid
compute launch. No durable ChatGPT background-worker ID was exposed in the
authoring session; repository checkpoints support resumption but do not certify
an active background task.
