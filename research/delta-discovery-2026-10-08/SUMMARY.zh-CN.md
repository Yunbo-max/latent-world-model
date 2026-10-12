# Delta 数学发现：修复、候选历史与条件结论

## R18 v3：从“精确商失败”修到“有预算的最小泄漏”

这次不是把 R18 v2 判错。v2 已经正确说明：同一前缀允许的不同未来分支若暴露互补方向，公共精确不可见空间会塌成零，任何精确零泄漏商都必须退化为完整 ledger。v3 保留这个反例，但把目标修成有明确条件的近似问题：对一次固定 destructive map 所合并的 pairwise 状态差 `K alpha`，若 `||alpha||<=R`，rank-`r` side code 保留 `V^T alpha` 后的最坏未来输出能量，精确等于 `R^2 max_pi lambda_max((I-VV^T)G_pi(I-VV^T))`。因此“该保留哪些方向”不再是模糊直觉，而是一个明确 Grassmann min--max；pathwise SVD 给必要下界，common PSD envelope 给安全上界。

一个二维例子说明为何这个区分重要：两条同前缀分支分别只看 `e1` 和 `e2`。只保留一维时，最优斜方向把最坏泄漏降到 `1/2`；公共 envelope `I` 的尾值却只能证到 `1`。所以 envelope 是可靠证书，不是最优解。

最可能失败的地方也被写死了：等式只适用于精确实数 side code；有限位量化要增加 cell/noise 项。它只处理一次固定映射；连续不同方向覆盖需要尚未得到的 constant-width code transition。`beta=1` 的 erased-row 还要求 paired states 共享当前 `k/v/beta`，否则 state-dependent value 可能把“被擦除”信息重新编码。Prefix tree 与 pairwise radius 的 coverage、global nonlinear routing、真正消费 code 的 decoder、matched-total-cost 和原生内部 scorer 都没有。

因此这是一条有价值的 Delta-specific 调试定理，不是新 updater。与 switched observability、balanced truncation、approximate bisimulation、直接 coefficient/protected-coordinate ledger 强碰撞；exact Grassmann 目标没有被伪称为已有逐式先例，也没有反过来被夸成原创性证明。四路独立最终字节审查通过后，R18 在 attempt 3/3 正式 park，候选/准入/选择增量为0。当前仍为 **5历史 / 0活动 / 0科学准入 / 0选择**，没有运行任何实验。

## R07 v2：把局部二次动作边际接回完整递归状态

这次修复的不是“真实性 gate”，而是 v1 把冻结参考二次式外推到耦合递归的范围错误。修订后，写入动作先注入完整状态（记忆、更新器、路由、belief、pending feedback 等），再在固定未来策略与共同外生后缀下传播。前向切向/反向 costate 给出精确一阶边际，二阶递推保留 costate 加权的动力学 Hessian；同时给出含余项的有限步下降证书，并修正 `q=0,h<0` 等不定曲率分支。仿射冻结极限精确退化回 v1，因此旧反例和正确阈值都被保留。

数学新意主要是把 R07 的适用边界和遗漏项写完整，而不是一个新 updater。完整状态 adjoint、DDP/iLQR、可微 MPC、MAML/learned optimizer 与 Bellman evaluation 已覆盖主体机制；Delta 只留下 rank-one 初始收缩，尚未证明总状态/FLOPs 更低。现实部署还缺动作前可得的 `q,h,kappa`，共同路径导数也不能自动代表自由运行因果效果。三路独立最终字节审查通过条件数学与来源，但判为 major-component collision/control-only；R07 在第2/3次修订后 park，实验未知，候选增量0。当前仍为 **5历史 / 0活动 / 0科学准入 / 0选择**。

## R02 v2：压缩状态会怎样破坏反事实信用

这条线解决的是一个很具体的漏洞：v1 在完整历史上用随机动作和延迟真实结果做 AIPW/OPE 是成立的，但若部署时只保留压缩商状态 `q`，不能自动把历史 propensity 和 outcome regression 都换成 `q` 的函数。新推导给出精确偏差 `Cov(mu_a(H),m_a(H)|q)/bar_mu_a(q)`；一个只有两种历史的反例就能产生 `1/4` 偏差。只有目标/行为策略、即时期望损失及动作条件下的下一商状态转移都真正经 `q` 因子化时，序贯 DR 才能由后向归纳合法下降。

Delta 特化的新意很窄：对预先声明的有限标量观测族，右商 `X -> XW` 必须至少覆盖相应协向量的联合行空间；如果下一商观测本身依赖 `W`，则问题变成递归不变子空间/固定点，而不是多加几个 moment 就能证明。这个边界有调试价值，但状态抽象 OPE、STAR、abstracted MIS、一般序贯 DR 与已有 R18 已覆盖主要功能；最可能失败在所需宽度退化为满宽、商核条件不可从前缀验证、外部 propensity 日志成本被漏算，以及原生任务根本没有商核真值或反事实回报。

因此三路独立终审通过的是“条件数学正确的控制结论”，不是原创方法或已验证效果。R02 用到第 2/3 次修订并 park；候选增量为0，当前仍为 **5历史 / 0活动 / 0科学准入 / 0选择**，未启动任何模型代码或实验。

## 最新交付：先修复两条关联线索

之前的条目并非全错：正确公式、反例和已知机制对照继续保留。按最新反馈完成了 [R01 v1](repairs/R01_VALUE_SPAN_AND_CREDIT_MARGIN.v1.md)，并经独立[数学审查](reviews/REPAIR_R01.math-review.md)与[来源审查](reviews/REPAIR_R01.source-review.md)核对最终字节。审查发现的 K/Q 上界递推表述歧义已改正并重新审查。两条是相互关联的修复，不计作两个新方法。

| 修复 | 解决哪个缺点 | 本次数学后果 | 已知部分与剩余问题 | 最可能失败处 |
|---|---|---|---|---|
| R01-A 固定 value 子空间 | 完整 gate feedback 会让切向秩增长，收缩不保证可压缩 | 共同固定右子空间内可精确递推；泄漏会通过 gate 返回子空间，已给完整误差式 | 不变量/降维已知；结构性限制等价较小 value-width Delta。仍需寻找因果可得且保留任务容量的几何 | 真实残差持续出空间、key/value导数遗漏、求gate界太贵，或收益仅来自容量缩小 |
| R01-B 动作信用裕量 | 小相对切向误差仍会翻转微弱写入信用；高秩却可能不影响信用 | residual与costate配对给信用区间；合法误差与全区间曲率界下可选有限下降步，否则保留基线 | adjoint/inexact-gradient下降已知；剩余是Delta结构能否提供便宜且有用的证书 | 误差界淹没信号、曲率界太松或取得证书比完整反传更贵 |

## R01 v2：不缩记忆，只缩信用商

这次修复了 v1 最实质的容量质疑：`S` 仍是完整名义 Delta 记忆，只维护 `U=XW` 作为某个动作/损失所需的切向商。数学上，非退化 scalar-gate 步要对任意完整切向精确递推，gate 导数协向量必须完全落在 `W` 的行空间；要从 `U` 精确恢复某个标量损失信用，该损失协向量也必须落在同一空间。于是最小宽度受这些协向量联合张成空间约束，而不是凭“低秩直觉”任选。若 `W` 随时间旋转，旧商通常不能无损搬到新商；近似商的误差还会被省略的完整切向经 gate 重新注入。

它的价值是把“何时能够保留完整记忆、却只算任务相关信用”变成了可证伪条件，并给出两个2×2反例；它的局限同样明确：通用 exact lumping、goal-oriented/DWR 与时变模型降阶已经覆盖核心思想，真实任务所需协向量并集可能很快长到 `d_v`，维护 `W/G/C` 和泄漏证书也可能比直接 JVP/VJP 更贵。因此当前结论是“条件数学成立、Delta 特化有解释价值、原创性与工程收益未证、实验未知”，不是失败，也不是候选准入。活动/准入/选择仍为0；没有运行代码或实验。

两条条件数学获支持；贡献差异和模型效果分别未闭、未知。下一步优先沿 A 的实际value几何与 B 的goal-weighted residual成本推进，比较同容量普通Delta、完整VJP/BPTT和同信息直接动作预测器；不能凭这次修复声称减少遗忘或递归变强。没有新模型代码或实验。

当前仍 **5历史 / 0活动 / 0科学准入 / 0选择**。pool20/selection15保持，指探索池与合格选择目标，不保证20个全新成功方法；旧历史/控制不抵扣活动池短缺。下面保留先前累计记录，不将其全部解释为数学错误。原生资产沿用已固定的 `lambada_openai`，较早笔记的 standard描述是历史版本，后续评估不得混用；此次未运行任何评分。

这是数学阶段的部分里程碑，不是 20→15 完成。构造历史现有 **5 张卡**；D01、D03、D05、D06、D07 已全部因重大功能或组合碰撞移出活动池。D07 的条件代数仍成立，但完整公式与作者代码审计只留下一个窄的 direct-hinge 实现差异，不能据此科学准入。当前**活动候选 0、科学准入 0、选择 0**，距目标仍差 20 个活动候选/15 个选择。没有项目代码、测试、训练、推理、原生评分、数据/模型下载、GPU 或实验运行。

| 条目 | 解决什么 | 数学上真正留下什么 | 与已有工作的差别 | 最可能失败处 | 当前处置 |
|---|---|---|---|---|---|
| D01 | 延后判断旧写入应保护还是释放 | 共享未来仿射路径时，一个事件的双状态差保持 rank-one；后验重权可精确压缩 | Wilson mixture、PF-RNN 已有后验多假设；压缩后与显式双状态预测完全相同 | 多事件分支爆炸；state-dependent features 破坏共享路径；无语义身份证据 | inactive equivalence control |
| D03 | 当前写入如何少扰动未来 query | `G=ΣωPᵀqqᵀP=JᵀJ`，并用归一化 inverse metric 写入 | 这是 observability/Gauss–Newton + APO/natural gradient + PDN/Q-Delta 的直接组合 | frozen path 不等于真实部署；密集 solve 昂贵；低扰动可等于快速遗忘 | inactive control |
| D05 | 有限精度状态应如何分配 bit | 条件性白化/water-filling 局部构造 | balanced realization、STEPQuant/DAMP 已实质覆盖 | 指标漂移、重复量化和内核成本；无新功能 | inactive history |
| D06 | 防止连续 erase/decay 把方向压扁 | 滑窗 `-logdet` 预算给条件性 `σ_min` 下界 | HGRN/谱-Jacobian 控制已有 retention floor；COLD/token bucket 已有窗口预算 | greedy clip 会产生 `[B,0,…]` 饥饿，无 utility/regret 最优性，不识别语义方向 | inactive guardrail |
| D07/WTSR | 不改推理结构，训练时直接保护实际写入方向 | frozen path 上 `||P W_i||²/||W_i||²=||Pk_i||²`；加入有限时域 survival hinge，推理零增量 | 一般 source contribution/realized survival 已知；同-key 时精确退化为 Tabular ICL Eq.10；write-rate decay 与 Delayed Supervision 覆盖主要功能；只余 arbitrary-key direct hinge | 只保 state norm，不保 query 可见性/语义；会保存过时事实；scale-blind；无 native 机制 scorer；未证明优于 CE/Delayed QA/write decay | inactive diagnostic, major functional collision |

## 本轮新增的否定边界

`NOGO-CAP-02` 证明：对所有旧状态与新值都精确覆盖当前 key 的仿射写入，必须满足 `Aᵀk=0`，所以旧状态路径必奇异；在显式有限精度下，若旧行为类与新值都需恢复，还必须支付联合编码容量。它不覆盖非线性/状态依赖更新、额外 side state、近似覆盖或预测商意义的恢复。

`DEFERRED-CORRECTION-DEBT` 证明共享 frozen affine 路径上 `main+debt=ideal` 的守恒，但 future-key 偿还就是 transported error feedback。精确追平取决于安全 transported-key 可达子空间；无事件身份不能决定 debt 应偿还还是取消，有身份又变成 replay/event memory。故它是控制，不是 D07。

新读的 DeltaTTT 已明确覆盖两层 state-dependent Delta、local squared targets、pre/post hidden target 与精确 chunkwise nonlinear recurrence。因此“堆多层 Delta + local reconstruction loss”直接归 baseline，不生成候选。

## D07 的合法范围

D07 保留普通 Delta/GDN 前向更新。训练期对观测序列采样 source `i` 和 horizon `h`，传播 `z_i=k_i, z_j=A_jz_{j-1}` 并正则 `s=||z_{i+h}||²`。后缀只作训练监督，推理不读未来 token/答案、不加状态或算子。

它同时给出一个明确冲突：若后续 key 与旧 source direction 的重合为 `c`，当前 residual 必须压到 `ε`，则普通 Delta 可保留的 source survival 最多是 `1-(1-ε²)c²`。所以这个 loss 只能是软代理，不能声称“完整纠错又完整保留”。独立审查已核对维度、梯度、gate domain、zero/tiny-write 约定、复杂度与 frozen/moving path 区分。

新审计固定了 Tabular ICL 的作者代码 `0be576b8481e153ce7489aba6ad64e278c133c09`，并确认其 `_apply_deltanet_beta_decay` 在训练与推理中实现 `beta*t0/(t0+position)`。在单位同-key、无额外 decay 的特例，`sqrt(s)=prod(1-beta)=C_i/beta_i`，与论文 Eq.10 精确对应。How Linear Attention Remembers 又给出一般 source contribution，RPMem 明确给出 realized-path source survival。因此“未发现完整 hinge 逐项复现”只是一项窄检索残余，不是原创性结论。

## 本轮新增的两个否定控制

`NOGO-OBLIQUE-03` 给出 `A=I-ka^T` 的精确二维奇异值。只要 `a` 含任一垂直于 `k` 的分量，裸因子必有 `||A||₂>1`；欧氏非扩张只能发生在 `a=ck,c∈[0,2]`。这不能外推到 `AD` 或 `DA`，因为独立 decay 可能抵消扩张，而且实际顺序不可交换。

`REVISION-EVIDENCE-POSTERIOR-EDIT` 说明额外已观测证据确可解除 residual-only TV no-go，但随后得到的是普通二假设 Bayes gate 加已知 protected/ridge/slot edit。无新增证据仍不可辨；完美 ID 退化 routing；future teacher 属于额外监督。独立复核纠正了 unequal-prior Bayes error、ridge 端点、平行地址可行性以及 BOCPD/mixture 的严格范围。两项都不计候选。

## 本轮继续闭合的三条路线

1. **Unitary Delta dilation**：一步 Halmos 扩张可以把被擦除分量搬进一个辅助槽，但第二次复用该槽就会让旧内容流回；严格 Delta contraction 的全时域 exact unitary dilation 需要无限维。有限时域版本每步用新槽，状态随 horizon 线性增长，实质是显式事件记忆。
2. **Counterfactual query-visible write utility**：固定路径下可以精确测一个 write 对未来 query/CE 的 signed contribution，解决了 D07 只看 state norm 的诊断缺陷。但对只控制该 write 的参数，最大化 utility 的梯度精确等于普通 future CE；AttriMem/HiMPO 等又已用 source ablation/signed memory credit。它能事后诊断 revision，不能从混合状态中选择性删除来源。
3. **SPD metric oblique Delta**：`A=I-wrᵀ` 在某 SPD metric 中非扩张当且仅当 `0<rᵀw≤2`。固定 metric 时，它精确等价于白化坐标中的 normalized/preconditioned Delta；逐 token metric 的局部证书不能自动推出整个产品稳定，且与 PDN/KDN/GDN2/QED 的几何重合。

同时加入 2026-10-02 的 GSA2 全公式边界：key→slot 使用 OJA2 correction，slot→value 使用 Delta2 correction，并在两侧解耦 erase/write。因此“双侧纠错、reverse/Oja update、两阶段共享 slots”不能再作为新候选名称；该论文的 arXiv 记录没有作者指定代码链接，所以未冒充源码审查。

## 2026-10-09 新增的五条严格边界

1. **随机化 survival**：带 `1/p` 的 Bernoulli Delta 在单步均值上等于普通 Delta，但固定 key 的相对路径方差指数增长；不补偿则只是更小的确定性 gate 加 update dropout 噪声。有限精度 stochastic rounding 是有效数值基线，却不能使单条轨迹永久保留。
2. **dual-frame 冗余编码**：`Z=FS` 的 exact recurrence 与原 Delta 共轭。方形 frame 只是坐标变换；冗余 frame 要增加状态/能量/bit。Delta 自己造成的干扰仍是合法 codeword，syndrome 完全看不见。
3. **checksum/sketch 修订判断**：任何因果 sketch 都受 data processing 限制。Bloom/SimHash 只有在稳定身份或严格几何间隔已经存在时才有效，且还需保存当前版本；这会变成 approximate dictionary/event memory，而不是新的 Delta 原理。
4. **causal polynomial/Krylov**：只能逼近从前缀可预测的 future-product 条件对象，无法消除不可预测后缀或一般非交换顺序。具体实现分别落回 D03 predictor、GKA/PDN solver、source trace 或 DeltaProduct。
5. **affine Magnus/commutator**：transition commutator 会漏掉 write chronology；相同 key、不同 value 即使 transition 交换，也仍有合法 last-write gap。BCH 的 bracket 是需要保留的顺序项，盲目抵消会破坏 revision semantics。

QED 的全文公式缺口也已正式闭合：query-derived 项进入同一个 erase covector，左侧写入仍沿 key；它保持一个 eigenvalue，却不保证 singular norm 或全时域 ordered-product 稳定。截至 2026-10-09 未定位作者指定公开实现，因此没有虚构 kernel/吞吐结论。

## 本轮新增的四条控制/no-go

1. **Reciprocal cycle**：增加 value→key 状态能诊断可逆性，却不能从相同已观察 pair 历史中判断修订或碰撞；当前 pair 完全写入后 cycle 自动为零。它与 BAM、GSA2、双向 ridge/RLS 和 reverse prediction 重合，并把状态约翻倍。
2. **Rank-revealing QR**：thin QR 可以精确判定新 key 是否增加线性方向，并给出保留旧约束的最小范数写入；但这个式子就是 hard OWM/projection，软化后就是 RLS/PDN。它识别线性不相容，不识别事实应修订还是共存；近相关时更新范数按 `1/rho` 爆炸。
3. **Martingale release**：合法 pre-outcome likelihood ratio 或 e-process 能把“永远至少一次错误释放”控制在 `alpha`，并给出 change 幅度—延迟关系。但普通 Delta residual 不自动满足该 filtration；完整构造仍是 e-detector/BOCPD/Kalman innovation 或 Bayes gate 加已知 edit，相同 observation law 的 revision/collision 世界无法被分开。
4. **时变度量洗白**：对任意可逆 transition 都能令 `H_t=A_t^{-T}H_{t-1}A_t^{-1}`，使移动度量能量恒定；标量衰减和爆炸都可被这个坐标变化隐藏。只有 uniform `mI<=H_t<=MI` 及分别的上/下 cross-time inequality 才能给物理稳定与保留下界，随后落回 D06、经典 contraction/dynamical isometry 或 RLS/PDN preconditioning。

四条路线均完成连续推导、边界/反例、最近工作比较和独立语义审查；它们没有获得 D 编号，也没有改变 **5 张构造历史、0 活动、0 科学准入、0 选择** 的真实计数。

## 本轮新增的四条严格处置

1. **Retroactive rollback Delta**：固定后续仿射图时，旧写入可以用 transported receipt 精确删除；一旦真实删除改变后续 key/gate/value，就出现额外 forcing sum，必须 checkpoint+replay。该 Delta 专用结论与工程权衡已有 2026 年直接工作，且 arbitrary stable-ID rollback 在有限精度下必须支付 provenance/history 信息。
2. **Set-valued Delta envelope**：维护全部相容线性 map 能诚实表示不确定性，但这是经典 set-membership filtering/version space。单一凸椭球或多面体不能无损表示 revision/coexistence 的离散 union；精确分支最坏指数增长，压缩后回到 OBE/Kalman/RLS 或 mixture。
3. **Orthogonal value rotation**：全局 Householder/Procrustes edit 受 Gram/范数可行性限制并按 value 方向污染未保护输出；单位 key 上的 exact local rotation 状态逐项等于普通 full-step Delta。state-dependent target matching 的 Jacobian 仍是奇异 row replacement，保范数不等于保关联。
4. **Provenance tensor Delta**：`u=k⊗c` 将即时干扰精确变成 `(qᵀk)(rᵀc)e`，但它是 TPR/Fast Weight Memory 特征上的普通 Delta。一热 `c` 就是按 ID 路由的独立 Delta memories；unique event tag 仍需 query-side ID 与索引，dense/random tag 则承担 VSA/HRR crosstalk。

这四项都不进入活动池。它们共同表明：可逆、集合不确定性、保范数和身份维度只有在付出 replay、分支、额外状态或外部 identity oracle 后才有用，并不会自行生成 revision/coexistence 的语义证据。

## 本轮新增的三条双重审查控制

1. **Exact-flow / implicit-proximal Delta**：冻结当前 key/value 后，精确梯度流系数是 `(1-exp(-τ||k||²))/||k||²`，proximal 系数是 `η/(1+η||k||²)`；两者都只是在同一 rank-one residual 上改标量门。单位 key 配合 softplus/exp 时与 sigmoid Delta 完全同图同梯度，且分别与 EFLA、Longhorn 直接碰撞。
2. **对称 / Strang split Delta**：`D^(1/2)(I-βkkᵀ)D^(1/2)` 与实际 KDA 因子每步相似，最坏非扩张界没有改善。naive 最后半衰减会破坏原 key 的精确 overwrite；修复后正是 preconditioned separate-address Delta。Strang 的高阶结论只在另行声明的 frozen continuous ODE 下成立。
3. **伪谱 / Kreiss transient Delta**：合法标准 Delta 因子满足 `||A||<=1` 且离散 Kreiss 常数精确为 1，逐步 penalty 因而无信息；Kreiss 定理又只管一个固定矩阵的幂，不管 token-varying ordered product。产品范数、Jacobian、common Lyapunov/JSR 和 future-product 预测才是正确对象，但都已是已有控制。

三条均由独立推导者与审查者分别核对公式、反例、最近工作和隐藏成本，不分配 D 编号。它们把“换时间参数”“换左右分裂顺序”“换局部稳定指标”三类伪新意排除在外；计数仍是 **构造历史 5、活动 0、科学准入 0、选择 0**。

## 重走第2步：目标与联合条件的实质推导

这轮不只排除模块，而是重新定义“何种预测/修订值得优化”。第一项给出可核查反例：普通 Delta 在固定线性高斯条件下的参数收缩恰是 noisy-query 最优预测；去偏恢复 latent map 后直接读同类 noisy query，风险可能严格增加。BC/IV 更新已有直接先例，均值与均方稳定不同，单 view 的 latent/noise 分解也不可辨。[推导与审查](rejected/NOISY_KEY_IDENTIFICATION_PREDICTION_CONTROL.md)。

第二项把修订有效性与未来 query 几何作为联合随机对象，推导最优编辑、分离门的精确风险差与相等条件；同时保留完整状态的 feature/gate/decay Jacobian 路径。二次目标只需相应联合矩，因此没有自动需要 diffusion 的结论。[联合条件风险](STEP2_JOINT_CONDITIONAL_RISK.md)经两位独立审查者按最终字节哈希复核。基础 weighted-Bayes/正常方程已知，不能宣称原创或候选准入；还需与同等信息联合 Bayes/teacher 比较，解决真实有效性监督、估计代价和 native 测量。

理论、表示、目标和计算构造都可按各自贡献义务继续，不要求每项成果必然增加新证据或部署模块。旧 no-go 只在原假设内适用。计数仍为 **5历史 / 0活动 / 0科学准入 / 0选择**；20/15目标短缺未改变，没有代码或实验。

## 下一合法动作

最新[真实预测目标推论](STEP2_OBSERVED_PREDICTIVE_TARGET.md)已经把不可得的validity/state-edit标签与可用的真实token CE分开。固定value方向只能修正残差的对应投影；改变gate不能一般实现未来风险的最优方向，方向收益和当前-fit冲突都有精确条件。完整CE度量必须穿过未来状态/workspace/plan/realization路径，GGN并非真实Hessian或稳定证书。这些不是新增loss名字、已实现方法或语义真值。

新增的压缩/读取推论是：在同一baseline、同一目标、同一动作族和嵌套因果信息下，完整信息最优动作若已由压缩信息决定，增加信息的最优风险收益恰为零；随机度量加权的动作差给出精确收益。这个“决定足够”条件弱于保留完整未来分布，仍有既有条件Bayes基础；事件读取只相对受限接口增加信息，当前writer并不读取事件。两位独立工作者已对最终字节完成数学与来源/接口审查，修正了微分交换条件。专门decision-sufficiency近邻、自然数据的重要性及估计总成本仍未闭合。

来源复读也确认普通远期CE已训练本项目writer，TTT官方代码亦学习内层任务。因此该思路的基本监督不是新发明。原生记录新增纠正：当前源码/官方harness使用lambada_openai，旧可行性表写standard，差异与原始固定bytes见[source audit](sources/OBSERVED_PREDICTIVE_TARGET_SOURCE_AUDIT.md)；不混报，保留5153。

下一步从这同一Step2入口调查受约束写入的自然方向差距、decision-focused表示与实际非因子化近邻，核查条件矩可估计性和可测量对象，再决定是否值得构造正式候选。5历史/0活动/0准入/0选择及20/15短缺不变。没有新代码或实验；不能把正常方程/信息价值恒等式凑进活动池，也不机械套用旧假设下的否定结论。

入口：[进度](PROGRESS.json)、[证据批次](method-batch.json)、[近邻图](CLOSEST_WORK.md)、[排名状态](RANKING.md)。当前没有全池排名或 top-15 选择。

## Step2 新结论：动作宽度不是新的充分性理论

这一轮把“压缩表示到底要多宽”写成了可核查的条件结论：若完整信息最优局部写入 `a*(X)` 在选定 causal feature 上做线性预测，并且原风险真的具有固定 SPD 二次 regret，那么宽度 `r` 的最佳额外风险等于加权 action operator 被截掉的奇异值平方和；多任务共享则把各任务算子纵向堆叠。随机、历史相关的风险 metric 不再能靠一个平均 covariance 加一次 SVD 解决。

这个结果没有获得候选资格。原因不是公式错，而是新审计找到了更直接的拆分覆盖：Task-Sufficient Contraction/Bayes quotient 已处理任务相关 source 与完整 regret profile，DSSR 已处理递归 writer 的未来 reader loss，RRR/Eckart--Young 已处理低秩截断。简单组合这些已知块不能冒充新方法。LongMemEval 虽有 QA 与 evidence-retrieval labels，仍没有 ideal Delta edit、内部删除或 action-rank 真值。

下一步只追踪一个更窄但真实未闭的问题：information-dependent random metric 是否能与完整递归 Jacobian 形成因果、可估计、比直接 CE/action predictor 更有判别力的构造。当前仍是 **5历史 / 0活动 / 0科学准入 / 0选择**，没有运行代码或实验。

## Step2 新结论：完整路径把“联合条件矩”变成已知 Gramian

这轮把上一条残余推到底。对一次低维 Delta edit，未来 CE 的一阶项是完整状态 Jacobian 反传的 gradient，PSD 二阶项是 `B^T sum J^T C J B`。它确实同时编码“修改能不能活到以后”和“以后哪些输出/query重要”，但数学上就是沿当前轨迹的 GGN 加权有限时域可观测 Gramian；精确 Hessian 还要加可能为负的动力学/读出曲率。最小反例中 `z(u)=u^2`、正标签、`u=0` 时 gradient 和 GGN 都为零，而 exact Hessian 为 `-1`，所以局部 PSD metric 不能冒充真实曲率或稳定证书。

部署时不能读取未来后缀。后缀只能在训练中提供随机 teacher，prefix-only 学习退化为 synthetic gradient/critic；RTRL、UORO、e-prop、DDP/iLQR 和 DSSR 已分别覆盖完整 sensitivity、随机 sketch、eligibility、未来二次 risk 与递归 rollout。逐后缀求 Newton edit 再平均一般也不是总体最优 edit。若 edit 会改变以后自由生成的 token/query 分布，teacher-forced derivative 还遗漏分布变化项，没有 overlap、环境或可信反事实模型就不可识别。

因此这轮得到的是一个有价值的统一解释、显式动作误差界和清晰失败条件，不是新候选。真正可能的新空间已缩到很窄：利用 Delta 的 rank-one 结构，在 prefix-only、无泄漏和固定计算预算下，证明一个结构化条件矩 estimator 比同信息的 direct action、普通 CE 或 synthetic-gradient predictor 更便宜或样本效率更高。当前没有这个结果，仍为 **5历史 / 0活动 / 0科学准入 / 0选择**；没有运行代码或实验。

## Delta 自我改进更新器：新增实际推导

本轮明确三类对象：参数级连续SFT、跨会话持久fast weights、单上下文适应。固定outer-trained更新器与部署时改进更新策略不同，不能从上下文记忆收益推出主干能力永久提高。

[耦合稳定性推导](STEP2_COUPLED_UPDATER_STABILITY.md)证明：状态依赖gate的完整Jacobian比冻结Delta多一个秩一反馈项；gate在0–1也可能局部扩张；两个稳定块可因正反馈联合不稳定；仅慢更新器不保证稳定。要精确保留固定旧query，应该让保护部分保持、在其固定纤维内约束可适应部分，并单独解决保护与真实修订冲突。独立审查修正了连续readout/域/商映射的过强解释。

[一手来源和作者源码审查](sources/COUPLED_UPDATER_RSI_SOURCE_AUDIT.md)确认SRWM/ACL/HOPE、Titans和SEAL的直接覆盖，并发现Sleepv2的扩容量巩固近邻。SEAL连续self-edit遗忘负证据保留；其付费原生judge和HOPE/Titans作者实现缺口没有被替换。它们只阻塞相应复现/测量义务，不阻塞其他数学调查。

当前结果是可审查控制与新的自然问题，非原创方法/RSI实验。仍5历史/0活动/0准入/0选择；20/15未完成。没有新增模型代码、完整执行矩阵或实验，旧工程与Local待执行项保留。

## 延迟反馈这一轮的直白结论

这轮没有把“等未来真实 token 再学”包装成新方法。真正留下的是一个更窄的数学边界：如果当前只决定一个标量 gate，那么未来风险对这次写入的一阶信用确实只要一个标量；在冻结未来 key/query/updater 的路径上，单个 Delta 写入还能用一个 query-side 向量和 value residual 精确传播，不必保存整块 `d_k*d_v` tangent。但一旦 updater 还要选择 key、value 或任意写入方向，精确线性信用的维数至少回到可行动作 span；同时追踪很多未结算写入，成本仍随 horizon 增长。

局部二次延迟结果不能从一次确定性写入中同时识别“该往哪走”和“曲率多大”。有 paired baseline 时至少需要两个不同非零 gate 幅度及合法随机化/同质性；总是写入的日志连“写入是否比不写更好”的符号都不能识别。有限 horizon 可以给出与长期目标相反的方向，teacher-forced 后缀也不能自动代表自由运行总效应。

最近工作把可声称空间进一步压窄：MAML/learned optimizer 已有 post-update future loss 和长 unroll；DNI、RTRL/UORO/e-prop 已有 future-gradient/eligibility；DSSR 已在固定 logged future 上评价 writer；SEAL/ACL/HOPE 已学 self-edit/Delta 更新；新近 TTT Ouroboros 更已把候选更新放入 pending，等独立真实文本到达后与 baseline 顺序比较并提交。因此“延迟验证再提交”是直接 baseline，不是本项目新候选。

当前最值得继续查证的三条只是研究优先级，不是已选模块：完整闭环破坏 rank-one tangent 后能否给出同预算低秩误差界；动作 span 约束能否在相同信息/容量/算力下优于直接 action predictor；是否存在不泄漏的公开原生协议同时测更新规则学习、旧能力保持和以后任务学习速度。第三项目前仍是 measurement gap。

本轮没有代码、实验或 D 编号；计数仍为 **5历史 / 0活动 / 0科学准入 / 0选择**。

## 完整闭环 rank-one 外推的最终边界

这轮把上面的第一个问题推到了一个紧的数学结论。冻结未来 gate/key/value 时，单个 Delta edit 的切向确实保持 rank one；但如果以后哪怕只有一个 scalar gate 可微地读取 memory，那么完整闭环方向切向每步都能注入一个新的 rank-one 方向。一个共享 sigmoid gate、依次使用未占用正交 key/value 的合法 Delta 路径，能让 exact matrix rank 随 horizon 线性增长。

这排除了“每步写入 rank one，所以远期精确信用永远 rank one”的推论。它还给出两类条件误差：固定 matrix rank 的最佳误差由奇异值尾决定；逐步截断误差按完整闭环有序 Jacobian 产品传播。只看冻结 Delta 左因子或 gate 范围不能冒充证书。

独立反例审查也阻止了更强的错误结论：矩阵秩不是一般算法内存下界，reverse-mode 可以不物化完整前向切向，规则化轨迹还能符号压缩；逐步线性化收缩与 algebraic rank 增长也可同时成立，而后者的幅度可能很小。因此这不是“必然遗忘”、性能提升或 RSI 证据。

来源结果同样明确：RTRL/NoBackTrack/UORO、KF-RTRL/OK、SnAp 与 e-prop 已经分别覆盖 exact、随机 rank-one、Kronecker、稀疏和 eligibility-factorized online sensitivity。新留下的只是 Delta-specific 紧控制，不是新压缩算法。现有 BABILong/RULER/LongMemEval/bAbI/LAMBADA/CITB/TRACE/SEAL 也没有 tangent rank、costate 或 ideal edit 原生标签；自然数据的 effective-rank 分布仍未测。

所以本轮的实际决定是：保存 theorem/control 和独立审查，拒绝分配 D 编号；后续只在能证明同预算 estimator 优势、或能找到不泄漏且可判别的自然测量时再构造候选。当前仍为 **5历史 / 0活动 / 0科学准入 / 0选择**，20/15短缺不变，也没有启动代码或实验。

## 收缩并不自动带来低相对有效秩

这轮继续追问高代数秩是否只是数值幻象，答案是否定的。存在合法 scalar-gate Delta 路径：每个完整一步切向算子都严格收缩，但终点切向的 H 个非零奇异值完全相等。因此它的绝对幅度会消失，相对谱却不压缩；把前者称为“低有效秩”会把信用消失误当成计算优势。

只有在更强条件下——每步注入秩有界、真实有序背景传输不增秩、transported contribution 按年龄几何衰减、初值另行记账——才能得到 rank 随 `log(1/epsilon)` 增长的绝对误差上界。随机 cutoff 可以在固定线性化路径上无偏，但必须满足 survival 单调和可积性；平坦谱还给任何无偏 rank-r 压缩一个明确方差下界。

来源结果没有支持新候选。Adaptive TBPTT 已估计几何 gradient tail，ARTBP 和 Randomized Telescopes 已做 inverse-survival 无偏截断，Stable Recurrent Models/Neumann-RBP 已有收缩尾界，Tropp sketches/Frequent Directions 与 RTRL/UORO/KF-RTRL/OK/SnAp/e-prop 已覆盖主要压缩工具。generic sketch 对非交换 Delta 递推并非自动闭合，但这个缺口本身还不是方案。

所以当前只保存新的严格反例和条件控制，不新增 D 编号。真正值得继续的唯一窄问题，是实际完整 Delta transition 是否有可审计的 closure，能在相同信息、内存和 FLOPs 下改善 costate/action-gradient 误差，而不是只让长期信号变小。计数仍为 **5历史 / 0活动 / 0科学准入 / 0选择**；没有代码、实验或 top-15 选择。

## 本轮修复：R02 随机更新动作归因

这条线并不是“原想法全错”。旧方案错在只观察一次实际写入，却想知道“如果没写会怎样”。修复办法是在训练/评估期真正随机选择写、跳过或其他有限更新动作，记录概率，再用之后的真实损失做 AIPW/顺序 DR。这样在重叠、共同后续策略、交叉拟合和有限时域等条件下，可以识别平均总效果。

它仍不能回答某一次历史写入的个体反事实，也不能从已混合的状态里恢复来源；稀有动作、长延迟和连续流会带来大方差或依赖问题。更关键的是，AIPW/顺序 OPE 已是成熟方法，SEAL 也已覆盖“按更新后的真实表现训练 self-edit”的高层机制。故 R02 保留为严格的因果对照，不计新候选。真正值得继续的残余是：Delta 几何能否证明更低方差、安全探索损伤界，或给顺序 DR 一个更小的充分状态。


## R03：把“随机试写”改成有保护预算的试写

这次不是再判一个 idea 死刑，而是给 R02 补上缺失的安全部分。R02 为了知道 write/no-write 哪个更好，必须让两者都有正概率；R03 进一步计算一次 Delta rank-one 写入会怎样移动仍有效旧查询的输出，并让写入概率同时权衡估计方差与该损伤预算。

修复后得到三个可靠结论：一是单步局部输出位移有精确闭式；二是如果有仍有效旧标签，可以写出旧平方风险的交叉项与充分上界，不能再把“小位移”误称为“小语义损伤”；三是预算过紧时，安全与因果 overlap 在数学上确实不可兼得。这个边界能告诉后续系统何时该缩小写入、补证据或停止探索。

它仍不是新候选。SEPEC 与 Safe Optimal Design 已经研究安全又信息高效的日志策略，其他 safe bandit/OPE 也覆盖主要优化；Delta 目前只提供一个便宜的局部 cost certificate，尚未证明长期网络安全或同预算优势。LongMemEval 和 SEAL 可看最终更新/遗忘，却不能原生验证 propensity 与反事实损伤。R03 因而在 v1 后 park，计数仍是 5历史/0活动/0准入/0选择；没有运行模型或实验。

### R03 v2：把单步保护界延伸到耦合时域，但不夸成长期保证

这次修复专门处理 v1 的真正缺口：一次写入的局部损伤公式不能直接代表后续网络。把 Delta memory 与更新器内部状态合成一个状态后，可用完整一步的局部 gain 有序传播初始写入；未来 query 若也依赖该状态，就把 query 生成器并入观测映射。这样得到“精确首步损伤 + 后续耦合传播”的有限时域上界，并能明确判断给定 exploration floor 和损伤预算时，随机动作概率是否存在。

代价和边界也很明确：所有 tube、gain、观测 Lipschitz 与基准风险界必须在动作前同时可用；结论约束的是随机策略下的条件期望损伤，不是每个写入动作都安全；若写入改变未来自由运行分布，仍需真实随机化或顺序 OPE，不能靠同一外生后缀冒充总因果效果。safe logging、small-gain 和 RTRL 类工具已覆盖主要部件，现有 benchmark 又缺联合所需标签，所以 R03 v2 是数学上更完整的 control，不是新方法。独立最终字节审查已通过条件结论；实际效果未知，计数保持 5历史/0活动/0准入/0选择，没有启动实验。


## R04：迁移当下不变，还要修复下一次更新

[修订推导](repairs/R04_CONSOLIDATION_DYNAMICS.v2.md)把快状态迁入慢参数具体化：M+=C、S−=C当下保持总读出，但原快Delta下一步会留下(I−P)C差。补偿完整递推能完全保持原轨迹，是单W Delta的等价表示；用总残差且只衰减快状态则真正改变保留行为，差别是有序强迫E(I−D)M。

独立审查实际debug了EC=0不保证E(I−D)C=0的错误：非均匀decay改变方向。v1原字节/二维反例保留，v2修复并重新审查最终字节。旧标量反例也复查：总残差能修复未释放/双记账，但慢保留对有效知识有益、对过时知识可能有害；C的有效性尚未识别。

来源补读Sleep扩容/seeding/reset、HOPE CMS，以及SynControl作者代码和SEAL/LongMemEval原生接口。主要快慢机制已知，但不把本条件理论逐式覆盖或整个巩固问题死亡当成结论。R04完成条件repair/control；理论原创性/同预算优势/原生机制测量未闭，实验未知。当前5历史/0活动/0准入/0选择，20池/15选择缺口保留。

## R04 v3：终于把“该不该迁移”写成可检查条件

这次修复了 v2 最关键的空白：不再靠“可靠/重要”口号选 `C`。先声明慢端和快端实际能表示的同一低维动作，再把未来查询损失、保护损伤与 Delta 的差异衰减传播放进联合二次风险。解本身是普通受约束 ridge；真正清楚的新推论是一个标量边界：若快记忆在目标 horizon 自然还会保留 `alpha^T`，那么它未来仍有效的条件概率 `p` 必须更大，正迁移才值得。慢衰减意味着更高门槛，长 horizon 意味着更低门槛。

这个结果有用，但没有被包装成新架构。Leimer 2019 已有快衰减/选择性慢巩固，Goldman 2024 有快慢时间常数和噪声理论，Dual-Layer Agentic Memory v2 已有反事实写入收益、成本门和慢巩固；普通 normal equation 更是标准方法。现有 LongMemEval/SEAL 只能看部分行为终点，不能原生识别 `p`、两个潜在动作结果或 Delta 内部传播。独立审查通过的是条件数学，不是原创性或实效。R04 到三次修订上限后 park，计数仍为5历史/0活动/0准入/0选择；没有运行代码或实验。

## R05：不知道联合关系，也不等于什么都做不了

这轮修的是一个很具体的错误姿势：我们不知道“这条新信息是否真的该覆盖旧知识”与“这次写入会影响哪些未来查询”的联合关系，不能因此把方向永久判死，也不能偷假设二者独立。修复后，只靠两边的发生率/平均敏感度和共同上界，就能算出联合收益的最窄可能区间；区间中点给最坏 regret 最小的 gate。更重要的是，只有区间下界大于零时，才存在一个正写入力度能对声明的局部风险在所有允许耦合下都优于不写。

这项结果最可能失败在三处：真实理想动作不只是 write/no-write；写入改变了未来自由运行分布；语义有效性没有外部证据。最近工作也很强：Fréchet 耦合、部分识别、鲁棒 Bayes 和 moment-DRO 已覆盖主要数学。所以这里的新意最多是 Delta 风险量的专门化边界，不是新架构。独立复审还修掉了矩阵 sharpness 过强、原子端点、`A=0` 除零和 benchmark 机制标签误读。最终状态是数学成立的 control、实验未知、无 D 编号；计数保持5历史/0活动/0准入/0选择。

## R06：少量真实审计能修什么，不能修什么

这次实际修复了 R05 的一个可操作缺口：不再只靠边际猜联合关系，而是在训练/评估期随机抽一小部分事件购买外部真实性标签。只要抽样概率在看见当前标签前确定、严格正且被记录，HT/AIPW 就能无偏恢复这段日志上的 `E[YZ]`。在同样标签预算下，最优规则优先审计“敏感度大、真实性预测不确定、成本低”的事件；若 `Z` 异质且合法可见，它可比均匀审计降方差。

关键限制也被明确保留。真实性 `Y` 不自动等于“完整 Delta 写入更好”的理想动作 `r`；完整 horizon `Z` 通常是事后量，不能偷用于当下决策；即使 `E[YZ]` 完全知道，动作诱导的长期代价仍可让 write/no-write 总效应反号。HT/AIPW、Neyman 分配、two-phase validation 和 active testing 已覆盖主要数学，现有编辑 benchmark 又没有联合的 `Y,Z,pi` 原生记录。因此 R06 是审查通过的 control，不是新候选；实验未知、无代码执行，计数保持5历史/0活动/0准入/0选择。

## R07：真信息也不一定值得现在完整写入

这次修复的是 R06 最关键的语义缺口。把一次 Delta 写入的局部风险拆成“新 target 收益 `b`、仍有效旧知识的有符号代价 `c`、曲率 `h`”后，动作条件不再含糊：只要 `Yb-c>0` 就存在有益小步；要让完整写入胜过不写需 `Yb-c>h/2`；要让完整写入成为连续最优则需 `Yb-c≥h`。所以真实性 `Y=1` 只是输入，不是写入许可。

这个结论也保留了明确失败边界：不知道 signed `c` 时，两个有相同真实性、收益和曲率的世界仍可要求相反动作；延迟拿到的 `Y` 不能回填同一次在线 gate；固定后缀局部风险也不能冒充自由运行总效果。Delta rank-one 结构让 `b,c,h` 可写成具体 JVP/二次型，但尚未证明比直接 action-value predictor 更便宜或更准。

KnowledgeEditor、AlphaEdit、O-Edit、LyapLock 和普通 cost-sensitive/凸二次决策已覆盖主体问题或机制。AToKe 提供历史/当前事实的时间标签，是比 CounterFact/KnowEdit/SEAL 更接近的测量资产，但仍缺动作前 `(b,c,h)` 与成对写/不写结果。因此 R07 保存为数学成立、贡献碰撞、实验未知的条件控制，不计候选；总计仍5历史/0活动/0准入/0选择，没有执行模型代码或实验。


## R08：事实过时的概率，不等于现在该释放保护

这轮把旧 posterior gate 修成了一个更诚实的决策问题。先估旧事实仍有效的概率 `p`，再把两个语义世界各自的 Delta 写入收益与保护损伤混成 `D_p(a)=h(p)a²-2q(p)a`。固定完整动作时可以得到精确阈值，但阈值方向由两边实际损失决定，不是永远“p 越低越该写”。两个 posterior 完全相同的世界，只要保护交叉项不同，就会要求相反动作。

若写入会擦掉以后能辨别真假的证据，或改变 memory/updater state，还必须加 Bellman continuation 与切换成本；一时有利的写入可能长期更差。联合 belief 区间能给保守端点证书，一步 query value 也能算，但这些分别是已知 robust Bayes 与 VoI/POMDP 工具。BOCPD、controlled QCD、时间事实阈值、AToKe、StableEdit、RLEdit 都是强近邻。

所以 R08 的价值是把“真实性判断”和“动作收益”严格拆开，并给出何时可用简单阈值、何时必须 abstain/求解动态状态的边界；它不是新架构。最可能失败在动作前 `q,h,Gamma` 不可得、多个事实联合状态爆炸，以及现有 benchmark 只看规定 edit 后的 QA。当前数学有条件成立、贡献碰撞、实验未知，不计候选。

R08 v2 实际 debug 了 `Gamma` 中最小的可解部分。若 keep/release 先选择观测通道，随后才看信号并在两个终端动作间重选，那么信息价值不是“posterior 方差越大越好”，而是 posterior 穿过 signed action-margin 阈值后带来的 `E|delta|` 增量。两个 posterior 分布可以均值、方差完全一样，却给出两倍不同的决策价值。与此同时，动作改变 memory 的代价必须单独保留，不能冒充信息收益；Blackwell 的“更有信息”也不能跨不同 memory/loss table 直接排序。

这次修复在明确条件下数学通过，但机制仍是已知 EVSI/Blackwell/controlled sensing 的 Delta 专门化。最可能失败点是动作特定 likelihood 与 terminal margin 在部署前不可估、两阶段假设不够、以及 AToKe 等现有资产没有随机 sensing/keep-release 反事实。因此 R08 在第2次实质修订后继续 park，实验未知，不计候选。

## R19：每个保护模式都稳定，不代表释放时仍稳定

这轮修的是一个组合接口。旧结果分别说明固定保护纤维内可以收缩、固定读出可以 transport、证据足够时可以考虑释放；但只要释放把过去被半范数忽略的方向重新算作误差，旧证书就可能从零瞬间跳到正值。R19 给出了精确条件：旧 kernel 经 reset 后必须仍落在新 kernel，有限乘法 jump factor 才存在。否则必须 erase/transfer，或额外保存新暴露方向的动态坐标，并把这笔注入成本写进递推。

独立审查先抓出了同模 reset 漏乘、ledger basis 与动态 coefficient 混淆、离散 selector 边界外推三处问题；修订后条件数学通过。它最可能失败在完整状态 metric 太贵、释放真实性仍不可辨识、非线性/不同分支没有统一证书，以及 direct value ledger 更简单。Baum 等 2025 switched-seminorm 工作已经直接覆盖共同 kernel 下的 mode-dependent 半范数与 dwell/leave；R19 只剩 kernel 改变时的 sharp debug boundary。因此它是有用的 theorem/control，不是新架构。当前仍为 **5历史 / 0活动 / 0科学准入 / 0选择**；没有运行代码或实验。

## R20：右侧曲率不是简单多乘一个矩阵

R09 的 rank-one 结论没有错；它假设所有 value 列共享同一个左侧风险度量。R20 把完整 query×value 曲率放回精确约束 `X^T k=e`：如果整个 metric 仍是一个 Kronecker 乘积，右侧因子会严格抵消，还是 rank one；但不可分的 Kronecker 和可以让不同输出模态需要不同左写方向。

最小 2×2 例中，唯一最优 edit 的确是 rank 2，而且最佳 rank-one 仍差 `1/48`。所以“完整曲率下 rank one 永远足够”这一外推被修正了。它最可能失败在三个地方：合法前缀看不到真正未来曲率；稠密 KKT/Sylvester solve 太贵；rank-r Delta、CG 或直接 predictor 用同样信息已经能做同样动作。K-FAC、Shampoo、CrispEdit、一般 GGN/KKT 和矩阵方程方法也形成重大碰撞。故 R20 保留为条件数学边界，不是新架构；当前仍为 **5历史 / 0活动 / 0科学准入 / 0选择**，实际效果未知且没有运行实验。

### R20 v2：把未来 oracle 换成合法前缀后，公式成立但问题还没解决

这轮实际修了 R20 最明显的缺口：不再假装部署时知道未来稠密曲率，而只用写入前已经出现的低秩 feature。精确解只需一个小 Gram 系统，仍保持当前 key 的纠错约束，也能完整复现旧 rank-two 例子。

但这里最容易误解的点是：**因果可用不等于能预测未来。** 旧 feature 可能已过时；用当前模型重算又需要 replay、旧 target 和 backward/JVP 成本。一个二维反例里，历史曲率一旋转，精确最小化旧 surrogate 的动作反而比普通 Delta 更伤；另一个近奇异例会让动作范数涨到 `1/epsilon`。M-FAC、SENG、WoodFisher 已经做了 past-gradient Woodbury，OGD/GEM/SketchOGD 已经做了过去梯度保护，所以小系统本身不是新方法。

最终结论：v2 数学正确、debug 有价值，贡献差异和实际效果仍未闭。它在第二次修订后继续 park，计数仍为 **5历史 / 0活动 / 0科学准入 / 0选择**；没有执行模型代码或实验。

### R20 v3：定理修紧了，但合法前缀仍不能认证未知未来

若未来风险度量和前缀代理在整个仿射可行空间上相对接近，v2 动作相对未来最优动作的锐利最坏比值是 `(M+m)^2/(4Mm)`，对称误差 `delta` 下为 `1/(1-delta^2)`。只约束可行差分不够，因为固定纠错基点与切向量的交叉项能制造无界损伤。独立数学审查用二维等号例和反例确认了这两点。

不能靠代数修好的地方也更明确：同一个前缀可以接上完全不同的未来曲率；低秩 sketch 没覆盖的方向能突然变重要；线性项和非线性轨迹甚至可在 Hessian 相同时要求相反动作。因此 `delta` 只能来自额外平稳、漂移、混合或概率覆盖假设，不能看完 suffix 再回填为当前 gate。PROMISE、Hessian sketch、Adaptive Newton、Hessian averaging 与 online Newton/regret 已覆盖“有强假设时如何用曲率”的主体机制。

最终留下的是一个锐利条件定理和一个实用 no-go：**合法前缀不足以认证未知未来的谱迁移。** 它不是新更新器，实际效果未知，也没有运行实验。R20 三次修订额度已用完并 park；计数仍为 **5历史 / 0活动 / 0科学准入 / 0选择**。


## R06 v2：修好了代理，但也找到了精确边界

这次不是把 R06 直接判死，而是把它最薄弱的“前缀敏感度”说法修成了精确定理。当前写入的范数 \(X=|\beta|\|k\|\|e\|\) 在冻结且不扩张的后续 Delta 路径上确实支配真实传播量 \(Z\)，所以可以据此做有限日志帧的最坏情形最优抽样。若外部还能证明 \(Z/X\) 有正下界，竞争损失有 sharp 上界；若没有，同一个前缀后面既可能完全抹掉也可能完整保留写入，竞争比可以无界。

最值得保留的是这个“何时有效/何时不可能”的条件边界，不是一个新架构。PPS/Neyman/active testing 已覆盖抽样主体；在线归一化、完整闭环影响、truth-to-action、原生联合标签和同成本收益仍未解决。三类独立终审通过最终字节，但不构成原创候选或实验成功；R06 当前用到第 2/3 次修订，候选计数保持不变。

## R01 v3：把“局部方向并集”修成精确的未来信用商空间

这次没有把 R01 原来的正确部分推翻。v2 已经证明：固定右侧子空间若要精确闭合，gate 和目标协向量必须落在该子空间；问题在于把所有局部方向直接并起来，并不一定是最小构造。v3 的修复是先固定真正关心的未来标量信用，再用完整伴随算子逐步向前缀传回。所有传回协向量的联合行空间，恰好给出环境全空间上 `X -> XW` 的最小宽度。

它也给出了更清楚的失败边界。若形式化后缀允许任意 rank-one 终端协向量和任意环境扰动，任何只看相同前缀的非满宽精确商都会漏掉某个方向；但这还不能说真实语言模型的 native loss 一定能实现每个方向，也不能说反例扰动一定可达。若只要求可达切向上的正确性，可能还能更小，必须另解受限对偶问题。

最可能失败的地方很实际：精确构造需要未来信用、完整 costate 和冻结路径 Jacobian，不是部署时免费的因果统计；多个目标会增加状态和反向计算；普通 reverse VJP/BPTT、直接 credit predictor、CLUE 或 R18 可能更简单。来源审查还确认，观测性、双模拟、精确 lumping、recurrent behavioral memory 和 R18 已覆盖一般机制；目标导向伴随模型降阶仍是待补的最近工作族。

三类独立终审通过的是这个有条件的 theorem/control，不是原创架构、原生测量或实验效果。R01 已用完第 3 次实质修订并 park，候选增量为 0；当前仍为 **5 历史 / 0 活动 / 0 科学准入 / 0 选择**，没有启动代码或实验。

## R03 v3：终于检查自由运行分布，但不是 Delta 独有新机制

R03 v2 只能在共同外生后缀上追踪两条耦合轨迹，不能证明真实自由运行策略改变后的分布安全。v3 把比较对象改成完整状态 law：参考转移每步把旧差异按 `kappa_h` 收缩，动作转移再注入 `epsilon_(a,h)` 的 kernel mismatch，于是得到有序乘积递推。Kantorovich–Rubinstein 对偶把状态距离转成 Lipschitz 保护损失上界；若常数有统一界，还能写出折扣总预算和随机动作概率的可行单纯形。

独立审查实际修了四个问题：metric 到 Frobenius 范数的不等式方向；持续 forcing 只能让**证书上包络**平台化，不能证明真实 gap 有正下界；动作前覆盖应是独立校准数据上的外层统一事件或在线 anytime 事件，不能写成退化的 `F_t` 条件概率；保护损失几何衰减还需要统一的 loss-Lipschitz 上界。

最近工作碰撞很强：一般 Markov/Wasserstein perturbation、Lipschitz model error、bisimulation metric 和 Wasserstein-robust MDP 已覆盖主体。Delta 的残余只是把 rank-one 写入范数接到通用证书的第一项。真正可能失败处是动作前根本估不准统一常数、全局 Lipschitz 太松导致永远不写、以及现有原生任务不暴露成对自由运行 law 和保护真实性。故 R03 三次修订额度已用完并 park，计数仍为 **5历史 / 0活动 / 0科学准入 / 0选择**；实际效果未知，没有运行代码或实验。

## R05 v4：不是把旧反例删掉，而是只在有条件证据的地方写

v3 的结论是：把所有 prefix 混在一起时，已知“修订概率”和“未来敏感度”的各自边际仍不够识别它们是否在同一条样本上同时发生。这个结论没有错；错位在于只考虑一个全局常数 gate。v4 允许 gate 看动作前本来就可见的 context，并在每个 stratum 重新做同一套 sharp bounds。

结果有两个门，不能混用：`a_R=(ell+h)/(2A)` 最小化“相对知道真实 joint moment 的 oracle regret”，即使 `ell=0` 也可能写；`a_S=ell/A` 才是相对 no-write 可认证的安全释放，只在 `ell>0` 时写。两个等概率 strata 可以出现 pooled lower bound 为零、但其中一层 lower bound 为 `0.8`，所以选择性写入确实比全局 no-write 更有表达力。与此同时，同边际不同耦合的旧反例仍能在另一层原样发生，安全门在那里保持不写。

这条修复数学上通过了三类独立终审，但不是新的研究候选。条件 LP、个体化 partial-ID policy、协变量辅助 bounds 与 robust baseline policy 已经覆盖主要思想；原生编辑任务又不提供动作前 joint labels。最可能失败的是 context 过细导致统计不确定性反而放大、`U` 太松使 lower bound 归零、或 common-path surrogate 与真实自由运行效果不一致。R05 三次修订额度已用完并 park；候选增量0，实际效果未知，没有执行模型代码或实验。

## R06 v3：能保证写入活下来，就必须接受改得没那么彻底

v2 已经证明，只知道未来不扩张，当前写入可能被后续 key 完全抹掉，所以没有正的竞争保证。v3 没有删掉这个反例，而是给每个未来 Delta 因子加一个公开的最小奇异值裕量。这样当前写入至少保留 `alpha=prod eta` 的比例，有限帧审计分配也得到明确的最坏竞争因子。

真正重要的新推论是代价：同一个裕量也让当前 key 的更新后误差至少剩下 `eta` 倍。一步 exact overwrite 会把这个裕量降到零；裕量越大，旧影响越不容易消失，但新误差也越难迅速修完。长时域又会把多个裕量相乘，保证很快变松；想让无限乘积保持正值，几乎等于预先限制一生能用掉多少覆盖强度。

这不是新架构。Delta/generalized-Householder 的谱、可逆残差和 PPS/active testing 都有直接近邻；完整闭环 Jacobian 与原生联合审计对象仍不存在。三类独立终审接受的是一个有用的条件定理和失败边界，不是原创 updater 或实验成功。R06 已达 3/3 次修订上限并 park，候选增量0；当前仍为 **5历史 / 0活动 / 0科学准入 / 0选择**，实际效果未知，没有运行代码或实验。

## R02 v3：能量化商状态误差，但不能把两种保证拼成 DR

这次修复把两个问题彻底分开。第一，若只在粗 quotient 上做 AIPW，偏差正好是 propensity 与 outcome 在同一 quotient cell 内的条件协方差除以 quotient propensity；Cauchy--Schwarz 给出的方差界是 sharp 的。第二，若另行假设每个可达完整历史上的即时奖励缺陷和下一 quotient 分布缺陷都统一有界，才可递推得到 fixed-policy 的有限时域 value 误差界。行为分布平均误差很小仍可隐藏目标策略下接近满幅的错误，因此两条结果不能拼成“近似 DR”。

Delta 专门化也只得到一个诊断：`q=SW` 会消掉被丢弃方向的直接 `AEW` 项，但 gate、key、value 等系数若依赖完整状态，导数仍可把隐藏信息漏回 quotient 动力学。独立审查已把 fiber 修成同时固定 `(q,z)`。最近工作中 AIS、approximate state abstraction、abstract-state OPE 和 bisimulation 已覆盖主要定量机制，所以这是一条有用控制而不是新方法。R02 三次修订额度已用完并 park；候选增量0，实效未知，未执行模型代码或实验。

## R09 v2：把静态保护度量改成真实的未来传播几何

这次不是删除旧想法，而是修正它真正要保护的对象。v1 只问当前静态度量下哪个写入方向代价小；v2 把写入沿未来 Delta 动力学传播，形成有限时域保护 Gramian，再求满足当前纠错约束的最小未来损伤方向。

数学上，在合法固定后缀下可以得到闭式逆度量更新；如果估计度量与真实度量有双侧谱夹逼，也有锐利竞争界。但两个完全相同的前缀可以接上互换的未来各向异性：此时任何前缀规则必须做同一个动作，普通 Delta 反而是最小最大解，竞争比是 `(M+m)^2/(4Mm)`。所以未来几何不能凭当前残差自动知道。

最近工作补审发现 Kalman Delta Networks 已经用滤波协方差调节 Delta 写入，这是很强的同信息基线；但它的协方差描述当前记忆估计不确定性，不等于未来保护查询的回拉 Gramian。这个区别保留了 R09 的下界，同时进一步削弱“新 updater”主张。

最终状态：条件数学成立、贡献是有用调试定理/对照、原创方法差异不足、实验未知。R09 停在第 2/3 次修订，候选增量为 0，没有运行代码或实验。


## R10 v2 直白结论：可以修，但修成的是强控制，不是新候选

原 idea 想用“保存量化残差、下一步再补”减少 Delta 状态的长期误差。v1 已证明：把同样总比特拆成主状态和残差不会凭空增加容量；如果残差改变后续写入，方法已经换了转移算子。

v2 补上真正遗漏的数学。冻结仿射路径下，若下一步把上一步残差乘以真实转移 \(A_t\) 再反馈，旧残差传播会精确抵消；若只能用一个标量，最优值由未来查询 Gramian 与残差协方差决定。残差在时间上相关时，最优标量还会随低频/高频能量移动。但独立审查发现一个关键条件：实际量化残差通常会随反馈系数变化，所以这些“最优”结论只在共同外生、对反馈不变的残差律下成立；普通确定性量化时只能当条件代理。

最可能失败的地方有四个：残差本身还要量化并再次产生传播误差；未来 Gramian/频谱部署时不可见；完整 \(A_tr\) 增加状态流量和计算；输出噪声更小不代表旧知识仍有效。更重要的是，状态空间误差频谱整形、固定码率 error feedback、图滤波 QEF 以及近期 recurrent quantization 已覆盖主要机制。因此本轮留下一个精确、有用的 Delta 调试定理和公平对照，R10 attempt 2 后 park，候选增量 0；第三次只在出现 Delta 非交换低秩、合法前缀估计、同总成本优势和原生测量对象时重开。


## R11 v2 直白结论：顺序差可以很便宜地算，但不知道该不该改

这次修复找到了真正有用的 Delta 结构。对两次最基本、没有额外衰减矩阵的 Delta 写入，先后顺序造成的差不是任意大矩阵，而是“两条 key × 两条 residual”的秩至多二乘积。即使按未来查询几何加权，也只需解一个至多 \(2\times2\) 的小问题，不必对白化后的大状态做稠密 SVD；第二条共同前态 residual 还能从实际顺序中重构。

独立审查同时抓住了一个容易忽略的错误：以两个分支的中点为基准做 rank-\(r\) 表示，不等于从已经执行的物理分支出发只做 rank-\(r\) 修改。最终版本把两者分开，并明确写出真实 no-op、物理编辑最优式，以及语义概率估错时在保留方向上的额外损失。

它最可能失败的地方仍然是信息而不是线性代数：系统没有合法的未来查询度量 \(G\)，也不知道当前顺序是正确历史还是破坏性覆盖；低秩修正若长期挂在状态上还会不断增秩，必须合并、重压缩或物化。更广的 gated/decayed Delta 也不一定保留这个二因子公式。

所以本轮保留的是一个更精确、更便宜的 pure-Delta 调试定理，不是新 updater。保序 Delta/WY、DeltaProduct 和小核 SVD 已覆盖主要机制；原生任务又没有 harmful-order 标签。R11 attempt 2 后 park，候选增量 0，实际效果未知，没有运行代码或实验。

## R12 v2 直白结论：能读出一次修改，不等于以后还能只靠这个摘要更新

v1 证明了一个静态问题：如果只看已经完成的编辑，什么时候压缩 syndrome 足以恢复关心的保护读出。v2 修的是更重要的递归问题：下一次 Delta 写入后，新的 syndrome 能不能只由旧 syndrome 和当前输入算出，而不再偷看完整记忆。

答案很严格但清楚。对固定仿射更新，syndrome 的零空间必须在更新后仍然不可见；等价地，syndrome 对应的子空间必须对转置更新保持不变。对最基本的 Delta 步，只要 gate 非零，每个 key 要么完全落在这个子空间里，要么与它完全正交。一个 key 同时跨过边界时，就能构造两份 syndrome 完全相同的记忆，让它们下一步产生不同 syndrome。跨边界泄漏的大小正比于 key 在子空间内外两部分范数的乘积。

独立审查还修了两个真问题。第一，完整的状态依赖更新只需要“组合后的整个下一步在每条 fiber 上一致”，不能把每个系数分别一致说成必要条件。第二，随意缩放 `H` 会随意缩放原始泄漏数值，因此最终改用正交基下的、只依赖子空间的诊断。

这条结果有价值，因为它把“静态能解码”和“递归够用”彻底分开，也给出了最小闭包和明确反例。但它不是新 updater：不变商/双模拟和项目里的 R18 已覆盖一般机制；直接保存同一闭子空间的正交坐标宽度相同，保存完整 `S` 时 syndrome 更只是辅助账本。现有原生任务也没有直接测量 fiber closure 或事实修订身份。

因此 R12 v2 停在第 2/3 次实质修订：数学条件成立，贡献是调试定理/强对照，原创方法差异不足，实际效果未知；候选增量为 0，计数仍为 **5 历史 / 0 活动 / 0 科学准入 / 0 选择**，没有运行模型代码或实验。

## R13 v2：未知转移模式下的共同保护读出

这次不是把 v1 换名字，而是改变了可见信息：下游知道可能的仿射 Delta 转移集合，却不知道实际发生了哪一个。修订后证明，一个共同仿射解码器存在，当且仅当一个块矩阵方程 `XM=N` 可解。即使每个候选转移都可逆，也可能不存在共同解码器；两个不同旧状态可以在不同模式下到达同一个新状态，但需要保护的旧值不同。

最重要的 debug 是缩小结论：`XM=N` 失败只能说明没有共同**仿射**解码器。只有当相同可见信息下确实存在两个可达旧世界、其目标值间距为正，才能把结论扩展为任意点解码器至少承担一半直径的最坏误差；如果不同模式的像互不相交，非线性分段解码仍可能成功。

数学、来源和对抗审查均通过这个限定版本。最近工作里，Moreno 2005 的多系统同时函数观测器是最直接碰撞；共同矩阵方程、广义逆和集合成员观测也覆盖主要机制。直接保存保护值的 ledger 仍是必须比较的简单方案，而且成本不存在无条件优劣。现有原生任务不暴露模式、内部矩阵、相容目标集合或 ledger 状态，因此实际效果保持未知。R13 在第 2/3 次实质修订后停放，不进入候选池；计数不变。

## R14 v2：后验不确定时，最稳健的写法可以精确求，但证书本身仍是难点

v1 假设已经有一个精确的来源后验，这太强。v2 把它改成动作前可见的区间 `[ell,u]`，并把“两槽里该写多少”重新推完。结果很整齐：最坏情形后验是把 `1/2` 投影到这个区间，再代回普通 Bayes 写入。还得到精确的后验错估代价、只允许一次完整写入时的写/不写阈值，以及一个明确反例：如果区间自信但错误，所谓稳健写入会比完全不写更差。

真正的限制没有被藏起来。这个区间必须由合法的 prefix-only 程序构造，并且要声明覆盖保证的抽样条件；边际 calibration 或 Bayesian credible interval 不能自动当成逐 token 证书。多槽推广还需要统一正曲率，最不利后验可能是内部混合，不能只检查顶点上的 Bayes 风险。

这条线保留为有用的定理和调试控制，但不是新 updater。Gamma-minimax、credal DRO 和后验决策 regret 已覆盖主体机制；最强简单基线就是直接做同一个 minimax router。原生任务也没有 slot identity 与所有反事实写入的联合 scorer。因此 R14 在第 2/3 次修订后 park，候选增量0；数学条件成立，贡献差异不足，实际效果未知，没有运行代码或实验。

## R15 v2：把“永远是二次响应”修成全局次数边界与局部可信域

v1 的正确部分是：如果未来结果对有限写入动作确实是一个给定的二次响应面，那么完整二次单项式的 Gram 满秩正好识别全部系数。问题在于，这个二次闭包不能从 Delta 更新式本身推出。v2 把动作先注入完整状态，再让后续状态真实依赖动作；多项式转移的次数会逐步相乘。一个抽象、未归一化的标量 Delta 代数例子已经让终端平方损失达到 `2*3^H` 次。它只反驳“裸代数自动二次”，不冒充发布版 FLA 的归一化实现。

这轮还修正了另一个过度结论：`binom(r+m,m)` 只是把任意 `m` 次黑箱多项式全部系数都拟合出来时的饱和维数，不是所有 Delta 决策都必须付出的 intervention rank。若递推结构已知，或者只想找最优动作，直接微分递推可能只需一次 VJP 加 `r` 次 HVP；但这同样是 DDP/iLQR/GGN 或直接 action optimizer 能用的同信息能力，不能据此算新方法。

可保留的局部结论是：在一条固定分支附近，如果三阶导数在半径 `rho` 的球上统一有界，二次 Taylor 模型误差至多 `M3*rho^3/6`，按它选动作的真实 regret 至多 `M3*rho^3/3`。最可能失败处是部署前拿不到合法的半径和三阶导证书，动作还会改变后续分支；现有原生任务也不同时暴露内部随机写入和各分支自由运行结果。

三类独立终审通过的是这个条件定理/调试控制。R15 第 2/3 次修订后 park，候选增量 0；当前仍为 **5历史 / 0活动 / 0科学准入 / 0选择**，实际效果未知，没有运行代码或实验。下一条独立未耗尽路线是 R16 v2。

## R16 v2：非交换流可以精确压到主动谱核，但只在结构化 decay 下真正便宜

v1 只证明了差异落在 \(\Lambda\)-Krylov 子空间，没有把它变成可执行公式。v2 将 decay 的相同特征值分组：如果 (k) 只碰到 (r) 个组，那么联合生成元相对纯 decay 的所有解析函数修正都只在这 (r) 维空间里发生，并精确化成 (B=D+cc^\top) 的小核。这样，指数传播、仿射源积分和强制端点方向都能统一计算；把相近谱值合并时，状态误差和归一化方向误差也有显式上界。

最关键的 debug 来自独立审查：一般对称 \(\Lambda\) 的特征向量可能是稠密的，所以“小核”并不自动等于“小成本”。只有坐标对角/tied-group 结构，或另外计费的快速固定特征变换，才能得到 (O(dm+r^2m+r^2)) 的顺序成本；若 (r=d)，又回到二次成本。

这条线的数学现在是完整的条件定理，但主要数值机制与 DPR1、矩阵函数低秩更新、expmv 和 grouped KDA 重合；自然 joint flow 仍不满足 exact overwrite，强制端点仍是已知 inverse-metric Delta。它也没有证明 joint generator 合理、没有 scan closure、没有事实修订证据或原生机制 scorer。因此 R16 在第 2/3 次修订后 park：**5历史 / 0活动 / 0科学准入 / 0选择**，实际效果未知，未运行代码或实验。下一条独立未耗尽路线是 R17 v2。


## R10 v3：低秩残差载体的最后一次修订

这轮没有把旧 idea 简单判死，而是修了两个真正的数学缺口。第一，低秩载体是否精确，不只取决于初始残差；所有以后可能注入的量化误差方向也必须一起进入不变闭包。第二，“Delta 每步只是秩一修正”并不意味着残差一直低秩：逐元素量化可以把一个秩一矩阵的误差立刻变成满秩。

修订后的精确结论是：固定基底 (U) 只有满足 ((I-UU^	op)A_tU=0) 才能无泄漏传播；否则每步泄漏及其后续放大都有明确递推。还构造了一族合法、非交换的 Delta 模式，证明稳健共同载体在最坏情况下必须是全宽。时变基底可以沿单条轨迹保持低秩，但基底本身、尺度、传输和 QR 都要计成本，等价的直接低秩增广状态也能用同样信息和操作。

所以这条线的正确定位不是“方法失败”，而是“第三次修订得到一个可复用的边界定理”。它能告诉后续设计何时低秩残差必然泄漏、何时必须扩宽，以及哪些成本不能藏掉；但共同不变子空间、切换系统降阶和误差反馈已经覆盖主体机制，现有 benchmark 也不能原生隔离这个机制。R10 在 3/3 后 park，候选增量仍为 0，实际效果未知，未运行任何实验。

交付：substantive commit `d6758ff92b7bbd9113547642e74bdc41130f2a5f` 已逐文件精确读回；receipt 为 `research/delta-discovery-2026-10-08/sources/REPAIR_R10_V3_DELIVERY_READBACK.json`（SHA256 `48ddb20af1c6505d827189eff125fc6296f3ab578e90bd7989b11e490ceba9ea`）。这只证明交付字节，不代表实验验证或原创性通过。

## R11 v3：修正了什么

- **原问题**：v2 没有严格区分“同一 overlay 被后续 Delta 被动传播”和“后续又注入新的语义修正”，容易让人误以为每一步都会自动增秩。
- **数学修正**：固定系数下，(C=LR^	op) 只更新 (L)，单个 overlay 秩不增；多次新 gap 注入才累积，而且最坏可精确到 (2m)。如果 commutator 依赖被修正状态，必须保留 (MC)。
- **保留价值**：得到 query 可见最小精确秩、加权最优截断误差以及初始误差不能漏掉的重压缩传播式。
- **为什么仍未成为 idea 候选**：核心机制已被有序 Delta/WY、DeltaProduct 与低秩维护覆盖；语义 selector、因果 metric、同成本优势和原生测量都未闭合。
- **状态**：四路独立最终字节审查通过限定结论；R11 尝试 3/3 已用完并 park；候选数不变，实际效果未知。

Delivery: substantive commit `aac96a58daa28a455012b95e8015dd1f0926c2ad` exact readback verified for all 14 substantive paths; receipt `research/delta-discovery-2026-10-08/sources/REPAIR_R11_V3_DELIVERY_READBACK.json` (SHA256 `a0618e7676b5173020e1897aee93e4072026df47105ad12a26890ed1e0e954fb`).

## R12 v3：有限 key 下能把最小闭包算出来，但不是新 updater

这次确实修了一个具体缺口。v2 已经给出“保护摘要要递归自洽，必须落在所有 Delta 左因子的共同不变子空间”及最小 fixed point；v3 在完整 key 家族事先已知时，把这个 fixed point 化成一个很直观的图：两个 key 内积非零就连边，从与保护 query 有重叠的 seed 出发，整块连通分量都必须保留。最小宽度就是保护 query 与这些 key 的联合秩。

它最有用的地方是一个 sharp debug：开始时与保护方向正交的 key 可以被省掉，但以后只要出现一个 bridge key 把两块连起来，先前省掉的历史就无法从旧摘要恢复。因此在线“看见新 key 再扩容”并不等价于事先知道完整 key 家族；要么保留完整状态/回放/ledger，要么承认信息已经丢失。把很小的 Gram 边直接阈值删掉也不是 exact，长序列误差还要看有序传播、状态大小和 conditioning。

四路独立审查确认限定数学成立，也确认它只是一条 Delta 专门化的载体证书。一般不变商/双模拟、同时分块与 frame graph 已覆盖主体；真正运行的 \(Y=U^TS\) 与同一个基上的直接降维状态完全相同。字典、Gram、QR/SVD、基存储、key lookup 和精度成本都必须计入，现有 bAbI/LAMBADA/RULER/BABILong/LongMemEval 又不原生暴露这套内部图与 bridge counterfactual。

所以 R12 第 3/3 次修订到此 park：数学正确、贡献是条件定理/调试控制、候选增量0、实验效果未知。计数保持 **5历史 / 0活动 / 0科学准入 / 0选择**；没有运行模型代码或实验。下一条接续为 R13 attempt 3。

Delivery: substantive commit `4e8effff833f0b553982532a9615b288dc95da14` exact readback verified for all 14 substantive paths; receipt `research/delta-discovery-2026-10-08/sources/REPAIR_R12_V3_DELIVERY_READBACK.json` (SHA256 `8532cf0969f3634d810e98128533d1b9f3aa66da405220735589378c2cbe31e4`). This verifies delivery only, not originality, candidate admission, native measurement validity, empirical benefit, or experiment completion.

## R13 v3：保留“丢失的最少坐标”，但它是强对照而不是新 updater

这轮没有把 R13 简单判死，而是修正了 v1 的过度付费：如果写入后的状态还保留了大部分旧读出，就不必把整个保护值都另存一份。真正必须额外保存的只有被写入矩阵核空间擦掉、同时又被保护查询看见的部分；其最小行数是 \(\operatorname{rank}(Q^\top N)\)。

对一次 exact rank-one Delta overwrite，这个结论很干净：保护方向不碰被擦除方向时不用 ledger；一旦有重叠，只需且必须保存一个 \(d_v\)-向量，与保护 query 的数量 \(p\) 无关。若不想反演很小的奇异值，可以把低奇异保护方向放入 ledger；但这只是固定 spectral-cut 解码器里的状态换稳定性，不能冒充自由解码的全局最优。

它最可能失败在三处：保护对象本身未必因果可得或仍然有效；basis、系数、SVD、精度、带宽和延迟可能吃掉状态节省；现有原生 benchmark 只看端点，不能证明收益来自该 ledger。更关键的是，同一个最优 lost-coordinate ledger 本身就是最强同信息简单对照，R18/R12/R19 和 observer/invariant 理论已覆盖主体。

所以五路独立审查通过的是一个可复用的边界定理和 debug control，不是新架构。R13 第 3/3 次修订到此 park：候选增量 0，实验效果未知，计数保持 **5历史 / 0活动 / 0科学准入 / 0选择**；没有运行代码或实验。下一条接续为 R14 attempt 3。

### R13 v3 delivery closure

Substantive commit `a68d861d1bfcc8e7e2ccc006f98c9ebbe7f00eaa` was written to literal `main` with expected parent `7b1ccbcb2cfc4f1554c97aea4b87fe4d03d42f02` and `force=false`. All 15 substantive paths were fetched at that exact commit and matched the submitted bytes. Receipt: `research/delta-discovery-2026-10-08/sources/REPAIR_R13_V3_DELIVERY_READBACK.json` (SHA256 `5a44009c73c0a8440e38442226354a6a2ecb38c98b7b3f903cba72e89e458579`). This verifies delivery only, not originality, candidate admission, native measurement validity, empirical benefit, or experiment completion.

## R14 v3：证书不是凭 residual 变出来的，现有路线到这里应当停

这次不是再给 router 加一个 loss，而是直接检查 v2 尚未回答的问题：假如两个世界在写入前给模型看到的全部记录几乎一样，但一个应写槽1、另一个应写槽2，那么一个“逐 token 有效”的 provenance 区间能有多窄？答案是：若两世界可见分布的总变差为 `delta`，区间至少以 `(1-2 alpha-delta)_+` 的概率同时包含 0 和 1；完全不可区分时，它经常只能诚实地给 `[0,1]`。

同一重叠部分还迫使任何更新器承担至少 `(1-delta)lambda/(1+lambda)` 的两槽局部风险。完全不可区分时，v2 的对称小步写恰好达到这个极限；硬动作如果不允许随机混合就选择不写，允许混合时有另一条明确边界。这说明 v1/v2 的数学并没有被推翻，但剩余问题属于信息不足，不是再换一种 Delta 几何就能解决。

最可能失败处也写清了：真实任务可能有能区分版本的 ID、时间戳、外部纠错信号或可查询证据；一旦加入这些信息，下界会变弱。但这些信息也必须给直接 Bayes/minimax router、事件 ledger 和 direct action predictor，并计入标签、状态、检索、延迟和计算成本。现有 bAbI/LAMBADA/RULER/LongMemEval/模型编辑原生 scorer 只能测行为端点，不能验证这一内部证书机制。

因此 R14 在第 3/3 次实质修订后正式 park：留下一个有用的证书坍缩与风险下界定理，不升级为新候选；实际效果未知，没有运行代码或实验。下一步转到 R15 的最后一次修订，而不是继续给 R14 换名循环。

交付闭环：实质内容已以旧 `main` 头 `0052709f6ac9aa98b0e199a75b2d1da0608e974c` 为 expected parent、`force=false` 推进到 `3bd31945097eefe9d58a8a79feea45facb206a03`；14 个路径均从该精确提交读回且字节一致。收据：`sources/REPAIR_R14_V3_DELIVERY_READBACK.json`（SHA256 `ff1a18601d70b479696ac703bdc3121cb4e3d13f42f3aa284e977a037948a1ba`）。这只证明交付，不证明原创性、科学准入、原生测量有效性或实验收益。

## R15 v3：局部导数不是半径证书，第三次修订到这里应当停

v2 已经说明，真实耦合 continuation 下响应次数可能快速增长；但它仍留下一个希望：也许只看当前点的有限阶导数，就能选出一个安全的非零动作半径。v3 把这个希望直接检验了。对任意只使用同一 prefix 和零动作处 `p` 阶 jet 的规则，可以构造两种非负未来损失：它们在当前点到 `p` 阶完全一样，却在球的相反方向更优。于是规则至少在一个世界里承担显式 regret；仅凭有限 jet 不能得到非平凡、与未知尺度无关的固定半径保证。

真正可修复的地方也保留了。若能在整个动作球附近合法证明 `(p+1)` 阶导数统一有界，Taylor 余项和动作 regret 都有可计算上界；若响应确实是已知低次数多项式，完整 jet 能识别它；若知道损失范围或允许不写，也有松弛安全界；若像 trust region 那样实际试一个动作并读到 branch-consistent outcome，则是新增证据，而不是从导数里凭空推出证书。

这条线的数学边界通过四路独立最终字节审查，但不成为新 updater。高阶正则化/trust-region、DDP/iLQR/GGN、直接 action/Q predictor、经验 dose means 和 OPE 是强对照。现有 Open Bandit Pipeline、Ouroboros、LongMemEval、bAbI、LAMBADA、RULER 可以测日志动作或行为端点，却不提供 joint jet、全局包络和所有 free-running 分支结果。

因此 R15 在第 3/3 次实质修订后 park：留下有限-jet 不可辨识性定理与明确重开条件，候选增量0；当前仍为 **5历史 / 0活动 / 0科学准入 / 0选择**，实际效果未知，没有运行代码或实验。下一步转到 R16 attempt 3。

交付闭环：实质内容已以旧 `main` 头 `072433bb5301ca8ae15a79e8122ba1d87c33f142` 为 expected parent、`force=false` 推进到 `51f48c750b2212675e9e41df2f4b1b780d102f6d`；14 个路径均从该精确提交读回且字节一致。收据：`sources/REPAIR_R15_V3_DELIVERY_READBACK.json`（SHA256 `7ceae336239e11f67de4c5971cd430b42526b71a0547d9fcf20f80d4fed0c458`）。这只证明交付，不证明原创性、科学准入、原生测量有效性或实验收益。

## R16 v3：单步小核不会自动变成序列小核

这轮实际修了 v2 留下的关键问题。对每个 token，联合指数与纯 decay 的差可以落在很小的 active core；但把很多 token 连起来时，这些方向会累积。最直接的反例甚至不需要非交换：依次使用正交 key，每步 correction 都是秩1，整个 chunk 的 correction 却精确达到秩 (H)。所以“每步低秩”不能当作“整段固定低秩”的证明。

正面边界也写清了：如果所有 key 和 decay 共享一个事先声明的 reducing carrier，就能把 active 部分做成精确的 (r) 维 affine scan；但补空间仍必须独立闭合并计费。若补空间或基是稠密的，总成本仍可能很高。离线 executor 可以读取已经给定的完整 chunk 来找基，但那不是固定的在线因果状态，basis discovery、存储和重构都不能免费。

独立审查还修正了来源接口：Martin--Cundy 论文支持一般 affine scan 理论，但其公开 CUDA 只实现逐坐标/对角递推；不能拿来证明 dense (r	imes r) core 已有高效实现。最终数学通过的是条件定理和调试边界，不是新 updater。它与 direct reduced affine recurrence、Delta/WY、R10/R11/R12 和低秩维护强重合，也没有新的 retain/revise 证据、原生机制测量或匹配总成本优势。

因此 R16 第 3/3 次修订后 park：候选增量0，实际效果未知，计数保持 **5历史 / 0活动 / 0科学准入 / 0选择**；没有运行模型代码或实验。下一步接续 R17 attempt 3。

### R16 v3 delivery closure

Substantive commit `89f92b1a50da312199698fc644deb88021d077f1` was advanced to literal `main` with expected parent `8f8287cb7a62c8a3314ba5aab80ebbef1e58155e` and `force=false`. All 14 substantive paths were fetched at that exact commit and matched the submitted bytes. Receipt: `research/delta-discovery-2026-10-08/sources/REPAIR_R16_V3_DELIVERY_READBACK.json` (SHA256 `b498e02d681fb1dac3453eca0a2de18af3047fac9e0373c79212f4765cd3e279`). This verifies delivery only, not originality, candidate admission, native measurement validity, empirical benefit or experiment completion.


## R17 v3 — residual-scaled spectral certificate (attempt 3/3)

R17's final repair changes the target from arbitrary overwritten-pair quotient recovery to the actual no-write-versus-Delta-write action. For a frozen/common-exogenous suffix,

\[
\mathcal I_\omega(\beta)=\beta^2\lVert e\rVert_2^2 k^\top G_\omega k.
\]

If an already lawful prefix certificate satisfies \(G_\omega\preceq U_t\preceq L_tL_t^\top+\epsilon_t I\), then the deployed score \(s_t=\lVert e\rVert^2(\lVert L_t^\top k\rVert^2+\epsilon_t\lVert k\rVert^2)\) yields the safe gate \(\beta=\min(1,\sqrt{\tau/s_t})\). This is a conditional theorem, not a construction of pointwise conditional coverage and not a semantic retain/revise oracle.

The repair is mathematically useful but has major mechanism collision with learned scalar Delta gating, observability/future-query Gramians, Eckart--Young--Mirsky, randomized low-rank approximation and Frequent Directions. Direct scalar-score/global bounds, dense gating, the ordinary quadratic gate, R09 inverse-metric editing and a protected-coordinate ledger remain mandatory controls. Float-count savings do not establish matched-bit or matched-total-cost advantage; a certificate also has weaker capability than a ledger because it throttles or abstains instead of restoring protected values.

Four independent final-byte reviews passed the stated conditional scope. Native bAbI/LAMBADA/RULER/LongMemEval endpoints do not identify the certificate mechanism, and no experiment was run. R17 is parked after attempt 3/3 with candidate delta 0; active/scientifically admitted/selected counts remain 0. Reopening requires a deployed lawful prefix certificate, matched-total-cost advantage and a native mechanism-identifying measurement. Next substantive line: R18 attempt 3.


Delivery: substantive commit `7772ff0a0ce4192127d6476bc93fecdb4cf65020`; all 14 substantive paths were read back byte-for-byte at that exact commit. Receipt: `research/delta-discovery-2026-10-08/sources/REPAIR_R17_V3_DELIVERY_READBACK.json` (SHA256 `c07694da42bf47a3535dbcfdde3df7eaa9bba6b159faf30404d18cde692087b9`).

## R18 v3 仓库交付

最终数学件、screen、source audit、四路 review 与七个累计 tracker 已写入实质 commit `82674bd2999d8c6a801c92111ea9c76e20f18d3c`，14/14 路径按该 commit 精确读回。读回证明的是文件交付一致性，不是实验验证；本轮没有启动模型代码、训练或评分。

## R19 v3：把一般图着色修成可算的有限域定理，但仍不是新 updater

这次修复的实质是把 R19 v2 里一般、难算的 confusion graph 收紧到完整有限域线性/仿射分支族。给定写后仍可见的 `Az`，把所有未来分支目标堆成 `B`，真正还需保存的维度恰为 `r = rank([A;B]) - rank(A)`。

每个相同 `Az` 的 fiber 都分成 `q^r` 个冲突部件；发送一个 `r` 维 syndrome 可以恢复任意已揭示分支，而一个同样大小的 clique 证明任何非线性或零误差随机编码也不能少于 `q^r` 个消息。这是清楚、可计算、可反证的条件定理。

最可能失败的地方也很明确：真实 Delta 是浮点、噪声、连续和重复写入的；reachable support 或合法分支可能依赖状态；basis、decoder、量化、溢出和每个 prefix 的构造都有成本。更关键的是，最强 direct signature 与 R18 ledger 只要做同样的行约简，就正好得到相同的 `r` 维对象，所以 syndrome 没有同信息或同总成本优势。原生 benchmark 也不能识别这个内部机制。

因此四路审查通过的是数学定理和 debug control，不是候选方法。R19 第 3/3 次修订到此 park，候选增量0，实际效果未知；总计数仍为 **5历史 / 0活动 / 0科学准入 / 0选择**。本轮没有启动模型代码、训练、推理或评分。下一步是汇总全部 bounded-repair 结果，只从真正新的残余问题或来源证据重走 Step 2，而不是循环重命名已耗尽路线。

