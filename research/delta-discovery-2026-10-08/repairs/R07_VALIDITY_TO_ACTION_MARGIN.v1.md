# R07 v1：真实性到 Delta 写入动作的边际桥

状态：**条件数学成立的局部决策证书；不是 D 候选；未执行实验**  
谱系父项：`R06_SELECTIVE_VALIDITY_AUDIT.v1.md`，SHA256 `9f2d3ab00aa6c036c5cde10f18cddb73fa1a120545f43d0f83f8df0da7cdc8a3`。  
修复目标：R06 能以随机外部审计识别事实真实性 `Y`，却不能推出 R05 的理想二元动作 `r`。本修订不给 `Y=r` 加口号，而是求出使这一桥接成立所需的最小收益、保护交叉项和曲率边际，并保留不满足条件时的两世界反例。

## 1. Formal object、语义与信息边界

当前动作前状态为 `S^-`，标准 Delta 提议为

\[
e=v-(S^-)^\top k,\qquad U=\beta k e^\top,\qquad u=\operatorname{vec}(U),
\]

实际 gate 为 `a\in[0,1]`，即 `S(a)=S^-+aU`。`a=1` 只是完整执行当前提议；除非 key 已归一化或 gain 已补偿，它不必把 self-key 残差一次清零。外部审计标签 `Y\in\{0,1\}` 只说明本次新 target 是否应被当作有效事实：`Y=1` 时新 target 项进入声明风险；`Y=0` 时该 target 项不进入。它不提供保护集合、旧 target 是否仍有效、未来 query、动作后的自由运行分布或两个潜在动作结果。

为得到一个可实际核验的桥，先声明固定参考轨迹/固定 probe 上的线性平方 surrogate。令

\[
\rho_n=f_n(S^-)-y_n,\quad d_n=J_nu,\qquad
\rho_p=f_p(S^-)-y_p,\quad d_p=J_pu,
\]

其中 `n` 是新事实 probe，`p` 是事先声明且仍有效的保护 probe 直和空间；内积包含预先固定的半正定权重。定义

\[
b=-\langle\rho_n,d_n\rangle,\qquad
c=\langle\rho_p,d_p\rangle,
\]

\[
h_Y=\|d_p\|^2+Y\|d_n\|^2+\lambda\|u\|^2\ge0.
\]

`b` 是有效新 target 沿提议方向的一阶收益；只有 `b\ge0` 时该 Delta 提议才与新 target 对齐。`c` 是保护残差的一阶有符号代价：`c>0` 表示写入起初增加保护损失，`c<0` 表示它碰巧也改善保护目标。`h_Y` 是 probe 曲率加动作正则，不是事实标签。

这些对象若使用未来真实 query/target，只能事后诊断；部署 gate 所需界必须在动作前 filtration 内可见，或由过去外部反馈校准成同时有效的上/下界。R06 的 `Y` 也可能是事后/延迟审计标签：只有动作前已经返回的外部 `Y` 才能 gate 同一次写入；事后 `Y` 只能用于日志估计、校准或后续策略，不能回填本次动作。动作前审计的延迟与标签成本必须计入信息预算。模型自生成 target 不是外部有效性证据。

## 2. 连续推导：精确二次桥

声明风险为

\[
L_Y(a)=Y\|\rho_n+a d_n\|^2+\|\rho_p+a d_p\|^2
+\lambda a^2\|u\|^2.
\]

直接展开得到相对 no-write 的精确风险差

\[
\Delta_Y(a)=L_Y(a)-L_Y(0)
=2a(c-Yb)+a^2h_Y.
\]

令净收益边际

\[
q_Y=Yb-c.
\]

若 `h_Y>0`，连续 gate 的唯一最优解为

\[
a_Y^*=\operatorname{clip}_{[0,1]}\frac{q_Y}{h_Y}.
\]

更细地，`q_Y<=0` 时连续最优为 no-write，`0<q_Y<h_Y` 时最优为部分 gate，`q_Y>=h_Y` 时完整写入才是连续动作集的最优点。因此存在某个正 gate 严格优于 no-write 当且仅当 `q_Y>0`；完整写入只需在二元比较中优于 no-write 当且仅当

\[
q_Y>\frac{h_Y}{2}.
\]

按 R05 的二元动作族 `{no-write, full-write}`，并约定平局选 no-write，理想标签正是

\[
r_{\rm quad}(Y)=\mathbf 1\!\left\{Yb-c>\frac{h_Y}{2}\right\}.
\]

当 `h_Y=0` 时，一般线性风险的完备分段是：`Delta_Y(a)=-2aq_Y`，`q_Y>0` 取 `a=1`，`q_Y<0` 取 `a=0`，`q_Y=0` 时所有 gate 等价而约定 no-write。在本节声明的半正定平方 surrogate 中，`Y=1,h_1=0` 会强迫相关 `d` 和正则项为零，进而 `b=c=q_1=0`；`Y=0,h_0=0` 只强迫 `c=q_0=0`，`b` 可非零但不参与该分支。非零 `q_Y` 分支只是对更一般线性风险的边界说明。故没有除零漏洞。

## 3. `Y=r` 何时真成立

对该声明 surrogate，`r_quad=Y` 对两个真实性分支同时成立，当且仅当

\[
b-c>\frac{h_1}{2}
\quad\text{且}\quad
-c\le\frac{h_0}{2}.
\]

第一式说：真事实的方向性收益必须大于保护一阶损伤与完整步二阶代价。第二式说：对无效 target，完整写入不能仅靠改善其他已声明 probe 而胜过 no-write。真实性只是第一项的开关；真正完成桥接的是 `(b,c,h_0,h_1)` 的联合 margin。

若动作前只有区间

\[
b\in[\underline b,\overline b],\quad
c\in[\underline c,\overline c],\quad
h_Y\in[\underline h_Y,\overline h_Y],
\]

则以下是可检查的稳健充分条件；这些区间必须来自同一个同时覆盖事件，不能把若干边际 95% plug-in 界当作联合 95% 证书：

\[
\underline b-\overline c>\frac{\overline h_1}{2}
\quad\Longrightarrow\quad Y=1\Rightarrow r_{\rm quad}=1,
\]

\[
-\underline c\le\frac{\underline h_0}{2}
\quad\Longrightarrow\quad Y=0\Rightarrow r_{\rm quad}=0.
\]

两式同时成立才可把 R06 审计到的 `Y` 合法替换为这个局部二元 `r_quad`。界没有通过，只表示证书拒绝判断；不证明事实错误或写入一定有害。

## 4. `Y` 单独不足：最小两世界反例

取同一个真实新事实 `Y=1`、同一个 Delta 提议、`b=1`、`h_1=1`。

- 世界 A 的保护交叉项 `c=0`，则 `Delta_1(1)=-1<0`，所以 `r_quad=1`；
- 世界 B 的保护交叉项 `c=1`，则 `Delta_1(1)=1>0`，所以 `r_quad=0`。

两世界有相同真实性、同一新 target 对齐和同一二阶敏感度，只改变旧知识的有符号交叉项就得到相反动作。任何只输入 `Y`、不观察或约束 `c` 的规则都不能在两世界同时正确。R06 的审计点识别 `E[YZ]` 也不会自动识别这个交叉项。

另一个必要边界是 `b<0`：即使 `Y=1`，提议方向也把新 target 推得更差；真实性不能修复错误的 key/value/write direction。

## 5. 非线性未来的有限步修订

对完整固定后缀局部风险，令 `2(c-Yb)` 是 `a=0` 的方向导数、`2h_Y` 是方向二阶导数，并假设 `a\in[0,1]` 上三阶余项满足

\[
\Delta_Y(a)=2a(c-Yb)+a^2h_Y+R_Y(a),
\qquad |R_Y(a)|\le\frac{\kappa_Y}{6}a^3.
\]

若动作前同时有效的界给出 `q_Y\ge\underline q_Y>0`、`h_Y\le\overline h_Y`、`kappa_Y\le\overline\kappa_Y`，则任何满足

\[
2\underline q_Y>
a\overline h_Y+\frac{a^2\overline\kappa_Y}{6}
\]

的正 gate 被认证优于 no-write。这里 `overline h_Y,overline kappa_Y>=0`。若 `overline kappa_Y=0,overline h_Y>0`，可取 `0<a<min{1,2 underline q_Y/overline h_Y}`；若二者都为零，则任意 `a in (0,1]` 都被证书接受。`overline kappa_Y>0` 时正根为

\[
a<\frac{-3\overline h_Y+
\sqrt{9\overline h_Y^2+12\overline\kappa_Y\underline q_Y}}
{\overline\kappa_Y}.
\]

完整写入的充分条件是

\[
2\underline q_Y>
\overline h_Y+\frac{\overline\kappa_Y}{6}.
\]

这只是固定参考路径上的局部/有限步证书。若写入改变以后 token、检索、用户反馈或 updater state 的分布，需 R02/R03 的随机化、顺序 OPE 或可信环境模型；本余项不能吸收未知 change-of-measure。

## 6. Delta 专门化与可计算构造

即时线性 readout `o(q)=S^Tq` 下，Delta 位移为

\[
o_a(q)-o_0(q)=a\beta(q^Tk)e.
\]

对保护残差 `r(q)=S^Tq-y_p(q)`、权重 `M_p`、`G_p=E[qq^T]` 与 `C_p=E[q r(q)^T]`，有精确式

\[
c=\beta k^TC_pM_pe,\qquad
\|d_p\|^2=\beta^2(e^TM_pe)(k^TG_pk).
\]

若新事实 probe 就是 `(k,v)`，令 `kappa=||k||^2`，则

\[
b=\beta\kappa e^TM_ne,\qquad
\|d_n\|^2=\beta^2\kappa^2e^TM_ne.
\]

因此保护二次项包含 R03 的 `k^TG_pk` 几何，而本修订新增必须保留的**有符号残差交叉项** `c`。只知道位移能量或 null-space 范数不能判断它是修正还是破坏。

若保护 probe 满足 `d_p=0`，则 `c=0` 且保护曲率也为零，桥退化为“新 target 收益是否超过自身曲率/正则”；这是硬投影/AlphaEdit 类强 baseline，不是 R07 的原创机制。若保护空间与写入方向冲突，降低 `c` 往往同时降低 `b`；不能只优化一边。

计算已有 `u` 只需标准 Delta 成本；固定 `m` 个 probe 的 JVP/readout 代价与 `m` 成正比，稠密保护 Gram 或完整 horizon Jacobian 可能远高于写入本身。还需保护 target `y_p` 和“仍有效”证据；R06 的单个新事实审计不提供它们。

## 7. 旧反例复查与失败边界

1. R06 的 `Y=1` 但完整写入有害反例被精确定位为 `b-c<=h_1/2`，没有删除。
2. R05 的 joint-moment 不可识别性仍在：未观测 `c,h` 或 action utility 时，真实性边际不能点识别动作。
3. R03 的低位移不等于低语义风险仍成立；`c` 需要有符号 residual/target，而不是只有 `||d_p||^2`。
4. 保护 target 若已过时，`c` 会把应释放的知识误当损伤；真实性桥需要旧 target 有效性，不只是新 target 真值。
5. `b,c,h` 若来自事后真实 future，就发生部署泄漏；prefix predictor 仍需独立校准与误差界。
6. 多个候选写入相互作用时出现交叉 Hessian，逐项标量桥不能组合成全局最优动作。
7. 真正 ideal action 不在 `{0,u}`、或更换 key/value 方向优于缩放时，`r_quad` 只是局部二元标签。
8. 正确 bridge 不证明样本效率、长期改善或 RSI；实验效果保持未知。

## 8. 区别性预测与强简单对照

可证伪预测：控制 `Y=1,b,h_1` 后，完整写入的收益会在 `c=b-h_1/2` 处反号；硬保护降低 `c` 却同时削弱 `b` 时，最优 gate 可不升反降。若实测动作偏好只由 `Y` 决定、与方向性收益/保护交叉项/曲率无关，本桥的 declared surrogate 不合适。

强对照必须包括：no-write、标准 Delta、仅按真实性 gate、普通 future-loss/action predictor、硬投影/soft preconditioner、AlphaEdit/O-Edit、KnowledgeEditor 的 KL/constrained edit、LyapLock 的长期 preservation constraint、R05 minimax gate 与 R06 审计。直接预测 `Delta_Y(1)` 使用同样信息且更简单；R07 只有在分解出的证书更可校准、更便宜或能给拒绝边界时才可能有实用价值，当前未证明。

## 9. 原生测量可行性

CounterFact/ROME、KnowEdit/EasyEdit、AlphaEdit/O-Edit 与 LyapLock 原生提供 efficacy、paraphrase/generalization、locality/neighborhood、sequential preservation 或下游 endpoint。它们没有同时记录：外部 grounded `Y`、动作前 `b,c,h` 的 Delta 证书、保护 target 仍有效性，以及同一事件的 write/no-write 潜在结果。现阶段只能复用行为终点检查必要现象，不能声称原生识别 bridge，也不新增标签、metric、case、scorer 或结果。

## 10. 处置与重开条件

R07 完成了 R06 明确要求的 `Y->r` 数学 bridge：真实性要与方向性收益、保护有符号交叉项和曲率 margin 联合，才足以决定局部 full-write/no-write；同时给出精确二次、稳健区间、三阶余项和两世界不可识别边界。

它目前仍是 **known constrained quadratic decision / locality-preserving edit 的 Delta 专门化 control**。核心 normal form 是一维受约束二次决策；保护投影、正则/长期 preservation 与局部 edit objective 有直接近邻。没有 prefix-only 低成本证书、原生 joint labels、同预算优势或自由运行效果，因此不分配 D 编号，不增加活动/准入/选择计数。

只有至少一项新证据才重开：`(b,c,h)` 可由严格更便宜的 Delta 充分统计在部署前校准；旧/新 validity 联合审计形成原生可测闭环；证书对直接 action predictor 有样本或计算优势；或把标量桥扩展为顺序 coupled-state theorem 且不退化为已知 constrained optimization/OPE。
