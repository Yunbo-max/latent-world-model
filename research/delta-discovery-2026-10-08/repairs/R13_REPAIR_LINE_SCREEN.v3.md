# R13 repair-line screen v3 — bounded transport with a minimal erasure ledger

## Lineage and bounded attempt

- Immutable parents: R13_DYNAMIC_COVECTOR_PROTECTION.v1.md and R13_ROBUST_COMMON_COVECTOR.v2.md, with their counterexamples and exact-byte reviews.
- Substantive attempt: **3 of at most 3**.
- v1 established exact covector transport through one known realized affine step and showed singular overwrite and near-singular conditioning.
- v2 changed the information set to a hidden transition family and proved a common-decoder identifiability obstruction.
- Remaining repairable defect: v1 compared transport mainly with retaining the whole protected value. That overpays when the post-state still contains most protected directions.

## Failure type and patch

Failure type: **target/construction mismatch plus hidden cost**.

The patch returns to the ordinary Delta interface where the realized step is causally known. For a declared protected family \(Q\), it decomposes the old readout into:

1. the component recoverable from the post-state; and
2. the smallest linear side ledger required for the erased kernel, or for a declared low-singular subspace excluded by a stability threshold.

The exact one-step coefficient problem is
\[
XA+KL^\top=Q^\top,
\]
where \(L^\top S\) is retained before the write. Its minimum exact ledger width, an unconstrained rank-budget tail, and a constrained spectral-cut tradeoff are derived without pretending that regularization creates information.

## Alternatives screened

| Patch | Real mathematical delta | Decision |
|---|---|---|
| Minimal erased-quotient ledger | exact lower bound \(\ell_\star=\operatorname{rank}(Q^\top P_{\ker A})\), attaining construction, and tail formula | selected as theorem/debug repair |
| Arbitrary-switch bounded covector theorem | useful no-go for repeated partial Delta modes, but elementary common fixed-subspace specialization | retain as failure boundary |
| Finite path language or automaton mode | does not remove same-information ambiguity; revealing the path label reduces to v1 | rejected as rescue |
| Learned mode posterior or validity gate | changes the information set and still needs external validity evidence | baseline only |
| Decoder bank or side code | reduces to common observers or R19 confusion coding | mechanism collision |
| Modify the write to protect \(Q\) | projection, OGD, OWM, GEM, and protected-edit families | different known construction |

## Preserved counterexamples

- v1 exact-overwrite impossibility remains when no side information is retained.
- v2's invertible hidden-mode pair remains impossible for a mode-blind decoder; v3 assumes the realized step is known and does not erase that counterexample.
- A small coefficient residual has no semantic-error implication without a certified state norm.
- Near overwrite, an exact no-ledger decoder amplifies noise by the reciprocal retained singular value.
- Finiteness or a regular path language alone does not identify the realized mode or the protected fact's validity.
- A spectral-cut tail based on \(G_\tau\) is valid only when the cut decoder is fixed or low-singular post-state directions are excluded. It is not the unconstrained optimum.

## Cost and controls

The ledger carries \(\ell d_v\) scalars. Unless regenerated from already available metadata, a matched-cost comparison must also charge \(d_k\ell\) coefficients for \(L\), \(p\ell\) for \(K\), \(pd_k\) for \(X\), offsets and precision; kernel/SVD setup amortization; the pre-read \(L^\top S\); the post-read \(XZ\); the ledger term \(KH\); bandwidth, traffic, latency, and reuse horizon.

Same-information controls include the identical optimal lost-coordinate ledger, full protected-value ledger, revealed-mode v1 transport, full Delta/no compression, matched replay/checkpoint or external KV, R18 direct quotient, set-membership observation, and the Bayes conditional mean.

## Expected disposition

The patch can reduce extra per-item state from \(p d_v\) to \(\ell_\star d_v\) for a fixed protected family while retaining the ordinary post-state. That genuinely repairs v1's coarse ledger comparison. But generalized inverses, reduced/functional observers, low-rank approximation, reversible side information, and packet-internal R18/R12/R19 cover the mechanism.

Attempt 3 is terminal. Subject to final-byte review, R13 is exhausted and parked with candidate delta zero and empirical effect unknown. No model code, test, training, inference, scoring, download, or experiment was authorized or performed.
