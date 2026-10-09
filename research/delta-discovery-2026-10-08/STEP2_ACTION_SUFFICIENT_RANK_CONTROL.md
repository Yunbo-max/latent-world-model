# 第2步续接：决定充分性的低秩边界与 Delta 动作秩控制

状态：**已知理论的 Delta 专用推论与否定控制；不是新候选、原创性裁决、模型实现或实验结果。** 与 `STEP2_OBSERVED_PREDICTIVE_TARGET.md` 属同一条 Step2 调查线，不重复计数。

恢复基线：literal `main` `1b91721f5141de01ce1a167b5620aab270c0578f`。本轮没有运行项目源码、测试、训练、推理、评分、数据/模型下载或 GPU 作业。

## 1. 问题与决定

上一轮证明：在相同目标、动作族和因果信息下，压缩信息足够的最弱条件是完整信息最优动作已能由压缩信息决定。本轮补读后确认，这个一般命题已被 **Bayes-sufficient representation / Bayes quotient** 直接形式化；任务改变时的失效也已有 **loss-shift via Bayes quotients** 结果。更新后的定向检索又发现 2026-10-06 的 **Task-Sufficient Contraction**：它以完整可行动作 regret profile 定义 consumer-specific source，在有限动作下保持整条 one-step rate--regret curve，并对 affine feasible-action set 的二次风险给出精确投影商。因此不能把“只保留最优决定”、"保留可行动作的相对代价"或其 affine-quadratic 投影本身作为新理论或新方法。

更直接地，2026-09 的 DSSR 已对递归 writer 定义 reader loss、budget loss 与 write-time regret；在其设定中，方法和实验报告把候选 state 随真实 writer 向前滚动的评分能够预测结果，而固定-context评分会隐藏后续重写。它还报告长 lag 下 per-step credit assignment 失败。因此“用未来 reader loss 训练递归 writer”和“把 writer rollout 纳入评分”也不能作为本项目新意；这里不把其实证结论冒称一般必要性定理。

仍有一个对 Delta 有用、可计算但同样基于经典 reduced-rank regression 的控制：若 causal feature 通过一个宽度为 `r` 的线性表示预测局部最优 edit，所付出的未来二次风险恰等于一个任务加权算子的尾部奇异值能量。它回答“压缩状态至少要多宽”只在明确的线性、固定度量、固定任务族内成立；不证明一般语义容量，也不需要 diffusion。

## 2. 从 Bayes quotient 到可计算线性宽度

令 `X` 表示一次 edit 前可用的完整因果信息，`phi(X) in R^p` 为已声明、中心化且二阶可积的 causal feature，`Sigma=E[phi phi^T]`。动作 `a in R^d` 是当前允许的局部写入参数。固定正定风险度量 `M in R^(d x d)`，完整信息下唯一最优动作记为 `a*(X)`。若要把下式解释为原决策风险 regret，还必须显式假设

`L(a|X)-L(a*(X)|X)=||a-a*(X)||_M^2`

（允许再加与动作无关的项）。没有这个固定 SPD 二次 regret 假设，后面的量只是加权 action-distillation proxy；多任务公式逐任务继承同一条件。

一般决定充分性只要求 `a*(X)` 对压缩表示 `Z` 可测；这是 Bayes quotient 的直接特例。现在额外限制 `Z=R phi in R^r`、head 为 `WZ`。先做加权线性投影：

`B = E[a* phi^T] Sigma^{-1}`，`epsilon = a* - B phi`，

其中先假设 `Sigma` 正定；奇异时在其支持子空间使用 Moore--Penrose inverse。正常方程给 `E[epsilon phi^T]=0`。于是对任意线性动作算子 `C=WR`，

`E ||C phi-a*||_M^2 = E||epsilon||_M^2 + ||M^(1/2)(C-B)Sigma^(1/2)||_F^2`。

交叉项因正常方程为零。若 `M,Sigma` 正定，`rank(C)<=r` 与 `rank(M^(1/2) C Sigma^(1/2))<=r` 等价；任意秩不超过 `r` 的白化算子也能反变换成某个 `C=WR`。令

`L = M^(1/2) B Sigma^(1/2)`，其奇异值为 `sigma_1>=...>=sigma_s>0`。

Eckart--Young--Mirsky 定理给出

**`inf_(W,R) E||WR phi-a*||_M^2 = E||epsilon||_M^2 + sum_(i>r) sigma_i(L)^2`.**

因此：

- 在线性可预测部分上，宽度 `r` 精确足够当且仅当 `r>=rank(L)`；
- `sum_(i>r) sigma_i^2` 是压缩本身的最优额外风险，不是总风险；`epsilon` 是所选 feature/head class 的不可约项；
- `R,W` 不可识别：任意可逆 `G in R^(r x r)` 把 `(W,R)` 变为 `(WG^-1,GR)` 而不改动作；不能把单个坐标解释成已识别语义。

这不是新的矩阵定理：它就是加权 reduced-rank regression 加 Bayes-action target。它与 Task-Sufficient Contraction 的对象也不同但相邻：后者问哪些 source 状态在**所有可行动作的 regret profile**下等价；这里先固定线性 feature/head class，再问逼近最优动作映射的 rank--risk 曲线。前者证明“仅保留最优动作可能过粗”，后者的 SVD 尾和只是在额外线性/固定度量假设下量化有限宽度逼近，不能升级为新的充分性商。

## 3. 多任务/多 horizon 的共享表示秩

若任务 `tau=1,...,T` 共享 `phi,Sigma`，各自有常数正定度量 `M_tau`、权重 `pi_tau>0` 和最佳线性动作 `B_tau phi`，而每个任务允许自己的 head `W_tau`、共享同一表示 `R phi`，则堆叠

`L_stack = [sqrt(pi_1) M_1^(1/2) B_1 Sigma^(1/2); ...; sqrt(pi_T) M_T^(1/2) B_T Sigma^(1/2)]`。

同一低秩逼近论证给出共享表示的最优总动作误差

**`sum_tau pi_tau E||epsilon_tau||_(M_tau)^2 + sum_(i>r) sigma_i(L_stack)^2`.**

当所有 `epsilon_tau=0` 时，精确共享线性决定充分的最小宽度是 `rank(L_stack)`。在保留既有 row blocks 及其权重、只追加正权新任务块时，rank 与固定 `r` 的尾能量不减；若重归一化全部任务权重，则没有这个单调结论。新任务位于既有 row space 时，精确所需 rank 不增加，但对 `r<rank(L_stack)`，奇异值和尾能量仍可能变化。只有当前 `r>=rank(L_stack)` 时，继续增宽才不会因这个线性瓶颈改善；新增独立 row-space方向会提高精确所需宽度，并可给固定窄表示带来正尾能量。该预测仍需合法 estimator 和自然对象，不能把样本 SVD 当总体充分性证明。

## 4. 对 Delta 的精确含义

沿上一轮固定 value 方向的可写族 `delta S=a e^T`，完整信息动作是

`a*(X)=(||e||^2 C_X + lambda I)^(-1) h_X`，

其中 `C_X=E[qq^T|X]`、`h_X=E[q(e^Tg)|X]`，且 `e`、baseline、future law、动作族必须与被比较对象一致。若一个 causal feature 的线性 head 预测该 `a*`，上节的 `L` 才是 **Delta action-observable operator**。

三个边界很重要：

1. 若只允许 `a=alpha k`，动作输出是一个标量 `alpha*`。输出秩至多 1；高维 state 并不由这个动作族本身要求。困难可以是条件标量函数高度非线性、信息缺失或估计昂贵，而不是输出动作秩高。
2. 放开到 `d` 维写入方向时，action rank 可升至 `d`，但 value-orthogonal future residual 仍不可达。更宽的 action representation 不会突破 `delta S=a e^T` 的 value-side 限制。
3. 真实 CE 的局部动作使用完整路径 `K` 和 GGN/真实 Hessian条件。若条件度量 `M_X` 随历史变化，风险为 `E[(C phi-a*)^T M_X(C phi-a*)]`，不再化为一个固定白化 SVD。无约束线性正常方程是

   `E[M_X(C phi-a*) phi^T]=0`，

   或向量化为 Hessian `E[phi phi^T tensor M_X]`。rank 约束下是加权低秩问题；把 `E[M_X]` 与普通 covariance 分别平均一般错误。这与 Step2 的“有效性和未来 query 几何必须联合”结论一致。

## 5. 任务/损失迁移：零源风险不能保证目标风险

决定充分性是目标和动作族相关的。令 `X=(U,V)`，源任务最优动作只依赖 `U`，目标任务最优动作只依赖 `V`，而 `U,V` 独立。表示 `Z=U` 对源任务可 Bayes-minimal，却对目标任务没有信息；把目标平方损失尺度乘任意常数即可令目标 excess risk 任意大。故不存在只由“源任务充分”推出的分布无关迁移保证。对递归 writer 还需声明未来任务族和闭包：一个只对当前 edit 最优的 quotient 可以删掉当前不用、但更晚 query 才需要的事实；没有后续观测重新提供它时，未来风险严格增加。

一个合法但很弱的稳健边界是：若对所有 `x,a` 有 `|L_target(a|x)-L_source(a|x)|<=delta`，则同一动作规则的目标 excess risk 至多为其源 excess risk 加 `2 delta`。这个上界需要统一风险接近，不能由共享输入分布或 source probe success 自动得到。Bayes quotient 的 loss-shift 结果已经给出更直接的严格 refinement 障碍；本反例不计新贡献。

## 6. diffusion 的必要性边界

固定二次局部动作风险只需要决定 `a*` 所需的条件矩/动作映射；低秩定理只涉及二阶对象，没有因多模态 future 自动需要 diffusion。有限标签 log loss 的 Bayes action本身是完整条件概率向量，严格 proper scoring rule 也要求条件 law；但本项目这里的动作是低维 edit `a`，不是直接报告完整 future distribution。

只有当声明的动作/目标确实是分布生成或抽样、且其损失不能由有限 elicited property/条件矩决定时，分布模型才可能提供必要对象。即使如此，还必须证明简单 autoregressive CE、显式 mixture 或 conditional density estimator 不足，并计入采样/teacher/推理成本。当前没有这样的必要性证明；diffusion 继续是可选方法，不是主创新或默认解。

## 7. 自然测量与成本边界

- bAbI 全 20 tasks 和 LAMBADA 5153 项提供 native endpoint，但没有 `a*`、`B`、`M_X` 或 representation-sufficiency 标签。可以从模型/teacher 派生局部动作，却会引入模型版本、horizon、求解误差、full-path autodiff 和额外信息访问；它不是 benchmark 原生真值。
- LongMemEval 的 500 个问题含 `knowledge-update` 类，官方 QA evaluator 对生成答案作 yes/no 判定，能够测最终更新行为；数据同时提供 `has_answer` turn labels 与 `answer_session_ids` retrieval labels，可测 turn/session evidence recall。它仍不标注单步 ideal edit、action rank、内部删除或 Bayes quotient，因而不能单独验证上述机制。
- probe 成功只说明选定 probe、有限样本和优化下的可恢复性；probe 失败可能来自容量、样本或优化。不能把 probe 当总体 sigma-algebra inclusion。

常数度量下形成 `d x p` action operator、做 full SVD 的成本至少为存储 `O(dp)`，dense 分解约 `O(min(d p^2,d^2 p))`；随机/历史依赖度量还需估计 `pd x pd` Kronecker 正常方程或使用矩阵自由近似。完整 CE teacher 动作另需未来激活、JVP/VJP/solve 和数据访问。2080Ti 适配、显存和耗时均未测；100M/1B 每 arm/seed 只是后续资源背景。

## 8. 处置与下一合法动作

**处置：不分配 D 编号。** 一般决定充分性与任务迁移分别被 Bayes-sufficient representation / loss-shift 直接覆盖；Task-Sufficient Contraction 更直接覆盖完整 regret-profile source、整条 one-step rate--regret 曲线及 affine-action quadratic quotient；线性宽度公式被 reduced-rank regression/Eckart--Young 覆盖；decision-focused learning 与 posterior Bayes action map 覆盖了直接优化决定这一训练原则；DSSR 又直接覆盖递归 writer 的 future-reader-loss、forward rollout 与长 lag credit assignment。Delta 专用写法是有用的控制和测量设计约束，不形成科学准入。

保留的真正未闭问题是：在相同 causal 信息和总计算下，是否存在自然文本中稳定、可估计且显著的 **非标量、非固定度量 Delta action operator**，其低秩尾能量能预测 native endpoint 的失败，并且优于普通 CE、同信息直接 action predictor、增宽 state/MLP 和已有 preconditioned/TTT 方法。若没有原生可测量对象或最近工作差异，继续保持 measurement gap，而不是自造标签/benchmark。

计数保持 **5 历史 / 0 活动 / 0 科学准入 / 0 选择**，20/15 短缺不变。
