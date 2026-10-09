# D05 最近工作全文审计：重大功能重合

结论：major_functional_collision; narrow_future_gramian_residual_not_admitted。D05 的条件性代数仍可作为有限精度控制基线保存，但不再计入 20 个活动候选，也不进入科学准入或选择。

## 被覆盖的核心功能

D05 用状态激励度量 \(C\) 白化，再以未来读出风险 \(O\) 对角化：

\[
T=C^{1/2}U,\qquad
T^{-1}CT^{-T}=I,\qquad T^\top OT=\Lambda,
\]

并对局部量化风险 \(\sum_i\lambda_i2^{-2b_i}\) 做连续 water-filling。三部分都已有强邻近基础：

1. 经典 fixed-point 状态空间实现已用 controllability/state-excitation 与 observability/roundoff-noise Gramian 选择 input-normal、output-diagonal 坐标并降低舍入噪声。D05 的 \(T\) 是该构造在 Delta 冻结路径度量上的直接专门化。主要来源包括 Moore (1981, DOI 10.1109/TAC.1981.1102568)、Mullis & Roberts (1976)、Hinamoto et al. (2003, DOI 10.1109/TCSI.2002.807512, Eqs. 7--16) 与 Corbin et al. (2025, DOI 10.1016/j.sysconle.2025.106178, Sec. 3)。
2. **STEPQuant**, arXiv:2609.38169v1（2026-09-29），已经直接面向 GDN/KDA 的 Delta recurrent state：Eq. 5 写量化误差递推，Eqs. 6--8 写生命周期混合位预算，Eqs. 9--10 写 key-row/readout impact，Eqs. 17--18 写校准重建。官方仓库 Dreamer-Toby/STEPQuant 固定 commit 61f24c9c2bc188b60a6c7525e7f86c7459bc737d，相关接口为 stepquant/core.py::{delta_step,row_impact,impact_factors,lifetime_weight}、calibration.py::{LayerStatistics,_distortions,calibrate}、allocation.py::{allocate_dp,allocate_lagrangian}、quantization.py::{fit_state,StateCodec}。
3. **DAMP**, arXiv:2608.27513v1（2026-08-27），Eqs. 8--10 已覆盖量化误差能量、decay persistence 与预算化高精度通道选择。论文未提供可固定的作者代码入口；“未定位”不当作代码不存在。
4. **MambaQuant**, arXiv:2501.13484v1, Sec. 4.2 Eqs. 10--13，覆盖 covariance/KLT 与旋转；**SmoothQuant**, PMLR 202，覆盖保持函数等价的通道缩放，官方 commit c61476f...；**LeapQuant**, arXiv:2609.38166v1，覆盖递归状态的低秩补偿和平滑。

## 仍然存在但不足以准入的字面残余

D05 与上述工作并非逐式同构：它定义完整有限时域 transported-query Gramian

\[
O_t=\sum_h\omega_hP_{t,h}^{\top}q_{t+h}q_{t+h}^{\top}P_{t,h},
\]

并联合 \(C_t\) 做全非对角广义特征基、连续 water-filling，以及 prefix-only 的 \(O_t\) 预测器。审计未发现单篇工作原样组合这四项。

但该残余是已知 balanced/input-normal realization、transform coding/rate distortion 与 STEPQuant/DAMP 问题设置的组合；它没有建立新的记忆原理。还留下 \(O(d^3)\) 分解、时变基对齐、预测漂移、重复量化交叉项、metadata 与混合位 kernel 成本。卡片证明仅覆盖一次局部量化注入，也不足以推出全轨迹收益。

## 处置

- 保留 cards/D05.json 和其独立数学审查，作为有条件成立的历史构造和强控制基线。
- 从活动候选数中移除；不宣称原创、verified、scientifically admitted 或 selected。
- 若未来重开，只能围绕一个经一手来源审查仍未覆盖、且不依赖已知模块机械组合的残余重新建卡；不能复用 D05 名称反向认证。

本审计只进行了论文/作者源码静态阅读；未执行项目代码、软件测试、量化、推理、评分、数据下载或 GPU 工作。
