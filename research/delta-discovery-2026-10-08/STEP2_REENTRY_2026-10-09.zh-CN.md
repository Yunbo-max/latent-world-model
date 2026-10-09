# 根据首轮发现重走第2步：Delta 数学问题再定位

日期：2026-10-09。来源 parent：057bc2abbf8b8510273cc4fb004e2063c5cc894c。
用户原话：“我觉得你继续做数学推导然后或者看看有没有其他的结合方式或推论可以优美的解决一些问题，根据这轮的发现去重走2”。
角色：web_supervisor；单一作者 /root。本文件是已做推导的研究笔记，不是候选准入、独立审查或实验结果。无项目执行。

## 方向修正

保留五张构造历史和全部否定记录，但当前活动候选仍为零。第2步重新定位问题，不能只不断扩大 rejected 清单，也不能把所有研究价值收缩到“产生新的身份语义证据”。

重点考察三个相连对象：完整网络的写入传播；修改有效性与查询几何的联合风险；实现这个风险所需的最小统计量。组合、表示、目标、计算和有价值理论均可成为贡献；必须有实质差别、必要交互及可证伪预测，不能由模块数量判定新意。以下四组结果复用链式法则、二次优化、条件期望和方差分解，数学工具本身已知，不将四个推论计为四个新模型。

旧 no-go 的假设决定其适用范围。改变信息、读出、状态或目标后需要重推，既不能直接套用旧否定，也不能称旧否定已被突破。

## 推论一：冻结路径与完整记忆传播的差，可以明确写出

### 对象和假设

S 是 key-by-value 状态。固定已经观察的外部输入 x，考虑可微映射
F_t(S)=A_t(S)S+B_t(S)。
A=(I-beta kk^T)D，B=beta k v^T。若 features 真正独立于这份状态，A、B 关于它的导数为零；不能因为 residual 包含 S 就误认为 A、B 也依赖 S。

对于多层网络，z 必须包含所有参与因果反馈的 recurrent states；只分析一份矩阵不能省略其他 state 的反馈。下式对局部矩阵 F 成立，全网络应用需改用完整 z 的 Jacobian。

### 实际推导

沿状态扰动 E 求方向导数：
J_t[E]=A_t E+(dA_t[E])S_(t-1)+dB_t[E]。

第一项是上一轮冻结特征 trace；后两项是 feature feedback，令 C_t=J_t-L_t，L_t[E]=A_tE。

对于起点 perturbation，完整的一阶传播为 J_T ... J_(i+1)E，而冻结传播为 L_T ... L_(i+1)E。精确算子差满足 telescoping：
J_T...J_(i+1)-L_T...L_(i+1)
= sum_(r=i+1)^T J_T...J_(r+1) C_r L_(r-1)...L_(i+1)。

因此误差范数至多
sum_r (product_(j=r+1)^T ||J_j||) ||C_r|| (product_(j=i+1)^(r-1) ||L_j||)。
空乘积为 identity。这个界没有保证小；即使每个反馈项较小，长 horizon 或放大乘积仍可累积。

最终读出若是 R(z_T,x)，真实输出一阶差还需乘 DR；若 query 自身依赖状态，DR 必须包含 query 的导数。完整 finite edit 不等于这个局部导数；需要二阶余项或真实 counterfactual replay。

### 独立代数路线（同一作者自检）

标量 s'=s+beta(s)(v-s)，e=v-s：
ds'/ds=1-beta(s)+beta'(s)e。
冻结系数得到的却是 1-beta。e=0 时反馈项消失；远离拟合点时反馈可增强或削弱敏感度。此例只验证链式法则和适用范围，不是自制 benchmark。

### 研究决定

R2-J 是问题线索：前一轮 frozen trace 什么时候足以代表完整 query-visible influence？是否存在可计算的误差控制或保持并行性的结构条件？
不能直接把“加入状态依赖 gate”“惩罚 Jacobian”“多层 Delta”当新方法：经典 recurrent FWP、DeltaTTT、TTT 和梯度传播方法均为强近邻。
可证伪预测：只有反馈项和读出敏感度都受控时，frozen norm 才能近似可读取影响；矩阵范数保留不保证事实有效。
复杂度：完整 Jacobian 的维度是全部状态维数；JVP/VJP 虽可避免显式矩阵，仍需要网络计算和跨时激活。无软件或成本验证。

## 推论二：修改有效性与查询几何相关时，最优结合不能分别平均

### 正式对象

当前可用前缀信息为 F。假设有一个条件随机的目标矩阵修改 Delta 和未来线性查询 q；本节只研究冻结、局部、二次的目标，不把它当完整 LM 的 CE 或真实事实标签。
G=qq^T，U 是只允许依赖 F 的当前矩阵 edit，lambda>0 为配置的 regularization。
L_F(U)=E[||q^T(U-Delta)||^2 | F]+lambda ||U||_F^2。
要求有关二阶矩有限、E[||q^T Delta||^2|F]有限。查询/目标不依赖所选择的 U；否则以下冻结优化不适用。

### 连续推导

定义 H=E[G|F]+lambda I，T=E[G Delta|F]。
展开：
L_F(U)=tr(U^T H U)-2tr(U^T T)+constant。
H 正定，梯度 2HU-2T，所以唯一最优解
U*=H^(-1)T。

配方得到精确 regret：
L_F(U)-L_F(U*)=tr((U-U*)^T H (U-U*)) >=0。

这不是 E[Delta|F] 与 E[G|F] 的任意组合：
T=E[G|F]E[Delta|F]+E[(G-EG)(Delta-EDelta)|F]。
遗漏的 matrix cross moment 才是本节有意义的交互对象。

### 二假设特例

令 Z∈{0,1}，p=P(Z=1|F)。目标 edit=Z k e^T；Z=1 表示该局部目标需要这个 edit，Z=0 表示不需要。该定义不是已经辨识的语义真值。
G_R=E[G|Z=1,F]，G_C=E[G|Z=0,F]。
于是
H=(1-p)G_C+pG_R+lambda I，
T=pG_R k e^T，
U*=[(1-p)G_C+pG_R+lambda I]^(-1)pG_R k e^T。

若先分别平均再相乘，会把 T 错替换为 p[(1-p)G_C+pG_R]k e^T。
两者差为 p(1-p)(G_R-G_C)k e^T。
p=0/1，或 G_R=G_C，或差恰好 annihilate k 时，该项消失。这些是成功特例，不是一般假设。

### 逻辑例子与可计算构造

取 p=1/2，k=(1,0)^T，
G_R=[[2,1],[1,2]]，G_C=[[2,-1],[-1,2]]。
两者 SPD，平均为 2I。lambda=0 时仍有唯一解：
U*=(1/2,1/4)^T e^T。
分别平均的方案为 (1/2,0)^T e^T；其风险多出 ||e||^2/8。
这里差别改变了方向，而非只换 gate 数值。这个矩阵例子是代数说明，不是科学评测。

形式构造是从前缀预测 PSD 平均 G 和 cross moment T，再解 H U=T。它在数学上可计算，但暂未成为可部署新方法：预测目标是否合法、近邻是否已覆盖、如何训练、低成本参数化均未闭合。G_R/G_C 不能靠未来答案在 inference 时直接取得，也不能把 Z 设成免费身份 oracle。
这里 rank-one 目标使 U*=u e^T；一般目标 T 不必低秩。

### 误差和代价

若预测 Hhat=H+E、That=T+N，且 ||E||<lambda，则
Uhat-U*=Hhat^(-1)(N-EU*)，
||Uhat-U*||_F <= (||N||_F+||E|| ||U*||_F)/(lambda-||E||)。
结合 regret 恒等式可界定估计误差的作用；小 lambda 会恶化条件数，不能仅追求更强 correction。

参考 full metric 的瞬态存储 O(d_k^2)，分解 O(d_k^3)，一般多 RHS solve 还需 O(d_k^2 d_v)。二假设 rank-one RHS 可降低 RHS 部分但不消除 factorization。低秩/对角近似需要单独误差分析，不算另一个候选。

### 研究决定

R2-C 是最值得补读的结合线索：语义/目标条件与 query relevance 是否有 consequential correlation？cross moment 能否由当前实际可用信息学习，并在相同信息/成本下超越 factorized baseline？
这属于经典条件 Bayes quadratic decision 的具体展开，不宣称原创。必须与 D01/D03、Bayesian Layers、KDN/GKA/PDN/QED、mixture-conditioned control 和 amortized optimization 比较实质功能；完整近邻/源码/测量审查仍 pending。
反证/淘汰条件：cross moment 为零、不可预测、相同信息的直接 CE 已等效学习、或者 solve/teacher 开销吞掉收益。强简单替代是直接预测 u 或 T，而不是默认需要 diffusion。

## 推论三：二次风险只需要条件矩，不能据此证明 diffusion 必要

前节的 decision 只需要 H 和 T；完整联合分布并非这个固定二次决策的必要输入。
因此若 diffusion 仅用于采样未来 (q,Delta)，其作用是估计同样的两个条件矩。公平替代是直接 conditional-moment regression 和同信息的普通 predictor。

设随机 edit Uxi 只依赖 F 和独立随机种子，给定 F 与真实未来 (q,Delta) 条件独立。记 m=E[Uxi|F]。展开 cross term 得：
E[L_F(Uxi)|F]=L_F(m)+E[tr((Uxi-m)^T H(Uxi-m))|F] >= L_F(m)。

随机执行一个采样出的 edit，在这个二次风险下不能胜过它的平均 edit。若 draw 与真实未来通过额外已观测证据耦合，条件信息集必须扩大，这不是原结论的反例。
平均 samplewise optimum E[Hxi^(-1)Txi|F] 也一般不等于 (EHxi)^(-1)ETxi；不能把先求逆再平均当作最优决策。

这个推论不否定 diffusion：
- 非线性 readout、离散选择或非二次风险可以依赖高阶/多峰结构，需要另行推导；
- diffusion 可能是更好的有限容量分布估计器，但要与同信息、同成本直接 predictor 比较；
- teacher 学到了训练总体规律，不等于为某条无可辨信息的历史创造额外证据。
不据此固定 diffusion 的轮数或推理步骤。没有建立它为主创新的必要性。

## 推论四：新增证据的收益，可以与单纯噪声分开

固定可由 F 得知的 PSD 度量 G，未知理想 edit Y 有有限二阶矩。二次风险下最优 edit 为 E[Y|F]（G 正定时唯一；半正定时 nullspace 不影响风险）。
额外真实可观察证据 E 到达后，令 mu_E=E[Y|F,E]，mu=E[Y|F]。
条件方差分解给出：
R_before(F)-E[R_after(F,E)|F]
=E[tr((mu_E-mu)^T G(mu_E-mu))|F] >=0。

证明：Y-mu=(Y-mu_E)+(mu_E-mu)，条件于 F,E 时第一项均值为零，交叉项消失。这个是新增证据的 Bayes risk value，并非每条 realized sample 的改善保证。
二假设 Y=Z e 且 e 由 F 得知时，收益为 Var(P(Z=1|F,E)|F) e^T G e。
若“新增证据”是由前缀和独立噪声生成的 hallucinated continuation，Y 与 E 给定 F 条件独立，那么 mu_E=mu，理想 Bayes 收益为零。训练好的模型参数应视为已经固定且属于 F 所采用模型；不能混淆总体先验学习和额外逐事件事实证据。

这说明 delayed evidence 有条件价值，而 random denoising 本身没有 information 增益。单步 posterior gate、change detector 仍是已有强基线。真正问题是合法可用信息及联合风险，而非增加采样次数。

## 来源核对与未闭事项

本次实际重新读取：
- DeltaTTT v1 的 arXiv abs 和 HTML §2、§4.1 Eqs5–12：<https://arxiv.org/html/2610.08553v1>。已确认两层 layerwise Delta，并没有将“非线性”本身当新候选。
- Recurrent FWP v2 的原始 PDF：<https://arxiv.org/pdf/2106.06295>，含 SlowNet 可依赖以往 fast states/outputs 的一般定义，以及作者代码链接 <https://github.com/IDSIA/recurrent-fwp>。本轮未读取该代码，不宣称 implementation audit 完成。
- MIRAS v1 HTML 的 Huber memory 段落：<https://arxiv.org/html/2504.13173v1>。误差 clipping/robust loss 已有直接近邻，不能作为独立新意。
- Memory by Design v4 abs：<https://arxiv.org/abs/2605.31163v4>，2026-10-07更新。此次 HTML/PDF 获取失败，故只记摘要邻居，全文和作者代码审查 pending。不从摘要判定 R2-C 已碰撞或已新颖。

源记录纠正：旧 sources/DELTATTT_FULL_AUDIT.md 将作者写为 Alex Cheng 等，不正确。当前 abs 和 HTML 均列 Yining Li、Dongchen Han、Jie Fu、Gao Huang。旧字节/审查绑定保留；本文件记录纠正，不据此重新认证旧审核的所有条目。

现有 measurement feasibility 记录继续适用，但其 native scorer 不会直接给 cross moment 或 full Jacobian 真值。行为 endpoint 与 internal proxy 必须分开；没有实际项目失败 prevalence、目标标签资格、source-code audit 或实验收益。不得自造 benchmark/标签来补缺。

## H03 决定与下一步

决定：根据用户反馈返回第2步，采用“条件范围修正 + 必要交互 + 简化/统一”三条数学路径，仍在同一个 Delta discovery batch。
优先深入 R2-C/R2-J，R2-D（diffusion）作为必要性检查，R2-E（evidence value）作为判别边界。它们是线索和推论，不是四个准入候选，不强制等量扩展。

下一动作：
1. 用本笔记的完整对象对照概率记忆/条件控制近邻的实际推导和作者源码，而不是仅按标题判死。
2. 检查 causal cross moment 学习是否有可辨、可取得的训练目标；复用原生 benchmark，缺标签记 measurement gap。
3. 提出确实改变功能或解释的构造，补齐假设、连续推导、区别性预测、复杂度和强替代。
4. 进行独立语义审查及 originality/importance/feasibility 审查；未完成前不给 D 编号和 candidate count。
5. 保留20候选/15选择缺口；代码、完整实验设计及 Local 执行在后续适用边界。
