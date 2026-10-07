# 作者实现审查：Huginn 与 Recurrent Memory Transformer

日期：2026-10-07。角色：独立的 Web 源码审查工作单元。状态：**source_audited_not_executed**。

本审查读取了本项目的 README、SOURCE_AUDIT、MATHEMATICAL_DESIGN 与 workflow-checkpoint，并通过作者仓库取得下列固定版本的完整源码文件，再逐项检查相关前向、状态更新、损失、训练入口与生成路径。没有下载模型权重或数据，没有导入、安装或运行这些项目，没有执行测试、训练、推理或原生评测。

**结论：存在可追溯到真实作者实现的技术基础，但不能把两个现成 wrapper 直接相套后称为已完成模型。** Huginn 提供共享深度循环；RMT 提供跨文本段的固定大小记忆。二者可以形成一个需要明确适配的条件语言模型基线。它不自动实现本项目第 5 节的概率过滤模型，也没有新的原创性结论。兼容性分析不是候选选中、代码准入、G01 或实验 PASS。

最应先处理的五个事实是：Huginn HF 主前向实际忽略传入的 attention mask；训练与 HF/RMT 的 label shift 约定不同；Huginn 默认后端关闭了可回退的 SDPA 实现；RMT HF wrapper 的 k2 detach 没有作用到调用者；Huginn 的 embedding scale 与 RMT 的跨段 hidden-state scale 不能未经处理直接混用。证据如下。

## 1. 固定来源与实际阅读范围

所有 GitHub 链接固定到提交，而非浮动分支。取得完整文件不代表整个仓库、全部实验分支或所有依赖已经审完。

| 来源 | 固定版本、关键文件 | 本次实际检查 |
|---|---|---|
| Huginn 原论文 | [2502.05171v1](https://arxiv.org/html/2502.05171v1)，2025-02-07 | 第 3 节架构、随机深度与截断反传；第 4.1 节初始化、锁步采样与训练设置 |
| Huginn 作者训练模型 | [model_dynamic.py](https://github.com/seal-rg/recurrent-pretraining/blob/1ea7220ec7eb42d13e89db0663df254d0bcdc28e/recpre/model_dynamic.py)；提交 `1ea7220ec7eb42d13e89db0663df254d0bcdc28e` | RecurrentGPT 构造、forward、iterate_forward、core_block_forward、随机深度采样与初始化，约 962–1372 行；相关 attention/block 定义 |
| Huginn 作者 HF 模型 | [raven_modeling_minimal.py](https://github.com/seal-rg/recurrent-pretraining/blob/1ea7220ec7eb42d13e89db0663df254d0bcdc28e/recpre/raven_modeling_minimal.py)；同一提交 | attention、SandwichBlock、主 forward、循环与初始化、分步接口、动态 cache、标准生成分派及 generate_minimal；未把 speculative/diffusion/adaptive 的所有分支当作已验证路径 |
| Huginn 训练接线 | [train.py](https://github.com/seal-rg/recurrent-pretraining/blob/1ea7220ec7eb42d13e89db0663df254d0bcdc28e/train.py)、[data_loading_utils.py](https://github.com/seal-rg/recurrent-pretraining/blob/1ea7220ec7eb42d13e89db0663df254d0bcdc28e/recpre/data_loading_utils.py) | train_step、validate、dataloader 接线、label shift、get_attention_mask |
| Huginn 配置与后端 | [model_registry.py](https://github.com/seal-rg/recurrent-pretraining/blob/1ea7220ec7eb42d13e89db0663df254d0bcdc28e/recpre/model_registry.py)、[raven_config_minimal.py](https://github.com/seal-rg/recurrent-pretraining/blob/1ea7220ec7eb42d13e89db0663df254d0bcdc28e/recpre/raven_config_minimal.py)、[config_dynamic.py](https://github.com/seal-rg/recurrent-pretraining/blob/1ea7220ec7eb42d13e89db0663df254d0bcdc28e/recpre/config_dynamic.py)、[attention_backends/interface.py](https://github.com/seal-rg/recurrent-pretraining/blob/1ea7220ec7eb42d13e89db0663df254d0bcdc28e/recpre/attention_backends/interface.py)、[attention_backends/pytorch.py](https://github.com/seal-rg/recurrent-pretraining/blob/1ea7220ec7eb42d13e89db0663df254d0bcdc28e/recpre/attention_backends/pytorch.py)、[launch_configs/recurrent.yaml](https://github.com/seal-rg/recurrent-pretraining/blob/1ea7220ec7eb42d13e89db0663df254d0bcdc28e/launch_configs/recurrent.yaml) | 真实小模型与最终模型形状、embedding scale、后端选择、示例配置的适用边界 |
| RMT 原论文 | [2207.06881v1](https://arxiv.org/pdf/2207.06881v1)，2022-07-14 | 第 3.2 节 read/write memory、块内全连接 mask、跨段 BPTT；第 4 节任务与目标范围 |
| RMT 2022 作者实现 | [mem_transformer.py](https://github.com/booydar/LM-RMT/blob/f088ea99a830b6bb88cb23140c537057f0fa9477/pytorch/mem_transformer.py)、[train.py](https://github.com/booydar/LM-RMT/blob/f088ea99a830b6bb88cb23140c537057f0fa9477/pytorch/train.py)；提交 `f088ea99a830b6bb88cb23140c537057f0fa9477` | memory 参数、准确 mask、_forward、输出切片、训练/验证的跨段状态与 BPTT 分支；作者 README 确认这是 2022 LM/算法实验实现 |
| RMT 后续作者 HF wrapper | [language_modeling.py](https://github.com/booydar/recurrent-memory-transformer/blob/9d0ebe1778687995697fe68e886bc1dcf0e45e1c/modeling_rmt/language_modeling.py)；提交 `9d0ebe1778687995697fe68e886bc1dcf0e45e1c` | 文件全部 195 行：MemoryCell、RecurrentWrapper、segment、loss、manage_gradients、generate |
| RMT 后续作者训练入口 | [run_finetuning_lm_rmt.py](https://github.com/booydar/recurrent-memory-transformer/blob/9d0ebe1778687995697fe68e886bc1dcf0e45e1c/run_finetuning_lm_rmt.py)、[trainer.py](https://github.com/booydar/recurrent-memory-transformer/blob/9d0ebe1778687995697fe68e886bc1dcf0e45e1c/lm_experiments_tools/trainer.py)、[WikiText 脚本](https://github.com/booydar/recurrent-memory-transformer/blob/9d0ebe1778687995697fe68e886bc1dcf0e45e1c/scripts/wikitext/finetune_wikitext_short_rmt-sv.sh)、[requirements.txt](https://github.com/booydar/recurrent-memory-transformer/blob/9d0ebe1778687995697fe68e886bc1dcf0e45e1c/requirements.txt) | 数据分段、有效段长、padding/labels_mask、模型包装与优化；训练器 step 的 loss/backward/update；依赖未精确锁版 |

关键文件的 Git blob SHA，供之后下载与差异检查使用：

| 文件 | Blob SHA |
|---|---|
| Huginn raven_modeling_minimal.py | `0e83a0766644df9113a8923f43350c6a1b5a182c` |
| Huginn model_dynamic.py | `e8ef88e6148463ce0723ad0c9676073c5a9f447c` |
| Huginn train.py | `46e89314e079d7af0f3eb043fb9289b3e1ce7071` |
| Huginn attention_backends/pytorch.py | `57e961d4c2f548d45719c83f6545bc5da7670d8c` |
| RMT HF language_modeling.py | `ea0908d51b4b84b3d364e2f511ee7d7703aec4b6` |
| RMT HF run_finetuning_lm_rmt.py | `c63e6b0b582c17cc7a8828c294b66917df062ccc` |
| RMT 2022 mem_transformer.py | `c8f32ca5a9c7473b0d4af2f98a11ebb9ac5357cc` |

## 2. Huginn：实际循环与训练约定

### 2.1 可以从代码确认的算子

令输入文本长度为 L、隐藏维数为 d，γ 为 embedding scale。忽略可选噪声和非主配置的其它 injection 变体，最终 Huginn 形状的计算为

\[
e=P(\gamma E(x)),\qquad s_0\sim\operatorname{TruncNormal},\qquad
s_{k+1}=B_R\!\left(A[s_k;e]\right),
\]
\[
h=N_f\!\left(C(N_f(s_r))\right),\qquad \ell=W_{\mathrm{LM}}h.
\]

这里 A 是 `2d→d` 线性适配器，B_R 是同一个多层 core；P 与 C 分别只调用一次。`ln_f` 在 `iterate_forward` 返回时与 coda 后各使用一次，不能仅凭论文概述在每次循环边界额外加入同一个 final norm。每个 SandwichBlock 自身另有 attention 前后与 MLP 前后的 RMSNorm。RoPE 使用文本位置，主形状不把内部循环编号作为语义时间；模型文件中的 step 仍用于执行/cache 标识。

默认 `initialize_state` 为每个 forward 重新抽取与 e 同形的噪声。HF 文件支持显式 `input_states`，但这只是起始工作区接口。默认模型没有 RMT 式跨段记忆状态，也没有概率后验对象。

`state_init=like-init` 时先以 embedding 初始化标准差抽截断正态，再乘 γ。最终配置 γ=√d、初始化标准差 √(2/(5d))，所以状态的初始化尺度约为 √(2/5)，并受截断影响。不是直接给 d 维状态取标准正态，也不是持久记忆的每段重置规则。

### 2.2 两个反传轴不能混淆

深度循环先做 n 次 `torch.no_grad()`，再做 k 次保留梯度的 core，最后计算一次 coda 与 LM loss。主 sampler 的实际源码是：

\[
a=\max(\mathrm{mean\_recurrence}-\mathrm{mean\_backprop\_depth},0),\quad
b=\mathrm{mean\_backprop\_depth},
\]
\[
\lambda\sim\operatorname{LogNormal}(\log(a+b)-0.5\cdot0.5^2,\,0.5),
\quad r\sim\operatorname{Poisson}(\lambda)+1,
\quad n=\max(r-b,0),\quad k=\min(b,r).
\]

当默认 mean_recurrence=32、mean_backprop_depth=8 时，这个训练 sampler 的期望总步数为 33；eval 默认固定为 32。这是应记录的源码语义，不能把配置字段名当成精确的训练分布均值。训练版用 microbatch step 等构造随机数种子，锁步选项影响跨 rank 采样。缩小或截断这个分布是显式协议变更。

HF `num_steps` 传入一个标量时，源码把它解释为全部 no-grad、零个 grad steps。不能以为在 `model.train()` 下传 `num_steps=K` 就训练了 K 次共享 core。训练须使用训练 sampler 或明确的 `(n_no_grad,n_with_grad)` 对。训练版 `num_steps_pair` 也应传两元素对象。K=0 不是经过此代码验证的正常设置：训练实现返回的 `xk` 需要实际循环赋值。

跨文本段的 BPTT 是另一个独立轴。只保留最后 k 个深度循环不等于只反传 k 个文本段。若以后将 memory 作为 prelude 输入，它在每个保留梯度的循环通过 e 重新注入，仍可形成跨段梯度；如果把 memory 从已 detach 的输出中取出，这条路径会消失。

### 2.3 Mask 与 loss 的真实行为

- HF `forward` 约 676 行与 `embed_inputs` 约 921 行都把 `prepared_attn_mask` 设为 None，`compile_mask` 调用被注释。用户传入的 padding、文档或阶段 mask 在这些路径上不生效。
- 没有 cache 的 attention 使用下三角因果 SDPA。带 cache 的单 token query 可以访问全部已有 key；多 token query 使用 lower-right 因果偏置。这个原本的因果性不意味着 padding/样本分界自动正确。
- 训练 `get_attention_mask` 约 825–827 行直接返回 `(None,None)`。不能从 `doc_block_attn` 配置名宣称已有文档隔离。
- `data_loading_utils.shift_inputs_and_labels` 先做 `inputs[:-1]` 与 `labels[1:]`。HF 主模型 loss 与训练模型 loss 都直接比较同位置 logits 和传入 labels，没有再做 Hugging Face 常见的内部 shift。RMT 的外层 loss 则会做一次 shift，二者不能双重 shift。
- HF loss 明确 ignore -100；动态模型普通 PyTorch 分支使用 cross_entropy 默认 ignore 值，融合分支还使用 objective 配置。统一 ignore 值必须落实到 collator 和具体 head 分支，不能仅从 tokenizer.pad_id 推断。
- HF 返回 `latent_states` 时 clone 后 detach；`return_head=True` 的 `hidden_states` 则是附着计算图的最终 h 张量。要训练 RMT 式写 memory，不能误用 detach 后的 latent_states；也不能把这个张量当成标准 HF 的逐层 hidden-state tuple。

### 2.4 生成与 cache

常规 `generate` 走 HF GenerationMixin；指定 `continuous_compute` 才走作者 `generate_minimal`。后者若启用连续计算，会把上一个输出位置的 latent 作为下一个 token 的初始状态。它仍带自回归 KV cache，不是一个已经有固定大小跨会话 memory 的实现。

动态 cache 按“展开的 layer/循环步”与 token 位置保存 K/V，coda 使用负索引，避免与 core 混同。缓存空间通常随文本长度与展开深度增长。可选压缩/缺失 cache 查找策略不是免费的精确等价；多处硬编码 2 个 prelude 层、4 个 core 层，静态 cache 尺寸也用 `4+4r`，dtype 写死 bfloat16。缩小形状后照抄这些路径会留下错误索引或不合适精度。

对所需组合，先明确无 cache 的语义参照与固定 K，再单独资格审查 cache 优化。比较 cached/uncached 时须固定 dropout 与每个 token 的初始随机状态；不同随机初始化导致的不同输出不能全算作 cache 错误。

## 3. RMT：原论文版本和后续 HF 版本是两个具体实现

### 3.1 原论文与 2022 实现

每段使用 `[M, X, M]`。前缀 read memory 来自上一段，后缀 write memory 汇集当前段；输出的 write block 成为下一段 M。memory 在一整个 backbone 前向结束后写一次，不是每个 attention 层写一次。它是确定性的学习状态转移，不是带可计算密度的后验。

在 `same_length=False`、无 Transformer-XL cache、`mem_at_end=True` 的 2022 实现中，普通文本保留因果 mask，但 read/read 块与 write/write 块被解除三角限制。论文第 3.2 节明确说明了这点。若同时使用 Transformer-XL cache，memory block 是否能读 cache 还由 `read_mem_from_cache` 决定；普通 cache 与可训练 memory token 是不同对象。

`init_mem_tokens` 注册可训练 memory 参数，并把一次抽取的向量复制为多个初始 memory token；2022 代码这一初始化与后续 HF wrapper 的逐元素独立随机初始化不同。`forward` 返回 write memory 与非 memory 位置的 LM loss；训练入口显式携带状态。普通训练步先 detach 上一段 memory；`mem_backprop_depth>0` 分支重新计算历史段以构造反传链。该分支含 `mem_tokens.values = ...` 这种需要实测的状态恢复写法，训练路径还打印 `para_model.module...`，不能视为可靠的单卡开箱入口。源码已读不等于旧训练器可直接运行。

### 3.2 后续作者 HF wrapper 的完整状态路径

MemoryCell 中，初始参数形状为 `(m,d)`，初始化为独立正态乘输入 embedding 的实测 std；起始状态为按 batch repeat 的可训练参数。每段把同一个输入 memory_state 放在文本前后。forward 返回最后一层 suffix hidden states 作为新 memory，去掉前后 memory 的 logits 后交给外层。

RecurrentWrapper 的 `forward` 每次调用从 `memory_state=None` 开始，只在本次输入切出的多个段之间传递。它不是已实现的跨 API 调用持久会话存储。若把连续历史分成多次 wrapper 调用，原始接口会重置 memory；未来需要显式的 state-in/state-out/reset/episode-ID 合约。

该 wrapper 只给 backbone 扩展普通 padding mask，未实现论文的 memory 块内双向 mask。因此标准 GPT 因果 backbone 下，read/read 与 write/write 也都是三角结构。这个后续作者变体可以采用，但必须命名为所固定的 HF wrapper 行为，不能声称精确复现 2022 mask。

外层先拼接所有段的普通 token logits，再用 `logits[:-1]` 预测 `labels[1:]`；memory 位置没有词表监督。跨段的最后一个普通 token 预测下一段首 token 的目标仍在拼接损失中，没有因分段而自动丢弃。`labels_mask[:-1]` 在源码中索引预测位置；若任务 mask 以目标 token 为坐标定义，必须重写/转换其约定并核对边界，不能把两种坐标混用。

### 3.3 确认的源级缺陷与未资格审查的生成

1. **k2 截断未生效。** `manage_gradients` 的最后两行只在函数局部重新绑定 `memory_state=memory_state.detach()`，返回的是布尔值；调用者不接收新的状态。因此这条路径不会 detach 外层持有的张量。不能用 k2 声称显存只保留限定文本段。`max_n_segments` 与 `vary_n_segments` 也不是此 wrapper 内实际执行的段数上限/随机裁剪。
2. **最终生成位置需要核对。** `generate` 对之前的段做 MemoryCell.forward，再对最后一段调用 MemoryCell.generate。后者仍构造 `[M,X,M]` 并直接传给 backbone.generate；未去掉 suffix memory。训练的普通 token logits 与生成从 suffix 后开始的条件位置不同。此处是静态可见的训练/生成接线差异，尚未用固定模型确认其数值影响。
3. **生成不返回下一轮持久 memory。** wrapper 的 generate 返回生成结果，没有 state-out 接口，不能自动继续外部历史流。
4. **padding 的间接影响。** 即使 loss 忽略 pad，write memory 若看见 pad，后续段仍可能受污染。组合后的 mask 必须从输入到所有循环和 coda 真正生效。
5. **版本不是运行环境。** requirements 未锁版本，HF generate/cache API 与 accelerate 接口随版本变化。旧脚本还有本机数据路径和多进程假设；需要 Local 的原生 Conda 环境资格审查，不能照抄命令当已可运行。

## 4. 可以支持的组合合约：一个有作者依据的条件语言模型

本节是**兼容性规格**，用来说明“以真实代码为基础”究竟要改哪里；不是新候选的已选数学卡，也不是完整实验设计。继承的机制分别来自上面的 Huginn 和 RMT。组合、精度移植、状态接口与下列语义决策均须在后续代码映射中列为本项目改动。

**后续范围说明：** 本轮最终采用的 `FULL_MODEL_PROPOSAL.md` 进一步改成独立 cross-attention writer，并用 `[SEG, X]` 的前移 reader 行监督；它没有采用本节的 RMT suffix writer。本节保留为作者机制的兼容性对照，不是最终实现规格。最终方案的专门审查见第 8 节。

### 4.1 三种状态与写入时刻

| 状态 | 来源与寿命 | 更新时机 |
|---|---|---|
| 持久文本记忆 M | RMT 的固定 m×d 状态；在同一个有序 episode 中跨段传递 | 一段新的外部输入完成完整前向后提交一次 |
| 段内工作区 s_k | Huginn 的逐位置隐状态，形状 `(L+2m,d)` | 对固定的段输入和进入段时的 M 做 K 次共享 core 迭代 |
| 输出上下文/临时状态 | 已生成的 token 和可选的临时 cache | 每个输出 token 更新；不自动写回外部证据记忆 |

RMT 原始 LM 流并不区分“外部证据”与“模型自己输出的文字”。若要符合本项目现有数学语义，查询/回答期间必须读取一个 M 快照，把生成文字保留在临时工作区，丢弃对应的候选 write memory；真实的新用户证据另行进入外部更新。这个生命周期策略是本项目新增的接口约束，不应归功于原 RMT，也不能作为已实现行为陈述。

对于纯文本 LM 复现，应按作者的文本流定义更新 memory；对于外部证据只写一次的目标接口，则必须额外说明预训练流与查询阶段的监督关系。这两种模式不能在训练与评测时隐式切换。当前数据与监督尚未冻结，因而本审查没有认证后一种完整训练方案。

### 4.2 精确可选 mask

给一段的输入按 R=read memory、X=普通文本、W=write memory 排列。下面“允许”均还要与有效 key/padding mask 相交；行是 query，列是 key。没有跨 episode/cache 的隐式可见性。

| Query → Key | R | X | W |
|---|---|---|---|
| R，后续 HF 因果变体 | 仅同块当前位置及之前 | 禁止 | 禁止 |
| X | 全部 R | 仅同段当前位置及之前 | 禁止 |
| W，后续 HF 因果变体 | 全部 R | 全部本段有效 X | 仅同块当前位置及之前 |
| R，2022 块内双向变体 | 全部 R | 禁止 | 禁止 |
| W，2022 块内双向变体 | 全部 R | 全部本段有效 X | 全部 W |

必须选定一种，而不是把两个作者版本都叫作同一精确 mask。若以 2022 论文机制为参照，采用其块内双向 mask；若以最直接的 HF decoder wrapper 为参照，则采用全序列三角 mask。

两种都保持普通 token 对未来普通 token 的因果性：R 从未读本段 X；X 从未读 W；每个重复 core 都使用同一个禁止关系；逐位置 adapter 不能跨位置传未来信息。因此重复 K 次不会因“写 memory 已看完整段”反向泄漏到本段较早的普通 token。相反，把更新后的 W 重新送进同段 R，会破坏这个论证，不能作为无害的循环优化。

只有段完成时将最终 W 提交到下一段。内循环的 e 与进入段时的 memory 快照固定；改变 K 会改变最后写出的内容，但不增加“新证据已写入”的计数。

显式 SDPA bool mask 中 True 表示允许，2022 实现的 byte mask 中 1 表示遮挡，转换时必须翻转相应逻辑。[PyTorch 2.6 SDPA 文档](https://docs.pytorch.org/docs/2.6/generated/torch.nn.functional.scaled_dot_product_attention.html)还要求区分显式 attn_mask 与 is_causal 参数。不能只把新 mask 接到现有 helper，同时保留未经核对的 `is_causal=True`。有自定义 memory 块 mask 时，以完整显式 mask 表达因果性更清楚。

### 4.3 Memory 的尺度与位置

Huginn 在主 forward 中给全部 `input_embeds` 乘 γ=√d。RMT 直接把上一段最后一层 hidden state 当成下一段 embedding。两者直接组合时，会把通常已归一化、O(1) 的 memory 再乘 √d；这个 read/write 边界与普通 embedding 的尺度约定不同。

至少要明确选择一种一致的坐标约定：

- 在**缩放后的 embedding 空间**保存 M，prelude 输入为 `[M, γE(X), M]`，写出最终 head hidden states 的 W。进入预处理时不再整体乘 γ；初始 memory 参数也要放到相同尺度。
- 或在**原始 embedding 空间**保存 M_raw，仍给整个输入乘 γ，写回时保存 `H_W/γ`；初始 memory 参数可以沿用 HF RMT 的 embedding-std 初始化。

两种只有在初始化和写回边界都作一致转换时才是坐标等价。这里没有冻结其中一种，也没有宣称未经适配的作者 wrapper 已经做到。省略这个选择会使“同一个 memory state”的数值含义随接口改变。

位置编码同样须明确：单段位置包含 R/X/W，长度为 L+2m；局部 RoPE 位置在每段重建。不能在 memory 插入后仍使用只为 L 个普通 token 构造的 position_ids。跨段长期顺序由 memory 承担，不自动得到额外的全局时间戳语义。最大位置缓存应覆盖真实的 L+2m。

### 4.4 损失与生成的一致接口

可追溯的基础目标是普通 token 的下一 token 交叉熵；R/W 槽位不产生词表 target。跨段位置的 target、episode 首尾、BOS/EOS、padding 与任务监督区间要由同一套绝对普通-token 索引产生。只能 shift 一次。memory 写入获得的训练信号主要来自后续段；每个独立训练样本若只有一段且无其它 memory loss，最后的 write output 没有未来 LM loss 监督，不能据此宣称已经训练了长期记忆。

基础 RMT 也没有在丢失原始历史后重建证据账本的保证。这里的 M 是压缩表示，并不满足现有数学草稿中概率族、观测密度或 filtering ELBO 的定义。若选择本条件 LM 合约，必须明确它是概率过滤方案的经验架构参照；若坚持概率过滤模型，则还欠缺对应的 latent distribution、transition、observation 与推断目标实现映射。

生成需要自行核对 next-token 读取位置：取最后一个有效普通 token 的 logits，不能无条件用增广序列的最后位置，因为最后位置是 W。一种可审查的语义参照是：对未提交的当前段，每次从相同进入段 M 计算当前普通-token 前缀，读取其最后普通位置；当前段关闭时才接纳 W，下一段再开始。查询回答阶段则只更新临时状态、保持证据 M 不变。复用 KV cache 是后续优化，其等价性需要单独检查；本节没有生成执行代码或声称这种路径已经运行。

### 4.5 不能直接套 wrapper 的接口清单

| 冲突 | 源码事实 | 所需适配 |
|---|---|---|
| embedding 参数名 | RMT 用标准 `inputs_embeds`；Raven 用 `input_embeds`，且先读 input_ids.shape | 显式 embedding 入口与形状/位置处理，不能靠 kwargs 静默透传 |
| hidden-state 输出 | RMT 读取 `hidden_states[-1]` 的逐层 tuple；Raven 可返回的是单个 head 张量 | 明确 head/latent 类型与是否 detach |
| mask | Raven 主路径忽略传入 mask | 贯穿 prelude/core/coda 的真实 mask |
| 标签 | RMT 外层 shift；Huginn 主 loss 已假定传入 shifted labels | 选定一个 loss 所有者，保证单次 shift |
| 训练深度 | scalar num_steps 为全 no-grad | 正确的 n/k 合约与状态日志 |
| 记忆梯度 | RMT k2 helper 未实际返回 detach 后状态 | 调用者显式采用新状态；单独声明段 BPTT 与深度 BPTT |
| embedding scale | 归一化 hidden memory 进入全局 √d 缩放 | 固定一个 memory 坐标约定 |
| 长期状态 | RMT 外层每次调用重置；Raven cache 随上下文增长 | state-in/state-out、episode reset 与有界存储规则 |
| 生成位置 | RMT generate 包含 suffix；训练去掉 memory logits | 对齐普通-token 读出和提交时刻 |

这些改动构成新的组合/移植实现。准确称呼是“基于固定作者实现的组合基线/适配”，不是对 Huginn 或 RMT 已完成的论文结果复现，更不是“无先例的新 world model”。

## 5. RTX 2080 Ti 与 100M / 1B token 的实际边界

[NVIDIA 官方产品页](https://www.nvidia.com/content/nvidiaGDC/zz/en_ZZ/geforce/graphics-cards/rtx-2080-ti.html)列出标准 RTX 2080 Ti 的 Turing 架构和 11 GB 显存；[官方 compute capability 表](https://developer.nvidia.com/cuda/gpus)列为 7.5。这不等于用户当前可用显存或设备数量已实测。

### 5.1 后端不能沿用作者默认值

Huginn `attention_backends/pytorch.py` 在导入时启用 flash SDP，并关闭 math、memory-efficient 与 cuDNN SDP。名称是 `sdpa` 不代表保留了可用 fallback。其 interface 文件还导入多种 Triton/AMD/其它后端；仅把 provider 配成 sdpa 也不能保证消除这些依赖。

[FlashAttention 作者仓库当前说明](https://github.com/Dao-AILab/flash-attention#nvidia-cuda-support)将主 CUDA FlashAttention-2 路径列为 Ampere/Ada/Hopper；Turing 指向另一个只支持核心功能子集的仓库。该额外实现本次未资格审查，不能直接成为依赖承诺。bfloat16 也不是此设备上可以照搬的主 CUDA flash 路径。可审查的移植方向是 PyTorch 原生 SDPA 的合适可用后端、FP16 混合精度与 loss scaling，并保留 FP32 数值敏感计算；具体 PyTorch/CUDA 组合、mask 支持、梯度有限性和显存需 Local 实测。不会生成 Docker 要求。

### 5.2 有真实小形状，但没有现成的设备承诺

作者 registry 的 `magpie-150m` 是现成的小模型配置：d=1024、32 heads、FFN=3520、1/4/1 prelude/core/coda、add injection、post-norm、mean recurrence=20、poisson-fill、backprop depth=4。它和最终 Huginn 的 sandwich/concat/lognormal 配置并不相同。因此可以把它作为明确的作者小模型来源；不能仅缩尺寸后把所有设置都叫作原始 Huginn 3.5B 的精确复现。

最终 `nebel-raven-3.5b` registry 写出 3,509,051,040 参数。仅两个 FP32 Adam moment 就约 28.1 GB，尚未计参数、梯度和激活；标准 11 GB 单卡不能直接全参数复现该训练设置。量化推理能否装下也不等价于预训练可行性，不能偷换。

作者 `launch_configs/recurrent.yaml` 是 10B-token 的示例，含大 world batch、本机 tokenizer 路径、相同 train/val 数据路径及“另划验证集”的待办；当前 loader 也未支持示例所写的 pkds 路径。它是历史配置证据，不是用户 100M/1B 预算下的可运行计划。

### 5.3 两种 token 数与两种截断都要记账

用户的 100M/1B 继续解释为候选的训练 token 预算，不能改写成参数量。计数至少分开：真实非 padding 训练文本 token、参与监督的 target token、重复历史输入 token、memory 槽位计算量、实际 core 次数。重放历史、截断反传或 memory 槽位均不应悄悄扩大/虚报语料预算。

若普通段长 L、memory 数 m、总文本量 D，单段序列长为 N=L+2m；逐层位置计算量粗略随

\[
D\left(1+\frac{2m}{L}\right)(l_P+\mathbb E[r]l_R+l_C)
\]

变化，但 attention 还有 N² 项。保留 S 个文本段的梯度，同时每段反传 k 个深度循环，会同时增加激活驻留；共享权重并不消除它。采用 math attention 还可能显式保存与 heads×N² 成比例的中间量。不能仅凭 m×d 的 memory 参数大小估算训练显存。

相同模型、采样分布和计数口径下，1B token 的文本工作量约为 100M 的十倍。这不提供吞吐/完成日期，也不保证小预算已出现 Huginn 大规模论文的能力。模型、段长、反传窗口、batch、数据与完整比较仍需后续设计和 Local qualification。

## 6. 需要 Local 验收的具体软件性质

以下是上述源码风险直接导出的验收义务，全部 **pending**；不是自造科学 benchmark，也没有结果可用于论证方法有效。

| 性质 | 需要证据回答的问题 |
|---|---|
| 因果与 padding | 固定随机性后，改变未来普通 token 不改变较早 logits；改变被 mask 的 pad 不改变有效 write memory/后续 logits；memory 块 mask 与所选作者变体一致 |
| 一次 shift | 每个受监督的绝对普通-token 位置恰好对齐正确下一个 token，含跨段边界、BOS/EOS、答案首 token 与忽略区间 |
| 实际反传链 | 保留的深度步和文本段产生预期梯度；截断边界外不连接图；写 memory 的输出未被误 detach |
| 状态生命周期 | 新 episode 重置；继续同 episode 的分段调用与一次调用按合约等价；查询/生成不增加外部证据写计数 |
| 内循环语义 | 增加 K 不重新摄取同一段外部输入；同段 W 不回注入 R；一段只提交一次 memory |
| 生成对齐 | next-token logits 来自最后有效普通位置；阶段 memory 不提前提交；cached 版本在固定初始随机状态下与语义参照符合声明的等价范围 |
| 设备与数值 | 实际选择的 SDPA 后端支持所需显式 mask；FP16 loss scaling 正常；loss/grad 有限；峰值显存与耗时有原始记录 |
| 恢复与预算 | checkpoint 恢复 RNG、深度 sampler 进度、数据位置、episode memory 和 token 计数；不会重复计数或跳过待预测 target |

这些检查由 Local 在项目的执行 harness 下完成；Web 本次只做静态源级推理。它们也不能替代原生 benchmark、强基线、完整比较与统计判定。

## 7. 尚未闭合的科学与交付边界

| 项目 | 本次状态 |
|---|---|
| 作者代码真实性、固定版本与相关运算阅读 | 已完成本文所列范围 |
| 源级兼容性 | 有具体可审查的接口、mask、loss 和状态合约；仍含待决尺度/版本选择 |
| 完整 world-model 数学语义 | 未完成；确定性条件 LM 与过滤分布模型不可混同 |
| 独立数学审查、约 20 个候选与 top-15 选择 | 本次未执行，未授予任何 PASS |
| 原创性与最近邻穷尽调查 | 未完成；本文明确承认 RMT、Huginn 及已有组合族的贡献 |
| 代码和完整实验设计 | 本次仅交付审查文档，不是实现或可派发计划 |
| 模型/数据下载、环境安装、测试与实验 | 均未执行 |
| 硬件测量、运行时间与显存 | 未测量 |

工作流依据为项目既有 Research Autopilot 的 Web/source-audit 角色合约；另读取了当前 `skill-6ac68a8f6ff481919a700388dd326f62/references/workflow-harness.md`。复现/源码审查不要求伪造一个新的 20→15 批次；若将这里的组合发展成新科学候选，则原有数学、选择与代码生成边界仍适用。本文没有填写 gate 通过字段，也没有改变项目 ledger。

下一阶段可以直接使用本文的作者来源、冲突清单与待验收性质完善全模型定义和真实 derivation-to-code 映射；但“已经读到可用组件”不能替代完整推导、必要选择与完整实验设计。

## 8. 对最终采用的独立 writer 方案的追加审查

此节是在上述作者审查完成后，按主集成作者要求检查实际新文件 `FULL_MODEL_PROPOSAL.md`。读取时 SHA-256 为 `4555a1f44d8ff6675efb9d53c3c2ef989091c431ab3f21c9f3495e4b3ab08e09`。后续任何修改都需要按受影响性质复核。本节是有限范围的独立数学/依赖图审查，不是源码执行或项目全部科学 gate 的裁决。

### 8.1 与前文参照方案的区别

最终方案把 prelude 输入改成 `[SEG, X]`，采用学习的位置向量、确定 workspace 初值和固定 K=4；core 通过 cross-attention 读不可变旧 memory；writer 单独从完整真实 token 的 prelude 表示更新 memory，且不读 core/coda 输出。这与两个作者原实现都有实质差异。它是明确的已知组件工程构造，不能当成忠实 RMT/Huginn 复现；作者的相关实证效果也不能自动转移给它。

这一改变避开了 suffix 生成位置、Raven 返回 detach 后 latent、跨接口 √d memory 缩放等直接套 wrapper 的问题，前提是实现真正按新公式完成，且没有再混入旧接口。

### 8.2 因果与 label 对齐：推导未发现冲突

设当前段真实 token 为 x_1,…,x_ell，prelude 位置 0 是 SEG。因果 prelude 使 E_j 只依赖 x_1,…,x_j。训练 reader 取 E_0,…,E_(ell−1)，其中 row j 通过每个共享 core 的逐位置 adapter、因果 self-attention、只读上一段 memory 的 cross-attention 和逐位置 MLP，仍仅依赖旧 M 与 x_1,…,x_j。因果 coda 保持这一依赖集合。因此 **row j 预测 x_(j+1)** 是正确对齐。

软件接口已经把此偏移落实在“从 `[SEG,X]` 取前 ell 行”，所以 `forward_segment` 的 target 正好是原 tokens；loss 再做 Huginn collator 式 shift 或 HF CausalLM 式 shift 都会错误。这同时覆盖段首 x_1 和段末 x_ell，不需要把上一段最后 logits 跨接为下一段首 token 的分布。新段首分布来自新 memory 与 SEG，这是该新模型明确选择的因子化。

Writer 取 E_1,…,E_ell，可见当前全部已消费 token。只要 `next_memory` 不回注当前 reader，便不存在当前目标经 writer 回流到其自身预测的前向边。图中只有 M_t→下一段 logits。功能式返回新 tensor 而不原地修改 M_(t−1) 是必要条件。

固定参数、旧 M、K 与无 dropout 的情况下，完整 teacher forcing 的 row j 和单独计算该前缀的最后 row 具有同样的允许依赖集合和运算定义。不同矩阵形状允许通常的舍入差异，但没有结构性的未来依赖。这一结论仍待 Local 检查具体 mask、切片和实现。

### 8.3 Writer 梯度：窗口要求是实质条件

Writer 专属参数不影响同段 reader logits；其首条语言学习路径是“当前 writer→下一段 memory read→下一段 loss”。因此至少要有两个连续、同文档、未 detach 的段。文件已经正确排除了逐段 detach 训练独立 writer 的错误，并明确四段 TBPTT 窗口、窗内固定参数、窗口 loss 后统一反传与更新。

实现还必须保持这些细节：初始 memory 的 `tanh(Z0)` 在新文档的训练前向中附着到 Z0；EOS reset 不把另一文档的 memory 带入；窗口末先完成所有反传，再更新参数和 detach 给下一窗口；按有效 token 总数加权，不能平均各段 mean loss 后把短段/EOS 段放大。每窗最后 write 若没有窗内下一段 loss，确实没有 writer 监督，该缺口不可通过名称消除。

梯度**路径存在**不保证每次梯度非零：饱和 gate、被 reader 忽略的 memory 或特定参数值可以使数值梯度为零。Local 应检查路径及有代表性的非退化状态，不把一次零梯度直接等同于方法不可学习，也不把一次非零梯度当科学效果。

### 8.4 有界性与 K 不变量：结论的范围正确

若初始 M=tanh(Z0)，新 proposal 也经 tanh，gate 经 sigmoid，则逐坐标凸组合在精确实数运算中保持 M∈[−1,1]。这不保证 Jacobian 收缩、记忆正确或长期学习稳定。文件已作此区分。

Writer 只读 prelude 与旧 memory，且无随机算子时，固定参数、同一个观测序列及相同分段边界下，改变 reader K 不改变持久 memory 轨迹。若先用不同 K 训练得到不同参数，或不同 K 生成了不同 token，memory 不再必须相同。验收 K 不变量时必须固定参数与被消费 token，不能把条件扩大到所有生成轨迹。

### 8.5 需要澄清的两项语义，不是已观察到的实现失败

1. 最终文件第 5 节在线状态机在完整段边界会提交采样得到的 token。这对第 1 节定义的“文本历史预测状态”是合理的：状态可记录模型说过什么。但若产品接口把某个 M 称为“仅外部证据的记忆”，则回答生成应从快照分支并丢弃其 write；不能同时宣称同一个 M 只含外部观测。角色/来源标记与明确的模式说明必须与训练数据、评测输入一致。
2. 逐 token softmax 归一化给出每个有限 horizon 的合法分布；仅定义 EOS 停止规则本身不保证最终以概率 1 发出 EOS。文档概率若要覆盖所有有限终止序列，需要几乎必然终止的条件，或明确最大长度下的截断/停止事件。固定有限生成 horizon 可以避免这项未证明的假设。

本次追加审查认可的是给定合约下的局部因果推导、索引配对、梯度路径、有界性与固定输入的 K 不变量。它没有认可训练质量、硬件适配、原生评测成绩、原创性、候选池完成或所有科学要求已满足。最终源代码尚未由本工作单元读取或执行。
