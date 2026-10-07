# Audit of the inherited 20-candidate discussion

Date: 2026-10-07. Scope: mathematical/source review; no experiment was run.
The earlier conversation supplied a ranked table, not a retained, verified
Research Autopilot selection packet. Preserve its IDs and reasoning, but do not
backdate reviews or certify new method implementation from that table.

Historical ranking: C16, C20, C05, C08, C01, C07, C12, C06, C03, C09,
C11, C14, C02, C19, C15; reserves C10, C04, C13, C18, C17.
This is **not the currently verified top 15**.

## What the four arguments establish

1. **Predictive sufficiency is task/distribution dependent.** With finite-precision
   state H(S)<=C bits and N independent m-bit facts, independence implies
   sum_i I(S;V_i)<=I(S;V_1,...,V_N)<=C. For independent uniform query Q,
   I(S;V_Q|Q)<=C/N. Fano gives Pe>=1-(C/N+1)/m (clamp below at zero).
   This is an average error bound, not a theorem about ideal infinite-precision
   real states. Selective exact memory helps only when the retained information
   covers the query distribution; random future queries retain the linear capacity cost.
2. **The spectral argument is conditional.** A normal linear mode with k-step
   retention needs |lambda| >= (1-epsilon_m)^(1/k); a uniformly contractive
   fixed-point reasoner needs |lambda| <= epsilon_r^(1/r). Disjoint requirements
   rule out that *same mode under that fixed operator*. They do not rule out
   nonlinear gating, different subspaces, phase-conditioned shared parameters,
   nonnormal transients, search or finite-step readout.
3. **The codec argument is task dependent.** Y independent of nuisance U given W
   motivates a sufficient task statistic, but does not prove an identifiable
   semantic latent, efficient learning, or a deployable decoder. For exact copy,
   syntax, quotation and certain multilingual decisions, surface detail is useful.
   A semantic reconstruction cycle alone admits constant/collapsed solutions.
4. **Noncommutativity is not an architecture lower bound.** BCH concerns local
   small-step composition with the appropriate operator/regularity conditions.
   Nonzero [M,R] implies that interchanging operations can change the result;
   it does not prevent a shared transition F(x,c) from implementing both. A
   single recurrence can also carry a phase register. Three physical networks
   are not mathematically necessary. The contribution must concern finite-resource
   generalization or efficiency versus this strong mode-conditioned control.

World-model correction: action conditioning alone does not identify interventions.
The A=U,Y=U counterexample is correct. Identifiability needs randomized actions,
measured confounders plus assumptions, or an environment with an explicit action
interface. Better text perplexity is not evidence of counterfactual world modelling.

## Candidate-by-candidate review

| ID | Construction and condition | Specific unresolved issue / distinguishing obligation |
|---|---|---|
| C01 | Minimize expected future-task distortion plus compressed-state rate and exact-store cost; marginal write rule follows only for separable additive costs. | C02 is a query-conditioned instance of this same objective. Predictive entropy alone does not determine storage: query distribution, distortion and capacity also matter. Needs retrieval/text-memory baseline. |
| C02 | Write item i when E_Q[loss_compressed-loss_exact] exceeds its storage cost. | Not an independently derived architecture from C01 without a concrete online query-risk estimator and different measurable consequence. Cannot count both toward a distinct pool by renaming distortion. |
| C03 | Best rank-r approximation has squared Frobenius residual sum_{j>r} sigma_j^2 for a defined linear predictive operator. | Eckart–Young does not equate this surrogate with future-task error. Define operator estimation, whitening, rank updates and a task-relevant error bound. |
| C04 | Store a fact after a large prediction innovation. | High innovation can be pure nuisance; residual magnitude is not task utility. Keep as a known novelty-gating baseline lead. |
| C05 | State sufficiency for action-indexed future distributions. | Interventional identifiability is missing. A language-only web corpus cannot identify the claimed action dynamics. Requires native action-based data and a separate budget. |
| C06 | Orthogonal memory/reasoning projections. | Pm Pr=0 alone does not decouple the full Jacobian: cross terms Pm J Pr and Pr J Pm must be controlled. Specify those terms and the actual retention guarantee. |
| C07 | Shared F_theta with an observed phase input c. | It is the strongest simple counterexample to the claimed necessity of separate networks. It may be a useful baseline, not automatically a novel method. |
| C08 | Freeze slow state during fast fixed-point updates; a triangular block Jacobian separates spectra. | A concrete special case of C16. Distinctness requires an additional consequence beyond the same write mask. Reasoner contraction still needs proof/enforcement. |
| C09 | Skew-symmetric memory flow preserves norm; gradient flow decreases an energy under regularity and suitable numerical integration. | Norm retention is not fact retention. Input injection, decoder conditioning, discretization and learned energy degeneracy are untreated. Euler discretization need not preserve norm. |
| C10 | For a kappa-contraction, residual bounds distance to fixed point by residual/(1-kappa). | Does not bound answer error without readout regularity/margins. Known adaptive-computation/fixed-point literature makes this a reserve control. |
| C11 | Task sufficient information bottleneck with exact-surface bypass. | Requires specified tasks and a noncollapsed tractable estimator; paraphrase invariance can erase useful distinctions. No unseen-task sufficiency guarantee. |
| C12 | Verbalize when the conditional loss reduction exceeds verbalization cost. | The loss difference is counterfactual at decision time. Needs a trained estimator or randomized development intervention; using held-out answers would leak labels. |
| C13 | Global latent to block latent to text. | This is a broad existing hierarchical-latent family. No new mechanism established by factorization alone. |
| C14 | Match semantic projections after encode/decode. | Constant latent/decoder satisfies the cycle. Add task sufficiency and anti-collapse constraints before treating it as an implementable candidate. Do not overwrite belief with the model's own wording as new evidence. |
| C15 | Route among decoder families by expected task distortion plus cost. | Generic decision rule; requires real, jointly compatible trained decoders and router supervision. AR/flow/block comparisons cannot be claimed with a single AR checkpoint. |
| C16 | Separate observation-indexed belief from internal-computation workspace. | Does not prevent computation from improving the *representation* of a fixed posterior. Compare identical write schedules and effective compute against a phase-conditioned shared model; do not confuse world time with physical wall-clock time. |
| C17 | Compose learned action transitions for branching planning. | Standard model-based planning pattern. Needs a real action-conditioned environment; no distinct construction established. |
| C18 | Deterministic recurrence plus stochastic latent uncertainty. | Broad RSSM-like family; stochasticity alone supplies neither calibration nor novelty. |
| C19 | Shared action-predictive factors plus private modality channels. | Shared information need not be sufficient: useful cross-modal synergy can be absent from individual modalities. Needs native paired modalities, missingness protocol and fair multimodal controls. |
| C20 | Explicit composition of observe/reason/emit operators. | C07 can implement this composition using a phase variable; C16 already defines the clocks. BCH does not supply an independent mechanism or guaranteed accuracy gain. |

## Current decision and next evidence

The 20 descriptions contain useful mathematical leads, but a verified distinct
20→15 selection is absent. C01/C02 and C08/C16 are concrete overlap risks;
C07/C20 directly expose the shared-operator counterargument. Do not manufacture
new names to fill the quota. The existing methods' actual data/compute behaviour
must determine whether a consequential gap remains.

Research Autopilot requires current selection, contribution value and collision
evidence before novel candidate code. The retained `verify_methods.py --before
code` report records this as blocked. Baseline reuse, evaluator qualification,
source inspection and a complete existing-model training pipeline remain useful
and permitted. No original candidate is implemented in this delivery.

Next scientific work: complete candidate-specific cards/reviews; resolve structural
overlaps; compare BDH-CQ, Coconut and mode-conditioned/shared recurrent alternatives
at claim level; obtain native baseline failure traces on the intended task; freeze
the six-field parent and applicable Gate 0/IPCG decisions. World/action and
multimodal claims require their own sourced data and cannot be inferred from the
language benchmark suite. Do not mark those gates passed from this document.
