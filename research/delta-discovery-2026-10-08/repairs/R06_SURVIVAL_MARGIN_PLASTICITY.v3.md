# R06 v3 — survival-margin audit certificate and plasticity boundary

Status: **conditional theorem/control; substantive repair attempt 3/3; not an active candidate; no experiment executed**. This versioned child preserves R06 v1/v2 and their counterexamples byte-for-byte. It repairs only the remaining question: when can the one-sided prefix envelope be changed into a genuine two-sided continuation law without reading the future?

## 1. Original problem, failure type, and patch

In key-by-value convention, the frozen-feature Delta recurrence has homogeneous factor

\[
A_s=I-\beta_s k_sk_s^\top,
\qquad
P_{i,H}=A_HA_{H-1}\cdots A_{i+1},
\tag{1}
\]

and current displacement

\[
U_i=\beta_i k_i e_i^\top,
\qquad e_i=v_i-S_{i-1}^\top k_i.
\tag{2}
\]

R06 v2 assumes only `||A_s||_2<=1`. It therefore obtains `Z_i=||P_{i,H}U_i||_F<=X_i=||U_i||_F`, but the future may annihilate or preserve `U_i`; no positive lower ratio follows.

Failure type: **insufficient assumption**, not a sign/order error. The patch is to enforce at deployment a public, action-time-known singular-value margin

\[
0<\eta_s\le \sigma_{\min}(A_s),
\qquad \|A_s\|_2\le1,
\tag{3}
\]

for every eligible future step. The finite audit frame, every event horizon `H_i` (or a shared `H`), and the margin schedule or cumulative margin budget must be fixed or prefix-measurable before allocation; none may be selected from the realized suffix. This changes the construction and must be charged as reduced write plasticity.

The result remains a frozen-feature, same-future-input statement. It is not a lower singular certificate for the full autoregressive coupled-state Jacobian.

## 2. Exact rank-one singular values and two-sided survival

Let

\[
\rho_s=\beta_s\|k_s\|_2^2.
\tag{4}
\]

For nonzero `k_s`, `A_s` is symmetric with eigenvalue `1-rho_s` on `span(k_s)` and eigenvalue `1` on `k_s^perp`. For `d_k>=2`, this gives

\[
\|A_s\|_2=\max\{1,|1-\rho_s|\},
\qquad
\sigma_{\min}(A_s)=\min\{1,|1-\rho_s|\}.
\tag{5}
\]

For `d_k=1`, both norms instead equal `|1-rho_s|`; for `k_s=0`, `A_s=I` and the corresponding write displacement is zero. The sufficient restriction below and the product bounds remain valid in every case.

For nonzero keys, the exact effective nonexpansive margin set is `rho_s in [0,1-eta_s] union [1+eta_s,2]`. A simple non-overshooting sufficient implementation is

\[
0\le\rho_s\le1-\eta_s<1.
\tag{6}
\]

With unit-normalized keys, one can parameterize `beta_s=(1-eta_s)sigmoid(g_s)`. This is a proposed mathematical interface, not a claim that the pinned author implementation already enforces a positive `eta_s`.

For arbitrary matrices, `||AB||_F<=||A||_2||B||_F` and `||AB||_F>=sigma_min(A)||B||_F`. Repeated application to (1) gives

\[
\left(\prod_{s=i+1}^{H}\eta_s\right)\|U_i\|_F
\le
\|P_{i,H}U_i\|_F
\le
\|U_i\|_F.
\tag{7}
\]

Define

\[
\alpha_{i,H}=\prod_{s=i+1}^{H}\eta_s.
\tag{8}
\]

Then the formerly missing endpoint-sharp two-sided bound is valid:

\[
\boxed{\alpha_{i,H}\le Z_i/X_i\le1}
\quad\text{whenever }X_i>0.
\tag{9}
\]

No commutativity of future keys is used. The lower product bound is sharp: if every future key is aligned with the left factor of `U_i` and `1-rho_s=eta_s`, equality holds; if every future key is orthogonal to that factor, the ratio is one.

## 3. Consequence for selective-audit allocation

Retain the v2 finite-frame Bernoulli design with positive-envelope events, no active caps, budget `B`, and envelope propensities

\[
\pi_i^{\rm env}=B\frac{X_i}{\sum_jX_j}.
\tag{10}
\]

For realized `r_i=Z_i/X_i`, v2 proves

\[
R=
\frac{J(\pi^{\rm env};Z)}{J^*(Z)}
=\frac{\sum_iw_ir_i^2}{(\sum_iw_ir_i)^2},
\qquad
w_i=\frac{X_i}{\sum_jX_j}.
\tag{11}
\]

Assume a nonempty positive-envelope frame, `sum_i X_i>0`, `B>0`, and that the KKT caps are inactive for both the envelope design and the clairvoyant oracle. Equivalently for the displayed proportional solutions, require `B max_i X_i/sum_j X_j<=1` and, for the realized nonzero `Z`, `B max_i Z_i/sum_j Z_j<=1`. Let `alpha=min_i alpha_(i,H_i)>0` over the declared frame, with every `H_i` fixed or prefix-measurable as above. Applying the sharp scalar Kantorovich inequality to `r_i in [alpha,1]` yields

\[
\boxed{R\le K(\alpha)=\frac{(1+\alpha)^2}{4\alpha}}.
\tag{12}
\]

The endpoint factor is sharp for the interval model. If every `X_i=0`, the target moment is zero and `R` is undefined as in v2; active floor/cap regimes require their clipped designs and are not covered by (11)--(12). The guarantee concerns the HT second-moment objective used in v2; it is not automatically a variance, semantic-validity, action-benefit, or full-network-loss guarantee. Event-specific margins can be kept instead of replacing them by their minimum, but the exact minimax allocation over the resulting normalized box is a separate robust-design problem and is not claimed solved here.

## 4. The same margin prices plasticity

The rank-one update at its own key has residual

\[
\begin{aligned}
e_s^+
&=v_s-S_s^\top k_s\\
&=v_s-\left(S_{s-1}+\beta_sk_se_s^\top\right)^\top k_s\\
&=(1-\rho_s)e_s.
\end{aligned}
\tag{13}
\]

Therefore (3) implies

\[
\boxed{\|e_s^+\|_2\ge\eta_s\|e_s\|_2.}
\tag{14}
\]

The lower survival certificate and the inability to finish the new correction are the same singular-value constraint. Exact overwrite (`rho_s=1`) gives zero immediate residual but also `sigma_min(A_s)=0`, reproducing the v2 annihilation counterexample. Conversely, a positive `eta_s` makes the state step invertible but forbids exact one-step correction.

For a uniform margin `eta` and `L=H-i` future steps,

\[
\alpha_{i,H}=\eta^L,
\qquad
K(\eta^L)=\frac{(1+\eta^L)^2}{4\eta^L}.
\tag{15}
\]

For nonzero `e_s` and `tau in (0,1]`, if a current-key correction requires `||e_s^+||<=tau||e_s||`, any construction in (6) must permit `eta<=tau`. Hence even the best uniform-margin certificate compatible with that one-step correction has factor no smaller than `K(tau^L)`. Multiple microsteps do not remove the same algebraic tradeoff when they use the same fixed key and target with every `rho` in `[0,1)`: both the residual fraction and survival along that key multiply over the microsteps.

It is useful to write the survival cost additively:

\[
\Gamma_{i,H}=\sum_{s=i+1}^{H}-\log\eta_s,
\qquad
\alpha_{i,H}=e^{-\Gamma_{i,H}}.
\tag{16}
\]

A finite prefix-time guarantee therefore requires a precommitted remaining certified-dissipation budget. Over an unbounded stream, a uniform margin below one still drives `alpha` to zero exponentially. A nonzero infinite-horizon certificate product requires `sum_s -log eta_s<infinity`; this is effectively a finite total certified overwrite-cap budget and can prevent continued adaptation. It need not equal realized survival when the per-step bounds are slack. The repair solves a finite-horizon conditional problem, not lifelong preservation plus unrestricted learning.

## 5. Old counterexamples and new failure boundaries

The v1/v2 counterexamples remain:

1. `Y` is factual validity, not signed update benefit; R07/R08 remain mandatory controls.
2. Returned audits that alter later actions require sequential OPE, not one-step HT/AIPW.
3. Full-network feature, routing, token and updater changes are absent from `P_(i,H)`.
4. Offline finite-frame normalization is not a causal one-pass allocation rule.
5. Existing benchmarks do not natively expose `(Y,X,Z,pi)` or paired audit counterfactuals.

New boundaries are:

6. A sigmoid gate has values below one but no strictly positive distance from one; it does not by itself provide a public `eta>0`.
7. Approximate key normalization or kernel-level beta rescaling must be included in `rho=beta||k||^2`; checking only raw beta is insufficient.
8. If the actual homogeneous factor is `A_sD_s`, its lower product also includes `sigma_min(D_s)`; retaining the upper envelope additionally requires `||D_s||_2<=1`. A singular decay destroys the lower bound and an expansive block destroys `Z_i<=X_i`.
9. A prefix-predicted margin without simultaneous coverage is an estimator, not certificate (3).
10. Near-one `eta` preserves old perturbations but makes one-step correction weak; small `eta` learns quickly but makes (12) exponentially loose.

## 6. Information, state, compute, prediction, and controls

For fixed `eta`, the capped gate adds no recurrent coordinates and only a scalar rescaling after the existing sigmoid. A scheduled margin or remaining dissipation budget costs at least its schedule/ledger and enforcement logic. Computing `X_i` remains `O(d_k+d_v)` once `k_i,e_i` exist. The audit budget, offline frame normalization, external labels, and post-horizon instrumentation are unchanged from v2.

Distinguishing prediction: compared at the same audit count, the finite-horizon competitive gap of envelope PPS should stay within (12) only on traces for which the enforced memory factors and frozen-path target are valid. Raising `eta` improves the certified survival floor while raising the certified residual floor and reducing the maximum permissible `rho`; actual residual worsening follows only when the gate is at its cap or under a fixed-logit scaled parameterization.

Falsifiers of the stated memory certificate are an eligible factor with `sigma_min(A_s)<eta_s`, or an observed exact one-step correction from a nonzero pre-update residual while a positive same-step survival margin is claimed. A coupled-state perturbation whose full Jacobian contracts below the memory-block product is instead an explicit applicability failure: it refutes extending (7) beyond frozen memory propagation, not (7) itself. None of these failures can be repaired by deleting the trace.

Strong same-information controls are ordinary Delta with an uncapped sigmoid gate, fixed damped Delta, invertible/bi-Lipschitz residual parameterizations, uniform HT/AIPW, generic learned influence/Neyman allocation, fixed-size PPS, direct residual/action-advantage prediction, and no-write/fixed-Delta baselines. Any benefit must charge slower correction, margin enforcement, schedule state, labels, and instrumentation.

## 7. Closest work and disposition

DeltaNet supplies the residual correction update, but its original paper does not unconditionally impose the unit-L2 key convention used by the simplest parameterization above. Parallel DeltaNet and the pinned FLA **layer defaults** supply the normalized-key/sigmoid-gate implementation context already audited in v2; the low-level naive kernel consumes already-generated keys and beta. Grazzi et al.'s *Unlocking State-Tracking in Linear RNNs Through Negative Eigenvalues* directly analyzes the `I-beta kk^T` family, extends its eigenvalue range to `[-1,1]`, and implements the negative branch by scaling sigmoid beta. Invertible Residual Networks proves that a residual block whose residual map has Lipschitz constant below one is invertible and bi-Lipschitz, directly covering the general mechanism of enforcing a residual survival margin. PPS/Neyman and active-testing work cover adjacent inverse-probability and proposal-allocation principles, but do not themselves prove the independent-Bernoulli rectangular-robust factor in (12). The present contribution is therefore the Delta-specific identity tying the same rank-one singular factor to both audit survival and current-key correction, plus its finite-horizon multiplicative boundary.

This is a useful final debugging theorem/control, not a new updater: the proposed gate cap is ordinary damping/invertibility, the audit allocation is known, the guarantee can be exponentially vacuous, and no native matched-cost measurement object exists. Mathematical correctness, source collision, and empirical status remain separate.

Decision: **park after substantive attempt 3/3; lineage exhausted; candidate increment zero; empirical effect unknown.** Reopen only upon genuinely new external evidence: a native lawful audit object, a complete-state rather than memory-block margin with tractable cost, or a proved same-information advantage that overcomes the preservation–plasticity lower bound.

No project code, tests, model execution, benchmark scoring, training, inference, data/model download, GPU work, paid service, or Docker was used.
