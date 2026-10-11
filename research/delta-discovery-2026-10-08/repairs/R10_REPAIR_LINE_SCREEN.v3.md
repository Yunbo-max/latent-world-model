# R10 v3 repair-line screen: invariant residual carrier

Recorded: 2026-10-11. Role: Web mathematics/source review only. This is attempt 3 of at most 3 substantive repairs in the R10 lineage.

## Earliest live gap

R10 v1 proved that a split code whose decoder only sees the same total bit budget has no cardinality advantage over a direct code, and that coarse-visible error feedback changes the operator rather than exactly recovering the full-precision trajectory. R10 v2 repaired the residual-law comparison and derived transition-matched finite-horizon and spectral controls, but it had to carry a full residual through

\[
A_t=(I-\beta_t k_tk_t^\top)D_t.
\]

Its earliest unclosed mathematical question is therefore narrow and testable: can the transported residual be kept in a rank-\(r\) carrier, \(r<d\), without using future information and while preserving the exact Delta order?

## Chosen patch

Write the residual as \(R=UC\), with fixed orthonormal \(U\in\mathbb R^{d\times r}\). Derive:

1. the exact common-invariance criterion for legal Delta transitions;
2. the Delta-specific projected core and leakage;
3. the exact accumulated error when the carrier is only approximate;
4. a legal noncommuting mode family that forces any robust exact carrier containing a declared residual direction to have width \(d\);
5. the costs and escape clauses for a moving basis.

This changes state/structure relative to v2 and is therefore a substantive repair, not a renamed scalar feedback coefficient.

## Pre-registered decision

- A natural prefix-lawful restricted mode family with a small common carrier plus a matched-total-cost advantage could remain a lead.
- If exactness reduces to standard common invariant/reachable closure, approximate transport pays explicit leakage, and a legal family forces full width, then the result is a useful Delta boundary theorem only. R10 is parked after attempt 3/3, with candidate delta zero.

No model code, benchmark execution, training, inference, or scoring is authorized in this screen.
