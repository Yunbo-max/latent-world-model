# R13 repair-line screen — three bounded attempts

This screen resumed the existing failed records and selected three lines with an explicit mathematical delta. It does not create three candidates. Each line is limited to one substantive revision attempt here; old artifacts, counterexamples, and reviews remain unchanged.

## 1. Dynamic protected-readout transport — completed R13 child, PARK

- Parent problem: `STEP2_COUPLED_UPDATER_STABILITY.md` proves a fixed protected readout conflicts with strict contraction but leaves rotating/transported readers open.
- Failure type: target mismatch plus missing structural assumptions. A fixed `L` was asked to protect an ordered, time-varying recurrence.
- Patch: hold one realized affine step fixed and solve `Q_t^TA_t=Q_{t-1}^T` with the affine offset charged explicitly.
- Preserved result: contraction still cannot preserve distinctions in an erased direction; semantic validity/release remains unidentified.
- New exact boundary: transport exists iff `ker(A_t) subset ker(Q_{t-1}^T)`. At exact Delta overwrite, it exists iff `Q_{t-1}^TD_t^{-1}k_t=0`; otherwise two prior states collapse to one post-state. Before overwrite, the overlapping reader component grows as `1/|1-beta||k||^2|` in addition to conditioning from `D_t`.
- Why not a candidate: generalized inverses, functional observers, adjoint transport, and reversible-memory controls cover the mechanism family. For the declared fixed numerical invariant, directly storing `Y` uses `p d_v` scalars and dominates persisting `Q_t,C_t` (`p d_k+p d_v`).
- Reopen condition: a causal protected-object/validity selector plus a downstream operation unavailable to the direct ledger, with matched precision/state/compute/access.

## 2. Retroactive rollback — bounded derivation, PARK

- Parent problem: `rejected/RETROACTIVE_ROLLBACK_DELTA.md` tried to undo an old write locally, although later ordered transitions change its final effect.
- Failure type: construction mismatch and nearest-work collision.
- Patch: freeze later affine maps `F_t(X)=A_tX+B_t`, compose them as the affine monoid `(A_2,B_2)o(A_1,B_1)=(A_2A_1,A_2B_1+B_2)`, and delete a leaf in a product tree. The exact single-record correction is `S_T^{(-j)}=S_T-P_{T:j+1}delta_j`.
- Preserved result: direct subtraction or `F_j^{-1}` at the endpoint is generally wrong. A suffix-independent endpoint undo exists iff the deleted affine map commutes with every admissible suffix; for a fixed invertible suffix `R`, the correct undo is `R o F_j^{-1} o R^{-1}`.
- Old counterexample: in one dimension, `f(s)=s/2+1/2`, `r(s)=s/2`, `s_0=0`; deletion should yield zero, direct subtraction gives `-1/4`, direct endpoint inverse gives `-1/2`, while conjugated undo and propagated correction give zero.
- Why not a candidate: the construction is exact-record omission plus generic retroactive ordered-product data structures. Long products densify; full endogenous rollback changes future keys/gates and still requires replay or a shadow trajectory.
- Reopen condition: a Delta-structured sublinear suffix theorem that strictly beats ordered-product trees and checkpoint/replay under matched information.

## 3. Reciprocal key/value cycle — bounded derivation, PARK

- Parent problem: `rejected/RECIPROCAL_CYCLE_DELTA.md` used a bidirectional cycle score as evidence for revision versus collision.
- Failure type: insufficient information and known-mechanism collision.
- Patch: retain the exact geometry but withdraw the semantic claim. For `F:k->v`, `G:v->k`, residuals `e_v=v-Fk`, `e_k=k-Gv`, cycle residuals satisfy `c_k=e_k+Ge_v` and `c_v=e_v+Fe_k`. Thus, conditional on `F,G`, the cycle score is deterministic post-processing of the two residuals and adds no sigma-field.
- Preserved result: the score can still be a geometry/conditioning certificate. At population least squares, whitened cycle risk is `(d_k-r)+(d_v-r)+2 sum_i(1-sigma_i^2)^2`, a CCA spectral quantity; zero requires a full-support perfect linear bijection.
- Old counterexample: revision and coexistence worlds with the same current bidirectional residuals remain observationally indistinguishable; low cycle error shows near-bijection, not factual validity.
- Why not a candidate: CCA, streaming CCA/Oja, bidirectional associative memories, GSA2, and DeltaProduct cover the geometry and multi-correction mechanisms. A bidirectional Delta using `(e_v,e_k)` is the same-information simple control.
- Reopen condition: a prefix-only observable not determined by bidirectional residuals, or a Delta-specific interference theorem strictly stronger than CCA/residual controls.

## Decision

Dynamic covector transport was selected for a complete versioned child because it closes an explicit parent assumption gap and yields a sharp overwrite/conditioning theorem. Retroactive rollback and reciprocal cycle were not advanced beyond this bounded screen because their repaired constructions collide directly with stronger known controls. A fourth inspected set-valued/query-quotient line was also parked: its exact minimal query subspace is functional-observer/set-membership mathematics, and a direct `R^TS` summary meets the same lower bound.

No project code, model execution, training, inference, scoring, dataset/model download, or GPU work was performed. Empirical effects remain unknown.
