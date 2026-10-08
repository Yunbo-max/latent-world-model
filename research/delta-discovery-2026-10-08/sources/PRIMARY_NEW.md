# Delta primary-source audit — 2026-10-08

Actual reader: `/root/delta_primary_audit`, delegated by `/root`. Role: math-only `web_supervisor`. Papers and pinned author source were read; no source imported/executed, no tests, training, scoring, data or model downloads. This document is an evidence audit, not a candidate qualification or originality verdict.

## QED: full-text prerequisite resolved; author-code prerequisite open

Primary: [arXiv:2608.13668v1 PDF](https://arxiv.org/pdf/2608.13668), 13 August 2026, 10 pages. Read pp1–4 §§2–3, pp6–8 discussion, p9 Appendix A, p10 references. Direct HTML/PDF opening initially failed; indexed primary PDF subsequently opened successfully. The previous abstract-only record must not be mistaken for this formula reading.

For unit key k, its Eq6 changes the erase/read vector to a=b⊙k+λd, d=(I−kkᵀ)(b⊙q). The write direction remains k: S=(I−kaᵀ)D S_previous+k(w⊙v)ᵀ. Eq11–12 give ΔS=−λk(Sbarᵀd)ᵀ and Δo(q)=−λ(qᵀk)Sbarᵀd relative to GDN2. It samples key-orthogonal old content, then cancels through the editable key component. It still cannot change a probe x⊥k, and its immediate effect is zero when q⊥k. Appendix A caps learned per-head λ at0.25. Orthogonal projection preserves aᵀk and the nontrivial eigenvalue; the paper does not establish a Euclidean contraction or arbitrary-product norm bound. Its gate/projection component necessity remains inconclusive in reported ablations. No code link occurs in the inspected PDF; primary author repository not identified by targeted search or 99 GitHub code-search matches to the arXiv ID. This is an unresolved interface gap, not proof that no code exists.

## Our algebraic consequence of the QED recurrence

This subsection is an independently performed calculation, not a claim taken from the authors. Freeze inputs/features and set D=I. In orthonormal basis [k,u] with a=c k+s u, the two-dimensional transition is A=[[1−c,−s],[0,1]]. Since Au=−s k+u, ||Au||²=1+s²: any nonzero oblique component violates Euclidean non-expansiveness, while the eigenvalues remain1 and1−c. For 0<c<1, A^n has upper-right entry −s[1−(1−c)^n]/c. Thus its asymptotic shear can be large even without expansive eigenvalues.

This is attainable within QED's gate structure: k=e1,q=e2,b=(ε,1−ε), 0<ε<1, λ>0 gives c=ε, s=λ(1−ε). Taking ε small makes s/c arbitrarily large. These are admissible mathematical feature inputs, not an observed project/model failure or a native benchmark. A nontrivial decay can moderate this example but requires an actual bound on the full ordered transition. A learned contextual encoder can avoid the regime; no unconditional model-performance conclusion follows. A proposal based solely on an unchanged spectral radius has not closed this condition. A different safe construction still needs nearest-work review: merely appending an orthogonal contraction already collides with EDA and multi-step Delta baselines.

## PDN: exact theory versus actual stable diagonal recurrence

Primary: [2604.21100v1](https://arxiv.org/html/2604.21100v1), 22 April 2026; inspected §§2.3–3.5, Theorem3.1, Appendix C.1–C.3 and E.3/F.1.3. In the paper's value-by-key convention, exact P=(λI+Σkkᵀ)⁻¹ yields write key P_previous k/(1+kᵀP_previous k), and recovers historical ridge from zero initialization. Diagonal approximation removes this exact equivalence. Actual stable ATK uses the current diagonal accumulator, bounded log-space squash, and drops the Sherman–Morrison normalization. Hence “inverse-Gram exact theory” and “stable practical PDN” are different baselines; neither proves predictive sufficiency.

Pinned author commit: [7bd753279af87b39114149a104c5bde9bf67145f](https://github.com/ntumm120/preconditioned-deltanet/tree/7bd753279af87b39114149a104c5bde9bf67145f). `3rdparty/flash-linear-attention/fla/ops/precond_gated_delta_rule/naive.py`, function `naive_recurrent_precond_gated_delta_rule`, returns `(o,S,A)`, accepts separate initial S/A and gates. Its A update precedes M=exp(−log(x) r/(1+|r|)), r=log(A+eps)−center; residual reads raw k, write uses M⊙k. `fused_recurrent.py` implements the same data path, optional decay/layout/variable sequence controls; that recurrent autograd backward explicitly raises NotImplementedError. The existence of a separate chunk path must not be replaced with a claim that this particular recurrent function trains. No author code was executed.

## GDN2: author source exists; channel gating is not free write addressing

Primary: [2605.22791v1](https://arxiv.org/html/2605.22791v1), 21 May 2026; inspected §§2–3, Eq8–10 and chunkwise section. Key-by-value recurrence S=(I−k(b⊙k)ᵀ)D S_previous+k(w⊙v)ᵀ changes erase/read channels and value-write channels; left write direction remains k. This already covers simple erase/write-strength decoupling. An early audit filter missed the lowercase `gdn2` source paths; it was corrected by reading the full recursive tree.

Pinned author commit: [ac0c3cd94709351da07c1c114ad322472b29716b](https://github.com/NVlabs/GatedDeltaNet-2/tree/ac0c3cd94709351da07c1c114ad322472b29716b). `lit_gpt/gdn2.py`, class `GatedDeltaNet2.forward`, predicts sigmoid b/w, dispatches chunk or recurrent kernels, and updates layer cache. Optional erase-range extension multiplies b by2. `lit_gpt/gdn2_ops/fused_recurrent_gdn2.py`, functions `fused_recurrent_gdn2_fwd_kernel` and `fused_recurrent_gdn2`, applies decay, reads through b⊙k, forms w⊙v−erase, writes rank-one along k, then reads q. Shapes include b[B,T,HV,K], w[B,T,HV,V], state[N,HV,K,V], with optional transposed layout. Kernel/source existence is statically verified, runtime correctness is untested here.

## GKA: use v3 and finite Chebyshev solve, not a per-token exact inverse

Primary: [2511.21016v3](https://arxiv.org/html/2511.21016v3), 17 May 2026; inspected §4.1, Algorithm1, §4.2, Appendix B/C/J and compared v1 §4.1. It maintains H/U statistics and outputs U CH(H+λI,q,r), λ=a||H||F; spectral bounds require positive norm/regularization. v3 fixes Algorithm1 ω0=2 (v1 displayed0 while Appendix B specified2). Canonical β-augmented H/U inputs are now recommended, while reported paper experiments used β=1. Appendix J already covers latent sketching. A finite iteration solver is approximate; exact ridge/Kalman optimality belongs to its limiting/formal object and assumptions.

Pinned author commit: [774c1048afd826e35b9222a7116ffd0fc50bcad6](https://github.com/awslabs/hybrid-model-factory/tree/774c1048afd826e35b9222a7116ffd0fc50bcad6). Under `training/src/hmf/model/hybrid_zoo/layers/gated_kalmanet/ops/chebyshev/`, `gka_chebyshev_solve.py` exposes `latent_chebyshev`, `gka_chebyshev_gla`, `torch_decoding_one_step`; configuration includes num_iter, ridge_strength, solver_type, bp_lambda. `chebyshev_iteration.py` exposes `chebyshev_iteration_forward_triton` and `ChebyshevIteration`, uses ω=2 and returns solved query, Frobenius statistics, and key-key state. Backward launches another finite solve; it must not be called an exact inverse gradient merely from the solver name. Straight covariance, ridge, Chebyshev, variable iteration count, or sketching alone is not a new candidate.

## KDN: mandatory September nearest work

Primary: [2609.07816v2 PDF](https://arxiv.org/pdf/2609.07816v2), 29 September 2026, 26 pages; inspected §§3–4, Eq5–21 and Appendix D overwrite argument. Dense formal filtering propagates P_hat=D P Dᵀ+Ω, κ=P_hat k/(r+kᵀP_hat k), S=S_hat+κ(v−S_hatᵀk)ᵀ. Diagonal reverse-KL projection preserves exact one-step posterior mean only conditional on the retained diagonal prior. Its posterior precision update and μ-scaled post-write information increment already calibrate future overwrite; μ>1 is not the exact mean-field posterior of the same measurement. The diagonal covariance recurrence admits a Möbius scan, followed by input-only asymmetric Delta/WY memory scan. Treat repeated-observation confidence, noise-dependent gains and diagonal uncertainty as covered neighbors, not project originality.

Version correction receipt: the initial unversioned fetch was mistakenly labelled v1 in this draft. Root's independent header check prompted re-opening the first page: it explicitly reads arXiv2609.07816v2, 29 September2026. The explicit v2 URL was then opened and returned the same26-page/1914-line document and equations. No v1 comparison was performed; the inspected formula conclusions above bind v2.

Pinned author commit: [53e437be8591521a508bb6a04cd5b26594a3d5ec](https://github.com/ngocbh/kalman-delta-networks/tree/53e437be8591521a508bb6a04cd5b26594a3d5ec). `lit_gpt/kdn_ops/diag_kdn_naive.py`, functions `diag_kdn_gain_naive`, `naive_recurrent_diag_kdn`, and private chunk oracle: computes gain from predictive covariance before scaled precision increment, then memory innovation; returns output and `(memory,precision)`. `initial_precision`, `info_scale`, `output_final_state` are explicit inputs. The reference/source mapping is inspected; no software receipt is claimed.

## EDA: independently addressed erasure already exists

Primary: [2606.26560v1](https://arxiv.org/html/2606.26560v1), 25 June 2026; inspected §3.3–3.5, Eq8–18. EDA applies (I−βkkᵀ)(I−γeeᵀ)D before the write, with learned independent erase address e. It contracts the pre-write response at e toward zero and then performs Delta correction at k. The exact implementation reduction doubles substeps: erase at e with zero value and decay, then write at k with identity decay. Its bounded log-decay gate and update-order cross term are explicit. Independent stale-address cleanup and simple two-step Delta are therefore covered. Author kernel locator is [QwenLM/FlashQLA](https://github.com/QwenLM/FlashQLA); actual pinned source inspection remains open in this audit. Readiness of that source is not inferred from the paper's release promise.

## Byte identities of read author files

Fetched exact Git blobs; standard-library UTF-8 SHA256 and Git blob SHA1 were computed without executing source. All seven fetched bytes matched their listed Git blob IDs. These hashes pin what was inspected, not mathematical truth.

| Repo and relative path | Git blob SHA1 | SHA256 |
|---|---|---|
| PDN `3rdparty/flash-linear-attention/fla/ops/precond_gated_delta_rule/naive.py` | 4a2273f25a89b509332e8755391e78cc594a16b0 | 266c86596ba23dff12b367afaa15620cb4d1c7b751f8a9f0122cc6d99517e870 |
| PDN same directory `fused_recurrent.py` | 379833023039110fce79568984faf1b4b5d77bc9 | 1bdf503a1f533c93bcad4d31ee954e6fbfbfe04e3d822b2f23437df4fe56b92f |
| GDN2 `lit_gpt/gdn2.py` | 4a0199c69b2097d2637bb8714d707bd53e67e91d | 5d93765adcb4e9bf755e7d4160a01d4e2ee8438ec55759d17903223dd18b0324 |
| GDN2 `lit_gpt/gdn2_ops/fused_recurrent_gdn2.py` | b994d407c6f0bae69c939426cd72dd7196eb0d28 | aee06a5fe471a194680a5762cbb733118d0e52ad816732a4e1742cb7485a2db1 |
| GKA above directory `gka_chebyshev_solve.py` | 590fb707328e269b473b5e93af02b3351bdf4ebb | d93180d1801759c5a31a96a0c8e064ad6759104a497a3a1d0a7331b5f417dd86 |
| GKA above directory `chebyshev_iteration.py` | 743f71c5ffd79cec7f8bd4cd69c172f2bcc287ec | f0b37685a3e8f6b5a66e07ab2ed041300dc621ca35adc29d5c438876e322278f |
| KDN `lit_gpt/kdn_ops/diag_kdn_naive.py` | 0e1d77dac63a350c659825cfa393969b4e51c958 | 87876ebe27fb175685548b7d8d59ad83e5c3e04164be78b4366f2a7ea226327d |

## FlashQLA source availability and hardware scope

The EDA paper's author kernel locator was then inspected at exact commit [da06429d54b0f577de0a638f451ac8f0b395e0ac](https://github.com/QwenLM/FlashQLA/tree/da06429d54b0f577de0a638f451ac8f0b395e0ac). Its recursive tree and README expose GDN `chunk_gated_delta_rule(q,k,v,g,beta,...initial_state)` and Hopper/Blackwell kernels. The inspected tree contains no EDA/erase-named interface; README is a GDN kernel library, so this audit cannot claim a released EDA implementation from that locator. This is a bounded inspected-tree finding, not a global absence claim. README requirements are SM90/100/103/120/121 and CUDA12.8+/PyTorch2.8+, which do not cover the user's RTX2080Ti (Turing). Kernel wall-clock claims on newer hardware cannot establish the project's cost/feasibility. No installation or run was attempted.

FlashQLA README exact Git blob01942dda618270e2f77dd03aaf499f890b235e0c, SHA2561993a45a8cdae8bb9c637ac617f7365c66991d4157bbaaff9d9c6cbbbc03b3e7; UTF-8 bytes matched the Git blob identity using standard-library hashing.

Remaining scope: QED author-code interface and actual EDA adapter/kernel source; source reading for other requested nearest works belongs to the separate nearest-work packet. No full pool distinctness/ranking selection is established here.
