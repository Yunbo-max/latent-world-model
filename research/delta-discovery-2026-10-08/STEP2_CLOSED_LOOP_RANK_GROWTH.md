# Delta 完整闭环信用：前向切向秩增长、固定矩阵秩边界与截断误差控制

状态：Step2 条件数学控制；不是 D 候选、RSI 证据、实现或实验设计。恢复的 literal-main parent 是 `4552000c4719b9aa5db6fd1948ab321704a1db3f`。本文只处理一个窄问题：冻结未来路径时单个标量 Delta gate 的 rank-one eligibility，在未来 gate 继续读取记忆的完整闭环里是否仍能保持固定秩。未执行项目/上游代码、测试、训练、推理、评分、数据/模型下载、GPU 或 Docker。

## 1. 对象与范围

令 Delta memory 为 `S_j in R^(d_k x d_v)`。在一条给定外部输入的名义轨迹上，取一个焦点标量扰动 `theta`（例如时刻 `t` 的 gate），定义完整闭环切向量

`X_j = partial S_j / partial theta in R^(d_k x d_v)`。

若以后 `D_j,beta_j,k_j,v_j` 全部冻结，已有结果是

`X_(j+1)=L_j X_j`, `L_j X=(I-beta_j k_j k_j^T)D_j X`,

所以由一次 rank-one 注入开始的 `X_j` 始终 rank one。这里改成更真实但仍受控的情形：以后 gate 可微地依赖当前 memory，`beta_j=b_j(S_j,F_j)`；其余未来特征先固定。记

`bar S_j=D_jS_j`, `e_j=v_j-bar S_j^T k_j`, `U_j=k_j e_j^T`, `G_j=nabla_(S_j) b_j`。

沿名义轨迹微分

`S_(j+1)=(I-beta_j k_jk_j^T)bar S_j+beta_j k_jv_j^T`

得到精确局部递推

**`X_(j+1)=L_j X_j + U_j <G_j,X_j>_F`.**

第二项是 state-to-gate feedback 的 rank-one 注入。若 key、value、decay、query、workspace 或 updater state 也依赖状态，它们会再加入对应方向；本文的反例只需最弱的 scalar-gate feedback，故不能被“单步写入 rank one”排除。

## 2. 有限时域秩上界

对任意矩阵 `X`，左乘不增加秩：`rank(L_jX)<=rank(X)`。由秩的次可加性，

`rank(X_(j+1)) <= rank(X_j)+rank(U_j)`。

因此若初始焦点注入 `rank(X_(t+1))<=r_0`，以后第 `s` 步反馈方向秩至多 `r_s`，则

**`rank(X_(t+H)) <= min(d_k,d_v,r_0+sum_(s=1)^(H-1) r_s)`.**

标量 gate 的 `U_s=k_se_s^T` 满足 `r_s<=1`，故上界是 `min(d_k,d_v,H)`。这是上界，不是“秩必然增长”；若所有反馈方向落在已有行/列张成、`<G_j,X_j>=0` 或被后续 erase 消掉，秩可以保持一。结论只是否定**无条件固定秩 exact eligibility**。

## 3. 上界可达的合法 Delta 局部构造

取 `d_k=d_v=d>=H`，标准基为 `a_1,...,a_d`。令名义初态 `S_1=0`，焦点切向量 `X_1=a_1a_1^T`。对 `j=1,...,H-1` 选

- `D_j=I`, `k_j=a_(j+1)`；
- `v_j=a_(j+1)`，因此在名义路径上 residual `e_j=a_(j+1)`；
- 所有步骤共享同一个平滑 gate `beta(S)=sigma(4 S_(11))`。

名义写入只改第 `2,...,H` 行，所以始终 `S_(11)=0`，从而名义 `beta=1/2`，且 `G=a_1a_1^T`。这是一个统一、全局有界的 state-dependent scalar gate，不需要每步另设中心。

归纳假设 `X_j=sum_(i=1)^j a_ia_i^T`。因为 `X_j` 的第 `j+1` 行为零，

`L_jX_j=(I-(1/2) a_(j+1)a_(j+1)^T)X_j=X_j`；

同时 `<G_j,X_j>_F=1`，于是

`X_(j+1)=X_j+a_(j+1)a_(j+1)^T=sum_(i=1)^(j+1)a_ia_i^T`。

因此

**`rank(X_H)=H`**，直到维数饱和。这个构造只证明存在合法名义轨迹及其局部切向；标准外部驱动 DeltaNet 未必让 gate 直接读取 `S_(11)`，但本文研究的完整反馈 learned updater 允许这种可微 recurrent-state statistic。它不声称模型能从可见前缀学到该 gate，也不提供事实有效性、旧知识 oracle 或性能提升。

由此得到清晰区分：当前时刻的动作 VJP `partial_beta J=k^T Lambda e` 仍是一个标量；但“这个标量扰动以后如何通过 state-dependent updater 影响所有写入”的前向 eligibility 可以随时域线性增秩。低维当前动作信用不等于固定秩完整闭环 sensitivity。

## 4. 固定矩阵秩近似的不可消失误差

上面的 `X_H=diag(1,...,1,0,...)` 有 H 个非零奇异值且都为 1。Eckart--Young--Mirsky 给出任意 rank-`r<H` 矩阵 `Y` 的最优误差

**`min_(rank(Y)<=r)||X_H-Y||_F=sqrt(H-r)`,**

以及 `min ||X_H-Y||_2=1`。更一般地，若对角反馈幅度为 `c_1,...,c_H`，按绝对值降序为 `|c|_(1)>=...>=|c|_(H)`，则最优 Frobenius 尾误差是

`[sum_(i=r+1)^H |c|_(i)^2]^(1/2)`。

所以任何声称“标量 gate 因为每步 rank one，故完整 directional tangent 本身也能永久保持 rank one/fixed matrix rank”的方案都有反例。有限精度、随机投影或 Kronecker/稀疏结构可以降低成本，但必须记账 bias、variance 或结构假设；它们不改变 exact-rank 事实。

这个 rank 下界**不是**一般内存/计算下界：上述对角构造可以由规则和时间索引符号压缩，reverse-mode 也可不显式物化 `X_H` 而直接得到一个标量 gate gradient。若要证明所有 exact algorithms 都需 `Omega(H)` 状态，必须另定信息/通信模型，并让方向和系数形成足够丰富的独立族。本文只否定“用一个固定矩阵秩 `r` 的 decoded forward eligibility 对整个转移类逐点精确表示”。该秩在 key/value 两侧可逆换基下不变，但对任意非可分的 `vec(S)` 重参数化或另一种 tensorization 不具坐标不变性；它是实际 Delta key-by-value 表示的结构命题，不是抽象状态复杂度定理。

### 4.1 名义线性化逐步收缩也不等于固定 exact rank

取 `D_j=alpha I`、`0<alpha<1`，把共享 gate 改成 `beta(S)=sigma(4 epsilon S_(11))`，其中 `0<epsilon<1-alpha`。对 Frobenius 诱导范数，冻结左乘部分的范数至多 `alpha`，feedback 算子 `X -> U<G,X>` 的名义范数为 `epsilon`，所以沿该构造路径的每个完整一步 Jacobian 范数至多 `alpha+epsilon<1`。同一正交方向构造仍在每步产生非零新对角项，有限 H 的 exact rank 继续递增直到维数饱和。这是局部线性化收缩，不是未证明的全局非线性 contraction。

但这些项的幅度会被 `alpha` 衰减。因此严格收缩不推出固定 algebraic rank；反过来，高 exact rank 也不推出远期 credit 数值上重要。后续必须分别报告 exact rank、singular-value tail 和完整有序产品增益。

## 5. 可记账的截断误差上界

把完整切向递推抽象为线性算子 `A_j` 作用在矩阵空间上：`X_(j+1)=A_jX_j`。令近似器每步作某个 rank-`r` 压缩

`hat X_(j+1)=T_r(A_j hat X_j)`，

并把当步丢弃量定义为

`Q_j=A_jhat X_j-T_r(A_jhat X_j)`。

误差 `E_j=X_j-hat X_j` 满足精确递推

`E_(j+1)=A_jE_j+Q_j`，

故

**`||E_T|| <= ||A_(T-1:0)|| ||E_0|| + sum_(s=0)^(T-1) ||A_(T-1:s+1)|| ||Q_s||`.**

这里 `A_(b:a)=A_b...A_a` 保持真实时间顺序；空乘积为恒等。若完整闭环有序乘积满足 `||A_(b:a)||<=C rho^(b-a+1)`、`||Q_s||<=tau_s`，且 `E_0=0`，则

`||E_T||<=C sum_s rho^(T-1-s) tau_s`。

当 `rho<1`、`tau_s<=bar tau` 时得到 `C bar tau/(1-rho)`；`rho=1` 时只能得到累加 `C sum tau_s`，`rho>1` 时误差可放大。逐步 gate 有界或冻结 Delta 左因子非扩张都不能替代对**完整闭环**产品的这个假设。

若末端 loss costate 为 `Lambda_T`，信用误差满足

`|<Lambda_T,E_T>_F|<=||Lambda_T||_F ||E_T||_F`；多时刻 loss 对每个对应 costate 作同样求和。该界可计算的前提是记录真实截断残差 `Q_s` 或合法上界，以及完整产品的可核条件；局部神经估计不能冒充全局 certificate。

另一个常见近似是把 feedback 冻结。写 `A_j=A_j^0+R_j`，`tilde X_(j+1)=A_j^0 tilde X_j`。则

`X_(j+1)-tilde X_(j+1)=A_j(X_j-tilde X_j)+R_jtilde X_j`，

最终误差同样是有序 transported forcing sum。只有 `R_j` 小、冻结切向有界且完整闭环产品受控时，frozen-path rank-one eligibility 才是有误差界的近似；没有这些条件就只是不同目标。

## 6. 稳定性、信息与自然问题边界

秩增长与数值不稳定是不同性质。所有新方向都可乘任意小非零系数，rank 仍增长；反之，高秩切向在强收缩下的尾奇异值可以很小。本文因此不声称 rank 增长必然造成遗忘、训练失败或高 loss，只给出 exact representation/cost 的边界。

同样，切向量只描述给定名义轨迹附近的局部微分。它不识别旧事实是否仍有效，不识别 write/no-write 的自由运行因果收益，也不允许部署读取未来 token。未来真实 token 只可作为训练后缀监督，并须与同信息 direct action、普通 CE、固定 learned updater、UORO/KF-RTRL/SnAp/OK 和 frozen rank-one 控制比较。

可证伪的自然问题被收窄为：在相同可见前缀、动作族和总计算下，闭环切向的奇异值尾部是否实际小到可压缩，以及截断残差加完整产品界能否预测真实 delayed-credit 误差。已有 bAbI、LAMBADA 与 LongMemEval 没有原生 tangent、奇异值或 ideal edit 标签；它们只能作为最终输出 endpoint，不能单独认证该机制。若以后需要内部 instrumentation，那是新实验设计义务，不是当前 native benchmark 已提供的 ground truth。

## 7. 最近工作碰撞与处置

RTRL 已递推完整 recurrent sensitivity；UORO/NoBackTrack 用随机 rank-one reduction 给无偏但有方差的近似；KF-RTRL 与 OK 使用 Kronecker 因子/和压缩；SnAp 只保留有限图距离上的稀疏 influence；e-prop 把 eligibility 与 learning signal 因子化。因而“完整 sensitivity 会变大，需低秩/稀疏/结构近似”不是新发现，也不能以 Delta 命名重新计数。

本文保留的 Delta-specific 价值只有一个严格、窄的控制：即使每次 memory 写入和 gate-feedback 注入都是 rank one，完整闭环的单扰动切向秩仍可按时域线性增长，并有一个合法 Delta 构造达到上界；固定秩近似必须暴露尾误差和闭环传播条件。这可防止把上一轮 frozen-path rank-one eligibility 误外推到 learned updater。

由于该结论是已知 online-sensitivity 压缩问题的 Delta 实例化，且没有形成比现有 UORO/KF-RTRL/SnAp/OK 更强的更新器、估计器或同预算测量，本轮处置为：

**conditional theorem/control; major component collision; no D ID; no scientific admission.**

计数保持 **5 历史 / 0 活动 / 0 科学准入 / 0 选择**；20/15 目标短缺不变。
