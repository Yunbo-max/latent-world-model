# R03 v3 repair-line screen — free-running distribution safety

Date: 2026-10-10  
Lineage parents: `R03_PROTECTION_AWARE_LOGGING.v1.md`, `R03_COUPLED_HORIZON_SAFETY.v2.md`  
Attempt: 3/3  
Execution boundary: mathematical/source review only; no code, tests, model execution, training, inference, scoring, downloads, GPU, Docker, or paid services.

## 1. Why this line was reopened

R03 v1 gave an exact one-step protected-query displacement for a rank-one Delta write and exposed the positivity-versus-harm feasibility boundary of randomized logging. R03 v2 repaired the unsupported leap from one step to a horizon by propagating the complete memory/updater-state difference through pre-action measurable tube/gain bounds. Its precise unresolved boundary was that a same-exogenous-path certificate is not a free-running total-effect certificate: the action can alter future tokens, queries, retrieval, policy decisions, and feedback distributions.

This is a **target/construction mismatch**, not a false v2 theorem. The v2 construction bounded two trajectories driven by a shared suffix; the desired target compares two induced laws over the complete closed-loop state. The v3 patch therefore changes the formal object from a pathwise state difference to a Wasserstein distance between the two free-running state laws.

## 2. Proposed patch and evidence gate

Let the complete closed-loop state contain the Delta memory, updater state, query/policy state, environment state, and every variable needed to make the future Markov. Let the write/no-write actions induce initial laws and possibly distinct transition kernels. If one reference kernel is contractive in `W_1`, while the action-induced kernel mismatch is uniformly bounded, triangle inequality yields a computable recurrence

\[
\delta_{h+1}\le \kappa_h\delta_h+\varepsilon_h.
\]

Kantorovich--Rubinstein duality then turns `delta_h` into an expectation-gap bound for a Lipschitz protected loss. This directly addresses the v2 free-running gap and does not require a shared future token path.

The evidence gate is strict:

1. `delta_0`, `kappa_h`, `epsilon_h`, and loss Lipschitz constants must have simultaneous action-time upper bounds; post-hoc estimates do not certify deployment.
2. The state must be closed under the real policy/environment/query/feedback dynamics. Omitting an action-affected component invalidates the Markov kernel comparison.
3. The bound is distributional expected harm, not per-action semantic correctness, and it does not identify whether an old fact remains valid.
4. The construction must be compared with generic Markov perturbation, Lipschitz model-error, bisimulation/robust-MDP, direct rollout, and sequential-OPE controls.

## 3. Decision from the bounded source screen

The patch is mathematically viable, but its main recurrence and value/expectation consequences collide strongly with established work:

- Rudolf--Schweizer already bound differences between successive laws of perturbed Markov chains under Wasserstein ergodicity and transition-kernel discrepancy.
- Asadi--Misra--Littman derive a geometric accumulation of one-step Wasserstein model error under Lipschitz dynamics and then a value-error bound.
- Ferns--Panangaden--Precup use Wasserstein/bisimulation metrics to relate transition/reward similarity to value similarity.
- Neufeld--Sester bound robust versus non-robust MDP values using Wasserstein transition ambiguity and Lipschitz conditions.

Consequently the only defensible residual is a Delta-specific instantiation: the immediate law displacement can sometimes be bounded from the rank-one write norm, and the resulting distributional bound can be inserted into the already known safe-logging feasibility constraint. That is a useful audit/control interface, not evidence of a new algorithmic mechanism.

## 4. Lineage decision

Proceed with the v3 derivation because it closes a real mathematical gap and provides a falsifiable boundary. Unless an independent review finds a missing Delta-specific theorem or same-budget advantage, R03 must be parked after attempt 3/3 with candidate delta zero. The original v1/v2 bytes, counterexamples, and reviews remain authoritative for their scopes.

