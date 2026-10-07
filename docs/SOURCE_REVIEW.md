# Source review and scientific scope

Read on 2026-10-07. Source interfaces were inspected; execution is pending on Local.

| Primary source | Retained identity / inspected part | Consequence |
|---|---|---|
| SmolLM2 paper | https://arxiv.org/html/2502.02737v1 ; pretraining setup, dataset ablations and small-model section | Use a released Llama implementation and report data/compute identity. A 100M scratch run is not comparable to a released model's total training. |
| SmolLM2-135M | https://huggingface.co/HuggingFaceTB/SmolLM2-135M/commit/93efa2f097d58c2a74874c7e644dbc9b0cee75a2 ; config and file inventory | Pin width-576, 30-layer reference, 49,152-token vocabulary and complete weights. The reduced config is a baseline scale choice. |
| Transformers Llama | https://huggingface.co/docs/transformers/v4.46.2/model_doc/llama | Use released AutoModel/LlamaForCausalLM, local model paths, checkpointing and HF export. Native qualification pending. |
| FineWeb-Edu | https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu/commit/87f09149ef4734204d70ed1d046ddc9ca3f2b8f9 ; README/config metadata | `sample-10BT`, `train`, `text` are actual source fields. User budget controls retained size. |
| Coconut paper | https://arxiv.org/html/2412.06769v2 ; continuous-thought method and experiments | Reuse as a published latent baseline. Continuous hidden-state feedback is not new here. |
| Coconut code | https://github.com/facebookresearch/coconut/tree/27273cb8cca4bb763c041a63b036d0c3b7cbbb48 ; README, coconut.py, run.py, dataset.py, requirements, task configs, GSM acquisition and MIT license | Preserve curriculum/extraction. Notice one-item generation, FP32/BF16 switch, optimizer-resume limit, 32-process preprocessing and final-stage selection. |
| BDH-CQ | https://arxiv.org/html/2608.09888v1 ; memory/reasoning formulation and ARC evaluation | Functional overlap with the high-level belief/workspace proposal. Its results do not validate this project or a text-only causal world model. |
| lm-evaluation-harness | https://github.com/EleutherAI/lm-evaluation-harness/tree/6d2abda4fd171e68a8789330c4149e37c1ca0bda ; evaluator.py, api/task.py, tasks/__init__.py, models/huggingface.py, task YAMLs, utils conversion | Use ConfigurableTask revision kwargs, HFLM existing-model API and simple_evaluate native sample logging. |
| Native tasks | Full HF revisions in configs/sources.json; repository metadata and evaluator YAMLs | WikiText document-level scorer; full HellaSwag/PIQA validation and ARC-Easy test. Data/scorer qualification pending. |
| PyTorch prior versions | https://pytorch.org/get-started/previous-versions/ ; 2.5.1 wheel family | Specify native cu121; inspect actual driver compatibility. |
| nanoGPT | https://github.com/karpathy/nanoGPT/commit/3adf61e154c3fe3fca428ad6bc3818b27a3b8291 ; repository notice | Considered, not selected: current README calls it deprecated. |

No strongest-baseline qualification, Natural Gate 0, completed originality/IPCG,
verified 20→15 selection, CUDA/test pass, scorer-parity receipt, outcome or causal
world-model effect exists for this project. The prior conversation's ELF/Cola/
Kimi/STARS claims are not used to authorize code or asserted as exhaustively
audited here. Their claim-level collision work remains scientific continuation.

The mathematical audit corrects the inference from noncommutativity to mandatory
operator separation and identifies structural overlaps. This source record
supports baseline implementation decisions, not a declaration of novelty.

The independent software review and resolved findings are in
`DELIVERY_REVIEW.md`. ARC-Easy released split sizes (test 2,376; validation 570)
were checked against the pinned dataset README at
https://huggingface.co/datasets/allenai/ai2_arc/raw/210d026faf9955653af8916fad021475a3f00453/README.md.
