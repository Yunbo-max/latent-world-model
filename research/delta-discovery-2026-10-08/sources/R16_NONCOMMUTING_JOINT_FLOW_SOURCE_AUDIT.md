# R16 noncommuting joint flow — source, author-interface, novelty, and measurement audit

- Math artifact: repairs/R16_NONCOMMUTING_JOINT_FLOW.v1.md
- Artifact SHA256: 737f49385a232bdf9261c0fe7bec10955d0856ac7315e71ea226d7c78895d7d6
- Scope: bounded formula/interface/collision audit, not exhaustive priority certification or empirical validation.
- Execution: static source reading and mathematics only; no project/upstream execution, model, benchmark, training, inference, scorer, data/model download, GPU, Docker, or paid service.

## 1. Delta/KDA recurrence baseline

KDA is the closest operational control because its actual recurrence decays the state and then performs a residual rank-one write. The pinned Flash Linear Attention source is:

- Kimi Linear / KDA paper arXiv:2510.26692v2, §3 Eqs. (1)–(2) and §6.2
- fla-org/flash-linear-attention@07ca1e49ef6ca76a7f0dbc8d5ad040ab59434c38
- fla/ops/kda/naive.py, blob 51ff7076b26244366cf7ed2999ed13052da19cd5
- interface naive_recurrent_kda

The loop first applies elementwise channel decay S = S * exp(g_i), then forms v_i - k_i^T S, then adds the rank-one write. KDA is not incorrectly approximating a hidden simultaneous ODE; R16 adds a different frozen sub-token generator. The pinned implementation is decisive for actual order.

## 2. Scalar flow and preconditioning collisions

The EFLA author code implements the scalar exact-flow gate but retains ordinary rank-one erase/write:

- paper arXiv:2512.12602v5, §3.1 Eqs. (10)–(11), §3.2 Eqs. (12)–(15), Eq. (28), and Appendix F Eqs. (51)–(68)
- declare-lab/EFLA@f188eae5133bb3aa37c441980db5a440db396f05
- mnist.py, blob bbfc1a81a35c91c70283cea08ec0bf7784370326
- forward computes alpha=-expm1(-beta*lambda)/(lambda+1e-6), then applies the usual residual update.

This is a direct collision when \(\Lambda k\) is parallel to \(k\); it does not implement R16's dense noncommuting transition.

The practical PDN implementation is a strong endpoint control:

- paper arXiv:2604.21100v1, §2.3 Eqs. (1)–(2), §3.1 Eqs. (3)–(5) and Theorem 3.1, §3.2, and §3.3 Eq. (7)
- ntumm120/preconditioned-deltanet@7bd753279af87b39114149a104c5bde9bf67145f
- 3rdparty/flash-linear-attention/fla/ops/precond_gated_delta_rule/naive.py, blob 4a2273f25a89b509332e8755391e78cc594a16b0
- naive_recurrent_precond_gated_delta_rule maintains a diagonal accumulator, applies a stable squash, reads with the raw key, and writes with the preconditioned key.

The PDN paper's non-diagonal inverse-Gram theory must not be conflated with this stable diagonal implementation. R16's endpoint direction is a normalized inverse metric with \(H=P_\tau^{-1}\), so it collides at the mathematical-function level with PDN/RLS and internally with R09. R16 does not claim the practical PDN kernel computes its dense metric.

## 3. Exact discretization and structured-SSM collision

For a constant linear system, the R16 affine solution is standard zero-order-hold/exponential integration. The S4 paper, Efficiently Modeling Long Sequences with Structured State Spaces, formulates continuous linear state-space dynamics and discretization. Its author repository exposes structured recurrent kernels and a diagonal ZOH branch:

- S4 paper arXiv:2111.00396
- state-spaces/s4@e757cef57d89e448c413de7325ed5601aceaac13
- models/s4/s4.py, blob deb534192dbf2b7795b29283e14d9430b9b00195
- the diagonal SSMKernelDiag ZOH branch uses (exp(dtA)-1)/A; the broader S4 construction also includes bilinear discretization and DPLR structure.

This is a generic exact-discretization collision, not evidence that S4 implements R16's token-varying Delta residual. S4 obtains efficiency from fixed structured generators and specialized kernels, whereas R16 changes \(M=\Lambda+kk^\top\) per token and products of the dense exponentials do not remain one DPLR factor.

S5 (arXiv:2208.04933) supplies a second author-code ZOH control: lindermanlab/S5@3c18fdb6b06414da35e77b94b9cd855f6a95ef17, s5/ssm.py blob bdc8a6c1cfdd8713bc960b1ea1101b029ac8f5c4, function discretize_zoh. Its diagonalized fixed generator again differs from the per-token R16 generator.

Longhorn (arXiv:2407.14207v5, §3.2 Eq. (5), Theorem 3.1/Eq. (6), Eq. (7), Algorithm 1) is a distinct implicit/proximal control. The author code Cranial-XIX/longhorn@4ea174598787ee189f889d17f9a02c2bbdc381a4, models/longhorn.py blob 41fc512429416cb175eec28fcb79b761087c0f39, Longhorn.step, deploys an elementwise \(1-dt\,k^2\) gate. The fused/reference repository Cranial-XIX/longhorn_cuda@1be52220873ccc44fe84f052c150db578fcb5c33, mamba_ssm/ops/selective_scan_interface.py blob 49d94a28903dd788d88365e4a02d443c8c628945, function selective_scan_online7_ref, exposes the same approximation. It does not compute the noncommuting exact ZOH.

## 4. Matrix-function update and exponential-action collision

Computing

\[
f(\Lambda+kk^\top)-f(\Lambda),\qquad f(z)=e^{-\tau z},
\]

is a standard low-rank matrix-function-update problem.

- Beckermann, Kressner & Schweitzer, Low-rank updates of matrix functions, arXiv:1707.03045 / SIAM J. Matrix Anal. Appl. 2018, derives Krylov approximations for \(f(A+D)-f(A)\).
- Beckermann et al., Low-rank updates of matrix functions II: Rational Krylov methods, arXiv:2008.11501, strengthens this numerical-control family.
- Al-Mohy & Higham, Computing the Action of the Matrix Exponential, with an Application to Exponential Integrators, SIAM J. Sci. Comput. 2011, is a primary control for \(\exp(A)B\) without forming \(\exp(A)\).
- Jakovčević Stor, Slapničar & Barlow, arXiv:1405.7537v2, gives forward-stable eigendecomposition for real symmetric diagonal-plus-rank-one matrices; a full basis is still \(O(d^2)\)-scale representation/computation rather than a fixed scalar/rank-one gate.

These sources prevent claiming a Krylov implementation as a new Delta algorithm. R16's retained delta is the Delta-specific Krylov support/rank, exact-write collision, affine-source gap, and cost boundary. A finite Krylov approximation needs an error contract and comparison with direct exponential action, split KDA, PDN, and multistep DeltaProduct.

## 5. Internal lineage and novelty boundary

- rejected/EXACT_FLOW_IMPLICIT_DELTA_CONTROL.md already proves exact scalar residual flow changes only the gate.
- rejected/SYMMETRIC_SPLIT_DELTA_CONTROL.md and rejected/AFFINE_MAGNUS_COMMUTATOR_CONTROL.md already place split/Magnus corrections in known numerical-analysis territory.
- repairs/R11_ORDER_GAP_COMPRESSION.v1.md already derives low-rank signed adjacent order gaps under frozen features.
- repairs/R09_FINITE_BUDGET_OVERWRITE_PROTECTION.v1.md already derives normalized inverse-metric endpoints and exact-overwrite singularity.
- R13 treats dynamically transported readouts; none supplies semantic validity or revision evidence.

R16's mathematical delta is narrow but real as a packet theorem: the full simultaneous generator departs from pure decay on the \(\Lambda\)-Krylov space of \(k\), can exceed rank one immediately, and has an affine source discrepancy that a homogeneous commutator misses. This does not establish a novel efficient updater.

## 6. Native measurement feasibility

bAbI, LAMBADA, RULER, and LongMemEval provide endpoint prediction/QA behavior. They do not natively reveal a true continuous sub-token generator, the exact internal transition/source pair, or which leaked association remained valid. A comparison could test endpoint utility but not identify the declared mechanism without added instrumentation, which is outside this mathematical stage.

No reviewed native asset jointly supplies the continuous generator, exact internal state action, causal validity labels, and matched-cost dense-versus-split computation. The measurement gap remains; no benchmark, metric, label, or result is fabricated.

## 7. Audit decision

- Mathematical/source consistency: conditionally supported for the declared frozen simultaneous ODE.
- Functional novelty: PARTIAL_THEOREM_DELTA / MAJOR_METHOD_COLLISION; bounded-search priority remains INCONCLUSIVE_EXPAND_SEARCH.
- Architecture candidate: not admitted.
- Experimental effect: unknown; no execution.
- Reopen condition: independent justification of the simultaneous ODE plus a certified structured action with matched-budget advantage, or new causal evidence resolving protection versus revision.

This bounded audit prevents method duplication but does not claim exhaustive literature priority.
