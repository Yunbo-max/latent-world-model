# TRANSPORTED-INFLUENCE-LEDGER：精确控制恒等式，非独立候选

对冻结特征仿射 Delta \(S_j=A_jS_{j-1}+B_j\)，若事件 \(i\) 写入 \(u_ic_i^\top\)，定义

\[
r_{i,t}=A_tA_{t-1}\cdots A_{i+1}u_i.
\]

把旧值改为 \(c_i+\delta_i\) 后，

\[
S_t^{\rm revised}=S_t+r_{i,t}\delta_i^\top,
\]

这与在事件 \(i\) 修改后沿同一组未来 \(A,B\) 完整 replay 精确等价。多事件可维护 \(R_t=[A_tR_{t-1},u_t]\)。

该恒等式不构成 D07：

- \(r_{i,t}\) 是标准 forward sensitivity/eligibility trace；RTRL 的 \(J_t=B_t+C_tJ_{t-1}\) 与其同构，e-prop 也使用延迟学习信号乘前向 eligibility。
- 单事件且 \(\delta_i=(\pi_t-\pi_{t-1})e\) 时，它就是 D01 的 \(l_te^\top\) 修复项。
- 无事件身份时，当前输出残差诱导的线性映射 \(\{\delta_i\}\mapsto\sum_i(q^\top r_{i,t})\delta_i\) 一般至少有 \((M-1)d_v\) 维零空间，无法定位应修改的旧写入。
- 绝对新值需要保存旧 \(c_i\)、稳定事件身份和来源，状态变成 \(M(d_k+d_v)\) 加元数据，本质上退化为项目已有的 sparse exact-event memory。
- 对状态依赖的未来网络，正确传输是完整 \(DF_j\)，仅用 \(A_j\) 对有限修订一般只是线性化；若 Jacobian Lipschitz 常数为 \(H_m\)，误差由各步 \(O(H_m\|\Delta S\|^2)\) 经后续 Jacobian 放大项累加。只有未来动力学外生且仿射时该 replay 等价精确。
- 保存 \(M\) 条 trace 每 token 需 \(O(Md_k)\) 时间和内存；淘汰后不能再保证被淘汰事件可精确修订。

因此它仅保留为控制：冻结仿射路径下应与 exact replay 一致；当 \(q^\top k_t=0\) 但 \(q^\top r_{i,t}\neq0\) 时可修复普通 current-key Delta 无法直接触及的旧写入。最强对照是相同信息访问的 exact event replay、完整 RTRL trace 与 D01 单事件分支。核心机制已知且依赖额外事件身份，不占活动候选名额。
