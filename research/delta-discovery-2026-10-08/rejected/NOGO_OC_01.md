# NOGO-OC-01：Chronological Commutativity No-Go

令 \(F_t(S)=A_tS+B_t\)，其中 \(A_t=(I-\beta_tk_tk_t^\top)D_t\)，\(B_t=\beta_tk_tv_t^\top\)。两个连续更新交换顺序的精确差异为

\[
F_j(F_i(S))-F_i(F_j(S))
=[A_j,A_i]S+(A_j-I)B_i-(A_i-I)B_j. \tag{1}
\]

因此只约束 transition commutator 不足以保护真实 revision；写入项本身也不可交换。增广仿射矩阵可同时表达两部分。

记 \(P_t=k_tk_t^\top,E_t=I-\beta_tP_t\)，并使用本项目中 \(D_i,D_j\) 均为对角矩阵、因而彼此可交换的条件。直接展开得

\[
[A_j,A_i]=
-\beta_iE_j[D_j,P_i]D_i+
\beta_i\beta_j[P_j,P_i]D_jD_i-
\beta_jE_i[P_j,D_i]D_j. \tag{2}
\]

对单位 key 与对角 \(D\)：

\[
\|[D,kk^\top]\|_2=
\sqrt{k^\top D^2k-(k^\top Dk)^2},\qquad
\|[P_j,P_i]\|_2=|\rho|\sqrt{1-\rho^2}.
\]

故 contractive decay 下可得对应三项上界；标量 decay 时精确 transition 交换范数与 \(\beta_i\beta_j|\rho|\sqrt{1-\rho^2}\) 成正比，在平行和正交 key 时均为零，而非随 cosine 单调增加。

关键反例：令 \(D_i=D_j=I,k_i=k_j=k\)。此时 \([A_j,A_i]=0\)，但

\[
(A_j-I)B_i-(A_i-I)B_j
=\beta_i\beta_jk(v_j-v_i)^\top. \tag{3}
\]

在一维取 \(k=q=1,\beta_i=\beta_j=1,S_0=0\) 时，按 key \(q=k\) 读取的值分别为 \(v_j\) 与 \(v_i\)。所以“让 transition 交换”会错过最典型的同地址真实修订。

对一组固定、外生的仿射 token 映射（重排后 \(A_t,B_t\) 不因先前状态改变），可把任意排列按每个 inversion pair 一次的相邻交换恢复为时间序。在 \(\|A_t\|_2\le1,\|B_t\|_F\le b_t\) 下，前缀状态由 \(M_\star=\|S_0\|_F+\sum_tb_t\) 控制，后缀非扩张，telescoping 给出状态绝对误差上界

\[
\sum_{(i,j)\in\mathcal I_\pi}
\left[M_\star\|[A_j,A_i]\|_2+
\|(A_j-I)B_i-(A_i-I)B_j\|_F\right]. \tag{4}
\]

它可作冻结特征仿射路径的代数/数值诊断，但不是 CE 或语义保证。若重排改变后续 feature、gate 或 key，需分析完整 Jacobian，本式不适用。

不存在由此自然导出的新并行方法：仿射摘要

\[
(P_2,R_2)\circ(P_1,R_1)=(P_2P_1,P_2R_1+R_2)
\]

虽不交换却满足结合律；精确 parallel prefix/scan 只需结合律并保留连续区间时间顺序。Parallel DeltaNet（arXiv:2406.06484v6, Secs. 3.1--3.2）的 ordered WY 与 DeltaProduct（arXiv:2502.10297v7, Sec. 4 Eq. 3）的有序 Householder 因子已是直接基线。commutator 对精确有序 scan 的正确性无必要作用，只诊断非法重排或近似重排的敏感性。若采用无序近似，式 (3) 反驳 transition-only 准则；即使利用 diagonal+rank-one 结构、预计算内积或小 Gram 表示，全 pair 诊断仍约需 \(O(C^2(d+m))\) 工作，对一般稠密仿射矩阵则会更高。

浮点结合误差可能随 balanced tree 深度改善，但结果可接近零，故没有无条件相对误差保证；WY/三角求解条件数也需另计。本记录未运行数值测试。

处置：保留式 (1)--(4) 为顺序敏感性诊断；淘汰“commutator-aware Delta”独立候选。强制交换会牺牲 revision，或退化为已有正交/slot 路线。
