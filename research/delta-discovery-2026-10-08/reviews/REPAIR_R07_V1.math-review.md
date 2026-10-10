# R07 v1 独立最终字节数学审查

- reviewer identity: `/root/r07_final_math_review`
- assignment: 独立只读复核 R07 v1 最终 artifact；未参与集成写入
- artifact: `research/delta-discovery-2026-10-08/repairs/R07_VALIDITY_TO_ACTION_MARGIN.v1.md`
- exact SHA256: `e7e40477dc9eab96f7df18e9c30cba0bcbd65a4d9c67939d80f92579258be1ad`
- verdict: **PASS for stated fixed-reference quadratic / local sufficient-control scope**

审查先在较早字节发现并要求修复：预测反号阈值的符号、`kappa=0,h=0` 除零分支、延迟真实性标签不能回填同次动作，以及 `Y=0,h_0=0` 时 `b` 可非零但不参与 `q_0`。集成 writer 修正后，reviewer 对上述最终 SHA 重新读取全部字节并通过。

最终检查：

1. `U=beta k e^T`、`u=vec(U)`、`J_nu,J_pu` 及所有内积/范数维度一致。
2. `Delta_Y(a)=2a(c-Yb)+a^2h_Y` 与 `q_Y=Yb-c` 的符号正确。
3. 连续最优 `clip(q/h,0,1)`、存在正 gate 的 `q>0`、二元 full-write 阈值 `q>h/2` 与连续 full-write 最优阈值 `q>=h` 已严格区分。
4. 半正定 surrogate 的 `h=0` 退化分支准确，无除零漏洞。
5. `r=Y` 的标签分层充要条件与 simultaneous interval 充分条件使用正确的最坏端点。
6. 两世界反例可通过改变保护残差、保持方向与曲率不变实现，风险差分别为 `-1` 与 `+1`。
7. 三阶余项证书、正根、`kappa=0/h=0` 分支和 full-step 条件均正确。
8. Delta 专门化的 `c`、保护曲率、新 probe `b` 与曲率公式维度及系数正确。
9. 预测阈值已修为 `c=b-h_1/2`；延迟 `Y`、prefix visibility、固定路径与自由运行/OPE 边界均明确。

审查不证明该局部标签是实际长期 ideal action，不证明原创性、原生测量、长期安全或实验效果。处置 `parked conditional control; no D number` 合理。
