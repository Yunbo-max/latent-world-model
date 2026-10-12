继续 Yunbo-max/latent-world-model 的同一 Delta 验证目标，执行用户于2026-10-12的最新授权：“可以用cpu先检验，rsi-simple吧插件”“我觉得你可以开始了去验证所有实验”。这取代旧任务中的数学阶段禁执行、暂停及20→15配额前提，仅针对当前Simple CPU阶段；不授权收费服务、GPU、容器、另一个主机或新的模型数据接口。不要创建重复任务，不开展无关的新idea池。

工作身份：wake task 6ac78ded796081918d2123402544d760；科学模式 rsi-simple0.3.0-simple.9；CPU idea validate-delta-mechanisms；当前goal_contract_version=1，源digest=e2b9d1c04fdb680bdf6e069ec387d84ec8f92efed5c44f59b7724ab446db5ae8。主目录 /workspace/scratch/99b5aeb15819/research/delta-cpu-validation-2026-10-12。这是定时接续实际研究和实验的任务，不是提醒；定时唤醒不等于期间持续计算。

先读取实时main，恢复该目录的 README.zh-CN.md、AGENTS.md、POLICY_TRANSITION.json、checkpoints/CPU_CHECKPOINT.json、RESULTS_SUMMARY.json、coverage_inventory.json、review/COVERAGE_REVIEW.md、review/INDEPENDENT_NUMERICAL_REVIEW.md及具体未闭条目的钉住原文。已核验首轮交付commit dec11d8b2b3b9ccb88894ab7ab6361fe1ec0b8c2，包含350个逐文件SHA核验通过的交付文件，后续实时main可能更先进；不能把该pin当永久最新。保留旧Delta历史、另一latent项目内容及他人写入，不覆盖旧数学证明的原字节。旧任务合同存于 checkpoints/PREVIOUS_TASK_CONTRACT.md。

当前已有实际证据：65个不同数值check ID，加1来源完整性check；R01–R20每条最新修复有代表性构造案例，另检查部分旧控制和信息论分支。15次成功数值命令，1次语法失败已用新任务ID修复，runner累计命令wall time9.624778882秒、attempts_used16；测试中65个数值检查均通过。它们不是65个独立模型训练/原生benchmark，不是每条定理的所有分支，不证明原创性、速度优势、SFT少遗忘或部署中RSI。已修复旧SPD存在性定理漏写的零因子identity例外，原来源保留。完整反馈梯度、局部保护未来失效等结论按具体构造条件解释；未来信息audit-control不可冒充公平部署对手。

如原目录/runner还在，先使用已有状态；否则从同一repo精确commit恢复，不能重新init或重置计数/预算。恢复包 RECOVERY.zip.b64 / RECOVERY_MANIFEST.json 包含70份钉住原文、vendor、SQLite一致备份、attempt/receipt/log和实际源代码。大文件连接器读取可能截断，优先用Git树中 recovery_parts/part-0000.b64 至 part-0269.b64的SHA fetch_blob：按文件名排序，核对每个blob和长度（前269个8192字符、最后4072），无分隔符拼接，核对manifest中的整包hash后用 scripts/restore_archive.py 恢复。不要仅凭短预览当完整包；不要为恢复生成新runner。路径不能原样恢复时明确对现存状态做路径重定位/reconciliation，保留原attempt身份、源digest、预算及deadline，不能暗中重新开始。

恢复后读取vendor/rsi-simple-0.3.0-simple.9的SKILL.md和本轮适用Simple指南；沿用固定source历史，插件被更新不静默替换已执行来源。先 status/inbox/health/alerts，检查真实PID和持久状态，再决定是否启动唯一runner supervisor，不能并发第二个writer或重复提交已完成任务。status/inbox输出很大，应保存在本地并提取关键信息，保留原数据而非在对话打印全量。已开放decision request在交接时为decision-b74c4313ba9b4d338d6dff7058781db5，但应采用实时inbox未消费请求。agent.command在此阶段为空，平台scheduled worker负责读取decision并通过Simple response/submit推进；不要声称已有自动模型命令或连续agent进程。

资源边界沿用已实际配置：单数值作业、BLAS/OMP请求1线程、guard_cpu data allocation limit256MiB；这不是硬RSS上限，真实线程未直接测量。宿主共享CPU约8核、cgroup8GiB，NumPy/SciPy已可用，Torch/pytest缺失，不能把共享宿主额度当独占。总max_attempts40、max_command_seconds3600、deadline_epoch1791881465.5041356，已用16次和9.624778882秒，保留累计历史；预算或deadline到界时保存准确未完成项/停止原因，不暗中提高、重置或把停止说成科学完成。

下一轮从最早未覆盖义务推进：
1. 从coverage_inventory和独立review选择有具体价值的旧控制/STEP2、遗漏条件或分支，绑定对应原文hash；完成数学预测、独立参考和可证伪数值设计，不能只多抽seed凑进度。尤其旧D05、保护预算/实际G能量与R17证书曲率区别、R08两个因果世界的完整构造及其他清单缺口。
2. 补FP32、近退化/病态条件及量化误差。区分理论假设失效、有限精度问题、实现bug和模型效果未知；发现错误先按版本修复并重新检查原失败构造，保留失败和全部结果。
3. 对有计算优势主张的机制计算构造、维护、query/update及状态成本，比较最强同信息、同容量简单JVP/VJP/ledger/Delta控制。当前小矩阵Jacobian差异及计时不足以证明速度收益；不要使用有额外未来信息/容量的臂制造优势。
4. 先核对既有公开原生任务作者文档、数据/代码与native scorer，再运行当前CPU真实可行的验证。允许用户已授权的当前CPU代码设计和执行；任何来源/安装/数据通路不可用只阻塞依赖项，先继续独立可行检查。绝不能用自制fixture指标填公开benchmark或完整LM结果表。旧13arms×2seeds的100M/1B均是每run预训练target-token预算，整个tier合计2.6B/26B预训练targets另26M适应targets；框架/数据/真实GPU主机未具备时明确pending，不运行伪缩小矩阵并称全部实验完成。

每批经同一Simple runner登记plan/input hashes、真正执行命令、读取原始输出、保留exit code、耗时及资源receipt；提出具体结果驱动下一步，必要时使用可用原生子代理做独立推导/审查，只有一个集成writer。重要修改绑定新bytes和review，当前角色的静态独立审查不等于未见确认或独立重复实验。不要写all done/pass只因任务命令成功。每批更新覆盖清单的已测具体条件和未测具体义务、中文结果、checkpoint及可恢复runner快照，提交同一main，expected_sha+force=false，精确commit逐文件SHA读回。遇到main新写入先读再合并，不能force/reset。

目标仍开放。继续完成全部当前CPU可检验义务并分别说明剩余原生LM/SFT/RSI实验的实际阻塞；不恢复旧20→15筛选终点，也不因首轮覆盖R01–R20而结束。若真实资源/权限/数据前提使后续全部依赖项无法继续，记录external_wait/具体缺口并报告，不能宣称整个goal完成。新异常（OOM/timeout/启动失败/来源或提交不完整）在实际发现的唤醒中及时报告并保留；同一无变化阻塞去重。只有真实重大结果、需用户处理的新阻塞或阶段交付时通知。
