# Counterfactual query-visible write utility — future CE attribution, not a new Delta rule

Disposition: **rejected as a distinct method; retained as a training diagnostic/control**.

## Exact frozen-path contribution

Let

\[
\bar S_i=D_iS_{i-1},
\qquad e_i=v_i-\bar S_i^\top k_i,
\qquad E_i=\beta_i k_i e_i^\top,
\]

and freeze all later features so \(A_j=(I-\beta_jk_jk_j^\top)D_j\).  Removing only source edit \(E_i\), while retaining its pre-decayed state, gives exactly

\[
S_u-S_u^{(-i)}=P_{u\leftarrow i}E_i,
\qquad P_{u\leftarrow i}=A_u\cdots A_{i+1}.
\]

At a future query,

\[
\delta m_{i,u}
=\beta_i(q_u^\top P_{u\leftarrow i}k_i)e_i.
\]

This is query-visible and signed, unlike D07's raw \(\|Pk_i\|^2\).  If downstream logits are affine, \(\delta z_{i,u}=R_u\delta m_{i,u}\), and the exact frozen-feature cross-entropy utility is

\[
U_{i,u}=\ell(z_u-\delta z_{i,u},y_u)-\ell(z_u,y_u)
=(\delta z_{i,u})_{y_u}
+\operatorname{LSE}(z_u-\delta z_{i,u})
-\operatorname{LSE}(z_u).
\]

Positive \(U\) says the write helped the observed target; negative \(U\) says it hurt.  In a nonlinear whole network, subtracting the frozen source is not a full causal deletion if future keys, gates, queries or hidden states change.  Exact deletion then requires replay; a Jacobian is only a local approximation.

## Exact equivalence to ordinary future CE for write-local parameters

For parameters \(\theta_i\) affecting only source write \(i\), write \(z_u=z_u^{(-i)}+\delta z_{i,u}(\theta_i)\).  The leave-one-write-out branch is independent of \(\theta_i\), so

\[
\nabla_{\theta_i}[-U_{i,u}]
=\nabla_{\theta_i}\ell(z_u,y_u).
\]

Maximizing exact utility therefore supplies exactly the ordinary future-CE gradient, plus a write-independent baseline.  Its local expansion is the familiar influence quantity

\[
U_{i,u}\approx
-\nabla_z\ell(z_u,y_u)^\top\delta z_{i,u}
+\tfrac12\delta z_{i,u}^\top H_\ell\delta z_{i,u}.
\]

A positive-margin loss wrongly requires unrelated writes to help every sampled query.  With shared parameters, directly maximizing the loss difference can also improve the objective by degrading the counterfactual branch rather than improving the real one.

A detached target \(\bar U_i\) used to train a causal predictor for the write gate is merely delayed teacher/future-CE distillation.  It needs a frozen or EMA teacher to avoid a moving target and must be compared with equally informed future CE and delayed QA.

## Why retrospective sign does not solve revision

A later negative utility can diagnose that an old write became harmful.  It cannot selectively remove the write after its contribution has mixed into a fixed aggregate state.  Selective release needs stable source identity, an event store or retained per-source traces; keeping exact traces grows with the number of writes.  An unpredictable future revision cannot be anticipated by a causal gate at source time.

Single-source leave-one-out also fails under redundancy and synergy, depends on horizon/metric, can miss temporary computation, and is not invariant to compensating downstream reparameterizations.  Shapley-style coalition credit addresses some interactions but is established and much more expensive.

## Nearest work and cost

How Linear Attention Remembers already defines the transported source contribution and query access.  AttriMem uses signed source ablation attribution as process reward for retain/update/discard decisions; HiMPO uses signed local counterfactual memory utility plus hindsight relevance.  ContextCite, influence functions, TracIn and Data Shapley cover the broader source-credit mathematics.  Delayed Supervision is the strongest simpler semantic alternative inside Delta/RWKV-style recurrent memory.  LoLA's self-recall error is unsigned and routes to sparse cache, but is another direct memory-selection baseline.

Tracking \(M\) frozen source directions costs \(O(Md_k)\) state and \(O(MTd_k)\) work for diagonal-plus-rank-one Delta transitions; exact nonlinear deletion can require one replay per source.  Training-only attribution leaves inference unchanged and therefore supplies no new deployed mechanism.

The Delta-specific formula is useful as a diagnostic separating query access from raw state survival.  It does not define an active candidate.  No project code, test, model, benchmark, training, inference, scorer, download or GPU work was executed.
