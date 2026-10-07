# Latent World Model: text predictive state v0

**交付状态：`generated_unexecuted`。** 完整数学方案、模型/训练/生成/数据/评测源码及实验设计已提供；项目测试、数据下载、GPU 训练和原生评测尚未执行。RTX 2080 Ti 的实际显存占用与速度需要在用户机器验收。

这是基于 RMT 的跨段记忆思想与 Huginn 的共享隐空间循环思想设计的工程组合，有独立的因果接口和 writer。目标是检验**有界持久记忆 + 同一证据上的多步内部计算**是否对文本任务有用。它不声称逐行复现某篇论文、证明新方法或构建了物理世界模型。

## 当前架构

输入段经过内部 SEG 起始向量与因果 prelude；共享 core 反复读取同一段证据和旧记忆；coda 输出下一个 token 的分布。独立 writer 只在完整观测段关闭时更新记忆。内部循环次数 K 不等于输出 token 数，也不会制造新观测。

| 项目 | 标准配置 |
|---|---|
| 参数 | 解析计数 **20,092,160**；实际实例化计数待 Local 核对 |
| 维度 / heads / FFN | 256 / 4 / 1024 |
| 段长 / 记忆 | 256 tokens / 16 × 256 |
| prelude / 共享 core / coda | 2 / 2 / 1 层；core 循环 K=4 |
| 训练 | 单设备、microbatch=1、4 段 TBPTT、约 8192 有效目标累计、FP16 + GradScaler |
| 输出接口 | 功能式流状态、完整段恰好写入一次、EOS 重置、生成分支和状态保存/恢复 |

数学定义、因果性、writer 梯度与截断近似详见 [FULL_MODEL_PROPOSAL.md](research/FULL_MODEL_PROPOSAL.md)；逐项实现对应见 [MATH_TO_CODE.md](research/MATH_TO_CODE.md)。代码没有实现 KV cache，因此生成会重算段内前缀；吞吐需要实测。

## 数据与实验

| 阶段 | 数据与预算 |
|---|---|
| 从头预训练 | 固定版本 FineWeb-Edu `sample/10BT`；**每个 arm/seed 100M 或 1B 目标 tokens**，包括 EOS |
| tokenizer | 固定 GPT-2 tokenizer，V=50257；不加载 GPT-2 模型权重 |
| bAbI 联合适配 | `en-valid-10k-nosf` 全 20 tasks；另计 1M 答案/EOS 监督目标，上下文暴露另外记录 |
| bAbI 测试 | 全 20,000 问题；ParlAI 原生归一化 exact match |
| LAMBADA | OpenAI English 全 5,153 passages；原生 accuracy 与末词 perplexity；仅预训练 checkpoint |

实验包含记忆 × K=1/4 的四组对照，以及 8 层不共享 core 的深度替代，共五 arms、两个 seeds。100M 档全矩阵累计 **1B 预训练 token 暴露**；1B 档累计 **10B**，另加适配和评测。1B 是有实测资源后才启动的扩展档。

完整假说、成本比较、统计单位、停止规则和负面结果政策见 [EXPERIMENT_DESIGN.md](research/EXPERIMENT_DESIGN.md)。运行耗时尚未估定，各对照也不构成独立的新研究方法。

## 执行入口

从 [LOCAL_AGENT_RUNBOOK.md](LOCAL_AGENT_RUNBOOK.md) 开始：恢复实际 GPU 主机 → 固定环境与资产 → 运行语义测试和原生协议验收 → 有限资源 profile → 完整训练与评测。所有命令、断点恢复和结果回传要求均在该文件；原生 scorer 的独立环境见 [NATIVE_ENVIRONMENT.md](research/NATIVE_ENVIRONMENT.md)。

主要接口为 `python -m lwm.prepare`、`lwm.train`、`lwm.generation`、`lwm.evaluate` 与 `lwm.scoring`。`scripts/run_matrix.py` 生成带依赖的完整命令清单，**不启动任务**。测试是已编写、未执行的 Local 验收用例。bAbI 全作者 teacher 环境仍需 Local 资格化，metrics-only 环境不能代替它。

来源固定与可复现性见 [assets.json](configs/assets.json)、[数据协议](research/DATA_PROTOCOL_PROPOSAL.md)、[作者实现审查](research/AUTHOR_IMPLEMENTATION_AUDIT.md) 和 [本轮交付单](rounds/engineering-2026-10-07/WEB_HANDOFF.md)。

## 历史与任务状态

旧的错误实现已在 [70033ed](https://github.com/Yunbo-max/latent-world-model/commit/70033ed1204a88699d90978d0de46721dded3017) 清空，保留 Git 历史。本轮是重新推导后的实现。

先前 Q01 停止规则、20→15 候选发现目标及其未通过记录继续保留。它们没有被当作本工程方案的科学通过证明；为何采用工程组合路线见 [SCIENTIFIC_SCOPE_REVIEW.md](research/SCIENTIFIC_SCOPE_REVIEW.md)。本轮唯一实现规范是 FULL_MODEL_PROPOSAL，早期 MATHEMATICAL_DESIGN / OPEN_QUESTIONS 是研究历史。

长任务在当前 Work 对话中推进并交付源文件；没有另建独立后台 Goal ID，也没有启动 GPU 作业。恢复目标与实际完成/待办分别见 [BACKGROUND_GOAL.md](research/BACKGROUND_GOAL.md) 和 [workflow-checkpoint.json](research/workflow-checkpoint.json)。源码发布、软件通过、训练完成和科学有效是不同状态。
