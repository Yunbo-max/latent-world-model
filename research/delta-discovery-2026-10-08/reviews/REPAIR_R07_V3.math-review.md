# R07 v3 independent mathematics review

- Reviewer identity: `/root/r07v3_math`
- Assignment: fresh read-only final-byte review; no authorship and no file edits.
- Artifact: `repairs/R07_FACTOR_CORE_JOINT_MARGIN.v3.md`
- Reviewed SHA256: `a455e43a40d3be167f1712db3ef515945597e8868c97a11d16b33ebf8fbe9e80`
- Verdict: **PASS as a conditional exact theorem/debugging control; not a new active candidate. Attempt 3/3 is exhausted and parking is mathematically justified.**

## Checks

1. Equations (1)--(6) have consistent dimensions and orientations. With `S,U,Delta S in R^{d_k x d_v}`, `K,Z_t in R^{d_k x m}`, `E in R^{d_v x m}` and `c_t,a in R^m`, induction yields `Delta S_t=Z_t Diag(a)E^T`; transposition before multiplying by `q_t` gives `Delta o_t=E Diag(c_t)a`.
2. Equations (7)--(11) expand the half-weighted quadratic with the correct factors: `g=rho+sum Gamma_t^T W_t r_t` and `H=R+sum Gamma_t^T W_t Gamma_t`. The Hadamard identity is exact and `W_t,R >= 0` imply positive semidefiniteness by congruence. The scalar mapping to v1 is `g=-2q`, `H=2h`. Cartesian feasibility plus diagonal `H` is sufficient for separability; the artifact correctly limits necessity to uniform exactness over linear terms.
3. Equation (12), `(I-gamma uu^T)DZ=DZ-gamma u(u^TDZ)`, is exact and costs `O(d_km)` for diagonal `D`. Dense transitions, factor state, common/varying metric, `O(Hm^2)` accumulation and dense `O(m^3)` QP qualifiers are directionally correct. A future end-to-end account must also charge `Gamma_t^T W_t r_t`, up to `O(d_v^2+d_vm)` per step for dense `W_t`, unless `W_tr_t` is already computed by the no-action loss path.
4. Equations (13)--(17) rederive exactly. With `beta(S)=S`, `S_1=2a-a^2`; the frozen objective change is `a/2+a^2`, while the true change is `-a/2+(7/2)a^2-2a^3+a^4/2`. Thus the omitted `beta'(S)(v-Sk)` path reverses the first-order sign. The gate remains within `[0,1]` on the declared interval.
5. Equations (18)--(21) follow by subtracting the coupled and frozen recurrences. The norm recursion and Lipschitz objective envelope are valid; replacing the linear mismatch assumption by a quadratic one yields the stated quadratic envelope. The bounds still require an action-time-valid common tube, coefficient mismatch bounds, local Lipschitz constants and a separate tail bound.
6. The disposition is conservative: this is an exact low-rank weighted-least-squares/Hadamard-Gram reduction only under action-independent affine suffix coefficients. It does not close the prefix-information, free-running-law, native-measurement or matched-total-cost gaps.

## Unresolved limits

- Fixed simultaneous proposals are not sequential residual recomputation or ordered DeltaProduct updates.
- State-dependent keys, gates, values, queries, updater state, routes or action-dependent laws generally destroy the affine response core unless special cancellation occurs.
- Obtaining the frozen suffix, dense varying value metrics or large `m` can erase the factor-propagation saving.
- Weighted least squares, Hadamard/Schur Gram structure and reduced QPs are known mechanisms, so candidate delta remains zero and empirical effect remains unknown.
