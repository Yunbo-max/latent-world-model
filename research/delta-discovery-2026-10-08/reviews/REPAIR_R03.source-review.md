# R03 v1 独立来源与贡献审查

- Reviewer assignment: `/root/r03_safe_logging_sources`
- Artifact: `research/delta-discovery-2026-10-08/repairs/R03_PROTECTION_AWARE_LOGGING.v1.md`
- Artifact SHA256: `af20487798b2c88039013c945c97778dad189266144a5436539d7d780467d7a3`
- Source audit: `research/delta-discovery-2026-10-08/sources/REPAIR_R03_PROTECTION_AWARE_LOGGING_SOURCE_AUDIT.md`
- Source-audit SHA256: `9cfe58925c73daa861f00ebb5534de47b9cec01c963e3a2e1786850568757067`
- Decision: **ACCEPT — useful control/theoretical boundary; not a candidate**
- Required corrections: none after final-byte rebind

独立全文/代码接口复核支持以下结论。

1. **直接机制碰撞。** SEPEC 已优化满足安全约束且降低 IPW/DR policy-evaluation 方差的 exploration policy；Safe Optimal Design 已构造相对 production baseline 安全、信息高效的 logging design，并覆盖 side information/linear contextual 扩展。Pacchiano et al. 的 stage-wise constrained bandit 用 cost UCB 作悲观约束；CLUCB 与 SEA 分别覆盖累计 baseline-relative safety 和 propensity + 高置信 OPE 部署；Wang--Agarwal--Dudík 覆盖 agnostic OPE、IPS/DR/SWITCH。因此“安全/成本约束 propensity 优化”不能登记为新方法。
2. **保护基线已存在。** 固定 commit/function 的 GEM、EWC baseline、A-GEM 与 OGD 已覆盖 replay-gradient inequality、Fisher penalty、参考梯度投影和旧输出梯度正交投影。把这些机制直接换到 S/k 坐标不构成新贡献；source audit 已避免把 GEM 仓库里的 EWC baseline 冒充 EWC 原作者仓库。
3. **可保留的 Delta 残余。** rank-one frozen-readout 证书 `d_a=α_a²β²(eᵀMe)kᵀG_pk`、平方风险交叉项/充分界及 overlap-budget 不可行条件是条件正确、可证伪的 Delta 特化理论结果。但尚无相对 SEPEC/Safe Optimal Design/硬投影的严格同预算统计或计算优势，也没有长期 coupled-state 或原生测量闭合。
4. **代码接口边界。** LongMemEval 固定作者 commit 的 knowledge-update/LLM-judge 接口只测终点 QA/检索，不含 propensity、counterfactual 或 protected-validity。SEAL 固定作者 commit 的 request handler、TTT helper 与 continual self-edit 流程测 LoRA/SFT 后表现及连续遗忘，不是 Delta randomized logging。SEPEC PMLR 页面未给 code link；Safe Optimal Design 虽有 supplementary ZIP，本轮未建立固定作者代码接口。公式级碰撞成立，但不能冒充完整实现审计。

未闭条件：决策时 protected set / `G_p` 可辨识性；adaptive actions 下 simultaneous/anytime `U_a`；语义风险标签与交叉矩；persistent stream 的 sequential OPE 和完整 coupled-state Jacobian；相对强对照的严格同预算优势；原生 propensity/counterfactual benchmark。实际效果仍为 unknown/unexecuted。

最终处置：`control, not candidate` 有充分依据；计数保持 5 历史 / 0 活动 / 0 科学准入 / 0 选择。
