# Independent mathematical review — R12 v1

Reviewer: `/root/r12_math_review`

Reviewed exact artifact:

- `repairs/R12_SUBSPACE_SYNDROME_READOUT.v1.md`
- SHA256 `da1a0df6bb3f9ba95605c8ee7200622dec61ca595031dc6c02a23852d01aefce`

Mode: independent semantic mathematics review; reviewer did not edit or publish artifacts and ran no project/model code.

## Checks and corrections

- Verified dimensions `M∈R^{m×r}`, `C∈R^{p×r}`, `R_0=CM†∈R^{p×m}`.
- Verified `ker M⊆ker C ⇔ row(C)⊆row(M) ⇔ ∃R:RM=C` and the pseudoinverse decoder.
- Verified the symmetric two-point constant. Required the invariant edit budget `||Ba||≤ρ` and scoped (8) as the exact zero-syndrome hidden-class minimax radius/global lower bound.
- Verified that `CM†` is a minimum, not necessarily unique, operator-norm extension and that only singular directions visible through `C` amplify noise.
- Verified equations (9)–(11), the noiseless qualification in (13), and all rank-one Delta dimensions/edge cases.
- Strengthened the direct-statistic control: a rank factorization stores `rank(C)d_v` coordinates, matching the minimum syndrome width.
- Corrected the multi-query notation by choosing `J∈R^{s×r}`, `row(J)=span_j row(C_j)`, so every `C_j=F_jJ` and `JA` reconstructs all targets.

## Verdict

**PASS for mathematical correctness and stated conditional scope.** This is a generic linear sufficient-statistic theorem/control. It is not an originality pass, empirical result, active method candidate or selection approval.
