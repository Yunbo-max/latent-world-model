# R09 v2 dynamic-Gramian source, novelty, implementation, and measurement audit

Audit scope: `repairs/R09_DYNAMIC_PROTECTION_GRAMIAN.v2.md`. Primary-formula and fixed-interface review only; no imported/executed code, model/data download, training, inference, scoring, or benchmark run.

## 1. Preserved R09 v1 evidence

R09 v1 and its source/reviews remain unchanged on literal main. Its audit is `sources/REPAIR_R09_OVERWRITE_PROTECTION_SOURCE_AUDIT.md`, SHA256 `c74e96dcc7c19f9b9fd8a1e261f839b5c81002cf9340fa8452adc20a24408c01`. It pins Original/Parallel DeltaNet, Preconditioned DeltaNet (PDN), Gated KalmanNet, OWM, GEM/A-GEM/OGD/EWC, AlphaEdit/O-Edit/AlphaEdit+, Rank-Greville/QR-RLS, and native endpoint assets. The v1 conclusion remains: normalized inverse metrics, projection, and soft conflict geometry are established baselines; the bounded Delta-specific Pareto certificate is useful but not a new updater.

The v2 child receives fresh review because its object changes from a static metric to a transported finite-horizon metric and a prefix minimax theorem.

## 2. Direct dynamic-control collisions

### Finite-horizon observability/energy Gramian

For a linear time-varying perturbation `delta z_{j+1}=A_{j+1} delta z_j` and quadratic output `delta z_j^T Q_j delta z_j`, the sum of transported forms `sum Phi^T Q Phi` is the standard finite-horizon observability/energy Gramian. R09 v2 equation (1) is this object restricted through the rank-one Delta injection. Its recursion `G_j=Q_j+A_{j+1}^T G_{j+1}A_{j+1}` is the finite-horizon discrete Lyapunov recursion, derived directly in the artifact.

Primary neighboring sources:

- B. C. Moore, **Principal Component Analysis in Linear Systems: Controllability, Observability, and Model Reduction**, *IEEE Transactions on Automatic Control* 26(1), 1981, DOI `10.1109/TAC.1981.1102568`. This is classical Gramian/balanced-realization machinery.
- Sanjay Lall, Jerrold E. Marsden, and Sonja Glavaski, **A Subspace Approach to Balanced Truncation for Model Reduction of Nonlinear Control Systems**, *International Journal of Robust and Nonlinear Control* 12, 2002, DOI [`10.1002/rnc.657`](https://doi.org/10.1002/rnc.657). The paper extends controllability/observability covariance construction using simulated/experimental trajectories and reduces to linear balanced truncation in the linear case.
- Yu Kawano and Jacquelien M. A. Scherpen, **Empirical Differential Gramians for Nonlinear Model Reduction**, [`arXiv:1902.09836v2`](https://arxiv.org/abs/1902.09836v2), Section 3.1 equations (4)--(6), Definition 3.2 equation (8), and Section 4.1. Its differential/variational observability construction is a direct pullback-of-output-sensitivity neighbor.

These sources block any claim that transported sensitivity energy or a Gramian recursion is new. R09's only specialization is the explicit current-key affine constraint and Delta residual factor.

A closer nonlinear/variational collision is Kazma and Taha, **Observability for Nonlinear Systems: Connecting Variational Dynamics, Lyapunov Exponents, and Empirical Gramians**, [`arXiv:2402.14711v7`](https://arxiv.org/abs/2402.14711v7), revised 2 August 2026. Proposition III.1 equations (10a)--(10b) define variational state/output maps; Remark III.1 equation (13) gives the ordered transition-Jacobian product; Proposition III.2 equations (14)--(16) give `V_o=Psi^T Psi`, the stacked `Psi`, and its chain-rule form; Corollary III.1 equations (17)--(18) reduce to the linear observability Gramian. The author repository is pinned at `mhkazma/ObsNonSys-VarGram@2bb5060454ddc63cd57681355fa6300fb9c6dc2e`. `AVarObsGram.m`, blob `d2c548fe310b3e76463e5524a476199f5c482d8a`, constructs ordered `Phi_0_k`, sets `Psi_0_k=C*Phi_0_k`, and computes `Wo_M{idx2}=Psi'*Psi`; `AVarDyn.m`, blob `da73adbc53352c9a4eb24f8ae45b0bdb5677fe62`, evaluates `A_x=modelVar.jacobian(x)` and evolves `ddelta_xdt=A_x*delta_x`. This is the same transported-Jacobian quadratic pattern as R09 v2 before the Delta affine constraint is imposed. Static inspection only; no code was run.

### DDP/iLQR and complete-state value curvature

Tassa, Erez, and Todorov, **Synthesis and Stabilization of Complex Behaviors through Online Trajectory Optimization**, IROS 2012, primary PDF [`https://roboti.us/lab/papers/TassaIROS12.pdf`](https://roboti.us/lab/papers/TassaIROS12.pdf), Section II.A--B, equations (1)--(8): Bellman recursion, local quadratic `Q`, affine control, and backward value recursion. Full DDP contains costate contractions with second derivatives of dynamics; iLQG/iLQR drops them.

R09 v2's frozen or Gauss--Newton Gramian is therefore a known approximation branch. R07 v2 already records the exact complete-state first/second directional derivatives and pinned differentiable-MPC implementation. V2 explicitly imports that boundary rather than claiming a full nonlinear certificate.

### Adaptive/online control does not make future geometry free

Dean, Mania, Matni, Recht, and Tu, **Regret Bounds for Robust Adaptive Control of the Linear Quadratic Regulator**, NeurIPS 2018, [`arXiv:1805.09388`](https://arxiv.org/abs/1805.09388) and [proceedings PDF](https://papers.neurips.cc/paper/7673-regret-bounds-for-robust-adaptive-control-of-the-linear-quadratic-regulator.pdf), derives regret under explicit dynamics, stability, noise, exploration, and estimation conditions. Hazan et al., **Logarithmic Regret for Online Control**, [`https://research.google/pubs/logarithmic-regret-for-online-control/`](https://research.google/pubs/logarithmic-regret-for-online-control/), likewise assumes a declared online-control setting.

Simchowitz and Foster, **Naive Exploration is Optimal for Online LQR**, ICML 2020, [primary paper](https://proceedings.mlr.press/v119/simchowitz20a/simchowitz20a.pdf), and Chen, Molloy, Summers, and Shames, **Regret Analysis of Online LQR Control via Trajectory Prediction and Tracking**, L4DC 2023, [primary paper](https://proceedings.mlr.press/v211/chen23a/chen23a.pdf), additionally make exploration or preview/prediction assumptions explicit. These are not direct Delta algorithms, but they show that learning a useful future control metric requires declared system, variation, excitation, or preview conditions and paid observations. They do not justify estimating an unrestricted autoregressive suffix from a prefix.

## 3. Internal collision: R20 v3 is exact

`repairs/R20_SPECTRAL_TRANSFER_CERTIFICATE.v3.md` already proves, for a shared affine constraint and a two-sided relative spectral premise, the sharp Kantorovich factor

`(M+m)^2/(4Mm)`

and the symmetric-radius factor `1/(1-delta^2)`. It also proves that no prefix-measurable rule can certify a nonvacuous sandwich over unrestricted identical-prefix continuations. R09 v2's equation (8) is a specialization to the transported protection Gramian; equation (10) makes the identical-prefix obstruction concrete with swapped anisotropy and shows ordinary Delta is minimax on that two-world family.

This is a useful lineage repair and cross-check, but not a new spectral method.

## 4. Inverse-metric and editing collisions remain

- PDN, arXiv:2604.21100v1, theory Sections 2.3--3.5/Theorem 3.1, uses a normalized inverse historical Gram matrix; the author implementation pinned by v1 uses a diagonal bounded practical approximation rather than the full theoretical inverse.
- AlphaEdit, O-Edit, and AlphaEdit+ use covariance/nullspace or softened conflict geometry to reduce damage to retained associations.
- OWM, GEM/A-GEM/OGD/EWC, and RLS/QR-RLS are established protection/preconditioning controls.

Replacing their static geometry by a transported query Gramian is mathematically natural, but its general form is already observability/value-Hessian machinery. No author code is attributed to R09.

### Closest Delta-specific uncertainty baseline: Kalman Delta Networks

Bui, Huang, and Ying, **Kalman Delta Networks: Uncertainty-aware Associative Memory**, [`arXiv:2609.07816v2`](https://arxiv.org/abs/2609.07816v2), revised 29 September 2026, is a mandatory direct baseline. Equations (5)--(6) formulate latent associative memory as a linear--Gaussian state-space model; Proposition 3.1 equation (7) gives the exact Kalman predict/update recursion and gain, including predictive covariance

`P_hat_t = D_t P_{t-1} D_t^T + Omega_t`,

and the Kalman gain `kappa_t=P_hat_t k_t/(r_t+k_t^T P_hat_t k_t)` in the residual write. Equation (8) recovers the fixed-gain Delta family from an isotropic surrogate. Diagonal KDN starts at equations (9)--(10); its later parameterization, prediction, and gain appear in equations (18)--(20), with the reverse-KL diagonal projection and associative uncertainty scan developed in the intervening derivation. Isotropic KDN's scalar retained uncertainty and gain are summarized in Proposition E.2, equations (61)--(63). Thus KDN directly addresses overwrite/protection before unknown future queries with accumulated past-evidence uncertainty, dense Riccati geometry in the ideal filter, and diagonal/isotropic scan-compatible approximations.

This is not R09 v2's object. KDN's `P_t` is a filtering covariance for uncertainty about the current latent key--value map under the declared state-space model. R09 v2's `G_{t:H}` is an action-relevant pullback of declared future protected-query/value curvature through a suffix. KDN therefore strengthens the same-information baseline and further blocks any broad claim that covariance-aware Delta overwrite control is new, but it neither supplies the unseen future-sensitivity Gramian nor defeats R09's identical-prefix swapped-anisotropy lower bound.

The author repository is pinned at `ngocbh/kalman-delta-networks@53e437be8591521a508bb6a04cd5b26594a3d5ec` (27 September 2026). The README blob `51789ff1e0aeca398ba550c8c34c31ba719ec111` states the retained full associative-memory matrix and the isotropic/diagonal uncertainty states. `lit_gpt/diag_kdn.py`, blob `1b4fbc230d2f2f8a51ef52a2880ae3fcc9cc2fe9`, routes learned retention/process-noise/observation-noise quantities through `_diag_kdn_gain` and `chunk_kalman`; `lit_gpt/iso_kdn.py`, blob `862b7002a7148681a26de18c4a8b4559914334e0`, uses the scalar `iso_kdn_gain` path. Static interface inspection only; no repository code was executed.

## 5. Native measurement feasibility

The v2 claim needs a record containing, before the write, the complete recurrent state, the legal action, the action-indexed transition/Jacobian law or a calibrated continuation distribution, protected stage metric, and a matched-cost comparator. To identify action utility rather than retrospective displacement it additionally needs randomized propensities or lawful off-policy assumptions and grounded old/new validity.

The packet-pinned assets have narrower native objects:

- AToKe supplies time-conditioned old/current facts and endpoint QA fields, not pre-action Jacobians or action propensities.
- CounterFact/ZSRE and KnowEdit/EasyEdit supply prescribed edit efficacy/generalization/locality endpoints, not grounded action value.
- LongMemEval supplies long-context memory endpoint scoring, not per-write transition Gramians.
- SEAL reports continual self-edit outcomes but does not expose paired Delta write/no-write potential outcomes or this per-action Gramian.
- bAbI and LAMBADA provide reasoning/language endpoints, not recurrent-state curvature labels.

These assets can falsify endpoint usefulness after a policy is implemented. They do not natively identify equations (5)--(8). No benchmark, label, metric, case, scorer, or result is manufactured.

## 6. Novelty and disposition

| Component | Coverage | R09 v2 residue |
|---|---|---|
| transported quadratic / Gramian recursion | classical linear systems and model reduction | Delta affine-write specialization |
| complete-state value curvature | DDP/iLQR/differentiable control | explicit warning against frozen-suffix overclaim |
| normalized inverse metric | PDN/RLS/projection/editing controls | dynamic metric inserted into v1 frontier |
| covariance-aware Delta overwrite protection | Kalman Delta Networks | future protected-query pullback and same-prefix lower bound, not filtering covariance |
| spectral transfer | R20 v3 and sketch/Newton literature | swapped-future R09 specialization |
| prefix identifiability | R20/R05/R08 controls | exact two-world minimax ordinary-Delta result |

Decision: **source-supported conditional theorem/control; major mechanism collision; no candidate upgrade**. Mathematical correctness still requires independent final-byte review. Empirical effect remains unknown because no execution occurred. Reopening requires a Delta-specific causal estimator/cost theorem or a native action-level measurement object, not another name for a Gramian, Lyapunov solve, or value Hessian.

A bounded primary-source and author-code search through **2026-10-11** found Kalman Delta Networks as a close Delta-specific covariance baseline, but found no exact prefix-causal estimator that supplies the unseen **future protected-query pullback Gramian** with a matched-cost guarantee over KDN and the other listed controls. This narrower statement is a bounded negative search result, not an exhaustive field search or an originality proof.
