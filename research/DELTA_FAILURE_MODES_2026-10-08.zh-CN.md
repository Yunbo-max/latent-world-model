# Delta 的缺点与改进位点：diffusion 作为可选工具

## 本次范围纠正

用户于 2026-10-08 23:31 Europe/London 说：“我觉得diffusion是一个方法但是不是主要吧？你看看还有什么idea可以，就是针对当前的方法缺点是什么”。

据此，主线调整为 **Delta 记忆更新本身的缺点及改进**。Diffusion 是可选训练、预测或读出工具，不是预定的主要贡献，也不是每个方案的必需组件。上一份 DELTA_DIFFUSION_DIRECTION 记录保留为历史方向，不能再据其优先级强行选择 diffusion 写入方案。

本记录中的“当前方法”指 Delta/KDA 这一类递推记忆的结构性问题，并非本项目已测出的失败归因。现有工程源码尚未按以下方向更换，也没有本轮训练或测试结果。本轮是概念与数学诊断，不是完整原创方法选择、产品设计规格或可执行实验计划。

## 最值得聚焦的问题

**当前残差告诉模型“这个 key 的读出错了”，但仅凭这个残差，不能判断哪些旧关联已经过时、哪些关联还必须保留。**

两个解释性情形需要不同动作：

- 同一个事实真实变化：旧值应替换。
- 不同事实编码得相近：旧值应保留，新事实也应能访问。

神经网络产生 key/value/gate 的上下文可能帮助区分它们。因此不能说现有 Delta 模型绝对无法识别变化；这里的严格结论是：局部残差与数值 key 相似性本身不足以给出这种语义判断。若两个情形连所有可用输入、状态和条件都相同，任何仅依赖它们的确定性规则都不能选择不同动作。

## 三个不同的失效机制

统一采用 \(S\in\mathbb R^{d_k\times d_v}\)，读出 \(S^\top q\)：

\[
\bar S_t=D_tS_{t-1},\quad e_t=v_t-\bar S_t^\top k_t,\quad
S_t=\bar S_t+\beta_t k_te_t^\top.
\]

### 1. 写入干扰：纠正一个关联会影响其他查询

相对于衰减后的状态：

\[
\Delta o(q)=\beta_t(q^\top k_t)e_t.
\]

只要 \(q\) 与当前 \(k_t\) 重叠，该查询就会改变。是否有益取决于它原来的误差方向；并非所有改变都是破坏。缩小 \(\beta_t\) 会同时缩小纠错与干扰，无法单独识别应该保护的关联。

Gated DeltaNet-2 将 erase/write 解耦，但其 active edit 仍沿 \(k_t\) 写入。由原文 Eq.10 推得，对其他查询的变化仍含 \(q^\top k_t\)；它不提供所有旧查询保持不变的保证。这里是从公式作出的推断，不是作者已验证的普遍失败结论。

### 2. 长期保留：稳定的状态仍可能忘记信息

冻结所有输入特征，写成：

\[
S_t=A_tS_{t-1}+B_t,\quad
A_t=(I-\beta_tk_tk_t^\top)D_t,\quad
B_t=\beta_tk_tv_t^\top.
\]

第 \(i\) 次加性写入在时刻 \(t\) 的展开贡献为：

\[
A_tA_{t-1}\cdots A_{i+1}B_i.
\]

对于单位 key、\(0\le\beta_t\le2\)、\(\|D_t\|_2\le1\)，每步转换不放大范数；但 **不放大不等于保留**。若 \(D_t=\alpha I\)、\(0<\alpha<1\)，贡献范数至多为
\(\alpha^{t-i}\|B_i\|_F\)。即使没有全局 decay，后续相似 key 的纠错也可以擦除相同方向的旧关联。

这是冻结特征后的精确展开。深层网络特征随状态变化、生成路径改变或加入非线性转换时，不能把同一矩阵乘积当作完整网络 Jacobian。距离本身也不是唯一因素：中间写入的方向、强度和遗忘同样重要。

### 3. 容量与可辨识性：再好的更新也不能无条件容纳所有信息

固定 key 与线性读出，多个查询要求：

\[
Q^\top S=V.
\]

若 \(Q\) 的列之间线性相关，目标 \(V\) 必须满足相应关系；任意指定的多个 value 不一定可同时拟合。特别是相同 query/key 若需要不同答案，单一线性映射不能区分它们；必须引入不同的地址、上下文或任务条件。

有限精度边界更一般：若状态有 \(P\) 个数、每个可用 \(b\) bits，则最多有 \(2^{Pb}\) 个可辨识编码。无损保留 \(n\) 个独立、各有 \(V_0\) 类可能值的事实，以便任意查询，至少要求：

\[
n\log_2V_0\le Pb.
\]

这是固定精度、任意无损恢复的计数边界；不能由实向量维数直接断言有限信息量，也不能据此说整个非线性语言模型最多记 \(d_k\) 个事实。

## 三条同一 Delta 主线内的研究 lead

它们是针对不同缺点的可分析位点，不是三套已选择的新架构，更没有“全新”的结论。

### A. 识别并释放仍有预测价值的保护方向：当前优先调查

**问题：**写入时，应当保护哪些查询的答案？发生真实变化时，如何释放保护，而不把过时信息锁死？

先用一个已知几何构造定位困难。设 \(U\) 的正交列张成要保护的 query 子空间，\(P_U=I-UU^\top\)。求最小改动：

\[
\min_\Delta\|\Delta\|_F^2,\qquad
\Delta^\top k=\gamma e,\qquad \Delta^\top U=0.
\]

保护约束要求每一列 \(\Delta\) 都位于 \(U\) 的正交补。于是修正约束只依赖 \(P_Uk\)。对每个 value 坐标，Cauchy–Schwarz 给出最小范数解；当 \(P_Uk\ne0\) 时：

\[
\Delta=\gamma\frac{P_Uk}{k^\top P_Uk}e^\top.
\]

因此当前残差成为 \((1-\gamma)e\)，受保护方向的输出完全不变，并且

\[
\|\Delta\|_F
=\frac{|\gamma|\|e\|}{\|P_Uk\|}.
\]

后一个式子揭示代价：新方向越接近保护子空间，纠错所需修改越大；若 \(P_Uk=0\)、\(\gamma e\ne0\)，两类要求不可兼得。

**由推导产生的调查位点：**重要问题不是再写一个投影公式，而是从因果可用信息中选择、更新和释放 \(U\)，区分仍有效的旧知识与应被修订的关联。软 query 风险度量也属于预条件几何，不能单凭它命名原创。

**条件预测：**保护方向选择正确时，近 key 的新事实应较少破坏有效旧关联；真实事实变更仍能快速适应。

**反证：**过时关联被锁住；普通预条件 Delta 达到相同效果；收益仅来自小步长、更大状态或额外监督。具体如何因果估计保护价值仍未完成，不是可直接实现的合格候选。

### B. 根据预测损伤决定是否写入长期状态

**问题：**哪些更新值得承受长期覆盖风险？慢状态不应只按固定次数提交，也不应把所有新信息等价吸收。

可用一个带保护的 ridge 诊断来连接纠错收益和剩余方向。设慢状态 \(S^{\rm slow}\) 与保护子空间 \(U\)，令 \(e=v-S^{{\rm slow}\top}k\)，求：

\[
\min_\Delta
\|\Delta^\top k-e\|^2+\lambda\|\Delta\|_F^2,\qquad
U^\top\Delta=0,\quad\lambda>0.
\]

令 \(k_\perp=P_Uk\)，在正交补上求一阶条件可得：

\[
\Delta=\frac{k_\perp e^\top}{\lambda+\|k_\perp\|^2},\qquad
e_{\rm after}=\frac{\lambda}{\lambda+\|k_\perp\|^2}e.
\]

它既保护指定读出，也说明可用方向不足时纠错收益变小。可调查的提交规则应考虑这样的收益与未来预测损伤，而非固定每四步提交。

**限制与反证：**保护满整个空间会阻止所有新写入；只依赖当前误差不能识别长期价值；双状态、慢门和正交更新各有先例。若收益完全由更慢 decay 或额外状态容量解释，则没有新的提交机制贡献。此处不采用双状态为最终架构。

### C. 根据冲突分配地址与有限容量

**问题：**识别到保护与纠错不可兼得时，是否应分配不同地址，而不是在同一位置继续覆盖？

数学动机来自相同 query 无法同时映射到两个不同 value，以及 A 中 \(P_Uk=0\) 的不可行边界。一个可能的实现线索是带冲突信号的稀疏分区：写入路由 \(w\)，读取路由 \(r\)。忽略分区内遗忘，多个状态的 active edit 对读出的影响形如：

\[
\Delta o(q)=\sum_a r_a\,\beta_a(q_a^\top k_a)e_a.
\]

不相交的读写分区可隔离该次 active edit，但前提是路由确实区分应共存的关联；错误路由仍会丢失或混合信息。

**限制与反证：**路由不创造无限容量；总状态、地址元数据和路由计算均需计费。简单增加 slots、sparse addressing 已有直接方法。固定总状态预算后若不能优于既有稀疏 Delta，或者收益全由更大存储解释，就不能主张新的容量分配原则。因果冲突判别与分配规则未完成。

## 已有工作覆盖与本轮阅读范围

| 一手工作 | 已覆盖内容与准确边界 |
|---|---|
| Preconditioned DeltaNet 2604.21100v1 | 阅读 §3.1–3.3：分开 read/write key，以 inverse Gram 得到历史 ridge 解；实际近似模型使用对角统计与稳定参数化。近似后 exact 等价定理不再成立。不能把“加入协方差/预条件”称为新意。 |
| Gated DeltaNet-2 2605.22791v1 | 阅读 §3.1 Eq.8–10：channel-wise erase 与 write 解耦；erase 改 key 侧读取，write 改 value，左侧写入方向仍为 \(k\)。简单分开两个门不是新贡献。 |
| Gated KalmaNet 2511.21016v1 | 阅读 §3.2、§4.1、§7：Kalman 理论动机与实际实现须区分。实际维护 \(H_t,U_t\)，用有限次 Chebyshev 迭代近似解带 ridge 的 query 系统；不是每 token 显式 exact Kalman inverse update。 |
| Sparse Delta Memory 2607.07386v1 | 阅读 §3.1–3.3：显式 memory table 上稀疏地址读写及容量扩展。故多 slots/稀疏路由不是未有的框架。本文的 exact-dense-recovery 说法本轮未独立验证，不作为本项目推导依据。 |
| QED 2608.13668v1 | 已读取全文 Eq.6--15：query-derived 正交项并入同一 erase covector，左侧写入仍沿 key；它保持非平凡特征值但不保证 singular norm 或有序乘积稳定。2026-10-09 的公开检索未定位作者指定实现，因此公式审查已完成、代码接口仍 unavailable；见 `delta-discovery-2026-10-08/sources/QED_FULL_FORMULA_CODE_AUDIT_2026-10-09.md`。 |
| Kimi Linear 2510.26692v2 | 阅读 §7.1–7.2：作者讨论纯 linear attention 在精确复制和极长上下文细粒度检索的困难，以及混合设计。不能把它外推成 KDA 在所有长程任务都差。 |

本轮是定向缺点诊断与碰撞核查，不是穷尽检索或最终原创性裁决。独立分析来自 /root/arch_solver_memory、/root/arch_predictive_belief、/root/figure_dka_identify。三条 lead 的决定性新规则均尚未完成；历史候选池 1/0/0 不变。

## 决策

优先把科学问题聚焦为：

**Delta 如何因果识别应保留的关联，在真实变更时释放它，并在容量冲突时避免无依据覆盖？**

先调查 A 的保护与释放问题；B/C 是可能的后续实现路线，不预先叠加。Diffusion 可以辅助预测、训练或读出；普通远期 CE、教师监督和更简单预测器也必须保留为替代解释。是否采用 diffusion 由其不可替代的具体作用决定。

以上不表示“现有门没有上下文”或“新方法已解决语义判断”。下一步要导出具体因果可计算规则，完成最近工作逐项比对、预测与反证，再按既有数学与选择流程进入代码。

## 2026-10-09 补充否定边界

后续连续推导又排除了四个看似能补上 A/B 的捷径：双向 reciprocal cycle 在当前 pair 完全写入后成为恒等式，并不增加 revision/collision 身份信息；rank-revealing QR 只能判定线性约束是否相容，其最小改动式就是 hard protected projection，软化后回到 RLS/PDN；martingale/e-process 可以严格控制合法 pre-outcome change detector 的 anytime 误释放，却仍是标准 sequential detection 加已知 edit，不能区分同观测律的两个语义世界；任意 inverse-transported 时变 SPD metric 都能把物理衰减或爆炸重标成等距，若没有统一 coercivity 与双边 cross-time inequality，就不是 retention certificate。这四项分别保存为控制/no-go，不计入候选池；当前构造历史 5、活动 0、科学准入 0、选择 0。

同日再排除四个捷径：任意旧事件回滚在固定仿射路径上只是已发表的有序 receipt transport，真实删除会改变后续特征而要求 checkpoint+replay；集合值可行域是经典 set-membership/version-space，单凸近似不能保存 revision/coexistence 的离散分支；value-space 正交修正受 Gram/范数条件限制，其 exact key-local 形式与普通 full-step Delta 相同；`k⊗身份标签` 的 provenance lift 是 TPR/Fast Weight Memory 上的普通 Delta，一热标签就是 routed slots，唯一事件标签仍需索引。它们说明“保留不确定性、可逆、保范数、增加身份维”都不会自动产生新语义证据或新 recurrence；均保存为独立审查控制，不计候选。

再由三组双重数学审查排除三条参数/算子路线：冻结 token 的 exact gradient flow 与 implicit proximal 都精确退化为普通 Delta 的标量门，且分别被 EFLA、Longhorn 覆盖；`D^(1/2)` 对称分裂与 KDA 每步相似，修复同 key 读出后回到 PDN/GDN2 式预条件地址；标准 contractive Delta 的局部 Kreiss 常数恒为 1，时变产品则必须直接审查 ordered Jacobian/product、common Lyapunov 或 JSR。三者可作为数值和诊断基线，但不增加因果信息、身份或语义 release，因此不计候选。

## 一手来源

- <https://arxiv.org/html/2604.21100v1>
- <https://arxiv.org/html/2605.22791v1>
- <https://arxiv.org/html/2511.21016v1>
- <https://arxiv.org/html/2607.07386v1>
- <https://arxiv.org/abs/2608.13668>
- <https://arxiv.org/html/2510.26692v2>

