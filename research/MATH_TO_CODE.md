# 当前数学到源码映射

当前采用规范是[扩展规格](../rounds/full-plan-2026-10-08/EXPANSION_SPEC.md)，完整逐项矩阵见[覆盖表](../rounds/full-plan-2026-10-08/COVERAGE.md)。源码generated_unexecuted；下表保留v0推导/对照历史，_read中的旧循环已拆到_workspace，coda读出到_language。

| 扩展公式 | 实际入口 | 真实连线 |
|---|---|---|
| R_u=TopK(score(tokens[:u],过去事件)) | episodic.index/retrieve、model._retrieved/EpisodicReader | forward_segment/predict_prefix/plan_prefix -> _workspace；trainer与stream完成段后才append |
| Z=tanh(Wz H+bz)、p=softmax(realize(Z)) | model.plan_prefix/realize_plan、realization.plan_snapshot/restore_plan | 既有仿射投影含可训练bias；训练_read和真实生成plan_next；独立CLI只realize保存Z |
| A=cW/max(1,||W||F)、H'=tanh(AH+B) | ContractiveWorkspace.matrix/forward、_workspace | 同一次计算固定forcing/current矩阵；finite K梯度完整；旧Transformer分支保留 |
| q(y|M)=softmax(Emb*tanh(Wf*mean(M))) | model.predict_future | window_objective仅loss用next target；trainer/history/checkpoint/validation接通 |
| L=(sum CE_main+beta*sum CE_state)/Nmain | train.window_objective/main/validation_nll | main NLL、state pairs、重复监督预算、验证CE、gradient tensor inventory各自日志 |
| (M4-R4)-(M1-R1) | scoring.factorial_bootstrap / interaction、run_matrix | 全native manifests/IDs/分母后共同episode/passage重采样；原生replay依赖 |

以上均是已知机制的具体工程构造，不是Q01或充分性/新颖性证明。

# 数学到源码的逐项对应

本表对应 `FULL_MODEL_PROPOSAL.md` 的唯一采用方案；SCIENTIFIC_SCOPE_REVIEW 中的 RMT suffix 方案是保留的备选推导。状态为 `generated_unexecuted`。源码审查和语法解析不等于运行验收。

| 数学对象/要求 | 实际实现 | Local 验收 |
|---|---|---|
| 可学习内部 SEG、段内位置、因果 prelude | `lwm.model.LatentWorldModel._encode`；`CausalBlock`；`Attention` 的上三角 mask | 改变当前/未来 token 不得改变预测它的 logits；段首受监督 |
| H0=E，concat adapter，K 次同参数 core | `LatentWorldModel._read`；`adapter`；同一 `core` ModuleList | loop count 改变计算，参数不重复创建；无内部 `no_grad` |
| 所有内部步读取相同旧记忆 | `_read` 的局部 memory，`CoreBlock.cross_attention` | caller memory 不变；内部循环不调用 writer |
| 最后工作区经独立 coda/绑定词表矩阵输出 | `_read` 的 `coda`、`output_norm`、`F.linear(..., embedding.weight)` | 对相同状态/前缀比较 teacher 与 prefix logits |
| 末位置选择与逐位置 norm/投影可交换 | `predict_prefix` 设置 `_read(last_only=True)`，仅在完整 coda 后切片 | `test_prefix_projects_only_next_position_without_changing_logits` 和 `test_prefix_projection_preserves_parameter_gradients`；训练仍输出全部行 |
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

## Full original-plan extension map

Current complete map: [COVERAGE](../rounds/full-plan-2026-10-08/COVERAGE.md); equations: [EXPANSION_SPEC](../rounds/full-plan-2026-10-08/EXPANSION_SPEC.md). EpisodicStore -> model._retrieved -> actual reader, plan_next -> realize_plan -> real language output, stream_payload/restore_stream, history_payload/restore_history and normalized next-segment state CE all have concrete source/training/generation/checkpoint routes. `lwm.realization` consumes persisted Z with no replanning. `configs/full_plan_experiments.json` and run_matrix --design generate train/inference/native-replay/paired-comparison dependencies. No code or tests were executed by Web. Conditional adaptive/Q01 and identified physical/semantic ideals remain explicitly unimplemented.
