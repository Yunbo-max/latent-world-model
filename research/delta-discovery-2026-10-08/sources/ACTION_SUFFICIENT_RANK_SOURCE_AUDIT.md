# Action-sufficient rank：来源、代码与原生测量审计

状态：2026-10-09 的 Step2 定向审计；只读论文、作者代码和原生 benchmark 接口，未执行任何项目/上游代码或下载数据。

## 1. 决定充分性的直接理论碰撞

### Bayes-Sufficient Representations in Supervised Learning

- Vasileios Sevetlidis, arXiv:2606.04045v1, 2026-06-02。
- §3.1 Definition 1 把表示定义为能经某 head 实现至少一个 Bayes-optimal action；Lemma 3.1 给出 Bayes predictor 对表示可测的 factorization 判据。
- §3.2 Definition 2 / Theorem 3.2 在唯一动作情形定义 `sigma(a*(X))` 的 Bayes quotient，并证明表示充分当且仅当该 sigma-field 被表示包含。
- §3.3 区分 sufficiency 与 minimality；§3.4 Proposition 3.3 连接 loss elicited conditional property；§3.5 明确 squared loss 只需条件均值、finite-label log loss 需要完整条件概率向量。
- §4 明确 probe 只是有限样本可恢复性诊断，不是总体 sigma-field inclusion。
- arXiv 页面未给出作者代码链接；定向 GitHub/Web 检索也没有定位官方仓库。故只记录论文公式，不能虚构实现审查。
- 结论：本项目上一轮“完整信息最优动作可由压缩信息决定”就是该框架的特例；一般 claim 已被直接覆盖。

### Loss-Shift Transfer via Bayes Quotients

- Vasileios Sevetlidis, arXiv:2606.13178v1, 2026-06-11。
- 论文以固定 `P(X,Y)`、改变 loss 的 quotient refinement 表述迁移失败；严格 refinement 时，源任务 Bayes-minimal 表示不足以支持目标任务。
- finite-output log loss 的 frozen-transfer excess risk 精确为 `I(Y;X|H)` / 条件 KL。
- 结论：仅由源目标决定充分推出目标充分的尝试已有直接否定；本轮独立任务反例仅是控制。

### Task-Sufficient Contraction：更直接的 regret-profile 近邻

- Joss Armstrong, “Task-Sufficient Contraction: Source Selection for Machine Information Interfaces,” arXiv:2610.08884v1, 2026-10-06。
- Definition 1--3 先定义 conditional risk、regret 与 regret-profile equivalence；consumer-specific source `G_C` 只合并对每个可行动作都有相同 regret 的 source states。Theorem 1 / Eq.8--10 在有限 source/action 条件下证明以 `G_C` 替换 `X` 保持完整 one-step rate--regret curve。
- §6.3 Theorem 2 对 `f(t,a)=||t+a||^2`、`aff(A)=a_0+V` 证明 `g_t(·)=g_t'(·)` 当且仅当 `t'-t in V^perp`，所以 `Pi_V t` 是 canonical regret-profile quotient；Eq.15 的 fixed-energy 特例是 centered load。论文同时给出相同最优动作但不同非最优动作 regret 的反例。
- §8 明确这是 static theory，不解决 state-changing action、递归闭包或未来未声明 task。它覆盖本轮“只保留最优动作可能过粗”和 affine-quadratic task projection；本轮 SVD 尾和只剩额外线性 feature/head class 下的 RRR 逼近控制，不是新的 sufficiency quotient。

两个它所比较的直接近邻也封闭了更宽的命名空间：

- Walsh, arXiv:2606.09858v1，把 finite single-cycle 的 full support state、action alphabet 与 consequence-sensitive policy regret 写成 rate--regret problem；policy equivalence 是 exact zero-regret endpoint。它不解决 recurrent state，但已覆盖“action-sufficient compression + regret distortion”的单周期解释。
- Wei et al., “What Must a World Model Distinguish for Planning?”, arXiv:2609.33030v1，§3.2 区分 mechanism/response/decision sufficiency；§4.1 Eq.1--2 令所需区分显式依赖 query、candidate set 与 regret cover；§5.1--5.2 进一步说明搜索/候选生成阶段可要求比最终选择更多的信息。这与本项目“修改有效性 × future-query geometry 必须联合”高度相邻，但仍不是 Delta 在线条件矩的构造或可估计性结果。

## 2. 低秩与任务导向训练的直接近邻

### Reduced-rank regression

- A. J. Izenman, “Reduced-rank regression for the multivariate linear model,” Journal of Multivariate Analysis 5(2):248--264, 1975。
- 该工作研究已知秩约束下的 multivariate linear regression，历史上以 canonical variates/SVD 给出 reduced-rank 解。
- 本轮固定 SPD 输出度量与 feature covariance 后的 `sum_(i>r) sigma_i^2` 公式直接由白化加 Eckart--Young--Mirsky 得到；不是新矩阵定理。
- 更现代且可直接核查的算法定位是 Donnat & Tuzhilina, JMLR 27(160), 2026，§3 Eq.7 的 rank-constrained least squares；Algorithm 1 先做 OLS，再以 rank-`r` SVD 截断。它与 Eckart--Young--Mirsky 一起直接覆盖本轮固定 metric/covariance 的可计算部分。

### Action-Sufficient State Representations

- Huang et al., “Action-Sufficient State Representation Learning for Control with Structural Constraints,” arXiv:2110.05721v2, 2022-06-19 / ICML 2022, PMLR 162:9260--9279。
- §2.1/Proposition 1 用结构图、Markov 与 faithfulness 假设选择影响未来 reward 的最小 action-sufficient state components；§3 用 structured sequential VAE 估计。
- 该工作是 POMDP/RL 的结构因果状态选择，不是 Delta 局部 edit 的 weighted low-rank theorem；但“action-sufficient state”名称与目标不能作为本项目新意。

### Decision-focused / posterior-Bayes action learning

- Wilder, Dilkina & Tambe, AAAI 2019, “Melding the Data-Decisions Pipeline”。作者仓库 `bwilder0/aaai_melding_code` 固定 `1fd7d6a5f39e4e6560d91547ac9f8a8d70962c9c`。
  - `README.md` blob `75adfd04bf5d7cc0c5959c138311e47220a23bdb`：声明 differentiable LP 与 submodular solvers。
  - `submodular.py` blob `1dd4771ae61e9acdf28d622b06ca427b53c9bc0a`：`ContinuousOptimizer.forward` 求最优决定，`backward` 经 KKT system 对参数求导。
  - `coverage.py` blob `95d48c16c7e863eafc8c3b077c7e981e1416d8ee`：coverage objective、gradient/Hessian 和 projected optimizer。
  - 这些接口显示直接按 downstream decision 训练已有实际实现；不等于本项目已运行或适用于 Delta。
- Mandi et al., ICML 2022, PMLR 162:14935--14947，§1/摘要把 decision-focused learning 表述为直接优化 solver 决定质量，并给 pointwise/pairwise/listwise ranking losses。
- Rychener, Kuhn & Sutter, ICML 2023, PMLR 202:29455--29472，Assumption 4.2 要求 loss 对 action 光滑、decision map 对参数光滑且相应梯度有界；Theorem 4.3 在其步长条件下给出趋向 stationary point，而不是全局最优。把该点识别成 posterior Bayes action 还要另假设它是 global minimizer 且 decision-map class 足够丰富；Proposition 4.4 给出 finite-observation lookup-table 条件。不能把这些有条件结果写成任意标准 end-to-end 算法的无条件结论。
- 结论：将表示目标从预测真值改为 downstream action/regret 的原则已有充分近邻；本轮只能保留 Delta-specific条件和成本边界。

### Decision-Sufficient State Representations（递归 writer 的直接近邻）

- Bingyu Shen & Boyang Li, “Decision-Sufficient State Representations: Measuring and Reducing Write-Time Regret,” arXiv:2609.32805（v1 2026-09-26；当前审读 v2 2026-09-29），preprint under review。
- §3 Eq.1 定义递归 writer `z_t=U(g,z_(t-1),a_(t-1),o_t)`，冻结 reader，并把相对 full history 的 sufficiency gap 分为 hindsight read-time oracle 的 budget loss `beta_t` 与 prospective recursive writer 的 write-time regret `kappa_t`。论文明确说明 read-time oracle 不是严格 bound。
- §4 Eq.2 以未来 reference-action reader log-likelihood 给候选 state 打分；关键区别是把候选 state 经同一 writer 在真实 logged steps 上递归 forward 到未来决定点。论文报告 window/fixed-context score 对 lossy writer 会隐藏重写，故采用 recursive form。
- §5.4--5.6 报告在预注册 test split 上只在短 lag 有显著收益，长 lag gates 失败；一旦早期 rewrite 丢失事实，best-of-n 候选无法恢复，per-step score又看不到连续后续保留所需的信用链。
- 论文 §5.1 的 TextWorld 原生对象有 privileged optimal-policy action，只用于 reader loss/oracle，不给 writer/reader。它与普通文本 next-token任务的信息条件不同，不能直接移植为本项目真值。
- 正文给出匿名代码仓库 `https://anonymous.4open.science/r/AgentDSSR`。匿名页面不暴露 Git SHA，只显示 Snapshot ready 2026-09-25（available until 2027-03-01），故不虚构 commit pin；固定的可见 raw tokens 为 `README.md` `b635535a`、`dssr/score.py` `0f30b28b`、`scripts/score_candidates.py` `7ef1af52`。README 指向 `run/03_dssr.sh`（round-0 SFT、DPO rounds）与 `run/04_test.sh`；`scripts/score_candidates.py` 从 `dssr.score` 导入 `ScoreJob`、`Target`、`subset_scores` 与 `sufficiency_matrices_recursive_many`，与正文 recursive candidate scoring 对应。README 还要求 one GPU >=32GB，不能假定 2080Ti 可执行。本轮只读接口，未执行或复现。
- 结论：递归 writer 的 downstream reader loss、forward-rolled候选评分和长延迟 credit assignment 已被直接覆盖。Delta 残余必须超出这一功能，例如给出可核查的连续状态特有结构/界，而不是重新命名未来 loss。

## 3. Predictive state 是更强而不同的对象

- Singh, James & Rudary, “Predictive State Representations: A New Theory for Modeling Dynamical Systems,” UAI 2004:512--519，§2 Eq.1--3 以 tests 的成功概率定义 predictive state、core tests 与递归更新；它要求未来预测充分性，通常严格强于固定 loss/action family 的 Bayes quotient。ICML 2003 的 “Learning Predictive State Representations” 是另一篇论文，二者不混引。
- 因此本项目不能把 action sufficiency 写成“完整 predictive state 已实现”；反过来，也不能用 PSR 的强要求否定目标相关压缩的可能性。

作为另一条区别，Tishby--Pereira--Bialek, physics/0004057v1，§3.1 Eq.15 与 Eq.28 的 Information Bottleneck 保留 relevance distribution / mutual-information tradeoff；它不等同于 fixed-loss action quotient，不能用 IB 名称替代上面的 regret 对象。

## 4. 原生 benchmark 接口

### 项目已有 bAbI/LAMBADA

- 沿用既有固定 source records：bAbI 20 tasks/20000 denominator；LAMBADA 使用当前源码与 official harness 对应的 `lambada_openai`、5153 denominator。
- 两者给 native answer/last-token endpoint，不给 ideal Delta action、full-state Jacobian、conditional metric 或 Bayes quotient label。任何 teacher/local solve 产生的 action label 都是派生对象，必须另记模型、版本、信息和成本，不能冒充原生标注。

### LongMemEval

- Wu et al., ICLR 2025 / arXiv:2410.10813；作者仓库 `xiaowu0162/LongMemEval` 固定当前审计 commit `9e0b455f4ef0e2ab8f2e582289761153549043fc`。
- `README.md` blob `3490db4f796c14903788ecb3e33f056cab438bb0`：500 questions，含 knowledge updates、temporal reasoning、multi-session 与 abstention；schema 包含 question/type/answer/date/haystack sessions。
- `src/evaluation/evaluate_qa.py` blob `4732f3772b04a2b9069121ade304e6320494abc2`：`knowledge-update` prompt 只要求响应包含更新后的正确答案；即使同时含先前信息也可判正确。scorer 输出 yes/no endpoint。
- README 还明确 `has_answer: true` 是 turn-level evidence label，`answer_session_ids` 是 session-level evidence label，官方 retrieval 评测可测相应 recall；因此不能笼统称整个 benchmark“只有 endpoint”。这些原生标签仍不直接判定“旧关联是否被局部 edit 删除”、representation rank 或 Bayes action sufficiency。若未来使用，必须分开 QA endpoint 与 retrieval labels，并保留 native scorer/500 denominator，固定并记账 judge arm；README 官方示例 `gpt-4o` 有 API 成本，但 model zoo 也支持本地 `llama-3.1-70b-instruct` endpoint，故不无条件写成“必须付费”。本数学阶段没有下载或评分。

## 5. 覆盖决定

| 原子主张 | 最近工作覆盖 | 残余 |
|---|---|---|
| 压缩表示只需恢复固定任务 Bayes action | Bayes-Sufficient Representations 直接覆盖 | Delta 动作族实例化，不是一般新理论 |
| source contraction 保留所有动作 regret / rate--regret curve | Task-Sufficient Contraction 直接覆盖 | 其理论是静态的，不解决递归 writer 闭包 |
| 任务/loss 改变可破坏充分性 | Loss-Shift Transfer 直接覆盖 | Delta horizon/query/task family 的具体实例 |
| 宽度 `r` 的最优线性动作误差是尾奇异值 | RRR + Eckart--Young 直接覆盖 | 随机度量、在线估计、自然重要性仍未闭合 |
| 直接按决定质量训练表示/预测器 | Decision-focused learning / posterior Bayes action 直接覆盖 | Delta 因果 writer 的具体可达/成本约束 |
| 递归 writer 用未来 reader loss、forward rollout 评分 | DSSR 直接覆盖并报告长 lag 失败 | Delta 连续状态的特有结构/界尚未出现 |
| 知识更新任务能验证 action rank | 不成立 | LongMemEval 有 QA endpoint 和 evidence-retrieval labels，但没有 action-rank/内部 edit 标签 |

审计处置：`major direct collision / retain controls and an unadmitted Delta-specific lead`。未定位 Bayes-sufficiency 两篇预印本的作者代码；DSSR 匿名代码接口已固定但未执行。这些事实不影响论文公式碰撞，也不能被解释为不存在其他 prior implementation。当前唯一可继续核查的残余是 information-dependent random metric 与递归因果估计/Jacobian 的非平凡耦合；它尚未成定理或自然测量对象。没有新增 D 编号。
