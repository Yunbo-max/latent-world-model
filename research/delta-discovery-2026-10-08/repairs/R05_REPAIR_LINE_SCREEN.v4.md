# R05 v4 修复线筛选：prefix-conditioned partial identification

状态：**第三次实质修订的进入记录；保留 v1–v3 原字节；不自动升级候选**  
直接父项：`R05_PARTIALLY_IDENTIFIED_VALIDITY_GEOMETRY.v3.md`，SHA256 `c8911d5910f96f73e4c7320827a048f57d33f2c2c00c0c2cbd7d172687d9325c`。  
本线预算：attempt `3/3`。本文件只决定为何值得做最后一次修订，不替代最终数学与来源复审。

## 1. 原问题与失败类型

v3 在固定动作前信息下，以

\[
p=E[r],\qquad \mu=E[Z],\qquad 0\le Z\le U
\]

给出 `m=E[rZ]` 的 sharp Fréchet/support 区间。若 `m_-=0`，仅凭这些汇总边际不能认证任何正 gate 对声明 surrogate 一致优于 no-write。这一 no-go 数学正确，但把部署时已经可见的 prefix heterogeneity 全部池化，因而存在**目标/构造不匹配**：一个全局常数 gate 不能表达“只在证据足够的上下文写入”。

这不是删掉反例，也不是把未知量改名。patch 改变可用决策类与合法信息：引入严格 `F_t` 可测的 prefix context `C`，允许 gate 为 `a(C)`，并逐层保留同一个耦合反例。

## 2. 为什么这次修订有真实数学增量

需要同时完成四件事：

1. 推导条件 sharp bounds `m_-(c),m_+(c)`，而非把无条件式逐字替换符号；
2. 说明何时逐层 worst case 可积成全局 worst case——需要 rectangular conditional ambiguity，而不是无条件交换 `sup` 与期望；
3. 给出 pooled no-write 失败但 contextual write 可认证的显式分层例子；
4. 把有限样本的 nuisance estimation、同步覆盖与细分 strata 代价写进失败边界。

若上述任一步不能成立，本线在第三次尝试后 park，不再循环改写。

## 3. 预期处置边界

- 数学价值：可能得到一个精确、可证伪的 conditional-control theorem。
- 新颖性风险：高。个体化 partial-identification policy learning、conditional LP、covariate-assisted sharp bounds 与 robust policy improvement 已是直接近邻。
- 测量风险：高。原生编辑 benchmark 不提供 `r`、`Z`、`m(c)` 或 paired write/no-write potential outcomes。
- 候选门槛：只有证明 Delta 结构带来现有 conditional-policy 方法没有的统计/计算后果，才可能进入 D；仅得到条件化闭式不计新候选。

