# D03 broad collision audit

Reviewer: `/root/d03_broad_collision`.  Scope: primary-paper mathematics and static author-interface reading only; no project code, test, model, benchmark or experiment was executed.

Disposition: **major functional collision; retain as a verified mathematical control, not an active scientifically admitted candidate**.  This is a `REROUTE_EVIDENCE` decision rather than an originality proof or an irreversible claim that no literal formula duplicate exists.

## Exact equivalence class

For one value channel, write a current state edit as \\(\delta s\\).  With future coefficients frozen,

\[
\delta y_{t+h}=r_{t,h}^{\top}\delta s,
\qquad
r_{t,h}=P_{t+h,t}^{\top}q_{t+h}.
\]

If row (h) of (J) is \\(\sqrt{\omega_h}r_{t,h}^{\top}\\), then

\[
G_t=\sum_h\omega_h r_{t,h}r_{t,h}^{\top}=J^{\top}J.
\]

Thus D03's metric is simultaneously (i) the finite-horizon observability Gramian of the frozen linearized output map and (ii) the Gauss--Newton Hessian of squared function-space discrepancy.  The constrained solution

\[
u^*=\frac{(G+\lambda I)^{-1}k}
{k^{\top}(G+\lambda I)^{-1}k}
\]

is the normalized natural-gradient/proximal direction under \\(k^{\top}u=1\\).  The derivation and dimensions are valid, but these are known mathematical objects.

## Major functional collisions

### Observability and adjoint sensitivity

Classical finite-horizon time-varying observability already uses

\[
W_o=\sum_h\Phi_h^{\top}C_h^{\top}C_h\Phi_h.
\]

D03 substitutes \\(C_h=q_h^{\top}\\).  Discrete adjoints likewise propagate output sensitivities through the reverse, time-ordered product \\(P^{\top}q\\).  Therefore transported future queries, the ordered adjoint and quadratic future-output disturbance are not new mathematical primitives.

### Amortized Proximal Optimization

Bae et al., *Amortized Proximal Optimization*, NeurIPS 2022, §3.1--3.2 and Eq. 3--4, combine current loss with function-space and weight-space discrepancy and obtain

\[
\Delta\theta=-(\lambda_{\rm FSD}G+\lambda_{\rm WSD}I)^{-1}g.
\]

Section 4.1 learns a preconditioner and Theorem 1 identifies the corresponding inverse function-space metric.  Algorithm 1 also exposes the extra discrepancy batch, lookahead, forward/backward and meta-update accesses.  D03 replaces ordinary parameters with a Delta fast-weight state, replaces (g) with an exact-interpolation normalization and chooses a temporal readout Jacobian for (G); the central “protect predicted outputs with a learned inverse function metric” function is already covered.  Primary source: <https://proceedings.neurips.cc/paper_files/paper/2022/hash/3af25aa3de8b7b02ddbd1b6be5031be8-Abstract-Conference.html>.  A dedicated author repository was not located in the bounded search, so Algorithm 1 is the recorded interface.

### Preconditioned DeltaNet

PDN's theoretical direction already has the inverse-history-metric form

\[
\frac{P_{t-1}k_t}{1+k_t^{\top}P_{t-1}k_t},
\qquad
P_t=\left(\lambda I+\sum_{i\le t}k_ik_i^{\top}\right)^{-1}.
\]

D03 changes the source of the metric from historical keys to predicted future outputs and normalizes for exact current-key interpolation.  The family-level collision is strong.  The actual author implementation at commit `7bd753279af87b39114149a104c5bde9bf67145f`, function `naive_recurrent_precond_gated_delta_rule`, uses a stabilized diagonal accumulator and an elementwise preconditioned key rather than a dense inverse-Gram solve; theory and implementation must not be conflated.  Fixed details are in `D03_D04_SOURCE_AUDIT.md`.

### Q-Delta

Q-Delta's Eqs. 17--20 use

\[
S_t=\alpha_tS_{t-1}(I-\beta_t(k_t+\lambda_tq_t)k_t^{\top})
+\beta_tv_tk_t^{\top},
\]

and its earlier equations expand time-ordered key/query propagation.  The author repository `psmiz/Q-Delta` at commit `4afe5b5146c02acab0e59eb44929e77cfe9c6cf9` routes `QDelta.forward` through `chunk_qdelta_rule(q,k,v,g,beta,lq)`; the chunk implementation uses \\(x=k+\lambda q\\).  It is a partial rather than literal collision: Q-Delta changes the residual probe while its left write direction remains (k); D03 changes the left write direction to (u) while retaining the (k)-residual.  Full evidence is in `QDELTA_FULL_AUDIT.md`.

### Other neighbors

QD3 accumulates past-query second moments and uses a scalar query heat to modulate later writes; it does not predict a future Gramian or rotate the write direction.  GEM/GPM-style continual-learning projection, natural gradient, influence functions and optimal-control adjoints cover the general interference geometry without alone reproducing the full D03 interface.  These are required baselines, not a claim of exact identity.

## Narrow residual and failure boundaries

The remaining literal combination is:

> predict from the prefix a token-conditioned, time-varying future observability metric and use it to choose a normalized Delta left-write direction satisfying \\(k^{\top}u=1\\).

This is a direct composition of observability/adjoints, function-space proximal optimization and an inverse-metric Delta direction.  Under this project's originality threshold it is insufficient for scientific admission.  It also has material boundaries:

1. the exact disturbance statement freezes all future coefficients; deployed edits can change future (A,q,k), requiring a full nonlinear Jacobian analysis;
2. minimizing future output energy can prefer directions that dynamics rapidly erase, so it does not imply long-term retention or lower language-model CE;
3. a dense metric costs \\(O(d^2)\\) state and an \\(O(d^3)\\) solve per update; a rank-(r) form still needs \\(O(dr)\\) predicted state and \\(O(dr^2+r^3)\\) solve work, versus the much cheaper practical PDN/Q-Delta recurrences.

## Exact-byte inputs reviewed

- `cards/D03.json`: `72e5aa1447cdab738e77646d131bb79bc783c9d69faff872c0b357c95987cfec`
- `sources/QDELTA_FULL_AUDIT.md`: `c72884dadcccb3a652279aad03a2017a47ef1738dac37cac12d715c717503be9`
- `sources/PRIMARY_NEW.md`: `43d79694d8c5403318497fd1ba4f42bd0029dfdb75143abeaf96c2af89a155b2`
- `sources/D03_D04_SOURCE_AUDIT.md`: `21f64e20cc7eed0209b2f200283ad4d8b43592135797e1a87bb0f08f6413d5e5`

The bounded search was sufficient to establish multiple major functional collisions but not to prove exhaustive absence of other precedents.  The appropriate action is therefore reroute/inactivate, not an absolute “first” or “no prior art” claim.
