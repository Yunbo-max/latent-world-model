# Independent review — SYMMETRIC-SPLIT-DELTA-CONTROL

Reviewers: `/root/symmetric_split_math` and `/root/symmetric_split_audit`. Read-only mathematical/source review; no project execution.

Decision: **reject as candidate; retain as a symmetric-coordinate/ODE-discretization control**.

- Both reviewers derived the same (D-\beta D^{1/2}kk^\top D^{1/2}) factor and its reciprocal-address oblique Delta form.
- The symmetric factor is per-step similar to KDA's actual ordered factor; Complex KDA already states this relation. Ordinary KDA and the sandwich share the same nonexpansive worst-case bound under the legal gate range.
- Naive splitting no longer performs exact correction at the original key. Correcting that defect yields PDN-style preconditioned addressing; using two Delta half steps falls under DeltaProduct.
- Strang's second-order global interpretation requires an explicit frozen continuous-time model and exact subflows. It is not a free theorem about learned token recurrences.
- Time-varying products, semantic retention, revision/collision identification and capacity remain unresolved.

The only defensible hypothesis is a numerical/optimization ablation against matched PDN/GDN2/DeltaProduct controls. That does not justify scientific admission or a D-number.
