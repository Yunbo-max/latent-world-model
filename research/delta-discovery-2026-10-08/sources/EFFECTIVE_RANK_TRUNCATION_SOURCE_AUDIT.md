# Delta 有效秩与随机截断：primary-source、作者接口和原生测量审计

状态：2026-10-09 UTC bounded audit。只读论文、作者链接、固定作者仓库与既有 benchmark 文档；未执行项目/上游代码、测试、训练、推理、评分、数据/模型下载、GPU 或 Docker。本文支持 `STEP2_EFFECTIVE_RANK_TRUNCATION_CONTROL.md` 的最近工作与测量结论，不证明原创性。

## 1. 收缩与确定性截断已被直接覆盖

### Adaptive TBPTT

[Aicher, Foti & Fox, arXiv:1905.07473v2 / UAI 2020, PMLR 124](https://arxiv.org/abs/1905.07473) 在 §3.1--3.3 定义 `phi_k=||partial L_s/partial h_(s-k)||`。Assumption A-1 要求从某个 `tau` 起 `E phi_(k+1)<=beta E phi_k`，`beta in (0,1)`；A-2 有界 `||partial H/partial theta||<=M`。Theorem 1 对 `K>=tau` 给出 TBPTT absolute bias 上界

`M E[phi_tau] beta^(K-tau)/(1-beta)`，

并给相应相对界。算法周期性用较长窗口估 decay，再用 `BPTT(2K,K)`；假设或预算不满足时退回 `K_max`，不是逐轨迹全局证书。

作者仓库固定为 [`aicherc/adaptive_tbptt@1bab8664ff8bc1fc892b6e5cdbb40a7d015d8421`](https://github.com/aicherc/adaptive_tbptt/tree/1bab8664ff8bc1fc892b6e5cdbb40a7d015d8421)：

- `tbptt/adaptive_truncation.py` blob `4261a05f56441af659bba7074dedc12bd2f4637e`：`calculate_gradient_norms`、`estimate_logbeta_max/quantile/ols`、`log_abs_error_estimate`、`log_rel_error_estimate`、`adaptive_K_estimate`；
- `tbptt/tbptt.py` blob `61ff38e38e3b6db6d601f84d6d343dfc07ebc6c7`：`TBPTT_minibatch_helper.train(...,K)` 与 `train_one_batch`，含 buffer/double-window 路径。

所以“估计几何 decay/effective horizon 并选择 K 控制 truncation bias”是直接先例。Delta 路线若不能给出更弱且可核的完整 ordered-product 条件，或同预算更强保证，只是改名。

### Stable Recurrent Models 与 fixed-point RBP

[Miller & Hardt, arXiv:1805.10369v4 / ICLR 2019](https://arxiv.org/abs/1805.10369) 在全局 lambda-contractive transition 及 Lipschitz/smooth 条件下，给 inference truncation 对 `1/epsilon` 的对数长度和 gradient truncation 的 `O(k lambda^k)` 差异，随后训练轨迹结论还需要投影 SGD/学习率等假设。它证明 fading-memory 控制，不证明固定 algebraic rank 或长期信息保留。本轮 bounded search 未定位可确认的作者官方代码，故不虚构 pin。

[Liao et al., arXiv:1803.06396v4 / ICML 2018](https://arxiv.org/abs/1803.06396) 的 Neumann-RBP 在收敛 fixed point 和 Neumann convergence（例如充分条件 `||J||<1`）下用 `sum_(t=0)^K J^t`，尾部由 `||(I-J)^(-1)|| ||J||^(K+1)` 控制；当最后 K 个 state 都在 fixed point 时等价于 K-step TBPTT。作者仓库 [`lrjconan/RBP@9c6e68d1a7e61b1f4c06414fae04aeb43c8527cb`](https://github.com/lrjconan/RBP/tree/9c6e68d1a7e61b1f4c06414fae04aeb43c8527cb) 的 `model/rbp.py` blob `dab4b9451b1b5c0dcf5f898a6699236e0f92b9c0` 在 `RBP(...,truncate_iter,rbp_method)` 中实现 repeated-VJP `Neumann_RBP`，并列 `CG_RBP/RBP`。这是 fixed-point 结果，不是 transient free-running Delta 定理，但排除普通 Neumann 截断的新颖性。

## 2. 无偏随机 horizon 已被直接覆盖

### ARTBP

[Tallec & Ollivier, arXiv:1705.08209v1](https://arxiv.org/abs/1705.08209) §3 Proposition 1 / §4 使用随机截断指示与 conditional cut probability `c_t`。非截断时在反向递推乘 `1/(1-c_t)`，得到无偏 gradient。固定 cut rate 控制平均 segment 长度，但 inverse-survival 乘积会放大方差；几何 dynamics 下 cut schedule 仍须满足相应 decay 条件。

本轮未定位独立的作者 ARTBP 仓库；`ctallec/uoro` 是 UORO 实现，不能冒充 ARTBP 代码。结论是：inverse-survival randomized TBPTT 的无偏性已知，无偏本身不能支持新 Delta 候选。

### Randomized Telescopes

[Beatson & Adams, arXiv:1905.07006v1 / ICML 2019](https://arxiv.org/abs/1905.07006) §2.1 Proposition 2.1、§4--5 把 `Y_H=Y_0+sum Delta_n` 随机截断，并在权重条件下保持无偏。其优化分析另假设 uniformly convergent gradient approximants `G_n=nabla L_n`、增量 `Delta_n=G_n-G_(n-1)` 满足 `||Delta_n||_2<=psi_n`、归一化线性成本 `C(n)=n`，并在 convex compact domain 上讨论 regret。论文明确把 ARTBP 视为 fixed Russian-roulette 例；在这些条件下，几何 `psi_n<=c p^n` 配 `q(n) proportional p^n` 可给 horizon-independent expected work/second moment，仍是 cost--variance 权衡。当前 Delta ordered-gradient sequence 尚未证明满足这些前提。

作者仓库固定为 [`PrincetonLIPS/randomized_telescopes@506541538c0c00adeb5791d85dec8c81da285639`](https://github.com/PrincetonLIPS/randomized_telescopes/tree/506541538c0c00adeb5791d85dec8c81da285639)：

- `randomized_telescope.py` blob `d86481442bf366cb6e23c74024013847879d711d`：`GeometricRandomizedTelescope`、`PolynomialRandomizedTelescope`，以及二者继承的 `RandomizedTelescopeTemplate.sample_vms`；
- `adaptive_randomized_telescope.py` blob `9ca84163a5d2b7ae631790f20bb7c7cafdd6219e`：No/Fixed/Collapsed/Adaptive telescope 类。

固定代码还含未闭接口：`AdaptiveRandomizedTelescope.__init__` 使用未定义 `T`，`finalize` 检查未设置的 `smooth_std`；仓库 README 也提示代码需整理。因此这里只把论文公式和实际接口作为来源证据，不宣称 production-ready。若 Delta 要前进，必须定义真实 ordered closed-loop gradient approximation sequence，并给出新的结构性 variance/cost 结果。

[Rhee & Glynn, “A New Approach to Unbiased Estimation for SDE's,” arXiv:1207.2452v1 / WSC 2012](https://arxiv.org/abs/1207.2452) 与 [“Unbiased Estimation with Square Root Convergence for SDE Models,” *Operations Research* 63(5), 2015, DOI 10.1287/opre.2015.1404](https://doi.org/10.1287/opre.2015.1404) 是两个不同出版物，共同构成从 biased hierarchy 得无偏有限方差 estimator 的一般谱系；对当前 recurrent truncation，ARTBP 与 Randomized Telescopes 是更直接碰撞。

## 3. Streaming low-rank 是强基线，但不是直接闭环解

[Tropp et al., arXiv:1902.08651v1, §2.3--2.7、§5、§6](https://arxiv.org/abs/1902.08651) 对 scalar-linear stream `A <- eta A + nu H` 维护 range/co-range/core random sketches，并重建 near-best rank-r approximation及独立 Frobenius error estimator。作者 MATLAB 仓库 [`alpyurtsever/SKETCH@b578c6ba5e22f8080eb9ded18adaa7b706ca7860`](https://github.com/alpyurtsever/SKETCH/tree/b578c6ba5e22f8080eb9ded18adaa7b706ca7860) 中：

- `@ThreeSketch/LinearUpdate.m` blob `5318c61c70e7e5e6b36dd68b4cf445606d85109c` 处理 full/factored H；
- `@ThreeSketch/LowRankApprox.m` blob `9da1178fadf3c1a1d2681f0f946e4d77a79604af`；
- `@ThreeSketch/FixedRankApprox.m` blob `56355bc854af000f31f9d60d71e6d24e8c23465b`；
- `@ThreeSketch/ErrorEstimate.m` blob `5d10fc084883037f14bdc6ab8ff8dc0e35372603`。

[Frequent Directions, arXiv:1501.01711v2](https://arxiv.org/abs/1501.01711) 给 row-stream covariance/projection error 控制；作者仓库 [`edoliberty/frequent-directions@691df9edb2ffbc2fdddc2cec3b703a3f1e438d4d`](https://github.com/edoliberty/frequent-directions/tree/691df9edb2ffbc2fdddc2cec3b703a3f1e438d4d) 的 `frequentDirections.py` blob `4bb3500cbea9c81c21cbeea5cd5db60ac4006d3d` 含 `FrequentDirections.append` 与 SVD shrink。

这些方法不直接闭合 `X_(j+1)=L_jX_j+U_j<G_j,X_j>`：例如 range sketch `X Omega^T` 可左传，但 co-range/core sketch 通常不能在任意、非交换 `L_j` 下只凭现存 sketch 更新，除非证明额外 closure。Frobenius/covariance error 也不自动等于 downstream costate/action error。因此它们是必比 baseline，而不是可直接贴到 Delta 的解。

## 4. Online recurrent sensitivity 的既有近邻

项目既有 `CLOSED_LOOP_RANK_GROWTH_SOURCE_AUDIT.md` 已按固定论文/作者接口审查：RTRL exact sensitivity、NoBackTrack/UORO 随机 rank-one、KF-RTRL/OK Kronecker、SnAp sparse influence 与 e-prop eligibility factorization。这里复用该证据，不换名重复计数。

结合本轮来源，四类主张都已发生主要碰撞：

1. contractivity/geometric tail + deterministic adaptive K；
2. inverse-survival/random-horizon unbiasedness；
3. generic streaming/SVD low-rank approximation；
4. recurrent sensitivity 的 rank/Kronecker/sparse/eligibility 压缩。

尚未关闭的窄问题不是“effective rank 是否可能小”，而是：对非交换完整 Delta 递推，能否在线维护合法压缩器/证书，直接控制 `|<Lambda_T,X_T-Xhat_T>|` 或 action-gradient MSE，并在相同 causal information、state bytes、JVP/VJP、replay 与总 FLOPs 下优于上述方法及 direct action prediction。

## 5. 原生测量可行性

下表复用项目已经固定版本、数据格式和 native scorer 的 [`BASELINE_NATIVE.md`](BASELINE_NATIVE.md)、[`MEASUREMENT_FEASIBILITY_2026-10-09.md`](MEASUREMENT_FEASIBILITY_2026-10-09.md) 与 [`PROJECTED_DELAYED_CREDIT_SOURCE_AUDIT.md`](PROJECTED_DELAYED_CREDIT_SOURCE_AUDIT.md)。本文不把摘要式映射冒充对每个资产的新一轮全量审计。

| 资产 | 原生可测 | 不能认证 |
|---|---|---|
| bAbI 20 tasks / 20,000 aggregate test denominator（20×1,000） | 短程多事实推理与任务级 accuracy | 闭环 tangent、ordered products、有效秩或 updater credit |
| LAMBADA-openai / 5,153 | 非局部文本预测 endpoint | 距离、检索、语言与记忆机制解耦 |
| BABILong | task × context-length 的分布式事实推理退化 | 长度同时加 distractor；不能把退化归因于 tangent rank |
| RULER | NIAH、variable tracking、aggregation 与 null accounting | scorer 不观察内部传播；检索改善可解释 endpoint |
| LongMemEval v1/v2 | knowledge-update/temporal QA、evidence retrieval、accuracy--latency frontier | ideal edit、内部删除、训练信用、奇异谱；证据标签不得泄漏给部署 updater |
| CITB / TRACE | 顺序任务 retention/transfer、BWT 等参数级 endpoint | fast-state Delta；FWT 也不是后续任务的 sample/compute learning speed |
| SEAL continual | 每轮 self-edit 后对已见问题重评，最接近连续编辑遗忘 endpoint | updater 自改证据、知识有效性 oracle、tangent rank |
| StreamingQA | 时间知识更新的 EM/F1 | 历史时间不等于逐事实有效性，也不测内部递推 |

机制主张必须依赖以后合法 instrumentation：small-state/full-horizon exact BPTT 或 RTRL reference、预注册 singular-tail 定义、每步 truncation residual、ordered-product gain、frozen/full gradient gap，以及绑定同一原生样本的 truncation intervention。只有相关性不能证明高有效秩导致 endpoint loss。

资源边界沿既有审计保留：LongMemEval 的参考原生 judge/大型 reader、TRACE 的 7B/13B 报告设置、SEAL 的默认 7B/双 GPU/付费 grader 与当前单卡 RTX 2080 Ti / no-paid 条件不匹配；这不是“任何缩小配置都绝不可能运行”的结论。RULER/BABILong 长长度 sweep 和所有缩小配置都仍待 Local 可行性验收。本轮没有下载或运行它们。

## 6. 来源决定

处置为 **useful Delta-specific counterexample/control / major component collision / native mechanism measurement gap / no D ID**。本轮没有发现 matched-budget 的 Delta estimator 优势。计数保持 5 历史 / 0 活动 / 0 科学准入 / 0 选择。
