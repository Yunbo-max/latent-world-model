# R15 v2 — coupled Delta response degree, exact closure, and saturated-design cost

Status: **conditional theorem/debugging control; parked after substantive attempt 2/3, not an active D candidate**. This is a versioned child of `R15_INTERVENTION_RANK_BOUND.v1.md`. It preserves the parent's support, confounding, fixed-descendant, horizon, and individual-effect counterexamples. It repairs only the missing structural step: when is the delayed loss actually quadratic in the current Delta action, and how quickly can that premise fail?

## 1. Formal object and patch

Let the causal prefix be `F`, and let a current action coordinate `z in R^r` enter the complete post-action state affinely,

\[
x_0(z)=a+Bz.
\tag{1}
\]

After the action, one declared branch-consistent continuation evolves as

\[
x_{h+1}=F_h(x_h),\quad h=0,\ldots,H-1,
\qquad Y(z)=\ell(x_H(z)).
\tag{2}
\]

All future keys, values, gates, queries, updater state, generated tokens, external feedback, and randomness that affect the response must be included in `x` or explicitly conditioned on. Equation (2) may describe a deterministic common-random-number branch only when the held randomness is exogenous and each branch generates its own endogenous descendants. A teacher-forced suffix is a different controlled estimand. For a causal conditional mean `mu(z,F)=E[Y(z)|F]`, consistency, conditional randomization/exchangeability, positivity on the compared interventions, branch-consistent descendants, and integrability are additionally required. Random polynomial maps require a uniform almost-sure degree bound for the same polynomial closure after expectation.

V1 assumed an exact quadratic conditional mean. V2 instead derives response order from `(F_h,ell)` and gives a local fallback when exact closure fails.

## 2. Polynomial composition theorem

For a vector polynomial map, define its total degree as the largest total degree of any coordinate after exact cancellation. Suppose `F_h` has degree at most `d_h>=1` and `ell` has degree at most `p`. Because (1) is affine,

\[
\deg_z x_H(z)\le \prod_{h=0}^{H-1}d_h,
\qquad
\deg_z Y(z)\le m:=p\prod_{h=0}^{H-1}d_h.
\tag{3}
\]

This follows inductively from `deg(f circ g)<=deg(f)deg(g)`. Equality need not hold because coefficients can cancel; the bound is an upper bound until a leading term is exhibited.

Let `psi_m(z)` contain every monomial of total degree at most `m`. Its dimension is

\[
q_m={r+m\choose m}.
\tag{4}
\]

For the correctly specified, unrestricted exact degree-at-most-`m` conditional-mean family

\[
E[Y\mid F,z]=theta^T psi_m(z),
\tag{5}
\]

the full coefficient vector is identified pointwise (or almost surely) in `F` from a randomized design if and only if

\[
G_m(F)=E[psi_m(Z)psi_m(Z)^T\mid F]
\tag{6}
\]

has rank `q_m`, under finite feature/outcome second moments and the causal conditions above when (5) is interpreted interventionally. The v1 kernel proof applies verbatim: a nonzero vector in `ker G_m` gives two coefficient vectors that agree almost surely on logged support and can disagree elsewhere. This is a coefficient-identification iff for the saturated family, not a lower bound for every structured degree-`m` recurrence or for identifying only its optimizer. Low-dimensional action alone does not justify low-order interpolation.

### Exact quadratic closure

If every continuation map is affine (`d_h=1`) and the terminal or accumulated loss has degree at most two in the augmented state (`p<=2`), then `Y(z)` has degree at most two. V1's `q_2=1+r+r(r+1)/2` saturated lift is then justified when all quadratic coefficients are treated as unknown. This includes a frozen/exogenous linear Delta suffix with fixed gates/keys/values/queries and a quadratic state/readout loss. This is sufficient, not necessary: nonlinear maps can cancel or preserve a quadratic invariant.

This closure is fragile. State-dependent feature generation, nonlinear routing, normalization, sampling, clipping, or nonquadratic language loss can invalidate it even when the current injection `Bz` is rank one.

## 3. A one-step scalar Delta counterexample

Take one scalar memory cell. The current action writes

\[
S_0(z)=z.
\]

At the next step choose an algebraically admissible unconstrained scalar Delta recurrence with `D=1`, `beta=1`, state-dependent key `k(S)=S`, and value `v=0`. This is not asserted to be the literal normalized-key/sigmoid-gate scalar interface of the inspected FLA implementation. Since `e=v-Sk=-S^2`,

\[
S_1=S_0+k(S_0)e(S_0)=S_0-S_0^3=z-z^3.
\tag{7}
\]

With quadratic terminal loss `ell(S)=S^2`,

\[
Y(z)=(z-z^3)^2=z^2-2z^4+z^6.
\tag{8}
\]

Therefore the bare Delta update identity does not imply an exact quadratic response, even though the current edit is one-dimensional, affine, and the terminal loss is quadratic. Binary write/no-write and the v1 baseline-plus-two-dose design cannot recover the unrestricted degree-six coefficient vector; a known or lower-parameter structured recurrence may need fewer or no fitted interventions, and its optimizer can be easier than full coefficient recovery.

If the same continuation repeats, `S_(h+1)=S_h-S_h^3`. Its leading monomial has nonzero coefficient and degree `3^(h+1)`, so

\[
\deg S_H=3^H,\qquad \deg Y=2\cdot 3^H.
\tag{9}
\]

For scalar `z`, exact recovery of every coefficient in the saturated degree-`2*3^H` family needs at least `2*3^H+1` independent feature rows, hence that many distinct noiseless levels including the intercept; noisy estimation also needs replication and conditioning. For `r` coordinates, the ambient unrestricted lifted feature count is

\[
{r+2\cdot3^H\choose 2\cdot3^H},
\tag{10}
\]

before conditioning and noise are considered. This is a saturated black-box design cost, not a demonstrated coefficient-span lower bound for the fixed witness or a claim that trained Delta networks attain every coefficient.

## 4. Local quadratic fallback and its exact error account

Let the branch-consistent response `Y` be three-times continuously differentiable on the action ball `A_rho={z:||z||_2<=rho}`. Define the second-order Taylor model at zero,

\[
Q_2(z)=Y(0)+g^Tz+\tfrac12 z^THz,
\quad g=B^T\nabla_x J(a),
\quad H=B^T\nabla_x^2J(a)B,
\tag{11}
\]

where `J(x)` is the declared fixed-branch continuation loss from post-action state `x`. Because (1) is affine, no injection-curvature term appears. For a causal expected response, differentiating through the expectation requires valid dominated interchange and an integrable uniform derivative envelope. If the trilinear spectral norm of the third derivative satisfies

\[
\sup_{||z||\le rho}||\nabla_z^3Y(z)||_{op}\le M_3,
\tag{12}
\]

then Taylor's theorem gives

\[
|Y(z)-Q_2(z)|\le \epsilon_rho:=M_3rho^3/6.
\tag{13}
\]

If `z_Q` minimizes `Q_2` on the same action set and `z_*` minimizes `Y`, then

\[
Y(z_Q)-Y(z_*)\le 2\epsilon_rho=M_3rho^3/3.
\tag{14}
\]

The proof is the two-surrogate sandwich
`Y(z_Q)<=Q_2(z_Q)+epsilon<=Q_2(z_*)+epsilon<=Y(z_*)+2epsilon`.
Thus a quadratic response model is a valid bounded-regret action rule only with a declared radius and a checkable derivative bound. Stability of the state does not by itself bound `M_3`; repeated Jacobians, Hessians, normalization singularities, and route/token switches all matter.

For the scalar witness (8), the quadratic Taylor model is `Q_2(z)=z^2`; the exact residual is `-2z^4+z^6`. Its leading error is fourth rather than third order because odd terms cancel, but it is still not globally quadratic and its best finite-dose extrapolation depends on radius.

## 5. Model derivatives versus causal interventions

Under complete differentiable model access for the declared branch, one reverse/VJP gives `g`; `r` Hessian-vector products in the columns of `B` recover the symmetric action Hessian in (11). This can be cheaper than fitting all `q_2` coefficients from noisy branches. It is not a same-information improvement over black-box outcomes: it assumes correct internal transition/loss derivatives and a fixed differentiable branch. A direct local action optimizer, DDP/iLQR/GGN, or Q model with the same derivatives can use the identical object.

With only delayed real outcomes, v1's randomized-design conditions remain necessary. Derivatives of a teacher-forced or learned world model do not identify the free-running causal response unless that model and its branch law are valid for the claimed estimand. Conversely, fitting a high-degree polynomial from interventions pays the feature count (4), support, conditioning, and branch cost; the Delta parameterization supplies no free outcomes.

## 6. Old counterexamples, new predictions, and failure boundaries

All v1 counterexamples survive: no overlap, hidden assignment, unidentified individual signs, horizon reversal, factual-descendant reuse, sequential support, and exponential branch enumeration.

V2 adds falsifiable structural predictions:

1. Under a truly affine continuation and degree-at-most-two loss, every equally spaced third directional finite difference whose four points stay inside the closure region vanishes exactly, up to numerical error.
2. For the scalar state-dependent-key witness, the response has nonzero fourth and sixth coefficients; a quadratic fit that is exact at three levels must fail at another generic level.
3. On a fixed neighborhood `0<rho<=rho_0` with one finite uniform constant `M_3`, worst-case action regret of the quadratic minimizer scales no worse than `rho^3`; failure of that scaling falsifies the declared bound/branch assumptions. With a radius-dependent `M_3(rho)`, only the fixed-radius bound (14) follows.
4. Detaching or freezing future key/value/gate/query generation can restore affine-quadratic closure, but then measures a controlled fixed-path surrogate, not the full coupled updater.

The theorem does not cover discrete token/route switches with an ordinary global derivative bound. Piecewise-smooth regions may each admit a local model, while crossing a boundary requires a different nonsmooth or distributional analysis.

## 7. Information, state, computation, and same-information controls

- Saturated exact polynomial intervention: `q_m=binom(r+m,m)` coefficients, at least `q_m` independent feature rows for full unrestricted coefficient recovery, dense Gram state `O(q_m^2)`, generic dense solves up to `O(q_m^3)`, and branch cost proportional to logged/queried actions and horizon. Known structured recurrences or optimizer-only goals may be cheaper.
- Local derivative route: one trajectory plus one VJP and `r` HVP directions, with activation storage/recomputation and a model-validity obligation; no external counterfactual evidence is created.
- Direct controls: finite-arm means; OLS/WLS/D- or G-optimal polynomial design; HT/AIPW/sequential DR; lawful paired replay/Settlement; ordinary future CE; direct Q/action prediction; DDP/iLQR/GGN or direct constrained action optimization using the same derivatives.
- Delta-specific content: equations (7)–(9) expose how the residual `v-S^Tk` and a state-dependent future key can multiply the current action and cause exact response-order growth in the unconstrained algebra. Equation (10) is the ambient saturated lift at that degree. These are negative structural facts, not an exclusive algorithmic capability or an exact embedding of released DeltaNet.

## 8. Native measurement and disposition

Open Bandit Pipeline can test generic finite-action OPE but not coupled Delta response degree. TTT Ouroboros exposes finite dose menus and Recorded Replay/Settlement, so a dose-fit residual is measurable there, but Recorded Replay fixes descendants and Settlement does not provide ground-truth coefficients for arbitrary free-running actions. LongMemEval, bAbI, LAMBADA, and RULER expose endpoint behavior without randomized internal writes or action-response truth. No reviewed native asset jointly exposes a prefix, exact Delta action coordinate, branch-consistent free-running outcomes over enough doses, and the derivative/degree certificate.

**Disposition.** The exact degree theorem, scalar Delta witness, and local regret bound are mathematically useful. They close the v1 low-order-assumption gap by proving both its affine-quadratic success regime and a one-step failure. They do not create a new updater or a matched-information advantage over direct response/Q/control methods. R15 is parked after substantive attempt 2/3, contributes zero active/admitted/selected candidates, and may reopen only with a lawful prefix-measurable closure/radius certificate, a Delta-specific operation unavailable to same-information direct action optimization, matched total-cost advantage, and a native action-response measurement object. Empirical effect remains unknown.
