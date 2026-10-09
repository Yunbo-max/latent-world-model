# R04 v3 联合选择：来源、实现、碰撞与测量审计

审计对象：`repairs/R04_CONSOLIDATION_DYNAMICS.v3.md`，SHA256 `eb4ddfd81c947bf6fc176a1863f1618f3d095fc2366850c9964f0524384d8093`。审计日期 2026-10-09。本文是 integration writer 的来源审计，独立来源复核另存；所有仓库内容只做静态读取，没有执行作者程序、下载模型/数据、训练、推理或评分。

## 1. 继承且仍适用的公式/实现证据

R04 v3 不重新把已完成阅读包装成新发现。下列证据由 v2 audit 固定，v3 只引用其与选择问题直接相关的部分：

1. **Sleep**：Behrouz et al., *Language Models Need Sleep*, arXiv `2606.03979v2`，实际阅读 §3.2–3.3、Eq.(3) 及资源说明。它已有发送端 expert、较慢 MLP 扩容、teacher/student distillation、base update 和 reset；因此“选择后进入慢端”与“睡眠式巩固”不是 R04 的新点。论文页未定位到可固定的作者实现，不能用第三方实现补足。
2. **HOPE / Nested Learning**：arXiv `2512.24695v1`，实际阅读 §7.1 Eq.(70)–(74) 和 §8。CMS 已覆盖多频率参数/记忆更新；它没有给 R04 的 additive interface 或 survival threshold，但足以否定“多时间尺度本身是新机制”。没有定位到可固定的作者 HOPE 实现。
3. **SynControl**：Bicknell & Latham, eLife reviewed preprint 2025，作者仓库 `babicknell/SynControl@d8681d2af9f858827fa1f22f7910e00eb2284fbc`。静态读取 `scripts/run_simple_model.py::run` blob `1b1984b15988d469f4e60a9645f22637a4349f08` 和 `syn_control/bayes_learn.py::{BayesLearner.__init__,update}` blob `bbc87aa387a565d0ca589bdcbe3b5853f8838b14`。总预测误差驱动快控制，慢更新显式校正快控制影响；“联合快慢误差”已有直接强近邻。
4. **SEAL**：作者仓库 `Continual-Intelligence/SEAL@6d9c9f9ee392c6cc618e771f399d436d190f6ca4`。静态读取 `continual_self_edits.py::{run_one_sequence,_merge_lora}` blob `24fc1506c20b9a1f7159e51db6818ccc1bfeb137` 与 `TTT_server.py` blob `ffa2b8f3e04ce45a3b8737645fd7819c88f0096c`。它提供连续 self-edit/LoRA merge 和旧任务矩阵，是遗忘负证据及参数级对照，不是 Delta fast→slow 迁移实现。
5. **普通二次决策/模型编辑**：MELO Proposition 1、APO 的 posterior/二次参数优化、ROME/AlphaEdit 的投影/正规方程已在 joint-conditional-risk audit 逐项记录。故 v3 式(5)–(8) 的 normal equation、硬约束消元和 PSD 几何必须归为已知数学；潜在残余只能来自 Delta 的有序传播、可表示接口及 survival-matched 条件后果。

还需区分两篇同名 **Language Models Need Sleep**：除上面的 Behrouz et al. `2606.03979v2` 外，Sangyun Lee et al. 的 arXiv `2605.26099` 把近期 context 通过 `N` 次离线 recurrent passes 和 learned local rule 写入持久 SSM fast weights。它是相关 fast-weight consolidation 近邻，但不是快状态向较慢参数的 selective migration，也未发现 `p>alpha^T` 阈值；本审计不把两篇同名工作混为一个实现或机制。

## 2. 本轮新增直接碰撞

### 2.1 Selective synaptic consolidation 已有更早机制

Leimer, Herzog, Senn，*Synaptic weight decay with selective consolidation enables fast learning without catastrophic forgetting*，bioRxiv DOI `10.1101/613265`（2019）。bioRxiv 入口本轮返回 403，但作者学位论文镜像保留该论文全文；独立复核实际读到 `w=w_f+w_s`、快分量衰减、超过活动/快权重阈值后进入慢分量以及过早巩固损伤的公式与讨论。没有定位到作者代码，也没有发现精确的 `p>alpha^T` 条件风险阈值；但“衰减快权重 + 选择性慢巩固”已经是公式级强机制碰撞，而不是 R04 创新。

### 2.2 动态快慢巩固已有噪声—时间常数理论和作者实现

Bhasin, Raymond, Goldman，*Synaptic weight dynamics underlying memory consolidation*，PNAS 2024，DOI `10.1073/pnas.2406010121`。作者仓库 `goldman-lab/consolidation-integration@e54415ca7a445d7ab5d8a3bc6142e4fe645e6f57`，本轮静态读取 README 及 notebooks：

- `simulations-heterosynaptic.ipynb` blob `bdfa2e5879862d7543e285f125696f0c769b8ba1`：含 `tau_f,tau_mvn,tau_learn,tau_post`、ideal consolidation gain 和显式 ODE；
- `simulations-external-noise.ipynb` blob `a57a44499606f4c06bd949501dffa10e52bf65b5`：含对应时间常数、噪声驱动动态与指数学习项；
- `calculations-heterosynaptic.ipynb` blob `196c7fcdf3077c4b5fef136639a03212058c88b8`：理论计算入口。

notebook 仅按原始 JSON/代码单元静态读取，未执行。该工作已覆盖快慢动态、时间积分和噪声/学习权衡；没有发现 R04 的 Delta 有序 `E(I-D)` 传播或二元未来有效性阈值。它是理论/实现近邻和未来对照，不是 v3 公式的直接先占证明。

### 2.3 2026 年 agent memory 已明确 cost-aware routing + slow consolidation

*Dual-Layer Agentic Memory with Fast Write Routing and Slow Consolidation*，固定 arXiv `2608.22215v2`（2026-08-31）。独立复核实际阅读全文 HTML §§3.3–3.4：写入反事实奖励 `r(W)=EM(W)-EM(D)-lambda_s`、value-of-escalation gate、SFT write-back 与 probe-based flush；Table 2 报告 1,752 个 stable facts 的 degradation。作者仍声明代码/数据 acceptance 后发布，故没有作者实现可读。它直接覆盖 cost-aware write routing、选择性 slow consolidation、反事实 action value 与遗忘监控，显著压缩 R04 的方法差异；但其对象不是本稿的线性 Delta `E(I-D)` 推导，不能据此断言式(2)–(11)逐式已知。

## 3. 原生测量与可辨识性

`xiaowu0162/LongMemEval@9e0b455f4ef0e2ab8f2e582289761153549043fc` 的 README blob `3490db4f796c14903788ecb3e33f056cab438bb0` 与 `src/evaluation/evaluate_qa.py` blob `4732f3772b04a2b9069121ade304e6320494abc2` 已实际读取。knowledge-update endpoint 可以测更新后答案，但 scorer 允许同时包含旧信息，也不暴露潜在的巩固/不巩固未来损失、内部 `C,L,G,g` 或事实有效性。SEAL 原生连续编辑矩阵可测参数级旧任务保持，但默认多 GPU 且依赖付费 grader，机制和当前资源均不匹配。本阶段不执行、不替换 scorer、不造数据。

因此：真实后来 token/任务反馈可作为离线预测风险监督；它们不是部署时可见 oracle。观察日志若没有随机化/overlap/顺序可交换性，不能识别同一前缀下巩固与不巩固两个潜在结果。v3 的标量阈值是声明分布下的条件决策结果，不是由现有 benchmark 自动验证的事实标签。

| 主张 | 最近工作/原生对象 | 本轮可支持状态 |
|---|---|---|
| 快衰减、慢巩固、选择性 capture | Leimer 2019；Goldman 2024；Sleep；SynControl | 机制已知，不能计新方法 |
| Delta `E(I-D)` 有序传播下的联合充分矩 | v2 推导 + 普通二次决策近邻 | 条件数学可审；原创差异未闭 |
| `p>alpha^T` survival-matched 阈值 | 本稿标量模型；未发现精确公式碰撞 | 有价值 lead，不足以准入 |
| 更新后行为 endpoint | LongMemEval、SEAL matrix | 可测部分终点，不识别内部机制/反事实 |
| 提高 updater / RSI | 上述资产均不足 | measurement gap，实验未知 |

## 4. bounded search 与处置

检索日期 2026-10-09。定向检索包括：`fast slow weight decay selective consolidation threshold`、`fast memory slow consolidation cost aware routing`、`synaptic weight dynamics memory consolidation code`、`Dual-Layer Agentic Memory fast write routing slow consolidation`。使用 primary arXiv、DOI/期刊页和作者仓库；第三方摘要只作定位，不作公式证据。搜索不是系统综述；`2608.22215v2` 已完成全文公式阅读，但作者代码/数据尚未公开。

贡献审查结论：v3 式(3)–(11) 若数学独立复核通过，可保留为 **Delta differential-decay 下的条件化选择理论/control**；normal equation、选择性快慢巩固和多时间尺度不是新贡献。`p>alpha^T` 是最清晰的残余可证伪陈述，但最近工作精确差异、同预算统计优势与原生机制测量尚未闭合。建议 R04 在第三次修订后 park，不进入活动/科学准入/选择计数。重开需要全文/作者代码证据支持精确残余，或出现能原生判别 joint survival 几何的同预算对象。
