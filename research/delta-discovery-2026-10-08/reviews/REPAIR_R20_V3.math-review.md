# Independent math review — R20 v3

Reviewer: `/root/r20_math`  
Assignment: independent derivation and edge-case review; reviewer did not author repository files.  
Artifact: `research/delta-discovery-2026-10-08/repairs/R20_SPECTRAL_TRANSFER_CERTIFICATE.v3.md`  
Artifact SHA256: `9fff175d5a25aa905ba1cc8efa11ae5d6bf56a1f66539619f4f0ba7481aedde7`

## Verdict

**PASS only as a conditional pure-quadratic theorem/control; FAIL as a deployable candidate repair.** Candidate increment remains zero.

## Independent checks

1. The loose chain \(M/m\) is valid but not sharp. Whitening the surrogate and using the minimum-norm projection property reduces the ratio to
   \((u^\top Gu)(u^\top G^{-1}u)\), whose sharp bound is the Kantorovich constant
   \[
   \frac{(M+m)^2}{4Mm}.
   \]
2. For \(m=1-\delta\), \(M=1+\delta\), the sharp worst-case ratio is \(1/(1-\delta^2)\), not the endpoint-chain value \((1+\delta)/(1-\delta)\).
3. The smallest useful prior linear domain for a fixed nonzero target is
   \(L_e=\operatorname{span}(\mathcal C_e)=\ker A+\operatorname{span}\{\widehat x\}\). An ex-post bound on \(\operatorname{span}\{\widehat x,x_H\}\) is algebraically sufficient but depends on the unknown future.
4. The equality witness \(\widehat H=I_2\), \(H=\operatorname{diag}(m,M)\), \(u=(1,1)/\sqrt2\), \(u^\top x=1\) attains the constant.
5. For the symmetric Loewner uncertainty set, the minimax action remains the surrogate optimizer because the pointwise worst case is the upper endpoint. Robustification therefore does not define a new action.
6. Edge cases are correctly separated: \(e=0\), \(m=0\)/\(\delta\ge1\), singular metrics, and a one-dimensional feasible span.

## Required scope limits

The result does not cover a future linear term, nonlinear remainder, changed free-running trajectory, factual validity, or an unobserved counterfactual loss. A spectral premise on feasible differences alone is insufficient because it omits affine base--tangent cross terms.

## Final assessment

The artifact incorporates the corrected sharp constant, the correct affine-span domain, and the no-new-action minimax consequence. The remaining missing object is a prefix-checkable transfer law. Mathematical status: `accepted_conditional`; contribution and empirical status remain unproved.
