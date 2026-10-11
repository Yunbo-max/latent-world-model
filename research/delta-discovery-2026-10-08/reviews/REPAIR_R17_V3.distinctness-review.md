# R17 v3 final-byte distinctness and cost review

- Reviewer: `/root/commutator_candidate`
- Assignment: independently compare R17 v3 with prior internal lines and strongest same-information/capability controls, including hidden state and total-cost differences.
- Math artifact SHA256: `f7bf7ce4f7e94262ec337ebd299a7ffe7cd7ee6dd883b5b7c4e016fcf1e322d0`
- Repair screen SHA256: `87c517c94e2540eba7e64bf588d202672b581488969c8372fc6a34a3641f5bcc`
- Source audit SHA256: `ad288ebffcbf4bd90242265e2117e98370951de88fb806424c91d699bd932f97`
- Execution: static mathematics, source, cost and distinctness review only; no edits, code, tests, model or experiment.
- Verdict: **PASS_CONDITIONAL; PARK; CANDIDATE_DELTA_0**.

R17 v3 genuinely repairs an action-target mismatch: it restricts the erased-pair question to the actual no-write versus Delta-write action, restores `||e||^2`, and makes the one-sided spectral tail explicit. That is a substantive attempt, but the components remain ordinary scalar Delta gating, an externally supplied observability/future-query Gram, and classical/streaming low-rank approximation.

An `O(dr)` factor can help only if multiple directions reuse it and its construction, calibration, precision, metadata and refresh costs beat direct scalar or dense controls. Its smaller float count than a protected ledger reflects weaker capability: it throttles/abstains rather than preserving values through an unsafe write. No matched-total-cost advantage or native mechanism measurement is established. Reopening requires a deployed lawful prefix certificate, matched-cost advantage over scalar/dense/ledger controls, and a mechanism-identifying measurement; rank or threshold variants do not qualify.
