# R01 v1 独立语义数学审查

审查者：`/root/repair_final_math`。实际 assignment：独立审查 root 集成的 repair，而非参与该 subject 的初始生成；限定数学、条件、成本与旧反例，不执行项目/上游代码或软件测试。角色 web_supervisor。

最终 subject：`research/delta-discovery-2026-10-08/repairs/R01_VALUE_SPAN_AND_CREDIT_MARGIN.v1.md`。实际读出字节 SHA256：`f5feb459fa62ce9cbe3d0568ca61b812cd9de44b4e80c672306a295c2b6b85d3`。最初审查字节 hash：`1b1cf42bf5d41f974e9dfe4950d2a8a3ef4ff3d56e4f203946dd0214d6897d51`。初稿仅有 K/Q 上界序列使用 <= 的歧义；审查建议使构造等于或大于右端，writer 已修改为等式构造、真实导数范数 <= 上界，并对 B 给区间 supremum。本人重新读回该完整修改段并重新计算最终 hash。本 review 不沿用旧 parent 的 pass。

结论：**CONDITIONAL_MATH_SUPPORTED；算法/理论贡献差异未闭；实验效果未知**。没有发现最终版的实质代数错误。这是两条可关联的修订条件构造，不是两个新科学候选或已有效 updater。

## formal_object

S、X、G 的维度均为 d_k × d_v，k 为 d_k，e 为 d_v，V 为 d_v × r，Y 为 d_k × r。A=(I−βkkᵀ)D 左乘，不能倒换 D；作者保留了正确时序。G 是 gate 对 pre-decay S 的导数，e 对 post-decay S 定义，两者并不混淆。

信用部分的 z 是全联合状态，X 是一个标量动作的状态切向，c 是相配 loss covector。它不是所有 updater 参数的完整 sensitivity，也不是事实有效性或自由生成收益。固定真实 teacher-forced suffix 的 F_H(a) 是明确数学对象，可微性/输入路径未在公式中偷换。

## operations_and_conditions

固定右投影与任意左 A 相容，因为 (AX)Π=A(XΠ)，不要求不同 A 交换。通过该不变量归纳证明闭包，不依赖 singular-value 衰减。泄漏部分使用精确线性切向差，而不是把不同 nominal state 的 Jacobian 当同一个。信用部分先展开有序 products、再交换有限求和，最后用对偶范数；有限步部分由整个步长区间上的 Taylor 积分余项支撑，不能用单点 Hessian 或 GN 代替 M。

## derivation

独立重推 X⁺=DX+βk(−XᵀDᵀk)ᵀ+k eᵀ⟨G,X⟩ 得 A X+k eᵀ⟨G,X⟩。若 X=YVᵀ、e=Ve_r，则两项分别为 AYVᵀ、ke_rᵀVᵀ⟨GV,Y⟩，所以所写 reduced map 及 rank≤r 成立。结构性 S=ZVᵀ、v=Vw 给 residual=V(w−ZᵀDᵀk)，即 S⁺=Z⁺Vᵀ 恒等式，即使 k/D/β 对联合状态求导，固定 V 的 memory block 仍封闭；它不证明 updater 其余状态封闭。

投影/余空间两块都读 ⟨G,T+R⟩。相减后 E⁺=J[E]+ke_Rᵀ⟨G,hatX⟩，符号与 forcing 正确。若 G(I−Π)=0，余空间切向与 G 正交，因此 projected component 可自治。这一成功特例并非完整切向精确。

信用 residual η_j=hatX_j−J_jhatX_{j−1}−B_j 给 E_j=J_jE_{j−1}−η_j；product 展开保留正确 order。对每个 loss 求和后，初值系数为 λ_0=Σ_jP_(j:1)ᵀω_jc_j，第 i 个 residual 系数为负的 λ_i=Σ_(j≥i)P_(j:i+1)ᵀω_jc_j。故 g−hatg=λ_0ᵀE_0−Σ_iλ_iᵀη_i 正确，含 j=i 的 identity。Frobenius 或所定范数必须与 dual matching。直接 a-loss derivative 在两式完全相同才取消，文中明确额外近似需预算。

独立算 sign-flip 反例：⟨diag(−ε/2,1),diag(1,ε)⟩=ε/2，而删尾后为 −ε/2；相对 tangent error=ε/√(1+ε²)→0。它确实说明相对 state error 不保证动作符号，不是经验失败证据。

当 g∈[hatg−δ,hatg+δ]，gd≤hatg d+δ|d|。二次余项给所写 majorizer；h=|hatg|−δ>0 时，方向 −sign(hatg)，沿该方向的一维函数为 −hu+Mu²/2，最优合法 u=min(h/M,R)。R>0 时严格下降，裁剪界 −hu/2 正确。h≤0 时零步最小；M=0、R=0、baseline gate 已在边界等情况已单列。曲率链式项 L K²+G Q+2N K+D 及 z'' 的 mixed terms 正确。最终上界序列修订已排除随意选择过小 K/Q 的歧义。

## assumptions

我另构造两个解析边界以攻击条件，而没有运行模型或数值测试。第一，取 d_k=d_v=2、Π=diag(1,0)、S=0、k=e_1、β=1/2、D=I，令 v(S)=e_1+S_11 e_2、X=E_11。名义 e=e_1 在 span，但完整 dv[X]=e_2，得到 X⁺=(1/2)E_11+(1/2)E_12，故只有 nominal e-span 不能封闭完整 feature-dependent network。subject §2.2 正确保留这个边界。

第二，同一 Π、k=e_1、v=e_1、S=0、D=I，gate β(S)=σ(4S_12)，G=E_12，初始 X=R=E_12、T=0。完整反馈生成 E_11，projected recurrence 从零仍为零。因此 hatX≠XΠ 确可发生；G(I−Π)=0 会排除这个机制。subject 泄漏交叉项不可删。

固定 V 必须与焦点 action 无关，在线改变 V 要加 Z dVᵀ。基于未来 suffix 事后挑选 V 只能作训练分析。γ 是名义 J 的合法 operator 上界；全区间曲率界需 interval suprema，点导数不够。loss/readout/critic、nominal path、B/J、随机选择或 free-generation law 的近似均会产生额外误差。最终版均明确这些义务。M 与 δ 的便宜、非松估计目前未给出，它是 practical gap 而不是已完成方法。

## method_expression

可计算构造确实存在：存 Y，递推 reduced tangent；或用投影 recurrence 与 leakage forcing 控制 E；把 residual bound/costate bound 转成 scalar credit interval，再求一维 majorizer 的合法步长。也允许 BPTT/其他估计器输入同一 scalar margin，故 A/B 是必要数学连接而非两个名字拼接。

然而 nominal full S 未消失，固定结构 Z 本质削减 value width。计算 GV 一般 O(d_k d_v r)，dense D 的乘法 O(d_k²r)，多个焦点/参数敏感度另乘其数量；full costate/interval bounds 可抵消低秩账面收益。B 最后 O(1) 不代表整体 O(1)。这些成本区分支持作者保留同容量 reduced Delta、直接动作预测及完整 reverse-mode 为强对照。

## prediction_and_falsifier

正确预测是给定条件下固定右-span invariance、受 leakage/product/readout 预算约束的信用误差，以及 margin 和 interval M 合法时该 fixed-suffix F_H 的下降。旧 effective-rank parent 的 X_H=α^(H−1)Σ_(i=1)^HE_ii 保留 H 个正交 residual directions，r<H 的 V 不满足 exact-span 前提；它仍给相对误差 √((H−r)/H)，没有被修复文件删掉或否认。

有效性不由这些证明推出。若自然路径无合适 prefix V、δ大于信用、M无法合法控制或算 bounds 比完整反传贵，当前算法优势主张不成立/未支持；条件理论仍正确。若 exact-span 实现另有出空间 tangent 或合法误差/curvature certificate 被真实导数违反，则相应数学/实现合同被证伪。bAbI/LAMBADA endpoint 不标注内部 tangent/curvature truth，本 review 不补造测量。

## closest_alternative

本文是 invariant-subspace reduction、linear error transport、goal-weighted adjoint residual 与 smooth inexact-gradient majorization 的 Delta 对象展开。它修复了无条件低秩与仅按 tangent relative error 判信用的错误外推，但证明不建立原创性。普通同宽度 Delta+BPTT/RTRL、直接 action predictor、TBPTT/完整 VJP、保守步长或保持基线是必须比较的同信息替代。没有凭本文新增 oracle、额外反馈、能力提升、长期学习效率或 RSI 证据。

未认证：近邻覆盖完整性与 source implementation fidelity（另有 source review）、数学之外的 candidate admission/selection、现有模型局部或区间常数、训练/部署可行性、软件正确性、显存/时间实测、native benchmark 效果或跨任务改进。此次仅实际文件/哈希读取与解析推导审查；没有 project execution/test/scoring。
