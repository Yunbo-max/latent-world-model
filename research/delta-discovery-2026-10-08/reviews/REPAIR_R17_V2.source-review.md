# Independent final-byte source and novelty review — R17 v2

- Reviewer: `/root/r17v2_source_review`
- Math SHA256: `c7f7843a9508dbb5cc6fdf9525e23dc311eff070f58b572bb133850722eb1438`
- Source-audit SHA256: `f8f7bd33008eda1750506833af5e5dff6be71d7f7bcaa60dbffac811e3929ea2`
- Verdict: **PASS_CONDITIONAL_CONTROL; NOT_CANDIDATE**
- Execution: bounded source and interface review only; no project/upstream execution.

## Reasoning

The audit correctly binds the final bytes and preserved v1 audit. Petersen is attributed to Ian R. Petersen alone and limited to concept-level evidence from publisher metadata. Statistical locators are adequate: Tropp Theorem 6.1 for matrix Bernstein, Howard et al. Section 4.3/Corollary 3 for time-uniform matrix bounds, and Powel--Morgansen Sections II-B--IV for empirical stochastic observability Gramians and Fisher information.

The nearest-work decision is appropriately conservative. Robust unobservability, PSD support functions/DRO, matrix concentration/confidence sequences, predictive quotients and internal R09 cover the main mechanism; R12/R18 cover recursive closure. The retained difference is the Delta exact-overwrite erased-direction specialization and the explicit expected-versus-realized leakage warning, not a new architecture.

The benchmark statement is bounded to the fixed bAbI, LAMBADA, RULER and LongMemEval revisions inherited from R18 Section 5. Those assets expose endpoints but not the internal Gram, prefix prediction-set coverage or counterfactual erased state. No native mechanism-identifying benchmark was located in this bounded audit.

## Adjudication

Pass as a conditional theorem/debugging control. Active, admitted and selected deltas are zero; empirical effect remains unknown.
