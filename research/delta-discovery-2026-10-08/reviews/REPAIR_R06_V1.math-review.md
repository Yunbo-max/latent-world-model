# R06 v1 独立最终字节数学审查

- reviewer identity: `/root/r06_final_math_review`
- assignment: 独立只读复核 R06 v1 最终 artifact；未参与集成写入
- artifact: `research/delta-discovery-2026-10-08/repairs/R06_SELECTIVE_VALIDITY_AUDIT.v1.md`
- exact SHA256: `9f2d3ab00aa6c036c5cde10f18cddb73fa1a120545f43d0f83f8df0da7cdc8a3`
- verdict: **PASS for stated conditional-control scope**

复核过程先在 SHA `e93830a...` 发现两项需修错误：无 clipping 的 `pi=rho Z/EZ` 示例与统一 positivity floor/上界不兼容；`U_A=0` 时 no-write bridge 会除零。集成 writer 修订并生成上述最终 SHA 后，reviewer 重新读取全部字节并通过。

最终检查：

1. `u=vec(beta k e^T)`、`Ju`、`Z=||Ju||²` 与所有 moment/variance 的维度一致。
2. 在线 prefix-only proxy 与事后动作无关 `Z^0` 分离；审计选择 filtration 与可预测 propensity 合法。
3. HT/AIPW 的设计无偏性、固定非适应 Bernoulli 方差、适应性 martingale quadratic variation 限定正确。
4. HT 的 `Z²q` 与 AIPW 的 `Z²q(1-q)` KKT/Neyman 分配、成本/clipping/fixed-B 条件正确。
5. positivity、预算、延迟 censoring 与 audit-feedback policy shift 边界成立。
6. `Y`（事实真实性）没有与 `r`（理想二元动作）偷换；bridge 明确要求 `0<L_m<=m_r<=A<=U_A`。
7. 选择泄漏与自由运行长期代价反例成立。
8. `O(1)` 估计账本与 Jacobian/proxy/真实标签的主要成本分开。

审查只接受内部条件数学，不证明原创性、原生测量可得或实效。处置 `park as known two-phase/Neyman/importance control; no D number` 合理。
