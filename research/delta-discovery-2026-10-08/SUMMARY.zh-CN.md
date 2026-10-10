# Delta 数学发现：修复、候选历史与条件结论

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
