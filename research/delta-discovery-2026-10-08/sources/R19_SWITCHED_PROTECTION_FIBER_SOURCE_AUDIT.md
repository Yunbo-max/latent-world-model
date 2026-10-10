# R19 switched-protection source, collision, interface and measurement audit

Scope: primary mathematical sources, already-pinned author interfaces, and native measurement feasibility. No project or author code was executed; no model/data was downloaded; no test, training, inference, scoring, GPU work, paid service or Docker was used.

## 1. Fixed primary sources and actual read scope

| Source | Fixed identity / read scope | Consequence for R19 |
|---|---|---|
| Baum, Liu, Qin and Stursberg, *Using Seminorms To Analyze Contraction of Switched Systems With Only Non-Contracting Modes* | arXiv `2512.16338v1`, 2025-12-18; full HTML/PDF inspected: §2 Definition 6 and equations (15)--(19), §3 Lemma 1 and equations (22)--(28), Theorem 2 and equations (60)--(63) | This is the decisive direct neighbor. It uses mode-dependent PSD seminorms with a fixed common kernel/invariant subspace, cross-mode comparisons `P_new preceq beta P_old`, and dwell/leave-time conditions. R19 (2)--(12) is therefore not a new switched-seminorm mechanism; the residual is restricted to what fails when the kernel itself changes and the additional coordinate/reset obligation. |
| Branicky, *Multiple Lyapunov Functions and Other Analysis Tools for Switched and Hybrid Systems* | IEEE TAC 43(4):475--482 (1998), DOI/IEEE record `10.1109/9.664150`; primary-publisher metadata/abstract and theorem scope only | D1/supportive provenance for multiple mode-dependent Lyapunov functions; it is not used here as formula-level evidence. |
| Hespanha and Morse, *Stability of Switched Systems with Average Dwell-Time* | CDC 1999 author-hosted full PDF `https://www.eng.yale.edu/controls/1999/average.pdf`; §1 definition `N_sigma(t,T)<=N_0+(t-T)/tau_D`, §2 uniform exponential/induced-norm setup, §3 Theorem 2, and §4 Assumption 3 equations (11)--(12)/Theorem 4 inspected | The switch-count factor and average-dwell conversion behind R19 (10)--(12) are known. R19's finite product is a direct discrete tangent specialization, not a new dwell-time theorem. |
| Della Rossa and Tanwani, *Converse Lyapunov Results for Stability of Switched Systems with Average Dwell-Time* | arXiv `2405.03560`; primary abstract/main-contribution scope inspected, not used as formula-level evidence | D1/supportive evidence that modern work supplies converse multiple-Lyapunov characterizations for average-dwell classes. |
| Veer and Poulakakis, *Ultimate Boundedness for Switched Systems with Multiple Equilibria Under Disturbances* | arXiv `1809.02750`; primary abstract/result scope inspected, not used as formula-level evidence | D1/supportive evidence that switched disturbance/ultimate-bound accounting is established territory. |
| Project primary-source packet for coupled updater stability | `sources/COUPLED_UPDATER_RSI_SOURCE_AUDIT.md`; full HOPE/Titans/SEAL/ACL/Sleep mechanisms and pinned available SEAL/ACL interfaces already inspected there | Learned/self-modifying updates, old/new-task meta-objectives and multi-timescale consolidation are already covered. R19 cannot promote mode switching to recursive self-improvement. |
| Project temporal-release packet | `sources/REPAIR_R08_TEMPORAL_VALIDITY_SOURCE_AUDIT.md`; BOCPD, POMDP/controlled change detection, AToKe, StableEdit and RLEdit scopes already fixed | Evidence-dependent release and switching cost are direct prior controls. R19 contributes only the missing dynamics composition boundary, not a new release policy. |
| Project dynamic-readout/quotient packets | `sources/R13_DYNAMIC_COVECTOR_SOURCE_AUDIT.md` and `sources/R18_RECURSIVE_JOINT_QUOTIENT_SOURCE_AUDIT.md` | Functional observers, generalized inverses, recursive invisible quotients and direct sufficient-coordinate ledgers cover the transport and side-state mechanisms used by R19. |

Baum et al. is materially closer than the earlier generic multiple-Lyapunov sources: its mode-indexed PSD seminorms, invariant common kernel, cross-mode matrix comparison and dwell/leave analysis directly overlap the R19 proof skeleton. Its fixed-common-kernel assumption also isolates the only defensible extra boundary in R19: if a protection release changes the kernel, a finite comparison can fail and an honest certificate must reset/transfer or account for the newly exposed coordinates. The exact finite-factor criterion in R19 (5)--(6) is elementary PSD generalized-Rayleigh algebra. A bounded search did not locate the identical Delta release-ledger corollary, but absence of a verbatim composite is not evidence of firstness.

## 2. Author implementation interfaces

R19 is a theorem/control and introduces no executable algorithm dependency. The classical control papers do not provide an author implementation needed to evaluate equations (3)--(6); no code pin is fabricated.

For learned updater/release neighbors, the already audited interfaces remain the authoritative record:

- SEAL official `Continual-Intelligence/SEAL@6d9c9f9ee392c6cc618e771f399d436d190f6ca4`; the continual driver persists merged LoRA parameters and uses a paid GPT-4.1 grader. It does not expose protection-mode PSD energies or cross-mode tangent labels.
- ACL official `IDSIA/automated-cl@3d7b53adb4b6b43acd82b9a381a2c631d0e59a5d`; `layer.py::SRWMlayer.forward` exposes evolving self-referential state, not a certified release/reset interface.
- HOPE/Titans author implementation gaps and HOPE equation/chunk ambiguity remain exactly as recorded; no third-party implementation is substituted.
- R08's AToKe/StableEdit/RLEdit author interfaces provide temporal/editing controls but no native scorer for the R19 kernel condition.

Thus no source or implementation supports a claim that R19 is already empirically effective, cheaper than a direct ledger, or a deployed self-improving updater.

## 3. Mathematical collision and retained difference

Baum et al. already supplies the direct semidefinite switched-system neighbor: Definition 6 gives a PSD seminorm and invariant nullspace; Lemma 1 assumes the same kernel for every mode and compares mode matrices at switches; Theorem 2 combines a separating family with dwell/leave conditions. The product bound

`V_T <= product(rho_t^2) product(mu_switch) V_0`

and its average-dwell corollary are therefore standard switched-seminorm/multiple-Lyapunov logic. The exact existence criterion

`ker(P_old) subseteq ker(R^T P_new R)`

is the PSD domination condition for a finite generalized Rayleigh quotient. The direct released-coordinate rank is the same sufficient-statistic/quotient dimension logic already used in R12 and R18.

The narrow retained contribution is therefore only a debugging bridge across project records and the fixed-kernel condition in Baum et al.: fixed-fiber Delta stability deliberately uses a seminorm with neutral protected directions; an evidence-triggered release can change that kernel and make those directions transverse; unless a reset maps them into the new kernel or their dynamic coordinates are carried explicitly, an old-energy-only stability certificate has an infinite switch multiplier. This corrects a composition gap without declaring any parent result false and does not constitute a new switched-seminorm framework.

Novelty disposition: **major component collision; scoped Delta protected-fiber corollary only; not scientifically admitted**.

## 4. Information, resource and native-measurement boundary

R19 assumes the protection mode and reset are lawfully chosen from arrived information. It does not infer factual validity. A posterior/hazard, external feedback, replay or audit state used to choose release is additional information and must be charged separately. The released-coordinate ledger has local real dimension `rank(P_new^(1/2) R K_old)`; its basis, precision, decoder, mode ID and update cost count. A full dense metric over the complete recurrent state is generally infeasible; low-rank/local certificates lose global coverage.

Existing native assets can measure only downstream endpoints:

| Asset | Can measure | Does not natively expose |
|---|---|---|
| bAbI / LAMBADA / RULER / BABILong | task accuracy, final-token or long-context retrieval under an implemented model | protection mode, PSD energy, reset tangent, cross-kernel truth, paired release/no-release state |
| LongMemEval | temporal/knowledge-update QA endpoints and evidence sessions | complete joint state, semantic mode ground truth at action time, equations (3)--(6), causal attribution |
| SEAL continual self-edit | old-question accuracy after later parameter merges | fast-state protected fiber, matched reset, native cross-mode energy; official grader also violates the no-paid-service constraint |
| AToKe-like temporal editing | dated knowledge/edit outcomes | a Delta-state switch certificate or same-state paired intervention |

A future implementation could derive JVPs and energies on unchanged native samples, but that would be an added diagnostic, not a native label/scorer. No benchmark, label, metric, case or result is invented here.

## 5. Search and decision receipt

Search date: `2026-10-10`. Exact bounded query strings included:

- `mode dependent semidefinite Lyapunov seminorm switched systems kernel average dwell time`;
- `switched system multiple Lyapunov semidefinite common kernel generalized eigenvalue`;
- `arXiv switched systems seminorm contraction kernel dwell time`;
- `arXiv 2512.16338 Using Seminorms To Analyze Contraction of Switched Systems With Only Non-Contracting Modes PDF Baum`;
- `Branicky multiple Lyapunov functions switched hybrid systems 1998`;
- `Hespanha Morse stability switched systems average dwell time pdf`;
- `converse Lyapunov average dwell time arxiv`; and
- `switched systems disturbances multiple equilibria ultimate boundedness arxiv`.

Fixed primary retrievals were `https://arxiv.org/html/2512.16338v1`, `https://arxiv.org/pdf/2512.16338`, and `https://www.eng.yale.edu/controls/1999/average.pdf`, plus the DOI/arXiv records listed in §1. The Baum full arXiv HTML/PDF and Hespanha--Morse author PDF provide the formula-level evidence; publisher/arXiv abstract-only items are marked supportive rather than used as formula-level proof. Existing fixed packet audits supplied the already-read updater, temporal-release, functional-observer and native-interface evidence. This is a bounded search receipt, not a claim of exhaustive field-wide originality coverage.

Decision: R19 is worth retaining only as a conditional theorem/control because it closes a project-local mathematical interface and gives a sharp changed-kernel failure condition. Baum et al. decisively removes any broader claim to mode-dependent switched-seminorm novelty. R19 does not provide a distinct update architecture, an originality-certified theorem family, a release-validity estimator, matched-budget advantage or empirical evidence. Candidate delta is zero.
