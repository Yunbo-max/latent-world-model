# Independent review — Revision-evidence posterior edit

- reviewer: `/root/revision_control_review`
- reviewed artifact: `research/delta-discovery-2026-10-08/rejected/REVISION_EVIDENCE_POSTERIOR_EDIT.md`
- exact artifact SHA256: `455ca60d940f17da9de6ff6f0f122a2d3bbc45848e130e0477627d3fe144d3d4`
- verdict: **VERIFIED_REJECTED_CONTROL**

The final artifact correctly limits the posterior formula to points with a nonzero denominator and separates equal-prior conditional TV from the general unequal-prior Bayes error.  It does not use TV classification error as a bound on language CE or downstream memory.  Perfect identification is explicitly conditional on disjoint evidence laws rather than assumed from an ID name.

For \(U\in\mathbb R^{d\times m}\), the gradient equation is

\[
[aa^\top+(1-\gamma)kk^\top+\lambda I]U
=\gamma a e_a^\top+(1-\gamma)k e_k^\top,
\]

so the closed form is dimensionally correct and unique for \(\lambda>0\).  The endpoint language is also correct: finite ridge does not give exact overwrite or hard protection; the protected minimum-norm formula appears only in the \(\lambda\to0\), \(z\ne0\) constraint limit.  For \(k=\pm a\), coexistence feasibility is exactly \(e_k=0\), not an imprecise comparison of old and new values.

The construction is a Bayes action for the declared edit loss, not for sequence likelihood in general.  Its two principal components collide with known Bayesian/change-point gating and protected/ridge/slot editing.  A collapsed two-hypothesis posterior is not a full BOCPD run-length posterior, and taking one posterior-risk action is not dynamically identical to maintaining a predictor mixture; the artifact preserves these distinctions while recording the substantial functional collision.

The remaining prerequisites are real: a reliable old address must be retrieved, one protected linear query does not imply semantic/nonlinear protection, teacher-derived \(\gamma\) must be compared under equal information, and public native tasks do not expose per-write revision/coexistence labels.  The rejection as a distinct method is therefore justified.

No files were edited by the reviewer, and no project code, tests, models, benchmarks, training, inference, scorer or GPU work was executed.
