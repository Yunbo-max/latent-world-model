# Delta 数学发现后台阶段

用户请求：2026-10-08 23:42 Europe/London，Delta 数学推导 10–20 个，后台慢慢推进。

目标取 20 个实质不同候选；完整数学审查后全池排序、默认选择前15。Diffusion可选。阶段仅数学与来源/可行性审查，不含新模型代码或实验。

最新解释以 2026-10-09 17:08:50 Europe/London 反馈为准：“我们之前分析的都错误吗为啥这么严格”，“idea错误可以debug或者改正呀”。20 是约20条实质不同探索池目标，不保证20个全部原创、科学准入或实验成功；只选有资格者，数量不足诚实报告。先修复2–3条有证据线索，每条最多3次有具体delta的数学修订，保留旧字节/反例/review。局部错误、条件缺口、已知机制碰撞和效果未知分别处理；已知部分可保留为强对照，有价值理论也按相应贡献义务审查。

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
