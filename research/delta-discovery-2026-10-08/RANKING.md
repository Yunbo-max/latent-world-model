# 全池排名尚未到达

目标是最多 20 个实质不同、数学成立且通过近邻审查的候选，再对完整池排序并默认选择前 15。构造历史现有 D01、D03、D05、D06、D07 五张卡；决定性审查已把 D01/D03/D05/D06 移为控制或历史，活动池只剩 **D07 一张**。D07 的条件数学和独立审查成立，但函数级作者代码/完整公式碰撞审计、科学必要性和原生测量仍未闭。

**没有全池排名、没有 method-selection、没有 selection-review，也没有 `selection_verified`。** 单张活动卡不能产生 top-15，四张被移出的卡也不能被反向计入排名。

当前活动线索 D07 的比较对象是：普通远期 CE、Delayed Supervision、How Linear Attention Remembers 的 source trace，以及 Tabular ICL 的 write-rate decay。其内部量 `||P k_i||²` 与 D03 的 future-readout metric、D06 的 global spectral floor 确实不同；这只证明对象 distinctness，不证明外部原创性或任务收益。D07 可能提高一个状态方向的范数却不提高 query 可见性，甚至保存过时事实，因此科学准入仍为 0。

本轮新增/闭合的否定控制包括 exact-overwrite/reversible-retention no-go 与 deferred-correction debt 的 error-feedback 等价；DeltaTTT 又排除了“多层/local-target/nonlinear Delta”作为伪新候选。这些结果减少无效路线，不增加活动计数。

最终排名仍将基于问题价值、数学后果、最近工作残余、区别性预测、最强简单替代及总成本。当前不得给出“最优 2–3 项”或暗示 D07 已获推荐。
