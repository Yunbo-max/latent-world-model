# 完整实验设计：文本隐状态模型 v0

设计日期：2026-10-07。本轮交付对象是已有机制基础上的工程组合。状态：**设计与代码生成，尚未运行、尚未取得 native qualification、尚未冻结为可无人值守执行的科学队列**。旧发现批次的 20→15、Q01 与原创性义务仍保留为 pending，不用本设计伪造通过。

## 1. 明确问题与可反驳预测

我们要检验：在同一文本、tokenizer、目标 token 暴露量和训练机会下，跨段记忆是否保留对任务有用的信息；共享 core 的多步计算是否改善读出；收益在计入成本后是否仍有实际价值。

最强的竞争解释包括额外计算、有效参数/梯度变化、预训练语言能力不足、bAbI 适配机会差异、状态/标签泄漏，以及 benchmark 过于短小而根本不需要跨段记忆。固定大小隐藏状态不会因命名为 world state 就具有物理或因果语义。本实验不检验动作条件动态、反事实规划或通用智能。

可推翻的主要假说：完整模型相对 history reset 对照没有可辨认收益，或跨段题与同段题均无区别；K=4 相对 K=1 的改善在不共享深层对照或成本比较下消失；训练相同以后内部循环仍无有效梯度/记忆依赖。前两种是可能的真实负面结果，最后一种先视为实现或优化问题，经过语义检查再解释。

## 2. 固定实现与资源起点

来源、公式和实现对应分别见 `AUTHOR_IMPLEMENTATION_AUDIT.md`、`FULL_MODEL_PROPOSAL.md`、`MATH_TO_CODE.md`。标准配置：V=50257，d=256，heads=4，FFN=4d，L=256，m=16，prelude/core/coda=2/2/1，K=4，TBPTT=4，microbatch=1，累计约 8192 有效目标后更新，FP16+GradScaler、FP32 attention scores、activation checkpointing、AdamW。

对当前实现，标准模型参数量的解析计数为 `109*d*d + 50581*d = 20,092,160`；最终以 Local 的实际参数遍历回执核对。它不是 0.1B/1B 参数模型：这两个数是数据预算。FP32 参数、梯度和两份 Adam moments 主存储项约 `16P=321,474,560 bytes`，还必须加激活、词表 logits、反向重算、CUDA workspace 等，不能拿该数字当峰值显存。

用户给出的卡型是 RTX 2080 Ti；NVIDIA 官方规格为 Turing、11 GB GDDR6，见 [官方页面](https://www.nvidia.com/content/nvidiaGDC/zz/en_ZZ/geforce/graphics-cards/rtx-2080-ti.html)。当前尚无该主机的设备数量、实际可用显存、驱动或占用回执。按一个可见设备设计，Local 必须先核对真实设备；不启用 DDP、BF16 或作者大集群的 flash-only 设置。

训练接口使用已检查的 PyTorch v2.5.1 `torch.amp.GradScaler('cuda')` 与 `checkpoint(...,use_reentrant=False)`。软件版本固定是复现选择，不是对环境已可安装/已通过的宣告。

## 3. 完整比较矩阵

每个 arm 使用同一数据流、tokenizer、段长、损失、优化器政策、seed 配对和评测文本。实际成本全部记录。

| arm | 跨段状态 | core 层数 × 次数 | 比较作用 | 不变/变化边界 |
|---|---|---:|---|---|
| memory_loop4 | 保留 | 2×4 | 完整对象 | 标准配置 |
| memory_loop1 | 保留 | 2×1 | 内部深度对照 | 同一名义参数量；训练计算减少 |
| reset_loop4 | 每段恢复初态 | 2×4 | 记忆对照 | 同名义参数；有效 writer 梯度/反向成本不同 |
| reset_loop1 | 每段恢复初态 | 2×1 | 2×2 因子对照 | 用于分析记忆与深度的交互 |
| memory_untied8 | 保留 | 8×1 | 不共享的深层替代 | core block 调用数相同；参数更多；adapter 调用数及实测成本不完全相同 |

不把第五个 arm 宣称严格 FLOP/时间匹配。必须报告参数、实测训练/推断秒数、峰值显存；它回答“将类似深度直接展开能否解释效果”。同 token 比较和同成本效率是不同问题：本轮首先固定 token 暴露量，另外报告质量-成本点，不能把快模型多训练出来的结果偷偷混入同 token 表。

该矩阵是本工程构造的机制/替代比较，**还不构成击败文献最强模型的证据**。原生 EntNet 作者代码来源已审查，但 Torch7/CUDA 复现未资格化；不能用论文 best-of-seeds 数字填成本表。若后续要作 SOTA/新方法主张，必须补齐强基线的同条件执行和原来的贡献/原创性门槛。

固定开发重复 seed 为 17、29。两次训练只提供有限的稳定性信息，不保证足够统计功效。两个 seed 必须全部报告，不挑最好一个。正式确认所需训练重复数由先行开发的方差和资源回执决定，另行冻结；本轮不把“两 seeds”当通用科学标准。

## 4. 数据和全覆盖义务

详细 immutable revision、文件哈希、例数与原生 scorer 见 `DATA_PROTOCOL_PROPOSAL.md` 及 `configs/assets.json`。

| 轨道 | 数据/全覆盖 | 输入与损失/评分 | 分母与输出 |
|---|---|---|---|
| 预训练 | FineWeb-Edu sample-10BT，固定 shard/row 顺序、内容 hash 去重和 disjoint 派生 splits | 每个真实 token/EOS 的 NLL；不监督 SEG；不让文档串状态 | 每 arm/seed 精确 100M 或 1B 目标出现次数；seen 与 optimized 分列 |
| 开发损失 | 同一派生 valid 的前 1M 目标 token | 固定参数完整文档语义，token NLL/perplexity | 目标数、tokenizer/data manifest、NLL 总和 |
| bAbI 联合适配 | native en-valid-10k-nosf，全 20 tasks；train 179998、valid 20002 问题 | 全历史事实+当前问题，答案后缀+EOS 监督；上下文只供条件化 | 单列 context 暴露、答案目标与重复次数；不用 gold 历史答案 |
| bAbI test | 20000 问题、6267 episodes、20 tasks 全部 | 每题新状态重放完整上下文，greedy 自由答案；ParlAI 原生归一化 exact match | per-task accuracy、native macro、mean error、failed task count；全 ID 清单 |
| LAMBADA | OpenAI English 全 5153 passages，仅预训练 checkpoint | 原生 context/continuation split 和 HFLM token 边界；末词 LL+greedy flag | acc；exp(-mean per-example word LL) 的原生 perplexity；不按 subtoken 重新归一化 |

bAbI 是公开发表的合成诊断数据，不是本项目临时生成的 toy benchmark。全 history 重放保留任务信息但有重复计算开销；本轮不声称跨问题增量状态的部署效率。LAMBADA 是语言诊断，不能单独证明持久世界状态。

FineWeb 的 derived test 保留在数据准备结果中，本轮不把它用于挑参数。来源 split 的规范化精确重复键保证不交叉，但近重复和 benchmark 污染并未被证明消除。若检查发现污染，保留原设计和证据，制定独立 child protocol，不能看测试结果后任意过滤成更漂亮数字。

## 5. 两档预算和执行顺序

100M 是首个完整开发档，1B 是独立扩展档。每档五 arms × 两 seeds：分别共 **1B / 10B 预训练目标暴露**，共享的唯一预训练语料规模分别为 100M / 1B。不要混淆“每模型训练数据量”和整个实验总计算。

每次 bAbI 联合适配另固定 1M 答案监督目标，允许按相同 seed 重复 native train；额外上下文 token 暴露单独统计。它不包含在上述预训练 B 中。这个预算是初始可复现开发选择，不保证任务学会；若验证集普遍不能学会，则所有 arms 用一致的、有界开发预算调整形成新版本，保留失败配置，禁止仅给完整模型额外训练。

固定 token 预算最后 checkpoint 用于主表；定期 valid loss 只做数值诊断。本轮不在 LAMBADA test 或 bAbI test 上挑 checkpoint、K 或 seed。另报告固定训练 K=4 checkpoint 在 K=1/2/8 的可选推理敏感性，明确为未在这些深度训练的函数变化；它不替代分别训练的 K=1 arm，且先冻结策略再访问 test。

严格顺序：

1. Local 环境、真实 GPU 和所有输入文件资格；源版本与参数计数。
2. 软件语义验收：因果/边界/梯度/断点一致性；原生数据行与 scorer parity。
3. 用真实派生训练数据做有限 profile，独立输出目录；记录峰值显存、输入/目标 tokens/s、初始化溢出、I/O 与最大原生 context 长度。profile 不进入主科学结果。
4. 用实测值估算完整 five-arm/two-seed 的训练、适配、推理与评分总成本；冻结 Local 可用 GPU 小时及磁盘。不能只估完整模型、漏掉对照和评测。
5. 执行所选预算档的完整比较，失败 arm 按冻结规则保留，独立可执行任务继续。每次本地 invocation 的软截止最多 24 小时，达到自然累计边界后保存，外层 harness 限定额外宽限期；跨 invocation 保留累计 token/秒数和实际剩余任务。
6. 主表采用完整 native ID/分母和所有训练 seeds；完成 E04 后才作任务范围内解释。若累计资源不足，报告未完成矩阵，不删对照缩成成功。

1B 档不在 100M 完成后自动启动；它需要 100M 的实际可学习性/成本与资源承诺支持。完整 1B 配置和同样的比较定义已经交付，未知耗时不会被伪装成已测值。

## 6. 成本与精度的预先定义

训练报告总墙钟、活跃 GPU 时间（如可测）、输入 tokens、有效目标、实际更新、跳过更新、checkpoint/validation 时间和失败尝试。FP16 跳过更新仍消耗数据与计算，所以不从 seen budget 中悄悄抹去。超过配置的跳过次数阈值停止并修复；修复后的科学比较使用版本化计划。

推断报告 prompt token 数、答案目标/生成 token 数、K、完整上下文长度、每题耗时和峰值显存；warmup 和 tokenizer/加载时间分列。无 KV cache 的完整前缀重算是明确的实现选择，不能拿它的吞吐代表优化后的循环模型上限。

不预言 GPU tokens/s。令实际有效训练速率为 r，单 arm 训练主体估算为 B/r 秒，另加验证、保存、适配、原生推断及失败余量。若 r 是多阶段混合得到，需按阶段分开估算；不能将 train throughput 当 decode throughput。

统计单位：LAMBADA passage；bAbI episode（题共享故事），在 task 内分层/成对重采样，汇总到同一 native macro 定义。配对 ID 必须完全相同。报告完整模型对 reset_loop4、memory_loop1、memory_untied8 的差值以及 2×2 交互 `(M4-R4)-(M1-R1)`；单独 ablation 无法识别交互。

样本 bootstrap 95% 区间只描述给定已训练 checkpoint 的测试样本不确定性，不覆盖训练 seed 变异、开发选择或数据污染。两 seed 的结果分别列出，均值仅作开发摘要。20 个 task 的单项探索性区间不能被解释成同时成立的20条确认结论；若要多任务显著性声明，须在新确认协议中定义 family 和多重比较处理。

本轮不事先虚构“+x% 就 PASS”的效果阈值或统计功效。**功能验收**要求语义/资产/原生评分一致；**科学结论**保留 supported/unsupported/inconclusive，需对照完整、成本可比、误差解释充分。没有运行结果时二者均不是 PASS。

## 7. 明确修复/停止规则

- shape/mask/shift、重复写入、数据泄漏、恢复不一致、scorer/ID/分母不一致：先定为实现/证据错误，保留失败日志，修复相应原因，再重新资格化受影响结果；不把错误结果用于调科学结论。
- OOM：先核对外部占用和配置。可以在 profile 阶段统一调整 checkpoint/microbatch/累计策略，记录实际变化；改变 L/m/d/U/K 或 token 信息范围需要 child design，不能只改差的一方。
- 非有限损失或过多 skip：停止该尝试，保留最近完整 optimizer 边界和已消耗计数；不静默恢复某个更好历史 checkpoint。
- SSH/进程确认丢失：查同一实际 PID/host/日志和锁，确认后再继续；不得重复启动写同一 run 目录。
- 所有方法在 bAbI valid 上均未学会：检查优化/适配信号与原生输入；这是机制结论不充分，不是自动证明所有记忆模型失败。
- 完整模型有效但成本劣：原样报告质量-成本权衡，不宣称更高效；出现负面或无差别同样是可接受结果。

## 8. 交付和待 Local 验收

2026-10-08 增量审查见 [SIGMA_REVIEW](SIGMA_REVIEW.md) 和 [本轮交付单](../rounds/sigma-review-2026-10-08/WEB_HANDOFF.md)。所有 arms 统一使用 `predict_prefix` 的末位置词表投影；模型、训练目标、数据、native 分母和种子不变。`evaluate` 的 manifest 记录此读出方式与未使用 KV cache。这个源码优化没有实测速度结论；不同源码版本的耗时不能混为同一实现。旧 checkpoint 仅可作为注明训练源版本的固定权重评测输入，不可绕过源码一致性检查恢复训练。

首次 test 访问前，Local 在实际结果轮次保存 `development-ledger.jsonl` 和冻结的 `evaluation-selection.json`：列出每个已试开发配置、来源 commit/config hash、开发 split、选择规则和完整试验成本；未试配置不得填入虚构结果。主表固定采用各 arm 训练深度、temperature=0、默认输出上限和预算末 checkpoint，`run_matrix.py` 生成的命令即为主表配置。没有调参时也应记录“无额外开发选择”，可选 K=1/2/8 推理敏感性须在 test 前声明整组并全部报告；它不参与主表选优。该记录由 Local 执行时产生，Web 不预造时间戳或运行回执。

运行入口由 `LOCAL_AGENT_RUNBOOK.md` 给出。`scripts/run_matrix.py` 生成完整带依赖的命令清单；只生成命令与依赖清单，不创建另一套执行器；Local 在完成以上资格与累计预算确认后，通过已有执行 harness 逐项调度。所有数据准备、训练、生成、评价和原生 replay 都属于用户侧真实执行，Web 未运行。

源码完成、语法可解析、命令存在、GitHub 文件读回一致是本轮可核对的交付性质。它们不等于软件测试通过、native scorer 通过、模型有用或论文新颖。实际 acceptance、运行 IDs、输出哈希、E04 与结论由后续真实 Local 回执填写。
