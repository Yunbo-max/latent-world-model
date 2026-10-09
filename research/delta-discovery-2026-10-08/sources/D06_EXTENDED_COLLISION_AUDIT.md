# D06 extended collision audit

Reviewer: `/root/d06_extended_collision`.  Scope: primary-paper mathematics and static author-repository interface reading; no project code, test, model, benchmark or experiment was executed.

Disposition: **major functional composition collision; narrow literal residual not admitted**.  Preserve the log-volume inequality as a diagnostic/guardrail and equal-cost control; remove D06 from the active candidate pool.

## What remains literally unmatched

The bounded search did not find a paper placing the exact ordinary-Delta cost

\[
c_t=-\log\det[(I-\beta_tk_tk_t^\top)D_t]
\]

inside the same length-(W) causal hard budget.  This negative search result is not an originality proof.  The residual is a direct composition of known retention/spectral controls and known rolling resource-budget controllers, without a new allocation theorem.

## Dynamic lower-bound retention gates

HGRN, Qin, Yang and Zhong, NeurIPS 2023, Algorithm 1 / Eq. 2, uses an input-dependent forget gate with a learned lower bound,

\[
\lambda_t=\gamma^k+(1-\gamma^k)\odot\mu_t,
\qquad
h_t=\lambda_t\odot e^{i\theta}\odot h_{t-1}
+(1-\lambda_t)\odot c_t.
\]

The lower bound rises monotonically across layers, giving upper layers slower decay while retaining parallel scan because the gate depends only on the current input.  This directly covers the neural function “make retention input-dependent but prevent its decay from becoming too aggressive”.  D06 replaces the per-channel learned floor with a global rolling log-volume cap and applies it to the Delta matrix erase.

Primary paper: <https://proceedings.neurips.cc/paper_files/paper/2023/hash/694be3548697e9cc8999d45e8d16fe1e-Abstract-Conference.html>.  Official repository: <https://github.com/OpenNLPLab/HGRN>; its README points to `Doraemonzzz/hgru-pytorch` for standalone code and identifies `hgru/`, `example.py` and `grad_check.py`.  The available page did not expose a stable commit SHA, so this is recorded as a branch-level interface rather than a fabricated immutable pin.

## Window budgets and token buckets

Liakopoulos et al., *Cautious Regret Minimization: Online Optimization with Long-Term Budget Constraints*, ICML 2019, defines COLD and a comparator class constrained on every length-(K) window, then studies regret/budget tradeoffs: <https://proceedings.mlr.press/v97/liakopoulos19a.html>.  Its learner's theorem is not D06's exact hard causal realization, so this is a functional, not formula-level, collision.  Token-bucket rollout/control literature likewise makes the accumulated bucket level an explicit state and permits saving and bursts.  D06's queue of the previous (W-1) realized costs is the continuous-cost version of a standard sliding-window limiter.

## Spectral, Jacobian and reversible recurrence family

Spectral-RNN explicitly constrains transition singular values near one; coRNN and UnICORNN derive lag-independent/controlled hidden-gradient bounds under stated step/weight assumptions; LEM uses state-dependent timescale gates; LinOSS supplies stable time-reversible recurrence with associative scan; Reversible RNNs restore exact reversal by storing finite-precision lost bits.  Their author repositories include:

- `zhangjiong724/spectral-RNN/code`;
- `tk-rusch/coRNN`;
- `tk-rusch/unicornn` (`network.py::{UnICORNN_CODE,UnICORNN_compile}` in the task examples);
- `tk-rusch/LEM/{src,LEM_cuda}`;
- `tk-rusch/linoss`;
- `matthewmackay/reversible-rnn::{revgru.py,revlstm.py,buffer.py}`.

None is the same Delta hard-budget formula.  Together they cover the broad contribution claim “impose structural/spectral/reversible guarantees for long-range recurrence”.

## D06's missing optimization object

The actual scalar rule

\[
c_t=\min\left(\widetilde c_t,
B-\sum_{j=t-W+1}^{t-1}c_j\right)
\]

is greedy maximal-feasible clipping in cost space.  It is not a projection unless a metric and feasible-variable map are specified and the corresponding minimizer is derived.  If \\(\widetilde c_t\ge B\\), it can generate \\([B,0,\ldots,0,B,\ldots]\\); the equally feasible allocation (B/W) avoids starving the next (W-1) updates.  With no future utility, oracle, regret or competitive theorem, D06 establishes hard feasibility but not useful allocation.

Radially scaling both the write/erase gate and decay cost also lacks an optimality argument.  The D06 card itself shows that decay does not improve the current post-decay residual, so proportional scaling of the two costs is not derived from the immediate correction objective.  Euclidean projection onto a simplex would generally not equal this radial map.  Finally, a determinant aggregates all directions and is dimension-conservative; it does not identify semantically important or query-relevant directions.

## Surviving control value

Under the declared contractive frozen-feature path, the budget yields the useful conditional bound

\[
\sigma_{\min}(P)\ge e^{-B}.
\]

This is a cheap scalar diagnostic, guardrail or fixed-cap/soft-penalty baseline.  It should not count toward the 20 active candidates.  A future candidate would need a task/query-weighted causal allocation objective together with a valid optimality, regret or competitive result and a compatible parallelization story; simply renaming the present radial clip is insufficient.
