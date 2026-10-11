# Independent adversarial and hidden-cost review — R12 v3

Reviewer: `/root/r12_v3_adversarial`  
Mode: independent read-only counterexample, hidden-assumption, numerical and matched-cost review; no artifact editing and no model/project execution.

## Reviewed exact bytes

- math SHA256 `0df2d08785ba551cbe4ee3499550c24a1d3487fd297c6a760b2edc4eae99f16b`
- screen SHA256 `9b357b384bb6d142b936aaa7da86ce9ad023ab2a91e8de2b7c886c1cbe5ed6a9`
- source SHA256 `e39180a3ee83b9764b16b36d24e3620fe36f88d541516d70afca5e4e7627a36a`

## Attacks and results

### Lineage, degeneracy and dimensions

The repaired lineage is accurate: v2 supplied the set-theoretic least fixed point; v3 evaluates it for a finite family. Duplicate, dependent and non-normalized nonzero keys do not break the proof. Disconnected component spans are orthogonal. The state width is `rank[Q,K_R]`, not vertex count, and all displayed recurrence dimensions agree. A beta-zero-only key forces no direction and is correctly excluded.

### Decay/order attack

The graph result is valid for the stated symmetric pure factors. It does not extend to a general matrix decay. For example, with `d=2`, `Q=k=e_1`, `beta=1/2`, and
`D=[[1,1],[0,1]]` in `F=(I-beta e_1e_1^T)D`, the graph returns `span(e_1)` but `F^Te_1=(1/2,1/2)` leaves it. States differing only in coordinate two then have the same old syndrome and different next protected coordinate. The artifact correctly falls back to `F_i^TV subset V`.

### Hidden-selector attack

Let `S_+=(1,1)^T` and `S_-=(1,-1)^T`, which share the retained `e_1` coordinate. A selector reading the discarded sign can choose `e_1` versus `e_2`, producing different next retained coordinates. Thus selection, strength and value must be external or factor through the retained state; a separate full-state generator makes the reduced state only an auxiliary ledger, not a total-state compression. This boundary is stated.

### Future bridge attack

With carrier `span(e_1)`, full states `(0,0)` and `(0,1)` share reduced state zero. A later key `(e_1+e_2)/sqrt(2)` with `beta=1,v=0` yields next retained coordinates `0` and `-1/2`. Post-hoc basis expansion cannot reconstruct the missing history. Section 6 and the measurement section correctly require ex-ante family information and forbid test-suffix leakage.

### Numerical attack

For `k_1=e_1`, `k_2=epsilon e_1+e_2`, exact width jumps at `epsilon=0`. Thresholding forfeits exactness. The artifact gives the leakage operator and propagated bound and shows small pairwise overlaps need not imply small subspace leakage. Exactness needs a certified zero pattern/rank; numerical tolerances are metadata, not proof. Stability remains separate.

### Total-cost attack

Equation (2) is ordinary Delta in direct reduced coordinates. The artifact now charges dictionary, seed/Gram construction, dense or sparse graph, QR/SVD, basis, decoder, cache, lookup/certification, precision, traffic and amortization. Runtime `O(m_star d_v)` assumes supplied identity/cached coordinate; otherwise projection is charged. No advantage over the identical direct-coordinate control is claimed.

The minimality result is global over all ambient states and allowed operator sequences. A smaller reachable-set quotient is possible in principle but requires a different derivation.

## Retained counterevidence

- v1 static decoding did not imply recursion; v3 only evaluates v2's finite-family closure object.
- seeded components can span the full space, eliminating compression.
- geometry cannot identify semantic truth or beneficial revision.
- direct reduced coordinates are algebraically identical.
- unseen bridges rule out lossless prefix-only expansion.
- matrix decay, hidden selectors and finite-precision edge deletion remain failure boundaries.

## Verdict

**FINAL-BYTE PASS** for the scoped theorem/debugging certificate; candidate admission **NO**. It is a finite evaluation of v2's carrier and a narrow specialization of known common-invariant-subspace geometry, not a distinct updater. R12 attempt 3/3 is exhausted and should be parked with `candidate_delta=0`; empirical effect remains unknown.

