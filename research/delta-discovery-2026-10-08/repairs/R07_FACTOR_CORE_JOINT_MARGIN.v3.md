# R07 v3 — factor-core joint Delta action margin and feedback boundary

Status: **conditional exact subcase/debugging control; attempt 3/3 exhausted and parked, not an active D candidate**. This versioned child of `R07_COUPLED_DIRECTIONAL_MARGIN.v2.md` closes v2's explicit multi-write gap for a frozen affine Delta suffix, then gives a counterexample and perturbation envelope delimiting when that reduced core can represent the complete recurrent action. It preserves v1's truth-versus-action result and v2's complete-state derivative; it does not turn a frozen suffix into a prefix oracle or a free-running causal effect.

## 1. Original defect and precise patch

R07 v2 states that multiple writes interact through cross-Hessian terms, but it does not derive them or determine when Delta structure avoids a dense complete-state derivative. The patch changes neither the information set nor the target. It isolates the strongest exact structural case:

- `m` proposed rank-one writes are fixed before choosing their amplitudes;
- the declared suffix has action-independent affine Delta coefficients;
- the declared losses are quadratic in linear memory reads;
- the action can be optimized jointly rather than by adding scalar margins.

Let `S in R^{d_k x d_v}` and

\[
S_0(a)=\bar S_0+\sum_{r=1}^m a_r\,\beta_r k_r e_r^\top,
\qquad a\in[0,1]^m.
\tag{1}
\]

The proposal residuals `e_r`, keys `k_r` and rates `beta_r` are held fixed while `a` is chosen. Sequentially recomputing a later residual after applying an earlier amplitude is a different nonlinear construction.

For a fixed suffix,

\[
S_{t+1}=A_tS_t+B_t,
\qquad
A_t=(I-\gamma_tu_tu_t^\top)D_t,
\tag{2}
\]

where `A_t,B_t`, the query `q_t`, target `y_t` and loss weight `W_t\succeq0` do not depend on `a`. Define

\[
K=[\beta_1k_1,\ldots,\beta_mk_m]\in\mathbb R^{d_k\times m},
\qquad
E=[e_1,\ldots,e_m]\in\mathbb R^{d_v\times m},
\tag{3}
\]

\[
Z_0=K,\qquad Z_{t+1}=A_tZ_t,
\qquad c_t=Z_t^\top q_t\in\mathbb R^m.
\tag{4}
\]

## 2. Exact response factorization

Subtract the no-action trajectory. Induction in (2) gives

\[
\Delta S_t(a)=Z_t\operatorname{Diag}(a)E^\top.
\tag{5}
\]

For the value read `o_t=S_t^Tq_t`,

\[
\boxed{\Delta o_t(a)=E\operatorname{Diag}(c_t)a=: \Gamma_ta,}
\qquad \Gamma_t\in\mathbb R^{d_v\times m}.
\tag{6}
\]

Thus every proposed write retains its value direction `e_r`; the suffix changes only its transported key-side scalar `c_{t,r}`. This is stronger than the generic rank-one initial contraction in v2, but only because (2) excludes action-dependent coefficient feedback.

## 3. Exact joint QP and Hadamard Gram

Let `r_t=\bar o_t-y_t` and use

\[
J(a)=\rho^\top a+\tfrac12a^\top Ra
+\sum_{t=0}^{H}\tfrac12(r_t+\Gamma_ta)^\top W_t(r_t+\Gamma_ta),
\qquad R\succeq0.
\tag{7}
\]

Then, with no Taylor approximation,

\[
\boxed{J(a)-J(0)=g^\top a+\tfrac12a^\top Ha,}
\tag{8}
\]

\[
g=\rho+\sum_t\Gamma_t^\top W_tr_t,
\qquad
H=R+\sum_t\Gamma_t^\top W_t\Gamma_t.
\tag{9}
\]

The Delta factorization exposes every cross term:

\[
\boxed{
H=R+\sum_t
(c_tc_t^\top)\odot(E^\top W_tE)
=R+\sum_t\operatorname{Diag}(c_t)E^\top W_tE\operatorname{Diag}(c_t).}
\tag{10}
\]

Both forms show `H\succeq0`: the second is a sum of Gram matrices, while the first also follows from the Schur product theorem. Mixed signs in `c_t` or in off-diagonal entries do not break positive semidefiniteness. Negative loss weights or indefinite `R` do.

The exact joint action is therefore

\[
a^\star\in\arg\min_{a\in[0,1]^m}
g^\top a+\tfrac12a^\top Ha.
\tag{11}
\]

For `m=1`, (8) recovers v1's scalar quadratic branch after matching its sign convention. For `m>1`, the objective separates—and coordinatewise scalar optimization is uniformly exact over linear terms—when the feasible set is a Cartesian product and every off-diagonal `H_{rs}` vanishes. With cross terms, independent gates are not generally exact, although a particular `g` or active constraint can make their chosen action coincide accidentally.

## 4. Computation and the honest cost boundary

If `D_t` is diagonal, multiplying a `d_k x m` factor by (2) costs

\[
D_tZ_t-\gamma_tu_t(u_t^\top D_tZ_t),
\tag{12}
\]

or `O(d_k m)` time and `O(d_k m)` carried state per suffix step. Query contraction also costs `O(d_km)`. With a common dense value metric, `E^TWE` costs `O(d_v^2m+d_vm^2)` once; varying dense `W_t` pays this per step. Hessian accumulation costs `O(Hm^2)` and a dense box-QP solve can cost `O(m^3)`. Memory is `O((d_k+d_v)m+m^2)` beyond the no-action path.

These are not universal savings. A dense `A_t` costs `O(d_k^2m)`; large `m`, dense varying value metrics, obtaining future coefficients/probes, or computing the no-action suffix can dominate. The comparison must include those bytes/FLOPs and a same-information direct `m`-action advantage predictor. The theorem only avoids propagating `m` dense `d_k x d_v` memory tangents in the frozen affine case.

## 5. State-dependent feedback can reverse the first-order decision

The frozen core is not the complete-state v2 derivative. A scalar Delta-form example makes the omission exact. Let

\[
S_0(a)=a,\qquad k=v=1,\qquad \beta(S)=S,
\tag{13}
\]

on `a in [0,1]`. One future update is

\[
S_1(a)=S_0(a)+\beta(S_0(a))(1-S_0(a))=2a-a^2.
\tag{14}
\]

Use only quadratic read losses,

\[
J(a)=\tfrac12(S_0(a)+\tfrac32)^2+\tfrac12(S_1(a)-1)^2.
\tag{15}
\]

Freezing the future gate at `beta(0)=0` predicts `S_1^fr(a)=a` and

\[
J_{\rm fr}(a)-J_{\rm fr}(0)=\tfrac12a+a^2,
\tag{16}
\]

so it rejects every sufficiently small positive write. The true coupled objective is

\[
J(a)-J(0)=-\tfrac12a+\tfrac72a^2-2a^3+\tfrac12a^4,
\tag{17}
\]

whose first derivative is negative. A sufficiently small write helps. The omitted `beta'(S)(v-Sk)` path flips the sign; state-dependent keys/values/routes supply analogous terms. The frozen QP remains exact only if such feedback is absent or cancels so that every declared read remains affine in `a`.

This does not contradict v2: its complete Jacobian includes the missing coefficient path and its higher derivatives produce the cubic/quartic terms.

## 6. A conditional perturbation bridge, not a prefix oracle

Let `\widetilde S_t(a)` be the coupled memory path and `\bar S_t(a)` the frozen path from the same (1). Suppose an action-time-valid tube supplies, for `x=||a||_1`,

\[
\|\widetilde A_t(a)\|_2\le\varrho_t,
\tag{18}
\]

\[
\|[\widetilde A_t(a)-A_t]\bar S_t(a)
+\widetilde B_t(a)-B_t\|_F\le\eta_t x,
\tag{19}
\]

and the declared stage loss is `L_t`-Lipschitz in `S` on that tube. If

\[
C_0=0,\qquad C_{t+1}=\varrho_tC_t+\eta_t,
\tag{20}
\]

then induction gives

\[
\|\widetilde S_t(a)-\bar S_t(a)\|_F\le xC_t,
\qquad
|\widetilde J(a)-\bar J(a)|\le x\sum_tL_tC_t.
\tag{21}
\]

Therefore the frozen QP certifies improvement only when its predicted decrease exceeds this error (plus any separately bounded tail). If the one-step mismatch in (19) is instead `eta_t x^2`—for example because an enforced structural condition cancels the entire first-order coefficient-feedback path—the same recursion yields a quadratic error envelope.

The counterexample (13)--(17) shows why the linear term cannot be discarded generically. More importantly, (18)--(21) are usable online only if their constants, suffix and tail are simultaneously measurable before the action. Estimating them from the realized future is retrospective diagnosis; a generated suffix is not external evidence.

## 7. Old counterexamples and additional failure boundaries

1. `Y` still does not identify action utility; signed target benefit, preservation cost and continuation remain separate.
2. V2's dynamics-curvature, hidden-state, finite-tail, indefinite-curvature, nonsmooth-route, Bellman-switching and free-running-law counterexamples remain unchanged.
3. Equation (10) repairs rather than deletes v2's multi-write warning: cross terms are explicit and generally nonzero.
4. The simultaneous injection in (1) is not the ordered sequential recomputation implemented by DeltaProduct or ordinary token chronology. Treating one as the other changes residuals and the objective.
5. A frozen future can be exact retrospectively and still be unavailable at action time. A learned suffix predictor must be compared with a direct action-value predictor using the same information and total budget.
6. A local tube does not identify an action-dependent environment or token law. Randomization/OPE/overlap obligations from R02/R03 remain.

## 8. Sources, strong controls, predictions and disposition

Delta/WY and DeltaProduct already preserve products of ordered rank-one/Householder transitions; weighted least squares, Schur/Hadamard Gram identities and reduced box QPs are classical; DDP/iLQR and differentiable MPC already compute finite-horizon joint action curvature. R11 supplies a different small-core theorem for an adjacent-order gap, and R20 supplies a different low-rank constrained curvature solve. The exact R07 residual is only the frozen-suffix response identity (5)--(10), the `O(Hd_km)` Delta-factor propagation under diagonal-plus-rank-one transitions, and the feedback sign-reversal boundary.

Conditional predictions, not results:

1. Under the frozen affine assumptions, direct rollout and the factor-core QP agree up to numerical error; nonzero cross terms expose a source of disagreement with independent scalar gates rather than guaranteeing disagreement for every linear term and active set.
2. With state-dependent gates/keys/routes, the disagreement begins at first order exactly when the omitted coefficient derivative has nonzero contraction with the loss costate; otherwise higher-order drift remains possible.
3. A same-information direct action predictor or generic JVP/VJP method that matches the joint decisions at lower total cost removes the practical need for the core.
4. If no action-time simultaneous tube/tail certificate exists, the factor core remains a retrospective/frozen-policy diagnostic rather than a safe deployment gate.

Existing AToKe, SEAL, CounterFact/ROME, KnowEdit/EasyEdit, LongMemEval, StreamingQA, CITB, TRACE, bAbI and LAMBADA endpoints can test final accuracy, locality, retention or continual behavior. They do not expose the joint proposed-write amplitudes, frozen suffix coefficients, internal response Gram, paired action outcomes and matched total cost required to identify this mechanism. This is a measurement gap, not a failed experiment.

R07 is mathematically repaired as far as the bounded third attempt permits, but the positive mechanism is a known reduced quadratic control under assumptions that exclude the original coupled difficulty. No lawful validity signal, prefix future, free-running causal estimator, native internal scorer or demonstrated matched-cost advantage remains. R07 is exhausted and parked as a theorem/debugging control; counts remain **5 historical / 0 active / 0 scientifically admitted / 0 selected**. Empirical effect is unknown and no code or experiment was run.
