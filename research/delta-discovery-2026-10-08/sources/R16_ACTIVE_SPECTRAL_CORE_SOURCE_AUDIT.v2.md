# R16 v2 active spectral core — source, collision, and measurement audit

- Math artifact: repairs/R16_ACTIVE_SPECTRAL_CORE.v2.md
- Artifact SHA256: e97793f06e6c10eb56bac6dd8913f3435fe604cb9c8de190a2b816d4ea6e43bb
- Scope: bounded primary-source and author-interface audit; not exhaustive priority certification or empirical validation.
- Execution: static source reading and mathematics only; no project/upstream execution, model, benchmark, training, inference, scorer, data/model download, GPU, Docker, or paid service.

## 1. Preserved operational controls

The pinned KDA, EFLA, PDN, S4/S5, Longhorn, and internal R09/R11 controls in R16_NONCOMMUTING_JOINT_FLOW_SOURCE_AUDIT.md remain applicable. V2 does not reinterpret KDA's explicit decay-then-write chronology as an approximation error. It tests a different simultaneous frozen generator, now under a small active-spectrum condition.

The exact endpoint is still a normalized inverse-metric edit. The practical PDN kernel remains diagonal rather than the dense theoretical inverse-Gram object; v2 does not claim that implementation computes \(P_\tau^{-1}\). R09 is the exact internal collision.

## 2. Exact diagonal-plus-rank-one eigendecomposition

Jakovčević Stor, Slapničar, and Barlow, *Forward stable eigenvalue decomposition of rank-one modifications of diagonal matrices*, arXiv:1405.7537v2 / Linear Algebra and its Applications 2015, study

\[
A=D+\rho zz^\top.
\]

Section 1, equations (3)–(5), gives the secular roots

\[
1+\rho\sum_i\frac{z_i^2}{d_i-\lambda}=0
\]

and eigenvectors proportional to \((D-\lambda I)^{-1}z\). The paper states that each eigenpair is \(O(n)\), all eigenpairs are \(O(n^2)\), and the shift-and-invert construction is independently parallelizable across eigenpairs. Section 2 gives algorithm dpr1eig; the paper identifies LAPACK DLAED4 and the public Arrowhead.jl implementation as operational controls. Netlib DLAED4 solves one secular root and DLAED9 updates roots/eigenvectors.

This supports the sharpened core cost when the diagonal basis is already the deployed basis: all \(r\) core eigenpairs are \(O(r^2)\), not a necessary \(O(r^3)\) generic dense eigendecomposition. It does **not** imply a cheap spectral transform for arbitrary symmetric \(\Lambda\), \(O(r)\) for the full core eigenbasis, or cheap dense application to \(m\) value channels. A general eigenspace basis may cost \(O(d^3)\) to discover, \(O(d^2)\) to store, and \(O(drm)\) to project/lift; applying the base exponential can cost \(O(d^2m)\). Applying the dense \(r\times r\) core basis remains \(O(r^2m)\). Repeated diagonal values and zero components require the standard deflation/Givens treatment; the math artifact handles repeated values as spectral groups rather than pretending the irreducible secular formula applies unchanged.

## 3. Matrix-function update and Krylov collision

Beckermann, Kressner, and Schweitzer, *Low-rank updates of matrix functions*, arXiv:1707.03045 / SIAM J. Matrix Anal. Appl. 2018, approximate

\[
f(A+bb^*)-f(A)
\]

in a Krylov subspace. Their Hermitian construction compresses the update to a small matrix function, proves polynomial exactness, analyzes convergence for the exponential, and accounts for matrix-vector, orthogonalization, and small-core costs. This is a direct prior family for v1's Krylov support and for any approximate exponential-action implementation.

Beckermann, Cortinovis, Kressner, and Schweitzer, *Low-rank updates of matrix functions II: Rational Krylov methods*, arXiv:2008.11501 / SIAM J. Numer. Anal. 2021, uses rational Krylov subspaces for the same low-rank-update object. Algorithm 3 covers the Hermitian shared-basis case. Theorem 3.3 gives rational exactness; Theorems 4.3 and 4.5 provide polynomial and Hermitian rational approximation bounds; the exponential specialization supplies pole/convergence controls. The paper also warns that an iterate-difference stopping test is heuristic near stagnation. A finite polynomial/rational Krylov action is therefore not a new Delta mechanism or automatically a certified implementation.

V2's exact reduction is narrower: because \(k\) activates only \(r\) distinct eigenspaces of symmetric \(\Lambda\), that invariant subspace closes exactly and the compressed matrix is the explicit DPR1 core \(D+cc^\top\). This is a useful packet theorem/control, but it resides inside structured matrix-function computation. Its \(O(dm+r^2m+r^2)\) action claim is restricted to coordinate-diagonal/tied groups or an explicitly charged fast fixed basis.

Farrell, *The number of distinct eigenvalues of a matrix after perturbation*, arXiv:1508.07633v2, relates distinct eigenvalue counts and exact Krylov iteration counts after low-rank perturbations. It is compatible with the spectral-dimension viewpoint but does not by itself prove the v2 active-eigenspace identity; the packet derives that identity using the spectral theorem and a Vandermonde argument.

## 4. Generic exponential-action collision

Al-Mohy and Higham, *Computing the Action of the Matrix Exponential, with an Application to Exponential Integrators*, SIAM J. Sci. Comput. 2011, compute \(e^{tA}B\) without forming \(e^{tA}\), using backward-error-driven scaling and truncated Taylor degree selection.

The author's higham/expmv repository was pinned at 779f27e81afba16b9b2454ef0460ecf7bad23988. File expmv.m identifies Algorithm 3.2, selects degree/scaling, and applies the scaled Taylor recurrence. For \(M=D+kk^\top\) with diagonal or otherwise \(O(dm)\)-applicable \(D\), every multiplication by \(M\) and a \(d\times m\) block costs \(O(dm)\). Thus a \(p\)-step action has a direct \(O(pdm)\) baseline under that same fast-matvec interface; a general dense generator must charge its actual block-multiply cost. Calling the action itself novel is untenable.

## 5. Delta/KDA nearest mechanisms

KDA in *Kimi Linear*, arXiv:2510.26692v2, section 3 equation (1), uses

\[
S_t=(I-\beta_tk_tk_t^\top)\operatorname{Diag}(\alpha_t)S_{t-1}
+\beta_tk_tv_t^\top.
\]

Section 6.2 and Appendix B give its constrained-DPLR/WY chunk representation. The order is declared and differs from the exponential of a sum. R16's simultaneous semantics are not the same mechanism, but its varying dense transitions lose this compact exact chunk representation.

DeltaProduct, arXiv:2502.10297, section 4 equation (3), uses multiple sequential online-gradient steps per token and explicitly unrolls their affine product. The author repository was pinned at d62241a81d07aa32b1b65e7d17377f6a7cd0a5d8; flash-linear-attention/fla/layers/gated_deltaproduct.py generates multiple keys, values, and gates before interleaving them into the Delta kernel. Products of multiple rank-one factors are therefore a strong control, not R16 residual novelty.

Complex KDA, arXiv:2609.24797, analyzes \(H_kD\), its commutator, and signed diagonal factors; its theorem characterizes orthogonal DPR1 matrices by a Householder times a diagonal sign matrix. The author repository was pinned at eaca750bf82843c74fb66864980e00c5a70c9a14, with signed decay and a rank-one Householder coefficient \(\beta\in[0,2]\) in fla/layers/complex_kda_layer.py. CKDA does not compute R16's joint exponential, but it blocks broad claims that noncommuting DPR1 expressivity itself is new.

## 6. Structured-SSM and direct-action collision

S4/S5 show that fixed structured or diagonalized continuous generators can admit efficient recurrent/convolutional actions. V2 instead has a token-dependent core \(D_t+c_tc_t^\top\) and active basis \(U_t\). The exact one-token action is structured, but products need not retain one shared low-rank basis. V2 therefore does not inherit a compact exact scan from fixed-generator SSMs.

A direct discrete implementation of equations (10)–(12) is exactly the same function as the continuous-time story. Any claimed advantage must be against this same-action control and against grouped KDA at matched information, active-group count, tolerance, and total computation.

## 7. Certified grouping boundary

The Duhamel bounds in equations (17)–(18) follow from the integral identity for exponential perturbations and the contraction norm of \(e^{-tA}\) for \(A\succeq0\). Equation (19) additionally assumes an explicit positive lower bound on both endpoint denominators. These are deterministic numerical-analysis certificates; they do not identify which decay groups are scientifically correct, cover low-precision roundoff/backward cost, or certify downstream model quality.

The grouped generator changes the target object. A grouped-KDA baseline is mandatory so that any benefit cannot be attributed merely to smoothing the decay spectrum or spending an \(r^2m\) core budget. For a non-coordinate basis, basis discovery, forward/backward transforms, base-exponential action, and storage are also part of the matched budget.

## 8. Exact scan and native measurement boundary

One-token exact action does not imply training-time sequence parallelism. With varying \(U_t\), products of

\[
e^{-\tau_t(\Lambda_t+k_tk_t^\top)}
\]

are generally dense and do not remain diagonal-plus-fixed-rank. Exact associative prefix combination therefore needs a new closed representation or dense composition; approximate recompression needs cumulative forward, backward, and gradient error contracts.

bAbI, LAMBADA, RULER, and LongMemEval do not jointly expose a true continuous sub-token generator, active spectral groups, exact internal state action, causal validity labels, and matched-cost controls. Synthetic frozen matrix fixtures could later verify the numerical identities, but that would be numerical validation rather than a natural scientific benchmark. No execution or result is claimed here.

## 9. Audit decision

- Mathematical consistency: conditionally supported for symmetric PSD \(\Lambda\), frozen \(k,v,\tau\), declared active groups, \(k\ne0,\tau>0\) for normalized formulas, and the stated denominator condition for normalized approximation. Efficient action additionally requires coordinate-diagonal/tied groups or a separately charged fast fixed basis.
- Numerical originality: REJECTED_MAJOR_COLLISION.
- Delta-specific residual: PARTIAL_THEOREM_DELTA.
- Bounded-search priority: INCONCLUSIVE_EXPAND_SEARCH; no first/new claim.
- Architecture candidate: not admitted.
- Scalable training and scientific value: unclosed.
- Experimental effect: unknown; no execution.

The retained contribution is an exact active-spectrum dimension/core theorem, a corrected DPR1 cost statement, and certified grouping error. The endpoint updater, matrix-function machinery, exponential action, multiple rank-one products, and broad noncommuting DPR1 expressivity have strong prior controls. Reopen requires independent evidence for the simultaneous generator and a matched-cost consequence unavailable to grouped KDA, direct DPR1 action, expmv, rational Krylov, CKDA, and DeltaProduct.
