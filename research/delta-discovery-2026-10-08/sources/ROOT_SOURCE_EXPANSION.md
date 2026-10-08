# 有界近邻扩展与未闭条件

实际读者 /root，2026-10-08。只读取一手资料；未运行项目、测试、数据下载或模型。

## D01相关旧方法

Wilson/Nassar/Gold 2013 PLOS Computational Biology，doi:10.1371/journal.pcbi.1003150。读取Methods“Full Bayesian model”“Reduced model”，Eqs19–25邻近说明。多个Delta预测器按后验权重混合及减少状态的近似已有先例。HTML公式部分为图像，未逐式解码，不能宣称全文公式核验。

同时读取2018-06-26纠正doi:10.1371/journal.pcbi.1006210：原change-point prior错误曾进入代码，纠正后原Eq48的简化条件不再成立。不得借用旧图8–9解析性能结论。纠正指向bobUA/2013WilsonEtAlPLoSCB；GitHub API返回仓库迁移，返回的numeric repository重定向URL被connector拒绝，作者代码尚未固定。此项只是近邻线索，不能据此反向证明D01原创。

Dusenberry等2020 ICML，PMLR119:2782–2792，原PDF <https://proceedings.mlr.press/v119/dusenberry20a/dusenberry20a.pdf>，读取§2.2–3.4、Eq1–3。共享权重加rank-one乘法因子、多模态posterior和概率mixture已有成熟先例；其Bayesian slow-weight变分对象与D01单事件仿射fast-state差分不同。这个差异不是原创性裁决。Google/edward2作者代码只定位、未固定或检查，本轮不使用其代码作完成证据。

## 新近邻和来源范围

Voltic arXiv:2610.05700v1，官方摘要已检索；实际HTML/PDF均返回DisabledError。波动与随机性分离的概念已覆盖，全文机制/作者代码仍待来源补齐；不靠摘要排除碰撞。

Memory by Design arXiv:2605.31163v1全文可读，D01作者已读取；未来必须注明用v1，不将新版本检索记录混入这个固定阅读。Delayed Supervision arXiv:2609.32312v1 §3/§7已实际读取，普通延迟语义监督及隔离训练分支属于已知强简单解释。

本次搜索没有fieldwide saturation；相同公式/近似或名字不同不能计不同候选。后续最早合法动作是完成D01的低秩多模型/Voltic残余对照，以及D03可因果使用的metric估计条件，不能由“未找到”等同“没有先例”。

## D03的已知控制几何

Boyd/Lall Stanford EE263原讲义 <https://ee263.stanford.edu/lectures/observ.pdf>，本次读取全部7页，尤其p4的stacked observability matrix O和p6的nullspace条件。我们由此作代数映射：时变系统在h处的输出行是q_(t+h)^T P_(t+h,t)，加权堆叠后，O^T O=Σ_h ω_h P^T q q^T P，正是D03的实现目标Y。有限时域observability Gramian及其输出能量二次型是已知控制对象；并非新数学名词或新原理。D03仍待审的是从因果前缀预测该对象，并由它限制一次Delta写入的代价/必要性。

Q-Delta arXiv:2606.08804 / ICML2026 PMLR306:96722–96739，官方入口 <https://proceedings.mlr.press/v306/park26f.html>。官方摘要已实际读取，mixed key–query prediction errors及query参与状态更新已有覆盖；原HTML访问失败，官方PDF和作者psmiz/Q-Delta需进一步按公式和固定源码核查。不能仅凭名称或摘要断言它与D03等价或不同。

## 实际检索记录

provider: 当前search_service；engine版本未暴露，索引版本未知。日期2026-10-08，语言未限制，未设recency/domain过滤；技术结论只用一手来源。root本次system2查询原文：

- `low rank Bayesian ensemble fast weights delta rule retrospective memory mixture`
- `Voltic 2610.05700 delta volatility stochasticity`
- `Memory by Design Probabilistic Sequence Layers 2605.31163`

返回的关键一手条目：PLOS2013、PMLR2020、arXiv2605.31163、arXiv2610.05700、arXiv2002.06715；非一手条目未作结论依据。未保留完整raw-index快照或parser规范，故这不是满足collision saturation的正式search-run。这是明确的调查范围与缺口记录，不是准入替代品。
