# Project working instructions

Before setup, execution or repair, read `LOCAL_AGENT_RUNBOOK.md` and
`rounds/2026-10-07/WEB_HANDOFF.md` at the exact delivered commit. The download
inventory is in `LOCAL_AGENT_RUNBOOK.md#download-datasets-and-models` and
`configs/sources.json`.

- This is a research codebase. Apply the installed canonical Research Autopilot.
- Web generates and source-reviews only. Do not run this project's tests,
  inference, training, evaluation or model/dataset downloads on Web.
- Local controls the user's actual GPU host and uses the existing Research
  Autopilot `run_harness.py` as the single execution owner. Do not launch a second
  ad hoc job scheduler or install an LLM agent on the GPU host.
- User-stated hardware: RTX 2080 Ti; plan one GPU and confirm actual VRAM/driver
  with read-only host inventory. Native Conda; no containers. Do not ask again
  for the already supplied hardware or GitHub destination.
- `configs/train_31m_100m.json` is the default source configuration. 1B tokens,
  135M scratch and pretrained continued-training configurations are separate
  optional comparisons, not an instruction to run every configuration now.
- No original C01–C20 mechanism is implemented or scientifically admitted.
  Preserve the historical ranking and the overlap/counterexample audit. Recheck
  the actual method evidence before implementing a candidate; never replace
  missing evidence with a `verified: true` field.
- Published baseline reuse and qualification may proceed within an explicitly
  restored finite Local authorization; do not relabel native benchmark runs as
  runtime maintenance or use engineering fixtures as scientific evaluation.
- Keep native benchmark samples, prompts, labels, metrics and denominators.
  Preserve failures, exact code/input identities and raw per-example outputs.
- Code/config delivery is authorized to `Yunbo-max/latent-world-model` literal
  `main`. One integration writer, expected-parent update, exact commit readback.
  Preserve any later user commits. No force push. No HF output destination is
  confirmed; keep weights local and do not upload them to an invented Hub repo.
- Every run records generated/tested/executed/verified as separate statuses.
  No assertion that a hosted background task exists without a real provider ID.
