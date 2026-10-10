# R05 v4 独立对抗复审

- Reviewer：`/root/r05_v4_adversarial_review`
- Artifact：`repairs/R05_PREFIX_CONDITIONAL_PARTIAL_ID.v4.md`
- SHA256：`8451497499d6b4a9fb13bbf5aca5464b85c3e27eaca6d50633460738c3acfbaf`
- Verdict：**PASS-AS-CONDITIONAL-MATH-CONTROL / PARK；不是 D 候选；实验未知。**

## 反例与隐藏代价复查

1. 旧反例未被删除：任一 stratum 内取 `p=mu=1/2,U=1`；`r=Z~Bern(1/2)` 给 `m=1/2`，`r=1-Z` 且相同 `Z` 边际给 `m=0`。条件化仍不能从边际点识别 joint moment。
2. 非矩形反例保留：三个等概率 strata、`A_i=1`、各投影 `[0,1]`，但共同约束 `sum m_i=3/2`。rectangular midpoint 外包络值为 `1/4`，真实共同约束下最大平均 regret 仅 `1/6`；故逐层 sharp projection 不推出非矩形原问题的 exact integrated supremum。
3. `A→0` 无 population 奇点，因为 `0<=h-ell<=A`，但插件比率可不稳定。最终稿要求合法次序置信集或 prefix-time floor/no-write 回退。
4. `C` 动作前可测只是必要条件；事后选择分层必须进入 sample splitting 与 simultaneous coverage。Cross-fitting 不会让潜在 `r` 可识别，样本最大值也不是合法 `U` 证书。
5. `a_R=(ell+h)/(2A)` 是 conditional interval-DRO/Chebyshev-center action；直接 joint `m_c` predictor 是同信息强基线。`a_S` 才是声明 surrogate 下的 baseline-safe release。

四项初审阻断——可积性、随机 `u` 的条件成本、common-path 改进范围、gate domain——均已在最终 SHA 关闭。保留适用域为 finite/countable `C`、端点可实现的 rectangular conditional ambiguity、固定 `{0,u}` 动作族、合法支持/矩、common-path quadratic surrogate 与可积动作前成本。

## Park 条件

attempt `3/3` 后 park。只有出现 Delta-specific 可解非矩形结构、合法 joint evidence/simultaneous coverage，或相对 direct contextual predictor/conditional DRO 的同信息同预算统计或计算优势证明时重开。

