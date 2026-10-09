# Exact-flow / implicit-proximal Delta control

Disposition: **rejected as a distinct candidate; retained as an exact reparameterization control**. Mathematics and source analysis only; no project code, test, training, inference, benchmark, model/data download or experiment was run.

## Exact object

With key-by-value state \(S\in\mathbb R^{d_k\times d_v}\), post-decay state \(\bar S=D S_{t-1}\), key \(k\), target \(v\), \(a=k^\top k\), and residual \(e_0=v-\bar S^\top k\), consider

\[
\dot S=k(v-S^\top k)^\top .
\]

Because \(\dot e=-a e\), the exact frozen-token flow is

\[
S(\tau)=\bar S+c_F k e_0^\top,
\qquad c_F=\frac{1-e^{-a\tau}}{a}.
\]

The proximal/implicit update

\[
S^+=\arg\min_U\frac{\|U-\bar S\|_F^2}{2\eta}
+\frac12\|U^\top k-v\|^2
\]

is

\[
S^+=\bar S+c_P k e_0^\top,
\qquad c_P=\frac{\eta}{1+\eta a}.
\]

Both are ordinary Delta updates with a scalar effective step. They are the same family under

\[
\eta=\frac{e^{a\tau}-1}{a}.
\]

For unit keys, \(\tau=\operatorname{softplus}(z)\) gives \(1-e^{-\tau}=\sigma(z)\); \(\eta=e^z\) gives \(\eta/(1+\eta)=\sigma(z)\). Forward map and gate gradient therefore coincide exactly with the standard sigmoid-gated Delta recurrence.

For any query,

\[
\Delta o(q)=c(q^\top k)e_0,
\]

so cross-query interference, lack of event identity, and revision-versus-collision ambiguity are unchanged. The old-state transition has eigenvalue \(1\) on \(k^\perp\) and \(e^{-a\tau}\) or \((1+\eta a)^{-1}\) on \(k\): it is nonexpansive, not globally contractive, and stability is not retention. Exact overwrite appears only in the infinite-time/infinite-prox-strength limit and is the known minimum-Frobenius projection/NLMS update.

## Closest work and implementation boundary

- EFLA, arXiv:2512.12602v5, Eqs. 10--15 and 28, explicitly derives the exact zero-order-hold flow and coefficient; its official `mnist.py` computes `-expm1(-beta*lambda)/lambda` before the identical erase/write recurrence.
- Longhorn, arXiv:2407.14207v5, Eqs. 5--7, derives the same implicit proximal rank-one map. Its efficient deployed recurrence uses a diagonal approximation, but the full mathematical object is already present.
- DeltaNet (ICML 2021), NLMS/passive-aggressive projection, and implicit online learning cover the explicit, normalized and proximal limits.

The leading cost remains (O(d_kd_v)) work and state; exact flow adds a scalar `expm1`/division and needs an (a\to0) limit. Large (a\tau) saturates both update and gradient. Multiple ODE substeps do not enlarge the reachable map family while (k,v) are frozen. A simultaneous noncommuting decay generator would be a different object and was not smuggled into this route.

**Ruling:** direct algebraic and primary-source collision; no D-number.
