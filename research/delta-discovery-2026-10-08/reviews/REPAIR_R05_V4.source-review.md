# R05 v4 独立来源、原创性与原生测量复审

- Reviewer：`/root/r05_v4_source_review`
- Repair SHA256：`8451497499d6b4a9fb13bbf5aca5464b85c3e27eaca6d50633460738c3acfbaf`
- Source audit：`sources/R05_V4_PREFIX_CONDITIONAL_SOURCE_AUDIT.md`
- Source-audit SHA256：`3d431f1e0f3367014950a55641780fb11785fd54a89527becaf5e5d951619a24`
- Verdict：**PASS_FOR_CONDITIONAL_CONTROL / DIRECT_CONTRIBUTION_COLLISION / NATIVE_MEASUREMENT_GAP / NOT_D**

## 实际核查

- Ben-Michael `2506.12215v2` 的 §2.1 式 (1)–(2) 已把总体 bounds 写成协变量条件 LP 解的期望，§3 覆盖 conditional nuisance 的 debiasing/cross-fitting，§4 覆盖 partially identified value 的 policy learning。
- D'Adamo `2111.10904v3` 覆盖协变量条件的 individualized partial-ID policy、minimax risk/regret、surrogate score 与 orthogonal/sample-split estimation。
- Ji–Lei–Spector `2310.08115v3` 覆盖 pretreatment covariates 收紧部分识别界及 conditional nuisance、uniform-valid inference 和 selection 代价。
- Kallus–Zhou NeurIPS 2018 在 uncertainty set 正确指定时覆盖相对 baseline 的 personalized minimax-regret safety。其 ambiguity set 与 R05 不同，故是功能近邻而非精确公式同构。
- Christensen–Moon–Schorfheide 与 Kitagawa–Lee–Qiu 进一步确认 partial-ID minimax/fractional decision 属于既有决策论对象。

因此已覆盖的贡献骨架是“conditional identified set → individualized robust/minimax policy → nuisance estimation”。本轮未定位到完全相同的 Delta 二变量闭式，故正确表述为**贡献/功能层直接碰撞，Delta-specific closed-form specialization**，不能声称首个、新范式或精确逐式复现。

父审计固定的 ROME/CounterFact、EvEdit、EasyEdit 与 sequential-editing 接口只暴露 efficacy、paraphrase/generalization、locality、portability/event QA 和连续编辑 endpoints；不提供动作前 `p_c,mu_c,U_c,m_c`、随机 propensity 或 paired write/no-write potential outcomes，不能直接验证 sharpness 或 minimax regret。

## 未闭条件

Ben-Michael、D'Adamo、Ji 作者实现尚未固定 commit；Kallus–Zhou 关联代码接口已读但 commit 未锁定。原生机制 benchmark、同信息同容量同计算优势与实际效果均未知。来源支持 attempt `3/3` 后 park、candidate delta `0`。

