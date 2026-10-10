# R18 v1 — recursive joint-state quotient after exact Delta overwrite

Status: **conditional theorem/control; parked after attempt 1, not an active D candidate**. This versioned child of `R17_PREDICTIVE_QUOTIENT_OVERWRITE.v1.md` repairs a real scope gap: R17's fixed future-query operator is not a recursively closed quotient when later queries, gates, retrieval, auxiliary memory, or updater state depend on the edited state. R18 lifts the analysis to the complete recurrent state and separates an exact global fiber statement, an exact affine finite-horizon theorem, and a merely local nonlinear Jacobian certificate. Classical observability, bisimulation, functional observers, predictive states, and the packet's own full-Jacobian controls cover the main mechanism. The retained contribution is a Delta-specific debugging bridge, not a new updater or an empirical result.

## 1. Original problem, exact patch, and state timing

Let the complete state immediately before the current update be

\[
x_t=(\operatorname{vec}S_t,r_t)\in\mathbb R^n, \tag{1}
\]

where `r_t` includes every recurrent component that can causally affect later keys, values, gates, queries, retrieval, workspace, or updater behavior. With the current lawful prefix and current exogenous input fixed, let

\[
W_t:x_t\mapsto x_t^+ \tag{2}
\]

be the **complete current update**, not only the memory-block assignment. Separately, let `Phi_{t:H}(x_t)` be the declared old/reference behavior over a fixed future exogenous suffix when initialized from the pre-update state. This reference must say whether it omits the destructive write, subtracts a known affine write, or otherwise defines the old behavior being protected. Defining the reference only after the destructive map would make its lost directions invisible by construction.

The exact global question is whether the reference behavior is decodable from the complete updated state. The answer is the fiber condition

\[
\boxed{W_t(x)=W_t(x')\Longrightarrow
\Phi_{t:H}(x)=\Phi_{t:H}(x').} \tag{3}
\]

Equation (3) is equivalent to the existence of a set-theoretic decoder `g` on `range(W_t)` with `Phi_{t:H}=g o W_t`. This is the nonlinear version of R17's kernel factorization. It is recoverability of the declared old behavior, not proof that the deployed update acts as identity on a semantic quotient, identifies which facts remain valid, or uses the decoder.

For fixed current `k,v,D`, unit `k`, and an unchanged side state, the memory block is

\[
S_t^+=(I-kk^\top)DS_t+kv^\top,\qquad
A=(I-kk^\top)D. \tag{4}
\]

If `D` is invertible, the complete update fiber has tangent directions

\[
\mathcal K_t={(\operatorname{vec}(D^{-1}ka^\top),0):a\in\mathbb R^m\}. \tag{5}
\]

But (5) is **not** the general complete-state kernel. If the same current step updates `r_t^+=R(S_t,r_t)`, a lost memory direction `E` survives in the joint state whenever `D_SR[E]` is nonzero. If current `k,v,D` depend on state, all corresponding derivatives also belong in `DW_t`. Thus R18 uses `ker DW_t`; (5) is only the fixed-coefficient, no-side-copy specialization.

If `D` is singular, the memory-block kernel is instead

\[
\{E:DE\text{ has every column in }\operatorname{span}(k)\}, \tag{5a}
\]

which can contain additional `ker D` directions. A pseudoinverse `D^dagger k` does not enumerate it. Cross-block cancellation between memory and auxiliary perturbations can also enlarge the complete kernel. For a non-unit key or separately parameterized write rate, exact projection requires `beta ||k||_2^2=1`; otherwise the map is a partial overwrite and may be invertible.

## 2. Full joint finite-horizon invisible subspace

First fix a nominal reference trajectory and future exogenous suffix. Let the reference dynamics and declared read be

\[
x_{j+1}=F_j(x_j),\qquad y_j=H_j(x_j), \tag{6}
\]

with complete Jacobians

\[
J_j=DF_j(x_j),\qquad C_j=DH_j(x_j). \tag{7}
\]

`C_j` includes the derivative of a state-dependent query/readout; `J_j` includes every path through later keys, values, gates, retrieval, other memory and updater state. Define transition products

\[
\Psi_{u\leftarrow t}=J_{u-1}J_{u-2}\cdots J_t,
\qquad \Psi_{t\leftarrow t}=I, \tag{8}
\]

and the stacked finite-horizon observation derivative

\[
\mathscr O_{t:H}=
\begin{bmatrix}
C_t\\
C_{t+1}\Psi_{t+1\leftarrow t}\\
\vdots\\
C_H\Psi_{H\leftarrow t}
\end{bmatrix}. \tag{9}
\]

The maximal tangent subspace invisible to every declared read through `H` is

\[
\mathcal N_{t:H}=\ker\mathscr O_{t:H}. \tag{10}
\]

It has the backward recursion

\[
\boxed{\mathcal N_{H:H}=\ker C_H,\qquad
\mathcal N_{j:H}=\ker C_j\cap J_j^{-1}\mathcal N_{j+1:H}.} \tag{11}
\]

Proof follows directly: a tangent `delta x_j` is invisible now iff `C_j delta x_j=0`, and invisible later iff `J_j delta x_j` belongs to the next invisible subspace. Induction gives (9)–(11). Therefore the exact local no-extra-aliasing condition for the complete current update is

\[
\boxed{\ker DW_t(x_t)\subseteq\mathcal N_{t:H}
=\ker D\Phi_{t:H}(x_t).} \tag{12}
\]

Equation (12) is necessary and sufficient for **first-order** decodability at the chosen trajectory. When `W_t`, every `F_j`, and every `H_j` are affine, their Jacobians are the maps themselves up to constants, so (12) is the exact finite-horizon factorization condition. For nonlinear maps it is not a finite-edit theorem.

More generally, let `R_t` map the pre-update state into the declared reference state (for example, post-decay but before the destructive write), and let `Psi_ref` be the future read stack beginning there. Then `D Phi=(D Psi_ref)(D R_t)`, and the non-tautological local condition is

\[
\ker DW_t\subseteq\ker\big((D\Psi_{ref})(DR_t)\big). \tag{12a}
\]

Using `(D Psi_ref)(DW_t)` as the protected target would make the inclusion automatic and say nothing about erased old behavior. Decodability is also weaker than direct preservation by the deployed path. In general, if `Psi_dep` is the downstream deployed read stack, direct first-order equality without an extra decoder requires

\[
(D\Psi_{dep})(W_t(x_t))DW_t(x_t)
=(D\Psi_{ref})(R_t(x_t))DR_t(x_t). \tag{12b}
\]

Only when both branches share the same downstream derivative under a common state identification does this reduce to

\[
\operatorname{range}(DW_t-DR_t)\subseteq\ker D\Psi_{ref}. \tag{12c}
\]

and an affine finite theorem must additionally match or lawfully subtract the current write offset. R18 proves the recoverability condition unless this stronger equality is explicitly stated.

Choose any full-row-rank `Q_j` with `ker Q_j=\mathcal N_{j:H}`. Equation (11) implies

\[
J_j\mathcal N_{j:H}\subseteq\mathcal N_{j+1:H},\qquad
\mathcal N_{j:H}\subseteq\ker C_j. \tag{13}
\]

Hence there exist quotient maps `Jbar_j,Cbar_j` such that

\[
Q_{j+1}J_j=\bar J_jQ_j,\qquad C_j=\bar C_jQ_j. \tag{14}
\]

This is the missing recursive closure in R17. It also shows why merely checking one static `ker O` is insufficient when the quotient basis changes with time or the future transition does not descend to it.

## 3. Delta specialization and weighted certificate

Let `L_k:R^m to R^n` inject a value-direction coefficient into the fixed Delta lost tangent:

\[
L_ka=(\operatorname{vec}(D^{-1}ka^\top),0). \tag{15}
\]

Under the assumptions of (5), (12) becomes

\[
\boxed{\mathscr O_{t:H}L_k=0.} \tag{16}
\]

For declared positive-semidefinite output weights `R_j`, define the full joint finite-horizon Gramian

\[
G_{t:H}=\sum_{j=t}^{H}
\Psi_{j\leftarrow t}^{\top}C_j^\top R_jC_j
\Psi_{j\leftarrow t}\succeq0. \tag{17}
\]

Then the weighted squared visible old-behavior change of a lost tangent is exactly

\[
\sum_{j=t}^{H}\|R_j^{1/2}C_j\Psi_{j\leftarrow t}L_ka\|_2^2
=a^\top L_k^\top G_{t:H}L_ka. \tag{18}
\]

Define the weighted invisible space

\[
\mathcal N^R_{t:H}=\ker
\begin{bmatrix}
R_t^{1/2}C_t\\
R_{t+1}^{1/2}C_{t+1}\Psi_{t+1\leftarrow t}\\
\vdots\\
R_H^{1/2}C_H\Psi_{H\leftarrow t}
\end{bmatrix}. \tag{18a}
\]

Then, for positive-semidefinite weights,

\[
\boxed{L_k^\top G_{t:H}L_k=0}
\Longleftrightarrow
\operatorname{range}L_k\subseteq\mathcal N^R_{t:H}. \tag{19}
\]

This equals the unweighted condition `range L_k subseteq N_(t:H)` only when every `R_j` is positive definite on the declared output subspace (equivalently, its square root is injective on the relevant output range). A singular PSD weight can deliberately ignore a visible output component and certifies only the weighted quotient.

R17's memory-only frozen suffix is recovered only when the joint Jacobians have no omitted cross-block paths and the memory block of `Psi` equals R17's ordered `P_u`. The difference is not a new metric: it is whether the derivative is taken through the full recurrent computation.

## 4. Old counterexamples rechecked and new witnesses

### Frozen-path false safety

Let the complete state be `(s,h)`, and let exact overwrite replace scalar `s` by a constant while leaving `h` unchanged. In the old/reference path set

\[
h_{t+1}=h_t+\gamma s_t,\qquad y_{t+1}=h_{t+1}. \tag{20}
\]

A memory-only frozen read that holds `h` fixed sees no direct future query of `s` and can assign zero Gram to the erased direction. The complete Jacobian has `partial h_{t+1}/partial s_t=gamma`; hence `C_{t+1}J_t(1,0)^T=gamma`. For nonzero `gamma`, (12) fails. The omitted cross-block, not the algebra of R17's fixed operator, causes the false safety conclusion.

### Memory-block false destruction

At the current step instead set `s^+=0` and `h^+=s`, with the declared old quotient equal to `s`. Although the memory block erases `s`, the complete update retains that threatened quotient because the value is copied into `h^+`; `(1,0)` is not in `ker DW_t`. This is not global injectivity—the old `h` direction is discarded—and a mixed cross-block map can still have cancellation directions. A no-go based only on `ker A` would overstate loss. The side state and its precision/cost must be charged; this construction is just an auxiliary ledger unless it has another matched-budget benefit.

### Local certificate is not global

Replace (20) by `h_{t+1}=h_t+s_t^2` and linearize at `s_t=0`. The full first-order cross derivative is zero, so every tangent test in (12) passes, while finite states `s=0` and `s=epsilon` are merged by overwrite but have reference outputs differing by `epsilon^2`. Thus a pointwise Jacobian kernel condition cannot certify finite nonlinear fiber constancy.

Even an injective derivative away from singular points is not a global test. With `W(s)=s^2` and old behavior `Phi(s)=s`, `DW(s)` has zero kernel for every `s != 0`, yet `s` and `-s` are globally aliased by `W` and have different old behavior. Pointwise rank therefore cannot replace checking complete fibers.

For a smooth constant-rank `W_t`, annihilating `D Phi` on the vertical tangent `ker DW_t` at every point makes `Phi` constant on each connected component of a regular update fiber. Disconnected fibers or singular points still require a global check. Equivalently, a global recursively usable quotient relation must preserve outputs and be forward invariant under every allowed future input/action; that is a bisimulation/congruence obligation, not a consequence of one nominal Jacobian.

### Horizon and free-running boundaries

Extending the horizon adds block rows to (9), so `N_{t:H+1} subseteq N_{t:H}`. Finite-horizon safety does not imply unbounded safety. A teacher-forced suffix also fixes future tokens/actions. If the edit changes their distribution, the nominal `J_j,C_j` describe only the fixed-descendant path; free-running effects require a lawful environment/policy model, overlap or counterfactual interaction. Diffusion or self-generated continuations do not create external evidence.

For a state-dependent linear read `y=q(x)^T S`, `C_j` contains both `q^T delta S` and `(Dq[delta x])^T S`. Hard top-k routing, argmax and sampled discrete transitions may be nondifferentiable; an almost-everywhere-zero Jacobian can miss a finite route switch. R18's tangent certificate does not cover such switches without a separately declared generalized or finite-difference analysis.

## 5. Computation, information, and strongest simple controls

Let `n` be the dimension of the complete recurrent state. Explicitly forming all dense `J_j` and a full Gramian can cost `O(H n^3)` by naive matrix products and `O(n^2)` state; stacked observability construction is similarly prohibitive. Matrix-free JVP/VJP can test `m` known Delta-lost basis directions in `O(mH)` full-network derivative passes, but must also charge suffix generation, activation checkpoint/recompute or replay storage, and rank-revealing coverage if an exact nullspace claim is made. Krylov/random probes provide approximations rather than exact kernel certificates. A rank-`r` quotient basis costs `O(nr)` unless fixed or generated, and updating a time-varying basis adds its own metadata, conditioning, and precision cost.

The strongest same-information controls are:

1. direct full-joint unrolled JVP/VJP sensitivity on the threatened directions;
2. directly store and propagate sufficient coordinates `Q_jx_j` using (14);
3. a protected-value/auxiliary ledger when the threatened read family is known;
4. no-write, partial overwrite, or ordinary soft preconditioning when the certificate is too expensive.

The direct side-channel lower bound makes the comparison explicit. Let the columns of `K` span `ker DW_t` and let `Q=D Phi_{t:H}`. Augmenting the update with a linear side code `Mx` recovers the local old quotient iff

\[
\ker DW_t\cap\ker M\subseteq\ker Q. \tag{21}
\]

The smallest real-valued side-code dimension is

\[
\boxed{r_{lost}=\operatorname{rank}(QK).} \tag{22}
\]

Indeed, on `ker DW_t` the code must separate the quotient by `ker Q`, whose dimension is `rank(QK)`. The bound is attained by choosing `r_lost` independent linear functionals whose restrictions to `ker DW_t` span the row space of `Q|_(ker DW_t)`; this constructs the side-code map rather than merely naming a basis of the image. This is a real-linear dimension statement, not a finite-bit lower bound, and it is exactly the direct sufficient-coordinate/syndrome control already represented by R12.

R18 does not identify `Q_j` causally at deployment. A bank built from future suffixes is training/audit information, not a lawful online oracle. Post-overwrite adaptive internal probes cannot recover two old states already mapped to the same complete state: by induction they receive the same internal transcript. Pre-overwrite probe responses that are retained are extra side state and must be compared with directly retaining the protected values.

## 6. Distinguishing predictions and measurement boundary

The theorem makes four conditional predictions:

1. When R17's frozen Gram is zero but a full cross-block product in (9) is nonzero, a perturbation along the exact overwrite kernel can alter the declared reference future behavior; the discrepancy should track the omitted joint path.
2. When a side-state current-update block makes `DW_tL_k` nonzero, the matrix block may erase a direction without the complete update merging it; charging that side state removes the apparent contradiction.
3. Equation (19) by itself certifies only the weighted behavior of the fixed Delta-lost subspace. Under specialization (5), where `range L_k=ker DW_t`, and when every `R_j` is injective on the relevant declared output range so `N^R_(t:H)=N_(t:H)`, (19) is equivalent to (12); for an affine finite-horizon reference the full declared old behavior is then exactly factorable through the complete updated state. In a nonlinear model the same zero is only first-order unless the global fiber/congruence condition (3) is checked.
4. Increasing the declared horizon or output family can only shrink the invisible subspace and can turn the same overwrite from locally admissible to inadmissible.

bAbI, LAMBADA, RULER, BABILong and LongMemEval expose answer/token/retrieval endpoints, not paired pre-update joint states, complete current-update fibers, `J_j,C_j`, the backward invisible subspace, or a native scorer for (12). They may later test behavior of an implementation, but they cannot natively attribute a gain to recursive quotient closure or distinguish it from extra state/retrieval. The generative audit in the predictive-fiber source requires reset/probe access beyond these established native interfaces. This remains a measurement gap; no benchmark, label, metric, or result is invented.

## 7. Closest work, retained value, and disposition

Linear observation quotients, invariant unobservable subspaces, functional observers, and exact bisimulation already provide (11)–(14) in general systems language. Nonlinear bisimulation supplies the global forward-congruence requirement; predictive fibers and predictive-state representations supply full-future behavioral quotients. Wang's depth-indexed predictive fibers directly capture finite-horizon depth loss, and Li et al.'s recurrent behavioral memory explicitly separates instantaneous sufficiency from right-congruent recursive state. Project-internal `R01-v2`, `R12`, `R13`, `STEP2_REENTRY`, `STEP2_RECURSIVE_RANDOM_METRIC_CONTROL`, and R17 already cover quotient closure, direct sufficient coordinates, dynamic covectors, complete Jacobians, and the one-step overwrite kernel.

The useful residual is narrow but concrete: the fixed memory-block overwrite kernel may be either rescued by a same-step side-state path or exposed by a later endogenous cross-block, and the correct local decision is the inclusion of the **complete current-update kernel** in the **complete recursively invisible subspace**. This corrects two opposite overclaims without deleting R17's theorem or counterexamples.

**Decision:** park after substantive attempt 1. Add zero active, scientifically admitted, or selected candidates. Reopen only if a lawful prefix-only construction computes a stable full-joint quotient below the matched total cost of direct sufficient-coordinate storage/JVPs, remains valid beyond one nominal suffix, and yields a native measurable prediction not already implied by observability, bisimulation, predictive fibers, or PSR. Changing the horizon, probe count, quotient basis, or Jacobian approximation alone is not a new repair.
