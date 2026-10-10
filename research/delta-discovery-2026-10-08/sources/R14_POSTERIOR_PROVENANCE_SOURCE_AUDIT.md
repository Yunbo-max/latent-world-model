# R14 posterior-provenance source, code-interface and novelty audit

Audit date: 2026-10-10. Scope: primary papers, author repositories and already pinned project records. No code, model, benchmark, training, inference or scorer was executed.

## Decision

R14's conditional derivation is supported, but the architecture/mechanism is strongly covered. Multiple routed slots, posterior/responsibility-weighted local fitting, tensor role binding, sparse address selection and protected ridge updates are established families. The retainable result is narrower: latent-identity Bayes risk and a common-residual soft tensor write generally induce different actions, with an exact equality condition and ambiguity price. This is a theorem/diagnostic, not a new routed-memory architecture.

## Fixed primary sources and interfaces

| Source | Version / section / author interface actually inspected | Functional coverage and residual |
|---|---|---|
| Jordan & Jacobs, *Hierarchical Mixtures of Experts and the EM Algorithm* | [MIT AI Memo AIM-1440](https://bitsavers.trailing-edge.com/pdf/mit/ai/aim/AIM-1440.pdf), “Applying EM to HME,” Eqs. 18–29 and Algorithm 1; online algorithm from Eq. 32 | latent expert indicator, posterior responsibilities, posterior-weighted least squares and online RLS. Adding separable ridge gives R14's shrinkage family. It does not state R14's Delta tensor/common-residual non-equivalence. |
| Smolensky, *Tensor Product Variable Binding and the Representation of Symbolic Structures* | [1990 primary PDF](https://www.lscp.net/persons/dupoux/teaching/AT1_2014/papers/Smolensky_1990_TensorProductVariableBinding.AI.pdf) | role/filler tensor binding. One-hot identity is a coordinate rewrite of explicit blocks/slots; probabilistic identity does not itself select the Bayes action. |
| Schlag, Munkhdalai & Schmidhuber, *Learning Associative Inference Using Fast Weight Memory* | [arXiv:2011.07831v2](https://arxiv.org/abs/2011.07831v2); official code `ischlag/Fast-Weight-Memory-public@64c077f02ec320ec535cb66db3600453e1ef445f`, `catbAbI/models/lm_fwm.py::TPRRNNCell` and `language-modelling/fwm/myfastweights_v2.py::FWM.write/forward` | the actual code constructs a two-address tensor `s⊗r`, reads its current value and adds a residual outer product. This directly covers tensor-bound residual fast memory, not calibrated provenance. |
| Schlag, Irie & Schmidhuber, *Linear Transformers Are Secretly Fast Weight Programmers* | [PMLR 139](https://proceedings.mlr.press/v139/schlag21a.html); author code `ischlag/fast-weight-transformers@ebe13ea2e6409da91d12d22175f4f6efe8bf2f0a` | outer-product and Delta fast-weight primitives; choosing `phi(k,c)=k⊗c` is a feature/address choice. |
| Lample et al., *Large Memory Layers with Product Keys* | [NeurIPS 2019 paper](https://papers.neurips.cc/paper_files/paper/2019/file/9d8df73a3cfbf3c5b47bc9b50f214aff-Paper.pdf); official `facebookresearch/XLM@cd281d32612d145c6742b4d3f048f80df8669c30`, `xlm/model/memory/memory.py::HashingMemory`, plus `PKM-layer.ipynb` | product-key top-k and softmax-weighted sparse slot access. Original PKM is not online context-state revision, but it is the strong indexed retrieval control. |
| Zhao & Jones, *Fast-weight Product Key Memory* | [arXiv:2601.00671v2](https://arxiv.org/abs/2601.00671v2), §§2–3; author code `SakanaAI/fast-weight-product-key-memory@b1c8e234b523d70245fa197eed4b80a985c413a8`, `src/models/fwpkm/fwpkm.py` | sparse routed slots, softmax routes, local MSE and test-time fast-weight updates. Learned address weights are not necessarily calibrated provenance posteriors, and the paper does not provide R14's separate-residual theorem. |
| Cabannes et al., *Sparse Delta Memory* | [arXiv:2607.07386v1](https://arxiv.org/abs/2607.07386v1), §3.1 Eqs. 3–5 and Appendix A; official `facebookresearch/sparse-delta-memory@183e7df809131b80ad4393741029d0f20fc3640b`, `lingua/sparse_delta_memory/layer.py::SparseDeltaMemory` and `memory_ops.py::GatedSparseMemoryWriteRead` | explicit large sparse table, top-W write/top-R read, product-key addressing and gated residual write. The project's earlier row-local-versus-aggregate formula discrepancy remains; no unsupported dense-limit claim is borrowed. |
| Zeng et al., *ARM: Attention with Routed-Memory for Learnable Sparse Control* | [arXiv:2609.24417v1](https://arxiv.org/abs/2609.24417v1), §§3.1–3.2, Eqs. 3–7 | fixed routed slots, Gumbel-softmax selection and sigmoid-gated blending. No author repository was located in this bounded audit, so no implementation claim is made. |
| Hartvigsen et al., *GRACE* | [NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/file/95b6e2ff961580e03c0a662a63a71812-Paper-Conference.pdf); author code `Thartvigsen/GRACE@f674183f17a995d109e10ee6140d4c3e6d016115`, `grace/editors/grace_barebones.py::GRACEAdaptor.forward` | creates/routs edit slots using nearest keys, radius and observed label conflict. This is a hard routed edit-memory control, not an uncertain causal identity posterior. |
| Wang et al., *WISE* | [arXiv:2405.14768](https://arxiv.org/abs/2405.14768); EasyEdit code `zjunlp/EasyEdit@4c109870955a4522ac3d7cf10ad00f34de8e4f0d`, `easyeditor/models/wise/WISE.py::WISEAdapter.forward` | main/side memories, activation-distance routing and edit shards/merge. It is parameter editing with heuristic routing, not R14's Bayes-risk minimizer. |

MEMoE, LEMoE and MELO further populate the identity-routed edit/expert neighborhood; they are corroborating neighbors, not needed to establish the main collision.

## Exact collision and narrow residual

Classical HME supplies latent identity, posterior responsibility and weighted least-squares/RLS. R09 supplies protected quadratic/inverse-metric geometry. Direct per-slot soft routing therefore implements R14's normal equation without a tensor representation.

The tensor/common-residual mismatch is nevertheless real. For `y_i=S_i^Tk`, posterior `pi`, and `ybar=sum pi_i y_i`,

\[
\sum_i\pi_i\lVert v-y_i\rVert^2
=\left\lVert v-\sum_i\pi_i y_i\right\rVert^2
+\sum_i\pi_i\lVert y_i-\bar y\rVert^2.
\]

A soft tensor write driven only by `v-ybar` targets the first term, whereas latent-identity risk contains the dispersion term and slot-specific residuals. R14's Eq. (5a) states the exact restricted equality condition. This decomposition/counterexample and the scoped ambiguity price are the only retained theory delta.

## Posterior semantics and information budget

R14 defines `F_t` to include current causal `k,v`, slot state and declared protection summary. That makes `pi=P(J|F_t)` a legal decision-time posterior, but `v` is not a ground-truth identity label. A genuine posterior still requires a prior and likelihood or a calibration guarantee; otherwise `pi` is only a learned gate score. HME responsibilities use observed targets under an explicit expert likelihood. Future task answers, old-knowledge validity or ideal edit labels would be extra information and must be given equally to controls.

If two identities induce the same law over every causally visible variable, no router can identify them. Reliable identifiers make the posterior one-hot and reduce the method to ordinary deterministic slots. An explicit new-identity hypothesis is required; renormalizing over existing slots is not a solution.

## Native measurement and implementation boundary

Existing bAbI, LAMBADA, RULER and LongMemEval endpoints do not jointly expose per-write latent identity, calibrated posterior, world-conditional signed protection consequences and paired actions. LongMemEval includes timestamped knowledge-update questions but does not natively score R14's internal posterior or Bayes risk. Model-edit benchmarks prescribe edits and measure efficacy/locality; they do not supply the same internal objects. No new benchmark, label, metric or result is introduced.

No software execution is authorized here. Source/code inspection establishes interface overlap only; it does not show empirical equivalence or success.

## Novelty ruling

- mathematical correctness: conditional pass, subject to exact-byte review;
- mechanism novelty: not established, strong HME/routed-memory/protected-ridge collision;
- architecture candidate: not admitted;
- theory value: retain the latent-risk versus common-residual theorem, equality condition and ambiguity floor;
- experimental effect: unknown.

Reopen only with a Delta-specific causal statistic or regret/interference theorem that beats direct per-slot posterior routing under equal information, slot state, writes, FLOPs and precision. Do not claim the first Bayesian routed Delta memory, a novel posterior-weighted slot update, or a new tensor provenance representation.
