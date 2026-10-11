# Independent final-byte adversarial review — R18 v2

- Reviewer: `/root/r18v2_adversarial`
- Math artifact SHA256: `df90d64c215268d83d3a499be9e527a994a69d8b8d4a7969fbeffb8618e5f813`
- Screen SHA256: `f0f5266b74f8f56531f395acc1e5d66b4e075a3815408502eb94e6f6160d9411`
- Verdict: **PASS after correction; conditional affine-tree theorem/control only**

The initial exact-byte artifact failed this review. Required repairs were: consistent leaf/edge indexing; prefix-conditional rather than unconditional coverage; a fully prefix-measurable and update-fiber-uniform tree; explicit same-word versus bisimulation scope; and an automaton-state all-horizon fixed point. The final hashes above contain those corrections.

Adversarial checks passed:

1. Path/node conditioning is retained. The artifact does not conflate an exact constrained tree with its rectangular hull or use an unsafe existential/union kernel.
2. The full tree and numeric operators are lawful prefix-time objects. Realized future suffixes, answers and posterior modes are not exposed early. Learned coverage is explicitly conditional on `P(E_t|F_t)>=1-delta` almost surely.
3. An unstructured readout norm ball collapses the exact common kernel to zero; nontrivial robust compression therefore requires charged structure rather than silently assuming the desired nullspace.
4. `W(s)=s^2`, a step-function route, and the delayed shift-register witness preserve the global-fiber, hard-routing and finite-horizon failure boundaries.
5. Dynamic bases, automaton state, decoder metadata, precision, rank tolerance and branch computation are charged. The direct ledger attains the affine lost-visible rank lower bound.
6. The result is same-labelled-word trace equivalence, not general nondeterministic bisimulation; controlled mode/action information must descend to the quotient or be retained.

No remaining attack justifies rejecting the scoped theorem, but none supports candidate admission. Final disposition: attempt 2/3 parked, `candidate_delta=0`, contribution a known-mechanism Delta debugging control, native mechanism measurement missing, empirical effect unknown.
