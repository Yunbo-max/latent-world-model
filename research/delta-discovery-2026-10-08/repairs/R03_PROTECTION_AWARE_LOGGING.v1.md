# R03 v1 — 保护感知的 Delta 随机动作日志

状态：数学修复稿；R02 的 versioned child。它给出一个可核查的单步旧查询损伤证书，并把该证书与随机动作日志的方差直接耦合。它不是实验结果，也不自动成为新候选。

## 1. 原问题、失败步骤与 patch

R02 通过在训练/评估期随机选择写入动作并记录 propensity，修复了“只观察一次实际写入却推断未写入反事实”的不可识别性。但任意保持 positivity 的随机探索都会故意执行潜在有害写入；仅用平均未来损失训练行为策略，没有给仍有效旧查询任何显式保护。

失败类型是目标/构造不匹配，而不是 R02 的 AIPW 代数错误：因果可识别要求每个待评估动作获得正概率，旧知识保护又要求危险写入概率足够小。R03 的 patch 是让同一个行为概率同时进入：

1. AIPW/DR 的逆 propensity 方差；
2. 由 Delta rank-one 写入几何推出的旧查询损伤预算。

因此策略不是“独立 Bayes gate + 平均 metric”，而是求解一个受保护损伤约束的实验设计问题。动作、损伤证书和 propensity 都只能使用决策前可见信息。

## 2. Formal object 与可见信息

在历史 \(H\) 下，以 post-decay 状态 \(\bar S=DS\) 为基准，令

\[
e=v-\bar S^\top k,\qquad
S^{a}=\bar S+\alpha_a\beta k e^\top,
\]

其中有限动作集 \(a\in\mathcal A\) 的缩放 \(\alpha_a\) 已在决策前固定；二元控制是 \(\alpha_0=0,\alpha_1=1\)。行为策略为 \(A\sim\mu(\cdot\mid H)\)，且 \(\mu_a\ge\epsilon>0\)。动作后的真实有限时域损失 \(Y^a\) 与 R02 一样在共同 continuation policy 下定义。

保护对象不是“所有历史知识”，而是一个条件查询分布 \(Q_p(\cdot\mid H)\)，其查询二阶矩

\[
G_p(H)=\mathbb E[qq^\top\mid H,q\text{ 仍应受保护}]
\]

必须来自可审计的 replay/probe 集、外部有效性证据或有覆盖保证的估计器。当前 residual 本身不能辨认事实是否仍有效；若 \(G_p\) 不可识别，后述安全保证也不可识别。

## 3. 精确单步损伤、旧风险与有限动作证书

对任意保护查询，rank-one Delta 写入相对 \(\bar S\) 的输出改变为

\[
\Delta o_a(q)=(S^a-\bar S)^\top q
=\alpha_a\beta(q^\top k)e.
\]

给定 value-output 度量 \(M\succeq0\)，冻结单步 readout 的平方输出位移恰为

\[
\begin{aligned}
d_a(H)
&=\mathbb E_{q\sim Q_p}\|\Delta o_a(q)\|_M^2\\
&=\alpha_a^2\beta^2(e^\top Me)\,k^\top G_p(H)k.
\end{aligned}
\]

维度为：\(S\in\mathbb R^{d_k\times d_v}\)，\(k,q\in\mathbb R^{d_k}\)，\(e\in\mathbb R^{d_v}\)，故 \(k^\top G_pk\) 和 \(e^\top Me\) 都是标量。二元 write/no-write 时 \(d_0=0\)，\(d_1=\beta^2(e^\top Me)k^\top G_pk\)。

但输出位移不等于旧任务风险增量。若仍有效保护标签 \(y(q)\) 可见，令 \(r(q)=\bar S^\top q-y(q)\)、\(C_p=\mathbb E[q r(q)^\top M]\)，则平方保护风险满足精确式

\[
R_p(\bar S+\Delta S_a)-R_p(\bar S)
=2\alpha_a\beta k^\top C_pe+d_a.
\]

因此仅约束 \(d_a\) 不能无条件保证旧损失不升：交叉项可为正且任意大。若另有可审计界 \(R_p(\bar S)\le\rho\)，Cauchy--Schwarz 给出

\[
\Delta R_{p,a}\le 2\sqrt{\rho d_a}+d_a.
\]

故使 \(d_a\le(\sqrt{\rho+B}-\sqrt\rho)^2\) 是 \(\Delta R_{p,a}\le B\) 的充分条件。标签是否仍有效仍需额外证据；几何本身不能回答。上述量也不是 CE 损失或完整未来网络损伤；传播到 nonlinear continuation 必须加入真实状态 Jacobian 与 loss 曲率/Lipschitz 条件。

若 simultaneous upper certificate \(U_a(H)\ge d_a(H)\) 以至少 \(1-\delta\) 的概率成立，则约束

\[
\sum_a\mu_a(H)U_a(H)\le b(H)
\]

在该事件上保证本次随机动作的**条件期望单步输出位移**至多 \(b(H)\)。它不是 realized-damage、全时累计、事实正确性或长期保留保证。

## 4. 二元闭式解：方差与保护的必要耦合

对独立/reset 的单决策单位，记结果噪声方差为 \(\sigma_a^2(H)=\operatorname{Var}(Y^a\mid H)\)。若 outcome model 对本次 outcome 固定/可预测，令 \(\delta_a=m_a-\widehat m_a\)，则线性 contrast \(\sum_aw_am_a\) 的 AIPW 条件方差中随 propensity 变化的部分为

\[
\sum_a\frac{g_a}{\mu_a},\qquad g_a=w_a^2(\sigma_a^2+\delta_a^2).
\]

余下的 \(-(\sum_aw_a\delta_a)^2\) 与 \(\mu\) 无关。二元且 outcome model 正确时，write/no-write effect 的可变部分为

\[
V(p)=\frac{\sigma_1^2}{p}+\frac{\sigma_0^2}{1-p},
\qquad p=\Pr(A=1\mid H),
\]

当 \(\sigma_0+\sigma_1>0\) 时，无约束极小点为 \(p_N=\sigma_1/(\sigma_0+\sigma_1)\)；若二者都为零，则 \(V\equiv0\)，所有可行 \(p\) 都最优，后述唯一性不适用。保护与 positivity 给出

\[
pU_1\le b,\qquad \epsilon\le p\le1-\epsilon.
\]

定义

\[
u=\begin{cases}
1-\epsilon,&U_1=0,\\
\min\{1-\epsilon,b/U_1\},&U_1>0.
\end{cases}
\]

当 \(\sigma_0+\sigma_1>0\) 时，\(V\) 在 \((0,1)\) 严格凸；若且仅若 \(u\ge\epsilon\) 时问题可行，并且唯一最优解为

\[
p^*=\Pi_{[\epsilon,u]}(p_N).
\]

若 \(b<\epsilon U_1\)，严格 positivity 与当前损伤预算不可能同时满足。此时只能放松 estimand/positivity、增加保护证据以收紧证书、改变动作集（例如更小 \(\alpha\)），或停止探索；不能宣称既安全又可识别。若约束把 \(p_N\) 截断，则精确方差代价为

\[
V(p)-V(p_N)=\frac{[\sigma_1(1-p)-\sigma_0p]^2}{p(1-p)}\ge0.
\]

若基准动作也有成本 \(U_0\neq0\)，约束应为 \((1-p)U_0+pU_1\le b\)，可行区间按 \(U_1-U_0\) 的符号求交，不能继续使用 \(pU_1\le b\)。

## 5. 多动作 KKT 形式

对有限 \(K\) 个动作，求解

\[
\min_{\mu}\ J(\mu)=\sum_a\frac{g_a}{\mu_a}
\quad\text{s.t.}\quad
\sum_a\mu_a=1,\ \mu_a\ge\epsilon,\ \sum_a\mu_aU_a\le b.
\]

忽略暂不活跃的下界，Lagrangian 一阶条件给出

\[
-\frac{g_a}{\mu_a^2}+\lambda+\eta U_a=0,
\qquad
\mu_a^*=\sqrt{\frac{g_a}{\lambda+\eta U_a}},\quad\eta\ge0.
\]

\(\lambda,\eta\) 使总概率和损伤约束成立；触及 \(\epsilon\) 的动作进入 active set 后重新求解。多动作问题可行当且仅当 \(K\epsilon\le1\) 且

\[
b\ge\epsilon\sum_aU_a+(1-K\epsilon)\min_aU_a.
\]

若存在 \(U_0=0\) 的 no-write，这变为 \(b\ge\epsilon\sum_{a\ne0}U_a\)。该形式说明高方差动作需要更多样本，而高损伤动作被系统性降权；但它本质上是通用 constrained optimal design，Delta 的专属部分只在可低成本计算的 \(U_a\)。

## 6. 旧反例复查与新增反例

R02 的旧反例都仍成立：

- 随机化只识别总体 action value，不识别单个历史写入的个体反事实；
- 后续策略不同需要顺序 DR，长乘积 propensity 仍可爆方差；
- overlapping persistent stream 不能伪装成独立行；
- 有限 horizon 不证明无限期收益。

R03 新增边界：

1. **保护集合不可识别。** 两个世界有相同可见 \(H,k,e\) 与 probe 输出，但“仍有效查询”集合不同，则可有相同估计 \(\widehat G_p\) 和不同真实 \(d_a\)。
2. **稀有方向遗漏。** 平均二阶矩可使罕见但关键方向损伤被稀释；若要求 worst-case，必须对审计集合取上确界或使用谱界，通常更保守。
3. **一阶/单步错配。** \(d_a=0\) 只说明当前保护 readout 对该写入正交，不排除写入改变后续 key、gate 或 updater state 后造成损伤。
4. **positivity 不可行。** \(b<\epsilon U_1\) 时不存在二元行为策略；删除这个条件会把不可行问题伪装成算法。
5. **估计证书失配。** 若 \(U_a\) 不是 simultaneous upper bound，plug-in \(\widehat G_p\) 低估会直接破坏安全结论。
6. **安全但不学习。** 令 \(b=0\) 或证书极松可把所有非基准动作概率压到最低，保持某种保护却没有足够统计功效或更新收益。

## 7. 可计算构造、信息与成本

精确稠密 \(G_p\) 需要 \(O(d_k^2)\) 状态，计算 \(k^\top G_pk\) 为 \(O(d_k^2)\)。低秩 probe 矩阵 \(Q=[q_1,\ldots,q_r]\) 可用

\[
k^\top\widehat G_pk=\frac1r\|Q^\top k\|^2
\]

降到 \(O(rd_k)\)，但只覆盖该 probe 分布；sketch 误差必须进入 \(U_a\)。若仅知 \(\|q\|\le Q_{\max}\)，则

\[
d_a\le \alpha_a^2\beta^2(e^\top Me)\|k\|^2Q_{\max}^2,
\]

这是可审计但常过度保守的 fallback。

除 \(G_p\) 外还需预测/估计 \(\sigma_a\)，记录精确 \(\mu_a\)，并用真实延迟结果训练或评估。为了给整个时间轴高概率保证，需要 anytime/union control 和依赖处理；单步 \(1-\delta\) 证书不能直接相乘成长期保证。

一个具体的有限样本证书是：若独立保护查询上

\[
Z_{aj}=\|\Delta S_a^\top q_j\|_M^2\in[0,B_a],
\]

且 \(K\) 个动作在取样前固定，则 Hoeffding + union bound 给出同时概率至少 \(1-\zeta\) 的

\[
U_a=\widehat d_a+B_a\sqrt{\frac{\log(K/\zeta)}{2n}}\ge d_a.
\]

若动作由同一数据生成，必须使用独立样本、覆盖整个动作类的统一界或 anytime confidence sequence，普通事后 union bound 无效。另一种写法是：若 \(\|G_p-\widehat G_p\|_{\rm op}\le r_G\)，则

\[
U_a=\alpha_a^2\beta^2(e^\top Me)
\{k^\top\widehat G_pk+r_G\|k\|^2\}.
\]

若允许 \(\gamma\in[0,1]\) 缩放同一写入，冻结二次位移满足 \(d(\gamma)=\gamma^2d(1)\)，所以 \(\gamma\le\sqrt{b/U_1}\) 是局部期望位移的安全域。这条 star-convex 路径是可计算控制，不代表多步语义安全。

在冻结未来特征且相同外生输入下，若 \(\Delta S_{i+h}=P_{i+h:i}\Delta S_a\)，未来矩可精确写为

\[
d_{a,h}=\operatorname{tr}\!\left(
M_h\Delta S_a^\top P_{i+h:i}^\top G_{p,h}P_{i+h:i}\Delta S_a
\right).
\]

完整网络中 action 会改变未来 key、query、gate、updater state 和 token trajectory；此时只能对联合扰动 \(\delta z_a\) 使用真实 \(J_{h:i}\)。若 Jacobian 在相关邻域为 \(L_h\)-Lipschitz，则

\[
\|g_h(z+\delta z_a)-g_h(z)\|
\le\|J_{h:i}\delta z_a\|+\tfrac12L_h\|\delta z_a\|^2.
\]

计算或界定完整 \(J\) 可能消除 rank-one 证书的廉价优势；R02 的随机 delayed outcome 仍可识别总效果，但不能据此事前保证全轨迹安全。

## 8. 同信息强对照、最近工作差异与测量缺口

强对照包括：固定 \(\epsilon\)-greedy、无保护的 clipped Neyman allocation、no-write、安全基准策略、硬保护投影/soft preconditioner、CLUCB、SEA、高概率/期望 stage-wise constrained bandits、普通 AIPW/DR/SWITCH，以及同资源 outcome model。

SEPEC 与 Safe Optimal Design 已直接覆盖“安全且方差/信息高效的 logging policy”；其他最近工作还覆盖相对安全基线保守探索、部署前高置信 OPE、逐轮成本约束和约束策略线性规划。因此受损伤预算约束的 propensity 优化本身不能作为新方法。R03 的窄 Delta 特化是：rank-one 写入让指定保护查询分布的单步平方输出位移化为标量 \(\alpha_a^2\beta^2(e^\top Me)k^\top G_pk\)，并给出旧平方风险交叉项/充分界，从而显式显示保护预算与 causal overlap 的不可行边界。

LongMemEval 的 knowledge-update 项和 SEAL 的连续 self-edit forgetting 结果可观察终点更新/遗忘，但它们都不原生提供：随机 Delta 动作 propensity、决策时的真实仍有效保护分布、该单步证书或 matched-budget action-effect scorer。因此自然机制测量仍有 gap；没有发明新标签、指标或结果。

## 9. 可证伪预测与 disposition

若该控制有用，则在相同动作集、propensity 下界、样本数与总计算下：

1. 当 \(k^\top G_pk\) 上升时，最优 write 概率应按 \(b/U_1\) 截断，而不是只由预测收益决定；
2. 观测到的平均单步保护输出损伤应不超过预算（仅在证书覆盖事件和目标查询分布内）；
3. 相比固定 epsilon，AIPW 方差可降低，但当保护约束活跃时会高于无约束 Neyman 下界；
4. 若 full-Jacobian 长期损伤与单步证书无关，则该控制只能保护局部 readout，必须判负其长期主张。

结论：R03 v1 在明示条件下数学成立，且确实修复了 R02 “可识别但无旧查询损伤预算”的缺口；但核心优化与 safe/constrained contextual bandit、optimal design 已发生机制碰撞。当前只保留为 **Delta 特化安全日志控制/理论边界**，一次修订后 park，不分配 D 编号，不增加 active/scientific-admitted/selected 计数。重新开启 R03 v2 要求证明同预算下相对 SEPEC/Safe Optimal Design 或硬保护基线的 Delta-specific 统计/计算优势，或把证书扩展为可合法估计的完整 coupled-state 长期损伤并有原生可测量对象。

本稿未执行项目代码、软件测试、模型训练、推理、评分、数据/模型下载、GPU 作业或 Docker。
