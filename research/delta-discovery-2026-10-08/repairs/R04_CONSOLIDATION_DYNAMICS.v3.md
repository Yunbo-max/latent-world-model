# R04 v3 — 可表示 Delta 巩固的联合收益—损伤判据

状态：R04 lineage 第三次、也是当前上限内最后一次实质数学修订；条件理论/可计算 control，**未计 D 候选、未证明原创方法、未产生实验结果**。父文件 `R04_CONSOLIDATION_DYNAMICS.v2.md` 及其非均匀衰减反例、review 和字节全部保留。本稿只修复 v2 留下的最早缺口：在相同状态/信息/计算预算下，什么可表示分量 `C` 值得由快状态迁入慢状态。若本稿仍不能闭合重要性、最近工作差异和原生测量，R04 按三次修订预算 park；重开需要新的外部证据或不同数学对象，不能再换 loss 名称。

## 1. 原问题、确切缺口与 patch

v2 已经证明两件不能混淆的事：完整 affine compensation 只是单状态 Delta 的冗余坐标；“总残差 + 仅快衰减”则真正引入

\[
\delta W_T=\sum_{j=1}^{T}P_{T:j+1}E_j(I-D_j)C.\tag{1}
\]

它没有给出 `C` 的合法选择器。原缺口不是式(1)错误，而是**目标/构造不匹配**：仅说“可靠、重要或可迁移”既没有把未来收益与仍有效旧查询损伤放进同一风险，也没有约束慢参数实际能表示什么。patch 为：

1. 把慢端增加和快端删除写成两个显式线性接口，先推导近似表示误差；
2. 将 v2 的 differential-decay 传播拉回到可执行低维控制 `z`；
3. 对真实未来目标的联合条件风险求解，而不是用独立有效性 gate 乘平均 metric；
4. 给出均匀衰减下的“有效性概率必须超过快记忆自然存活率”阈值，并用 still-valid / obsolete 两个旧反例复查；
5. 分离预测风险可估计性、事实有效性可辨识性、保护约束和 generic ridge/直接 action predictor 的已知部分。

## 2. Formal object、信息与可表示接口

沿用 v2 的加性 key-by-value 子模型 `W=M+S\in\mathbb R^{d\times m}`，查询输出 `o(q)=W^T q`。冻结同一未来外部路径时

\[
E_t=I-\beta_t k_tk_t^T,\quad A_t=E_tD_t,\quad
P_{T:j+1}=A_T\cdots A_{j+1},
\]

并定义左作用的巩固传播算子

\[
R_T:=\sum_{j=1}^{T}P_{T:j+1}E_j(I-D_j).\tag{2}

\]

控制 `z\in\mathbb R^p` 由决定时刻的因果过滤 `F` 产生。采用按列堆叠的 `vec` 约定；慢端可实现增加和快端删除分别为

\[
\operatorname{vec}(C_s)=B_s z,\qquad
\operatorname{vec}(C_f)=B_f z,
\]

其中 `B_s,B_f` 是声明的可实现接口，不是免费满宽矩阵。慢参数为非线性 `theta` 时，`B_s` 只能是明确工作点的 Jacobian/局部表示；有限修改需要实际函数差而不能直接写 `theta+=C`。固定预算比较必须计入 `p`、预测 moment 的状态、慢/快两端和求解成本。

由 v2 式(10)，未来总状态差的向量形式是

\[
t_T(z)=\{(I_m\otimes P_{T:1})(B_s-B_f)+(I_m\otimes R_T)B_s\}z=:T_Tz.\tag{3}

当前读出完全保持要求 `(B_s-B_f)z=0`。若接口在所选子空间精确匹配，令 `B_s=B_f=B`，则

\[
T_T=(I_m\otimes R_T)B.\tag{4}

若不能匹配，第一项是立即表示误差，不得用后续“慢保留”抵消后宣称无损迁移。冻结路径只在两条比较路径具有相同 `A_t,k_t,q_t` 时精确；完整闭环需要把所有状态、路由、更新器和生成分布的 Jacobian/score 项纳入，不能把(3)当全模型有限修改定理。

## 3. 未来输出风险的精确有限维解

令索引 `i` 同时表示合法未来时刻、查询和任务；基线不巩固输出为 `o_i^0`，真实监督目标为 `y_i`，残差 `r_i=o_i^0-y_i\in\mathbb R^m`，输出权重 `Q_i\succeq0`。条件于 `\mathcal F`，联合 law `(i,L_i,r_i,Q_i)` 被固定且不随所比较的 `z` 改变，相关二阶矩有限；若动作改变未来查询/反馈 law，以下只是 frozen-law surrogate。令

\[
L_i=(I_m\otimes q_i^T)T_i,\qquad \delta o_i=L_i z.
\]

考虑相对零巩固的条件风险

\[
\Delta\mathcal J(z\mid\mathcal F)
=\mathbb E[\|r_i+L_i z\|_{Q_i}^2-\|r_i\|_{Q_i}^2\mid\mathcal F]
+\lambda z^T H_0z.\tag{5}

\]

其中 `\lambda>0,H_0\succ0` 是明确的控制/资源正则。定义**联合**充分矩

\[
G=\mathbb E[L_i^TQ_iL_i\mid\mathcal F],\qquad
g=\mathbb E[L_i^TQ_i r_i\mid\mathcal F],\qquad
K=G+\lambda H_0.\tag{6}

展开得

\[
\Delta\mathcal J(z)=z^TKz+2g^Tz,
\]

故唯一最优控制和相对零动作的最优改变量为

\[
\boxed{z_*=-K^{-1}g},\qquad
\boxed{\Delta\mathcal J(z_*)=-g^TK^{-1}g}.\tag{7}

这一步是普通受限 ridge/二次决策的正常方程，**不宣称新定理**。Delta 特化在 `L_i`：它同时含实际 `P` 顺序、`E(I-D)`、查询和可表示接口。把有效性概率、平均查询 metric、平均存活率分别预测后相乘，一般不能恢复 `g` 或 `G`；需要其联合 law。若 `D_t=I` 且接口精确匹配，(2)给 `R_T=0`，于是 `L_i=0,G=g=0,z_*=0`。此时仅搬移不可能通过本机制改变冻结未来轨迹；任何收益必须来自额外容量、近似误差、有限精度、其它隐态或改变的闭环 law。

若有必须保持的已知保护输出，写线性约束 `Az=0`，令 `N` 的列为 `ker(A)` 的正交规范基。则

\[
z_{\rm prot}=-N(N^TKN)^{-1}N^Tg.\tag{8}

只有 `N^Tg\ne0` 才有非零的一阶/二次风险收益；若收益梯度完全落在被保护方向，硬保护下零动作最优。近病态 `N^TKN` 会放大范数和估计误差。保护标签或可信目标本身是额外信息；未知旧知识是否仍有效时，不能把(8)当免费 oracle。soft protection 只应作为(5)联合未来样本的一部分，不能独立 gate 后再平均。

## 4. Delta 快慢子模型中的 survival-matched 阈值

取可核查标量特例：无后续写入 `\beta_t=0`，均匀快衰减 `D_t=\alpha I,0\le\alpha<1`，一个现有快记忆值为 `c\ne0`，允许迁移比例 `z\in[0,1]`。令 `s=\alpha^T` 是该分量在 horizon `T` 的自然存活率。未巩固输出为 `o^0=sc`，迁移的额外输出为 `(1-s)cz`。令 `U\in\{0,1\}` 表示未来目标是 still-valid 的 `c` 还是 obsolete 的 `0`，`p=\Pr(U=1\mid\mathcal F)`。带 `\lambda z^2` 的风险导数给

\[
z_{\rm unc}
=\frac{(1-s)c^2(p-s)}{(1-s)^2c^2+\lambda},\qquad
z_*=\operatorname{clip}_{[0,1]}(z_{\rm unc}).\tag{9}

因此正迁移的精确阈值是

\[
\boxed{p>s=\alpha^T}.\tag{10}

`p=s` 时零迁移在有正则时唯一最优；`p<s` 时受限最优为零。无正则且 `p=1` 时 `z*=1`，完整保留仍有效信息；`p=0` 时最优不迁移，让快记忆继续衰减。这个结果把“置信度高就巩固”修正成**置信度必须超过当前 horizon 下不做巩固仍会保留的比例**。更慢的自然衰减提高阈值；更长 horizon 降低 `s`，使相同 `p` 更愿意巩固。它是模型内条件预测，不是已测事实。

多 horizon/查询时不能用单一 `p`。在同一标量分量、非负权重 `w_i\ge0` 下，正迁移需要

\[
\mathbb E[w_i(1-s_i)U_i\mid F]
>\mathbb E[w_i(1-s_i)s_i\mid F].\tag{11}

若有效性与 horizon、查询重要性或衰减相关，`E[U]` 与平均 metric/平均 `s` 的乘积会给错决定；这正是 joint conditional risk 的残余，而不是 Bayes gate 的换名。

## 5. 旧反例复查与不可辨识边界

v2 的 still-valid/obsolete 两世界在(9)下不再只是口头边界：两世界可有完全相同的前缀 `F`、当前 `c` 和 Delta 几何。无正则纯预测风险时它们分别要求 `z=1` 与 `z=0`；`\lambda>0` 时分别要求正的 shrinkage 解与零，仍不存在同时最优的单一动作。若部署前看不到能改变 `p` 的外部证据，任何确定策略至少在一个世界次优；几何本身不识别事实有效性。模型自评、自生成未来或当前 residual 不是新外部证据。

离线训练可以用**后来真实到达的 token/任务反馈**估计(5)的预测风险，因为 `y_i` 只进入 loss；部署时只能由 `F` 预测 `G,g` 或直接预测 `z_*`。这闭合的是条件预测决策，不保证某条具体事实在未来永远有效。若行为策略影响未来文本、查询或反馈到达，(5)的固定 law 不再是总因果效应；需要合法随机化/overlap、sequential exchangeability 或完整参数依赖 rollout 导数。事实日志只含已采取巩固动作时，不能同时识别“巩固/不巩固”的潜在未来损失。

一个前缀通常只有一条未来轨迹；样本矩只是总体估计问题。若对同一条件分布有合法样本，`L_i^TQ_iL_i` 与 `L_i^TQ_i r_i` 的样本均值分别无偏；条件预测、截断 horizon、冻结特征和近似 solve 会增加估计/逼近/优化误差。完整 conditional diffusion 在二次对象(5)下没有必要性：`G,g` 已是决策充分矩；只有非二次、chance constraint、多模态动作或其它分布性目标才需要超出这些矩的信息，而且仍需同样合法监督。

## 6. 计算、强简单替代与实际可实现性

完整 `p` 维 `G` 需 `O(p^2)` 状态、稠密解 `O(p^3)`；大状态必须用低秩/对角/迭代近似并记其方向误差。形成 `L_i` 需要 v2 的冻结有序传播；真实网络需完整 JVP/VJP、激活保存/重算或合法 critic。预测这些 moments 的网络、旧任务回放、真实未来反馈、慢参数和求解器都计入相同总预算。

最强同信息替代包括：

1. 直接预测 `z_*(F)` 的普通 action predictor 或远期 CE；在可表示性足够时 population Bayes 动作相同，moment 形式只能凭结构共享、PSD/约束或统计/计算效率取胜；
2. 固定预算单状态 Delta、普通较慢 decay/write-rate、已知快慢总残差；`D=I` 是必要 no-effect control；
3. hard projection/soft preconditioning、EWC/GEM/A-GEM/OGD 和适用的 SFT/LoRA+replay/distillation；
4. HOPE/CMS、Sleep consolidation、SynControl、SEAL 与同容量 learned updater；新增原文、容量、付费 judge 或更多反馈不能算本构造自身收益。

本稿的可计算 construction 是 `(2)-(8)`，但 generic normal equation 和 selective consolidation 都已有强近邻。要把它升级成方法候选，必须证明在相同合法监督和总成本下，Delta 传播结构使 moment 估计/solve 有实际可验证优势，或给出最近工作没有的自然任务后果；仅实现(7)不够。

## 7. 区别性预测、falsifier 与原生测量

条件预测：

1. exact representable、冻结路径、`D=I` 时，任何 R04 Patch-B 迁移效应都应为零；非零结果 falsify 当前等价条件或表明存在未计状态/资源差。
2. 均匀衰减标量控制中，迁移开关应在 `p=alpha^T` 变号；若同一目标/信息/成本下系统性不符，式(9)的风险、horizon 或实现映射错误。
3. 若独立 `p` gate 的因子化近似在正概率条件集合上改变 Bayes 动作，它应劣于 joint moment/direct action；仅有 `U` 与 `(q,T,D)` 相关但最优动作不变时，不应宣称必然收益。若 mixed moment 实际因子化，新增耦合也不应获益。
4. representability mismatch 的影响含 `(B_s-B_f)` 立即项；只报告蒸馏当下误差而忽略其后续 `P` 传播不足以支持长期保留。

这些是数学 falsifier，不是新造 benchmark。LongMemEval knowledge-update 可测更新后回答，但原生 judge 接受同时提及旧信息，且不暴露 `C,L_i,G,g`；SEAL 连续 self-edit 下三角矩阵可测参数级旧任务保持，却是 LoRA merge、默认多 GPU/付费 grader，非 Delta fast→slow 机制。bAbI/LAMBADA 只给 endpoint，不给有效性、潜在结果或 updater 学习效率。现有原生资产因此只能测部分行为端点，不能单独认证(10)、事实释放或 RSI；measurement gap 保留。本阶段没有下载、运行或评分。

## 8. 与最近工作差异及最终处置

来源/作者实现定位见 `sources/REPAIR_R04_V3_SELECTION_SOURCE_AUDIT.md`。已知覆盖包括：快慢权重和 selective consolidation、SynControl 的总预测误差与慢/快耦合、HOPE/CMS 多频率自修改、两篇不同的同名 Sleep 工作、SEAL 连续参数 merge，以及联合 Bayes/weighted normal equation、APO/模型编辑的函数空间二次几何。2026-08 的 Dual-Layer Agentic Memory v2 还明确给出 cost-aware write routing、反事实写入奖励、selective slow consolidation 与遗忘 probe；本轮已读全文公式，但作者代码/数据仍未公开，不能把缺失实现写成已审查。

数学状态：`(3)-(11)` 在声明的线性/冻结/固定-law条件下是可复核的连续推导；贡献差异状态：把通用 survival 决策边界拉回 Delta differential-decay 接口是有价值的条件表述，但阈值本身并非 Delta 特有，generic decision principle 和 selective fast/slow consolidation也已知，尚未建立足够独立的新方法差异；实验状态：未知且未执行。

**处置：park R04 after bounded repair。** 保留 v1 错误、v2 修复和 v3 联合选择定理；不把此前分析说成“都错”，也不把局部修复自动升级为候选。R04 不增加活动/准入/选择计数。重开条件：针对 `(10)/(11)` 的实质最近工作空缺被全文/代码审查支持，并且存在同预算原生对象可判别 joint survival 几何；或新证据改变固定-law/可表示接口。下一条独立合法工作应转向其它最有希望 repair，而不是第四次改写 R04。
