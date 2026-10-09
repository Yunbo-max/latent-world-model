# 全池排名尚未到达：当前活动池为零

目标是最多 20 个实质不同、数学成立且通过近邻审查的候选，再对完整池排序并默认选择前 15。构造历史现有 D01、D03、D05、D06、D07 五张卡；决定性审查已把五张全部移为控制、诊断或历史，当前活动池为 **0**。D07 的条件数学仍成立，但完整公式与作者代码审计确认：一般 source contribution、realized-path survival 及同-key 特例已被直接近邻覆盖，主功能又有 write-rate decay 与 delayed semantic supervision；只余 direct arbitrary-key hinge 的窄实现差异，不足以科学准入。

**没有全池排名、没有 method-selection、没有 selection-review，也没有 `selection_verified`。** 零张活动卡不能产生 top-15，五张被移出的卡也不能被反向计入排名。

D07 的比较对象是普通远期 CE、Delayed Supervision、How Linear Attention Remembers/RPMem 的 source trace/survival，以及 Tabular ICL 的 write-rate decay。其内部量 `||P k_i||²` 与 D03 的 future-readout metric、D06 的 global spectral floor 确实不同，但它仍可能提高状态范数而不提高 query 可见性，甚至保存过时事实。重新准入需要 formal arbitrary-key separation、与同信息语义监督的非等价、revision release 及可识别测量四项同时闭合。

本轮又闭合两个否定控制：裸 oblique erase 的精确奇异值 no-go，以及 evidence-conditioned revision edit 对 Bayes gate + protected/ridge/slot 几何的分解。它们减少无效路线，不增加活动计数。

最终排名仍将基于问题价值、数学后果、最近工作残余、区别性预测、最强简单替代及总成本。当前不得给出“最优 2–3 项”或暗示任何历史卡已获推荐。
