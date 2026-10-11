# R13 repair-line screen v2 — uncertain realized transition

## Lineage and bounded attempt

- Parent bytes remain unchanged: `R13_REPAIR_LINE_SCREEN.md` and `R13_DYNAMIC_COVECTOR_PROTECTION.v1.md`.
- Substantive attempt: 2 of at most 3.
- Original problem: v1 can transport a declared old readout through one *known realized* affine Delta step, but it does not cover a decoder that knows only a lawful set of possible realized transitions.
- Failure type tested: insufficient information plus target/construction mismatch. This is not a correction to v1's algebra.
- Concrete patch: require one mode-blind decoder to work for every admissible affine transition, reduce the requirement to one simultaneous matrix equation, and derive a nonlinear ambiguity lower bound when the transition mode is not identifiable.

## Screened alternatives

| Patch | Mathematical delta | Decision |
|---|---|---|
| Common decoder over a finite/affinely generated transition family | exact block-kernel iff; full generalized-inverse family; two-mode invertible-Delta counterexample | **selected for the v2 child** because it changes the information structure and closes a genuine gap in v1 |
| Set-valued output of all compatible old reads | exact uncertainty set is valid, but every point estimate retains at least half its diameter in worst-case error | retain as a corollary/control; set-membership filtering is established and the set does not restore the old value |
| Posterior-average decoder | squared-risk optimum is the conditional mean with irreducible conditional variance | retain as a distribution-dependent baseline; it changes exact protection to Bayes estimation |
| Reveal the realized mode or retain the pre-update protected value | reduces to mode-specific v1 transport or a direct ledger | mandatory same-information controls; neither is a new R13 mechanism |

## Decision

The v2 patch produces a useful robust non-identifiability boundary, not a new updater. Even when every possible Delta transition is individually invertible, a single mode-blind transported covector can fail to exist. A direct protected-value ledger remains an exact `p d_v`-scalar control that succeeds without identifying the transition. It is smaller when the decoder must persist both `X` and an unconstrained offset, but an offset-free common decoder can instead cost `p d_k` and may be smaller when `d_k<d_v`; no general cost ordering is claimed. Common functional observers, simultaneous matrix equations, generalized inverses, and set-membership estimation cover the general mechanism family.

R13 is therefore parked after attempt 2 with candidate delta zero. Attempt 3 may reopen only if a causal native protected object requires an operation that cannot be performed from its direct value ledger, the transition uncertainty has a certified low-complexity structure, and the proposed representation beats mode labels, direct ledger, replay, and set-membership controls under matched state, precision, information, compute, and access.

No project code, software test, model execution, training, inference, scoring, dataset/model download, GPU work, or invented benchmark was used.
