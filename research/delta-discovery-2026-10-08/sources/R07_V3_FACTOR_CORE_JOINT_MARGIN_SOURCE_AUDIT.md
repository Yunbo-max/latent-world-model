# R07 v3 factor-core joint margin — source, implementation, collision and native-measurement audit

Audit date: 2026-10-11  
Scope: `repairs/R07_FACTOR_CORE_JOINT_MARGIN.v3.md`; bounded primary full-text and static author-interface comparison. No project or upstream code, tests, data, models, scorer or experiment were run.

## 1. Preserved lineage

R07 v1's truth-versus-action quadratic and source audit remain unchanged. R07 v2's complete-state first/second directional derivative, costate-weighted dynamics curvature, score-function boundary and final-byte reviews also remain unchanged. V3 does not inherit their pass: it changes the object to a simultaneous multi-action frozen-affine suffix and therefore receives new math, source, adversarial and measurement review.

The v3 claim is deliberately narrow. It says that fixed rank-one proposal directions passed through fixed affine Delta transitions and quadratic reads yield an exact reduced box QP. It does not claim that actual learned future keys, gates, routes, value targets or future laws are fixed.

## 2. Delta/WY and DeltaProduct controls

**Yang et al., “Parallelizing Linear Transformers with the Delta Rule over Sequence Length,” arXiv:2406.06484v6.**

- Official full text: <https://arxiv.org/abs/2406.06484> and <https://arxiv.org/pdf/2406.06484v6>.
- Reused read depth: Section 2.2 for the Delta recurrence and Sections 3.1--3.2 / Appendix B for the exact ordered compact WY-style product.
- Consequence: fixed ordered products of Delta/Householder factors and their compact action are established. Yang et al.'s exact WY formula does not by itself cover arbitrary interleaved diagonal `D_t`; R07 v3 only uses direct recurrent application of `(I-gamma uu^T)D`, which is still linear in `d_k m` for diagonal `D` but is not called the same WY kernel. The skinny-factor propagation is an algebraic specialization, not a new transition family.

**Siems et al., “DeltaProduct: Improving State-Tracking in Linear RNNs via Householder Products,” arXiv:2502.10297v7.**

- Official full text: <https://arxiv.org/abs/2502.10297> and <https://arxiv.org/pdf/2502.10297v7>; Section 4 defines multiple ordered Delta/Householder microsteps and Section 5.2/Figure 5 evaluates state tracking.
- Author-maintained FLA pin reused from the packet: `fla-org/flash-linear-attention@a7880060012c862d58575ee23f613cafcd728d03`, `fla/layers/gated_deltaproduct.py`, blob `82d1a62ac228f3c80aa8818b6e0d0082ce6635b8`.
- The inspected `GatedDeltaProduct.forward` projects `num_householder` keys, values and rates, uses `chunk_gated_delta_product` for training/chunk mode, and flattens ordered microsteps into `fused_recurrent_gated_delta_rule` for recurrent inference. The authors' task repository remains pinned at `automl/DeltaProduct@d62241a81d07aa32b1b65e7d17377f6a7cd0a5d8`.

DeltaProduct is an essential control but not identical to v3's action object: it applies ordered microsteps whose later residuals arise in chronology, whereas v3 simultaneously scales a fixed proposal bank. This difference blocks silently using the v3 affine QP for sequentially recomputed writes. It does not create method novelty; exact ordered Delta/DeltaProduct is the stronger executable baseline.

## 3. Joint quadratic action and optimal-control collision

**Tassa, Erez & Todorov, “Synthesis and Stabilization of Complex Behaviors through Online Trajectory Optimization,” IROS 2012.**

- Primary paper: <https://roboti.us/lab/papers/TassaIROS12.pdf>.
- Reused read scope: Section II.A--B, equations (1)--(8), for the finite-horizon Bellman recursion, joint local quadratic `Q(delta x,delta u)`, cross derivatives and backward value recursion.
- Consequence: retaining a joint action Hessian and solving a finite-dimensional constrained quadratic model is standard DDP/iLQG control machinery. V3's new algebraic content is the frozen Delta response factorization, not joint-action optimization.

**Amos et al., “Differentiable MPC for End-to-end Planning and Control,” NeurIPS 2018.**

- Primary paper: <https://papers.nips.cc/paper_files/paper/2018/hash/ba6d843eb4251a4526ce65d1807a9309-Abstract.html> and <https://arxiv.org/abs/1810.13400>.
- Reused read scope: equations (1), (5)--(12) for LQR/costates and nonlinear MPC convexification, plus Sections 4.1--4.2, equations (14)--(19) and Modules 1--2 for the box-constrained QP and KKT differentiation.
- Pinned author repository: `locuslab/mpc.pytorch@1fb5d416436e1b2d56494ac4c2cab9008c6413bb`; `mpc/mpc.py` blob `d5174e9142098c5a51c81ba7bbbb205a38fb7c7f`, `mpc/lqr_step.py` blob `cad5d6c46d70547f6da2392474f5ae6e811a3f24`, and `mpc/pnqp.py`.
- Static interface consequence: `MPC` linearizes dynamics and quadratizes cost; `LQRStep/lqr_backward` forms the joint `Q_xx,Q_xu,Q_ux,Q_uu` blocks and solves the backward recursion; `pnqp.py` provides the constrained subsolve.

These controls already cover “do not sum scalar margins; solve the joint quadratic action.” Weighted least squares, Gram matrices, the Schur product theorem and box-QP solvers also cover the generic mathematical core. The exact identity

\[
H-R=\sum_t(c_tc_t^\top)\odot(E^\top W_tE)
\]

is a useful Delta-coordinate derivation, not a new optimizer.

The same elimination pattern is also standard in condensed linear-quadratic MPC. Cole et al., “Exploiting GPU/SIMD Architectures for Solving Linear-Quadratic MPC Problems,” arXiv:2209.13049, Section II equations (1)--(4), stacks and eliminates affine states to obtain a dense QP in the control variables; Section III further condenses its KKT system. Otta et al., arXiv:2002.06835, reviews state condensing and move blocking. These are functional collisions, not claims that either paper states the Delta Hadamard identity verbatim.

Kolda & Bader, “Tensor Decompositions and Applications,” *SIAM Review* 51(3), Section 2.6 equation (2), gives the classical Khatri--Rao Gram identity `(A odot B)^T(A odot B)=(A^TA)*(B^TB)`. Vectorizing the rank-one R07 responses yields precisely this type of Hadamard Gram. The coordinate identity is useful but not a new linear-algebra mechanism.

## 4. Internal packet collisions and exact residual

- R07 v2 already gives the complete coupled first/second derivative and explains why fixed coefficients omit coefficient/state feedback.
- R09 v2 gives a future-protection Gramian and its prefix-information boundary.
- R11 v2 gives a different factor/core reduction for a two-write adjacent order gap, with exact Delta/WY and DeltaProduct controls.
- R15 v2 gives the affine/quadratic response-closure boundary and shows how nonlinear coupled continuations raise intervention degree.
- R20 v1--v3 give low-rank constrained curvature solves, prefix-surrogate drift and a same-prefix future-curvature impossibility.

The v3 residual is therefore limited to: (i) the simultaneous fixed-proposal response identity, (ii) the Hadamard factorization of all multi-action cross terms, (iii) `O(Hd_km)` key-factor propagation for diagonal-plus-rank-one frozen transitions, and (iv) an explicit state-dependent-gate sign reversal. Those results are useful for debugging, exact-baseline construction and rejecting invalid scalar composition. They do not define a distinct updater.

## 5. Cost and same-information controls

The advertised `O(Hd_km)` covers only transition of the skinny key-side factor. A fair total cost also includes:

- storage of already supplied/cached proposal factors, `O(m(d_k+d_v))`;
- residual construction/read cost, up to `O(md_kd_v)` for computing every `e_r=v_r-S^\top k_r` from a dense state, unless those residuals are already produced or cached by the declared proposal path, plus the separately charged key/value projection cost;
- no-action suffix rollout and every future probe/target used to build the objective;
- query contractions and value-metric Gram work, up to `O(H(d_v^2m+d_vm^2))` for varying dense `W_t`;
- `O(Hm^2)` Hessian accumulation, `O(m^2)` state, conditioning/tolerance and up to cubic dense QP factorization;
- applying the selected rank-`m` update, `O(md_kd_v)`, plus any prefix predictor/calibration and routing metadata.

Strong same-information controls are no-write; frozen-proposal additive application with the exact same proposal bank; ordinary causal sequential Delta that recomputes later residuals; all-write/rank-`m` Delta; independent scalar/diagonal-QP gating with the same `g,diag(H)`; an explicitly vectorized dense action QP (algebraically identical correctness baseline); same-data batch ridge/least squares when proposals arise from supplied targets; paired suffix rollout or finite differences for small `m`; a direct action-vector/advantage predictor; and generic JVP/HVP/DDP when leaving the frozen affine scope. A future-answer oracle is only an upper bound, not a fair controller.

No matched-total-cost advantage is established.

## 6. Native measurement feasibility

Available public interfaces can measure endpoints:

- AToKe supplies `time_true`, `time_new`, history and old/new answers for temporal facts.
- CounterFact/ROME and KnowEdit/EasyEdit measure supplied-edit efficacy, generalization and locality.
- LongMemEval v1/v2, StreamingQA, CITB, TRACE and related memory/continual suites measure retention, temporal QA or continual endpoint behavior.
- SEAL records post-edit and continual outcomes, but it is parameter-level self-editing with a different resource/interface contract.
- bAbI/ParlAI and LAMBADA/lm-evaluation-harness remain fixed native reasoning/language endpoints.
- DeltaProduct's author task repository measures ordered group state tracking; order representation is not a label for whether a proposed internal write should be jointly accepted.

None exposes a native joint tuple containing a prefix-fixed bank of `m` Delta proposals, frozen suffix coefficients, internal response factors, gold joint action, paired same-prefix action outcomes and matched byte/FLOP cost. Instrumented algebra can check the identity or QP KKT residual, but that is implementation verification, not a native scientific endpoint. Native tasks could later falsify usefulness; they cannot identify the proposed mechanism without extra non-native labels.

Using realized suffix queries/targets or benchmark answers to form the online action is leakage. A prefix predictor would require its own calibration, state and total-cost comparison. The mechanism-identifying measurement gap therefore remains open; empirical effect is unknown rather than negative.

## 7. Decision

- Mathematical source support: conditional on fresh final-byte review.
- Primary/author-interface fidelity: supported for the bounded claims above; all inspection was static.
- Functional novelty: **MAJOR_COMPONENT_COLLISION / CONTROL_ONLY**.
- Architecture or estimator candidate: not admitted.
- Prefix/free-running causal validity: not established.
- Native mechanism measurement: unavailable in the inspected interfaces.
- Attempt status: 3/3 exhausted.
- Candidate/count effect: zero.

R07 v3 should be retained as an exact structured control and a sharp feedback boundary. Reopening this lineage would require either a Delta-specific factorization of the full coupled Jacobian/Hessian—including coefficient derivatives—with nonvacuous prefix-valid drift/tail calibration cheaper than direct JVP/action prediction, or a native randomized multi-action causal record. Another frozen-factorization or solver variant is insufficient.
