# Delta 主张的原生测量可行性

本记录只核查公开 benchmark 的原始任务、数据格式、native scorer、信息访问与大致成本。未下载数据，未执行 scorer、模型、测试或实验；没有新造 benchmark、样本、标签、metric 或结果。

## 主张—资产映射

| 资产 | 可支持的有限主张 | 不能支持的主张 | 原生边界 |
|---|---|---|---|
| bAbI 20 tasks | 短程顺序状态更新、事实覆盖、时间推理、路径与多跳；tasks 1--3、5、14、19 尤其相关 | 不能证明长距离保留；没有 paired order-swap，不能识别 commutator | 官方生成器 `facebookarchive/bAbI-tasks@ccd8fd6...`；ParlAI `a29567f...` 的 1k/10k teacher。保留 20 tasks × 1,000 test = **20,000** 分母。ParlAI 对 task 8/19 的逗号标签规范化不能与 raw-label scorer 混报 |
| LAMBADA | 篇章级非局部线索对自回归语言建模有用 | 距离不可控；不能区分保留、推理或语言能力；不测写入顺序 | 官方 Zenodo v1，测试 **5,153**。EleutherAI harness `d6de816...` 的 `lambada_standard` 是可信第三方实现，不是作者 scorer；必须冻结 standard，不能与 OpenAI 预处理版混用 |
| RULER v1 | NIAH 的远距检索、variable tracking 的长上下文多跳绑定、aggregation 的累积统计及长度曲线 | VT 无反向/交换配对，NIAH 不测状态修订；不能单独证明隐藏状态的传播机制 | 官方 main `c3f5e3b...`，v1 新流水线 branch `e8bbff6...`；13 tasks、每 task/length 500。scorer 是大小写不敏感 substring/reference coverage，额外错误文本不受罚，必须保留 null counts |
| LongMemEval | 在线时间顺序、knowledge-update 与 temporal-reasoning 最贴近修订顺序；S/oracle/M 区分历史长度与证据可见性 | KU prompt 允许“旧信息 + 新答案”仍判正确；不直接测矩阵 commutator | 官方 repo `9e0b455...`、cleaned release、500 questions。QA judge 固定 `gpt-4o-2024-08-06`，与无付费服务约束冲突；本地替代 Llama-3.1-70B 不适合单卡 RTX2080Ti。retrieval scorer 只适合显式暴露 session/turn retrieval 的方法 |
| BABILong | **delayed influence 最强现有资产**：20 个 bAbI task 的事实散布到 PG-19 长文，可按 task×length 观察传播/组合退化 | 仍无 paired order-swap；长度同时增加 distractor，不能仅凭总分归因于传播算子 | 作者 repo `booydar/babilong@7a6efee...`；100/1,000 samples per task-length。`metrics.py` 从封闭标签集提取答案并要求唯一正确标签/集合，比 RULER substring 更严格 |

## 对本轮方向的判定

- **delayed influence/长期传播**：`conditionally_measurable`。首选 BABILong task×length 曲线；RULER VT/NIAH 次级交叉验证。若只改善 NIAH 而不改善 VT/BABILong 多事实任务，更像检索改善而非一般传播改善。
- **commutator/更新顺序敏感性**：`measurement_gap`。LongMemEval KU/TR 与 bAbI task-wise accuracy 只能显示结果层面的时序保持；没有原生 paired swap 协议。不得自行反转样本或造配对 benchmark 来填洞。
- **LAMBADA 与标准 bAbI**：保留为全量语言/短程控制，不作上述机制主张的决定性证据。

## 信息公平与强基线

普通 Delta/fixed-K、Gated DeltaNet、KDA、RWKV-7 及候选去掉特定机制的同骨架消融，必须使用相同参数规模、target tokens、数据顺序、生成预算和原生样本。若使用 RAG/oracle/supporting-fact IDs，必须单列额外信息访问：bAbI supporting-fact index 不可给普通模型；LongMemEval 的 `answer_session_ids`/`has_answer` 只供 scorer；任何索引、top-k、CPU RAM、额外模型与检索耗时均需计账。

## 规模边界（不是运行承诺）

- bAbI：20,000 短样本，适合完整低成本控制，不是长程证明。
- LAMBADA：5,153 passages，结论范围窄。
- RULER：13 tasks × 6 lengths × 500 = **39,000 generations**，4K--128K 累计约 **1.64B 输入 token positions/arm**；仅 VT 约 126M。未在 2080Ti 验时。
- LongMemEval-S：约 57.5M 输入 token positions/arm，另加 500 回答与 500 judge 调用；M 约 750M。官方 QA judge 当前受权限/付费约束阻塞。
- BABILong：单一 32K 长度，100-sample 全 20 tasks 约 64M 输入 token positions/arm；1,000-sample 版约 640M。跨全部长度必须另算累计预算。

这些映射只证明资产与主张的可测范围，不证明任何候选有效，也不构成完整实验矩阵或 dispatch。
