# Delta 数学发现：可逆、反事实效用与度量稳定三条路线的严格处置

这是数学阶段的部分里程碑，不是 20→15 完成。构造历史现有 **5 张卡**；D01、D03、D05、D06、D07 已全部因重大功能或组合碰撞移出活动池。D07 的条件代数仍成立，但完整公式与作者代码审计只留下一个窄的 direct-hinge 实现差异，不能据此科学准入。当前**活动候选 0、科学准入 0、选择 0**，距目标仍差 20 个活动候选/15 个选择。没有项目代码、测试、训练、推理、原生评分、数据/模型下载、GPU 或实验运行。

| 条目 | 解决什么 | 数学上真正留下什么 | 与已有工作的差别 | 最可能失败处 | 当前处置 |
|---|---|---|---|---|---|
| D01 | 延后判断旧写入应保护还是释放 | 共享未来仿射路径时，一个事件的双状态差保持 rank-one；后验重权可精确压缩 | Wilson mixture、PF-RNN 已有后验多假设；压缩后与显式双状态预测完全相同 | 多事件分支爆炸；state-dependent features 破坏共享路径；无语义身份证据 | inactive equivalence control |
| D03 | 当前写入如何少扰动未来 query | `G=ΣωPᵀqqᵀP=JᵀJ`，并用归一化 inverse metric 写入 | 这是 observability/Gauss–Newton + APO/natural gradient + PDN/Q-Delta 的直接组合 | frozen path 不等于真实部署；密集 solve 昂贵；低扰动可等于快速遗忘 | inactive control |
| D05 | 有限精度状态应如何分配 bit | 条件性白化/water-filling 局部构造 | balanced realization、STEPQuant/DAMP 已实质覆盖 | 指标漂移、重复量化和内核成本；无新功能 | inactive history |
| D06 | 防止连续 erase/decay 把方向压扁 | 滑窗 `-logdet` 预算给条件性 `σ_min` 下界 | HGRN/谱-Jacobian 控制已有 retention floor；COLD/token bucket 已有窗口预算 | greedy clip 会产生 `[B,0,…]` 饥饿，无 utility/regret 最优性，不识别语义方向 | inactive guardrail |
| D07/WTSR | 不改推理结构，训练时直接保护实际写入方向 | frozen path 上 `||P W_i||²/||W_i||²=||Pk_i||²`；加入有限时域 survival hinge，推理零增量 | 一般 source contribution/realized survival 已知；同-key 时精确退化为 Tabular ICL Eq.10；write-rate decay 与 Delayed Supervision 覆盖主要功能；只余 arbitrary-key direct hinge | 只保 state norm，不保 query 可见性/语义；会保存过时事实；scale-blind；无 native 机制 scorer；未证明优于 CE/Delayed QA/write decay | inactive diagnostic, major functional collision |

## 本轮新增的否定边界

`NOGO-CAP-02` 证明：对所有旧状态与新值都精确覆盖当前 key 的仿射写入，必须满足 `Aᵀk=0`，所以旧状态路径必奇异；在显式有限精度下，若旧行为类与新值都需恢复，还必须支付联合编码容量。它不覆盖非线性/状态依赖更新、额外 side state、近似覆盖或预测商意义的恢复。

`DEFERRED-CORRECTION-DEBT` 证明共享 frozen affine 路径上 `main+debt=ideal` 的守恒，但 future-key 偿还就是 transported error feedback。精确追平取决于安全 transported-key 可达子空间；无事件身份不能决定 debt 应偿还还是取消，有身份又变成 replay/event memory。故它是控制，不是 D07。

新读的 DeltaTTT 已明确覆盖两层 state-dependent Delta、local squared targets、pre/post hidden target 与精确 chunkwise nonlinear recurrence。因此“堆多层 Delta + local reconstruction loss”直接归 baseline，不生成候选。

## D07 的合法范围

D07 保留普通 Delta/GDN 前向更新。训练期对观测序列采样 source `i` 和 horizon `h`，传播 `z_i=k_i, z_j=A_jz_{j-1}` 并正则 `s=||z_{i+h}||²`。后缀只作训练监督，推理不读未来 token/答案、不加状态或算子。

它同时给出一个明确冲突：若后续 key 与旧 source direction 的重合为 `c`，当前 residual 必须压到 `ε`，则普通 Delta 可保留的 source survival 最多是 `1-(1-ε²)c²`。所以这个 loss 只能是软代理，不能声称“完整纠错又完整保留”。独立审查已核对维度、梯度、gate domain、zero/tiny-write 约定、复杂度与 frozen/moving path 区分。

新审计固定了 Tabular ICL 的作者代码 `0be576b8481e153ce7489aba6ad64e278c133c09`，并确认其 `_apply_deltanet_beta_decay` 在训练与推理中实现 `beta*t0/(t0+position)`。在单位同-key、无额外 decay 的特例，`sqrt(s)=prod(1-beta)=C_i/beta_i`，与论文 Eq.10 精确对应。How Linear Attention Remembers 又给出一般 source contribution，RPMem 明确给出 realized-path source survival。因此“未发现完整 hinge 逐项复现”只是一项窄检索残余，不是原创性结论。

## 本轮新增的两个否定控制

`NOGO-OBLIQUE-03` 给出 `A=I-ka^T` 的精确二维奇异值。只要 `a` 含任一垂直于 `k` 的分量，裸因子必有 `||A||₂>1`；欧氏非扩张只能发生在 `a=ck,c∈[0,2]`。这不能外推到 `AD` 或 `DA`，因为独立 decay 可能抵消扩张，而且实际顺序不可交换。

`REVISION-EVIDENCE-POSTERIOR-EDIT` 说明额外已观测证据确可解除 residual-only TV no-go，但随后得到的是普通二假设 Bayes gate 加已知 protected/ridge/slot edit。无新增证据仍不可辨；完美 ID 退化 routing；future teacher 属于额外监督。独立复核纠正了 unequal-prior Bayes error、ridge 端点、平行地址可行性以及 BOCPD/mixture 的严格范围。两项都不计候选。

## 本轮继续闭合的三条路线

1. **Unitary Delta dilation**：一步 Halmos 扩张可以把被擦除分量搬进一个辅助槽，但第二次复用该槽就会让旧内容流回；严格 Delta contraction 的全时域 exact unitary dilation 需要无限维。有限时域版本每步用新槽，状态随 horizon 线性增长，实质是显式事件记忆。
2. **Counterfactual query-visible write utility**：固定路径下可以精确测一个 write 对未来 query/CE 的 signed contribution，解决了 D07 只看 state norm 的诊断缺陷。但对只控制该 write 的参数，最大化 utility 的梯度精确等于普通 future CE；AttriMem/HiMPO 等又已用 source ablation/signed memory credit。它能事后诊断 revision，不能从混合状态中选择性删除来源。
3. **SPD metric oblique Delta**：`A=I-wrᵀ` 在某 SPD metric 中非扩张当且仅当 `0<rᵀw≤2`。固定 metric 时，它精确等价于白化坐标中的 normalized/preconditioned Delta；逐 token metric 的局部证书不能自动推出整个产品稳定，且与 PDN/KDN/GDN2/QED 的几何重合。

同时加入 2026-10-02 的 GSA2 全公式边界：key→slot 使用 OJA2 correction，slot→value 使用 Delta2 correction，并在两侧解耦 erase/write。因此“双侧纠错、reverse/Oja update、两阶段共享 slots”不能再作为新候选名称；该论文的 arXiv 记录没有作者指定代码链接，所以未冒充源码审查。

## 下一合法动作

从零活动候选重新寻找具有新 causal observable 或 state invariant 的部署递推，并在分配新 D 编号前完成最近工作分离。排除 GSA2 双侧 slot correction、unitary dilation、source-utility attribution、fixed-metric preconditioning，以及所有既有 inactive/no-go 路线；不得只换 loss、坐标、门范围或辅助噪声来凑数。

入口：[进度](PROGRESS.json)、[证据批次](method-batch.json)、[近邻图](CLOSEST_WORK.md)、[排名状态](RANKING.md)。当前没有全池排名或 top-15 选择。
