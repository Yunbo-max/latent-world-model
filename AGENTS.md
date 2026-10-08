# Project instructions

Before setup, acceptance, execution or repair, read these files at the **same delivered Git commit**:

1. [LOCAL_AGENT_RUNBOOK.md](LOCAL_AGENT_RUNBOOK.md), especially [input acquisition](LOCAL_AGENT_RUNBOOK.md#download-datasets-and-models).
2. [Current Web handoff](rounds/delivery-review-2026-10-08/WEB_HANDOFF.md), including its link to the prior full delivery.
3. [Adopted mathematical specification](research/FULL_MODEL_PROPOSAL.md), [math-to-code map](research/MATH_TO_CODE.md), and [complete experiment design](research/EXPERIMENT_DESIGN.md).

User scope: implement a text predictive latent-state model with persistent memory, independently controlled internal recurrent computation and a separate language readout, based on existing models. RTX 2080 Ti is user-stated. Data profiles are 100M/1B **pretraining target tokens per model run**, not parameter counts. The current construction is an explicitly disclosed engineering adaptation; do not claim a faithful Huginn/RMT reproduction, novelty or validated world dynamics.

Research Autopilot role split applies. Web authors and reviews source as `generated_unexecuted`; Local executes actual environment/software/native acceptance and experiments through the existing admitted SSH/native harness. Do not run a second competing background controller or use a written task file as a launch receipt. No Docker requirement.

Preserve history: the old discovery batch in `research/method-batch.json` and Q01 readiness report remain unfinished. They are not fabricated qualifications for this engineering source. If pursuing a new scientific contribution, resume their real mathematical, selection, originality and experimental obligations. Do not edit a verifier or manufacture receipts to make it pass.

Critical implementation contracts:

- `forward_segment(tokens,memory)` predicts the **same** token positions; do not shift targets again. Internal SEG carries the segment-first prediction.
- Reader loops do not write memory. Only a completed non-EOS segment is publicly committed; partial prefixes stay in the serialized state.
- Prefix inference computes the complete causal hidden sequence, then projects only the last position to the vocabulary. Do not slice before coda or truncate teacher-forcing targets. Read the equivalence proof in research/SIGMA_REVIEW.md before changing this path.
- Writer needs subsequent-segment loss through an untruncated within-window graph. Do not detach each segment. Keep document resets and TBPTT detaches distinct.
- Preserve pinned asset bytes, native bAbI/LAMBADA IDs/scorers and full denominators. Software fixtures are not scientific evaluation.
- Keep pretraining and bAbI adaptation target/context budgets distinct. Report all arms/seeds, actual elapsed cost, skipped optimization and failed attempts.
- Resume only compatible checkpoint/data/config/source; reconcile real host/PID and lock before retrying a lost launch. Never silently overwrite a live run or reset accumulated budgets.

GitHub destination is `Yunbo-max/latent-world-model`, branch `main`, already authorized by the owner. Use one integration writer and expected-parent updates, preserve concurrent work, and read back actual files at the exact remote commit. No HF output destination or training-host connection was supplied to Web; do not invent either or upload weights/data elsewhere.
