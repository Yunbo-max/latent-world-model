# R05 v3 独立来源、原创性与原生测量终审

- reviewer: `/root/r05_source_review`
- assignment: 独立核对最终数学字节、primary/full-text 来源、作者实现接口、最近工作边界与 native measurement；未生成被审对象
- math artifact final SHA256: `c8911d5910f96f73e4c7320827a048f57d33f2c2c00c0c2cbd7d172687d9325c`
- source audit: `research/delta-discovery-2026-10-08/sources/REPAIR_R05_V2_PARTIAL_ID_SOURCE_AUDIT.md`
- source audit expected/observed SHA256: `67105cd08b1fe8d48fd8a99753fd47f1e8bc9c0ea4afb1c1ccde7f7c1aeb0014`
- verdict: **PASS — source/contribution/native-measurement scope**

## 证据核对

1. Puccetti & Wang (2015) 全文的固定边缘 Fréchet class、quantile/rearrangement 表示、supermodular 极值与 countermonotonic 下界直接支撑二元非负乘积 `rZ` 的极端耦合。审计把它列为已知 primitive，没有冒充原创。
2. Robust Bayes partial-identification 来源用于 Gamma-minimax/regret 邻域；Delage–Ye 只作宽泛 moment-DRO 对照，层级没有混淆。
3. EvEdit 被准确描述为 event description 加五个相关 QA/completion：前四可由上下文推断，第五 unknown；没有将 endpoint 类别伪装成内部更新机制标签。
4. 固定实现位置复核无误：ROME commit `0874014cd9837e4365f3e6f3c71400ef11509e04` 的 `experiments/py/eval_utils_counterfact.py::compute_rewrite_quality_counterfact`；EvEdit commit `9a09377517a22cd87f100621df52fc254b19800c` 的 QA/Completion 资产；sequential-edit commit `6e3ba9a87978a23b6db2676ba7540216bf5d4fd0` 的 `experiments/evaluate_unified_editing.py`, `DS_DICT`, `GLUEEval`；EasyEdit commit `4c109870955a4522ac3d7cf10ad00f34de8e4f0d` README 的 locality/portability schema。
5. 检索边界明确为有界审计，没有把未命中写成不存在性证明。

## 贡献与测量处置

sharp support/quantile bounds、Fréchet coupling、Gamma-minimax regret 与 moment-DRO 是已知邻域。只保留 `validity × Delta horizon sensitivity` 风险映射、可部署 gate 与 no-write 条件作为待查重的 specialization/corollary；状态为 conditional control，不是 D 候选。

CounterFact/ROME、EvEdit、EasyEdit 与 sequential editing 原生提供行为 endpoint，但不提供逐次 Delta 的 `r,J,Z,m`、propensity 或配对潜在结果，因此不能原生点识别该控制量。最终 v3 仅修正退化分支、排版与 reviewed/parked 处置，不改变来源、接口、benchmark 或原创性结论；最终集成字节复核通过。
