# 定向近邻图与阅读边界

2026-10-08 实际阅读。箭头表示候选必须比较的最近机制，不代表证明相同或原创。精确版本、section/公式、作者 commit/文件/函数与字节固定见下列 source audit；没有接口阅读的项目明确 pending。

| 方向 | 已知机制/实际区别 | 状态与证据入口 |
|---|---|---|
| DeltaNet → GDN → KDA | 原始 residual Delta、decay gate、通道级遗忘；保持 decay 与 rank-one 因子实际顺序 | [原始文献与作者接口](sources/BASELINE_NATIVE.md)，[版本清单](sources/BASELINE_SOURCE_MANIFEST.json) |
| DeltaNet → RWKV-7 / DeltaProduct | 广义/多步更新不能仅改名计候选 | 同上，具体公式及 naive/time-mixing 接口已读，未执行 |
| DeltaNet → GDN2 / QED / EDA | erase/write 细化与 query 参与擦除已知；GDN2/QED 左侧 write 仍沿 k；EDA 独立 erase address 已有先例 | [QED 全公式/公开代码审计](sources/QED_FULL_FORMULA_CODE_AUDIT_2026-10-09.md)及 [PRIMARY_NEW](sources/PRIMARY_NEW.md)。QED 作者指定公开实现截至 2026-10-09 未定位；不虚构 kernel/吞吐审查 |
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
| GSA2 two-sided correction | OJA2 纠正 key→slot，Delta2 纠正 slot→value，共享 latent slots，并在两侧解耦 decay/erase/write | [GSA2 全公式审计](sources/GSA2_FULL_AUDIT.md)。双侧纠错、reverse/Oja correction、两阶段共享 slots、重复 correction 与 WY/UT 并行化均归直接 baseline；无作者指定代码链接，不虚构源码审查 |
| unitary/orthogonal Delta dilation | 单步 Halmos completion 可把 erase defect 放进辅助槽；复用槽会使旧内容回流，严格 contraction 的全时域 finite unitary dilation 不存在 | [NOGO-UNITARY-DILATION](rejected/NOGO_UNITARY_DILATION.md)及[独立审查](reviews/NOGO_UNITARY_DILATION.review.md)。有限时域需随 horizon 增长的新槽并退化显式记忆，不计候选 |
| counterfactual query-visible source utility | 固定后续路径时可精确删除一个 write 并测未来 query/CE 的 signed utility | [推导](rejected/COUNTERFACTUAL_QUERY_WRITE_UTILITY.md)及[独立审查](reviews/COUNTERFACTUAL_QUERY_WRITE_UTILITY.review.md)。对 write-local 参数梯度等于普通 future CE；AttriMem/HiMPO 等已覆盖 signed source reward，保留 diagnostic/lead，不计候选 |
| Lyapunov metric oblique Delta | `A=I-wrᵀ` 存在 SPD 非扩张度量 iff `0<rᵀw≤2`，且必须 `Hw∥r` | [度量控制](rejected/LYAPUNOV_OBLIQUE_METRIC.md)及[独立审查](reviews/LYAPUNOV_OBLIQUE_METRIC.review.md)。固定 H 精确白化为 normalized Delta；时变局部证书不自动组合，PDN/KDN/GDN2/QED 已覆盖核心几何，不计候选 |
| randomized Delta survival | compensated Bernoulli correction 保持单步均值但 repeated-key relative variance 指数增长；未补偿 mask 等价较小确定性 gate 加 update-dropout 噪声 | [推导](rejected/RANDOMIZED_DELTA_SURVIVAL.md)及[独立审查](reviews/RANDOMIZED_DELTA_SURVIVAL.review.md)。Zoneout、recurrent update dropout、stochastic rounding、low-discrepancy recurrent-cache dither、LeapQuant/STEPQuant 覆盖主要功能，不计候选 |
| redundant dual-frame Delta | `Z=FS` 的 exact encoded recurrence 与原 Delta 共轭；`r=d` 只是换坐标，`r>d` 是更宽物理冗余。合法 Delta 干扰仍在 code subspace，syndrome 看不见 | [NOGO-DUAL-FRAME-04](rejected/NOGO_DUAL_FRAME_04.md)及[独立审查](reviews/NOGO_DUAL_FRAME_04.review.md)。只缓解外部噪声/已知 erasure，属于 classical frame coding 与 D05/STEPQuant/PDN 控制 |
| checksum/sketch revision detector | 任意 causal sketch 受 data processing 限制；Bloom/SimHash 只有在稳定身份或角度间隔已提供证据时才工作，并且仍需 latest-value/version state | [控制](rejected/CHECKSUM_REVISION_SKETCH.md)及[独立审查](reviews/CHECKSUM_REVISION_SKETCH.review.md)。退化 approximate dictionary/event memory 或 evidence-conditioned gate，不计候选 |
| causal polynomial/Krylov future product | single-basis polynomial 只能逼近 prefix 可预测的 conditional future object；不能消除 suffix conditional variance 或一般 noncommutative order | [控制](rejected/NOGO_CAUSAL_POLYNOMIAL_FUTURE_PRODUCT.md)及[独立审查](reviews/NOGO_CAUSAL_POLYNOMIAL_FUTURE_PRODUCT.review.md)。分别落入 source trace、D03 predictor、GKA/PDN solver 或 DeltaProduct |
| affine Magnus/commutator compensation | exact order gap 必须含 affine write 项；same-key transitions 虽交换，different values 仍有 last-write gap。BCH aggregate 的 `+1/2` bracket 是顺序项而非应删除误差 | [控制](rejected/AFFINE_MAGNUS_COMMUTATOR_CONTROL.md)及[独立审查](reviews/AFFINE_MAGNUS_COMMUTATOR_CONTROL.review.md)。抑制 bracket 会破坏 revision semantics；exact affine scan 已可结合并行，不计候选 |
| reciprocal-cycle Delta | 同时维护 key→value 与 value→key 状态，并用 pre-write cycle loss 生成有限个 rank-one 更新 | [控制](rejected/RECIPROCAL_CYCLE_DELTA.md)及[独立审查](reviews/RECIPROCAL_CYCLE_DELTA.review.md)。full interpolation 后当前 cycle 恒等；无身份时 revision/collision 仍不可辨，BAM、GSA2、双向 ridge/RLS 与 reverse-prediction head 覆盖主要功能，不计候选 |
| rank-revealing constraint Delta | thin QR 精确区分新方向、冗余约束与线性不相容；最小 Frobenius edit 为 `Π⊥k eᵀ/(kᵀΠ⊥k)` | [控制](rejected/RANK_REVEALING_CONSTRAINT_DELTA.md)及[独立审查](reviews/RANK_REVEALING_CONSTRAINT_DELTA.review.md)。这是 Greville/QR-RLS 与 hard OWM/projection；soft relaxation 回到 RLS/PDN，不能给冲突添加语义标签 |
| martingale release gate | predictable likelihood ratio / conditional-CGF e-process 可给 hard release 的 anytime false-alarm bound | [控制](rejected/MARTINGALE_RELEASE_CONTROL.md)及[独立审查](reviews/MARTINGALE_RELEASE_CONTROL.review.md)。属于 e-detector/BOCPD/Kalman innovation change detection 加已知 edit；普通 Delta residual 不自动是 pre-outcome innovation，且同分布 revision/collision 的 stopping law 相同 |
| time-varying metric laundering | `H_t=A_t^{-T}H_{t-1}A_t^{-1}` 使任意可逆 prefix 在移动度量中等距 | [no-go](rejected/TIME_VARYING_METRIC_LAUNDERING.md)及[独立审查](reviews/TIME_VARYING_METRIC_LAUNDERING.review.md)。无 uniform coercivity 时可同时隐藏物理衰减与爆炸；合法双边 cross-time bound 回到经典 contraction/dynamical-isometry 或 D06，写方向回到 RLS/PDN，不计候选 |
| retroactive rollback Delta | frozen-affine event receipt 可沿有序 suffix 精确运输；真实 omission 改变后续特征时出现 forcing sum | [控制](rejected/RETROACTIVE_ROLLBACK_DELTA.md)及[独立审查](reviews/RETROACTIVE_ROLLBACK_DELTA.review.md)。arXiv:2609.06872v3 已给 Delta 专用 transport criterion/replay certificate；一般精确语义是 checkpoint+replay，任意 stable-ID 删除需要 provenance/history，不计候选 |
| set-valued Delta envelope | 维护与观测相容的线性 map 集合，做 transition Minkowski 扩张、measurement intersection 与椭球外包络 | [控制](rejected/SET_VALUED_DELTA_ENVELOPE.md)及[独立审查](reviews/SET_VALUED_DELTA_ENVELOPE.review.md)。直接属于 set-membership identification/version spaces；单凸集不能无损保存 revision/coexistence 离散分支，union 最坏指数增长，不计候选 |
| orthogonal value rotation | value-space Householder/Procrustes 保范数并尝试保护旧输出 | [控制](rejected/ORTHOGONAL_VALUE_ROTATION_CONTROL.md)及[独立审查](reviews/ORTHOGONAL_VALUE_ROTATION_CONTROL.review.md)。全局 edit 受 Gram 条件限制且按 value 方向泄漏；unit-key exact local form 与 full-step Delta 状态逐项相同，adaptive form Jacobian 奇异，MOSE/unitary/GSA2 近邻充分，不计候选 |
| provenance tensor Delta | lifted address `u=k⊗c` 将即时干扰变为 `(qᵀk)(rᵀc)` | [控制](rejected/PROVENANCE_TENSOR_DELTA.md)及[独立审查](reviews/PROVENANCE_TENSOR_DELTA.review.md)。这是 TPR/Fast Weight Memory 上的普通 Delta；one-hot tag 精确等价 routed independent slots，unique event tag 仍需索引，dense tag 回到 VSA/HRR crosstalk，不计候选 |
| exact-flow / implicit Delta | frozen-token gradient flow 与 proximal solve 都只改变 rank-one Delta 的标量步长 | [控制](rejected/EXACT_FLOW_IMPLICIT_DELTA_CONTROL.md)及[双重审查](reviews/EXACT_FLOW_IMPLICIT_DELTA_CONTROL.review.md)。unit-key softplus/exponential 参数化精确等于 sigmoid gate；EFLA 和 Longhorn 直接覆盖 exact-flow 与 implicit 公式，不计候选 |
| symmetric / Strang-split Delta | `D^{1/2}(I-βkkᵀ)D^{1/2}` 每步与 KDA 相似；同-key 修复变成 preconditioned separate-address Delta | [控制](rejected/SYMMETRIC_SPLIT_DELTA_CONTROL.md)及[双重审查](reviews/SYMMETRIC_SPLIT_DELTA_CONTROL.review.md)。Complex KDA 已写出相似关系；PDN/GDN2/EDA/DeltaProduct 覆盖可执行修复，Strang 阶数只在显式 frozen ODE 下成立，不计候选 |
| pseudospectral / Kreiss Delta | 标准 contractive Delta 因子满足 `K(A)=1`；固定矩阵 Kreiss 常数不约束 token-varying 有序乘积 | [控制](rejected/PSEUDOSPECTRAL_TRANSIENT_DELTA_CONTROL.md)及[双重审查](reviews/PSEUDOSPECTRAL_TRANSIENT_DELTA_CONTROL.review.md)。合法替代落回 product/Jacobian norm、common Lyapunov/JSR、PDN 或 D03 future-product；仅保留为 oblique shear 诊断，不计候选 |

| noisy-key identification / prediction | covariance subtraction 是 BC-LMS；paired-view 是 IV。恢复 latent slope 可增加 noisy-query 风险；单一观测不能识别 latent/noise 分解 | [连续数学控制](rejected/NOISY_KEY_IDENTIFICATION_PREDICTION_CONTROL.md)、[原文/固定作者代码](sources/NOISY_KEY_EIV_SOURCE_AUDIT.md)、[双重精确字节审查](reviews/NOISY_KEY_IDENTIFICATION_PREDICTION_CONTROL.review.md)。不计候选 |
| Step2 joint validity × future geometry | 条件二次最优解依赖联合矩，而非仅边际 posterior 与平均 metric；基础正常方程与 weighted Bayes/APO 已知 | [问题重定位和实际推导](STEP2_JOINT_CONDITIONAL_RISK.md)、[数学/来源审查](reviews/STEP2_JOINT_CONDITIONAL_RISK.review.md)。理论/目标线索，贡献及原生测量待闭合；不计活动卡 |

上述已读的是必要公式/算法与具体接口，不是所有论文/仓库逐行审计。引用量与 checker 通过不证明原创性。原始代码未运行，未下载模型/数据，未造实验结果。公共可测量对象和原生 scorer 边界见 [BASELINE_NATIVE](sources/BASELINE_NATIVE.md) 与[本轮可行性核查](sources/MEASUREMENT_FEASIBILITY_2026-10-09.md)；机制主张的 measurement gap 不能由通用 QA 得分消除。

第2步最新[观测预测目标推论](STEP2_OBSERVED_PREDICTIVE_TARGET.md)：真实未来 token CE 可定义监督，不需免费 r/u；固定 value方向的最优edit是标量ridge、gate可达性有精确条件，完整CE/GGN仍需full-state路径与局部误差。TTT v1 §2.2–2.3及官方JAX/PyTorch固定代码已经学习outer next-token任务；APO与Martens覆盖proximal/GGN基础。[实际来源审查](sources/OBSERVED_PREDICTIVE_TARGET_SOURCE_AUDIT.md)保留代码/函数/pin和APO作者代码不可得状态。随机风险下的最优动作信息充分性是条件Bayes推论，其专门decision-focused近邻仍pending，不能用“无需保留全部分布”一句话申请原创准入。该续接不计新卡。

原生记录修正：上列旧MEASUREMENT_FEASIBILITY把LAMBADA写作standard，但当前已查的project/scorer/preparation和官方配置实际采用**lambada_openai**。固定文件/blob/函数与差异在新source audit中逐项保留；不得混合版本，5153分母和旧历史不变。没有改评测代码或假称旧standard已获资格。

## Step2 action-sufficient rank 的直接近邻闭合

新的定向审计把静态对象拆成两块：Task-Sufficient Contraction / Bayes quotient / Walsh rate--regret / Wei planning sufficiency 已覆盖“任务决定应保留哪些 source distinctions”；固定 SPD metric 与 feature covariance 下的最优 rank-`r` action map 则是 RRR + Eckart--Young--Mirsky。两块的简单拼接不是新方法。DSSR 还直接覆盖递归 writer 的 future reader loss 与 forward rollout，并有正文链接的匿名代码接口；旧“未找到代码”记录已纠正。

唯一未闭的是 information-dependent random metric、完整递归 state Jacobian 与因果在线估计的共同耦合；它尚无自然真值、定理或可计算方案，因此只保留未准入 lead。LongMemEval 的 QA arm 有 endpoint，retrieval arm 有 turn/session evidence labels，但都不标注 ideal Delta edit、内部删除、Jacobian 或 action rank。详见 [审计](sources/ACTION_SUFFICIENT_RANK_SOURCE_AUDIT.md) 与 [独立审查](reviews/STEP2_ACTION_SUFFICIENT_RANK.review.md)。

## Step2 递归随机条件矩的闭合

[完整推导](STEP2_RECURSIVE_RANDOM_METRIC_CONTROL.md)把剩余耦合写成 `B^T sum J^T C J B`：它是沿 teacher-forced 轨迹的 CE/GGN 加权有限时域 differential/variational observability Gramian。精确 Hessian 还含 residual 与 dynamics/readout 二阶曲率；binary CE `z(u)=u^2,y=1,u=0` 给出 gradient=GGN=0、exact Hessian=-1 的最小反例。DNI、RTRL/UORO/e-prop、DDP/iLQR 与 DSSR 分别覆盖 future-gradient prediction、递归 sensitivity/sketch、二次 cost-to-go 与 logged-future writer rollout。

[固定来源/接口/native审计](sources/RECURSIVE_RANDOM_METRIC_SOURCE_AUDIT.md)保留 variational-Gramian、UORO/e-prop、iLQR 代码 pin 以及 bAbI/LAMBADA/LongMemEval 的真实标签边界。prefix-only 条件矩可用 suffix 作随机 teacher，但逐 suffix Newton 动作不能先求解再平均；自由运行分布被 edit 改变时还缺 score-function/反事实识别项。该线索形成严谨控制和误差界，没有获得 D 编号；当前残余只剩 Delta rank-one 结构能否给出相对 direct action/CE/synthetic-gradient 的可证明低成本优势。


## Delta 自改进更新器授权：新增近邻和稳定性控制

[完整来源/作者接口审查](sources/COUPLED_UPDATER_RSI_SOURCE_AUDIT.md)加入 HOPE/Titans、SEALv2及持续LoRA合并/原生GPT grader、SRWM/ACL、Sleepv2。自身产生Delta指令、旧/新任务元目标、多频率巩固和self-edit已覆盖；Sleep扩容量，SEAL评分依赖付费服务，HOPE/Titans作者代码未可得，均不能冒称同资源已验证实现。

[实际推导](STEP2_COUPLED_UPDATER_STABILITY.md)给完整gate-feedback Jacobian及O(n)局部结构乘积、bounded-beta和slow-clock反例、统一小增益与固定保护纤维条件。这是已知微分/控制几何的Delta实例化，不分配D编号；动态保护/合法释放和同预算学习效率仍待构造、查重与自然测量。

## Projected delayed credit / learned-updater collision boundary

[数学控制](STEP2_PROJECTED_DELAYED_CREDIT.md)、[来源/作者接口/测量审计](sources/PROJECTED_DELAYED_CREDIT_SOURCE_AUDIT.md)和[独立数学审查](reviews/STEP2_PROJECTED_DELAYED_CREDIT.math-review.md)共同收窄了 delayed-feedback 路线。

- MAML 与 learned optimizer 已覆盖 post-update future/query loss、更新器内部状态、多步 outer objective、二阶项/一阶近似和 truncated BPTT。
- DNI、RTRL/UORO/e-prop 覆盖 synthetic future gradient、exact/随机低秩 online sensitivity 和 eligibility-learning-signal 分离。
- ACL/SRWM、SEAL、HOPE 覆盖 learned/self-generated Delta rule、downstream self-edit reward、旧新任务目标与多频率自修改 memory。
- DSSR 在固定 logged future 上递归 rollout writer 并以冻结 reader 的未来 reference-action likelihood 评分。
- [TTT Ouroboros](https://arxiv.org/abs/2610.05076) 及作者仓库 `lingjivoo/ttt-ouroboros@f7811f878679864e686c84abcd83dd05efdc0417` 已实现 Fixed Generation / Recorded Replay、gradient conflict、pending candidate、独立真实文本顺序验证和 Settlement；“未来证据到了再提交”直接归 baseline。

当前未被本轮 source read 直接消除的只是：动作空间投影充分性/线性 summary 维数下界、frozen-path 单 gate rank-one eligibility，以及完整闭环下能否证明相对相同 low-rank action family 的成本或误差优势。它们仍缺原创性覆盖、可执行构造与原生三目标测量，故为 conditional control/lead，不是活动候选。

## Endogenous scalar-gate tangent rank growth

[完整推导](STEP2_CLOSED_LOOP_RANK_GROWTH.md)、[primary/作者接口/native审计](sources/CLOSED_LOOP_RANK_GROWTH_SOURCE_AUDIT.md)与[独立数学](reviews/STEP2_CLOSED_LOOP_RANK_GROWTH.math-review.md)/[来源审查](reviews/STEP2_CLOSED_LOOP_RANK_GROWTH.source-review.md)关闭了上段最后一个易误读点。

- frozen future gate/key/value 路径上的单 edit 确实保持 rank one；
- 但只要未来一个标量 gate 可微地读取 memory，exact focal directional tangent 每步就可再注入一个 rank-one 方向；共享 sigmoid gate 与依次正交 key/value 给出达到线性上界的合法 Delta 路径；
- 即使每个名义一步 Jacobian 严格收缩，有限时域 exact algebraic rank 仍可增长，只是奇异值幅度可衰减；
- fixed-matrix-rank decoded forward eligibility 有明确 Eckart--Young 尾误差，逐步截断误差则按完整闭环有序产品传播；
- 矩阵秩不是一般算法内存下界，reverse VJP 或符号表示可不物化该切向。

RTRL/NoBackTrack/UORO、KF-RTRL/OK、SnAp 与 e-prop 已覆盖 exact/随机低秩/Kronecker/稀疏/eligibility 近似的主要问题。因此这是一项 Delta-specific tight control，不能重新命名为低秩信用方法，也不证明遗忘或 RSI。BABILong、RULER、LongMemEval、bAbI、LAMBADA、CITB、TRACE、SEAL 只能给 endpoint/保持结果；没有一个原生 scorer 暴露 tangent rank、costate 或截断误差真值。处置：major component collision；无 D 编号，计数不变。

## Effective-rank / truncation boundary

[完整推导](STEP2_EFFECTIVE_RANK_TRUNCATION_CONTROL.md)、[固定来源/作者接口/native 审计](sources/EFFECTIVE_RANK_TRUNCATION_SOURCE_AUDIT.md)与[独立数学](reviews/STEP2_EFFECTIVE_RANK_TRUNCATION.math-review.md)/[来源](reviews/STEP2_EFFECTIVE_RANK_TRUNCATION.source-review.md)审查了“高代数秩是否在收缩下自然可压缩”。

- 一个合法 scalar-gate Delta 路径可让每个完整一步切向算子都严格收缩，同时终点的归一化奇异谱在 H 个方向上完全平坦；稳定不推出低相对 effective rank。
- `O(log(1/epsilon))` 的绝对秩只在即时注入秩有界、有序背景传输保秩、transported contribution 按年龄衰减且初值另计时成立；它可退化为长期信用整体消失。
- 固定路径 Russian-roulette 可无偏，但 survival 单调、可积性与方差必须记账；平坦谱对任意无偏 rank-r 压缩给出核范数方差下界。
- Stable Recurrent Models、Neumann-RBP、Adaptive TBPTT、ARTBP、Randomized Telescopes、Tropp sketches/Frequent Directions，以及既有 RTRL 系列压缩已覆盖主要部件。

generic streaming sketch 对任意非交换 `L_t` 的 co-range/core 更新并不自动闭合，这是残余接口边界，不是已构成的新方法。只有能为真实完整 Delta transition 证明合法 closure，并在同信息、bytes/FLOPs 下改善 costate/action-gradient 误差，才值得重开候选构造。当前无 D 编号，计数不变。
## R01 repair nearest-work delta

[修订推导](repairs/R01_VALUE_SPAN_AND_CREDIT_MARGIN.v1.md)、[固定来源审计](sources/REPAIR_R01_SOURCE_AUDIT.md)与[独立最终来源审查](reviews/REPAIR_R01.source-review.md)保留以下对照：离散固定右-span闭包不同于Lubich–Oseledets连续variable-factor projector splitting，但都是已知不变量/低秩表示几何；强制S=ZVᵀ、v=Vw就是较小value-width Delta。SnAp的稀疏结构是其他合法full-sensitivity简化对照。Vernimmen–Glineur v2及固定作者utilities_neuro.py使用relative-gradient oracle和已给smoothness参数，不能提供本项目的合法残差/曲率常数或神经loss全局收敛。R01的absolute scalar interval和finite-step majorizer自行推导，仍属inexact-gradient/adjoint error原则，不称新优化器。Hallak全文尚缺；adjoint作者overview仅支持已知原则，不冒充全文公式审查。残余是因果value几何或Delta-specific、同总成本可得的goal-weighted certificate；它们尚未构成D候选，不因已知部件就否定全部后续修复。

### R01 v2: full-capacity credit quotient

[R01 v2](repairs/R01_VALUE_SPAN_AND_CREDIT_QUOTIENT.v2.md)保留完整 `S`，只问线性切向商 `X↦XW` 是否足以递推并恢复目标信用。CLUE 的精确线性 lumping 已给出 Jacobian 行空间不变与最小不变子空间闭包；goal-oriented/DWR model reduction 已知以目标权重选择降维误差；线性时变 MOR 也直接覆盖时变投影/基接口。因此 `G=GWW^T`、`C=CWW^T`、相关协向量并集的宽度下界、时变基核包含与泄漏信用界，当前只记作这些通用原则在 scalar-gate Delta Jacobian 上的具体化/推论，不声明新机制。精确固定版本、作者实现接口、已读范围与未读缺口在[来源审计](sources/REPAIR_R01_V2_CREDIT_QUOTIENT_SOURCE_AUDIT.md)中；[数学审查](reviews/REPAIR_R01_V2.math-review.md)和[来源审查](reviews/REPAIR_R01_V2.source-review.md)绑定最终 artifact SHA `93683c851ddee51fbfa197e6b088bda6968ab112b38aad351f351c851021d2b5`。残余只可能是：真实 Delta 因果接口能以显著小于 `d_v` 的可证协向量并集工作，并且总成本优于 plain forward JVP / reverse VJP；目前无证据，故不准入。

## R02 randomized-action credit

| Component | Nearest work / interface | Residual and decision |
|---|---|---|
| finite randomized update action + delayed loss | Dudík–Langford–Li DR/AIPW | established general estimator; Delta only supplies the action map |
| changed future update policy | Jiang–Li sequential DR | requires target-reachable overlap and cumulative ratios; no Delta advantage proved |
| downstream self-edit reward | SEAL author code at `6d9c9f9...` | high-level collision; SEAL is LoRA/TTT and not propensity-logged Delta OPE |
| knowledge-update endpoint | LongMemEval at `9e0b455...` | measures final QA, not internal randomized action credit; native judge uses GPT-4o |
| remaining Delta claim | structured nuisance / safe logging / sufficient history | unproved repair leads; no candidate admission |


## R03 — protection-aware randomized Delta logging

- **Retained Delta result:** frozen one-step protected-query displacement d_a=α_a²β²(eᵀMe)kᵀG_pk; exact protected squared-risk cross-term; positivity–damage feasibility boundary.
- **Nearest direct mechanisms:** SEPEC (safe exploration minimizing IPW/DR evaluation variance), Safe Optimal Design (safe information-efficient logging), stage-wise constrained contextual bandits, CLUCB/SEA, IPS/AIPW/DR/SWITCH.
- **Strong protection controls:** no-write, hard projection/soft preconditioning, GEM, EWC, A-GEM, OGD.
- **Residual difference:** a cheap Delta rank-one local certificate can instantiate the generic safe-design cost, but no strict same-budget advantage or long-horizon semantic certificate is proved.
- **Disposition:** useful control/theoretical boundary; parked after R03 v1; not an active candidate.

### R03 v2 — coupled-horizon repair

[R03 v2](repairs/R03_COUPLED_HORIZON_SAFETY.v2.md) replaces the unsupported jump from one-step displacement to long-horizon safety with a conditional theorem on the complete joint memory/updater state. The bound uses pre-action measurable simultaneous tube constants, ordered products of complete-step gains, and an augmented observable for endogenous future queries. Its hybrid form retains the exact Delta first-step term and bounds only later propagation; the logging simplex is feasible exactly when `b_H >= epsilon_mu sum_a Ubar_a + (1-K epsilon_mu) min_a Ubar_a`, with `K epsilon_mu <= 1`.

This does not create a new safe-learning mechanism. Safe exploration/design supplies the propensity optimization; incremental stability and small-gain analysis supply the dynamical certificate; RTRL-family work supplies full sensitivity alternatives. The certificate controls conditional expected harm under the randomized action distribution, not every action, and a common-exogenous trajectory does not identify free-running distribution effects. Existing LongMemEval/SEAL/CITB/TRACE/bAbI/LAMBADA interfaces do not jointly expose propensities, protected-validity labels, uniform gains, and counterfactual outcomes. Exact-byte math and source reviews accept the scoped theorem but keep R03 parked with zero candidate admission.


## R04 consolidation repair/control

[Source audit](sources/REPAIR_R04_CONSOLIDATION_SOURCE_AUDIT.md) pins Sleep 2606.03979v2 §3.2–3.3, HOPE 2512.24695v1 Eq70–74, SynControl d8681d2af9f858827fa1f22f7910e00eb2284fbc actual total-residual/fast-slow control interfaces, and SEAL/LongMemEval drivers/scorers. Full compensation is redundant single-W Delta; fast-only decay gives E(I-D)M. Strong known controls do not certify this exact conditional theorem as fully covered or original. Sleep/HOPE author code, 1987 formula reading and native persistent Delta consolidation gaps remain. Independent final-byte reviews accept scope; no candidate.

### R04 v3 joint selection

[Updated audit](sources/REPAIR_R04_V3_SELECTION_SOURCE_AUDIT.md) adds formula-level selective consolidation in Leimer et al. 2019, fast/slow noise-timescale dynamics plus pinned author notebooks in Bhasin–Raymond–Goldman 2024, and Dual-Layer Agentic Memory `2608.22215v2` §§3.3–3.4 (counterfactual write reward, escalation gate, SFT write-back, probe flush). It also separates Sangyun Lee et al. `2605.26099` persistent SSM fast-weight Sleep from Behrouz et al. `2606.03979v2` expert/distillation Sleep. Generic quadratic Bayes action, fast/slow selective consolidation and cost-aware routing are covered; no read source was found to give the exact `p>alpha^T` statement, but that threshold is a generic survival decision special case, not sufficient method novelty. Author code/data for Dual-Layer remain unavailable. R04 v3 is a parked conditional theory/control, not a candidate.

## R05 部分识别门的最近工作处置

R05 的 support/quantile 端点属于固定边缘 Fréchet class 与 rearrangement 极值；区间上的 minimax-regret 决策属于 partial-identification/robust-Bayes 邻域，moment-DRO 是更宽泛对照。残余仅是把这些已知原理映射到 `validity × Delta horizon sensitivity` 的标量风险、并导出 no-write 可认证边界；这是一条待查重的专门化 corollary，不足以形成新算法候选。

原生接口核查限定在固定版本：ROME/CounterFact、EvEdit、EasyEdit、sequential editing 均能测 efficacy/locality/reasoning/下游退化等 endpoint，但不记录 R05 所需逐次 `r,J,Z,m` 或两个潜在动作结果。来源、贡献差异与 measurement gap 的最终独立复核均通过；处置为 parked control，候选增量0。
