# 递归随机条件矩：论文、代码接口与原生测量审计

状态：2026-10-09 Step2 定向审计。只读公开论文、作者资料和既有原生 benchmark 记录；未执行项目/上游代码或下载数据。

## 1. 微分/变分可观测 Gramian

- Yu Kawano & Jacquelien M. A. Scherpen, “Empirical Differential Gramians for Nonlinear Model Reduction,” arXiv:1902.09836v2（2019-10-29；后发表于 Automatica 127, 2021, 109534）。
- Definition 3.2 Eq.(8) 的 differential observability Gramian 沿指定非线性轨迹积分 state-transition Jacobian 与 output Jacobian 的拉回；其变分系统式明确依赖 fixed trajectory，并在 LTI 情形退化为经典 observability Gramian。
- 这直接覆盖本轮 `sum_j J_(j<-t)^T C_j J_(j<-t)` 的结构语义；离散有限时域、输出曲率权重与 edit 注入 `B_t` 是本项目实例化，不是新 Gramian。
- 来源：https://arxiv.org/abs/1902.09836 。本轮未定位或执行一个与 Delta 接口相同的作者实现，不虚构 code pin。

更直接的离散接口是 Kazma & Taha, “Observability for Nonlinear Systems: Connecting Variational Dynamics, Lyapunov Exponents, and Empirical Gramians,” arXiv:2402.14711v7：§III Eq.(10) 给 `delta x_(k+1)=Phi_0^k delta x_0` 与输出变分，Eq.(13) 保留真实时间顺序的完整乘积，Eq.(14--15) 形成 `Psi^T Psi`，Appendix C Eq.(36) 写出非线性输出 Jacobian的加权和。作者仓库 `mhkazma/ObsNonSys-VarGram` 固定 commit `2bb5060454ddc63cd57681355fa6300fb9c6dc2e`；`AVarObsGram.m` blob `d2c548fe310b3e76463e5524a476199f5c482d8a` 构造 `Phi_0_k`、`Psi_0_k=C*Phi_0_k` 和 `Wo_M=Psi'*Psi`，`AVarDyn.m` blob `da73adbc53352c9a4eb24f8ae45b0bdb5677fe62` 联合积分状态与 Jacobian。其代码用线性 `C`，非线性输出扩展在论文中；仍是固定轨迹局部量，不解决未知未来分布的 prefix-only 估计。

## 2. GGN、DDP 与 iLQR 的曲率边界

- Schraudolph, “Fast Curvature Matrix-Vector Products for Second-Order Gradient Descent,” Neural Computation 14(7), 2002；Martens, “Deep learning via Hessian-free optimization,” ICML 2010；以及 Botev, Ritter & Barber, “Practical Gauss-Newton Optimisation for Deep Learning,” ICML 2017，给出神经网络 GGN 的 PSD pullback 与矩阵自由乘积背景。
- GGN 保留 output-loss curvature 经 Jacobian 拉回，通常丢弃 network/dynamics 二阶项；因此它不等于任意神经递推的精确 Hessian。
- Jacobson & Mayne, *Differential Dynamic Programming*, 1970；Tassa, Mansard & Todorov, “Control-Limited Differential Dynamic Programming,” ICRA 2014。DDP 的局部二阶展开含动力学二阶导数与 costate 的收缩；iLQR 常用一阶线性化动力学，省掉该张量项。
- 一个近期可核接口是 Haas-Heger & van den Berg, “Square Root Gauss-Newton iLQR,” arXiv:2609.21053v1，Eqs.(10),(12--20)：用动力学 Jacobian、`R_t^T W_t R_t` PSD cost metric、`F_t^T S_(t+1)F_t` 与 Schur-complement 型 backward update。相邻公开实现 `vroulet/ilqc` 固定 commit `62839d83f59a148cc60535c064c1780cdc818820`，`algorithms/algos_steps.py` blob `0ecf48c9b2185b0c11a3eff5dc316b522be5f1c4` 暴露 `classic_oracle`、`ddp_oracle`、`newton_oracle`、`lin_quad_backward` 与 `quad_backward_ddp`。本轮只读，未执行。
- 结论：本轮 `H=M+R`、GGN backward recursion 与“精确递推须加 dynamics curvature”均是这些标准对象的直接实例。PSD 方便求解不等于真实 Hessian 或稳定证书。

## 3. Synthetic gradients 与在线递归梯度

### DNI / Synthetic Gradients

- Jaderberg et al., “Decoupled Neural Interfaces using Synthetic Gradients,” ICML 2017 / arXiv:1608.05343。
- recurrent/BP(lambda) 部分用当前 hidden state 预测累计未来 loss gradient，并以随后得到的真实/bootstrapped gradient 训练 synthetic-gradient model；论文也给 critic 类比。
- 来源：https://arxiv.org/abs/1608.05343 。本轮未定位可固定的作者官方代码；只记录论文公式，不借第三方实现作作者接口或 code pin。
- 结论：`tilde g(F_t)` 预测未来 edit gradient 已被直接覆盖；预测 metric 是二阶扩展线索，不因增加矩阵输出自动成为新方法。

### RTRL 与 e-prop

- Williams & Zipser, “A Learning Algorithm for Continually Running Fully Recurrent Neural Networks,” Neural Computation 1(2), 1989：RTRL 在线递推状态对参数的完整偏导，在参数固定/定义匹配时无 TBPTT 截断偏差，但时间/内存昂贵。
- Ollivier, “Online Natural Gradient as a Kalman Filter,” arXiv:1703.00209v3，§3.1 Definition 11 / Theorem 12：Eqs.(3.2--3.5) 给 RTRL sensitivity，Eqs.(3.7--3.13) 把在线 Fisher、natural-gradient 更新与扩展 Kalman filter 连接。它联合了完整递归 Jacobian与当前观测信息 metric，但不是未知未来条件 Gramian；参数持续改变时 exact sensitivity 还需冻结/小步解释。
- Bellec et al., “A solution to the learning dilemma for recurrent networks of spiking neurons,” Nature Communications 11:3625, 2020，Methods/eligibility traces：把可前向递推的 eligibility trace 与 learning signal 分离；e-prop 的生物可行 learning signal 是近似，而 eligibility recursion 本身由局部 Jacobian 得到。
- 作者仓库 `IGITUGraz/eligibility_propagation` 固定 commit `efd02e6879c01cda3fa9a7838e8e2fd08163c16e`；`numerical_verification_eprop_factorization_vs_BPTT.py` blob `4cb33d52ea204cca3449b489d243ddea8e5c275f` 用 autodiff 核对精确 learning signal，`Figure_3_and_S7_e_prop_tutorials/models.py` blob `1e17fe926ecda60aeeff5e7907a245c901877723` 的 `compute_eligibility_traces` 生成 eligibility。它面向 spiking RNN，不是 Delta memory 的现成代码；本轮未执行。
- 结论：完整 Jacobian/eligibility 的在线维护及其近似已有直接近邻。任何 Delta 构造都必须比较 state size、JVP/VJP 次数、截断/低秩 bias，而不能只写“在线 Jacobian”。

### UORO

- Tallec & Ollivier, “Unbiased Online Recurrent Optimization,” arXiv:1702.05043。作者仓库 `ctallec/uoro` 固定 commit `135a057edcd83fda17db5785607cf4af1fb0cfdd`；`uoro.lua` blob `96134bb7c07fc60e242aa5711d44bf4fd8bb1e6b` 保存 rank-one `sbar/thetabar`，`UORO:forward` 结合局部 backward、forward differentiation、随机符号和范数缩放。
- 它给无偏但高方差的低秩 sensitivity/gradient estimator；求逆和 argmin 是非线性，故无偏 `hat M` 不推出无偏 `hat M^(-1)` 或最优 edit。它是任何“低秩因果 Jacobian sketch”必须比较的直接 baseline。

## 4. 递归 writer 与 future loss

- Shen & Li, “Decision-Sufficient State Representations: Measuring and Reducing Write-Time Regret,” arXiv:2609.32805v2，已在 `ACTION_SUFFICIENT_RANK_SOURCE_AUDIT.md` 固定正文与匿名代码接口。
- 其 candidate state 会沿真实 logged steps 用同一 writer 前滚，再由冻结 reader 的未来 reference-action likelihood 评分；这已覆盖“固定观测后缀评价递归 writer”的主要功能。论文报告的长 lag 失败是其设定下实证，不升级为普适 no-go。
- 它没有给编辑后自由运行 token/query 分布的反事实识别，也没有 Delta 条件 GGN 真值；所以本轮的 off-policy 边界仍是合法问题，但尚非新构造。

## 5. 随机探针与低秩恢复的限制

- Hutchinson trace estimator 与 Hutch++（Meyer et al., “Hutch++: Optimal Stochastic Trace Estimation,” SOSA 2021 / arXiv:2010.09649）估计矩阵 trace；它们不从少量 quadratic probes 无条件恢复完整矩阵、eigenspace 或 rank。
- randomized range finding 可在谱衰减、oversampling 与误差条件下近似低秩子空间，但这些是额外假设。故本轮仅允许把 JVP probe 写成 trace/quadratic-form estimator；不能把 probe 数量当作已识别的语义容量。

## 6. 原生对象与信息边界

- bAbI：官方生成器 `facebookarchive/bAbI-tasks` 固定 commit `ccd8fd6af76d35346109e7bb5f7de9138d055e01`；20 个 QA tasks 有 answer 与 supporting-fact sentence IDs。后者可作合成 relevance 诊断，但不提供 edit gradient、full-state Jacobian、future GGN 或 counterfactual rollout label；项目仍保留全20 tasks、20000 denominator。
- LAMBADA：Paperno et al., ACL 2016；项目沿 `EleutherAI/lm-evaluation-harness` 固定 commit `d6de81643928d653435c431bae19945d41d32520` 的 `lm_eval/tasks/lambada/lambada_openai.yaml`，`dataset_path: EleutherAI/lambada_openai`、`output_type: loglikelihood`、test split、最后词目标及 perplexity/accuracy。完整 denominator 5153；它不标注 evidence、edit、Jacobian 或条件矩。
- LongMemEval：沿已固定作者仓库 `xiaowu0162/LongMemEval` commit `9e0b455f4ef0e2ab8f2e582289761153549043fc`；500 questions，QA judge 与 turn/session evidence labels 可测最终更新回答和检索，但不提供 ideal Delta action、内部 Jacobian、teacher-forced vs free-running total effect 或 action regret。
- 任何从模型反传、局部 solve 或 teacher rollout 得到的 `g,M,u*` 都是派生标签。必须固定 teacher/checkpoint、后缀目标、horizon、动作族、probe/solve 精度与额外访问成本；不能冒充 benchmark 原生监督。

## 7. 覆盖表与决定

| 原子主张 | 最近工作覆盖 | 未闭残余 |
|---|---|---|
| 完整递归 Jacobian 拉回未来输出几何 | differential/variational observability Gramian | Delta 全状态边界与可承受结构 |
| PSD future curvature | GGN/iLQR | 精确 Hessian 的 dynamics/network curvature 与近似误差 |
| edit 时刻预测 future gradient | DNI/synthetic gradients | 校准、长 lag 与 direct-action 基线 |
| 在线维护完整 recurrent sensitivity | RTRL | 状态/参数维复杂度 |
| eligibility 与 learning signal 分离 | e-prop | 非脉冲 Delta 接口及近似 bias |
| logged future 前滚评价 writer | DSSR | edit 改变未来分布时的反事实识别 |
| 随机 probe 获得 full metric/rank | 不成立 | 只能在额外结构下估计 trace/子空间 |

审计处置：`mathematically valid synthesis / major component collision / no candidate admission`。本轮公式把三条旧线索——完整 Jacobian、联合条件矩、动作 regret——严谨接上，并给出可证伪误差界；但尚未发现一个在真实文本信息条件下既可识别、又比 direct action/CE/现有 critic 更有优势的 Delta 特有 estimator。无 D 编号，计数保持 5/0/0/0。
