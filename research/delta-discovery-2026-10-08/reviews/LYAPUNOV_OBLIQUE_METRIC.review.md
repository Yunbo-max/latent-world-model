# Independent review — SPD metric rescue of oblique Delta

- reviewer: `/root/lyapunov_oblique_audit`
- reviewed artifact: `research/delta-discovery-2026-10-08/rejected/LYAPUNOV_OBLIQUE_METRIC.md`
- exact artifact SHA256: `c82ed50bee17c6cb48bfc463cc690913a6ba5d11121be126e65b0334a2a20fd6`
- verdict: **VERIFIED_REJECTED_COORDINATE_CONTROL**

The existence condition \(0<r^\top w\le2\), the necessary alignment \(Hw\parallel r\), the PSD slack and the whitening equivalence were independently checked.  The condition-number lower bound in the artifact is algebraically identical to \((1+\sin\theta)/(1-\sin\theta)\); it correctly diverges near orthogonality.  The artifact also preserves the ordered-decay and time-varying-metric caveats: token-local certificates do not compose without a cross-time Lyapunov inequality.

Fixed metric oblique Delta is exactly normalized symmetric Delta after a linear coordinate transform.  Direct functional collisions include PDN inverse-Gram addressing, KDN covariance gain, GDN2 oblique erase, QED query-derived erase, protected/natural-gradient geometry and stable/orthogonal RNN parameterizations.  In particular, existence of a token-specific metric is a weak after-the-fact certificate and does not establish product stability or numerical safety.

A causal time-varying metric satisfying the cross-step inequality, uniform conditioning and a non-equivalence to PDN/KDN could be a future lead, but no such update law is present.  Rejection as a distinct candidate is justified.

No files were edited by the reviewer, and no project code, tests, models, benchmarks, training, inference, scorer, download or GPU work was executed.
