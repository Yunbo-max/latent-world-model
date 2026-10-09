# R03 保护感知随机日志：来源与碰撞审查

审查对象：`repairs/R03_PROTECTION_AWARE_LOGGING.v1.md`。本文件固定主要全文/作者入口、公式碰撞和原生测量边界；网页摘要不替代公式阅读。

## 1. 主要来源

1. Wan, Kveton, Song, **Safe Exploration for Efficient Policy Evaluation and Comparison**, ICML 2022, https://proceedings.mlr.press/v162/wan22b.html 。该文直接研究既安全又高效的 bandit policy-evaluation 数据收集，推导 exploration policy 并讨论 DR 扩展；这是 R03 最直接的上层机制碰撞。
2. Zhu, Kveton, **Safe Optimal Design with Applications in Off-Policy Learning**, AISTATS 2022, https://proceedings.mlr.press/v151/zhu22a.html 。论文构造相对 production baseline 安全且信息高效的 logging policy，并覆盖 side information 与线性 contextual 扩展；这直接否定把“安全 propensity 优化”作为新主张。
3. Kazerouni, Ghavamzadeh, Abbasi-Yadkori, Van Roy, **Conservative Contextual Linear Bandits**, arXiv:1611.06426v2 (2017), https://arxiv.org/abs/1611.06426 。论文的 CLUCB 要求累计表现相对 baseline 在所有时刻保持阈值，并给出保守代价；其安全对象是累计 reward，不是 Delta 旧查询输出损伤。
4. Jagerman et al., **Safe Exploration for Optimizing Contextual Bandits**, arXiv:2002.00467v1 (2020), https://arxiv.org/html/2002.00467v1 。SEA 用 logging policy 收集数据、高置信 OPE 比较候选与已部署策略，只有候选 LCB 超过部署 UCB 才切换。它已覆盖“安全基线 + propensity/OPE + 置信部署”，但没有 Delta 几何损伤证书。
5. Pacchiano, Ghavamzadeh, Bartlett, **Contextual Bandits with Stage-wise Constraints**, JMLR 26 (2025), https://jmlr.org/papers/volume26/24-0267/24-0267.pdf 。其逐轮约束为期望 cost 不超过阈值；有限臂 OPB 每轮解 `max Σπ_a u_a^r` s.t. `Σπ_a u_a^c≤τ`，并以 cost UCB 作悲观安全约束。R03 的 `Σμ_a U_a≤b` 属于同一通用约束族。
6. Wang, Agarwal, Dudík, **Optimal and Adaptive Off-policy Evaluation in Contextual Bandits**, ICML 2017, https://proceedings.mlr.press/v70/wang17a.html 。该文给出 agnostic OPE 的 minimax 边界，IPS/DR 匹配常数阶，并提出 SWITCH 的 bias-variance 折中。R03 延续 R02 的 AIPW/DR 识别，不能把它计作原创。
7. Xu et al., **LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory**, ICLR 2025, https://proceedings.iclr.cc/paper_files/paper/2025/file/d813d324dbf0598bbdc9c8e79740ed01-Paper-Conference.pdf ，作者仓库 https://github.com/xiaowu0162/LongMemEval 。原生轴包括 knowledge update，但记录是终点问答/检索，不含随机 Delta 更新 propensity 或内部保护损伤标签。
8. Zweiger et al., **Self-Adapting Language Models (SEAL)**, NeurIPS 2025 / arXiv:2506.10943, https://arxiv.org/abs/2506.10943 ，作者实现 https://github.com/Continual-Intelligence/SEAL ，作者说明 https://jyopari.github.io/posts/seal 。SEAL 用更新后 downstream performance 作为 self-edit 学习信号，并报告连续 self-edit 的旧任务遗忘；其动作是生成 SFT 数据/指令并更新参数，不是 Delta fast-weight 安全 propensity 设计。

## 2. 公式级碰撞结论

- `μ_a≥ε`、IPS/AIPW/DR 与 inverse-propensity variance 属于标准随机化/OPE。
- 在期望 cost 约束下选择随机策略属于 stage-wise constrained contextual bandit/线性规划；在估计 cost 上加置信上界也是已有 optimism-pessimism 安全机制。
- `μ_a=sqrt(g_a/(λ+ηU_a))` 是凸实验设计的 KKT 结果；即使推导正确，也不是独立新架构。
- R03 可保留的 Delta-specific 内容只有 rank-one 写入的精确局部证书 `d_a=α_a²β²(eᵀMe)kᵀG_pk`、平方风险交叉项/充分界，以及由它得到的 overlap-budget 不可行条件 `b<εU_1`。
- 硬投影/soft preconditioning 是更强的同信息对照：若保护方向已知且允许改动作，它们可直接降低 `d_a`；R03 的残余价值在于当仍需随机比较完整动作时显式优化采样概率。

## 3. 作者代码接口核查

- SEAL 作者仓库 `Continual-Intelligence/SEAL` 固定 commit `6d9c9f9ee392c6cc618e771f399d436d190f6ca4`。`general-knowledge/src/inner/TTT_server.py` 的 server request handler 接收训练序列、评估问题、LoRA 超参和 reward mode 并训练临时 adapter；`accuracy_and_texts` 是回答生成/评分 helper；`general-knowledge/src/continual/continual_self_edits.py` 逐步生成 self-edit、训练并 merge LoRA，输出下三角旧任务表现矩阵。README 明示需要 OpenAI API key，并称全部实验可用 2×A100/H100 运行、其他硬件可能需重构或缩小模型；本阶段未运行。
- LongMemEval 作者仓库 `xiaowu0162/LongMemEval` 固定 commit `9e0b455f4ef0e2ab8f2e582289761153549043fc`。数据字段含 `question_id/question_type/question/answer/question_date/haystack_*`；`src/evaluation/evaluate_qa.py::get_anscheck_prompt` 进行 LLM judge，`print_qa_metrics.py` 汇总 task/overall 并固定官方 judge。它不提供 propensity、write/no-write potential outcomes 或 protected-query validity oracle。
- SEPEC 的 PMLR 页面未给 code link；Safe Optimal Design 的 PMLR 页面提供 supplementary ZIP，但本轮未建立可固定的作者代码接口/commit。该实现缺口不影响全文公式级 collision，却不能写成完成了作者代码接口审查。
- 本轮在论文页与定向 GitHub 搜索中也未确认 CLUCB、SEA 或 JMLR stage-wise paper 的作者官方实现入口；因此没有用第三方实现冒充作者代码，也没有基于未确认代码接口作机制结论。

连续学习的强实现对照也已固定，而非只按名称查重：GEM (`facebookresearch/GradientEpisodicMemory`, commit `34c6b8e9a0607db7567301c48b727430d20bee7e`, `model/gem.py::{store_grad,overwrite_grad,project2cone2,Net.observe}`)、EWC（同仓库 `model/ewc.py::Net.observe`）、A-GEM (`facebookresearch/agem`, commit `45421499483b28935491251e9e821c55e8b3c089`, `model/model.py::create_stochastic_gem_ops`) 与 OGD (`MehdiAbbanaBennani/continual-learning-ogdplus`, commit `b633f2c5949f6ea165e2e76aab3d043065d770a8`, `ogd/tools.py::project_vec`) 已分别覆盖 replay-gradient 不等式、Fisher 二次惩罚、参考梯度投影与旧输出梯度正交投影。直接把它们换到 S/k-space 不计新方法。

## 4. 原生可测量性

| 主张 | 现有原生对象 | 状态 |
|---|---|---|
| knowledge-update 后终点正确性 | LongMemEval knowledge-update | 可测终点，不测 propensity/certificate |
| 连续 self-edit 后旧任务遗忘 | SEAL continual-learning protocol | 可测参数编辑结果，机制与资源不匹配 |
| 单步保护查询输出损伤 | 需决策时有效保护 query 集与内部 readout | 无原生标签；measurement gap |
| AIPW action effect | 需随机动作、精确 propensity、真实延迟损失 | 现有 Delta benchmark 不原生提供 |
| 长期 coupled-state 安全 | 需完整 Jacobian/长期有效性与依赖处理 | 单步证书不足 |

## 5. 审查决定

来源支持 R03 是一个条件成立、可证伪的 Delta 特化安全日志控制；来源同时否定把“成本约束的随机策略优化”作为原创候选。数学正确性、贡献差异、实际效果三者必须分开：前者待最终字节独立数学审查；机制新颖性目前不足；实际效果完全未知且未执行。计数保持 5 历史 / 0 活动 / 0 科学准入 / 0 选择。
