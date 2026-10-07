# Existing-model research base: implementation plan

Goal: deliver reproducible training and published-baseline qualification code for one RTX 2080 Ti, while repairing the unsupported candidate-selection claims.

Architecture: use the released Transformers Llama implementation, the pinned SmolLM2 tokenizer, deterministic FineWeb-Edu token preparation, a token-budgeted single-GPU trainer, and the pinned EleutherAI evaluation harness. Reuse the author Coconut repository for a continuous-reasoning comparison; do not relabel it as an original method.

Spec: the user requests code and main-branch delivery to Yunbo-max/latent-world-model, specifies RTX 2080 Ti and 0.1B or 1B training data. Interpret B as tokens, recorded as an assumption. No training is requested on Web.

## Constraints and decisions

- Default 100,000,000 prediction targets; 1,000,000,000 is an independent opt-in budget, not an automatic continuation of a completed cosine schedule.
- Default scratch Llama: 8 layers, width 384, 6 attention heads, 2 KV heads, FFN 1024, tied 49,152-token vocabulary, 512 context. A separate 135M scratch / pretrained reference uses the original SmolLM2 config.
- FP32 master parameters, FP16 autocast and GradScaler. No BF16, FlashAttention-2, distributed launch or containers for the main trainer.
- The published Coconut runner requires torchrun even for one GPU and uses FP32 with bf16=false. Keep that separate from the main trainer and record its limitations.
- Preserve all 20 proposed IDs and the historical ranking. C01/C02 overlap; C16/C08/C20 are not yet established as independent mechanisms. No new method modules before actual selection and contribution gates.
- Research Autopilot's Web role takes precedence over execution-oriented skill defaults: write meaningful acceptance tests, source-review them, leave all execution pending. This is not completed TDD.
- GitHub is the only authorized output destination. HF input downloads are separate from HF output publication, whose destination is still undecided. No HF writes.

## Review focus

1. Exact target-token accounting on partial batches, last context and FP16 overflow.
2. Resuming optimizer/RNG/data position without silently replaying or skipping training.
3. Train/dev document separation, immutable upstream inputs and local input hashes.
4. Original benchmark prompts, labels, metrics, full denominators and raw sample logs.
5. Source delivery must not be reported as passed tests, method novelty or an active background job.

## Tasks

- [x] Prepare source pins, configs, input download commands and meaningful acceptance tests.
- [x] Implement reusable data preparation and training for existing Llama models, checkpoint/export and resource telemetry.
- [x] Implement native four-benchmark evaluation and retained dataset/sample identity; generate complete Coconut author-runner configurations.
- [x] Produce candidate audit, baseline coverage, Local host/harness handoff and progress record.
- [ ] Conduct a fresh source review, repair substantive findings, deliver main with expected-parent update and readback.

The experimental methods and a complete 15-method scientific matrix remain gated work, not completed tasks hidden in this baseline plan. Baseline development answers whether the available model/data/evaluator can support a future discriminating comparison; it cannot establish Three-Clock benefit.
