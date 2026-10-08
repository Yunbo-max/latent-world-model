# D03/D04 sources actually inspected

Author: /root/delta_retention_derivation. Role: web_supervisor, mathematical authoring only. No project execution, scoring, data/model acquisition, or GPU work. Read 2026-10-08 UTC. These are inspected locators and bounded reading scope, not original-paper copies or an exhaustive novelty search.

## Delta and preconditioned Delta

- DeltaNet arXiv2406.06484v6, 2025-01-15, https://arxiv.org/html/2406.06484v6: §§2.2–3.2, update/residual and ordered low-rank products. State orientation transposed into project key-by-value convention. Ordered transport is inherited linear-recurrence algebra, not a new theorem.
- PDN arXiv2604.21100v1, https://arxiv.org/html/2604.21100v1: §§3.1–3.3 distinguish exact inverse-key-Gram historical regression from actual diagonal approximation. No historical ridge-equivalence claim survives the diagonal substitution unchanged. Direct preconditioning is not counted as a new candidate.
- Author repository `ntumm120/preconditioned-deltanet`, commit `7bd753279af87b39114149a104c5bde9bf67145f`, inspected through exact Git blobs. File `3rdparty/flash-linear-attention/fla/ops/precond_gated_delta_rule/naive.py`, blob `4a2273f25a89b509332e8755391e78cc594a16b0`, function `naive_recurrent_precond_gated_delta_rule(q,k,v,g_atk,g,beta_atk,beta,initial_state,initial_A_state,...)`: inputs q/k/v are B,T,H,K/V; returned S is B,H,K,V; auxiliary A is B,H,K. MIT author source capture `PDN_AUTHOR_NAIVE_PINNED.txt` was read and verified in scratch only, not republished as candidate code or packet source. The published D03_SOURCE_MANIFEST.json records actual byte identities and immutable locators. Actual A statistic decays and adds gated squared keys. A bounded, centered log transform creates diagonal M. Old-state residual is read using k; its write uses M⊙k. This is a direct write-direction baseline for D03.
- At same pin, layer `fla/layers/precond_gated_deltanet.py`, blob `7aff15a31833a648043c10074d7742ad840c14da`, `PrecondGatedDeltaNet.forward` has chunk/recurrent/naive paths, stores recurrent_state/A_state in cache. This layer was read; the original file is not retained here because the recurrence evidence is sufficient.

## QED full-formula reading

QED arXiv2608.13668v1, 2026-08-13, https://arxiv.org/html/2608.13668v1, §§2–3.2 and Discussion. Eq6 forms a gated, key-orthogonal query term in the erase vector. Eq11 keeps the added state edit along the left write direction k. It does not choose the future-transported write direction in D03. Orthogonality leaves the nontrivial eigenvalue unchanged; this does not establish a Euclidean singular-value bound or stability under products of nonnormal transitions. No author repository link appears in inspected paper; author-code interface remains unavailable, not guessed.

## Delayed supervision nearest objective

Delayed Supervision for Test-Time Language Models, arXiv2609.32312v1, 2026-09-26, https://arxiv.org/html/2609.32312v1, §§3.1–3.3 and7. Future semantic QA is an existing outer supervision construction. It keeps native updates, verifies retention/revision labels in simulator trajectories, and isolates answer branches from the continuing history. D03 instead estimates a matrix-valued transported sensitivity from training suffixes and changes the write direction. This difference is a candidate residual, not established originality. Delayed QA, standard continuation CE, and direct suffix-loss differentiation are indispensable simpler explanations. Labels for symbolic revision are not inferable from plain text without an actual supplied labeling process. No authors' source was inspected for this paper in this worker scope; root closest-work audit must complete that interface if needed.

## Finite-precision collision

When Quantization Breaks Memory: Recurrent-State Write-Back in Low-Precision Temporal Inference, arXiv2609.04490v1, 2026-09-03, https://arxiv.org/pdf/2609.04490, primary PDF successfully read after v1-URL and HTML failures. §§2.2–2.3 and Supplement S8, EqsS18–S23 define compensated write-back, clipped floating residual and quantized residual variants. Basic recurrence error feedback is therefore an existing baseline, not D04 novelty. Results concern their fluorescence-lifetime GRU/LSTM setting, not measured Delta faults. No author code is promised here; paper states simulator-repository link withheld for review. D04 is rejected from the new active candidate count; transported full residual is also just an exact lifted affine recurrence with another full state, not an accepted scientific contribution.

## Additional unresolved nearest work

Kalman Delta Networks: Uncertainty-aware Associative Memory, arXiv2609.07816v2, 2026-09-29, https://arxiv.org/pdf/2609.07816. HTML/v1 failures were followed by successful unversioned primary PDF opening; actual header is v2, not v1. Reader /root/delta_math_review_b independently retained KDN_REVIEW_SOURCE_AUDIT.md and exact author oracle KDN_AUTHOR_NAIVE_PINNED.txt, commit53e437be8591521a508bb6a04cd5b26594a3d5ec. I also opened primary PDF and read §§3.2–4.1: gain from predictive posterior covariance is known matrix-weighted residual editing, while D03's matrix estimates future-response perturbation sensitivity. Distinct estimands do not alone establish originality; exhaustive collision/semantic qualification remains open. KDN information scaling acts on post-write precision, affecting later writes while preserving current gain.

## Native measurement feasibility (read-only)

NVIDIA/RULER literal main pinned `c3f5e3b4f87f97e048793bb510a3a6b19a46bf3a`. This is the original main pipeline; current README points to newer v1/v2 branches, which are not silently substituted. Read-only original bytes inspected and hash-bound by D03_SOURCE_MANIFEST.json; full source captures remain scratch-only and are not republished:

| Author path | Git blob | Scratch-only capture |
|---|---|---|
| scripts/data/synthetic/niah.py |729eddc260ef5a9aa0473557cd249abca232764a|RULER_NIAH_PINNED.txt|
| scripts/synthetic.yaml |29cfa5f60b49a7fa53f8dccbbd4f0c7c9e7834fa|RULER_TASK_CONFIG_PINNED.txt|
| scripts/eval/evaluate.py |3cd5663cff3051bacd0e73d28bd440b660bbe50d|RULER_EVALUATE_PINNED.txt|
| scripts/eval/synthetic/constants.py |94b2ba622c14d5e8fcbdf3825f223e13a0e110ec|RULER_METRICS_PINNED.txt|

`generate_input_output` creates published needle tasks; `generate_samples` returns input/outputs plus position/length metadata. Native `get_pred_and_ref` reads input, pred, outputs and ID. `string_match_all` averages reference-substring coverage per prediction; `string_match_part` permits any reference. Neither is exact semantic fact preservation. `run_evaluation_per_task` records empty-output denominator, but main skips absent task files; any later complete evaluation must preserve missing cases as failures or explicit gaps, never silently report a smaller pool. No scorer was executed.

RULER recall can measure ordinary delayed retrieval under published task definitions. It cannot isolate D03's theoretical frozen-feature perturbation metric, distinguish correct revision from coexistence, or certify numerical-state fidelity. Those remain measurement gaps. Native assets are publicly documented; tokenizer, essay/wordlist/scorer dependencies are not acquired or qualified here. Full bAbI20/20000 and LAMBADA5153 remain existing project assets and cannot prove all retention claims alone. A single RTX2080Ti and0.1B/1B target-token backgrounds do not certify the added suffix-target cost or runtime feasibility. No Docker, paid service, synthetic benchmark invention, experiment matrix or dispatch is introduced.
