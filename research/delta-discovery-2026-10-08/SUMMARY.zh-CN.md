# Delta 数学发现：最近工作淘汰与三个否定边界

2026-10-09，从实时 `main` 的 `1e9cf6099c19c77e622a976459858730f8bc0a23` 继续。这是数学阶段的部分交付，不恢复已关闭的源码阶段。

构造历史目前有 **4 张卡、4 份独立语义审查**，但 D05 经全文/作者接口最近工作审计被判重大功能重合，活动池降为 **D01、D03、D06 共 3 张**。D06 的限定近邻审计保留条件性残余，却没有原创性或科学准入结论。证据 checker 的 math-qualified 仍只有 D03；**科学准入 0，选择 0，距 20/15 目标仍很远**。单次运行和定时启用不证明运行间隙连续工作。所有项目测试、软件、推理、原生评分、GPU与实验均未执行。

| 卡片 | 要解决的缺点 | 真正推出的构造 | 已知部分与残余差别 | 最可能失败处 |
|---|---|---|---|---|
| [D01](cards/D01.json) | 旧写入可能是真修订，也可能是近 key 的另一事实；当下残差无法独自判别 | 对一个尚未判明的事件保留两种编辑分支；共享未来仿射路径时，两状态之差精确保持为 `l eᵀ`。以一个基状态、两向量和后验对数赔率表示，后续真实观察重新加权旧编辑 | Bayesian predictor mixture、低秩共享与保护投影已知。残余是单事件 fast-state 差分的精确压缩与后验回溯接口；同样的两个完整状态 mixture 必须作为最强基线，预测完全相同 | 状态依赖特征破坏共享路径；多个歧义事件产生分支爆炸；未来更新可能抹去差分。后验权重针对两个策略，并不自动等于“语义真假” |
| [D03](cards/D03.json) | 当前 key 或历史 key 的几何不能描述一次写入经过未来更新后影响哪些 query | 把未来 query 逆向传输至写入时刻，构造有限时域可观测 Gramian；用实际前缀预测其条件均值，求保持当前 key 纠错量且有范数上界的最小扰动写入方向 | Gramian、矩阵预条件与约束二次优化已知。Q-Delta 全文已有 query-mixed residual 与 adjoint key；D03 的窄残余是用预测未来 transported-query metric 改左侧 write 方向 | 指标认为会被遗忘的方向代价低，可能把新事实写进容易消失的方向；保护旧输出也可能保护错误。密集求解与 teacher 目标生成成本高，单次冻结路径结论不保证真实网络收益 |
| [D05（已移出活动池）](cards/D05.json) | 同样数量的状态 bit 对未来输出的破坏可能高度不均匀 | 条件性数学推出 `C/O` 白化和连续 water-filling，但只覆盖一次局部量化注入 | 经典 input-normal/output-diagonal realization 已覆盖坐标原理；STEPQuant/DAMP 直接覆盖 Delta-state 的有序误差、readout impact、生命周期与预算混合精度。完整 future Gramian 只是窄组合残余 | 重大功能重合；另有 `O(d^3)`、指标漂移、重复量化与 kernel/metadata 成本，故不科学准入 |
| [D06](cards/D06.json) | erase/decay 连续花费体积，短期纠错可能不可逆地压低长期状态方向 | 把 `-log det A` 作为逐步支出，用滑窗 token budget 投影普通 Delta 门；在每因子谱范数不超过 1 时，给出窗口内 `sigma_min(P)>=exp(-B)` | determinant/singular-value 不等式、dynamical isometry 和约束门控均非新。残余是普通 Delta 的因果滑窗 log-volume 门投影 | 只保实数状态范数，不知道哪个方向语义重要；预算会削弱即时修订。反向依赖可贯穿后续序列，训练并行性与最近工作碰撞未闭 |

D01 的概率混合发生在两个归一化输出分布上，不能把两个状态取均值后 softmax 当作同一算法；只允许实际已经观察到的 token 更新证据，生成 token 不是外部事实。D03 的 suffix 只用于训练标签，推理输入必须是实际前缀。D05 的 future metric 也只可作 stopped training target，部署 predictor 只能读前缀；D06 完全不需要未来标签。四卡都未给确定性状态虚构 KL/ELBO。

本轮新增三个不计候选的边界。`NOGO-MR-01` 证明：固定规定的 current-key 收缩时，任何线性擦除的全局最坏方向保留不超过 `1-beta`，普通 Delta 已达到 maximin 上界；改进只能换成 query-weighted 风险、放宽收缩、增加状态/读出或支付扩张与数值代价。`NOGO-OC-01` 给出完整仿射顺序差，其中同 key 不同 value 时 transition commutator 为零但写入顺序误差非零；精确 parallel scan 只需结合律，故 commutator-aware 路线不产生新架构。`TRANSPORTED-INFLUENCE-LEDGER` 在冻结仿射路径下等于 forward sensitivity/eligibility trace；无事件身份不可辨，有身份又退化为 exact-event replay。

之前的 `NOGO-RC-01` 仍说明：若“真修订”和“相近 key 的不同事实”在现有因果信息上不可辨且要求相反动作，任何内部随机化（包括 diffusion）都不能创造证据。投影边界仍说明保护写入会随 `1/||Πk||` 爆炸，`Πk=0,e!=0` 时不可行。所有这些都作为控制或淘汰依据，不增加候选数量。

[CONTROL_MATH.md](CONTROL_MATH.md) 及其独立审查给出一个有用否定结果：QED 形状的斜投影更新可在单步特征值受控时有非正规瞬态放大；在明确参数下，两步乘积也能放大。这里只否定把谱界直接当作无条件乘积收缩证明的推论，并非运行 QED、证明训练不稳定或发现项目故障。此控制不计候选。

简单协方差释放（D02）没有推出超越已知近邻的构造；普通误差补偿（D04）与原文方法碰撞，保留[否定记录](DISPOSITIONS.json)，不凑入数量。历史不合格 Q01 和旧源码交付状态均保留。

原生可行性阅读见 [BASELINE_NATIVE.md](sources/BASELINE_NATIVE.md) 与[本轮测量核查](sources/MEASUREMENT_FEASIBILITY_2026-10-09.md)：保留 bAbI 全 20 tasks/20,000 和 LAMBADA 全 5,153。BABILong 是 delayed influence 最有辨别力的现有 task×length 资产，RULER VT/NIAH 可作次级交叉验证；但没有原生 paired order-swap benchmark，commutator 主张仍是 measurement gap。LongMemEval KU/TR 语义接近，官方 QA judge 固定 GPT-4o，与无付费约束冲突，本地 70B 替代也不适合单卡 2080Ti。没有下载资产、造新任务/指标/标签或用数学反例冒充 benchmark。

本轮已把 D05 的最近工作前提闭合为否定处置，并对 D06 完成第一轮正交/谱/慢遗忘/体积保持邻域审计。下一前提是 D01 的低秩 recurrent ensemble、D03 更广 collision audit，以及 D06 的在线约束控制/Jacobian 下界/资源分配一手审查；同时继续推导真正独立机制。当前不能给出全池排名或最终最优 2–3 项；三张活动卡都只是待科学准入的数学线索。

入口：[进度](PROGRESS.json)、[证据批次](method-batch.json)、[近邻图](CLOSEST_WORK.md)、[排名状态](RANKING.md)。review 身份与实际 SHA256 均可查询。完整 author source 文本只留作读取缓存，发布固定版本/文件/函数及字节清单；不重新分发原始源码。
