# R15 v3 — finite-jet ambiguity and the boundary of a prefix trust certificate

Status: **terminal conditional theorem/debugging control; parked after substantive attempt 3/3, not an active D candidate**. This is a versioned child of `R15_COUPLED_RESPONSE_DEGREE.v2.md` and preserves the original bytes, causal counterexamples, abstract Delta degree-growth witness, and reviews. It repairs one remaining premise only: whether local response derivatives available at action time can themselves certify a nonzero safe radius.

## 1. Formal object and information boundary

Let `F` be the lawful causal prefix, let `r>=1`, and let `p` be a nonnegative integer. A current Delta write coordinate is `z in A_rho={z in R^r: ||z||_2<=rho}`. `Y(z)` is either a deterministic scalar branch-consistent response or the conditional mean delayed loss under the declared continuation; a centered loss difference may be signed. All endogenous descendants must be generated separately in each branch; future tokens, answers, validity labels, external reactions, and unchosen branch outcomes are not in `F`.

At `z=0`, suppose an updater observes the complete order-`p` response jet

\[
J_pY(0)=\{\nabla^jY(0):j=0,\ldots,p\}.
\tag{1}
\]

The action rule may be deterministic or randomized, but it is measurable only with respect to `(F,J_pY(0))` and exogenous randomization. Compared worlds have the same `F`, belong to the declared response class, and use the same exogenous-randomization law independent of the world sign. If `F` already identifies the entire continuation response, the ambiguity class below is not admissible. A certificate is *uniformly sound* for a response class when its claimed regret bound holds for every member of that class. Derivatives of a learned or teacher-forced model certify the free-running response only if that model and branch law are correct for the claimed estimand.

V2 proved that a declared uniform third-derivative bound repairs a quadratic model. V3 asks whether a finite jet can supply such a bound or a positive radius by itself.

## 2. Finite-jet ambiguity theorem

Fix any finite `p>=0`, `rho>0`, unit vector `u in R^r`, `c>0`, and common constant `C`. Put `n=p+1` and define two polynomial responses on `A_rho`:

\[
Y_s(z)=C+s\,c\,(u^Tz)^n,\qquad s\in\{-1,+1\}.
\tag{2}
\]

Both responses have value `C` at zero and every derivative of order `1` through `p` vanishes, so

\[
J_pY_+(0)=J_pY_-(0)=(C,0,\ldots,0).
\tag{3}
\]

Thus the two worlds are indistinguishable to any rule using only `(F,J_pY(0))` when their lawful prefixes otherwise agree.

Let the rule output a possibly random `Z in A_rho` and set `T=u^TZ`, so `|T|<=rho`. If `n` is odd, the two minima are attained at opposite boundary points and equal `C-c rho^n`. The expected regrets are

\[
R_+=c\{E[T^n]+rho^n\},\qquad
R_-=c\{rho^n-E[T^n]\}.
\tag{4}
\]

Their average is `c rho^n`, hence

\[
\max(R_+,R_-)\ge c rho^n.
\tag{5}
\]

If `n` is even, `Y_+` is minimized when `u^Tz=0`, while `Y_-` is minimized at either boundary. Then

\[
R_+=cE[T^n],\qquad
R_-=c\{rho^n-E[T^n]\},
\tag{6}
\]

and therefore

\[
\max(R_+,R_-)\ge \frac{c rho^n}{2}.
\tag{7}
\]

These bounds include deterministic rules as degenerate randomizations. For signed centered responses, or a response class with no fixed range/scale restriction across jets, `c` can be arbitrarily large and no finite scale-free uniform regret bound follows. For ordinary nonnegative losses, choose `C>=c rho^n`; the same regret lower bounds survive because the constant cancels. At a fixed observed `C` this constrains `c<=C/rho^n`, so the zero action has the trivial finite bound `Regret(0)<=C` when the loss lower bound is zero. The theorem therefore rules out a *nontrivial scale-free* positive-radius optimizer certificate from the finite jet alone; it does not deny such a range-derived vacuous bound. This is an information boundary, not a statement that typical trained networks realize the adversarial pair.

### Directional and multivariate scope

The witness lives on one line inside the `r`-dimensional action ball. Additional orthogonal action coordinates cannot remove the ambiguity because both responses depend only on `u^Tz`. The result also applies conditionally on any fixed prefix `F`; making the jet prefix-dependent does not reveal the first omitted directional term.

## 3. Sufficient repairs and their limits

### Uniform derivative envelope

Assume instead that `Y` is `(p+1)` times continuously differentiable on an open neighborhood containing the closed action ball and that

\[
\sup_{z\in A_rho}\|\nabla^{p+1}Y(z)\|_{op}\le M_{p+1},
\tag{8}
\]

where the operator norm is the supremum of the multilinear form over unit vectors in every argument.

Let `Q_p` be the order-`p` Taylor polynomial at zero. Taylor's theorem gives

\[
|Y(z)-Q_p(z)|\le
\epsilon_p:=\frac{M_{p+1}rho^{p+1}}{(p+1)!}
\quad\text{for all }z\in A_rho.
\tag{9}
\]

If `z_Q` minimizes `Q_p` and `z_*` minimizes `Y` on the same compact ball, then the same two-surrogate sandwich used in v2 yields

\[
Y(z_Q)-Y(z_*)\le 2\epsilon_p
=\frac{2M_{p+1}rho^{p+1}}{(p+1)!}.
\tag{10}
\]

The witness (2) has `M_{p+1}=c(p+1)!`. Its lower bounds (5) and (7) show that dependence on the first omitted derivative and on `rho^(p+1)` cannot be removed, up to constants, from a nontrivial uniform finite-jet guarantee.

Equation (8) is extra global information. A current residual, gradient, Hessian, stability radius, or finite list of derivatives at zero does not imply it. In a coupled Delta continuation it must account for every future Jacobian and higher derivative, normalization denominator, gate saturation, route/token switch, and branch-law derivative. A radius-dependent envelope is not a certificate until it is itself bounded on the proposed radius.

### Exact polynomial degree

If the response is known a priori to be a polynomial of degree at most `p`, then its complete `p`-jet at one point identifies the polynomial and the pair (2) is outside the class. If the declared degree cap is `m>p`, the pair with exponent `p+1<=m` remains admissible. Therefore v2's degree bound `m=p_loss product_h d_h` converts the problem into either:

1. obtain all required coefficients/derivatives through degree `m` or enough lawful action values to identify the chosen structured family; or
2. impose and validate a lower-order approximation with a remainder envelope.

For the v2 scalar abstract Delta witness, `m=2*3^H`; a low-dimensional current write does not make the required global response order small.

### Known range or lower bound

A known global range, nonnegativity plus the observed baseline, or another valid lower bound can yield a finite fallback regret bound without derivatives. Such a bound may be vacuous for action selection: it does not distinguish the sign of the omitted term or certify that a nonzero action improves over zero. It is therefore a valid repair to the claim of finiteness, but not a repair of the missing improving-direction certificate.

## 4. Trial outcomes change the information set

A trust-region or regularization method can propose `z`, observe a branch-consistent `Y(z)`, compare actual and predicted decrease, and adapt the radius. That is a lawful repair when a simulator, resettable environment, or real randomized trial supplies the outcome. It does not turn (1) into a prefix-only certificate: it acquires new post-action information and pays branch/sample cost.

With noisy real outcomes, v1's consistency, conditional randomization/exchangeability, positivity, dependence, delay, and censoring conditions remain. A factual descendant reused across actions is still not a free-running counterfactual. A teacher-forced validation ratio certifies only its controlled suffix estimand.

## 5. Relation to Delta structure and preserved counterexamples

The Delta write geometry still gives the immediate affine injection `x^+(z)=x^+(0)+Bz`. It can make action derivatives cheaper to pull back, but it places no bound on the first omitted derivative of the coupled continuation. V2's scalar recurrence `S_(h+1)=S_h-S_h^3` remains an explicit witness that later state-dependent keys can raise response order. V3 adds that even exact derivatives through an arbitrary finite order do not certify the next term.

All v1 and v2 failure boundaries survive: no overlap, hidden assignment, individual-effect nonidentifiability, horizon reversal, factual-descendant reuse, sequential support, exponential branch cost, degree growth, local/global mismatch, and discrete route switches. V3 does not claim that no useful local model exists; it gives explicit sufficient conditions or additional outcomes under which a radius claim can be sound.

## 6. Predictions, falsifiers, and boundary cases

1. Any purported nontrivial scale-free positive-radius optimizer certificate based only on a finite local jet can be falsified by the pair (2), which preserves every observed derivative through order `p` and changes the best action. A declared global range may still give a loose fallback bound.
2. Under a valid common envelope (8), the worst-case optimizer regret of the order-`p` Taylor rule is at most proportional to `rho^(p+1)` as in (10). A branch-consistent residual larger than (9) falsifies the declared envelope, branch, or derivative calculation.
3. If an exact degree cap at most `p` is genuinely established, the finite-jet ambiguity disappears. Failure to identify the response then comes from derivative/coefficient access, noise, support, or conditioning rather than an omitted polynomial term.
4. An adaptive acceptance ratio can rescue an initially bad radius only after lawful trial outcomes are observed; it should not be reported as a zero-outcome prefix certificate.

The first statement is a theorem, not an empirical prevalence claim. The second and third are conditional, and the fourth distinguishes information regimes.

## 7. Information, state, computation, and strongest controls

- A complete dense order-`p` Taylor model in `r` action coordinates has `q_p=binom(r+p,p)` monomials through degree `p`; explicitly storing all coefficient tensors is `Theta(q_p)` state before optimizer work. Structure can reduce this, but must be derived rather than inferred from Delta rank one.
- Higher derivatives through a full coupled horizon require higher-order automatic differentiation or structured recurrences plus their activation/recomputation cost. Certifying a uniform envelope (8) is an additional global bound, not a by-product of computing the jet.
- Exact black-box polynomial recovery retains v2's lifted-design support, conditioning, sample, and solve costs. Optimizer-only identification may be cheaper but does not identify the full response.
- The literal simplest safety baseline is `z=0` / no write / ordinary Delta. Strong same-information controls are the identical Taylor/regularized model used by high-order optimization, related structured second-order approximations such as DDP/iLQR/GGN, direct differentiable action optimization, and a direct Q/action predictor. Extra-information controls are empirical per-dose means or direct validation choice, randomized arm/dose outcomes, HT/AIPW/sequential DR, lawful paired branches, and trust-region acceptance from actual outcomes.

No listed control becomes Delta-specific merely because its action coordinate parameterizes a Delta write.

## 8. Native measurement and terminal disposition

Open Bandit Pipeline can evaluate generic logged-action estimators but has no internal Delta jet or coupled response. Ouroboros exposes finite dose menus, Recorded Replay, and later Settlement; these can measure finite-dose disagreement on their declared controlled or real-text branch, not a uniform derivative envelope or arbitrary free-running potential outcomes. LongMemEval, bAbI, LAMBADA, and RULER expose endpoint behavior without native randomized internal writes, exact action derivatives, branch-consistent counterfactuals, or a certified remainder constant.

No reviewed native asset jointly exposes `(F,J_pY(0),M_(p+1),rho)`, randomized branch-consistent actions, and ground-truth free-running response. Creating a bespoke case, label, or scorer is outside this stage and would not be native validation.

**Disposition.** Attempt 3 closes the remaining R15 premise negatively and constructively. A finite jet alone cannot supply a nontrivial scale-free optimizer guarantee on the missing positive trust radius; a uniform remainder envelope, exact degree cap, range-derived fallback, or new trial outcomes repairs different parts of the mathematics but lands on established high-order optimization, interpolation, elementary range bounds, experimental design, or OPE controls. R15 is parked with its three versions preserved, candidate delta `0`, no scientific admission or selection, and empirical effect `unknown`. Reopen only if genuinely new external evidence or a Delta-specific structural certificate changes the information class, survives same-information/matched-total-cost controls, and has a native mechanism-identifying measurement object.
