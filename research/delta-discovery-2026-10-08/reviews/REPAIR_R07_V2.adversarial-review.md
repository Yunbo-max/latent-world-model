# R07 v2 独立最终字节对抗审查

- reviewer identity: `/root/r07v2_adversary`
- assignment: 独立只读对抗复核 R07 v2 最终 artifact；未参与集成写入
- artifact: `research/delta-discovery-2026-10-08/repairs/R07_COUPLED_DIRECTIONAL_MARGIN.v2.md`
- exact SHA256: `4259fee0afb25db2624972efcbd7ed6658b5aec16af84163583b8c14b96fdee3`
- verdict: **PASS for the stated fixed-policy/common-exogenous finite-horizon local theorem/debugging-control scope; not a free-running causal certificate or candidate admission**

较早字节的独立对抗审查发现并要求修正不定曲率下的 `q=0,h<0` small-step 边界及 LaTeX 呈现字节。最终 SHA 已全部修正。完整状态、一/二阶递推、costate-weighted dynamics Hessian、显式 action 依赖项、不定曲率分支、余项证书、score 一二阶项、finite-horizon 尾部、Bellman continuation、离散路由与 free-running 因果边界均正确限定；旧 truth-versus-action 和 signed-protection 反例未删除。JVP/VJP/二阶传播成本及 direct action-value、DDP/iLQR、RTRL/e-prop、Bellman/POMDP 与 OPE 强对照已计入。

本审查不证明 prefix-only `q,h,kappa` 可得，不证明尾界、自由运行因果效果、原创 updater、原生测量闭环或实验收益。将该 lineage 作为 attempt 2/3 的 parked conditional control、candidate delta zero、empirical unknown，处置合理。
