# NOGO-OBLIQUE-03 — a bare oblique erase factor cannot be Euclidean-nonexpansive

Disposition: **accepted no-go/control; not a candidate**.  This elementary rank-one result prevents treating an unconstrained oblique erase direction as a free retention improvement.

## Exact singular-value reduction

Let \(k,a\in\mathbb R^d\), \(\|k\|_2=1\), and

\[
A=I-ka^\top.
\]

Write

\[
a=ck+su,
\qquad u^\top k=0,
\qquad \|u\|_2=1,
\qquad s\ge0.
\]

On the ordered orthonormal basis \((k,u)\),

\[
Ak=(1-c)k,
\qquad
Au=u-sk,
\]

so the nontrivial block is

\[
B=
\begin{pmatrix}
1-c & -s\\
0 & 1
\end{pmatrix}.
\]

With \(\tau=(1-c)^2+1+s^2\), the two eigenvalues of \(B^\top B\) are

\[
\lambda_\pm=
\frac{\tau\pm\sqrt{\tau^2-4(1-c)^2}}{2},
\]

and the block singular values are \(\sqrt{\lambda_\pm}\).  For \(d>2\), the orthogonal complement contributes singular values equal to one.

## Nonexpansiveness iff the erase is aligned and bounded

If \(s>0\), then for the unit vector \(u\),

\[
\|Au\|_2^2=\|u-sk\|_2^2=1+s^2>1.
\]

Hence every genuine oblique component forces \(\|A\|_2>1\), independently of \(c\).  If \(s=0\), then

\[
A=I-ckk^\top,
\qquad
\|A\|_2=\max\{1,|1-c|\},
\]

with the obvious removal of the orthogonal-complement value in one dimension.  Therefore

\[
\|A\|_2\le1
\quad\Longleftrightarrow\quad
s=0\ \text{and}\ c\in[0,2].
\]

The endpoints are exact: \(c=0\) is the identity and \(c=2\) is a Householder reflection.  For a key-by-value state, the induced Frobenius norm of left multiplication \(S\mapsto AS\) is likewise controlled by \(\|A\|_2\).

## Scope: the result does not decide the full ordered update

An independent pre-decay changes the conclusion.  From \(\|A\|_2>1\) one cannot infer

\[
\|AD\|_2>1
\quad\text{or}\quad
\|DA\|_2>1.
\]

For example, \(D=\gamma I\) yields norm \(\gamma\|A\|_2\), which is nonexpansive for sufficiently small \(\gamma\).  A general \(D\) can attenuate or eliminate the expanding direction.  The actual multiplication order must be retained because \(AD\) and \(DA\) need not agree; only orthogonal \(D\) preserves \(\|A\|_2\).

This no-go concerns the bare factor \(I-ka^\top\) in the Euclidean/Frobenius geometry.  It does not rule out oblique erase mechanisms with compensating decay, a different metric, bounded transient expansion, or explicitly paid numerical conditioning.  It is known elementary linear algebra and supplies a guardrail, not a new Delta mechanism.  No project code, test, benchmark, model, training, inference, scorer or GPU work was executed.
