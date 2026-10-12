# Independent final-byte source and novelty review — compound query hedge v1

Reviewer: `/root/compound_query_hedge_final_source`  
Workflow: `rsi-simple@0.3.0-simple.9`  
Parent binding: `main@fd320bc4a51c9e41b4c8ceab488e8be28d3b1f2e`  
Artifact SHA256: `2a9f90ac4be9851c66bc96edef0ee3f54b2ef92c5baf334198c4e3db13c07494`  
Source audit: `research/delta-discovery-2026-10-08/sources/STEP2_COMPOUND_QUERY_HEDGE_SOURCE_AUDIT_2026-10-12.md`  
Verified source-audit SHA256: `067ae1e2d10657f4f6aab36814d0cd6100fcf915c2a0acb9ff6988ab39b89660`

Verdict: **PASS for classical theorem/control; candidate delta zero.**

Timo et al. directly match the causal cache-before-request and request-specific delivery structure. Their Lemma 3 equation (4) gives the single-user rate--distortion--cache region; Section III.A gives `[R_X(D)-C/L]^+` with `C/L` cached bits per independent source; Section III.B equations (6)--(7) and Lemma 4 extend the operational characterization to multivariate Gaussian squared error. Substituting `C=R`, `L=m`, delivery rate `Delta` and the scalar Gaussian RDF produces the active minimax formula exactly.

Mahmood--Wagner is correctly distinguished: its encoder receives the source and distortion at runtime before forming one message, not an immutable prefix before query reveal. The average-demand wording is bounded to the actual read depth: prior work blocks novelty of introducing the `p_j` objective, while equations (8)--(10) are labeled independently derived and were not formula-matched to the cited CISS paper. Author-code wording claims only that no code audit was performed, not that code is absent.

The source evidence therefore supports mechanism collision and `candidate_delta=0`; it does not establish broad originality, implementation equivalence or empirical behavior. No code or experiment was run.
