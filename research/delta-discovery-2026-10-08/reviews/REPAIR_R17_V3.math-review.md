# R17 v3 final-byte mathematical review

- Reviewer: `/root/capacity_candidate`
- Assignment: independently check dimensions, algebra, PSD ordering, probability composition, limiting cases and the repaired scalar comparator.
- Math artifact SHA256: `f7bf7ce4f7e94262ec337ebd299a7ffe7cd7ee6dd883b5b7c4e016fcf1e322d0`
- Repair screen SHA256: `87c517c94e2540eba7e64bf588d202672b581488969c8372fc6a34a3641f5bcc`
- Source audit SHA256: `ad288ebffcbf4bd90242265e2117e98370951de88fb806424c91d699bd932f97`
- Execution: exact-byte hashing and static semantic review only; no code, tests, model or experiment.
- Verdict: **VERIFIED_CONDITIONAL_THEOREM_REJECTED_CONTROL**.

For the declared frozen/common-exogenous suffix, `S^+-Sbar=beta k e^T` gives the exact energy `beta^2||e||^2 k^T G k`. The two Loewner inequalities imply the low-rank-plus-tail bound without independence. Top-eigenspace truncation and the tail-only upper matrix have the stated PSD ordering. The gate is valid only after a lawful prefix certificate has already been issued. The random-compression sigma fields and union-bound accounting are explicit.

The final comparator states `lambda>=0`, `c_t>=0`, `e!=0`, and `beta in [0,1]`; hence `beta*=1/(1+lambda c_t)` is the unique constrained minimizer. At `e=0` every gate has zero comparator loss and no uniqueness is claimed.

The theorem does not construct conditional coverage, solve semantic retain/revise validity, cover an endogenous nonlinear continuation, or prove empirical benefit. Parking after attempt 3/3 with zero candidate/admission/selection delta is correct.
