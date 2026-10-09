# 第2步续接：用真实预测目标闭合联合风险，先约束可实现写入

状态：条件数学、目标与接口推论；**不是新候选、原创性裁决、模型实现或实验结果**。母问题仍是 Delta 的局部纠错与未来查询干扰。与 STEP2_REENTRY、STEP2_JOINT_CONDITIONAL_RISK 属于同一条调查线，不能按章节重复计数。

恢复基线：literal main `12bf91d20444ec86c1ae9c15f3ed47aa5c690859`。本轮未运行项目源码、测试、autodiff、求解器、训练、生成或评测。旧 latent 工程和 Local 验收保持原状。

## 1. 本轮实际关闭什么前提

上一轮目标 `E||J(δ−r u)||²` 假定存在修改有效性 r 和理想状态修改 u。普通文本没有提供这两种真值。可以改变目标为**对实际后续 token 的预测风险**，让已发布文本里的 token ID 只在离线 loss/teacher 侧出现。这样关闭的是预测监督的可定义性，不是事实修订有效性的可辨识性。

自然问题改为：在固定因果前缀、相同未来文本分布和相同可实现写入族下，当前 key 残差的写入方向是否已经足以优化未来预测？若不足，差距来自哪个可计算的残差/敏感度条件？这是成功与失败均可能的条件问题，不宣称本项目已经发生该故障。

数学操作：B05 条件化 → C04 残差分解 → D01 受限优化 → D05 完整输出度量的拉回 → H02/H06 等价性与成功特例。下文实际执行这些操作；不是待 Local 推导的 TODO。

## 2. 精确线性参照：未来残差决定可实现 rank-one edit

固定因果信息 F。所有条件期望以下均给定 F。Sbar∈R^(d×m)、当前 k∈R^d、e∈R^m 为 F 可测；Sbar=D S，e=v−Sbarᵀk。保持 D 与 erase 顺序，普通 Delta 为 S+=Sbar+β k eᵀ。

先只分析实际可写族 S(a)=Sbar+a eᵀ，a∈R^d，固定 e。未来 q∈R^d、目标 y∈R^m 的条件联合分布**不随 a 改变**，相关二阶矩有限。设 g=y−Sbarᵀq。若没有后续写入且读出线性，下面是精确风险；若有固定仿射传播，须先把传播计入读出算子；真实 LM 不能直接用未来 raw q 代替完整传播。

定义 λ_a>0 和

L(a)=E||g−e(qᵀa)||²+λ_a||a||²。

展开平方，令 C=E[qqᵀ]、h=E[q(eᵀg)]、M=||e||²C+λ_a I：

L(a)=aᵀMa−2aᵀh+E||g||²。

M 正定，梯度 2Ma−2h，因此

**a*=M^−1 h，L(a)−L(a*)=(a−a*)ᵀM(a−a*)。**

这里 h 是查询与**可修正残差**的联合矩，不是独立平均 E[q] E[eᵀg]。代数说明：d=m=1，e=1，等概率 q=±1、g=q，则 E q=E g=0、h=C=1，a*=1/(1+λ_a)。这是逻辑例子，不是新 benchmark、训练数据或测量结果。合法更强替代是同信息的直接条件预测器；平均分解不是它的通用性质。

若 e≠0，设 z=(eᵀg)/||e||²、g_perp=g−e z，则 eᵀg_perp=0，

L(a)=||e||² E[(z−qᵀa)²]+E||g_perp||²+λ_a||a||²。

所以这个构造实际就是沿固定 value 方向的标量 ridge；**g_perp 无法由这一次写入修正**。若 h=0，则唯一最优 a*=0；风险不要求无条件写入。若 e=0，则写入恒为零，h=0，λ_a 选择 a=0。增加 gate 或改方向不能突破固定 e 的可达族。

正则必须注明对象：λ_S||δS||_F²=λ_S||e||²||a||²，和本节 λ_a||a||²不同；不能偷偷在变动 e 尺度时将两者视为同一惩罚。e=0 时状态惩罚还会留下参数非唯一性。

### 当前纠错、gate 和未来风险何时相容

若只允许 a=α k 且 k≠0，则 α*=kᵀh/(kᵀMk)。限制 α∈[0,1] 时，严格凸的一维风险给出 clip(α*,0,1)。放开方向相对无约束 gate 的精确风险优势是

hᵀM^−1h−(kᵀh)²/(kᵀMk)≥0，

等号当且仅当 M^−1h∈span(k)。因此只有这个条件不成立时，未来预测目标在此参照下需要方向上的改变。非负 gate 可能进一步限制可达动作，不能用无约束公式冒充 [0,1] 的结果。

若额外坚持当前 key 修正 kᵀa=b，则 KKT 给出

a_c=a*+M^−1k (b−kᵀa*)/(kᵀM^−1k)，

L(a_c)−L(a*)=(b−kᵀa*)²/(kᵀM^−1k)。

普通 Delta a=βk 对应 b=β||k||²；只有单位 k 才能写 b=β。若 k=0，b≠0 不可行，b=0 是空约束。e=0 时规定非零 b 只是参数约束，不能产生实际纠错。

成功特例：当前-only q=k、y=v 时 g=e，h=||e||²k；a*=||e||²k/(λ_a+||e||²||k||²)。λ_a→0、k≠0、e≠0 得到最小范数当前完全拟合 k/||k||²。该极限与已知 normalized Delta/ridge 几何重合，不能重新计方法。

## 3. 观测监督合同：不能把 latent value 目标当免费标签

线性参照中的 y 必须有真实来源。如果 y 是固定、明确的未来观测特征 φ(x_future)，它是**声明的特征预测代理**，不是已识别的语义真值；若 φ 随参数训练，目标会移动，其梯度/stop-gradient 是不同算法。普通文本不能提供唯一的“正确 hidden value”。因此对实际文本采用下一节的 token CE 对象更直接。

离线单样本 qqᵀ 与 q(eᵀg) 可是所声明条件总体的无偏观测，前提包括相同因果采样合同、有限矩、未按已知结果选样本。一个前缀通常只有一个观察到的后续轨迹；不能把它叫作已实测的条件均值。跨前缀训练是估计/函数逼近，必须保留泛化与条件-law 失配。

推理时仅能用 F 预测 C,h/a，或用已到达的新观测更新 F；未来 suffix、答案、supporting-fact 标注和真实未来 Jacobian 不得成为 writer 输入。离线 teacher 可以分析未来，但其额外文本、模型、梯度与计算必须记账，且训练标签不能泄漏到 deployer。

还有一个重要成功边界：若原读出已经满足 Sbarᵀq=E[y|F,q]，则 E[g|F,q]=0，塔式法则给 h=E[q eᵀ E[g|F,q]]=0。写入不改善此已充分知情的平方预测器。正 h 可以来自受限模型、压缩、未纳入当前信息或学习不足；不能单凭 h 把原因归为 Delta 遗忘，更不能把其含义等同于新增信息。F 的选择、读取原始事件的权限和受限 readout 都是问题的一部分。

## 4. 对真实 token 的合法 CE：完整路径与可达族一起拉回

设 a 是当前可实现 edit 参数。对于 teacher-forced 的真实未来 token x，实际 logits 为 l(a,X)∈R^V；X 包含已经声明的未来文本前缀/目标采样。以 a=0 为展开点，p=softmax(l(0,X))，t_x 是实际 token 的 one-hot。**标签只进入 loss**。参数、基线因果状态和条件未来文本分布在这个局部决策问题中固定；特征可以对状态变化响应。

要求有关条件风险/梯度/曲率矩有限，logits 在讨论域内二次可微，且有可支配界等合法条件使微分与条件期望可交换；涉及后面的 Taylor 界还要求实际条件风险在整个 edit 线段邻域三次可微。单样本光滑不自动供应这些条件。a 是当前 state edit 的局部决策参数，不能把下面的求解冒充整体 θ 的实际训练优化器。

令 K=∂l/∂a|0。若从 δS=a eᵀ 出发，列优先 vec 注入为 W=e⊗I_d；把该 block 注入完整初始状态，再经所有后续完整状态转移、retrieval 消费、workspace、plan 和 realization 的导数，才得到 K。它不是仅冻结 features 的 rank-one 连乘。若检索选择因 edit 改变且离散，局部区域导数不能代表跨切换的有限修改。

每项 CE 的一阶导数是 Kᵀ(p−t_x)。logit-space Hessian 为 C_p=diag(p)−ppᵀ，是 PSD。于是对**声明的条件未来样本分布**，

g_CE=E[Kᵀ(p−t_x)|F]，B_0=E[KᵀC_p K|F]，B=B_0+λ I，λ>0。

局部 GGN/proximal 二次对象 Q(a)=g_CEᵀa+(1/2)aᵀBa 有唯一解

**a_CE*=−B^−1g_CE。**

这就以真实 token 监督替换了不可得的 r/u 标签。B_0 是由 categorical model Fisher/GGN 拉回的几何；g_CE 由实际文本标签取期望。两者的目标分布要分别注明。外积 E[g_sample g_sampleᵀ] 是 empirical Fisher，一般不能替换 B_0 后还声称同一推导。

完整 Hessian 还含 R=E[Σ_i(p_i−t_x,i) ∂²l_i/∂a²|F]。GGN 删除它；只有 logits 对 a 仿射、该项消失或其近似误差受控时，才能把上述二次对象当真实 CE 的 Hessian 展开。不能从 PSD B_0 推出完整 recurrent 模型稳定或有限 edit 下降。若真实条件风险在局部三阶导数范数≤L_3，则

L_CE(a)−L_CE(0)≤Q(a)+(||R||−λ)||a||²/2+L_3||a||³/6。

这给出明确的**充分**下降检查条件：右边<0；常数必须实际合法供应，神经局部估计不是全域证书。本轮没有供应或测量它们，未接通停止/验收算法。

估计/solve 误差也不能隐去：对精确 Q，任意 ahat 的 regret=(1/2)||ahat−a_CE*||_B²。相对零 edit 的净 surrogate 改善 iff ||ahat−a_CE*||_B²<g_CEᵀB^−1g_CE。即使精确解有益，条件均值学习、截断 horizon、低秩/对角近似和 solve 误差也可能吞掉它。此 iff 只属于二次 Q，不属于真实 CE。

固定未来真实文本采样的 teacher forcing 是本文的对象；自由生成未来会改变输入 law。若对参数依赖的 rollout 风险求导，还需其 sampling/score 项，不能复用冻结 law 公式。权重/horizon/mask 改变哪个预测风险，不能当免费信息。

## 5. 压缩与事件读取的统一条件：保留最优决定，不必保留全部分布

这条推论允许“表示/目标”成果，而不强制新 recurrence。令 A⊂B 是**同一次 edit 决策时**实际允许的信息集。保持同一 Sbar/e，且它们 A 可测；保持同一个未来(q,y)总体与 λ_a>0。令 M_B=||e||²E[qqᵀ|B]+λ_a I、h_B=E[q(eᵀg)|B]，a_B=M_B^−1h_B。塔式法则给 M_A=E[M_B|A]、h_A=E[h_B|A]，a_A=M_A^−1h_A。

条件于 B 已有配方 L_B(a)−L_B(a_B)=||a−a_B||²_(M_B)。令 a=a_A，再对 A 取条件期望；常数与 λ_a 项同样通过塔式法则。因此信息细化的精确最优风险价值为

**R_A*−E[R_B*|A]=E[||a_B−a_A||²_(M_B)|A]≥0。**

在相关风险可积时，λ_a>0使等号等价于 a_B=a_A 几乎处处。就是说，压缩接口对**该目标、该可写族**足够的最弱条件是完整信息的最优动作已可由压缩信息决定；保留 M,h 是充分条件，却不是必要条件。它弱于保留整个未来条件分布，也不等于 I(Future;history|state)=0。该条件随 query law、value 方向、正则和动作约束改变，不能认证所有任务的充分性。

若精确事件来自已观察完整历史 H，B 可是有限 compressed/read-access A 加当前允许读取的事件；它只相对受限接口增加可用信息，**不对 H 新增事实**。若由 A 与独立噪声生成的虚构 continuation 给定 A 与真实未来条件独立，则 M_B=M_A,h_B=h_A，这个理想 Bayes 价值为零。受限函数族或计算改变可能仍有作用，和新证据信息增益要分开。

关键接口条件：事件必须在这次动作之前可用。当前源码的 episodic reader 在读取/推理路径，MemoryWriter不读取 episodic store；不能用此推论声称现有 writer 已获得 B。若 retrieval 在未来 query 到达后才发生，应改为后续读取/决定问题重新推导。改变 Sbar/e 或模型 class、增加参数/teacher/读取预算也不是本恒等式的单纯信息细化。这个是已知条件 Bayes/信息价值原理在随机风险度量下的推论，最近 decision-sufficiency 文献尚待补读，不宣称原创。

## 6. 与现有 latent 架构的真实接点和边界

本次源码阅读绑定上述 main；具体 Git blob 和函数见 sources/OBSERVED_PREDICTIVE_TARGET_SOURCE_AUDIT.md。

| 实际已有对象 | 对本推导的意义 | 不能声称的东西 |
|---|---|---|
| MemoryWriter 的 gated bounded slots | 可分析未来 CE 经 post-write M 的梯度 | 它不是 Delta S+=Sbar+βkeᵀ；本轮没替换它 |
| window_objective 的 main CE / within-window writer graph | 已有真实后续 token 监督，早段 writer 可以经后段 loss 学习 | 新增“未来风险 loss”名字不产生新监督；TBPTT 截断仍在 |
| predict_future(M) 的下一段首 token CE | 只看 compressed state 的合法有限代理 | 不证明整段未来/全查询充分性；不能扫描到后来 eligible token |
| 原始事件 store + 每行因果 query/reader | 改变了完整可用信息和输出路径 | retrieval 增益不能归为更好压缩；generated 来源不变成外部事实 |
| workspace → Z=tanh(WzH+bz) → 独立 realization | 若分析真实 edit risk，导数须穿过这些接口 | Z 没有已识别语义；saved plan 仅可独立产生下一符号分布 |
| 观测/内部计算/表达三个 clocks | 离线未来标签与真实新观测不混淆；reader 不额外 commit | 多内部计算不自动新增证据或 writer 学习目标 |

单个 fixed saved-plan readout 的局部 Jacobian rank 受该 plan 输入维数约束，但**重新规划的多条未来查询可能给更大联合可见空间**。因此不能拿 Z 的单步宽度直接断言全未来信息容量或 Delta 可保留关联数。本轮不另起无依据 codec 模型。

## 7. 来源、成本、可测量性与决定

线性 normal equations、KKT 保护与 GGN/Fisher/proximal 拉回均有既有基础，详见同名 source audit。TTT 通过 outer next-token CE 学习内层重建 views，APO 学习 function-space/weight-space proximal optimizer；因此“用未来 CE 教 writer”和“加 Jacobian metric”都不能作为本轮新意。这不是对所有目标/表示/计算组合的普遍 no-go。

后续值得审查的自然残余是：**在同一因果信息、受限 value 方向/当前-fit 条件和总计算下，未来预测最优方向何时存在可观测的、可估计的 gate 不可达差距？**差距为零、预测器已充分知情、value 正交误差占主导、真实 rollout law 不匹配、GGN 局部误差过大或 teacher/solve 成本吞掉收益，均是明确失败条件。需读实际最近构造、自然任务/现有强基线并确认重要性，不能将此问题立即改名为新 D-card。

参照 dense d×d metric 的存储 O(d²)、分解 O(d³)，每个 sample 的 C/h 形成分别 O(d²)/O(dm)（残差读出本身也计 O(dm)）。一般 r 维可达 CE 参数族 dense B 为 O(r²) 存储/O(r³) solve，完整网络 K 的形成与未来跨时激活可能昂贵。矩阵自由 B_0z=E[Kᵀ C_p Kz] 可用 JVP/VJP；C_p z=diag(p)z−p(pᵀz) 是 O(V)，不需 V²显式矩阵，但词表 logits、传播与反向不是免费。精度、GPU显存、速度均未实测，不保证2080Ti适配；100M/1B每arm/seed只是后续资源背景。

bAbI 的原生答案和 LAMBADA 的最后词提供文本预测 endpoint；它们不提供唯一 hidden y、r/u 或真实 full Jacobian 标签。可使用已定义的答案/文本 CE 作训练监督，不能修改原生 scorer 或用该 CE代替 native 结果。保留20 tasks/20000与5153分母、历史 source reads和Local pending。当前只能证明数学条件，未证明这些差距在自然数据中常见；无完整新实验矩阵、dispatch或自造 benchmark。

**决定：保留为同一 Step2 的监督、可达接口与 decision-sufficiency 推论，不放 rejected/，也不新增 D 编号。**已关闭“预测风险必须依赖 latent validity 标签”的错误前提；未关闭条件矩可估计性、最近工作剩余差别、自然重要性、成本与科学准入。普通远期 CE、同信息直接条件均值预测和已有 TTT/proximal优化是强替代；此二次对象仍不要求 diffusion 全分布采样。保留 5历史/0活动/0科学准入/0选择及20/15短缺。下一合法动作针对上述方向差距与目标相关的决定充分性，调查现有非因子化写入/预测目标、decision-focused表示与可观测自然任务，逐条件判断，不继续堆已知模块。
