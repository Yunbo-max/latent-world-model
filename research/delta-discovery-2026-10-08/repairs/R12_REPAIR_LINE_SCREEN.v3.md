# R12 repair-line screen v3 — finite-family autonomous closure

## Lineage and fixed boundary

- Parent v1: `R12_SUBSPACE_SYNDROME_READOUT.v1.md`. It proved when a static syndrome `H^T\Delta` determines a protected effect `Q^T\Delta`, but it did not close the syndrome under later Delta updates and did not beat direct reduced coordinates.
- Parent v2: `R12_AUTONOMOUS_SYNDROME_CLOSURE.v2.md`. It proved the exact closure condition `F_i^T V\subseteq V`; for a pure Delta factor `F_i=I-\beta_i k_i k_i^T` with `\beta_i\ne0`, this is equivalent to `k_i\in V` or `k_i\perp V`. It also gave the least fixed-point construction. What remained was an explicit finite-family evaluation, dimension certificate and prospective-information boundary for that fixed point.
- Attempt budget: this is R12 attempt 3/3. Old bytes, counterexamples and reviews remain unchanged.
- Stage boundary: mathematical/source/measurement review only. No model execution, training, inference, scoring or generated benchmark evidence.

## Three evidence-bearing repair options

| line | concrete delta from v2 | decision |
|---|---|---|
| A. Declared finite key-family closure | Replace an unspecified future key process by a fixed, externally declared finite family. Evaluate v2's least fixed point by connected components of the non-orthogonality graph. | **Derive fully in v3.** This yields an explicit finite certificate, dimension/cost statement and bridge-key boundary; it does not invent the fixed point itself. |
| B. Thresholded/approximate graph | Drop sufficiently small Gram edges to obtain a smaller carrier. | **Park.** Thresholding is not exact; error depends on ordered leakage and conditioning. Without a new spectral margin, it is only an approximation heuristic already covered by projection/truncation controls. |
| C. Implicit checksum/hardware advantage | Keep the same closed coordinates but claim they are cheaper because they are called a syndrome. | **Reject as a candidate delta.** `U^T S` is exactly the direct reduced state in a basis `U`; naming or implementation placement does not create a mathematical or matched-cost advantage.

## Why line A is the bounded repair

The bounded residual after v2 is not another learned gate: it is to evaluate v2's least jointly invariant fixed point for a declared finite key family. Pairwise non-orthogonality gives an explicit component certificate for that already-defined object. Coefficients and operator selection must also be externally visible or factor through the retained state; a hidden-state selector can otherwise reintroduce discarded information. This changes the assumptions and target honestly: it certifies when exact autonomous protection can be lower-dimensional; it does not infer semantic validity, predict unseen future keys, or claim a new updater.

## Stop rule

After v3, R12 is parked regardless of whether the theorem passes: the third substantive attempt is exhausted. It may reopen only if new evidence supplies at least one of:

1. a lawful prefix-causal mechanism that handles an undeclared future bridge key without retaining the discarded state or an equivalent ledger;
2. a matched-total-cost advantage over direct reduced coordinates/full Delta under the same declared key information; or
3. a native record that identifies the closure mechanism rather than endpoint answer quality alone.

