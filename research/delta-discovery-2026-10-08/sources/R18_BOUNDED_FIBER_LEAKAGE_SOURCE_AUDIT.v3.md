# R18 v3 bounded-fiber leakage ledger — source, interface, collision and measurement audit

- Subject: `../repairs/R18_BOUNDED_FIBER_LEAKAGE_LEDGER.v3.md`
- Scope: bounded primary-source and actual-interface reading plus mathematical comparison and native-measurement feasibility. This is not exhaustive priority certification or empirical validation.
- Execution: static reading only; no project/upstream code, tests, model execution, training, inference, scoring, dataset/model download, GPU, Docker or paid service.

## Preserved v1/v2 evidence

The v1/v2 audits remain binding. They already locate R18 against linear/switched-system observability, regular-language path constraints, common invariant subspaces, predictive/right congruence, functional observers and direct state-coordinate ledgers. V3 does not relabel that reading as novelty. It asks the narrower repair question left by v2: if the exact common kernel is too small, what side-ledger width suffices for a declared nonzero discrepancy budget on a bounded same-update fiber?

The fixed DIACRITIC source inspection from v2 also remains binding: `XianyaoLi/DIACRITIC@08858b...`, with `_refine`, `GammaSolver.solve`, `gamma_J`, `Adapter`, `record`, `certify_env` and `certify`, is an actual environment-refinement/certification interface. It does not implement the R18 min--max side-ledger problem or provide a Delta prefix coverage contract.

## Switched-system balanced-truncation collision

Petreczky, Wisniewski and Leth, *Balanced truncation for linear switched systems*, arXiv:1302.0221v2, is a decisive nearby mathematical source. Its abstract separately states `L2/l2` approximation-error bounds and Gramian/singular-value interpretations; for strongly stable discrete-time linear switched systems it additionally defines “nice” controllability/observability Gramians. Equations (2)--(3) are the continuous-time common observability/controllability LMIs; equation (4) poses the target input-output error bound, which the Error bound theorem in Section 6 proves under the paper's balanced-Gramian assumptions. Sections 3--6 develop norms/Gramians, invariance, singular-value interpretation and the error proof. This is direct prior art for using common Gramians and truncated spectral directions to control switched input-output error, not for R18's exact fiber min--max formula.

Gosea et al., *Balanced truncation for linear switched systems*, arXiv:1712.02158, likewise uses mode-coupled Lyapunov equations/inequalities, Gramian-based balancing and error bounds. These sources differ in formal setup from R18's destructive-update fiber and side code, but they make any broad claim of novel switched-path spectral reduction untenable.

No author-maintained implementation for the Petreczky--Wisniewski--Leth procedure was verified in the bounded search. That absence is recorded rather than substituting an unverified third-party repository.

## Approximate-bisimulation collision

Girard, Pola and Tabuada, *Approximately bisimilar symbolic models for incrementally stable switched systems*, arXiv:0807.5022, constructs approximate symbolic abstractions under incremental stability, using common or multiple Lyapunov functions. Girard, *Low-Complexity Quantized Switching Controllers using Approximate Bisimulation*, arXiv:1209.4576, uses approximate bisimulation to reduce switching-controller complexity. These are strong neighboring sources for replacing exact behavioral equivalence by a quantified error relation. R18's exact formula is specialized to one destructive state fiber and a linear side ledger; it is not the first approximate behavioral abstraction.

The v2 regular-language observability source, Baştuğ et al., arXiv:1409.1444v2, and Petreczky/Bako/van Schuppen, arXiv:1103.1343, remain the closest sources for path-constrained observability and switched realization. Berger, Jungers and Wang, arXiv:2209.05320, remains relevant to common invariant-subspace computation. Petersen's robust-unobservability work remains relevant to parameter uncertainty. Together these sources cover most of the general mechanism.

## Empirical Gramian and actual interface

Christian Himpe's author-maintained `emgr` remains fixed at commit `79c4355b7f064130fbfb08db18c178f9e297a5dd`. `py/emgr.py` exposes `emgr(f,g,s,t,w,pr,nf,ut,us,xs,um,xm,dp)`; `w="o"` perturbs state coordinates, accumulates output trajectories and returns an empirical observability Gramian through the configured inner product. It is a real trajectory-Gramian baseline for estimating observable directions.

It does not enumerate R18's prefix-conditioned legal path tree, solve the robust Grassmann min--max objective, issue the bounded-fiber contract, or account for a recurrent side ledger. It is therefore a construction/control baseline, not evidence that R18's conditional theorem is false or novel.

## Mathematical distinction and collision decision

For each path, R18's `G_pi=Z_pi^T Z_pi` and its best path-specific rank-`r` tail are standard SVD/Eckart--Young--Mirsky objects. A common envelope `Gamma >= G_pi` is a common Gramian/LMI-style certificate. Optimizing one shared subspace against a maximum of pathwise residual norms belongs mathematically to a min--max/common-subspace optimization class; this bounded audit did not verify a primary source containing R18's exact operator-norm objective, so it is not cited as a term-by-term prior result. The two-path witness in the artifact is useful because it prevents the common-envelope eigenspace from being reported as the exact robust optimizer, but it does not turn the surrounding known ingredients into a new architecture.

The retained Delta-specific contribution is narrower: derive the coefficient fiber from the exact destructive update kernel, charge a side ledger in that coefficient space, and state the exact worst-case leakage and boundedness boundary. This is best classified as a theorem/debugging bridge with major neighboring-mechanism collision.

## Delta interface and same-information controls

Yang et al., *Parallelizing Linear Transformers with the Delta Rule over Sequence Length*, arXiv:2406.06484v6, gives the gated Delta recurrence. The fixed author implementation `fla-org/flash-linear-attention@a7880060012c862d58575ee23f613cafcd728d03`, `fla/layers/delta_net.py`, projects and applies a sigmoid scalar `beta` and passes it to the recurrent/chunk kernels. Thus ordinary write attenuation already exists and is mandatory when `beta<1` makes the post-decay erase factor invertible. Literal quotient loss disappears only if the decay and relevant complete-state map are also injective; singular decay can retain a kernel.

For `beta=1`, the memory-only erased-row statement assumes paired states share the same current exogenous features and the generated `k`, `v` and gate. If those quantities depend on the hidden paired state, the kernel must be taken from the complete ordered joint map. A direct ledger of the erased coefficients, a task-specific direct protected-coordinate ledger, and v2's exact common kernel are mandatory controls. R17's residual-scaled spectral certificate is a distinct same-information control for a single actual action. The R18 side ledger provides a stronger all-pairs-in-a-bounded-fiber capability and must pay for that distinction.

## Native measurement audit

The fixed public assets remain bAbI/ParlAI `a29567f7ce76992fd1f03c51ba9e3b155a37ea51`, lm-eval LAMBADA `d6de81643928d653435c431bae19945d41d32520`, RULER `c3f5e3b4f87f97e048793bb510a3a6b19a46bf3a` with pipeline `e8bbff677ca2c239640dc90f93310dcf32408c93`, BABILong as previously recorded, and LongMemEval `9e0b455f4ef0e2ab8f2e582289761153549043fc`.

Their native interfaces score endpoint tokens or answers. They do not expose controlled same-update pairs `x,x+K alpha`, path maps `Z_pi`, a declared pairwise fiber radius, the robust rank-`r` optimum, a prefix tree/radius coverage event, exact-real versus finite-bit side-ledger error, repeated-write code transport, side-ledger bits/metadata, or a matched-total-cost direct ledger. An instrumented paired-state intervention trace would be a new measurement object. None is created or claimed here.

## Audit decision

- Mathematics: conditionally supported for the declared affine tree, bounded fiber and exact side-code convention.
- Broad originality: **REJECTED_MAJOR_COLLISION** with switched-system observability, balanced truncation, approximate bisimulation and direct sufficient-coordinate storage. The exact Grassmann objective is classified as min--max/common-subspace mathematics, not claimed to have a verified term-by-term source collision in this bounded audit.
- Residual contribution: **PARTIAL_THEOREM_DELTA** — exact bounded-fiber min--max leakage, a safe but potentially conservative common-envelope certificate, and a precise unbounded-fiber boundary specialized to a destructive Delta state kernel.
- Architecture candidate: not admitted.
- Native mechanism measurement: absent.
- Experimental effect: unknown; no execution.

R18 closes after attempt 3/3 as useful conditional theory. Rank, radius, SDP objective, threshold and eigensolver variants are not new repairs.
