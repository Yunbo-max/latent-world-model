# NOGO-UNITARY-DILATION — finite reusable orthogonal state cannot realize strict Delta forgetting

Disposition: **accepted no-go/control; not a candidate**.  Orthogonal dilation can preserve one erase step or a fixed finite horizon, but a fixed finite augmented state cannot preserve the original Delta readout while exactly reproducing strict contraction for all horizons.

## One-step rank-one dilation

For a unit key and bare Delta erase,

\[
A=I-\beta kk^\top,
\qquad \alpha=1-\beta,
\qquad \delta=\sqrt{\beta(2-\beta)},
\qquad 0\le\beta\le2,
\]

we have \(I-A^\top A=\delta^2kk^\top\).  Its rank-one Halmos/Julia completion needs only one auxiliary value row:

\[
U=
\begin{bmatrix}
I-\beta kk^\top & \delta k\\
\delta k^\top & -\alpha
\end{bmatrix},
\qquad U^\top U=I,
\qquad U^2=I.
\]

For visible state \(S\in\mathbb R^{d\times m}\) and auxiliary \(r\in\mathbb R^{1\times m}\),

\[
S^-=AS+\delta kr,
\qquad
r^-=\delta k^\top S-\alpha r.
\]

The erase substep conserves \(\|S\|_F^2+\|r\|_2^2\).  Adding the ordinary external write \(\beta kv^\top\) to \(S^-\) gives the standard Delta current-key update only when the incoming auxiliary is zero.  The affine write is external forcing; a homogeneous-coordinate matrix containing a nonzero translation is not itself orthogonal.

## Reusing the auxiliary slot breaks Delta

For fixed \(k,\beta\), let \(a_t=k^\top S_t\) and temporarily omit new writes.  The key/auxiliary pair follows

\[
\begin{bmatrix}a_t\\r_t\end{bmatrix}
=
\begin{bmatrix}\alpha&\delta\\\delta&-\alpha\end{bmatrix}
\begin{bmatrix}a_{t-1}\\r_{t-1}\end{bmatrix}.
\]

Because the block is an involution, \(a_1=\alpha a_0\) but \(a_2=a_0\), whereas Delta requires \(a_2=\alpha^2a_0\).  At \(\beta=1\), erased content reappears completely after the second use.  A rotation completion changes the visible path to \(\cos(n\theta)\), not the required \(\cos^n\theta\).  For different steps, defect channels feed back cross-terms into the visible state, again breaking the ordered Delta product.

More generally, if an orthogonal block \(\begin{bmatrix}A&B\\C&E\end{bmatrix}\) must give visible update \(S'=AS\) for every current auxiliary, independence requires \(B=0\).  Orthogonality then forces \(AA^\top=I\), excluding every strict Delta contraction.

## All-horizon finite-dimensional impossibility

On a strict scalar contraction direction \(|\alpha|<1\), suppose finite-dimensional unitary \(U\) satisfied

\[
PU^nJ=\alpha^n
\qquad\text{for every }n\ge0.
\]

For an embedded unit vector \(x\), finite-dimensional spectral decomposition gives

\[
\langle x,U^nx\rangle=\sum_jw_je^{in\theta_j},
\qquad w_j\ge0,quad\sum_jw_j=1.
\]

Its long-run squared mean is positive after equal eigenphases are grouped, while \(N^{-1}\sum_{n<N}|\alpha|^{2n}\to0\), a contradiction.  Thus a nonunitary Delta contraction requires an infinite power dilation for all horizons.  A constant repeated key is already a counterexample to any claimed construction for arbitrary time-varying sequences.

## Exact finite-horizon version and cost

For a declared horizon \(H\), use a fresh zero auxiliary row for every step.  The first \(H\) visible states then exactly equal standard Delta while each erased defect is retained separately.  This costs \(dm+Hm\) scalars before storing any key, source identity or provenance; accessible semantic retrieval normally raises it to \(dm+H(d+m)\).  Recycling a slot either resets and discards information or allows old content to re-enter the visible state.  The construction is therefore a growing event memory in different coordinates, not constant-size lossless Delta.

Orthogonality proves reversibility given the complete input sequence and total augmented state.  It does not prove query accessibility, semantic validity, robustness at finite precision, correct revision release, or preservation through an additional ordered decay \(D_t\).

## Direct collisions and scope

Halmos/Julia and Sz.-Nagy/Egervary dilation supply the classical construction and horizon boundary.  Fong, Li and Tino, arXiv:2408.08071, already apply finite orthogonal dilation to recurrent reservoirs with projected readout.  DeltaProduct identifies Delta factors as generalized Householder maps and permits reflection-like negative eigenvalues; orthogonal/unitary RNNs and GORU cover norm-preserving recurrence, while reversible RNNs explicitly retain lost finite-precision bits in a growing buffer.  HOLA and Sparse Delta Memory are stronger engineering baselines when an explicit bounded cache/slot state is allowed.

Accordingly, the valid artifact is a Delta-specific no-go and finite-horizon control, not a new method.  No project code, test, model, benchmark, training, inference, scorer, download or GPU work was executed.
