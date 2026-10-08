# 完整模型方案：持久状态、固定证据循环与语言读出

日期：2026-10-07。工作角色：Web 数学/源码作者。状态：**完整的已知组件工程构造，待独立审查；任何后续实现均应标记 `generated_unexecuted`。** 本文没有运行项目代码、测试、训练、推理，也没有下载数据或权重。它不是 Q01 停止规则的改名，不宣称原创方法、科学 gate 通过或已经完成 20→15 筛选。

2026-10-08 续审：上述日期是初稿时间；父版本的独立源码/数学审查已记录于 [SOURCE_REVIEW](SOURCE_REVIEW.md) 和 [SCIENTIFIC_SCOPE_REVIEW](SCIENTIFIC_SCOPE_REVIEW.md)，不能将初稿的“待独立审查”误读为这些审查没有发生。软件和科学验证仍待 Local。本轮仅增加下述末位置读出的等价实现，依据与新文献影响见 [SIGMA_REVIEW](SIGMA_REVIEW.md)。

建议用这一明确的整体模型作为实现对象：跨文本段保留固定大小的隐状态；段内用共享参数多次处理固定输入和固定旧记忆；最后由独立语言头输出分布；一个单独的 writer 在完整新文本段到达后写入一次。它借鉴 Huginn 的 prelude/core/coda 和 RMT 的跨段记忆，**不是任一论文的忠实复现**。先前数学文件中的变分过滤模型是另一个概率参考；本方案不把任意隐藏向量冒充贝叶斯后验，也不需要虚构 ELBO。

## 1. 研究对象与精确语义

把每个文档或有角色标记的对话序列分成顺序文本段
\(X_t=(x_{t,1},\ldots,x_{t,\ell_t})\)，其中 \(1\le\ell_t\le L\)。除文档尾部外，段长固定为 \(L\)；一个真实 EOS token 是最后一个预测目标。一个 batch lane 同时只处理一个文档，EOS 后 reset。v0 不把两个文档装入同一段，也不在模型内部隐式推断文档边界。

| 符号/对象 | 张量形状 | 精确含义 |
|---|---|---|
| \(n,L,m,d,V\) | 标量 | batch 数、最大段长、记忆槽数、宽度、词表大小 |
| \(M_{t-1}\) | \(n\times m\times d\) | 已完成文本段的确定性压缩状态；不包含当前段的未消费 token |
| \(P_t\) | 每 lane 至多 \(L-1\) 个 token | 尚未提交的当前段前缀；属于可用上下文，不是新的持久槽 |
| \(E_t\) | \(n\times(\ell_t+1)\times d\) | `[SEG, X_t]` 的因果 prelude 表示 |
| \(H_t^{(k)}\) | \(n\times\ell_t\times d\) | 内部第 \(k\) 步工作区；不是新的外部观测 |
| \(O_t\) | \(n\times\ell_t\times V\) | 每行预测该段同一位置目标 token 的 logits |
| \(M_t\) | \(n\times m\times d\) | 完整消费 \(X_t\) 后的一次 writer 输出 |

`SEG` 是可学习的内部向量，不是语料 token，不进入 token 预算，也没有对应预测损失。它使每个段的第一个 token 都由旧记忆生成，避免漏掉段首目标。在线状态是二元组 \((M_{t-1},P_t)\)，不能只序列化 \(M\) 后丢掉部分段。

本方案中的“world state”只能先解释为**文本历史的潜在预测状态**：它要支持未来文本预测、跨段信息使用和更新；没有实体槽、物理坐标或校准概率的预设语义。若语料是带来源和角色的对话，状态表示“谁说了什么”的历史；模型生成一句话，并不使该句话成为独立的外部事实证据。角色/来源必须由真实数据序列提供，不能由模型自行制造。

## 2. 具体网络定义

以下给出一个确定的 v0，而不是让实现者从一组未定模块中猜选。\(N\) 表示逐位置 RMSNorm；所有不同下标的线性层和 block 参数独立，只有 core 在内部步之间共享。v0 dropout 为 0，workspace 初始化确定；这样固定参数、token 前缀和 \(K\) 时训练与生成的数值函数可直接比较。

### 2.1 Prelude：仅编码当前段的已见 token

设 \(W_{\rm emb}\in\mathbb R^{V\times d}\) 为词嵌入，\(s_{\rm seg}\in\mathbb R^d\) 为段起始向量，\(p_0,\ldots,p_L\) 为可学习段内位置向量：

\[
A_{t,0}=s_{\rm seg}+p_0,\qquad
A_{t,i}=W_{\rm emb}[x_{t,i}]+p_i\quad(1\le i\le\ell_t),
\]
\[
E_t=\operatorname{Prelude}(A_t).
\]

Prelude 使用严格的因果自注意力：位置 \(i\) 只能读 \(0{:}i\)。位置在每段重置；跨段顺序只能通过 \(M\) 表达。本版 prelude 不读旧记忆，便于区分当前证据编码与持久状态。

训练读入 \(\bar E_t=E_{t,0:\ell_t}\)，即位置 \(0,\ldots,\ell_t-1\)。Writer 读入 \(E_t^+=E_{t,1:\ell_t+1}\)，即完整真实 token 的表示。注意：最后一个真实 token 需要进入 writer，但不能进入预测它自己的 reader 行。

每个普通因果 block 可采用 Huginn 风格 sandwich 结构：

\[
B=N_2(A+\operatorname{CausalSA}(N_1(A))),\qquad
\operatorname{Block}(A)=N_4(B+\operatorname{MLP}(N_3(B))).
\]

本版 MLP 固定为门控 SiLU：\(\operatorname{MLP}(u)=W_o(\operatorname{SiLU}(W_a u)\odot W_b u)\)。若实现改用普通前馈层，应将差异记入配置和数学映射，不能把两者称为同一精确架构。

### 2.2 Core：固定输入和旧记忆上的共享循环

\[
H_t^{(0)}=\bar E_t,
\qquad
A_t^{(k)}=W_A[H_t^{(k-1)};\bar E_t],\quad W_A:\mathbb R^{2d}\to\mathbb R^d,
\]
\[
H_t^{(k)}=\operatorname{Core}_{\phi}(A_t^{(k)},M_{t-1}),
\quad k=1,\ldots,K.
\]

每个 core block 依次执行因果自注意力、读旧记忆的 cross-attention、MLP；各残差后用独立 RMSNorm。一个明确的 block 是

\[
U=N_2(A+\operatorname{CausalSA}(N_1(A))),
\]
\[
V=N_4(U+\operatorname{CA}(N_3(U),N_M(M_{t-1}+S))),
\]
\[
\operatorname{CoreBlock}(A,M_{t-1})
=N_6(V+\operatorname{MLP}(N_5(V))),
\]

其中 \(S\in\mathbb R^{m\times d}\) 是共享的可学习槽身份向量。Cross-attention 的 query 来自当前工作区，key/value 来自所有旧记忆槽。标准多头注意力每头为

\[
\operatorname{Attn}(Q,K,V)
=\operatorname{softmax}(QK^\top/\sqrt{d_h}+A_{\rm mask})V.
\]

只有文本自注意力具有因果 mask；旧记忆全部来自已完成文本段，可以全部读取。每一个 \(k\) 使用**同一个** \(M_{t-1}\) 和 \(\bar E_t\)。不得在 core 内调用 writer，不得将 \(H^{(k)}\) 追加成新 token，不得把不同内部步当作不同观测。

\(K\) 控制内部计算次数，语言输出长度另由实际采样 token 数控制。v0 固定 \(K=4\)，完整反向传播穿过所有四次 core；改变 \(K\) 是一个明确的推理设置，不附带“更深必然更好”的保证。Q01 的仿射停止证书不适用于这里的任意非线性 Transformer，不能默认启用。

### 2.3 Coda：只从最后工作区读语言

\[
D_t=\operatorname{Coda}_{\omega}(H_t^{(K)}),\qquad
O_t=N_f(D_t)W_{\rm emb}^{\top},
\]
\[
p_{\theta,K}(x_{t,i}\mid M_{t-1},x_{t,<i})
=\operatorname{softmax}(O_{t,i-1})[x_{t,i}].
\]

Coda 使用因果 block，且不直接读取旧 token 原文、\(E\) 或 \(M\) 的旁路；输入/输出词嵌入权重绑定。它仍能通过 \(H^{(K)}\) 访问这些信息。禁止 coda 在 token 维度做无 mask 池化或双向注意力。

“独立语言读出”指参数及调用阶段独立；不声称 coda 只有线性层，也不声称其计算免费。

在线 `predict_prefix` 只需要末行。设 R 为末位置选择，因最终 \(N_f\) 逐位置运算，\(R[N_f(D)W_{\rm emb}^{\top}]=N_f(RD)W_{\rm emb}^{\top}\)。因此可以在完整 coda 之后、最终 norm/projection 之前选择末行；训练仍保留全部监督行。不得把选择提前到混合位置的注意力之前。舍入与 Local 验收条件见 SIGMA_REVIEW §3。

### 2.4 Writer：一次消费完整段、一次返回新记忆

Writer 不读取 \(H^{(K)}\)，使用已消费的 \(E_t^+\) 和旧记忆：

\[
C_t=\operatorname{CA}_w(N_q(M_{t-1}+S),N_e(E_t^+)),
\]
\[
T_t=M_{t-1}+C_t,\qquad
U_t=T_t+\operatorname{MLP}_w(N_u(T_t)),
\]
\[
\widetilde M_t=\tanh(W_vN_v(U_t)),
\qquad
G_t=\sigma\!\left(W_g[N_g(M_{t-1});N_h(U_t)]+b_g\right),
\]
\[
\boxed{M_t=(1-G_t)\odot M_{t-1}+G_t\odot\widetilde M_t.}
\]

所有这些张量的输出形状都是 \(n\times m\times d\)。初值 \(M_0=\tanh(Z_0)\)，\(Z_0\) 为可学习、各槽独立初始化的参数；不能把所有槽初始化为相同向量且又没有槽身份，否则对称结构允许槽永远相同。

Writer 可读取整个**已经结束**的当前段，故此处 cross-attention 不需要段内因果 mask。它返回新张量，绝不原地修改调用方旧 \(M\)。同一已消费段只允许业务状态机提交一次。

两个直接结论：

1. 因 \(G\in[0,1]\)、\(\widetilde M\in[-1,1]\)，逐坐标凸组合给出 \(M_t\in[-1,1]^{n\times m\times d}\)。这是状态幅度界，不是压缩映射证明；\(G\) 和 \(\widetilde M\) 都依赖旧 \(M\)，其 Jacobian 仍可能放大扰动。
2. 固定参数和观测段，writer 不含 \(K\)，因此 \(\partial M_t/\partial K\) 的离散对应是：选择任何 reader 深度，都得到同一个 \(M_t\)。内部深度改变不会重新计入证据。这个不变量来自架构分离；它不证明读出校准，也不阻止 logits 随 \(K\) 变得错误地过度自信。

代价也明确：writer 不能把深层 core 得到的新解释直接写回。因此模型可能受到较浅 writer 的压缩瓶颈限制；这一设计选择需要被比较，而不是包装成必然优势。

## 3. 这是一个正常化的生成模型，但不是已识别的物理世界模型

给定固定 \(K\)，每一行 softmax 都归一化，顺序生成一个段并更新状态：

\[
p_{\theta,K}(X_t\mid M_{t-1})
=\prod_{i=1}^{\ell_t}
p_{\theta,K}(x_{t,i}\mid M_{t-1},x_{t,<i}),
\qquad M_t=U_\theta(M_{t-1},X_t).
\]

在固定有限长度或有明确 EOS 终止约定下，其联合过程可写成

\[
p_{\theta,K}(X_{1:T},M_{1:T})
=\prod_{t=1}^T p_{\theta,K}(X_t\mid M_{t-1})
\,\delta_{U_\theta(M_{t-1},X_t)}(dM_t).
\]

状态更新发生在该段采样/观察之后，因而是合法的观测驱动状态空间生成过程。直接最大似然可训练它，没有隐状态积分，也没有理由附加一个来源不明的 KL 项。\(M\) 没有被证明等于真实 \(Z\) 的后验；这一构造不同于自主隐动力学 \(p(z_t\mid z_{t-1},a_t)\) 加观测模型。没有动作及相应数据时，不能宣称学到了反事实干预或真实世界因果机制。

同样，状态的可逆坐标变换可以由 writer 和 reader 的相反变换补偿而不改变文本分布。因此语言似然不能唯一识别“第几个槽代表什么”。

## 4. 因果性与训练/生成等价性的推导

对 prelude 的层数归纳：\(E_{t,j}\) 只依赖 \(x_{t,1:j}\)。在 reader 第 \(k\) 步归纳，若所有 \(H_{t,j}^{(k-1)}\) 只依赖 \(M_{t-1},x_{t,1:j}\)，则点式 adapter、因果自注意力、只读旧记忆的 cross-attention、点式 MLP 保持此性质。Coda 同样保持它。因此位置 \(i-1\) 的 logits 不依赖 \(x_{t,i}\) 或任何未来 token。

虽然训练时 prelude 同时计算了最后 token 的表示，reader 只取前 \(\ell_t\) 行；因果 mask 保证这些行不含后续信息。Writer 的新状态只用于下一段。因此不存在通过 writer 回流到当前段 logits 的前向边。

在固定参数、相同 \(K\)、相同初始记忆、无 dropout/随机噪声且一致精度运算的条件下，对每个前缀长度 \(u<\ell_t\)，并行 teacher forcing 的第 \(u\) 行和以该前缀单独重计算所得的最后一行相同，至多有不同矩阵形状产生的浮点舍入差异。真实 token 与采样 token 仅决定随后条件化的前缀取值；不改变模型函数。这种计算等价不消除 teacher forcing 的分布暴露问题。

不能用“训练时返回旧记忆预测的段末 logits，推理时先更新新记忆再用它预测同一 token”之类混合约定。本版段首一律从 `[SEG]` 和当段开始时的已提交记忆产生，段内一律从当前 prefix 及同一已提交记忆产生。

## 5. 精确的软件接口与状态机

推荐接口与上述公式一一对应：

| 接口 | 输入/输出 | 约束 |
|---|---|---|
| `initial_memory(batch_size)` | 返回 `[n,m,d]` | 训练时保留到 \(Z_0\) 的梯度；无需原地写；EOS 后用它 reset |
| `forward_segment(tokens, memory)` | `[n,ell]`, `[n,m,d]` → `logits[n,ell,V]`, `next_memory[n,m,d]` | `tokens` 本身就是 labels，**不得再次 shift**；reader 用 `E[:,:ell]`，writer 用 `E[:,1:ell+1]` |
| `predict_prefix(prefix, memory)` | `[n,u]`, `[n,m,d]` → `[n,V]` | \(0\le u<L\)；重算 `[SEG,prefix]` 全部 reader/coda 隐状态，仅对最后位置作最终 norm/词表投影；不写记忆 |
| `commit_segment(segment, memory)` | 完整已消费 `[n,L]` → `[n,m,d]` | 仅运行 prelude+writer；与 `forward_segment` 的 writer 使用同一函数和参数；不依赖 reader 深度 |

v0 单设备实现允许无 padding 的等长 batch，调用者负责 EOS 与文档管理。若以后允许 padding，必须同时添加 reader 有效-key mask、writer 有效-token mask 和 loss mask；只掩盖 loss 不能阻止信息从 padding 或另一文档泄漏。长度 0 的 `forward_segment`/`commit_segment` 应显式拒绝；长度 0 的 `predict_prefix` 必须支持。

在线顺序如下：

1. 从 \((M,P)\) 计算 `predict_prefix(P,M)`。Prompt 消费也使用同样 token 接口，只是 token 来自输入而非采样。
2. 采样或接受一个 token，追加到 \(P\)。`predict_prefix` 任意重算都不增加提交计数。
3. 若该 token 是 EOS，先保留其预测/损失，再清空 \(P\)、reset \(M=M_0\)。即使 EOS 恰在第 \(L\) 个位置，也无需先写一个马上丢弃的状态。
4. 否则若 \(|P|=L\)，执行一次 `M=commit_segment(P,M)`，随后清空 \(P\)。下一 token 由空 prefix 和新 \(M\) 预测。
5. 若只因输出 token 上限、用户暂停或输入暂时结束而停在 \(|P|<L\)，保留 \((M,P)\)；**不提前提交部分段**。恢复时从原状态继续。

离线 `forward_segment` 可以为含 EOS 的尾部短段返回一个数学上的 `next_memory`，但调用者必须丢弃它并 reset；它不会影响任何有效 loss。没有 EOS 的数据切片尾部不是文档结束：保留部分段并与下一切片拼接。若人为提交任意短段，就改变了分段及模型分布，不能称为同一生成流程。

生成 v0 使用部分段完整重算，避免 KV cache 的深度索引、缓存压缩或缓存重用带来的额外近似。将来引入 cache 时需要逐深度等价验证；一个普通 Transformer 的单套缓存不自动等价于共享深度循环。

多选题评分时，应从同一 prompt 状态复制 \((M,P)\) 分支，逐个消费候选 token；候选之间不能串联写同一记忆。读取 prompt 的完整段如无需 token 分数，可只调用 prelude+writer，得到的记忆与完整 reader 路径相同；这是分离 writer 带来的精确优化。

## 6. 训练目标、writer 梯度与 TBPTT 的真实限制

唯一的 v0 训练目标是所有有效真实 token 的负对数似然：

\[
\mathcal L(\theta)
=-\frac{1}{N_{\rm tok}}
\sum_{t,i}\log p_{\theta,K}(x_{t,i}\mid M_{t-1},x_{t,<i}),
\quad M_t=U_\theta(M_{t-1},X_t).
\]

这包括文档首 token、每段首 token、所有段末 token 和真实 EOS；不包括 `SEG`、padding 或额外“思考 token”。不默认加入熵下降、相邻隐状态一致性、自生成解释监督或未定义的世界状态回归目标。

**不能在每一段后 detach 然后期待独立 writer 学习。** 设 writer 专属参数为 \(\psi\)，当前段损失为 \(\ell_t(M_{t-1})\)。当前 reader 不读 \(M_t\)，所以如果每次入段的 \(M_{t-1}\) 都已 detach，则

\[
\frac{d\ell_t}{d\psi}=0
\]

对于这些 writer 专属参数严格成立。Prelude 的共享参数可能收到 reader 梯度，不代表 writer 的 gate、cross-attention 和 proposal 参数被训练。

推荐连续 \(U=4\) 段组成一个 TBPTT 窗口，最低 \(U\ge2\)。窗内参数固定，所有段的损失求和后反向传播，窗内所有 \(M\) 转移保留计算图；optimizer 更新后才把窗口最后状态 detach 给下一窗口。短文档在 EOS reset，不让梯度跨文档传播。需要足够多真实多段文档，否则 writer 几乎没有未来 token 学习信号。不同窗口的最终一次 write 没有窗内未来 loss，不能假装每次转移都受到完整长期监督。

精确地，令 \(A_s=\partial M_s/\partial M_{s-1}\)，\(B_s\) 为该 writer 及 prelude 在固定输入和固定旧状态下对参数的导数。完整文档梯度包含

\[
\frac{dM_{t-1}}{d\theta}
=\sum_{j<t}A_{t-1}\cdots A_{j+1}B_j
\]

以及可学习初值的导数项。TBPTT 删除窗口起点以前的这些项，故是有偏梯度近似；它保留数值记忆，不保留任意久远的学习信用。如果有 \(\|A_s\|\le\rho<1\)、\(\|B_s\|\le B_*\)、\(\|\partial_M\ell_t\|\le G_*\)，遗漏距当前至少 \(q\) 次转移的尾项才有条件性上界

\[
\|\Delta\nabla\ell_t\|
\le G_*B_*\frac{\rho^q}{1-\rho}.
\]

本模型没有建立这些全域界；writer 的数值幅度有界不推出它们。强收缩又可能抹掉长期记忆。因此不能由一个短 TBPTT 窗口承诺任意长依赖学习。

还有独立的参数陈旧问题：optimizer 更新前产生的 detached \(M\) 被下一版参数继续使用，它通常不等于用新参数重放完整历史得到的状态。v0 把这记作 stateful TBPTT 的训练近似；评测固定参数并从文档头重建状态。历史 burn-in 重计算可减少局部不匹配，但不能被描述为完整历史精确重算。

Core 深度方向与文档时间方向是两种不同截断。v0 不截断 \(K\) 的梯度；activation checkpoint 可以重算同一函数节省激活，不能 detach 来冒充 checkpoint。若开启随机算子，重算必须保持所需 RNG 状态。

## 7. 内部深度训练与推理必须说明的区别

固定 \(K=4\) 给出最容易审查的单个条件分布。若随后用 \(K=1,2,8\) 推理，函数仍有定义，记忆也不变，但这是深度分布改变，并不保证受过相应训练。

如后续明确采用随机深度 \(K\sim q\)，真实目标是

\[
\mathbb E_{K\sim q}\big[-\log p_{\theta,K}(X)\big],
\]

不是 \(-\log\mathbb E_K[p_{\theta,K}(X)]\)。由 Jensen，不应把二者混写。\(q\) 的支持、概率、采样单位和每个深度的总计算都必须冻结；只把“随机深度”写进配置而不改变目标说明是不充分的。可先采用明确的小有限集合，但本文不将超参数设置凑成新研究候选。

## 8. 为什么这一架构回答原来的完整问题

模型同时定义了：

- **状态存在与延续：** \(M_t\) 跨段保留，固定大小，存在可训练的转移 \(U\)。
- **读取与修正计算：** 同一旧状态和当前前缀可在 \(H^{(k)}\) 中反复重组，内部步不新增文字或外部观测。
- **表达解耦：** 语言分布只在最后通过 coda 读取；增加 \(K\) 不增加输出 token 数。
- **统一学习信号：** 所有模块由未来文本 NLL 经明确计算图训练；writer 经后续段的 loss 获得信用。

但这不证明它比普通模型更有价值。容量有限时，旧历史 \(H\) 被压缩成 \(M\)，现有笔记中的分解仍适用：

\[
\mathcal R(q)-H(Y\mid H,Q)
=I(Y;H\mid M,Q)
+\mathbb E\operatorname{KL}(p(Y\mid M,Q)\Vert q(Y\mid M,Q)).
\]

固定所有可用 \((M,Q)\) 后增加内部计算不能恢复第一项丢掉的区别。核心科学假说只是：在合适数据和预算下，学习到的压缩足够保留任务信息，而共享内部计算改善第二项。两者都需要被原生任务证据推翻或支持。

## 9. 已知来源、实际读取与本构造的区别

本轮重新读取了以下作者来源；仅作方法/代码阅读，不是运行验证：

| 来源 | 版本与读取范围 | 可复用事实与边界 |
|---|---|---|
| [Huginn 论文](https://arxiv.org/html/2502.05171v1) | arXiv:2502.05171v1，第 3 节架构、目标与深度截断 | prelude、共享循环 core、输入重注入和 coda 已有；本方案确定初态、加入持久槽及独立 writer，因此不是复现 |
| [Huginn 作者源码](https://github.com/seal-rg/recurrent-pretraining/blob/1ea7220ec7eb42d13e89db0663df254d0bcdc28e/recpre/raven_modeling_minimal.py) | commit `1ea7220ec7eb42d13e89db0663df254d0bcdc28e`；本轮读 attention、SandwichBlock、forward、iterate、core、初始化区间 | 能确认拼接 adapter、共享 core 和 shifted labels 约定。该文件 forward 将 `prepared_attn_mask` 设为 `None`；不能照搬为本项目 padding 正确性的证据 |
| [RMT 论文](https://arxiv.org/pdf/2207.06881) | arXiv:2207.06881v2，第 3 节与记忆 BPTT 说明 | 跨段记忆和通过记忆传播梯度已有明确先例；本文单独 writer 不等于其首尾 memory-token 实现 |
| [RMT 模型源码](https://github.com/booydar/LM-RMT/blob/e2895080868afc390386220f2b68a56c4a218126/pytorch/mem_transformer.py) | commit `e2895080868afc390386220f2b68a56c4a218126`；读初始化、`_forward` 的 memory 拼接/mask、输出切片 | 明确区分 token 预测隐藏态与段尾 write-memory；不复用其旧软件依赖或声称本版等价 |
| [RMT 训练源码](https://github.com/booydar/LM-RMT/blob/e2895080868afc390386220f2b68a56c4a218126/pytorch/train.py) | 同一 commit；读 `mem_backprop_depth`、训练 detach/recompute 区间 | 作者有跨段信用处理路径；本版使用显式多段窗口目标，不盲复制旧训练脚本 |

现有 [SOURCE_AUDIT.md](SOURCE_AUDIT.md) 中 AVF、BDH-CQ、Coconut、STARS 等仍约束新意判断。以上组件和这里的索引、因果性、TBPTT 分析都不能单独构成新颖性结论。本文的工作成果是把完整工程对象和可检验条件固定下来，供代码与实验设计准确实现。

## 10. RTX 2080 Ti 与 100M/1B token 的工程起点

以下是待 Local 测量的配置起点，**不是数学最优值、显存适配承诺或已测速度**：

| 项 | 起点 | 选择理由 |
|---|---:|---|
| 最大段长 \(L\) | 256 | 让段内二次注意力与在线部分段重算保持有限；更短段会加重记忆压缩负担 |
| 槽数 \(m\) | 16 | 给持久状态一个清楚的小容量；不暗示 16 个真实世界实体 |
| 宽度 \(d\) | 256，384 作为另一个资源档 | 控制参数/激活；需由 Local 内存与吞吐决定，不能任意扩到 1B 参数 |
| Prelude/core/coda 层数 | 2/2/1 | 将词编码、共享内部计算、读出明确分离 |
| Writer | 1 次 cross-attention + gated MLP 更新 | 保留独立可训练更新与一次提交语义 |
| 内部深度 \(K\) | 4 | 完整反传可审查；不是固定点求解器保证 |
| TBPTT 窗口 \(U\) | 4，最低 2 | 给 writer 真实的未来段 loss 路径；更长窗口增加激活与长程信用 |
| 精度/attention 后端 | 由 Local 确认 | 不把作者大集群的 BF16 或特殊 fused kernel 当作该 GPU 可用证据 |

共享 core 参数量与 \(K\) 无关，但计算和反向激活随 \(K\) 增加。设词表大小 \(V\)、MLP 宽度 \(f\)，参数主项约为 \(Vd\) 加各真实 block 的 \(d^2,df\) 投影；应以最终实现计数，不能用“有效深度”重复算参数。词表投影成本 \(O(n\ell dV)\) 也不能从预算中删去。

完整段训练的自注意力主项约为

\[
O\!\left(n(\ell_P+K\ell_R+\ell_C)
(Ld^2+L^2d+Ldf)\right),
\]

另加 core 的 \(Lm\) cross-attention、writer、词表投影及反向。\(U\) 段间顺序计算；显存受保存图、checkpoint、batch、优化器和词表 logits 共同影响。

无 KV cache 的生成不是廉价部署方案：一个段内对所有前缀重算，自注意力总项含 \(\sum_{u=1}^L u^2=O(L^3)\)，线性投影含 \(O(L^2)\)。它的作用是先把训练/生成语义保持一致，并为后续缓存提供精确参照；吞吐必须实测。

100M 和 1B 暂解释为**训练中有效目标 token 的累计出现次数**。`SEG`、padding、reader 内部步、writer 对同一 token 的额外计算不增加这个数。重复 epoch 会增加暴露次数但不增加独立语料规模，两者要分别报告。配置及有效 batch 不变时，1B 约需 100M 的十倍更新/计算量；不能由此推断学习收益或训练小时数。数据选择、语料访问及评测切分由另一份完整实验设计明确，不能由 token 数倒推世界模型能力。

## 11. 可推翻的主张与明确失败边界

以下是数学/实现核对与科学假说的区别，不是已经完成的测试，也不是替代原生 benchmark 的自制任务。

| 主张/假说 | 推翻或限制它的证据 | 后果 |
|---|---|---|
| 每个有效 token 仅监督一次，且没有未来泄漏 | 实现的索引/依赖图允许 target 或未来状态影响同一位置 logits，或漏掉段首/EOS | 实现错误；任何训练/评测结论无效 |
| 并行训练和部分段生成是同一条件函数 | 相同参数、前缀、记忆、\(K\) 下存在超出合理数值误差的 logits 差异 | 先修 mask、位置、shift 或边界；不能解释成研究收益 |
| Reader 深度不改变固定观测的持久记忆 | 只改 \(K\) 或只重算 query 就改变提交次数/\(M_t\) | 架构分离没有实现 |
| Writer 可从未来语言 loss 学习 | 窗内有后续有效段却始终没有 writer 计算图/梯度路径 | 检查 detach、loss 聚合和记忆旁路；零性能提升不是首要解释 |
| 持久记忆保留跨段有用信息 | 在合格原生长依赖任务上，记忆 reset/屏蔽与完整模型无差别，或强可执行替代方案占优 | 不能声称记忆有必要；检查训练覆盖与容量，再决定是否放弃 |
| 增加内部计算有净价值 | 在计入所有成本、同等信息的比较中，固定深度或非共享网络相同/更优；\(K\) 扩展下降 | 参数共享或循环深度未获得所声称收益 |
| 输出对旧事实的更新正确 | 原生知识更新任务上仍旧事实占优，或模型把自己输出当权威来源 | 当前预测状态不够支持这一世界状态主张 |
| 状态幅度界意味着稳定世界推理 | 即使 \(M\) 有界，reader 仍振荡、塌缩或错误自信 | 幅度界仅是幅度界；不得升级为收敛或正确性证书 |

其他具体风险包括槽塌缩、有限 \(m d\) 容量干扰、浅 writer 丢掉日后所需信息、只有短文档导致 writer 无监督、短 TBPTT 无法学习远距离信用、错误把跨文档状态传给下一文档、强局部 coda/reader 忽略记忆、训练语料与对话来源标记不匹配，以及从小预算模型的语言能力不足错误推断机制无效。每种解释都必须被实际数据和合格对照区分。

## 12. 本文完成的工作与剩余条件

已完成的是一个张量、索引、概率因子化、writer 更新、NLL、生成状态机和梯度路径均闭合的完整模型构造；对因果性、训练/生成函数一致性、记忆幅度与 writer 梯度给出了直接推导。它足以让作者按同一数学对象写源代码，而不会把 Q01 当作整个模型。

尚未完成：独立数学/实现审查，新的候选池与科学筛选，完整原创性裁决，符合母问题的训练数据/原生评测资格、合格比较，以及 Local 的代码验收、硬件测量和实验。本文不修改这些真实状态。已知组件工程交付与新研究方法准入须分开标记；任何决定沿工程构造先交付的上层记录也不得伪造研究筛选或通过记录。

数学自审采用的具体路径是概率因子化与因果归纳（B01/B04）、梯度场与 stop-gradient 审计（H05）、压缩误差与截断误差分解（C04）、状态有界和收缩区别（G03/H06）。按当前项目所记录的 Research Autopilot 包 `e0/remote-skills/skill-6ac68a8f6ff481919a700388dd326f62` 读取了入口、workflow-harness、research-policy 的 Start/resume 与 Research loop、math-analysis、math-operation-graph 相关族、math-derivation-paths 相关路径与 math-handoff。本文只作数学和源码作者记录，不把 skill 阅读本身作为 gate 证据。
