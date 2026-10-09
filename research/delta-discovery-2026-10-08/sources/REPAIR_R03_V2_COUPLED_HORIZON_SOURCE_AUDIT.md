# R03 v2 耦合时域安全：来源、机制碰撞与测量审计

审查对象：`repairs/R03_COUPLED_HORIZON_SAFETY.v2.md`。观察日期 2026-10-09 UTC。此审计复用同一项目已经固定并全文/代码接口审查的来源，新增的是这些来源之间对 v2 精确 claim 的映射；没有把摘要、第三方实现或论文结果冒充本项目结果。

## 1. 直接上层机制

1. Wan, Kveton, Song, **Safe Exploration for Efficient Policy Evaluation and Comparison**, ICML 2022, PMLR 162。`REPAIR_R03_PROTECTION_AWARE_LOGGING_SOURCE_AUDIT.md` 已读正文的安全约束 exploration policy 与 IPW/DR 方差优化；它直接覆盖“在安全约束下选择 propensity”的通用本体。
2. Zhu, Kveton, **Safe Optimal Design with Applications in Off-Policy Learning**, AISTATS 2022, PMLR 151。已读正文覆盖相对 production baseline 的安全且信息高效 logging design、side information 与 linear contextual 扩展。v2 把 cost 换成 coupled-horizon Delta certificate，不足以单独形成新方法。
3. Kazerouni et al. CLUCB、Jagerman et al. SEA、Pacchiano et al. stage-wise constrained bandits 及 Wang--Agarwal--Dudík OPE 已在 R03 v1 审计固定。它们覆盖 baseline-relative、逐轮成本、高置信部署与 IPS/DR/SWITCH 对照。

## 2. 完整耦合传播与 sensitivity 碰撞

1. 项目 `STEP2_COUPLED_UPDATER_STABILITY.md`（最终 SHA256 `70f3cff118db5699a67dd9cf808157d16779acc6b5f57ea6edadd3a620629d4b`）已经从完整 `[[A,B],[C,D]]` Jacobian 推出正比较矩阵小增益条件，并证明 bounded gate、分别稳定的块与慢 updater 都不充分；还给出 protected-fiber 结构。v2 不把这些已知控制重新计数，而是把其增量 bound 接到 R03 的 positivity feasibility。
2. `COUPLED_UPDATER_RSI_SOURCE_AUDIT.md` 已读 discrete-time small-gain primary source arXiv:2105.02376v1 的相关 theorem/corollary，并明确本项目只使用更窄的 uniform incremental comparison。v2 的 `Gamma_h` 几何和 energy sum 是该类控制的直接推论，不声称原创稳定性定理。
3. `STEP2_CLOSED_LOOP_RANK_GROWTH.md` 及其来源审计已固定 RTRL、NoBackTrack/UORO、KF-RTRL/OK、SnAp 与 e-prop 的 exact/随机低秩/Kronecker/稀疏/eligibility 近邻，并给出 Delta closed-loop tangent rank 可随 horizon 线性增长的紧控制。故 v2 不能声称远期 sensitivity 仍 rank one；它只传播注入范数。
4. `PROJECTED_DELAYED_CREDIT_SOURCE_AUDIT.md` 已审查 MAML、learned optimizers、DNI、DSSR、SEAL、ACL/SRWM、HOPE 与 TTT Ouroboros 的全文/作者接口。普通 post-update future loss、synthetic credit、self-generated Delta instruction 和延迟 paired validation 都是强对照。

## 3. Delta 来源与 claim 边界

R03 v1 已从 post-decay `Delta S=alpha beta k e^T` 推出指定保护 query 分布上的精确首步位移与平方风险交叉项。v2 新增的严格对象是

`rank-one injection norm × full coupled incremental gain × horizon output sensitivity`

及其回代后 `b_H >= epsilon U_1,H` 的 positivity 可行性条件。这一接口对排除“单步安全自动等于长期安全”有用；但每个上层构件分别属于 Delta 基础代数、安全实验设计和增量稳定。当前 bounded audit 不支持“首个”“原创算法”或“同预算更优”的表述。

若完整 `gamma/L` 的 uniform 认证成本高于 rollout/JVP/VJP，rank-one 即时注入并没有计算优势。若动作改变自由运行 token/反馈分布，same-exogenous-path certificate 不是 total potential outcome；必须回到 R02 的随机化/顺序 OPE。若 protected-validity 不可识别，则 output-energy 也不是语义安全。

## 4. 作者实现与原生测量复用

- SEAL 官方仓库固定 `Continual-Intelligence/SEAL@6d9c9f9ee392c6cc618e771f399d436d190f6ca4`；已读 continual driver、TTT server、grader utility。它测 LoRA/SFT self-edit 后的旧问题保持，默认含 GPT-4.1 judge 与双 GPU/7B 资源，既不提供 Delta propensity/coupled Jacobian 标签，也不适配当前无付费/单 2080Ti 条件。
- ACL/SRWM 官方 `IDSIA/automated-cl@3d7b53adb4b6b43acd82b9a381a2c631d0e59a5d` 已读 stateful self-referential layer 接口；它证明 self-generated Delta update 已有作者实现，不提供 v2 的保护 validity 或 safety certificate scorer。
- HOPE/Titans 的相关全文已读；HOPE 作者实现未定位、Titans 作者仓库当时为空，不能用第三方实现填补。此缺口只阻塞相应 faithful implementation，不改变 v2 的通用控制碰撞。
- LongMemEval v1/v2、CITB、TRACE、bAbI、LAMBADA 的原生对象和 scorer 边界已经在现有 source audits 固定。它们能看 QA/BWT/endpoint，但没有决策时 protected-validity、uniform gain、propensity 与 paired update outcomes。

## 5. 决定

来源结论：**数学修复有用，机制原创性未闭，仍是 control/theory boundary。** R03 v2 比 v1 更准确地给出 coupled-horizon 条件与不可行边界，但没有满足重新开启条件中的同预算 Delta-specific 优势，也没有原生 joint measurement。0 个新候选；5 历史 / 0 活动 / 0 科学准入 / 0 选择保持。

本审计没有运行项目/作者代码、测试、训练、推理、评分、数据/模型下载、GPU、Docker 或付费调用；固定来源的既有代码读取是静态接口审查。
