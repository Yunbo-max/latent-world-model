# R04 v2 独立数学审查

- assignment：独立检查 Delta 快慢巩固修订稿的公式、顺序、条件、反例、可计算构造和隐藏成本；不执行项目或作者代码。
- 实际审查身份：平台子代理 `/root/r04_math_review`，独立于 integration writer `/root`。
- reviewed_at：2026-10-09 20:40:08 UTC。
- artifact_ref：`research/delta-discovery-2026-10-08/repairs/R04_CONSOLIDATION_DYNAMICS.v2.md`，12506字节，SHA256 `ba81ea9506160ee5e640faed2673ad068e925da82bb7ea77595999d7151f2732`。
- scope：math；outcome：accepted_conditional_control_after_revision。
- 集成说明：以下保留实际工作者逐项推理及决定，由root排版保存；不把数学通过当作原创性、科学准入、选择或实验通过。

## v1发现与v2最终字节复审

实际核实v1：11684字节，SHA256 `7d717fd36c285d9e401fd5e3967b66ddacae4e1318d857ebd49c5409dd65c09d`。v1第5节用 `EC=0` 作为慢强迫项消失条件，在一般D下错误；公式(7)/(8)的实际项为 `E(I−D)C`。

反例：`k=C=(1,1)ᵀ/√2,β=1,D=diag(1,1/2)`。此时EC=0，但 `E(I−D)C=(−1,1)ᵀ/(4√2)≠0`。即使D是合法对角收缩，非均匀衰减也改变方向。v2正文及第9节已改成正确条件，另注明D保存write span时EC=0可作充分条件。实际读取v2并核实新hash，修订成立；原反例没有删除，未沿用v1pass。

## 公式逐项审查

| 公式 | substantive rationale |
|---|---|
| (1) | 初快差−C、慢差C；相同affine B抵消，快差依序左乘A得−PC，总差(I−P)C。指定查询零差与任意查询零总差条件正确。 |
| (2) | 要求A(S−C)+B'=AS+B−C，唯一移项得到B'=B+(A−I)C。必要性限于固定A、可自由改加性B；一般补偿未必只沿当前k。 |
| (3) | M+AS+B+(A−I)M=A(M+S)+B，确实执行同一标准Delta。只给冗余表示，不给保留改善。 |
| (4) | D=I时补偿为−βkkᵀM，总残差尺寸和转置正确。 |
| (5) | ED−I=(D−I)−βkkᵀD；必须DM，不能交换D/E；完整补偿含满矩阵衰减项。 |
| (6) | DS先衰减，再以M+DS形成残差，顺序正确。 |
| (7) | 展开S+=EDS+B−βkkᵀM，加M并代入S=W−M，得到AW+B+E(I−D)M。v2条件解释正确。 |
| (8) | 两条Patch B轨迹初总差0、慢差C，差分为AδW+E(I−D)C；有序强迫和正确，与naive公式(1)不同。 |
| (9) | E,D均非扩张则各P非扩张；三角不等式和||EX||F≤||E||₂||X||F给所列界。严格a<1时几何和也正确，仅是冻结总状态位移界。 |
| (10) | 初总差Ĉ−C、慢差Ĉ，因此Pr0加E(I−D)Ĉ强迫和正确。初差改变未来系数时失效，稿件已明确。 |

维度：M/S/C/W为d_k×d_v，E/D/A/P为d_k×d_k，B为d_k×d_v，Wᵀq为d_v列；qᵀδW=0与输出列零差等价，无转置错。

## 两种patch及闭环条件

Patch A保持总递推，等价单W标准Delta，不能同时称更强保留算法；单W低开销强对照保留。Patch B的实际差别由E(I−D)M决定，D=I时消失；分解本身不是新方法。

冻结公式需相同A/B/q/continuation。非线性充分条件亦成立：转移/读出仅依赖总W及不变其它状态，快转移为T(M+S,ξ)−M，则固定迁移g_C与转移交换。若updater隐态/gate/特征分别读取M/S，此条件不可用，需联合状态推导。

## 反例、极限与成本

原v=0标量例精确显示naive无法释放慢分量，Patch B在D=I、β=1时让快状态抵消M，两边总输出0，确实修复旧反例。可选字面双计补充：同例令v=c，未迁移输出c，naive迁移后快/慢均c，总输出2c；Patch B两边仍c。这不要求改变v2结论。

β=0,D=αI特例给有效信息保留收益；相同信息过时且目标0时又有损害，不能用稳定性判真实性。E特征值为write方向1−β||k||²，正交方向1；0≤β||k||²≤2保证非扩张，多维无衰减rank-one通常不严格收缩。强迫位移界不是CE改善界。

接受须保留成本：满宽M多存d_kd_v个数，固定容量不能与仅S比较；Patch A一般满矩阵补偿不一定能用rank-one接口；函数族/地址不匹配需拟合误差；代数恒等不保证浮点取消和访问成本。C有效性、可识别选择、跨任务收益均未解决，来源真实性/贡献差异由另行来源review负责。没有模型、训练、测试、评分执行。

## Semantic checks

| check | status | rationale/evidence |
|---|---|---|
| formal_object | accepted scoped | §2同地址加性子模型，区别任意慢网络；v2hash绑定。 |
| operations_and_conditions | accepted conditional | §3–6实际执行不变性、消去、强迫分解和传播；冻结/闭环条件明确。 |
| derivation | accepted after revision | 逐项重推(1)–(10)，非均匀D错误由保留反例的v2修复。 |
| assumptions | accepted conditional | C可见可表示，M两次迁移之间固定；同未来系数和状态访问限制明确。 |
| method_expression | accepted control | Patch A等价控制，Patch B快慢构造，未认证原创。 |
| prediction_and_falsifier | accepted scoped | D=I、非均匀D泄漏、有效/过时相反后果及初拟合误差可直接核对。 |
| closest_alternative | identified; source review separate | 单W、普通快慢总残差/慢衰减强对照明确，来源差异仍须审查。 |

最终决定：v2无必须继续修订的数学错误，可保存为完成的条件repair/control；贡献差异、原生测量未闭，实验未知，candidate/selection不增加。所有数学evidence均绑定v2hash，v1仅作错误历史。
