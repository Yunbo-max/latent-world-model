# 全池排名尚未到达：当前活动池为零

目标是最多 20 个实质不同、数学成立且通过近邻审查的候选，再对完整池排序并默认选择前 15。构造历史现有 D01、D03、D05、D06、D07 五张卡；决定性审查已把五张全部移为控制、诊断或历史，当前活动池为 **0**。D07 的条件数学仍成立，但完整公式与作者代码审计确认：一般 source contribution、realized-path survival 及同-key 特例已被直接近邻覆盖，主功能又有 write-rate decay 与 delayed semantic supervision；只余 direct arbitrary-key hinge 的窄实现差异，不足以科学准入。

**没有全池排名、没有 method-selection、没有 selection-review，也没有 `selection_verified`。** 零张活动卡不能产生 top-15，五张被移出的卡也不能被反向计入排名。

D07 的比较对象是普通远期 CE、Delayed Supervision、How Linear Attention Remembers/RPMem 的 source trace/survival，以及 Tabular ICL 的 write-rate decay。其内部量 `||P k_i||²` 与 D03 的 future-readout metric、D06 的 global spectral floor 确实不同，但它仍可能提高状态范数而不提高 query 可见性，甚至保存过时事实。重新准入需要 formal arbitrary-key separation、与同信息语义监督的非等价、revision release 及可识别测量四项同时闭合。

本轮继续闭合三条看似可行但不独立的路线：unitary dilation 需要随时域增长的 defect slots；query-visible counterfactual utility 对局部写入就是普通 future CE，并与 AttriMem/HiMPO 式 signed credit 碰撞；固定 SPD metric oblique Delta 精确等价于白化后的 preconditioned Delta。GSA2 又直接覆盖双侧 Oja/Delta correction 与共享 slots。它们减少无效路线，不增加活动计数。

2026-10-09 的下一轮又独立闭合五条路线：随机 Bernoulli survival 只把均值保留换成乘法方差或 recurrent dropout；dual-frame 只能以更宽状态保护外部噪声，不能侦测合法 code-subspace 内的 Delta 干扰；checksum/sketch 不能从无身份的因果观测中创造 revision 证据；causal polynomial/Krylov 分别退化为未来风险预测、solver、trace 或 DeltaProduct；Magnus/commutator 抑制会同时抹掉合法 last-write chronology。QED 全文公式与公开代码可得性审计也已闭合。它们继续减少无效路线，但活动、科学准入和选择计数仍全为零。

同日再闭合四条路线：reciprocal cycle 在当前 pair 完全写入后变成恒等式，且与 BAM/GSA2/双向 ridge 碰撞；rank-revealing QR 的精确新意只是已知 hard projection/QR-RLS feasibility diagnostic；martingale release 提供严格 anytime false-release 控制却仍是标准 change detector 加既有 edit，并受 revision/collision 信息边界限制；任意 inverse-transported time-varying metric 能把收缩或爆炸都重标为等距，必须加入 uniform coercivity 与双边 cross-time bound 才有物理意义，随后回到 D06/经典 contraction。四项均有独立数学审查，只作为控制/no-go 保存，活动计数不变。

本轮又闭合四条：历史回滚在 frozen-affine 路径上是已发表的 receipt transport，真实 state-dependent omission 则必须 checkpoint+replay；集合值状态是经典 set-membership/version-space，单一凸包不能保存离散 revision/coexistence 分支；value 侧正交修正受 Gram 条件限制，而精确 key-local 版本与 full-step Delta 完全相同；`k⊗provenance` 是 TPR/Fast Weight Memory 上的普通 Delta，一热标签等价独立 slots，唯一事件标签仍需索引。四项都经独立审查，继续作为否定控制保存；构造历史仍为 5、活动/准入/选择仍为 0。

本轮再由三组独立数学/审查对闭合三条路线：exact-gradient-flow 与 implicit proximal 在 frozen token 下都是普通 Delta 的标量门重参数化，并与 EFLA/Longhorn 直接碰撞；half-decay/Delta/half-decay 的对称因子与 KDA 每步相似，修复原 key overwrite 后就是 PDN 式预条件读写地址；标准 contractive Delta 的逐步 Kreiss 常数恒为 1，而固定矩阵伪谱理论不能控制 token-varying 有序乘积，真正可执行的版本落回 product/Jacobian norm、common Lyapunov/JSR 或 D03。三项均只保留为控制，构造历史仍为 5、活动/准入/选择仍为 0。

最终排名仍将基于问题价值、数学后果、最近工作残余、区别性预测、最强简单替代及总成本。当前不得给出“最优 2–3 项”或暗示任何历史卡已获推荐。

第2步重定位新增了 [联合条件风险理论线索](STEP2_JOINT_CONDITIONAL_RISK.md)：方向性混合矩、完整内生 Jacobian 和有限二次矩边界已独立审查，weighted-Bayes/APO 原理碰撞保持可见。它尚缺 Delta-specific contribution、自然监督/测量与 tractability，因此不进入排序或选择。理论/目标构造无需强制改变递推，但同样不能免除新意、问题价值与条件审查。noisy-key BC/IV 只作目标识别控制；计数不变。

后续[真实预测监督与决定充分性推论](STEP2_OBSERVED_PREDICTIVE_TARGET.md)关闭预测监督对象的定义，并给出rank-one/gate条件、完整CE/GGN的代理边界与随机风险信息价值恒等式；[双重审查](reviews/STEP2_OBSERVED_PREDICTIVE_TARGET.review.md)按实际最终SHA绑定。它是同一Step2线索，TTT/ridge/Bayes/proximal已知基础和专门近邻缺口均保留，未完成自然重要性/估计成本/科学准入，不进入任何排名；活动/准入/选择仍为0。

[决定充分性的低秩控制](STEP2_ACTION_SUFFICIENT_RANK_CONTROL.md)进一步证明：在固定 SPD 二次 regret、线性 feature/head 下，宽度 `r` 的最优额外风险就是加权 action operator 的尾奇异值能量，多任务共享使用 stacked operator 且必须保留不可约 residual。它经最终字节数学/来源审查后仍被 Task-Sufficient Contraction、Bayes quotient、DSSR 与 RRR/EYM 分块直接覆盖，只留下随机信息依赖 metric × 递归 Jacobian × 因果估计的未准入残余。因此不分配 D 编号，不进入排序；计数仍为 **5历史 / 0活动 / 0准入 / 0选择**。

[递归随机条件矩控制](STEP2_RECURSIVE_RANDOM_METRIC_CONTROL.md)现已把该残余严格化：固定 teacher-forced 后缀上的联合对象是完整状态 Jacobian 拉回的 GGN/变分可观测 Gramian，精确 Hessian 另有可能不定的动力学/读出曲率；prefix-only predictor 是 synthetic-gradient/critic 类估计，编辑改变未来分布时还缺反事实项。动作/二次风险误差界可证，但 observability、GGN/DDP/iLQR、DNI、RTRL/UORO/e-prop 与 DSSR 已覆盖主要部件，native 数据也没有条件矩或理想 edit 标签。故仍不分配 D 编号、不进入排序；全池和 top-15 均未形成，计数不变。

新增授权后的[耦合更新器推导](STEP2_COUPLED_UPDATER_STABILITY.md)与[来源审查](sources/COUPLED_UPDATER_RSI_SOURCE_AUDIT.md)仍属Step2控制。SRWM/ACL/HOPE已覆盖自修改Delta及旧新任务学习目标；通用小增益/稳定纤维不是新候选。当前仍5历史/0活动/0准入/0选择，20/15短缺保留。没有池排序或推荐2–3项；新方向是待查重、待测量线索，不是重新批准代码/实验。

[动作投影延迟信用控制](STEP2_PROJECTED_DELAYED_CREDIT.md)得到四项条件结果：固定小维动作族只需 costate 在动作 span 上的投影；任何对所有动作精确评分的线性 summary 至少需要该 span 的维数；frozen 后续路径上的单个标量 Delta gate 有精确 rank-one eligibility；只观察局部二次延迟结果时，识别斜率/曲率需要条件 intervention Gram 满秩。完整闭环反馈、多个未结算 edit 和学习 key/value 方向会重新打开高维信用与长时程成本。MAML、learned optimizer、DNI、RTRL/UORO/e-prop、ACL/SRWM、DSSR、SEAL 与 TTT Ouroboros 已覆盖主要机制；尤其 Ouroboros 已实现 pending candidate、独立真实文本顺序验证和 Settlement。该结果经独立数学审查仍只是控制/lead，不分配 D 编号或进入排序；计数保持 **5历史 / 0活动 / 0准入 / 0选择**。

[完整闭环秩增长控制](STEP2_CLOSED_LOOP_RANK_GROWTH.md)进一步给出紧反例：未来只需一个读取 memory 的 scalar gate，单一焦点扰动的 exact Delta matrix tangent 就可每步增加一个独立 rank-one 方向；共享 gate 构造达到线性上界，并有 fixed-rank singular-tail 与 ordered truncation-error 界。独立审查同时限定：这不是一般算法内存下界，高 exact rank 也不等于数值重要或遗忘。RTRL/UORO、KF-RTRL/OK、SnAp、e-prop 与经典 EYM/扰动界覆盖主要方法成分，现有 native scorer 又不提供 tangent/rank 真值。因此它只关闭 frozen-path rank-one 的错误外推，不分配 D 编号或进入排序；计数仍为 **5历史 / 0活动 / 0准入 / 0选择**。

[有效秩与随机截断控制](STEP2_EFFECTIVE_RANK_TRUNCATION_CONTROL.md)又关闭了“只要完整路径收缩，高秩切向就会低相对秩”的外推：严格收缩路径仍可有平坦 H 维归一化奇异谱。年龄截断的对数绝对误差界需要额外保秩和 fading assumptions，无偏截断还承担 survival/variance 条件；Adaptive TBPTT、ARTBP、Randomized Telescopes、稳定 RNN 与 streaming/online sensitivity compression 已覆盖主要机制。它只留下真实非交换 Delta closure 和 costate-weighted matched-budget 优势这一窄缺口，不分配 D 编号或进入排序；计数仍为 **5历史 / 0活动 / 0准入 / 0选择**。
[R01 v1修复](repairs/R01_VALUE_SPAN_AND_CREDIT_MARGIN.v1.md)完成两条关联线索的独立最终字节审查。研究优先级为：先核实A的因果value-span闭包/容量条件，再核实B的goal-weighted residual证书能否省总成本；这是修复工作的先后依赖，不是正式候选排名或top15。已知降维Delta与inexact-gradient/adjoint weighting作为强对照保留；未闭贡献/成本/效果分别记录。活动/准入/选择仍0，池20/选择15短缺未填充。数学成立的控制不等于整个科学问题淘汰，旧反例也不删除。

[R01 v2修复](repairs/R01_VALUE_SPAN_AND_CREDIT_QUOTIENT.v2.md)解决了 v1“直接缩小 value-width 会丢容量”的目标错配：完整 `S` 不压缩，只压缩切向/信用商。但精确商宽度至少覆盖所有非退化 gate 与目标协向量的联合行空间，时变基还需核包含，近似闭合仍依赖被省略的完整切向泄漏。由于核心机制与 exact lumping、goal-oriented/time-varying MOR 重合，它目前是有用的条件理论控制，不进入正式排名。只有证明真实因果协向量并集小且总成本优于 plain JVP/VJP，才有重开候选资格；否则 R01 在第二次实质修订后暂存。计数仍为5历史/0活动/0科学准入/0选择，20/15短缺不变。

## R02 control disposition

R02 is excluded from the candidate ranking. Its conditional causal mathematics passed independent final-byte review, but the operative estimator is standard AIPW/sequential OPE and the native mechanism measurement is missing. Pool and selection counts are unchanged; it cannot displace or enter a top-15 list.


## R03 排名处置

R03 不进入活动池排名。问题价值高：它正面处理“为了因果识别而探索”与“保护仍有效旧查询”之间的冲突；数学后果也明确，包括局部损伤闭式、平方风险充分界和 positivity–budget 不可行条件。但贡献差异不足：安全 logging / constrained optimal design 已被 SEPEC、Safe Optimal Design 及相关 safe bandit 工作覆盖；实际效果和长期 coupled-state 安全未测。故其身份是 control/boundary，得分不替代候选资格，不能用于 top-15。全池仍 0 活动、0 准入、0 选择。

R03 v2 已修复“单步证书被误当长期证书”的问题：完整耦合状态的有序 gain、内生 query 的复合观测、精确首步加后续上界，以及概率单纯形可行条件均经最终字节复核。它只在事先可审计的统一 tube/gain 条件下给出随机 logging 的条件期望损伤证书，不保证每个动作安全，也不覆盖 edit 改变自由运行分布后的总效应。safe design、small-gain 与 online sensitivity 是强已知对照，原生联合测量仍缺失。因此修复提高了数学完整性，但没有改变 R03 的排名资格：仍为 parked control，候选增量为 0。


## R04修复处置

R04 v2条件数学通过，独立review修复非均匀D几何错误。问题价值是避免巩固双记账、区分当前读出/未来递推；完整补偿等价单W，差异decay产生显式强迫。主要快慢机制已知，C有效性/表示/固定总成本和原生测量未闭。不进入候选排序/top15，也不永久淘汰巩固。下一研究优先级为C联合风险/表示条件，其次具有真实Delta结构优势的信用商；这是工作优先级，不是正式选中2–3项。活动/准入/选择0，20/15短缺不变。

R04 v3完成第三次有界修订：用可表示接口和联合未来风险选择迁移，得到受约束 normal equation，并在标量快衰减特例得到 `p>alpha^T` 的正迁移边界。数学复核通过的仅是声明条件下的 control/theory；普通二次决策、选择性巩固和 cost-aware routing 有直接近邻，阈值不是 Delta 独有，真实 `p` 与反事实收益也不由部署几何识别。因此 R04 正式 park，不进入候选排序/top15；只有精确最近工作空缺和同预算原生判别对象同时出现才重开。活动/准入/选择仍0，20/15短缺不变。

## R05 排名处置

R05 修复了“联合标签不可得就只能停止”的过强结论：边际信息仍能给 `m=E[rZ]` 的锐利识别区间、minimax-regret gate 和 no-write 的充要认证边界。数学、来源与 measurement scope 的最终字节审查均通过。

它仍不进入活动池或 top15。原因不是公式错误，而是核心决策工具已由 Fréchet coupling、partial identification、Gamma-minimax 与 moment-DRO 覆盖；Delta 残余目前只是标量专门化，没有同预算 estimator 优势，也缺原生 joint mechanism measurement。R05 在 v3 后 park，候选增量0；全池仍0活动、0准入、0选择。
