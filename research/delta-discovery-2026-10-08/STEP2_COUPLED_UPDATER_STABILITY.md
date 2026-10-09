# Delta 自更新器：耦合稳定性、保护纤维与可计算导数边界

状态：数学控制与未准入研究线索；不是新 D 候选、RSI 实证、模型实现或实验设计。恢复 parent 为 `87380653675efecf29335f522190a3a95bb6f67b`。本轮只做来源阅读、推导与独立审查，未执行项目或作者代码。

## 1. 自然问题和信息对象

用户新增问题是：在相同因果前缀、记忆容量、总计算下，能否学习怎样更新 Delta，以吸收新任务同时保护仍有效旧能力，并提高后续学习效率？本笔记先关闭一个前提：**局部 Delta 门有界不保证状态依赖、自修改更新器的联合系统稳定；严格全状态收缩又不等于保护旧记忆。** 这不否定学习更新器，而是指定必须审查的对象。

令 `F_t` 包含截止 t 已观察的输入、已到达外部反馈、以前动作/随机种子和合法持久状态。未来真实 token 只能作为训练后缀监督；其 CE 不是旧事实有效性标签。写入决策必须 `F_t`-可测。固定外部输入路径的敏感度和自由运行总效应仍按前轮区分。

三类部署必须分开：

| 对象 | 实际改变 | 最低证据义务 |
|---|---|---|
| 参数级连续 SFT/LoRA | 慢参数及优化器状态 | 新任务学习、仍有效旧任务 endpoint、总训练/回放成本 |
| 跨会话持久 fast weights | 会话间保留的 S 及其 state | 持久化/重置语义和后续会话效果；不能称主干能力提升 |
| 单上下文适应 | 上下文内 S/z | 原生上下文预测；不能外推为跨任务永久改进 |

固定 outer-trained `phi` 的更新器 `U_phi` 可以学会适应，但部署时更新 S 不是部署时学习 phi。若更新器内部 z 改变并改变以后写入策略，它属于策略状态适应；若 phi 本身也在线变化，必须纳入联合状态及真实反馈。任一循环不自动证明未来新任务的学习效率提高。

定义 `x=vec(S) in R^n`，列向量化，`n=d_k d_v`；`z in R^m` 包含 updater 参数、动量、可影响后续更新的统计量。若反馈延迟，队列/生成该反馈的内生状态也必须纳入 z，不能把由 x 决定的反馈当固定常数丢掉导数。分析的是同一可观察外部输入序列下

`x^+=T_t(x,z)`, `z^+=V_t(x,z)`。

这是一个明确更新顺序的 map：若 V 使用 `x^+`，则 `V_t(x,z)=tilde V_t(T_t(x,z),z)`，下面的 C/D 已包含这条链。不是两个独立更新公式的随意拼接。路径导数要求可微 map；内生随机、离散选择或不光滑反馈需单独的分布/score或非光滑分析，不能假定增加队列状态就自动得到可微精确导数。

## 2. 由 Delta 秩一结构得到精确 JVP/VJP

先作局部控制：当前 k/v 外生固定，`D=I`，`beta=beta(x,z)`，

`e=v-S^T k`, `w=vec(k e^T)=e tensor k`,
`x^+=x+beta w`。

设 `r=grad_x beta`, `s=grad_z beta`，则

**`A=partial_x T=I-beta(I_(d_v) tensor kk^T)+w r^T`，`B=partial_z T=w s^T`.**

连续推导：`d e=-(dS)^T k`；因此 `d(beta k e^T)=k e^T d beta-beta kk^T dS`；`d beta=r^T dx+s^T dz`；列向量化后得到 A/B。维度分别 n×n、n×m。`w r^T` 正是冻结门的 Delta 乘积遗漏的一项。

任意方向 `(H,p)` 的精确前向导数为

`dS^+=(I-beta kk^T)H+k e^T(r^T vec(H)+s^T p)`。

对 S 输出的协向量 `G in R^(d_k x d_v)`，对应 VJP 为

`A^T vec(G)=vec((I-beta kk^T)G)+r <G,k e^T>_F`，
`B^T vec(G)=s <G,k e^T>_F`。

这避免形成 n×n Jacobian：固定 k/v 的 Delta 部分每方向 O(n)，额外是 gate-network JVP/VJP 及 m 维状态成本。它是精确结构成本结论，**不是完整 meta-gradient O(n)**：多步链、z map、训练参数敏感度和保存/重算激活仍需额外成本。若 k/v/D 依赖状态，完整微分是

`dSbar=D dS+(dD)S`，
`de=dv-(dSbar)^T k-Sbar^T dk`，
`dS^+=dSbar+(d beta)k e^T+beta(dk)e^T+beta k(de)^T`。

不能冻结这些项来认证 HOPE/SRWM 或深层网络。前轮完整 Jacobian/远期 CE/GGN 推导直接复用，不换名重复计数。

## 3. 有界 beta 的解析反例与一个狭窄充分条件

标量 `k=1,v=0,beta(S)=sigmoid(-cS),c>0`，故 `T(S)=(1-beta(S))S`。其精确导数

`T'(S)=1-beta+cS beta(1-beta)`。

在 `cS=3`，`beta=1/(1+exp(3))`，所以 `T'>1` 等价于 `3(1-beta)>1`，严格成立。尽管每个冻结 beta 的因子在 (0,1)，状态依赖 map 在这里局部扩张。这个反例否定全域非扩张，**不证明平衡点不稳定、典型轨迹爆炸或本项目模型失败**。

更具体地，单位 k 下令 `Q=I_(d_v) tensor kk^T` 为写入子空间的正交投影，`w in range(Q)`。如果对所有被分析状态 `r=Qr`，则 A 在 `ker(Q)` 上是恒等，在 range(Q) 上为 `(1-beta)I+w r^T`；两个子空间无剪切。因此当 `0<=beta<=1` 且

**`||w|| ||r|| <= beta`**

时，`||A||<=max(1,1-beta+||w||||r||)<=1`。如果再有 `B=0`，这给该局部固定 k/v map 的非扩张充分条件。此式只是保守可计算 guardrail，非必要条件，也不保证损失下降。`r=Qr` 可通过 beta 只依赖 `S^T k` 来满足，gate 梯度/残差范数仍须合法上界；单点估计不是全域证书。

若 `r` 有 ker(Q) 分量且 `w!=0`，A 从一个单位保持方向向写入子空间注入非零分量：对 `h in ker(Q)` 且 `r^T h!=0`，`Ah=h+w r^T h`，正交给 `||Ah||²=||h||²+||w||²(r^Th)²>||h||²`。所以任何这种裸剪切都会破坏欧氏非扩张。这与既有 oblique/shear no-go 相连，不能计新方法；加入 decay、动态 metric、侧状态或改变目标后必须重新推导。

## 4. 联合耦合 Jacobian 与小增益条件

完整联合 Jacobian 是 `J_t=[[A_t,B_t],[C_t,D_t]]`，其中 `C=partial_x V`、`D=partial_z V`。固定凸且前向不变域上若有统一 operator-norm 上界

`||A_t||<=a`, `||B_t||<=b`, `||C_t||<=c`, `||D_t||<=d`，非负常数，

由 mean-value 积分和三角不等式，两轨迹距离满足

`[||delta x^+||;||delta z^+||] <= K [||delta x||;||delta z||]`, `K=[[a,b],[c,d]]`。

存在严格正权重 `p,q` 和 `gamma<1` 使 `K[p;q]<=gamma[p;q]` 当且仅当 `rho(K)<1`。直接解两个标量不等式得到（b/c=0 的端点也由权重极限或严格小裕量处理）

**`a<1, d<1, bc<(1-a)(1-d)`**。

于是加权最大范数 `max(||delta x||/p,||delta z||/q)` 每步至多缩 gamma，给统一同输入增量收缩。若只有点上界，则只是局部导数诊断；域非凸/路由不光滑、域未不变或随机输入律被 edit 改变时，不能据此称全局稳定。每步各有 spectral radius<1 也不足以证明任意有序乘积稳定；这里用统一 K/固定权重明确避开这个漏洞。

**单独稳定不推出联合稳定：**标量线性 `A=D=1/2,B=C=3/5`，两个孤立块都收缩，但联合特征值 `1/2+3/5=11/10>1`。这是精确反例，不是 benchmark。

**只放慢 updater 也不够：**设比较块为 `D<=1-eta mu,C<=eta c0`，`0<eta mu<=1`。小增益条件变成 `b c0<mu(1-a)`，eta 消掉。更强反例是实际线性矩阵 `J_eta=[[1/2,3/5],[3eta/5,1-eta/2]]`：`det(I-J_eta)=eta(1/4-9/25)<0`，故有实特征值大于1，对任意 eta>0 成立。慢时钟只能降低增长速率，不能把这组正反馈变成稳定。这不否定所有两时间尺度算法；负反馈/不同耦合/目标改变必须单独分析。

若外部扰动引入 additive 距离项，统一 gamma 还能给 `d_t<=gamma^t d_0+sum gamma^(t-1-j) eps_j`。这只能解释敏感度/扰动放大，不给遗忘率、知识有效性或新任务学习效率。

## 5. 保护应在横向空间检查：严格全状态收缩会丢掉区别

设某些仍有效旧查询由固定线性 `Lx` 表示。要求精确保护是

`L T_t(x,z)=Lx` 对被保护域全部成立，而不是仅当前训练样本不掉分。

微分给 `LA=L` 和 `LB=0`。故联合 map 若全状态严格收缩，固定非零 L 所区分的初态差不能永久保持：同输入轨迹距离趋零，固定有界线性 readout L 的差也趋零。非线性 readout 则需要可达域上的一致连续性（例如连续读出且可达域紧致）；无界域上只有连续性不足。这个结论只针对初态信息、同后续输入和上述读出条件；外部再提供信息、重放或改变读出/表示可避开，稳定本身也不要求严格收缩。

选择正交坐标 `p` 表示被保护行空间，`r0` 表示 ker(L)，令 `y=(r0,z)`。精确保护下联合 Jacobian 具有形状

`[[I,0],[E,J_y]]`，

所以合理对象是**固定 p 的纤维/横向空间收缩**，不是全系统收缩。沿用同一凸且前向不变联合域、相容的固定范数，并要求全部连接线段上 `||J_y||<=gamma<1`、`||E||<=epsilon`；于是 mean-value 积分同时给出相同 p 的纤维收缩与跨 p 的距离上界，两轨迹差满足

`delta p_t=delta p_0`，
`||delta y_t||<=gamma^t||delta y_0||+epsilon(1-gamma^t)/(1-gamma)||delta p_0||`。

这是可保留区别又控制可适应分量的充分结构。当 E 非零，y 的动力学一般依赖所保留的 p；所以它是按 p 参数化的一族纤维动力学，不是与 p 无关的商映射。只有额外代表元独立性（例如适当全域条件下 E=0）才支持后一解释。它不保证新写入可行；如果欲改的 query 落在被保护行空间且目标必须改变，保护约束直接冲突。也不说明哪些旧查询仍有效，L 的构造和释放必须有合法信息，不能用 oracle。小增益可以在 J_y 的 memory/updater 子块上应用。动态 L_t 则需运输/旋转/释放项与跨时间条件，不能由本固定 L 结果免费认证。

## 6. 与训练目标和真实反馈的连接

选择可见更新器参数 phi，训练期可用真实已观察后缀 `L_future`；梯度通过上述 J 链并包含 updater 自身的变化，已有 BPTT/RTRL/MAML/learned-optimizer 机制。有限 horizon 截断丢掉尾协态；若完整链满足可用 gamma 与每步损失梯度界 G，才可界尾影响，例如从状态敏感度计的几何尾 `G gamma^H/(1-gamma)`；保护 neutral 子空间、非收缩或分布变化时该式不成立。它不是免费全 meta-gradient bound。

部署线上反馈可以驱动 V，但自生成 token、自评或自预测未来只是内部量，不能冒充独立外部效用。外部反馈真实可见仍不自动标注“旧事实已过时”。提高 phi 的未来任务效用需要任务分布、因果更新前后比较和等资源对照；减少局部 surrogate 不等于持续提高学习效率。

建议的可证伪自然问题是：在合法输入和反馈下，Delta 的 rank-one gate-feedback 项能否用比一般 updater 更小成本约束，同时保留可学习的横向空间并在原生任务上优于固定 learned updater？本笔记只给精确结构与必要缺项，**尚无非碰撞的完整新构造**。

## 7. 最近工作、原生测量和成本

SRWM (ICML2022) 已有自身产生 k/q/beta/value 并用 Delta 修改整个矩阵；HOPE/Nested Learning §8 已有 self-referential key/value/query/rate/decay memories 和多频率 CMS；Titans 已有 test-time memory、momentum/forgetting；SEAL 用 outer RL 训练生成 self-edit 的策略，再 inner adaptation。不能把这些名称重组合为本项目原创。来源与真实作者接口见同目录 `sources/COUPLED_UPDATER_RSI_SOURCE_AUDIT.md`；小增益、增量收缩、保留 invariant/semistability 是已知控制数学，不作首创主张。

强替代：普通固定 Delta/GDN；固定 outer-trained updater；同容量 SRWM/HOPE 类（需作者实现或明确独立实现）；同信息直接 action predictor/普通远期 CE；参数级任务采用 SFT/LoRA+replay、EWC/GEM/A-GEM/OGD 的适用对照。额外参数、保留原文、更多反馈/回放、探针或更长训练均必须计账。

原生测量可行性（不是完整实验矩阵）：

- bAbI 全20 tasks/20000、LAMBADA 5153 测上下文 QA/末词 endpoint，不原生提供在线 updater 改进曲线或知识有效性/internal Jacobian 标签。
- LongMemEval QA/evidence labels 支持跨会话记忆更新后的回答，不能认证 phi 递归变强、ideal edit 或保护横向空间。
- SEAL 作者 continual self-edit 评测可作参数级遗忘相关来源，但与本项目 fast-state持续/重置接口不等价；不得搬来它的结果当 Delta 结果。
- 数学反例和导数界可直接由代数审查支持；不是用 toy 得分证明科学价值。新任务效率、部署 phi 改进、语义释放仍有 measurement/identification gaps。

单方向局部导数 O(n)+gate/V 网络导数；z 存储 O(m)、完整参数敏感度可能 O((n+m)P)、BPTT 激活随 horizon，独立旧任务回放/反馈获取另计。global Jacobian bound 的构造/验证比局部 JVP 昂贵；多方向探针不能证明全域上界。2080Ti/100M或1B每arm/seed仍只是后续资源背景，显存/时间未测。本轮不存在训练、推理、测试或评分结果。

## 8. 导航决定

操作路径：H05 精确更新场 → A04 自适应门导数 → F04 秩一导数计算 → H06 反例 → G03 统一小增益 → H02/G06 保护横向空间。每个连接的条件如上，不走完整操作清单。

决定 **CONTINUE Step2**：加入用户已授权的 updater RSI 问题；把 bounded-gate、slow-clock 和 full-contraction 三个不充分解释关闭，同时保留横向空间可学习性与结构成本的开放问题。此文不新增 D 编号、不占活动候选、不恢复旧源码任务。独立数学/来源审查记录绑定最终字节。只有证明重要残余、完整构造与最近工作差异并闭合适用测量/形式义务后，才进入候选池。20/15目标与5历史/0活动/0准入/0选择保持。
