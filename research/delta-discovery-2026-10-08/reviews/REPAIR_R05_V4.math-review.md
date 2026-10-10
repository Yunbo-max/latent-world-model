# R05 v4 独立数学复审

- Reviewer：`/root/r05_v4_math_review`
- Artifact：`repairs/R05_PREFIX_CONDITIONAL_PARTIAL_ID.v4.md`
- SHA256：`8451497499d6b4a9fb13bbf5aca5464b85c3e27eaca6d50633460738c3acfbaf`
- Verdict：**PASS，限于 scoped conditional-control theorem；不是候选或效果结论。**

## 实际复核

1. 对每个 stratum，`ell=max(0,mu-(1-p)U)` 与 `h=min(mu,pU)` 是声明的 unrestricted Bernoulli × bounded-variable conditional coupling 类的 sharp bounds；完整 conditional `Z` marginal 的分位重排界也正确。真实 Delta 若含额外结构或 `U` 只是保守证书，文档已正确降级为外界。
2. 随机成本已修为 `Lambda=lambda||u||²`、`nu_c=E[Lambda|C=c]`，故条件 surrogate 的二次系数 `A_c=mu_c+nu_c` 在粗 context 内仍正确且量纲一致。
3. `A_c>0` 时 oracle `m_c/A_c`、区间 minimax-regret gate `(ell_c+h_c)/(2A_c)` 与最坏 regret `(h_c-ell_c)²/(4A_c)` 均由一维 quadratic Chebyshev center 得到，并自动落在 `[0,1]`。`A_c=0` 已分段，不再含 `0/0`。
4. `a_R` 与 baseline-safe gate `a_S=ell/A` 已明确分离。`a_S` 的 integrated worst-case difference 为 `-E[ell_C²/A_C]`（按 `A=0` 分段）；在 `P(ell_C>0)>0` 时严格为负，`ell=0` a.s. 时任何在 `A>0` 上非零动作均不能统一严格改进。
5. finite/countable `C`、conditional rectangularity、可测端点与 `E[A_C]<infinity` 足以让逐层 worst case 分离；一般标准 Borel 扩展被正确保留为 measurable-selection 条件项。共同参数、总量或平滑约束会破坏 exact separation，文档未越界。
6. pooling inequalities 与两层例子均成立：共同 `U` 下 Jensen 给 `E ell_C>=ell_pool`、`E h_C<=h_pool`；变化 `U_C` 的支持感知版本也正确，且没有与只知道 `U_max` 的不同信息模型混比。

## 已由复审促成的修正

初稿曾混淆 `a_R` 与安全释放门、把层内变化的 `u` 成本写成 stratum 常数、用 indicator 掩盖 `0/0`，且缺少可积性。最终 SHA 已全部修正，并保留同边际不同耦合反例。

## 未闭条件

非矩形歧义、连续 context 的可测选择/统计覆盖、有限样本 simultaneous confidence、common-path surrogate 到自由运行因果效应的外推、原生 joint labels 与同信息同预算优势仍未闭。数学通过不支持 D 编号、科学准入或实验有效性。

