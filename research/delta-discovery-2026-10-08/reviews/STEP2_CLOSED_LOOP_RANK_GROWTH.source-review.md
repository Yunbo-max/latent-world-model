# Independent source and measurement review: closed-loop Delta rank growth

Reviewer: `/root/full_loop_rank_source_review`  
Assignment: independent review of primary-paper claims, author-code identities/interfaces, biased/unbiased distinctions, native-measurement mapping and disposition.  
Artifact: `research/delta-discovery-2026-10-08/sources/CLOSED_LOOP_RANK_GROWTH_SOURCE_AUDIT.md`  
Final reviewed SHA256: `d3317f0423c5e3a29febd81cb8df900c38d25d60e18c39a47121ba736667d358`  
Mode: source reading only; no project/upstream execution, tests, training, inference, scoring, downloads, GPU or Docker.

## Review history

The first exact-byte review of SHA256 `21777cb270afd2418709907d4faba8e6ad0e5d2f896115354990ea8b1dcd75a3` returned **REVISE** for two provenance/measurement overgeneralizations:

1. a combined CITB/TRACE/SEAL row incorrectly made the 2080Ti/paid-grader mismatch appear to cover CITB, whose primary setup includes T5-small and native scripts;
2. a combined LongMemEval v1/v2 row obscured that v1 supplies 500 QA/evidence-session objects while v2 supplies 451 Insert/Query and accuracy--latency/LAFS objects.

The writer split both rows and explicitly bound inherited benchmark numeric/interface claims to the already reviewed projected-credit and measurement-feasibility packets.

## Final decision

**ACCEPT** on final SHA256 `d3317f0423c5e3a29febd81cb8df900c38d25d60e18c39a47121ba736667d358`.

The reviewer confirmed:

- NoBackTrack/UORO are randomized unbiased reductions rather than exact deterministic fixed-rank sensitivities;
- KF-RTRL is an unbiased Kronecker approximation, OK is minimum-variance only inside its stated unbiased Kronecker-sum class, and SnAp is biased reachability sparsification;
- e-prop's eligibility/learning-signal factorization is not an exact fixed-rank full-sensitivity claim;
- UORO, OK and e-prop author-code identities/pins are not fabricated, while missing KF-RTRL/SnAp author implementations remain explicit gaps;
- no public native asset in the audited packet exposes internal tangent, costate, matrix rank, truncation error or ideal edit as native ground truth;
- the Delta-specific tight construction is therefore a useful formal control with major component collision, not a method candidate or originality claim.

Counts remain unchanged.
