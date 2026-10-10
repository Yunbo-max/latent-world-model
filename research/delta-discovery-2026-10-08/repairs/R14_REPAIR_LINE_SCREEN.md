# R14 repair-line screen — identity uncertainty before memory geometry

Scope: mathematics, primary-source and native-measurement feasibility only. No model code, benchmark, training, inference or scoring was executed.

## Three bounded repair clues

| Parent line | Exact failure | Failure type | Preserved result | Concrete repair tested | Screen decision |
|---|---|---|---|---|---|
| `rejected/PROVENANCE_TENSOR_DELTA.md` | The tag `c` is assumed to be the correct source/entity/version identity. The tensor write only executes that already-solved decision. | insufficient information / oracle assumption | `k⊗c` gives product-similarity interference and one-hot tags are exactly routed Delta slots | replace oracle identity by a causal posterior `π=P(J=i|F_t)` and derive the Bayes action over the same slots | selected as R14 because it changes the information model without deleting the old counterexample |
| `rejected/PSEUDOSPECTRAL_TRANSIENT_DELTA_CONTROL.md` | per-factor Kreiss constants are vacuous on legal contractive Delta and do not compose over token-varying products | target mismatch | nonnormal transient growth remains a valid diagnostic for oblique factors | use an actual ordered finite-horizon product or complete Jacobian | not selected: this is already product/Jacobian risk, common/path-complete Lyapunov control, and overlaps R11/R13 |
| `rejected/ORTHOGONAL_VALUE_ROTATION_CONTROL.md` | exact key-local rotation is state-identical to full-step Delta; adaptive target matching loses isometry | mechanism identity / construction mismatch | global Gram feasibility and local equivalence are correct | add uncertainty over which slot/value should rotate | not selected: it reduces to the same identity-posterior routing problem with a stricter Gram feasibility set |

R14 therefore attempts one substantive revision of the provenance lineage. It does not count the other two lines as candidates or retry them under new names.

## State transition

The old byte record and review remain authoritative for the identity-oracle construction. R14 changes only one assumption: identity is latent, and the updater receives a prefix-measurable posterior rather than the true tag. It asks for the optimal action under a declared local loss, not for recovery of the hidden identity without evidence.

The repair is useful only if it produces either (i) a Delta-specific action unavailable to direct routed slots, or (ii) a sharp theorem/counterexample that narrows the science. The attached R14 artifact obtains (ii), while direct posterior-weighted slot writes remain the stronger implementation control.
