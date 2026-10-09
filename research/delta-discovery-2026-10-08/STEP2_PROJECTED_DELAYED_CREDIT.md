# Delta 延迟反馈：动作空间投影信用、可识别阶数与长期缺口

状态：Step2 条件数学控制与未准入线索；不是新 D 候选、RSI 证据、实现或实验设计。恢复 parent 为 `47f3875232ae0416aa6d05f2363fee1c27e00798`。本轮只做静态数学、来源/作者接口阅读与独立审查，不运行项目或上游代码、测试、训练、推理、评分、数据/模型下载、GPU 或 Docker。

## 1. 问题、因果信息与三种不同对象

令 `F_t` 是写入前实际可见的信息：已观察前缀、已到达的外部反馈、合法持久状态和已记录随机性。未来真实 token 可在训练时作为后缀监督，但部署写入不能读取它；自生成 token、自评或预测未来不构成新的外部证据。

把所有会改变以后计算的量并入增广状态 `x_t in R^n`，包括 `vec(S_t)`、更新器内部状态、workspace、gate/decay 和必要的延迟反馈队列。当前可执行动作 `u_t in R^r` 通过

`x_(t+1)=f_t(x_t,u_t,xi_(t+1))`

进入状态；以后策略仍可依赖状态。未来风险为

`J_(t,H)=E[sum_(j=1)^H gamma^(j-1) ell_(t+j)(x_(t+j),xi_(t+j))]`。

必须分清：

1. **单次动作梯度** `nabla_(u_t) J`：如果只改变当前写入，以后策略固定，它回答“这一次状态修改的局部方向”。
2. **更新器参数 meta-gradient** `nabla_phi J`：共享参数 `phi` 还会改变所有以后写入、更新器状态和访问分布；它一般不是单次动作梯度。
3. **写入相对不写入的因果收益**：这是潜在结果差 `Y(u)-Y(0)`；只观察事实动作后的延迟损失不自动识别它。

固定 outer-trained `phi`、部署只更新 `S/z` 是适应；只有合法反馈确实改变 `phi` 或可证明改变后续更新策略且提高新任务学习效率时，才有更强的自我改进主张。本文不作该主张。

## 2. 完整伴随与 Delta 的投影信用

先固定一条可微、给定外部输入的后缀路径。令完整闭环 Jacobian

`A_j=partial_x f_j + partial_u f_j partial_x U_phi`

包含 key/value/gate、更新器内部状态和以后策略对状态的依赖；若把这些量冻结，就只是旧的 surrogate。把折扣吸收入 `c_j=gamma^(j-t-1) nabla_(x_j) ell_j`，定义伴随

`lambda_T=c_T`,
`lambda_j=c_j+A_j^T lambda_(j+1)`。

若当前动作在一阶上以 `B_t=partial_(u_t) f_t` 注入，则

**`nabla_(u_t) J_(t,H)=B_t^T lambda_(t+1)`.**

这说明延迟反馈的局部充分对象不是完整未来文本或完整 `lambda`，而是伴随在**可执行动作空间**上的投影。

以下把 decay 后状态记为 `bar S=D S`，并令 `e=v-bar S^T k`。对固定 `k,e` 的标量 Delta gate，

`S^+=bar S+beta k e^T`, `w=vec(k e^T)`,

故 `B=w`，动作信用是一个标量

**`g_beta=w^T lambda=<Lambda,k e^T>_F=k^T Lambda e`**，

其中 `Lambda=unvec(lambda)`。若只允许 value 幅度 `a in R^(d_v)`，`S^+=bar S+k a^T`，则

`B=I_(d_v) tensor k`, `g_a=Lambda^T k`。

若未来风险对 `S^+` 的梯度块为 `Lambda`，当前 Delta 动作的精确 VJP 为

`partial_beta J=k^T Lambda e`,
`partial_v J=beta Lambda^T k`,
`partial_k J=beta[Lambda e-bar S Lambda^T k]`。

但若 updater 同时改变 `beta,k,v`，完整微分仍是

`d(Delta S)=(d beta)k e^T+beta(dk)e^T+beta k(de)^T`,
`de=dv-(d bar S)^T k-bar S^T dk`, `d bar S=(dD)S+D(dS)`，

并且 state-dependent decay、后续查询和路由项也进入 `A_j`。只预测一个 gate 信用不能冒充整个 updater 的 meta-gradient。

共享 `phi` 的可重参数化 meta-gradient具有

`nabla_phi J=E[sum_j d_j+sum_j G_j^T lambda_(j+1)]`,

其中 `G_j=partial_phi f_j+partial_u f_j partial_phi U_phi`，`d_j` 是 loss 的显式 `phi` 导数；若转移本身不直接含 `phi`，第一项才为零。此式还假定初始 `x_t` 与 `phi` 无关；否则要加 `(partial_phi x_t)^T lambda_t`。任何不可重参数化且分布依赖 `phi` 的随机节点都需要 `E[L(tau)nabla_phi log p_phi(tau)]` 型 score 项，不限于离散反馈。停止未来 updater 梯度得到的是有定义的 surrogate，不是同一目标的精确梯度。

## 3. Delta 狭窄但精确的结构残余：单 edit 的秩一 eligibility

再取更窄的 frozen-path 控制：未来 `D_r,beta_r,k_r,v_r`、query 和外部输入固定，且实际顺序保持为

`S_(r+1)=A_r S_r+c_r`, `A_r=(I-beta_r k_r k_r^T)D_r`。

令 `bar S_t=D_t S_t`、`e_t=v_t-bar S_t^T k_t`。当前 gate 的微扰才是 `delta S_(t+1)=k_t e_t^T delta beta_t`。因此

`delta S_j=P_(j<-t+1) k_t e_t^T delta beta_t`,
`P_(j<-t+1)=A_(j-1)...A_(t+1)`，

始终为 rank one。对固定未来 query `q_j`，

`delta o_j=e_t [q_j^T P_(j<-t+1)k_t] delta beta_t`，

若每步损失对该 edit 的全部依赖只经过固定读出 `o_j=S_j^T q_j`（没有额外的 `S_j`、workspace 或多读出路径），从而

**`partial L_(t,H)/partial beta_t=sum_j w_j [q_j^T a_j][e_t^T nabla_(o_j)ell_j]`**，

其中 `w_j` 是该步的折扣/风险权重，`a_(t+1)=k_t`, `a_(r+1)=A_r a_r`。所以单个 focal gate 在这些条件下无需保存 `d_k d_v` 的 dense state tangent；若 `D_r` 对角，`A_r a_r=D_r a_r-beta_r k_r(k_r^T D_r a_r)` 每步 `O(d_k)`，eligibility 状态为 `O(d_k+d_v)`。

这是真正来自 Delta 秩一参数化的计算结论，但范围很窄：完整 `partial_h U_phi`、动态 query/workspace、updater-state feedback 会破坏该 rank-one forward tangent；对所有尚未结算的历史 edits 分别保留精确 `a_j,e_t`，总状态仍随有效 horizon/未结算数增长。反向得到完整 `Lambda` 后的当前 VJP 虽仍是 `k^T Lambda e`，传播 `Lambda` 本身也没有免费压缩。任何采用同一 low-rank action family 的直接 updater 都能复用该结构。

因此它是**冻结后续路径上单 edit 的精确 credit 压缩**，不是完整闭环 meta-gradient 的 Delta 独占优势。后文的表示下界说明为什么把更新方向也交给 updater 后，这个一维结论一般不再成立。

## 4. 一个精确表示下界：低维信用何时真的充分

考虑 edit 时刻可能采用的一族注入矩阵 `{B_a}`，定义全部可行动作的一阶张成空间

`U=span_a range(B_a) subseteq R^n`, `s=dim(U)`。

**投影充分性。** 对任意动作，一阶未来效应 `lambda^T B_a u` 只依赖 `Pi_U lambda`；用 U 的一组正交基表示它只需 s 个标量。

**维数必要性。** 假设线性 summary `R lambda in R^p` 要对所有 `lambda`、所有 `a,u` 精确恢复 `lambda^T B_a u`。若 `delta in ker(R)`，`lambda` 与 `lambda+delta` 的 summary 相同，精确恢复要求 `delta^T z=0` 对所有 `z in U`，即 `ker(R) subseteq U^perp`。由 rank-nullity，

**`rank(R)>=dim(U)=s`.**

因此：

- 当前方向固定、只调一个 `beta` 时，`s=1`，标量 delayed credit 在一阶上可充分；
- 允许固定 k 上的全部 value 幅度时，`s<=d_v`；
- 若 k 与 e 可遍历基向量，`e_j tensor k_i` 张成整个 `R^(d_k d_v)`，对全部可能 Delta 方向精确评分一般需要 n 维线性信息；无条件不存在固定低维**线性** exact summary。任意实数的病态非线性编码可藏入无限信息，所以若要把下界扩到一般 critic，必须另加连续性、有限精度、噪声或可计算性条件。

这不是“Delta 天然解决 meta-gradient”的证明，而是一个架构边界：**gate-only updater 可把信用问题压到一维，但学习写入方向会重新打开高维信用与探索成本。** 低维近似只有在动作族受限、伴随具有可验证低秩/稀疏结构，或接受可记账误差时才合法。

## 5. 局部二次动作与同信息强替代

沿可行动作坐标的局部风险写成

`Q(u)=c^T u+(1/2)u^T H u`, `H succ 0`。

其中 `c=B^T lambda`，`H` 是 exact Hessian 的动作空间拉回，或明确标注的 GGN/阻尼近似。部署只可使用 `F_t`，故 Bayes 二次动作依赖

`bar c=E[c|F_t]`, `bar H=E[H|F_t]`,
`u*=-bar H^(-1) bar c`，

而不是先对每条未来求 `-H^(-1)c` 再平均；该闭式需要 `bar H succ 0`。exact Hessian 若不定，只能在明确的局部 trust region、阻尼或 PSD GGN surrogate 下使用相应公式。标量 gate 在 `bar h>0` 时为 `beta*=clip_([0,1])(-bar c/bar h)`。这复用前轮联合条件矩结论；仅把 credit 写成动作投影不产生新信息。

在相同 `F_t`、动作族、容量和训练后缀下，直接 action predictor `D(F_t)` 如果能表示同一个可测映射，就能实现同一 population Bayes 动作。预测 `c,H` 的潜在优势只能来自：跨多个动作重用、约束/PSD 参数化、统计效率或可计算性；不能来自额外部署信息。必须比较普通远期 CE、直接 `u*` predictor、固定 learned updater 和相同 rank-one 动作族。

一个可计算差异是：一次完整 reverse/VJP 得到 `lambda` 后，可用 `B_a^T lambda` 对多个候选方向作局部评分；K 次完整 paired rollout 则重复未来计算。但前者只是局部线性/二次近似，仍需保存或重算后缀激活；若部署改用 prefix critic，又回到条件估计、校准和 direct-action 对照。

## 6. 只有标量延迟结果时的可识别阶数

若没有可微 teacher-forced replay，只观察外部延迟结果，令 paired baseline 已知并在局部满足

`D=Y(beta)-Y(0)=beta c+(1/2)beta^2 h+epsilon`,
`E[epsilon|F_t,beta]=0`。

写 `z(beta)=(beta,beta^2/2)`。假设二次模型正确、条件二阶矩有限，且 `c,h` 是给定 `F_t` 的固定可测系数；或随机化满足 `beta independent (c,h) | F_t`，此时目标是条件均值 `E[(c,h)|F_t]`。在 sequential exchangeability/随机化成立时，该相应参数由条件矩识别当且仅当

**`G(F_t)=E[z(beta)z(beta)^T|F_t]` 正定。**

确定性 gate 在同一信息状态只给 rank-one G；只使用 `beta in {0,b}` 也只能识别组合 `bc+b^2h/2`。已有 paired baseline 时，至少需要两个不同非零幅度才能在这些同质性/随机化条件下分离斜率与曲率；若 baseline 截距也未知，则 `(1,beta,beta^2/2)` 需要 rank 3。它不识别单条轨迹随机的 realized `c,h`。非负 gate 不能用对称 `+/-delta` 免费消掉二次项；one-sided 差分含曲率偏差。

更一般地，日志若总写入，只观察 `Y(1)`：世界 A 可有 `Y(0)>Y(1)`，世界 B 可有 `Y(0)<Y(1)`，但事实分布完全相同，因果收益符号不可识别。序列 IPS/DR 需要支持、sequential exchangeability 与 propensity/outcome 条件，权重方差还可能随 horizon 乘法增长。模型自评或自生成未来只是 outcome-model 假设，不补充外部证据。

固定真实后缀上对内部状态做 write/no-write replay 是另一个对象：它可精确计算该 checkpoint、该后缀和 teacher-forced computational graph 的 paired 预测损失，但需要额外状态/前滚计算，也不标注事实是否过时，更不识别 edit 改变未来输入分布后的总效应。

## 7. finite horizon、TBPTT 与自由运行边界

任意有限 H 都可能给错误方向。令当前标量动作直接设 `x_1=a`，前 H 步总损失为 `(a+1)^2/2`，第 `H+1` 步损失为 `M(a-1)^2/2`。在 `a=0`，有限期导数为 `1`，而加入尾项后为 `1-M`；任意 `M>1` 使符号反转。倒计时变量可并入状态，所以反例不依赖非马尔可夫 oracle。

若单次 edit 的注入为 B，令未折扣的未来 loss gradient 为 `b_(t+j)=nabla_x ell_(t+j)`，并假设完整闭环 Jacobian（不是第3节冻结 Delta 左乘算子）的有序乘积满足

`||A_(t+j-1)...A_(t+1)||<=C rho^(j-1)`, `||b_(t+j)||<=L`,

则只有在 `gamma rho<1` 时，截断动作信用有条件尾界

**`||g_infty-g_H||<=||B||LC (gamma rho)^H/(1-gamma rho)`.**

逐步谱半径小于1、平均一步 norm 小或冻结 Delta 因子都不够。上一轮保护纤维含 neutral 方向时，除非 B 到未来 loss gradient 的该方向耦合为零、目标折扣/终止或另有可求和条件，这个几何尾界也不能使用。

对共享 `phi`，TBPTT 丢掉的是早期参数注入经完整乘积到后来 loss 的双重和；状态收缩不自动使未折扣、无限期 meta-gradient 可求和。离散路由、剪裁和采样还会破坏普通 pathwise 式。

teacher-forced 风险 `E_(P_data)L` 与自由运行 `E_(P_phi)L` 也不同。参数依赖轨迹律的导数除固定路径项外还含 distribution/score 项。两个模型可在**数据分布支持内**的所有 teacher-forced 上下文上完全相同，却在某个模型自由生成后才到达的支持外状态上分别吸收错误或立即恢复；相同 teacher-forced NLL 不控制长期 closed-loop 错误。没有 overlap、交互、合法 paired replay 或经独立验证的生成模型时，不能把 fixed-suffix gradient 称为总效应。

## 8. 最近工作、直接碰撞和剩余线索

本轮新发现的最近工作是 **Self-Generated Feedback Destabilizes Test-Time Training**（arXiv:2610.05076v1，2026-10-04）及作者仓库 `lingjivoo/ttt-ouroboros` commit `f7811f878679864e686c84abcd83dd05efdc0417`。它已经：

- 用 Fixed Generation、Recorded Replay 和 paired one-update 分离生成反馈、读入与持久写入；
- 把 `g_real^T Delta W` 与实际 paired harm 的关系作为 gradient-conflict **诊断**，不是提交选择规则；
- 用未来到达的独立真实文本比较候选状态与未写状态，按顺序验证并提交 Settlement；
- 在作者 `scripts/deferred.py` 中实际维护 pending updates、baseline/candidate probe、顺序接受、容量淘汰和生命周期计数。

因此“等未来真实文本到了再作 paired 验证”“pending 后选择提交”已是强直接基线，不能作为新候选。梯度内积是强诊断/近邻；同预算、部署合法的 projected-gradient selector 仍需另行查重和证明，不能被该实现一概判死。其结果是该论文设定的负/正证据，不是本项目实验结果；仓库配置还面向 CUDA、125M/760M/3B 或 Qwen3-4B 等资源，不能推断 2080Ti 可行。

更广泛地，DNI/synthetic gradients 已预测未来 gradient；RTRL/UORO/e-prop 已覆盖完整或近似 online sensitivity/eligibility；ACL/SRWM 已用自生成 value/target、key 与 rate pattern 形成 Delta rule，并以旧/新任务 meta-loss 训练；HOPE 已有 self-modifying multi-frequency memory；SEAL 已用 downstream reward 学 self-edit；learned optimizers/MAML/PES 已处理长 unroll 与 meta-gradient。前轮 `STEP2_RECURSIVE_RANDOM_METRIC_CONTROL.md` 已审查 GGN/DDP/DSSR 等，不重复计数。

保留但**尚未准入**的窄线索只有：对固定小维 Delta 动作族，用动作投影伴随在一次后缀反传后复用多个候选，并把可识别阶数/动作 span 作为选择 updater 自由度的显式成本约束。要成为候选，至少还需证明它在相同独立证据、动作容量和总计算下优于：

1. TTT Ouroboros Settlement / sequential paired validation；
2. `g_real^T Delta W` 一阶冲突诊断、可能的投影选择器及 GEM/A-GEM/OGD 类保护；
3. 同信息直接 action predictor 或普通远期 CE；
4. 固定 learned updater、ACL/SRWM/HOPE；
5. 只减小 gate、拒绝全部写入或增加外部真实文本。

目前没有这样的定理或原生结果，所以不分配 D 编号。

## 9. 原生测量与资源边界

- bAbI 全20 tasks/20000 与 LAMBADA-openai 5153 仍只提供 endpoint，不标注 action credit、write/no-write potential outcomes、外部知识有效性或 updater 改进。
- LongMemEval 的 QA 和 turn/session evidence labels 可测回答/证据引用，仍没有 ideal Delta action、counterfactual future law 或 meta-gradient。
- TTT Ouroboros 提供公开 causal-control/Settlement 实现和独立真实文本验证流程；它是最近机制/可行性来源，不自动成为本项目已资格化 benchmark，也不能把论文结果搬作本项目结果。
- WebShop/ALFWorld 有原生任务反馈，可测试 agent endpoint；要主张 updater 改进仍需相同信息、更新预算、matched write/no-write、失败分母和跨新任务效率，而不是只报成功率。
- 外部验证需要保留 pending state、额外真实 evidence、至少一次 baseline/candidate 评估；K 个顺序候选可能需要 K 次比较。投影近似需要一次完整后缀反传、激活保存/重算及每候选内积。所有额外 token、显存、CPU、反馈和状态必须计账。

这些资产/成本只做可行性边界；本轮没有设计完整实验矩阵或运行任何测量。2080Ti、100M/1B 每 arm/seed 仍只是后续背景，实际显存/时间未知。

## 10. 导航决定

操作路径：H05 完整闭环更新场 → F04 伴随/矩阵自由投影 → E04 动作子空间分解 → H06 表示下界与有限期反例 → B04 条件可识别矩 → G03 尾界。每一步条件已显式列出，不把操作名当贡献。

决定 **CONTINUE Step2, no admission**。本轮得到：

1. frozen path 上单个 rank-one Delta gate 的低维 exact eligibility；
2. 可执行动作空间投影信用的精确充分性；
3. 对全部动作精确评分所需 summary 维数的下界；
4. 标量延迟结果识别局部斜率/曲率所需的 intervention rank；
5. finite-horizon、TBPTT、teacher-forced/free-running 和事实/反事实的严格失败边界；
6. 一个直接的新碰撞：TTT Ouroboros 已实现独立证据上的 sequential Settlement 与 gradient-conflict 分析。

这些结果收窄了合法 updater：gate-only delayed credit 在一阶上低维，但学习方向需要支付更高信用/探索成本。它们尚未证明原创方法、Delta 优势或 RSI。计数维持 **5 历史 / 0 活动 / 0 科学准入 / 0 选择**；20/15 短缺不变。
