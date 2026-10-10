# R06 选择性真实性审计：来源、作者接口与原生测量审计

状态：**final-byte review pending**。  
绑定对象：`repairs/R06_SELECTIVE_VALIDITY_AUDIT.v1.md`（SHA 待最终字节复审）。  
检索/读取截止：2026-10-10 01:58 UTC。只记录实际读取的全文、固定作者仓库接口与有界检索；不把“未发现同式”写成不存在证明。

## 1. 直接理论碰撞

### 1.1 无偏主动学习与 influence/PPS 分配

- Imberg et al., **Optimal sampling in unbiased active learning**, AISTATS 2020, PMLR 108：https://proceedings.mlr.press/v108/imberg20a.html ，全文 https://proceedings.mlr.press/v108/imberg20a/imberg20a.pdf 。
- 实际读取 §2 的顺序选择、正 inclusion probability 与 inverse-probability/HT 无偏风险；§3 与 Propositions 1--3 的方差最优 PPS/influence sampling。它直接覆盖“用样本损失或 influence/sensitivity 安排昂贵标签，再用已知 propensity 校正”的抽象机制。
- R06 的 `pi∝Z sqrt(q/c)` 或 residual-aware `pi∝Z sqrt(q(1-q)/c)` 是该类 Neyman/influence allocation 在二值事实标签乘 Delta 敏感度上的特例，不是新的采样原理。

### 1.2 Active testing

- Kossen et al., **Active Testing: Sample-Efficient Model Evaluation**, ICML 2021, PMLR 139：https://proceedings.mlr.press/v139/kossen21a.html ，全文 https://proceedings.mlr.press/v139/kossen21a/kossen21a.pdf 。
- 实际读取 §§2.1--2.2 与 §3.1：固定模型、昂贵测试标签、顺序随机 acquisition 与 LURE 无偏风险；Eq. (5) 的 ideal proposal、Eq. (6) 的 surrogate approximation，以及随已审计标签自适应的条件选择概率。
- 若 R06 目标是总体真实性/风险，选择性审计加 propensity 校正与该范式直接相邻。

### 1.3 两阶段 validation sampling

- Amorim, Tao, Lotspeich, Shaw, Lumley, Shepherd, **Two-Phase Sampling Designs for Data Validation in Settings with Covariate Measurement Error and Continuous Outcome**, JRSS A 2021，全文 https://pmc.ncbi.nlm.nih.gov/articles/PMC8715909/ 。
- 实际读取 §2 的 phase-1/phase-2 setup 与 §4.1.1、Eqs. (8)--(9) 的 influence-function Neyman allocation。R06 用便宜 Delta sensitivity/proxy 作 phase-1，再购买真实性标签，属于同一设计框架。
- Chen and Lumley, **Optimal multiwave sampling for regression modelling in two-phase designs**，全文 https://pmc.ncbi.nlm.nih.gov/articles/PMC7902311/ 。实际读取 pilot/multiwave 后更新 influence function 与 allocation 的接口；它覆盖“先少量审计、再适应性重分配”的直接 baseline。

### 1.4 适应性推断

- Hadad et al., **Confidence intervals for policy evaluation in adaptive experiments**, PNAS 2021：https://www.pnas.org/doi/10.1073/pnas.2014602118 。实际读取 history-adapted assignment、IPW 重尾与加权 AIPW 区间讨论。
- Cook, Mishler, Ramdas, **Semiparametric Efficient Inference in Adaptive Experiments**, CLeaR 2024：https://proceedings.mlr.press/v236/cook24a.html ，全文 https://proceedings.mlr.press/v236/cook24a/cook24a.pdf 。实际读取 §2 history-dependent propensity/truncation 与 §4 time-uniform confidence sequence/data-dependent stopping。
- 因此自适应改变 audit probability、早停或反复选 horizon/gate 时，iid 区间不是合法新贡献；适应性 AIPW/martingale/CS 是强控制。

## 2. 公式核对与残余

对 `m=T^{-1}sum Y_tZ_t`，Bernoulli 审计 HT 方差为

\[
T^{-2}\sum_t(1-\pi_t)(Y_tZ_t)^2/\pi_t.
\]

固定期望成本下 oracle propensity 与条件二阶 contribution 的平方根成正比。审计前 `Y` 未知，anticipated-optimal HT 为 `pi∝Z sqrt(P(Y=1|X)/c)`；AIPW 则按 residual influence 的条件二阶矩分配。故 sensitivity-only allocation 只在稳健或额外条件下最优；同时估计 `E[Y]`、`E[YZ]` 等多目标时也没有自动共同最优。

可保留的 Delta residual 不是采样器本身，而是：

1. `Z=||Ju||²` 或其完整递推版本是否可用严格更低成本、prefix-only 地获得；
2. proxy `widetilde Z` 是否对 residual influence 有充分性/效率界；
3. `Y`、保护损伤和动作曲率能否构成可检查的 `Y→r` bridge；
4. 完整 coupled state 是否让 sequential DR/OPE 得到严格更小的充分状态或方差。

这些均未由当前 R06 建立。

## 3. 固定作者实现与原生接口

### ROME / CounterFact

- 作者仓库 `kmeng01/rome`，commit `0874014cd9837e4365f3e6f3c71400ef11509e04`。
- 文件 `experiments/py/eval_utils_counterfact.py`，blob `80bb6be2b47c61b3fd2613d626955ff549615690`，函数 `compute_rewrite_quality_counterfact`。
- 输入/输出覆盖 rewrite、paraphrase、neighborhood、attribute 与 generation 行为 endpoint；该固定版本未记录 audit indicator、inclusion probability、独立 gold validity、write/no-write potential outcome 或 Delta `J,Z`。

### EvEdit

- 作者仓库 `Lumos-Jiateng/EvEdit`，commit `9a09377517a22cd87f100621df52fc254b19800c`。
- `README.md` blob `df82ba7a066590e0fd149dd483b7724901b1f59e`；`EvEdit_benchmark/QA.json` blob `28abf34b7c8c51ca117a7ac9cf5b985bf0b93b8a`；`EvEdit_benchmark/Completion.json` blob `99098abac635fb3065f96a27729cd48759dc6acb`。
- 发布的是事件相关 QA/completion endpoint；README 说明从 CounterFact 过滤并以 GPT-3.5 扩增。它不提供随机审计 propensity 或部署时旧知识仍有效 oracle。

### EasyEdit / KnowEdit

- 作者仓库 `zjunlp/EasyEdit`，commit `4c109870955a4522ac3d7cf10ad00f34de8e4f0d`。
- `examples/KnowEdit.md` blob `15198d39aaef40a4adb71439821997d22061b4f8`：prompt、target_new、ground_truth、portability/locality 字段。
- `easyeditor/evaluate/evaluate.py` blob `a7c0a2114e50b789aca828547c0db5227b3f6a9c` 与 `easyeditor/editors/editor.py` blob `db7ebda61eb7a2579a0d555ef64c734f7b81faa1`：rewrite/rephrase、locality、portability 与 sequential edit 接口。
- 均为行为 endpoint/答案键，不是随机 verification design。

### 连续编辑正则化

- Gupta et al., **Lifelong Knowledge Editing requires Better Regularization**, arXiv:2502.01636v2 / Findings EMNLP 2025；作者仓库 `scalable-model-editing/knowledge-editing-regularization`，commit `6e3ba9a87978a23b6db2676ba7540216bf5d4fd0`。
- `experiments/evaluate_unified_editing.py` 顺序 edit 并周期评估；`create_samples_cf.py` blob `a3bb82a0a981b2233259139e742c5bd6a6f75b6a` 以固定 seed 生成 unique-subject shuffled indices。
- 这是 evaluation sampling，不记录 sensitivity-based audit propensity。

### SEAL

- 作者仓库 `Continual-Intelligence/SEAL`，commit `6d9c9f9ee392c6cc618e771f399d436d190f6ca4`。
- `general-knowledge/src/continual/continual_self_edits.py` blob `24fc1506c20b9a1f7159e51db6818ccc1bfeb137`：固定数据子序列、self-edit、LoRA tune/merge、当前/先前问题 accuracy matrix。
- `general-knowledge/src/inner/TTT_server.py` blob `ffa2b8f3e04ce45a3b8737645fd7819c88f0096c`：pre/post outcome、adapter gain 与 GPT-4 judge。
- `general-knowledge/src/EM/build_SFT_dataset.py` blob `45e945502df9e3279d4867d6dfcdae7f62b6d220`：按 adapter/proxy mean 排候选。
- SEAL 是用 post-update outcome 学 self-edit 的强高层近邻；其标签不是随机事实审计，固定版本也未记录 propensity。

## 4. 原生测量结论

上述资产可原生测 edit efficacy、paraphrase、locality、portability、事件 QA/completion、连续 edit 后退化或 self-edit gain；均不联合提供 `(外部 grounded Y, Delta Z, audit pi)`，也不提供 write/no-write 双潜在结果。把预注册随机审计叠加在它们上面会构成新评估协议，不是原生 scorer。本阶段不造标签、case、metric、协议或结果，measurement gap 保留。

## 5. 来源处置

**MECHANISM COLLISION / REROUTE TO THEORY OR CONTROL。** 条件数学可通过；主体机制被 HT/AIPW、Neyman/PPS、two-phase validation、active testing 和适应性推断覆盖；原创性未建立，实验效果未知。不要把碰撞写成整个科学问题错误：真正可修残余是最优 propensity 的语义/公式、`Y→r` bridge、Delta proxy 充分条件、序列总效应与可测量闭环。
