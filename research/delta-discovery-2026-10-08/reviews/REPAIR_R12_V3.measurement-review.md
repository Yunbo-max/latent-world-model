# Independent measurement review — R12 v3 Gram-component closure

Reviewer: `/root/r12_v3_measurement`  
Mode: independent native-measurement, information-parity and total-cost audit; no code, model, benchmark, scorer, training, inference, dataset download or experiment executed.

## Reviewed exact bytes

- screen `repairs/R12_REPAIR_LINE_SCREEN.v3.md`: SHA256 `9b357b384bb6d142b936aaa7da86ce9ad023ab2a91e8de2b7c886c1cbe5ed6a9`
- math `repairs/R12_GRAM_COMPONENT_CLOSURE.v3.md`: SHA256 `0df2d08785ba551cbe4ee3499550c24a1d3487fd297c6a760b2edc4eae99f16b`
- source `sources/R12_V3_GRAM_COMPONENT_SOURCE_AUDIT.md`: SHA256 `e39180a3ee83b9764b16b36d24e3620fe36f88d541516d70afca5e4e7627a36a`

## Verdict

**PASS** for the stated mathematical measurement gap and conditional endpoint falsifiability; **BLOCK** native mechanism identification, matched-cost advantage, empirical benefit and candidate admission. Empirical status is unknown, not failed or solved.

The graph theorem and `m_star=rank[Q,K_R]` are directly checkable on an externally declared linear key family. That is theorem verification, not a native language-task outcome. Existing tasks can later falsify endpoint consequences of a lawful implementation, but none exposes the internal objects needed to attribute an effect to Gram-component closure.

## Native claim map

| claim | native status |
|---|---|
| seeded components evaluate v2's least carrier | exact linear-algebra check only |
| reduced recurrence preserves declared protected readout | endpoint accuracy can falsify an implementation, not identify the mechanism |
| bridge key makes old discarded state necessary | mathematical counterexample; no native bridge-loss label |
| proper carrier yields practical advantage | requires total-cost comparison with identical `U^T S` and full Delta/WY |
| graph distinguishes valid revision from forgetting | false: geometry contains no semantic-validity signal |
| thresholded graph gives useful approximation | unestablished; needs a separate accumulated-leakage protocol |

## Fixed native assets and lawful scope

The review reuses already inspected fixed revisions; it does not claim new execution or qualification.

- **bAbI/ParlAI** `facebookresearch/ParlAI@a29567f7ce76992fd1f03c51ba9e3b155a37ea51`: native exact-match can compare short endpoint answers, but the adapter resets each question and exposes no persistent keys, graph, carrier or bridge loss.
- **LAMBADA OpenAI variant** at lm-evaluation-harness `d6de81643928d653435c431bae19945d41d32520`, 5,153 passages: detects broad language damage only; each item is a fresh passage with no prescribed edit/key family.
- **RULER** official `c3f5e3b4f87f97e048793bb510a3a6b19a46bf3a`, retained pipeline `e8bbff677ca2c239640dc90f93310dcf32408c93`: long-range endpoint degradation only. The retained grid is 39,000 generations and about 1.64B input-token positions per arm; it exposes none of the internal closure objects.
- **BABILong** `booydar/babilong@7a6efee29f5cac03c3c410e6799c80fd2ffe3610`: delayed QA under distractors only. At 32K, all 20 tasks require about 64M/640M input positions per arm for 100/1,000 samples; no internal graph or carrier labels.
- **LongMemEval** `xiaowu0162/LongMemEval@9e0b455f4ef0e2ab8f2e582289761153549043fc`, 500 questions: update/temporal QA is the closest endpoint proxy, not a mechanism record. Retained estimates are about 57.5M positions for S or 750M for M per arm plus 500 judge calls. The pinned QA path requires `gpt-4o-2024-08-06`, so it is not execution-ready under the no-new-paid-service boundary and no substitute judge is authorized.

## Future-information boundary

The complete family must be structural and declared before compression. Building the graph or basis from held-out/test-suffix keys leaks future information. An observed development dictionary certifies only that subfamily unless future membership is independently guaranteed. Every control must receive the same dictionary, queries, key indices, gates, values, precision and future-family information. Exact zero edges are discontinuous; thresholding creates a different approximate claim.

## Same-information controls

1. Direct orthonormal `Y=U^T S` on the identical `V_star`—algebraically the same state and update and therefore decisive.
2. Full Delta/WY with the same sequence and precision.
3. No compression.
4. Fixed blocks/slots or sparse routing with the same dictionary and total state budget.
5. Measured projection/truncation when exact edges are relaxed.

A redundant `K_R^T S` ledger stores `|R|d_v` values and updates from a Gram column; it offers no rank-revealed advantage over `U^T S`.

## Total-cost obligations

For `d=d_k`, `p=d_v`, `n=|K|`, `m=m_star`, and `q` protected columns, charge:

- dictionary `nd`; seed products up to `O(ndq)`;
- dense Gram `O(n^2d)` work and `O(n^2)` storage, or certified sparse topology/weights and `O(n+|E|)` components;
- QR/SVD, rank tolerance, basis `dm`, decoder `mq`, cached coordinates up to `nm`;
- setup amortization over a declared horizon;
- online `O(mp)` only with supplied identity/cached coordinate, otherwise add `O(dm)` projection and lookup;
- key/value/gate generator, metadata, traffic, precision, quantization and certification.

Direct `U^T S` has exactly the same `mp` recurrent state, basis, coordinates, decoder and update cost, so R12 v3 establishes no matched-cost advantage.

## Final disposition

- theorem measurability: PASS under the declared family;
- native endpoint falsifiability: conditional PASS after lawful implementation with unchanged native scorer;
- mechanism attribution / semantic validity / total-cost advantage: blocked;
- empirical effect: unknown;
- candidate admission: NO; `candidate_delta=0`;
- R12 attempt 3/3: exhausted and park.

Reopen only with a lawful ex-ante structured family, a same-information total-cost advantage over direct coordinates and Delta/WY, and a native record distinguishing closure from generic endpoint quality.

