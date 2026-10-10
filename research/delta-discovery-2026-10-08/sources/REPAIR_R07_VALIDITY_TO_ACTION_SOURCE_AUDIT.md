# R07 真实性到动作边际：来源、作者实现与原生测量审计

状态：**final-byte review pending**。  
绑定对象：`repairs/R07_VALIDITY_TO_ACTION_MARGIN.v1.md`，SHA256 `e7e40477dc9eab96f7df18e9c30cba0bcbd65a4d9c67939d80f92579258be1ad`。  
检索/读取截止：2026-10-10 02:55 UTC。只把实际读取的 primary paper/full formula、固定作者仓库接口与原生 benchmark 字段写入；“未发现同式”不等于不存在证明。

## 1. 最近理论与机制碰撞

### 1.1 KnowledgeEditor：目标收益与非目标保持的受约束优化

- De Cao, Aziz, Titov, **Editing Factual Knowledge in Language Models**, arXiv:2104.08164v2 / EMNLP 2021：https://arxiv.org/abs/2104.08164 。
- 实际读取摘要及全文方法：作者训练 hyper-network，以受约束优化修改目标事实并尽量不影响其余知识；还用 paraphrase 扩充 edit target。R07 的“新 target 收益 versus 保护损伤”不是新的问题分解。
- 固定作者仓库 `nicola-decao/KnowledgeEditor`，commit `c1c0db35b65d498de6877ef5acf2ffa5321818a3`。`src/models/one_shot_learner.py` blob `99288bd16a74ea34aa22db68dc179dc5c28cad01` 的 `OneShotLearner.forward` 从条件输入与 supplied edit gradient 生成 gated update；矩阵 gradient scale 与 bias 用 outer-product 参数化。`src/models/bart_seq2seq_augmented_kilt.py` blob `cfb06912704bbbfdf9333ebdef1edd4953d8639f` 的 `get_logits_orig_params_dict`、`get_kl_lp_cr` 与 `training_step` 组合目标 edit、原模型 KL 与 constraint regularizer。本轮只作固定字节的静态接口审查，没有执行或下载模型。

### 1.2 AlphaEdit：已知保护子空间的硬零位移

- Fang et al., **AlphaEdit: Null-Space Constrained Knowledge Editing for Language Models**, arXiv:2410.02355v4 / ICLR 2025：https://arxiv.org/abs/2410.02355 ，全文 https://arxiv.org/html/2410.02355v4 。§2.2 Eqs. (4)--(6) 写 memorization/preservation least squares；§3.1 Eq. (7) 证明 `Delta'K_0=0` 时 `(W+Delta')K_0=WK_0=V_0`；§3.2 Eqs. (8)--(10) 从 `K_0K_0^T` 的小奇异方向构造投影；§3.3 Eqs. (11)--(15) 加入 previous-edit covariance。
- 固定作者仓库 `jianghoucheng/AlphaEdit`，commit `b84624f44dfe8fc6cd9e41df916c44124a0c46dc`。`experiments/evaluate.py` blob `2b154d9a2b6d3568d6b246b044b59ca270c09e9c` 的 `get_project` 由 `get_cov`、SVD 与 `S < nullspace_threshold` 构造 `U_small U_small^T`；`AlphaEdit/AlphaEdit_main.py` blob `6cc07e798bbc91e91d04ef7195d255d22a9c36c5` 的 `apply_AlphaEdit_to_model` 对 supplied `target_new` 算 residual、解 projected linear system 并更新 cache；`AlphaEdit/compute_ks.py` blob `2d33ef079b2f46689ba8cf90fd44490d6ab06433` 计算 key；`AlphaEdit/compute_z.py` blob `b204c90be297ed25571e563344eefab9a5f0dd9b` 优化目标 value。
- 对 R07 而言，`d_p=0` 会同时令保护线性项 `c` 与保护曲率为零，是明确强 baseline。AlphaEdit 不提供新事实真实性 `Y`，也不判断保护知识是否已过时；硬保护不能替代 validity-to-action 识别。

### 1.3 O-Edit：顺序 edit 与隐式知识方向的正交化

- Cai and Cao, **O-Edit: Orthogonal Subspace Editing for Language Model Sequential Editing**, arXiv:2410.11469：https://arxiv.org/abs/2410.11469 。
- 实际读取 §2--§4 与 Appendix B 的公式/伪代码：Eq. (1) 已把 edit pair `(x_t,y_t)` 当给定并要求 target 输出/域外保持；Eq. (24) 对累计 edit update 施加正交条件；Eq. (26) 从隐式知识梯度子空间移除已编辑方向；Algorithms 1--2 以 ROME/MEMIT 更新为底座，维护累计 `Delta W_total` 并逐次投影。论文实验的 CounterFact/ZsRE reliability/generalization/locality 与 OpenCompass SIQA/LAMBADA/CommonsenseQA/GSM8K 都是行为 endpoint。
- 本轮没有找到论文作者声明的官方代码仓库；不把同名或第三方仓库冒充作者实现。
- 这直接覆盖“用已知历史/隐式知识方向降低交叉干扰”的构造层面。它仍不从普通事实标签推出 action utility；R07 的残余只可能是有符号 margin/拒绝边界，不是再命名正交投影。

### 1.4 LyapLock：长期编辑收益与 preservation 约束

- Wang et al., **LyapLock: Bounded Knowledge Preservation in Sequential Large Language Model Editing**, arXiv:2505.15702v2 / EMNLP 2025：https://arxiv.org/abs/2505.15702 。
- 实际读取 §§3.2--3.3：作者把长期 edit loss 放在累计 preservation-loss 约束下，用 virtual queue / Lyapunov drift 得到逐步问题；论文 Eq. (12) 的 step objective 已显式组合 edit、历史 edited knowledge 与 preservation loss，随后给出闭式 perturbation。
- 论文链接的仓库 `caskcsg/LyapLock` 在固定 main commit `c5e6186c05808eea3a3507c866ddc2111111c07d` 的树 `59b890d037cbdb13590359ed4636da6533fad6cc` 没有可审查实现；该 commit 删除了唯一一行 “code will be released soon”。因此本轮能审查全文公式，不能把作者实现当已核实接口。
- R07 的标量 `benefit - signed protection cost - curvature` 与该类 constrained long-term edit objective 强相邻；R07 没有 LyapLock 的长期 queue，也没有其经验主张。

### 1.5 通用二次/鲁棒决策碰撞

R07 的 normal form

\[
\Delta_Y(a)=h_Ya^2-2a(Yb-c),\qquad 0\le a\le1,
\]

是单变量凸二次规划；区间上下界后的判断是 robust margin certificate。`clip(q/h,0,1)`、binary threshold `q>h/2`、Taylor remainder margin 均是标准凸决策结果。Delta 的专门性只在 rank-one `u=vec(beta k e^T)` 让线性项与曲率有结构化 JVP/readout 形式；若没有更低信息/计算代价或更紧统计界，不能把该 normal form 计为新方法。

- Elkan, **The Foundations of Cost-Sensitive Learning**, IJCAI 2001：https://mlanthology.org/ijcai/2001/elkan2001ijcai-foundations/ 。二类 posterior 加 cost threshold 是已知 Bayes-risk 决策；若 R07 只改写成真实性 posterior 超过成本比，它也不是新机制。

### 1.6 ROME/MEMIT/MEND：给定 target 后的 edit-success/locality 优化

- ROME：https://arxiv.org/abs/2202.05262 ，官方页 https://rome.baulab.info/ 。CounterFact 官方说明其目标就是 counterfactual；它检验学会反事实 target 后的 specificity/generalization，不提供独立 grounded truth。
- MEMIT：https://arxiv.org/abs/2210.07229 ，作者仓库 `kmeng01/memit` commit `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b`；`memit/memit_main.py` blob `c401ef483081b5f68e4fec908bb7c9b69ca1fbeb` 的 `execute_memit` 接受 supplied `target_new`，计算 value residual，并解 covariance-preconditioned linear system 后分层写入。
- Mitchell et al., **Fast Model Editing at Scale (MEND)**, arXiv:2110.11309v2 / ICLR 2022：https://arxiv.org/abs/2110.11309 。§2 定义 supplied desired output、equivalence-neighborhood generality 与 unrelated-input KL locality；§3.2 的目标 `L_MEND=c_e L_e+L_loc` 已显式平衡 edit 与 locality。Appendix C.4 还说明 edit label 可是 plausible/fictitious，进一步证明协议不是 grounded validity oracle。
- 固定 MEND 作者仓库 `eric-mitchell/mend` commit `e04fdb9cc784188906feffeb171025872933a5a8`：`trainer.py` blob `7ca58c85d0623101e14e5b12f016e36e24dac4df` 的 `EditTrainer.edit_step` 组合 edit/locality loss；`algs/mend.py` blob `711a6d544204aecb2bac9c8d68c01015fb0a47db` 的 `MEND.edit` 由 supplied labels 的 NLL 梯度生成 pseudo-gradient。
- 这些方法直接碰撞“已给 target 后如何兼顾修改与保持”，却都没有解决独立 `Y` 到未来 action utility 的识别。

## 2. 与项目已有控制的精确关系

- R03 已给 `Delta o(q)=a beta(q^Tk)e`、保护位移能量和 coupled horizon 上界；它主要给无符号 `||d_p||^2`，不能恢复 R07 必需的 signed cross term `c=<rho_p,d_p>`。
- R05 已证明不知道理想动作与敏感度的联合关系时只能部分识别；R07 只在 pointwise simultaneous margins 成立时提供一个 `Y->r_quad` bridge。
- R06 的 HT/AIPW 可估计选择性审计总体的真实性 moment；总体 moment 不能给单例 `b,c,h`，事后审计 `Y` 也不能回填同一时刻 online gate。
- AlphaEdit/O-Edit 是 `c`/干扰的构造控制，KnowledgeEditor/LyapLock 是 target-versus-preservation 的目标/约束控制；这些都是 R07 必须胜过的同信息 baseline。

## 3. 固定原生评估接口

沿用 R06 已固定并读过的资产：

- ROME/CounterFact：作者仓库 `kmeng01/rome` commit `0874014cd9837e4365f3e6f3c71400ef11509e04`，`experiments/py/eval_utils_counterfact.py` blob `80bb6be2b47c61b3fd2613d626955ff549615690`，函数 `compute_rewrite_quality_counterfact`。它解包 `target_new,target_true`，对 rewrite/paraphrase/neighborhood/attribute prompts 比较 token NLL，并另报 generation endpoints；这些是指定反事实 edit 的行为量，不是外部真实性或潜在动作效用。
- EasyEdit/KnowEdit：`zjunlp/EasyEdit` commit `4c109870955a4522ac3d7cf10ad00f34de8e4f0d`；`examples/KnowEdit.md` blob `15198d39aaef40a4adb71439821997d22061b4f8` 提供 prompt、`target_new`、`ground_truth`、portability/locality 字段；`easyeditor/evaluate/evaluate.py` blob `a7c0a2114e50b789aca828547c0db5227b3f6a9c` 实现行为评估。
- SEAL continual self-edit：`Continual-Intelligence/SEAL` commit `6d9c9f9ee392c6cc618e771f399d436d190f6ca4`；`general-knowledge/src/continual/continual_self_edits.py` blob `24fc1506c20b9a1f7159e51db6818ccc1bfeb137` 记录连续 edit 后当前/旧问题 accuracy matrix；`general-knowledge/src/inner/TTT_server.py` blob `ffa2b8f3e04ce45a3b8737645fd7819c88f0096c` 记录 pre/post outcome 与 adapter gain。
- AToKe：Yin et al., **History Matters: Temporal Knowledge Editing in Large Language Model**, arXiv:2312.05497 / AAAI 2024：https://arxiv.org/abs/2312.05497 。固定作者仓库 `Arvid-pku/ATOKE` commit `a1b42e34e4130507220307ced3d681fb8719831f`，README blob `3821549dfaa06a3b67b3605a27a33e1d209f2d98`；数据接口显式含 `time_true`、`time_new`、`history_evaluation`、`answer` 与 `new_answer`。它能测历史/当前事实随时间的有效性，因此把“完全没有保护 target validity 标签”的说法收窄为：CounterFact、KnowEdit 与 SEAL 的上述原生 scorer 不提供这种时间有效性，而 AToKe 提供时间标签但不提供动作级联合桥。

这些接口能测 edit efficacy、paraphrase/generalization、locality、portability、连续退化和部分下游能力；它们不原生联合记录：

1. 独立外部 grounded `Y`；
2. 动作前 Delta `b,c,h` 及其同时置信界；
3. 除 AToKe 这类带时间字段的数据外，每个保护 target 在 edit 时仍有效的证据；即使 AToKe 有历史/当前时间标签，也没有动作前 Delta 证书；
4. 同一事件的 write/no-write 潜在结果或 randomized propensity；
5. 自由运行 future distribution 的 total action effect。

所以 CounterFact/KnowEdit/SEAL 最多检验行为后果；AToKe 进一步给出历史与当前事实的时间有效性，但仍没有动作前 `(b,c,h)`、randomized propensity 或同一事件的 paired write/no-write 潜在结果，不能原生识别 R07 action-level bridge。新增 paired outcomes、随机动作记录或前缀证书会构成新协议；本阶段不造数据、标签、metric、case、scorer 或结果。

## 4. 来源结论与 residual

**CONDITIONAL THEORY CONTROL / MECHANISM COLLISION。** R07 的重要贡献是把“真事实也可能不该完整写入”从反例改写成可检查 margin，并明确纯位移能量缺少 signed protection term；这比无条件否定更有用。但主体数学是受约束凸二次决策，保护构造、顺序正交化和长期 preservation objective 已有直接近邻。

当前可保留的 Delta residual 只有：

1. 证明 rank-one Delta 使 `(b,c,h)` 在 prefix-only 信息下比直接 action-value predictor 严格更便宜或更易校准；
2. 证明同时界在完整 coupled state 下仍可递推而不回到 full Jacobian/rollout；
3. 找到原生、可授权的旧/新 validity 与 randomized action outcome；
4. 给出同预算样本复杂度、计算或拒绝覆盖优势。

这些均未由当前 R07 建立。不得声称首次、完整原创、长期安全、事实正确即写入、实验成功或 RSI。
