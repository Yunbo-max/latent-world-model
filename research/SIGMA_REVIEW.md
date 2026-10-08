# Sigma 阅读后对本项目的决定

2026-10-08；父版本 `a8a86cf359ac0d8598ac7b2fa6465ffa120718ae`。这是已有模型的文献审查和有界工程修订，不是新的候选方法或 Sigma 复现。Web 交付状态为 `generated_unexecuted`。

## 1. 一手来源与实际可复用范围

[Large Language Continuous Diffusion Models, arXiv:2610.02665v1](https://arxiv.org/pdf/2610.02665v1)。以下是压缩的事实摘要；完整推导应直接读原文，而非把本文当作论文替代品。

Sigma uses blockwise Gaussian diffusion over 16-dimensional token embeddings, with causal clean context and bidirectional noisy blocks. Its objective combines a diffusion likelihood bound with an auxiliary autoregressive loss. Self-conditioning, score steering, embedding regularization and trajectory distillation address different stages. The named 3B/8B models contain 3.8B/8.5B total parameters; flagship training starts from a 1T-token AR checkpoint and adds over 300B tokens. Algorithm 2 counts an additional final readout beyond diffusion steps. Low-step quality remains limited; reported CFG timing uses H100/BF16 and first-block measurements. Sampling lanes are not independent training seeds. The diffusion perplexity is bound-based. Appendix D and E differ on endpoint weight decay, requiring implementation clarification.

事实定位：§2–3（印刷页 2–5）、§4–6（页 6–10）、Appendix B（页 22）、D Algorithms 1–2（页 26–27）、E（页 28）、G.1（页 34）、G.10/Table 20（页 44–45）。根会话阅读了主文及 B/D/E 的相关算法、优化与限制；独立审查补充 G.1 的评分口径和 G.10 的计时条件。D/E 的 weight-decay 差异是文字规范的不一致，不能替作者猜定实际实现。

[共同主导作者 Wei Guo 的 2026-10-07 公告](https://alexandreguo2001.github.io/)说明代码和权重正在内部审核、尚待发布；2026-10-08 查阅。[第一作者论文页](https://zhihanyang.com/about/)也只给出论文入口。已做有界的作者主页、GitHub/Hugging Face 和 NVIDIA 来源检索，**未资格化任何 Sigma 代码 commit、checkpoint、配置、loss/sampler 或 scorer 文件**。论文伪代码不等于读过发布实现；版本状态是 preprint/read，reproduction 是 not_attempted。

本项目已有的 Huginn/RMT/EntNet 代码以及 bAbI/LAMBADA 原生协议审查沿用父版本 [AUTHOR_IMPLEMENTATION_AUDIT](AUTHOR_IMPLEMENTATION_AUDIT.md) 和 [DATA_PROTOCOL_PROPOSAL](DATA_PROTOCOL_PROPOSAL.md) 中的固定来源；没有更换 tokenizer、数据资产或评分器。原始 Q01/discovery 未完成记录继续保留。

## 2. 数学审查：先区分当前模型的对象

本仓库的已实施对象由 [FULL_MODEL_PROPOSAL](FULL_MODEL_PROPOSAL.md) 唯一定义：

\[
M_s=U_\theta(M_{s-1},X_s),\quad
H^{k+1}=F_\theta(H^k,E,M_{s-1}),\quad
p(x_i\mid M_{s-1},x_{<i})=\operatorname{softmax}(o_i).
\]

这里的段索引 s、内部深度 k、输出位置 i 是三个不同轴。M 是已观察历史的确定性压缩，H 是当前条件函数的工作区；二者都未被定义成随机前向加噪变量。当前直接 NLL 的归一化来自逐 token softmax，不能仅凭隐藏表示是连续向量就改称扩散 ELBO。引入噪声预测、双向目标块或蒸馏 teacher 都会改变生成过程、信息集合和学习目标，必须形成另一个完整设计；本轮没有足够的发布实现与小预算证据支持这样替换。

一个与球面表示有关的通用反例也约束未来构造：若单位向量 a 与 −a 各占概率 1/2，其均值是 0，不能归一化成单位向量而仍称其为同一后验均值。若候选表示需要概率语义，必须区分“原子表示受约束”和“概率加权均值受约束”。当前 writer 的逐坐标凸组合只证明 M 的幅度界；没有证明概率校准、收缩、语义独立或槽多样性。因此本轮不向 writer 添加未经任务推导的球面正则项。

## 3. 从当前源码推出的精确读出优化

发现：父版本 `predict_prefix` 调用 `_read` 生成全部位置的 V 维 logits，再取最后位置。实际只需要下一个 token 分布；未使用的投影仍消耗计算和内存。

设 prefix 长度为 u，加入 SEG 后 n=u+1；D 是**完整** prelude、全部 K 次 core 和完整 coda 得到的 `[batch,n,d]` 隐状态。R 只选最后位置，N 是当前逐位置 RMSNorm，W 是共享词嵌入。则

\[
R\{N(D)W^\top\}=\{RN(D)\}W^\top=N(RD)W^\top.
\]

第一步是矩阵乘法对行选择的分配律；第二步依赖 N 不混合位置。W、归一化参数和所有先前计算均相同。由此只在最终 norm/projection 前取 `hidden[:, -1:]`，就得到同一条件函数的末行。它还保留对所有上游可达参数的数学导数。

不能把 R 提前到因果 self-attention/coda 之前：末位置仍需要前面位置的 key/value。这个改动不是 KV cache，也不删除 reader 内部前缀。训练 `forward_segment` 仍投影全部监督位置，writer 与提交状态机均保持原函数。不同矩阵形状可能引起浮点舍入差异，因此验收是合理精度下 logits/梯度一致，而非跨设备 bitwise 相同。

**可以推翻的具体预测：** 最后投影只消费每条序列一行；其输出与完整 teacher-forcing 最后对应行一致；非最后监督行仍存在；初态、记忆和权重均不改变。任一性质不成立就是实现错误，不能解释成模型改进。

将 multiply-add 计作两个 FLOPs，最后词表矩阵乘法从约 `2*batch*n*d*V` 减为 `2*batch*d*V`；这是单个算子的计数，不是整个模型加速比。显式 logits 输出从 `batch*n*V` 减为 `batch*V` 个元素。默认 batch=1、u=255、V=50257、FP32 时，输出张量减少 `255*50257*4=51,262,140 bytes`，约 **48.887 MiB**。这不是测得的峰值下降；allocator、工作区、其他激活和舍入均需 Local 验收。空 prefix 时 n=1，没有此项节省。

## 4. 2080 Ti 与训练预算的可比性

在本项目采用的 FP32 参数/梯度/两份 Adam moments 核算下，仅主存储项为 16P bytes：20,092,160 参数对应 321,474,560 bytes；3.8B 与 8.5B 参数分别为 60.8 GB 和 136 GB。这个独立估算尚未包含激活和工作区；将大模型原样放进当前单卡训练方式没有依据。CPU offload、量化或参数高效适配会形成不同的系统与实验，也不是当前已资格化路径。

保持当前 100M/1B **每个 arm/seed 的目标 token 预算**，并报告全部训练历史。预训练权重的既有暴露不能记为零，也不能把继续训练的 token 数与从头训练相等视为同一学习资源。主矩阵仍为五 arms × seeds 17/29：100M 档累计 1B，1B 档累计 10B，另计 bAbI 适配、上下文重放、profile 和失败成本。1B 扩展依赖真实可学习性和累计资源；不自动启动。

保持 FP16+GradScaler 训练及当前显式 FP32 数值保护；不从其他硬件的 BF16/吞吐结果推定 2080 Ti 的执行能力。这个读出优化主要作用于生成与末词评分，不减少 `forward_segment` 的训练词表投影。

## 5. 对完整实验设计的实际影响

| 结论或竞争解释 | 已交付的区分方式 | 本轮新增约束 |
|---|---|---|
| 更深只是花了更多算力 | 固定 token 的 K=1/4 与 untied8 对照；质量和实际成本并报 | 所有 arms 使用同一末位置读出实现，K/core 调用数不充当 FLOPs 或 tokens/s |
| 持久记忆是否有用 | memory/reset × K 的 2×2 对照；完整 native IDs | 幅度/秩等诊断不得代替任务有效性 |
| 数值优化是否改变预测 | teacher/prefix、边界、EOS 与梯度语义测试 | 新增末行读出数值/梯度一致与投影行数检查；Local 实际运行 |
| 热启动或选择引入额外收益 | 从头预训练；固定预算末 checkpoint；valid 开发与 test 分离 | 测试前保存全部开发配置与选择记录，未执行项保持空结果 |
| 速度来自未计入的成本 | 训练 events、完整 evaluator 墙钟/显存/tokenization 记录 | 报告设置、输入/输出长度、首例计时、未使用 KV cache；没有测量前不作速度结论 |

不新增一个未经实现/资源资格化的 Sigma 基线，也不将本项目 bAbI/LAMBADA 数字与其他任务的论文表格相减。原 [EXPERIMENT_DESIGN](EXPERIMENT_DESIGN.md) 的全 20 个 bAbI tasks、20,000 test 问题、5,153 LAMBADA passages、全部对照、失败记录和原生 scorer 义务保留。

本轮不用开发后挑选最有利的 K。主表仍采用各 arm 自己训练的深度。K=1/2/8 的推理敏感性如果启用，应在首次 test 访问前冻结并完整报告，不能据此替换主表。

## 6. 后续边界

当前可交付的是有出处的模型定位、独立的等价推导、对应源码和完整 Local 验收说明。软件实际通过、原生接口资格、2080 Ti 吞吐/峰值、完整训练及科学结论仍待 Local。

未来若要转向连续扩散，应先取得可固定版本的作者实现/权重，核对 loss 分母、梯度路径、掩码、精度、优化组与最终 readout 计数，并建立符合预算的完整竞争假说与实验。这里记录研究入口，不创建一个未经过推导的扩散模块或空壳训练器。
