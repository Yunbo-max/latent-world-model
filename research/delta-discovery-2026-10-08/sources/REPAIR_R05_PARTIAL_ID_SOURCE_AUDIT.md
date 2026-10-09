# R05 v1 来源、最近工作与原生测量审计

状态：source audit draft；绑定对象为 `repairs/R05_PARTIALLY_IDENTIFIED_VALIDITY_GEOMETRY.v1.md` 的最终审查前版本。独立 source reviewer 必须重新绑定最终 SHA256。

## 1. 固定来源与读取范围

### Robust Bayes / partial identification

- Aradillas Fernández, Montiel Olea, Qiu, Stoye, Tinda, **Robust Bayes Treatment Choice with Partial Identification**, arXiv:2408.11621，读取 2024-08 HTML v1 的定义、主要定理与讨论；全文入口：https://arxiv.org/abs/2408.11621 。论文明确区分 ex-ante `Gamma`-minimax regret 与 ex-post posterior robust criterion，并说明部分识别下随机化动作可为最优。它是 R05 的直接决策论近邻，但不含 Delta memory、`Z=||Ju||²` 或本文闭式区间。
- Montiel Olea, Qiu, Stoye, **Decision Theory for Treatment Choice Problems with Partial Identification**, arXiv:2312.17623，摘要与引用链核对：https://arxiv.org/abs/2312.17623 。用于确认 minimax-regret/partial-ID 是成熟主线，不作为 R05 闭式推导的出处。
- Delage & Ye, **Distributionally Robust Optimization under Moment Uncertainty**, Operations Research 58(3), 2010；作者公开 PDF：https://web.stanford.edu/~yyye/distRobOpt_OR_rev0.pdf 。读取 ambiguity set、support/mean/covariance 与 worst-case expectation 定义。它覆盖“只凭矩与支持集做 worst-case 决策”的一般机制；R05 不得把 moment ambiguity/minimax 包装成新优化范式。

R05 的 `m_-,m_+`、二点 sharpness 构造、平方 regret 中点解和 no-write 条件均在卡内逐步推导；来源只支持其所属已有理论家族，不证明该 Delta 特例原创。

### Knowledge editing / sequential degradation

- Meng et al., **ROME / CounterFact** 作者仓库 `kmeng01/rome`，README 与公开 evaluator 接口核对；仓库：https://github.com/kmeng01/rome 。README 指向每条 CounterFact record 的 `compute_rewrite_quality`，结果围绕 edit request、paraphrase/neighborhood 与生成质量，不是逐 Delta action 的潜在结果日志。
- Liu et al., **EVEDIT: Event-based Knowledge Editing for Deterministic Knowledge Propagation**, EMNLP 2024，论文：https://aclanthology.org/2024.emnlp-main.282/ ；作者仓库固定到 commit `9a09377517a22cd87f100621df52fc254b19800c`：https://github.com/Lumos-Jiateng/EvEdit/tree/9a09377517a22cd87f100621df52fc254b19800c 。实际读取 `README.md`、`EvEdit_benchmark/QA.json` 与 `Completion.json`。样本有 `id` 和五组问答/补全，含旧事实、新事实、推理及 unknown 问题；没有 `r,J,Z,p`、写入 propensity 或 write/no-write 双潜在结果。
- Gupta et al., **Lifelong Knowledge Editing requires Better Regularization**, arXiv:2502.01636v2 / Findings EMNLP 2025；全文：https://arxiv.org/abs/2502.01636 ，作者仓库：https://github.com/scalable-model-editing/knowledge-editing-regularization 。读取论文 §3、连续编辑与 downstream 评估，以及作者 `experiments/evaluate_unified_editing.py`：它按批次编辑、调用 CounterFact/zsRE scorer，并定期跑 GLUE 类下游任务。它提供连续退化负证据和 endpoint scorer，不提供 R05 联合隐变量。
- EasyEdit 作者框架：https://github.com/zjunlp/EasyEdit 。读取 README 的 factual editing 数据、locality 与 portability 结构。它扩展行为端点评估，但仍没有本文机制变量的原生真值。

## 2. 真实最近工作差异

| 近邻 | 已覆盖 | R05 仅剩的具体差异 | 处置 |
|---|---|---|---|
| Gamma-minimax / partial-ID treatment choice | 识别集、regret、robust action、随机化 | Delta 固定写入方向上 `validity × horizon sensitivity` 的闭式 scalar specialization | 理论特例，不足以声称新范式 |
| moment-DRO | 支持/矩歧义集上的 worst-case expectation | `rZ` 的 sharp support-moment interval 与 no-write 边界 | 可能是有用推论；原创性未立 |
| Bayes edit gate / change detector | 估计 revision 概率或控制 false release | 指出边际概率不等于联合 future geometry，并量化 regret | 不能创造 validity 证据 |
| R03 v2 horizon certificate | 给动作前 finite-horizon harm 上界 | 该上界可充当 `U`，但不识别 `r` 或 `m` | 必要交互，非完整方案 |
| CounterFact/EvEdit/EasyEdit | efficacy、paraphrase、locality、event reasoning、unknown | 无内部 Delta 联合标签/反事实 potential outcomes | 保留 measurement gap |
| sequential editing regularization | 多次 edit 后编辑分数和 downstream degradation | 无逐写入 `rZ` coupling 或 robust gate ground truth | 可测终点，不能测机制 |

## 3. 作者实现与接口核查

1. EvEdit 作者仓库最近 commit 为 `9a09377517a22cd87f100621df52fc254b19800c`（2024-02-16）。`EvEdit_benchmark` 实际包含 `QA.json`、`Completion.json`、`counterfact.json`、`events.json`；这里没有执行或下载模型/数据，只读目录与小范围文本。
2. ROME README 明确 evaluator 入口；当前作者仓库的历史路径可能与 MEMIT fork 的 `eval_utils_counterfact.py` 不同，故本审计只声称已核对公开接口，不冒称逐行复现 scorer。
3. Gupta et al. 作者仓库 `evaluate_unified_editing.py` 的 `DS_DICT` 实际映射 CounterFact/MultiCounterFact/zsRE scorer，并在序列 edit 中可定期调用 downstream evaluator；这支持“endpoint 可测、联合机制不可测”的结论。
4. Robust Bayes 与 Delage–Ye 提供论文公式；未发现与 R05 同名的作者软件接口。没有软件接口不妨碍数学近邻成立，也不能反向支持原创。

## 4. 原生测量结论

可由现有资产原生测量：edit success、paraphrase/generalization、neighborhood/locality、event deduction、unknown 回答、连续 edit 后下游准确率。

不能原生测量：一次 Delta 提议是否真实有效 `r`、完整未来 Jacobian `J`、方向敏感度 `Z`、其 joint moment `m`、动作 propensity、write/no-write 双潜在损失、minimax-regret 相对 oracle 的真实性。

因此本轮不能声称 benchmark 已验证 R05；也不创建新 benchmark、标签、metric、case 或结果。

## 5. 来源结论

R05 的数学问题真实且闭式边界可检查，但主要机制与 partial identification、Gamma-minimax regret 和 moment-DRO 高度相邻；知识编辑资产只支持问题价值和 measurement gap。source 结论是 **conditional control, novelty unresolved/not established, native mechanism measurement absent**。

