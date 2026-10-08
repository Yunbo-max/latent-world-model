# Delta + diffusion：长程拟合研究主线

这是方向收敛与数学边界记录，不是已验证的新模型、最终原创性结论或执行计划。

## 用户确定的范围

用户先要求聚焦 Delta，随后明确：“我们的核心就是用 diffusion 去帮助 delta 实现长距离的拟合”，并补充：“我们可以提出自己的方法在这个框架下”。据此，研究围绕一条主线展开：

**以 Delta 递推状态为骨架，研究 diffusion 如何帮助学习更适合长程预测的写入与保留规则。**

此前六条独立架构路线暂停作为并行主线；保留原有推导与负面证据。KDA、RWKV-7 是需要理解和对照的相关方法，不是需要同时拼进一个模型的两个模块。用户没有指定 diffusion 只能用于训练，也没有确认某个具体新更新式。

## 用直白的话说

Delta 每次接收新信息，会先读出当前记忆对它的预测，再把预测误差写回状态。我们要研究的是：**这次修正怎样兼顾当前信息和以后仍要用的信息。**

优先调查 diffusion 的长跨度去噪信号能否指导早期的写入方向、写入强度和遗忘，而不只让输出端更会使用已经存好的状态。举例只是解释：早处出现的身份或规则，经过大量后续写入后，仍应支持远处依赖它的预测。不能把这样的解释性例子当成实验或自制 benchmark。

这不是说普通语言模型训练没有远期监督。端到端 next-token loss 已能回传到早期写入。需要证明的是 diffusion 的多噪声尺度或条件分布学习究竟增加了什么，而不是把“梯度来自未来位置”本身称为创新。

## 已有 Delta 骨架与相关方法

采用 \(S_t\in\mathbb R^{d_k\times d_v}\)：

\[
\bar S_t=D_tS_{t-1},\qquad
e_t=v_t-\bar S_t^\top k_t,\qquad
S_t=\bar S_t+\beta_tk_te_t^\top,\qquad
o_t=S_t^\top q_t.
\]

等价地：

\[
S_t=(I-\beta_tk_tk_t^\top)D_tS_{t-1}
+\beta_tk_tv_t^\top.
\]

顺序是先衰减、再纠错；一般不能交换 \(D_t\) 与秩一修正因子。

| 已有方法 | 与当前问题相关的机制 |
|---|---|
| DeltaNet | 当前 key 的重建误差驱动秩一写入，以上式中 \(D_t=I\)。 |
| Gated DeltaNet | 增加标量遗忘，\(D_t=\alpha_tI\)。 |
| KDA | 将遗忘细化为通道级对角门，\(D_t=\operatorname{Diag}(\alpha_t)\)。 |
| RWKV-7 | 广义 Delta 更新，包括向量门和更灵活的替换；不能直接当成与 KDA 相同的更新式，也不能把所有 RWKV 版本统称为 Delta。 |
| 本项目收敛后的研究目标 | 推导 diffusion 对长程预测有实质作用的写入/保留机制；具体构造、额外成本和原创差异尚待确定。 |

KDA 原文 §3 的状态递推已由 Web 阅读核对。RWKV-7 本轮核对论文摘要中的 generalized delta rule 定位，不据此声称完成其所有推导审查。

## 数学上真正需要跨过的距离

### 局部纠错不等于所有查询都改善

固定当前特征，在衰减后状态 \(\bar S_t\) 上加入一次 Delta 写入，对任意查询 \(q\) 的影响为：

\[
\Delta o(q)=\beta_t(q^\top k_t)e_t.
\]

当前 key 的残差变为：

\[
v_t-S_t^\top k_t=(1-\beta_t\|k_t\|^2)e_t.
\]

对于非零 \(k_t,e_t\)，在 \(0<\beta_t\|k_t\|^2<2\) 时，当前 key 的平方重建误差严格减小。它不保证其他查询改善，也不保证 token CE 减小。查询与写入 key 的重叠可以带来有益修正，也可以造成干扰，取决于目标误差方向。

此结论是已知 Delta 公式的代数后果，用于定位问题，不是新的贡献。

### 一次写入如何抵达远期读出

考察两个分支在时刻 \(t\) 仅相差一次写入
\(\delta S_t=\beta_tk_te_t^\top\)，之后输入相同，且未来所有 key、value、gate 和查询冻结。令

\[
A_j=(I-\beta_jk_jk_j^\top)D_j,\qquad
P_{t,h}=A_{t+h}A_{t+h-1}\cdots A_{t+1}.
\]

相减后，后续相同的加性写入抵消：

\[
\delta S_j=A_j\delta S_{j-1}
\quad\Longrightarrow\quad
\delta S_{t+h}=P_{t,h}\delta S_t.
\]

因此：

\[
\delta o_{t+h}
=\beta_t\left(q_{t+h}^\top P_{t,h}k_t\right)e_t.
\]

这里的有效远期查询是 \(P_{t,h}^\top q_{t+h}\)。当前纠错的方向是 \(k_t\)，远期预测能否读到这次修正取决于它经过后续转换后是否仍与远期查询相关。这解释了为什么只看当前重建误差不足以评估长程作用。

这是条件精确恒等式，而不是完整深层网络的通用公式。未来特征若随被改变的状态变化、生成 token 改变或加入非线性转换，则需要完整 Jacobian 分析；不能继续把同一 \(P_{t,h}\) 当成精确传播器。输出变化也不是损失改善。

若冻结特征下，远期损失对读出的梯度为 \(g_{t+h}\)，一次小写入的一阶损失变化为：

\[
\delta\ell_{t+h}
\approx \beta_t
(q_{t+h}^\top P_{t,h}k_t)
(e_t^\top g_{t+h}).
\]

两项的方向共同决定修正是否有益；单纯提高保留强度可能保留错误关联。

这一推导经 /root/arch_solver_memory 独立代数审查，保留了冻结特征、相同未来输入与乘积顺序的条件。

## diffusion 的位置与信息边界

设历史为 \(H\)，压缩状态 \(S=C_\phi(H)\)，问题或预测条件为 \(Q\)，目标为 \(Y\)。如果读出

\[
Z=D_\theta(S,Q,\xi)
\]

中的随机噪声没有额外历史或目标信息，即 \(Y\rightarrow S\rightarrow Z\) 在给定 \(Q\) 后构成 Markov 链，则数据处理不等式给出：

\[
I(Y;Z\mid Q)\le I(Y;S\mid Q).
\]

所以，仅增加去噪轮数不能可靠区分已经被压到相同状态、却需要不同答案的历史。训练可以改变压缩函数 \(C_\phi\)，从而改变被保留的信息；这与固定状态上的更强读出是不同机制。

**优先研究的路径：**早期信息经过中间 token 的真实因果 Delta 更新后，在远处目标片段上施加去噪预测监督，并让梯度进入早期 key/value、write 和 decay。目标是理解并构造其对长程写入信用分配的作用，而非立即采用一个普通辅助 loss 作为新方法。

以连续表示的噪声预测损失作为分析对象：

\[
\mathcal L_{\rm den}
=\mathbb E_{\tau,h,\epsilon}
\left\|\epsilon-\epsilon_\theta(Y_\tau,\tau,Q,S_{t+h-1})\right\|^2,
\]

其中 \(S_{t+h-1}\) 仅由真实因果前缀构成，噪声尺度 \(\tau\) 与文本距离 \(h\) 是不同变量。离散 token 的 masked diffusion 可以有相应的 CE 目标，此处不是对实现形式的最终选择。

链式求导包含去噪损失对状态的梯度以及状态对早期写入的导数。由上面的传播式可见，长程梯度也可能被后续转换削弱；普通长跨度 denoising 并没有自动消除这个问题。

必须保留以下限制：

- 未来目标只作为训练监督；真实未来内容、目标标签或教师答案不得进入推理时的持久写入。
- 接近干净的目标块、局部可见 token 或更强教师可能提供绕过历史状态的捷径。低 denoising loss 不是长程记忆改善的证据。
- 直接从早期 \(S_t\) 预测远期目标，不等于保证信息在中间的 Delta 更新后仍被保留。
- 推理是否需要 diffusion、是否采用自适应去噪，尚未决定。Delta 框架本身不要求固定四轮；增加轮数也不等于解决记忆丢失。

## 最接近的 diffusion 工作已经覆盖什么

| 一手工作 | 本轮实际阅读范围与碰撞 |
|---|---|
| FLARE v2 | §3.1–3.2：混合 backbone 上的联合 AR/block-diffusion、clean/noisy 两路训练和递推状态接口。广义的 Delta/hybrid + diffusion 组合已存在。 |
| DeltaFlow v1 | §3：双向 GDN、噪声时刻条件化 decay/write、相邻噪声表示一致性；保留周期性 full attention。不能把这些机制重新命名为本项目原创。 |
| DreamingGoose v1 | §3、§4.4、§7：gated Delta recurrence 转换为 diffusion、训练 forward cells、recall curriculum。其特定小模型实验中 diffusion pretraining 未自动恢复 recall；训练符号范围和未见符号范围表现不同。不能外推为所有 diffusion 模型都失败。 |

这些已有工作不排除本项目提出自己的方法，但把原创问题收窄为：**在固定 Delta 状态预算与受控成本下，diffusion 怎样改变写入及覆盖，使长距离预测所需的信息更可辨识、可迁移。**

本轮不是穷尽文献检索，也没有支持“首个”或“全新架构”的结论。此前审查已提示协方差预条件、多 key 更新和 erase/write 解耦各有直接近邻，应继续逐项核对任何后续具体构造。

## 必须能被推翻的主张

以下是机制判别条件，不是新增可执行实验矩阵：

1. 若仅冻结 writer、增强 diffusion reader 就达到同样改善，则不能把收益称为记忆写入或保留能力增加。
2. 若相同信息、数据、容量和训练计算下，普通远期 CE 或教师监督取得同样效果，则不能主张 diffusion 有额外机制；收益可能来自更强远期监督。
3. 若去噪效果提高但经过更多中间写入后长程依赖仍消失，则主要假设没有得到支持。
4. 若改善只覆盖训练中的符号绑定而不支持原生任务要求的泛化，则不能声称学会了普遍的长程记忆规则。

经验验证仍使用既有公开任务、原生数据与评分协议；此处不编造 benchmark、结果或成本。

## 当前决策与下一步

收敛方向已经由用户确定；具体数学方法尚未选定。下一步只围绕这条 Delta + diffusion 主线，建立一个能区别于普通远期监督、已有噪声门和 diffusion 转换的具体构造，并给出假设、推导、预测和失败边界。

本次只更新研究文档和 checkpoint。既有工程源码、配置、Local 执行责任与历史证据保留。原始发现池仍为 1 constructed / 0 math-qualified / 0 selected；本记录不是补齐候选池或完成正式选择。所有项目软件测试、训练和原生评估仍无本轮运行结果。

## 一手来源

- DeltaNet：<https://arxiv.org/html/2406.06484v1>
- Gated DeltaNet：<https://arxiv.org/html/2412.06464v1>
- KDA / Kimi Linear：<https://arxiv.org/html/2510.26692v1>
- RWKV-7：<https://arxiv.org/abs/2503.14456>
- FLARE：<https://arxiv.org/html/2606.01774v2>
- DeltaFlow：<https://arxiv.org/html/2608.01240v1>
- DreamingGoose：<https://arxiv.org/html/2609.34253v1>
