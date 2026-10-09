# R01 v2 独立语义数学审查

审查者：`/root/r01v2_math_review`。assignment：只读攻击 root 集成的 versioned child，逐项检查维度、Frobenius 等式、quotient 充要条件、readout、最小宽度、time-varying W、误差递推与反例；未参与 subject 生成，未修改文件，未执行项目/模型/测试。

最终 subject：`research/delta-discovery-2026-10-08/repairs/R01_VALUE_SPAN_AND_CREDIT_QUOTIENT.v2.md`，SHA256 `93683c851ddee51fbfa197e6b088bda6968ab112b38aad351f351c851021d2b5`。

最初审查字节 `b9132df801abfb54479a51d8014ca56d39111e6449a6078b722e73cae8fdc75c` 得到 `ACCEPT_WITH_REQUIRED_CORRECTIONS`。审查指出两处过强表述：最小宽度 union 未排除 `k=0` 或 `W^Te=0` 的退化 transition；time-varying W 把 carry 项的核条件无条件写成完整 J 的条件，遗漏 `A=0` 和 carry/feedback 特殊抵消。writer 保留旧字节历史，修订后审查者重读最终字节。来源审查随后只补 plain forward JVP 对照与完整成本账，不改变定理；审查者再次按最终 SHA 确认。

结论：**ACCEPT / conditional mathematics accepted / general quotient mechanism known / novelty, cost, measurement and empirical effect unresolved / no candidate admission**。

## 独立重推

令 `L(X)=XW`、`Q=WW^T`。`<GQ,X>_F=<GW,XW>_F` 维度和迹循环均正确。对 `R in ker L`，

`J[R]W=k(W^Te)^T<G,R>`。

当 `k !=0` 且 `W^Te !=0`，此式对所有 R 为零，当且仅当 `G` 正交于 `ker L`，即 `G=GQ=HW^T`。因此所给 reduced recurrence 是 nondegenerate scalar-gate block 的精确 quotient；B 只需通过 `BW` 注入。

对 loss covector C，`<CW,XW>=<CQ,X>`。要对全部 X 等于 `<C,X>`，充要条件是 `C=CQ`；取 `X=C(I-Q)` 给必要性。两个 `2x2` 反例也成立：`G=R=E_12,W=e_1` 时 `RW=0` 但下一 quotient 非零；`C=E_12` 时 transition 可闭合而 loss 不可恢复。

最终宽度式只对 `T_W={j:k_j!=0,W^Te_j!=0}` 的 G 和实际非零权重 readout 的 C 取 row-space union，退化步不被错误计入；并明确这是假设对所有 full tangents exact 的下界，reachable subset 可更弱。

time-varying 部分先定义 carry map `M(X)=AXW_next`。正确条件是 `ker L_current subset ker M`。当 `A!=0`，用 `X=uz^T` 可化为 value-vector 核包含，等价于 `range(W_next) subset range(W_current)`；`A=0` 无此限制。完整 J 则需单独的 `ker L_current subset ker(X -> J[X]W_next)`，允许特别抵消。最终文件不再把 carry 条件冒充 full-J 普遍必要条件。

近似 recurrence 相减得到

`D^+=barJ[D]+kr^T<G_perp,X>`。

在明确 Frobenius/Euclidean 范数下，`||kr^T||_F=||k||_2||r||_2`，q/d majorizer 和 `<C,X>-<CW,hatU>` 的两项界成立。它们是固定名义路径线性 tangent certificate，不是非线性域的稳定性定理。

## 未闭条件

- 只覆盖规定 scalar-gate memory block；key/value/decay/query/updater state 的 full joint Jacobian 需另推。
- exact theorem 面向所有 full tangents；reachable-set quotient 可能更小。
- 没有 prefix-only、低成本 W 构造，也没有便宜的 `G_perp/C_perp` 认证。
- row-space union 可能增长到 `d_v`，小 r 无普遍保证。
- 还没有相对 exact scalar forward JVP、reverse VJP/BPTT、direct predictor、RTRL/SnAp 的 matched-total-cost 优势。
- 一般 exact lumping 已知；本 review 不认证原创性、软件或实验效果。

本 review 的 ACCEPT 只接受条件数学和反例边界，不产生 D 编号、科学准入、选择或实验验证。
