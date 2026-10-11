# R08 v3 — sharp channel-free temporal release certificate

Status: **conditional theorem/debug control; substantive attempt 3/3; not a candidate**  
Lineage: `repairs/R08_TEMPORAL_VALIDITY_RELEASE.v1.md` -> `repairs/R08_ACTION_DEPENDENT_INFORMATION_VALUE.v2.md` -> this child.  
Scope: mathematics, source comparison and measurement feasibility only. No model code, test, training, inference, scorer, benchmark dispatch or data/model download was executed.

## 1. Original problem and concrete patch

R08 v1 repaired the false implication “high probability of obsolescence implies release” by inserting signed Delta action losses and the Bellman continuation. R08 v2 then made the continuation exact for a two-stage binary decision **when the action-specific signal channel is known**. Its remaining deployment gap is that an action not taken reveals no sample from its counterfactual observation channel. Plugging in an estimated `g_a` without support would turn the missing channel into an oracle.

This third child does not pretend to identify that channel. It derives the sharp range of the v2 information value over every Bayes-plausible channel with the same prefix prior, propagates those ranges into an exact release-minus-keep interval, and gives a two-world proof that no prefix-only estimator can shrink the interval without additional assumptions or action support. This is an **assumption/identification repair**, not an empirical success claim.

## 2. Formal object and timing

Use the v2 timing. Before the first action, `F` is observed and

`p=P(V=1|F)`, with `V in {0,1}`.

The first action `a in {K,R}` selects a known post-action memory `m_a`, an immediate expected loss `G_a`, a forced measurement cost `kappa_a`, and an action-specific signal experiment. After the signal, the terminal action is re-optimized. For fixed `m_a`, its two affine terminal risks give

`delta_a(x)=L_{1,a}(x)-L_{0,a}(x)=u_a+w_a x`,

`B_a(x)=min_d L_{d,a}(x)`.

Let `Pi_a` be the posterior random variable produced by the action-`a` experiment. A lawful experiment obeys Bayes plausibility

`Pi_a in [0,1]` and `E_a[Pi_a|F]=p`.

The channel is **unidentified** when the prefix record fixes `p,G_a,kappa_a,m_a,u_a,w_a` but supplies no action-`a` likelihood or supported sample from which its posterior law can be recovered. The action may not change `V` during this two-stage window. If it does, the action-specific predicted prior `T_a(p)` and its transition law are additional unidentified objects; the theorem below cannot absorb that causal state change into information value.

R08 v2 proved, for every specified lawful channel,

`I_a = B_a(p)-E_a B_a(Pi_a)`

`    = {E_a |delta_a(Pi_a)|-|delta_a(p)|}/2 >= 0`.              (1)

## 3. Theorem 1: sharp channel-free information envelope

Define the perfect-information ceiling

`U_a(p) = {(1-p)|delta_a(0)|+p|delta_a(1)|-|delta_a(p)|}/2`.     (2)

Then, over the declared ambiguity class of **all** Bayes-plausible binary-state experiments with prior `p`—which contains both an uninformative and a fully revealing kernel—

`0 <= I_a <= U_a(p)`,                                            (3)

and both endpoints are attainable. Hence `[0,U_a(p)]` is the sharp identified set for the gross information value under exactly that unrestricted experiment class. If the lawful sensor alphabet/family, shared parameters, cost or information budget excludes either endpoint experiment, (3) remains a universal outer bound but need not be sharp; optimize over the actual feasible channel set instead.

**Proof.** The lower bound follows from convexity of `x -> |delta_a(x)|`, as in v2. It is attained by the uninformative experiment `Pi_a=p` almost surely.

For any `x in [0,1]`, convexity also places the graph below its endpoint chord:

`|delta_a(x)| <= (1-x)|delta_a(0)|+x|delta_a(1)|`.

Taking expectations and using `E Pi_a=p` gives (2)--(3). Equality is attained by the perfectly revealing experiment `Pi_a=V`, whose posterior is `1` with probability `p` and `0` with probability `1-p`. Every intermediate value is attained by mixing the uninformative and perfectly revealing experiments. More generally, for `0<p<1`, every law `mu` on `[0,1]` with mean `p` is implementable by the likelihood kernels `g_1(dx)=x mu(dx)/p` and `g_0(dx)=(1-x)mu(dx)/(1-p)`. At `p=0` or `1` only the degenerate posterior is lawful, the two endpoint experiments coincide, and `U_a=0`. QED.

If `w_a=0`, or if `delta_a(x)` has no sign change in the open interval `(0,1)`, the absolute value is affine on the whole prior domain and `U_a=0`: no experiment can change the terminal action. Writing `t_a=-u_a/w_a`, for `0<t_a<1`,

`U_a=|w_a| p(1-t_a)` when `p<=t_a`, and `U_a=|w_a| t_a(1-p)` when `p>=t_a`.  (3a)

Thus `U_a>0` exactly when `0<p<1`, `w_a!=0`, and `0<t_a<1`; endpoint kinks `t_a in {0,1}` still give zero. The quantities `u_a,w_a,I_a,U_a,H,DeltaQ` have loss units, while `p,t_a` are dimensionless.

### Supported posterior interval

If lawful external information restricts `Pi_a` to `[l_a,r_a]` with `0<=l_a<=p<=r_a<=1`, the same chord argument gives the sharper ceiling

`U_a^[l,r](p) = {[(r_a-p)|delta_a(l_a)|+(p-l_a)|delta_a(r_a)|]/(r_a-l_a)-|delta_a(p)|}/2`  (4)

when `l_a<r_a`, and zero when `l_a=r_a=p`. It is sharp over posterior laws with that support restriction: the maximum places the unique mean-matching masses on the two endpoints; the minimum remains the uninformative posterior at `p` when that experiment is allowed. A merely estimated or post-action interval is not a lawful substitute for a prefix-valid support restriction.

## 4. Theorem 2: sharp release-minus-keep interval

Separate the non-information part of the v2 action comparison:

`H = (G_R-G_K)+(kappa_R-kappa_K)+B_R(p)-B_K(p)`.                (5)

Then

`DeltaQ := Q_R-Q_K = H-I_R+I_K`.                               (6)

Suppose the two channel identified sets are independently rectangular,

`I_R in [ell_R,u_R]`, `I_K in [ell_K,u_K]`.

The sharp identified set for the action difference is

`DeltaQ in [H-u_R+ell_K, H-ell_R+u_K]`.                         (7)

The extrema are attained by combining the endpoint experiments actionwise. With no channel information, `(ell_a,u_a)=(0,U_a)` and

`DeltaQ in [H-U_R, H+U_K]`.                                    (8)

Therefore:

- release is robustly preferred exactly when `H-ell_R+u_K < 0`;
- keep is robustly preferred exactly when `H-u_R+ell_K > 0`;
- otherwise the optimal action is not identified by the declared prefix, and abstention/query/randomized data collection or an explicit ambiguity rule is required.

These are strict-choice statements. Equality includes a tie. They do not claim that abstention is free; any query, delay or randomized exploration cost must be included in `G` or `kappa`.

For optional measurement, v2 gives `B_a(p)-[I_a-kappa_a]_+`. Define

`J_a=[I_a-kappa_a]_+`,

`J_a^L=[ell_a-kappa_a]_+`, `J_a^U=[u_a-kappa_a]_+`,

and now exclude a separate forced measurement charge from

`H_opt=(G_R-G_K)+B_R(p)-B_K(p)`.

Monotonicity gives the sharp net-value interval `J_a in [J_a^L,J_a^U]` when the channel endpoints are independently attainable, and

`DeltaQ_opt in [H_opt-J_R^U+J_K^L, H_opt-J_R^L+J_K^U]`.          (9)

Thus optional measurement never adds `kappa_R-kappa_K` as a second charge; its cost appears only inside each positive part.

## 5. Two-world nonidentifiability: same records, opposite actions

Take `p=1/2` and terminal risks `L_0(x)=x`, `L_1(x)=1-x`. Then `B(p)=1/2`, perfect information has terminal risk zero, and `U_R=1/2`. Let keep produce an uninformative signal in every world and choose the visible non-information margin `H=1/4`.

Assume the behavior policy always keeps. Compare:

- World A: the untried release channel is uninformative, so `I_R=0` and `DeltaQ=1/4>0`; keep is better.
- World B: the untried release channel perfectly reveals `V`, so `I_R=1/2` and `DeltaQ=-1/4<0`; release is better.

Every prefix, chosen action, keep-channel signal and observed keep outcome has the same law in the two worlds. Only the unsupported release channel differs. Thus no estimator measurable with respect to those records can identify the sign of `Q_R-Q_K`. Model self-evaluation or a self-generated suffix cannot distinguish the worlds because it adds no external causal evidence.

This is not a universal impossibility once the information changes. A randomized or otherwise supported record can identify the required action values under declared consistency, conditional exchangeability/sequential randomization, positivity for both actions, correctly timed outcomes, and adequate observation of the loss table/state. Known structural channel/outcome models, justified smoothness or external experiments can also extrapolate beyond logged support, but their assumptions and uncertainty must be charged. Without such added structure, g-computation/IPS/DR does not nonparametrically point-identify an unsupported action; the point claim must be replaced by a justified sensitivity/partial-identification set.

## 6. Old counterexamples rechecked

No earlier counterexample is removed.

1. **Same posterior, different protection geometry (v1).** This changes `H` and possibly both `U_a`; a posterior-only gate still fails.
2. **Release destroys later evidence (v1).** In the two-stage specialization it appears as a smaller `I_R` or larger non-information continuation cost. In a longer horizon the present envelope is insufficient and the full belief+memory Bellman state is still required.
3. **Equal posterior mean and variance, different value (v2).** The v3 ceiling uses the extreme convex expectation, not a mean/variance plug-in, so the v2 example remains inside the interval.
4. **Blackwell order scope (v2).** Perfect revelation maximizes information only for a fixed hidden state, memory and terminal loss table. It does not rank actions that change `H`, validity transitions or future state.
5. **Hysteresis (v1).** The previous action and switching fee belong in the action-history-dependent part of `G_a`, hence in `H`. At identical `p`, the v1 example with immediate release margin `-0.1` and switching cost `0.2` still reverses the optimal action with `a_(t-1)`. The channel envelope does not make `p` sufficient or remove hysteresis.

## 7. What was repaired—and what was not

The patch makes a formerly unusable missing-channel object computable as a sharp interval from prefix-visible quantities under the declared channel class. It yields an `O(1)` analytical screen once `p` and the two terminal affine loss tables are supplied. This is useful when the interval sign is decisive: the controller need not hallucinate a counterfactual likelihood. Unknown-channel design-space uncertainty is nevertheless distinct from logged-data uncertainty in `G_a`, `m_a`, transitions or terminal coefficients; uncertainty in those base terms requires a joint outer optimization and generally widens the action interval.

It does **not** provide a prefix-only point estimator, a multistep sufficient state, a learned updater, or a universal compute/statistical advantage. Computing the Delta branch coefficients can still require the protected contractions/JVPs inherited from R07; estimating a calibrated `p` and lawful support restriction has its own evidence cost. If the interval straddles zero, the theorem deliberately refuses to manufacture a decision.

The strongest same-information alternatives are:

1. direct robust bounds or a direct predictor for `Q_R-Q_K`;
2. no-write/never-release and ordinary always-release Delta;
3. a generic partially identified policy or controlled-sensing POMDP;
4. randomized sequential OPE/g-computation when supported action records exist;
5. full pre-write history/external KV or replay at matched state and information budgets.

A decomposed predictor cannot have a distribution-free dominance theorem over a direct action-value predictor merely because it exposes `p` and `I_a`: the direct class can compose the same estimated components. Any advantage must come from separately stated structural restrictions, calibration, sample complexity or total cost.

## 8. Information, state and cost

- Analytical evaluation of (2), (5) and (8) is constant time/state after the six scalar branch values are known.
- The certificate stores no extra Delta matrix, but its accounting must include the validity estimator, branch coefficients, support/sensitivity metadata, precision, and any action-randomization ledger.
- Identifying both channels from data requires action support and action-timed signals/outcomes. Sequential action-dependent observation requires the full propensity/history record; one-step inverse weighting cannot repair changed downstream policies by itself.
- If action changes validity, memory, routing, future observation support or terminal loss beyond the declared `H`, enlarge the causal state and use the corresponding Bellman/OPE object.

## 9. Native measurement and falsifiable consequences

AToKe supplies prescribed temporal transitions and historical/current QA endpoints. StableEdit and RLEdit supply sequential editing procedures. bAbI, LAMBADA, RULER, BABILong and LongMemEval supply endpoint behavior or long-context scores. None of the audited native objects jointly provides a pre-action randomized keep/release sensing action, both action-specific signal kernels or propensities, signed Delta branch coefficients, query cost, and identifiable post-action terminal losses. They can evaluate later behavior of an implementation but cannot natively verify sharpness of (8) or identify its counterfactual channel.

Falsifiable predictions, not results:

- when `H>0` but `H<U_R`, two admissible release channels can reverse the optimal action while all keep-only records remain identical;
- if both margins have no kink on `[0,1]`, the channel-free interval collapses to the static decision because `U_R=U_K=0`;
- added lawful support restrictions can only weakly reduce the ceiling in (4), whereas a post-action or future-derived restriction can spuriously shrink it;
- if a same-information direct robust action-value method yields tighter calibrated intervals at lower total cost, the R08 decomposition has no independent engineering value.

The absence of a native action-level object is a measurement gap, not a failed experiment. Empirical effect remains unknown.

## 10. Closest work, distinctness and final disposition

The channel envelope is the binary EVPI ceiling over the v2 EVSI object; Blackwell theory identifies uninformative and perfectly revealing experiments as the extreme controls. Turning missing counterfactual channel values into an action interval is a low-dimensional partial-identification/robust-decision specialization. R05 already establishes prefix-conditional partial-identification gates and baseline-safe decisions for another Delta surrogate; controlled-sensing POMDPs, causal policy evaluation and robust policy learning cover the general mechanisms. R18 separately covers recursive sufficient-state/quotient closure, so it is not recounted here.

The residual value is a clean Delta-specific debugging theorem: the exact v2 absolute-margin formula gives a closed-form, sharp release/keep/abstain interval without inventing an unavailable channel. This does not establish method-level novelty, a smaller multistep state, or native measurability.

Final status after independent final-byte reviews:

- mathematical: conditional sharp theorem/control under the stated two-stage timing and rectangular actionwise channel ambiguity;
- contribution: known EVPI/EVSI, Blackwell and partial-identification mechanisms with a narrow Delta signed-margin specialization;
- empirical: unknown; no execution;
- candidate accounting: `candidate_delta=0`; counts stay 5 historical, 0 active, 0 scientifically admitted, 0 selected;
- lineage: substantive attempt 3/3 exhausted and parked.

Reopen only if new evidence supplies a native randomized action-level temporal record, or a non-rectangular Delta channel structure with a proven tighter lawful bound and matched-total-cost advantage over direct robust action-value prediction. A renamed confidence score, self-generated future, or unlogged action channel is not a reopening delta.
