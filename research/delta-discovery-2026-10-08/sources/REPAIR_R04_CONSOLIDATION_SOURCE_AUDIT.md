# R04 快慢巩固递推：来源、实现与测量审计

审计对象：`repairs/R04_CONSOLIDATION_DYNAMICS.v2.md`，SHA256 `ba81ea9506160ee5e640faed2673ad068e925da82bb7ea77595999d7151f2732`。2026-10-09 阅读；本稿是 root 来源审计，独立来源审查另存，不自称独立。所有代码仅静态读取。

## 1. 恢复和最近工作范围

恢复 parent main `3f323bf039d280a983078aafe8bc272ca085f464` 的 AGENTS、checkpoint、GOAL/PROGRESS/batch 和既有 R01–R03/STEP2 累积来源。R04 接续 coupled-updater 的 consolidation 缺口，没有把已有小增益/Jacobian、随机日志或信用 quotient 重命名。以下阅读是补充原义务，不声称所有近邻已查尽。

### Sleep：全文明确存在扩容、蒸馏和 reset

Ali Behrouz, Farnoosh Hashemi, Adel Javanmard, Vahab Mirrokni，**Language Models Need Sleep: Learning to Self-Modify and Consolidate Memories**，固定 arXiv `2606.03979v2`（2026-07-10），https://arxiv.org/html/2606.03979v2 。本轮实际读取 §3.2–3.3、Eq(3) 的 seeding objective 及 appendix resource 说明。§3.2 向较慢 MLP 新增低秩 expert；§3.3 用尚未应用的新 base 参数定义 student，保持旧 teacher，通过 distillation 训练新慢 expert，再应用 sender base update 并 reset sender experts。不能把新增参数/蒸馏的收益外推为固定总状态下无损迁移，更不能称本稿(2)是该作者算法。v2 作者列表含 Javanmard，v1/旧网页的三人列表不应替代固定v2。

来源碰撞：巩固、较慢记忆、teacher/student、reset 和扩展容量早已覆盖。R04 的残余是一个明确加性 Delta 子模型中的当下读出与递推兼容条件；没有发现足以证明它是新理论贡献的文献饱和证据。论文页仅有 arXiv bug tracker GitHub 链接；定向标题+github 查询未确认作者官方实现，不用第三方 Sleep/HOPE 代码冒充。这是作者代码缺口，不是“作者必无代码”的结论。

### HOPE/Nested Learning：多频率并非本稿的 additive transfer

固定 `2512.24695v1`，https://arxiv.org/html/2512.24695v1 ，复读 §7.1 Eq(70)–(74)、§8 入口。CMS 的 sequential chain、定频更新和 head-wise aggregation 已覆盖多时间尺度；对参数更新/上下文梯度的嵌套解释不是 `M+=C,S−=C` 的全闭环等价性保证。官方说明 https://research.google/blog/introducing-nested-learning-a-new-ml-paradigm-for-continual-learning/ 已在 inherited audit 读取；本轮不将其摘要当新公式证据。作者 HOPE 可固定实现仍未确认。Titans 原有审计/作者接口缺口继承，不新称完成。

### 快慢耦合已有直接 Delta/控制近邻

Brendan A. Bicknell, Peter E. Latham，**Fast and slow synaptic plasticity enables concurrent control and learning**，eLife reviewed preprint v1，2025-03-24，DOI `10.7554/eLife.105043.1`。主站本轮出现 client challenge；实际全文从作者 UCL PDF https://www.gatsby.ucl.ac.uk/~pel/papers/fast_slow_elife25.pdf 读取 Results pp2–3、Methods “Online linear regression” pp17–18、Code availability p42。PDF 文本提取有部分公式缺失，不能只据提取文字声称全部公式核对；因此进一步固定**作者仓库** `babicknell/SynControl` commit `d8681d2af9f858827fa1f22f7910e00eb2284fbc`（2024-09-20），实际读取：

- `scripts/run_simple_model.py::run`，blob `1b1984b15988d469f4e60a9645f22637a4349f08`：`y=(w+dw)@X`, `f=y−y_tar`；慢更新 `w−=lr*(f−dw*N*nu_bar)*X`，快更新 `dw−=f/(N*nu_bar)`。快控制针对总预测，慢学习显式扣去快控制的影响；不是简单独立两个 loss 的拼接。
- `syn_control/bayes_learn.py::{BayesLearner.__init__,BayesLearner.update}`，blob `bbc87aa387a565d0ca589bdcbe3b5853f8838b14`：总权重 m+dw，真实误差/迟滞缓冲、posterior mean/variance、Kalman/control gain 和 eligibility，体现控制与慢学习耦合。读取对应定义和 update，不运行 Riccati/scipy/模拟。

它的 toy fast 更新是 uniform across synapses，目标由真实 teacher signal给出，慢更新校正的是快控制去除后的误差；R04 rank-one key write、离散迁移和 decay ordering 并非该代码同式。但“总输出误差 + 快慢耦合纠偏”已明确是强 baseline，不能以R04总残差为主创新。其真实target/平滑性与语言知识有效性不同；不能直接把控制学习称为 LM RSI。

经典快慢权重：Hinton/Plaut 1987 author PDF https://www.cs.toronto.edu/~hinton/absps/fastweights87.pdf 已打开但网页正文无可检索文本，截图接口只返回placeholder，未据此完成公式级审查；J. Schmidhuber 的作者回顾 https://people.idsia.ch/~juergen/fast-weight-programmer-1991-transformer-bigrefs.html 的1987 summed weights说明可支持历史近邻定位，不能替代1987全文公式审查。1987原文精确对照仍列缺口，不用它证明R04完全覆盖。

## 2. 实际 SEAL 作者接口与预算

**Self-Adapting Language Models (SEAL)** arXiv:2506.10943，作者仓库 `Continual-Intelligence/SEAL` commit `6d9c9f9ee392c6cc618e771f399d436d190f6ca4`，本轮重新静态读取：

- `general-knowledge/src/continual/continual_self_edits.py::{run_one_sequence,_merge_lora}`，blob `24fc1506c20b9a1f7159e51db6818ccc1bfeb137`。生成新 passage self-edit，积累旧QA，tune/eval临时adapter，随后 `merge_and_unload` 到下一步 base。含 base row 和旧任务下三角矩阵。代码的 docstring merge/eval顺序概述与实际流程不完全同序；这里以函数实际执行顺序为准，不声称merge之后立即评估同一轮。
- `general-knowledge/src/inner/TTT_server.py::accuracy_and_texts` 和 request loop，blob `ffa2b8f3e04ce45a3b8737645fd7819c88f0096c`。请求含 train_sequences、eval_questions及LoRA超参，回答由 `grade_with_gpt4` 判定；临时adapter是每轮请求，不等于跨轮base不变。

这是参数级连续更新/merge，非快记忆 recurrence compensation，不能说 SEAL 自己已经实现R04。作者已有连续self-edit遗忘的负证据保留；不将 LoRA merge 本身视为无遗忘巩固。原生 driver 默认7B且要求至少两GPU ID；沿用的 RTX2080Ti 预算不能宣称此原生程序可直接运行。官方grade依赖付费API；本阶段不执行也不替换成自造metric。

## 3. 原生 benchmark/scorer 复查

`xiaowu0162/LongMemEval` commit `9e0b455f4ef0e2ab8f2e582289761153549043fc`：本轮读 `README.md` blob `3490db4f796c14903788ecb3e33f056cab438bb0` 和 `src/evaluation/evaluate_qa.py::get_anscheck_prompt` blob `4732f3772b04a2b9069121ade304e6320494abc2`。原生格式为 question_id/question_type/question/answer/question_date/haystack_*，hypothesis输出；更新任务允许回答含旧信息，只要包含正确更新答案。judge模型在脚本中固定映射为 gpt-4o/gpt-4o-mini或本地70B接口；这不是内部Delta迁移/旧知识有效性评分。README已有V2链接，本轮范围固定原版本，不声称其覆盖V2。数据资产有官方发布入口，本轮不下载；has_answer与answer_session_ids是评价标签，不能送给部署更新器。

| R04主张 | 可用原生对象 | 限制/状态 |
|---|---|---|
| knowledge-update终点正确性 | LongMemEval已有官方格式与QA judge | 可测终点，非巩固机制证据；无付费执行授权 |
| 参数连续编辑的旧任务表现 | SEAL官方下三角矩阵 | 参数级、默认资源不匹配；仍可作为已知强对照 |
| Eq(1)–(10)递推一致性/几何条件 | 数学符号审查 | 本轮有推导和反例；没有用新造benchmark代替原生测量 |
| 持久化Delta快→慢改善后续学习效率 | 未找到直接原生配套任务/scorer | measurement gap；不能把单上下文准确率当基础能力提高 |
| 跨新任务/部署中改进updater、RSI | 上述endpoint均不足 | updater参数真实改进、迁移和外部新任务证据缺失 |

## 4. 更新后的贡献审查

Patch A 是 affine gauge/redundant representation 的消元结果，任何匹配的信息/状态都可用单W实现，不计新架构。Patch B 总残差与差异衰减是已知快慢思想的Delta特化；(8) 和非交换条件是有价值的诊断，但尚无独立最近工作差异或原生机制测量，不能因局部数学修复而准入。强同信息对照必须包含固定预算单W Delta、普通快慢总残差、write-rate/decay以及适用时LoRA+replay/distillation。效益未知，未评估。

定向查重仅作bounded search：system2三个query：fast slow weights consolidation subtract fast weights function preserving memory delta rule；Sleep multi timescale learning fast experts consolidation reset 2606.03979；Complementary Learning Systems neural networks weight consolidation fast slow Ba 2016 fast weights。system1验证：Language Models Need Sleep github Behrouz consolidation；Hinton Plaut fast weights slow weights consolidation 1987。后续system2：105043 fast slow weights consolidation code；fast weights slow weights subtract consolidation。搜索引擎快照/版本未暴露，完整性未认证；有些结果是第三方笔记，仅定位不用作公式证据。

处置建议：R04保留为修复完成的理论/control，2/3数学修订尝试；保留v1错误和review。下一合法动作是从已有joint-conditional-risk线索重新审查可表示C的有效性/收益联合目标，以及其与本文差异衰减项的必要作用；这需要实质新delta，不是保证再修订一次必有候选。5历史/0活动/0准入/0选择以及20/15缺口保持。
