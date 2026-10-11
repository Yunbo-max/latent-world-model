# R11 attempt-3 repair screen

Lineage preserved byte-for-byte:

- `repairs/R11_ORDER_GAP_COMPRESSION.v1.md`, SHA256 `38d5ba6cb4e897b602b9897c940468cdaab0b603f5e3d9055b3f98dc52e1929b`;
- `repairs/R11_FACTOR_CORE_ORDER_GAP.v2.md`, SHA256 `452b5753a732a6b9d868ecf2d3647a9d6efcc5f8c0c8fd6932b58342847d0b63`;
- all parent counterexamples, source audits, and reviews.

Attempt 3 screens the only remaining mathematical/cost defect in v2: the statement that a factored correction overlay must keep growing merely because later residuals read it. That is too broad. Under a common frozen-feature pure-Delta path, a single low-rank overlay is closed under the left transition and never increases rank. The legitimate unresolved question is instead whether repeated new semantic corrections admit a fixed-rank exact carrier.

Chosen operations: F03 sufficient recurrent state, F04 ordered low-rank products, G04 variation of constants, C04 error decomposition, H06 sharp counterexample. The patch must:

1. derive exact lazy overlay propagation and its actual state/read cost;
2. retain the dependence of a new order gap on an already corrected pre-state;
3. prove a sharp repeated-injection rank/query-capacity boundary;
4. separate passive propagation, new injections, recompression error, selector information, and endogenous-feature effects;
5. compare against exact chronological Delta/WY, the identical overlay engine with the same selector, direct same-information action prediction, and generic low-rank maintenance.

Anything that merely renames the overlay, changes a rank threshold, or reuses the 2x2 solver is not a substantive delta. No code, model, test, scorer, or benchmark may be executed in this Web mathematics stage.
