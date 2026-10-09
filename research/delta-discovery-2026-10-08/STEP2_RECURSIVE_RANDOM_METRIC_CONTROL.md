# 第2步续接：递归随机条件矩、完整 Jacobian 与因果动作误差界

状态：**已知微分可观测 Gramian、GGN/iLQR、synthetic gradient 与在线递归梯度的 Delta 专用统一控制；不是新候选、原创性裁决、模型实现或实验结果。** 与前三份 Step2 推导属于同一调查线，不重复计数。

恢复基线：literal `main` `ead8a4ed7a38c37653ca9c2acab525c0aabe0278`。本轮没有运行项目/上游源码、软件测试、训练、推理、评分、数据/模型下载、GPU 或 Docker。

## 1. 自然问题与结论

问题不是“给 Delta 再加一个 metric loss”，而是：一次当前 edit 经**完整递归状态**改变未来损失时，未来查询几何、修改有效性和传播路径能否合成一个在 edit 时刻可因果估计、可计算且真正改善动作 regret 的对象？

固定一条 teacher-forced 后缀后，答案有一个精确的局部形式：未来输出曲率通过完整状态 Jacobian 拉回 edit 空间，形成有限时域、轨迹依赖的 GGN/微分可观测 Gramian。它统一了“未来 query covariance”和“传播存活”，但不是新对象。精确 Hessian 还含动力学/读出的二阶曲率项；把它删掉只能称 GGN/iLQR 型 PSD 近似。

在 edit 时刻，真实后缀尚未观察。合法对象是条件期望或 Bayes action；后缀导出的 Gramian/gradient 只能作为训练期监督，不能直接进入在线递推。学习它是 second-order synthetic-gradient/critic 路线。更强的简单基线是用相同因果信息直接预测局部最优 edit；分解成 gradient 与 metric 不增加信息，只可能提供结构、复用、约束或样本效率。

最重要的失败边界是：teacher-forced 后缀的导数对**同一固定 token 路径**精确，但若 edit 改变以后生成的 token、动作或 query 分布，它不是自由运行部署风险的总效应。没有 overlap、环境交互、合法 replay/importance 权重或可信生成模型时，这个反事实缺口不能由 Jacobian 或 diffusion 自动补上。

## 2. 形式对象：完整递归路径

令 `F_t` 是 edit 前可用信息的 sigma-field。把整个持久状态、workspace、gate、decay、计划/表达中会影响未来预测的变量并入 `h_j in R^n`。在给定已观察 teacher-forced 后缀 `xi=(x_(t+1:T),y_(t:T))` 上，

`h_(j+1)(u)=F_j(h_j(u),x_(j+1)),    h_t(u)=h_t+B_t u`，

其中 `u in R^d` 是允许的局部 edit 坐标，`B_t in R^(n x d)` 是其注入 Jacobian。未来风险为

`L_t(u;xi)=sum_(j=t)^T w_j ell_j(h_j(u),y_j)`。

在 `u=0` 的未编辑轨迹上定义

`A_j=partial F_j/partial h_j`，`J_(j<-t)=A_(j-1)...A_t`，`J_(t<-t)=I`，

把权重吸收进局部量：`r_j=w_j nabla_(h_j) ell_j`，`C_j=w_j GGN_(h_j)(ell_j)` 为输出损失对 `h_j` 的 GGN 块，故 `C_j` 半正定。则 edit gradient 是

**`g_t(xi)=B_t^T sum_(j=t)^T J_(j<-t)^T r_j`.**

这已经显示冻结旧 Delta 因子乘积的局限：完整 `A_j` 必须包含 edit 对以后 key/query/gate/decay、其他 memory、workspace 及 readout 的一阶影响。只有冻结特征、相同未来输入且不存在这些旁路时，旧的线性未来乘积才与该 Jacobian 路径一致。

## 3. 精确 Hessian 不等于 GGN

链式法则给出

`nabla_u^2 L_t(0;xi) = M_t(xi) + R_t(xi)`，

其中 PSD 拉回项

**`M_t(xi)=B_t^T [sum_j J_(j<-t)^T C_j J_(j<-t)] B_t`**

而 `R_t` 同时收集本地 readout/loss residual curvature `D_j=w_j nabla^2_(h_j)ell_j-C_j` 以及损失协态与轨迹二阶导数的收缩。若定义协态

`a_T=r_T`，`a_j=r_j+A_j^T a_(j+1)`，

则精确状态 Hessian 可写成

`Q_T=C_T+D_T`，

**`Q_j=C_j+D_j+A_j^T Q_(j+1) A_j+sum_a (a_(j+1))_a nabla^2 F_(j,a)`.**

仿射注入下 exact edit Hessian 是 `B_t^T Q_t B_t`；非线性注入还需协态与注入二阶导数的收缩。等价地，对每个未来坐标 `h_(j,a)`，轨迹项含

`B_t^T [sum_(j,a) r_(j,a) nabla_(h_t)^2 h_(j,a)] B_t`，

而 `D_j` 保留没有被 GGN 吸收的本地网络/损失曲率。故：

- 仿射动力学/读出下 `R_t=0`；
- 在合适的零残差或梯度与轨迹曲率收缩为零条件下也可相等；
- 一般神经递推中 `M_t` 只是 GGN，不能冒称真实 Hessian、全局证书或稳定性定理；
- 精确二阶 DDP 保留动力学曲率，iLQR/GGN 丢弃它以换取 PSD 与可算性。

最小反例说明差项甚至会改变曲率符号：令标量 logit `z(u)=u^2`，标签 `y=1`，binary CE 为 `ell(u)=log(1+exp(-u^2))`。在 `u=0`，`dz/du=0`，所以 gradient 与 GGN 都为零；但 `d^2 ell/du^2=-1`。负曲率完全来自 `ell_z d^2z/du^2`。因此“GGN 小”既不证明真实曲率小，也不证明该点稳定。

对固定轨迹，令 `P_T=C_T`，反向递推

**`P_j=C_j+A_j^T P_(j+1) A_j`**

（按是否把终端/当前损失计入相应平移下标），则 `M_t=B_t^T P_t B_t`。上面的精确 `Q_j` 同时增加 `D_j` 与未来 costate 对 `nabla^2 F_j` 的张量收缩。这个 `P_t` 正是有限时域、线性时变的可观测 Gramian/GGN pullback；非线性时它依赖选定轨迹，并非新型 Delta memory。

方向 `v in R^d` 的矩阵自由计算是：先前向 `z_t=B_t v`，`z_(j+1)=A_j z_j`，再反向 `b_T=C_T z_T`，`b_j=C_j z_j+A_j^T b_(j+1)`，于是

**`M_t(xi)v=B_t^T b_t`**，以及

**`v^T M_t(xi)v=sum_j z_j^T C_j z_j`.**

它对已实现的固定后缀和选定 GGN 对象是 sample-exact；每次 CG 迭代可用一组 JVP/VJP 而不显式形成 dense matrix。精确 HVP 则需对上述协态递推作方向微分，额外加入 `(D_h A_j[z_j])^T a_(j+1)` 与本地 exact Hessian-vector 项；这与 Pearlmutter/DDP 的 vector--tensor contraction 相同。随机探针只能估计 trace/二次型或在额外低秩假设下恢复近似子空间，不能从少量 probe 宣称已识别完整条件矩或 action rank。

## 4. edit 时刻的因果可估计性

部署时 `xi` 尚未出现。因果目标只能是

`bar g_t=E[g_t(xi)|F_t]`，`bar M_t=E[M_t(xi)|F_t]`，

或直接是条件局部 Bayes action。训练时可从已观察后缀计算 realization target，并拟合 `tilde g(F_t), tilde M(F_t)`；若平方误差可积、函数类含真条件期望且达到总体全局最优，则平方损失的最优预测器才等于上述条件期望。这些条件不成立时，“预测未来曲率”只是近似 critic。

为保证 `tilde M` 半正定，可预测因子 `L L^T` 或 PSD 参数化；但 `E[L(xi)L(xi)^T|F_t]` 一般不等于 `E[L|F_t]E[L|F_t]^T`。先平均因子再相乘会系统丢失条件方差，不能冒充条件 GGN。直接预测矩阵还要承担 `O(d^2)` 输出、PSD 投影或低秩/对角结构的偏差。

同样不能先逐后缀求 Newton 动作再平均。若标量 `(M,g)` 以相同概率取 `(1,1)` 或 `(3,-1)`，条件总体二次风险的最优动作是 `-(E M)^(-1)E g=0`，而逐样本动作 `-g/M` 的平均为 `-1/3`。这正是“metric 与修改有效性必须联合”的最小反例；无偏 Jacobian/metric sketch 经求逆后也通常不再无偏。

`bar g_t` 的学习就是 synthetic gradient 的直接特例；RTRL 给完整在线敏感度但通常计算昂贵，e-prop 用 eligibility trace 与近似 learning signal 分离。将同一框架扩展到曲率可叫二阶 synthetic critic，但名称不构成新贡献。

## 5. 从估计误差到可证伪的动作风险

在同一因果目标、同一动作族下，采用带阻尼的局部二次模型

`q(u)=g^T u + (1/2)u^T A u`，`A=M+lambda I`，`M` 半正定、`lambda>0`。

真局部动作 `u*=-A^(-1)g`。令 `Delta g=tilde g-g`、对称 `Delta M=tilde M-M`、`tilde A=A+Delta M` 和 `tilde u=-tilde A^(-1)tilde g`。由 resolvent identity，

`tilde u-u* = -tilde A^(-1) Delta g + tilde A^(-1) Delta M A^(-1) g`。

若 `||Delta M||_2<lambda`，则

**`||tilde u-u*|| <= (||Delta g|| + ||Delta M|| ||u*||)/(lambda-||Delta M||)`.**

并且真二次模型的 excess 恰为

`q(tilde u)-q(u*)=(1/2)||tilde u-u*||_A^2`，

从而至多为

**`(||A||/2) [(||Delta g||+||Delta M||||u*||)/(lambda-||Delta M||)]^2`.**

若通过构造保证 `tilde M` 半正定，`tilde A` 的最小特征值至少 `lambda`，分母可用 `lambda`；但这不消除 `M` 的模型误差、第三阶余项或反事实分布偏差。局部二次预测只在 edit 足够小、Hessian/Lipschitz 余项受控且 solve 误差另计时才联系真实 CE。

更明确地，若真实局部 Hessian `H` 满足 `||H-M||<=rho`，三阶 Taylor 余项常数为 `L_3`，并令对称正定的阻尼 metric `tilde M` 满足 `tilde M≻0`、`tilde u=-tilde M^(-1)tilde g`（这里把阻尼并入两个 metric），则

`R(tilde u)-R(0) <= -(1/2) tilde g^T tilde M^(-1) tilde g + ||tilde g-g|| ||tilde u|| + (||tilde M-M||+rho)||tilde u||^2/2 + L_3||tilde u||^3/6`。

只有右侧严格为负才给局部充分下降。无法合法界住 `rho,L_3`、存在离散检索/路由切换或 exact Hessian 不定时，必须保留 trust region/line search；神经局部估计不能冒充全域证书。

该界给出明确成功条件：在相同 `F_t`、动作族与总预算下，联合预测 `g,M` 必须使动作 excess/真实 endpoint 优于：(i) 只预测 `g` 加标量/单位 metric；(ii) 对角/低秩 metric；(iii) 直接预测 `u*`；(iv) 普通远期 CE/DSSR 式 forward rollout；(v) 增宽 state/MLP。对固定动作族，直接 `u*` predictor 与分解预测拥有相同可用信息，后者只有在结构归纳偏置、跨动作复用、约束或样本/计算效率上才可能赢。

## 6. teacher forcing 与自由运行的不可混淆边界

固定观测后缀上的 `g_t(xi),M_t(xi)` 是**同一 computational path** 的精确一/二阶对象。若部署目标也明确为 teacher-forced next-token risk，它合法；若 edit 会改变随后生成 token、环境动作或 query 分布，则观测后缀来自未编辑行为。继续沿原后缀求导只估计 controlled direct path，不是编辑后自由运行分布的 total effect。

要识别后者至少需要清楚声明的一项：行为与目标策略 overlap 下的 importance correction、同状态反事实 replay、可交互环境，或经独立验证的生成/动力学模型。纯文本 next-token 数据没有真实 action/intervention 记录，不能猜出物理世界反事实。Diffusion 即使拟合多模态后缀也只是一个条件生成器；没有识别假设、正确条件 law 与成本优势时，它既不消除 off-policy bias，也不是必要方法。普通 autoregressive CE、mixture 或 direct conditional predictor 仍是强替代。

## 7. 信息、复杂度与自然测量

- 完整反向 `P_j` 需要未来激活/Jacobian；dense `n x n` 状态 metric 的存储为 `O(n^2)`，递推乘法通常至少 `O(n^3)`，结构化 JVP/VJP 才可能降低。
- `m` 个方向探针的前向成本约为 `m` 条 JVP 轨迹；它们给投影信息而非完整矩阵。Hutchinson/Hutch++ 主要解决 trace，不是 full metric recovery。
- RTRL 式完整参数/状态敏感度会引入大规模 eligibility state；e-prop/低秩/截断近似必须分别记录 bias 与遗漏路径。
- UORO 可给因果、无偏但高方差的 rank-one sensitivity 估计；`E[hat M^(-1)]` 一般不等于 `(E hat M)^(-1)`，所以它不自动产生无偏 edit。
- bAbI 全20 tasks/20000 和 LAMBADA 5153 只给 native endpoint，不给 edit gradient、Jacobian、GGN、反事实后缀或动作真值。
- LongMemEval 的 QA 与 turn/session evidence labels 可测更新后的回答和证据检索，但仍不标注 ideal edit、自由运行反事实、内部条件矩或 action regret。
- 用 teacher/模型反传得到 `g,M,u*` 属派生监督；必须记录 teacher、checkpoint、horizon、teacher-forced/free-running 目标、solve/探针误差、额外 token/显存/CPU 和失败分母，不能称 benchmark 原生标签。

2080Ti 可行性、显存和时间都未测；100M/1B 每 arm/seed 只保留作以后资源背景。

## 8. 最近工作碰撞与处置

| 本轮对象 | 已有直接近邻 | 剩余义务 |
|---|---|---|
| `sum J^T C J` 的轨迹依赖条件矩 | differential/variational observability Gramian；GGN | Delta 全状态接口与成本实例化，不是新数学对象 |
| 精确 Hessian 与 PSD 近似的差 | DDP 的 dynamics curvature；iLQR/GGN | 真实神经递推中何时近似足够 |
| 未来 gradient 的因果预测 | DNI/synthetic gradients | 长 lag、校准、同信息 direct-action baseline |
| 完整在线递归敏感度 | RTRL；e-prop eligibility traces | 可承受结构和近似误差 |
| 联合预测 gradient/metric 后求动作 | learned second-order critic / Newton-style action | 是否优于直接 `u*` predictor 的可识别优势 |
| teacher-forced 后缀评价 writer | DSSR recursive forward rollout | 自由运行分布改变时的反事实识别 |

**处置：不分配 D 编号。** 推导得到一个严谨、可证伪的统一控制和动作误差界，但核心部件被微分 Gramian、GGN/DDP/iLQR、synthetic gradients、RTRL/e-prop 与 DSSR 覆盖；当前没有证明 Delta 特有的联合 estimator 在相同信息/计算下优于直接动作或普通 CE，也没有 native 反事实标签。

下一合法残余缩小为：寻找一个真实文本监督下可识别的结构条件，使 `bar M_t` 的低秩/对角递归 estimator 比直接动作 predictor 具有可证明的跨 horizon/跨动作复用或样本复杂度优势；否则把该线索保留为诊断/训练控制，不构造候选。计数保持 **5 历史 / 0 活动 / 0 科学准入 / 0 选择**，20/15 短缺不变。
