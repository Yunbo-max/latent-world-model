# R19 v2 prefix-branch-code source, collision, interface, and measurement audit

Scope: primary mathematical sources, already-pinned author interfaces, and native measurement feasibility. No project or author code was executed; no model/data was downloaded; no test, training, inference, scoring, GPU work, paid service, or Docker was used.

## 1. Fixed primary sources and read scope

| Source | Fixed identity / inspected scope | Consequence |
|---|---|---|
| Meng and Ramamoorthy, *Quantum advantage in zero-error function computation with side information* | arXiv `2402.01549v1`, 2024-02-02; full HTML inspected, especially §I-A Definition 1 and equations/definitions around the one-instance confusion graph, and the classical coloring statement | Decisive direct collision. Their graph joins source values sharing decoder side information while requiring different function values; one-shot fixed-length classical communication is a proper coloring and has alphabet size `chi(G)`. R19 v2 is this theorem with pre-write state as source, `(W,visible branch label)` as side information and released value as function. |
| Khajenejad and Yong, *Simultaneous Mode, State and Input Set-Valued Observers for Switched Nonlinear Systems* | arXiv `2102.10793v1`, 2021-02-22; full HTML inspected: system (3), Problem 1, §3.1 equations (4)--(5), (9), (12)--(15), (18), Algorithm 1 lines 145--170, and §3.2 residual elimination | Decisive mechanism neighbor. It uses a bank of mode-matched set-valued observers, residual-based elimination and union of compatible state/input sets. A prefix ambiguity set or release-mode bank is not a new estimator mechanism. Its main stated model has one true mode constant over time, so it is not a formula-level proof of R19's changing protection semantics. |
| Baum, Liu, Qin and Stursberg, *Using Seminorms To Analyze Contraction of Switched Systems With Only Non-Contracting Modes* | arXiv `2512.16338v1`, 2025-12-18; formula-level scope inherited and rechecked from R19 v1: Definition 6/equations (15)--(19), Lemma 1/equations (22)--(28), Theorem 2/equations (60)--(63) | R19 v1's mode-dependent PSD seminorm, cross-mode factor and dwell skeleton are already covered. V2 does not restore novelty by adding discrete branch coding. |
| Angeli, Philippe, Athanasopoulos and Jungers, *Path-Complete Graphs and Common Lyapunov Functions* | arXiv `1612.03983v1`, 2016-12-13; primary abstract and stated main theorem inspected | Supports the known control that branch-labeled Lyapunov inequalities/path-complete graphs certify arbitrary switching and imply common min/max Lyapunov constructions. Used as a collision/control pointer, not formula-level support for Theorem 1. |
| Girard, Pola and Tabuada, *Approximately bisimilar symbolic models for incrementally stable switched systems* | arXiv `0807.5022`; primary abstract/contribution scope inspected | Supports the established transition-system/symbolic-abstraction route: under common or multiple Lyapunov incremental-stability assumptions, finite approximately bisimilar models are constructed. R19's finite transition relation is not a new abstraction framework. |
| Petreczky, Bako and van Schuppen, *Realization theory of discrete-time linear switched systems* | arXiv `1103.1343v2`; primary full-paper theorem scope inspected | Decisive collision for stacking lawful mode-word output maps and quotienting their common kernel: minimal switched realizations are characterized through reachability/observability and Hankel rank. R19's linear fork-rank formula is only a one-step Delta corollary. |
| Kong, Payne, Zhu and Johnson, *Saltation Matrices: The Essential Tool for Linearizing Hybrid Dynamical Systems* | arXiv `2306.06862v3`, Proc. IEEE 2024, DOI `10.1109/JPROC.2024.3440211`; equation (9), variational update (10), transition-sequence caveats, and official `robomechanics/Saltation-Tutorials@c0c1c4ab55db481e167763a9476113d010906134` interface inspected | A reset Jacobian omits event-time sensitivity at a smooth transversal guard; the saltation matrix is the correct local baseline. Grazing, simultaneous guards or different transition sequences require stronger set/Bouligand treatment. This correction is known, not R19 novelty. |
| Project R18 v2 and R19 v1 packets | `repairs/R18_PREFIX_CAUSAL_ROBUST_QUOTIENT.v2.md`, `sources/R18_PREFIX_CAUSAL_ROBUST_QUOTIENT_SOURCE_AUDIT.v2.md`, and the R19 v1 artifact/audit/reviews | R18 already requires prefix-measurable path families, global fiber/right congruence and direct-ledger rank; R19 v1 already proves the realized-branch PSD kernel obstruction. V2 may retain only the finite zero-error specialization and its explicit bit assumption. |

The exact graph-coloring theorem does not depend on Meng--Ramamoorthy's quantum extension; only their classical Definition 1 and coloring statement are used. Their paper also traces the result to Witsenhausen's 1976 zero-error side-information work. The accessible primary full text is sufficient to establish a decisive mechanism collision; R19 does not claim firstness.

## 2. Author-code/interface status

R19 v2 is a theorem/debug control and introduces no executable algorithm dependency. No official implementation is needed to validate the elementary coloring equivalence, and no code pin is fabricated for the classical information-theory or switched-control papers.

The already audited model interfaces remain unchanged. SEAL, ACL/SRWM, HOPE/Titans, AToKe-like temporal editing and the project's Delta neighbors do not expose a native finite recurrent-state alphabet, release-confusability graph or zero-error branch code. Khajenejad--Yong's Algorithm 1 is a paper algorithm for compatible-set propagation and mode elimination, not a drop-in language-model interface. Nothing in these sources establishes that R19 is empirically effective, cheaper than direct storage, or recursive self-improvement.

The fixed saltation tutorial repository is an actual robotics interface, not a Delta implementation: `Hybrid iLQR/h_ilqr.m` accepts flows/resets/guards/guard Jacobians/saltation functions, while generated helpers such as `Hybrid iLQR/dynamics_helpers/salt/calc_salt12.m` return concrete saltation matrices including the guard-time denominator. No file exposes protection fibers, prefix branch codes or language-model release labels.

## 3. Collision and retained difference

After checking that the released target is single-valued for every fixed `(state,visible label)`, Theorem 1 maps exactly to zero-error function computation with decoder side information. If that feasibility condition fails, R19 has a hidden-branch relation rather than a deterministic function and no side-code size can repair it.

- source symbol: pre-write state `x`;
- decoder side information: destructive state and visible branch label `(W(x),lambda(b))`;
- desired function: the unique released value `g_b(x)` determined by `(x,lambda(b))` under the feasibility condition;
- message: prefix code `c(x)`; and
- characteristic/confusion graph: equation (3) of the artifact.

Consequently `chi(G)` is established machinery, not a new theorem family. Multiple-model set-valued observers cover honest propagation of compatible modes/states under uncertainty. Approximate bisimulation/symbolic abstraction and path-complete Lyapunov work cover branch-aware transition relations and stability certificates. Internally, R18 v2 covers the continuous/linear prefix-robust quotient and direct sufficient ledger.

Petreczky et al. make the linear collision sharper: stacking transported reads over all lawful switching words and removing their common invisible subspace is switched observability/minimal-realization machinery. Kong et al. likewise remove any claim that replacing a reset derivative by a guard-aware saltation map is new. These sources leave the finite zero-error Delta mapping as a useful explanation, not a distinct mechanism.

The narrow retained value is project-local and diagnostic: it repairs R19 v1's illegal use of a realized/common branch, prohibits differentiating through an arbitrary discrete selector, and gives a finite-precision exact side-state cost for a Delta release. It does not create a distinct update rule or matched-cost advantage.

Novelty disposition: **decisive zero-error function-computation collision plus major set-valued-observer/R18 overlap; scoped Delta debugging corollary only; not scientifically admitted**.

## 4. Information, cost, and measurement boundary

The finite alphabet is a substantive assumption. Its construction must charge range, quantization, reachable-set coverage and codebook/decoder metadata. Exact coloring can be computationally intractable; the chromatic number is a characterization, not a scalable learned update. On continuous states, the artifact makes no finite-bit claim. A later approximate result would need a distortion metric, noise/roundoff model, decoder regularity and prefix-conditional coverage.

The branch label must be genuinely visible after the switch. If it is predicted, its error and calibration are separate evidence. If it is visible before the destructive write, a mode-specific code is allowed but timing has changed. If the full old state survives until label arrival, that state is the storage control. Semantic validity remains unidentifiable from identical prefixes without external evidence, exactly as in R08.

Existing native assets measure downstream endpoints only:

| Asset | Can measure later | Missing central object |
|---|---|---|
| LongMemEval `xiaowu0162/LongMemEval@9e0b455f4ef0e2ab8f2e582289761153549043fc` | 500-question knowledge-update/temporal/retrieval endpoints plus official retrieval recall/NDCG | paired same-state release alternatives, confusability graph, code optimality or causal attribution; the official QA scorer uses a paid GPT-4o endpoint unavailable in this phase |
| LongMemEval-V2 `xiaowu0162/LongMemEval-V2@2cc8c540bdb87fe6761629b585e727e1c4704520` | ordered `insert(trajectory)`/`query` interface, 451-question dynamic-state/premise/gotcha endpoints, context tokens and latency | no protection mode, destructive fiber, side-code bits or paired branch counterfactual; published reader/embedding/judge and long-asset requirements are not admitted on the stated 2080Ti |
| EvoMemBench `DSAIL-Memory/EvoMemBench@aa4cea8fd936b76b2d3591d3ef897030617dc43a` | InEp-Know Accurate Retrieval, Selective Forgetting and Conflict Resolution, plus accuracy/progress/token use | no R19 graph/fiber labels; several native paths require external hosted API credentials/services or separate environments |
| AToKE `Arvid-pku/ATOKE@a1b42e34e4130507220307ced3d681fb8719831f` | sequential rewrite data with old/new targets, time and history/current evaluation fields | no released scorer/implementation in the inspected repository and no need to infer release from a lawful prefix; no branch/fiber mechanism label |
| SEAL `Continual-Intelligence/SEAL@6d9c9f9ee392c6cc618e771f399d436d190f6ca4` | lower-triangular old/new accuracy after continual parameter merges | parameter-level LoRA editing, not fast-state release; CLI states at least two GPUs/default 7B and the paid grader violates current resources |
| bAbI, LAMBADA, RULER, BABILong | task accuracy/token prediction/long-context retrieval | no temporal validity, obsolete/still-valid distinction, finite recurrent alphabet, destructive fiber, lawful branch relation or zero-error target |

An implementation could derive the graph on a finite instrumented state set, but that would be a new diagnostic with coverage assumptions, not a native benchmark scorer. The mechanism claim remains unmeasured.

For any future behavioral comparison, the required same-information controls are full released-value signature storage, full pre-write-state retention, R18's prefix-robust ledger, no-write/never-release, ordinary always-release Delta, R08's direct release rule with identical arrived evidence, time-conditioned latest-wins/KV, memory-free full history at the same context cap, and same-capacity replay/external KV. State bytes must include the color, branch/mode ID, evidence history, codebook, decoder and precision metadata. An oracle branch/future-validity arm is only an upper bound, never a fair primary baseline.

## 5. Search receipt and decision

Search date: `2026-10-11`. Bounded primary-source queries included:

- `zero error function computation side information characteristic graph chromatic number primary paper`;
- `Witsenhausen characteristic graph side information zero error coding`;
- `Orlitsky Roche coding for computing graph entropy`;
- `set-valued observer switched systems unknown mode hybrid systems`;
- `path-complete Lyapunov switched systems mode dependent quadratic`;
- `approximate bisimulation switched systems finite symbolic model`;
- `saltation matrix hybrid guard reset event time sensitivity`; and
- `realization theory discrete-time linear switched systems observability Hankel rank`.

Fixed full-text retrievals used `https://arxiv.org/html/2402.01549v1` and `https://arxiv.org/html/2102.10793v1`; the remaining primary records and R19 v1's fixed Baum full text support only their declared scopes. This is a bounded collision audit, not exhaustive field-wide originality proof.

Decision: retain R19 v2 only as a conditional theorem/debug control. It successfully repairs causality and discrete branch divergence for an explicitly finite state object, but the exact coding theorem is known, the compatible-mode mechanism is known, R18 already covers the linear/global quotient boundary, and no native measurement or matched-cost Delta advantage exists. Candidate delta remains zero; empirical effect remains unknown.
