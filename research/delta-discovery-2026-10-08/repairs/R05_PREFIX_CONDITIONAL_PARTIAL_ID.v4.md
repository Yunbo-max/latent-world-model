# R05 v4：前缀条件化的部分识别 Delta 门

状态：**待 final-byte 独立复审的条件数学 control；不是 D 候选；未执行实验**  
直接父项：`R05_PARTIALLY_IDENTIFIED_VALIDITY_GEOMETRY.v3.md`，SHA256 `c8911d5910f96f73e4c7320827a048f57d33f2c2c00c0c2cbd7d172687d9325c`。  
修订类型：目标/构造不匹配修复；attempt `3/3`。v1–v3 的公式、反例与复审原字节全部保留。

## 1. 原问题 → 具体 patch

v3 对全体 prefix 池化，只允许常数 gate。其 `m_-=0` 结论正确地说明 pooled marginals 不足，却不能排除：部署时已知的某些 prefix strata 有正的 conditional lower bound，因而可以只在这些 strata 写入。

令 `C` 为动作前 filtration `F_t` 可测的有限或可数 context；它只能由同一可见 prefix、当前状态与预先固定的特征映射得到，不能包含未来 token、任务答案、事后 edit 成败或有效性 oracle。沿用 v3 的固定提议方向

\[
u=\operatorname{vec}(\beta_t k_t e_t^\top),\qquad
Z=\|Ju\|_2^2,\qquad r\in\{0,1\}.
\]

允许 gate 为 `a(C)∈[0,1]`。提议方向 `u` 与其成本可在同一 stratum 内随更细的 `F_t` 信息变化；令随机成本 `Lambda=lambda||u||²`。对每个正概率 stratum 定义

\[
p_c=P(r=1\mid C=c),\quad
\mu_c=E[Z\mid C=c],\quad
m_c=E[rZ\mid C=c],\quad \nu_c=E[\Lambda\mid C=c],\quad 0\le Z\le U_c,
\]

以及 `A_c=mu_c+nu_c`。`Lambda` 必须非负、可积、动作前可测，并与 `Z` 使用相同的平方输出损失量纲；不能在看到未来结果后调节。若 `u` 在每个 stratum 内固定，才可把 `nu_c` 简写为 `lambda||u_c||²`。

## 2. 条件 sharp identification

逐层应用 v3 的 support argument 得

\[
\ell_c=\max\{0,\mu_c-(1-p_c)U_c\},\qquad
h_c=\min\{\mu_c,p_cU_c\},
\]

且 `m_c∈[ell_c,h_c]`。这些界只对“固定 `p_c,mu_c` 与 support、其余条件耦合任意”的声明模型 sharp；若 `U_c` 只是保守证书，或真实 Delta 的 `r,Z,J,u` 受额外结构约束，它们只是外界。对每个固定 `c`，只要条件概率空间允许在原子内随机化，端点由让 `r=1` 与高 `Z` 质量尽量错开或重合达到；不可分割的有限原子空间则应使用实际可行耦合集。

若完整 conditional `Z|C=c` 边际已知，`ell_c,h_c` 可替换为条件分位重排界

\[
\ell_c^Q=\int_0^{p_c}Q_{Z\mid c}(s)\,ds,\qquad
h_c^Q=\int_{1-p_c}^1Q_{Z\mid c}(s)\,ds.
\]

条件化没有消除不可识别性：v3 的相同边际、不同耦合反例可在任一 stratum 内原样构造。

## 3. 条件 minimax-regret 定理

声明的集成 surrogate 为

\[
\mathcal L(a;m)=E\!\left[A_Ca(C)^2+(1-2a(C))m_C\right].
\]

知道 `m_c` 时，`A_c>0` strata 的 oracle 为 `a_c^*=m_c/A_c`；`A_c=0` 时必有 `mu_c=m_c=nu_c=0`，约定 `a_c^*=0`。下文所有比值均按此分段定义，不把 `0/0` 与 indicator 相乘。

令歧义集为 **conditional rectangular**：给定 `C` 后，每个 stratum 的 admissible coupling 可在 `[ell_c,h_c]` 内独立选择，并且存在实现端点的可测条件核。假设 `A_C,ell_C,h_C` 可测且 `E[A_C]<infinity`。对有限 `C`，这是有限直积；对一般标准 Borel `C` 还需端点可测、可积支配与 measurable selection，本文不把后者无条件化。

相对知道 `m_C` 的 oracle，regret 为

\[
\mathcal R(a;m)=E\!\left[\rho_C(a,m_C)\right],\qquad
\rho_c(a,m)=
\begin{cases}
A_c(a-m/A_c)^2,&A_c>0,\\
0,&A_c=0.
\end{cases}
\]

在 rectangular 条件下，worst case 可逐层分离。每个 `A_c>0` stratum 的两端 Chebyshev-center 解为

\[
a_R(c)=\frac{\ell_c+h_c}{2A_c},
\]

而 `A_c=0` 取 `a_R(c)=0`。因为 `0<=h_c<=mu_c<=A_c`，该解自动落在 `[0,1]`。集成最坏 regret 为

\[
\sup_m\mathcal R(a_R;m)
=E\!\left[q_C\right],\qquad
q_c=
\begin{cases}
(h_c-\ell_c)^2/(4A_c),&A_c>0,\\
0,&A_c=0.
\end{cases}
\]

若 ambiguity set 含跨 stratum 的共同参数、总量约束或平滑耦合，`sup` 未必与期望交换；上述值只可作 rectangular 外包络的保守解，不能冒充原问题的 exact minimax。

## 4. 何时上下文恢复可认证写入

相对 contextual no-write，固定策略的 conditional difference 是

\[
\Delta_c(a;m_c)=A_ca(c)^2-2a(c)m_c.
\]

对 `a(c)>0`，它在该 stratum 对所有 admissible couplings 严格为负，当且仅当

\[
A_ca(c)<2\ell_c.
\]

因此某一 stratum 存在一致改进的正 gate，当且仅当 `ell_c>0`。这里及下文的“改进”都只指声明的集成二次 common-path surrogate，不推出自由运行未来损失、语义有效性或原生 endpoint 改进。在 rectangular ambiguity/envelope 下，整个策略相对全局 no-write 的最坏差为

\[
E[A_Ca(C)^2-2a(C)\ell_C].
\]

定义与 minimax-regret gate 明确不同的安全释放门

\[
a_S(c)=
\begin{cases}
\ell_c/A_c,&A_c>0,\\
0,&A_c=0.
\end{cases}
\]

它恰在 `ell_c>0` 时写入，并给出 conditional worst-case gain `-ell_c²/A_c<0`。又因 `0<=ell_c<=A_c`，有 `ell_c²/A_c<=A_c`；在前述 `E[A_C]<infinity` 下，只要 `P(ell_C>0)>0`，其集成 worst-case difference 就严格为负。若 `ell_C=0` 几乎处处，则任何在 `A_C>0` 集合上非零的 gate 之最坏差非负，不能认证严格改进（`A_C=0` 的 gate 仅与 no-write 等价）。注意 `a_R` 优化的是相对未知 oracle 的 regret；当 `ell_c=0<h_c` 时它一般仍为正，不能冒充 baseline-safe gate。

## 5. 池化为何会丢失合法证据

先取共同 support 上界 `U`。令 `p_bar=E[p_C]`、`mu_bar=E[mu_C]`。池化区间为

\[
\ell_{pool}=\max\{0,\mu_{bar}-(1-p_{bar})U\},\qquad
h_{pool}=\min\{\mu_{bar},p_{bar}U\}.
\]

由 `max(0,x)` 的凸性与 `min(x,y)` 的凹性，

\[
E[\ell_C]\ge \ell_{pool},\qquad E[h_C]\le h_{pool}.
\]

所以在同一个 conditional model 投影到 pooled observable 时，条件信息不会放宽 aggregate joint-moment bounds。若 `U_C` 随 context 变化，对应合法比较是

\[
E[\ell_C]\ge\max\{0,E\mu_C-E[(1-p_C)U_C]\},
\]

\[
E[h_C]\le\min\{E\mu_C,E[p_CU_C]\}.
\]

把右侧再换成只知道 `U_{max}` 的粗模型是在比较不同信息集，不能声称 strict sharpening。

显式例子：两个等概率 strata、`U=1`。取

\[
(p_1,\mu_1)=(0.9,0.9),\qquad (p_0,\mu_0)=(0.1,0.1).
\]

则 `ell_1=0.8`、`ell_0=0`；池化却有 `p_bar=mu_bar=0.5`、`ell_pool=0`。常数 gate 无法由 pooled marginals 认证，但 contextual 策略可直接取 `a(1)=ell_1/A_1<=1`、`a(0)=0`。旧反例没有被删除：它仍可发生在 `C=0`，并迫使安全门在该层 no-write。

## 6. 估计、信息、状态与计算成本

闭式 gate 本身每 stratum 为 `O(1)`，但 `p_c,mu_c,U_c` 不是免费 oracle：

- `p_c` 需要合法的 ideal-action/validity 监督或经审计代理；模型自评和自生成未来不是新外部证据。
- `mu_c` 与 `U_c` 需要动作前未来几何估计或证书；R03 类型 bound 可供 control，但保守性会把 `ell_c` 压回零。
- 细分 context 降低 identification ambiguity，却提高 estimation uncertainty。有限样本必须给 simultaneous confidence region，再对整个 region 优化；逐 bin 插件端点不提供覆盖保证。
- 连续/高维 `C` 需要预先规定函数类、cross-fitting/debiasing 或 regularized conditional LP；这些成本可能超过直接预测 joint value `m_c`。
- 当 `A_c` 很小时，population 比率虽因 `0<=h_c<=A_c` 不发散，插件估计仍可能极不稳定；置信集必须强制合法次序，或设定动作前 floor 并回退 no-write。
- 若 context 映射依赖写入后的状态、未来 token 或事后标签，就是数据泄漏，不是修复。

该构造不增加持久记忆矩阵维度，但需要保存/计算 context statistics 或一个条件预测器；真实总成本必须与同信息的 contextual predictor 对齐。

## 7. 最近工作、强简单对照与真实残余

| 对照/近邻 | 已覆盖 | R05 v4 仅剩内容 |
|---|---|---|
| D'Adamo, Orthogonal Policy Learning Under Ambiguity | 协变量条件的个体化 partial-ID policy、minimax 类准则、orthogonal estimation | Delta 固定方向 surrogate 的标量闭式 |
| Ben-Michael, conditional linear programs | 条件 LP bounds、debiased estimation、policy learning | Bernoulli-validity × bounded-sensitivity 的二变量解析特例 |
| Ji–Lei–Spector covariate-assisted bounds | 协变量可收紧 partial-ID bounds；模型无关推断 | 同上，无一般推断增量 |
| Kallus–Zhou robust policy improvement | 个体化 policy 与 baseline-safe minimax regret | 不同 ambiguity set 下的 Delta 命名特例 |
| contextual Bayes/joint predictor | 直接预测 `m_c` 或 action value | R05 只在 joint label 缺失时给保守区间 |
| no-write / pooled v3 | 零额外估计成本，最强安全 control | v4 的 `a_S` 只在 lawful context 使 `ell_c>0` 时释放；`a_R` 不保证 baseline safety |

因此必要数学交互是：`C` 同时改变 validity probability 与未来敏感度的 joint identified set，并据此改变 Delta gate；但这一交互已落入成熟的 covariate-conditioned partial identification / policy learning 范畴。当前没有证据表明该闭式带来同信息、同容量、同计算下的独立统计或计算优势。

## 8. 原生测量与可证伪预测

可由既有编辑任务测量的仍是 endpoint efficacy、paraphrase/generalization、locality、事件相关 QA、unknown 与连续编辑后下游退化。它们没有原生的 pre-action `C,p_c,mu_c,U_c,m_c`、随机化 propensity 或 paired write/no-write potential outcomes，因此不能直接验证 sharpness 或 minimax regret。

若未来获得合法记录，以下可证伪：

1. 在同一 stratum 固定 conditional marginals、只改变 `r-Z` 排序，oracle gate 会在 `[ell_c/A_c,h_c/A_c]` 内改变，R05 gate 不变。
2. pooled `ell_pool=0` 但某些 `ell_c>0` 时，`a_S` 可认证选择性写入；若所有 `ell_c=0`，`a_S` 退化为 no-write，而 `a_R` 仍可能为正且不安全。
3. context 越细不保证经验性能越好；若 simultaneous uncertainty 增长快于 identification width 缩小，robust gate 会更保守。
4. 若 direct contextual `m_c` predictor 在同信息/预算下校准更好，R05 没有实用优势。

## 9. 失败边界与处置

失败边界：non-rectangular cross-stratum ambiguity、不可测/泄漏 context、无效 `U_c`、ideal action 不在 `{0,u}`、动作改变未来分布导致共同路径 surrogate 失效、缺乏 simultaneous coverage、以及原生机制标签缺失。

本次修复保留了 v3 的 no-go，并把它精确缩到每个可见 context 内；它没有把“普遍不能保证”循环写成否定，也没有删除反例。数学若经独立复审成立，其贡献仍是 **useful conditional control theorem**。由于直接理论碰撞与 measurement gap，不分配 D 编号，不增加 active/admitted/selected 计数。attempt `3/3` 后该线 park；重开条件是出现 Delta-specific 的非矩形可解结构、合法 joint evidence，或同预算计算/统计优势证明。

