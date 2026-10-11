# R13 v3 source and collision audit — minimum erasure ledger

## Frozen atomic claim

For one causally known affine transition \(Z=AS+B\) and declared old readout \(Q^\top S+C_0\), the minimum width of a real-linear pre-transition side ledger permitting exact recovery is
\[
\ell_\star=\operatorname{rank}(Q^\top N),
\qquad \operatorname{col}(N)=\ker A.
\]
The bound is attained by an explicit SVD factorization. At exact rank-one Delta overwrite, an overlapping protected family needs exactly one \(d_v\)-vector, while an orthogonal family needs none. A declared spectral cut can bound inverse amplification by moving protected low-singular directions into a ledger. This is a conditional information/control theorem, not a semantic-validity rule or a new updater.

## 1. Primary sources and exact scope

| Work | Fixed locator and read depth | Material used | Boundary |
|---|---|---|---|
| Penrose, *A generalized inverse for matrices* (1955) | Proc. Cambridge Philosophical Society 51(3), DOI 10.1017/S0305004100030401; inherited primary read from R13 v1 | generalized inverse and consistent matrix factorization | does not establish Delta novelty or semantic protection |
| Eckart & Young, *The Approximation of One Matrix by Another of Lower Rank* (1936) | Psychometrika 1:211--218, DOI 10.1007/BF02288367; primary solution scope checked | best low-rank Frobenius approximation used for the side-budget tail | classical theorem; no R13 priority |
| Luenberger, *Observers for multivariable systems* (1966) | IEEE TAC 11(2), DOI 10.1109/TAC.1966.1098323; primary metadata/abstract and accessible opening discussion inherited from v1 | reduced and linear-functional state observation | strong mechanism-family collision |
| Roman & Bullock, *Design of minimal order stable observers for linear functions of the state via realization theory* (1975) | IEEE TAC 20(5):613--622, DOI 10.1109/TAC.1975.1101061; primary abstract/metadata checked | minimum-order observers for vector linear functions | broader dynamic problem, but directly covers the minimum-order objective |
| Darouach, *Existence and design of functional observers for linear systems* (2000) | IEEE TAC, DOI 10.1109/9.855556; primary metadata/abstract checked | functional-observer existence and construction | not the same one-step SVD formula; decisive conceptual collision |
| Moreno, *Simultaneous observation of linear systems: a state-space interpretation* (2005) | IEEE TAC, DOI 10.1109/TAC.2005.851447; primary formulation and conditions inherited from R13 v2 | common functional observation across several systems | governs hidden-mode extensions, not the revealed single-step theorem |
| Pappas, *Bisimilar Linear Systems* (2003) | Automatica 39(12):2035--2047, DOI 10.1016/j.automatica.2003.07.003; author PDF locator checked | quotient/equivalence view of retained behavior | general systems-theory comparator |
| MacKay et al., *Reversible Recurrent Neural Networks* (2018) | NeurIPS proceedings paper and author repository scope inherited from v1 | forgotten information requires retained side bits | architecture comparator; does not prove this linear minimum |
| Zhao et al., *Constrained Common Invariant Subspace and Its Application* (2024) | IEEE TAC 69(10):6821--6835, DOI 10.1109/TAC.2024.3378769; definitions, theorems, algorithm and reducibility application checked | common/constrained invariant subspaces and exact reduction | directly covers attempts to market the protected subspace itself as a new mechanism |
| Berger, Jungers & Wang, *Data-driven invariant subspace identification for black-box switched linear systems* | arXiv 2209.05320v1 / CDC 2022; Sec. II-A, Prop. 1 and Thm. 2 inspected | common invariant space, block triangularization, near-invariance leakage | approximate common-space learning is established |
| Rota & Strang, *A note on the joint spectral radius* (1960) | Indagationes Mathematicae 22:379--381; author-hosted PDF checked | arbitrary-switch product growth | repeated-mode blow-up is an elementary specialization |
| Blondel & Tsitsiklis, *The boundedness of all products of a pair of matrices is undecidable* (2000) | Systems & Control Letters 41(2):135--140, DOI 10.1016/S0167-6911(00)00049-9; primary theorem scope checked | general all-products boundedness/JSR hardness boundary | blocks a generic cheap switching-certificate claim |

The observer and invariant-subspace works cover the mechanism family, not necessarily the exact one-step formula \(\ell_\star=\operatorname{rank}(Q^\top N)\). No priority claim is made for that formula.

## 2. Delta source and author-code interface

The inherited pinned Delta sources remain:

- Schlag, Irie & Schmidhuber, ICML 2021 / PMLR 139, Sec. 4.2, equations (23)--(25), for the Delta update and query read;
- Yang et al., arXiv 2406.06484, for the ordered Delta recurrence and chunk/recurrent equivalence;
- Flash Linear Attention at fla-org/flash-linear-attention commit a7880060012c862d58575ee23f613cafcd728d03:
  - fla/ops/delta_rule/naive.py, function delta_rule_recurrence, computes the residual, scales by beta, applies the rank-one write, and reads \(q^\top S\);
  - fla/layers/delta_net.py, method DeltaNet.forward, produces \(q,k,v,\beta\) and exposes recurrent/cache state.

The implementation sees the realized key, gate, and value at the write. Hence v2's hidden mode is an explicit downstream interface restriction, not an inherent Delta limitation.

No inspected implementation exposes a protected-object oracle, minimum-erasure ledger, semantic-validity label, kernel certificate, or spectral-cut policy. Absence is not novelty evidence.

## 3. Decisive internal collision

At literal-main commit 7b1ccbcb2cfc4f1554c97aea4b87fe4d03d42f02:

- research/delta-discovery-2026-10-08/repairs/R18_PREFIX_CAUSAL_ROBUST_QUOTIENT.v2.md, Git blob 259bab3e5263484cec9e552a2278696c0df76772, already derives the minimum direct threatened-ledger width \(\operatorname{rank}(O_TP_tK_t)\) for a complete-state erased fiber under a prefix-declared future tree.
- Its source audit, Git blob de66eddb3d0fd771b76f07cdff3e289a16eeb3dd, adjudicates the direct ledger as attaining the same affine lower bound.
- R12's finite-key carrier is direct sufficient coordinates.
- R19's prefix branch-code result gives the corresponding zero-error side-code/confusion boundary beyond linear real-valued ledgers.

R13 v3 contributes a cleaner one-step SVD attainment, cross-column scalar lower bound, constrained spectral-cut tradeoff, and exact one-vector Delta-overwrite corollary. Those are useful specializations and repair v1's coarse \(p d_v\) ledger comparison. They are not a distinct method after R18/R12/R19.

## 4. Collision map

| R13 v3 object | Closest mechanism | Residual | Disposition |
|---|---|---|---|
| \(XA+KL^\top=Q^\top\) | generalized inverse / functional observer | explicit one-step side-ledger factorization | known algebraic family |
| \(\operatorname{rank}(Q^\top N)\) | minimum-order functional observation; R18 direct ledger | Delta specialization and cross-column accounting | theorem/debug control |
| unconstrained rank-budget tail | Eckart--Young | protected-kernel residual \(Q^\top P_{\ker A}\) | classical low-rank approximation |
| constrained spectral-cut hybrid | truncated SVD / regularized inverse plus side information | exact split with fixed high-singular decoder | known stability/state tradeoff |
| rank-one overwrite corollary | reversible side bits / direct syndrome | one \(d_v\)-vector on nonzero overlap | sharp Delta corollary, not updater |
| arbitrary-switch bounded transport | common invariant subspace / JSR | repeated rank-one Delta proof | elementary specialization |

## 5. Native measurement audit

The retained benchmark revisions are endpoint-only:

- bAbI / ParlAI a29567…: short-context exact-match QA; no persistent transition, kernel, ledger, or protected-object truth;
- LAMBADA / lm-eval d6de816…: 5,153-passage final-word endpoint; no declared write, mode, or protected target;
- RULER c3f5e3… with pipeline e8bbff…: NIAH, variable tracking, aggregation, and length degradation; no kernel/ledger label or mechanism attribution;
- BABILong 7a6efe…: delayed multi-fact QA under distractors; no state intervention or side-ledger ground truth;
- LongMemEval 9e0b455…: temporal/session/update answer endpoints; its pinned scorer path uses gpt-4o-2024-08-06 and is not executable under the current no-new-paid-service boundary.

These tasks can later falsify endpoint benefit of an implementation. They cannot identify \(\ell_\star\), certify a same-post-state lost quotient, prove semantic validity, or attribute gain to the ledger instead of extra state or replay. Internal SVD and matrix traces are theorem diagnostics, not native scientific scores. Empirical effect remains unknown.

## 6. Controls, costs, and decision

Strong same-information controls are the full protected-value ledger, identical optimal lost-coordinate ledger, revealed-mode v1 transport, full Delta/no compression, matched replay/checkpoint or external KV, R18 direct quotient, set-membership observation, and a Bayes conditional mean under the same lawful prior and observations.

Comparisons must charge retained bytes; \(L,K,X\) coefficient storage unless already available; factor precision; kernel/SVD setup and reuse horizon; pre-read, post-read and ledger multiplication; bandwidth, traffic, latency; transition/mode access; and calibration examples. A real-linear scalar lower bound cannot be promoted to an unconditional bit lower bound.

Search date: 2026-10-11. The audit reused full primary reads pinned by R13 v1/v2 and R18, and refreshed the minimum-order, common-invariant and JSR sources above. This is a bounded repair audit, not two saturated novelty rounds, and it supports mechanism collision rather than an exhaustive priority claim.

**Verdict:** source support is adequate for the scoped theorem after independent final-byte mathematical review. The residual is a useful Delta-specific minimum-erasure certificate. Originality, candidate admission, native mechanism measurement, and empirical benefit are not established. R13 attempt 3/3 should be exhausted and parked with candidate delta zero.
