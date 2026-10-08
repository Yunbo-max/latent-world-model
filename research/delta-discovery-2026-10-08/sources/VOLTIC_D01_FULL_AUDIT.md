# Voltic 与修正版 Bayesian Delta mixture 对 D01 的审计

审计者：`/root/voltic_d01_audit`；集成者：`/root`。日期 2026-10-08 UTC。只做一手论文/作者源码静态阅读；未运行代码。

## Voltic v1

全文：arXiv `2610.05700v1`，2026-10-05，<https://arxiv.org/html/2610.05700v1>。实际读取 §3.1–3.5、Appendix A/B/D/F/G。单列潜状态满足

`z_t|z_(t-1) ~ N(A_tz_(t-1),diag(v_t))`，`x_t|z_t ~ N(k_t^Tz_t,s_t)`。

其精确滤波量为

`P_t=A_tU_(t-1)A_t^T+diag(v_t)`，`g_t=P_tk_t/(s_t+k_t^TP_tk_t)`，

`U_t=P_t-g_tk_t^TP_t`，`M_t=A_tM_(t-1)+g_t(x_t^T-k_t^TA_tM_(t-1))`（§3.1 Eq.1–3）。

Voltic-D 每 token 作 assumed-density moment projection，仅保留 covariance 对角；Voltic-Q 在长度 Q 的块内保留“对角减至多 Q 个 rank-one 项”，块边界只传对角（§3.3–3.4 Eq.7–9，Appendix B.3 Eq.31–34）。其低秩量是短块 covariance 修正，不是两个反事实 memory states 的差。

关键边界：`v_t,s_t` 是当前输入投影产生、由 sequence CE 端到端训练的参数；作者明确不从当前 mean state 的 predictive likelihood 在线推断这两个 rate。feature-space Gaussian 也不是 token likelihood。dense covariance 为每 head `O(N²)`；D/Q 降为 `O(N)`/`O(QN)`，主 memory 为 `NP`。

论文 v1 没有作者 code URL。对标题、arXiv ID、作者、Voltic-D/Q 作了定向仓库检索，没有定位作者仓库；这只表示本协议下未找到，不证明源码不存在，故无可固定 commit/function。

## Wilson–Nassar–Gold mixture 及纠正

实际读取 Wilson, Nassar, Gold 2013 PLOS Computational Biology，DOI `10.1371/journal.pcbi.1003150`，Methods 的 reduced model 与二节点 mixture；以及 2018 correction，DOI `10.1371/journal.pcbi.1006210`。

作者仓库现为 `d-r-b-o-b/2013WilsonEtAlPLoSCB`。固定 master `16f265808d7854cda6d19ecc48b5a7bf11fe1ad8`；修正算法 commit `7e717d41d8bbbc7a3d11444d4f60f0fc725f3aba`。关键 blob：`simulate.m` `c9c68e9742b6b7bc03df3d5bc8e72814552bc58e`；`makeTransitionMatrix_2017.m` `3e43ae0fc051ef1d3893695639d7cfc87e22edde`；错误旧版 `makeTransitionMatrix_2013.m` `cf744ae01a852934a08aa35c5a5bc3d6ddaeaedc`；两个 sufficient-stat update blob `20fdb7ae...`、`22089737...`。

每个 node 保存 run-length、Delta-like mean 和 posterior weight。源码实现 `pi^- = T pi`、`pi_i ∝ likelihood_i pi_i^-`，预测为 posterior-weighted node mean。2018 correction 指出原 change-point prior 错误进入过代码；修正后旧 Eq.48 假设及 Fig.8/9 二/三节点解析比较不再成立。任何近邻引用必须使用修正版。

## 与 D01 的比较与裁决

Voltic 是一份 Gaussian mean 加 covariance 近似，无离散 counterfactual 分支；D01 是一次不确定旧写入后的两种完整 token-predictive policy，其差在共享未来仿射路径下精确保持 `l e^T`。因此 Voltic 不直接包含 D01 的概率 mixture、rank-one state-difference compression 或 later-likelihood reweighting。

但 Voltic 已覆盖“变化与观测噪声应不同响应”“附加不确定性状态控制 Delta write”“低秩协方差辅助状态”。D01 不能宣称这些宽泛贡献。

Wilson mixture 是实质部分碰撞：Bayesian likelihood 重权多个 Delta predictors、后续观察改变旧估计在预测中的权重、posterior-weighted mixture 都已有。D01 的唯一残余是：**单个不确定矩阵写入在共同后续 affine Delta 动力学下，两个全矩阵分支差可精确压缩为 `l e^T`，并产生与两个显式完整状态的 token-probability mixture 相同的预测。** 最强基线就是两份完整状态；它预测完全等价，只少了状态压缩。

裁决：Voltic 为不同但高风险近邻，Wilson 为实质部分碰撞。recurrent low-rank ensemble/counterfactual fast-state 邻域尚未饱和，D01 维持 `INCONCLUSIVE_EXPAND_SEARCH`，不升级原创性或科学准入。
