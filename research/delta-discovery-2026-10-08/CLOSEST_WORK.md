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
| D01 → 双完整状态 mixture / Wilson / rank-one Bayesian ensemble / Memory by Design / Voltic | 双完整状态 mixture 是预测等价强基线。低秩表示与 mixture 均已有；单事件 fast-state 的残余需继续比对 | [D01 sources](sources/D01-sources.md)、[ROOT扩展](sources/ROOT_SOURCE_EXPANSION.md)。Wilson 2018纠正已读；原始公式图像和迁移后作者代码待核；Voltic仅摘要，不假称全文 |
| D03 → PDN / QED / KDN / Delayed Supervision / observability Gramian / Q-Delta | 历史度量、当前 query 擦除、后验协方差和普通远期监督均是强解释。未来传输度量不同于当前几何，但还未完全排除 query-mixed 更新 | D03 audit、ROOT扩展；Q-Delta官方元数据/摘要已读，全文公式和作者接口 pending |
| D04 → When Quantization Breaks Memory | 普通补偿与误差反馈直接碰撞；大辅助状态不自动是新机制 | [否定卡](rejected/D04_COMPENSATION_COLLISION.md) |

上述已读的是必要公式/算法与具体接口，不是所有论文/仓库逐行审计。引用量与 checker 通过不证明原创性。原始代码未运行，未下载模型/数据，未造实验结果。公共可测量对象和原生 scorer 边界见 BASELINE_NATIVE；机制主张的 measurement gap 不能由通用 QA 得分消除。
