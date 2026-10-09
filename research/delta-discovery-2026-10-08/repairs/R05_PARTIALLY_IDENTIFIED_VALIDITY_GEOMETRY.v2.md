# R05 v2：未知有效性与未来几何的部分识别 Delta 门

状态：**条件数学 control / versioned child；不是 D 候选；未执行实验**  
直接父项：`R05_PARTIALLY_IDENTIFIED_VALIDITY_GEOMETRY.v1.md`，SHA256 `ce124a8bbe131f12c697f23ba0755650a18d72fbfe17d674a908b447a2bb602e`。  
修订原因：独立审查接受标量主定理，但要求限定矩阵 sharpness、显式处理 `U=0`、消除 Delta 时间索引歧义，并把“有益”严格限制到声明的局部正则 surrogate。v1 原字节保留。

## 1. 修订后的 formal object

令 `S_t^-` 明确表示当前动作前的 prefix state，

\[
e_t=v_t-(S_t^-)^\top k_t,
\qquad U_t=\beta_t k_t e_t^\top,
\qquad u=\operatorname{vec}(U_t).
\]

若项目递推把写入前状态记为 `S_{t-1}`，则上式等价地使用 `e_t=v_t-S_{t-1}^T k_t`。所有对象均对部署时 filtration `F_t` 条件化：`u`、gate `a∈[0,1]` 与 `lambda>=0` 为 `F_t` 可测；当前没有未来 token、任务答案、有效性 oracle 或理想 edit 标签。

在固定 horizon 的声明基准轨迹上，令 `J` 为完整局部状态—输出 Jacobian，

\[
Z=\|Ju\|_2^2,qquad 0\le Z\le U,qquad
r\in\{0,1\}.
\]

`r=1` 表示该二元理想动作族选择完整提议 `u`，`r=0` 表示 no-write；真实理想动作不在 `{0,u}` 时本模型失配。定义

\[
p=\mathbb E[r],\quad \mu=\mathbb E[Z],\quad
m=\mathbb E[rZ],\quad
\lambda_u=\lambda\|u\|_2^2,quad A=\mu+\lambda_u.
\]

声明的局部正则二次 surrogate 为

\[
L(a;m)=\mathbb E[Z(a-r)^2]+\lambda_u a^2.
\]

若写入改变未来输入分布、线性化失效或 `U` 不是动作前共同上界，本文件不声称真实自由运行损失被控制。

## 2. 已知 joint moment 时的 oracle

由 `r²=r`，

\[
L(a;m)=Aa^2+(1-2a)m
=A\left(a-\frac mA\right)^2+m-\frac{m^2}{A}.
\]

在 `A>0` 时，`0<=m<=mu<=A`，故约束内唯一 oracle 为

\[
a^*(m)=m/A.
\]

把 `m` 因子化成 `p mu` 得 `a_sep=p mu/A`；它额外假定 `r` 与方向未来敏感度 `Z` 条件独立，或至少 `E[rZ]=p mu`。

## 3. 只知道边际时的锐利标量识别集

先处理退化情形：若 `U=0`，则 `Z=mu=m=0`。当 `lambda_u>0` 时唯一 minimax-regret gate 为 `a_R=0`；若 `lambda_u=0`，surrogate 对所有 `a` 相同，取 `a_R=0` 作为 no-write 约定。以下归一化与非退化 sharpness 构造假设 `U>0`。

仅知 `p,mu,U` 时，support 约束给

\[
m_- = \max\{0,\mu-(1-p)U\},\qquad
m_+ = \min\{\mu,pU\}.
\]

上界来自 `rZ<=Z` 与 `rZ<=rU`；下界来自 `(1-r)Z<=(1-r)U`。锐利性可由 `Z∈{0,U}`、`P(Z=U)=mu/U` 并让 `r=1` 的质量与 `Z=U` 尽量重合或错开达到。

最小不可识别反例取 `p=1/2` 且 `Z∈{0,U}` 各半。若 `r=1` 恰落在 `Z=U`，则 `m=U/2`；若恰落在 `Z=0`，则 `m=0`。两世界的 `r`、`Z` 边际相同，oracle gate 却分别为

\[
\frac{U/2}{U/2+\lambda_u}
\quad\text{与}\quad 0.
\]

故 checksum、模型自评或自生成未来若不带来新的外部联合证据，不能点识别 gate。

若 `Z` 的完整边际分布已知、`Q_Z` 为广义分位函数，则在所有具有给定边际的联合耦合中，

\[
m_-^Q=\int_0^p Q_Z(s)\,ds,
\qquad
m_+^Q=\int_{1-p}^1 Q_Z(s)\,ds.
\]

含原子时允许在原子内部条件随机化。对不可分割的固定有限样本空间，端点未必精确可达；此时应使用其实际可行耦合集。

## 4. 可计算的 minimax-regret gate

相对知道真实 `m` 的 oracle，

\[
\operatorname{Reg}(a;m)
=L(a;m)-\min_b L(b;m)
=A\left(a-\frac mA\right)^2.
\]

因此对 `m∈[m_-,m_+]`，唯一 minimax-regret gate 与最坏 regret 为

\[
a_R=\frac{m_-+m_+}{2A},
\qquad
\sup_m\operatorname{Reg}(a_R;m)
=\frac{(m_+-m_-)^2}{4A}.
\]

因子化 gate 的最坏 regret 是

\[
\frac{\max\{(p\mu-m_-)^2,(m_+-p\mu)^2\}}{A},
\]

且仅当 `p mu=(m_-+m_+)/2` 时是 minimax-regret 解。

## 5. 对声明 surrogate 的 no-write 认证边界

相对 no-write，

\[
L(a;m)-L(0;m)=Aa^2-2am.
\]

对固定 `a>0`，它对识别集中每个 admissible coupling 的**声明局部正则 surrogate** 都严格优于 no-write，当且仅当

\[
Aa<2m_-.
\]

因此存在某个可统一认证的正 gate 当且仅当 `m_->0`。若 `m_-=0`，不能仅凭这些边际证据认证任何正 gate 优于 no-write。这里“优于”包含正则项，不能外推为真实自由运行任务损失必然改善。

若仅有 `p∈[p_L,p_U]`、`mu∈[mu_L,mu_U]` 且 `U` 固定，一个保守外包络是

\[
\underline m=\max\{0,\mu_L-(1-p_L)U\},
\qquad
\overline m=\min\{\mu_U,p_U U\}.
\]

端点组合若不满足共同数据生成约束，该外包络不锐利；应直接对联合置信集合优化。

## 6. 矩阵必要界与 sharpness 限定

若 `H=J^T J` 且动作前有 `0≼H≼L I`，则

\[
0\preceq G_r\preceq G,
\qquad G_r\preceq pL I,
\qquad G_r\succeq G-(1-p)L I,
\]

其中 `G=E[H]`、`G_r=E[rH]`。这些均为必要 Loewner 界。

对固定方向 `u`，若只保留 `p`、`mu=u^TGu` 与 `U=L||u||²`，这些必要界投影为前述锐利标量界。若同时固定完整矩阵 `G` 或其他方向的矩，标量端点未必仍可达；不同方向的端点也一般不能由同一个联合分布同时达到。故本文件不把方向wise sharpness 拼成一个完整矩阵识别定理。

## 7. 旧反例复查、必要交互与未修复部分

- `STEP2_JOINT_CONDITIONAL_RISK.md` 的 joint-moment oracle 保持；本修订只在固定提议方向上处理 joint moment 不可得。
- `REVISION_EVIDENCE_POSTERIOR_EDIT.md` 的 Bayes gate 可估计 `p`，但不估计 `r-Z` 耦合时只得到 factorized gate。
- `MARTINGALE_RELEASE_CONTROL.md` 的 e-process 可控误释放，却不能区分观测同分布、耦合不同的两个世界。
- `CHECKSUM_REVISION_SKETCH.md` 的 data-processing no-go 保持。
- R03 v2 的 finite-horizon gain/tube 证书至多帮助给出合法 `U`；它不提供 `r`，也不识别 `m`。

修复后仍缺：语义 validity 的外部证据、自由运行 total effect、一般多方向 ideal edit、同预算优于直接 joint predictor/未来 CE 的计算或统计结果。

## 8. 可证伪预测与失败边界

1. 固定 `p,mu,U`，只改变 `r` 与 `Z` 的排序，factorized gate 不变，oracle gate 可在 `[m_-/A,m_+/A]` 移动。
2. `mu>(1-p)U` 等价于 `m_->0`，此时存在对声明 surrogate 统一优于 no-write 的小 gate；否则无此认证。
3. 知道完整 `Z` 边际只能把识别区间缩到 quantile bounds；除非区间塌缩或加入可检验耦合假设，仍不能点识别。
4. 若真实数据支持条件独立，简单 Bayes gate 会被支持；这不会证明 R05 有额外实效。
5. 若 ideal action 不在 `{0,u}`、`J`/未来分布随动作强变、或 `U` 事后取得，则结论失效。

## 9. 强简单对照、成本与原生测量

| 对照 | 同信息结论 | R05 尚需证明 |
|---|---|---|
| no-write | `m_-=0` 时唯一可统一认证的不写动作 | 新联合证据使 `m_->0` |
| factorized Bayes gate | 便宜，但隐含 `E[rZ]=p mu` | 耦合不确定性下显著 regret 差 |
| joint predictor / ordinary future CE | 直接预测 `m`、loss 或 action | 同信息同容量下的校准/成本优势 |
| hard projection / soft preconditioner | 约束已知保护几何 | 不识别该不该释放；R05 也不替代它 |
| robust Bayes / moment-DRO | 已覆盖 ambiguity-set 决策 | R05 仅是 Delta 标量特例/边界 |

一旦 `p,mu,U,lambda_u` 可用，区间与 gate 是 `O(1)`；主要成本在外部 validity 监督、未来几何/JVP/VJP/critic 与动作前共同上界。矩阵动作会回到估计 `G_r` 或完整 action predictor 的成本，因此没有同预算优势证明。

CounterFact/ROME、EvEdit、EasyEdit 与连续编辑工作可测 efficacy、paraphrase、locality、event reasoning、unknown 回答和下游退化，却不原生记录每次 Delta 写入的 `r,J,Z,p`、propensity 或两个潜在动作结果。本阶段不造新标签、metric、case 或结果；mechanism measurement gap 保留。

## 10. 处置

v2 完成第一次实质修订：保留 v1 的正确标量结论，修复矩阵 sharpness、退化情形、状态索引和效益语义。主要机制仍与 partial identification、Gamma-minimax regret、Fréchet coupling 与 moment-DRO 直接相邻；数学成立不等于原创方法或实效。状态为 **final-byte re-review pending conditional control**；不分配 D 编号，不增加活动/准入/选择计数，实际效果未知。

