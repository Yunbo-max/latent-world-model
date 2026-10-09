# R04 v2 独立来源与贡献审查

- reviewer：`/root/r04_source_review`，实际平台子代理，独立于writer。
- assignment：root指派修改后数学稿和来源审计的只读独立核对；不执行模型、作者代码、tests/评分/实验，不写仓库。
- reviewed_at：2026-10-09。
- artifact_ref：`repairs/R04_CONSOLIDATION_DYNAMICS.v2.md`，SHA256 `ba81ea9506160ee5e640faed2673ad068e925da82bb7ea77595999d7151f2732`。
- source_ref：`sources/REPAIR_R04_CONSOLIDATION_SOURCE_AUDIT.md`，SHA256 `22897c6cd9061bdf699860f294c317cb5428d524bb6949b9d89fe5517bae5ca4`。
- 字节核查：实际只读hash工具核对，两文件匹配assignment；结论不能继承到未来改稿。
- outcome：accepted_source_scope_and_conditional_control_not_originality_certification。
- 集成说明：root排版保存实际工作者报告，网页工具session refs改成来源审计中同URL的持久地址，保留证据和未闭项。

结论：来源归属和贡献范围表述可接受，无必须修改两份当前文件的来源错误；R04可保存为完成的条件理论/构造控制修复，不认证原创候选、实验效果或科学准入。

## 实际独立读取与核查

| source | inspected scope | result |
|---|---|---|
| Sleep 2606.03979v2 | §3.2–3.3及seeding objective训练说明 | 新低秩expert、prospective student、迁移前teacher、随后sender更新/reset准确；扩容蒸馏不是固定预算精确搬移。 |
| HOPE 2512.24695v1 | §7.1 Eq70–74 | 多频率、nested/sequential/head-wise变体准确；没有R04 additive全轨迹等价保证。 |
| eLife 105043.1 | UCL作者PDF Results/Online linear regression/Code availability | 总快慢输出/兼容控制学习信号明确；部分PDF公式缺失，进一步读作者实现。 |
| SynControl | d8681d2af9f858827fa1f22f7910e00eb2284fbc，run_simple_model.py::run和BayesLearner初始化/update | blobs 1b1984b15988d469f4e60a9645f22637a4349f08、bbc87aa387a565d0ca589bdcbe3b5853f8838b14匹配。 |
| SEAL | 6d9c9f9ee392c6cc618e771f399d436d190f6ca4，continual driver/TTT接口 | blobs匹配；实际tune/eval/记录旧QA再merge供下一轮，审计顺序准确。 |
| LongMemEval | 9e0b455f4ef0e2ab8f2e582289761153549043fc，README/QA prompt | blobs匹配；评分允许旧信息伴随正确更新答案，不证明内部迁移或释放。 |

公式来源： https://arxiv.org/html/2606.03979v2 ，https://arxiv.org/html/2512.24695v1 ，https://www.gatsby.ucl.ac.uk/~pel/papers/fast_slow_elife25.pdf 。实现的精确路径/blob和原生字段见绑定source_ref。

## 碰撞与残余差异

Sleep参数扩张及输出分布蒸馏与R04 affine compensation不同，不能从其经验结果推出固定预算无损巩固。HOPE CMS支持多时间尺度已知判断，但不能直接证明或反驳R04加性子模型定理。

SynControl是实质近邻：toy计算(w+dw)@X总误差，fast对所有synapse同一标量修正，slow扣除fast贡献；BayesLearner进一步维护误差估计、迟滞、control/Kalman gain和eligibility。总预测误差让快慢协调已知，不能作R04主创新。但代码没有R04离散M+=C,S−=C，也没有同式E(I−D)C搬移强迫项；rank-one、离散搬移和非交换decay是不同formal object。证据支持强baseline，**不足以断言整套条件理论已逐式覆盖**。

Patch A消去快状态即可得，单W复现轨迹；有诊断价值，无独立容量/预测收益。Patch B是已知快慢思想的Delta特化，具体传播式可保留修复成果；相同theorem/boundary的近邻检索未充分，不能升级理论原创认证。SEAL参数merge非快状态recurrence compensation，不得据merge证明无遗忘。

## 成本与原生测量

满宽M增存、同映射可表示、拟合和闭环变化成本已明确，限制必要。未来还须计慢参数持久化/读出、optimizer/eligibility和搬移；本文没承诺免费。LongMemEval has_answer/answer_session_ids为评价证据，不送部署更新器；knowledge-update终点评分容许旧信息，不能直接区分错误慢保留/双计/正确搬移。SEAL原生旧任务矩阵测参数遗忘，但7B、双GPU和GPT grader不视为满足项目预算。

符号定理无需伪造benchmark才成立；符号结果加终点QA也不证明持久化Delta提高跨任务学习效率。保留measurement gap合理。

## 未闭义务和决定

1. Sleep/HOPE作者实现未固定，阻塞实现级完整对照，不抹去已读公式。
2. 1987原文公式未闭，历史定位不证明完全覆盖。
3. 原创性检索未充分覆盖，不授予first/全新/候选资格。
4. 有效、可表示且值得搬移的C未给出，几何不识别过时知识。
5. 所有效益未实验验证，没有作者/模型程序执行。

决定：保存v2为repair/control，数学贡献范围明确、来源差异条件化、实际效果未知。接续可研究C联合收益/损伤目标与差异衰减的必要相互作用；无须永久淘汰整个consolidation，也不能增加active/qualified/selected数量。
