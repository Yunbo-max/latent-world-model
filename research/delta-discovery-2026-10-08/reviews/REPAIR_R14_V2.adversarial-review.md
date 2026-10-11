# Independent adversarial and fair-budget review — R14 v2

Reviewer: `/root/r14_v2_adversarial`  
Reviewed at: 2026-10-11T07:47:35+01:00  
Mode: independent read-only counterexample, hidden-cost and attribution review;
no editing or project/model execution.

Reviewed exact final bytes:

- math SHA256
  `073146ac7af184d9d39146911686af9b1de911688ed5a945d7f628ac5d5a6bbb`

## Attacks and repairs checked

- The certified interval is external and prefix-measurable; marginal calibration
  is not silently upgraded to tokenwise coverage.
- The explicit invalid interval example (`lambda=1`, true `p=0.1`, asserted
  interval `[0.9,1]`) makes the robust write worse than no-write, so robustness
  is not claimed without certificate validity.
- Continuous shrinkage and hard abstention use different action sets. The
  one-touch thresholds and the extra `(1,1)` budget case are therefore kept
  separate.
- The operational identity is unique and closed-world; the theorem does not
  solve new-slot discovery, distributed facts or provenance identification.
- Only posterior ambiguity is robustified. Wrong interference cost, residual,
  local Hessian or future Jacobian may invalidate the local prescription.
- The strongest same-information control is a direct minimax per-slot router,
  which is algebraically the same rule. State and information costs are charged;
  no architecture-level novelty or unfair extra evidence is claimed.
- The `lambda -> 0` endpoint and multi-slot coercivity gaps found in preliminary
  review are repaired in the exact final bytes.

## Verdict

**CONDITIONAL PASS as a scoped theorem/debug control; candidate admission NO.**
No remaining byte-level mathematical blocker was found. External coverage,
local-model fidelity, native measurement and empirical effect remain open. Park
after repair attempt 2 with `candidate_delta=0` and `experiment_status=unknown`.
