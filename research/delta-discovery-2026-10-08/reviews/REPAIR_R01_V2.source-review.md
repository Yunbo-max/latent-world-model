# R01 v2 独立来源、原创性与原生测量审查

审查者：`/root/r01v2_source_review`。assignment：只读检查最终 repair 与 source audit 的 primary formulas、实际作者实现、最近工作、总成本和原生测量；未参与 subject 生成或修改，未执行上游/项目代码、测试、模型或评分。

最终绑定：

- `repairs/R01_VALUE_SPAN_AND_CREDIT_QUOTIENT.v2.md`: SHA256 `93683c851ddee51fbfa197e6b088bda6968ab112b38aad351f351c851021d2b5`。
- `sources/REPAIR_R01_V2_CREDIT_QUOTIENT_SOURCE_AUDIT.md`: SHA256 `3ea1ebcce6d15bf085b150d7af872143ec07c8587af3b2dd75e72c448d51862f`。

最初字节审查为 `ACCEPT_WITH_REQUIRED_CORRECTIONS`；artifact/source 分别为 `b9132df801abfb54479a51d8014ca56d39111e6449a6078b722e73cae8fdc75c` 与 `1935ed1b150803d4c1ab82756078b47e6d324e088ede943ed393d18daa0a7616`。writer 按六项必改修订后，审查者重读最终字节并给 **ACCEPT**。

## 已确认碰撞与接口

CLUE arXiv:2004.11961v2 的 Definition 1/§2/Algorithms 1–2 已给 constrained exact lumping、`row(LJ(x)) subset row(L)` 判据和包含指定 observables 的最小共同 invariant row-space closure，并追溯 Li–Rabitz。因此 exact observable quotient、kernel invariance 和 minimal closure 是已知一般机制。

作者维护仓库 `clue-developers/CLUE` 固定 commit `0576e9b8477bc511e3fea29a3c296c5d30b688aa`；`clue.py` blob `3226783022746ea3eeeddd207e95495be18a427b`，`linalg.py` blob `c774c461e4584870b070ef3ad99f3929ec609003`。`construct_matrices`、`_lumping`、`find_smallest_common_subspace`、`Subspace.apply_matrices_inplace` 的记录准确。该 commit 是 2024 作者维护/扩展版，不是 2020 论文快照；random/auto_diff 分支未被本审查验证为 theorem 证据。

RTRL/full JVP/VJP、SnAp、adjoint/goal-weighted residual 是必要近邻。新增 primary 入口 MORe-DWR arXiv:2304.01140、2311.08907 与 linear time-varying MOR arXiv:1607.02846，使 goal-functional residual、basis enrichment 与 time-varying projection 成为明确必查碰撞类；本轮未完成其作者代码/全公式审查，故不宣称精确等价。

## 贡献边界

`G=GQ`、`C=CQ`、row-space union 下界与 time-varying kernel containment 是一般 lumpability/信息充分性的 Delta operator specialization；leakage-to-credit 是 goal-oriented/dual-weighted error transport 的 Delta 展开。可保留的价值是 full nominal S 不被压缩、对规定决策 quotient 的显式充要式、两个小反例和 full-X leakage recursion。它们是具体 theorem/control，不是已经证明的新机制。

原创性只有在出现 `Delta rank-one structure + target-specific right quotient + causal cheap structural interface` 的联合构造后才值得重开。现在没有 prefix-only W、长期小 union-width、便宜 leakage certification 或 fieldwide originality closure。

## 成本与测量

强对照必须包括单 focal scalar 的 plain forward JVP/direct tangent、reverse VJP/checkpoint、direct credit predictor、RTRL/SnAp、full-width Delta+bottleneck W 和一般 lumping。总成本必须计 full S、U、W、G/C 获取、leakage/costate bound、activation replay 与 prefix-W 认证，不能只报 `d_k r`。

bAbI/LAMBADA/LongMemEval/CITB/TRACE/SEAL 等原生 scorer 只能给 endpoint/连续编辑后果，不给 `row(G/C)` union、合法 prefix W、leakage certificate 或同 FLOP/byte credit error。内部 instrumentation 不等于 native scorer；当前无实验效果。

## 最终决定

**ACCEPTED_CONDITIONAL_THEORY_CONTROL / general mechanism known / useful Delta specialization / originality unresolved / feasibility conditional / empirical effect unknown / no D admission**。

未闭义务：只有出现具体 structural interface 后，继续 target-conditioned sensitivity、task/goal-oriented MOR、minimal realization/observability 与 learned subspace 的窄查重和作者实现；证明 causal prefix W、cheap `G_perp/C_perp` certificate 与非平凡 union-width界；做同信息、同 bytes/FLOPs/activation replay 的完整成本比较；分开 endpoint 与 mechanism measurement；scalar-gate block 失效时重推 full joint Jacobian。本 ACCEPT 不产生候选、科学准入、选择或实验验证。
