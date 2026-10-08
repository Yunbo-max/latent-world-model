# D05/D06 最近工作：本轮读取范围与未闭边界

读取日期：2026-10-08。目的只是界定 D05/D06 的碰撞风险；引用不是原创性证明，也没有执行作者代码、项目代码或实验。

## D05（Balanced-Precision Delta）

- Dettmers 等，*LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*，arXiv:2208.07339；Frantar 等，*GPTQ*，arXiv:2210.17323；SmoothQuant（Xiao 等，ICML 2023）是后续必须逐式核对的强量化基线。本轮尚未完成它们与“未来读出风险下的递归状态坐标/位分配”的全文公式级对照。
- 本轮实际打开了 arXiv:2112.11438 的全文版本。其主张是用敏感度/Hessian 近似与优化分配语言模型权重的混合精度；对象是参数/层量化，而不是 Delta 的时变递归状态或冻结未来读出 Gramian。
- 本轮实际打开了 arXiv:1611.07065v2 的官方摘要。它研究低精度 RNN 权重/偏置及三值化；仅凭摘要不足以排除递归状态量化碰撞。
- classical balanced realization、transform coding/rate-distortion water-filling、旋转量化与 recurrent-state quantization 仍是主要未闭来源族。D05 的白化与 water-filling 都是已知数学；残余只可能是把因果预测的冻结未来读出风险用于 Delta 状态表示，且还需来源排查。

因此 D05 只保留为“条件代数已修复、最近工作 pending”的构造 lead；不计科学准入或选择。

## D06（Sliding Log-Volume Retention Budget）

- 本轮实际打开了 Chen、Pennington、Schoenholz，*Dynamical Isometry and a Mean Field Theory of RNNs*（ICML 2018）的 PMLR 官方页。其范围是初始化时信号传播/可训练性与 dynamical isometry；尚未读取到与逐 token Delta 门预算等价的构造。
- 本轮实际打开了 Helfrich、Willmott、Ye，*Orthogonal Recurrent Neural Networks with Scaled Cayley Transform*（ICML 2018）的 PMLR 官方页。其对象是正交 RNN 参数化，不等于对普通 Delta 的 erase/decay log-volume 支出施加滑窗 token-bucket 投影。
- log-determinant regularization、constrained recurrent gating、token-bucket/rolling-resource projection 与状态保持证书仍需一手公式/实现审计。当前 determinant/singular-value 不等式和滑窗预算数学本身都不是原创定理。

因此 D06 只保留为“普通 contractive Delta 下的条件性构造、最近工作 pending”；不能把它外推至 QED/D03 的斜/非收缩因子，也不计科学准入或选择。

## 证据边界

上述页面读取足以说明若干强邻居与对象差异，不足以完成穷尽性 collision audit。没有识别到等价方法不等于不存在；未定位作者代码也不等于代码不存在。后续必须固定论文版本、具体公式、作者实现 commit/文件/函数，才能关闭最近工作检查。
