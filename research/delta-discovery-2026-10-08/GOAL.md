# Delta 数学发现后台阶段

用户请求：2026-10-08 23:42 Europe/London，Delta 数学推导 10–20 个，后台慢慢推进。

目标取 20 个实质不同候选；完整数学审查后全池排序、默认选择前15。Diffusion可选。阶段仅数学与来源/可行性审查，不含新模型代码或实验。

实际服务：复用 scheduled_authoring_continuation 任务 `6ac78ded796081918d2123402544d760`；按小时续接。此文件不是启动回执，连续执行未经证明。原代码阶段已完成/停用历史保留。

恢复入口：同commit的 PROGRESS.json、method-batch.json、项目 research/workflow-checkpoint.json。

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
