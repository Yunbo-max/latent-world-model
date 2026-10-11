# Independent native-measurement and cost review — R10 v3

Reviewer: `/root/r10_measurement`  
Math artifact SHA256: `45308be5fbe91a9faff92e08fe3acec7f976cca4c3959b59a92fdf4e674a5c47`  
Source audit SHA256: `056ce512aaf123fe66a3d95a71b869a8d7713bd0f5889a7538bf86ec881be04c`  
Decision: **PASS for an honest measurement-gap disposition; not empirical validation or candidate qualification.**

## Claim-to-measurement audit

- bAbI, LAMBADA, RULER, and a later small MQAR screen can measure downstream answer/token behavior. They do not natively label common-carrier membership, \(\|(I-UU^\top)A_tU\|\), invariant-hull width, injection tail, residual tail rank, saturation, basis traffic, matched finite-state capacity, or factual validity.
- Computing those quantities requires model-internal hooks or a custom profiler. Such diagnostics are useful but are not native benchmark scorers and cannot alone close mechanism attribution.
- No affordable existing native object separates operator closure/leakage from semantic gains. Endpoint improvement would remain confounded by extra state, metadata, and compute.

## Cost and controls

The generic costs in the artifact are correct: dense project/reconstruct is \(O(dr)\) per residual column; token-varying diagonal \(D_t\) gives \(O(dr^2)\) generic core formation and \(O(r^2m)\) application; moving basis adds \(dr\) state and roughly \(O(dr^2)\) thin QR; full residual Delta transport is \(O(d)\) per column. Measuring spectral leakage adds diagnostic cost.

Required controls are the same-\(U\) direct projection, direct low-rank augmented state, same-total-bit main/full residual including scales and saturation, classical dithered/error feedback, and same-rank/compute truncation. Equal-cardinality relabeling is a capacity control, not an efficient baseline.

Pinned FLA, GatedDeltaNet, and STEPQuant interfaces support the static interface audit. No affordability or infeasibility result was measured on the RTX 2080 Ti; the correct statement is only that an affordable native mechanism object is not qualified.

Measurement remains open, empirical effect remains unknown, and candidate delta remains 0.
