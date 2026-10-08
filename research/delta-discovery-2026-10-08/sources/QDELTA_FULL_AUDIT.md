# Q-Delta 全文与作者接口审计

审计者：`/root/qdelta_full_audit`；集成者：`/root`。日期 2026-10-08 UTC。只做一手论文、作者源码静态阅读；未运行源码、测试、推理或评分。

## 固定身份与读取范围

- 最终发表身份：Park, Kim, Park, *Q-Delta: Beyond Key–Value Associative State Evolution*, PMLR 306:96722–96739, 2026，<https://proceedings.mlr.press/v306/park26f.html>。PMLR 页面与代码链接已读；其 PDF 在本宿主暴露为 `application/octet-stream`，未解析，不能声称与预印本逐字相同。
- 公式来源：arXiv `2606.08804v1`，2026-06-07，<https://arxiv.org/html/2606.08804v1>。实际读取 §2.1、§3.1–3.3、Appendix B/C/D。
- 作者仓库：`psmiz/Q-Delta`，commit `4afe5b5146c02acab0e59eb44929e77cfe9c6cf9`，tree `72a94f93917eda03466f4d8414581820acde446e`。
- 关键 blob：`qdelta/qdelta.py` `b1760d35148a2de7ab010389c137e771e84a0c1c`；`qdelta/qdelta_rule/chunk.py` `66c95cc8da7f744dede3c1212dd66a2390e85b49`；`common/chunk_scaled_dot_kxt.py` `b4b233701569f062c8c831b287fdc75c46588f47`；`wy_fast.py` `064abb0ba2c60755437d4ef3cbb356c8f801ad04`；`fused_recurrent.py` `078a154453205555121a2f9b702ec5c632642594`；`modeling_qdelta.py` `fb3efe737b0c88e5a41c8d5b8180f7a55ad8a846`；340M/1B config `1cf6ed2f...`/`7227842d...`。

## 实际公式与保证边界

论文方向取 `S∈R^(d_v×d_k)`：

`vhat=S_(t-1)k_t`，`ohat=S_(t-1)q_t`，`x_t=k_t+lambda_t q_t`。Eq.17–20 为

`S_t=S_(t-1)+beta_t(v_t-S_(t-1)x_t)k_t^T`

以及带门版本

`S_t=alpha_t S_(t-1)(I-beta_t x_t k_t^T)+beta_t v_t k_t^T`，`o_t=S_tq_t`。

因此 query 改变混合残差/擦除 covector `x`；新增外积仍沿 `v k^T`。Table 1 的局部在线目标含 `Sk` 的线性配对项，论文也明确该更新不是 `||v-Sx||²` 的普通严格梯度下降。

Eq.8–15 将通用递推按实际顺序展开：历史 key 经过 `prod P_j^T` 传播后与当前 query 配对。这是与 D03 的实际数学重合，不能再声称“首次让未来传播后的 query 影响 Delta”这一宽泛贡献。

Lemma 3.1 在不含 `alpha` 的递推下给出

`v-S_tx=(1-beta k^Tx)(v-S_(t-1)x)`。

收缩要求 `beta k^Tx∈(0,2)` 及统一 `rho=sup|1-beta k^Tx|<1`。Theorem 3.2 还要求 mixed-target drift 一致有界。它约束当前混合误差，不是状态范数、长期保留、未来 read disturbance、CE 或最终 gated recurrence 的无条件保证；加入 `alpha` 后需相对 `alpha S_(t-1)` 重新陈述。

## 作者接口静态审查

`QDelta.forward` 分别投影 q/k/v，令 `beta=sigmoid(b_proj h)`、`lambda=sigmoid(lamb_proj h-lamb_bias)`、`alpha=exp(g)`；chunk 路径把 `lq=lambda` 传入 `chunk_qdelta_rule`。`chunk_scaled_dot_kxt` 和 `wy_fast` 实际使用 `x=k+lambda q`。训练只允许 chunk，语言模型仍用普通 shifted-token CE，没有额外未来矩阵目标。

固定源码中 fused-recurrent 分支没有从 `QDelta.forward` 传入 `lq`，其 kernel 是普通 gated Delta；`FusedRecurrentFunction` 还把 `lq/lk` 关键字传给不接收它们的内部 forward。这里仅记录**静态接口缺口**，没有执行，不能称为测试失败。`allow_neg_eigval` 会把 beta/lambda 乘二，超出论文 `[0,1]` 条件；发布 config 默认关闭。论文 Appendix 的 lambda bias 与最新 commit 的 `0.9` 也有小版本差异。

## 与 D03 的逐原子比较

转置到项目的 key-by-value 状态 `M`：

- Q-Delta：`barM=alpha Mprev`，`x=k+lambda q`，`Mnew=barM+beta k(v-barM^Tx)^T`。
- D03：`barM=DMprev`，先用训练期 ordered future query 形成条件预测 metric `G`，再解 `min u^T(G+lambda I)u`，约束 `k^Tu=1, ||u||≤R`，最后 `Mnew=barM+gamma u(v-barM^Tk)^T`。

Q-Delta 的写入地址固定为 k，残差 probe 是当前 x；D03 改写入地址 u，残差仍按当前 k，并且部署时只能用前缀预测未来传播 metric。Q-Delta 证明当前 mixed error 收缩；D03 只有冻结单次编辑的条件二次最优性和 metric 近似界。Q-Delta 保持 `O(LD²)` 与 chunk kernel；D03 的稠密参考构造要额外 transient `d²` metric、`d³` solve 和 teacher target。

裁决：**部分概念/数学碰撞，但更新机制不同**。Q-Delta 已覆盖 query-aware Delta 与伴随传播代数；未覆盖条件未来 observability metric、受约束左写入方向或精确当前 key 纠错。D03 可保留为条件数学候选，但 Q-Delta 必须是最强简单对照，原创性只允许落在这个狭窄残余；成本和可行性明显弱于 Q-Delta。更广 collision search 仍未饱和。
