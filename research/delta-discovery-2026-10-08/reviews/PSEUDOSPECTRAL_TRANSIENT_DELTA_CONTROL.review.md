# Independent review — PSEUDOSPECTRAL-TRANSIENT-DELTA-CONTROL

Reviewers: `/root/pseudospectral_delta_math` and `/root/pseudospectral_delta_audit`. Read-only mathematical/source review; no project execution.

Decision: **reject as candidate; retain only as a scoped diagnostic/control**.

- The audit proved (K(A_t)=1) for every standard contractive Delta factor, so the proposed local penalty is vacuous there.
- Both reviews found that fixed-matrix Kreiss theory does not compose over token-varying ordered factors. Counterexamples with matched local data and different ordered products close that extrapolation.
- Product/Jacobian norm penalties, common/path-complete Lyapunov functions, joint spectral radius and D03-style predicted future products exhaust the causal executable variants.
- Exact or grid Kreiss estimation adds substantial resolvent cost and breaks the efficient recurrence advantage without adding semantic evidence.
- Oblique variants may still use the quantity as a diagnostic, but no native public text benchmark identifies pseudospectral transient growth, and non-normality can be useful.

No D-number is assigned. Reopening requires an observed internal transient failure plus a causal fixed-cost statistic that is not equivalent to product/Jacobian regularization or common-metric preconditioning.
