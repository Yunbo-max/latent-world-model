# Source and measurement audit — irreversible query-shift refinement tax

Date: 2026-10-12  
Scope: primary-source and native-measurement audit for `STEP2_QUERY_SHIFT_SUCCESSIVE_REFINEMENT_2026-10-12.md`. This record establishes mechanism collision and measurement limits; it is not a broad originality guarantee, author-code verification, or experiment.

## 1. Primary sources read

1. William H. R. Equitz and Thomas M. Cover, **Successive Refinement of Information**, IEEE Transactions on Information Theory 37(2), 1991.  
   Author-hosted fixed PDF: <https://web.stanford.edu/class/ee376a/files/refinement.pdf>  
   Relevant locations: abstract; Section II definition; Theorem 2; Gaussian squared-error example; tree-code discussion. The paper defines two-stage descriptions, proves that zero rate loss is characterized by compatible rate--distortion-optimal reconstructions forming the Markov chain (X\to\widehat X_2\to\widehat X_1), and gives Gaussian squared-error as a positive case. This directly covers the general zero-tax criterion used here.

2. Albert No, Amir Ingber, and Tsachy Weissman, **Strong Successive Refinability and Rate-Distortion-Complexity Tradeoff**, arXiv:1506.03407v1, 2015.  
   Version URL: <https://arxiv.org/abs/1506.03407v1>  
   Relevant locations: introduction and Section II, especially the two-stage region allowing distinct distortion measures (d_1,d_2), the rate constraints, and the Markov/test-channel criterion. This blocks any novelty claim based merely on changing the distortion or query metric between stages.

3. Jayanth Nayak, Ertem Tuncel, Deniz Gündüz, and Elza Erkip, **Successive Refinement of Vector Sources Under Individual Distortion Criteria**, IEEE Transactions on Information Theory 56(4), 2010, DOI 10.1109/TIT.2010.2040858.  
   DOI record: <https://doi.org/10.1109/TIT.2010.2040858>  
   Read depth: title, bibliographic record and abstract-level claim only; the author PDF endpoint returned 403 in this audit. The verified abstract states that vector Gaussian sources under individual component squared-error criteria are not successively refinable everywhere. This is a direct collision for the general phenomenon, but no internal theorem number or unobserved formula from that paper is used here.

4. Victoria Kostina and Ertem Tuncel, **Successive Refinement of Abstract Sources**, IEEE Transactions on Information Theory 65(10), 2019; arXiv:1707.09567v2.  
   Version URL: <https://arxiv.org/abs/1707.09567v2>; author copy: <https://authors.library.caltech.edu/records/2w1rr-78143>  
   Relevant locations: Section II begins with two possibly different distortion measures; equations (10)--(17) define immutable layered messages, stage decoders, distortions and cumulative rates; equations (18)--(21) restate the Rimoldi region and its point-to-point lower bounds; Theorem 2, equations (26)--(33), gives the general parametric boundary. This is essentially the static i.i.d. object in the active artifact when both metrics are known at joint code design.

5. Chao Tian and Suhas N. Diggavi, **Multistage Successive Refinement for Wyner-Ziv Source Coding with Degraded Side Informations**, IEEE Transactions on Information Theory; arXiv version linked from <https://arxiv.org/abs/cs/0605001>.  
   Read depth and locations: arXiv full text, Section 2 Definition 1 and equations (4)--(7) for layered messages/decoders; Section 3 Theorem 1 and equations (11)--(14) for the multistage degraded-side-information region; Sections 4--5 for refinability and Gaussian cases. This is a neighboring stronger-information setting; the present theorem uses no decoder side information and therefore does not inherit those gains.

6. Shlezinger, Eldar and collaborators on task-based quantization, including **Deep Task-Based Quantization**, arXiv:1908.06845, and the primary task-based/indirect rate--distortion sources already pinned in `STEP2_QUERY_WEIGHTED_RATE_DISTORTION_SOURCE_AUDIT_2026-10-12.md`.  
   Version URL: <https://arxiv.org/abs/1908.06845>  
   Read depth: abstract/overview-level for arXiv:1908.06845 in this audit; the exact finite-resolution task-based formulas relied on here are instead pinned in the parent audit, including Shlezinger--Eldar--Rodrigues arXiv:1807.08305v1. These sources cover downstream-task distortion and learned task-aware quantization, but not by themselves the immutable-prefix penalty after an unannounced metric shift.

7. Ertem Tuncel, P. Koulgi, and K. Rose, **Rate--Distortion Approach to Databases: Storage and Content-Based Retrieval**, IEEE Transactions on Information Theory 50(6), 2004.  
   Author PDF: <https://intra.engr.ucr.edu/~ertem/Publications_files/it2004_06.pdf>; DOI: <https://doi.org/10.1109/TIT.2004.828068>  
   Relevant locations: abstract and Section I describe a scalable base search layer and a reconstruction enhancement layer with different layer distortions and query as decoder side information; Section II-C Definition 3 defines successive achievability; Theorems 1--3 give the query-dependent and full successive regions and a no-rate-loss test. This is the strongest semantic collision for “query-weighted fidelity plus append-only refinement.”

8. Emin Martinian, Gregory W. Wornell, and Ram Zamir, **Source Coding With Distortion Side Information At The Encoder**, arXiv:cs/0408062; later IEEE Transactions on Information Theory.  
   Version URL: <https://arxiv.org/abs/cs/0408062>  
   Read depth: abstract/metadata-level in this audit. The verified claim is that encoder knowledge of distortion side information changes the coding problem and can incur a large penalty; no internal formula is imported. It supports treating the reveal time of `W_2` as an information-timing variable, while also showing that the unknown-distortion theme is not new.

9. A. Mahmood and A. B. Wagner, **Lossy Compression with Universal Distortion**, arXiv:2110.07022v3; IEEE Transactions on Information Theory 69(4), 2023.  
   Version URL: <https://arxiv.org/abs/2110.07022v3>  
   Read depth: abstract/metadata-level in this audit. The verified scope is runtime-revealed distortion measures and universal redundancy; no internal theorem or equation is used. This is a required baseline for an online/compound residual, though it does not itself impose an immutable first-stage description plus append-only refinement.

Official-code search scope: on 2026-10-12 the audit checked the cited arXiv/DOI/author pages and bounded GitHub searches by exact paper title and author names. No official implementation repository for the classical information-theoretic theorem papers was identified among those inspected records. This remains unresolved beyond that bounded surface; it is not an exhaustive absence claim, and no third-party implementation is treated as author code. The benchmark repositories listed below are separately pinned as official release interfaces, not implementations of the theorem.

## 2. Exact mechanism mapping

| Artifact component | Closest established mechanism | Residual value |
|---|---|---|
| immutable first message plus appended second message | classical two-stage successive refinement | Delta timing/state interpretation only |
| different query metrics (W_1,W_2) | successive refinement with distinct distortion measures; vector individual-distortion coding | explicit query-Gram specialization |
| zero-tax Markov condition | Equitz--Cover and later refinability literature | a checkable warning that commutation alone is insufficient |
| orthogonal Gaussian witness | vector Gaussian/component distortion coding and scalar Gaussian RDF | short no-slack proof with exact (R_1)-bit tax for the displayed independent-coordinate case |
| fresh re-encoding comparator | point-to-point rate--distortion baseline | separates irreversibility cost from endpoint coding quality |
| query-weighted distortion | task-based/indirect quantization | connects the coding boundary to declared Delta queries |
| search/query base layer plus reconstruction enhancement | database rate--distortion with query side information | blocks semantic relabeling of layered query coding |
| `W_2` unknown until after `M_1` | distortion-side-information and universal-distortion coding | residual information-timing case; not solved merely by the static witness |

The main static scientific object is therefore covered. The new packet contribution is a transparent Delta-coordinate theorem/control and a matched-cost debugging target, not a new coding region or updater. The bounded residual is an online/compound formulation in which `W_2` is genuinely absent from the first-stage filtration, the state may evolve, and metadata/query descriptions are charged; that residual is not established as a candidate here.

## 3. Formula and condition audit

- The finite-block converse uses
  
  \[
  D_2\ge\sigma^2 2^{-2(\Delta+\epsilon_n)}
  \]
  
  without inserting an (o(1)) into the exponent. Vanishing terms belong only to asymptotic boundary/achievability statements.
- Independence gives (I(B^n;M_1)\le I(B^n;M_1\mid A^n)) because their difference is (I(A^n;B^n\mid M_1)\ge0).
- The exact tax conclusion assumes (0<D_1\le\sigma^2), a feasible first-stage code, and a first-stage rate on the point-to-point boundary. Rate or distortion slack can hedge information toward the future coordinate, exactly as the displayed (epsilon_n) term records.
- Zero tax at both point-to-point boundaries requires the ordering (R_{d_1}(D_1)\le R_{d_2}(D_2)) and compatible optimal test channels with (X\to\widehat X_2\to\widehat X_1). Mere shared eigenvectors, commuting query Gramians, nested subspaces, or trace monotonicity do not prove compatibility of active water-filling allocations.
- The orthogonal Gaussian lower bound is sharp: independently code (A) in the first message and (B) in the appended message. It is a witness, not a universal penalty for every source or metric path.
- If a fresh stage-2 encoder has the complete source history and the same final payload budget, its feasible set contains the concatenated progressive code. Thus progressive coding cannot claim lower ideal final distortion; any residual practical advantage must be in rewrite traffic, raw-history access, latency, work memory, or restricted computation.

## 4. Native measurement and matched-cost audit

This section extends the packet's exact earlier measurement record `research/delta-discovery-2026-10-08/sources/STEP2_NEW_NATIVE_MEASUREMENT_AUDIT_2026-10-12.md` (SHA256 `975e6dfcd8f879a25d77e2052872dbb8eced23a03c4fbb63933247ffdab3b3eb`), which pins paper versions, repositories, commits and native interfaces for WritePolicyBench and the packet's established memory/task assets. The additional repositories below were read without executing them. No inspected public benchmark natively exposes all of: a byte-identical immutable stage-1 snapshot; a stage-2 query/distortion revealed only afterward; equal final payload; adaptive metadata; raw-history archive/read traffic; cumulative rewrite traffic; encode/decode compute; and a common scorer.

| Public asset and exact release | Native interface/scorer read | Missing object |
|---|---|---|
| WritePolicyBench, arXiv:2602.02574; official `edgardcham/WritePolicyBench@9cfc1f4979a91ee41ccebd320839186c2933ad2f` | `writepolicybench/policy.py::WritePolicy.select(step, store)` chooses `WRITE/MERGE/EXPIRE/SKIP`; `writepolicybench/evaluator.py::run_policy_on_episode(...)` scores frozen `data/episodes/*.jsonl` streams with retained-set F1, utility per KB and write-only regret under its native byte model | no changing reconstruction metric, decoder, or immutable layered code; adaptive codecs, raw archive and full rewrite compute are not natively priced |
| AToKE-ME, arXiv:2312.05497; official `Arvid-pku/ATOKE@a1b42e34e4130507220307ced3d681fb8719831f` | `datasets/AToKe-ME.json`; README-defined historical/current by relative/explicit question scores HRS/HES/CRS/CES and paraphrase score | the JSON contains `requested_rewrite`, future evaluation prompts and gold aliases together; causal stage-1 use needs non-native field masking; no bit/code/metadata accounting |
| LongMemEval-V2, arXiv:2605.12493; official `xiaowu0162/LongMemEval-V2@2cc8c540bdb87fe6761629b585e727e1c4704520` | backends implement `memory_modules.memory.Memory.insert(trajectory)` and `query(query, query_image)`; `evaluation/harness.py` uses a fixed reader and the repository writes `aggregated_metrics.json`; leaderboard combines accuracy and query latency | backend state size, stage-1 snapshot immutability, insert/rebuild traffic and rewrite cost are not constrained |
| EvoMemBench, arXiv:2605.18421; official `DSAIL-Memory/EvoMemBench@aa4cea8fd936b76b2d3591d3ef897030617dc43a` | repository task suites cover in-/cross-episode knowledge and execution, each with its own native task scorer and launch path documented in task READMEs | heterogeneous harnesses have no single byte-accurate state, immutable snapshot, query-metric schedule or raw-archive/re-encoding ledger |

These assets cannot be spliced together and called one native benchmark because their data-generating processes and scorers differ. Static answer/retrieval tasks such as bAbI, BABILong, LAMBADA and RULER remain endpoint controls already documented elsewhere in the packet, but are not claimed as newly inspected or version-pinned by this audit. A lawful future derived mechanism audit would have to freeze and hash (Z_1) before revealing (W_2), allow only an appendage on the progressive path, run a fresh-code path at the same final payload, and report the resource vector

\[
(D_1,D_2,\text{persistent bits},\text{written bits},
\text{archive bits},\text{raw reads},\text{encode/decode cost}).
\]

That is a measurement specification, not an experiment executed here.

## 5. Required controls and hidden costs

Required same-information controls are: ideal fresh re-encoding from the same lawful source history; retained-state-only recoding when raw history is unavailable; standard layered/nested coding; a robust single code for a declared metric family; direct task-aware quotient/ledger coding; raw external key--value or replay access when equally charged; and simple no-update/last-(k)/merge policies for deployment-cost context.

Costs that cannot be hidden inside one “memory size” number include final persistent bits, cumulative writes, full-source archive and reads, basis/Gram/codebook metadata, framing and checksums, encoder/decoder parameters if instance-adaptive, stagewise compute and latency, scratch memory, garbage collection/write amplification, and query-law prediction state.

## 6. Source and measurement decision

The theorem is mathematically useful as a debugging boundary: current-metric optimal compression can consume all rate needed by a later orthogonal query, and append-only refinement then pays an exact tax in the displayed Gaussian case. But classical successive refinement and vector individual-distortion coding cover the central mechanism, while no native public scorer closes the matched-cost measurement gap. Retain as `theorem/control`, `candidate_delta=0`, empirical effect unknown. Reopen a method candidate only on evidence of a lawful prefix-causal mechanism with a strict matched-resource advantage over the listed standard controls.
