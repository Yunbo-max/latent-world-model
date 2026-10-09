# Independent review — Counterfactual query-visible write utility

- reviewer: `/root/counterfactual_source_audit`
- reviewed artifact: `research/delta-discovery-2026-10-08/rejected/COUNTERFACTUAL_QUERY_WRITE_UTILITY.md`
- exact artifact SHA256: `a2a8cb972bf9915af5e4761132ff505191d28e09ef04867dc151b4a1d910dd9c`
- verdict: **VERIFIED_REJECTED_CONTROL_OR_LEAD**

The frozen-path removal identity, query-visible contribution and cross-entropy difference are correct under fixed later features.  The reviewed bytes correctly distinguish this from a full nonlinear intervention requiring replay.  For write-local parameters, the counterfactual branch is constant, so maximizing the exact utility has precisely the ordinary future-CE gradient.  The redundancy, synergy, horizon and moving-target failures are therefore substantive rather than implementation details.

The functional collision is major.  AttriMem already uses signed source-ablation attribution as process reward for retain/update/merge/compress/discard; HiMPO defines signed write-local counterfactual utility with hindsight relevance; ContextCite, influence functions, TracIn and Data Shapley cover the broader source-credit mathematics.  How Linear Attention Remembers supplies the Delta/linear-attention source-transport and query-access decomposition, while Delayed Supervision is a stronger direct semantic alternative.

No exact prior implementation was located that fully replays a Delta matrix-state deletion and trains a history-only predictor to modify the deployed recurrence.  That narrow residual remains only a lead: it must specify the intervention, full replay, causal inference-time information, actual state path and comparison against ordinary future CE/Delayed QA/HiMPO.  It is not currently scientifically admissible or countable.

No files were edited by the reviewer, and no project code, tests, models, benchmarks, training, inference, scorer, download or GPU work was executed.
