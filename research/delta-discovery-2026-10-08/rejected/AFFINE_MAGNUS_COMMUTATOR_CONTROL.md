# AFFINE-MAGNUS-COMMUTATOR — order diagnostic, not a Delta candidate

Disposition: **conditionally valid order diagnostic/control; not a candidate**.

For affine Delta steps

\[
T_i(S)=A_iS+B_i,qquad
A_i=I-\beta_i k_ik_i^\top,qquad
B_i=\beta_i k_iv_i^\top,
\]

chronology “\(i\) then \(j\)” means \(T_j\circ T_i\).  The exact adjacent-order gap is

\[
T_jT_i(S)-T_iT_j(S)
=[A_j,A_i]S+(A_j-I)B_i-(A_i-I)B_j.
\]

For unit keys and \(c=k_i^\top k_j\),

\[
[A_j,A_i]=\beta_i\beta_jc
(k_jk_i^\top-k_ik_j^\top),
\quad
\|[A_j,A_i]\|_2=
\beta_i\beta_j|c|\sqrt{1-c^2}.
\]

The affine terms cannot be omitted.  With the same key, transition matrices commute but

\[
T_jT_i(S)-T_iT_j(S)
=\beta_i\beta_jk(v_j-v_i)^\top.
\]

At exact overwrite, this is precisely last-write/revision semantics.

## What Magnus aggregation actually says

Represent an affine map by a homogeneous block.  When a compatible logarithm exists,

\[
\mathcal T_i=e^{\mathcal X_i},\qquad
\mathcal X_i=
\begin{bmatrix}X_i&b_i\\0&0\end{bmatrix},
\]

where \(A_i=e^{X_i}\) and \(B_i=\phi_1(X_i)b_i\), not generally \(B_i=b_i\).  The bracket is

\[
[\mathcal X_j,\mathcal X_i]=
\begin{bmatrix}
[X_j,X_i]&X_jb_i-X_ib_j\\0&0
\end{bmatrix}.
\]

For chronology \(i\) then \(j\), BCH gives

\[
\log(e^{\mathcal X_j}e^{\mathcal X_i})
=\mathcal X_j+\mathcal X_i+
\tfrac12[\mathcal X_j,\mathcal X_i]+O(\|\mathcal X\|^3).
\]

Thus \(+\tfrac12\) is the second-order term required when approximating the ordered product by one aggregate exponential.  Adding a negative bracket to an already exact sequential recurrence instead suppresses chronology; it is not an accuracy correction.

For the same key and \(0\le\beta<1\), \(a=-\log(1-\beta)\), \(X=-akk^\top\), \(b=akv^\top\) reproduce the exact affine step.  The affine bracket is \(a_ia_jk(v_j-v_i)^\top\), matching the small-step order effect.  Canceling it makes old/new order invariant and destroys the desired revision behavior.

## Scope and cost

Exact erase \(\beta=1\) and zero decay are singular, so a compatible logarithm may fail.  Second-order truncation also needs small generators and controlled cumulative norm; \(-\log(1-\beta)\) diverges as \(\beta\to1\).  Long horizons accumulate nested commutators.  State-dependent future features require nonlinear vector-field/Jacobian brackets rather than frozen affine matrices.

Exact affine composition

\[
(A_j,B_j)\star(A_i,B_i)
=(A_jA_i,A_jB_i+B_j)
\]

is already associative and preserves chronology, so parallel scan does not require commutation.  Dense generator/log/bracket/exponential state costs at least \(O(d^2+dd_v)\) storage and generic \(O(d^3+d^2d_v)\) work; rank grows across many brackets and general KDA decay destroys a fixed low-rank form.

Classical BCH/Magnus and commutator-free integrators, exact affine scans, DeltaNet/DeltaProduct ordered low-rank products and order-invariant RLS/PDN are direct neighbors.  The missing ingredient would be a semantic selector that suppresses harmful interference brackets but preserves legitimate revision brackets.  Algebra alone cannot identify it, returning to the revision/coexistence no-go.

No project code, test, model, benchmark, download or experiment was executed.
