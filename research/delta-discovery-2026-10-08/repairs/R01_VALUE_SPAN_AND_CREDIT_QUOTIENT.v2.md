# 修复 R01 v2：不压缩 nominal memory 的 Delta 信用商空间

状态：R01 的第 2/最多 3 次实质数学修订；已完成作者推导，待修改后字节的独立数学与来源审查。不是新 D 候选、科学准入、实现或实验结果。作者 `/root`，角色 `web_supervisor`。parent 为 main `13114650c049ac2cd757f4df6959c11880d6630d`。本文件是 `R01_VALUE_SPAN_AND_CREDIT_MARGIN.v1.md` 的 versioned child；不改写父文件、旧反例或旧 review。

## 1. 原问题 → patch

R01-v1 的固定右/value-span 闭包在数学上成立，但它有两个关键局限：

1. 结构实现 `S=ZV^T` 把 nominal memory 自由度从 `d_k d_v` 降为 `d_k r`；收益可能只是较小 value width。
2. 路径实现要求完整切向 `X` 和 residual `e` 落在同一固定 value span，原 flat-spectrum 反例可使所需 span 随 horizon 增长。

本次 patch 不再重构完整切向 `X`，也不约束 full-width `S`。只问：对指定未来写入决策，是否存在一个线性 quotient `L(X)=XW`，使该 quotient 的动力学和所需 scalar loss credit 闭合？这把“压缩模型容量”改为“压缩目标相关信用”。一般 exact lumping / invariant-subspace 原理已有强最近工作；本文件只推 Delta scalar-gate Jacobian 的必要充分条件、最小宽度、时间变化障碍和近似误差证书。

父字节：

- `repairs/R01_VALUE_SPAN_AND_CREDIT_MARGIN.v1.md`: `f5feb459fa62ce9cbe3d0568ca61b812cd9de44b4e80c672306a295c2b6b85d3`。
- `STEP2_CLOSED_LOOP_RANK_GROWTH.md`: `4839d87111588059f3db84e01f77de3aa836f15e7746c055beaae449da39a789`。
- `STEP2_PROJECTED_DELAYED_CREDIT.md`: `922ea86d3e5cdb83b703807f504bb9d77420b6635e0460d5013029f5e3b287cd`。

数学操作：由 `ker L` 不变性推 exact quotient；对 Delta 的 rank-one feedback 展开充要条件；由核包含关系推 time-varying quotient 障碍；再以 ordered residual recursion 给近似信用界。没有用操作名替代推导。

## 2. formal object 与信息边界

沿固定真实/teacher-forced suffix 的同一名义路径，考虑 R01-v1 已审查的 scalar-gate memory tangent：

`S_j in R^(d_k x d_v)`, `X_j=partial S_j/partial a`,

`J_j[X]=A_jX+k_j e_j^T <G_j,X>_F`,

其中 `A_j=(I-beta_j k_j k_j^T)D_j`，`e_j=v_j-(D_jS_j)^T k_j`，`G_j=grad_(S_j) beta_j`。若动作在后续 transition 还有直接使用，写成

`X_(j+1)=J_j[X_j]+B_j`。

这里仍是规定的 scalar-gate block；若 key/value/decay/query/updater state 也依赖 S，必须用完整 joint Jacobian，不能把下述条件自动外推。suffix 只可作训练/事后监督；部署时 W 或动作不得读取尚未到达的 token、答案或有效性 oracle。

取固定正交 `W in R^(d_v x r)`，`W^T W=I_r`，`Q=WW^T`，定义目标相关 quotient

**`L(X)=XW=:U in R^(d_k x r)`.**

注意 full nominal state S、full residual e、full tangent X 都可有任意 value 方向；只要求某个决策所需的 quotient 可闭合。

## 3. Delta quotient 的精确必要充分条件

分解 `G_j=G_jQ+G_j(I-Q)=:G_j^Q+G_j^perp`。Frobenius 恒等式为

`<G_jQ,X>_F=<G_jW,XW>_F=<G_jW,U>_F`。

令 `r_j=W^T e_j`，右乘 W 得

**`J_j[X]W=A_jU+k_j r_j^T <G_jW,U>_F+k_j r_j^T <G_j^perp,X>_F`.**

因此 quotient 对所有 X 精确闭合，当且仅当 `ker L` 在 J_j 下不变。证明不是口号：对任意 `R` 满足 `RW=0`，

`J_j[R]W=k_j r_j^T <G_j,R>_F`。

若 `k_j != 0` 且 `r_j != 0`，上式对全部 `R in ker L` 为零，当且仅当 G_j 正交于 `ker L`，即

**`G_j=G_jQ`，等价于存在 `H_j` 使 `G_j=H_jW^T`.**

这是非退化步的必要且充分条件。若 `k_j=0` 或 `r_j=0`，该步的 feedback 对这个 quotient 不可见，闭合可偶然成立；不能据此推出下一步或其他 readout 也闭合。

在 `G_j=G_jQ` 下，exact reduced recurrence 是

**`U_(j+1)=A_jU_j+k_jr_j^T<G_jW,U_j>_F+B_jW`.**

这里 B 本身不必落入 W；只需其可见注入 `B_jW`。与 v1 不同，e 也不必在 W，S 不必写成 `ZV^T`，所以 nominal Delta memory 仍有 `d_k d_v` 自由度。

### 3.1 scalar credit 还需 readout closure

设第 j 步 loss 对 memory 的 covector 为 `C_j=partial_(S_j) ell_j`。对所有 X，

`<C_j,X>_F=<C_jW,XW>_F`

当且仅当 **`C_j=C_jQ`**。充分性由 `<C_jW,XW>=<C_jQ,X>`；必要性取 `X=C_j(I-Q)` 即得。

所以 exact scalar action credit 可由 U 序列重构，需要两类不同条件：transition gate covector `G_j` 的 row/value span 被 W 包含，以及 audited loss covector `C_j` 的 row/value span被 W 包含。动力学闭合不自动等于目标闭合。

## 4. 最小宽度不是免费常数

令 `T_W={j: k_j != 0, W^T e_j != 0}` 为相对于候选 W 的非退化 transition 索引，并令 L 为所有需要以非零权重精确恢复的 loss/readout 索引。任何对全部 X 精确的固定 W 都必须包含每个 `j in T_W` 的 `row(G_j)`；要精确恢复规定 loss credit，还必须包含每个 `j in L` 的 `row(C_j)`。因此

**`r >= dim span( union_(j in T_W) row(G_j) union union_(j in L) row(C_j) )`.**

`T_W` 本身依赖候选 W；`k_j=0` 或 `W^T e_j=0` 的退化步不由该论证强制包含 `row(G_j)`。这既是构造建议也是针对所有 full tangents 的下界；若只要求 reachable tangent 子集，必要 span 可能更小。每个 G_j/C_j 单独低秩，不推出它们跨 horizon 的 union 低维。若非退化 transition 或实际计入的 loss 的 row directions 逐步在 `R^(d_v)` 中轮换，最小 r 可线性长至 `min(H,d_v)`；旧 flat-spectrum/rank-growth 障碍在“目标相关 row-space union”形式下仍存在。

一个确切成功特例是 gate 结构为 `beta_j=tilde beta_j(S_jW,z_j)`，且 audited loss/readout 对 S 的依赖也只经 `S_jW`。链式法则直接给 `G_j=H_jW^T`、`C_j=K_jW^T`；full S 仍可服务其他任务。这只证明该 gate/目标的 exact quotient，不证明 full model、其他 outputs 或基础能力可被压缩。

## 5. time-varying W 的旧反例复查

设第 j 步存 `U_j=X_jW_j`，下一步想要 `X_(j+1)W_(j+1)`。先只看 carry 项 `M_j(X)=A_jXW_(j+1)`。从 `XW_j` 对所有 X 恢复该项的精确条件是

**`ker(X -> XW_j) subset ker M_j`.**

当 `A_j != 0` 时，这等价于

**`range(W_(j+1)) subset range(W_j)`.**

证明：若 `A_j !=0`，取某个 u 使 `A_ju !=0`，并将任意 value row 放在形如 `u z^T` 的 X 中，即把矩阵核条件降为 `z^TW_j=0 => z^TW_(j+1)=0`。若 `A_j=0`，carry 项恒零，不施加该限制。在包含 rank-one feedback 的完整 step 中，正确充要条件是

**`ker(X -> XW_j) subset ker(X -> J_j[X]W_(j+1))`,**

还必须检查 G_j 与两个 W 的兼容性；特殊参数可使 carry 与 rank-one 项抵消，不能把 carry 条件误写成完整 J 的无条件必要条件。

在常见的 `A_j !=0`、无精确抵消情形，嵌套条件给 `W_(j+1)=W_jR_j`，carry 可由 `XW_jR_j` 传播。相同维度下任意旋转到不同子空间一般不闭合；在线扩张通常需要保存 union/additional state 或回看 full X。因而“每步学一个未来最优小子空间”一般不是合法递推，除非它只嵌套缩小、付出扩张状态、利用另行证明的特殊抵消，或重新计算完整切向。用未来 suffix 选择 W 只能做训练/事后分析，不能冒充 prefix-only deployment。

旧反例继续有效：若每步 G_j 或 C_j 的 row direction 进入新的正交 value 轴，固定小 r 无法 exact；若旋转 W 试图跟随新轴，则上一 quotient 不足以恢复新坐标。

## 6. 近似 quotient：显式 leakage，而不是删除 full X

不再假设 `G_j^perp=0`。定义只保留可见项的近似：

`hat U_(j+1)=A_j hat U_j+k_jr_j^T<G_jW,hat U_j>_F+B_jW`。

真实 `U_j=X_jW`，令 `D_j=U_j-hat U_j`，则精确误差递推为

**`D_(j+1)=bar J_j[D_j]+k_jr_j^T<G_j^perp,X_j>_F`,**

其中 `bar J_j[D]=A_jD+k_jr_j^T<G_jW,D>_F`。这表明 quotient error 仍由 full X 激励；不能只看 `hat U` 自证准确。

以下明确采用矩阵 Frobenius 范数、其诱导算子范数和向量 Euclidean 范数；因此 `||kr^T||_F=||k||_2||r||_2`，Frobenius 自对偶。若换其他范数，必须另证 compatible cross-norm 与对偶界。若

`bar gamma_j >= ||bar J_j||`, `gamma_j >= ||J_j||`,

并递推

`q_(j+1)=gamma_j q_j+||B_j||`, `q_0>=||X_0||`,

`d_(j+1)=bar gamma_j d_j+||k_j|| ||r_j|| ||G_j^perp||_* q_j`, `d_0>=||D_0||`,

则 `||X_j||<=q_j`, `||D_j||<=d_j`。这是 fixed nominal path 的 linear tangent certificate，不是整个非线性域的稳定证明。

将 `C_j=C_jQ+C_j(I-Q)=:C_j^Q+C_j^perp`。以 `<C_jW,hat U_j>` 估计 memory credit 时，

**`|<C_j,X_j>-<C_jW,hat U_j>| <= ||C_jW||_* d_j+||C_j^perp||_* q_j`.**

加权 horizon 的总信用误差可对 j 求和；若还有 direct action term、其他 joint-state block、名义路径、B、W 估计或 readout 近似，必须逐项加预算。exact costate 与 residual 的抵消可给更紧 a posteriori 标量界，但 exact reverse VJP/路径保存或重算可能已经是主要成本。

### 6.1 两个最小反例

取 `d_k=d_v=2`, `W=(1,0)^T`, `G=E_12`, `e=(1,0)^T`, 非零 k。令 `R=E_12`，则 `RW=0` 但 `<G,R>=1`，所以 `J[R]W=k !=0`：两个 full tangents 有同一 quotient，却有不同下一 quotient。任何省略 `G^perp` 的 exact 声明被直接否定。

再取 transition 已满足 `G=GQ`，但 `C=E_12`。动力学 quotient 闭合，`XW` 仍不能决定 `<C,X>`。所以 gate 低维与 loss credit 低维必须分别证明。

## 7. 可计算构造与同信息强对照

若架构本来就把 gate/readout 写成 `SW` 的函数，`G_jW` 可由该小接口的 JVP/VJP 得到，U 每个 focal scalar/action 只需 `d_k r` 状态；full nominal S 保留。diagonal A 时 reduced propagation 约 `O(d_k r)`，dense A 为 `O(d_k^2 r)`，另有 gate/readout接口成本。

若必须先形成 full G/C 再投影、用 full X 才能界 `G^perp` leakage，或为很多 focal actions 各存 U，则节省可能消失。W 本身要 `d_v r` 参数/状态，prefix-only估计还有 subspace drift 与校准误差。多个任务的 union row-space 可很快回到 full d_v。

必要强对照：

1. full reverse VJP/BPTT 或合法 checkpoint/recompute；
2. 对单 focal scalar 的 plain forward-mode JVP/direct tangent；
3. RTRL/SnAp/low-rank online gradient approximation，在同状态 bytes/FLOPs 下；
4. 同信息 direct action/credit predictor，不展开 tangent；
5. 普通 full-width Delta +固定 gate/readout bottleneck W；
6. v1 的真正小 value-width Delta，明确容量不同；
7. constrained exact lumping / minimal invariant-subspace算法作为一般 quotient baseline。

总成本必须同时计 full S、U、W、G/C 获取、leakage/costate bound 和 prefix-only W 认证，不能只报 `d_k r`。只在 structural W 接口使 transition/readout leakage小、union width长期小，且上述同预算对照不能取得相同信用时，才有实际优势线索。

## 8. 来源、可测性与决定

来源与作者实现核查见 `../sources/REPAIR_R01_V2_CREDIT_QUOTIENT_SOURCE_AUDIT.md`。CLUE 已给一般 constrained linear lumping 的 Jacobian-invariant row-space 判据和最小 invariant subspace 算法；本修订不能声称发明 exact quotient、observable-preserving reduction 或其最小闭包。RTRL/SnAp/低秩梯度与 R01-v1 的 credit residual/adjoint 近邻也继续有效。

现有原生 benchmark 可测 endpoint 与连续编辑表现，但没有 `G/C` row-space union、quotient leakage certificate、合法 W 选择或相同总计算 credit error 的原生 scorer。可以只读 instrument 既有样本；不能自造标签/metric或把 toy 反例分数写成效果。数学正确性由证明与独立反例审查决定；经验价值仍 unknown。

当前决定：**REPAIRED_CONDITIONAL_THEORY_LEAD / general quotient mechanism known / Delta-specific residual difference unresolved / experimental effect unknown / no candidate admission**。

这次 patch 实质解决了 v1 “必须压缩 nominal memory 容量”的局限：full S 可以保留。但它没有保证小 r、没有免费找到 causal W，也没有证明比 exact reverse credit 或 direct predictor便宜。下一次（最多第3次）只在获得具体的新结构或成本证据时继续：例如一个 prefix-computable gate/readout interface，使 `G^perp/C^perp` 可便宜认证且 union width 有非平凡上界。若只能 full-gradient 后投影或 W 随任务扩到 d_v，则 park 算法优势，保留本必要充分条件、下界与失效证据。

数量不变：历史5 / 活动0 / 科学准入0 / 选择0；pool_target=20、selection_target=15仍是探索与资格目标，不用本理论 lead 填数。未生成模型代码、完整实验矩阵或执行结果。
