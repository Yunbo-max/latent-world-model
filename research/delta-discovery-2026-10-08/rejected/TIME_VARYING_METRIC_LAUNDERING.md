# Time-varying metric laundering of Delta retention

Disposition: **accepted metric-loophole no-go; merge into D06 and the fixed-metric Lyapunov control; not a candidate recurrence**. This is a mathematical/source-only record. No project code, test, data, scorer or experiment was run.

## Exact pullback identity and why it is vacuous

For the homogeneous state path

\[
x_t=A_tx_{t-1},\qquad P_{t:1}=A_t\cdots A_1,
\]

assume every \(A_t\) is invertible. For any \(H_0\succ0\), define

\[
H_t=A_t^{-\top}H_{t-1}A_t^{-1}
    =P_{t:1}^{-\top}H_0P_{t:1}^{-1}.
\]

Then \(H_t\succ0\), \(A_t^\top H_tA_t=H_{t-1}\), and

\[
x_t^\top H_tx_t=x_0^\top H_0x_0.
\]

Thus an unconstrained prefix-dependent SPD metric can make **any finite invertible transition sequence** look isometric. This is a pullback-coordinate identity, not a certificate of Euclidean stability or retained information. If \(A_t\) is singular, no SPD \(H_t\) can satisfy the equality with \(H_{t-1}\succ0\), because a nonzero vector in \(\ker A_t\) gives a contradiction.

Two scalar counterexamples close the loophole. With \(A_t=cI\), the transported metric is \(H_t=|c|^{-2t}H_0\). For \(0<|c|<1\), the physical state vanishes while the moving norm is constant; for \(|c|>1\), the physical state explodes while the same moving norm remains constant. The metric merely rescales the answer.

## What a legitimate cross-time certificate requires

Assume a uniform envelope

\[
mI\preceq H_t\preceq MI,\qquad 0<m\le M<\infty.
\]

If

\[
A_t^\top H_tA_t\preceq H_{t-1},
\]

then telescoping gives only

\[
\|P_{t:1}\|_2\le\sqrt{M/m}.
\]

This is an upper stability bound, not retention. A separate lower inequality

\[
A_t^\top H_tA_t\succeq \rho_t^2H_{t-1}
\]

is needed to obtain

\[
\sigma_{\min}(P_{t:1})
\ge\left(\prod_{j=1}^t\rho_j\right)\sqrt{m/M}.
\]

Exact transported equality would give both sides with \(\rho_t=1\) only if the uniform envelope also held. Repeated physical contraction prevents that envelope by forcing the metric to blow up.

## Rank-one Delta specialization

For \(A=I-wr^\top\), the determinant lemma gives

\[
\det A=1-r^\top w,
\qquad
A^{-1}=I+{wr^\top\over1-r^\top w}
\]

when \(1-r^\top w\ne0\). Under exact pullback transport,

\[
\det H_t={\det H_0\over|\det P_{t:1}|^2}.
\]

Therefore repeated **volume** contraction with \(\prod_j|\det A_j|\to0\) forces the geometric mean of the metric eigenvalues to diverge, contradicting any uniform upper envelope. This is not by itself Euclidean contraction: for example

\[
A=\begin{bmatrix}1/2&0\\-10&1\end{bmatrix}
\]

has determinant \(1/2\) but large spectral norm. Ordinary normalized symmetric Delta, \(A=I-\beta kk^\top\) with \(0<\beta<1\), is the special nonexpansive case. For the actual ordered \((I-\beta kk^\top)D\), the determinant factors but the singular directions still depend on order.

## Cost, closest work and falsifier

Maintaining a dense \(H_t\) costs \(O(d^2)\) state and at least \(O(d^2)\) rank-one transport per token; a generic inverse is \(O(d^3)\). The Sherman--Morrison denominator becomes ill-conditioned near exact overwrite. Used only after the fact, \(H_t\) changes no deployed recurrence. Used to transform reads/writes, it is a prefix-dependent coordinate change that amplifies directions already being erased.

Classical multiple-Lyapunov and contraction analyses require mode/storage-function switching conditions, fixed or uniformly coercive metrics, or closed-cycle inequalities; they do not license an arbitrary metric chosen by inverse transport along each prefix. Dynamical-isometry work directly controls physical Jacobian singular values. If the metric is tied to a key Gram inverse it reduces to RLS/PDN preconditioning; if it enforces two-sided physical singular bounds it reduces to orthogonal/unitary/retention control. D06 already records the physical-coordinate log-volume cost.

Falsifier: any claimed retention theorem using only \(A_t^\top H_tA_t=H_{t-1}\) must also exhibit uniform \(m,M\) and a nontrivial lower cross-time inequality. Without them, the scalar counterexamples refute the interpretation. This record closes a proof loophole; it does not introduce a new state update and receives no D-number.
