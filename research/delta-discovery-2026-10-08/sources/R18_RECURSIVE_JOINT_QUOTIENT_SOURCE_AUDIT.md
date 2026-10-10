# R18 recursive joint quotient — primary-source, author-interface, distinctness, and measurement audit

Date: 2026-10-10. Subject: `../repairs/R18_RECURSIVE_JOINT_QUOTIENT.v1.md`; subject SHA256: `c3b32f912637b5ba3f1e6978f0c981d517a3d561736e246a7b2d392011d8f559`. Scope: bounded primary-source and actual-interface reading plus native-measurement feasibility. No project/upstream code, tests, model execution, training, inference, scoring, dataset/model download, GPU work, or Docker was used. Current fixed reads from R17 and the Step2 full-Jacobian audit were rejoined rather than relabeled as new evidence.

## 1. Linear quotients and recursive invariance: decisive mechanism collision

George J. Pappas, *Bisimilar Linear Systems*, Automatica 39 (2003), DOI <https://doi.org/10.1016/j.automatica.2003.07.003>.

- The author-hosted full text was rechecked at <https://www.georgejpappas.org/wp-content/uploads/2024/04/AUT03.pdf>. Section 6.1 Theorem 16/equation (19) gives `A ker H subseteq ker H + range(B)` for one-step discrete-time bisimulation; Corollary 17/equations (26), (28) extends it to timed multi-step transitions. Section 7 Theorem 21/equations (39)–(41) computes the maximal controlled-invariant subspace inside an observation kernel by iterative intersection/preimage. In Section 8.1, the observation-preservation condition immediately before equation (47) is `ker H subseteq ker C`; after choosing `H=C`, equation (47) becomes `A ker C subseteq ker C + range(B)`.
- For fixed-input/common-affine Delta differences, the input term cancels and the condition reduces to transition invariance of the quotient kernel. This is a direct mechanism-level collision with R18's backward invisible-subspace construction.
- R18's `N_j=ker C_j cap J_j^-1 N_(j+1)` is the finite-horizon time-varying backward form of the same observation-plus-transition compatibility. Choosing `Q_j` with `ker Q_j=N_j` and factoring `Q_(j+1)J_j` and `C_j` through `Q_j` is standard quotient linear algebra.

Paulo Tabuada and George J. Pappas, *Bisimilar Control Affine Systems*, Systems & Control Letters 52(1), 2004, DOI <https://doi.org/10.1016/j.sysconle.2003.09.013>, author-hosted full text <https://www.georgejpappas.org/wp-content/uploads/2024/04/TP04SCL.pdf>.

- Tabuada–Pappas Theorem 4.1 characterizes pushforward-compatible vector fields; Definition 4.3 introduces invariant and controlled-invariant distributions; Theorem 4.4 characterizes controlled invariance. Theorem 4.5 requires a surjective submersion with connected fibers and invariant `ker Tr` for local bisimulation; Theorem 4.6 gives the controlled analogue. These are precisely the regularity and fiber conditions missing from a single nominal Jacobian test.
- This primary work characterizes nonlinear/control-system equivalence through output agreement and forward-compatible relations/distributions. It supports the global-congruence collision, not an assertion that it contains R18's Delta formulas verbatim.

A.J. van der Schaft, *Equivalence of Dynamical Systems by Bisimulation*, IEEE Transactions on Automatic Control 49(12), 2004, author-deposited full text <https://ris.utwente.nl/ws/files/6620093/01369393.pdf>.

- Section III Algorithm 3.3 and Theorem 3.4/equations (21)–(25) compute the maximal bisimulation relation by iterative subspace refinement; Section IV constructs quotient/reduced systems. This independently confirms that recursive quotient closure and refinement are established geometric-control machinery.

Jeremy Rodgers, *Observable Quotients and Exact Projected Dynamics* (author-deposited 2026 preprint), DOI <https://doi.org/10.5281/zenodo.21371251>.

- R17's audit read Proposition 3.2/Corollary 3.3 on fiber constancy and kernel annihilation, Theorem 5.2 on semigroup descent via kernel invariance, and Theorem 6.4/Proposition 7.7 on projected dynamics and finite observability.
- This source is not peer reviewed and describes its ingredients as classical. It is corroboration, not priority evidence. It independently reinforces the distinction among one-step factorization, recursive closure, and unresolved-memory terms.

Conclusion: the recursive quotient construction is a major mechanism collision. R18's residual is only the explicit placement of a Delta exact-overwrite fiber inside the complete recurrent tangent state, including cross-block rescue and exposure witnesses.

## 2. Full-Jacobian observability Gramian: exact internal collision

Yu Kawano and Jacquelien M. A. Scherpen, *Empirical Differential Gramians for Nonlinear Model Reduction*, arXiv:1902.09836v2 / Automatica 127 (2021), 109534; Mohamad H. Kazma and Ahmad F. Taha, *Observability for Nonlinear Systems: Connecting Variational Dynamics, Lyapunov Exponents, and Empirical Gramians*, arXiv:2402.14711v7.

- The current `RECURSIVE_RANDOM_METRIC_SOURCE_AUDIT.md` read Kawano–Scherpen Definition 3.2/equation (8): a differential observability Gramian pulls output derivatives back through the state-transition Jacobian along a fixed nonlinear trajectory.
- It read Kazma–Taha Section III equations (10), (13)–(15), and Appendix C equation (36), including correctly ordered transition products and nonlinear output Jacobians. This is the same full-joint finite-horizon object as R18's equations (9), (17), and the backward zero-kernel recursion.
- Actual author interface remains pinned at `mhkazma/ObsNonSys-VarGram@2bb5060454ddc63cd57681355fa6300fb9c6dc2e`: `AVarObsGram.m` blob `d2c548fe310b3e76463e5524a476199f5c482d8a` constructs `Phi_0_k`, `Psi_0_k=C*Phi_0_k`, and `Wo_M=Psi'*Psi`; `AVarDyn.m` blob `da73adbc53352c9a4eb24f8ae45b0bdb5677fe62` jointly integrates state and Jacobian. The code uses a linear output matrix while the paper gives the nonlinear-output extension. No execution receipt is claimed.

This source pair is decisive against presenting the R18 Gramian or backward kernel recursion as a new memory mechanism. The Delta kernel specialization and two opposite cross-block error modes are useful debugging consequences only.

## 3. Predictive fibers, PSR, and functional observers

Two very recent direct neighbors make the recursive/minimal-state collision stronger.

Qinyou Wang, *Fiber Fingerprints of Hidden Learning-State Dynamics*, arXiv:2608.15976v1, full HTML <https://arxiv.org/html/2608.15976v1>.

- Definition 2.3/equations (2.5)–(2.6) defines complete and finite-horizon predictive equivalence; Theorems 2.4–2.5/equations (2.7)–(2.8) give transition congruence and Nerode-style minimality. Remark 2.7/equation (2.10) explicitly warns that a finite-depth relation loses one unit of depth after a transition, so using the same finite horizon before and after a step is not recursively well typed. Definition 2.8/equations (2.12)–(2.13) repairs this with prefix-depth fibers.
- Section 4.6/equation (4.19) introduces a positive-semidefinite future-observability field. Appendix A.7 identifies regular-fiber tangents with a Jacobian kernel only under smoothness and local constant rank, and switches to tangent-cone language at singular fibers; Appendix A.8 gives the same-first-derivative/not-the-same-finite-response obstruction. These are direct collisions with R18's depth-indexed recursion, Gramian, and local-versus-global warning.
- No official author repository was found in the bounded search. The paper does not state the exact Delta overwrite specialization or the two cross-block witnesses, but those are scoped corollaries rather than a new quotient mechanism.

Xianyao Li et al., *Minimal Recurrent Behavioral Memory for Imitation under Partial Observability*, arXiv:2609.25757v1, full HTML <https://arxiv.org/html/2609.25757v1>.

- Definition 2 distinguishes a recurrent realization from an instantaneous statistic; Definition 3 and Appendix A.2 Lemma 2 require backward recursive compatibility/right congruence. Theorem 1/equation (2) shows that the equivalence classes admit a deterministic recurrent update and, when the relation is transitive, minimize conditional entropy. Definition 4/Proposition 2 handles nontransitive compatible assignments. This independently closes the gap between one-step sufficiency and recursive state closure.
- The author repository is pinned at `XianyaoLi/DIACRITIC@08858b1c20958a2e3a4687a3502b9087ee80d0f5`. `toy/gamma_solver.py::_refine` (lines 63–87), `GammaSolver.solve` (121–137), and `gamma_J` (139–146) refine finite symbolic history classes; `certify/core.py::Adapter` (32–52), `record` (95–136), `certify_env` (143–159), and `certify` (162–172) record and certify environment histories. It is an enumerable-history/reset-oracle solver, not an online Delta Jacobian construction, and no execution receipt is claimed.

Linzhe Zhang and Changming Xu, *What Can a Recurrent State Safely Forget?*, arXiv:2609.23366v1, full HTML <https://arxiv.org/html/2609.23366v1>.

- Section 2 defines predictive equivalence/fibers and requires an exact semantics-preserving corrector to stay within a fiber. Theorem 2 gives the local quotient constraint; Sections 3.1–3.2 add finite audit-bank and generative reset/probe certificates.
- R18 is narrower: a finite-horizon tangent audit on one fixed joint trajectory. It neither learns the complete predictive fiber nor obtains the source's generative audit access. No official author repository pin was found in the bounded R17 audit.

Singh, James, and Rudary, *Predictive State Representations: A New Theory for Modeling Dynamical Systems*, arXiv:1207.4167v1; Zhan, Uehara, Sun, and Lee, *PAC Reinforcement Learning for Predictive State Representations*, arXiv:2207.05738.

- PSR represents state by predictions of future tests and provides recursive observable-state updates. The later PAC paper's Section 2 defines tests, system-dynamics matrices, core tests, and predictive states; its assumptions and active action sequences are much stronger/different than R18's local overwrite diagnosis.
- The inspected author PSRNN baseline stays pinned at `cmdowney/psrnn@fd13b60f1cb62f2aed00348fe839ed9358655c79`: `psrnn_cell_impl.py::PSRNNCell.call` produces a state-conditioned matrix update, and `two_stage_regression.py` supplies random-feature, SVD, and ridge two-stage estimation. It implements a learned recursive predictive state, not a Delta overwrite certificate.

Functional-observer sources remain those in `R13_DYNAMIC_COVECTOR_SOURCE_AUDIT.md`: Luenberger 1966 DOI `10.1109/TAC.1966.1098323`, Roman–Bullock 1975 DOI `10.1109/TAC.1975.1101061`, Penrose generalized inverses, and adjoint transport. R13 computes a selected visible covector; R18 computes the maximal finite-horizon invisible tangent subspace. They are dual views of the same factorization geometry.

## 4. Internal distinctness and strongest simple comparator

| Existing packet result | Relation to R18 | Decision |
|---|---|---|
| R17 predictive quotient | direct parent; already says recursive use needs invariant/time-varying congruence | R18 constructively fills that scope gap for a fixed full-Jacobian finite horizon, not a new method |
| Step2 recursive random metric | its full-Jacobian observability/GGN Gram has the same kernel when output weights are positive definite on the declared output space | R18 is the binary/backward-kernel form; singular weights certify only the weighted quotient |
| R13 dynamic covector | transports chosen visible functionals and gives the same generalized-inverse/functional-observer collision | R18 collects all visible covectors; no new decoder or selector |
| R12 syndrome readout | static kernel factorization plus direct sufficient-coordinate dominance | R18 composes it through time; `rank(QK)` direct side ledger remains the control |
| R01-v2 quotient closure | exact lumping/invariant-row-space skeleton | different declared endpoint, same quotient mechanism |
| Wang predictive fibers / Li recurrent behavioral memory | finite-depth fibers, depth loss, right congruence and recursively minimal state are direct current neighbors | R18 retains only the explicit Delta overwrite and joint cross-block debugging specialization |

The strongest same-information baseline is ordinary Delta plus the direct `r_lost=rank(QK)` lost-visible coordinate ledger, with its basis, decoder, precision, suffix/operator construction, and metadata charged. Full unrolled JVP/VJP is the direct diagnostic baseline. R18 provides no lower-cost prefix-only construction and no method-level residual.

## 5. Native measurement feasibility

| Asset / fixed interface | Native object and possible endpoint use | Missing R18 object / fairness boundary |
|---|---|---|
| bAbI via ParlAI `a29567f7ce76992fd1f03c51ba9e3b155a37ea51`, `parlai/tasks/babi/agents.py` and `ExactMatchMetric`; 20 tasks / 20,000 test questions | short factual, temporal, path and multi-hop QA endpoint | fixed `en-valid-10k-nosf` input and scorer neither expose nor consume supporting-fact IDs; those exist only in original/other variants as extra diagnostic labels and cannot be updater input. The current adapter replays full context in a fresh stream per question, so it does not test cross-question persistent-state recursion; no joint-state perturbation, `J,C`, quotient/kernel label or paired overwrite |
| LAMBADA OpenAI variant through lm-eval `d6de81643928d653435c431bae19945d41d32520`, `lambada_openai.yaml`; 5,153 passages | final-word log likelihood, greedy accuracy, perplexity | fresh passage state and no overwrite event, distance control, joint intervention or recursive-closure label; score changes mix language modeling, access and memory |
| RULER official main `c3f5e3b4f87f97e048793bb510a3a6b19a46bf3a`, `rulerv1-ns` pipeline `e8bbff677ca2c239640dc90f93310dcf32408c93`, native evaluation/scripts; 13 tasks x 6 lengths x 500 | NIAH, variable tracking, aggregation and length-degradation endpoints | substring/reference coverage does not expose state/Jacobian/kernel and cannot attribute a gain to R18; preserve null/missing counts and identical generation budget |
| LongMemEval author repo `9e0b455f4ef0e2ab8f2e582289761153549043fc`; 500 questions | knowledge update, temporal QA, session/turn retrieval endpoints | native knowledge-update judge may accept old information plus the updated answer; evidence IDs are scorer-side; no paired state intervention or quotient truth. The repo exposes judge aliases, but pinned `print_qa_metrics.py` asserts `gpt-4o-2024-08-06`; native QA scoring is not execution-ready under no-new-paid-service plus one RTX 2080 Ti, and listed local Llama-3.1-70B is neither assumed feasible nor authorized |
| BABILong author repo `booydar/babilong@7a6efee29f5cac03c3c410e6799c80fd2ffe3610`; `metrics.py` unique-answer extraction from a closed label set; 100/1,000 samples per task-length | long delayed multi-fact QA endpoint; at 32K, all 20 tasks are about 64M/640M input-token positions per arm, with all-length totals counted separately | length also adds distractors and does not isolate R18; no native joint tangent, no-write counterfactual, or overwrite-kernel ground truth |

These tasks can conditionally test downstream behavior of a later implementation; none natively provides paired same-prefix state interventions, the full joint state, `C_t/J_t`, `ker O_(t:H)` truth, overwrite/no-overwrite potential outcomes, a causal prefix-only quotient certificate, or attribution separating the certificate from extra state/retrieval. JVP/VJP instrumentation on unchanged native samples would be a derived measurement, not a native label or scorer. The predictive-fiber paper's reset/probe audit is closer, but assumes additional generative access and is not one of the project's fixed native Delta scorers.

Cost/accounting remains material: the complete state dimension includes `vec(S)`, reader/network hidden state, updater state, query/key generator state, and every recurrent cache. A stacked `(Hp) x n` operator uses `O(Hpn)` storage; exact dense QR/SVD can cost `O(min(Hpn^2,(Hp)^2n))`; matrix-free checks still charge horizon, directions, activation checkpoint/recompute and numerical tolerance. Random probes do not establish an exact kernel. Any quotient basis/decoder/scales/routing/certification state must be counted.

Existing approximate endpoint costs stay those already derived: full RULER is about 39,000 generations and 1.64B input-token positions per arm; LongMemEval-S about 57.5M and M about 750M input-token positions per arm plus 500 judge calls. The official LongMemEval QA judge conflicts with the no-new-paid-service/single-2080Ti boundary; no substitute string scorer or assumed local 70B execution is authorized.

Measurement status: theorem mathematically checkable; native endpoints conditionally usable; native mechanism identifiability is a `measurement_gap`; empirical effect is unknown.

## 6. Bounded search and final source decision

The bounded search joined the exact functional objects `linear bisimulation observation kernel transition invariance`, `nonlinear control bisimulation invariant distribution`, `variational observability Gramian`, `predictive state recursive core tests`, and current packet functional-observer/quotient records. The search did not find a primary source writing the exact combined phrase “ordinary Delta exact-overwrite kernel plus complete-joint backward invisible-subspace recursion plus cross-block rescue/exposure witnesses.” That absence is not priority evidence: every structural component is established, and the combination is a direct specialization.

- Mathematical-source support: sufficient for the conditional affine/local theorem after independent exact-byte review.
- Mechanism originality: **major component collision / scoped Delta debugging corollary only**.
- Author implementation: adjacent observability/PSR interfaces inspected; no R18 implementation or runtime advantage exists.
- Measurement: endpoint feasibility only; internal mechanism gap.
- Empirical status: unknown; no execution.
- Candidate delta: zero; park after attempt 1.

Reopen only with a globally checkable nonlinear Delta congruence that strictly strengthens the closest theory, or a lawful prefix-causal quotient construction that beats full observability/direct sufficient-coordinate/functional-observer/PSR controls at matched total state, precision, FLOPs/JVPs, information and native measurable behavior.
