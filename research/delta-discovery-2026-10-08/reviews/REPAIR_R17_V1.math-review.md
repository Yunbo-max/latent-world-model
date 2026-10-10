# R17 v1 independent final-byte mathematical review

Reviewer: `/root/r17_quotient_math`. Assignment: independently derive and attack the exact-overwrite kernel, future-observation factorization, Gram condition, singular/partial-overwrite boundaries, conditional rate-distortion chain, and direct-code control. The reviewer did not author repository bytes, modify files, or run project/model code, tests, training, inference, scoring, or experiments.

- Artifact: `research/delta-discovery-2026-10-08/repairs/R17_PREDICTIVE_QUOTIENT_OVERWRITE.v1.md`
- Exact reviewed SHA256: `8e765da62723fe76480397284c716259ac8dad6ddacc9c8da18842c5d56df78a`
- Verdict: **PASS / conditional mathematics accepted / theorem-control only / park / zero candidate admission**.

## Independent reasoning

For unit `k`, invertible `D`, and `A=(I-kk^T)D`, `ker A=span(D^-1k)`, hence the matrix kernel is exactly `{D^-1ka^T:a in R^m}`. For a fixed old-behavior operator `O`, `ker(A·) subseteq ker O` is necessary and sufficient for the old quotient to factor through the overwritten old-state map: equal overwritten states imply equal declared old behavior, and any violating kernel vector is a sharp indistinguishable-pair witness.

The review confirmed that this is quotient decodability/no-extra-aliasing, not identity preservation by the deployed updater. The final artifact explicitly retains the stronger obligations: affine new-write handling, an actually used decoder or direct pre/post equality, recursive congruence, and semantic validity.

With `P_{u:t+1}=A_u...A_{t+1}` excluding the current `D`, the pre-decay condition is `q_u^TP_{u:t+1}D^-1k=0`; in the post-decay domain it is `q_u^TP_{u:t+1}k=0`. The scalar Gram identity, positive-weight support, value-weighted column operator `W_u^(1/2)E^TP_u^Tq_u`, Kronecker Gram, singular-`D` preimage kernel, and `beta<1` invertibility boundary are dimensionally and logically correct.

The finite-code chain `B>=H(Z|K)>=I(Q;Z|K)>=I(Q;Qhat|K)>=R_{Q|K}(delta)` is valid when `K` is shared side information and `Qhat` is decoded from `(Z,K)`. The exact entropy form is correctly restricted to a discrete exactly reproduced quotient. R10's relabeling argument survives quotienting when split components are consumed only through the same decoded quotient and all metadata/side information is counted.

## Corrections closed before acceptance

The independent review required and then rechecked: explicit suffix order; positive-weight `O_+`; the value-space operator order and singular-weight boundary; nonlinear-loss versus full-output scope; a precise `B^TS` direct comparator; finite-horizon/full-Jacobian boundaries; and decodability rather than semantic-identity terminology. All corrections are present in the bound bytes.

Unclosed items are scientific rather than algebraic: a lawful prefix-only query law, causal recursive quotient closure, matched basis/metadata/certification cost, semantic revision validity, native internal measurement, field-wide originality, and empirical effect.
