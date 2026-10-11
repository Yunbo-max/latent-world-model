# Independent mathematical review — R12 v3 Gram-component closure

Reviewer: `/root/r12_v3_math`  
Assignment: independent final-byte mathematical review; read-only, no artifact editing and no project/model code, test, training, inference, scoring or experiment.  
Reviewed: 2026-10-11.

## Exact reviewed artifacts

- screen SHA256 `9b357b384bb6d142b936aaa7da86ce9ad023ab2a91e8de2b7c886c1cbe5ed6a9`
- math SHA256 `0df2d08785ba551cbe4ee3499550c24a1d3487fd297c6a760b2edc4eae99f16b`
- source SHA256 `e39180a3ee83b9764b16b36d24e3620fe36f88d541516d70afca5e4e7627a36a`

## Scope reconstructed

The object is a finite active dictionary known before compression and pure transitions

\[
S^+=(I-\beta_i k_i k_i^T)S+\beta_i k_i v^T,\quad\beta_i\ne0.
\]

The selected key, strength and value must be external or factor through the retained prefix/state; exactness is over every ambient `S` and allowed sequence. A fixed linear state `Y=U^TS` must be autonomous and recover `Q^TS`. This is not a theorem for an undeclared neural key continuum, hidden-state selector, non-scalar decay, restricted reachable set, one schedule, or nonlinear/time-varying codec.

## Checks

1. **Lineage.** v2 already supplied the least fixed point. v3 correctly evaluates it for a finite family and adds the component/dimension/cost/bridge certificate.
2. **One factor.** Invariance under `F_i` is equivalent to invariance under `k_i k_i^T`; the rank-one image argument proves exactly `k_i in V` or `k_i perpendicular V`. Zero-only operators are excluded.
3. **Graph theorem.** Every seed is forced into any feasible `V`; nonzero-Gram paths propagate membership. An unselected component is orthogonal to `V_0` and all selected components. Thus
   `V_star=V_0+span{k_i:i in R}` is feasible and contained in every feasible subspace, hence is the unique least carrier. `m_star=rank[Q,K_R]` is correct; vertex count is not confused with dimension.
4. **Recurrence.** For orthonormal `U`, `h_i=U^Tk_i` and
   `Y^+=(I-beta_i h_i h_i^T)Y+beta_i h_i v^T` is exact. Since `Q=U(U^TQ)`, the decoder is correct.
5. **Bridge impossibility.** Histories differing only in a discarded `e_2` coordinate share the old reduced state but yield different protected states after `e_1+e_2`; prospective exactness requires the complete family, replay, full state or equivalent ledger before compression.
6. **Approximation.** The cross-boundary norm, projected-error recursion and unrolled bound follow directly. The unit-key example has projected and orthogonal norm `1/sqrt(2)` although each displayed generator overlap is `1/sqrt(2r)`, correctly refuting an unconditioned threshold claim.
7. **Scope/cost.** Unseen keys, numerical zero discontinuity, discarded-state selectors, general left decay, semantic validity and native mechanism measurement remain explicit limits. Dictionary, Gram, graph, QR/SVD, basis, decoder, cache, lookup, precision and amortization are charged. Runtime `O(m_star d_v)` holds only with supplied/cached projected key; otherwise projection is additional. Direct `U^TS` is algebraically identical.

The dimension statement is limited to fixed linear syndromes working on all ambient states and allowed sequences. It is not a lower bound for nonlinear infinite-precision encodings, terminal-only finite horizons or restricted reachable sets.

## Outcome

**PASS** for the scoped finite-family theorem, recurrence, counterexample, approximation boundary and cost certificate. This establishes mathematical consistency only, not originality, empirical benefit, native measurement, scientific admission or selection.

- `candidate_delta: 0`
- scientific state: conditional theorem/debugging control
- empirical state: unknown / not executed
- lineage: attempt 3/3 exhausted; park

Reopen only with a lawful unseen-key mechanism, matched-total-cost advantage, or native mechanism-identifying record.

