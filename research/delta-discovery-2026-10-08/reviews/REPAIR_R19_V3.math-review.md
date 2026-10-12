# R19 v3 independent mathematics review

- Reviewer identity: `/root/capacity_candidate`
- Assignment: independently rederive the final finite-field theorem and check dimensions, graph structure, chromatic number, nonlinear/randomized zero-error lower bounds, affine-subspace restriction, counterexamples, costs, and terminal disposition.
- Artifact SHA256: `ea932cd7350806d52d66f2fd243f9d9e23a849dabfae438ce10183e34c40fc49`
- Screen SHA256: `7affc2c5f17aaef3f7a5a46b0739b9725fbadefe8fd2d06870465400fa8494ee`
- Verdict: **PASS; no blocking correction**

## Reasoning

The dimensions are consistent. For stacked `B`, rank-nullity gives

`r = dim ker(A) - dim(ker(A) intersect ker(B)) = rank([A;B]) - rank(A)`.

A row-space complement of `row(A)` inside `row([A;B])` has exactly `r` rows. Thus `C` satisfies `row([A;C])=row([A;B])`, `ker(A) intersect ker(C)=H`, and each branch factors as `B_m=D_m A+E_m C`; fixed affine offsets are restored by the decoder.

Inside an `Az` fiber, differences lie in `ker(A)`. Two states are nonadjacent exactly when their difference lies in `H`; the independent parts are therefore `H`-cosets and all distinct parts are completely joined. There are `q^r` parts. A complement of `H` in `ker(A)` gives a clique of size `q^r`, while `Cz` gives a coloring with `q^r` colors. Hence `chi(G)=q^r`, the minimum alphabet is `q^r`, and fixed binary width is `ceil(r log_2 q)`.

The clique proof is encoder-agnostic. Private zero-error randomness requires disjoint message supports on adjacent states; shared exact zero-error randomness induces a proper deterministic coloring for almost every supported seed. The same lower bound follows. Average error, variable length, noisy/approximate release, block coding and repeated writes are correctly excluded.

For an affine reachable set `z0+im(U)`, `U` is read as a full-column-rank basis of the direction space and the replacement `A -> AU`, `B -> BU` is correct. Arbitrary supports and state-dependent or hidden labels correctly return to the v2 graph and feasibility conditions.

The witnesses and limiting cases are consistent. Dense basis metadata, `O(rn)` encoding, decoders, labels and finite-field representation remain charged. A row-reduced direct signature and R18 joint-row ledger require exactly the same `r` symbols, so there is no matched-information advantage or repeated-write updater.

Disposition: exact finite-field one-shot zero-error terminal theorem/debug control; attempt 3/3 exhausted, `candidate_delta=0`, empirical effect unknown. No project code, tests or experiments were performed.
