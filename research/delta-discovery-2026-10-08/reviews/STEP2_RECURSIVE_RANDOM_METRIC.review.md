# Step2 递归随机条件矩：独立数学与来源审查

状态：两位独立工作者已对最终字节作只读复核。本记录不把审查接受等同原创性、科学准入、代码实现或实验验证。

## 绑定对象

- 数学/处置：`STEP2_RECURSIVE_RANDOM_METRIC_CONTROL.md`
  - SHA256 `0e992547b81d56213d0b189a727f995cfddfa4ea69343794ad9084c0ed539cb0`
- 来源/接口/native：`sources/RECURSIVE_RANDOM_METRIC_SOURCE_AUDIT.md`
  - SHA256 `3091825d9bf093907a53dfb9ee4aec5f00e0946f16353c09c80f2aa5f75f6f84`

## 独立数学审查

身份：`/root/recursive_metric_math`。

初审结论：`revise`。审查者发现 horizon 权重没有进入 gradient/GGN 公式，本地 readout/loss residual curvature 没有在 exact Hessian recursion 中显式出现，而且只有 quadratic form、缺少实际 `Mv` 的 forward-JVP/backward-VJP 递推。修订后又补入对称 `Delta M` 与阻尼 `tilde M≻0` 的条件。

最终 exact-byte 结论：`accept`。审查者确认：

- `w_j` 已一致吸收到 `r_j,C_j`；
- `D_j=exact local Hessian-C_j` 与 costate 对 `nabla^2 F_j` 的收缩同时进入 exact `Q_j`；
- GGN `Mv`、exact-HVP 边界和 `z(u)=u^2` binary-CE 反例成立；
- resolvent/action-regret 与 Taylor 局部充分下降界的条件、符号和逆合法；
- teacher-forced/off-policy 边界以及 no-candidate 处置成立。

## 独立来源、代码接口与 native 审查

身份：`/root/recursive_metric_sources`。

初审结论：`revise`。审查者纠正 Kawano--Scherpen 的发表信息，并发现无法核实 `deepmind/synthetic_gradients` 为作者官方仓库，要求删除该 code pin。它同时补读并固定 Kazma--Taha variational-Gramian、Ollivier RTRL/Fisher、UORO、e-prop、iLQR 代码/公式接口及 bAbI、`lambada_openai`、LongMemEval 原生字段边界。

最终 exact-byte 结论：`accept`。审查者确认：

- Kawano--Scherpen 版本/期刊信息和 DNI “未定位可固定作者代码”表述准确；
- Kazma--Taha、RTRL/Fisher、UORO、e-prop、GGN/DDP-iLQR 的覆盖语义和固定 pins 一致；
- bAbI supporting facts、LAMBADA last-token 与 LongMemEval QA/evidence labels 都不提供 ideal edit、Jacobian、条件曲率或自由运行反事实；
- `major component collision / no candidate admission / no D / 5-0-0-0` 处置来源忠实。

## 共同未闭条件与决定

- prefix-only 条件 `g,M` 的函数逼近只从单后缀获得随机 teacher；自然文本下的泛化和条件均值估计未验证；
- edit 改变自由运行 future law 时，teacher-forced derivative 遗漏分布变化项；没有 overlap、交互环境或可信反事实模型；
- exact Hessian 与 GGN 的差、三阶余项和离散 retrieval/route 切换没有全局可用界；
- UORO/sketch 的无偏 sensitivity 不推出无偏 inverse/argmin；dense/CG/JVP/VJP 的 2080Ti 成本未测；
- 同信息 direct action、普通 CE、synthetic-gradient 与 DSSR rollout 是强简单替代，尚无 Delta rank-one 专用优势定理或 native 标签。

决定：`mathematically valid synthesis / major component collision / retain a narrow unadmitted structural lead`。不分配 D 编号，不进入全池排名或选择；维持 **5 历史 / 0 活动 / 0 科学准入 / 0 选择**。

执行边界：只读来源、静态数学、独立语义审查和标准库哈希；没有运行项目/上游代码、软件测试、训练、推理、评分、数据/模型下载、GPU 或 Docker。
