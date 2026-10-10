# R06 v1：敏感度加权的选择性真实性审计

状态：**数学成立的两阶段审计 control；不是 D 候选；未执行实验**  
谱系父项：`R05_PARTIALLY_IDENTIFIED_VALIDITY_GEOMETRY.v3.md`，SHA256 `c8911d5910f96f73e4c7320827a048f57d33f2c2c00c0c2cbd7d172687d9325c`。  
修复目标：R05 只有边际信息，`m=E[rZ]` 仅部分识别。本修订问：在固定外部审计预算下，哪些额外真实标签能合法缩小该缺口；不把事实标签偷换成理想动作标签，也不使用写入时不可见的未来量。

## 1. 原问题、patch 与严格语义

R05 的 `r∈{0,1}` 是声明二元动作族 `{no-write, full-write}` 中的**理想动作标签**。普通事实审计通常只返回

\[
Y_t\in\{0,1\},
\]

表示新陈述为真或旧陈述仍有效。一般 `Y_t≠r_t`：即使新事实为真，完整写入也可能因 key 冲突、保护损伤或容量代价而不如 no-write。反之，若审计能直接给出 `r_t`，它已近似知道两个动作的反事实未来效用，不再是普通事实核验。

因此本修订首先估计

\[
m_Y=\mathbb E[YZ^0],
\]

而不是无条件声称识别 `m_r=E[rZ]`。其中 `Z_t^0∈[0,U]` 是预先声明、动作无关的冻结轨迹局部敏感度；例如在合法固定后缀/基准轨迹上

\[
Z_t^0=\|J_tu_t\|_2^2,
\qquad
u_t=\operatorname{vec}(\beta_t k_te_t^\top).
\]

若 `J_t` 依赖未来 token/query，则 `Z_t^0` 不是写入时 prefix 可测量对象，只能事后用于两阶段抽审，或由 prefix-only 代理 `\widetilde Z_t` 决定审计概率。模型自生成未来只是一种代理，不是外部真实性证据。

## 2. 可预测审计设计与点识别

令 `G_t` 为选择当前审计时已经可见的信息，`A_t∈{0,1}` 为是否请求昂贵外部标签，

\[
\pi_t=P(A_t=1\mid\mathcal G_t),
\qquad \pi_t\ge\epsilon>0.
\]

`pi_t` 必须在看到当前 `Y_t` 前确定并记录。若 `Z_t^0∉G_t`，要求

\[
A_t\perp (Y_t,Z_t^0)\mid\mathcal G_t;
\]

若 horizon 结束后已算出动作无关 `Z_t^0` 再抽审，可把 `Z_t^0` 纳入 `G_t`，只要求 `A_t⊥Y_t|G_t`。过去已经返回的审计结果可进入未来 `G_t`，但 `pi_t` 必须对选择时 filtration 可预测。

对有限日志目标

\[
m_{Y,T}=\frac1T\sum_{t=1}^T Y_tZ_t^0,
\]

Horvitz--Thompson 估计为

\[
\widehat m_{\rm HT}
=\frac1T\sum_{t=1}^T\frac{A_tY_tZ_t^0}{\pi_t}.
\]

条件于全部潜在 `(Y_t,Z_t^0)`，有

\[
\mathbb E_A[\widehat m_{\rm HT}]=m_{Y,T}.
\]

这只点识别该段日志的总体平均联合矩，不识别单例标签、条件门、个体反事实或新部署分布下的自由运行总效应。

## 3. 增广估计与设计方差

令 `q_t∈[0,1]` 是只依赖审计前信息和过去已返回标签的可预测真实性模型。则

\[
\widehat m_{\rm AIPW}
=\frac1T\sum_t Z_t^0
\left[q_t+\frac{A_t}{\pi_t}(Y_t-q_t)\right]
\]

在真实随机化 propensity 正确记录时对任意 `q_t` 设计无偏。离线拟合 `q` 需 sample splitting/cross-fitting；若 `Z` 也只在审计后可见，应直接对 `Y_tZ_t^0` 做 outcome regression，而不能把不可见的 `Z` 填入当时的 acquisition rule。

非适应、固定 `pi_t,q_t` 的独立 Bernoulli 审计下，条件设计方差为

\[
\operatorname{Var}_A(\widehat m_{\rm HT})
=\frac1{T^2}\sum_t
\left(\frac1{\pi_t}-1\right)(Y_tZ_t^0)^2,
\]

\[
\operatorname{Var}_A(\widehat m_{\rm AIPW})
=\frac1{T^2}\sum_t
\left(\frac1{\pi_t}-1\right)(Z_t^0)^2(Y_t-q_t)^2.
\]

因此 AIPW 不自动优于 HT；只有 residual prediction 足够好时才降方差。适应性可预测的 `pi_t,q_t` 下，对应的逐项和是 martingale predictable quadratic variation，无条件方差是其期望；iid 标准误无效，应使用 martingale CLT/Freedman 或 anytime-valid confidence sequence。

## 4. 固定预算下的最优审计概率

令审计成本 `c(X)>0`、期望预算 `E[c(X)pi(X)]≤b`、`epsilon≤pi≤1`。最小化重要性方差项

\[
\mathbb E\frac{a(X)}{\pi(X)}
\]

的 KKT 解为

\[
\pi^*(X)=\operatorname{clip}_{[\epsilon,1]}
\sqrt{\frac{a(X)}{\eta c(X)}}.
\]

若审计前已知 `Z^0` 且 `q(X)=P(Y=1|X)`，则

\[
a_{\rm HT}(X)=(Z^0)^2q(X),
\qquad
\pi^*_{\rm HT}\propto \frac{Z^0\sqrt q}{\sqrt c}.
\]

对正确 outcome regression 的 AIPW，

\[
a_{\rm AIPW}(X)=(Z^0)^2q(X)(1-q(X)),
\qquad
\pi^*_{\rm AIPW}\propto
\frac{Z^0\sqrt{q(1-q)}}{\sqrt c}.
\]

若完全不信任 `q`，取中心 `q_0=1/2` 的稳健 residual 上界得到 `pi∝Z^0/sqrt(c)`。因此“只按 Delta 敏感度审计”仅是额外条件下的稳健/近似分配，不是一般 oracle。固定恰好 `B` 个样本还需 PPS/rejective sampling 与二阶 inclusion probabilities；不能沿用独立 Bernoulli 方差式。

在单位成本、稳健中心 `q_0=1/2`，并且 `0<rho Z/E[Z]<=1` 对目标支持 `{Z>0}` 几乎处处成立时，可为这个示例放松统一 `epsilon` floor、只保留目标支持上的 positivity，并取无 clipping 的 `pi=rho Z/E[Z]`。它把重要性二阶矩从

\[
\frac{\mathbb E[Z^2]}{4\rho}
\quad\text{降至}\quad
\frac{(\mathbb E Z)^2}{4\rho},
\]

差为 `Var(Z)/(4rho)`。这只有在 `Z` 异质且合法可见时产生结构收益；`Z` 近常数时退化为均匀审计。该闭式是 Neyman/importance allocation 的 Delta 特例。

## 5. positivity、延迟与审计反馈

若某个 `Z^0>0` 区域的 `pi=0`，则该区域 `Y=0` 与 `Y=1` 两个世界观测等价而 `m_Y` 不同，故不可点识别。对全部 `T` 事件要求统一 `pi_t≥epsilon` 且期望审计数不超过 `B`，必要条件为

\[
B\ge T\epsilon.
\]

所以无限流上的“固定少量审计 + 全局固定 positivity floor”不能同时成立。还需二阶可积性 `E[(YZ)^2/pi]<∞`；确定性 top-B 敏感度审计会令其余样本 propensity 为零。

若审计标签延迟返回且截止时完成指示为 `C_t`、可审计完成概率为 `gamma_t`，在条件独立 censoring 下可使用联合权重 `1/(pi_t gamma_t)`。若返回速度在给定可见信息后仍依赖未知 `Y_t`，固定截止估计一般有偏。

若返回标签立即改变 updater 与未来 query/action 分布，估计对象变成 audit-feedback policy。要评估无审计策略，必须 firewall 标签直到评估窗口结束，或使用完整顺序 DR/OPE；单步 HT/AIPW 不能修复轨迹分布变化。

## 6. 从事实审计到 no-write 认证还缺 bridge

R05 的风险差是

\[
\Delta(a;m_r)=Aa^2-2am_r,
\qquad A=\mu+\lambda\|u\|^2.
\]

只有在额外、可检查的 bridge 假设下，事实标签才可代替理想动作标签。例如若能证明 `r=Y`，且在联合置信事件上 `0<L_m≤m_r≤A≤U_A`（故 `U_A>0`），则任意

\[
0<a<\frac{2L_m}{U_A}
\]

可在联合置信事件上认证声明 surrogate 优于 no-write；稳健选择可取

\[
a_{\rm cert}=\min\left\{1,\frac{L_m}{U_A}\right\}.
\]

若 `L_m=0`，只表示审计不足以认证正写入，不证明写入无益。更重要的是，普通真值审计本身不提供 `r=Y`。

最小语义反例：新事实为真 (`Y=1`)，但其 key 与仍有效旧事实重叠，完整写入的保护/容量损伤大于新事实收益，于是理想动作仍为 no-write (`r=0`)。

即使 `m_Y` 被精确识别，也不能推出自由运行总效应。取 `u=J=Z=Y=1`，两个世界

\[
L_A(a)=(a-1)^2,
\qquad
L_B(a)=(a-1)^2+2a^2
\]

有相同 `Y,Z,m_Y`；完整写入相对 no-write 在 A 中改善 `-1`，在 B 中损伤 `+1`。差异来自动作诱导的长期代价，局部真实性加权敏感度不识别它。

## 7. 旧反例复查、预测与反证

- R05 的部分识别反例仍成立于没有真实审计的区域；R06 仅在合法 positivity 覆盖范围内加入联合证据。
- 若审计机制偷看当前标签，记录一个伪 propensity 不能修偏。例：`Y~Bernoulli(1/2), Z=1, A=Y`，错误记录 `pi=1/2` 得 `E[AYZ/pi]=1`，而 `E[YZ]=1/2`。
- 用完整未来 `Z` 指导当下写入或当下 acquisition 属于泄漏；合法在线版本只能用 `widetilde Z`，其效率界另证。
- 坏 `q` 不破坏正确随机化下 AIPW 的设计无偏，却可能使方差高于 HT。
- 未知 label sensitivity/specificity 时识别的是 noisy-label moment，而非真实 `m_Y`。
- 最坏情形均值标准误仍是 `O(U/sqrt(B))`；没有 bridge 或结构假设，Delta 形式不突破真实标签数下界。

可证伪预测：在同一标签预算下，合法 `Z` 异质且与 residual influence 对齐时，敏感度加权审计应比均匀审计降低 `m_Y` 方差；`Z` 近常数、proxy 失配或真实性几乎确定时，优势消失或 AIPW/均匀设计更强。

## 8. 同信息强对照、成本与原生测量

必须比较：均匀审计+HT、均匀审计+AIPW、通用 Neyman/influence allocation、直接 plug-in `T^{-1}sum Zq`、R05 Fréchet 下界、no-write/fixed Delta；长期策略问题须用顺序 DR/OPE。

HT/AIPW 每步计算 `O(1)`，统计量可流式维护；主要成本是 `B` 个外部标签与可靠 `Z`/proxy。若 `Z` 需要完整 Jacobian，其代价可能远高于审计估计本身。现有 ROME/CounterFact、EvEdit、EasyEdit、连续编辑与 SEAL 可测行为终点，但不原生联合提供外部 grounded `Y`、Delta `Z`、随机审计 `pi` 或 paired action outcomes。本阶段不新造标签、协议、metric、case 或结果。

## 9. 处置与重开条件

数学修复成立：少量真实审计把 R05 的“完全没有联合证据”改成对 `E[YZ^0]` 的设计型点估计，并给出正确的 residual-aware audit allocation、positivity/延迟边界与条件 no-write 认证接口。

但 HT/AIPW、Neyman/PPS、two-phase validation、active testing 和适应性推断已覆盖主体机制；Delta 目前只提供 acquisition score 的具体形式。状态为 **mathematically valid two-phase audit control; mechanism collision; park after v1**。不分配 D 编号，不增加活动/准入/选择计数，实际效果未知。

只有出现至少一项实质新证据才重开：`Y→r` 的可检查 Delta bridge theorem；真正 prefix-only 的 `widetilde Z` 对 full-horizon `Z` 的效率/regret 界和严格低成本优势；完整耦合状态下顺序 DR/OPE 的 Delta 充分状态/方差优势；或真实原生审计来源、已记录 propensity 与动作无关 `Z^0` 的可测量闭环。
