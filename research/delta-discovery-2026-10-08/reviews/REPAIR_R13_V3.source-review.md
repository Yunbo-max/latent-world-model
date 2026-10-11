# R13 v3 independent final-byte source and mechanism review

- Reviewer: /root/r13_v3_source
- Assignment: primary-source scope, author-code interface, internal collision and benchmark-revision audit
- Math artifact SHA256: 17b8dc6e2ac819957347ed4cd617cda22bf42ac8b9b9c0439fbf774adcb2b75d
- Source audit SHA256: 6d3cb8b0692fa5d13a207dc5368d2ec7342289b2439dd4a8a5b9c01899e7a787
- Repair screen SHA256: 4ea68df206d2f415a6474a3f2741d372f5c1fb209343b46ff71e863bc96daae8
- Verdict: **PASS with no blocking source or mechanism-scope error**

The reviewer independently recomputed all three hashes and checked the theorem/scope interface, primary locators, Delta author implementation, internal R18/R12/R19 collisions and retained benchmark revisions.

The Penrose, Eckart--Young, Luenberger, Roman--Bullock, Darouach, Moreno, Pappas, Zhao et al., Berger--Jungers--Wang, Rota--Strang and Blondel--Tsitsiklis locators and uses remain within their actual scope. The audit does not claim that those works state the exact one-step R13 formula; they establish the surrounding generalized-inverse, observer, quotient, common-invariant and switching mechanism families.

The pinned Delta paper and Flash Linear Attention commit support the residual, gate, rank-one write and query-read interface. The implementation internally computes \(q,k,v,\beta\) and exposes recurrent/cache state; the audit correctly treats hidden mode as an imposed downstream interface restriction rather than an inherent Delta limitation.

At literal-main 7b1ccbcb2cfc4f1554c97aea4b87fe4d03d42f02, R18 Sec. 5 already gives the complete-state erased-fiber direct-ledger rank \(\operatorname{rank}(O_TP_tK_t)\), of which R13 is a one-step specialization. R12 sufficient coordinates and R19 zero-error side coding are also correctly presented as broader internal collisions.

The inherited benchmark pins are consistent: ParlAI a29567f7ce76992fd1f03c51ba9e3b155a37ea51; lm-eval d6de81643928d653435c431bae19945d41d32520; RULER c3f5e3b4f87f97e048793bb510a3a6b19a46bf3a and pipeline e8bbff677ca2c239640dc90f93310dcf32408c93; BABILong 7a6efee29f5cac03c3c410e6799c80fd2ffe3610; LongMemEval 9e0b455f4ef0e2ab8f2e582289761153549043fc.

No blocking citation, scope, collision, or spectral-cut error remains. Candidate delta zero, terminal park and empirical-unknown status are source-supported; originality and empirical benefit are not.
