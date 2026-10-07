# 数学到源码的逐项对应

本表对应 `FULL_MODEL_PROPOSAL.md` 的唯一采用方案；SCIENTIFIC_SCOPE_REVIEW 中的 RMT suffix 方案是保留的备选推导。状态为 `generated_unexecuted`。源码审查和语法解析不等于运行验收。

| 数学对象/要求 | 实际实现 | Local 验收 |
|---|---|---|
| 可学习内部 SEG、段内位置、因果 prelude | `lwm.model.LatentWorldModel._encode`；`CausalBlock`；`Attention` 的上三角 mask | 改变当前/未来 token 不得改变预测它的 logits；段首受监督 |
| H0=E，concat adapter，K 次同参数 core | `LatentWorldModel._read`；`adapter`；同一 `core` ModuleList | loop count 改变计算，参数不重复创建；无内部 `no_grad` |
| 所有内部步读取相同旧记忆 | `_read` 的局部 memory，`CoreBlock.cross_attention` | caller memory 不变；内部循环不调用 writer |
| 最后工作区经独立 coda/绑定词表矩阵输出 | `_read` 的 `coda`、`output_norm`、`F.linear(..., embedding.weight)` | 对相同状态/前缀比较 teacher 与 prefix logits |
| 完整已观察段的一次 gated writer | `MemoryWriter.forward` 与 `_write` | 新状态逐坐标在 [-1,1]；改变 K 不改变相同观测的写入 |
| logits 第 i 行预测 tokens 第 i 项 | `forward_segment`: reader E[:,:-1]，writer E[:,1:] | `window_objective` 不再 shift；所有首/尾/EOS 目标各计一次 |
| 生成时不提前提交部分段 | `StreamState`、`observe`、`predict_prefix`、`commit_segment` | 0..L−1 前缀保留；只有非 EOS 达到 L 才写入；短 commit 拒绝 |
| EOS 是已预测的终止目标 | `observe` 直接 reset；训练由文档索引管理边界 | 含 EOS 的尾部 writer 返回值丢弃，不跨文档传状态 |
| 新观测与生成分支的生命周期 | `ingest` 返回新状态；`generate` 返回分支状态，不原地修改输入 | 调用者原状态保持；想保留外部证据状态时丢弃生成分支 |
| 窗内 writer 经下一段 NLL 学习 | `window_objective` 连续调用 `forward_segment` 后合并损失 | 至少两段且后续损失有效时，早段 writer 有梯度 |
| TBPTT 截断及梯度累积 | `train.main` 每个 U 段窗口 backward 后 detach；多个独立窗口累积梯度，再更新 | 不把梯度累积误叫更长 BPTT；窗口首之前梯度被截断 |
| token 加权而非窗口平均 | `loss_sum / accumulate_targets` backward，先乘 accumulate_targets/实际目标数，再 unscale；FP64 计算全局梯度范数 | 短文档/尾 batch 不被重复放大；修正乘法的溢出也由 AMP 检出；答案 mask 排除 context 目标 |
| 精确 100M/1B 目标预算 | `CorpusCursor.take_window(max_targets=remaining)`；训练 seen_targets | SEG/padding/内部循环不计 token；跳过优化的目标另列 |
| 不丢文档边界的恢复 | `CorpusCursor.state_dict`，checkpoint memory/counters/RNG/optimizer/scaler | 中断恢复和不中断的参数/样本位置一致；不兼容源码/资产拒绝恢复 |

训练以 U 个相邻段为一次反向传播窗口。梯度累积把多个这种窗口合为一次优化器更新，但不会延长它们之间的反向传播路径。数值记忆会继续跨窗口传递；优化器更新后继续使用旧参数生成的 detached memory 是本文已经披露的 stateful TBPTT 近似。评测固定参数，从每篇/每个完整问题上下文的起点重新构造状态。

`memory_enabled=False` 是 history-reset 对照：reader 每段只见同一个可学习初态，writer 结果被丢弃。模块名义参数和 writer 前向调用仍存在，但有效梯度、writer 反向计算与记忆模型不同。比较必须报告真实总成本，不能宣称两者计算严格相等。

实际采用固定 K、确定初态、dropout=0，无 Q01 提前停止、无隐式固定点梯度、无未定义 ELBO、无 flash-only kernel、无 BF16 前提。手工 FP32 attention score/softmax 是明确的兼容性选择；是否高效由 Local 测量。

测试文件是软件语义验收，允许小整数张量检查因果/梯度/恢复。它们不是新造的科学评测集，也不替代完整 bAbI/LAMBADA 原生验收。
