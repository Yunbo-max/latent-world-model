# R05 v3 独立数学终审

- reviewer: `/root/r05_math_review`
- assignment: 独立复推并核对最终字节；未生成被审对象
- artifact: `research/delta-discovery-2026-10-08/repairs/R05_PARTIALLY_IDENTIFIED_VALIDITY_GEOMETRY.v3.md`
- expected/observed final SHA256: `c8911d5910f96f73e4c7320827a048f57d33f2c2c00c0c2cbd7d172687d9325c`
- verdict: **PASS — conditional mathematics; control, not candidate**

## 审查历史

v1 的标量主定理基本正确，但审查要求限定矩阵 sharpness、显式处理退化情形、消除写入前状态歧义、限定“有益”的风险语义，并补齐原子分位端点条件。v2 落实后，终审又发现 `U>0` 但 `A=mu+lambda_u=0` 时 oracle/regret 会出现 `0/0`，以及两处 TeX 反斜杠丢失。v1、v2 原字节均保留；v3 补齐一般 `A=0` 分支并重新终审。

## 最终复核

1. `S_t^-` 明确为动作前状态；`u=vec(beta k e^T)` 的维度与 Delta 写入一致。
2. `A=0` 时必有 `mu=lambda_u=m=0`，声明 surrogate 对全部 gate 相同，约定 no-write；全部除法公式明确限定 `A>0`。
3. 仅给 `p,mu,U` 时，`m_-=max(0,mu-(1-p)U)` 与 `m_+=min(mu,pU)` 的 support bounds 及二点构造 sharpness 正确。
4. 给完整 `Z` 边际时，分位积分上下界正确；原子内随机化与有限不可分割样本空间的可达性限制已声明。
5. `a*(m)=m/A`、区间中点 minimax-regret gate、最坏 regret 及 factorized gate 条件均正确。
6. `Aa<2m_-` 是固定正 gate 对声明局部正则 surrogate 统一严格优于 no-write 的充要条件；存在可认证正 gate 当且仅当 `m_->0`。
7. 不确定 `p,mu` 的保守外包络正确；Loewner 界是必要条件，directionwise sharpness 已限制在只保留标量投影信息的场景。
8. 自由运行 total effect、语义 validity、一般动作方向和同预算实效均未被这些局部结论证明。

## 处置

最终集成字节逐段复核通过；与先前通过版本相比仅把处置从 pending 改为 reviewed/parked。贡献身份仍是 Delta 标量部分识别/鲁棒门控的条件理论与 control；不能据此声称原创算法、科学准入或实验效果。
