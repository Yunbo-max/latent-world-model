# Delta 闭环切向的有效秩：收缩、年龄截断与无偏压缩的条件边界

状态：Step2 条件数学控制；不是 D 候选、RSI 证据、实现或实验设计。恢复的 literal-main parent 是 `617b21a049541e441ecd251f36fcb095365475a8`。本文承接 `STEP2_CLOSED_LOOP_RANK_GROWTH.md`：完整闭环切向的代数秩可以随时域增长；这里检验“收缩是否自动使它低有效秩，以及是否由此得到 Delta 特有的同预算估计优势”。未执行项目/上游代码、测试、训练、推理、评分、数据/模型下载、GPU 或 Docker。

## 1. 对象与三种不能混淆的“低秩”

令 `S_t in R^(d_k x d_v)`，焦点扰动的完整切向为

`X_t = partial S_t / partial theta`。

闭环线性化写成 `X_(t+1)=A_t X_t`，其中 `A_t` 是沿给定名义轨迹的矩阵空间线性算子。对于只让标量 gate 读取 state、其余未来特征固定的受控情形，已有精确式

`A_t X = L_t X + U_t <G_t,X>_F`,

`L_t X=(I-beta_t k_tk_t^T)D_tX`, `U_t=k_te_t^T`。

在这个受控递推里，令 `gamma_s=<G_s,X_s>_F`，则有精确的有序展开

`X_T=L_(T-1:t)X_t + sum_(s=t)^(T-1) gamma_s L_(T-1:s+1)k_se_s^T`。

`gamma_s` 虽然由精确的过去切向内生决定，沿固定名义轨迹取值后该式仍是恒等式。若初值项也有低秩分解并把它与这些 rank-one 项一起写成 `X_T=AB^T`，非零奇异值平方等于

`eig[(A^TA)^(1/2)(B^TB)(A^TA)^(1/2)]`。

所以可由两个随 horizon 增长的小 Gram 矩阵求谱，而不必形成 `d_k x d_v` 切向；但因子数仍随时域增长。这是受控 scalar-gate 情形的结构便利，不是固定成本结论。

必须分别报告：

1. **代数秩** `rank(X_t)`：非零再小也计数；
2. **绝对 epsilon-rank**：存在 rank-r 的 `Y` 使 `||X_t-Y||<=epsilon`；
3. **相对或决策加权有效秩**：误差相对 `||X_t||`，或由实际 costate/action 评价。

强收缩可让整个 `X_t` 小到零矩阵就是好的绝对近似，却不必让归一化奇异谱集中。这是本轮最重要的范围修正。

## 2. 一个合法反例：完整一步严格收缩，但相对有效秩仍随 H 线性增长

取 `d_k=d_v=d>=H`、标准基 `a_1,...,a_d`、`X_1=a_1a_1^T`。令

- `D_j=alpha I`，其中 `0<alpha<1/2`；
- `k_j=v_j=a_(j+1)`；
- `beta(S)=sigma(4 alpha S_(11))`。

沿名义路径 `S_(11)=0`，故 `beta=1/2`，`G_j=alpha a_1a_1^T`，而 residual 方向给 `U_j=a_(j+1)a_(j+1)^T`。于是

`A_jX=alpha(I-(1/2)k_jk_j^T)X + U_j<alpha a_1a_1^T,X>_F`。

由三角不等式，`||A_j||_(F->F)<=2alpha<1`。归纳又给出

**`X_H=alpha^(H-1) sum_(i=1)^H a_ia_i^T`.**

所以 H 个非零奇异值完全相等。对任意 `r<H`，Eckart--Young--Mirsky 给出

`min_(rank(Y)<=r) ||X_H-Y||_F / ||X_H||_F = sqrt((H-r)/H)`,

且相对谱范数误差为 1。完整一步 Jacobian 一致收缩并没有产生低**相对**有效秩；它只是把整个 sensitivity 乘成 `alpha^(H-1)`。因此“absolute epsilon-rank 随时域变小”可能只是信用信号已消失，不能解释成既保留长期信息又获得低秩计算。

更精确地，任意相对谱误差 `epsilon<1` 都需要 rank H；达到相对 Frobenius 误差 epsilon 则需要 `r>=ceil[H(1-epsilon^2)]`，仍为 `Theta(H)`，而不是对所有相对定义都逐字等于 H。

这个反例仍只针对局部切向，不声称自然模型必然出现平坦谱，也不把切向秩当作算法内存下界。

## 3. 何时确实有对数绝对 epsilon-rank

考虑比“完整 `A_t` 收缩”更强、也更可审查的 Duhamel 分解

`X_T=P_(T-1:0)X_0 + sum_(ell=0)^(T-1) Z_ell`,

其中

`Z_ell=P_(T-1:T-ell) U_(T-1-ell)c_(T-1-ell)`

是距终点 `ell` 步的 transported injection，`ell=0` 时 `P_(T-1:T)` 是空乘积。假设：

1. `P` 是真实时间顺序的背景 transport，保持矩阵秩不增；
2. 每个即时 injection 的秩至多 p；
3. 对一个固定范数，`||Z_ell||<=B rho^ell`，`0<rho<1`；
4. 初值项的 transported rank 为 `r_init`，并单独保留；若要丢弃它，必须另给误差界。

保留初值项和最近 r 个 injection 得到 rank 至多 `r_init+pr` 的显式近似 `Y_r`，并有

**`||X_T-Y_r|| <= sum_(ell=r)^infty B rho^ell = B rho^r/(1-rho)`.**

故达到绝对误差 epsilon 的充分条件是

`r >= log(B/[epsilon(1-rho)]) / (-log rho)`。

这是一个年龄截断/遗忘记忆上界，不是 generic closed-loop contraction 的推论。若 state-dependent decay、key、value、workspace 或 updater state 的微分产生高秩 injection，例如

`d[D(S)S][X]=D(S)X+dD(S)[X]S`,

则即使 `D` 对角，第二项在 `S` 满行秩时也可一步满秩；上述 p 必须重新记账。若只知各 `A_t` 的谱半径小于 1，也不够：非正规矩阵 `[[rho,K],[0,rho]]` 的幂含 `m K rho^(m-1)`；需要带常数 C 的完整有序产品界，而不是局部 eigenvalue、gate 范围或冻结左因子。

当每个 `Z_ell` 都是 rank one、其左方向彼此正交且右方向也彼此正交，并且 `||Z_ell||_F=B rho^ell` 时，有限 T 的最优 rank-r 尾恰为

`B rho^r sqrt[(1-rho^(2(T-r)))/(1-rho^2)]`，

其无限时域上界/极限为 `B rho^r/sqrt(1-rho^2)`。这说明在这些额外双侧正交条件下，对 epsilon 与 rho 的对数依赖基本紧；只有 Frobenius 正交并不足够，例如 `E_11` 与 `E_12` 正交但相加仍为 rank one。方向抵消可让最佳 SVD 远优于年龄截断，也可让“先丢旧项再求和”破坏原有抵消；该上界只是充分而非自适应最优。

## 4. 决策误差比无加权 Frobenius rank 更接近科学对象

若最终信用只通过 costate `Lambda_T` 进入动作，则近似误差满足

`|<Lambda_T,X_T-Y>_F| <= ||Lambda_T||_* ||X_T-Y||`,

其中对偶范数必须与所选矩阵范数一致。一个 Frobenius 尾很小的方向仍可被特定 query/costate 强烈放大；反之，高秩切向可完全落在允许动作的零空间。因此真正有用的结论应固定：

- 物理 key-by-value 坐标与范数；
- 允许的 action/readout family；
- 同信息的 costate 或输出加权风险；
- 是否比较 absolute、relative 还是 action regret。

非正交换尺度会改变 numerical rank；任意 `vec(S)` 重张量化甚至会改变 matrix rank。任何一般计算下界还需另定在线/因果计算模型。reverse VJP 可以不物化 `X_T` 而得到标量信用，符号规则也可能压缩满秩矩阵。

## 5. 随机截断：无偏不等于低方差或新信息

对一个可求和的贡献序列 `X=sum_(ell>=0) Z_ell`，令随机 cutoff K 的 survival probability 为 `q_ell=P(K>=ell)>0`，则 Russian-roulette 估计

`hat X=sum_(ell>=0) 1{K>=ell} Z_ell/q_ell`

在固定名义轨迹、线性 transport、`sum_ell ||Z_ell||<infty`，且 `K<infty` almost surely（有限期望成本 `sum q_ell<infty` 已足够）等条件下满足 `E[hat X]=X`。一般非正交 nested-cutoff 情形可用更强充分条件 `sum_ell ||Z_ell||_F/sqrt(q_ell)<infty` 控制完整双重交叉和；仅有 `sum ||Z_ell||_F^2/q_ell<infty` 并不足够。若各 `Z_ell` 两两 Frobenius 正交，后一个较弱条件才足以给有限二阶矩，且方差精确简化为

`E||hat X-X||_F^2=sum_ell ||Z_ell||_F^2(1/q_ell-1)`。

survival 序列还必须满足 `1=q_0>=q_1>=...>0`。若 `||Z_ell||_F` 已按 ell 非增，则固定 `q_0=1`，在期望保留成本 `sum q_ell=C` 下，对 `ell>=1` 的 KKT 解是

`q_ell=min(1, ||Z_ell||_F/sqrt(lambda))`，

其中 lambda 使 `sum_(ell>=1) q_ell=C-1` 成立。一般非单调贡献需要带 monotonicity 的 isotonic pooling；若改成独立 inclusion，点式解才可不受 survival 单调约束。几何贡献给合法的几何尾概率。这是 ARTBP / randomized telescoping 类型的已知 cost--variance 配置；非正交贡献时 nested survival indicators 带交叉协方差，上式不能直接使用。

更一般地，任何 rank 至多 r 的随机矩阵 Z 若要求 `E[Z]=Y`，都有

`E||Z-Y||_F^2 >= ||Y||_*^2/r - ||Y||_F^2`。

证明只用 `rank(Z)<=r => ||Z||_*<=sqrt(r)||Z||_F`、核范数的凸性和 Jensen。不妨取 `Y=cI_d`，相对 MSE 至少为 `d/r-1`。因此上一节的平坦谱收缩反例也会迫使无偏低秩压缩承担大方差；随机化不会凭空创造低秩结构。

在受控 scalar-gate 递推中，rank-r 输入经一步至多变成 rank `r+1`，因而可对左右因子的小 Gram/SVD 做一步压缩，典型因子代价约为 `O((d_k+d_v)r^2+r^3)`，而不物化完整矩阵。但若 `G_t` 稠密，计算 `<G_t,p_iq_i^T>=p_i^TG_tq_i` 仍可能昂贵；一旦 key/value/decay/workspace/updater state 也依赖 memory，单步 `r -> r+1` 也不再保证。该便利没有给出相对现有 Kronecker/低秩 sensitivity 方法的统计优势。

这里的无偏性还是**固定轨迹条件**。若 sketch 本身改变以后 gate、query、memory 或自由生成路径，一般有

`E[A(hat X)hat X] != A(E[hat X])E[hat X]`，

必须把随机路径纳入目标和估计器重新推导，不能沿用线性 conditional-unbiased 结论。

## 6. 与已有方法的实质碰撞

- Stable Recurrent Models 已在全局 contractive transition、Lipschitz/smooth loss 等假设下给 recurrent model 与有限上下文近似的指数衰减梯度/训练差异；这不是 Delta 专属性质。
- Adaptive TBPTT 直接估计后向 gradient norm 的几何衰减，并用它控制 TBPTT bias；作者实现提供 `calculate_gradient_norms`、`estimate_logbeta_*` 与 `log_abs_error_estimate`。
- ARTBP 已用随机 truncation 和 `1/(1-c_t)` 补偿构造无偏 truncated BPTT，并明确承担方差。
- Randomized Telescopes 已系统化有限/无限循环的无偏随机截断、importance weights 及 cost--variance 选择；作者实现含 `GeometricRandomizedTelescope`、`PolynomialRandomizedTelescope` 与 adaptive/fixed variants。
- RTRL、NoBackTrack/UORO、KF-RTRL、OK、SnAp 与 e-prop 已覆盖 exact recurrent sensitivity、随机 rank-one、Kronecker、稀疏及 eligibility factorization。

所以“收缩后做低秩/截断”“随机化恢复无偏”以及“按贡献大小配置 survival”均是强控制，不足以分配新的 D 编号。Delta-specific 剩余义务是：在真实完整 transition 的可核结构下，证明 action/output-weighted estimator 相对 reverse VJP、TBPTT、UORO/KF-RTRL/OK/SnAp 和同信息 direct-action predictor 有 matched-budget 的 bias、variance、sample-complexity 或 runtime 优势。本轮没有得到该结果。

## 7. 可证伪问题、自然测量与失败边界

可证伪自然问题被收窄为：在固定真实输入、相同 suffix 信息和总计算下，

1. 完整闭环切向的预注册绝对、相对与 action-weighted singular tail 是否都小；
2. ordered-product 增益和每步截断 residual 是否能预测 full-reference delayed-credit error；
3. 在同 state bytes、dtype、JVP/VJP 次数、checkpoint/replay 和随机样本数下，结构化估计器是否改善 bias--variance--cost frontier；
4. 这种改善是否仍转化为原生 endpoint，而非只因长期 signal 已经衰减。

现有 bAbI/LAMBADA、BABILong/RULER、LongMemEval、CITB/TRACE/SEAL/StreamingQA 都没有闭环 tangent、costate、奇异值尾、截断 residual 或 ideal edit 原生标签。它们可分别测长上下文输出、知识更新、参数级保持/迁移或连续 self-edit endpoint，不能认证内部有效秩机制。需要以后把 exact/small-state BPTT 或 RTRL reference、谱和截断干预绑定到同一原生样本；这是新 instrumentation 义务，不是 benchmark ground truth，也不在本数学阶段执行。

强简单对照包括 full reference（仅小状态/有限 horizon）、frozen rank-one、TBPTT、ARTBP、UORO/NoBackTrack、KF-RTRL、OK、SnAp、e-prop、普通 future CE/BPTT、同信息 direct-action predictor 与固定 learned updater。持续学习 endpoint 另比较 LoRA/SFT+replay、EWC、GEM/A-GEM 与 OGD；RAG/full-history 只有把额外文本、索引内存、reader tokens 和 latency 全部记账后才是公平上界。

## 8. 决定

本轮形成两个严格边界：

1. 全闭环一致收缩不推出低相对有效秩；合法 scalar-gated Delta 路径可同时满足 `||A_t||<1` 与平坦的 H 维归一化奇异谱。
2. 对数绝对 epsilon-rank 需要 rank-bounded injection、rank-preserving ordered transport 与按年龄衰减的 transported norm；它是 fading-memory/age-truncation 控制，且可能只是 signal vanishing。无偏随机低秩压缩在平坦谱上有明确方差下界。

处置为：**conditional theorem/control; major component collision; native mechanism measurement gap; no D ID; no scientific admission.**

计数保持 **5 历史 / 0 活动 / 0 科学准入 / 0 选择**；20/15 目标短缺不变。下一合法问题不再是“收缩是否自动低秩”，而是寻找 Delta 实际 transition 中可审计的 rank-preserving/low-action-width 结构，并证明它在同因果信息与同预算下改善 action-weighted estimator，而非只让长期信用消失。
