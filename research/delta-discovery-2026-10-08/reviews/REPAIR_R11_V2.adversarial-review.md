# R11 v2 independent adversarial and fair-budget review

- Reviewer: `/root/r11_v2_adversarial_review`
- Math artifact SHA256: `452b5753a732a6b9d868ecf2d3647a9d6efcc5f8c0c8fd6932b58342847d0b63`
- Source audit SHA256: `f8c56d34300eea81c08deee5108ce914af46bc2076aa9a43928ec28f99d2863c`
- Verdict: **PASS**

The initial review found one blocking budget error and four material scope/cost omissions. A centered rank budget had been presented as though it were the rank of an online edit from the observed physical branch; `C=0` at `p=1/2` had therefore been mislabeled as no correction. The reviewer also required plug-in selector error, pure-Delta scope, action-invariant `G`, persistent-overlay costs, and physical-base-point controls. All findings were corrected before this final-byte review.

The final review confirms:

1. `bar S`, `S_z`, and the executed state `S_s` are explicit; equations (20)--(22) correctly use `(z-s)/2` and `(m-s)/2` under `rank(Delta)<=r`.
2. The real no-op is `Delta=0`; its conditional risks for `s=+1` and `s=-1` are correct.
3. Equation (23) separates plug-in calibration error on retained core directions from the physical truncation tail, and estimator cost is charged against a direct same-information predictor.
4. The theorem is limited to pure scalar-`beta` Delta and is not extended to a decay matrix, KDA, normalization, or state-dependent features.
5. `G` is decision-time lawful and action invariant; action-dependent future queries demote it to a local surrogate.
6. A carried low-rank overlay affects later residual reads and can grow in rank, so merge/recompression/materialization and their errors/costs are explicit.
7. Controls use the physical branch and matched information/rank/carry budgets. DeltaProduct remains an order-mechanism control, not a free semantic selector.

No hidden oracle, state, compute, equivalence, or candidate-accounting issue remains within the declared scope. Recommended status remains parked conditional theorem/control, attempt 2/3, candidate delta zero, empirical effect unknown.
