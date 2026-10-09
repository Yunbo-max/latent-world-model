# Independent source and native-feasibility audit: two repair lines

Source worker: `/root/repair_sources`, assigned by `/root` in this actual Work turn. Integration writer: `/root`. Source worker input SHA256: `78cf4e32eff8188bb34e5b41cb7fad3a41eaa1ab86d4d5cb92d5407d36fc280c`. This integrated audit is separately reviewed against the final repair bytes; it is not candidate admission. Scope: primary literature, actual author files, existing native records; no project/upstream execution, software tests, training, inference, scoring, data/model download, GPU, Docker or main writes by the source worker.

## 1. Fixed right/value-span repair

The repair is mathematically consequential: for orthonormal `V` and a recursion `X_next=L X+U <G,X>` with `X=Z V^T` and `U=u c^T V^T`, all left multiplication preserves the fixed right span. The small representation evolves as `Z_next=L Z+u c^T <G V,Z>`. It does **not** require left factors to commute. This narrows an earlier false universal inference from rank-one write or contraction to low exact rank. It does not erase the old counterexample, whose independent right directions violate the fixed-span assumption.

Source status:

- Koch & Lubich, *Dynamical Low-Rank Approximation*, SIAM J. Matrix Anal. Appl. 29(2):434–454, DOI https://doi.org/10.1137/050639703. Official page https://epubs.siam.org/doi/abs/10.1137/050639703 fetched; full text redirected to access page. Therefore **abstract/metadata only** here; no full-formula review claimed for the 2007 paper.
- Lubich & Oseledets, *A projector-splitting integrator for dynamical low-rank approximation*, https://arxiv.org/pdf/1301.1058, PDF contains arXiv v2 stamp, 8 Jan 2013. Full formulas actually read: §2 Eq.(3),(5)–(8), factor dynamics and tangent projector; §3.2 practical QR/SVD splitting; §4 Theorems 4.1–4.2, exactness for an exact-start rank-at-most-r matrix path and perturbation robustness. These are continuous-time variable-factor results, not the current discrete fixed-right-span theorem. Do not invoke them as if they prove the proposed repair. A bounded author-code search found no confirmed author repository; third-party embedding/PDE implementations are not author code.
- Existing project primary audits retained: RTRL, NoBackTrack §2 Eq.(4)/§3 rank-one trick, UORO Eq.(5), KF-RTRL §2–3, OK Definition1/Theorem1, SnAp §2.1/§3 and e-prop. This audit actually reread SnAp https://arxiv.org/html/2006.07232v1 §3.2 Eq.(4), §3.3 and its gated-architecture limitations. Sparse reachability is different from fixed right-span invariance, but proves structural restrictions on full Jacobian are already a strong simplification baseline.

Important distinction: representing full memory as `S=M V^T` with all values `v=V c` is an exact algebraic reduction to an r-value Delta memory. It changes representational capacity, rather than giving free sensitivity savings for an unconstrained d_v-value model. If only tangent is constrained, the assumptions must show every relevant injection and transition preserves that span; choosing a basis from a future terminal tangent is an oracle. If V is learned/adaptive and depends on the focal gate, its derivative adds a channel. Rotating V without that derivative is not full closed-loop credit.

Novelty disposition: **correctable hypothesis boundary / exact representation control / bounded residual lead**. Generic invariant-span geometry and low-rank reduction are known. A Delta-specific discrete characterization and a leakage-to-credit bound can be useful theory, but no new optimizer or matched-budget advantage is established. Exact rank closure alone does not supply a deployable updater or retention guarantee.

## 2. Residual interval and robust gate descent repair

This line changes the objective from recovering all high-rank tangent entries to certifying one scalar action derivative. A valid error interval `|g-ghat|<=delta` plus a valid smoothness bound yields a safe step if the slope margin exceeds uncertainty; abstention is a legitimate boundary rather than a failed method. The error propagation and scalar descent lemma are generic inexact-gradient/a-posteriori-error mathematics.

New primary dependence actually reviewed:

- Vernimmen & Glineur, *Worst-case convergence analysis of relatively inexact gradient descent on smooth convex functions*, https://arxiv.org/html/2506.17145v2, 11 Sep 2025. §1.1 explicitly assumes an admissible smoothness bound; Algorithm1 Eq.(1) defines a relative-error gradient oracle; §2 and Theorem3.1 derive conditional smooth-convex bounds. These convex global rates are not claimed for neural Delta losses. The scoped collision is error-aware step selection, not any Delta residual certificate.
- The paper directly links author repository `Verpierre/Inexact_gradient_descent`, observed main fixed to `6aa405019ba871770d22e3a227682c15e36fe15c`. Actual file `utilities_neuro.py`, Git blob `fb3828fda15305052fd0d0a8f6dff8cd3d102e71`, was read. `inexact_wc_gradient_descent` calls PEPit `inexact_gradient_step(...,notion='relative')`; `PV` and `my_PEP` assemble worst-case SDP constraints. This is analysis code with external solver dependencies, not a neural gate certificate or learned updater; none executed.
- Hallak & Levy, ICML2024 *A Study of First-Order Methods with a Deterministic Relative-Error Gradient Oracle*, https://proceedings.mlr.press/v235/hallak24a.html. Official publication page read; linked PDF fetch and OpenReview access unsuccessful. **Abstract/page-level lead only**, not full formula/code audit. It is a relevant projected/conditional-gradient nearest-work lead for gate constraints.

Novelty disposition: **valid repair/control, certificate-construction lead**. An uncertainty margin and smooth descent/abstention alone are not new. Residual certification might become a substantial contribution if it is causally obtainable and cheaper than exact full derivative at matched total cost, with a scope-specific Delta consequence. Needed distinctions: an analytically legal bound vs learned/local numerical estimate; observed past/arrived-feedback losses vs unseen future deployment labels; focal gate derivative vs updater meta-gradient; one-suffix descent vs general knowledge validity or RSI.

Cheap residual warning: a residual `r_j=T_j Xhat_j-Xhat_(j+1)` is only cheap if all terms needed for it are truly evaluated or legally bounded. A full dense JVP, full costate, long suffix replay, or global Jacobian/Hessian bound can dominate the saved sensitivity storage. Low-rank factors may allow contractions, but a norm bound on omitted full state-dependent key/value/decay/workspace derivatives cannot simply be declared available. If unavailable the result stays conditional; a neural prediction of a bound is not a certificate.

## 3. Native measurement and fair alternatives

Reused actually read project records: `sources/BASELINE_NATIVE.md`, `sources/MEASUREMENT_FEASIBILITY_2026-10-09.md`, `sources/PROJECTED_DELAYED_CREDIT_SOURCE_AUDIT.md`, `sources/CLOSED_LOOP_RANK_GROWTH_SOURCE_AUDIT.md`, `sources/EFFECTIVE_RANK_TRUNCATION_SOURCE_AUDIT.md`. No new benchmark or scorer invented.

| Asset | Existing native endpoint | Repair mechanism gap |
|---|---|---|
| bAbI20 / 20,000 test denominator | Per-task answer accuracy, short facts and reasoning | No fixed-value-span annotations, exact tangent/costate, residual bound or gate descent truth |
| LAMBADA-openai / 5,153 | Last-word prediction | No update-effect, fact-validity or gradient certificate labels |
| BABILong / RULER | Long-context endpoint, delayed influence/retrieval/VT | Length also changes distractors; no native tangent leakage/certificate labels |
| CITB / TRACE | Sequential parameter-learning retention/transfer | Not automatically persistent Delta fast-state update or learning-speed evidence |
| LongMemEval / SEAL continual | Update/temporal QA or self-edit retention | No exact internal derivative/certificate truth; official large-model/judge requirements retain documented resource gaps |

Theorems can be checked by independent semantic mathematics at this stage. Future claim-specific internal instrumentation tied to unchanged native samples needs later authorized Local work; it is not a new benchmark/scorer or an executed experiment here. Endpoint improvement alone cannot certify the interval or rank mechanism. Existing direct gradient/BPTT, fixed Delta, scalar-gate sensitivity, generic projected low-rank/Galerkin, UORO/KF-RTRL/OK/SnAp, ordinary future CE, direct action predictor and fixed learned updater are mandatory applicable strong alternatives.

Fair costs include full forward state, span/factor storage, basis construction/update, per-focal-action sensitivities, JVP/VJP count, costate and omitted-channel estimates, suffix activation/replay, certificate looseness/abstention, target-token budget and external feedback information. Compare model capacities when r-value restriction is enforced. A reduction in tangent storage does not by itself establish total training FLOP/wall-time improvement.

## 4. Decision and reopen conditions

Both lines are worthwhile repair-and-rederive work. Neither deserves rejection merely for lacking a universal theorem. Preserve old bytes/counterexamples/reviews; register versioned child lead and distinguish mathematical correctness, contribution difference and empirical unknowns. No D ID or scientific promotion follows from this audit alone.

Further step: a real causal structural restriction (or observable leakage envelope), the actual compressed recursion/certificate cost, and a nearest-work comparison showing whether this is only generic low-dimensional Delta/reduced derivative or a specific useful formal consequence. If the only cost saving comes from reducing model value dimension, compare directly to the same r-value ordinary Delta. If legal residual/smoothness bounds cannot be obtained affordably, park the practical certificate claim while retaining its conditional theorem.
