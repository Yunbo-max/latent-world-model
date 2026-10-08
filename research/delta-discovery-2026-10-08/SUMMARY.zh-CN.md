# Delta 数学发现：第二批实际推导与审查

2026-10-08，从实时 `main` 的 `806692203c91112027084020b4f7a817687b756e` 继续。这是数学阶段的部分交付，不恢复已关闭的源码阶段。

目前有 **4 张实际构造卡、4 份独立语义审查**。四卡条件数学获得支持；D05/D06 在逐项修正后各有六项数学/方法检查闭合，但最近工作仍 pending。证据 checker 的 math-qualified 仍只有 D03；**科学准入 0，选择 0，20/15 目标未完成**。单次运行和定时启用不证明运行间隙连续工作。所有项目测试、软件、推理、原生评分、GPU与实验均未执行。

| 卡片 | 要解决的缺点 | 真正推出的构造 | 已知部分与残余差别 | 最可能失败处 |
|---|---|---|---|---|
| [D01](cards/D01.json) | 旧写入可能是真修订，也可能是近 key 的另一事实；当下残差无法独自判别 | 对一个尚未判明的事件保留两种编辑分支；共享未来仿射路径时，两状态之差精确保持为 `l eᵀ`。以一个基状态、两向量和后验对数赔率表示，后续真实观察重新加权旧编辑 | Bayesian predictor mixture、低秩共享与保护投影已知。残余是单事件 fast-state 差分的精确压缩与后验回溯接口；同样的两个完整状态 mixture 必须作为最强基线，预测完全相同 | 状态依赖特征破坏共享路径；多个歧义事件产生分支爆炸；未来更新可能抹去差分。后验权重针对两个策略，并不自动等于“语义真假” |
| [D03](cards/D03.json) | 当前 key 或历史 key 的几何不能描述一次写入经过未来更新后影响哪些 query | 把未来 query 逆向传输至写入时刻，构造有限时域可观测 Gramian；用实际前缀预测其条件均值，求保持当前 key 纠错量且有范数上界的最小扰动写入方向 | Gramian、矩阵预条件与约束二次优化已知。Q-Delta 全文已有 query-mixed residual 与 adjoint key；D03 的窄残余是用预测未来 transported-query metric 改左侧 write 方向 | 指标认为会被遗忘的方向代价低，可能把新事实写进容易消失的方向；保护旧输出也可能保护错误。密集求解与 teacher 目标生成成本高，单次冻结路径结论不保证真实网络收益 |
| [D05](cards/D05.json) | 同样数量的状态 bit 对未来输出的破坏可能高度不均匀 | 在正定激励度量下白化状态，再对冻结未来读出风险的特征方向做连续 water-filling 位分配；实数算术下只是坐标变换，不改变 Delta 轨迹 | 白化、balanced realization、transform coding 与 water-filling 都是已知数学。残余只可能是因果预测 Delta 的 future-read metric 并用于时变状态量化 | 证明只覆盖一次量化注入；指标漂移会使非均匀分配比 uniform 更差。重复量化、坐标刷新、metadata 和混合位 kernel 成本可能吞掉收益 |
| [D06](cards/D06.json) | erase/decay 连续花费体积，短期纠错可能不可逆地压低长期状态方向 | 把 `-log det A` 作为逐步支出，用滑窗 token budget 投影普通 Delta 门；在每因子谱范数不超过 1 时，给出窗口内 `sigma_min(P)>=exp(-B)` | determinant/singular-value 不等式、dynamical isometry 和约束门控均非新。残余是普通 Delta 的因果滑窗 log-volume 门投影 | 只保实数状态范数，不知道哪个方向语义重要；预算会削弱即时修订。反向依赖可贯穿后续序列，训练并行性与最近工作碰撞未闭 |

D01 的概率混合发生在两个归一化输出分布上，不能把两个状态取均值后 softmax 当作同一算法；只允许实际已经观察到的 token 更新证据，生成 token 不是外部事实。D03 的 suffix 只用于训练标签，推理输入必须是实际前缀。D05 的 future metric 也只可作 stopped training target，部署 predictor 只能读前缀；D06 完全不需要未来标签。四卡都未给确定性状态虚构 KL/ELBO。

本轮还得到两个不计候选的边界。`NOGO-RC-01` 用 Le Cam/总变差说明：若“真修订”和“相近 key 的不同事实”在现有因果信息上不可辨且要求相反动作，任何内部随机化（包括 diffusion）都不能创造证据；等先验平均错误至少为 `(1-TV)/2`。另一个投影边界精确推出保护写入的范数按 `1/||Πk||` 爆炸，`Πk=0,e!=0` 时不可行；但它与已知 protection/preconditioning 邻域重合，因此只保留为反例边界。

[CONTROL_MATH.md](CONTROL_MATH.md) 及其独立审查给出一个有用否定结果：QED 形状的斜投影更新可在单步特征值受控时有非正规瞬态放大；在明确参数下，两步乘积也能放大。这里只否定把谱界直接当作无条件乘积收缩证明的推论，并非运行 QED、证明训练不稳定或发现项目故障。此控制不计候选。

简单协方差释放（D02）没有推出超越已知近邻的构造；普通误差补偿（D04）与原文方法碰撞，保留[否定记录](DISPOSITIONS.json)，不凑入数量。历史不合格 Q01 和旧源码交付状态均保留。

原生可行性阅读见 [BASELINE_NATIVE.md](sources/BASELINE_NATIVE.md)：保留 bAbI 全 20 tasks/20,000 和 LAMBADA 全 5,153。LongMemEval 有真实知识修订任务，但现有 scorer 不证明内部旧关联保护，原生 judge 也有未授权服务/资源缺口；RULER 的原生 substring coverage 不等于语义真值证书。没有下载资产、造新任务/指标/标签或用数学反例冒充 benchmark。RTX2080Ti、每 arm/seed 的 0.1B/1B target-token 仅保留作后续成本背景。

本轮已完成 Voltic 与 Q-Delta 全文/静态作者源码对照：Voltic 强化 D01 的已知 mixture/不确定性邻域；Q-Delta 已有 query-mixed residual probe 和 adjoint/time-evolved key，但写方向仍是 k，故 D03 机制不同却残余很窄。下一前提是 D01 的低秩 recurrent ensemble、D05 的 balanced/transform/recurrent-state quantization、D06 的 log-det/constrained-gating 一手公式与实现审计，同时继续推导真正独立机制。当前不能给出全池排名或最终最优 2–3 项；四卡都只是待科学准入的数学线索。

入口：[进度](PROGRESS.json)、[证据批次](method-batch.json)、[近邻图](CLOSEST_WORK.md)、[排名状态](RANKING.md)。review 身份与实际 SHA256 均可查询。完整 author source 文本只留作读取缓存，发布固定版本/文件/函数及字节清单；不重新分发原始源码。
