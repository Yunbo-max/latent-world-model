# Delta 完整闭环秩增长：primary-source、作者接口与测量审计

状态：2026-10-09 UTC bounded audit。只读论文、作者链接和既有固定作者接口；未执行项目/上游代码、测试、训练、推理、评分、数据/模型下载、GPU 或 Docker。此记录支持 `STEP2_CLOSED_LOOP_RANK_GROWTH.md` 的碰撞和测量边界，不证明原创性。

## 1. 直接 online-sensitivity 近邻

| Work | 真实对象 | 与本轮的碰撞 / 差异 |
|---|---|---|
| RTRL | Williams & Zipser, “A Learning Algorithm for Continually Running Fully Recurrent Neural Networks,” *Neural Computation* 1(2), 1989；状态对参数的完整 influence/sensitivity 递推 | 已覆盖完整闭环 recurrent sensitivity 随时间传播及其高维成本。本轮是 memory-to-scalar-focal-edit 的矩阵切向，不是新在线微分范式。 |
| NoBackTrack | [Ollivier, Tallec & Charpiat, arXiv:1507.07680v2](https://arxiv.org/abs/1507.07680)，§2 Eq.(4)、§3 rank-one trick | `G_(t+1)=partial_h f G_t+partial_theta f` 是 full sensitivity；随机符号 reduction 保持期望无偏，连续 deterministic projection 会有 bias。其 sequence-of-parameters derivative 与 current-parameter derivative 的接近还需小步条件。固定低秩不是 exact sensitivity；本轮未定位作者代码。 |
| UORO | [Tallec & Ollivier, arXiv:1702.05043v3](https://arxiv.org/abs/1702.05043)，Eq.(5)；作者仓库 [`ctallec/uoro`](https://github.com/ctallec/uoro) 固定已审 commit `135a057edcd83fda17db5785607cf4af1fb0cfdd`，`uoro.lua` blob `96134bb7c07fc60e242aa5711d44bf4fd8bb1e6b` | `sbar/thetabar` 对 RTRL influence 作随机 rank-one 无偏压缩，代价是 variance；实际 `UORO:forward` 传播 `sbar`、采样 Bernoulli signs 并作 norm scaling。本轮 exact-rank 反例不否定其无偏随机估计，也不能替代方差/成本比较。 |
| KF-RTRL | [Mujika, Meier & Steger, NeurIPS 2018](https://proceedings.neurips.cc/paper/2018/hash/dba132f6ab6a3e3d17a8d59e82105f4c-Abstract.html), arXiv:1805.10842，§2–3 | 利用特定 RNN Jacobian 的 Kronecker 结构形成无偏、memory-efficient approximation，并明确比较 UORO variance。没有定位到可确认的作者官方代码，故不虚构 pin。 |
| OK | [Benzing et al., ICML 2019](https://proceedings.mlr.press/v97/benzing19a.html), arXiv:1902.03993，Definition 1 / Theorem 1；作者之一仓库 [`marcelomatheusgauy/optimal_kronecker_approximation`](https://github.com/marcelomatheusgauy/optimal_kronecker_approximation) 固定 observed commit `76803fc7a64849a4a8bd37bbcbeb42bc52fb55c5`；`OK/OK_rank_r_unbiased.py` blob `113dbbe8db5d78cb6b59de7803c8e841171cf02e` | 在包含既有 Kronecker 近似的类中优化压缩方差；实际 TensorFlow 接口维护 rank-16 `G1/G2`，把传播项与即时项做 Gram--Schmidt 后在小系数矩阵上 SVD 压缩。只读代码，未执行。 |
| SnAp | [Menick et al., ICLR 2021](https://openreview.net/forum?id=q3KSThy2GwB), arXiv:2006.07232v1，§2.1 / §3 | `J_t=I_t+D_tJ_(t-1)` 是 exact influence；`n`-step graph reachability 截断为有偏稀疏近似。SnAp-1 只留 immediate influence，dense RNN 的 SnAp-2 可回到 full RTRL；不是低矩阵秩保证。没有定位到论文作者指定公开代码，故只记论文公式。 |
| e-prop | [Bellec et al., Nature Communications 2020](https://www.nature.com/articles/s41467-020-17236-y)；作者仓库 `IGITUGraz/eligibility_propagation@efd02e6879c01cda3fa9a7838e8e2fd08163c16e` | 因子化 eligibility traces 与 learning signal；局部/生物可行 signal 是近似。它说明“eligibility 结构化”已有强先例，但不是当前 Delta matrix-rank 定理。 |

这些来源已经覆盖核心机制：完整闭环 influence 一般很大，已有随机 rank-one、Kronecker-sum、稀疏与 eligibility factorization 等近似。OK 的最优性是其无偏随机 Kronecker-sum 近似类中的 minimum-variance 结果，不是 deterministic Eckart--Young 截断，也不使 true sensitivity 低秩。故不能把“用 low-rank 压缩 closed-loop tangent”计为新候选。

## 2. 本轮窄残余

未在上述 bounded read 中逐字找到的只是一个 Delta-specific 形式化：单次 rank-one Delta perturbation 在 future scalar gates 读取 memory 时，切向可每步增加一个独立 rank-one方向，并有合法构造达到 `rank=min(H,d_k,d_v)`；Eckart--Young 尾误差随后给 fixed-matrix-rank forward representation 的反例。

这项残余更适合作为防止误外推 frozen-path 结论的 theorem/control，而不是方法：它不提供新压缩器、不改善 UORO/KF-RTRL/OK/SnAp 的 bias/variance，也不解决写入有效性、revision 与旧知识保护。矩阵秩本身不是一般算法内存下界；符号表示或 reverse-mode 可不物化完整前向切向。任何更强 lower bound 都需另定信息/通信模型和丰富输入族。

## 3. 作者接口边界

- UORO 和 e-prop 沿项目既有已审固定 commit/blob 复用；没有重新执行。
- OK 的 PMLR 页面明确链接 code；本轮固定作者之一仓库的 observed commit，并实际读取 `OK_rank_r_unbiased.py` 的 rank factor、Gram--Schmidt 与小矩阵 SVD 路径。没有运行代码；它是 RNN-specific TensorFlow 实现，不是 Delta memory 的现成模块。
- KF-RTRL 与 SnAp 本轮没有定位到可确认的作者官方实现；第三方实现不冒充作者代码。
- 所有论文结果只是最近工作证据，不是本项目运行结果。

## 4. 原生测量可行性

| 资产 | 能测到 | 不能测到 |
|---|---|---|
| bAbI 20 tasks / 20,000 denominator | 受控推理 endpoint、任务级 accuracy | memory tangent rank、奇异值尾、截断 residual、ideal update 或闭环 credit error |
| LAMBADA OpenAI / 5,153 denominator | 最后一词 likelihood/greedy exact endpoint | updater sensitivity、事实有效性、write/no-write 因果收益 |
| LongMemEval v1 | 500 个长历史 QA，含 knowledge update/temporal 子集与 evidence session IDs | 内部 Delta tangent、exact costate、rank-r approximation truth；answer/evidence label 不能给部署 updater，原生 QA judge 还受当前 no-paid/2080Ti 条件阻塞 |
| LongMemEval v2 | 451 个 Insert/Query 对象；answer accuracy、query latency 与 LAFS frontier | 测 memory-system 查询权衡而非 updater 学习或 tangent rank，并引入 reader/embedding/judge 资源 |
| CITB | InstrDialog 任务矩阵上的 output-level retention、FWT/BWT；官方方案含 LM-adapted T5-small 与 native scripts | fast-state Delta 的闭环切向；FWT 不是以后任务的 sample/compute learning speed，不能把参数连续学习直接等同于 persistent fast state |
| TRACE / SEAL continual | TRACE 的任务/能力矩阵与 SEAL 的连续 self-edit retention | 都不标注 tangent rank 或仍有效事实；TRACE 原实验 7B/13B，SEAL 默认 Qwen2.5-7B、2 GPU 与 GPT-4.1 grading，当前 2080Ti/no-paid 条件不匹配 |

以上数值、原生接口和资源边界沿已复核的 [`PROJECTED_DELAYED_CREDIT_SOURCE_AUDIT.md`](PROJECTED_DELAYED_CREDIT_SOURCE_AUDIT.md)；BABILong/RULER 的 delayed-influence endpoint 与 scorer 限制另见既有 [`MEASUREMENT_FEASIBILITY_2026-10-09.md`](MEASUREMENT_FEASIBILITY_2026-10-09.md)。二者可测长时延行为后果，但同样不提供内部 tangent/rank ground truth。

因此该 theorem 的直接判别对象需要以后合法 instrumentation：记录 exact/full tangent 或可信 JVP/VJP reference、每步截断 residual、ordered-product amplification 与最终 gradient error。那是内部软件/实验设计，不是现有 native benchmark 的原生标签。本阶段不造 benchmark、不运行 instrumentation、不用 toy score 证明科学价值。

## 5. 公平对照与成本

任何以后声称低成本优势的方案至少比较：full exact sensitivity（若小尺寸可承受）、frozen rank-one surrogate、TBPTT、UORO/NoBackTrack、KF-RTRL、OK、SnAp、普通 future CE/BPTT、direct action predictor 与固定 learned updater。须记录 tangent bytes/dtype、随机样本数、rank/稀疏度、JVP/VJP 次数、激活/后缀 replay、truncation horizon、variance/bias、实际 wall time 与失败分母。

同样可见前缀与反馈是硬约束：未来 token 可在训练时提供后缀损失，部署不得读取未来答案、理想 edit、旧知识有效性 oracle 或事后奇异值。随机压缩没有创造外部证据。

## 6. 来源决定

处置为 **major component collision / useful Delta-specific control / no candidate admission**。这轮新数学足以关闭“rank-one write implies fixed-rank exact closed-loop credit”的错误推论，却不足以构造一个新 learned updater。计数保持 5 历史 / 0 活动 / 0 科学准入 / 0 选择。
