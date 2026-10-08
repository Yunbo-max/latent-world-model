# 原方案完整代码：重新打开的 Work 作者任务

用户指令：2026-10-08 16:34 Europe/London，“我希望你用这个autopilot去在后台去实现整个code”“搞好”。

当前 v0 源码基线：0391e099923c74b6dbb195cc2afbe1d78e442516。v0 完整源码交付不代表以下原始设想全部落地。本轮重新打开 source-authoring 目标，不撤销旧交付或假造其运行验证。

角色：web_supervisor，generated_unexecuted。实验与软件/原生/GPU验收留给 Local。GitHub destination 为 Yunbo-max/latent-world-model / literal main；RTX2080Ti、100M/1B每arm/seed target-token预算不变。HF输出目的地未知，无上传。

## 原设想与当前源码的实际差距

| 项 | v0 实际代码 | 本轮交付义务 |
|---|---|---|
| persistent belief / reasoning workspace 分离 | MemoryWriter、_read、共享core；已实现源文件，未运行 | 保持独立状态及信息依赖，审查扩展后因果、梯度和幂等 |
| 三时钟 | observation segment / reader K / output token 已分开；无真实action/world transition | 完整流状态机与来源边界；纯文本不得冒称干预建模 |
| compressed predictive state | 固定连续slots；只有NLL | 明确概率/预测对象、可训练目标和条件；充分性是目标非已证明事实 |
| sparse episodic exact memory | 无独立事件库、检索器、模型消费接口 | 实现容量/事件身份/来源/检索/读入/保存恢复及真实训练生成接线 |
| semantic state Z / language codec | 仅coda和绑定词表线性投影 | 明确可执行语义/表达契约，避免重命名；完成训练生成路径及对照 |
| memory/reasoning 谱分析 | 条件性设计动机，没有参数化/谱约束 | 审查假设，选择有依据的可执行构造并给出合法界/诊断；不能把局部估计当全域证明 |
| adaptive compute / residual certificate | 固定K；Q01为未选未实现历史候选 | 仅在数学/来源/准入条件补齐后实现；不擅自把Q01宣布合格 |
| compression / reasoning / compute / realization 目标 | window_objective 只有cross_entropy | 从真实概率对象和可用监督推导各项；接通估计器、梯度、权重、日志与消融 |
| full system | v0 train/generate/native scorers已有 | 全部新增状态/模块端到端连入这些入口，完整benchmark、统计和成本设计同步 |

这是实际源码差距清单，不是宣布每种辅助目标都必要或原创。原始聊天的20候选叙述与仓库方法批次不一致：仓库只有一个未通过Q01。不能自填完成记录；已有机制工程扩展先写闭合规格和来源审查，新原创候选仍按research-autopilot恢复真正研究准入。

## 当前科学边界

- predictive sufficiency I(F;history|state)=0 是设计目标，未有估计/验证结果。
- 长期保留和快速固定点收缩的谱冲突只在同一模态/算子及所述假设下成立。
- BDH-CQ已有memory/workspace分离公开公式；Huginn/RMT/AVF等相关机制已有来源。新颖性仍未裁决。
- 不给任意确定性隐藏向量附加来源不明的KL，不把标准CE改名成新loss，不为了覆盖表编造动作或世界标签。
- 科学结果、软件通过、GPU可行性均没有新证据。

本轮实际检查来源：src/lwm/model.py、train.py、generation.py、research/MATHEMATICAL_DESIGN.md、MATH_TO_CODE.md、FULL_MODEL_PROPOSAL.md、SCIENTIFIC_SCOPE_REVIEW.md、SOURCE_AUDIT.md、OPEN_QUESTIONS.md及workflow-checkpoint。上述源码在v0精确SHA通过connector读取，不执行项目代码。

## 作者宿主和恢复

唯一现有定时任务：6ac78ded796081918d2123402544d760。
实际task lookup返回conversation_id：6ac79d14-9fc8-83eb-8a16-056c5fa87aaa；旧仓库字段对应更早宿主，应作为历史保留，不能覆盖当前服务回执。
当前Task查得disabled；本轮计划在本文件和goal精确main发布后恢复它，并请求立即触发。未收到实际服务回执前，不将启用/触发当作已发生。
计划沿用该任务hourly schedule。它是定时续接，不是已证明两次调用间持续运行的long-goal进程。
当前会话由平台明确为Work Mode。后续每次触发仍须核对实际宿主，不因task title认证。
只一个main writer；当前作者交付检查点之后才请求run-now，避免主动造成两个集成写入者。

## 完成和验收

先写必要数学/接口规格、读取原论文和作者实现、处理独立审查，再生成对应模块。复用完整v0和有效来源，不反复立项。每模块必须有明确真实输入、输出、训练/生成路径、持久化、native比较与日志/Local验收；不接受空接口、TODO或让Local重新设计核心算法。

全过程保存真实源进度和具体阻塞，分清implemented / source-reviewed / Local-unexecuted。终点是整个扩展构造和源码/完整设计/手册经审查、main精确读回；不是文件或测试数，也不等待未来训练完成才能关闭源码任务。全部覆盖完成后报告逐项表并停用同一个任务。

当前next action：在实际Work续接中逐项恢复原构造，并先完成episode/semantic接口的闭合数学和来源规格；同时保持旧v0可用性，随后开展源码实现。原始候选scientific gate不被本检查点认证。
