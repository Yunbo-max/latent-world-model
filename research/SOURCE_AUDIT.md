# 原论文、实现与评测的阅读记录

检查日期：2026-10-07。下列“已读”指实际获取并检查所列部分，不等于复现结果、审完整仓库或完成原创性裁决。没有执行第三方项目代码、下载模型权重或下载训练/评测数据。

## 1. 直接相关的原论文

| 来源 | 已读范围 | 对当前设计的约束 |
|---|---|---|
| [Huginn / Recurrent Depth，2502.05171v1](https://arxiv.org/html/2502.05171v1) | 架构与循环训练部分，结合下表作者代码 | 共享循环、输入重注入、prelude/coda 已有实现；这本身没有证明持久世界状态语义 |
| [Coconut，2412.06769v2](https://arxiv.org/html/2412.06769v2) | 连续思维状态机制与训练课程，结合此前实际代码阅读 | 隐状态反馈不自动构成概率后验或环境动力学 |
| [BDH-CQ，2608.09888v1](https://arxiv.org/html/2608.09888v1) | 第 3–4 节的记忆更新与查询循环，及实现披露边界 | 广义“持久记忆 + 隐空间迭代”已有公开描述；精确维度和更新实现未完整公开，不能把第三方实现当作者源码 |
| [Iterative Amortized Inference，ICML 2018](https://proceedings.mlr.press/v80/marino18a/marino18a.pdf) | 第 3–4 节和后验修正形式 | 学习迭代后验更新是既有方法族 |
| [Amortized Variational Filtering，NeurIPS 2018](https://proceedings.neurips.cc/paper/2018/file/060afc8a563aaccd288f98b7c8723b61-Paper.pdf) | 第 2–3 节，尤其式 8–13、Algorithm 1 | 先验初始化、观测条件下反复优化、再推进外部时刻已有推导与实现 |
| [Expectation Propagation，UAI 2001，作者修正版](https://tminka.github.io/papers/ep/minka-ep-uai.pdf) | 第 3 节式 8–11；PDF 第 3 页截图核对 | 原算法移除旧 site、重新近似并替换；不能把这个操作直接当作新方法 |
| [STARS，2605.26733v1](https://arxiv.org/html/2605.26733v1) | 第 3 节、第 5 节局部稳定性条件；[会议记录](https://proceedings.mlr.press/v306/yang26t.html) | 稳定循环和 Jacobian 正则有近邻；训练惩罚不能直接当作全域压缩证明 |
| [Readout Blind Spot，2606.24898v1](https://arxiv.org/html/2606.24898v1) | 第 2 节尺度可见性与循环活动性的局部分析 | 读出忽略的状态方向仍可影响后续循环；不能从读出稳定推出整个动态受控 |
| [Focused Belief Propagation，AISTATS 2010](https://proceedings.mlr.press/v9/chechetka10a/chechetka10a.pdf) | 查询敏感度定义、式 7–9 和第 3.1 节 Algorithm 1 | 查询相关的敏感度计算已有先例；Q01 需进一步做算子与复杂度对照 |

另外检索到 [Residual Belief Propagation](https://arxiv.org/abs/1206.6837)，目前只核对到原论文元数据，未完成全文阅读。它必须留在 Q01 的待审查近邻清单，不能因尚未读取而视为没有重合。

## 2. 真实作者代码：精确版本与阅读范围

### Huginn

- 仓库：[seal-rg/recurrent-pretraining](https://github.com/seal-rg/recurrent-pretraining)。
- 固定提交：1ea7220ec7eb42d13e89db0663df254d0bcdc28e。
- 已读 README，以及 [recpre/raven_modeling_minimal.py](https://github.com/seal-rg/recurrent-pretraining/blob/1ea7220ec7eb42d13e89db0663df254d0bcdc28e/recpre/raven_modeling_minimal.py) 的 forward、iterate、core、循环采样与初始化相关区间。
- 源码能确认状态与输入嵌入进入循环、循环次数可控，以及前后处理与共享核心的分工。没有运行，也未完整审查训练实现 recpre/model_dynamic.py。
- 大规模作者训练配置不能直接移用到用户的 2080 Ti；这里只复用结构认知。

### Coconut

- 仓库：[facebookresearch/coconut](https://github.com/facebookresearch/coconut)。
- 此前已读并保留的固定提交：27273cb8cca4bb763c041a63b036d0c3b7cbbb48。
- 读取范围：coconut.py、run.py、dataset.py、示例配置、README 与依赖声明。
- 本轮只复用这些既有源码阅读，不声称重新核查了后续仓库版本或已复现论文。

### AVF

- 仓库：[joelouismarino/amortized-variational-filtering](https://github.com/joelouismarino/amortized-variational-filtering)。
- 本轮固定提交：f1032d62761c498e5206c0a2b07a012c8223b3de。
- 已获取仓库树；实际检查 [lib/models/srnn.py](https://github.com/joelouismarino/amortized-variational-filtering/blob/f1032d62761c498e5206c0a2b07a012c8223b3de/lib/models/srnn.py) 的编码、infer、generate、step，以及 [util/train_val.py](https://github.com/joelouismarino/amortized-variational-filtering/blob/f1032d62761c498e5206c0a2b07a012c8223b3de/util/train_val.py) 的外部步与内部推断循环。
- 实现确实提供梯度/误差信号编码，在同一观测下多次推断，然后推进时序状态。该实现依赖旧版软件接口；未安装、运行或移植。

STARS 与 Readout Blind Spot 的作者实现本轮尚未审查。EP 本轮阅读的是作者原文算法，没有宣称审过其完整代码。

## 3. 原生评测调查：LongMemEval

- 作者仓库：[xiaowu0162/LongMemEval](https://github.com/xiaowu0162/LongMemEval)。
- 固定提交：9e0b455f4ef0e2ab8f2e582289761153549043fc。
- 实际阅读 README 与 [src/evaluation/evaluate_qa.py](https://github.com/xiaowu0162/LongMemEval/blob/9e0b455f4ef0e2ab8f2e582289761153549043fc/src/evaluation/evaluate_qa.py)。
- 数据入口：[作者清理版数据](https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned)。本轮未下载，也未读取真实数据行。

文档与代码显示任务含多会话记忆、时间关系、知识更新和拒答等能力，原生问题有固定 ID 和对应历史。scorer 使用按题型构造的模型评判；不能悄悄替换为字符串 exact match。

需要核对完整 question_id 覆盖、历史输入与标签边界、原生判断提示和分母。与答案相关的检索标签不能作为模型输入。评判模型的成本与实际运行条件尚未落实。

README 指向后续的 [LongMemEval-V2](https://github.com/xiaowu0162/LongMemEval-V2)，本轮未检查 V2，因此没有把旧版审查描述为当前全领域覆盖。

**状态：候选评测来源，未冻结。** 它不自动解决预训练数据、世界动力学识别或 2080 Ti 上的训练可行性。没有原生输出、合格基线、统计结论或 Gate 0 PASS。

## 4. 本轮检索的范围与限制

检索覆盖了循环隐空间推理、持久记忆、迭代后验、证据 site 重估、循环稳定性，以及查询相关的残差/敏感度计算。最近资料以原论文和会议主站核对，代码以作者仓库固定提交读取。

这是**初步相邻工作调查**。尚未完成全部查询族、引用展开、独立角色审查和收敛检索；不作“没有先例”或高置信 KILL 裁决。主笔同时生成并检索了 Q01，不能把自审写成独立原创性审查。

已知功能重合要求回到母问题检查剩余贡献价值，不能不断把项目缩成一个小停止策略以逃避原始目标。当前完整模型、数据与实验设计均未获准冻结。

## Actual full-plan source review, 2026-10-08

Primary reading and fixed implementation pins are recorded in the independent [episodic spec review](../rounds/full-plan-2026-10-08/EPISODIC_SPEC_REVIEW.md) and [dynamics spec review](../rounds/full-plan-2026-10-08/DYNAMICS_SPEC_REVIEW.md), with actual source follow-ups in that round. LongMem author memory add/retrieve and neural-consumption files were read at b7f3c6b8db7471eb507971451f63f67e21c49ebf; Memorizing Transformers historical kNN/attention supports a family, not our lexical/raw-event implementation. Stable Recurrent Models supplies the tanh/operator-norm contraction premise; our differentiable Frobenius rescale is an explicit construction, not an asserted author-code reproduction. Gisting masking/cache source was read at3be0d062b6bdfd3caf51843bbc60261a0855f876, and Huginn model_dynamic at the existing pin; no source was executed. Latent conditional decoder precedents do not identify this model's semantics. Read-scope details, limitations and URLs remain in those review files rather than claiming every source repository fully audited.
