# Independent review — NOGO-CAP-02

- reviewer: `/root/nogo_cap02_review`
- reviewed artifact: `research/delta-discovery-2026-10-08/rejected/NOGO_CAP_02.md`
- exact artifact SHA256: `eb427d7dda60e53bea165002bbba0007b511c49d3412b2185f5fbc34d73cf7fc`
- verdict: **VERIFIED_REJECTED_CONTROL**

The revised exact bytes satisfy all requested corrections.  Dimensions are consistent, and varying independent (S) and (v) proves the affine exact-overwrite condition iff (A^\top k=0) and (u^\top k=1); nonzero (k\in\ker(A^\top)) makes the old-state path singular.  The ordinary-Delta specialization preserves (A=(I-\beta kk^\top)D), and its residual identity is correct.  The (D^{-1}ka^\top) witness is limited to invertible (D); the rank/nullity argument covers noninvertible (D) and justifies at least (m) lost real dimensions.

From (k=Qc), (A^\top Q=Q) and (u^\top Q=0), both protected-query contradictions follow: (A^\top k=k) versus (0), and (u^\top k=0) versus (1).  The orthogonal success case is valid.

The Fano section now defines finite-alphabet (M,V), finite post-state (Z), and decoder side information (K).  The conditional-entropy bound follows from \\(I(M,V;Z\mid K)\le H(Z\mid K)\le B\\); its exact-recovery cardinality corollary uses sufficient independence/uniformity assumptions.  The identifiability statement explicitly requires disjoint admissible behavior sets and excludes degenerate/equivalent cases.  The escape-route and nearest-work claims are appropriately bounded.

Rejection as a candidate is justified: this is a control/no-go, not a new update.  Its scope must remain explicit: exact overwrite for every (S,v) in the declared affine per-step class, full old-state recovery without auxiliary information/state, and deterministic state-only identifiability under identical inputs.  It does not cover restricted state manifolds, nonlinear/state-dependent or augmented updates, approximate overwrite, or recovery modulo a justified predictive quotient.  The Fano result additionally requires a finite post-state and finite alphabets.  Nearest-work coverage is bounded, not exhaustive.

No files were edited by the reviewer, and no project code, tests, benchmarks, training, inference or scorer was executed.
