# R05 v4 来源、原创性与原生测量审计

状态：**绑定 final repair bytes；独立来源复审待对本审计最终 SHA 回签**。  
绑定数学对象：`repairs/R05_PREFIX_CONDITIONAL_PARTIAL_ID.v4.md`，SHA256 `8451497499d6b4a9fb13bbf5aca5464b85c3e27eaca6d50633460738c3acfbaf`。  
父审计：`REPAIR_R05_V2_PARTIAL_ID_SOURCE_AUDIT.md`，其原字节与固定代码定位全部保留。  
本轮检索/读取截止：2026-10-10 20:45 UTC。只对下列实际读取的全文与官方页面作结论；不声称穷尽全部文献，也未完成 Ben-Michael、D'Adamo、Ji 作者实现的固定 commit 审计。

## 1. 本轮新增的最直接碰撞

### 1.1 Conditional linear programs

- Eli Ben-Michael, **Partial identification via conditional linear programs: estimation and policy learning**, arXiv:2506.12215v2：https://arxiv.org/html/2506.12215v2 。arXiv 页面把 v2 的最后修订日期列为 2025-08-14；HTML 渲染稿 front matter 另标 2026-08-24，二者分别记录，后者不冒充 arXiv 版本日期。
- 实际读取：§2.1 式 (1)–(2) 把部分识别参数写成协变量条件 LP 的逐点上下界，再取 `E[theta_L(X)]` 与 `E[theta_U(X)]`；§2.2 包含 joint potential-outcome 分布与 policy-learning 例；§3 Assumptions 1–2 给出条件 nuisance 的 debiasing、sample splitting/cross-fitting 需求；§4 明确扩展到 value partially identified 的 policy learning。
- 判定：R05 v4 的每-stratum Fréchet 闭式是这个 conditional-LP 范式的极低维解析特例。条件化、取期望、debiased estimation 与 policy learning 均不是新原语。

### 1.2 Individualized policy learning under partial identification

- Riccardo D'Adamo, **Orthogonal Policy Learning Under Ambiguity**, arXiv:2111.10904v3，2022-12-30：https://arxiv.org/pdf/2111.10904 。
- 实际读取：§1–§2 关于 `X` 条件的 partially identified CATE、minimax risk/regret 等 ambiguity criteria、个体化 policy；§3 的 surrogate welfare；§4–§5 的 orthogonal/sample-split estimation 与 non-smooth nuisance 代价。
- 判定：它直接覆盖“协变量条件的个体化 robust policy + partial identification + estimation”。R05 的 Delta 变量替换与二变量闭式不能单独建立科学原创性。

### 1.3 Covariates can sharpen partial-identification bounds, but estimation is nontrivial

- Ji, Lei, Spector, **Model-Agnostic Covariate-Assisted Inference on Partially Identified Causal Effects**, arXiv:2310.08115v3，2026-08-24：https://arxiv.org/abs/2310.08115 。
- 实际读取：摘要、主文关于 pretreatment covariate stratification、conditional distribution nuisance、optimal-transport duality、uniform validity 与 covariate/model selection。
- 判定：支持“合法 pre-action covariates 可缩小 identified set”及“高维条件估计会带来推断代价”；不直接给 R05 的 scalar gate，但进一步削弱条件化本身的原创性。

### 1.4 Robust personalized policy improvement

- Nathan Kallus, Angela Zhou, **Confounding-Robust Policy Improvement**, NeurIPS 2018：https://proceedings.neurips.cc/paper/2018/file/3a09a524440d44d7f19870070a5ad42f-Paper.pdf 。
- 实际读取：§3 对 baseline policy 的 minimax-regret improvement、个体化 policy class 与 propensity uncertainty set；结论。
- 判定：在 uncertainty set 正确指定的条件下，baseline-safe individualized robust policy 已知。其 sensitivity-model ambiguity 与 R05 的 fixed-marginal coupling ambiguity 不同，但“只有证据充分的上下文才偏离 baseline”不是独立新范式。作者关联代码仓库的静态接口含 `ConfoundingRobustPolicy(baseline_pol)` 与 `.fit(x,t,y,q0,GAMS,method_params,...)`，并支持 `interval`/`L1-budget` uncertainty；本轮未固定该仓库 commit，故不声称完成版本锁定的实现审计。

### 1.5 General partial-ID decision rules

- Christensen, Moon, Schorfheide, **Optimal Decision Rules when Payoffs are Partially Identified**, arXiv:2204.11748：https://arxiv.org/abs/2204.11748 。
- 实际读取：全文 §1、决策规则与 conditional identified set 论述、结论。其规则在给定 point-identified `P` 的 identified set 上最小化最大 risk/regret，并讨论 bootstrap/Bayes 实现。
- Kitagawa, Lee, Qiu, **Treatment Choice, Mean Square Regret and Partial Identification**, arXiv:2310.06242：https://arxiv.org/abs/2310.06242 。实际读取全文引言、minimax rule 与结论；它说明 fractional/randomized decision 在 partial identification 下亦是既有对象。

## 2. R05 v4 的数学来源边界

R05 v4 的新推导由三条标准事实组成：

1. 对每个 `C=c` 应用父审计已确认的 Bernoulli × bounded-variable Fréchet/support bounds；
2. 在 rectangular ambiguity 下，有限直积的 worst-case objective 按 stratum 分离；
3. 每层 quadratic regret 的区间 Chebyshev center 是端点中点。

“pooled lower bound 为零但某一 conditional lower bound 为正”的例子是上述条件化的直接推论。它对 Delta 控制很有用，但本轮全文已明确发现 conditional partial-ID estimation 和 individualized ambiguity-robust policy 的直接覆盖，故不得声明为首个或新架构。

## 3. 作者代码与原生 benchmark 接口

父审计已固定 ROME/CounterFact、EvEdit、EasyEdit 与 sequential-editing 作者仓库/文件/函数。本轮没有运行代码或下载数据；也没有发现这些原生 scorer 新增 per-action `r,Z,m_c` 或 paired potential outcomes。

Ben-Michael 与 D'Adamo 的方法处理可观测数据下的 conditional nuisance/identified set，不能凭论文公式自动生成 Delta 写入的 ideal-validity 标签。把编辑 benchmark 的 endpoint score 当 `r` 或把自由运行损失当动作前 `Z`，会产生 post-treatment leakage/定义错位。

## 4. 强简单对照与处置

- 同信息 baseline：no-write、pooled R05 v3、contextual Bayes/joint-value predictor、conditional LP、orthogonal ambiguity policy、R06 型审计。
- R05 v4 可能的优势只剩：对特定二变量 surrogate 有闭式、易解释、`O(1)`/stratum；尚无同预算统计或计算优势证明。
- 数学状态与贡献状态分离：即使 final-byte 数学通过，也只支持 `conditional control theorem`；原创性不成立，实效未知。

## 5. 来源结论

**contribution/function-level direct collision established；未定位到完全相同的 Delta 二变量闭式；Delta-specific closed-form specialization only；native mechanism measurement absent；not D/admitted/selected。** 第三次修订完成后应 park，除非获得合法 joint evidence、Delta-specific non-rectangular structure 或同预算优势证明。

