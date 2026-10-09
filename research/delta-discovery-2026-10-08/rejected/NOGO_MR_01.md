# NOGO-MR-01：规定 current-key 收缩下的最坏方向保留上界

推导者：`/root/minimax_retention_nogo`；状态：控制定理/否定路线，不计候选。日期：2026-10-09 UTC。未运行代码或实验。

工作在实数域。令 `k in R^d`、`||k||_2=1`、`alpha=1-beta`；状态为 `S in R^(d x p)`，value 为 `v in R^p`。要求 post-decay 旧状态差异的方形线性擦除子映射 `G in R^(d x d)` 对所有输入满足

`k^T G = alpha k^T`, `0<=alpha<=1`。

若最坏方向保留定义为 `r(G)=sigma_min(G)`，则其 maximin 最优值为

`sup_G sigma_min(G)=alpha=1-beta`。

上界不需要额外假设 `||G||_2<=1`：由 `G^T k=alpha k`，

`sigma_min(G)=sigma_min(G^T)<=||G^T k||_2=alpha`。

普通 Delta 擦除 `E=I-beta k k^T=alpha k k^T+(I-k k^T)` 的奇异值是 `{alpha,1,...,1}`，因此达到上界。故在“固定 `k,beta`、相同且对所有旧状态成立的规定 current-key 残差收缩 + 全局最坏方向保留”标准下，普通 Delta 达到 maximin 上界；不能靠斜投影、正交旋转或额外门在不改变问题的情况下普遍提高 `sigma_min`。

## 等号与反例边界

以 `k` 为第一基向量时，约束迫使

`G=[[alpha,0],[c,B]]`。

当 `0<alpha<=1` 时，`sigma_min(G)=alpha` 必须有 `c=0` 且 `sigma_min(B)>=alpha`；若还要求 contractive，则 `||B||_2<=1`。达到上界的映射可以在 `k` 的正交补上旋转或做受控变换，但从 `k` 向正交空间的 cross-coupling 会把最小奇异值严格压到 `alpha` 以下。`alpha=0` 时所有满足约束的方阵都奇异，最优值为 0，但不要求 `c=0`。

- `beta=1` 时 `alpha=0`，`G` 必然奇异；同状态维度的后续确定性线性左乘不能恢复已消去的秩。
- `beta=0` 且要求 contractive 时，达到 `sigma_min=1` 的实矩阵必须是固定 `k` 的正交映射。
- 一般实数 `beta` 的上界为 `sigma_min(G)<=|1-beta|`。
- 允许 expansive/nonnormal 映射仍不能突破该一步上界。若依靠后续扩张重新放大尚未消失的方向，其算子范数会放大相应扰动；条件数与有限精度误差需对具体乘积和实现另行分析，本定理不提供统一结论。
- 在冻结 `k,beta,v,D` 且 additive 项相同的两个轨迹间，additive write 对旧状态差异相消，因此不改变该齐次传播边界。若这些量依赖状态，必须审查完整 Jacobian。

## 与实际 Delta 顺序的关系

项目控制式使用

`F=E D=(I-beta k k^T)D`。

相对于 post-decay 状态的正确关系是 `k^T E=alpha k^T`，而完整因子满足

`F^T k=alpha D^T k`,

从而在任意维度匹配且 contractive 的 `D` 下

`alpha sigma_min(D) <= sigma_min(E D) <= alpha ||D^T k||_2 <= alpha`。

Decay 一般只会进一步降低最坏保留。在明确 `||D||_2<=1` 时，反序 `D E` 也满足 `sigma_min(DE)<=||DEk||=alpha||Dk||<=alpha`，却通常不实现同一个 post-decay current-key 残差规则；除非 `D` 与 `k k^T` 满足相应交换条件，不能交换两因子来绕过边界。

正交 `Q` 也不能在 `alpha<1` 时满足原约束，因为 `||Q^T k||=1`，而约束要求 `Q^T k=alpha k`。把当前误差旋转到隐藏方向可以保存总范数，但会让旧的正交分量混入当前读出，已经改变语义目标。

## 对候选设计的约束

合法改进只能改变比较对象或付出显式代价，例如：

1. 优化特定 query 分布、受保护子空间或有限时域输出风险，而非全局最坏方向；
2. 放松一步规定的残差收缩/插值；
3. 增加可读状态/外部证据或改变读出；
4. 接受扩张、噪声与数值条件代价。

这不会否定 D03 的特定 future-query 风险、D05 的有限精度表示或 D06 的门预算问题；它只否定“在相同规定 current-key 收缩下无代价提高全局最小奇异值”的普遍主张。作用域限于固定 `k,beta`、方形线性旧状态差分映射、同一收缩约束与全局 `sigma_min` 指标；不包括扩展状态、外部证据、读出改变或完整非线性网络。标准 Delta 达到该界也不代表它在语义保留、有限精度或未来任务风险上最优。

理论归属是奇异值变分定义和正交分解的直接推论，不宣称新定理。若存在满足 `k^T G=alpha k^T` 且 `sigma_min(G)>|alpha|` 的实矩阵，才反证核心结论。
