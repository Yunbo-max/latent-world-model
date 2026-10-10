# R17 v1 independent final-byte adversarial review

Reviewer: `/root/r17_adversarial`. Assignment: attack target definition, state timing, hidden future/oracle access, recursive closure, bit/side-information accounting, same-information controls, originality language, native measurement, and empirical claims. The reviewer did not author or modify repository files and did not execute project/model code, tests, training, inference, scoring, or experiments.

- Artifact SHA256: `8e765da62723fe76480397284c716259ac8dad6ddacc9c8da18842c5d56df78a`
- Source-audit SHA256: `2b94f1e9c3ec3d8753e045462fbb81cdc57db3f41a38ea249182c5ff73279ba2`
- Verdict: **PASS / conditional theorem-control only / no candidate admission**.

## Attack results

The final artifact no longer promotes `ker(A·) subseteq ker O` into semantic safety. It consistently states old-quotient decodability/no-extra-aliasing, explicitly weaker than identity on the quotient, and records the missing deployed decoder/subtraction/direct equality obligations. Prediction (11) is limited to the positive-weight family; zero-weight reads are not certified.

Pre-decay `D^-1k` and post-decay `k` are not mixed. The frozen suffix/query family is declared and is not presented as prefix-only deployment information. One-step factorization is separated from recursive closure; the full nonlinear system requires global fiber constancy or appropriately qualified Jacobian analysis. Value-weight dimensions and singular-weight kernels are explicit.

The finite-code result charges shared side information, codebooks and metadata, restricts the entropy endpoint to discrete exact reproduction, and retains the direct quotient encoder as the strongest simple representation baseline. Closest-work language assigns major component collision and claims only a bounded Delta diagnostic corollary. Native benchmarks are endpoint feasibility only; internal quotient measurement and empirical effect remain gap/unknown.

No further correction was required on the bound bytes.
