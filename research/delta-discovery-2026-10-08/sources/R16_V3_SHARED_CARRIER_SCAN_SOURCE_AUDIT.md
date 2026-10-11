# R16 v3 shared-carrier scan — source, implementation, collision, and measurement audit

- Math artifact: repairs/R16_SHARED_CARRIER_SCAN.v3.md
- Artifact SHA256: 48ec9e9e1c94191df3e8e5e8c87e810d4119d9d902ec61dd63e14d8c39ea0b4d
- Scope: bounded primary-source, author-interface, internal-collision, and native-measurement audit; not exhaustive priority certification or empirical validation.
- Execution: static source reading and mathematics only; no project/upstream code, model, benchmark, training, inference, scorer, data/model download, GPU, Docker, or paid service.

## 1. Preserved v2 evidence

The v2 DPR1, low-rank matrix-function update, rational Krylov, expmv, KDA, DeltaProduct, CKDA, S4/S5, R09/PDN/RLS, and benchmark audits remain applicable. V3 changes only the sequence-composition premise: it derives exact product-width growth, a shared-carrier closure condition, and a natural-flow recompression bound. It does not reinterpret KDA's ordered decay/write chronology as the joint exponential.

## 2. Generic affine scan is a direct collision

Martin and Cundy, *Parallelizing Linear Recurrent Neural Nets Over Sequence Length*, arXiv:1709.04057, section 1 and Algorithm 1, state that a linear recurrence \(h_t=\Lambda_th_{t-1}+x_t\) is a scan because matrix multiplication composes associatively and distributes over addition. Algorithm 1 summarizes blocks by a transition product and affine response, then scans the block pairs. Section 2.1 explicitly warns that dense matrix-matrix combination can cost \(O(n^3)\), motivating diagonal transitions for linear-cost combine.

The author repository eamartin/parallelizing_linear_rnns was read at commit da10de34701313e5556d67f4df4aacb76983e20c. Its linear_recurrent_net/linear_recurrence.h exposes `decays` and `impulses` as `n_steps` by `n_dims` arrays, and linear_recurrence.cu composes scalar decay/impulse pairs independently by coordinate. Thus the paper and Algorithm 1 provide the general affine-scan theory control for R16 v3 equation (12), whereas the released CUDA interface is an operational control only for the diagonal/elementwise special case; it does not implement a generic dense \(r\times r\) core composition. V3's only specialized content is the exact condition under which the R16 propagator can be reduced to an affine control and the sharp legal rank-growth witness when it cannot. Any dense-core implementation or speed claim would still require a separate interface and matched-cost comparison.

## 3. Delta/WY and ordered-product collision

Yang et al., *Parallelizing Linear Transformers with the Delta Rule over Sequence Length*, arXiv:2406.06484v6, sections 3.1–3.2, unroll the ordered Delta recurrence and use a compact-WY representation for products of Householder-like factors.

The pinned author implementation fla-org/flash-linear-attention@a7880060012c862d58575ee23f613cafcd728d03 remains the operational control. fla/ops/delta_rule/wy_fast.py exposes prepare_wy_repr_fwd and recompute_w_u_fwd; it builds the chunk triangular system and transformed key/value factors rather than a generic dense transition product. fla/ops/delta_rule/chunk.py consumes that representation. V3 does not show that its \(r\times r\) exponential core is cheaper than this ordered Delta/WY path.

R16's \(e^{-\tau(\Lambda+kk^\top)}\) is not KDA's ordered product. A common-carrier scan can evaluate the former exactly, but it does not make the two update semantics equal or prove the former scientifically preferable.

## 4. Internal invariant-carrier and low-rank-maintenance collisions

R10 v3 already derives the common-invariant-carrier criterion and invariant hull for Delta residual transport, including a full-width noncommuting witness and the costs of fixed/moving dense bases. R12 v3 turns the same closure question into a finite-key nonorthogonality-component certificate and gives the future-bridge impossibility when the family is not known ex ante. R16 v3 equation (21) is the joint-flow specialization of those controls.

R11 v3 already proves exact lazy propagation of low-rank overlays, additive rank growth under independent injections, transported recompression error, and generic QR/small-core-SVD controls. Brand's 2006 thin-SVD update remains the generic factor merge/recompression baseline. R16 v3 contributes a different legal source of the factors—matrix-function corrections—and the sharp PSD-exponential example, but not a distinct low-rank maintenance algorithm.

## 5. One-token active cores do not imply compact chunks

The v2 functional-calculus theorem implies \(\operatorname{rank}(C_t)\le r_t\) for each token. It does not imply \(\operatorname{rank}(P-Q)\le\max r_t\). V3's two telescopes are standard ordered product-difference identities, and its orthogonal-key example is exact inside the frozen R16 flow. Because the example is commuting, noncommutativity cannot be invoked as the sole reason for width growth.

Any exact factor ledger can remove dependencies, but its minimum width at a fixed chunk is \(\operatorname{rank}(P-Q)\). A robust fixed two-sided carrier must additionally close under the declared continuation family. This is not a universal classification of exact scan algorithms; other finite operator algebras and the dense affine pair remain possible. Approximate recompression is generic low-rank approximation; the natural-flow contraction gives a useful deterministic state-error bound but no semantic-loss, backward, or hardware guarantee.

## 6. Cost and same-information controls

Under a coordinate common carrier and coordinate-diagonal decays, the exact R16 chunk stores a complement diagonal action, an \(r\times r\) transition core, and an \(r\times m\) source. Generic combine costs include \(O(r^3+r^2m)\); a dense basis adds transform, discovery, storage, and backward costs. These must be compared against:

1. the identical direct \(r\)-dimensional affine recurrence/scan;
2. full affine composition when \(r\) is not small;
3. ordered Delta/WY and grouped KDA with the same grouping;
4. sequential exact DPR1 or exponential action;
5. R11 factor append/merge/recompression;
6. DeltaProduct at matched steps and total computation.

Calling the shared carrier an ODE or active-spectrum module does not create additional information or functionality. The direct core scan has exactly the same inputs, state, and outputs.

## 7. Native measurement boundary

Martin–Cundy and Delta/WY supply implementation controls for affine scan and ordered Delta composition, not semantic revision records. Existing bAbI, LAMBADA, RULER, LongMemEval, and DeltaProduct state-tracking endpoints can measure downstream behavior but do not jointly expose:

- the true simultaneous sub-token generator;
- exact one-token and chunk product-correction ranks;
- a prefix-known common reducing carrier;
- recompression residuals and backward error;
- valid-versus-obsolete association labels and paired update outcomes;
- matched kernel/traffic costs for the direct controls.

Synthetic matrix fixtures could test equations (4), (9), (18), and (25), but that would be numerical verification rather than a native scientific benchmark. No benchmark, data, case, label, metric, scorer, or result was created.

## 8. Audit decision

- Mathematical source support: conditional, for frozen symmetric PSD generators and the declared carrier assumptions.
- Mechanism originality: major collision with generic affine scan, Delta/WY, common invariant subspaces, and low-rank maintenance.
- Delta-specific residual: sharp legal product-rank boundary plus exact shared-carrier specialization.
- Architecture/scientific admission: not established.
- Measurement: native mechanism-identifying object absent.
- Empirical effect: unknown; no execution.

The source record supports a terminal theorem/control, not a first/new updater claim. R16 should remain parked after attempt 3/3 unless a lawful natural carrier or other exact closed representation gives a matched-total-cost advantage over the direct controls and the simultaneous generator receives independent scientific justification.
