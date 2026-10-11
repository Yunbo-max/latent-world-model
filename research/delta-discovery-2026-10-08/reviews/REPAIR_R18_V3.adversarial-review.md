# R18 v3 independent adversarial review

- Reviewer: `/root/checksum_revision_math`
- Artifact SHA256: `947ef43e1b5f34adb4e5badf07c0ca8fb68c01a31128f77dc3a433ce1b256879`
- Screen SHA256: `13e479bb327362295d71e0d5f423d2d4ce65edcc943d11b28a6773c149882430`
- Source-audit SHA256: `f430a7306be6ce1cc876a90bc2cd30c3b51d9f43e71a3b705d6988bae9cc105c`
- Execution: exact-byte static review only; no edits, project/model code, tests or experiments.
- Verdict: **PASS only for the stated exact-real, one-event/fixed-affine-map conditional theorem/control.**

Adversarial checks confirmed the fiber characterization, Rayleigh equalities, Grassmann min--max, pathwise lower bound, common-envelope upper bound and complementary-path witness. A finite path family admits an envelope; eigenspace degeneracy does not invalidate the tail certificate. The common pairwise radius must be uniform across the `V` choices in the min--max; if it depends on `V`, the objective becomes `R(V)^2 Lambda(V)`.

The earlier attacks are now explicit boundaries rather than suppressed counterexamples:

1. a finite-bit quantizer can merge distinct preserved coefficients even at `r=m`, so an added cell/noise term is required;
2. one fixed-width code cannot in general preserve two independently oriented destructive events without a sufficient transition, while appending codes grows state;
3. state-dependent `v(x)` can re-encode a row erased by the memory-only factor, so the full joint map is required unless current features are shared;
4. discontinuous routing can defeat a local Jacobian despite small state distance;
5. an individual-state radius is not the declared pairwise radius.

Costs now visibly include `nm+mr` dense basis entries, naive encoding, `O(Bm^2)` explicit path Gramians, nonconvex/SDP solving, precision, traffic, calibration and alignment. Conditions left open must remain open: prefix/radius validity under shift, nonempty finite path family, joint/anytime reuse accounting, nonlinear finite-difference closure, finite-bit leakage, repeated-write recurrence, a consuming decoder, matched-cost advantage, native measurement, originality and empirical effect. Park/close attempt 3/3 with zero candidate/admission/selection increment.
