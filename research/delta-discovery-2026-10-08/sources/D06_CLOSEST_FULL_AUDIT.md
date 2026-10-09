# D06 最近工作审计：残余保留，原创性未闭

结论：residual_survives; originality_collision_inconclusive。D06 暂保留为活动的条件性数学候选，但不标记 original、verified、scientifically admitted 或 selected。

## 数学复核

对单位 key、普通 symmetric Delta erase 与正的 contractive diagonal decay，

\[
A_t=(I-\beta_tk_tk_t^\top)D_t,
\quad
c_t=-\log\det A_t=-\log(1-\beta_t)-\sum_i\log d_{t,i}.
\]

若窗口内每个因子都是 contraction，则所有奇异值不超过 1，故对实际有序乘积 \(P\)：

\[
\sigma_{\min}(P)\ge |\det P|
=\exp\!\left(-\sum_t c_t\right)\ge e^{-B}.
\]

投影 \(d_i=\tilde d_i^\alpha,\ \beta=1-(1-\tilde\beta)^\alpha\) 把候选成本精确缩为 \(\alpha\tilde c\)。只要可用额度从前 \(W-1\) 个已实现成本计算，滑窗约束成立。

## 最近工作

| 工作 | 固定公式/接口 | 覆盖与残余 |
|---|---|---|
| scoRNN, ICML 2018 | Theorem 3.1 的 Cayley 参数化；作者仓库 SpartinStuff/scoRNN commit d390c9bac62c510963ff90d386fb02beccff0a1e, scoRNN.py::scoRNNCell.__call__ | 覆盖固定正交、零体积损失；不覆盖输入相关 Delta 修订或滑窗额度。 |
| Soft Orthogonality, ICML 2017 | Eq. 9 Stiefel/Cayley 更新，Eq. 10 奇异值带 \([1-m,1+m]\) | 覆盖逐矩阵谱约束，不覆盖累计 log-volume 分配。 |
| Dynamical Isometry, ICML 2018 | MinimalRNN Eq. 5，状态 Jacobian Eq. 10 | 控制初始化时端到端 Jacobian 谱；未发现运行时滑窗 gate projection。 |
| Stable Recurrent Models, arXiv:1805.10369v4 | 以 \(L_\rho\|W\|<1\) 保证 contraction | 是导致旧输入指数遗忘的反面对照，不是下奇异值保留预算。 |
| pLSTM, arXiv:2105.05944；Chrono Initialization, arXiv:1804.11188 | 预定慢遗忘/时间尺度 gate | 概念很近，但无 Delta erase 成本、滑窗硬约束或 \(\sigma_{\min}\) 保证。 |
| UnICORNN, arXiv:2103.05487v2 | symplectic Euler 与相空间体积保持；作者仓库 tk-rusch/unicornn | 覆盖长记忆的体积保持路线；不覆盖部分体积支出或滑窗预算。当前未固定可靠 commit SHA。 |
| Gated DeltaNet, arXiv:2412.06464v3 | \(S'=(I-\beta kk^\top)\alpha S+\beta kv^\top\)；官方 commit b53d6d3a161267432a79c1c04af69fa52bddc921，lit_gpt/gated_delta_net.py::GatedDeltaNet.forward/init_state 与 gated_delta_rule_ops/chunk.py | 直接覆盖 token gate 与标量衰减，但没有累计 log-det 限额。 |

KDA、RWKV-7、DeltaProduct、PDN、GDN2、GKA 与 QED 分别覆盖更丰富 decay/write/erase、微步、预条件或 query solve；当前审计未发现它们采用 D06 的滑窗累计 \(-\log\det\) 以及对应生存下界。限定检索未发现精确同构的主要 RNN 方法，只能记为有界阴性结果，不能作原创证明。

## 条件与风险

- 下界只适用于冻结特征仿射路径的欧氏扰动，不是语义记忆或完整非线性 Jacobian 证书。
- \(\beta=1\) 的完整替换花费无穷，因此被构造禁止。
- 成本随维数累积；统一衰减 \(r\) 单步即花 \(n(-\log r)\)，预算可能极度保守。
- 证明依赖每因子 contraction，不能直接移植到斜投影或可能 nonnormal 的 QED/GDN2 更新。
- 滑窗额度引入顺序依赖；尚无与现有 WY/chunk recurrence 等价的并行训练 scan。
- 有限精度仍可抹除小分量；determinant 生存不识别语义重要方向。

最强简单替代必须包括：相同实际总成本的固定 gate cap、GDN/KDA、chrono/pLSTM 慢衰减、相同平均成本的 soft log-cost penalty，以及正交/体积保持转移。下一轮科学准入前仍需在线约束控制、Jacobian 下界正则与资源分配的一手文献审查。

本审计只进行了静态数学/来源阅读；未执行代码、测试、训练、推理、评分、数据下载或 GPU 工作。
