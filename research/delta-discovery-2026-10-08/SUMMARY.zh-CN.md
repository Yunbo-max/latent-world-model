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
