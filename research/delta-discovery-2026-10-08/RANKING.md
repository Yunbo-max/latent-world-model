# 全池排名尚未到达：当前活动池为零

目标是最多 20 个实质不同、数学成立且通过近邻审查的候选，再对完整池排序并默认选择前 15。构造历史现有 D01、D03、D05、D06、D07 五张卡；决定性审查已把五张全部移为控制、诊断或历史，当前活动池为 **0**。D07 的条件数学仍成立，但完整公式与作者代码审计确认：一般 source contribution、realized-path survival 及同-key 特例已被直接近邻覆盖，主功能又有 write-rate decay 与 delayed semantic supervision；只余 direct arbitrary-key hinge 的窄实现差异，不足以科学准入。

**没有全池排名、没有 method-selection、没有 selection-review，也没有 `selection_verified`。** 零张活动卡不能产生 top-15，五张被移出的卡也不能被反向计入排名。

D07 的比较对象是普通远期 CE、Delayed Supervision、How Linear Attention Remembers/RPMem 的 source trace/survival，以及 Tabular ICL 的 write-rate decay。其内部量 `||P k_i||²` 与 D03 的 future-readout metric、D06 的 global spectral floor 确实不同，但它仍可能提高状态范数而不提高 query 可见性，甚至保存过时事实。重新准入需要 formal arbitrary-key separation、与同信息语义监督的非等价、revision release 及可识别测量四项同时闭合。

本轮继续闭合三条看似可行但不独立的路线：unitary dilation 需要随时域增长的 defect slots；query-visible counterfactual utility 对局部写入就是普通 future CE，并与 AttriMem/HiMPO 式 signed credit 碰撞；固定 SPD metric oblique Delta 精确等价于白化后的 preconditioned Delta。GSA2 又直接覆盖双侧 Oja/Delta correction 与共享 slots。它们减少无效路线，不增加活动计数。

2026-10-09 的下一轮又独立闭合五条路线：随机 Bernoulli survival 只把均值保留换成乘法方差或 recurrent dropout；dual-frame 只能以更宽状态保护外部噪声，不能侦测合法 code-subspace 内的 Delta 干扰；checksum/sketch 不能从无身份的因果观测中创造 revision 证据；causal polynomial/Krylov 分别退化为未来风险预测、solver、trace 或 DeltaProduct；Magnus/commutator 抑制会同时抹掉合法 last-write chronology。QED 全文公式与公开代码可得性审计也已闭合。它们继续减少无效路线，但活动、科学准入和选择计数仍全为零。

同日再闭合四条路线：reciprocal cycle 在当前 pair 完全写入后变成恒等式，且与 BAM/GSA2/双向 ridge 碰撞；rank-revealing QR 的精确新意只是已知 hard projection/QR-RLS feasibility diagnostic；martingale release 提供严格 anytime false-release 控制却仍是标准 change detector 加既有 edit，并受 revision/collision 信息边界限制；任意 inverse-transported time-varying metric 能把收缩或爆炸都重标为等距，必须加入 uniform coercivity 与双边 cross-time bound 才有物理意义，随后回到 D06/经典 contraction。四项均有独立数学审查，只作为控制/no-go 保存，活动计数不变。

本轮又闭合四条：历史回滚在 frozen-affine 路径上是已发表的 receipt transport，真实 state-dependent omission 则必须 checkpoint+replay；集合值状态是经典 set-membership/version-space，单一凸包不能保存离散 revision/coexistence 分支；value 侧正交修正受 Gram 条件限制，而精确 key-local 版本与 full-step Delta 完全相同；`k⊗provenance` 是 TPR/Fast Weight Memory 上的普通 Delta，一热标签等价独立 slots，唯一事件标签仍需索引。四项都经独立审查，继续作为否定控制保存；构造历史仍为 5、活动/准入/选择仍为 0。

最终排名仍将基于问题价值、数学后果、最近工作残余、区别性预测、最强简单替代及总成本。当前不得给出“最优 2–3 项”或暗示任何历史卡已获推荐。
