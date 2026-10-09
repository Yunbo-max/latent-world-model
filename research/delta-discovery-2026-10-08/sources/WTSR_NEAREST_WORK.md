# D07 / WTSR nearest-work lead audit

Reader: `/root/retention_candidate`, with root verification of the primary arXiv records on 2026-10-09.  Status: sufficient to define the collision question, **not** sufficient to clear originality or scientific admission.  No code, model, data, scorer or experiment was executed.

## How Linear Attention Remembers

Kichang Lee et al., *How Linear Attention Remembers*, arXiv:2609.33093v1, submitted 2026-09-27: <https://arxiv.org/abs/2609.33093>.

Section 2.2 / Eqs. 3--5 gives the same family of source-contribution decomposition: an earlier write is propagated by the ordered later transitions, and later-write overlap controls interference.  Its analysis and causal interventions establish that source traces are not new.  The bounded reading did not locate WTSR's exact arbitrary-key finite-horizon hinge loss in this paper.  That negative is only a lead for the next collision round.

## Tabular ICL write-rate decay

David L. Schnurr et al., *Adapting Linear-Time Architectures for Tabular In-Context Learning*, arXiv:2609.36337v1: <https://arxiv.org/abs/2609.36337>.

Section 4.4 and Appendix D.7 / Eq. 10 analyze the same-key scalar contribution

\[
C_s=\beta_s\prod_{t>s}(1-\beta_t)
\]

and introduce time-dependent effective write-rate decay \\(\beta_t^{\rm eff}=\beta_t c/(t+c)\\).  This is a major functional neighbor because it explicitly modifies later write strength to preserve earlier contributions.  The author repository `schnurrd/ICL-Architectures` and README paths `PFNs/configs/fla/fla_config.py` / `--config-arg` were located, but an immutable commit, blob and function-level implementation have not yet been pinned.  No stronger source-code claim is made.

## Delayed supervision

Jinha Kim and Taksh Kothari, *Delayed Supervision for Test-Time Language Models*, arXiv:2609.32312v1, submitted 2026-09-26: <https://arxiv.org/abs/2609.32312>.

Section 3 / Eqs. 4--6 leaves the recurrent update unchanged and trains long-term usability through delayed semantic questions.  It is a stronger simple alternative whenever verified delayed labels exist.  WTSR instead supplies a label-free frozen-path state-survival proxy; that distinction does not by itself establish scientific value.

## Collision question left open

The narrow residual is:

> regularize the finite-horizon norm survival of each realized arbitrary-key Delta write direction through the actual ordered later Delta transitions, without protecting every state direction or conditioning on a selected future query.

This is mathematically distinct from D03's \\(P^\top q\\) output-sensitivity metric and D06's global log-determinant floor.  It may still be only a more detailed same-function regularizer than write-rate decay, source-trace preservation, delayed supervision or ordinary long-horizon CE.  D07 therefore requires an independent exact-byte math review and a fixed-author-code/full-formula collision audit before any admission.
