# R18 v2 source, code-interface and native-measurement audit

Status: **collision confirmed; conditional theorem/control only; no candidate admission**.

## 1. Scope of the audit

R18 v2 changes the R18 v1 information boundary from a realized future suffix to a prefix-measurable tree/automaton of admissible complete-state affine modes. The audit asks whether the following are already covered: path-conditioned recursive indistinguishability, common invariant subspaces for switching systems, prefix-compatible predictive quotients, probabilistic recovery of invariant structure, and direct sufficient-coordinate observers.

The answer is yes at the mechanism level. The Delta-specific mapping remains useful as a debugging theorem, but no claim of first/new architecture is supported.

## 2. Primary-source collision map

### Linear switched realization and observability

Baştuğ, Petreczky, Wisniewski and Leth, *Model Reduction of Linear Switched Systems by Restricting Discrete Dynamics* (arXiv:1409.1444v2; Automatica 74, 2016), is the decisive collision. It represents admissible switching words by a regular language/finite automaton. Definition 8 and equation (13) define the `L`-unobservable subspace as the intersection of `ker(C_qA_v)` over admissible words; Lemma 4 constructs an `L`-equivalent quotient; Algorithm 2 computes the dual row-space family by automaton-state dynamic programming until rank stability. This is exactly the dual of R18 v2's node-indexed kernel intersections/preimages. It avoids enumerating exponentially many words but does not supply a Delta-specific advantage.

Petreczky, Bako and van Schuppen, *Realization theory of discrete-time linear switched systems* (arXiv:1103.1343) treat switching as an external discrete input, use noncommuting products of mode matrices, and characterize minimality through reachability and observability. Their realization/minimization procedures cover the arbitrary-mode-word linear quotient that R18 v2 specializes to an exact-Delta overwrite kernel.

De Santis, Di Benedetto and Pola, *Observability and Detectability of Linear Switching Systems: A Structural Approach* (arXiv:0802.4045) explicitly separates continuous-state and discrete-mode reconstruction. This is a direct warning that an unknown route/mode label is not free decoder information.

Tanwani, Shim and Liberzon, *Observability for Switched Linear Systems: Characterization and Observer Design* (IEEE TAC 58(4), 2013), recursively characterize the unobservable subspace for a known switching signal. This is the direct collision for R18 v1's fixed future path and prevents presenting v2 as merely repeating that recursion over several nominal paths.

The R18 v1 audit already pins Pappas, *Bisimilar Linear Systems* (Automatica 2003), Tabuada and Pappas (Systems & Control Letters 2004), and van der Schaft (IEEE TAC 2004): iterative maximal invariant/bisimulation refinements cover the core intersection/preimage and quotient logic.

### Predictive fibers and recurrent memory

Wang, *Fiber Fingerprints of Hidden Learning-State Dynamics* (arXiv:2608.15976v1), defines predictive equivalence, quotient descent, prefix compatibility/Nerode-style minimality, and finite-depth fibers whose type loses one unit of horizon per transition. This is a direct collision with treating a recursively usable predictive quotient as an unconstrained new object.

Li et al., *Minimal Recurrent Behavioral Memory for Imitation under Partial Observability* (arXiv:2609.25757v1), require continuation-support homogeneity/right congruence and construct exact minimal recurrent behavioral memory. The actual author repository is pinned at `XianyaoLi/DIACRITIC@08858b1c20958a2e3a4687a3502b9087ee80d0f5`. Relevant executable interfaces are:

- `toy/gamma_solver.py::_refine` (lines 63–87), `GammaSolver.solve` (121–137), and `gamma_J` (139–146), which refine behavioral classes and build the resulting memory;
- `certify/core.py::Adapter` (32–52), `record` (95–136), `certify_env` (143–159), and `certify` (162–172), which adapt and certify finite behavioral records.

These interfaces do not implement Delta overwrite repair, but they block novelty claims for recursive right-congruence/minimal-memory logic.

Baştuğ et al. state an official MATLAB data/code location (`https://kom.aau.dk/~mertb/`) in their numerical-example section. The location was inaccessible during this audit and no author mirror was found in bounded searches, so implementation bytes/functions are **not verified**. Tanwani–Shim–Liberzon link no official implementation. The previously pinned `mhkazma/ObsNonSys-VarGram@2bb5060454ddc63cd57681355fa6300fb9c6dc2e` implements nominal-path variational observability (`AVarObsGram.m` forms `Phi`, `Psi=C*Phi`, `Wo=Psi'*Psi`; `AVarDyn.m` integrates state plus variational Jacobian), not the automaton-language fixed point. It is a code collision with the v1 nominal/Jacobian audit only.

### Robust/common invariant subspaces and data-driven recovery

Berger, Jungers and Wang, *Data-driven invariant subspace identification for black-box switched linear systems* (arXiv:2209.05320), Proposition 1 characterizes a subspace invariant for every switching mode via common block-triangularization. Its sampled/scenario results provide probabilistic near-invariance; the paper explicitly warns that near block-triangularization does not generally imply an exact invariant subspace without extra information. Hence a learned prefix confidence set cannot be silently upgraded to exact quotient closure.

Petersen, *Robust Unobservability for Uncertain Linear Systems With Structured Uncertainty* (IEEE TAC 2007, DOI 10.1109/TAC.2007.902751), already directly covers robust-unobservability questions under structured uncertainty. Shang, *The Maximal Robust Controlled Invariant Set of Uncertain Switched Systems* (ACC 2004), uses vertex systems plus recursive preimage/intersection operations for robust invariance. Its controlled-invariance quantifiers are not identical to R18's universal no-leakage quantifier, so it is related support rather than a proof of R18 v2.

### Trace-equivalence scope

The common `L`-kernel identifies states that produce the same read trace under the **same** allowed switching word. If routing is state-dependent or nondeterministic and the desired relation permits different matching successors, a simulation/bisimulation relation on the transition system is required; a common linear kernel alone is insufficient. Enumerating algebraically possible but infeasible words is safe but conservative. This semantic distinction is a condition on R18 v2, not a novelty gap.

### Delta-neighbor implication

R18 v2 does not change the write rule of DeltaNet/Gated DeltaNet/KDA/RWKV-family mechanisms. It audits which complete-state distinctions an exact write may merge under a declared future family. Preconditioned/protected updates, direct ledgers, no-write/partial-write gates and full JVP/VJP remain stronger simple controls. Therefore no architecture-level novelty is claimed.

## 3. Exact residual difference

The residual artifact is the following synthesis, not an uncovered mechanism:

1. bind the complete exact-Delta overwrite fiber `ker A_t` to a prefix-measurable constrained future-mode tree;
2. warn that marginal per-time mode sets rectangularize and can be strictly overconservative;
3. derive the direct threatened-ledger lower bound `rank(O_T P_t K_t)` for that same tree and protected reference entrance;
4. expose a same-prefix two-world no-go where each oracle branch compresses but the lawful robust quotient is full rank;
5. keep mathematical correctness, contribution novelty and empirical status separate.

This may be retained as a theorem/debugging control. It does not support `candidate`, `selected`, “first”, or empirical-improvement language.

## 4. Native measurement audit

The pinned benchmark revisions remain endpoint-only:

- **bAbI / ParlAI `a29567...`**: exact-match on 20 tasks / 20,000 test questions. The pinned adapter restarts context per question and does not expose a persistent overwrite intervention, complete-state fibers or recursive-quotient truth.
- **LAMBADA / lm-eval `d6de816...`**: 5,153-passage final-word likelihood/accuracy/perplexity. It is a broad non-degradation endpoint with no declared write event or admissible operator tree.
- **RULER `c3f5e3...` plus pipeline `e8bbff...`**: NIAH, variable tracking, aggregation and length-specific native scores. It is the best pinned within-context retention endpoint, but it cannot identify the common invisible space or separate quotient closure from extra state/retrieval.
- **BABILong `7a6efee...`**: delayed multi-fact closed-answer extraction. Length changes distractors, and there is no state intervention, mode tree or ledger-rank label.
- **LongMemEval `9e0b455...`**: semantic/temporal/session/update endpoints with final judged answers. Evidence IDs are scorer-side, not updater inputs. The pinned `print_qa_metrics.py` scoring path asserts `gpt-4o-2024-08-06`; under the current no-new-paid-service and single-2080Ti boundary it is not execution-ready.

None natively exposes a prefix-conditioned `(J,C)` automaton, exact overwrite fibers, path coverage, a common recursive congruence, oracle-versus-lawful quotient rank, or overwrite/no-write potential outcomes. Computing these with JVP/VJP or a custom state intervention would be a derived diagnostic, not a native scorer. Native endpoint success cannot verify the universal mechanism claim.

## 5. Strong controls and fair cost

The primary exact comparator is ordinary Delta plus the direct pre-write ledger of width

\[
r_{lost}=\operatorname{rank}(O_TP_tK_t),
\]

using the same prefix-derived tree, basis, precision and decoder. If the repaired construction only selects write strength, it must also beat a same-prefix direct write/skip/strength predictor and no-write/partial-write/soft-preconditioned Delta. Full joint unrolled JVP/VJP on every represented branch is the expensive diagnostic control.

Fairness requires matching all recurrent state, tree/automaton and basis metadata, estimator parameters, precision, calibration examples, inference calls and generated tokens. No arm may receive the realized future mode, future token/answer, supporting-fact IDs, judge rationale or scorer evidence before it occurs.

With `B` enumerated lawful branches, `E` automaton edges, state dimension `n`, read dimension `p`, horizon `H` and `m` tested lost directions, explicit storage is `O(BHpn)`, dense branch operators can be cubic in `n`, and matrix-free auditing is `O(BmH)` full-network derivative passes plus rollouts. Recursive automata avoid enumerating every path but require basis/intersection/preimage work per edge and numerical rank decisions. The direct ledger pays the same basis-information cost. These are analytical planning estimates, not executed measurements.

## 6. Audit decision

- Mathematical identity: conditionally sound for a declared, prefix-measurable finite affine tree, subject to exact path conditioning and coverage.
- Source/novelty: core mechanism covered by switched realization/observability, common invariant subspaces, bisimulation/predictive quotients and direct observers.
- Author-code interface: inspected for the closest executable right-congruence/minimal-memory neighbor; it does not create a Delta novelty gap.
- Native measurement: endpoint feasibility only; mechanism identification and coverage calibration remain absent.
- Empirical effect: unknown; no experiment was run.
- Candidate decision: `candidate_delta = 0`; park after repair attempt 2/3.
