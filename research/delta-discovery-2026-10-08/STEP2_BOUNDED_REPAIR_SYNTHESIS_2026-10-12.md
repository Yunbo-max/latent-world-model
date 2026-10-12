# Step 2 bounded-repair synthesis — decision-equivalence and recursive-state boundary

Status: **R01--R20 bounded repair sweep closed as a theorem/control batch; no new active candidate.** This document consolidates the latest versioned children after each lineage used its bounded three substantive repair attempts. It does not close the overall 20-to-15 discovery goal, does not certify originality or empirical benefit, and does not authorize code or experiments.

## 1. What was repaired, and what survives

The repair program did not show that the earlier work was “all wrong.” It separated five different failure modes that had previously been mixed together:

1. **derivation error:** missing full-state Jacobian paths, wrong order, or a local statement presented as global;
2. **insufficient assumption:** the theorem is correct only under a checkable invariant carrier, coverage, contraction, finite precision, or finite-field restriction;
3. **target mismatch:** a method preserves a declared quotient but does not identify which fact remains valid;
4. **mechanism collision:** the repaired object is a known belief/quotient/ledger/preconditioner/scan object or is attained by an equally strong direct baseline;
5. **unknown empirical effect:** no authorized execution was performed, so lack of evidence is not recorded as failure.

The surviving outputs are therefore useful controls: exact conditions, lower bounds, counterexamples, and reopen criteria. None currently has a method-level residual large enough to become a new D card.

## 2. Decision-equivalent repair invariance

Let (W) contain the future world, provenance, future queries, and feedback. Let \(\mathcal F_t\) be the lawful pre-action prefix sigma-field, (T=T(\mathcal F_t)) a task-sufficient statistic, \(\Gamma(T)\) the complete feasible action set including the induced post-update transition, (L(W,a)) the scientific loss, and (C(a,T)) the total state/information/computation/precision/latency cost.

Assume that for every feasible (a),

\[
\mathbb E[L(W,a)\mid\mathcal F_t]=r(T,a)\quad\text{a.s.}
\]

Consider two repaired updater representations (U_1,U_2). If

- \(\sigma(U_1)=\sigma(U_2)=\sigma(T)\) modulo null sets, or all three are Blackwell-equivalent experiments for the present decision problem;
- they realize the same complete randomized action kernels, including the same state transition;
- and their feasible policy sets are identical after all costs are charged, with costs separable by (T),

then

\[
\inf_{\pi_1}\mathbb E[L(W,A_1)+C(A_1,T)]
=
\inf_{\pi_2}\mathbb E[L(W,A_2)+C(A_2,T)]
=
\mathbb E\!\left[\inf_{a\in\Gamma(T)}\{r(T,a)+C(a,T)\}\right].
\]

Here the action space is standard Borel, \(\Gamma(T)\) is a nonempty measurable correspondence, loss plus cost is lower bounded or integrable, and a measurable minimizer/epsilon-minimizer exists; otherwise the final term is interpreted as a conditional essential infimum over (T)-measurable randomized kernels. Proof: the two representations induce the same set of measurable randomized action kernels. With the same complete action and cost, they induce the same attainable set of joint laws of ((W,A)); therefore the risk infima agree. If a resource budget couples different histories globally, only equality of the two common feasible-policy infima follows; the pointwise Bayes-envelope expression need not hold.

This is a task-specific consequence of decision/Bayes sufficiency and Blackwell equivalence, not a new Delta theorem. It is the control that prevents a gate rename, basis change, syndrome coordinate, or loss rename from being counted as a repair. It does **not** apply when a proposal truly adds lawful evidence, changes the complete action/timing set, retains otherwise lost state, or proves a different computation-constrained policy class at matched total cost.

## 3. Recursive sufficient-state trichotomy

Let a reachable history be (h_t=(o_0,a_0,\ldots,o_t)), and define (h\equiv h') when every future policy induces the same joint law of future observations and release/write losses from the two histories. This reward-augmented predictive equivalence is a right congruence: for a common feasible action and a positive-conditional-probability observation,

\[
h\equiv h'\implies hao\equiv h'ao.
\]

For continuous observations, the same statement is made almost surely through a regular conditional kernel rather than pointwise at zero-probability observations. Hence (Z_t=[h_t]_\equiv) is a recursively closed sufficient state. Any deterministic recursively closed statistic that reproduces the full future observation/loss kernels for every admissible policy must refine this relation; a statistic preserving only the current optimal action or value can be coarser. In the full-kernel exact deterministic setting, a finite-alphabet state exists iff the reachable right congruence has finite index, and its minimum number of states is the number of reachable equivalence classes. With a known controlled finite (K)-state hidden model that contains all reward-relevant latent variables, the ordinary belief (b_t(x)=P(X_t=x\mid h_t)) is a direct fixed-((K-1))-real-coordinate baseline, but it generally has infinite cardinality and requires precision to be charged. With finite reward-augmented system-dynamics rank, a predictive-state representation gives another fixed-real-coordinate baseline, again with recursion, conditioning, precision, and update cost charged.

Three regimes follow.

### 3.1 No identifying evidence

Two worlds can expose the same prefix and future observations while requiring opposite retain/revise actions. For (\nu\in\{0,1\}) and (L(a,\nu)=\mathbf 1\{a\ne\nu\}), every prefix statistic selects the same action in both worlds. Under prior (p=P(\nu=1)), the minimum Bayes risk is (\min(p,1-p)). More recurrent width cannot create semantic validity evidence.

### 3.2 Independent facts accumulate

Suppose the (i\)-th write lawfully reveals an independent bit (u_i), and after (T) writes a future query may request any (u_j). Let (M) be the number of possible values of **all** retained information visible to the decoder at release time, including the surviving Delta/post-write state, side ledger, and every auxiliary updater state. An exact state with (M) possible values must satisfy

\[
\log_2 M\ge T.
\]

Otherwise two bit strings collide in state, and a query to a differing coordinate cannot be answered correctly in both. A direct provenance ledger attains the bound. Zero-error randomized state does not lower it: inputs that differ on a queryable coordinate must have disjoint retained-state supports. This is the repeated-write INDEX boundary left by R18/R19, not a constant-width repair. It assumes all (2^T) bit strings are possible, any coordinate may be queried, and zero-error exact decoding is required. Approximate or distribution-average decoding, restricted queries, correlated facts, and finite-horizon regret need rate-distortion/Fano or task-specific quotient bounds instead. Any claim about fixed real-valued width is meaningless without precision, range, noise/robustness, or continuity assumptions, because one infinite-precision real can encode arbitrarily many bits.

### 3.3 Bounded predictive structure

A finite-alphabet exact state is possible when the reward-augmented predictive right congruence has finite index. A known controlled (K)-state hidden validity model gives a fixed-((K-1))-real-coordinate belief baseline, not generally a fixed-bit state. Finite-rank predictive structure or a lawfully declared bounded active window/invariant carrier can likewise give fixed real coordinates, subject to recursive closure, precision, conditioning, and update cost. The strongest same-information controls are direct belief filtering, predictive-state recursion, a direct quotient ledger, or the corresponding reduced affine recurrence. Delta specialization has not yet shown a smaller state or lower matched total cost.

## 4. Full sweep disposition

| Lines | Primary repair object | Correct retained result | Why it is not a new candidate |
|---|---|---|---|
| R01--R03 | transported credit, causal quotient, free-running safety | scoped quotient/bias/contraction controls | future covectors or lawful dynamics/coverage are missing; standard causal/state abstraction controls dominate |
| R04--R08 | consolidation, partial identification, stability margins, joint actions, release information | explicit action/risk trade-offs and sharp information limits | semantics require counterfactual validity evidence; action/belief/OPE controls cover the mechanism |
| R09--R13 | Gramian/carrier/overlay/closed syndrome/minimum ledger | exact conditional carrier and lost-coordinate theorems | direct sufficient coordinates or ledger attain the same object; total-cost advantage is absent |
| R14--R15 | provenance identifiability and finite-jet boundary | observable-equivalence and local-certificate limits | same-record transformations cannot add evidence; valid reopening requires new observations or uniform envelopes/trials |
| R16--R20 | sequence scan, spectral certificate, recursive quotient, finite-field code, curvature transfer | scoped rank/quotient/coding/transfer controls | known scan/PSR/bisimulation/coding/solver objects or direct baselines match them |

Every current lineage is at substantive attempt 3/3. “Attempt exhausted” means the present construction is parked until its named premise changes; it does not declare the broader scientific question permanently impossible.

## 5. Reopen test for a genuinely new Step 2 object

A new object must answer at least one question with a concrete new delta:

1. **Information:** what lawful prefix observation or randomized intervention enlarges the sigma-field?
2. **State:** what previously lost sufficient information is retained, and why is it not just a direct belief/PSR/ledger coordinate?
3. **Action:** what complete post-update transition, timing, abstention, or evidence-acquisition action is newly feasible?
4. **Computation:** under identical risk and full accounting, what state/precision/FLOP/traffic/latency advantage is proved?
5. **Measurement:** what native estimand and scorer distinguish the claimed mechanism rather than only endpoint quality?

The sequential constant-width syndrome proposal fails this test under current evidence: without identifying evidence it cannot be oracle-correct; with independently accumulating facts it needs linearly growing bits; in the exact, same-information, recursively closed bounded-predictive setting it reduces to belief/PSR/right-congruence or the direct ledger. This does not exclude approximate learned states or a separately proved computation/statistical-efficiency contribution. The present proposal therefore remains a reusable boundary theorem with `candidate_delta=0`.

## 6. Integrity and status

Remote `main` was checked at `3eb34ab5eeb2cd2530a6f764f1b0fb7fe25cb0f2`. `repairs/R18_RECURSIVE_JOINT_QUOTIENT.v1.md` has Git blob `9fdab23b529b254b670eda326e954c3721aa300f`, and `sources/R18_RECURSIVE_JOINT_QUOTIENT_SOURCE_AUDIT.md` has Git blob `db9f2039c3e7bfc224af898b07ef444ce55a0c83`; both identities are the same there as at publication commit `80aafe57836411ab15f799b252e7dd57e685965b`. Differing SHA values were observed only in the non-authoritative local scratch copy and are not evidence that remote history was overwritten. Latest lineage records and exact-readback receipts remain the authority.

Scientific state after this synthesis: **5 historical retired cards; 0 active; 0 scientifically admitted; 0 selected; `selection_verified=false`.** The overall 20-to-15 phase remains incomplete. No model code, test, training, inference, scoring, data/model download, or experiment was run.
