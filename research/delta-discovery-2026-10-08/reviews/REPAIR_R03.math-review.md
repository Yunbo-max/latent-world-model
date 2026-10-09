# R03 v1 独立数学审查

- Reviewer assignment: `/root/r03_safe_logging_math`
- Artifact: `research/delta-discovery-2026-10-08/repairs/R03_PROTECTION_AWARE_LOGGING.v1.md`
- Final artifact SHA256: `af20487798b2c88039013c945c97778dad189266144a5436539d7d780467d7a3`
- Decision: **ACCEPT — conditional mathematical control; not a candidate**
- Required corrections: none

审查者从最终字节独立重算如下。

1. **维度与单步几何。** 对 `S:d_k×d_v`、`k,q:d_k`、`e:d_v`、`ΔS_a=α_aβkeᵀ`，`Δo_a(q)=α_aβ(qᵀk)e` 与 `d_a=α_a²β²(eᵀMe)kᵀG_pk` 的乘积和标量收缩均正确。
2. **保护平方风险。** 取 `r(q)=S̄ᵀq−y(q)`、`C_p=E[q r(q)ᵀM]`，直接展开得到 `ΔR_{p,a}=2α_aβ kᵀC_pe+d_a`；符号、因子二和维度正确。若 `R_p(S̄)≤ρ`，M-半范数 Cauchy 给出 `ΔR≤2√(ρd_a)+d_a`，从而 `d_a≤(√(ρ+B)−√ρ)²` 是 `B,ρ≥0` 时的充分条件，不是必要条件。
3. **AIPW 方差。** 固定/可预测 nuisance 下，线性 contrast 的 propensity-dependent 条件方差是 `Σ_a w_a²(σ_a²+δ_a²)/μ_a`，而 `−(Σ_aw_aδ_a)²` 与 `μ` 无关。正确 outcome model 的二元退化式也正确。
4. **二元解。** `p_N=σ_1/(σ_0+σ_1)`、`p*=Π_[ε,u](p_N)`、可行性 `u≥ε`（`U_1>0` 时等价 `b≥εU_1`）以及方差代价 `V(p)−V(p_N)=[σ_1(1−p)−σ_0p]²/[p(1−p)]` 均正确；双零方差需按稿中说明单独处理。
5. **多动作问题。** `Σg_a/μ_a` 在正 propensity 上凸。自由且 `g_a>0` 的坐标满足 `μ_a=sqrt(g_a/(λ+ηU_a))`；触 floor 的坐标固定后重求。floor-simplex 的最小线性损伤恰为 `εΣU_a+(1−Kε)min_aU_a`，因此稿中可行性条件是充要的；`g_a=0` 坐标按互补松弛处理。
6. **置信证书。** 固定有限动作集上的 Hoeffding-union bound 与 operator-norm 上界正确；数据依赖动作需独立样本、统一类界或 anytime confidence sequence 的限制已注明。它只控制覆盖事件上的 query-average/action-average 单步位移。
7. **传播范围。** 冻结 continuation 的 trace 公式维度正确；完整网络仅使用联合状态 Jacobian 与 Lipschitz-Jacobian remainder，没有把局部 rank-one 结论错误外推到未来 endogenous key/query/gate/token trajectory。

仍未闭合：保护分布和标签有效性是外部信息；`g_a` 需可预测 pilot 或保守上界；平均单步输出位移不建立逐查询、realized-action、累计、语义或完整网络安全；连续决策仍需依赖感知的顺序 OPE；尚未证明 Delta 几何损伤与 delayed-outcome variance 的关系，故没有 Delta-specific 样本复杂度优势。

审查结论：精确 rank-one 损伤、保护风险充分界与 positivity–damage 不可行边界成立；约束日志优化属于通用 safe experimental design。保存为控制，0 个新候选，并按稿中 reopening 条件 park。
