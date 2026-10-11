# R12 v2 — autonomous syndrome closure for Delta memory

Date: 2026-10-11  
Lineage parent: \`R12_SUBSPACE_SYNDROME_READOUT.v1.md\`  
Attempt: 2/3  
Contribution type: conditional theorem/debugging control  
Execution boundary: symbolic mathematics, primary-source and static interface reading only.

## 1. Original problem, exact failure, and patch

R12 v1 proved a correct static statement: for edits \(\Delta=BA\), a syndrome
\(H^\top\Delta\) determines a protected linear effect \(Q^\top\Delta\) iff
\(\ker(H^\top B)\subseteq\ker(Q^\top B)\). It also preserved the parent no-go:
numeric checksums cannot identify semantic revision truth.

The unclosed step was more basic. A persistent Delta memory does not receive an
exogenous sequence of already-computed edits. Its next residual contains
\(S_{t-1}^\top k_t\). If only the syndrome \(Y_{t-1}=H^\top S_{t-1}\) is retained,
that residual need not be computable. Thus v1's static sufficient statistic was
not yet a recursively sufficient state.

The v2 patch asks the exact causal question: **when can the fixed syndrome itself
be advanced from the prefix, without reading the discarded part of \(S\)?** The
answer is an invariant-kernel condition. For pure Delta it reduces to a sharp
dichotomy: every active key is either represented in the retained subspace or is
orthogonal to it. A quantitative leakage formula measures the best possible
one-step approximation when this fails.

## 2. Formal object and assumptions

Use the packet's key-by-value convention
\(S_t\in\mathbb R^{d_k\times d_v}\). With coefficients fixed by the lawful current
prefix, one step is

\[
S_t=F_tS_{t-1}+\beta_t k_tv_t^\top,\qquad
F_t=(I-\beta_tk_tk_t^\top)D_t. \tag{1}
\]

This is the residual form
\(D_tS_{t-1}+\beta_tk_t(v_t-S_{t-1}^\top D_t^\top k_t)^\top\)
under the stated order. The theorem below conditions on \(F_t,k_t,v_t,\beta_t\)
being available from the prefix independently of the discarded state. If gates,
keys, values or decay depend on hidden components of \(S_{t-1}\), the
necessary-and-sufficient condition is instead **composite fiber constancy**:
for the same observable exogenous input, equal \(H^\top S\) must imply equal
projected next state \(H^\top G(S)\). Individual coefficient constancy is a
simple sufficient condition, not a necessary one: hidden coefficients may vary
while their entire projected effect cancels. A fixed-coefficient proof cannot
erase this full-map/full-Jacobian obligation.

Let \(H\in\mathbb R^{d_k\times m}\) have full column rank and define

\[
Y_t=H^\top S_t\in\mathbb R^{m\times d_v},\qquad
V=\operatorname{col}(H),\qquad
P_V=H(H^\top H)^{-1}H^\top. \tag{2}
\]

An autonomous exact syndrome update is a map \(T_t\) such that
\(Y_t=T_t(Y_{t-1};k_t,v_t,\beta_t,D_t)\) for every ambient
\(S_{t-1}\). No future query, answer, validity label, or hidden full state is
available to \(T_t\).

## 3. Exact recursive-closure theorem

For a fixed affine step (1), the following are equivalent:

\[
\begin{array}{ll}
\text{(a)} & H^\top S=H^\top S'\Longrightarrow
H^\top(F_tS+\beta_tk_tv_t^\top)
=H^\top(F_tS'+\beta_tk_tv_t^\top),\\[2mm]
\text{(b)} & \ker H^\top\subseteq\ker(H^\top F_t),\\[1mm]
\text{(c)} & \operatorname{row}(H^\top F_t)
\subseteq\operatorname{row}(H^\top),\\[1mm]
\text{(d)} & F_t^\top V\subseteq V,\\[1mm]
\text{(e)} & \exists L_t\in\mathbb R^{m\times m}:
H^\top F_t=L_tH^\top.
\end{array} \tag{3}
\]

The equivalence of (a) and (b) follows by subtracting two states in one syndrome
fiber. Conditions (b)--(e) are the standard kernel/factorization/invariant-subspace
equivalences. When they hold, the exact reduced recurrence is

\[
\boxed{Y_t=L_tY_{t-1}+\beta_t(H^\top k_t)v_t^\top.} \tag{4}
\]

For a sequence of fixed-prefix affine steps, with exactness required for every
ambient state as defined above, \(Y\) is an exact recursive state iff (3) holds
at every step. A static v1 decoder for one accumulated \(\Delta\) does not imply
this property. On a declared proper reachable-state set, a weaker restricted
fiber condition may suffice and must be derived on that set.

If a protected readout \(Q^\top S_t\) must also be decoded for every ambient
state, then

\[
Q^\top=R H^\top
\quad\Longleftrightarrow\quad
\operatorname{col}(Q)\subseteq V. \tag{5}
\]

Equations (3) and (5), not either alone, are the full fixed-linear requirement:
the statistic must contain the target and its fibers must remain fibers after
every allowed Delta transition.

## 4. Pure-Delta dichotomy and minimum closed subspace

Set \(D_t=I\) and take \(\beta_t\ne0\). From

\[
H^\top F_t=H^\top-\beta_t(H^\top k_t)k_t^\top, \tag{6}
\]

condition (3) is equivalent to

\[
\boxed{H^\top k_t=0\quad\text{or}\quad k_t\in V.} \tag{7}
\]

Indeed, if \(H^\top k_t=0\), the quotient is unchanged. Otherwise the nonzero
rank-one difference in (6) belongs to \(\operatorname{row}(H^\top)\) iff
\(k_t^\top\) does, i.e. iff \(k_t\in V\).

For an allowed active-key family \(\mathcal K\) whose steps have \(\beta\ne0\),
an exact fixed syndrome therefore
requires every rank-one projector \(k k^\top\), \(k\in\mathcal K\), to leave
\(V\) invariant. Equivalently, every allowed key lies in \(V\) or \(V^\perp\).
Together with (5), the smallest admissible retained space is the fixed point

\[
V_0=\operatorname{col}(Q),\qquad
V_{j+1}=V_j+
\operatorname{span}\{k\in\mathcal K:P_{V_j}k\ne0\},\qquad
V_\star=\bigcup_jV_j. \tag{8}
\]

The iteration stabilizes in at most \(d_k\) strict dimension increases. Any
closed \(V\supseteq\operatorname{col}(Q)\) contains every \(V_j\), hence contains
\(V_\star\); conversely \(V_\star\) satisfies (7). Thus

\[
\boxed{m\ge\dim V_\star} \tag{9}
\]

for every exact autonomous syndrome carrying the declared protected readout.
If allowed keys are generic and connect the protected subspace to every ambient
direction, \(V_\star=\mathbb R^{d_k}\), so exact syndrome-only replacement gives
no key-side compression. A structured key family can leave a proper reducing
subspace, but then direct coordinates in an orthonormal basis of \(V_\star\) are
the same-width control.

For an infinite or implicit neural key family, (8) is a set-theoretic
characterization, not automatically a computable certificate. Exact global
closure requires a finite certified spanning/analytic description or another
proof over the full allowed family; finitely observed keys certify only their
observed subfamily.

For non-scalar \(D_t\), the correct condition remains
\(D_t^\top(I-\beta_tk_tk_t^\top)V\subseteq V\). Even when (7) holds, a decay that
mixes \(V\) with \(V^\perp\) can break closure. Scalar decay preserves the
pure-Delta dichotomy.

## 5. Sharp hidden-state counterexample

Suppose pure Delta, \(H^\top k\ne0\), and \(k\notin V\). Let
\(z=P_{V^\perp}k\ne0\) and choose any nonzero value vector \(a\). The two previous
states

\[
S'=S+za^\top \tag{10}
\]

have the same syndrome because \(H^\top z=0\). Their next syndromes differ by

\[
\begin{aligned}
H^\top F(S'-S)
&=H^\top(I-\beta kk^\top)za^\top\\
&=-\beta(H^\top k)\|P_{V^\perp}k\|_2^2a^\top\ne0. \tag{11}
\end{aligned}
\]

No deterministic or randomized rule using only the shared previous syndrome and
the same current prefix can guarantee exactness (or almost-sure exactness) for
both states. In residual
language, the hidden component changes \(S^\top k\), so the next Delta correction
is different. This is a recursive-state counterexample, not a semantic revision
counterexample; the original revision/coexistence and \(A\to B\to A\) failures
remain untouched.

## 6. Best one-step linear approximation and exact leakage

When exact closure fails, consider all linear reduced predictors
\(\widehat Y_t=L H^\top S_{t-1}+\beta(H^\top k)v^\top\).
For a Frobenius state budget \(\|S_{t-1}\|_F\le\rho\) and a **fixed coordinate
matrix \(H\)**,

\[
\min_L\sup_{\|S\|_F\le\rho}
\|(H^\top F-LH^\top)S\|_F
=\rho\|H^\top F(I-P_V)\|_2. \tag{12}
\]

The lower bound follows because every \(LH^\top\) vanishes on \(V^\perp\).
It is attained by \(L_\star=H^\top F(H^\top)^\dagger\), which matches the exact
map on \(V\) and leaves residual \(H^\top F(I-P_V)\).

For pure Delta,

\[
\boxed{\|H^\top F(I-P_V)\|_2
=|\beta|\,\|H^\top k\|_2\,\|P_{V^\perp}k\|_2.} \tag{13}
\]

With orthonormal syndrome coordinates \(U\), this is
\(|\beta|\|P_Vk\|_2\|P_{V^\perp}k\|_2\): leakage is zero when a key is fully
retained or fully orthogonal, and maximal for a mixed-direction key at fixed
norm. This gives a falsifiable numerical diagnostic without pretending that a
small average leakage is an exact state reduction.

The unnormalized quantity in (13) is basis-scale dependent: replacing \(H\) by
\(cH\) leaves \(V\), closure and information unchanged but multiplies syndrome
leakage by \(|c|\), while any decoder rescales inversely. Fair quantitative
comparison therefore uses orthonormal \(U\), or an end-to-end protected-output
error that includes decoder conditioning and finite precision. Arbitrary scaling
cannot be credited as smaller error.

If a reduced-only implementation uses the best one-step factor
\(L_t=H^\top F_t(H^\top)^\dagger\) and iterates
\(\widehat Y_t=L_t\widehat Y_{t-1}+\beta_t(H^\top k_t)v_t^\top+\eta_t\),
where \(\eta_t\) is quantization/roundoff, its error obeys the exact recurrence

\[
\epsilon_t=L_t\epsilon_{t-1}
+H^\top F_t(I-P_V)S_{t-1}-\eta_t, \tag{14}
\]

for \(\epsilon_t=Y_t-\widehat Y_t\). Therefore
\[
\|\epsilon_t\|_F\le
\|L_t\|_2\|\epsilon_{t-1}\|_F+
\|H^\top F_t(I-P_V)\|_2\|S_{t-1}\|_F+\|\eta_t\|_F. \tag{15}
\]
Stability of \(L_t\) does not remove the fresh hidden-state injection in (13).

## 7. Old theorem recheck and scope boundary

- R12 v1 remains correct for a static declared edit class. V2 does not retract its
  nullspace theorem, minimax hidden-edit pair, or pseudoinverse conditioning bound.
- V2 adds the missing recursive sufficiency obligation. If the full \(S\) is kept
  to compute residuals, \(Y\) is an auxiliary ledger and cannot be credited with
  replacing memory. If \(S\) is discarded, equations (3)--(9) apply.
- When \(k,v,\beta,D\) depend on discarded state, the projected **composite next
  state** must be constant on each syndrome fiber. Equal individual coefficients
  are sufficient but not necessary. The complete joint-state fiber/Jacobian
  analysis in R18 is the stronger control.
- Numeric closure does not identify whether a write is true, beneficial, stale or
  destructive. No checksum creates external evidence.
- The theorem concerns exact affine recurrence and a fixed \(H\). Adaptive
  \(H_t\) requires transporting old coordinates and charging basis metadata,
  precision and the information used to choose the new basis.

## 8. State, information, and compute cost

- Reduced state: \(m d_v\) scalars. A dense fixed \(H\) costs \(m d_k\) scalars
  unless implicit.
- Exact recurrence: applying a dense \(L_t\) costs \(O(m^2d_v)\); forming
  \(H^\top k_t\) costs \(O(md_k)\). Structured \(H,L_t\) may lower this only when
  that structure is supplied and compared fairly.
- Direct control: choose an orthonormal basis \(U\) of \(V_\star\) and store
  \(U^\top S_t\). This is exactly the syndrome in well-conditioned coordinates,
  with the same \(m d_v\) state and the same closure condition.
- Full-state control: ordinary Delta/WY or the released Delta kernel retains the
  state needed to compute \(S^\top k\); a separate syndrome then adds cost.
- Side information, changing bases, coefficient generators, quantization scales
  and decoder traffic count in total cost. A basis chosen using future queries or
  validity labels is privileged information, not compression.
- Certifying an infinite/implicit allowed-key family in (8), and retaining any
  full-state coefficient generator, are also charged. A sparse/implicit \(H\)
  may differ computationally from a dense \(U\), so the control is equal-width;
  compute superiority requires a matched total-cost demonstration.

Thus v2 closes a hidden-cost loophole rather than producing a capacity advantage.

## 9. Predictions, native measurement, and decision

Conditional predictions:

1. With fixed pure-Delta coefficients, the exact same-syndrome one-step error is
   zero exactly under (7).
2. For a mixed key in orthonormal syndrome coordinates, worst-case one-step
   leakage follows the normalized form of (13), not merely sketch width or
   \(\|k\|\).
3. Repeated approximate reduction follows (14)--(15); contractive reduced
   dynamics can still receive nonzero hidden-state error every step.
4. Adding an allowed key that overlaps the current retained space expands the
   minimum exact closed space by the fixed-point rule (8).

Existing bAbI, LAMBADA, RULER, BABILong and LongMemEval endpoints do not expose
paired full states with equal \(H^\top S\), the hidden residual difference,
\(V_\star\), or the leakage operator in (13). They can test an eventual system's
answers but cannot natively attribute a gain to autonomous syndrome closure. No
benchmark, label, metric or result is invented.

The general mechanism is an invariant quotient/lumping condition, already covered
by linear bisimulation and by this packet's R18 recursive joint quotient. The new
value is a clean Delta specialization, the exact active-key dichotomy (7), the
minimum reducing-space construction (8), and the sharp leakage (13). It is a
useful debugging theorem/control, not a distinct updater.

**Decision:** park R12 after attempt 2/3 with candidate delta zero. Reopen a final
attempt only if a real workload supplies an implicit/external \(H\) and structured
key/decay family for which (8) is provably proper, total state/metadata/traffic and
precision beat direct reduced coordinates/full Delta under matched information,
and an existing native measurement object exposes the claimed systems benefit.
Empirical effect remains unknown; no project code or experiment was run.

