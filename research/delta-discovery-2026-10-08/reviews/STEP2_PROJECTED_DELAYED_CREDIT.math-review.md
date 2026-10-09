# Independent mathematical review: projected delayed credit

Reviewer: `/root/projected_credit_math_review`  
Assignment: independent semantic review of dimensions, ordered Jacobians/adjoints, Delta differential, frozen-path rank-one eligibility, action-span representation bound, local intervention identifiability, finite-horizon bounds, counterexamples and hidden costs.  
Final artifact: `research/delta-discovery-2026-10-08/STEP2_PROJECTED_DELAYED_CREDIT.md`  
Final SHA256: `b6df898dd549ad3d563deb10ff791c11ab179f8d86a90ef157fa2a25dd6876d0`  
Mode: static mathematics only; no project/upstream execution, tests, training, inference, scoring, downloads, GPU or Docker.

## Review history

Initial exact-byte review of SHA256 `873b38a604e07162fa93c283fef9515682a24734ab377098cb9fbae247fd20c9` returned **REVISE**. It found six substantive scope/notation issues:

1. the focal residual did not consistently use the post-decay state;
2. the rank-one loss factorization lacked its fixed-readout-only path assumption and did not define its weights;
3. the action-span lower bound had been stated beyond the linear-summary class actually proved;
4. the scalar delayed-outcome Gram condition did not state whether it identified fixed coefficients or conditional means under randomization;
5. the finite-horizon bound reused an already-discounted symbol and did not distinguish the full closed-loop Jacobian from the frozen Delta left operator;
6. the teacher-forcing counterexample needed to restrict equality to contexts in data-distribution support.

It also requested explicit current-action VJPs, the initial-state term boundary in the meta-gradient, and the positive-definiteness condition for the quadratic action.

The writer corrected all six issues. Review of SHA256 `06c8fc68b775ed53b33287c3a8f6d5c072ca0d220af34e4e005cf239629560ed` found one remaining notation mismatch: `de` and the value action still used the pre-decay symbol. The final artifact consistently uses

`bar S=D S`, `e=v-bar S^T k`,

`S^+=bar S+k a^T`,

`de=dv-(d bar S)^T k-bar S^T dk`, `d bar S=(dD)S+D(dS)`.

## Final checks

Accepted as correct under its explicit assumptions:

- full closed-loop adjoint order and `B_t^T lambda_(t+1)` action gradient;
- Delta action VJPs and differential dimensions;
- rank-one propagation of one focal gate edit under fixed future features/actions and fixed readout-only loss paths;
- `O(d_k)` query-side eligibility with diagonal decay for that narrow path;
- sufficiency of projecting the costate onto the executable action span;
- the `dim(U)` lower bound for an exact **linear** summary that scores every action in the span;
- conditional quadratic-risk order: condition first, then solve; the PSD/positive-definite limitation is explicit;
- conditional Gram-rank requirements for local slope/curvature under model correctness, finite moments and randomization/homogeneity;
- finite-horizon sign reversal and the need for full ordered-product control in any geometric tail bound;
- teacher-forced versus free-running support, potential-outcome and total-write-log non-identifiability boundaries;
- population equivalence to a sufficiently expressive same-information direct action predictor.

## Final verdict

**ACCEPT as conditional Step2 mathematical control / lead; no admission.**

The artifact does not prove an original method, a low-dimensional full closed-loop meta-gradient, empirical advantage, recursive self-improvement or scientific qualification. Open obligations remain:

1. a controlled low-rank approximation error after full updater/state feedback destroys the frozen rank-one tangent;
2. an advantage over direct action prediction and ordinary future-CE/BPTT at matched information, action capacity and total compute;
3. an executable intervention/exploration design whose conditional Gram is sufficiently ranked without unacceptable sequential variance;
4. a native measurement that jointly tests update-policy learning, retention and later-task learning efficiency;
5. a substantive residual beyond sequential Settlement and gradient-conflict screening.

Counts remain **5 historical / 0 active / 0 scientifically admitted / 0 selected**.
