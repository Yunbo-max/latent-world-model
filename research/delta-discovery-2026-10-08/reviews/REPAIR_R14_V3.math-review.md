# Independent mathematical review — R14 v3

Reviewer: `/root/r14_v3_math`  
Mode: independent read-only derivation and exact-final-byte review; no editing, project code, test, training, inference, scoring or experiment.

Reviewed exact final bytes:

- `repairs/R14_OBSERVABLE_EQUIVALENCE_CLOSURE.v3.md`
- SHA256 `7656047affe4d7866358cb5b3a568ea27d5effad427b6d93c9cdf45a55c5aa81`
- screen SHA256 `69faa9df793a91bc6c1303c8dc03a20a4c67ca8c399528f1a92a7db7e6e04538`

## Checks

- Verified the total-variation convention through the common-submeasure identity `mu(Omega)=1-delta`.
- Re-derived the certificate event and expected-width bounds `(1-2 alpha-delta)_+` under each endpoint world, including randomized procedures and the exact-equivalence single-atom condition.
- Re-derived the continuous two-slot quadratic minimizer `a_1=a_2=1/(1+lambda)`, value `lambda/(1+lambda)`, and the sharp TV-only lower bound `(1-delta)lambda/(1+lambda)`.
- Confirmed that the TV formula is exact at `delta=0` and sharp over experiments with fixed TV, but is not asserted to determine the minimax risk of every fixed intermediate experiment.
- Verified the separate nonconvex hard-action value `min{1,(1+lambda)/2}` when mixing is available; the continuous-action Jensen claim is correctly restricted.
- Verified data processing, extra-information, closed-world, local-loss and matched-information boundaries.

## Verdict

**PASS, conditional on the explicitly declared two-world observable experiment and local quadratic loss.** No mathematical blocker remains on the bound bytes. This is a terminal theorem/debug control, not a new updater. `candidate_delta=0`; native measurement and empirical effect remain open/unknown; attempt 3 of 3 may be parked.
