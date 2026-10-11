# R13 v2 source and collision audit — robust common covector

## Frozen atomic claim

When the realized affine Delta transition is hidden inside a lawful family, one mode-blind affine decoder exists exactly when one simultaneous block equation `X M=N` is consistent. Even individually invertible Delta transitions can be jointly inconsistent, and any same-post-state pair with different protected old values gives a half-diameter minimax error lower bound for arbitrary point decoders. This is a conditional diagnostic/impossibility boundary, not a new updater.

## Primary sources and fixed scope

| Work | Fixed locator/read depth | Material used | Boundary |
|---|---|---|---|
| Penrose, *A generalized inverse for matrices* (1955) | DOI `10.1017/S0305004100030401`; inherited D2 reading from R13 v1 | generalized-inverse solution of a consistent matrix factorization | establishes classical algebraic machinery, not the v2 Delta example or novelty |
| *On the existence of a common solution X to the matrix equations A_i X B_j=C_ij* | Linear Algebra and its Applications 375 (2003), DOI `10.1016/S0024-3795(03)00608-6`; primary abstract/metadata read | necessary/sufficient conditions for common matrix-equation solutions are established territory | different sided equation and presentation; supports collision family only |
| Moreno, *Simultaneous observation of linear systems: a state-space interpretation* | IEEE Transactions on Automatic Control 50(7):1021--1025 (2005), DOI `10.1109/TAC.2005.851447`; primary full-text abstract, introduction, problem formulation, distinguishability conditions and conclusion inspected | derives necessary/sufficient conditions for a single simultaneous functional observer for several LTI systems using indistinguishability and gives a common-observer structure | strongest direct mechanism collision; dynamic multi-system observer rather than R13's one-step affine post-state factorization |
| Ng, Tan, Trinh & Ng, *A common functional observer scheme for three systems with unknown inputs* | Journal of the Franklin Institute 353 (2016), DOI `10.1016/j.jfranklin.2016.03.020`; primary abstract, introduction, model and stated existence-condition scope read | common functional observers estimate selected state functions when the active system/input is uncertain | later cascade/logic-switch extension with unknown inputs; supporting collision but less direct than Moreno (2005) |
| Angulo, Moreno & Fridman, *On functional observers for linear systems with unknown inputs and HOSM differentiators* | Journal of the Franklin Institute 351 (2014), DOI `10.1016/j.jfranklin.2013.12.001`; primary abstract/introduction scope read | necessary/sufficient proper functional-observer conditions under unknown inputs | not the identical common-mode theorem; reinforces observer collision |
| Chen et al., *Outlier-robust set-membership estimation for discrete-time linear systems* | International Journal of Robust and Nonlinear Control (2022), DOI `10.1002/rnc.5948`; primary publisher page, abstract and stated method scope inspected; formula sections unavailable | feasible-set propagation, set inversion, and zonotopic outer approximation under uncertainty | estimates a state set rather than restoring an erased protected value |
| Chai, Sun & Qiao, *Set membership state estimation with improved zonotopic description of feasible solution set* | IJ Robust and Nonlinear Control 23 (2013), DOI `10.1002/rnc.2842`; primary summary and method scope read | zonotopic descriptions and intersection-based feasible-set tightening are established | supports set-valued-control collision, not v2 equations |
| R13 v1 pinned Delta sources | `Yunbo-max/latent-world-model@11bee1aac0429e0501a5b4d3244bca63d34bdc3b`, path `research/delta-discovery-2026-10-08/sources/R13_DYNAMIC_COVECTOR_SOURCE_AUDIT.md`, Git blob `60c629354fea1ebfa25e28de739a810f567408d0`; it pins FLA `a7880060012c862d58575ee23f613cafcd728d03`, DeltaNet paper, adjoint, reversible recurrence, and functional observers | realized Delta interface and v1 collision map | reused unchanged; no author code exposes a robust common-covector option |

## Search record and coverage

Search date: 2026-10-11. Query families: `robust functional observer uncertain linear systems common functional observer`; `set membership observer uncertain linear systems zonotopic observer`; `simultaneous equations XA_i=C common generalized inverse`; backward references from the common-observer and set-membership records. The search found direct common-functional-observer, simultaneous-matrix-equation, and set-membership families immediately. It was a bounded repair search, not two saturated novelty rounds; inaccessible paywalled formula sections remain a coverage gap. The source verdict is therefore collision/park, never an exhaustive priority claim.

## Semantic comparison

| v2 object | Closest mechanism | Residual | Disposition |
|---|---|---|---|
| one decoder across hidden transition modes | Moreno (2005) simultaneous functional observation; later common observers | explicit one-step post-state factorization | established mechanism family; no method novelty |
| `X M=N` kernel iff and pseudoinverse family | simultaneous matrix equations / generalized inverses | compact block arrangement for this affine interface | elementary specialization |
| compatible target set `C(z)` | set-membership estimation | protects a declared old linear target rather than full state | known feasible-set logic |
| half-diameter ambiguity bound | minimax indistinguishability / triangle inequality | two-key invertible Delta witness | useful Delta-specialized counterexample, not an updater |
| Bayes conditional variance | conditional expectation | mode/state posterior specific to the interface | standard same-information baseline |

## Code and measurement audit

The inherited pinned FLA implementation computes the realized rank-one Delta update and cache state but provides no protected-object oracle, transition-family generator, common decoder, compatible-target set, or internal certificate. This absence is not evidence of novelty.

LongMemEval's native knowledge-update judge, bAbI, and LAMBADA do not expose transition-mode identity, internal matrix factors, compatible-target diameter, or ledger state. Analytic traces could test equations (8)--(14) but would be instrumentation, not a native scientific endpoint. No benchmark or scorer was invented; empirical effect remains unknown.

## Verdict

- Formula/source support: adequate for a conditional theorem after independent math review; central algebra is self-derived.
- Closest-work disposition: robust/common observer, simultaneous-equation, and set-membership mechanisms cover the general construction.
- Residual contribution: explicit Delta invertible-mode counterexample plus a sharp information boundary.
- Originality: not established; no candidate admission.
- Reopen only with a causal native protected object, a certified structured uncertainty family, an operation unavailable to a direct value ledger, matched-cost advantage, and a native or formal measurement object.
