# Independent source and novelty review — R10 v3

Reviewer: `/root/r10_sources`  
Math artifact SHA256: `45308be5fbe91a9faff92e08fe3acec7f976cca4c3959b59a92fdf4e674a5c47`  
Source audit SHA256: `056ce512aaf123fe66a3d95a71b869a8d7713bd0f5889a7538bf86ec881be04c`  
Decision: **PASS with major functional/theorem collision; candidate delta 0.**

The reviewer independently recomputed both hashes. An initial source review failed because two author identities were wrong; the source artifact was corrected and re-reviewed rather than inheriting a pass.

## Verified evidence

- Berger, Jungers, and Wang, arXiv:2209.05320v1, Proposition 1/equation (2), supports the common-invariant-subspace and simultaneous block-triangularization collision.
- Pontes Duff, Grundel, and Benner, arXiv:1806.00406v1, Theorems 2–3, supports the smallest common invariant hull containing injection ranges and the conditional Gramian-range statement.
- Baştuğ et al., arXiv:1409.1444v2, Lemma 3 and Claim 1, supports exact behavior preservation on a declared restricted switching language.
- Schulze and Unger, arXiv:1801.09445v1, covers envelope-system reduction for low-rank switching and conditional output/stability guarantees.
- Ohno, Zheng et al., Erbas et al., DAMP, and STEPQuant cover fixed-rate error feedback, state-space/graph QEF, recurrent residual memory, and recurrent-state quantization/allocation.
- Pinned static interfaces are reproducible at FLA `a788006...`, GatedDeltaNet `b53d6d3...`, and STEPQuant `61f24c9...`; the negative statements are limited to the inspected paths and no code was run.

The common-carrier criterion and minimal invariant hull are established objects. Delta-ordered leakage and the explicit noncommuting witness are useful specialized debug results, but do not establish a new updater, representation class, or matched-cost capability. Source/novelty status therefore supports attempt 3/3 exhausted and parking, not candidate admission.
