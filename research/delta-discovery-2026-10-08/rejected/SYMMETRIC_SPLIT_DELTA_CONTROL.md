# Symmetric / Strang-split Delta control

Disposition: **rejected as a distinct candidate; retained as a discretization and coordinate control**. Mathematics/source analysis only; no project execution.

## Exact recurrence

Let (H=D^{1/2}), (C=I-\beta kk^\top). Half-decay, Delta, half-decay gives

\[
S_t=HCHS_{t-1}+\beta Hk v^\top
=DS_{t-1}+\beta w(v-S_{t-1}^\top w)^\top,
\qquad w=Hk.
\]

For invertible (H), it is also an oblique post-decay Delta with reciprocal addresses

\[
r=H^{-1}k,\qquad
S_t=DS_{t-1}+\beta w(v-(DS_{t-1})^\top r)^\top.
\]

Thus exact residual shrinkage is at (r), not generally at the deployed original key (k). For scalar (D=\alpha I), unit (k), and full step, the naive final read is (\sqrt\alpha v): the last half-decay attenuates the just-written target. Repairing same-key overwrite yields

\[
S_t=DS_{t-1}+\beta\frac{Dk}{k^\top Dk}
\left(v-(DS_{t-1})^\top k\right)^\top,
\]

which is precisely a preconditioned/separate-read-write-address Delta step.

## Stability and splitting claim

The homogeneous factor (HCH) is similar to the actual KDA factor (CD), hence has the same eigenvalues, determinant and spectral radius. Under (\|D\|_2\le1) and (0\le\beta\|k\|^2\le2), both (CD) and (HCH) already satisfy operator norm at most one. Per-step symmetry removes one-step Euclidean shear but gives no stronger worst-case ordered-product bound and no lower retention bound; products of time-varying symmetric factors need not be symmetric or commuting.

Calling the construction Strang splitting is legitimate only after declaring a frozen continuous-time affine generator whose decay and Delta subflows are exact. Then the local error is (O(h^3)) rather than Lie splitting's (O(h^2)). A learned token-discrete recurrence supplies neither the simultaneous ODE nor a small-step assumption automatically. The affine commutator also contains the write-source term, so a homogeneous commutation argument is incomplete.

## Closest work and cost

Classical Strang splitting and Macaron Net already cover the generic Lie-to-Strang architecture move. Complex KDA (arXiv:2609.24797v1, section 3) explicitly records that (CD) is similar to (D^{1/2}CD^{1/2}). PDN covers preconditioned write addresses; GDN-2, EDA and generalized DPLR cover separate erase/write geometry; DeltaProduct covers multiple correction factors per token. The construction adds no identity, provenance, revision evidence or capacity.

Diagonal (H) keeps (O(d_kd_v)) leading work and state after algebraic collapse. Dense (D) needs a square root and dense products; inverse address transforms amplify small-decay coordinates. A literal two-half-step implementation adds bandwidth without changing the collapsed map.

**Ruling:** known similarity/preconditioning or conditional numerical-order ablation; no D-number.
