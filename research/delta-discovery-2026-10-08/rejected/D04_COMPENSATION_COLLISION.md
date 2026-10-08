# D04: transported quantization residual — excluded from active candidate pool

Author: /root/delta_retention_derivation. Status: rejected as a new method candidate; retained mathematical lead/control. No candidate code, software checks, model run or benchmark score.

## Question and exact algebra

For fixed real-arithmetic affine coefficients, let the desired Delta state be S*_t=A_t S*_(t−1)+B_t, where A_t=(I−β_t k_t k_tᵀ)D_t; decay and rank-one correction retain their actual order. Suppose a componentwise grid operator Q stores W_t and a separate residual C_t. Quantization is applied to state storage only; matrix arithmetic is assumed exact for this identity.

Ordinary write-back feedback carries discarded error unchanged into the next proposal:

Z_t=A_t W_(t−1)+B_t+C_(t−1), W_t=Q(Z_t), C_t=Z_t−W_t.

Writing the lifted state L_t=W_t+C_t gives

L_t=A_t L_(t−1)+B_t+(I−A_t)C_(t−1).

Thus unchanged compensation does not in general reproduce the original affine trajectory; the residual has to undergo the same intervening transition to do so. Its role is not necessarily wrong: changing the dynamics can help a model trained for that interface. This observation is not a claim that a published GRU solution should follow a different full-precision trajectory.

The transported variant is

Z_t=A_t(W_(t−1)+C_(t−1))+B_t,
W_t=Q(Z_t), C_t=Z_t−W_t.

Then L_t=Z_t=A_t L_(t−1)+B_t, and equal lifted initialization proves by induction L_t=S*_t for frozen coefficients. This is a standard compensated/lifted affine recurrence, not new memory capacity. A Delta step can multiply C without forming a dense A: first D_t C, then subtract β_t k_t(k_tᵀD_tC), costing O(d_k d_v) extra arithmetic plus a full residual state. It cannot swap D_t and the rank-one factor.

If residual storage is approximate, C_t=Q_C(Z_t−W_t) and d_t=Z_t−W_t−C_t, then lifted discrepancy E_t=S*_t−L_t obeys

E_t=A_t E_(t−1)+d_t,
E_t=P_(t,0)E_0+Σ_(i=1)^t A_t...A_(i+1)d_i.

For ||A_j||₂≤ρ<1 and ||d_i||_F≤η, this yields ||E_t||_F≤ρ^t||E_0||_F+η(1−ρ^t)/(1−ρ). The assumptions are substantial: operator singular norm, no residual clipping beyond the bounded d_i, frozen features, exact arithmetic elsewhere. Baseline with ρ=1 only gives linear worst-case accumulation. This is a standard stability error bound; it is not semantic retention, finite-bit information recovery, or a whole-network certificate.

Reading only W_t rather than L_t leaves output error qᵀ(W_t−S*_t)=−qᵀ(C_t+E_t), so a restored lifted trajectory does not by itself restore low-precision visible reads. Reading W+C returns to a higher-precision effective interface. If future neural coefficients depend on W rather than L, even the shared-coefficient trajectory comparison no longer applies.

## Actual nearest-work collision and decision

The primary paper *When Quantization Breaks Memory: Recurrent-State Write-Back in Low-Precision Temporal Inference*, arXiv2609.04490v1, 2026-09-03, was read at https://arxiv.org/pdf/2609.04490, §§2.2–2.3 and SupplementS8. EqsS18–S19 define unchanged error feedback with clipped floating auxiliary residual; EqsS20–S23 define finite-width residual memory. Basic extra-residual write-back is already covered, including explicit auxiliary-bit accounting. No author source was available in the inspected artifact; do not pretend formula-to-code or GRU implementation review.

Transporting the residual differs algebraically from unchanged feedback when A≠I, but its uncompressed exact identity is just a second full state realizing compensated affine arithmetic. It offers no demonstrated fixed-memory advantage over FP32 recurrent storage, compensated summation or native mixed-precision recurrence. A rank/bit-compressed version would require an actual allocation rule, observable prediction, loss/precision accounting and source collision audit; these are unresolved, not another candidate. The inspected numerical paper does not test Delta or this exact transported variant; no empirical claim is borrowed.

Necessary simple controls, if this lead is ever reopened, are native FP32 recurrent state, ordinary unchanged feedback, stochastic rounding, genuinely equal total-state-bit storage, and training with each actual write-back interface. These are feasibility directions only, not an approved experiment design. Native bAbI/LAMBADA or RULER answer accuracy cannot establish this lifted arithmetic identity; no new benchmark, examples, labels or metrics are created.

Decision: **do not count D04 as mathematically qualified distinct new candidate, do not select it, and do not generate model code**. Preserve this negative/collision record. Source details and pinned actual baseline/native-source artifacts are in ../sources/D03_D04_SOURCE_AUDIT.md.
