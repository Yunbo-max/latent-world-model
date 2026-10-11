# Independent final-byte mathematical review — R16 v2

- Reviewer: /root/commutator_compensation_math
- Assignment: fresh semantic review of the corrected active-spectrum theorem, structured-basis interface, dense costs, domain assumptions, perturbation bounds, scan scope, and disposition.
- Math artifact: research/delta-discovery-2026-10-08/repairs/R16_ACTIVE_SPECTRAL_CORE.v2.md
- Observed math SHA256: e97793f06e6c10eb56bac6dd8913f3435fe604cb9c8de190a2b816d4ea6e43bb
- Source audit: research/delta-discovery-2026-10-08/sources/R16_ACTIVE_SPECTRAL_CORE_SOURCE_AUDIT.v2.md
- Observed source-audit SHA256: 4fc11ab72193f7e7f4a796ce2267424020c81e8650c6dfc374a2bf035449f488
- Digest status: both match the assigned final bytes.
- Verdict: **PASS_CONDITIONAL**
- Execution: static mathematical/source-consistency review only; no edits or project execution.

## Reasoning

The domain and dimensions are correct. The artifact requires \(\tau>0\) and \(k\ne0\) for the normalized endpoint and separates the \(k=0\) pure-decay branch. Positivity of \(p_\tau\) on the PSD spectrum makes \(k^\top P_\tau k>0\).

For distinct active spectral values, the nonzero components \(\Pi_jk\) are orthogonal. Their normalized matrix \(U\) satisfies \(k=Uc\) and \(\Lambda U=UD\). The Vandermonde argument proves

\[
\mathcal K(\Lambda,k)=\operatorname{range}(U),\qquad
\dim\mathcal K=r,
\]

and this is the smallest \(\Lambda\)-invariant subspace containing \(k\). The lower bound remains correctly restricted to representations using such an invariant space.

The functional-calculus identity

\[
f(M)=f(\Lambda)+U[f(B)-f(D)]U^\top
\]

is exact because \(\operatorname{range}(U)\) and its orthogonal complement reduce both \(\Lambda\) and \(M\). The formulas for \(E_\tau,P_\tau,F_\tau\), and \(g_\tau\) follow, including the complete affine source. The scalar special case correctly reduces to \(g_\tau=k/\|k\|^2\).

The earlier cost-scope defect is closed. General symmetric \(\Lambda\) now charges potentially dense \(U\), \(O(drm)\) projection/lifting, \(O(d^3)\) basis discovery, \(O(d^2)\) storage, and \(O(d^2m)\) base action. Equation (15) is limited to diagonal tied coordinate groups, or a separately charged fast fixed basis. In the coordinate case, projection/lifting and the base action cost \(O(dm)\), all DPR1 core eigenpairs cost \(O(r^2)\), and core application costs \(O(r^2m)\), so

\[
O(dm+r^2m+r^2)
\]

is correct. The \(r=d\) worst case returns to \(O(d^2m)\).

The Duhamel bounds are correct:

\[
\|E-\widetilde E\|\le\tau\delta,\qquad
\|P-\widetilde P\|\le\tfrac12\tau^2\delta.
\]

The \(F\), natural-flow, and normalized-direction bounds follow by induced/Frobenius inequalities and quotient splitting. The sufficient denominator \(p_\tau(L)\|k\|^2\) is valid because \(p_\tau\) is positive and decreasing on the PSD spectrum. The artifact correctly separates these basis-independent bounds from the extra structure needed for cheap action.

Natural finite-time flow still cannot overwrite every initial state; the normalized endpoint remains an inverse-metric oblique Delta edit; its old-state factor is singular; and multiple active groups can create affine response at a query orthogonal to \(k\). Affine maps compose, but varying token bases need not retain a fixed-rank representation, so the result is sequential rather than a compact exact chunk scan.

## Final adjudication and open conditions

Accept the corrected bytes as a conditional theorem/control with zero active, scientifically admitted, or selected candidates. A future implementation must validate secular roots, deflation, finite precision, gradients, and realized transform/storage costs. Non-coordinate bases must continue to charge all discovery, transform, base-action, and storage costs. Reopening requires independent evidence for the simultaneous generator and a matched-cost consequence unavailable to grouped KDA, direct DPR1 action, expmv, rational Krylov, CKDA, or DeltaProduct, or new causal revision evidence. No empirical or scientific validity follows from this mathematical pass.
