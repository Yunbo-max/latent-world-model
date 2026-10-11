# R16 v3 — shared-carrier affine scan and cumulative-rank boundary

Status: **terminal repair attempt 3/3; conditional theorem/control, not an active D candidate**. This versioned child preserves R16_NONCOMMUTING_JOINT_FLOW.v1.md, R16_ACTIVE_SPECTRAL_CORE.v2.md, their counterexamples, and their independent reviews. The result below closes v2's unresolved exact-scan premise. It does not supply causal retain-versus-revise evidence, a distinct endpoint updater, or empirical validation.

## 1. Exact object and repair target

For token \(t\), freeze the prefix-produced quantities

\[
\Lambda_t=\Lambda_t^\top\succeq0,\quad k_t\in\mathbb R^d,
\quad \tau_t>0,
\]

and define the pure-decay and joint-flow propagators

\[
A_t=e^{-\tau_t\Lambda_t},\qquad
E_t=e^{-\tau_t(\Lambda_t+k_tk_t^\top)},\qquad
C_t=E_t-A_t. \tag{1}
\]

The natural affine write is

\[
S_t=E_tS_{t-1}+f_tv_t^\top,\qquad
f_t=p_{\tau_t}(\Lambda_t+k_tk_t^\top)k_t, \tag{2}
\]

where \(S_t\in\mathbb R^{d\times m}\). V2 proves that \(C_t\) and \(f_t\) are supported on the token's active spectral core, but leaves open whether those small one-token cores compose into a fixed-width exact chunk representation.

The repair asks two separate questions:

1. what exact width is needed when token cores vary; and
2. under what checkable restriction does an exact fixed-width associative affine scan exist?

All statements are frozen-feature identities. If the chosen memory changes later keys, decays, values, gates, or updater state, the full coupled Jacobian and nonlinear remainder are again required.

## 2. Exact product telescope and factor ledger

For \(b\ge a\), write ordered products

\[
P_{b:a}=E_bE_{b-1}\cdots E_a,\qquad
Q_{b:a}=A_bA_{b-1}\cdots A_a, \tag{3}
\]

with empty products equal to the identity. Replacing factors from right to left gives

\[
P_{b:a}-Q_{b:a}
=\sum_{j=a}^{b}Q_{b:j+1}\,C_j\,P_{j-1:a}. \tag{4}
\]

Replacing from left to right gives the equally valid dual identity

\[
P_{b:a}-Q_{b:a}
=\sum_{j=a}^{b}P_{b:j+1}\,C_j\,Q_{j-1:a}. \tag{4a}
\]

Equations (4) and (4a) must not be mixed termwise: one uses baseline suffixes and actual prefixes, while the other uses actual suffixes and baseline prefixes. For \(b=a+1\), equation (4) reads

\[
E_{a+1}E_a-A_{a+1}A_a
=A_{a+1}(E_a-A_a)+(E_{a+1}-A_{a+1})E_a.
\]

Choose any exact factorization \(C_j=L_jR_j^\top\) of rank \(s_j\). Then

\[
P_{b:a}-Q_{b:a}
=\mathcal L_{b:a}\mathcal R_{b:a}^\top, \tag{5}
\]

where

\[
\mathcal L_{b:a}
=\big[Q_{b:a+1}L_a,\ldots,Q_{b:j+1}L_j,\ldots,L_b\big],
\]

\[
\mathcal R_{b:a}
=\big[R_a,\ldots,P_{j-1:a}^\top R_j,\ldots,P_{b-1:a}^\top R_b\big]. \tag{6}
\]

Consequently

\[
\operatorname{rank}(P_{b:a}-Q_{b:a})
\le \min\!\left(d,\sum_{j=a}^{b}s_j\right). \tag{7}
\]

Equation (5) is an exact lazy factor ledger, not a fixed-width theorem: every independent one-token correction can append columns. Exact dependence removal is allowed, but its worst-case rank is governed by the actual product difference, not by the largest one-token active-core size.

## 3. The cumulative-rank bound is sharp inside R16

The failure does not require noncommuting factors. Let \(H\le d\), set

\[
\Lambda_j=0,\qquad k_j=e_j,\qquad \tau_j>0,
\]

for orthonormal coordinate vectors \(e_1,\ldots,e_H\). Then

\[
A_j=I,\qquad
E_j=I+\alpha_je_je_j^\top,\qquad
\alpha_j=e^{-\tau_j}-1\ne0. \tag{8}
\]

The factors commute and cross-products vanish, so

\[
P_{H:1}-I=\sum_{j=1}^{H}\alpha_je_je_j^\top,\qquad
\operatorname{rank}(P_{H:1}-I)=H. \tag{9}
\]

Each token has a one-dimensional active core, yet the exact chunk correction needs width \(H\). Thus no universal fixed rank determined only by \(\max_js_j\) can represent all prefixes.

The natural source shows the same carrier growth. Here

\[
f_j=(1-e^{-\tau_j})e_j, \tag{10}
\]

and later orthogonal factors leave earlier \(f_j\) unchanged. When \(m\ge H\) and the nonzero value rows are linearly independent, the affine source occupies \(H\) key directions (otherwise its key-side rank is at most \(\min(H,m)\)). This is a legal R16 example, not a generic matrix-product construction imported from outside the model.

## 4. Exact affine chunk summary

Unrolling (2) gives

\[
S_b=P_{b:a}S_{a-1}+Z_{b:a},\qquad
Z_{b:a}=\sum_{j=a}^{b}P_{b:j+1}f_jv_j^\top. \tag{11}
\]

For two adjacent chunks \(X=[a,c]\) and \(Y=[c+1,b]\), ordinary affine composition is

\[
(P_Y,Z_Y)\circ(P_X,Z_X)
=(P_YP_X,\;P_YZ_X+Z_Y). \tag{12}
\]

This operator is associative. It is always an exact scan summary, but \(P\) and \(Z\) can become dense/full-width. Associativity alone therefore does not imply a useful compact scan.

The v1 exact-write endpoint also remains affine. Its linear and source parts are

\[
\widehat E_t=(I-g_tk_t^\top)E_t,\qquad g_tv_t^\top. \tag{13}
\]

Equations (11)–(12) apply after substituting \((\widehat E_t,g_t)\), but the exact-write factor is singular and loses the natural-flow contraction used later.

## 5. Positive repair: a shared reducing carrier gives fixed-width closure

Let \(U\in\mathbb R^{d\times r}\) have orthonormal columns and let \(\mathcal U=\operatorname{range}(U)\). Assume, for every allowed token,

\[
\Lambda_t\mathcal U\subseteq\mathcal U,\qquad k_t\in\mathcal U. \tag{14}
\]

Because \(\Lambda_t\) is symmetric, \(\mathcal U\) reduces \(\Lambda_t\), hence also reduces \(\Lambda_t+k_tk_t^\top\), \(A_t\), and \(E_t\). Moreover \(f_t\in\mathcal U\). Define

\[
K_t=U^\top E_tU\in\mathbb R^{r\times r},\qquad
h_t=U^\top f_t\in\mathbb R^r. \tag{15}
\]

For a chunk, let

\[
K_{b:a}=K_b\cdots K_a,\qquad
H_{b:a}=\sum_{j=a}^{b}K_{b:j+1}h_jv_j^\top. \tag{16}
\]

Then the exact action separates as

\[
S_b
=Q_{b:a}(I-UU^\top)S_{a-1}
+U\big(K_{b:a}U^\top S_{a-1}+H_{b:a}\big). \tag{17}
\]

The compact summary is \((Q^\perp,K,H)\), where \(Q^\perp\) is the pure-decay action restricted to \(\mathcal U^\perp\). For adjacent chunks, its combine law is

\[
(Q_Y^\perp,K_Y,H_Y)\star(Q_X^\perp,K_X,H_X)
=\big(Q_Y^\perp Q_X^\perp,\;K_YK_X,\;K_YH_X+H_Y\big). \tag{18}
\]

Equation (18) is associative and fixed-width. It also applies to (13) because \(g_t\in\mathcal U\) under the same assumptions.

This is a constructive repair of v2's scan gap, but only under a declared common carrier. For a coordinate subspace \(U\) and coordinate-diagonal decays, a chunk stores a diagonal complement action, an \(r\times r\) core, and an \(r\times m\) source. A generic combine costs

\[
O(d+r^3+r^2m), \tag{19}
\]

before hardware effects, while applying the chunk to a state costs \(O(dm+r^2m)\) in that coordinate interface. A dense \(U\) adds projection/lifting, storage, discovery, and backward costs. Equation (19) is not claimed faster than KDA/WY, a direct dense \(r\)-core scan, or sequential recurrence.

For the fixed two-sided correction representation used here, the condition has an exact one-token characterization. With \(P_U=UU^\top\),

\[
[P_U,\Lambda_t]=0,\quad P_Uk_t=k_t \tag{19a}
\]

is equivalent to

\[
[P_U,A_t]=0,\quad C_t=P_UC_tP_U. \tag{19b}
\]

The forward implication is the reducing-space argument above. Conversely, (19b) makes both positive-definite \(A_t\) and \(E_t=A_t+C_t\) block diagonal and equal on \(\mathcal U^\perp\). Their unique symmetric principal logarithms are block diagonal and equal there, so \(\Lambda_t\) reduces \(\mathcal U\) and \(k_tk_t^\top\) is supported in \(\mathcal U\), which gives \(k_t\in\mathcal U\) when \(k_t\ne0\). This necessity is scoped to the fixed-\(U\), two-sided-support representation, not to every conceivable exact scan algorithm.

## 6. Why the shared-carrier condition is substantive

For a fixed two-sided active-correction representation that must be exact for every prefix, its carrier must contain every one-step correction range and every affine source direction. To remain closed under arbitrary allowed continuations, it must also contain their images under the allowed transition products. With seed

\[
\mathcal V_0=\operatorname{span}\!\left(
\bigcup_t\operatorname{range}(C_t)\cup\{f_t\}
\right), \tag{20}
\]

the robust exact carrier for the natural-flow representation is the invariant hull generated by the declared pure-decay family \(\mathscr A_{\rm allowed}\):

\[
\mathcal V_*
=\operatorname{span}\{A_h\cdots A_1z:
z\in\mathcal V_0,\ A_i\in\mathscr A_{\rm allowed},\ h\ge0\}. \tag{21}
\]

This representation needs \(\dim\mathcal V_*\) to be small, plus a cheap basis/action interface. The orthogonal example makes this dimension grow to \(H\); noncommuting families can also make it \(d\). For a causal recurrent state, choosing \(U\) from not-yet-observed future keys leaks suffix information, while prefix-time expansion cannot reconstruct components already discarded without an equivalent ledger. An offline exact chunk executor may inspect all already supplied chunk operators without changing the recurrence's causal output, but then full-chunk basis discovery, storage, and reconstruction are charged and the result is not a fixed online recurrent representation. Equation (21) describes the symmetric natural-flow family; a non-symmetric exact-write carrier would additionally need the appropriate left/right or transpose closure and is not claimed here.

Other exact closures can exist through a different finite-dimensional operator algebra, distinct left/right carriers, triangular flags, special cancellations, or the full dense affine pair. Equations (19a)–(21) do not claim a universal characterization of all scan algorithms; they characterize the common-carrier repair actually proposed here. The common-invariant-carrier and future-bridge boundaries independently derived in R10 and R12 therefore remain direct controls.

## 7. Approximate recompression has an exact error recursion

For the natural flow, set \(D_t=P_{t:1}-Q_{t:1}\). It obeys

\[
D_t=E_tD_{t-1}+C_tQ_{t-1:1}. \tag{22}
\]

Suppose a deployed ledger forms

\[
\widetilde D_t=E_t\widehat D_{t-1}+C_tQ_{t-1:1},\qquad
\widehat D_t=\widetilde D_t-R_t, \tag{23}
\]

where \(R_t\) is the discarded recompression residual. Then \(F_t=D_t-\widehat D_t\) satisfies

\[
F_t=E_tF_{t-1}+R_t. \tag{24}
\]

Since \(E_t\) is a PSD exponential, \(\|E_t\|_2\le1\), and therefore

\[
\|F_T\|_F\le \|F_0\|_F+\sum_{t=1}^{T}\|R_t\|_F. \tag{25}
\]

This is a deterministic certificate, not a claim that local SVD truncation minimizes future language loss. Transported discarded components can add coherently, backward/gradient error is unaccounted for, and the exact-write transition (13) need not be contractive. A weighted or horizon-aware recompressor again needs a lawful prefix-available metric and collides with R11's low-rank maintenance analysis.

## 8. Old failures and nearest controls rechecked

1. **Natural flow still misses exact overwrite.** Finite-time \(E_t\) is invertible; the v1 counterexample remains.
2. **The endpoint remains known geometry.** The normalized exact-write direction is still the R09/PDN/RLS inverse-metric oblique edit.
3. **Small one-token cores do not imply a compact sequence core.** Equations (8)–(9) give a sharp legal counterexample even with commuting factors.
4. **Shared-carrier closure is not a new semantic updater.** It is ordinary affine scan on a common invariant subspace and is directly controlled by a direct \(r\)-state recurrence using the same \(U,K,h\).
5. **No retain/revise evidence appears.** Neither the active spectrum nor the carrier tells whether a new observation should overwrite an old one.
6. **Full-network scope remains open.** State-dependent future features can destroy the frozen-path carrier and require the complete recurrent Jacobian.

Mandatory same-information controls are: direct full affine composition; ordered Delta/WY; grouped KDA with the same coordinate partition; direct \(r\)-dimensional affine recurrence/scan; R10/R12 common-carrier reductions; R11 exact lazy factors and generic QR/SVD recompression; DeltaProduct; and a sequential direct DPR1/exponential action at the same tolerance and total cost.

## 9. Falsifiable predictions and measurement boundary

The theorem predicts:

- in the orthogonal construction, exact chunk-correction rank equals the number of used coordinates;
- under (14), direct sequential evaluation and the summary (18) agree up to numerical error for every chunking;
- violating common invariance can create components outside \(U\) after one continuation;
- for natural-flow recompression, measured Frobenius product error is bounded by (25), while the same bound need not hold for the exact-write transition;
- at identical \((Q^\perp,K,H)\), a continuous-time description and a direct affine scan are functionally identical.

Existing bAbI, LAMBADA, RULER, LongMemEval, and DeltaProduct state-tracking endpoints do not natively expose the latent simultaneous generator, exact product-correction rank, an ex ante common carrier, discarded-factor error, semantic validity labels, and matched scan costs together. Synthetic matrix fixtures could check the identities but would be numerical verification rather than a natural mechanism benchmark. No benchmark, label, metric, result, or experiment is created here.

## 10. Terminal disposition

Attempt 3 repairs the exact-scan question rather than merely restating its absence. A shared reducing carrier yields a closed associative \(r\)-core together with an independently closed and explicitly charged complement action; in the generic varying-core ledger, one-token active widths can accumulate sharply to full dimension, and approximate recompression obeys an explicit transported-error recursion. The theorem does not exclude unrelated special finite operator algebras or the full dense affine scan.

The method-level proposal still fails scientific admission. The positive construction is the same operation as a direct low-dimensional affine recurrence on a common invariant carrier; the negative boundary overlaps established affine scan, ordered Delta/WY, low-rank maintenance, and internal R10/R11/R12 theorems. The simultaneous generator still lacks independent scientific justification, the endpoint remains a known inverse-metric edit, no causal revision evidence is added, no native mechanism-identifying record is available, and empirical effect is unknown.

**Decision:** park R16 after attempt 3/3 exhausted as a conditional theorem/control. Candidate delta is zero; active, scientifically admitted, and selected counts do not change. Reopen only with both (i) a lawful, naturally occurring prefix-known shared carrier or other exact closed representation with a matched-total-cost advantage unavailable to the direct controls, and (ii) independent evidence that the simultaneous generator or its update decision captures a natural Delta problem rather than merely reparameterizing an affine recurrence.
