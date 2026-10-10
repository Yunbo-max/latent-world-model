# R07 v2 coupled directional margin — source, implementation, novelty and native-measurement audit

Audit date: 2026-10-11  
Scope: `repairs/R07_COUPLED_DIRECTIONAL_MARGIN.v2.md`; bounded full-formula and static author-code comparison, not empirical validation or exhaustive priority certification.

## 1. Preserved R07 v1 evidence

The v1 source audit is retained unchanged at `sources/REPAIR_R07_VALIDITY_TO_ACTION_SOURCE_AUDIT.md`, SHA256 `a649af73e90b0529a95c2bdf726159b76133321f5a491feb063fdf6490c3c16b`. It pins and compares KnowledgeEditor, AlphaEdit, O-Edit, LyapLock, ROME, MEMIT, MEND, EasyEdit/KnowEdit, SEAL and AToKe. Its conclusion remains: target benefit versus signed preservation cost is a known constrained-edit problem; AToKe partly supplies temporal validity, but no reviewed native interface jointly supplies pre-action Delta margins, randomized propensities and paired action outcomes.

R07 v2 does not reuse the old review as a pass. It changes the mathematical object from a fixed-reference quadratic to a complete-state finite-horizon derivative, so the new artifact receives a fresh source comparison and fresh final-byte review.

## 2. Direct control-theory collision

### 2.1 Differential dynamic programming and iLQG

**Tassa, Erez & Todorov, “Synthesis and Stabilization of Complex Behaviors through Online Trajectory Optimization,” IROS 2012.**

- Primary paper: https://roboti.us/lab/papers/TassaIROS12.pdf
- Read scope: Section II.A--B, Eqs. (1)--(8). Eq. (2) is the Bellman recursion; Eqs. (3)--(5) form the local quadratic `Q(delta x,delta u)` and its derivatives; Eqs. (6)--(8) give the affine control law and backward value recursion.
- The paper explicitly distinguishes full DDP's costate contraction with second derivatives of the dynamics from iLQG's omission of those terms. This is the same distinction as R07 v2 equation (9). Therefore a complete-state first/second action margin is established optimal-control machinery, not a new Delta mechanism.

### 2.2 Differentiable MPC

**Amos, Jimenez, Sacks, Boots & Kolter, “Differentiable MPC for End-to-end Planning and Control,” NeurIPS 2018.**

- Primary paper: https://arxiv.org/abs/1810.13400 and https://papers.neurips.cc/paper/8050-differentiable-mpc-for-end-to-end-planning-and-control.pdf
- Read scope: Eq. (1) finite-horizon MPC; Eqs. (5)--(7) KKT/costate; Eq. (8) parameter gradients; Eq. (9) auxiliary LQR; Eqs. (10)--(12) nonlinear MPC convexification. The method differentiates an iLQR fixed point by an additional backward solve and warns that an unconverged fixed point can invalidate the implicit gradient.
- Pinned author repository: `locuslab/mpc.pytorch@1fb5d416436e1b2d56494ac4c2cab9008c6413bb`.
  - `mpc/mpc.py`, blob `d5174e9142098c5a51c81ba7bbbb205a38fb7c7f`, class `MPC` and `GradMethods`: linearizes nonlinear dynamics, quadratizes cost, solves repeated constrained LQR subproblems and controls differentiation through the fixed point.
  - `mpc/lqr_step.py`, blob `cad5d6c46d70547f6da2392474f5ae6e811a3f24`, `LQRStep` / `lqr_backward`: forms `Q=C+F^T V F`, partitions `Q_xx,Q_xu,Q_ux,Q_uu`, solves feedforward/feedback terms and performs Riccati recursion. `LQRStepFn.backward` solves the adjoint LQR, recursively forms costates `lams`, and returns derivatives with respect to cost, dynamics and initial state.
  - `mpc/pnqp.py` supplies the box-constrained QP solve.
- Static inspection only; no code, test or experiment was executed.

This author implementation directly covers “backward costate plus differentiable finite-horizon action calculation.” A Delta rank-one injection can reduce the final contraction to one direction, but that property is shared by any scalar intervention and does not remove the general recurrent differentiation.

## 3. Meta-learning and learned-updater collision

### 3.1 MAML

**Finn, Abbeel & Levine, “Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks,” ICML 2017.**

- Primary paper: https://proceedings.mlr.press/v70/finn17a.html ; Section 2.2 and Algorithm 1 differentiate a post-update query loss through an inner update and also discuss a first-order approximation.
- Pinned author repository: `cbfinn/maml@a7f45f1bcd7457fe97b227a21e89b8a82cc5fa49`; `maml.py`, `MAML.construct_model` / `task_metalearn`, separates inner `inputa` from post-update `inputb` and supports stop-gradient/first-order behavior.

### 3.2 Learned optimizers

**Andrychowicz et al., “Learning to learn by gradient descent by gradient descent,” NeurIPS 2016.**

- Primary paper: https://papers.nips.cc/paper_files/paper/2016/file/fb87582825f9d28a8d42c5e5e8b23d-Paper.pdf
- Eqs. (1)--(3) define a recurrent learned update and its finite-horizon outer loss; the paper discusses BPTT truncation, an approximation that drops a second-order path, and intermediate-loss surrogates.
- No author-code interface was asserted in this audit because the bounded search did not verify one.

These sources already cover “include updater hidden state and train/evaluate an update using future loss.” They do not supply R07's grounded truth/action bridge, but they prevent claiming that coupled updater state or future-loss differentiation is itself novel.

### 3.3 SEAL, Ouroboros and HOPE

- **SEAL**, https://arxiv.org/abs/2506.10943, Section 3.1 Eqs. (1)--(4), uses an inner self-edit followed by downstream outer reward. Pinned author repo `Continual-Intelligence/SEAL@6d9c9f9ee392c6cc618e771f399d436d190f6ca4`; packet-inspected interfaces include `general-knowledge/src/inner/TTT_server.py`, `query/query_server.py`, `EM/build_SFT_dataset.py` and `general-knowledge/src/continual/continual_self_edits.py`. Its continual results retain forgetting as negative evidence. This is a broad downstream-reward self-edit comparator, not a pre-action Delta certificate.
- **TTT Ouroboros**, https://arxiv.org/abs/2610.05076, pinned author repo `lingjivoo/ttt-ouroboros@f7811f878679864e686c84abcd83dd05efdc0417`, already implements pending candidate updates, independent sequential validation and settlement. Delayed validation/commit is therefore not an R07 residual.
- **HOPE / Nested Learning**, https://arxiv.org/abs/2512.24695 and https://research.google/blog/introducing-nested-learning-a-new-ml-paradigm-for-continual-learning/, provides multi-timescale and self-modifying-memory machinery. The packet's earlier full-formula audit found no verified author implementation; third-party implementations remain excluded. HOPE does not make future costates causally observable or prove recursive improvement.

## 4. Internal packet overlap and exact residual

The packet already contains:

- full state Jacobian versus frozen-feature products, exact Hessian, GGN/iLQR approximations, full-DDP dynamics-curvature terms, and RTRL/UORO/e-prop/DNI comparisons in the Step-2 recursive-metric/coupled-updater records;
- R01 transported costates and goal-weighted tangent quotients;
- R02 randomized action/OPE and quotient conditions;
- R03 common-path versus free-running law bounds;
- R08 Bellman continuation, switching cost and information-destruction counterexamples.

R07 v2 therefore contributes only a cleaned, lineage-specific theorem: v1's signed truth/protection margin is the zero-horizon affine/quadratic limit of the complete-state scalar directional action value, and the costate-weighted dynamics curvature is the exact term a frozen/Gauss--Newton analysis loses. This is useful debugging, but it does not create a distinct architecture or estimator.

The only possible future residuals are:

1. a proof that rank-one Delta permits the complete margin and tail certificate to be computed with strictly less prefix-only state or total FLOPs than general JVP/VJP/DDP/RTRL;
2. a lawful prefix estimator with simultaneous calibration and a same-information advantage over direct action-value prediction;
3. a bound from teacher-forced/common-noise derivatives to the action-dependent free-running law;
4. an action-level causal measurement object.

None is established here.

## 5. Native measurement feasibility

The following existing assets are available only for endpoint falsification:

- AToKe, author repo `Arvid-pku/ATOKE@a1b42e34e4130507220307ced3d681fb8719831f`, exposes `time_true`, `time_new`, `history_evaluation`, `answer` and `new_answer`, but no action-level potential outcomes or pre-action costates.
- SEAL's continual driver records edit/old-question accuracy after sequential self-edits, but its reported setup uses a large model/multiple GPUs and an external judge; it is not authorized or suitable for this math-only phase.
- LongMemEval v1 (https://github.com/xiaowu0162/LongMemEval), LongMemEval v2 (https://github.com/xiaowu0162/LongMemEval-V2), StreamingQA (https://github.com/deepmind/streamingqa ; https://arxiv.org/abs/2205.11388), CITB (https://github.com/hyintell/CITB ; https://arxiv.org/abs/2310.14510) and TRACE (https://github.com/BeyonderXX/TRACE ; https://arxiv.org/abs/2310.06762; packet-pinned commit `462e39f616134f4f819efeb3baea8638c03c7db4`, `metrics.py`) provide memory, temporal or continual endpoints.
- bAbI and LAMBADA provide controlled reasoning/language endpoints. Reused packet pins are ParlAI `a29567f7ce76992fd1f03c51ba9e3b155a37ea51` for bAbI and `lm-evaluation-harness@d6de81643928d653435c431bae19945d41d32520`, `lm_eval/tasks/lambada/lambada_openai.yaml`, for LAMBADA. These assets do not expose a joint pre-action recurrent state, exact action margin/curvature, grounded old/new validity, randomized propensity, paired write/no-write potential outcomes and matched byte/FLOP cost.
- CounterFact/ROME and KnowEdit/EasyEdit measure supplied-target efficacy/generalization/locality, not grounded validity or the causal benefit of taking versus withholding an internal Delta action.

No reviewed native benchmark jointly measures the v2 mechanism. Endpoint behavior can falsify usefulness but cannot verify the certificate decomposition. The missing object remains a measurement gap; no benchmark, label, case, metric, scorer or result is manufactured.

## 6. Audit decision

- Mathematical source support: conditional, subject to independent final-byte review.
- Functional novelty: **MAJOR_COMPONENT_COLLISION / CONTROL_ONLY**.
- Architecture candidate: not admitted.
- Empirical effect: unknown; no execution.
- Attempt status: 2/3 used; park unless a recorded reopen condition gains genuinely new evidence.

All repository inspection was static at the pinned commits. No project/upstream code, software test, training, inference, benchmark scoring, data/model download, GPU work, paid service or Docker action was performed.
