# R08 v2 — Action-dependent information value for temporal release

Status: **mathematically accepted conditional two-stage control; parked, not a candidate**  
Parent lineage: `repairs/R08_TEMPORAL_VALIDITY_RELEASE.v1.md` (preserved unchanged), `rejected/REVISION_EVIDENCE_POSTERIOR_EDIT.md`, `rejected/MARTINGALE_RELEASE_CONTROL.md`  
Substantive repair attempt: **2 of at most 3**  
Scope: mathematical/source review only; no model execution, training, inference, scoring, benchmark dispatch, or data/model download.

## 1. Exact v1 gap and repair type

R08 v1 correctly separated a hidden fact-validity posterior from release utility and wrote the dynamic correction as an abstract Bellman continuation difference `Gamma`. It did not make that term computable even in the smallest case where the first keep/release action changes which observation is later available. That is a **target/construction mismatch**, not a proof that temporal release is useless.

This child narrows the target to a two-stage problem and replaces the opaque continuation term by an exact expression. It preserves v1's posterior/action counterexample, robust endpoint result, and warning that a validity detector or e-process is not an action-value oracle.

## 2. Timing, information, and formal object

Let `F` be the pre-action sigma-field and `V in {0,1}` the validity state, with

`p = P(V=1 | F)`.

A first action `a in {K,R}` (keep or release) is chosen using `F`. Conditional on `F` and `a`:

1. the post-action memory `m_a` and all terminal loss coefficients are known before the new signal;
2. `a` selects an observation channel `g_a(y|v)` but does not change `V` during this two-stage window;
3. after observing `Y_a`, the posterior on signals with positive marginal probability is

`P'_a(y) = p g_a(y|1) / [p g_a(y|1) + (1-p) g_a(y|0)]`;

4. a terminal action `d in {0,1}` is re-optimized.

The necessary calibration statement is conditional under the action-indexed interventional kernel:

`E_a[P'_a | F] = p`.

On a supported randomized action event this is equivalently `E[P'_a|F,A=a]=p`. The interventional form remains well-defined for deterministic policies or zero-propensity counterfactual actions. It holds when `a` is chosen from `F`, or randomized independently of `V` conditional on `F`, and the likelihood is the actual interventional channel. The posterior's value on a null signal is arbitrary. If `a` changes validity itself, replace `p` by the action-specific predicted belief `T_a(p)=P(V_a=1|F,do(a))`; that state-transition effect is not information value. If memory is random or state-correlated, condition on observed memory or enlarge the belief state. The scalar derivation below does not cover an unobserved coupled memory state.

## 3. Exact binary-envelope identity

For fixed `m`, let terminal conditional risks be finite affine functions of belief,

`L_d(x,m) = alpha_d(m) + beta_d(m) x`,  `d in {0,1}`.

Define

`S(x,m)=L_0(x,m)+L_1(x,m)`,

`delta(x,m)=L_1(x,m)-L_0(x,m)=u(m)+w(m)x`,

and the optimized terminal Bayes risk

`B(x,m)=min_d L_d(x,m) = [S(x,m)-|delta(x,m)|]/2`.

Because `S` is affine and `E_a[P'_a|F]=p`, the gross continuation information value after action `a` is exactly

`I_a(p) = B(p,m_a) - E_a[B(P'_a,m_a)|F]`

`       = ( E_a[|delta(P'_a,m_a)||F] - |delta(p,m_a)| ) / 2 >= 0`.

The inequality is Jensen's inequality for the convex absolute value, equivalently concavity of the binary Bayes envelope. This is an equality, not a Taylor or frozen-feature approximation.

For `w(m) != 0`, let `t_m=-u(m)/w(m)`, so `delta(x,m)=w(m)(x-t_m)`. Then

`I_a(p)=|w(m_a)| [E|P'_a-t_{m_a}|-|p-t_{m_a}|]/2`.

Therefore generic posterior uncertainty is not the relevant object: information matters through probability mass crossing the action-margin kink. If `w=0`, `delta` is constant and `I_a=0`. If `w!=0` but the threshold lies outside `[0,1]`, or every posterior realization stays on one side of it, then `I_a=0`.

## 4. The v1 continuation term becomes computable

Let `G_a(p)` be the immediate expected loss of the first action, including a first-stage switching cost if applicable, and let `kappa_a` be a forced measurement cost. The two-stage action value is

`Q_a(p)=G_a(p)+kappa_a+E[B(P'_a,m_a)]`

`      =G_a(p)+kappa_a+B(p,m_a)-I_a(p)`.

Hence the exact release-minus-keep comparison is

`Q_R-Q_K = [G_R-G_K] + [kappa_R-kappa_K]`

`          + [B(p,m_R)-B(p,m_K)] - [I_R(p)-I_K(p)]`.

Release is strictly preferred exactly when this expression is negative. The bracket containing `B` is the post-action memory/terminal-loss effect; only `I_R-I_K` is the differential information value. Calling the whole continuation difference "VoI" would hide the causal memory effect.

If measurement can be skipped after action `a`, its optimized continuation is

`C_a(p)=min{B(p,m_a), kappa_a+E B(P'_a,m_a)}`

`      =B(p,m_a)-[I_a(p)-kappa_a]_+`.

Thus gross, forced-net, and optional-net information values are respectively `I_a`, `I_a-kappa_a`, and `[I_a-kappa_a]_+`. A fixed terminal switching fee can be absorbed into the affine `L_d`; a nonlinear or posterior-dependent fee need not preserve the identity.

For finite signal alphabet `Y_a`, exact evaluation costs `O(|Y_a|)` time and `O(1)` additional state once likelihoods and the four terminal branch coefficients are known. This is cheaper than a general multi-step POMDP only because the horizon, hidden state, and terminal action set were deliberately restricted.

## 5. Blackwell comparison: exact scope

Suppose experiment `E` Blackwell-dominates experiment `F`, and both use the same hidden state, prior, fixed memory, costs, and terminal loss table. Then `F` is a garbling of `E`, so its posterior is a conditional expectation of the finer posterior. Convexity of `|delta|` gives

`I_E >= I_F`, equivalently `E B(P'_E,m) <= E B(P'_F,m)`.

This does **not** order `Q_R` and `Q_K` when release and keep produce different memories, immediate costs, validity transitions, or terminal losses. Controlled sensing is therefore a baseline for the observation-channel part, not a proof that the more informative release action is globally better.

## 6. New counterexample: mean and variance are insufficient

Let `p=1/2`, `L_0(x)=x`, and `L_1(x)=1-x`, so `B(x)=min{x,1-x}`. Consider two Bayes-plausible posterior laws:

- `Pi_A`: `P'=1/4` or `3/4`, each with probability `1/2`;
- `Pi_B`: `P'=0,1/2,1` with probabilities `1/8,3/4,1/8`.

Both have posterior mean `1/2` and variance `1/16`, but

`E_A B(P')=1/4`, `I_A=1/4`,

`E_B B(P')=3/8`, `I_B=1/8`.

They are implementable signal experiments. For any support point `x` of marginal weight `w_x`, set

`P(Y=x|V=1)=2 w_x x`, `P(Y=x|V=0)=2 w_x(1-x)`.

The channel probabilities sum to one because each posterior law has mean `1/2`. Hence posterior mean and variance, or any loss-agnostic score determined only by those two moments, cannot replace the action-margin expectation `E|delta(P')|`.

## 7. Old counterexamples and failure boundaries

The v1 same-posterior protection counterexample remains: choose uninformative channels `P'_R=P'_K=p`. Then `I_R=I_K=0`, and different signed protection contractions still reverse `B(p,m_R)-B(p,m_K)` and the optimal action. The v1 information-destruction example is now an explicit negative differential-information term rather than an unspecified `Gamma`.

The repair fails or requires a larger state when:

- the first action causally changes validity but that transition is omitted;
- action assignment leaks hidden information not present in `F`;
- memory or loss coefficients remain unobserved and correlated with validity;
- the terminal decision occurs before the signal;
- the horizon exceeds one observation/terminal decision, so future beliefs and memory require Bellman recursion;
- there are more than two terminal actions, where the Bayes envelope is still piecewise affine/concave but no single absolute-margin identity covers every kink;
- likelihoods, temporal hazards, or signed Delta terminal losses are not identifiable from the visible prefix.

No old counterexample is deleted, and no empirical success is asserted.

## 8. Delta specialization and strongest simple alternative

For binary terminal keep versus full Delta release along a declared fixed direction, v1 gives branch loss differences affine in validity belief. Their difference is exactly `delta(p,m)` above; the observation channel value is therefore the expected absolute spread of that signed Delta action margin around its decision boundary.

This is a useful accounting specialization, not a new updater. The strongest same-information alternatives are:

1. directly predict `Q_R-Q_K` from the visible prefix and declared state;
2. solve the same two-stage controlled-sensing problem without a Delta decomposition;
3. use the full belief+memory POMDP when the short-horizon assumptions fail.

R08 would need a proved same-budget advantage over these alternatives, or a Delta-specific sufficient state smaller than the generic control state, before candidate admission.

## 9. Measurement and predictions

Existing temporal editing assets such as AToKe provide supplied old/current facts and post-edit QA-style outcomes, but not a native pre-action choice of observation channel, calibrated action-specific likelihoods, query costs, signed Delta margins, randomized propensities, or paired keep/release outcomes. StableEdit and RLEdit expose sequential edit procedures rather than this causal sensing object. Therefore the identity is checkable on a declared synthetic/analytical channel, while the natural empirical claim remains a measurement gap.

Falsifiable predictions, not results:

- two channels with the same posterior mean and variance can have different release value if their posterior mass falls differently around the signed action threshold;
- Blackwell improvement helps only after fixing memory, costs, and terminal losses;
- if a direct action-value predictor matches or beats the decomposed estimator at the same information/state/compute, the decomposition has no independent engineering value.

## 10. Disposition

The repair successfully replaces v1's opaque one-step continuation term by a correct, computable binary-envelope identity and separates memory, cost, and sensing effects. Independent review accepts the conditional mathematics after the timing, conditional-martingale, state-transition, and Blackwell-scope qualifications above.

The main mechanisms are standard binary Bayes risk, expected value of sample information, Blackwell comparison of experiments, and controlled-sensing POMDPs. The Delta content is a structured loss-table specialization. R08 v2 is therefore retained as useful conditional theory/control and **parked after substantive attempt 2/3**, not admitted as a distinct candidate. Mathematical status: accepted under stated assumptions. Contribution status: collision/bridge only. Empirical status: unknown. Counts remain 5 historical, 0 active, 0 scientifically admitted, 0 selected.

Reopen attempt 3 only for at least one concrete new delta:

1. a prefix-only estimator of the action-specific margin law with a proved same-budget advantage over direct `Q_R-Q_K` prediction;
2. a Delta-specific multi-step sufficient-state/continuation theorem materially cheaper than generic controlled sensing/POMDP;
3. a native causal temporal object with action-specific observation channels, pre-action margins, propensities, and identifiable keep/release outcomes.
