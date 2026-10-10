# Independent source and collision review — R12 v1

Reviewer: `/root/r12_source_review`

Reviewed exact artifacts:

- `sources/R12_SUBSPACE_SYNDROME_SOURCE_AUDIT.md`, SHA256 `66228ab044f660263684559e85803e373cb1bddb87a541efa5598a14f5b3e1ed`
- paired math artifact, SHA256 `da1a0df6bb3f9ba95605c8ee7200622dec61ca595031dc6c02a23852d01aefce`

Mode: independent primary-source/interface/scope review; no artifact editing, experiment, training, inference or scorer execution.

## Checks and corrections

- Corrected Nelson–Nguyen to the ambient-capped OSE lower bound and its parameter scope/locators.
- Scoped Li–Wang–Woodruff to its finite-bit, per-query randomized norm-sketch contract; it is an adjacent guard, not a direct theorem collision.
- Pinned Candès–Romberg–Tao to `math/0503066v2`, Theorems 1–2 and their structural assumptions.
- Separated the 2025 Parrini et al. journal article from the differently titled/authored ETS/arXiv precursor; only D1 terminology/fault-model evidence is claimed.
- Verified Flash Linear Attention commit `a7880060012c862d58575ee23f613cafcd728d03` interfaces in `fla/layers/delta_net.py` and `fla/ops/delta_rule/__init__.py`; the inspected pin exposes ordinary Delta kernels, not R12's syndrome decoder.
- Verified LongMemEval commit `9e0b455f4ef0e2ab8f2e582289761153549043fc` answer-level `knowledge-update` judge/aggregator paths; they do not expose the internal R12 mechanism variables.
- Required `INCONCLUSIVE_EXPAND_SEARCH` for exact theorem priority. Parking follows elementary factorization and same-width controls, not a coverage-complete novelty kill.

## Verdict

**PASS for source correctness/alignment and the conditional PARK decision.** This is not a novelty pass, candidate admission, empirical-effectiveness result or native-benchmark-readiness pass.
