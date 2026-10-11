# R19 v2 repair-line screen — prefix-causal branch uncertainty

Scope: mathematical repair, primary-source/interface audit, and native-measurement feasibility only. No project or upstream code, tests, model execution, training, inference, scoring, dataset/model download, GPU work, paid service, or Docker was used.

## Bounded repair choice

R19 v1 is mathematically correct only on a declared common branch: it assumes the realized protection mode/reset is available and explicitly stops at selector guards. Its exact PSD-kernel obstruction and realized-branch ledger rank remain valid. The earliest open premise is therefore not another dwell-time constant; it is whether a release certificate can be causal when several state-dependent branches remain compatible with the same prefix.

Three patches were screened:

| Patch | Why it matters | Decision |
|---|---|---|
| Stack all possible linear exposures `B_m=P_m^(1/2)R_mK` and store their joint row space | Removes the realized-mode oracle and gives width `rank(stack_m B_m)` | Correct but already the one-step linear specialization of R18 v2's prefix-robust quotient/direct-ledger theorem; retained as a corollary, not the main v2 result |
| Use `max_m h^T P_m h` or `sum_m P_m` as a common envelope | Makes the common kernel explicit | Rejected as a repair by itself: modewise contraction does not imply contraction of the envelope; all cross-mode/path inequalities are still required |
| Treat finite-precision reachable states and visible branch labels as a zero-error function-computation problem | Handles discrete guards and nonlinear branch divergence without differentiating the selector; gives an exact minimum one-shot side-code alphabet | **Selected for R19 v2**. It changes the mathematical object and information timing, but zero-error characteristic-graph coding, set-valued observers and R18's global fiber/right-congruence analysis are decisive controls/collisions |

## Patch and expected boundary

At the write time, the encoder sees only the lawful prefix and current finite state. The future release branch is not known. After the switch, the decoder may observe a declared branch label together with the destructive post-write state. There is a feasibility check before graph coloring: if two lawful branches of the same state have the same visible label but require different released targets, then no code of any size can work because the encoder cannot send two messages for the same state. Once that intra-state target consistency holds, two distinct pre-write states are confusable exactly when those same visible quantities can coincide while the required released value differs, and the minimum exact finite side code is the chromatic number of this confusability graph.

This repair is useful because it makes four hidden costs explicit: branch labels must actually be observed; state quantization/range must be declared; the code is written before the release; and computing an optimal coloring can itself be intractable. It does not infer whether a fact is obsolete, prove contraction after the released value is reconstructed, or establish an advantage over a direct ledger.

Disposition anticipated before final-byte review: conditional theorem/debug control, attempt 2 of 3, likely park with zero candidate increment because the exact mechanism is a Delta specialization of known zero-error function computation and set-valued/predictive-equivalence machinery. Attempt 3 should reopen only for a structured Delta family with a provable matched-total-cost advantage and a native mechanism-identifying object.
