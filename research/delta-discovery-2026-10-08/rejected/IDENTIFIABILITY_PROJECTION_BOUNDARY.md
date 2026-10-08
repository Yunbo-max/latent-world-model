# 固定线性读出的 alias/capacity 边界：不作为新方法

推导者：`/root/identifiability_candidate`；日期 2026-10-08 UTC。结论 `REJECT_AS_METHOD / retain_as_boundary_lemma`。

状态 `S∈R^(d×p)`、读出 `o(q)=S^Tq`。已有 query span 的正交基为 U，`Pi=I-UU^T`；post-decay 当前残差为 `e=v-Sbar^Tk`。要求增量同时满足 `U^T DeltaS=0` 与 `k^T DeltaS=beta e^T`。令 `z=Pi k`，逐列 Cauchy–Schwarz 给出唯一最小 Frobenius 范数解

`DeltaS*=beta z e^T/||z||²`，`||DeltaS*||_F=beta||e||/||z||`。

`z=0,e!=0` 时严格无解；若增量预算为 C，则可行当且仅当 `beta||e||/||z||≤C`。这只是几何可行性证书，不能决定应该释放哪个旧事实还是另存新事实。

全局约束 `A^TS=B` 有解当且仅当 `c^TB=0` 对所有 `c∈Null(A)` 成立；最小范数解为 `A(A^TA)^dagger B`。若 `A=U_A Sigma V^T`，其范数只在目标沿小奇异值方向有分量时按 `1/sigma_i²` 放大。没有状态范数、量化或噪声假设时，不能把这写成无条件有限 bit 容量定理。

显式假设 `||S||_2≤M`、state error `||E||_2≤epsilon_S`、query error `||delta q||≤epsilon_q` 时，单位 query 的读出扰动至多 `M epsilon_q+epsilon_S(1+epsilon_q)`。两 query 不确定集合相交时，不同目标的间距必须不超过两倍容许读出误差，否则观测不可辨识。无限精度下近 alias 仍可能靠无界状态范数插值，这正是必须公开动态范围假设的原因。

直接构造退化为已知保护投影；ridge 版本是 soft preconditioning/PDN 邻域；协方差版本是 KDN/Voltic 邻域；冲突后分槽是 Sparse Delta Memory/slots/routing。D01 现卡也已经使用相同 `k^TPi k` 分母。故本结果保留为后续设计约束和反例，不计活动候选。
