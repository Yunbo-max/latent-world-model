# 修复 R01 v1：value 子空间闭包与写入信用的误差裕量

状态：已完成的修订推导，最终独立审查见同轮 reviews；不是新 D 候选、科学准入、实现或实验结果。作者 /root，角色 web_supervisor。恢复 parent `4c15ce42cc8fee0808a444e079f9a0c09417dbf6`。用户于 2026-10-09 17:08:50 Europe/London 要求先 debug、修改并重推。保留全部原字节、反例和旧 review，本文件是 versioned child，不反向改写旧结论。

## 1. 为什么修这两条

原问题是：真实未来反馈怎样改善 Delta 写入，而不靠未来泄漏、免费记忆或额外计算解释收益？已有两条正确否定并未否定整个问题。

| 修复线索 | 原确切失败 | 类型 | 保留正确部分 | 本次 patch |
|---|---|---|---|---|
| R01-A：闭环低秩信用 | state-dependent gate 每步添加新 value 方向；即使严格收缩，归一化切向可有 H 个相等奇异值 | 假设不足；不是旧代数错误 | 完整导数含反馈项；收缩不推出低相对秩 | 改由固定右/value 子空间的精确闭包及泄漏界判断是否能低秩 |
| R01-B：可用写入决策 | 小绝对切向误差可能大于信用信号；高秩也未必影响所需标量动作信用 | 目标/近似标准不匹配 | 完整 ordered-Jacobian residual bound 与动作投影仍有效 | 把误差界转成真实方向导数区间和有限步损失裕量；没有裕量则保留原动作 |

这不是两个独立新方法。A 提供一种可核的信用近似；B 判断该近似是否足够支撑一次决策。B 也可接受 full BPTT、TBPTT 或其他有合法误差界的估计器。每条本次为第 1/最多 3 次实质构造尝试；没有新 delta 不重复修订。

父产物及实际 SHA256：

- `STEP2_CLOSED_LOOP_RANK_GROWTH.md`: `4839d87111588059f3db84e01f77de3aa836f15e7746c055beaae449da39a789`。
- `STEP2_EFFECTIVE_RANK_TRUNCATION_CONTROL.md`: `09bceabb9fc8e53dcf7ed877a4b9bc174af093b7406b7f9b51be62d3e60326f2`。
- `STEP2_PROJECTED_DELAYED_CREDIT.md`: `922ea86d3e5cdb83b703807f504bb9d77420b6635e0460d5013029f5e3b287cd`。

数学操作：P14/H06 原反例定位条件缺口 → F03/G06 子空间不变量 → C04/G04 有序误差传播 → C05/D01 误差区间下的有限步优化。没有把操作名字代替推导。

## 2. R01-A：保留完整 scalar-gate feedback 的精确子空间闭包

S 是 key-by-value，`S_j in R^(d_k x d_v)`。固定同一外部输入、同一名义路径，当前只有 scalar gate `beta_j=b_j(S_j)` 依赖该记忆；未来 k/v/D 外生固定。定义

`bar S_j=D_j S_j`, `e_j=v_j-bar S_j^T k_j`,
`A_j=(I-beta_j k_j k_j^T)D_j`, `G_j=grad_(S_j) beta_j`。

焦点标量动作 a 的完整切向 `X_j=partial S_j/partial a` 在焦点注入后满足

**`X_(j+1)=J_j[X_j]=A_j X_j+k_j e_j^T <G_j,X_j>_F`.**

门导数保留，不冻结闭环。取一个预先固定或仅从焦点前合法前缀确定、之后冻结的正交 V，`V in R^(d_v x r)`, `V^T V=I_r`, `Pi=VV^T`。假设 `X_0=X_0 Pi` 且沿这条名义路径所有 `e_j=Pi e_j`。令 `X_j=Y_j V^T`，则

`A_j X_j=(A_j Y_j)V^T`，
`k_j e_j^T=k_j(V^T e_j)^T V^T`，
`<G_j,Y_j V^T>=<G_j V,Y_j>`。

因此精确 reduced recurrence 为

**`Y_(j+1)=A_jY_j+k_j(V^T e_j)^T <G_jV,Y_j>_F`.**

归纳得到 `X_j=X_j Pi`、`rank(X_j)<=r`，不要求收缩、e_j 彼此正交、gate 不读取状态，也不要求 A_j 之间交换。顺序仍是 `(I-beta kk^T)D`。这是条件闭包，不是从 contraction 免费推出的 numerical-rank 结论。

若焦点是一次普通 scalar gate，`X_0=k_0 e_0^T`；初始闭包也需要 `e_0 in range(V)`。仅未来 e_j 受限不足够。

### 2.1 两种不同的合法实现条件

第一种是**名义路径条件**：在 full S 上恰有共同 residual value-span。它可由已到达路径检查，不能拿未来 suffix 构建 V 再称部署时已知；对更早动作是训练事后分析。

第二种是**结构性容量限制**：固定 V，令记忆始终 `S=ZV^T`，value generator 输出 `v=Vw`。即使 k、beta、D 可微地依赖 Z/updater 状态，完整非线性记忆 map 仍为

`Z^+=D Z+beta k(w-Z^T D^T k)^T`, `S^+=Z^+ V^T`。

从其恒等式求导，所有 memory tangent 都在该右子空间内；state-dependent k/D 的导数不会破坏这一已结构性封闭的 memory space。V 在本次焦点及后续路径固定，且不依赖被求导动作；学习或在线旋转 V 时必须加入 `Z dV^T` 等项。updater 内部状态及其切向另计，不能由 memory rank 界推出整个 sensitivity 低成本。

这第二种条件降低 physical memory 自由度至 `d_k r`，本质上是较小 value-width Delta；必须比较同一 Z/V、相同状态 bytes 的普通 Delta+BPTT/RTRL/直接动作预测器。它不是保持原 full-width 容量的免费压缩或新架构。

### 2.2 完整特征导数何时打破较弱闭包

一般 full S 下有

`dbar S=D X+dD[X] S`,
`de=dv[X]-(dbar S)^T k-bar S^T dk[X]`,
`dS^+=dbar S+dbeta[X] k e^T+beta dk[X]e^T+beta k de^T`。

即使名义 e in range(V)，`dD[X] S` 和 `k dv[X]^T` 等仍可有出空间分量。所以 §2 的较弱路径条件只认证规定的 scalar-gate transition，不认证完整网络；§2.1 的结构性封闭则通过完整 map 恒等式认证 memory block。其他层/workspace/反馈队列/自修改参数均须纳入实际 joint state。

## 3. R01-A 的泄漏 patch：不能把 projected approximation 当 exact projection

不假设 e 全部在 V。分解 `T_j=X_j Pi`, `R_j=X_j(I-Pi)`, `e_j^P=Pi e_j`, `e_j^R=(I-Pi)e_j`。因左乘与右投影可结合，完整切向的两块是

`T_(j+1)=A_j T_j+k_j(e_j^P)^T(<G_j,T_j>+<G_j,R_j>)`，
`R_(j+1)=A_j R_j+k_j(e_j^R)^T(<G_j,T_j>+<G_j,R_j>)`。

出空间 R 会通过 gate 返回 in-span T。只把 e 投影并递推，通常不等于 `X_j Pi`；只有额外消掉 `<G_j,R_j>` 或它的写入作用才相等。

一个确切成功特例是所有 j 满足 `G_j(I-Pi)=0`。此时 gate 只读取 in-span tangent，`<G_j,R_j>=0`；若 `hat X_0=X_0 Pi`，投影递推精确等于 T_j，即使 e_j 有出空间分量。它只保证 projected component，不保证完整 X 或任意 loss credit 精确。

定义低秩近似 `hat X_j=hat X_j Pi`：

`hat X_(j+1)=A_j hat X_j+k_j(e_j^P)^T<G_j,hat X_j>`。

令 E_j=X_j-hat X_j。两递推相减得到精确式

**`E_(j+1)=J_j[E_j]+k_j(e_j^R)^T<G_j,hat X_j>`.**

沿该名义路径若有可计算合法上界

`gamma_j>=||J_j||_(F->F)`，
`b_j>=||k_j|| ||e_j^R|| |<G_j,hat X_j>|`，

则 `epsilon_(j+1)=gamma_j epsilon_j+b_j`, `epsilon_0>=||E_0||_F` 给 `||E_j||_F<=epsilon_j`。可直接取保守点导数上界

`gamma_j=||A_j||_2+||k_j|| ||e_j|| ||G_j||_F`。

这里是固定轨迹上的 linear tangent error certificate，单点 G 足够定义该线性 J，**不**是整个非线性域的 contraction certificate。更紧有序产品界可替代逐步范数乘积。若在 hat state 而非真实名义 S 计算 A/e/G，还需状态/算子误差项；随机轨迹变化也必须另推。

联合 joint-state 的同类形式可用实际 JVP residual 定义，但计算 residual 可能与 full JVP 一样贵。对上述特殊结构，b_j 可由 residual value leakage、gate directional coefficient 与 key norm 得到；它不免费提供 ||G_j|| 或合法读出/曲率界。

## 4. R01-B：从切向误差转成动作信用区间

固定外部真实 teacher-forced 后缀、初始状态与模型参数，定义有限 horizon scalar objective

`F_H(a)=sum_(j=0)^H omega_j ell_j(z_j(a),a)`, `omega_j>=0`。

z 是全部可微联合状态；时序与反馈 queue 也包括在内。真实未来 token 仅作训练/事后监督；动作 a 在原决策时刻必须合法前缀可测。这里分析 F_H，不把它当自由生成总效应或无限未来总体风险。

令 `X_j=dz_j/da`, `J_j=partial_z T_j`, `B_j=partial_a T_j`，则

`X_j=J_j X_(j-1)+B_j`。

焦点单次干预在注入后 B_j=0；若共享 updater 参数在以后仍直接使用，B_j 通常不为零，不得省略。对任意近似定义实际 residual

`eta_j=hat X_j-J_j hat X_(j-1)-B_j`。

误差 `E_j=X_j-hat X_j` 精确满足 `E_j=J_j E_(j-1)-eta_j`。真实有序传播 `P_(j:i)=J_j...J_i` 给

`E_j=P_(j:1)E_0-sum_(i=1)^j P_(j:i+1)eta_i`。

若 `C_(j:i)>=||P_(j:i)||`（空乘积=1），则

`epsilon_j=C_(j:1)epsilon_0+sum_(i=1)^j C_(j:i+1)||eta_i||`。

完整状态 loss gradient `c_j=partial_z ell_j` 已包含 state-dependent query/readout。真实和近似 scalar credit 为

`g=F_H'(a)=sum_j omega_j(c_j^T X_j+partial_a ell_j)`，
`hat g=sum_j omega_j(c_j^T hat X_j+partial_a ell_j)`。

直接 loss derivative 在这一定义中相同，故

**`|g-hat g|<=delta=sum_j omega_j ||c_j||_* epsilon_j`.**

更贴合所需目标的精确式来自 costate。定义 `lambda_i=sum_(j=i)^H P_(j:i+1)^T omega_j c_j`，向量化矩阵时转置指 Frobenius adjoint。交换上述有限求和得

**`g-hat g=lambda_0^T E_0-sum_(i=1)^H lambda_i^T eta_i`.**

因此合法 `||lambda_i||_*<=B_i` 给另一界 `delta=B_0 epsilon_0+sum_i B_i ||eta_i||`。若实际残差与相应 costate 正交，高秩残差也不影响这一 scalar credit；但 exact costate 通常需要 reverse VJP/保存或重算路径，并非免费。此式是已知 adjoint residual weighting 的本对象展开，不能只因写成 Delta 就称原创。

为什么仅检查 relative tangent error 不够？取 `X=diag(1,eps)`, `hat X=diag(1,0)`, `C=diag(-eps/2,1)`，`eps>0`。相对 Frobenius 误差趋零，但 `<C,X>=eps/2` 与 `<C,hat X>=-eps/2` 符号相反。它是数学反例，不是新 benchmark。合法 absolute credit interval 会覆盖零，从而拒绝不受支持的方向。

范数和对偶范数须相配。若 c、direct derivative、B 或名义路径也近似，必须再加入各自误差预算；“critic 预测很准”不能直接提供确定性 delta。高概率 delta 只给对应事件上的结论，重复自适应决策还需 joint/anytime 覆盖。

§3 的 projected recurrence 用 complete J 求 residual，恰有 `eta_(j+1)=-k_j(e_j^R)^T<G_j,hat X_j>`；因此 A 与 B 的连接保留反馈交叉项，不是任意拼两个模块。

## 5. 区间下的有限步 gate 修订，而不是只看 gradient sign

设动作区间 `[a_min,a_max]`，a 为当前基线动作。要求 F_H 沿候选步长整个区间 C² 且

`F_H''(u)<=M`, `M>=0`。

这是真实 composite horizon objective 的曲率上界，不是某一个 hidden state Jacobian norm、GN 估计或单点 Hessian。Taylor 积分余项给

`F_H(a+d)-F_H(a)<=g d+(M/2)d²`。

结合 g in `[hat g-delta,hat g+delta]`，对合法 d 有

**`F_H(a+d)-F_H(a)<=hat g d+delta |d|+(M/2)d²`.**

优化这个一维凸上界。若 `|hat g|<=delta`，最小值由 d=0 达到，保留基线动作（不是默认把 gate 置零）。否则令 `h=|hat g|-delta>0`，方向 `s=-sign(hat g)`；该方向合法且曲率受界的最大距离为 R>=0。M>0 时

**`d*=s min(h/M,R)`**。

记 `u=|d*|`，有 `F_H(a+d*)-F_H(a)<=-h u+(M/2)u²`；只要 h>0、R>0，就严格为负。未裁剪时上界为 `-h²/(2M)`；裁剪时 u<=h/M 保证至多 `-h u/2`。M=0 且有限 R 时取 d*=s R；R=0 时保留基线。这是已知 inexact-gradient/smooth majorization 的动作区间特例，不称新优化器。

M 怎样合法获得？若整个动作区间上有 `||z_j'||<=K_j`, `||z_j''||<=Q_j`、loss state-Hessian norm <=L_j、state-gradient norm <=G_j、mixed derivative norm <=N_j、direct second derivative absolute value <=D_j，则链式法则给充分上界

`M=sum_j omega_j(L_j K_j²+G_j Q_j+2N_j K_j+D_j)`。

K/Q 的递推须包含 `T_zz,T_za,T_aa`，以及 updater/反馈的二阶导数；“gate 在0–1”没有给这些界。这个构造说明需查的对象，尚未为现有大网络提供便宜全区间 bound。只知道局部斜率的区间时，最多认证局部一阶方向，不能签发有限步下降。

具体地，令 `U_j=z_j''`，则链式法则为 `U_j=J_j U_(j-1)+T_(j,zz)[X_(j-1),X_(j-1)]+2T_(j,za)X_(j-1)+T_(j,aa)`。若整个区间各导数有合法 operator 上界 `gamma,t_zz,t_za,t_aa`，且 `b_j>=sup ||B_j||`，从真实初值导数界启动，取上界序列 `K_j=gamma_j K_(j-1)+b_j` 和 `Q_j=gamma_j Q_(j-1)+t_zz K_(j-1)^2+2t_za K_(j-1)+t_aa`。则真实 `||z_j'||<=K_j`, `||z_j''||<=Q_j`；也可取更大上界，不能取小于上述右端的数并声称它由该递推认证。该充分构造可极松，不能拿名义单点导数替代区间 suprema。

## 6. 旧反例复查与新的成功/失败预测

| 检查 | 修订后的结果 |
|---|---|
| 原 flat-H spectrum 构造 | e_j 依次占 H 个独立 value 方向，固定 r<H 的 V 不含全部 e_j；§2 前提明确不成立，§3 泄漏不被删除，原反例继续有效 |
| 非交换的左 A_j | 右-span closure 仍成立；无交换乘积或坐标重命名来掩盖反馈 |
| 低秩但小信用 | 信用趋零时仍需 h>0；error floor 可能让规则保留基线，不能用 tiny absolute tangent norm 宣称有用长期学习 |
| 高秩但所需信用可算 | full tangent rank 不阻止一个精确 VJP 标量信用；B 不以 rank 门槛否定决策，但计算成本另计 |
| 孤立 full state 的 e 漏出 V | 低秩近似仍可计算，只有完整误差预算低于 credit margin 才支持动作修订 |
| 固定结构 S=ZV^T | 完整 nonlinear memory closure 可成立，但 value capacity 降低；不能拿 full-width 对照宣称免费同容量优势 |
| 状态依赖 key/D、V旋转、updater z | 较弱路径闭包可失效；结构性固定 V 可保 memory closure，joint sensitivity/V导数仍单独计费 |
| 附加真实新知识/部署 RSI | 两个 patch 均未提供知识有效性标签、新外部反馈或跨新任务改善证据 |

区别性可证伪预测是：同 fixed V、同 causal nominal inputs 下 exact-span 结构能保持 rank<=r，即使 left factors 不交换；近似 closure 的信用误差应受完整 residual/product/readout 界约束；只有超过合法误差裕量的 gate 修订有该 F_H 的条件下降保证。若需要事后 target 来选 V、遗漏反馈残差、区间 M 无法成立或 exact same-width Delta已给相同成本，则相关工程/优势主张失败，数学 conditional boundary 可保留。

## 7. 信息、状态和总计算账

exact tangent factor Y 需 `d_k r` 数，V 另需 `d_v r`；r 个焦点方向/参数敏感度再乘相应列数，不能只报单焦点。full nominal S、updater z、梯度网络、history/checkpoint/feedback均未由此删除。

diagonal D 下 A_jY_j 约 O(d_k r)；dense D 为 O(d_k² r)。`V^T e` 约 O(d_v r)，`G V` 若稠密约 O(d_k d_v r)，gate JVP/gradient bound可能仍与完整网络一样贵。||e^R|| 及 residual budget也需实际可见状态/特征。若 gate结构允许直接对 Y作 directional JVP，可避免形成 G V，但次数、激活和 norm certificate另计。

B 的 scalar margin优化为 O(1)，真正昂贵的是 delta/M、真实后缀、完整 loss/readout、复算/激活和多动作监督；不能把最后一步便宜当整体便宜。RTX2080Ti、100M/1B每arm/seed只是资源背景，没有 measured runtime/VRAM。

训练可在合法已到达/teacher-forced真实 suffix 上构造信用目标；prefix-only updater可学习该目标的预测，但其泛化误差、校准和动作分布偏差另需验证。部署原动作不得读取还未到达 suffix。延迟到达反馈后，只能用于之后决策或合法 checkpoint/replay；旧动作的事后改善不等于对当时不可见未来的因果选择。普通远期 CE/BPTT、同信息 direct-action predictor、固定 learned updater是必要替代。

## 8. 来源、原生可测性与有限修复决定

本次 source/novelty 复核见 `../sources/REPAIR_R01_SOURCE_AUDIT.md`。已有 scalar-gate/JVP 路径、EYM、RTRL、KF-RTRL/OK、SnAp、invariant-subspace/reduced-model、inexact-gradient/trust-region均是强近邻。推导中没有引用文献保证来代替本离散闭包证明，也不将我们的 scalar majorizer等同于发表的 convex多步收敛定理。

现有 pinned bAbI全20/20000、lambada_openai全5153可以保留 endpoint；BABILong/RULER支持长上下文，LongMemEval支持跨会话QA更新，CITB/TRACE/SEAL有不同的continual对象。它们不提供 residual-span、exact tangent、error-margin 或合法 M ground truth。数学正确性用证明/独立反例审查；未来同原生样本上的 instrument是机制证据，不能自造benchmark/labels或用toy score证明效果。LongMemEval/SEAL的已记录付费judge和资源限制保持。

决定：两条 **REPAIRED_CONDITIONAL_CONSTRUCTION / contribution difference unresolved / experimental effect unknown**。没有再把“普适低秩不成立”解释为不允许修；也没有因 conditional pass 把已知小宽度Delta/保守下降界计新候选。

后续只允许有新证据的下一次修订：A研究是否有prefix可得、保持足够任务容量的value几何和更便宜gate界；B研究是否能在同总计算下产生有用delta/M，或只保留一阶训练信用。若仅回到普通compressed Delta或全Jacobian replay，则将对应算法优势park，保留已成立理论，并在具体新增结构/信息/成本证据出现时重开。池20/选择15目标不变，指探索池而非保证20个全新成功方法；历史5/活动0/准入0/选择0保持。未改候选模型源码、实验矩阵或Local记录。
