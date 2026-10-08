# NOGO-RC-01：观测历史不能普遍区分真修订与地址碰撞

推导者：`/root/revision_protection_candidate`；状态：控制定理/否定路线，不计候选。日期 2026-10-08 UTC。未运行代码或实验。

令潜在类别 `C∈{R,C}` 分别表示 true revision 与 collision/coexistence；实际可见历史随机元素为 `H_t=X_≤t`，其生成 filtration `F_t=sigma(H_t)`。因果随机决策是两世界共享、类别无关的 Markov kernel，记 `q(h)=Pr(delta=R|H_t=h)`。两世界在可见历史上诱导 `mu_R,mu_C`，但要求相反动作，则

`P_R(error)+P_C(error)=1-int q dmu_R+int q dmu_C ≥ 1-TV(mu_R,mu_C)`。

等先验平均错误至少 `(1-TV)/2`；若可观测历史分布完全相同，至少 `1/2`。不等先验只保证 `R_pi≥min(pi_R,pi_C)(1-TV)`；精确 Bayes 风险是在共同支配测度下积分 `min(pi_R dmu_R,pi_C dmu_C)`。对任意公共独立随机量 `xi` 和 measurable randomized channel `Z=T(H_t,xi)`，Markov-kernel 数据处理给出 `TV(P_R^Z,P_C^Z)≤TV(mu_R,mu_C)`，所以类别无关的内部随机化、额外算力或 diffusion 不能凭空补充身份信息。若随机源或 kernel 本身携带类别信息，结论不适用。

Delta 特例：单位 k、`k^TS-=v-^T`、新观察 `v+`、`e=v+-v-`，更新 `S+=S-+beta k e^T`。若两个世界具有相同的全部算法可见信息，任何共享随机算法产生相同的 beta 条件分布；只有在共同随机种子的 coupling 下才能说 realized beta 相同。真修订世界的 squared error 是 `(1-beta)^2||e||²`。碰撞世界若同一个固定地址的 readout 以概率 `rho,1-rho` 分别服务旧/新目标，最优输出是 `rho v-+(1-rho)v+`，不可约风险为 `rho(1-rho)||e||²`；若约束 `o=v-+beta e`，最优 `beta=1-rho`。这个连续平方损失折中与前述二元相反动作下界是两个相关但不同的结论。

同样，语义 logistic target 在两世界相反时，所需梯度差一个 `-grad a`，但所有 observed-only objective/gradient 的分布相同。next-token、denoising 或 sequential change detector 只能利用可观测 continuation law 的差异；在 likelihood ratio 恒为一时后验赔率不移动。使用特定未来结果在线决定属于标签泄漏。

反例边界：重复 `v+` 仍可能由“一实体改变”与“第二实体重复出现”的同一流生成；timestamp 只有在另加 last-write-wins 假设时才有信息；近似相同历史保留 TV 下界。`e=0`、`rho∈{0,1}` 或 `grad a=0` 时相应风险/梯度差退化；`TV=1` 时测试下界为零。contextual key、entity ID、已有隐藏状态、未来证据或语义标签若真实区分两世界，就不在同一可见历史 law 的假设内。

最近替代：BOCPD/likelihood change detector 需要指定 observation-law shift；投影/OWM 只在保护集合已知后决定怎样保护；covariance 表示不确定性而非身份；slots/routing 添加 discriminator；D01 合法地保留两个假设。Adams–MacKay 2007 `arXiv:0710.3742v1` 全文已读，其 exact run-length posterior 在未剪枝时每步/总状态随历史线性增长；它不解决两假设观测律完全相同的情形。Page 1954 只核对 Biometrika 41(1–2):100–115、DOI `10.1093/biomet/41.1-2.100` 元数据，未作公式级审计。

理论归属是 Le Cam two-point / binary hypothesis testing 的 TV 下界、Markov-kernel 下 TV data processing，以及平方损失下 conditional mean 的 L2 Bayes 最优性；Delta 代入是实例，不宣称新定理。裁决：没有可执行新方法。合法逃逸只有显式 provenance/entity identity、保留多个假设、分配独立地址或接受 Bayes compromise；它们分别回到既有候选/基线。若在严格同可见历史 law、共享类别无关算法的 paired worlds 上有因果方法低于上述界，才反证本结论。
