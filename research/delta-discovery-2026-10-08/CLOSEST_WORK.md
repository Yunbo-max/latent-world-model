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
| D01 → 双完整状态 mixture / Wilson / rank-one Bayesian ensemble / Memory by Design / Voltic | 双完整状态 mixture 是预测等价强基线。Wilson 的多 Delta-rule predictor mixture 与 Voltic 的高斯均值/协方差递推形成强部分碰撞；D01 只余“共同未来仿射路径下单事件两策略差分的 rank-one 精确压缩” | [D01 sources](sources/D01-sources.md)、[ROOT扩展](sources/ROOT_SOURCE_EXPANSION.md)、[Voltic全文审计](sources/VOLTIC_D01_FULL_AUDIT.md)。Voltic v1 未定位作者代码；低秩 recurrent ensemble 仍未闭，因此 D01 继续 pending |
| D03 → PDN / QED / KDN / Delayed Supervision / observability Gramian / Q-Delta | Q-Delta 的 query-mixed residual probe 与时间演化 key/adjoint 已知；其左侧 write 方向仍是 k。D03 改变左侧 write 方向 u，并以预测未来 transported-query Gramian 约束 kᵀu=1，机制不同但残余很窄 | [Q-Delta全文与作者源码审计](sources/QDELTA_FULL_AUDIT.md)、D03 audit、ROOT扩展。Q-Delta 必须作为强 baseline；更广 collision audit 仍 pending |
| D04 → When Quantization Breaks Memory | 普通补偿与误差反馈直接碰撞；大辅助状态不自动是新机制 | [否定卡](rejected/D04_COMPENSATION_COLLISION.md) |
| D05 → balanced realization / STEPQuant / DAMP / MambaQuant / SmoothQuant / LeapQuant | D05 的 (C/O) 白化、output-aware sensitivity 与 water-filling 被经典 input-normal/output-diagonal realization 及 Delta-state mixed-precision 工作实质覆盖。完整 future-query Gramian、密集广义特征基与因果预测器只是窄组合残余 | [D05全文审计](sources/D05_CLOSEST_FULL_AUDIT.md)。处置为重大功能重合；保留条件性数学历史，不再计活动候选 |
| D06 → orthogonal/unitary RNN / dynamical isometry / pLSTM/chrono / log-det control / constrained gating | 普通 contractive Delta 下，滑窗 log-volume token budget 给出显式最小奇异值下界。限定审计未发现精确同构，但各组成原语均已知；维数缩放、并行训练和语义错配仍未闭 | [D06全文审计](sources/D06_CLOSEST_FULL_AUDIT.md)。暂保留条件性残余，原创性与科学准入仍 unresolved |
| revision-vs-collision no-go | 当同一因果信息下两世界观测律接近且要求相反动作时，任意随机策略的等先验平均错误至少为 `(1-TV)/2`；diffusion/内部随机性不增加证据 | [NOGO-RC-01](rejected/NOGO_RC_01.md)及[独立审查](reviews/NOGO_RC_01.review.md)。这是 Le Cam/TV data-processing 的问题边界，不计新候选 |
| protected projection identifiability boundary | `z=Πk` 时最小范数保护写入为 `β z eᵀ/||z||²`；`z=0,e≠0` 不可行，范数随 `1/||z||` 爆炸 | [边界推导](rejected/IDENTIFIABILITY_PROJECTION_BOUNDARY.md)。与 projection/soft-preconditioner/slots/PDN-KDN 邻域重合，拒绝为独立方法 |
| minimax retention no-go | 固定精确 current-key contraction 时，任何线性 erase 的全局 `sigma_min` 不超过 `1-beta`；普通 Delta 已达到该 minimax 上界 | [NOGO-MR-01](rejected/NOGO_MR_01.md)。以后只能改成 query-weighted risk、放宽纠错、增加状态/读出或显式支付扩张与数值代价，不计候选 |
| chronological commutator no-go | transition 交换子遗漏 affine write 项；同 key 不同 value 即给出零 transition commutator、非零顺序误差。精确 parallel scan 只需结合律而非交换律 | [NOGO-OC-01](rejected/NOGO_OC_01.md)。保留为顺序诊断，不计候选 |
| transported influence ledger | 冻结仿射路径下旧事件影响可用 forward sensitivity 精确搬运，但与 RTRL/eligibility trace 同构；无事件身份不可辨，有身份则退化为 exact-event replay | [控制记录](rejected/TRANSPORTED_INFLUENCE_LEDGER.md)。不占 D07 |

上述已读的是必要公式/算法与具体接口，不是所有论文/仓库逐行审计。引用量与 checker 通过不证明原创性。原始代码未运行，未下载模型/数据，未造实验结果。公共可测量对象和原生 scorer 边界见 [BASELINE_NATIVE](sources/BASELINE_NATIVE.md) 与[本轮可行性核查](sources/MEASUREMENT_FEASIBILITY_2026-10-09.md)；机制主张的 measurement gap 不能由通用 QA 得分消除。
