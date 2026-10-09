# R03 v2 — 耦合时域的 Delta 保护能量与安全日志边界

状态：R03 v1 的第二次实质数学修订；条件安全控制/理论边界，不是实验结果、RSI 证明或自动准入的新 D 候选。

## 1. 原问题 → 具体 patch

R03 v1 已经正确解决两个局部问题：一次 rank-one Delta 写入对指定保护查询的冻结 readout 位移有精确闭式；把该位移上界放进 propensity 设计后，可以显式看见安全预算与 causal positivity 的不可行边界。它没有解决长期主张。v1 自己已经指出：后续 key、query、gate、updater state 或 token trajectory 会依赖本次写入，单步 `d_a` 可能与未来损伤无关。

失败类型不是 v1 代数错误，而是**目标/证书错配**：局部 frozen-readout certificate 被要求承担完整 coupled-state horizon safety。v2 的 patch 是：

1. 把 memory 与更新器内部状态放进同一个状态 `h=(x,z)`；
2. 把 rank-one Delta 写入当作时刻 `t` 的结构化状态注入；
3. 用后续完整联合 map 的增量增益，而不是只用冻结 Delta 左因子，传播该注入；
4. 得到有限时域保护输出能量的可计算上界，再把这个上界代回 v1 的安全 logging 约束。

这是一条必要的数学交互：propensity 下界强制危险动作以正概率发生，而其可允许概率取决于**完整闭环传播后的损伤能量**，不再只取决于当前 `k^T G_p k`。若增量增益不能在决策前合法上界，则 patch 不成立；不能用一次局部 Jacobian 或训练后未来 token 回填部署时证书。

## 2. Formal object、信息过滤与两种效果

令 `x=vec(S)`，`z` 包含所有能改变后续更新的 updater 参数/动量/统计/反馈队列，`h=(x,z)`。在决策前历史 `F_t` 下，动作 `a` 产生

\[
 h_{t+1}^a=F_t(h_t;\xi_t,a),\qquad
 h_{j+1}^a=F_j(h_j^a;\xi_j),\quad j>t,
\]

其中 `xi_j` 表示共同的外生输入路径。部署动作必须 `F_t`-可测；未来真实 token、答案、旧事实有效性标签或理想 edit 不在 `F_t` 内。

以下证书首先比较**同一外生路径**下的两个状态轨迹。它不自动等于自由运行 potential outcome：若动作改变以后采样 token、用户输入、检索结果或 feedback law，则总效果还含分布变化，必须继续使用 R02 的随机化/顺序 OPE 条件，或一个可信的环境模型。把两者混成一个 Jacobian 是错误的。

以 no-write `a=0` 为基准，定义即时注入

\[
 \eta_a=h_{t+1}^a-h_{t+1}^0=(\eta_{x,a},\eta_{z,a}).
\]

若动作只缩放 post-decay Delta 写入且不即时改 `z`，则

\[
 \eta_{x,a}=\operatorname{vec}(\alpha_a\beta k e^\top),\qquad
 \eta_{z,a}=0,qquad e=v-\bar S^\top k,
\]

所以在 Euclidean/Frobenius 范数下

\[
 \|\eta_a\|^2=\alpha_a^2\beta^2\|k\|^2\|e\|^2.
\]

若 logging、gate state 或在线更新器也被动作即时改变，`eta_z,a` 必须加入；删掉它会低估风险。

## 3. 完整联合增益给出的有限时域证书

对 `j>t`，假设在包含两条被比较轨迹的凸、前向不变 tube 上，完整 map `F_j` 在一个固定状态范数中满足可审计的增量界

\[
 \|F_j(h;\xi_j)-F_j(h';\xi_j)\|_*\le \gamma_j\|h-h'\|_* .
\]

这里 `gamma_j` 必须约束完整 block Jacobian `[[A,B],[C,D]]` 或其非光滑对应 Lipschitz map；只约束 `I-beta kk^T`、只看 gate 在 `[0,1]`、或分别检查 `A,D` 都不够。令

\[
 \Gamma_0=1,\qquad
 \Gamma_h=\prod_{j=t+1}^{t+h}\gamma_j\quad(h\ge1).
\]

归纳得到

\[
 \|h_{t+1+h}^a-h_{t+1+h}^0\|_*\le \Gamma_h\|\eta_a\|_*.
\]

未来 query 若是共同的外生保护 probe，可直接令时域 `h` 的保护输出为 `g_h(h_{t+1+h},q_h)`。若 query 由状态生成，则必须把所有 query-generating hidden state 纳入 `h`，并使用闭环复合输出

\[
 \widetilde g_h(h;\xi_h)=g_h(h,Q_h(h;\xi_h)).
\]

以下统一写成 `g_h`，但 `L_h` 必须约束实际使用的共同-query readout 或上述完整复合 map。在同一 tube 上要求

\[
 \|g_h(h,q)-g_h(h',q)\|_{M_h}\le L_h\|h-h'\|_*.
\]

其中 `M_h\succeq0`。对非负、决策前固定的权重 `w_h`，并在给定 `F_t` 后对两动作共享的同一 `xi_h`/probe 参考律取期望，有限时域平方位移能量于是满足

\[
 \begin{aligned}
 D_{a,H}
 &=\sum_{h=0}^{H}w_h\,\mathbb E_{q_h}\|g_h(h^a,q_h)-g_h(h^0,q_h)\|_{M_h}^2\\
 &\le \underbrace{\left(\sum_{h=0}^{H}w_hL_h^2\Gamma_h^2\right)}_{C_H}\|\eta_a\|_*^2
 =:U_{a,H}^{\rm dyn}.
 \end{aligned}
\]

这是完整 coupled-state 路径上的充分上界，不是近似等式。若动作改变 `xi_h` 或 query/target 的概率律，这个 pathwise 结果仍不包含 change-of-measure 项；不能用它声称自由运行总效果。若 `gamma_j<=gamma<1`、`L_h<=L`、`w_h=1`，则

\[
 C_H\le L^2\frac{1-\gamma^{2(H+1)}}{1-\gamma^2},
 \qquad
 C_\infty\le \frac{L^2}{1-\gamma^2}.
\]

若有折扣 `w_h=lambda^h`，只需 `lambda gamma^2<1` 才有相应无限和；若 `gamma>=1` 且无足够折扣，有限证书可随 horizon 指数增长，不能伪称长期安全。

### 3.1 保留 v1 的精确首步几何

若 `h=0` 的保护 readout 正是 `o(q)=S^Tq`，则无需用粗糙 `L_0`：

\[
 d_{a,0}=\alpha_a^2\beta^2(e^\top M_0e)k^\top G_{p,0}k
\]

是精确项。实际使用

\[
 U_{a,H}^{\rm hybrid}=w_0d_{a,0}+\|\eta_a\|_*^2
 \sum_{h=1}^{H}w_hL_h^2\Gamma_h^2.
\]

替换全时域粗界。这个 hybrid 只在首步 readout 条件成立时更紧；它没有把未来 endogenous query 重新冻结。

### 3.2 从位移到保护风险

若同一时域内仍有效保护 target `y_h(q_h)` 合法可见，并且风险比较使用与位移能量相同的共同 query/target 参考律，令 baseline 残差能量

\[
 R_{0,H}=\sum_{h=0}^{H}w_h\mathbb E\|g_h(h^0,q_h)-y_h(q_h)\|_{M_h}^2\le \rho_H.
\]

把各时刻残差和位移视为直和 Hilbert 空间中的两个向量，Cauchy--Schwarz 给出

\[
 R_{a,H}-R_{0,H}\le 2\sqrt{\rho_H U_{a,H}}+U_{a,H}.
\]

因此

\[
 U_{a,H}\le (\sqrt{\rho_H+B}-\sqrt{\rho_H})^2
\]

是 `B\ge0` 时使时域保护风险增加不超过 `B` 的充分条件。与 v1 一样，位移小不等于事实正确；若 protected target 的“仍有效”无法从合法证据识别，这只是条件证书。

## 4. 保护纤维揭示的旧反例：收缩并非免费

完整全状态严格收缩会逐渐抹去由初始状态携带的区别，因此它与永久精确保留并不相容。更合法的结构是固定保护坐标 `p`、只让可适应坐标 `y` 横向收缩：

\[
 p^+=p,\qquad y^+=f_j(p,y).
\]

若 `||partial_y f_j||<=gamma<1`、`||partial_p f_j||<=c_p`，动作注入分解为 `(delta p,delta y)` 后，已有 fiber bound 给出

\[
 \|\delta y_h\|
 \le \gamma^h\|\delta y\|
 +c_p\frac{1-\gamma^h}{1-\gamma}\|\delta p\|.
\]

若保护输出满足 `||delta o_h||<=l_p||delta p||+l_y||delta y_h||`，则把右侧平方后求和可得有限时域 `U_{a,H}^{fiber}`。该式给出一个不能删除的边界：

- `delta p=0` 时，写入纯属保护纤维内的适应，长期项可几何衰减；
- `delta p!=0` 时，保护坐标差不会自动消失，还会持续驱动 `y`；无折扣无限时域通常不能由 `gamma<1` 单独给有限预算；
- 若真实修订恰须改变 `p`，硬保护与修订目标冲突。只有额外的 release 证据或重新定义保护坐标才能解决，收缩本身不能识别旧知识是否过时。

因此 v1 的“`d_a=0` 不排除未来损伤”被修正为一个可检查的充分结构，而不是被删除；旧反例在未满足完整增益/tube/保护坐标条件时继续成立。

## 5. 回代安全 logging：长期传播改变 feasibility

要把第三节的条件定理用于部署，tube、`gamma_j`、`L_h` 和 `rho_H` 的数值都必须在动作前由 `F_t`-可测的 simultaneous upper bounds 给出；若只能事后用真实 future query/target 或已实现轨迹计算，它只是 retrospective diagnostic。令 `\bar U_{a,H}` 是在决策前同时成立的上置信证书，满足

\[
 \Pr\{D_{a,H}\le \bar U_{a,H}\ \forall a\mid\mathcal F_t\}\ge1-\delta.
\]

行为策略仍解，其中 `0<\varepsilon_\mu\le1/K`：

\[
 \min_{\mu}\sum_a\frac{g_a}{\mu_a}
 \quad\text{s.t.}\quad
 \sum_a\mu_a=1,\quad \mu_a\ge\varepsilon_\mu,
 \quad\sum_a\mu_a\bar U_{a,H}\le b_H.
\]

KKT 形式与 v1 相同；修订只替换了真正应进入约束的损伤对象。对有限非负 `\bar U`，多动作可行性当且仅当

\[
 b_H\ge\varepsilon_\mu\sum_a\bar U_{a,H}
 +(1-K\varepsilon_\mu)\min_a\bar U_{a,H}.
\]

二元 no-write/write 且 `U_0=0` 时，另有 `\varepsilon_\mu\le1/2`，预算必要条件变成

\[
 b_H\ge\varepsilon_\mu\bar U_{1,H}.
\]

因为 `U_{1,H}` 随 horizon、增益和保护输出敏感度增长，单步看似可行的探索可在长期预算下变成不可行。这是 v2 的判别预测；它并没有改变 safe optimal design 的通用优化本体。

重要的是，`sum_a mu_a Ubar_a<=b_H` 在 coverage 事件上只控制**随机动作采样前的条件期望损伤**。它不保证实际抽到的每个动作都有 `D_A<=b_H`。若要求 actionwise hard safety，必须对所有 `mu_a>0` 的动作逐个要求 `Ubar_a<=b_H`；危险动作又必须保持正 propensity 时，这个要求可能直接不可行。

若 full-state bound 只是数据依赖 plug-in 值，必须用独立校准、统一函数类界或 anytime confidence sequence 把 `gamma_j,L_h,rho_H` 的估计误差同时纳入 `\bar U`。逐步置信事件直接相乘、事后选择最小的证书或在同一日志上调参再声称 coverage 都无效。

## 6. 旧反例复查、新失败边界与最小反例

1. **完整闭环秩增长仍成立。** 每步 gate-feedback 可注入新 rank-one 方向；本稿只传播范数，不声称远期 tangent 保持 rank one。
2. **局部 Jacobian 不给 tube 上界。** 标量 `F(h)=h+h^2` 在 `h=0` 的导数为1，但任意正邻域上最大导数大于1；点值不能认证 `gamma<=1`。
3. **分别稳定的块仍可联合扩张。** `A=D=1/2,B=C=3/5` 的联合最大特征值为 `11/10`。因此不能用 memory gate 与 updater gate 的两个局部范围替代完整增益。
4. **低位移不等于低语义风险。** 若 baseline 残差/交叉项未知，`D` 只能控制输出移动，不能判断移动方向是否修正真值。
5. **外生路径不等于自由运行。** 两动作使以后 token 分布不同而状态 map 在各自路径上都收缩时，pathwise `U` 仍不识别 total effect；R02 的随机化/OPE 条件没有被消除。
6. **安全但不学习。** `gamma` 或 `L` 的保守上界会令所有非基准动作接近 propensity floor，估计方差变大且更新收益未知。
7. **永久保护与可修订冲突。** 把所有旧方向放进 `p` 可让 `delta p=0` 显得安全，却排除了真正需要覆盖的旧事实；这不是“无遗忘”成功。

## 7. 可计算性、信息成本和强简单替代

单次 Delta 注入范数由 `k,e,beta,alpha` 以 `O(d_k+d_v)` 额外标量计算得到；v1 的首步 probe 几何是 `O(rd_k)` 或稠密 `O(d_k^2)`。若已有可信逐步 `gamma_j,L_h` 上界，累计 `C_H` 只需 `O(H)` 标量递推。

真正困难的是取得这些上界：完整联合 JVP/VJP、uniform tube 认证、离散路由和随机环境处理，通常比 rank-one 局部证书昂贵；精确 tangent 还会按 horizon 增长，多个未结算 edit 的状态/计算至少随 pending 数增加。因而当前没有证明相对直接 rollout、完整 JVP/VJP、RTRL/UORO/e-prop、普通 future CE/action predictor 更省计算或样本。

最强简单替代必须包括：no-write、标准 Delta、固定 `epsilon`、v1 单步证书、普通 SEPEC/Safe Optimal Design、硬投影/soft preconditioner、固定 outer-trained updater、直接 future-loss/action predictor、顺序 DR、普通 full-Jacobian norm guard 及相同预算的 rollout。若 `U_dyn` 的优势只来自更多 probe、未来标签、保存原文或更多前滚，它不是同信息同资源优势。

## 8. 最近工作差异与原生测量

- SEPEC、Safe Optimal Design、stage-wise constrained bandits、CLUCB/SEA 与普通 OPE 已覆盖安全/成本约束的 logging 与方差权衡；v2 不声称重新发明该优化。
- 小增益/增量稳定与受保护纤维是已知控制工具；`STEP2_COUPLED_UPDATER_STABILITY.md` 已在本项目给出完整 block 条件与保护不变量边界。
- RTRL、UORO、KF-RTRL/OK、SnAp、e-prop 和本项目 `STEP2_CLOSED_LOOP_RANK_GROWTH.md` 已覆盖完整在线 sensitivity 及低秩/稀疏近似碰撞；只用范数证书不产生新信用算法。
- MAML、learned optimizer、DNI、DSSR、SEAL、ACL/SRWM、HOPE 与 TTT Ouroboros 已覆盖 post-update future loss、synthetic credit、self-generated Delta 更新和延迟真实后缀验证的主要机制。

本修订的窄残余只是：把 Delta 的 rank-one 即时注入大小、完整 coupled-state 增量增益和 safe-logging positivity 放进同一条可行性公式，明确单步安全什么时候不能外推。这个理论接口是否已被最近工作逐式覆盖尚未穷尽，但它目前没有证明新的算法能力或同预算优势。

LongMemEval/LongMemEval-v2 可测最终记忆问答，SEAL continual 可测连续 self-edit 后的旧问题保持，CITB/TRACE 可测任务级 BWT；它们都不原生提供决策时的真实保护集合、`gamma/L` 全域证书、动作 propensity 与 paired counterfactual outcome。bAbI/LAMBADA 也只有 endpoint。故本阶段只能记录 measurement gap，不能造标签、scorer 或结果。

## 9. 可证伪预测、状态与重开条件

在相同动作集、信息、propensity floor 和总预算下，v2 预测：

1. 当 `C_H` 随 horizon 或 coupled gain 增大时，允许的 write 概率上界按 `b_H/U_{1,H}` 收紧；
2. 若真实保护损伤与 `U_dyn` 无关，或 tube/coverage 频繁失效，则该证书不能承担长期安全；
3. 若 edit 完全位于稳定保护纤维内，未来位移应按几何界衰减；若含永久保护坐标分量，则不应观察到同样的 horizon 饱和；
4. 若普通 rollout/full-Jacobian guard 在同信息同计算下同样紧或更紧，则 Delta rank-one 入口没有实质优势。

处置：v2 数学在明确的同外生路径、uniform tube、合法保护目标和 simultaneous certificate 条件下成立；它完成了 R03 的第二次有证据修复，但核心仍是已知安全实验设计 + 已知增量稳定的条件组合。当前保留为 **coupled-horizon safety control / theory boundary**，不分配 D 编号，不增加 active/scientifically-admitted/selected 计数。第三次修订只在以下任一新 delta 出现时重开：

- 证明比直接 rollout/full Jacobian 或通用 robust safe design 更低的 Delta-specific 同预算证书成本；
- 找到不泄漏的原生 sequential protocol，能同时观察 propensity、保护有效性与更新反事实；
- 推导自由运行分布变化下合法、有限方差且可计算的顺序证书，而不是只给 pathwise bound。

本稿未执行项目/作者代码、软件测试、训练、推理、评分、数据/模型下载、GPU 作业、Docker 或付费服务。
