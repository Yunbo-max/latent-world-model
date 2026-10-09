# Orthogonal value rotation: isometric editability control

Disposition: **rejected as a standalone candidate; retained as an equivalence/no-go control**. No project execution was performed.

## Global value rotation

For key-by-value state \(\bar S\in\mathbb R^{d_k\times d_v}\), read \(o(q)=\bar S^\top q\). A global value-space orthogonal update

\[
S^+=\bar S Q^\top,\qquad Q^\top Q=I
\]

changes every output to \(o^+(q)=Qo(q)\). For current \(y=\bar S^\top k\), exact \(Qy=v\) is possible iff \(\|y\|=\|v\|\); otherwise the minimum error is \(|\|y\|-\|v\||\).

If a protected value subspace \(W\) must be fixed pointwise, exact feasibility is

\[
P_Wy=P_Wv,
\qquad
\|P_{W^\perp}y\|=\|P_{W^\perp}v\|.
\]

Equivalently, for protected columns plus the edited output, the old and target Gram matrices must match. As the protected span becomes full, the only feasible edit is \(v=y\).

When feasible, a Householder reflector maps \(y\) to \(v\):

\[
H=I-2nn^\top,
\qquad n={y-v\over\|y-v\|}.
\]

But it reflects every unseen output containing component along \(n\). Procrustes gives the best batch compromise when the Gram condition fails; it is not exact preservation.

## The attractive local construction is exactly Delta

For unit \(k\), rotate only the selected state row:

\[
\mathcal T_{k,Q}(\bar S)
=(I-kk^\top)\bar S+kk^\top\bar S Q^\top.
\]

For fixed \(Q\), this is a Frobenius-isometry. Its query effect is

\[
\Delta o(q)=(q^\top k)(Q-I)y.
\]

If \(Qy=v\), then

\[
\mathcal T_{k,Q}(\bar S)=\bar S+k(v-y)^\top,
\]

which is exactly the unit-key, full-step ordinary Delta update. Cross-query interference is unchanged:

\[
\Delta o(q)=(q^\top k)(v-y).
\]

If \(Q\) is chosen state-dependently to force the same fixed target \(v\), the overall mapping is simply row replacement

\[
F(\bar S)=(I-kk^\top)\bar S+kv^\top,
\]

whose Jacobian \((I-kk^\top)\Delta S\) is singular. Pointwise existence of an orthogonal \(Q(\bar S)\) does not make this adaptive map reversible or information-preserving.

## Partial, affine and lifted routes

For equal-norm endpoints, spherical interpolation preserves norm, but at the same \(\beta\) its Euclidean move

\[
2r\sin(\beta\theta/2)
\]

is at least the chordal Delta move \(2\beta r\sin(\theta/2)\). Norm preservation alone does not imply association retention.

A key-local affine translation is again a rank-one Delta write. A global affine isometry still must preserve distances to all protected anchors. A spherical lift can equalize norms only by adding hidden value coordinates; that state and decoding must be charged and collides with unitary-dilation/event-memory controls.

Pure multiplicative orthogonal state updates cannot write from \(S_0=0\). Adding an injection returns to an affine/bilinear RNN. Products preserve norm in exact arithmetic but can rotate an old association completely away; undo requires retaining the ordered transformation history.

## Costs and nearest work

A dense \(Q\) costs \(O(d_v^2)\) state and \(O(d_kd_v^2)\) to materialize; a reflector or plane rotation costs \(O(d_v)\) factor state and \(O(d_kd_v)\) application. A protected rank-\(r\) basis costs \(O(d_vr)\), while editability vanishes as \(r\to d_v\).

Householder and orthogonal Procrustes are classical. Unitary/orthogonal RNNs already use isometries for stability. Multiplicative Orthogonal Sequential Editing (AAAI 2026, DOI 10.1609/aaai.v40i40.40707) directly occupies orthogonal multiplicative model editing. GSA2, QED, Oja-style corrections, null-space editing and standard Delta cover the flexible residual/protection alternatives. The exact local construction above is not merely similar: it produces the identical Delta state.

Existing LM/retrieval/model-editing benchmarks can measure final behavior, but none identifies an internal value rotation as the cause or natively tests the Gram-feasibility theorem. No new benchmark should be invented for this route.

**Ruling:** global rotations are over-broad; exact local rotations equal ordinary Delta; adaptive target matching loses isometry; affine/lifted escapes add ordinary residual writes or billed extra state. No D-number is assigned.
