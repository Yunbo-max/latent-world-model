# Latent World Model: full text-state construction

**源码状态：generated_unexecuted。** 原方案的可执行文本构造已补齐：压缩预测状态、独立精确事件记忆与检索、belief/workspace 分离、观测/推理/表达时钟，以及可单独保存并读出的语言 plan。软件测试、原生资格、训练、2080Ti 显存和速度仍由 Local 验收。

当前入口：[完整覆盖表](rounds/full-plan-2026-10-08/COVERAGE.md)、[本轮交接单](rounds/full-plan-2026-10-08/WEB_HANDOFF.md)、[Local 操作手册](LOCAL_AGENT_RUNBOOK.md)。公式和真实边界见[采用规格](rounds/full-plan-2026-10-08/EXPANSION_SPEC.md)、[数学映射](research/MATH_TO_CODE.md)。旧 v0 的模型分支和配置仍是对照。

模型将已完成段压缩进连续 slots，同时保留容量受限的精确 token 事件。每个预测位置仅用已知前缀检索历史，原始 token 经新鲜嵌入和独立注意力被实际读取。固定 K 的工作区计算与 writer 更新分开；可选受约束 tanh 动力学具有固定 forcing 下的实数收缩界。工作区形成低维 Z，独立语言模块仅从 Z 输出分布。生成、训练、native 评测及保存/恢复均消费这些接口。

新增训练目标是压缩状态对同文档下一段首个 eligible token 的 proper categorical CE；主文本 CE、辅助 CE 和目标出现次数分别记账。它不估计完整 predictive sufficiency。连续 plan 也不代表已识别的句级语义、可逆 codec 或动作/物理世界状态。已知机制与文献重合保持可见；新颖性和历史 Q01/adaptive stopping 未被本工程交付认证。

| 项目 | 已选构造 |
|---|---|
| 默认扩展 | d256 / heads4 / FFN1024；段256；memory16x256；K4 |
| 事件检索 | 原始历史4096 tokens；最多2事件 / 512读取tokens；query32；lexical或recency |
| plan / 动力学 | Z宽128；独立realization；c0.9的固定forcing收缩分支，Transformer分支保留 |
| 训练 | 单卡、FP16 autocast/GradScaler；TBPTT4段；累计8192 eligible targets；beta0.1 |
| 恢复 | 模型/optimizer/scaler/RNG/cursor；memory/事件/receipt；部分prefix/来源/三时钟；严格身份 |

完整[实验设计](rounds/full-plan-2026-10-08/EXPERIMENT_DESIGN.md)保留 bAbI 全20 tasks / 20000问题和 LAMBADA 全5153。固定 FineWeb-Edu/GPT-2 tokenizer，无预训练权重。13 arms × 2 seeds，100M/1B是**每arm/seed预训练目标tokens**；累计2.6B/26B，另加26M bAbI适配目标及context/验证/评测/失败成本。全部204依赖卡含原生replay、成对比较及四组交互。矩阵生成器启动零个作业。

主要入口：`lwm.prepare`、`lwm.train`、`lwm.generation`、`lwm.realization`、`lwm.evaluate`、`lwm.native_parity`、`lwm.scoring replay/compare/interaction`、`scripts/run_matrix.py`。精确输入获取、环境、运行顺序和失败处理均在 Local 手册。无Docker、无付费服务、无Web GPU执行。

当前独立源码审查见[状态/因果报告](rounds/full-plan-2026-10-08/CONTINUATION_STATE_REVIEW.md)和[数学/训练/统计报告](rounds/full-plan-2026-10-08/CONTINUATION_TRAINING_REVIEW.md)。审查与静态解析不等于测试通过或科学有效。当前完整的是上述已定义文本工程构造；更广的原创发现、充分性/句级语义/动作模型/自适应证书不被宣称完成。

历史清空提交70033ed、v0交付及旧20→15批次保留。[当前检查点](research/workflow-checkpoint.json)与[目标记录](research/BACKGROUND_GOAL.md)区分源码、发布、运行和证据状态；[v0完整定义](research/FULL_MODEL_PROPOSAL.md)及[原实验设计](research/EXPERIMENT_DESIGN.md)继续作为历史/对照文档。
