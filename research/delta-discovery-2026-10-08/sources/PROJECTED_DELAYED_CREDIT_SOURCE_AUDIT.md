# Delta 投影延迟信用：primary-source、作者接口与测量审计

状态：2026-10-09 UTC 的 bounded source audit。它支持 `STEP2_PROJECTED_DELAYED_CREDIT.md` 的最近工作、实现接口和可测性边界，不是原创性证明、候选准入、项目实验或运行结果。角色为 `web_supervisor`；只读论文、作者网页、固定作者仓库和项目既有审计，没有 import、项目/上游代码执行、测试、训练、推理、评分、数据/模型下载、GPU、Docker 或付费调用。

## 1. 最直接的新碰撞：TTT Ouroboros

| 对象 | 固定身份 / 实际读取 | 与本线索的关系 |
|---|---|---|
| 论文 | [Self-Generated Feedback Destabilizes Test-Time Training: A Causal Decomposition of Long-Horizon Adaptation](https://arxiv.org/abs/2610.05076), arXiv:2610.05076v1, 2026-10-04；正文中 Fixed Generation、Recorded Replay、paired one-update、gradient conflict、Deferred Commitment / Settlement 段落 | 已经把生成反馈、读入与参数写入分开；用 `g_real^T Delta W` **诊断**真实文本梯度与候选更新的冲突；把候选更新放入 pending，等待以后到达的独立真实文本后，与未提交基线作顺序比较再提交。因而“未来真实文本到达后再 paired 验证/提交”和 pending lifecycle 是直接碰撞。论文明确没有把 `g_real^T Delta W` 用作 selection rule；同预算、部署合法的 projected-gradient selector 仍需另行查重和证明。 |
| 作者仓库 | [lingjivoo/ttt-ouroboros](https://github.com/lingjivoo/ttt-ouroboros), pinned observed commit `f7811f878679864e686c84abcd83dd05efdc0417` (2026-10-07) | 这是论文链接的作者实现；没有用第三方复现替代。 |
| `README.md` | blob `b116f6c2326791244647c23c75620f14725700fb` | 固定实验入口、模型系列和 causal decomposition/Settlement 导航。这里只读接口；论文结果不是本项目结果。 |
| `scripts/deferred.py` | blob `81687b3b992ddfe86ea2eb0561b529a828726380` | 实际维护 pending updates、baseline/candidate probe、顺序 validation、capacity eviction 与 lifecycle accounting。它是比抽象描述更强的实现碰撞。 |

关键区别也必须保留：该工作研究参数级 TTT/生成反馈失稳，而本项目的正式对象是 key-by-value Delta 状态及其动作空间信用。动作子空间的表示下界和 frozen-path rank-one eligibility 并未由这次 bounded read 宣称被其覆盖；但如果新提案只是“延迟真实文本验证后提交”，则已经直接碰撞。

资源边界：作者配置面向 CUDA 和 125M/760M/3B 或 Qwen3-4B 等模型。它证明存在公开因果控制实现，不证明 RTX2080Ti 可运行，也不允许把论文观察搬成本项目实测。

## 2. 长时程 meta-gradient / learned-optimizer 近邻

| Work | 固定来源与读到的机制 | 边界 |
|---|---|---|
| MAML | [Finn et al., ICML 2017](https://proceedings.mlr.press/v70/finn17a.html), arXiv:1703.03400v3, §2.2 / Algorithms 1–2；作者仓库 [cbfinn/maml](https://github.com/cbfinn/maml)，本轮定位到 `maml.py:MAML.construct_model`、nested `task_metalearn`、`inputa/labela` inner update、`inputb/labelb` post-update meta-loss、`FLAGS.stop_grad` 一阶近似，但没有可靠固定当前 commit | post-update 真实 query/future loss 的 meta-gradient、HVP 和一阶近似已是标准对象；“多步更新后用未来损失训练”本身直接碰撞。作者 commit 未闭合，不能虚构 pin。 |
| Learned optimizer | [Andrychowicz et al., NeurIPS 2016](https://arxiv.org/abs/1606.04474), Eq.(1)–(3) | 带 hidden state 的 learned updater、整段轨迹 outer loss、BPTT、截断和丢二阶项均已覆盖。未定位可确认的作者实现；第三方复现没有被当作者代码。 |
| Efficient Long-Horizon Learning for Learned Optimization (ELO) | [arXiv:2607.06772](https://arxiv.org/abs/2607.06772), current observed v4; author repo [xiaol827/ELO](https://github.com/xiaol827/ELO), pinned observed commit `664ef6503ae8d2b1d5b89b551680eff91472574a`; `README.md` blob `3845ed70fd8ac1dc236d9309988c8446dd0410d7`, actual long-unroll paths include `src/lopt_truncated_step_elo.py` and `src/truncated_pes_custom_elo.py` | failure-aware resume buffer、Persistent Evolution Strategies (PES) 和 progressive expert supervision 已直接处理 learned optimizer 的长 horizon 训练；不能把“延迟 outer loss + 截断/恢复”当 Delta 新意。它没有自动给出本文动作-span 维数下界或完整闭环下的低秩误差界。 |
| DNI / Decoupled Neural Interfaces | [Jaderberg et al., 2017](https://proceedings.mlr.press/v70/jaderberg17a.html) | synthetic gradient 预测未来信用；若本线索只学 `B^T lambda` critic，则属于必须比较的近邻。 |
| RTRL | Williams & Zipser, 1989；另见 [Ollivier, 2017, §3.1](https://arxiv.org/abs/1703.00209) 的 RTRL sensitivity / online Fisher 形式 | exact online state-to-parameter sensitivity；不截断但状态和更新成本高。 |
| UORO | [Tallec & Ollivier, 2018](https://arxiv.org/abs/1702.05043); author repo `ctallec/uoro@135a057edcd83fda17db5785607cf4af1fb0cfdd`, `uoro.lua` blob `96134bb7c07fc60e242aa5711d44bf4fd8bb1e6b` | 对 RTRL sensitivity 的 unbiased stochastic rank-one approximation；不是 exact sensitivity。 |
| e-prop | [Bellec et al., 2020](https://www.nature.com/articles/s41467-020-17236-y); author repo `IGITUGraz/eligibility_propagation@efd02e6879c01cda3fa9a7838e8e2fd08163c16e` | eligibility-trace 因子化配合近似/局部 learning signal；不能与 exact RTRL 混称。Delta 的残余只能是明确的因子化成本/误差后果。 |
| ACL / SRWM | [Metalearning Continual Learning Algorithms](https://arxiv.org/abs/2312.00276); author repo [IDSIA/automated-cl](https://github.com/IDSIA/automated-cl), pinned `3d7b53adb4b6b43acd82b9a381a2c631d0e59a5d` | SRWM 自生成 value/target、key 与 learning-rate pattern 的 rank-one Delta update，并在图像/分类式 in-context continual-learning 设置中用新旧任务 meta-objective；它不是 LLM 自然语言 update directive。只把 outer loss 接到 Delta recurrence 不构成剩余。 |
| DSSR | [arXiv:2609.32805v2](https://arxiv.org/abs/2609.32805)；匿名作者代码页的可见固定 token：`README.md` `b635535a`, `dssr/score.py` `0f30b28b`, `scripts/score_candidates.py` `7ef1af52`; interfaces `ScoreJob`, `Target`, `subset_scores`, `sufficiency_matrices_recursive_many` | 在固定 logged future 上递归 rollout 同一 writer，再以冻结 reader 的未来 reference-action likelihood 评分，直接覆盖“固定未来后缀评价写入”。匿名代码没有 Git SHA，token 不是 commit；其至少 32GB 单 GPU 要求也不适配 2080Ti。残余是 edit 改变未来分布时的因果识别和 Delta 结构成本。 |
| SEAL | [arXiv:2506.10943v2](https://arxiv.org/abs/2506.10943); author repo [Continual-Intelligence/SEAL](https://github.com/Continual-Intelligence/SEAL), pinned `6d9c9f9ee392c6cc618e771f399d436d190f6ca4` | downstream reward 学 self-edit，且作者连续 self-edit 结果保留了遗忘负证据。普通 downstream delayed reward 不新；部署自改 updater 也未由其自动证明。 |
| HOPE / Nested Learning | [arXiv:2512.24695](https://arxiv.org/abs/2512.24695), §§7.1–7.3 / 8.1–8.3：CMS Eq.(70)–(74)，自适应模块 Eq.(79)–(88)，chunk-frozen Eq.(90)，self-modifying memory + CMS Eq.(94)–(97)；[Google Research overview](https://research.google/blog/introducing-nested-learning-a-new-ml-paradigm-for-continual-learning/) | 是 self-modifying multi-frequency memory / 快慢组合的 broad conceptual neighbor，不自动覆盖 projected Delta action credit。未找到可固定的作者实现来消解 Eq.(90) chunk 索引与 Eq.(92) target/sign 记号问题；不用第三方实现填空。 |

本轮没有声称穷尽 2026 年全部文献。上表只支撑明确的机制碰撞和残余义务：若要保留“projected delayed credit”，必须比较 synthetic critic、直接 action predictor、普通 future CE/BPTT、PES/截断 learned optimizer、以及 Ouroboros 的 paired Settlement。

## 3. 原生测量可行性

| 资产 | 原生对象 / scorer | 能测到 | 不能认证 / 资源问题 |
|---|---|---|---|
| [CITB](https://github.com/hyintell/CITB), [paper](https://arxiv.org/abs/2310.14510) | InstrDialog 19 tasks / InstrDialog++ 38 tasks；任务矩阵上的 ROUGE-L、AR、FWT、BWT。本轮未固定仓库 commit/scorer path，故只是论文/仓库支持的 feasibility mapping | 输出级任务保持、BWT、未学任务零样本迁移 | FWT 不是学习速度；不识别理想 Delta action 或旧事实是否仍有效。完整逐步矩阵约为 `O(T^2)` 评测。 |
| [TRACE](https://github.com/BeyonderXX/TRACE), [paper](https://arxiv.org/abs/2310.06762), observed commit `462e39f616134f4f819efeb3baea8638c03c7db4` | 8 tasks，约 40k train/16k test；OP/BWT 与 general/instruction/safety deltas；`metrics.py` 含 task-dependent exact/F1/fuzzy/ROUGE-L/BLEU/SARI | 参数级连续学习的旧任务退化和广泛能力变化 | 原实验 7B/13B；GPT-4 judge 主要涉及 instruction-following/safety 路径，不是全部 task metric。对象不是 fast-state Delta，且无原生未来学习速率。 |
| SEAL continual driver | pinned `6d9c9f...`; `general-knowledge/scripts/continual_self_edits.sh`, `src/continual/continual_self_edits.py`, `src/utils.py`。SQuAD 风格 passages/questions；每轮 LoRA merge 后评全部已见问题，形成 lower-triangular accuracy matrix | 连续 self-edit 后已编辑问题的输出保持；是重要负/对照资产 | 默认 Qwen2.5-7B、`#SBATCH --gres=gpu:2`、GPT-4.1 grading；不提供旧事实有效性 oracle、基础能力全貌或 updater 自改证据。当前 no-paid/single-2080Ti 条件阻塞原生执行。 |
| [LongMemEval v1](https://github.com/xiaowu0162/LongMemEval) | 500 questions，含 knowledge update/temporal/abstention；QA endpoint 和 evidence session IDs | 最终长历史 QA、更新和时间推理 endpoint | 不是顺序学习矩阵或 updater 学习率；官方 QA judge 有付费依赖。answer/evidence IDs 不得输入更新器。 |
| [LongMemEval v2](https://github.com/xiaowu0162/LongMemEval-V2) | 451 questions；统一 Insert/Query interface；answer accuracy 与 query-latency/LAFS frontier | 超长 agent history 的查询准确率—延迟权衡 | reader/embedding/judge 是额外大模型资源；不测 Delta updater 学习或逐步旧能力损伤。 |
| [StreamingQA](https://github.com/deepmind/streamingqa), [paper](https://arxiv.org/abs/2205.11388) | 2007–2020 的 14 年 timestamped WMT news；主要按季度评测，`recent` 是问题日前一个月，另有 monthly fine-tuning 分析；normalized EM/F1 | 时间知识更新后的输出适应 | past 不等于逐事实有效性标签，数据/训练规模也远超本阶段。 |
| bAbI / LAMBADA | bAbI generator `facebookarchive/bAbI-tasks@ccd8fd6...` 与 ParlAI `a29567f7ce76992fd1f03c51ba9e3b155a37ea51`；20 tasks × 1,000 test = **20,000**。项目实际 LAMBADA variant 为 lm-eval `d6de81643928d653435c431bae19945d41d32520` 的 `lm_eval/tasks/lambada/lambada_openai.yaml`，test=**5,153**，last-word loglikelihood/greedy exact accuracy | 受控状态推理与语言 endpoint | 都不标注 action credit、write/no-write potential outcome、updater 改进或学习速度；不能与 `lambada_standard` 混报。 |

结论：没有一个已审查原生资产同时证明“学到更新规则、减少仍有效旧能力损伤、提高以后学习速度、部署中继续改进 updater”。CITB 最接近任务级保持/迁移；SEAL continual 最接近连续 self-edit 遗忘；Ouroboros 最接近候选写入的独立后缀验证。中央的 learning-speed 和 RSI 主张仍是 measurement gap。

## 4. 信息公平和因果边界

合法训练信息是当前已到达样本/标签、到达后的真实未来 token、协议允许且为所有 baseline 同样提供的 replay，以及已观察随机化日志。部署动作不得读取未来 token、未来答案、test label、理想 edit、旧知识有效性 oracle、LongMemEval answer/evidence 标签、bAbI supporting facts 或事后 judge verdict。

固定后缀上 write/no-write replay 可给该 checkpoint 和 teacher-forced graph 的 paired prediction loss；它不自动给自由运行总效应，也不标注事实有效性。观察日志的 IPS/DR 需要 sequential exchangeability、support、propensity/outcome 条件与方差记账。模型自评/自生成未来不是新的外部因果证据。

最强简单对照必须至少包括：no update、标准 Delta、同特征 scalar gate、普通 future CE/BPTT、同信息 direct action predictor、固定 outer-trained updater、同容量 low-rank updater、LoRA/SFT、等存储 replay、EWC/OGD/GEM/A-GEM，以及在允许外部历史时同原文访问量的 BM25/RAG/full-history。公平性按实际 bytes/dtype、raw-text/index、反馈 token、累计算力、激活重算、验证前滚和调参次数记账，不只按参数量。

## 5. 来源决定

来源结论为 **direct collision + residual open**：

1. Deferred validation/Settlement 已被 TTT Ouroboros 的论文与作者实现直接覆盖；不能作为候选。
2. delayed outer loss、synthetic gradient、online sensitivity、PES/长 unroll 和 learned Delta rule 均有强近邻。
3. 本轮剩余的数学对象是更窄的：动作空间投影充分性/维数下界、frozen-path 单 edit 的 rank-one eligibility，以及在完整闭环下能否得到同预算的近似误差或统计优势。
4. 现有原生资产尚不能认证 learning-speed 或部署中 updater 自我改进；不能靠自造 metric 或论文结果填补。

因此该线索保持 Step2 控制/lead，不分配 D 编号，不改变 5 历史 / 0 活动 / 0 科学准入 / 0 选择。

## 6. 检索边界

使用 primary paper / official author page / author-linked repository 定位；作者仓库以观察到的精确 commit 和 blob 固定。搜索只用于定位这些 primary sources，不以摘要或第三方实现替代全文/作者接口。没有下载数据/模型或运行仓库。当前检索不是穷尽 originality certification；未来若该残余进入完整候选，仍需针对 action-projected critics、low-rank adjoints 和 recurrent meta-gradient compression 做更窄的查重。
