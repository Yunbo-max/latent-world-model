# R05 v2 来源、最近工作与原生测量审计

状态：**v2 final-byte review pending**。  
父审计：`REPAIR_R05_PARTIAL_ID_SOURCE_AUDIT.md`，SHA256 `af64fd37ea501defba073e39a2d7c956bac402d016223f8ae5c5a7eba5e8d76c`；父审计原字节保留。  
绑定数学对象：`repairs/R05_PARTIALLY_IDENTIFIED_VALIDITY_GEOMETRY.v2.md`（最终 SHA 待复审）。  
检索/读取截止：2026-10-10 00:58 UTC。范围为下列论文全文、作者仓库固定 commit 与明确列出的文件；没有据此证明“所有文献均无同式”。

## 1. 直接理论近邻：不是 R05 新发明的原语

### 1.1 Fréchet class、极端耦合与分位重排

- Puccetti & Wang, **Extremal Dependence Concepts**, Statistical Science 30(4), 2015；arXiv:1512.03232，作者修订全文：https://sas.uwaterloo.ca/~wang/papers/2015Puccetti-Wang-STS.pdf 。
- 实际读取定位：§1 的 Fréchet class、Definition 1.1、quantile/rearrangement 表示与 Theorem 1.1；§3.1 的 bivariate countermonotonicity；§4 的 fixed-marginal optimization。
- 该来源直接支持“相同边际对应大量联合耦合”“同向/反向重排给二元超模函数的极端期望”这一理论家族。R05 的

\[
\max(0,\mu-(1-p)U)\le E[rZ]\le\min(\mu,pU)
\]

是 Bernoulli `r` 与 bounded `Z` 的 Fréchet–Hoeffding/support specialization；完整 `Z` 边际下的 quantile 积分是 bivariate extremal-coupling/rearrangement 原语。两者均不得声称为 R05 发明。

### 1.2 Partial identification 与 robust regret

- Aradillas Fernández et al., **Robust Bayes Treatment Choice with Partial Identification**, arXiv:2408.11621。实际读取 2024-08 HTML v1 全文 §1、§2.3 Definitions 1–2、Theorems 1–2 与结论：https://arxiv.org/html/2408.11621v1 。它明确区分 ex-ante `Gamma`-minimax regret 与 ex-post `Gamma`-posterior expected regret，并允许随机化动作。
- Montiel Olea, Qiu, Stoye, **Decision Theory for Treatment Choice Problems with Partial Identification**, arXiv:2312.17623：https://arxiv.org/abs/2312.17623 。本轮只核对摘要/引用链，不把它冒充逐式来源。
- Delage & Ye, **Distributionally Robust Optimization under Moment Uncertainty**, Operations Research 58(3), 2010。实际读取作者全文的 support/moment ambiguity set 与 worst-case expectation formulation：https://web.stanford.edu/~yyye/distRobOpt_OR_rev0.pdf 。这是广义 moment-DRO 近邻，不是 R05 的 Fréchet 闭式的最直接来源。

R05 的 squared-regret 中点解是把一个已知 quadratic regret 在闭区间上最小化的初等后果。直接碰撞后，残余只能表述为：**把已知依赖不确定性原语特化到 Delta 的 validity × horizon-sensitivity，并导出声明 surrogate 下的 no-write 认证边界**。原创性未建立。

## 2. 固定作者实现与原生接口

### ROME / CounterFact

- 作者仓库固定 commit：`0874014cd9837e4365f3e6f3c71400ef11509e04`。
- 实际文件：`experiments/py/eval_utils_counterfact.py`，blob `80bb6be2b47c61b3fd2613d626955ff549615690`。
- 函数：`compute_rewrite_quality_counterfact` 解包 `requested_rewrite`，读取 rewrite/paraphrase/neighborhood/attribute/generation prompts，并返回对应概率与 generation statistics。它是行为 endpoint scorer，不记录 Delta 内部 `r,J,Z,m` 或 paired write/no-write potential outcomes。

### EvEdit

- 论文：Liu et al., **EVEDIT: Event-based Knowledge Editing for Deterministic Knowledge Propagation**, EMNLP 2024：https://aclanthology.org/2024.emnlp-main.282/ 。
- 作者仓库固定 commit：`9a09377517a22cd87f100621df52fc254b19800c`。
- 实际读取：`README.md`；`EvEdit_benchmark/QA.json` blob `28abf34b7c8c51ca117a7ac9cf5b985bf0b93b8a`；`Completion.json` blob `99098abac635fb3065f96a27729cd48759dc6acb`；目录还列出 `counterfact.json` 与 `events.json`，但本轮不下载/执行它们。
- 精确语义：EvEdit 提供事件描述及每事件五组 related QA/completion；论文规定前四组可由 past/latest/event context 推断，第五组为 unknown。样例可涉及旧事实、新事实与推理，但发布字段只命名 `QA1`–`QA5`，未固定声明前三类语义标签。

### 连续编辑正则化

- Gupta et al., **Lifelong Knowledge Editing requires Better Regularization**, arXiv:2502.01636v2 / Findings EMNLP 2025：https://arxiv.org/html/2502.01636v2 。实际读取 §3、连续编辑与 downstream 评估。
- 作者仓库固定 commit：`6e3ba9a87978a23b6db2676ba7540216bf5d4fd0`。
- 实际文件：`experiments/evaluate_unified_editing.py`。`DS_DICT` 映射 MultiCounterFact/CounterFact/zsRE 到原生 scorer，循环按 batch 做 sequential edit，并可按步调用 `GLUEEval`。它测 edit endpoint 与周期性 downstream degradation，不提供逐写入联合机制标签。

### EasyEdit

- 作者仓库固定 commit：`4c109870955a4522ac3d7cf10ad00f34de8e4f0d`。
- 实际读取：`README.md` factual editing 数据树与 locality/portability 说明（CounterFact/ZsRE、distracting neighbor、other attribution、commonsense、inverse relation、one-hop、subject replacement）。这些是行为端点 schema，不是 R05 latent joint-moment ground truth。

## 3. 最近工作差异与处置

| 近邻 | 已覆盖 | R05 仅剩残余 | 处置 |
|---|---|---|---|
| Fréchet–Hoeffding / extremal coupling | support/固定边际下的 sharp dependence bounds、quantile rearrangement | Delta `r × ||Ju||²` 的命名与条件化特例 | 已知原语，不计原创 |
| Gamma-minimax / partial-ID decisions | identification set、robust regret、随机化动作 | 声明 surrogate 的闭式 gate/no-write corollary | 条件推论，不是新范式 |
| moment-DRO | support/moment ambiguity 上 worst-case 决策 | scalar closed form | 广义强 baseline |
| Bayes gate / change detector | 估计 revision 概率、控制 false release | 量化边际概率不足以识别 future-geometry coupling | 不创造外部 validity 证据 |
| R03 v2 horizon certificate | 事前 finite-horizon harm 上界 | 可提供 `U`，不提供 `r` 或 `m` | 必要交互，非完整方案 |
| ROME/EvEdit/EasyEdit/sequential editing | efficacy、paraphrase、locality、event-related QA、unknown、下游退化 | 没有 per-Delta joint variables 或 paired outcomes | 原生机制测量缺口 |

## 4. 有界检索记录与代码缺口措辞

本轮检索组合限于：`partial identification + minimax regret`、`moment uncertainty + DRO`、`extremal dependence/rearrangement + quantile`、`EvEdit/ROME/EasyEdit/sequential knowledge editing + official GitHub/evaluator`。读取上述固定论文和作者仓库后，**本次审计未核对到**一个实现 R05 exact scalar gate 的作者软件接口；这不是不存在性证明。

## 5. 原生测量结论

可原生测量：edit success、paraphrase/generalization、neighborhood/locality、事件相关 QA/completion、unknown 回答、连续 edit 后下游准确率。

不能原生测量：一次 Delta 提议的真实 validity `r`、完整未来 Jacobian `J`、方向敏感度 `Z`、joint moment `m`、动作 propensity、write/no-write 双潜在损失或相对 oracle 的真实 regret。

故 endpoint 结果不能反演机制，本阶段不创建 benchmark、标签、case、metric、scorer 或结果。

## 6. 来源结论

**conditional control；direct theoretical collision established；novelty unresolved/not established；native mechanism measurement absent；not D/admitted/selected。** R05 的价值是把一条 Delta 联合可辨识性缺口写成明确的 decision boundary，而不是发现 partial identification、extremal coupling 或 robust regret 本身。

