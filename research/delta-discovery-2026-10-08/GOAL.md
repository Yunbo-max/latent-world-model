# Delta 数学发现后台阶段

用户请求：2026-10-08 23:42 Europe/London，Delta 数学推导 10–20 个，后台慢慢推进。

目标取 20 个实质不同候选；完整数学审查后全池排序、默认选择前15。Diffusion可选。阶段仅数学与来源/可行性审查，不含新模型代码或实验。

最新解释以 2026-10-09 17:08:50 Europe/London 反馈为准：“我们之前分析的都错误吗为啥这么严格”，“idea错误可以debug或者改正呀”。20 是约20条实质不同探索池目标，不保证20个全部原创、科学准入或实验成功；只选有资格者，数量不足诚实报告。先修复2–3条有证据线索，每条最多3次有具体delta的数学修订，保留旧字节/反例/review。局部错误、条件缺口、已知机制碰撞和效果未知分别处理；已知部分可保留为强对照，有价值理论也按相应贡献义务审查。

最新实质里程碑是 [R02 v2 因果 DR 商修复](repairs/R02_CAUSAL_DR_QUOTIENT.v2.md)：它没有把 v1 的全历史随机化/AIPW 结论判错，而是定位了“把 propensity 和 outcome regression 都压到粗商状态”时的精确偏差，并给出两历史反例、序贯 DR 可下降到商状态的强充分条件，以及固定声明标量族对应的 Delta 右商行空间下界。三路独立终审只接受其为条件性调试定理/强对照；Hao 等状态抽象 OPE、STAR、MIS、一般序贯 DR 与 R18 已覆盖主体机制，原生测量和同信息成本优势未闭。因此 R02 在第 2/3 次修订后 park，候选增量为0、实验未知，计数仍为5历史/0活动/0科学准入/0选择。

本轮实际交付：[R01 v1 修复推导](repairs/R01_VALUE_SPAN_AND_CREDIT_MARGIN.v1.md)与[来源及原生测量审查](sources/REPAIR_R01_SOURCE_AUDIT.md)。两条相互关联修订为固定value-span的完整gate-feedback闭包/泄漏、残差到动作信用区间及有限步裕量；不是两个新D候选。原收缩/平坦谱反例继续成立。数学条件、贡献差异与实验未知分开记录，旧5张卡不抵扣活动池，20/15目标不变。[实际配置读回](sources/REPAIR_AUTHORIZATION_READBACK.json)与修复交付分开；同任务保持启用，本轮未调用run_now或新建任务。

R01 v2 的[修订推导](repairs/R01_VALUE_SPAN_AND_CREDIT_QUOTIENT.v2.md)不再把模型本身压成小 value-width：完整名义记忆 `S` 保留，仅压缩决策相关切向/信用商 `U=XW`。非退化步上，固定 `W` 对所有切向精确闭合要求 gate 协向量满足 `G=GWW^T`，目标信用还要求 `C=CWW^T`；相应行空间下界、时变基的核包含条件、泄漏递推与两个 2×2 反例均已保留。独立最终字节数学/来源审查接受其为“数学有条件成立的 Delta 特化理论控制”，但通用 lumping、goal-oriented/time-varying model reduction 已覆盖核心机制；原创性、同预算优势与实际效果未闭，因此仍不计 D 候选，计数保持 5历史/0活动/0准入/0选择。

R06 [选择性真实性审计](repairs/R06_SELECTIVE_VALIDITY_AUDIT.v1.md)沿 R05 增加真实随机审计：在选择时 propensity 可预测且 positivity 成立时，HT/AIPW 可点估计 `E[YZ]`，并给出 residual-aware 审计分配与条件 no-write 认证接口。独立最终字节审查实际修正了可行性/退化条件和论文、代码定位。普通真实性 `Y` 不等于理想动作 `r`，完整 horizon `Z` 也通常不是在线 prefix 可见；主体机制又与 HT/AIPW、Neyman、two-phase validation 和 active testing 直接碰撞。因此 R06 park 为 control，不计 D 候选；5历史/0活动/0准入/0选择及20/15短缺不变。

实际服务：复用 scheduled_authoring_continuation 任务 `6ac78ded796081918d2123402544d760`；按小时续接。此文件不是启动回执，连续执行未经证明。原代码阶段已完成/停用历史保留。

恢复入口：同commit的 PROGRESS.json、method-batch.json、项目 research/workflow-checkpoint.json。

## 2026-10-09 重走第2步

【2026-10-09 09:42 Europe/London 用户反馈：重走第2步】
用户原话：“我觉得你继续做数学推导然后或者看看有没有其他的结合方式或推论可以优美的解决一些问题，根据这轮的发现去重走2”。当前安装的 research-autopilot 技能可调用；沿用它，不重新安装插件，不把另一个项目的 autonomous-rsi 分支当本项目运行版本。
从当前零活动候选及上一轮条件结论重新定位问题（第2步），而非只继续扩展 rejected/ 目录。优先恢复 research/delta-discovery-2026-10-08/STEP2_REENTRY_2026-10-09.zh-CN.md 及其后续记录：完整状态 Jacobian 与冻结路径的差；修改有效性与未来查询几何的联合条件矩，而非独立 Bayes gate 加平均 metric；二次风险的充分条件矩与 diffusion 分布采样的必要性边界。保持 Delta 主线，同时认真探索具有必要数学相互作用的结合、统一和有价值推论。
已有 no-go 只在已证明的条件内适用；改变信息、目标、状态或假设后必须重新推导，不能把所有相关组合一概判死。既有简单组成不计新方法，但不得强行要求每个成果都引入“新因果证据”或改变部署递推；有价值的理论/表示/目标/计算构造也可成为研究成果，按相应贡献义务审查。禁止只换 loss 名称、坐标或超参数凑数。新的充分矩推导属于待查重线索，不是已经原创或科学准入。
第2步需要推导出可证伪的自然问题与成功/失败条件，补读相应真实论文/代码/原生benchmark后才推进候选构造；完整方案与独立审查前不计D编号。源状态保持5历史/0活动/0科学准入/0选择，除非有真实新证据。保留20/15目标短缺，数学阶段不执行模型代码或实验。每轮交付实际推导及决定，不只路线规划；复用同一任务、同一main和累计历史。

入口：[实际推导与决定](STEP2_REENTRY_2026-10-09.zh-CN.md)。任务身份和计划保持不变。

## 完整任务指令

使用当前 research-autopilot，在实际 ChatGPT Work 宿主中继续我已授权的 Yunbo-max/latent-world-model 项目 Delta 数学发现。用户于 2026-10-08 23:42 Europe/London 请求：“我觉得你要对于delta做数学推导吧10-20个你慢慢搞，后台任务”。上一条纠正是 diffusion 是可选方法，不是主要创新。以 20 个实质不同、数学成立的候选为目标，逐项审查后排名并按既有流程选择前15；不为凑数伪造原创性或推导。如果只找到10–19个成立候选，诚实记录数量与20/15目标短缺，不宣称完整选择。此阶段只完成数学、来源与可行性审查，不生成新候选模型代码、不设计完整可执行实验矩阵、不启动任何实验。

这是已有项目后台任务 6ac78ded796081918d2123402544d760 的新数学阶段，保留身份与hourly计划，不创建重复任务。旧“完成原方案全部代码”阶段已交付并停用，不恢复旧源码目标、不重新解释其完成标准。实际服务为 scheduled_authoring_continuation；定时启用与run_now接收不等于连续执行、当前运行或交付完成。以真实平台Work模式/调用证据和服务状态报告执行。当前配置会话是Work Mode；未来宿主未知时保存交接、报告一次具体问题，不用付费API、本地LLM或其他云服务替代，不虚构后台持续运行。

恢复最新literal main及同commit的 AGENTS.md、research/workflow-checkpoint.json、research/DELTA_FAILURE_MODES_2026-10-08.zh-CN.md、research/DELTA_DIFFUSION_DIRECTION_2026-10-08.zh-CN.md、research/ORIGINALITY_MATH_REVIEW_2026-10-08.md 和 research/delta-discovery-2026-10-08/GOAL.md、PROGRESS.json、method-batch.json。启动前最后读回的基线为27a189bd82515f06217d725a800650d7c44fbb4f；始终读取实时main，不把该SHA当永久最新。旧六路线暂停并行探索；旧Q01历史批次1 constructed/0 qualified/0 selected保留、不反向认证。新的Delta批次使用自己的ID和来源；旧不合格Q01是历史记录，不是当前活动候选。整个当前目标最多20个活动候选，保留否定、合并和淘汰记录。

读取同一当前skill revision的 SKILL.md、workflow-harness、web-background-work、math-analysis、math-operation-graph、math-derivation-paths、method-verification、research-quality-bar、literature-evidence、repository-round-trips，以及具体分析需要的模块。这是web_supervisor：可读论文、实际源码和原生benchmark资料，可写数学与审查记录；不得执行项目代码、软件测试、训练、推理、评分、GPU作业、数据/模型下载，不能通过子代理绕过。允许纯只读证据验证与标准库文件/哈希处理；不要冒充实验。沿用单卡RTX2080Ti、0.1B/1B预训练target-token预算作为后续可行性背景，不启动它、不增加付费服务，不使用Docker。无需重新问相同GitHub/HF/GPU intake；无HF上传目标且此阶段不需要上传。

研究主线是Delta状态更新的缺陷及其残余问题，不是将流行模块拼成20套架构。优先围绕：局部纠错与跨query干扰；仍有效关联的保护/真实修订时释放；更新传播和长期保留；有限精度、可辨识性及容量冲突；预测目标与历史ridge/当前key重建的差异；计算、并行化与数值条件限制。先做失败机制和成功特例的数学区分，不把未测的项目故障写成事实。不强制每类固定数量，不将参数、噪声尺度、seed、消融或同构公式视为不同方法。Diffusion只在推导证明其具体必要作用时纳入，也保留普通远期CE、teacher监督和简单预测器为替代解释。

保留并复用已经审查的控制数学：
S是key-by-value；S_t=(I−β_t k_t k_t^T)D_t S_{t−1}+β_t k_t v_t^T，不能交换D和rank-one因子；相对post-decay的Δo(q)=β(q^Tk)e。未来传播P是按实际顺序乘积，仅冻结未来特征、相同未来输入时精确；完整非线性网络需Jacobian。稳定不等于信息保留。指定保护query子空间的projection/soft-preconditioned edit是已知几何，保护与新写入冲突时可能不可行或范数巨大。有限维实状态没有无条件有限bit容量结论；有限精度/噪声或固定线性读出条件必须注明。当前残差本身不足以区分真实修订与近key的不同事实；上下文网络可能已有区分能力，不能作无条件否定。

完成以下实际产物：
1. 定向近邻图：原始DeltaNet、GDN、KDA、RWKV-7、Preconditioned DeltaNet(2604.21100)、Gated DeltaNet-2(2605.22791)、Gated KalmaNet(2511.21016)、QED(2608.13668)、Sparse Delta Memory(2607.07386)、DeltaProduct、相关protected/orthogonal/slot/fast-weight方法；必要时扩展引用。阅读真实公式、假设、算法与作者代码接口，记录固定版本/文件/函数/section。QED此前仅官方摘要，全文公式审查尚缺；不要把摘要当完整分析。GKA实际是H/U统计和有限次Chebyshev近似query solve，不是每token显式exact Kalman inverse。PDN非对角inverse-Gram理论、实际对角稳定预条件必须区分。GDN2左侧write方向仍k。简单协方差、erase/write解耦、每token多步Delta、多slots/稀疏路由都已有近邻；直接复现归baseline，不计原创候选。
2. 每个候选完成实质math-card：明确formal object及目标/采样/估计器/实际update；选择并实际执行适用数学操作；写连续的推导步骤和依据、显式假设与条件状态、由结果导出的可计算构造、相对Delta和最近方法的真实变化、区别性预测、失败边界/反证、强简单替代与判别比较、复杂度/状态与信息访问。不能只有名字、loss列表或熟知等式；未完成新构造留lead，不计数学合格候选。
3. 独立语义数学审查每卡：支持真实可用代理并行推导/审查，一个集成writer；按必要范围安排独立审查，保存实际身份、精确artifact SHA256、审查推理和未闭条件。检查维度、顺序、条件、可行性、极限/反例、等价性与隐藏代价。不能用全勾选或自填verified替代审查。发现错推导就修正或淘汰，保留历史。不同卡的实质 distinctness 必须核查。
4. 为候选的自然科学问题读取既有公开benchmark的原始文档/数据格式/native scorer/基线代码，复用有效既有bAbI/LAMBADA资料但不可假定它们足以测试所有保护/修订/容量主张。记录每个主张能否由既有原生任务衡量、资产可取得状态、最强简单baseline及大致成本条件；没有合适可测量对象保留measurement gap，不造benchmark、数据、案例、标签、metric或结果。这是feasibility/判别思路，不是此阶段完整实验设计或dispatch。
5. 维护新的 research/delta-discovery-2026-10-08/PROGRESS.json、method-batch.json、cards/与reviews/、CLOSEST_WORK.md及RANKING.md等必要实质记录，尽量复用少量清晰入口。遵循skill math-card/method-review/method-selection schemas并用实际字节SHA绑定；证据checker通过不证明原创/数学真理。每卡按已读原文与实质对照说明机制是否已覆盖、残余差别与未解决问题，不宣称首个/完全全新。
6. 完成整个池的审查和rank后给出顺序、每项比较理由（问题价值、数学后果、最近工作差别、预测、可行性/总成本）；按默认top15留下selected记录与selection-review，其他作为reserve。完整性不足不得篡改target或宣称selection_verified。输出一份直白中文总结：每个idea解决哪个缺点、数学新意在哪里、与已有工作差什么、最可能失败在哪里，以及最终最值得继续的2–3项。选中15是池排序，不等于推荐同时拼成15模块或批准新实验。
7. 每个实质里程碑推送到Yunbo-max/latent-world-model的literal main；一个integration writer，读取实时parent，expected_sha+force=false保并发，逐文件在精确commit读回。冲突就重读合并，不force/reset，不覆盖他人文件/旧源码/Local记录。只更新本Delta数学packet和必要checkpoint，避免无关工程更改。
8. 每轮从未闭的最早前提继续完成实质阅读/推导/审查，不只不断产出计划。可在单次宿主额度内完成若干完整卡；剩余保留并由同任务续接，不为每个模块建立任务。若已结束的运行恢复，先核对worker/task和main是否已有推进，避免重做/重复写入。实际科学前提缺失只阻塞依赖项，独立可行工作继续。

阶段完成：20个目标候选均有真实数学卡与审查、distinctness和nearest-work记录、全池排名与top15选择/审查、中文总报告，且main精确readback完成。到此停用同一个任务；不要转入新代码/实验或重新开启旧代码goal。真实不可解除的权限、来源、数学短缺或必要人类判断出现时，保存具体阻塞、已完成项和下一合法动作；重复同一阻塞不反复通知。只有实质里程碑、需用户处理的新阻塞和最终交付时通知。后台已配置、run_now已请求、实际运行、数学完成、原创性审查和实验验证分别报告。

补充入口：[联合风险详细条件与独立审查](STEP2_JOINT_CONDITIONAL_RISK.md)。与上述第2步笔记属于同一线索，不重复计候选。

最新续接：[真实预测监督、rank-one可达性与决定充分性](STEP2_OBSERVED_PREDICTIVE_TARGET.md)、[固定来源/接口/原生审查](sources/OBSERVED_PREDICTIVE_TARGET_SOURCE_AUDIT.md)、[独立最终字节审查](reviews/STEP2_OBSERVED_PREDICTIVE_TARGET.review.md)。它替换预测目标中的不可得 validity 标签，未认证语义修订；与旧 latent 工程源码明确分开。同一Step2线索，5历史/0活动/0准入/0选择保持，20/15目标未降级，代码/实验范围不变。

进一步续接：[决定充分性的低秩边界与 Delta 动作秩控制](STEP2_ACTION_SUFFICIENT_RANK_CONTROL.md)、[来源/代码/native 审计](sources/ACTION_SUFFICIENT_RANK_SOURCE_AUDIT.md)、[独立双重审查](reviews/STEP2_ACTION_SUFFICIENT_RANK.review.md)。固定 SPD 二次 regret、线性 feature/head 下的宽度风险是加权 RRR 的尾奇异值；Task-Sufficient Contraction、Bayes quotient、DSSR 与 RRR/EYM 已分别覆盖静态充分性、递归 future-reader 评分和低秩截断。只保留随机信息依赖 metric × 完整递归 Jacobian × 因果可估计性的未准入残余；计数不变。

最新续接：[递归随机条件矩、完整 Jacobian 与因果动作误差界](STEP2_RECURSIVE_RANDOM_METRIC_CONTROL.md)、[固定来源/代码/native 审计](sources/RECURSIVE_RANDOM_METRIC_SOURCE_AUDIT.md)。固定 teacher-forced 后缀上的联合对象严格化为 GGN 加权的变分可观测 Gramian；精确 Hessian、prefix-only 条件估计和自由运行反事实边界均已分开。主要部件被 observability/GGN/DDP-iLQR/DNI/RTRL-UORO-e-prop/DSSR 覆盖；只保留 Delta rank-one 结构能否形成更低成本联合 estimator 的未准入残余，计数不变。


## 2026-10-09 新增 Delta 自改进更新器授权

【2026-10-09 12:48:59 Europe/London 新增授权：Delta 自我改进更新器的数学发现】
用户原话：“我认为这个方向值得深入，但目前它是候选研究路线 我觉得你可以把这个扩展下搞idea在后台”。接续同一 latent-world-model / Delta 数学目标，将“学习如何更新自身 Delta 记忆，区分有益覆盖与破坏性遗忘”加入并优先展开。这里 RSI 指语言模型递归自我改进，不是修改 Research Autopilot 插件本身。不是新项目，不建立第二个任务或writer；不借用 theory/test10.8/4d 的代码、预算或执行授权。

本次只扩展数学、最近工作审查和原生测量可行性。保留原20候选/全池审查/前15目标及历史；下列是推导入口，不是6个已成立或原创候选，不要求固定数量，更不要求把它们拼成6个模块。Diffusion仍是可选辅助，不作为主创新。原候选模型代码、完整可执行实验矩阵、软件测试和训练/评分均不在当前数学阶段启动。未来代码/完整设计义务保留，不能因本次数学扩展假称已经完成。

执行前固定实时main，恢复全部已完成推导、碰撞、独立审查和累计历史。当前bootstrap只读到87380653675efecf29335f522190a3a95bb6f67b，该SHA不是永久最新；该revision已包含 STEP2_RECURSIVE_RANDOM_METRIC_CONTROL.md 及其review/source audit，完整Jacobian、GGN/DDP、RTRL/UORO/e-prop、DNI及DSSR有已记录碰撞。不要重复推导并换名计数。先核对真实服务运行者/写入归属，保持一个集成writer；当前bootstrap只修改该任务指令，不并发改项目文件，不再次run_now。下一次可接续时将本次授权、填好的研究目标和任务配置实际readback记录同步到本Delta GOAL/PROGRESS/checkpoint，保留既有字段和来源。

研究问题：在同样可见前缀、记忆容量和计算预算下，能否利用Delta的结构，学习更有效的更新规则，在吸收新知识/任务时减少仍有效旧能力受损，并改善后续学习效率？先区分参数级连续SFT、跨会话持久化fast weights和单上下文状态适应；不能将上下文记忆提高直接解释为基础能力提升。Transformer不擅长SFT、attention必然导致遗忘、冻结主干即不遗忘、Delta自然解决遗忘均不是已证事实。

以S为key-by-value，e=v-S^T k。先从标准Delta ΔS=β k e^T、其他查询改变Δo(q)=β(q^T k)e及已审查的完整后续递推出发。定义可见信息过滤、更新器状态/参数、外部反馈和未来损失；部署时不得访问未来token、任务答案、旧知识有效性oracle或内部理想edit标签。未来真实token可仅作为训练监督，其预测误差不自动提供事实有效性标签。

优先探索以下相互关联但尚待甄别的推导入口：
1. 更新干扰的可行性和容量边界：新写入误差与仍有效旧查询损伤的联合几何；保护空间与修订空间重叠时的最小风险、不可行/病态边界。硬投影、soft预条件、EWC/GEM/A-GEM/OGD、已审查rank控制为强简单对照；只有实质残余差异可成为候选。
2. 保护与释放的可辨识性：在未知知识是否过时的条件下，联合更新有效性与未来查询/target几何；明确能从真实因果输入及反馈估计什么、不可识别什么、误释放风险及额外证据成本。已有Bayes条件矩、变化检测/e-process/revision控制不能重新包装计数。
3. 延迟反馈对学习更新器的价值：推导多步post-update真实未来损失对写入方向/力度及更新器的梯度，区分固定未来特征和完整Jacobian、状态梯度和元梯度、有限horizon偏差。查重MAML/learned optimizers/TTT/SEAL/HOPE/DSSR/RTRL/critic/eligibility trace，要求Delta结构带来可证明且有条件的计算或统计后果；普通远期CE和直接action predictor是必须比较的同信息替代。
4. 自修改更新器的稳定性：联合状态包含记忆和更新器内部状态，推导耦合Jacobian、反馈放大、稳定而不学习/学习而遗忘的边界；冻结outer-trained更新器只是元学习策略，部署中更新记忆只是适应，改进更新器仍需真实反馈与未来任务证据，不能凭循环/RL标签宣称RSI。
5. 快慢记忆间巩固的条件：从可靠证据、预测贡献和跨任务可转移性推出何时允许从快状态进入较慢参数，分析巩固偏差/损伤和长期成本。多时间尺度、replay、distillation、CMS及快慢权重本身已知；需证明具体Delta巩固机制有残余作用，不能靠增加容量/保存原文获得不公平优势。
6. 反事实更新收益的因果可估计性：比较写入/不写入/替代更新后的未来损失，在相同信息和资源下推导估计偏差、方差、有限反馈与数据泄漏边界。不能把模型自评或自生成未来当新的外部证据；保留固定Delta、普通SFT/LoRA+replay、固定learned updater和同容量记忆为适用对照。

来源启动入口（必须全文公式+实际作者实现检查，不把摘要当完成）：
HOPE/Nested Learning https://arxiv.org/abs/2512.24695 与官方 https://research.google/blog/introducing-nested-learning-a-new-ml-paradigm-for-continual-learning/；
SEAL https://arxiv.org/abs/2506.10943、作者 https://jyopari.github.io/posts/seal、实际作者仓库 https://github.com/Continual-Intelligence/SEAL；
Titans https://arxiv.org/abs/2501.00663；再按残余问题加入TTT、learned optimizer、continual learning等primary sources。SEAL作者已报告连续self-edit遗忘，作为重要负证据保留。HOPE并不证明无限或保证递归自我改进；第三方HOPE实现不冒充作者代码。

交付：每个实质线索有formal object、假设、连续推导、可计算构造或有价值理论、预测、反例/失败边界、最强简单替代、最近论文/实际实现差异、资源/信息成本、可由既有原生benchmark衡量的主张与measurement gaps。区分训练后有适应性/学到更新策略/部署中更新策略/跨新任务提高学习效率，分别列所需证据。已覆盖机制归baseline/control；推导成立但原创性/测量未闭的保留lead，不计资格。独立review绑定真实artifact字节与assignment，全池按原合同去重排序，最终给中文直白结果和最有希望的2–3项，不能承诺必有新架构或永久变强。

沿用该项目已绑定的可信skill/workflow版本；读取当前真正适用模块并记录来源，不能因为另一个项目已安装autonomous-rsi而静默替换本项目模式。此任务是研究模型的RSI可能性，不安装daemon、不改插件、不发起付费API/云算力，不制造新host。保留同任务和原hourly触发；每轮应完成实质推导/核查并交付main精确readback，只报真实新证据、未完成项和下一动作。当前生效的已有Worker可能仍使用上次指令，更新配置不等于向正在执行的worker热注入，不声称已开始新增方向。


本轮实际入口：[耦合更新器稳定性与保护纤维](STEP2_COUPLED_UPDATER_STABILITY.md)。本项目沿用已绑定 restored-research-baseline，不采用另一个项目的 autonomous-rsi 技能分支。配置读取记录与来源哈希见 sources/RSI_AUTHORIZATION_READBACK.json；它不证明持续运行或科学完成。

本轮独立审查：[条件数学及修订历史](reviews/STEP2_COUPLED_UPDATER_STABILITY.math-review.md)、[来源/后果边界](reviews/STEP2_COUPLED_UPDATER_STABILITY.source-review.md)。两位实际工作者分别审查最终字节；来源作者的自身审计不冒称第二次独立来源审查。

最新续接：[完整闭环 scalar-gate tangent 秩增长与截断误差控制](STEP2_CLOSED_LOOP_RANK_GROWTH.md)、[primary/作者接口/native 审计](sources/CLOSED_LOOP_RANK_GROWTH_SOURCE_AUDIT.md)、[独立数学](reviews/STEP2_CLOSED_LOOP_RANK_GROWTH.math-review.md)与[来源审查](reviews/STEP2_CLOSED_LOOP_RANK_GROWTH.source-review.md)。它证明 frozen-path rank-one 不能无条件外推到 state-dependent updater，但不把矩阵秩冒充一般内存下界，也不构成新压缩器、RSI 或候选准入。计数和20/15短缺不变；代码/实验范围不变。

进一步续接：[收缩、有效秩与无偏截断的条件边界](STEP2_EFFECTIVE_RANK_TRUNCATION_CONTROL.md)、[primary/作者接口/native 审计](sources/EFFECTIVE_RANK_TRUNCATION_SOURCE_AUDIT.md)、[独立数学](reviews/STEP2_EFFECTIVE_RANK_TRUNCATION.math-review.md)与[来源审查](reviews/STEP2_EFFECTIVE_RANK_TRUNCATION.source-review.md)。严格收缩不推出低相对有效秩；对数绝对 epsilon-rank 需要更强的低秩注入、保秩传输和 fading-age 假设，并可能只是信用消失。ARTBP、adaptive TBPTT、randomized telescopes、稳定递归模型和既有 sensitivity/sketch 方法构成主要碰撞。处置仍是 control/no D；计数和20/15短缺不变，代码/实验范围不变。

## R02 v1 randomized-action repair

The passive counterfactual-write line is repaired only for a new estimand: average finite-action total effects under logged randomization, real delayed loss, overlap, and a common continuation policy. Final-byte math and source reviews passed. Standard AIPW/sequential OPE is the dominant mechanism; retrospective source release, semantic validity, long-run RSI and native mechanism measurement remain unresolved. R02 is a control, not a D candidate, and counts remain 5 historical / 0 active / 0 admitted / 0 selected.


## R03 修复：保护感知的随机 Delta 日志

R02 的随机 write/no-write 解决了平均动作效果的可识别性，却没有限制探索本身对仍有效旧查询的损伤。R03 以同一 propensity 同时控制 AIPW 方差和 Delta rank-one 局部保护损伤：对保护查询二阶矩 G_p 与 value 度量 M，单步输出位移精确为 d_a=α_a²β²(eᵀMe)kᵀG_pk；带有效旧标签时又得到平方风险交叉项和充分上界。严格 positivity 与损伤预算存在显式不可行边界，二元最优 propensity 是受安全上界截断的 Neyman allocation。

最终字节数学/来源复审接受该条件控制。但 SEPEC、Safe Optimal Design、CLUCB/SEA、stage-wise constrained bandits 和标准 OPE 已覆盖安全且信息高效的 logging design；LongMemEval/SEAL 只覆盖终点更新或遗忘，不原生提供 Delta propensity、保护有效性或 counterfactual scorer。因此 R03 在第一次修订后 park，不分配 D 编号。计数仍为 5历史/0活动/0科学准入/0选择；实际效果未知，未执行代码或实验。


## R04实际修复交付：迁移当下不变，还要修复下一次更新

[修订推导](repairs/R04_CONSOLIDATION_DYNAMICS.v2.md)把快状态迁入慢参数具体化：M+=C、S−=C当下保持总读出，但原快Delta下一步会留下(I−P)C差。补偿完整递推能完全保持原轨迹，是单W Delta的等价表示；用总残差且只衰减快状态则真正改变保留行为，差别是有序强迫E(I−D)M。

独立审查实际debug了EC=0不保证E(I−D)C=0的错误：非均匀decay改变方向。v1原字节/二维反例保留，v2修复并重新审查最终字节。旧标量反例也复查：总残差能修复未释放/双记账，但慢保留对有效知识有益、对过时知识可能有害；C的有效性尚未识别。

来源补读Sleep扩容/seeding/reset、HOPE CMS，以及SynControl作者代码和SEAL/LongMemEval原生接口。主要快慢机制已知，但不把本条件理论逐式覆盖或整个巩固问题死亡当成结论。R04完成条件repair/control；理论原创性/同预算优势/原生机制测量未闭，实验未知。当前5历史/0活动/0准入/0选择，20池/15选择缺口保留。

## R04 v3 最终有界修复：联合收益—损伤选择

[第三次修订](repairs/R04_CONSOLIDATION_DYNAMICS.v3.md)不再只说“选可靠的 C”，而把慢端/快端可表示接口、v2 的有序 `E(I-D)` 传播、真实未来输出风险和保护约束拉回同一低维控制 `z`。普通二次风险给联合充分矩 `G,g` 与受约束 normal equation；它们是已知决策数学，不冒称新定理。均匀衰减、无后续写入的标量特例给出清楚边界：仍有效概率 `p` 只有超过不做巩固时的自然存活率 `alpha^T` 才应正迁移。这个阈值是通用快慢决策边界在本 Delta 子模型中的实例，并非 Delta 独有。

独立审查修正了正则化两世界、frozen-law、正交保护基和“相关不必严格变差”等措辞。来源复核完成 Dual-Layer Agentic Memory v2 全文公式、Leimer 2019 快慢选择公式、Goldman 2024 作者 notebooks，并区分两篇同名 Sleep；cost-aware routing、选择性慢巩固、普通 normal equation 均已有强近邻。故 R04 在第三次修订后 park：数学条件结果保留，贡献差异与原生机制测量未闭，实验未知；计数仍为5历史/0活动/0准入/0选择。

## R03 v2：把局部损伤改成耦合时域证书

[第二次修订](repairs/R03_COUPLED_HORIZON_SAFETY.v2.md)把 R03 v1 的单步 `rank-one` 位移扩展为 `即时 Delta 注入 × 完整 memory/updater 增量增益 × 未来保护输出敏感度` 的有限时域能量界，并把它回代到安全 logging 的 propensity 可行性。独立数学审查先返回 REVISE，要求补齐 endogenous query 的复合 map、部署前 `F_t` 可测的 simultaneous bounds、随机动作期望安全与逐动作 hard safety之别、floor-simplex 与 PSD/shared-law 条件；修正后的最终字节通过复审。

结果在明示条件下成立，但不是新算法：SEPEC/Safe Optimal Design 覆盖安全日志优化，小增益/保护纤维覆盖动力学界，RTRL/UORO/e-prop 等覆盖完整 sensitivity。当前只保留“Delta 即时注入如何改变长期安全—positivity 可行性”的窄理论接口；自由运行总效果、同预算证书优势与原生 joint propensity/protected-validity/counterfactual 测量仍未闭。R03 在第二次修订后 park，不计新 D；计数仍为5历史/0活动/0准入/0选择，没有执行代码或实验。

## R05：从不可识别改成部分识别，而不是直接否定

[v1 原推导](repairs/R05_PARTIALLY_IDENTIFIED_VALIDITY_GEOMETRY.v1.md)、[v2 审查修订](repairs/R05_PARTIALLY_IDENTIFIED_VALIDITY_GEOMETRY.v2.md)与[最终 v3](repairs/R05_PARTIALLY_IDENTIFIED_VALIDITY_GEOMETRY.v3.md)把“未知语义有效性 `r` 与未来敏感度 `Z` 的联合矩不可得”改造成可计算的部分识别问题。只知道 `p=E[r]`、`mu=E[Z]` 和共同上界 `U` 时，`m=E[rZ]` 落在锐利 Fréchet/support 区间；区间中点给出 minimax-regret gate，且存在统一优于 no-write 的正 gate 当且仅当下界 `m_->0`。完整 `Z` 边际可用分位耦合进一步收紧，但仍不能凭边际点识别联合收益。

独立审查保留并修复了矩阵 sharpness、原子端点、动作前状态、`A=0` 除零与效益语义。来源审计确认 Fréchet/partial identification/Gamma-minimax/moment-DRO 是直接近邻；ROME/CounterFact、EvEdit、EasyEdit 与 sequential editing 只给行为 endpoints，不原生提供逐次 `r,J,Z,m` 或配对潜在结果。故 R05 是条件数学 control，不分配 D 编号、不进入 top15；计数仍为5历史/0活动/0准入/0选择，实际效果未知且未执行代码或实验。

## R07：把“真实性”修成“写入动作边际”

[修订推导](repairs/R07_VALIDITY_TO_ACTION_MARGIN.v1.md)补上 R06 最早的语义断点。对动作强度 `a∈[0,1]`，固定参考分布下的局部二次风险变化写成 `Δ_Y(a)=h_Ya²-2a(Yb-c)`：`b` 是新 target 的一阶收益，`c` 是仍有效保护对象的有符号一阶代价，`h_Y` 是曲率。由此得到精确边界：存在有益的正小步当且仅当 `Yb-c>0`；完整写入优于不写当且仅当 `Yb-c>h_Y/2`；完整写入还是连续最优才要求 `Yb-c≥h_Y`。因此“事实为真”本身不等于“现在应该完整写入”。

Delta rank-one 写入把这些量具体化为可检查的 key/residual/JVP 二次型，但旧反例仍成立：只知道 `Y`、收益幅度和曲率，若不知道保护交叉项 `c`，两个世界可给相反动作。修复后的贡献是一个条件性 action-margin control，不是新架构。KnowledgeEditor、AlphaEdit、O-Edit、LyapLock 与普通 cost-sensitive/凸二次决策覆盖问题分解和主要机制；AToKe 虽提供历史/当前事实时间标签，仍不提供动作前 `(b,c,h)`、随机 propensity 或成对动作结果。故 R07 park，实验未知，候选增量0；总计仍5历史/0活动/0准入/0选择。


## R08：时间有效性不是释放动作，但可以接到有符号动作边际

[修订推导](repairs/R08_TEMPORAL_VALIDITY_RELEASE.v1.md)把旧的静态 posterior gate 与 martingale release 线索重新接到 R07 的动作几何。隐藏旧事实有效性 belief 只决定分支权重；真正动作由 `D_p(a)=h(p)a²-2q(p)a` 决定。固定 full action 时得到方向可反转的精确 posterior 阈值；固定 belief 时，保护交叉项仍能让两个世界选择相反动作。故“检测到事实过时”与“释放保护现在有收益”被明确分开。

动态时必须加入 switching cost 和 Bellman continuation `Gamma`；写入会破坏后续证据或改变 memory/updater state 时，myopic 阈值可被最小反例反转。联合 sharp belief interval 可给端点 robust certificate；one-step query value 属普通 Bayes VoI。BOCPD、POMDP/controlled QCD、Zhang–Choi 时间后验阈值、AToKe、StableEdit 与 RLEdit 已提供直接近邻。[来源审计](sources/REPAIR_R08_TEMPORAL_VALIDITY_SOURCE_AUDIT.md)和独立最终字节数学/来源复核均通过。R08 因此保存为条件 theory/control，不计候选；实验未知，计数仍5历史/0活动/0准入/0选择。

[v2 修订](repairs/R08_ACTION_DEPENDENT_INFORMATION_VALUE.v2.md)没有把抽象 `Gamma` 包装成新模块，而是在严格两阶段时序下把它算出来：对固定动作后 memory 和两个仿射终端风险，`B=min(L0,L1)` 可写成仿射和减绝对动作边际，故动作特定观测的价值精确为 `I_a={E|delta(P'_a)|-|delta(p)|}/2`。`Q_R-Q_K` 因而拆成即时/切换成本、动作后 memory 风险和差分信息价值；可选 query 再变成 `[I_a-kappa_a]_+`。同均值同方差的两个可实现 posterior law 仍可给不同价值，说明方差代理不足；Blackwell 顺序也只有在 prior、memory 和 loss table 相同才可比较。

独立最终字节审查修正了 interventional conditioning、零概率 signal、常数边际与来源题名/DOI/定位后通过。[v2 来源审计](sources/R08_V2_ACTION_DEPENDENT_INFORMATION_SOURCE_AUDIT.md)确认 EVSI、Blackwell 与 controlled-sensing POMDP 已覆盖主体机制；Delta 只提供 signed-margin 解释。R08 在第2/3次修订后继续 park，候选增量0、实验未知。只有出现同预算 prefix margin-law 优势、Delta 专属更小多步充分状态或原生 causal temporal action 对象才重开第3次。


## R09有限预算覆盖—保护修复里程碑（2026-10-10）

R09没有删除`NOGO_CAP_02`的反例，而是修正了“只能精确覆盖或完全不写”的目标错配。对任意矩阵编辑`Delta S`，在固定纠错量、保护位移`tr(Delta S^T G Delta S)`与Frobenius能量之间导出了精确Pareto前沿、奇异端点、预算可行性和双上限支持函数。普通Delta被证明是固定纠错下唯一的最小能量端点，并非被预条件方向无条件支配；`gamma=1`时原仿射覆盖路径仍奇异。

三路独立最终字节审查通过的是条件静态几何定理。逆Gram/RLS、零空间编辑及AlphaEdit+软冲突松弛与主要机制直接重合；动态`G`的因果可得性、同预算优势和原生保护—动作测量仍未闭，实际效果未知。因此R09作为control/theory停放，不分配D编号，活动/准入/选择计数均不变。重开条件是获得prefix-only同预算动态/动作加权`G`估计、强于通用约束最小二乘的信息/状态下界，或原生因果protected-action对象。

## R10等比特残差修复里程碑（2026-10-10）

R10保留D04的原反例：不随`A_t`传输的残差不能恢复原仿射轨迹；精确传输的残差又相当于保存第二份完整状态。本次patch补齐了有限比特问题。若后续转移、读取和损失只通过`L=W+C`消费双状态，且侧信息与metadata同样计费，则双码本可解码的`L`最多只有`2^(b_W+b_C)`个值，直接同等比特码本可以逐点复现同一解码状态。因此这一路没有无条件容量收益；嵌套均匀网格只是细网格的混合进位编码。

另一条“只让粗量化`W`进入递归、残差只改变后续写回时机”的路线是不同算子，可能因接口兼容/噪声整形而优于未经重训的细精度可见状态，但它仍可被同总状态数的有限状态机重标号，不能从传输恒等式推出普遍容量突破。来源与作者实现核查显示，该算子族已被低比特recurrent-state residual/direction memory覆盖；DAMP与STEPQuant又覆盖了持久性/读出加权的比特分配，其中STEPQuant作者代码已实现离散DP/拉格朗日分配与校准。

三路独立最终字节审查通过条件误差递推、同基数表示边界、算子分离和附加随机假设下的有限时域风险/水填充控制。它们不证明新方法或效果。R10在第一次修订后park，不分配D编号；计数仍为5历史/0活动/0科学准入/0选择，实验状态未知且未执行任何代码、训练或评分。



## R11顺序差压缩修复里程碑（2026-10-10）

[R11修订](repairs/R11_ORDER_GAP_COMPRESSION.v1.md)没有再把交换子当成应被消掉的误差，而是保留真实顺序差：两种相邻Delta写入顺序之差在key侧秩至多2；给定共同、因果的未来查询Gram，秩预算的最优误差等于加权奇异值尾和。若隐藏的二元语义顺序标签在可见信息中不可辨识，则共同估计量还有精确Bayes风险下界。旧反例被保留：同key时线性转移可交换，但affine write仍可不交换；正交key时顺序差退化为0。

三路独立最终字节审查修正了奇异G核空间秩约束、分支共享度量、binary proxy边界、suffix符号、完整状态与白化成本，以及作者代码/原生scorer固定版本。来源核查显示有序WY chunk与DeltaProduct已经保留顺序，weighted SVD是通用控制；现有group state-tracking只测非交换表达能力，不测有害覆盖selector或未来query Gram。故R11作为条件theorem/control在第一次修订后park，不分配D编号；计数仍为5历史/0活动/0科学准入/0选择，实验未知且未执行代码、训练或评分。

## R12子空间syndrome读出修复里程碑（2026-10-10）

[R12修订](repairs/R12_SUBSPACE_SYNDROME_READOUT.v1.md)保留了原checksum路线的语义反例：压缩不能凭空判断revision/coexistence或latest truth。本次把错误目标改成checksum实际能回答的数值问题。若编辑限制在`Delta=BA`，syndrome为`H^T Delta`，则它能对所有允许编辑精确恢复保护读出`Q^T Delta`，当且仅当`ker(H^TB) subset ker(Q^TB)`；失败时存在同syndrome、相反保护输出的成对不可辨识编辑。伪逆给出噪声与子空间泄漏界，单次rank-one Delta是其一维特例。

三路独立最终字节审查进一步证明了强简单对照：对任意已知未来保护函数族，联合行空间维数为`s`时，任何精确syndrome至少需秩`s`，直接保存`JA`也只需`s d_v`标量。因此自由设计的`H`只是充分统计量换坐标，没有标量容量优势；语义有效性仍未识别。来源审计固定了OSE/压缩感知、FLA Delta接口及LongMemEval scorer边界，但精确定理优先权仍为`INCONCLUSIVE_EXPAND_SEARCH`。R12作为条件theorem/control在第一次修订后park，不分配D编号；计数仍5历史/0活动/0科学准入/0选择，实际效果未知且未执行代码、训练或评分。



## R13 动态协向量保护修复里程碑（2026-10-10）

[R13 三线筛选](repairs/R13_REPAIR_LINE_SCREEN.md)实际重推了动态读出、retroactive rollback 与 reciprocal cycle 三条较有希望的失败线索；后两条分别落回 exact-record omission/通用 retroactive ordered product，以及 bidirectional residual/CCA/GSA2 控制，因此有界停放。另检的 set-valued query quotient 也与 functional observer/set-membership optimal recovery 直接相邻。

[选中的 R13 修订](repairs/R13_DYNAMIC_COVECTOR_PROTECTION.v1.md)把固定保护读出改为穿过已实现仿射 Delta 转移的动态解码。精确条件是 \\(\\ker A_t\\subseteq\\ker Q_{t-1}^\\top\\)；在 exact overwrite 时退化为 \\(Q_{t-1}^\\top D_t^{-1}k_t=0\\)，否则两个不同旧状态会塌缩为同一 post-state。覆盖前的重叠分量按 \\(1/|1-\\beta\\|k\\|^2|\\) 放大，affine offset 只能扣除已知写入，不能恢复被奇异方向抹掉的信息。

三路独立最终字节审查修正了 endpoint/intermediate reader、full-Jacobian/VJP、offset-free singular proof、总状态和比特精度、对照公平性及来源固定。最终数学只作为 conditional theorem/control 通过。对当前“保存既定数值读出”的目标，直接保存 \\(Y\\) 只需 \\(p d_v\\) 标量，严格优于持久化 \\(Q_t,C_t\\) 的 \\(p d_k+p d_v\\)；functional observer、广义逆、adjoint 与 reversible memory 又覆盖主要机制。因此 R13 第一次修订后 park，不分配 D 编号；计数仍为5历史/0活动/0科学准入/0选择，原创性未建立，实验未知且未执行代码、训练或评分。


## R14 后验 provenance 写入修复里程碑（2026-10-10）

[R14 三线筛选](repairs/R14_REPAIR_LINE_SCREEN.md)选择了 provenance identity-oracle 缺口：原张量绑定公式本身不必错误，但它把“新观察属于哪个实体/版本”作为已知 code 输入，因而不能作为可部署 revision selector。

[修订推导](repairs/R14_POSTERIOR_PROVENANCE_WRITE.v1.md)把 oracle code 改为因果可见信息下的槽位后验 \(\pi_i\)，并在带有有符号保护代价和二次损伤的局部风险下导出逐槽 Bayes 动作
\[
a_i^*=H_i^{-1}(\pi_i r_i-\bar c_i).
\]
同一后验直接写入 tensor address 则共享残差 \(v-\sum_i\pi_i y_i\)，一般不等于上述动作；两槽反例中其风险与 no-write 都为1，而逐槽 Bayes 风险为1/2。对不可区分身份又得到精确正的 ambiguity floor，说明记忆几何不能制造缺失的身份证据。等写入数预算下，最强同信息对照是按 \(G_i=b_i^\top H_i^\dagger b_i\) 选择 top-\(B\) 的直接槽位路由，而不是 tensor lift。

三路独立最终字节复核通过条件数学、固定来源/作者接口、反例与成本边界。HME/加权LS-RLS、PKM/FwPKM/SDM/ARM 路由记忆、tensor binding/fast weights 及本项目 R07/R09 保护二次几何已覆盖主体机制；原生端点又不联合暴露校准身份后验与成对动作后果。故 R14 在第一次修订后保留为 theorem/control 并 park，不分配 D 编号；计数仍5历史/0活动/0科学准入/0选择，实验未知且未执行代码、训练或评分。


## R15 有限动作 intervention-rank 修复里程碑（2026-10-10）

[R15 三线筛选](repairs/R15_REPAIR_LINE_SCREEN.md)重查 counterfactual write utility、causal polynomial future product 与 exact-flow implicit Delta。主线选择了“有限动作子空间是否足以让 delayed write credit 可辨识”；多项式未来线回落到 R09/R11 与未知后缀，noncommuting exact-flow 仅保留为尚缺完整公式/代码查重的后续 lead。

[R15 修订](repairs/R15_INTERVENTION_RANK_BOUND.v1.md)没有假定低维注入自动提供反事实证据，而是显式加入 exact quadratic response surface。若
\[
\mathbb E[Y\mid\mathcal F,z]=\alpha+b^\top z+\tfrac12z^\top Hz,
\]
则全部系数可辨识当且仅当 lifted feature Gram \(G=\mathbb E[\phi(Z)\phi(Z)^\top\mid\mathcal F]\) 满秩；任意 \(d\in\ker G\) 都给出日志支持上相同、未试动作上不同的两世界。线性 \(r\) 维动作至少需要 baseline 加 \(r\) 个独立方向；任意二次响应需要 \(1+r+r(r+1)/2\) 个独立 feature rows。标量 gate 的 paired baseline 加两个非零幅度可分离斜率/曲率，而 write/no-write 只能识别端点差。

独立最终字节审查补正了增广状态注入维度、quadratic feature 的四阶矩条件、固定条件层 CRLB、paired intercept cancellation，以及 fixed recorded descendants 与 lawful common-random-number free-running pairing的区别。来源/作者接口审计确认 response-surface/optimal design、AIPW/sequential DR、MIPS/OffCEM 与 Ouroboros finite-dose Settlement 都是强直接控制；本项目 `STEP2_PROJECTED_DELAYED_CREDIT.md` 已含标量版本与大部分边界。故 R15 只是 multivariate consolidation/lower-bound control，第一次修订后 park，不分配 D 编号；计数保持5历史/0活动/0科学准入/0选择，实验未知且未执行代码、训练或评分。

## R16 非交换 joint-flow 修复里程碑（2026-10-10）

[R16 三线筛选](repairs/R16_REPAIR_LINE_SCREEN.md)接续 R15 留下的 noncommuting exact-flow lead，并同时复查 symmetric split/Magnus 与 R09 inverse-metric endpoint。选中的[修订推导](repairs/R16_NONCOMMUTING_JOINT_FLOW.v1.md)把标量 residual flow 改为冻结的联合生成元 \(M=\Lambda+kk^\top\)，推导完整 affine exact flow，而不是只比较齐次交换子。

自然联合流并不能精确覆盖目标；若强制有限端点精确写入，唯一的 \(P_\tau^{-1}\)-metric 最小改动恰是 R09/PDN/RLS 型归一化 inverse-metric Delta，且旧状态因子仍奇异。真正保留的新边界是：相对纯 decay 的差异支撑在 \(\operatorname{span}\{k,\Lambda k,\ldots\}\) 上，非交换时可立即超过 rank one；二维行列式首项与 affine source 的二阶差都已独立复核。

三路最终字节审查通过条件数学并固定 KDA、EFLA、PDN、Longhorn、S4/S5 与 matrix-function/Krylov 作者接口。exact ZOH、inverse-metric endpoint 和数值 action 均有强已知近邻；bounded novelty 仍是 INCONCLUSIVE_EXPAND_SEARCH，且一般稠密转移没有同预算优势或语义 revision 证据。因此 R16 在第一次修订后 park，不分配 D 编号；计数仍为5历史/0活动/0科学准入/0选择，实验未知且未执行代码、训练或评分。

## R17 预测商可解码性修复里程碑（2026-10-10）

[R17 三线筛选](repairs/R17_REPAIR_LINE_SCREEN.md)比较了 noisy-key 后验矩写入、预测商/rate-distortion 与低秩 rollback。后验矩路线可严格重推为条件 ridge，但需要额外校准后验并与 RLS/Kalman 重合；低秩 rollback 仍需事件级身份/载荷或 replay。唯一实际改变原过强目标且不添加观测的路线，是只要求 exact overwrite 后仍能解码声明的旧未来行为商；这不自动等于部署更新保持该语义不变。

[R17 修订](repairs/R17_PREDICTIVE_QUOTIENT_OVERWRITE.v1.md)证明：对 `A=(I-kk^T)D`，覆盖后状态能恢复声明的线性未来行为，当且仅当 `ker(A·) subseteq ker O`。`D` 可逆时被删除的矩阵方向恰为 `{D^-1 k a^T}`，于是条件等价于每个传播后的有效查询满足 `q_u^T P_u D^-1 k=0`；在 post-decay 比较域中则等价于 `q_u^T P_u k=0`。对应 PSD Gram 的零二次型给充要条件和非零时的精确可见损失。有限比特下，全状态 Fano 下界被收紧为声明商的 conditional rate-distortion；离散零失真才可写 `B>=H(Q|K)`。

旧反例没有删除：只要一个被抹除方向对允许查询可见，exact overwrite 仍不可逆地合并不同行为；R10 的同等比特直接码支配在 quotient 上继续成立。predictive fibers、task/regret-sufficient compression、conditional rate-distortion、functional observer 与本项目 R01/R12/R13 已覆盖主体机制。保留的只是 ordinary Delta kernel 与 frozen future-query Gram 的显式桥接。它不产生 causal revision 证据、便宜在线 quotient 或原生内部 scorer，故 R17 第一次修订后 park，不分配 D 编号；计数仍为5历史/0活动/0科学准入/0选择，实验未知且未执行代码、训练或评分。

## R18 完整联合状态递归商修复里程碑（2026-10-10）

[R18 三线筛选](repairs/R18_REPAIR_LINE_SCREEN.md)复查了完整联合 Jacobian 商、带噪概率商和自适应 probe。后两条分别需要额外噪声律/后验与外部交互，或退化为必须计费的预写 side ledger；本轮选择修复 R17 的递归闭包缺口。

[R18 修订](repairs/R18_RECURSIVE_JOINT_QUOTIENT.v1.md)把判据从 memory-only/frozen query 提升为“完整当前更新的核包含于完整未来递归不可见子空间”。它区分全局 fiber factorization、仿射精确有限时域和非线性一阶证书，并给出两个相反见证：后来 cross-block 会暴露被 memory-only 检查漏掉的方向；同一步 auxiliary state 也可能保存 memory block 擦除的声明商，但其状态、精度与成本必须计入。

独立最终字节审查修正了 PSD 权重只能证明加权不可见商、部署/参考两分支须使用各自下游导数、以及 side-state rescue 不能冒充全局可逆。Pappas/van der Schaft/Tabuada、微分可观测 Gramian、Wang 的有限深度 predictive fibers 与 Li 等的递归 behavioral memory 已覆盖主体机制；R12/R13/R17/Step2 也有直接内部碰撞。故 R18 只保留为 Delta-specific 调试 theorem/control，第一次修订后 park，不分配 D 编号；计数保持5历史/0活动/0科学准入/0选择，原生机制测量仍缺失，实验未知且未执行代码、训练或评分。

## R19 切换保护纤维修复里程碑（2026-10-10）

[R19 三线筛选](repairs/R19_REPAIR_LINE_SCREEN.md)复查了保护模式切换、有限精度 noisy overwrite 和稳定裕量—反馈响应。后两条分别回落到 Kalman/RLS/量化滤波，或标准输入输出灵敏度；本轮选择补齐固定保护纤维、动态协向量保护和证据触发释放之间缺少的 cross-mode 条件。

[R19 修订](repairs/R19_SWITCHED_PROTECTION_FIBER.v1.md)证明：旧保护半范数 (P_\sigma) 的乘法证书能穿过 reset (R_{\tau\sigma})，当且仅当
\[
\ker P_\sigma\subseteq\ker(R_{\tau\sigma}^\top P_\tau R_{\tau\sigma}).
\]
若释放让过去不计能量的方向变成 transverse，identity reset 下 jump factor 必为无穷；二维反例明确复现。修复不是删掉反例，而是用完整 reset 转移该方向，或携带至少 (\operatorname{rank}(P_\tau^{1/2}R_{\tau\sigma}K_\sigma)) 个局部实线性动态坐标，并把释放注入显式加入递推。

独立最终字节审查实际发现并修正了同模 reset 漏因子、ledger row-space 维度错配和 selector 分支边界。Baum 等 arXiv:2512.16338v1 已直接覆盖 mode-dependent PSD seminorm、共同 invariant kernel、跨模式矩阵比较和 dwell/leave 条件；Multiple-Lyapunov、广义 Rayleigh、functional observer/充分坐标及本项目 R08/R13/R18 还覆盖其余主体机制。原生任务也不提供保护半范数、reset tangent、cross-kernel 或 paired release state。故 R19 只保留为“共同 kernel 改变时”的 Delta-specific 组合接口调试 theorem/control，第一次修订后 park，不分配 D 编号；计数保持5历史/0活动/0科学准入/0选择，实验未知且未执行代码、训练或评分。

## R20 非可分 query×value 曲率边界（2026-10-10）

[R20 三线筛选](repairs/R20_REPAIR_LINE_SCREEN.md)选择重新检查 R09/D03 的 rank-one representer 假设。修订没有否定 R09：对左侧度量，甚至对完整的单 Kronecker 度量，右侧 value 因子都会在精确约束 `X^T k=e` 下消去，最优 edit 仍是归一化 inverse-left-metric rank one。

[R20 修订](repairs/R20_NONSEPARABLE_CURVATURE_EDIT.v1.md)给出一般正定 edit-space 曲率的 KKT/Schur 解，并证明真正非可分的 query×value 曲率和精确 damping 之和可以要求更高秩。一个 2×2 可核例的唯一最优 edit 为 rank 2；最佳可行 rank-one 的目标仍严格高 `1/48`。这保留了一个有用的条件边界：完整输出曲率不能总被一个新的左写方向吸收。

但一般 KKT、GGN/natural gradient、K-FAC、Shampoo、generalized Sylvester/Krylov 和 CrispEdit 已覆盖主体数学或相邻功能；PDN/GKA、DeltaProduct、多步 Delta、constrained CG 与 direct rank-r action predictor 是更便宜的同信息对照。当前没有 prefix-only 的合法 coupled-curvature estimator、同预算求解优势或原生 rank-gap scorer。故 R20 作为 reviewed conditional theorem/control park，候选增量0；状态仍为5历史/0活动/0科学准入/0选择，实验未知且未执行。

## R20 v2 前缀因果低秩曲率修复（2026-10-10）

[第二次修订](repairs/R20_PREFIX_CAUSAL_LOWRANK_CURVATURE.v2.md)不再沿用未来稠密曲率 oracle，而要求 `Hhat=lambda I+ZZ^T` 在动作前由可见前缀产生。精确约束 `X^T k=e` 下的解为 `x*=x0-PZ(lambda I+Z^TPZ)^(-1)Z^Tx0`；因子列 `z_j=w_j otimes p_j` 时只需求 `r x r` 系统并得到至多 `r+1` 个 rank-one factors，且精确恢复 v1 rank-two witness。

独立数学审查先抓出 empirical-Fisher/GGN 范围过宽和两个反例遗漏标量 `e=1`，修正后最终字节复审通过。旋转曲率反例证明 stale prefix metric 可能比 Euclidean Delta 更坏，近奇异 key 反例还会产生 `1/epsilon` 动作范数。[来源审计](sources/R20_V2_PREFIX_CAUSAL_CURVATURE_SOURCE_AUDIT.md)确认 M-FAC/SENG/WoodFisher 已覆盖 past-gradient 小 Gram/Woodbury，OGD/GEM/SketchOGD 已覆盖 past-gradient projection/sketch。合法前缀不等于未来曲率准确，更不识别事实是否仍有效；feature/JVP/replay 成本也不能忽略。因此 v2 是第二次有界 theorem/control，park、候选增量0、实验未知。第三次尝试只在出现可检查的 prefix-to-future transfer/regret 定理或同总预算原生优势时重开。

## R20 v3 锐利谱迁移与前缀不可认证边界（2026-10-10）

[第三次修订](repairs/R20_SPECTRAL_TRANSFER_CERTIFICATE.v3.md)把“过去曲率代表未来”改写为明确的相对谱夹逼。固定仿射约束下的锐利竞争因子是 `(M+m)^2/(4Mm)`，对称半径时为 `1/(1-delta^2)`；夹逼必须覆盖仿射可行集的线性包，而非只覆盖可行差分。对称 Loewner minimax 仍返回 v2 动作，没有产生新 updater。

决定性反例均被保留：线性项、有限非线性余项、半正定端点和低秩遗漏方向都能破坏外推；两个完全相同前缀可接出一个满足、一个违反夹逼的未来，因此非平凡 `delta` 不能仅从合法前缀确定。独立数学、来源和对抗复核确认 sketch/Newton、Hessian averaging 与 online/dynamic regret 已覆盖带强假设的正面机制。R20 用满三次修订并最终 park；留下的是条件定理和 no-go/control，不增加候选、准入或选择，实验未知且未执行。

## R06 v3 生存裕量—可塑性最终修订（2026-10-10）

[第三次修订](repairs/R06_SURVIVAL_MARGIN_PLASTICITY.v3.md)没有删除 v2 的“同一前缀可被未来抹除或保留”反例，而是明确增加可部署检查的假设：每个冻结 Delta 因子同时非扩张并具有公开的最小奇异值裕量。于是无须假定未来 key 交换，就有 `alpha||U||<=||PU||<=||U||`；在固定或前缀可测 horizon、两套比例设计都不触发 cap 时，v2 的 envelope PPS 相对未来 oracle 的因子不超过 `(1+alpha)^2/(4alpha)`。

同一个 rank-one 因子也给出 `e+=(1-rho)e`，所以生存裕量强制 `||e+||>=eta||e||`：保留旧扰动和快速消掉当前误差不是免费兼得。统一裕量在长 horizon 上指数衰减；非零无限乘积又要求有限总 certified overwrite-cap budget。三路最终字节审查通过该条件定理，同时确认 generalized-Householder、invertible residual 与 PPS/proposal allocation 的直接碰撞及原生联合测量缺口。R06 已用满 3/3 次修订并 park；候选增量为零、实验未知，计数仍为5历史/0活动/0科学准入/0选择。


## R06 v2：收缩包络修复

R06 第二次实质修订把“前缀敏感度代理”收紧为可检查的冻结路径收缩包络：若未来 Delta 因子满足 \(0\le\beta_s\|k_s\|^2\le2\)，则 \(Z_i=\|P_{i,H}U_i\|_F\le X_i=|\beta_i|\|k_i\|\|e_i\|\)。在有限日志帧上，矩形最坏情形的 HT 二阶矩由 \(\pi_i\propto X_i\) 精确最小化；若另有 \(\alpha\le Z_i/X_i\le1\)，相对未来知情分配器的最坏比为 \((1+\alpha)^2/(4\alpha)\)。但收缩本身只给上界；同一前缀可由未来 key 抹除或保留当前写入，故无正下界时该比无界。该结果是条件理论/强对照，和 Neyman/PPS/active testing 及既有 R20 不等式碰撞，不增加候选。R06 已用 2/3 次修订；实验效果未知。

## 2026-10-10 R01 v3 final bounded repair

R01 used its third and final substantive repair attempt. The v2 fixed-`W` closure theorem is preserved; the new child replaces the raw local gate/loss row-space union as a purported minimum with the exact adjoint-transported covectors of a declared finite future scalar-credit family. For ambient perturbations, their joint row span is the minimum width of an exact right quotient `X -> XW`.

The same derivation also closes the boundary honestly: a formal suffix/credit class that allows arbitrary rank-one terminal covectors and ambient perturbations forces full value width for a prefix-only exact rule, but lawful language-model/native-loss and reachable-tangent realizability are not proved. The construction needs future covectors/full costates and is not a causal deployment statistic.

Independent final-byte math, source and adversarial reviews passed only the conditional theorem/control. Observability, bisimulation, exact lumping, recurrent behavioral memory and R18 cover the general mechanism; goal-oriented adjoint model reduction remains an explicit extra search gap. R01 is parked after attempt 3/3 with candidate delta zero, measurement gap and empirical status unknown. Counts remain 5 historical / 0 active / 0 scientifically admitted / 0 selected; no code or experiment was started.

## R03 v3 free-running-law repair milestone (2026-10-10)

[R03 v3](repairs/R03_WASSERSTEIN_FREE_RUNNING_SAFETY.v3.md) repairs the v2 common-path limitation by comparing complete action-conditional state laws. Under declared Wasserstein contraction and one-step kernel-mismatch constants, it derives the ordered recurrence `delta_(h+1) <= kappa_h delta_h + epsilon_(a,h)`, its finite-horizon and discounted protected-loss envelopes, and a simultaneous safe-logging feasibility test. Independent review corrected the metric/Frobenius implication, removed an unjustified true-gap floor, replaced a degenerate history-conditional coverage statement with outer calibration coverage, and restricted geometric loss decay to uniformly bounded loss Lipschitz constants.

The result is a useful Delta specialization—the initial discrepancy is the rank-one write—but the main mechanism strongly collides with generic Markov/Wasserstein perturbation, Lipschitz model-error and robust-MDP value bounds. Prefix-time constants, native joint measurement and matched-cost advantage remain absent. R03 is therefore exhausted and parked after attempt 3/3 with candidate delta zero; counts remain 5 historical / 0 active / 0 scientifically admitted / 0 selected, and no code or experiment was run.

## R05 v4 prefix-conditioned repair milestone (2026-10-10)

[R05 v4](repairs/R05_PREFIX_CONDITIONAL_PARTIAL_ID.v4.md) repairs v3's pooled constant-gate mismatch without deleting its impossibility result. A lawful action-time context `C` yields per-stratum sharp Fréchet bounds `ell_c,h_c`. Under a declared rectangular conditional ambiguity set, the oracle-regret gate is `(ell_c+h_c)/(2A_c)`, while the distinct baseline-safe release is `ell_c/A_c`; only the latter writes exactly where the lower bound is positive. A two-stratum witness has pooled lower bound zero but a positive safe-write stratum, and the old identical-marginal/different-coupling counterexample remains valid inside every unresolved stratum.

Independent final-byte math, source and adversarial reviews fixed layer-random update cost, `A=0`, integrability, sharpness scope and the earlier regret/safety gate conflation. Ben-Michael conditional LP, D'Adamo individualized ambiguity policy, Ji–Lei–Spector covariate-assisted bounds and Kallus–Zhou robust policy improvement cover the contribution skeleton. Existing edit benchmarks still lack the pre-action joint variables. R05 is exhausted and parked after attempt 3/3 as a useful conditional control, with candidate delta zero and no experiment run.

## R02 v3 approximate causal/dynamic quotient milestone (2026-10-10)

[R02 v3](repairs/R02_APPROXIMATE_CAUSAL_DYNAMIC_QUOTIENT.v3.md) repairs v2 by replacing exact quotient sufficiency with two deliberately separate quantitative statements: a sharp quotient-cell AIPW covariance/variance bound, and a fixed-policy finite-horizon reward/transition-defect value recursion. It preserves the quotient-only non-identifiability witness and adds a rare-action counterexample showing why behavior-average error cannot replace a target-reachable uniform condition. For `q=SW`, discarded perturbations remove the direct projected term but can still enter through state-dependent coefficient derivatives; the final fiber condition correctly fixes both `q` and side state `z`.

Independent final-byte review accepts these equations only as a conditional theorem/debugging control. Approximate information states, approximate abstraction, abstract-state OPE, simulation/bisimulation and internal R18/R03 strongly cover the mechanism. No approximate sequential-DR theorem, lawful prefix-estimable uniform certificate, matched-cost advantage or native joint measurement object was obtained. R02 is exhausted and parked after attempt 3/3 with candidate delta zero; counts remain 5 historical / 0 active / 0 scientifically admitted / 0 selected, and no code or experiment was run.

## R07 v2 complete-state coupled directional-margin milestone (2026-10-10)

[R07 v2](repairs/R07_COUPLED_DIRECTIONAL_MARGIN.v2.md) repairs v1's frozen-reference limitation without deleting its signed truth/protection result. The action is injected into the complete recurrent state, then propagated through a fixed-policy/common-exogenous finite suffix. Forward tangents and reverse costates give the exact first directional derivative; second tangents or the reverse Hessian recursion add the costate-weighted transition curvature that frozen-feature and GGN/iLQR approximations omit. A simultaneous prefix-valid Taylor envelope gives a sufficient decrease certificate, with the `q=0,h<0`, indefinite-curvature and endpoint branches stated correctly.

The affine fixed-reference limit exactly recovers v1 and its truth-versus-action counterexample. Realized suffix derivatives remain retrospective/training quantities, not a deployment oracle; common-noise differentiation is not a free-running causal effect; multiple writes require cross-Hessian terms. Independent final-byte math, source and adversarial reviews pass only this conditional debugging theorem. Adjoint sensitivity, DDP/iLQR, differentiable MPC, MAML/learned optimizers and Bellman evaluation cover the main mechanism, while native tasks do not expose the required joint action-level object. R07 is parked after attempt 2/3, candidate delta zero, empirical effect unknown, and counts remain 5 historical / 0 active / 0 scientifically admitted / 0 selected. No code or experiment was run.

## R09 v2 dynamic-protection Gramian milestone (2026-10-11)

R09 attempt 2/3 replaces v1's static protection metric by the exact finite-horizon transported Gramian under a declared frozen/exogenous suffix. For a rank-one edit `Delta S=x e^T` and affine endpoint `k^T x=gamma`, the conditional optimizer is `x*=gamma H^{-1}k/(k^T H^{-1}k)`, with `H=G+mu I`.

The child preserves every v1 counterexample and adds an identical-prefix swapped-anisotropy construction. Without an externally justified continuation law, ordinary Delta is minimax on that two-future family and any prefix-only rule has competitive ratio `(M+m)^2/(4Mm)`; randomization does not remove the lower bound.

Independent final-byte mathematics, source, and adversarial reviews pass only the stated conditional theorem/control. Kalman Delta Networks is now the closest Delta-specific uncertainty baseline: its filtering covariance is not the unseen future protected-query pullback, but it strengthens the collision and baseline burden. Candidate/admission/selection counts remain unchanged; empirical effect is unknown and no project execution occurred.

R09 v2 delivery closure: substantive commit `0138a2a786f9b68b770ecf64251349aa3ecb491c`; all 12 changed paths matched exact-commit readback. Receipt: `research/delta-discovery-2026-10-08/sources/REPAIR_R09_V2_DELIVERY_READBACK.json` (SHA256 `0cc32a7dac3a02c6372afc07b4d0a549387f55488d3cbedcdd5c55dfac563078`).


## R10 v2 transition-matched residual milestone (2026-10-11)

The second bounded repair preserves v1's equal-cardinality and operator-change boundaries, then closes the correlated-defect branch. The exact frozen-affine recurrence is \(e_t=A_te_{t-1}-F_tr_{t-1}+r_t\). Under a common exogenous residual law invariant across compared feedback choices, \(F_t=A_t\) removes older residual propagation; scalar restrictions are future-read Gramian/covariance projections. For stationary correlated residuals the optimal restricted scalar is a weighted one-lag spectral ratio, not a universal Delta decay coefficient.

Independent final-byte review found and repaired the hidden residual--feedback endogeneity assumption, finite-residual nullspace scope, stability statement, fixed-rate source omission and comparator-fairness wording. Classical state-space error-spectrum shaping, Zheng et al. graph QEF, Ohno et al. fixed-rate error-feedback quantization, recurrent-state write-back, DAMP and STEPQuant cover the mechanism family. R10 v2 is therefore a useful conditional Delta debugging theorem/control, parked after attempt 2/3 with candidate delta zero. Empirical effect and a native mechanism measurement remain unknown; no code, test, training, inference or scoring was run.


### R10 v2 delivery closure

Substantive commit `2863f2177f97d0ad6fd6ba7c7c9bfec87ad25655` was published to literal `main` by expected-parent, non-force update. All 12 changed files were fetched again at that exact commit and hashed; the immutable receipt is `research/delta-discovery-2026-10-08/sources/REPAIR_R10_V2_DELIVERY_READBACK.json` (SHA256 `2700bae2e2d3bab87b8c394c1c67fa6a4f1dbdf21752597b0d3f38d0dcd12bda`). This verifies delivery bytes only, not originality, empirical benefit, or method admission.


## R11 v2 pure-Delta factor-core milestone (2026-10-11)

R11 attempt 2/3 repairs a real computational omission without deleting v1. For two pure scalar-\(\beta\) Delta steps, the exact adjacent order gap is

\[
K=\beta_i\beta_j(k_i^\top k_j)\,[k_i,k_j]\,[e_j,-e_i]^\top.
\]

The common-prestate second residual is reconstructible from the chronological post-first-write residual, and query-weighted low-rank optimization needs only two small Gram matrices plus an at-most \(2\times2\) SVD. Independent review then found and fixed a separate base-point error: rank relative to the branch midpoint is not the same as rank of an edit from the already executed physical order. The final theorem gives both budgets, the real no-op, and a plug-in selector-calibration penalty.

Three independent final-byte reviews pass this only as a conditional pure-Delta theorem/control. It does not extend to an intervening decay matrix or state-dependent features. Ordered Delta/WY, DeltaProduct and classical factored/core SVD cover the principal mechanisms. A decision-time action-invariant \(G\), calibrated semantic selector, persistent-overlay cost advantage and native harmful-order measurement remain absent. R11 v2 is parked with candidate delta zero; empirical effect is unknown and no code or experiment was run.


### R11 v2 delivery closure

Substantive commit `37e5e1b1d6098c6207fa3e753c1d6ed03b24c740` was published to literal `main` by expected-parent, non-force update. All 12 changed paths were fetched again at that exact commit and matched the authored bytes. Receipt: `research/delta-discovery-2026-10-08/sources/REPAIR_R11_V2_DELIVERY_READBACK.json` (SHA256 `e96edb7ee8fca0661b26dbc943c863620a76913667fb0af8d629b463b4bcfddb`). This verifies delivery bytes only; it does not establish method novelty, empirical benefit, or scientific admission.

## R12 v2 autonomous-syndrome closure milestone (2026-10-11)

R12 attempt 2/3 preserves v1's static protected-readout theorem and repairs its target mismatch: a syndrome must be recursively sufficient, not merely decode one completed edit. For `Y=H^T S` and a frozen affine state factor `F`, exact next-syndrome closure holds iff `ker(H^T) subseteq ker(H^T F)`, equivalently iff `F^T col(H) subseteq col(H)` or `H^T F=L H^T` for some `L`.

For pure Delta with nonzero gate, this collapses to a sharp key geometry: each key must lie inside or be orthogonal to the syndrome subspace. Iterating the keys that have nonzero projection into the current space gives the least closed protected subspace. A mixed key produces two full states with the same syndrome but different next syndrome, and the orthonormal-basis one-step leakage is exactly `|beta| ||P_V k|| ||P_(V^perp) k||`.

Independent final-byte math, source and adversarial review corrected two substantive overclaims: composite state-dependent closure does not require every coefficient to be individually fiber-constant, and raw `H` leakage is coordinate-scaled unless `H` is orthonormalized. The result remains a conditional theorem/control, not a new updater. Invariant quotient/bisimulation theory and internal R18 cover the general mechanism; direct coordinates on the same closed space and the full Delta state are mandatory controls. Native tasks do not expose exact fiber closure or semantic-revision identity. R12 v2 is parked after attempt 2/3 with candidate delta zero, empirical effect unknown, and no code or experiment run.

### R12 v2 delivery closure

The initial substantive commit `a5b4f859e8a05f4e471499aaeb187875fce1bf48` exposed connector-output truncation in two large tracker blobs during exact readback; the other ten paths matched. A second expected-parent, non-force commit `0067a6b304e3dc3ecff9b7e734c3fa83183c0aeb` rebuilt only those two blobs from three-byte-aligned chunks. All 12 authored paths then matched SHA256 at the effective substantive commit. Receipt: `research/delta-discovery-2026-10-08/sources/REPAIR_R12_V2_DELIVERY_READBACK.json` (SHA256 `625006c07a1b950a47f9241cc0875cd2069720a653dee36cf2d66d39efae4a3d`). This verifies delivery bytes only, not originality, admission or empirical benefit.

## R13 v2: hidden-transition common covector

R13 v1 is preserved byte-for-byte. The v2 child changes the information set: the decoder knows an admissible affine-transition family but not which mode occurred. One mode-blind affine decoder exists exactly when the simultaneous block equation `XM=N` is consistent, equivalently `ker(M) subseteq ker(N)`. Two individually invertible Delta updates can still map different old states to the same post-state while their protected values differ. This proves a half-diameter lower bound for arbitrary point decoders only when the conflicting histories are reachable under identical retained information; failure of the affine block condition by itself does not rule out a nonlinear piecewise decoder.

Independent final-byte math, source and adversarial reviews pass the scoped theorem/control. Moreno (2005) simultaneous functional observation is the strongest direct closest-work collision; generalized inverses, simultaneous matrix equations and set-membership estimation cover the remaining mechanisms. A direct protected-value ledger remains the mandatory exact same-information control. Native endpoints do not expose mode identity, internal factors, compatible-target diameter or ledger state. R13 v2 is parked after attempt 2/3 with candidate delta zero, empirical effect unknown, and no code or experiment run.

### R13 v2 delivery closure

Substantive commit `4247399fd0b7471bac5aaed7c486b5c31a4f3bb8` was written to literal `main` with an expected-parent, non-force update. All 13 authored paths were fetched from that exact commit and matched their SHA256 records; the receipt is `research/delta-discovery-2026-10-08/sources/REPAIR_R13_V2_DELIVERY_READBACK.json` (SHA256 `ec185523efc294e94b524d4d71f92972e2913bc23338ccf63ad6bc5ffa582027`). This verifies delivery bytes only, not originality, candidate admission, or empirical benefit.

## R14 v2: credal provenance repair (2026-10-11)

R14 v1 is preserved byte-for-byte. The v2 child replaces its supplied exact identity posterior with an external prefix-measurable interval `[ell,u]`. In the two-slot quadratic model, the exact minimax action is the point-posterior Bayes action evaluated at the projection of `1/2` onto that interval. The artifact also proves an exact posterior-misspecification regret identity, the separate hard one-touch/no-write thresholds, an invalid-certificate counterexample, and a positive-curvature multi-slot minimax/QCQP extension.

Independent final-byte math, source and adversarial reviews pass the scoped theorem/control. They do not pass a method: Gamma-minimax and credal/DRO decision theory cover the minimax skeleton, posterior-error decision regret is known, and the strongest same-information baseline is the algebraically identical direct minimax per-slot router. A Bayesian credible interval or marginal reliability curve is not automatically a tokenwise deployment certificate; the construction and its sampling conditions must be supplied. No native endpoint exposes slot identity plus all counterfactual writes. R14 v2 is parked after attempt 2/3 with candidate delta zero, empirical effect unknown, and no model code or experiment run.

### R14 v2 delivery closure

Substantive commit `9f14558d4e7b1196a1606a0c6cd0ac5f9072e926` was written to literal `main` with an expected-parent, non-force update. All 13 authored paths were fetched at that exact commit and matched their SHA256 records. Receipt: `research/delta-discovery-2026-10-08/sources/REPAIR_R14_V2_DELIVERY_READBACK.json` (SHA256 `fef02d6230c3a95d67b43510d506b4db726f24952237d77e3c2b25380bbeed78`). This verifies delivery bytes only, not originality, candidate admission, native measurement or empirical benefit.

## R15 v2: coupled response-degree repair (2026-10-11)

R15 attempt 2/3 repairs v1's frozen-quadratic scope. For an action injected into the complete state and propagated through polynomial continuation maps, response degree is bounded by the terminal-loss degree times the product of transition degrees. An abstract unconstrained scalar Delta recurrence attains degree `2*3^H` under terminal square loss, so bare Delta algebra does not imply a global quadratic response. This witness is not claimed to instantiate normalized-key/sigmoid released FLA.

The repair also removes a stronger false inference: `binom(r+m,m)` is only the dimension of a saturated black-box degree-`m` polynomial fit, not an inherent Delta intervention-rank lower bound. A fixed structured recurrence or optimizer-only target can be much smaller. Locally, a branch-smooth quadratic Taylor model has error at most `M3*rho^3/6` and optimizer regret at most `M3*rho^3/3` on a certified ball, but the needed uniform derivative/radius certificate is not presently prefix-available.

Independent final-byte mathematics, source and adversarial reviews pass only this scoped theorem/debugging control. Polynomial/Volterra design and same-information DDP/iLQR/GGN/action optimization cover the positive mechanisms; native branch-consistent intervention measurement and matched-cost advantage are absent. R15 v2 is parked with candidate delta zero and empirical effect unknown. Counts remain 5 historical / 0 active / 0 scientifically admitted / 0 selected; no code or experiment was run.

### R15 v2 delivery closure

Substantive commit `d4fdc86f0c25b9495b51779a12074f26e98d027d` was written to literal `main` with an expected-parent, non-force update. All 13 authored paths were fetched at that exact commit and matched their SHA256 records. Receipt: `research/delta-discovery-2026-10-08/sources/REPAIR_R15_V2_DELIVERY_READBACK.json` (SHA256 `120e423e1a42558a6db4ee4596810b4a25c4019bf4865ee40674450a1bc1650f`). This verifies delivery bytes only, not originality, candidate admission, native measurement or empirical benefit.

## R16 v2 主动谱核修订（2026-10-11）

[v2 筛选](repairs/R16_REPAIR_LINE_SCREEN.v2.md)没有删除 v1 的反例，而是专门修补“非交换 joint flow 是否必然需要一般稠密矩阵函数”这个计算缺口。[v2 推导](repairs/R16_ACTIVE_SPECTRAL_CORE.v2.md)按 decay 的不同特征值分组；若只有 (r) 个含有 (k) 分量的主动特征组，则所有相对纯 decay 的解析函数修正都严格落在该 (r) 维主动子空间，并化为 (B=D+cc^\top) 的 diagonal-plus-rank-one 核。精确指数、积分源项和归一化端点方向都由同一小核给出；近似分组另有显式 Duhamel 状态误差与归一化方向误差证书。

独立审查纠正了初稿隐藏的成本过度声明：一般对称 \(\Lambda\) 的特征基可稠密，发现、变换和基础作用仍须分别计费；只有坐标对角或 tied-group（KDA 风格）结构，或另行计费的快速固定特征变换，才得到顺序执行的 (O(dm+r^2m+r^2)) 条件成本。DPR1 eigensolver、低秩 matrix-function update、expmv、KDA/DeltaProduct/CKDA 已覆盖主要数值机制；而 joint generator 的科学依据、scan closure、retain/revise 证据与原生机制测量仍缺失。故 R16 在第 2/3 次修订后继续作为 theorem/control park，不分配 D 编号；计数与实验状态不变。

### R16 v2 delivery closure

Substantive commit `a1da709feed580c5fe9e98a5be57f4739f5a3259` was written to literal `main` with expected parent `1c10e20f3868fe1fb62c84adbf33efc558e3c309` and `force=false`. All 13 authored paths were fetched at that exact commit and matched local bytes. Receipt: `research/delta-discovery-2026-10-08/sources/REPAIR_R16_V2_DELIVERY_READBACK.json` (SHA256 `c2786b967abae083b6d1a11e67c2943fc85f7038d33f0230b9db9097192bde4a`). This verifies delivery only, not originality, admission, measurement validity or empirical benefit.



## R17 v2 因果预测泄漏证书修订（2026-10-11）

R17 v1 的 exact-overwrite 商定理保留，但其“未来查询 Gram”不是动作前可用量。v2 把它修成前缀可测的 PSD 预测集合 (mathcal G_t)：最坏泄漏是支持函数 (sup_{Ginmathcal G_t}k^	op Gk)，全集合精确不可见当且仅当 (k) 落在共同核中；谱范数球给出精确闭式 (k^	opwidehat Gk+arepsilonlVert kVert^2)。校准样本只支持条件均值和概率型路径界，不能在无支撑假设时把有限次零观测升级为确定零风险。

这是真实的因果接口修复，但 robust observability、DRO、矩阵浓缩、predictive quotient 与 R09 已覆盖主体机制；直接保存声明可观测子空间坐标仍是同信息强对照。原生端点不暴露 overwrite counterfactual 或 realized suffix Gram，实际效果未知且未执行实验。独立最终字节数学、来源、对抗审查通过的是 conditional theorem/debugging control；R17 attempt 2/3 后继续 park，候选、科学准入和选择增量均为0。


### R17 v2 delivery closure

R17 v2 数学卡、来源审计、三路独立最终字节审查及状态文件已在 substantive commit `86e4911f5c706f0b1340c01e5fc70e90541cc35c` 发布；12 个目标路径均从该精确 commit 读回并与提交字节一致。交付收据为 `research/delta-discovery-2026-10-08/sources/REPAIR_R17_V2_DELIVERY_READBACK.json`（SHA256 `117f7eb0868a9d882519fb95665c399f209cf081dd57a74453e18b914db81729`）。计数不变，下一条独立未耗尽修复 lineage 为 R18 v2。

## R18 v2 前缀因果鲁棒递归商空间（2026-10-11）

R18 v1 的完整联合状态递推没有被删除；v2 修补其最早未闭前提：真实未来 suffix 只能用于事后审计，当前写入不能把它当 oracle。修订后，动作前缀必须给出一棵在整个 overwrite fiber 上一致的受约束仿射模式树；递推保留路径耦合，而不是把每一时刻的模式边际集合错误地做笛卡尔积。

对每个树节点，最大共同不可见子空间满足沿合法边的 kernel/intersection/preimage 递推；由此显式构造递归 quotient。有限自动机版本是状态索引子空间族的最大不变 fixed point。当前完整更新线性部为 \(A_t\)、保护入口为 \(P_t\) 时，所有声明旧行为可从更新后状态恢复，当且仅当 \(\ker A_t\subseteq\ker(O_TP_t)\)。若失败，最小实线性 side ledger 宽度精确为 \(\operatorname{rank}(O_TP_tK_t)\)。

修复同时保留了负边界：相同前缀的两个未来若分别读取互补方向，每个 oracle 分支只需一维，但合法鲁棒 quotient 可能必须保留全部状态；一般范数球不确定性也会让精确共同 kernel 退化为零。非线性、hard routing、覆盖失败和有限 horizon 不能被 Jacobian 证书自动解决。

独立最终字节数学、来源、对抗与测量审查通过上述条件定理。Baştuğ 等人的正则语言 switched-system 不可观测子空间、quotient 与 Algorithm 2 是决定性机制碰撞；直接 lost-visible ledger 达到同一线性下界。现有 bAbI、LAMBADA、RULER、BABILong、LongMemEval 只测端点，不原生识别模式语言、覆盖率、overwrite fiber 或 quotient rank。故 R18 v2 在 attempt 2/3 后作为 theorem/debug control park，候选增量 0；实验效果未知，未运行代码或实验。

### R18 v2 delivery closure

Substantive commit `7cb9a1b6153f31ca056208bb9965ebb74ddb52d2` was written to literal `main` with expected parent `23003feefe751b41e521d05ad0b13adcb4bb8892` and `force=false`. All 12 authored paths were fetched at that exact commit; the six new artifacts matched local authored bytes and the six tracker/entry files matched the expected R18 fields or sections. Receipt: `research/delta-discovery-2026-10-08/sources/REPAIR_R18_V2_DELIVERY_READBACK.json` (SHA256 `c0b992be62fe2f53dc2721c57f91653f32638662218cbcf008db50b7e4bb2e9b`). This verifies delivery bytes only, not originality, candidate admission, native measurement or empirical benefit.


## R19 v2 前缀因果分支码修订（2026-10-11）

R19 v1 的已实现分支 PSD-kernel 阻塞保持不变；v2 修补其未来分支 oracle。对有限可达状态、破坏性写后映射、前缀声明的合法分支集合和事后可见标签，先检查同一状态在同一标签下是否欠两个不同目标：若是，则任何码长都无解；若否，则最小一发定长零误差 side-code 字母表恰为释放混淆图的色数。两个互补释放分支给出 K4 例子，说明每个已知分支只需 1 bit，并不代表写入前的合法码也只需 1 bit。

独立审查还纠正了线性附加宽度：解码器已经看到写后状态 A，因此最小新增实坐标是 rank([A;B_1;...;B_M])-rank(A)，而不是无条件的 stacked-rank。全路径版本使用相对于 row(A) 的联合行空间。硬 guard 反例、有限精度、着色计算、码本/解码器和完整增广状态成本均被保留。

该正结果直接碰撞于零误差函数计算与 decoder side information；set-valued switched observers、switched observability/R18、saltation 与 path-complete/bisimulation 是强控制。原生 benchmark 不暴露 destructive fiber、合法分支关系、混淆图或配对 counterfactual。故 R19 v2 在 attempt 2/3 后作为 conditional theorem/debug control park，候选增量 0，实证效果未知，未执行代码或实验。


### R19 v2 delivery closure

Substantive commit `3894f2337c21d076fcbbecfd7a9c0c6b66f6d89d` was written to literal `main` with expected parent `361497dc604b7cc02f3c5fe8fcac0917c371555a` and `force=false`. All 13 authored paths were fetched at that exact commit; seven new artifacts matched local bytes and six tracker/entry files matched the expected R19 v2 fields or sections. Receipt: `research/delta-discovery-2026-10-08/sources/REPAIR_R19_V2_DELIVERY_READBACK.json` (SHA256 `41fbe21f33d609d7f21600a02ea15ac1ff2cc7746aa70a65d15296e0b988ac88`). This verifies delivery bytes only, not originality, candidate admission, native measurement or empirical benefit.

## R07 v3 因子核联合裕度修订（2026-10-11）

R07 第三次也是本 lineage 最后一次有证据的数学修订，修掉了把多个写入的标量裕度独立相加的问题。在同时固定的 rank-one 提案、动作无关的仿射后缀和二次读出损失下，所有写入对未来读出的响应严格落在一个 m 维动作空间；联合 Hessian 精确为 Delta 响应的 Hadamard Gram，因此必须解联合 box QP，不能一般地逐写入决定。对角加 rank-one 的冻结 Delta 转移可用 skinny key factor 顺序传播，但 O(H d_k m) 只覆盖这一核心；残差构造、未来 probe/metric、Hessian、QP、最终 rank-m 写入及前缀预测均需另计。

旧反例没有被删除：一个合法的状态依赖 gate 已足以让冻结模型的一阶决策符号反转。冻结核到真实耦合递推的误差一般是一阶，只有额外的一阶抵消才能得到二阶包络，而且 tube、tail 与常数必须在动作前合法获得。四路独立最终字节审查只通过了条件定理/调试 control；weighted least squares、Khatri--Rao/Hadamard Gram、condensed MPC、DDP/differentiable MPC、Delta/WY 与 DeltaProduct 已覆盖主要机制，原生 benchmark 又不提供联合内部动作对象。故 R07 attempt 3/3 已耗尽并 park，候选增量为 0，计数保持 5 historical / 0 active / 0 scientifically admitted / 0 selected；实验效果未知，未执行代码或实验。

### R07 v3 delivery closure

Substantive commit `c3823b3e770d45c46c825a3c059aed0e113deefc` was written to literal `main` with expected parent `2efad2c3ad3b7ddaa52312f975a26676ef475b06` and `force=false`. All 13 authored paths were fetched at that exact commit and matched the submitted bytes or the declared tracker sections. Receipt: `research/delta-discovery-2026-10-08/sources/REPAIR_R07_V3_DELIVERY_READBACK.json` (SHA256 `fe5778210a0285bb2a7b37c06f04447df75e11180efbdfb16031d53984869e20`). This verifies delivery only, not originality, candidate admission, native measurement or empirical benefit.

## R08 v3 sharp channel-free release closure (2026-10-11)

R08 is repaired through its final bounded attempt. For each action, the affine binary-state terminal margin now yields a sharp information-value envelope between the uninformative and fully revealing channels. Under explicitly rectangular channel ambiguity, the release-minus-keep difference lies in `[H-U_R, H+U_K]`; strict sign separation certifies a robust action, while interval overlap requires abstention or an explicit ambiguity rule. A same-record pair of unsupported release-channel worlds gives opposite optimal actions, so the missing action record is a real identification boundary rather than a reason to erase the useful conditional theorem.

This is a theorem/debugging control, not a new updater. EVPI/EVSI, Blackwell/controlled sensing, partial identification, robust policy and no-overlap OPE cover the generic mechanism; R05 and R18 cover the nearest internal controls. Attempt 3/3 is exhausted, candidate/admission/selection counts remain 5 historical / 0 active / 0 admitted / 0 selected, and empirical effect remains unknown because no code or experiment was run.

Delivery: substantive commit `a60b7071cd852d5662e74b733cec616bd7fa07b0` exact readback verified; receipt `research/delta-discovery-2026-10-08/sources/REPAIR_R08_V3_DELIVERY_READBACK.json` (SHA-256 `4bc0d895443b54964671735260045d9744fa28010865d46d23791ea713498df1`).

## R09 v3 鲁棒 Gramian 载体修订（2026-10-11）

R09 的第 3/3 次修订把“单个已实现 suffix 的低秩 Gramian”改成动作前声明的有限合法未来族。每个模式的保护矩阵都可写成 transported factor Gram；最小公共精确载体是所有 transported factor range 的并空间，鲁棒写方向精确落在该载体与当前 key 的联合空间。对已知无 decay 主动子空间，rank-one Delta 后退递推每步为 \(O(s^2)\)，修正了 v2 对该特殊递推过粗的 \(O(Hd^3)\) 描述；basis、坐标、stage metric、solve 与物理写入成本仍单独计费。

新的 sharp witness 取 \(A_i=I-\beta e_i e_i^T\)、\(Q=\mathbf 1\mathbf 1^T\)、\(0<\beta<1\)：每个已实现 Gramian 都是 rank one，但 transported factors 构成 \(\mathbf 1\mathbf 1^T-\beta I\)，故公共精确载体为整个 \(\mathbb R^d\)。这说明 rank-one Delta 不自动产生小的 prefix-robust 保护状态；小载体也不识别其内部 PSD core。

四路最终字节审查在实际修正伴随顺序、半正定唯一性措辞和论文定位后通过。正结果与受约束语言 switched observability/quotient、switched Gramian/model reduction 及内部 R18/R16/R11/R20 决定性碰撞。原生 benchmark 不暴露动作前 carrier、未来 containment/core、grounded validity、propensity/paired outcome 与同成本记录。故 R09 attempt 3/3 耗尽并 park，candidate/admission/selection 增量均为 0，实验效果未知且未运行代码或实验。下一条独立未耗尽 lineage 为 R10 attempt 3。

### R09 v3 delivery closure

Substantive commit `09c5cd73d643dc2b51c9f91d8ca76aea639bbe27` was written to literal `main` with expected parent `77f25334fff828a9e5a584e5949f45d957ead13c` and `force=false`. All 13 authored paths were fetched at that exact commit and matched the submitted bytes. Receipt: `research/delta-discovery-2026-10-08/sources/REPAIR_R09_V3_DELIVERY_READBACK.json` (SHA256 `5e000a72dfe1accdfa728496c1a04f5b31f681d5862dcece0b554eeec89999a5`). This verifies delivery only, not originality, candidate admission, native measurement validity or empirical benefit.


## R10 v3 invariant residual carrier milestone (2026-10-11)

R10 attempt 3/3 preserves v1/v2 and repairs the remaining full-width-residual question. For a fixed orthonormal carrier (U), exact transport under the real ordered Delta transition (A_t=(I-eta_tk_tk_t^	op)D_t) holds exactly when ((I-UU^	op)A_tU=0). The v3 child derives the projected core, exact leakage, accumulated error including off-carrier injections, and the affine invariant hull seeded by both initial residual and every allowed new defect.

A legal noncommuting family of rank-one Delta modes can force any common carrier containing a declared dense residual direction to have width (d). The result is scoped: moving bases can preserve one realized low-rank path, but their basis state, traffic, factor precision, QR and dense core costs must be charged; new elementwise quantization residuals can also jump from rank one to full rank. Future keys/Gramians remain unlawful deployment inputs, and the frozen left-state theorem is not a full-network Jacobian guarantee.

Independent final-byte math, source, adversarial and measurement reviews pass only this conditional boundary/debug theorem. Common invariant subspaces, switched reachability/model reduction, classical error feedback and packet-internal R09/R16/R18 are major collisions. Existing native tasks do not isolate closure/leakage from endpoint utility. Candidate delta is 0, empirical effect is unknown, counts remain 5 historical / 0 active / 0 scientifically admitted / 0 selected, and R10 is parked after attempt 3/3. No code, model or scorer was executed.


### R10 v3 delivery closure

Substantive commit `d6758ff92b7bbd9113547642e74bdc41130f2a5f` was written to literal `main` with expected parent `a0e2ce2fbbee06a615d4a573e777f50773b912d7` and `force=false`. All 14 substantive paths were fetched at that exact commit and matched the submitted bytes. Receipt: `research/delta-discovery-2026-10-08/sources/REPAIR_R10_V3_DELIVERY_READBACK.json` (SHA256 `48ddb20af1c6505d827189eff125fc6296f3ab578e90bd7989b11e490ceba9ea`). This verifies delivery only, not originality, candidate admission, native measurement validity, empirical benefit, or experiment completion.

## R11 v3 修订里程碑（2026-10-11）

R11 的第三次实质修订没有删除旧反例，而是修正了 v2 对 overlay 传播的含混表述：固定且不随动作变化的纯 Delta 系数下，单个低秩修正只需更新左因子，秩不会自行增长；只有新的 gap 注入才累积秩，并可用合法的互不相交二维块达到 (2m) 的尖锐下界。修订同时补上了状态依赖 commutator 的 (MC) 项、query 可见最小精确秩、加权截断尾误差和包含初始误差的重压缩递推。

四份绑定最终字节的独立审查均通过这一限定定理/调试控制。它仍与 Delta/WY、DeltaProduct 和低秩 SVD 维护机制高度重合，且缺少合法语义 selector、前缀可因果 query metric、同总成本优势与原生机制测量。因此 R11 第 3/3 次尝试到此 park，候选增量为 0，实验效果未知；历史计数不变。下一条独立未耗尽线为 R12 第三次修订。

Delivery: substantive commit `aac96a58daa28a455012b95e8015dd1f0926c2ad` exact readback verified for all 14 substantive paths; receipt `research/delta-discovery-2026-10-08/sources/REPAIR_R11_V3_DELIVERY_READBACK.json` (SHA256 `a0618e7676b5173020e1897aee93e4072026df47105ad12a26890ed1e0e954fb`).

## R12 v3 有限 key Gram 连通闭包（2026-10-11）

R12 第三次修订没有重新发明 v2 的最小不变 fixed point，而是在“完整 key 家族于压缩前已声明、纯 scalar-beta Delta、选择器不读取已丢弃状态”的条件下把它算成显式图证书：以与保护子空间非正交的 key 为 seed，最小精确载体正好是保护子空间加所有 seed 连通分量的 key span，宽度为 \(\operatorname{rank}[Q,K_R]\)。正交基坐标 \(Y=U^TS\) 给出精确封闭 Delta 递推。

修订保留并加强了失败边界：一个以后才出现的 bridge key 可以让早先丢弃的正交方向突然变得必要，旧摘要无法事后补回；exact zero Gram edge 在有限精度下不连续，threshold 版本必须支付逐步泄漏与 conditioning；非标量 decay、隐藏状态 selector 和未声明 key 都需要回到完整算子/fiber 条件。字典、Gram、QR/SVD、基、缓存、lookup、precision 与 amortization 全部计费。

四路最终字节独立审查只通过了限定定理/调试 control。一般 invariant quotient、simultaneous reducing-space/frame-graph 理论与内部 R18/R09/R10 已覆盖主体，且 \(U^TS\) 就是同信息直接坐标，不是新 checksum/updater。R12 attempt 3/3 因此耗尽并 park；candidate delta 为 0，实验效果未知，计数仍为 **5 historical / 0 active / 0 scientifically admitted / 0 selected**。下一条最早未耗尽独立 lineage 是 R13 attempt 3。

### R12 v3 delivery closure

Delivery: substantive commit `4e8effff833f0b553982532a9615b288dc95da14` exact readback verified for all 14 substantive paths; receipt `research/delta-discovery-2026-10-08/sources/REPAIR_R12_V3_DELIVERY_READBACK.json` (SHA256 `8532cf0969f3634d810e98128533d1b9f3aa66da405220735589378c2cbe31e4`). This verifies delivery only, not originality, candidate admission, native measurement validity, empirical benefit, or experiment completion.

## R13 v3 最小擦除 ledger 修订（2026-10-11）

R13 第 3/3 次修订修正了 v1 的一个真实成本缺口：不再默认保存全部 \(Q^\top S\)。对写入前可见、写入后已知的仿射步 \(Z=AS+B\)，若 \(N\) 张成 \(\ker A\)，精确恢复旧保护读出的最小额外线性行数为
\[
\ell_\star=\operatorname{rank}(Q^\top N).
\]
显式 SVD 构造达到下界；即便编码器跨所有 \(d_v\) 列混合，仍至少需要 \(d_v\ell_\star\) 个实坐标。对 exact rank-one Delta overwrite，只要保护方向与被擦除方向重叠，恰需一个 \(d_v\)-向量，而不是 \(p\) 个。修订还区分了自由逆解码的全局最优与固定 spectral-cut 解码器的状态/稳定性交换。

五路独立最终字节审查确认了定理、反例、来源碰撞、总成本与测量边界。旧的 hidden-mode、语义有效性、近 overwrite 放大和完整非线性递推边界都保留。R18 的一般 erased-fiber ledger rank、R12 的直接充分坐标、R19 的零误差 side code，以及 functional observer、Eckart--Young、invariant/JSR 理论覆盖主体机制；最强同信息对照就是同一个最优 lost-coordinate ledger。

因此 R13 attempt 3/3 耗尽并 park：candidate delta 0，实验效果未知，计数仍为 **5 historical / 0 active / 0 scientifically admitted / 0 selected**。没有运行模型代码、测试、训练、推理、评分或实验。下一条独立未耗尽路线是 R14 attempt 3。

### R13 v3 delivery closure

Substantive commit `a68d861d1bfcc8e7e2ccc006f98c9ebbe7f00eaa` was written to literal `main` with expected parent `7b1ccbcb2cfc4f1554c97aea4b87fe4d03d42f02` and `force=false`. All 15 substantive paths were fetched at that exact commit and matched the submitted bytes. Receipt: `research/delta-discovery-2026-10-08/sources/REPAIR_R13_V3_DELIVERY_READBACK.json` (SHA256 `5a44009c73c0a8440e38442226354a6a2ecb38c98b7b3f903cba72e89e458579`). This verifies delivery only, not originality, candidate admission, native measurement validity, empirical benefit, or experiment completion.

## R14 v3 可观测等价终止里程碑（2026-10-11）

[R14 v3 修复筛选](repairs/R14_REPAIR_LINE_SCREEN.v3.md)把 v2 尚未闭合的“外部有效 posterior 区间”收紧为可判定的两世界问题：如果两种真实 provenance 对全部写前可见记录的分布总变差为 `delta`，但要求相反 slot，那么任何统一有效的区间必须以至少 `(1-2 alpha-delta)_+` 的概率退化为 `[0,1]`。同一个公共观测质量给出任意更新器的锐 TV 下界 `(1-delta) lambda/(1+lambda)`；`delta=0` 时 v2 对称连续写精确达到该下界，而确定性硬写/不写控制会选择不写，允许混合时另有 `min{1,(1+lambda)/2}` 边界。

这不是把 R14 判作“以前全错”：v1 的 point-posterior Bayes action 与 v2 的 credal minimax action均保留。v3 只是证明，在不增加因果证据或分布假设时，Delta residual/hidden state/router score 作为同一记录的函数不能通过 data processing 制造 provenance 信息。独立数学、来源/原创性、对抗和原生测量审查绑定最终字节；R14 第 3/3 次修订后以有条件终止定理/control park，候选增量0，实际效果未知，没有执行代码或实验。下一条最早未耗尽的独立修复线是 R15 attempt 3。
