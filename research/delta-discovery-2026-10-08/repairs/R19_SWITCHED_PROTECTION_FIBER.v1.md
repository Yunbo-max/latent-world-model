# R19 v1 — switched protection fibers and the release-jump obstruction

Status: **conditional theorem/control; parked after substantive attempt 1; not an active D candidate**. Exact-byte review status is recorded in the companion review artifacts. This versioned child joins three previously separate, correct controls: fixed-fiber contraction from `STEP2_COUPLED_UPDATER_STABILITY.md`, transported numerical protection from R13, and evidence-dependent release from R08. The repair supplies the missing cross-mode condition. It does not decide factual validity, prove learning efficiency, or report an experiment.

## 1. Original problem and concrete patch

Let `h` denote a perturbation of the complete recurrent state, including `vec(S)`, updater state, queues, routing state and every component that can affect later updates. A protection mode `sigma` declares which differences are neutral/protected and which transverse differences should contract. Represent its transverse energy by

\[
V_\sigma(h)=h^\top P_\sigma h,
\qquad P_\sigma\succeq0. \tag{1}
\]

The nullspace of `P_sigma` is deliberate: it contains state differences that the fixed-mode transverse certificate does not penalize, such as exactly retained protected coordinates. This is a seminorm, not a full-state Lyapunov norm.

For the complete within-mode tangent map `J_{sigma,t}`, assume the checked fixed-mode inequality

\[
J_{\sigma,t}^\top P_\sigma J_{\sigma,t}
\preceq \rho_\sigma^2 P_\sigma,
\qquad 0\leq\rho_\sigma<1. \tag{2}
\]

Equation (2) already implies `J_(sigma,t) ker(P_sigma) subseteq ker(P_sigma)`: a zero-energy protected difference cannot leak into the measured transverse coordinates while this certificate holds. It is the quadratic form of fixed-fiber contraction, not a claim that the protected fact remains semantically valid.

Suppose evidence/action logic changes protection mode from `sigma` to `tau`. Let `R_(tau,sigma)` be the derivative of the **complete** reset/transfer relation at that switch, including every state component; `R=I` means the state is retained and only its interpretation changes. A purely multiplicative multiple-energy proof needs a finite `mu_(tau,sigma)` satisfying

\[
R_{\tau\sigma}^\top P_\tau R_{\tau\sigma}
\preceq \mu_{\tau\sigma}P_\sigma. \tag{3}
\]

R19 derives exactly when (3) exists, what fails under release, and the minimum information that an honest repair must add.

## 2. Exact cross-mode condition and sharp factor

Let

\[
A_{\tau\sigma}=R_{\tau\sigma}^\top P_\tau R_{\tau\sigma}\succeq0. \tag{4}
\]

There exists a finite `mu` in (3) **if and only if**

\[
\boxed{\ker P_\sigma\subseteq\ker A_{\tau\sigma}}
\quad\Longleftrightarrow\quad
P_\tau^{1/2}R_{\tau\sigma}\ker P_\sigma=\{0\}. \tag{5}
\]

Necessity is immediate: if `h in ker(P_sigma)`, the right side of (3) is zero, so positive semidefiniteness forces `h^T A h=0`, equivalently `A h=0`. For sufficiency, (5) makes `A` vanish on the kernel of `P_sigma`; in the orthogonal decomposition `range(P_sigma) plus ker(P_sigma)`, the generalized Rayleigh quotient is finite. The smallest legal factor is

\[
\boxed{
\mu_{\tau\sigma}^*
=\lambda_{\max}\!\left(
P_\sigma^{\dagger/2}
A_{\tau\sigma}
P_\sigma^{\dagger/2}
\right),}
\tag{6}
\]

where the eigenvalue is taken on `range(P_sigma)`; the displayed full-space matrix has zeros on its orthogonal complement. Thus the usual cross-mode multiplier is not merely a tunable constant. With semidefinite protection energies it may be infinite.

### Release-jump obstruction

Releasing protection normally shrinks the ignored kernel. With identity reset, if

\[
\ker P_\tau\subsetneq\ker P_\sigma, \tag{7}
\]

choose `h in ker(P_sigma) \ ker(P_tau)`. Then `V_sigma(h)=0` but `V_tau(h)>0`, so no finite `mu` can satisfy (3). More generally the same obstruction occurs whenever `R h` is newly transverse. This does **not** say release is invalid. It says the old transverse certificate contains no magnitude information about a direction it intentionally treated as free.

The two-dimensional witness is exact. Let

\[
P_0=\begin{bmatrix}0&0\\0&1\end{bmatrix},\quad
J_0=\begin{bmatrix}1&0\\0&\rho\end{bmatrix},\quad
P_1=I,\quad J_1=\rho I,
\qquad 0<\rho<1. \tag{8}
\]

Each mode satisfies its own version of (2). For `R_(1,0)=I` and `h=e_1`, however, `V_0(h)=0` and `V_1(Rh)=1`. No finite cross factor exists. Replacing the reset by `R=diag(0,1)` makes (3) hold with `mu=1`, but it does so by erasing the newly released coordinate. A useful release must therefore transfer or bound that coordinate rather than hide this cost.

## 3. Switched finite-horizon theorem

For a mode sequence `sigma_0,...,sigma_T`, let a complete tangent step consist of the within-mode map followed by the declared switch/reset,

\[
h_{t+1}=R_{\sigma_{t+1},\sigma_t,t}
J_{\sigma_t,t}h_t. \tag{9}
\]

Here and throughout this child, a non-switch step has no separate reset:

\[
R_{\sigma\sigma,t}=I. \tag{9a}
\]

If an implementation applies a nontrivial same-mode reset, its own comparison factor must be included at every such step; equations (10), (12), and (16) cannot omit it.

If (2) and (3) hold at every step, direct multiplication gives

\[
\boxed{
V_{\sigma_T}(h_T)
\leq
\left(\prod_{t=0}^{T-1}\rho_{\sigma_t}^2\right)
\left(\prod_{t:\sigma_{t+1}\neq\sigma_t}
\mu_{\sigma_{t+1},\sigma_t,t}\right)
V_{\sigma_0}(h_0).}
\tag{10}
\]

No commutation is used; the factors follow the realized order. If `rho_sigma<=rho<1`, every switch factor is at most `mu>=1`, and the number of switches satisfies the average-dwell bound

\[
N(T)\leq N_0+T/\tau_a, \tag{11}
\]

then

\[
V_{\sigma_T}(h_T)
\leq \mu^{N_0}
\left(\rho^2\mu^{1/\tau_a}\right)^T
V_{\sigma_0}(h_0). \tag{12}
\]

Thus this certificate contracts only when `rho^2 mu^(1/tau_a)<1`. A posterior threshold, hysteresis rule or slow release clock does not by itself prove (3), and dwell time cannot repair an infinite release multiplier.

Equations (9)--(12) are exact for the declared linear tangent/switched system. For a nonlinear recurrent model they are local unless the quadratic inequalities hold uniformly on a forward-invariant domain and the **complete nonlinear reset relation** obeys the corresponding finite-state comparison bounds. A reset Jacobian alone is not a global reset bound. If mode selection depends on the state, the result applies only inside a positive-margin common branch/local invariant region where both compared trajectories follow the same certified mode sequence. At a selector guard, an ordinary Jacobian need not exist; if the trajectories take different branches, (10) does not apply. A valid extension must include the selector/guard and reset as a piecewise or hybrid relation (and, for continuous-time event linearization, the appropriate saltation map). Discrete routing cannot be silently differentiated through. For example, `sigma(h)=1[h_1>=0]` has arbitrarily close states on different branches at `h_1=0`, despite valid within-branch inequalities.

## 4. Repair when the old energy is blind

Let `K_sigma` have **orthonormal** columns spanning `ker(P_sigma)`. The newly exposed image at a switch is

\[
B_{\tau\sigma}=P_\tau^{1/2}R_{\tau\sigma}K_\sigma. \tag{13}
\]

When `B` is nonzero, a valid bound must add information. Take a rank factorization

\[
B_{\tau\sigma}=D_{\tau\sigma}Q_{\tau\sigma},
\qquad
Q_{\tau\sigma}\in\mathbb R^{r_{rel}\times \dim\ker P_\sigma},
\tag{13a}
\]

where `D` has full column rank and `Q` has full row rank. Define the minimal kernel-coordinate code

\[
C_{\tau\sigma}=Q_{\tau\sigma}K_\sigma^\top. \tag{13b}
\]

Then for every old-kernel perturbation `h=K_sigma z`, the newly exposed image is recovered exactly as
`P_tau^(1/2) R h = D C h`. More generally, a code `C` supports a finite quadratic bound exactly when

\[
\ker P_\sigma\cap\ker C_{\tau\sigma}
\subseteq
\ker(P_\tau^{1/2}R_{\tau\sigma}),
\tag{13c}
\]

equivalently `ker(C K_sigma) subseteq ker(B)`. Under (13c), finite-dimensional generalized-Rayleigh comparison gives finite `mu,nu` such that

\[
V_\tau(Rh)
\leq \mu V_\sigma(h)+\nu\|C_{\tau\sigma}h\|_2^2, \tag{14}
\]

where `C` is a causally available released-coordinate ledger or certified bound. Conversely, on unrestricted local perturbations in `ker(P_sigma)`, any `p`-coordinate linear code with an exact linear decoder for the newly exposed image satisfies `B=D_c(CK_sigma)` and therefore needs

\[
\boxed{r_{rel}=\operatorname{rank}
(P_\tau^{1/2}R_{\tau\sigma}K_\sigma)} \tag{15}
\]

real coordinates, since `rank(B)<=rank(CK_sigma)<=p`. The construction (13a)--(13b) attains the bound with `p=r_rel`. This is only a local linear statement for unrestricted old-kernel perturbations and an exact linear code/decoder, not a bit bound; precision, basis, decoder and mode metadata still count.

With (14), the switched recursion gains additive release injections. Put `g_t=J_(sigma_t,t)h_t`, define

\[
\alpha_t=\rho_{\sigma_t}^2
\begin{cases}
\mu_{\sigma_{t+1},\sigma_t,t},&\sigma_{t+1}\neq\sigma_t,\\
1,&\sigma_{t+1}=\sigma_t,
\end{cases}
\qquad
u_t=\nu_t\|C_tg_t\|_2^2
\tag{16a}
\]

at actual switch times and `u_t=0` otherwise. The scalar affine recursion is `V_(t+1)<=alpha_t V_t+u_t`, hence

\[
\boxed{
V_T\leq
\left(\prod_{t=0}^{T-1}\alpha_t\right)V_0+
\sum_{s=0}^{T-1}
\left(\prod_{j=s+1}^{T-1}\alpha_j\right)u_s.}
\tag{16}
\]

An empty product is one. Equation (16) exposes rather than deletes the cost of release; bounding `u_s` still requires the released-coordinate ledger or an independently valid magnitude bound.

Three concrete repairs therefore exist, each with a price:

1. keep a common positive-definite energy across all modes, losing exact neutral protected directions and often making strict contraction incompatible with exact retention;
2. use a reset that maps every old null direction into the new nullspace, which may erase or externally transfer the released content;
3. carry the `r_rel` newly exposed coordinates or a conservative bound and include their injection in (16).

Changing only the posterior threshold, gate name or time scale cannot replace these conditions.

## 5. Delta specialization and old-result recheck

For a key-by-value memory and fixed protected queries `L_sigma vec(S)`, the Step2 protected-fiber coordinates place exact retained differences in the neutral block and the memory/updater adaptation in the transverse block. The complete `J_(sigma,t)` must include state-dependent `k,v,beta,D`, updater state and delayed-feedback paths. Checking only `I-beta kk^T` is insufficient.

R13 remains correct: a fixed numerical protected read can be transported through an affine Delta step only under its kernel condition, and a direct value ledger is the strongest simple exact control. R19 asks a different question. Even if each mode separately has a valid transported read and transverse contraction, moving a direction from protected to adaptive changes the kernel of the energy. Equation (5), not the two within-mode proofs, decides whether the switch certificate composes.

R08 also remains correct: evidence can make release Bayes-optimal once switching cost and continuation value are counted. R19 adds that the continuation cost must include a finite cross-mode factor or the released-coordinate term. It does not supply the missing truth label, hazard, action propensity or external outcome.

The exact-overwrite obstruction is preserved. If a protected direction was already merged by the complete update and no side state retained it, changing mode later cannot recover it. Conversely, a side state that retained it can support release, but its state and precision are precisely the ledger cost in (15).

## 6. Predictions, failure boundaries, and simple controls

Conditional predictions:

1. A release that newly measures a previously neutral direction will make any old-energy-only multiplicative certificate fail, even when every mode is separately transversely contractive.
2. If the kernel condition (5) holds, measured release transients are bounded by the ordered product (10); increasing switch frequency worsens the conservative bound according to (12).
3. When (5) fails, a direct ledger with dimension `r_rel` is sufficient for the local newly exposed image and no lower-rank exact linear ledger can determine it on the old kernel.
4. A reset that appears to restore stability by annihilating released coordinates should also erase their downstream contribution unless an external transfer stores it elsewhere.

Failure boundaries:

- the theorem conditions on a lawful mode sequence and does not identify obsolete facts;
- pointwise Jacobians do not certify finite nonlinear edits, route switches or free-running distribution changes;
- a PSD energy can ignore behaviorally important directions by construction, so its kernel must be declared;
- average dwell time controls switch frequency, not semantic release error or an infinite jump factor;
- `r_rel` counts real linear coordinates, not bits, FLOPs or a learned basis;
- nonnormal transient output amplification can remain inside a quadratic upper bound and may make the certificate loose;
- external feedback responsiveness and later-task learning efficiency remain unproved.

Strong same-information controls are: never release/fixed protection; no-write or partial overwrite; R08's direct Bellman/POMDP decision; R13's direct protected-value ledger; a common full-state Lyapunov metric; classical multiple-Lyapunov/dwell-time certification; and replay/external storage when the released fact must be reconstructed.

## 7. Cost, measurement, closest work, and disposition

For complete state dimension `n`, a dense `P_sigma` costs `O(n^2)` state and quadratic application; a rank-`r` factor costs `O(nr)` plus mode and calibration metadata. Cross-factor estimation is a generalized eigenvalue problem on the measured subspace. A released ledger costs at least `r_rel` real coordinates locally, plus precision/decoder; determining semantic validity or a switching policy requires separate evidence and state. Full-network uniform certificates are much more expensive than a local JVP.

Existing bAbI, LAMBADA, RULER, BABILong and LongMemEval endpoints do not expose `P_sigma`, switch/reset tangents, cross-mode kernels or released-coordinate truth. AToKe-like temporal labels and continual-edit endpoints can test downstream release behavior of a future implementation but do not natively score (5), identify its cause, or provide paired same-state mode interventions. This is a measurement gap, not an invented benchmark.

Multiple-Lyapunov and average-dwell-time theory already covers the product mechanism in (10)--(12). Functional observers, sufficient-coordinate ledgers and the project's R12/R13/R18 cover the side-information/rank mechanism. R08 and known temporal model-editing/release work cover evidence-dependent switching. The scoped retained value is the exact warning that **semidefinite protected-fiber certificates do not compose across a release unless their kernels are compatible**, together with the Delta-state ledger cost of repairing that jump.

**Decision:** park after substantive attempt 1 with zero candidate increment. Exact-byte math, source/distinctness and adversarial review verdicts are bound in companion review artifacts. Reopen as a method only if a lawful Delta-specific representation makes the cross-mode factor or released-coordinate ledger strictly cheaper than direct protected values/common-metric controls at matched total state and compute, while also providing identifiable release evidence and a native measurable consequence. Empirical effect remains unknown.
