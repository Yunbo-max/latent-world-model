# R17 predictive quotient — primary-source, implementation, originality, and measurement audit

Date: 2026-10-10. Subject: `../repairs/R17_PREDICTIVE_QUOTIENT_OVERWRITE.v1.md`. Scope: bounded primary-source and interface reading, mathematical comparison, and native-measurement feasibility. No project/upstream code, tests, model execution, training, inference, scoring, dataset/model download, GPU work, or Docker was used.

## 1. Predictive fibers: direct semantic collision

Linzhe Zhang and Changming Xu, *What Can a Recurrent State Safely Forget?*, arXiv:2609.23366v1, 20 September 2026, full HTML: <https://arxiv.org/html/2609.23366v1>.

- Section 2 defines complete future behavior `Phi_infty`, predictive equivalence and the quotient/fibers. Definition 1 requires a semantics-preserving corrector to remain in each fiber. Theorem 2 derives the local quotient constraint and a rank/codimension bound.
- Section 2.1 Theorems 3–4 gives the finite/discrete versus predictive-continuum boundary and an approximate packing bound.
- Section 3.1, equation (1) and Theorem 6 defines a finite audit-bank predictive metric and a deterministic distortion certificate. Section 3.2 requires explicit generative reset/probe access for its PAC certificate; passive endpoint data do not automatically supply it.
- Section 4 names manuscript interfaces `experiments/run_all.py`, `run_mujoco_generative_pac.py`, `run_har_modern.py`, and `run_sequential_digits.py`. The arXiv page did not provide an author repository link, and the bounded audit found no trustworthy official repository pin; these manuscript filenames are not an execution receipt.

This paper already states the general semantic principle needed by R17: an exact corrector may delete only directions inside a predictive fiber. It does not mention Delta, instantiate `A=(I-kk^T)D`, derive `ker A={D^-1 k a^T}`, or connect that kernel to a fixed Delta suffix Gramian. There is also a semantic distinction: R17's `ker A subseteq ker O` says the old quotient is decodable from the overwritten state; Definition 1 in the predictive-fiber paper requires the corrector to act as identity on the predictive quotient. Recoverability is weaker unless the intended new write is subtracted/conditioned and the decoded old behavior is actually preserved. R17's formula is therefore a scoped algebraic specialization/control, not a new predictive-fiber mechanism.

## 2. Task-sufficient and rate–regret quotients

Joss Armstrong, *Task-Sufficient Contraction: Source Selection for Machine Information Interfaces*, arXiv:2610.08884v1, 6 October 2026: <https://arxiv.org/abs/2610.08884>.

- Section 3 equations (1)–(4) defines risk/regret and a regret-profile quotient. Propositions 1–3 give the coarsest pointwise regret-complete quotient and a Bayes-quotient boundary.
- Section 4 equations (7)–(10) and Theorem 1 show invariance of the finite-action one-step rate–regret curve after the task-sufficient contraction.
- The paper expressly treats a static/single-interface object rather than a recursively changing Delta state. No official author code was linked on the arXiv record inspected.

Mark Walsh, *Support sufficiency as action-sufficient compression: a single-cycle rate-regret formulation*, arXiv:2606.09858v1, 28 May 2026: <https://arxiv.org/abs/2606.09858>.

- Section 3 Proposition 1/equation (7) gives the policy-equivalence quotient. Section 7 equations (10)–(14) gives deterministic bounded-regret partitions. The actual rate–regret definitions are in Section 9 Definitions 9–10/equations (18)–(19), Proposition 4/equation (20), and the variational equation (22); the zero-regret endpoint is Section 10/equation (26).
- Section 14.5/equation (32) leaves recurrent/long-horizon conditional rate–regret as an open extension. This source does not by itself cover R17's recursive-state bridge.

These works directly cover the idea that only decision- or regret-relevant distinctions must be retained. They do not erase the need for R17 to declare a causal future-query family, show recursive closure, or pay for its interface. They also mean the quotient target itself cannot be claimed as a new Delta invention.

## 3. Classical linear observation quotients and recursive closure

George J. Pappas, *Bisimilar Linear Systems*, Automatica 39 (2003), DOI: <https://doi.org/10.1016/j.automatica.2003.07.003>.

- Section 5 Proposition 9/equation (14) gives the observation-kernel inclusion needed for output preservation.
- Section 6 Theorem 16/equation (19) gives a discrete-time bisimulation condition including invariance of the observation kernel modulo input reachability.
- Section 8.1 equations (47)–(48) constructs exact linear observation quotients.

Jeremy Rodgers, *Observable Quotients and Exact Projected Dynamics*, author-deposited preprint, DOI: <https://doi.org/10.5281/zenodo.21371251> (2026).

- Section 3 Proposition 3.2/equation (3.2) states functional descent iff constancy on fibers; Corollary 3.3/equation (3.3) gives the linear kernel-annihilation form.
- Section 5 Theorem 5.2 separates one-step factorization from semigroup descent via kernel invariance; Section 6 Theorem 6.4/equation (6.10) and Section 7 Proposition 7.7/equations (7.9)–(7.10) give projected-dynamics and finite-observability forms.

The latter is not peer reviewed and itself describes the ingredients as classical, so it is corroborating rather than decisive priority evidence. Together these sources make clear that kernel-compatible observation factorization and recursive quotient closure are established control ideas. R17's exact Delta kernel substitution remains a diagnostic corollary.

## 4. Conditional rate-distortion, information bottleneck, predictive distortion, and PSR

Le, Tan and Motani, *Second-Order Coding Rates for Conditional Rate-Distortion*, arXiv:1410.2687v1: <https://arxiv.org/html/1410.2687v1>.

- Section II Definition 1/equations (4)–(6) states the source with side information at both encoder and decoder.
- Definition 5/equations (11)–(14) defines `R(X;D|S)=min I(X;Y|S)` under expected distortion; equation (15) gives the first-order theorem.

R17's `B >= R_{Q|K}(delta)` is a direct finite-code/data-processing corollary. `B >= H(Q|K)` needs discrete exact reproduction; it must not be asserted for a general continuous quotient.

Tishby, Pereira and Bialek, *The Information Bottleneck Method*, arXiv:physics/0004057v1: <https://arxiv.org/abs/physics/0004057>. Section 2.1/equation (5) states the rate-distortion starting point; Section 3.2 equations (16)–(17) gives the information-bottleneck self-consistency equations. This is a general relevant-information baseline, not a Delta overwrite theorem.

Marzen and Crutchfield, *Predictive Rate-Distortion for Infinite-Order Markov Processes*, Journal of Statistical Physics 163 (2016), DOI: <https://doi.org/10.1007/s10955-016-1520-1>, arXiv precursor 1412.2859. Equation (5) defines a predictive rate-distortion objective, equation (6) uses divergence between conditional futures, and the first lemma/theorem reduce past compression to causal-state prediction. The authors' 2021 correction, DOI <https://doi.org/10.1007/s10955-021-02698-1>, withdraws the general operational sensor-achievability interpretation because the standard rate-distortion theorem does not apply universally; conditional-entropy distortion retains the communication/predictive-IB interpretation. Accordingly, this source is evidence for the full-future lossy-quotient objective, not support for R17's finite-code operational lower bound. That bound is independently the explicit cardinality/data-processing corollary supported by the conditional rate-distortion definition above.

Singh, James and Rudary, *Predictive State Representations: A New Theory for Modeling Dynamical Systems*, arXiv:1207.4167v1: <https://arxiv.org/abs/1207.4167>. Section 2/equation (1) forms the histories-by-future-tests system-dynamics matrix; Section 4 develops core tests and linear PSR updates. PSR targets all-future predictive sufficiency and is stronger/different from a finite declared future-query bank.

Inspected author PSRNN interface: `cmdowney/psrnn@fd13b60f1cb62f2aed00348fe839ed9358655c79`. `psrnn_cell_impl.py::PSRNNCell.call` forms the state-conditioned matrix from `W_FE_F,b_FE_F`, multiplies the input and normalizes; `two_stage_regression.py` provides `RFF_Projection`, `featurize`, `svd_projection`, and the two-stage ridge estimator; `ptb_word_lm.py` instantiates the cell. These interfaces implement predictive-state learning, not R17's overwrite certificate. No execution receipt is claimed.

## 5. Internal project collisions and residual

The packet already contains strong controls:

- `NOGO_CAP_02.md`: exact overwrite singularity and full-behavior finite-bit bound, with predictive quotient explicitly listed as an escape boundary;
- `R01_VALUE_SPAN_AND_CREDIT_QUOTIENT.v2.md`: exact quotient closure and observable-preserving lumping collision;
- `R10_EQUAL_BIT_TRANSPORTED_RESIDUAL.v1.md`: same-cardinality direct-code dominance and operator boundary;
- `R12_SUBSPACE_SYNDROME_READOUT.v1.md`: kernel containment and direct sufficient-coordinate dominance;
- `R13_DYNAMIC_COVECTOR_PROTECTION.v1.md`: `ker A subseteq ker Q^T`, exact-overwrite obstruction, functional-observer collision and direct-ledger control;
- `STEP2_OBSERVED_PREDICTIVE_TARGET.md`: decision-sufficient information and future-prediction target boundaries.

The bounded search did not find a primary source writing the exact composite formula `ker((I-kk^T)D) subseteq ker O` together with `D^-1k`, the frozen suffix Gramian, and the conditional quotient rate-distortion bound. This absence is not a field-wide originality claim. The defensible residual is an explicit ordinary-Delta diagnostic that joins already known components. The main mechanism, target and information bound have major collisions.

Originality disposition: **major component collision / retain scoped Delta corollary / no method-level admission**. Do not claim first, new, or complete recurrent rate-distortion theory. The exact composite specialization was not found in this bounded audit; both constituent theories are established.

## 6. Author interfaces and nearest implemented controls

No R17 implementation was produced. The closest inspected author-facing interfaces remain those already pinned in the packet:

- original Delta/Gated Delta/KDA/RWKV/PDN/GDN2/GKA/QED/SDM/DeltaProduct interfaces in `PRIMARY_NEW.md` and associated source audits;
- R12/R13 direct sufficient-coordinate and functional-observer controls, which are mathematical/reference interfaces rather than an R17 implementation;
- predictive-fiber manuscript script names above, without an official repository pin.
- PSRNN author commit/interface above, which provides a recursive predictive-state baseline but not an exact-overwrite implementation.

The author-code audit therefore does not support a claim that R17 is implemented, faster, or absent from all codebases. The same-information baseline is a direct sufficient-coordinate/quotient encoder followed by ordinary Delta on the remaining state.

## 7. Native measurement feasibility

Existing native assets expose behavioral endpoints but not R17's full internal object:

| Asset | Native object | R17 claim it may partly stress | Missing object |
|---|---|---|---|
| bAbI/ParlAI pin already recorded in `OBSERVED_PREDICTIVE_TARGET_SOURCE_AUDIT.md` | answer exact match over declared QA episodes | finite factual/query retention endpoint | counterfactual pre-overwrite pair, frozen suffix operator, quotient label, `G`, and same-information direct quotient |
| LAMBADA OpenAI variant already pinned in that audit | final-word log likelihood/accuracy/perplexity | long-context endpoint | exact Delta-erasure fiber and conditional quotient source |
| RULER pinned in prior measurement/source records | synthetic long-context retrieval/aggregation endpoints | broader finite query families | internal overwritten direction, full declared query law, quotient entropy/rate-distortion |
| LongMemEval pinned in prior records | session/turn evidence plus QA endpoint | update/retention behavior and evidence localization | ideal write/release label, counterfactual no-overwrite behavior, exact predictive quotient or code budget |

These endpoints can compare implemented systems later, but they cannot natively verify the kernel-containment theorem, identify semantic revision validity, or attribute gains to quotient coding rather than extra retrieval/state. Predictive-fiber Section 3 provides a purpose-built generative audit protocol, yet it assumes conditional reset/probe access and is not one of the project's established native Delta benchmarks. No native internal scorer, affordable matched-cost implementation object, or empirical result is claimed.

## 8. Final source decision

- Mathematics/source relation: the exact Delta kernel calculation is a correct specialization of predictive fibers, linear factorization/functional observers, observability Gramians and conditional rate distortion.
- Contribution difference: the explicit `D^-1k`/post-decay `k` convention and sharp future-query witness are useful debugging controls; no distinct updater or source of causal evidence remains.
- Measurement: endpoint feasibility only; the internal quotient certificate remains a measurement gap.
- Empirical status: unknown; no execution.
- Candidate delta: zero; park after attempt 1.

Reopen only if a causal prefix-only interface identifies a stable recursively closed quotient, certifies it below the matched total cost of direct sufficient-coordinate storage, and yields a native measurable prediction not already implied by predictive fibers/task sufficiency/rate distortion.
