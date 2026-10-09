# 定向近邻图与阅读边界

2026-10-08 实际阅读。箭头表示候选必须比较的最近机制，不代表证明相同或原创。精确版本、section/公式、作者 commit/文件/函数与字节固定见下列 source audit；没有接口阅读的项目明确 pending。

| 方向 | 已知机制/实际区别 | 状态与证据入口 |
|---|---|---|
| DeltaNet → GDN → KDA | 原始 residual Delta、decay gate、通道级遗忘；保持 decay 与 rank-one 因子实际顺序 | [原始文献与作者接口](sources/BASELINE_NATIVE.md)，[版本清单](sources/BASELINE_SOURCE_MANIFEST.json) |
| DeltaNet → RWKV-7 / DeltaProduct | 广义/多步更新不能仅改名计候选 | 同上，具体公式及 naive/time-mixing 接口已读，未执行 |
| DeltaNet → GDN2 / QED / EDA | erase/write 细化与 query 参与擦除已知；GDN2/QED 左侧 write 仍沿 k；EDA 独立 erase address 已有先例 | [PRIMARY_NEW](sources/PRIMARY_NEW.md)。QED 全文已读；EDA 作者专门实现未定位，不当作已检验代码 |
| 历史 ridge → PDN | 理论非对角 inverse-Gram 与实际稳定对角预条件有差别，不能混成一项实现保证 | PRIMARY_NEW；[D03 audit](sources/D03_D04_SOURCE_AUDIT.md)、[源码字节清单](sources/D03_SOURCE_MANIFEST.json) |
| Bayesian covariance → GKA / KDN | GKA 是 H/U 统计和有限次 Chebyshev query solve；KDN 高斯增益、对角逆 KL/扫描近邻已经覆盖简单协方差释放 | PRIMARY_NEW；[KDN v2公式/作者源码审查](sources/KDN_REVIEW_SOURCE_AUDIT.md) |
| 稀疏/多槽 → Sparse Delta Memory | 路由与容量本身不新；正文 row-local residual 与附录/源码 aggregate Delta 差异仍需澄清 | BASELINE_NATIVE；未借用未经闭合的 dense 等价性 |
| 保护几何 → OWM/projection/soft-preconditioner | 正 ridge 的软算子不是幂等正交投影；指定保护子空间可能与新写入冲突 | BASELINE_NATIVE；D01 card 的可行性条件 |
| D01 → 双完整状态 mixture / Wilson / PF-RNN / BatchEnsemble / Voltic | 后验加权多假设、recurrent particles 与低秩 ensemble 均已有先例；在单事件共享未来仿射条件下，D01 与显式双完整状态 mixture 是可逆坐标重参数化，预测逐项相同 | [决定性审计](sources/D01_DECISIVE_COLLISION_AUDIT.md)。保留为 exactness/equivalence control，重大功能碰撞，不再计活动候选 |
| D03 → observability/adjoint / APO / PDN / Q-Delta | `G=JᵀJ` 是有限时域 observability/Gauss–Newton function metric，归一化 inverse-metric 方向是 natural-gradient/proximal edit。APO、PDN、Q-Delta 分别覆盖主要功能；只余 token-conditioned 未来 metric 的直接组合 | [广义碰撞审计](sources/D03_BROAD_COLLISION_AUDIT.md)、[Q-Delta全文与作者源码审计](sources/QDELTA_FULL_AUDIT.md)。保留为 normalized-observability control，不再计活动候选 |
| D04 → When Quantization Breaks Memory | 普通补偿与误差反馈直接碰撞；大辅助状态不自动是新机制 | [否定卡](rejected/D04_COMPENSATION_COLLISION.md) |
| D05 → balanced realization / STEPQuant / DAMP / MambaQuant / SmoothQuant / LeapQuant | D05 的 (C/O) 白化、output-aware sensitivity 与 water-filling 被经典 input-normal/output-diagonal realization 及 Delta-state mixed-precision 工作实质覆盖。完整 future-query Gramian、密集广义特征基与因果预测器只是窄组合残余 | [D05全文审计](sources/D05_CLOSEST_FULL_AUDIT.md)。处置为重大功能重合；保留条件性数学历史，不再计活动候选 |
| D06 → HGRN / Spectral-RNN / coRNN / UnICORNN / COLD / token bucket | 普通 contractive Delta 下的滑窗 log-volume budget 确有条件性最小奇异值界；但动态 retention floor、谱/Jacobian 保留及窗口资源控制均已知，当前 greedy clip 无 utility/regret/competitive 最优性 | [扩展碰撞审计](sources/D06_EXTENDED_COLLISION_AUDIT.md)。保留为 log-volume diagnostic/guardrail，不再计活动候选 |
| D07 WTSR → source traces / write-rate decay / Delayed Supervision | `||P k_i||²` 在 frozen path 上确实是实际 source-write 方向的归一化状态生存；但一般 source contribution、realized-path survival 与同-key 标量特例均已有直接近邻，主要保留功能又有 write-rate decay 与 delayed semantic supervision | [完整碰撞审计](sources/D07_FULL_COLLISION_AUDIT.md)、[独立裁决](reviews/D07.collision-review.md)。只余 arbitrary-key direct hinge 的窄公式差异，无必要性、revision release 或 native 机制测量，移为 inactive diagnostic |
| DeltaTTT → multi-layer/local-target nonlinear Delta | 两层状态依赖 Delta 写入、local squared targets、pre/post hidden target 与 exact chunkwise nonlinear recurrence 已是明确方法族；不能把堆叠 Delta 或局部 reconstruction loss 计作新候选 | [DeltaTTT原文审计](sources/DELTATTT_FULL_AUDIT.md)。未定位作者指定代码，故不虚构接口；未生成候选 |
| revision-vs-collision no-go | 当同一因果信息下两世界观测律接近且要求相反动作时，任意随机策略的等先验平均错误至少为 `(1-TV)/2`；diffusion/内部随机性不增加证据 | [NOGO-RC-01](rejected/NOGO_RC_01.md)及[独立审查](reviews/NOGO_RC_01.review.md)。这是 Le Cam/TV data-processing 的问题边界，不计新候选 |
| protected projection identifiability boundary | `z=Πk` 时最小范数保护写入为 `β z eᵀ/||z||²`；`z=0,e≠0` 不可行，范数随 `1/||z||` 爆炸 | [边界推导](rejected/IDENTIFIABILITY_PROJECTION_BOUNDARY.md)。与 projection/soft-preconditioner/slots/PDN-KDN 邻域重合，拒绝为独立方法 |
| minimax retention no-go | 固定精确 current-key contraction 时，任何线性 erase 的全局 `sigma_min` 不超过 `1-beta`；普通 Delta 已达到该 minimax 上界 | [NOGO-MR-01](rejected/NOGO_MR_01.md)。以后只能改成 query-weighted risk、放宽纠错、增加状态/读出或显式支付扩张与数值代价，不计候选 |
| chronological commutator no-go | transition 交换子遗漏 affine write 项；同 key 不同 value 即给出零 transition commutator、非零顺序误差。精确 parallel scan 只需结合律而非交换律 | [NOGO-OC-01](rejected/NOGO_OC_01.md)。保留为顺序诊断，不计候选 |
| transported influence ledger | 冻结仿射路径下旧事件影响可用 forward sensitivity 精确搬运，但与 RTRL/eligibility trace 同构；无事件身份不可辨，有身份则退化为 exact-event replay | [控制记录](rejected/TRANSPORTED_INFLUENCE_LEDGER.md)。不占 D07 |
| exact overwrite / reversible retention no-go | 对所有旧状态和值都精确覆盖当前 key，强制旧状态线性路径奇异；显式有限精度下，共存旧行为类与新值还需联合编码容量 | [NOGO-CAP-02](rejected/NOGO_CAP_02.md)及[独立审查](reviews/NOGO_CAP_02.review.md)。只覆盖声明的 affine/all-state/no-side-state 条件，不计候选 |
| deferred correction debt | `main+debt=ideal` 在共享 frozen affine 路径上精确，但 future-key repayment 是 transported error feedback；安全偿还是 projection+controllability，无身份不可选择取消，有身份退化 replay/event memory | [控制记录](rejected/DEFERRED_CORRECTION_DEBT.md)及[独立审查](reviews/DEFERRED_CORRECTION_DEBT.review.md)。不占 D07 |
| bare oblique erase no-go | 对 `A=I-kaᵀ`，erase 方向任一垂直于 `k` 的分量都使裸因子 `||A||₂>1`；只有 `a=ck,c∈[0,2]` 可欧氏非扩张 | [NOGO-OBLIQUE-03](rejected/NOGO_OBLIQUE_03.md)及[独立审查](reviews/NOGO_OBLIQUE_03.review.md)。不能外推到 `AD/DA`；独立 decay 及实际顺序必须单独审查，不计候选 |
| evidence-conditioned revision edit | 新观测证据可解除 residual-only TV no-go；posterior-weighted ridge 有闭式两向量解，hard-protection 极限回到 `Πk/||Πk||²` | [控制推导](rejected/REVISION_EVIDENCE_POSTERIOR_EDIT.md)及[独立审查](reviews/REVISION_EVIDENCE_POSTERIOR_EDIT.review.md)。无证据仍不可辨，完美 ID 退化 routing，概率证据是 Bayes gate+已知 edit，future teacher 是额外监督，不计候选 |

上述已读的是必要公式/算法与具体接口，不是所有论文/仓库逐行审计。引用量与 checker 通过不证明原创性。原始代码未运行，未下载模型/数据，未造实验结果。公共可测量对象和原生 scorer 边界见 [BASELINE_NATIVE](sources/BASELINE_NATIVE.md) 与[本轮可行性核查](sources/MEASUREMENT_FEASIBILITY_2026-10-09.md)；机制主张的 measurement gap 不能由通用 QA 得分消除。

