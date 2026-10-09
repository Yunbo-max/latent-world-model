# R05 v1：未知有效性与未来几何的部分识别 Delta 门

状态：**条件数学 control / versioned child；不是 D 候选；未执行实验**  
谱系：`STEP2_JOINT_CONDITIONAL_RISK.md` → 本文件。它修复的不是联合风险公式，而是该公式需要部署时不可得的 `validity × future geometry` 联合量。原文件、反例和审查保持不变。

## 1. 原问题、失败类型与保留结论

令一次 prefix 可见的 Delta 提议为

\[
U_t=\beta_t k_t e_t^\top,\qquad e_t=v_t-S_t^\top k_t,
\]

并记 `u=vec(U_t)`。旧 Step2 在线性化未来读出下使用

\[
G=\mathbb E[J^\top J\mid\mathcal F_t],\qquad
G_r=\mathbb E[rJ^\top J\mid\mathcal F_t],
\]

其中 `r∈{0,1}` 表示“这次提议在目标 horizon 仍应成立”。沿固定方向 `u` 的最优力度依赖

\[
m=u^\top G_r u=\mathbb E[r\|Ju\|_2^2\mid\mathcal F_t].
\]

失败类型是**假设不足/不可识别**，不是代数错误：仅有边际有效概率 `p=E[r|F_t]` 与平均未来敏感度 `mu=E[||Ju||²|F_t]` 时，一般不能恢复 `m`。保留的正确结论是：若 `G_r` 已知，联合条件矩而非 `pG` 决定最优写入力度；本修订给出 `G_r` 不可得时的锐利边界和稳健动作。

## 2. 信息、对象与明确假设

所有条件期望以下均对部署时 filtration `F_t` 条件化；公式省略该条件。

1. `u`、候选 gate `a∈[0,1]`、正则 `lambda>=0` 均为 `F_t` 可测；实际动作是 `aU_t`。
2. `J` 是从当前状态扰动到固定 horizon 未来读出的完整局部 Jacobian。若未来 token/query 随动作改变，`J` 只描述声明基准轨迹上的局部风险，不是自由运行总因果效果。
3. `Z=||Ju||²` 满足 `0<=Z<=U<∞`。`U` 必须是动作前可用的共同上界；它可来自显式 Jacobian/gain 证书，但不能事后读取真实未来。
4. `r∈{0,1}`，且理想动作被限制为二元族 `{0,u}`。这是假设，不代表真实最优更新必与 `u` 共线。
5. 已有历史/训练数据至多给出 `p=E[r]`、`mu=E[Z]`（或它们的可信区间）；部署时没有当前样本的 `r`、未来答案、旧知识有效性 oracle 或理想 edit 标签。
6. 风险是声明轨迹上的局部二次风险

\[
L(a;m)=\mathbb E[Z(a-r)^2]+\lambda\|u\|_2^2a^2.
\]

记 `lambda_u=lambda||u||²`、`A=mu+lambda_u`，并假设 `A>0`。退化情形 `A=0` 时所有声明方向损失均为零，gate 不可由该目标区分。

## 3. 连续推导一：联合量为何不能由边际 gate 恢复

展开 `r²=r`：

\[
L(a;m)=Aa^2+(1-2a)m.
\]

若 `m` 已知，平方完成给

\[
L(a;m)=A\left(a-\frac mA\right)^2+m-\frac{m^2}{A},
\qquad a^*(m)=\frac mA.
\]

因为 `0<=m<=mu<=A`，约束 `a∈[0,1]` 不截断该解。独立/因子化近似把 `m` 换成 `p mu`，因此 `a_sep=p mu/A`；它只有在 `E[rZ]=E[r]E[Z]` 或恰好满足同一方向矩条件时才正确。

仅知 `p,mu` 和 `0<=Z<=U` 时，令 `X=Z/U`（`U>0`），则 `E[X]=q=mu/U`。Fréchet/support 约束给出

\[
m_- = \max\{0,\mu-(1-p)U\},\qquad
m_+ = \min\{\mu,pU\}.
\]

证明直接来自

\[
0\le rZ\le Z,\quad rZ\le rU,
\quad (1-r)Z\le(1-r)U.
\]

这些界对“只固定 `p,mu,U`”是锐利的：令 `Z` 只取 `{0,U}`、`P(Z=U)=mu/U`，再把 `r=1` 的质量尽量与 `Z=U` 重合或错开，分别达到上、下界。

### 最小同边际反例

取 `p=1/2`，且 `Z∈{0,U}` 各半。两个世界有完全相同的 `r` 边际和 `Z` 边际：

- 世界 A：`r=1` 当且仅当 `Z=U`，所以 `m=U/2`；
- 世界 B：`r=1` 当且仅当 `Z=0`，所以 `m=0`。

但两者最优 gate 分别为

\[
a_A^*=\frac{U/2}{U/2+\lambda_u},\qquad a_B^*=0.
\]

因此任何只读 `p` 与 `Z` 边际的算法，在这两个世界输入相同却需要不同动作；额外 checksum、模型自评或自生成未来不会自动增加外部识别信息。

若 `Z` 的完整边际分布已知，令 `Q_Z(s)` 为其广义分位函数，则重排不等式把区间收紧为

\[
m_-^{Q}=\int_0^p Q_Z(s)\,ds,
\qquad
m_+^{Q}=\int_{1-p}^1 Q_Z(s)\,ds,
\]

含原子时用广义分位积分。它仍不点识别 `m`，除非区间塌缩或再加入可检验的耦合假设。

## 4. 连续推导二：可计算的 minimax-regret gate

相对知道真实耦合 `m` 的 oracle，regret 为

\[
\operatorname{Reg}(a;m)
=L(a;m)-L(a^*(m);m)
=A\left(a-\frac mA\right)^2.
\]

对识别集 `m∈[m_-,m_+]`，最坏点必在端点；两端等距给唯一的 minimax-regret gate

\[
a_R=\frac{m_-+m_+}{2A},
\qquad
\sup_m\operatorname{Reg}(a_R;m)
=\frac{(m_+-m_-)^2}{4A}.
\]

因子化 gate 的最坏 regret 是

\[
\sup_m\operatorname{Reg}(a_{sep};m)
=\frac{\max\{(p\mu-m_-)^2,(m_+-p\mu)^2\}}{A}.
\]

它仅当 `p mu=(m_-+m_+)/2` 时等于 minimax-regret 解。这个构造没有创造新的有效性证据；它只对同一不完整信息做保守决策。

## 5. 连续推导三：何时能证明“写一点比不写好”

与 `a=0` 比较：

\[
L(a;m)-L(0;m)=Aa^2-2am.
\]

因此对任意固定 `a>0`，它对所有 admissible coupling 都严格改善当且仅当

\[
Aa<2m_-.
\]

于是存在某个严格正、统一有益的 gate 当且仅当 `m_->0`。若 `m_-=0`，边际信息允许一个世界令有效性只落在零敏感度样本上；此时任何正写入都不能由这些边际信息认证为优于 no-write。这是本修订最重要的可证伪边界。

若 `p∈[p_L,p_U]`、`mu∈[mu_L,mu_U]` 且 `U` 固定，一个保守外包络为

\[
\underline m=\max\{0,\mu_L-(1-p_L)U\},
\qquad
\overline m=\min\{\mu_U,p_U U\}.
\]

它只有在端点组合与共同数据生成约束相容时才锐利；否则应直接对联合置信集合优化，不能把分别估计的区间冒充精确识别集。

## 6. 矩阵版的必要界，而非伪造完整解

若 `H=J^T J` 且动作前已知 `0≼H≼L I`，则

\[
0\preceq G_r\preceq G,
\qquad G_r\preceq pL I,
\qquad G_r\succeq G-(1-p)L I.
\]

前两式来自 `rH≼H` 与 `rH≼rLI`；末式来自 `(1-r)H≼(1-r)LI`。对每个固定方向 `u`，它们退化为上面的锐利标量界。**不能**把所有方向各自可达的端点拼成一个同时可达的矩阵 `G_r`；没有额外交换性/共同特征基/分布结构时，上述 Loewner 关系只是必要条件。

## 7. 旧反例复查与本次 patch 的真实作用

- `REVISION_EVIDENCE_POSTERIOR_EDIT.md` 的 Bayes gate 仍可作为 `p` 估计器，但若不估计 `r` 与未来几何的耦合，它只给 `a_sep`，不能恢复 `a^*(m)`。
- `MARTINGALE_RELEASE_CONTROL.md` 的 e-process 可控制误释放概率，但两个观测同分布世界仍有相同 stopping law；本修订不删除该不可识别反例。
- `CHECKSUM_REVISION_SKETCH.md` 的 data-processing no-go 保持：压缩状态不提供新外部证据。
- `STEP2_JOINT_CONDITIONAL_RISK.md` 的联合矩最优式保持；本修订把“联合矩未知”从一句限制变成锐利标量识别区间、regret 与 no-write 边界。
- R03 v2 的有限时域 gain/tube 证书至多帮助形成动作前 `U`；它不提供 `r`，也不识别耦合 `m`。

## 8. 区别性预测、反证与失败边界

1. 在相同 `p,mu,U` 下，只改变 `r` 与 `Z` 的排序，factorized gate 的行为不变，但 oracle gate 可在整个 `[m_-/A,m_+/A]` 移动。
2. 当 `mu>(1-p)U` 时 `m_->0`，存在统一优于 no-write 的小 gate；当 `mu<=(1-p)U` 时，任何正 gate 都不能仅由边际量统一认证。
3. 获得更紧的 `Z` 分布只会把 quantile 识别区间缩小；若仍有宽度，则单纯增加几何精度不能替代 validity–geometry 联合证据。
4. 若后续真实数据发现 `r` 与 `Z` 近条件独立，则 `p mu` 可作为经验近似；这会支持简单 Bayes gate，而不是证明本控制有增益。
5. 若真实理想动作不在 `{0,u}`、局部 Jacobian 失真、`U` 不是事前共同上界、或写入改变未来分布，则本风险与证书不适用。

## 9. 强简单替代与判别比较

| 对照 | 同信息下能做什么 | 本修订必须多证明什么才有价值 |
|---|---|---|
| no-write | 当 `m_-=0` 时是唯一可统一认证的不损伤动作 | 找到 `m_->0` 或额外联合证据 |
| factorized Bayes gate | 使用 `p mu`，便宜但隐含条件独立 | 用耦合变化显示其 regret 明显大于 `a_R` |
| 直接联合预测器 | 从历史真实反馈预测 `m` 或动作收益 | 同信息、同容量下比稳健区间更准/更便宜 |
| 普通未来 CE / action predictor | 直接学后续损失或更新动作 | 证明 partial-ID 控制改善校准或安全，而非只加保守性 |
| hard projection / soft preconditioner | 在指定保护几何下限制干扰 | 它们不识别是否该释放；本控制也不替代它们 |
| robust Bayes / moment-DRO | 对歧义集做 minimax 或 regret | 这是本构造的主要已知机制；不能计作原创算法 |

## 10. 复杂度、状态与信息成本

一旦 `p,mu,U,lambda_u` 可用，标量界与 `a_R` 是 `O(1)` 状态/计算。真实成本在获得它们：

- `p` 需要外部可核实的 validity 监督或可辩护的历史代理；模型自评不是新证据。
- `mu` 或 `Z` 分布需要未来读出几何的训练期样本、JVP/VJP、critic 或 gain proxy。
- `U` 需要部署前、对 admissible future tube 同时成立的上界；事后最大值有泄漏。
- 矩阵动作或多方向 joint update 会回到估计 `G_r`/完整 action predictor 的成本。

因此目前没有证明相对普通 CE、直接 action predictor 或 robust decision baseline 的同预算优势。

## 11. 原生测量可行性

CounterFact/ROME 原生 scorer 提供 edit efficacy、paraphrase 与 neighborhood 行为；EvEdit 提供事件、旧/新/推理/未知问答；连续编辑工作还测 edit 成功与周期性 downstream accuracy。它们可看最终行为，却不原生记录每次 Delta 写入的 `r`、`J`、`Z`、`p`、propensity 或两个潜在动作结果。因此：

- “边际相同但耦合不同导致不同最优 gate”是可构造的数学反例，不是现有 native benchmark 的直接指标；
- endpoint retention/locality 可作为外部结果，但不能反演 `m` 或证明机制；
- 本阶段不造新标签、case、metric 或 scorer，measurement gap 保留。

## 12. 处置

本修订完成一次有界 repair：数学上把联合标签缺失转为 sharp scalar partial-identification interval、minimax-regret gate 和 uniformly-beneficial-write 边界。它没有解决语义 validity 的来源，且主要决策机制与 partial identification、Gamma-minimax regret 和 moment-DRO 直接相邻。故状态为 **review pending control/conditional theory**；不分配 D 编号，不增加活动/准入/选择计数，实际效果未知。

