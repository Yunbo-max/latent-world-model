# Source audit — compound query hedge before demand reveal

Date: 2026-10-12  
Scope: primary-source novelty and formula audit for `STEP2_COMPOUND_QUERY_HEDGE_2026-10-12.md`. This supports a mechanism-collision decision, not a broad firstness guarantee or experiment.

## 1. Decisive primary source

Roy Timo, Shirin Saeedi Bidokhti, Michèle Wigger and Bernhard C. Geiger, **A Rate-Distortion Approach to Caching**, IEEE Transactions on Information Theory 64(3), 2018; arXiv:1610.07304.  
Fixed sources: <https://arxiv.org/abs/1610.07304>; journal-author PDF <https://perso.telecom-paristech.fr/wigger/Timo-TIT2018.pdf>.

Full-formula read depth:

- Section I.B and Figure 1: a cache phase occurs before the user request, followed by a request-specific delivery phase.
- Section II.A, code definition: cache encoder `phi_c^(n): X^n -> M_c^(n)`; one delivery encoder `phi_l^(n)` and decoder `varphi_l^(n)` for each possible request; the user chooses the request only after the cache message is placed.
- Lemma 3, equation (4):
  `R(D,C)=min_{U:I(X;U)<=C} max_l R_{X_l|U}(D_l)` for the worst-demand single-user problem.
- Section III.A, identical independent sources: `R(D,C)=[R_X(D)-C/L]^+`, and the stated optimal policy compresses each source to its RD limit, caches `C/L` bits from each, then transmits the remainder.
- Section III.B, equations (6)--(7) and Lemma 4: multivariate Gaussian counterpart under squared error.
- The paper explicitly distinguishes its arbitrary/worst-demand model from Wang--Lim--Gastpar's iid-demand model and notes prior Gaussian average-demand work.

Collision: set cache capacity `C=R`, delivery rate `R(D,C)=Delta`, use `L=m` identical independent scalar Gaussians, and invert `R_X(D)=0.5 log2(sigma^2/D)`. This yields exactly
`D=sigma^2 2^{-2(Delta+R/m)}`.
The active minimax theorem is therefore a transparent specialization of a published operational region. Correlated-source and Gaussian extensions are also already inside that framework.

## 2. Average-demand and layered Gaussian neighbors

Timo et al. identify G. J. O. 't Veld and M. C. Gastpar, **Caching Gaussians: Minimizing Total Correlation on the Gray-Wyner Network**, CISS 2016, pp. 478--483, as studying the Gaussian setup under an average-performance criterion with demand probabilities. Read depth in this audit: bibliographic record and the explicit characterization in Timo et al.; the full CISS formulas were not independently retrieved. This is sufficient to block a novelty claim based only on introducing `p_j`, but not to attribute equation (10) verbatim to that paper.

Qianqian Yang and Deniz Gündüz, **Centralized Coded Caching for Heterogeneous Lossy Requests**, arXiv:1604.08178v1, 2016. Fixed source: <https://arxiv.org/abs/1604.08178v1>. Read depth: full arXiv HTML/abstract and stated problem/results. It uses independent Gaussian files, requests revealed only after placement, heterogeneous distortions, and layered caching based on Gaussian successive refinability. It is a direct mechanism neighbor, although its multi-user multicast setting is broader than the single-user theorem here.

Chien-Yi Wang, Sung Hoon Lim and Michael Gastpar, **Information-Theoretic Caching: Sequential Coding for Computing**, IEEE Transactions on Information Theory 62(11), 2016; arXiv:1504.00553. Fixed source: <https://arxiv.org/abs/1504.00553>. Read depth: abstract and Timo et al.'s comparison. It models partial data delivered before random requests and gives a single-letter single-user characterization. Its iid symbol-request model is not identical to the whole-file worst-demand Gaussian witness, but it blocks a broad claim that query-after-prefix sequential coding is new.

## 3. Universal/runtime distortion is not the residual

Asif Mahmood and Aaron B. Wagner, **Lossy Compression with Universal Distortion**, arXiv:2110.07022v3, 2022-10-04. Fixed source: <https://arxiv.org/abs/2110.07022v3>. Full-formula read depth: problem definitions and main theorems in the arXiv HTML/PDF.

Their universal encoder receives the source block and distortion measure together at runtime and forms one binary message; the decoder may not know the distortion unless it is conveyed. Their Theorem 1 gives vanishing minimax operational redundancy for generalized universal distortion over finite alphabets, and subsequent results quantify bounded-class and pointwise redundancy. This does not supply an immutable prefix formed before the future distortion/query is revealed. It is an important control for runtime metric adaptation, not the same information pattern.

## 4. Relationship to the parent theorem

Classical successive refinement remains the right neighbor when both layer objectives are known at joint design. The active object instead withholds the demand from the first encoder and allows a demand-specific delivery message. That temporal change is real, but rate--distortion caching already formalizes it. The new derivation does not repair its way around the prior work; it identifies the exact classical bucket.

## 5. Author implementation status

No author implementation was needed to verify the information-theoretic formulas, and no code was executed. No released code audit is claimed for Timo et al., 't Veld--Gastpar, Yang--Gündüz, Wang--Lim--Gastpar, or Mahmood--Wagner. The active contribution decision rests on paper-level operational regions, not implementation behavior.

## 6. Novelty and source verdict

- Mathematical correctness: the independent-Gaussian converse and allocation are supported and independently derivable.
- Functional distinctness: failed. The worst-demand object and its exact equal-allocation solution are already covered by lossy single-user caching; the Bayesian extension is also a known caching direction.
- Delta-specific residual: only interpretation, resource ledger, and a possible future structured restriction. No new updater, code family, or rate region has been shown.
- Classification: `classical theorem/control`, `candidate_delta=0`, empirical effect unknown.

No claim of firstness, broad originality, or empirical advantage is supported.
