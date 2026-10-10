# R06 v2 independent mathematical review

- Reviewer identity: `/root/r06_v2_math_review`
- Assignment: independent dimension/order/optimization/boundary review of R06 v2 after repair
- Artifact: `repairs/R06_CONTRACTIVE_ENVELOPE_AUDIT.v2.md`
- Exact artifact SHA256: `93c92c3b31a8b3b46820dfd5a0d90c08de834370e3a347641dfbb7aa887dc5cd`
- Verdict: **PASS**

The first review required four corrections: the current-write norm needed `|beta_i|`; the clipped allocation had to separate zero-envelope coordinates and the high-budget regime; the oracle needed active-support/strict-positivity qualifications and `sum Z>0`; and the normalization had to be scoped to an offline finite frame. The exact reviewed bytes contain all four repairs.

Independent checks on the final bytes:

1. Dimensions and multiplication order are valid: `A_s,P_{i,H}` are key-space square matrices, `U_i,S_i` are key-by-value, and `P_{i,H}=A_H...A_{i+1}`.
2. Under `0<=beta_s||k_s||^2<=2`, each future rank-one factor is nonexpansive, so `||P U||_F<=||U||_F`.
3. The rectangular minimax reduction and no-cap PPS/Neyman allocation follow from Cauchy--Schwarz.
4. The floor/cap cases, zero-envelope support, excess-budget nonuniqueness and all-zero case are now correct.
5. Equation (14) is correctly a worst-case HT second-moment ratio, not a generic conditional-variance ratio.
6. The tilted-weight identity, Kantorovich factor `(1+alpha)^2/(4alpha)`, endpoint sharpness and `1/delta` divergence witness are correct on the declared support.
7. The same-prefix annihilation/preservation witness proves that contraction alone gives no positive continuation lower bound.
8. Frozen-path versus full-Jacobian, adaptive-feedback, residual-calibration, measurement and total-cost limitations are explicit.

Scientific disposition: mathematical pass for a conditional Delta-specialized theory/control; no novelty pass, empirical verdict or candidate admission follows.
