# Independent source review — R12 v3 Gram-component closure

Reviewer: `/root/r12_v3_source`  
Assignment: independent final-byte primary-source, author-interface, novelty/collision and native-measurement audit; read-only, no model/project execution.

## Exact artifact binding

- screen SHA256 `9b357b384bb6d142b936aaa7da86ce9ad023ab2a91e8de2b7c886c1cbe5ed6a9`
- math SHA256 `0df2d08785ba551cbe4ee3499550c24a1d3487fd297c6a760b2edc4eae99f16b`
- source SHA256 `e39180a3ee83b9764b16b36d24e3620fe36f88d541516d70afca5e4e7627a36a`

The explicit `V_0=col(Q)` definition resolves the sole formal cleanup from the first source pass. No mathematical defect remains under the stated finite-family and selector assumptions.

## Independent theorem check

For `P_i=k_i k_i^T` and nonzero `beta_i`, invariance under `F_i=I-beta_iP_i` is equivalent to invariance under `P_i`, giving the dichotomy `k_i in V` or `k_i perpendicular V`. Nonzero-inner-product paths force membership throughout seeded components; keys outside them are orthogonal to both `V_0` and every included component. Thus the displayed `V_star` is feasible and contained in every feasible carrier. The recurrence, full-span collapse, bridge counterexample and leakage bound are consistent.

Along a path,

\[
P_{i_0}\cdots P_{i_m}=
\left(\prod_{r=0}^{m-1} k_{i_r}^Tk_{i_{r+1}}\right)k_{i_0}k_{i_m}^T,
\]

which makes the common reducing-space collision explicit.

## Primary sources and author interface

1. **Delta rule.** Schlag et al., *Linear Transformers Are Secretly Fast Weight Programmers*, arXiv:2102.11174v3, Section 4, Eqs. 23–25 and Appendix A.1. Yang et al., *Parallelizing Linear Transformers with the Delta Rule over Sequence Length*, arXiv:2406.06484v6, Sections 2.2 and 3.1–3.2, Eqs. 3–4 and 10–11: <https://arxiv.org/html/2406.06484v6>.
2. **Pinned FLA interface.** `fla-org/flash-linear-attention@a7880060012c862d58575ee23f613cafcd728d03`: `fla/ops/delta_rule/naive.py` blob `d1f65a859a9cf74b98e71fbd9eb18c2165f9822a` implements residual write; `fla/layers/delta_net.py` blob `6f34aba3fa77367162d75b4937db46b1cd8007b2` generates q/k/v/beta and caches full state; `wy_fast.py` blob `672bf0ec84dc9aa9e7fcda6a1bd8cb4f123c5f78`, `chunk.py` blob `de56d867b01e7974d58bad306b8aba28b5d02830`, and `__init__.py` blob `8c8459c46fbc1de6dd3647a38d9870500d44aad2` expose ordinary recurrent/chunk/WY paths. They do not expose a predeclared finite dictionary or autonomous reduced-carrier API.
3. **Exact abstraction collision.** G. J. Pappas, *Bisimilar Linear Systems*, Automatica 39 (2003), Sections 5.1, 6.1 Theorem 16/Eqs. 18–21, Corollary 17/Eqs. 26–28, and Section 7 Theorem 21/Eqs. 39–41: <https://www.georgejpappas.org/wp-content/uploads/2024/04/AUT03.pdf>. This covers quotient fibers, invariant kernels and fixed-point construction.
4. **Simultaneous block collision.** Maehara and Murota, *A Numerical Algorithm for Block-Diagonal Decomposition of Matrix *-Algebras, Part II*, Theorem 1.1, Proposition 2.1, Eq. 2.4 and Proposition 2.2: <https://optimization-online.org/wp-content/uploads/2009/05/2292.pdf>. Nonzero generator couplings and transitive closure recover simultaneous algebra blocks; the R12 graph is the rank-one symmetric specialization.
5. **Finite-frame graph.** Chien and Waldron, SIAM J. Discrete Math. 30(2), 2016, Section 3 and Theorem 4.1, DOI `10.1137/15M1042140`, use the same non-orthogonality graph in finite-frame structure. This is not the carrier theorem but confirms the graph machinery is established.

No source using the exact seeded-Delta wording was found, but absence of that phrase is not originality evidence. The characterization follows immediately from known invariant/reducing-space theory plus rank-one projector products.

## Measurement/source boundary

Pinned bAbI/ParlAI, LAMBADA OpenAI, RULER, BABILong and LongMemEval assets measure endpoints only; none exposes the ex-ante key family, exact Gram graph, carrier rank, equal-`Y` paired states or bridge intervention. LongMemEval's pinned answer judge also requires `gpt-4o-2024-08-06`, outside the no-new-paid-service boundary. Using held-out future keys to construct the graph would leak information. A synthetic linear fixture could check identities but would not be a native empirical result.

## Verdict

- correctness: conditional PASS;
- provenance: general mechanism known; finite graph certificate is a narrow Delta-specific specialization;
- author implementation: dynamic keys/full state, not the assumed finite dictionary;
- novelty: not established; no first-method or architecture claim;
- executable object: exactly direct reduced coordinates `U^T S`, not an independent checksum/updater;
- measurement: native mechanism record absent; empirical effect untested;
- counting: candidate delta zero; attempt 3/3 exhausted and park.

Remaining limitations are the disclosed scientific assumptions: ex-ante complete family, dictionary/basis cost, exact edge convention, selector factorization, unseen bridges and native-measurement gap.

