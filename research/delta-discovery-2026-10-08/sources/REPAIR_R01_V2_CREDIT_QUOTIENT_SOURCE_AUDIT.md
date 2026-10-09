# R01-v2 信用商空间：来源与最近工作审查

状态：作者 `/root` 的 source audit；待最终 artifact 字节独立来源审查。对象为 `../repairs/R01_VALUE_SPAN_AND_CREDIT_QUOTIENT.v2.md`。只做论文/作者代码/原生资产静态核查，不执行项目、上游代码、模型、测试或评分。

## 1. 最直接碰撞：constrained exact lumping

Ovchinnikov, Pérez Verona, Pogudin, Tribastone, **CLUE: Exact maximal reduction of kinetic models by constrained lumping of differential equations**, arXiv:2004.11961v2（2020-12-15），全文 HTML：<https://arxiv.org/html/2004.11961v2>。

实际读取：

- Definition 1 定义 `y=Lx` 的 exact lumping；指定 linear observables 必须可由 y 恢复。
- §2 明确援引并使用判据：L 是 lumping 当且仅当 `row(LJ(x)) subset row(L)` 对所有 x 成立。
- Algorithm 1 把多项式 Jacobian 展成常矩阵 `J_i`，从 observable rows 出发闭包；Algorithm 2 求包含 observables 的最小共同 invariant subspace。
- 论文明确其贡献是 exact constrained lumping、minimal row-space closure 与高效算法，而不是近似神经网络信用传播。

实质比较：R01-v2 的 `ker L` 在离散 tangent operator 下不变，与一般 exact lumpability/quotient closure 同一数学骨架；因此“为指定 observables 找最小 exact quotient”不具备原创性。在本次 bounded CLUE 对照中未被显式实例化的是：对 Delta scalar-gate rank-one operator 展开的 `G=GQ` 非退化充要条件、把 transition gate covector 与 loss covector union 写成 value-width下界、time-varying右子空间的核包含障碍，以及带 full-X leakage 的目标信用界。这不是 fieldwide “only” 声明；仍需 task/goal-oriented reduction、time-varying projection 与 target-conditioned sensitivity 的更窄查重。

## 2. 作者实现固定版本与实际接口

论文链接的旧仓库已重定向到 `clue-developers/CLUE`。静态读取 GitHub REST，固定：

- repository: <https://github.com/clue-developers/CLUE>
- default branch: `master`
- exact commit: `0576e9b8477bc511e3fea29a3c296c5d30b688aa`（2024-09-12；当前作者维护/扩展版，不是 2020 论文原始快照）
- `clue/clue.py` blob `3226783022746ea3eeeddd207e95495be18a427b`
- `clue/linalg.py` blob `c774c461e4584870b070ef3ad99f3929ec609003`

读取的真实代码路径：

- `FODESystem.construct_matrices`: `polynomial/rational/random/auto_diff` 四种 Jacobian-derived matrix construction；`_construct_matrices_from_polys` 的 docstring 明确构造 paper Algorithm 1 Step 2 的 `J_i^T`。
- `FODESystem._lumping`: 调 `construct_matrices(method)`，把用户 `observable` 转成 vectors，再调用 `find_smallest_common_subspace`。
- `clue/linalg.py::Subspace.apply_matrices_inplace`: 从当前基向量出发依次右乘输入矩阵、吸收新独立向量，直到共同 invariant subspace 闭包。
- `clue/linalg.py::find_smallest_common_subspace`: docstring 明说返回包含给定 vectors 的最小共同 invariant subspace；有 rational/modular reconstruction 与 invariance check 分支。

代码 pin 只证明上述接口确实存在；本轮没有执行代码，也没有验证 `random/auto_diff` 分支对任意系统的 exactness，故这些分支不用于支撑 R01-v2 theorem。

作者实现与 R01-v2 的差异：它面向 symbolic/rational/polynomial ODE state lumping，维护 observable-preserving exact reduced ODE；R01-v2 面向沿一条 Delta 名义路径的离散 memory tangent 与 scalar credit，且显式保留 full nominal S。代码没有现成实现本对象的 causal prefix W、Delta gate/readout leakage证书或同预算 credit estimator。但这只是对象/接口差异，不能擦除 invariant-quotient 核心碰撞。

## 3. goal-oriented 与 time-varying reduction 是新增必查碰撞类

本轮补读 primary 摘要/正文入口，但未完成作者实现审查：

- Fischer et al., **MORe DWR: Space-time goal-oriented error control for incremental POD-based ROM**, arXiv:2304.01140：将 dual-weighted residual 用于 goal-functional error estimate 和在线 basis enrichment。<https://arxiv.org/abs/2304.01140>
- Fischer et al., **Adaptive space-time model order reduction with dual-weighted residual (MORe DWR) error control for poroelasticity**, arXiv:2311.08907：同一 goal-oriented DWR/POD 框架的扩展。<https://arxiv.org/abs/2311.08907>
- Cruz Varona and Lohmann, **Model reduction of linear time-varying systems with applications for moving loads**, arXiv:1607.02846：明确讨论 time-varying projection matrix 的额外自由度与导数项。<https://arxiv.org/abs/1607.02846>

这些来源足以把 `leakage -> scalar goal error`、自适应 enrichment 与 time-varying W 的一般思想降为强近邻类别，但本轮未读完全部公式/作者代码，不能据此宣称精确等价或完成原创性 closure。下一次只有在形成具体 structural interface 时才继续深查。

## 4. 其他已审近邻继续约束主张

R01-v1 source audit 已固定检查：RTRL、UORO/KF-RTRL/OK、SnAp、inexact-gradient/descent margin、EYM/rank-one online gradient及 Delta scalar-gate/JVP路径。结论继续适用：

- exact scalar credit 可由 reverse VJP/adjoint 得到，不要求重构 full tangent；
- online low-rank sensitivity近似已有成熟近邻，必须匹配总状态和计算；
- residual-weighted credit与下降裕量属于已知数值/优化骨架；
- 仅把这些写成 Delta 符号不构成新方法。

`G=GQ`、`C=CQ`、row-space union 下界和 time-varying kernel containment 是 Delta rank-one/operator 的清楚 specialization/elementary corollary；leakage-to-credit 是标准 goal-oriented/dual-weighted error transport 的 Delta 展开。它们可作为有用的具体 theorem/control，不应称为未覆盖的新机制。R01-v2 的可信残余差别只可能在 `Delta operator structure + observable-specific right quotient + causal/cheap structural interface` 的联合条件上。当前没有证据证明该联合构造未被覆盖，也没有成本/效果数据。

成本对照还必须包含单 focal scalar 的 plain forward-mode JVP/direct tangent，而不只 full RTRL 或 reverse VJP；总账包括 full S、U、W、G/C 获取、leakage/costate bound 与 prefix-only W 认证。

## 5. 原生测量与 measurement gaps

可复用已固定资产：bAbI 全20任务、LAMBADA、BABILong/RULER、LongMemEval、CITB/TRACE/SEAL。它们可测 endpoint QA、长上下文、跨会话更新或连续自编辑，但原生 scorer 不给：

- `row(G_j)` / `row(C_j)` 的跨 horizon union dimension；
- `||G_j(I-Q)||`、`||C_j(I-Q)||` 或有序 quotient-credit error certificate；
- W 是否只由合法 prefix 得到；
- 与 full reverse VJP、direct predictor、RTRL/SnAp 在相同 bytes/FLOPs 下的内部 credit error；
- “基础能力提升”与上下文/fast-weight适应的因果分离。

所以这些是 measurement gaps，不新造 benchmark、标签或 metric。未来若进入设计阶段，只能在既有原生样本上增加清楚标注的内部 instrument，并保留原 scorer；当前不设计完整实验矩阵、不执行。

## 6. 来源决定

- 一般 exact quotient / constrained observable-preserving lumping：**major mechanism collision / baseline**。
- Delta rank-one operator 的具体闭包充要条件、time-varying障碍、row-space union下界、leakage-to-credit界：**有用的对象级 specialization/theorem/control；不是已证明的新机制，原创性未闭**。
- 保持 full nominal S 是否带来同预算优势：**未知；可能被 full gradient/projection成本抵消**。
- 科学状态：**不准入、不编号、不选中**。

下一来源动作只在第3次修订出现具体 structural interface 后进行：查该接口与 target-conditioned sensitivity reduction、task-oriented model reduction、minimal realization/observability及神经网络 learned subspace 方法的公式和作者实现；没有新结构不做换词查重循环。
