# 数据与原生评测协议提案

日期：2026-10-07。角色：web_supervisor。状态：**source-inspected / generated_unexecuted；尚未冻结，尚未经 Local 资格验收**。本文件是源证据与可执行命令草案，不是运行回执、结果或 Gate PASS。本轮仅读取作者论文、作者代码、Hub 元数据和少量真实数据行；没有下载训练语料、评测全集或权重，没有运行项目代码、训练、推断或 scorer。

## 1. 建议锁定的最小覆盖

| 资产 | 用途 | 能支持的范围 | 不能支持的范围 |
|---|---|---|---|
| FineWeb-Edu sample-10BT 的确定性前缀，GPT-2 tokenizer | 100M / 1B token 预训练；独立留出的语言建模开发损失 | 同一语料、预算和 tokenizer 下的学习与成本比较 | 不证明世界状态具有可解释语义；验证集损失不代替原生任务 |
| bAbI v1.2，English 10k，完整 20 tasks，ParlAI 原生 train/valid/test | 有监督适配后的状态跟踪与组合推理 | task 1/5/7/8/9/10/14 的状态更新，task 2/3/15/17/18/19 的组合计算；其余任务保留完整报告 | 这是已发表的合成诊断基准，不是新造的诊断例子，也不能外推到真实长时自主智能 |
| LAMBADA OpenAI English，完整 5,153 test passages，零样本 | 不经 bAbI 适配的预训练 checkpoint 的语言模型诊断 | 广篇章上下文下的末词准确率与末词 perplexity | 不证明持久世界状态、动作模型或因果规划；小模型可能准确率很低 |

bAbI 的两个必要机制对照仍使用**相同原生故事、问题、标签和 scorer**：保持/清空跨事实持久状态，以及固定同一权重时改变问题后的内部迭代次数。它们不是新 benchmark。信息可见性、总计算量、训练机会须匹配；仅增加循环次数带来得分变化不能单独识别“内部推理”。完整方法和对照队列由主方案冻结，本文件不替代它。

预训练后的零样本 LAMBADA 与 bAbI 有监督适配后评测属于不同轨道。**不能把 100M-token 小模型的 bAbI 零样本失败当作记忆机制失败**。bAbI 适配必须对全部方法使用相同原生训练问题、顺序、监督字段和预算。

## 2. 不可变来源与实际阅读范围

| 来源 | 固定版本 | 实际检查 |
|---|---|---|
| [FineWeb-Edu](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu) | 87f09149ef4734204d70ed1d046ddc9ca3f2b8f9 | 数据卡、sample/10BT 的 14 个文件的字节数与 LFS SHA-256、live rows API 的一行 |
| [GPT-2 tokenizer](https://huggingface.co/openai-community/gpt2/tree/607a30d783dfa663caf39e06633721c8d4cfcd7e) | 607a30d783dfa663caf39e06633721c8d4cfcd7e | 文件清单、Git blob ID、大小；不取模型权重 |
| [ParlAI](https://github.com/facebookresearch/ParlAI/tree/a29567f7ce76992fd1f03c51ba9e3b155a37ea51) | a29567f7ce76992fd1f03c51ba9e3b155a37ea51 | bAbI build.py、agents.py、三个 all10k 原生样例文件、FbDeprecatedDialogTeacher、TeacherMetrics / ExactMatchMetric / normalize_answer、convert_data_to_parlai_format.py、eval_model.py |
| [Recurrent Entity Networks 作者实现](https://github.com/facebookarchive/MemNN/tree/d7c5f6d5e1a4af6417ffff98535a96bb0947a6a8/EntNet-babi) | d7c5f6d5e1a4af6417ffff98535a96bb0947a6a8 | README、data.lua、main.lua；已有持久实体状态的强相关基线。旧 Torch7/CUDA 依赖未在当前 GPU 主机验证 |
| [LAMBADA OpenAI 数据](https://huggingface.co/datasets/EleutherAI/lambada_openai/tree/900124bf3b8235c6daf21033af9948b3f07346c4) | 900124bf3b8235c6daf21033af9948b3f07346c4 | metadata、data/ 与 en/test/ 文件身份、live rows API 一行；default 与 en JSONL 是相同 LFS 对象 |
| [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness/tree/d6de81643928d653435c431bae19945d41d32520) | d6de81643928d653435c431bae19945d41d32520 | lm_eval/tasks/lambada/lambada_openai.yaml、README、ConfigurableTask.process_results、metrics.mean/perplexity、HFLM 末词 token likelihood/greedy 判定、CLI 与 pyproject |

相关原论文：
- [FineWeb，2406.17557](https://arxiv.org/abs/2406.17557)：作者发布的现成开放教育文本来源；sample-10BT 是约 10B GPT-2 tokens 的随机样本，不等于本项目精确 token 计数。
- [bAbI，1502.05698v10](https://arxiv.org/pdf/1502.05698)：第 3 节任务与第 5 节评分，答案按对错计；95% 是作者约定的任务通过阈值。
- [EntNet，1612.03969v3](https://arxiv.org/pdf/1612.03969)：第 5 节 10k / v1.2 数据、平均错误率、失败任务数；附录的联合训练不能混同于逐任务训练。文章区分状态估计与预测世界演化，二者不能互相替代。
- [LAMBADA，ACL 2016](https://aclanthology.org/P16-1144/)：原始任务定义。当前选择的是 harness 所定义的 OpenAI 处理版本，不能冒称原始 LAMBADA 字节级复现。

许可证记录：FineWeb-Edu 数据卡为 ODC-BY；tokenizer 模型卡为 MIT；ParlAI 代码为 MIT。LAMBADA OpenAI 数据卡标为 MIT，但需同时保留其原始文学文本来源说明，不能把托管卡片许可证理解为对原小说的无限再分发授权。数据留在用户已有资源上的输入缓存；结果仓库保存清单/哈希和预测，不提交整个训练语料。

## 3. FineWeb-Edu：文件清单与容量界限

原生配置 sample-10BT，原生 split=train。源 API：
https://huggingface.co/api/datasets/HuggingFaceFW/fineweb-edu/tree/87f09149ef4734204d70ed1d046ddc9ca3f2b8f9/sample/10BT?recursive=false&expand=false

下面每个 SHA-256 是 API 返回的 LFS 内容对象身份，不是本地臆造的校验值。全部文件共 **28,518,193,415 bytes**；前两个共 **4,305,041,546 bytes**。

| 文件（相对于 sample/10BT/） | bytes | SHA-256 |
|---|---:|---|
| 000_00000.parquet | 2152819114 | b1ba7b2ce4cb5ea6ef42dca40263eabb85f37700d01693a68e9b30a31d78e871 |
| 001_00000.parquet | 2152222432 | 3fcf2dc69cd52503986276d3d2d26a8c356d0f2ea28a0de4fdbda8cf87755693 |
| 002_00000.parquet | 2151796315 | 547ae182d132c9f06b6ce63149567208ea9f57630bfd9b1a2938e504f0c9ebd7 |
| 003_00000.parquet | 2152437524 | 22184e6eb25759ddd97783751ffc73e1705dfa2542e630dae1f2a8bac8ee6ddb |
| 004_00000.parquet | 2152338550 | 33557ddd87a07a4ae6fcaf7a4789c7b484e5cc0c273ca12a65b74200e6d8748b |
| 005_00000.parquet | 2152189947 | e08d79927ecb377786572cd854817c748ceb8880878b1a0eb91abf8c85d505ea |
| 006_00000.parquet | 2152689867 | 554fa2613c9261d6c9c396caab881de3160175794c6c3e1856bf28a0e9cb9b76 |
| 007_00000.parquet | 2150686637 | 4b7d1f697d4afff7f5f65cb7aa4d83acc6db716da4d46ea23399d0c50608c6e3 |
| 008_00000.parquet | 2151274846 | a6d9dcc0c72ecd7c7f0173c2d06b3a4249a2ccaa94961469d1a522ca689bbf1a |
| 009_00000.parquet | 2151913277 | f836cd3c70b95776699eb6c356b2dbf702816e25dcf39992f5c80a29029d23c3 |
| 010_00000.parquet | 2152798864 | e5a2eae25f057f0856a10bfae314c6ca8ea8bb08456d2131e9e89b2b8305e2f6 |
| 011_00000.parquet | 2152323681 | db71cf0425bb3d1813a09f12ff1acd6dabdfb91a2e4f141960254ee5a7f036e7 |
| 012_00000.parquet | 2152069689 | 08b47a3e1c25161f796d2f8dbf99ccf60affdebdcea4910833d0d5783315551f |
| 013_00000.parquet | 540632672 | b393f51fefab26cd6f4c8f65707c1924f6666c4961a0ebebe04bb57f7ec832de |

Local 默认先取前两个；若去重/切分后不足，则严格按表顺序追加，不跳 shard、不重采样。14 个全部处理后仍不足则明确失败，不重复数据补足。下载硬界限为 30,000,000,000 source bytes；输入/预处理工作区先验磁盘预留 50 GB，**这是建议容量而非实测峰值，且不含模型 checkpoint、Conda 与全部实验日志**。1B uint16 target tokens 为 2 GB；文档索引、校验文件、临时下载和多个预算输出另计。每次运行实际记录下载/解压/准备字节数和磁盘峰值。

真实 schema 预览来自：
https://datasets-server.huggingface.co/rows?dataset=HuggingFaceFW%2Ffineweb-edu&config=sample-10BT&split=train&offset=0&length=1

观察到 9,672,101 rows；首行 id 为 <urn:uuid:0d8a309d-25c5-405d-a08a-c11239f0d717>，dump=CC-MAIN-2013-20，token_count=845，正文标题为 “The Independent Jane”。实际字段有 text/id/dump/url/file_path/language/language_score/token_count/score/int_score。不可根据主数据卡强求 sample 中存在 date 字段。Viewer 是 live 预览；Local 必须在固定 Parquet 字节上再次确认，而不是把 live API 当不可变快照。

## 4. tokenizer、边界、切分与精确预算

只用固定 tokenizer，不加载 GPT-2 权重。取以下全部小文件：

| 文件 | bytes | Git blob SHA-1 |
|---|---:|---|
| config.json | 665 | 10c66461e4c109db5a2196bff4bb59be30396ed8 |
| merges.txt | 456318 | 226b0752cac7789c48f0cb3ec53eda48b7be36cc |
| tokenizer.json | 1355256 | 4b988bccc9dc5adacd403c00b4704976196548f8 |
| tokenizer_config.json | 26 | be4d21d94f3b4687e5a54d84bf6ab46ed0f8defd |
| vocab.json | 1042301 | 1f1d9aaca301414e7f6c9396df506798ff4eb9a6 |

词表 50,257；EOS/BOS sentinel 使用 GPT-2 的 50256。正式代码仍要 Local 检查实际 tokenizer 映射，而不是仅依赖本文常量。推荐直接读 tokenizer.json，关闭自动特殊 token 添加，不做 lowercasing 或文本截长。

拟冻结的数据规则如下，必须出现在实现/manifest 中：

1. 按源 shard 名称排序；每个 shard 按 Parquet 原始行序。独立文档就是单个 text 字段，绝不按段落/行误切文档。
2. split key 为 SHA-256(UTF-8(" ".join(NFC(text).split())))。这里只对去重键做 NFC 和空白合并；模型见到原始 text。空文档丢弃并计数。相同 key 只保留最早行，避免相同内容跨集合。
3. bucket = int(key 前 16 个 hex 字符, 16) mod 10000。0–49 为 validation，50–99 为 test，100–9999 为 train。该划分是**本项目派生预训练划分**，不是伪称 FineWeb 原生 validation/test。
4. 训练目标序列为 encode(text, add_special_tokens=False) + [50256]。本项目采用 FULL_MODEL_PROPOSAL.md 的内部 SEG 向量：forward_segment 的输出与同位置目标对应，不额外前置 50256，也不再次右移 labels。预算计目标序列中的实际、非 padding、参与交叉熵的 token；SEG 不计入预算。
5. B 精确取 100,000,000 或 1,000,000,000。100M 是 1B 同一确定性目标流的前缀。最后一篇可只消费剩余的目标前缀，显式记录 truncated_tail；不能超预算后四舍五入，也不能为了凑整虚构文档结束符。
6. validation/test 各固定前 1,000,000 目标 token；按同样边界记录。两个训练预算共享这两份派生留出集，不随模型/seed 改变。它们用于训练诊断/开发，不替代 bAbI/LAMBADA。
7. 文档开头有显式 reset mask；文档内 BPTT/chunk 边界只 detach，不 reset。下一篇必须 reset。当前模型把 semantic EOS 当作真正结束，因此 FineWeb 正文不能产生同值控制 token：在 tokenizers==0.20.3 中设置 Tokenizer.encode_special_tokens=True，再 encode(add_special_tokens=False)，将正文中的特殊-token 字面串按普通字符编码；断言正文 ids 中没有 50256，然后仅追加一个 semantic EOS。如果所用 tokenizer 后端不能提供相同普通文本编码，则明确排除此类训练文档并记录数量/身份，不静默重写内容。对原生 benchmark 不得丢行或改文本；保持官方编码，模型需要把输入中的字面 token 与人为结束/reset 控制区分，无法做到则资格验收失败。
8. 保留文档 id、source shard/row、内容 hash、split、token offset/length、是否尾部截断、预处理源码版本、tokenizer 文件身份和所有排除计数。batching 不能改变这些身份。
9. 该规则保证规范化完全重复文本不跨 split，**不保证近重复、同 URL 改版、同站点内容或 benchmark contamination 已清除**。Local 应冻结并记录近重复/污染审计；结果中保留未知范围。不能在看过测试结果后改过滤规则。
10. B 默认指预训练目标 token。bAbI 适配的输入曝光 token、答案监督 token、epochs 和更新次数须单列。若用户预算被解释为全部训练 token 上限，则先确定适配预算并从 B 扣除；不能偷偷在 B 之外训练后称总量为 B。

## 5. bAbI 原生合同

来源路径（均为上述固定 ParlAI commit）：
- [build.py](https://github.com/facebookresearch/ParlAI/blob/a29567f7ce76992fd1f03c51ba9e3b155a37ea51/parlai/tasks/babi/build.py)
- [agents.py](https://github.com/facebookresearch/ParlAI/blob/a29567f7ce76992fd1f03c51ba9e3b155a37ea51/parlai/tasks/babi/agents.py)
- [原生 test 样例](https://github.com/facebookresearch/ParlAI/blob/a29567f7ce76992fd1f03c51ba9e3b155a37ea51/parlai/tasks/babi/test/babi_all10k_test.yml)
- [原生 train 样例与计数](https://github.com/facebookresearch/ParlAI/blob/a29567f7ce76992fd1f03c51ba9e3b155a37ea51/parlai/tasks/babi/test/babi_all10k_train.yml)
- [原生 valid 样例与计数](https://github.com/facebookresearch/ParlAI/blob/a29567f7ce76992fd1f03c51ba9e3b155a37ea51/parlai/tasks/babi/test/babi_all10k_valid.yml)

作者 builder 下载 http://parl.ai/downloads/babi/babi.tar.gz，SHA-256 为 **f7f0bee187efca0d81c3daac1b162cda4eb7f9505dee5ad6846eabbed3dbf92e**。Local 可用同主机 HTTPS；必须通过相同内容 hash，不能“下载成功”就认定正确。当前 Web HEAD 未给出可用大小证据；建议下载上限 64 MiB、解压上限 512 MiB，超限暂停检查来源，不绕过校验。

loader 实际路径为：
assets/parlai/bAbI/tasks_1-20_v1-2/en-valid-10k-nosf/qa{task}_{train|valid|test}.txt。

这里 nosf 明确采用不提供 supporting facts 的输入。原始 archive 可能同时含其他目录，它们不属于本次选中输入。全部 20 task 的官方例数：

| split | 问题数（评分分母） | episodes |
|---|---:|---:|
| train | 179998 | 56396 |
| valid | 20002 | 6265 |
| test | 20000 | 6267 |

不能把 HF babi_qa 的“story rows”当作问题数：实际 live 预览 en-10k-qa1/test 为 200 个故事，每故事含多个问题。官方 ParlAI test 首个 episode 的第一个问题是 “Where is John?”，答案 hallway；之后相同 episode 的问题依赖先前事实。该真实例子与 [HF 少量行预览](https://datasets-server.huggingface.co/rows?dataset=facebook%2Fbabi_qa&config=en-10k-qa1&split=test&offset=0&length=1) 一致。HF 只用作 schema 旁证；正式获取用带作者 checksum 的 archive。

输入只包含事实文本与当前问题。native labels / eval_labels、supporting_ids、正确候选的注入、答案索引、reward 等不得进入模型。train 标签只进入已声明答案监督损失。teacher 的 label_candidates 可能把当前正确标签补进列表，**不得把每例原生候选列表当作无泄漏输入**；若需要受限词表，只能从训练集冻结公共答案词表并对所有方法相同。默认自由生成单一答案。

精确 teacher 解析规则：每行先 strip() 再把字面反斜杠+n 替换为换行；空行跳过。以第一个空格分离数字行号，再按 tab 分字段，每字段 strip。当前行号不大于上一行号时开始新 episode。累积 x 用单个换行连接本段事实和当前问题；非空第二字段标识带标签例子，而不是依靠问号字符猜测。labels 按竖线分割；第四字段是候选列表，第三字段按 reward 解析（本次必须用 nosf 文件，不能把原始 supporting IDs 当 reward）。每次 yield 问题后 x 清空，因此下一个 native_text **仅含新增事实与新问题，不重复先前问题，也不添加任何先前答案**。模型需要自行保持先前事实状态。为一次性上下文基线构造 full_context 时，累积先前事实而不加入 gold answers；保留 native_text 供逐字 parity。作者 parser 对 EOF/episode 边界的未配对事实会 yield labels=None；若 Local 实际遇到这种记录，应保留并检查 denominator/teacher 行为，不能自行静默丢掉。

样本 ID 固定为 (archive SHA, task, split, 零基原生问题序号)，episode ID 固定为 (archive SHA, task, split, 零基原生 episode 序号)，并保留该问题的 episode 内 turn 序号和原始物理行号。不同 task/split 的相同行号不是同一个统计单元。以上 tar member 名称来自已读 loader；Web 未获取或列出实际 tar，Local 必须验证成员与源码期望一致。

v0 适配器为每个问题构造包含全部先前事实和当前问题的完整 context，并从新状态重放这个 context；SFT 与评测使用完全相同的序列化。这样每个问题仍拥有该故事的全部历史事实，不输入先前 gold answers，也不在已包含历史的状态上再次追加完整历史。每个输入 token 在该次重放中消费一次，回答写入的工作分支在样本结束时丢弃。episode 身份仍保留，用于原生行对照和聚类统计。此选择的代价是重复重建前缀，不能宣称已经测量了跨多个问题增量维护状态的效率。未来若改为按 native_text 增量推进事实并只读回答，需要另行证明两条路径的分段/来源语义一致。

原生评分采用 ParlAI 的 TeacherMetrics.evaluate_response → ExactMatchMetric.compute：
- normalize_answer：lowercase，标点替换为空格，移除 a/an/the，合并空白。
- bAbI teacher 对 task 8、19 的标签执行 comma → space，**没有把列表任意排序**。保持此行为；不用自己写的 set match、substring、token F1 或 LLM judge 代替。
- 每个问题一条预测；非法/空字符串计错；缺失/重复/额外 ID 必须使整份结果的资格失败，不缩分母。
- primary：20 个任务各自 accuracy 与 native macro accuracy；同列报告 mean error=1−macro accuracy，以及 error>0.05 的 failed-task count。最后两项是原论文 summary，不能取代逐任务 native accuracy。
- 只按验证集选择 checkpoint/循环策略，不能挑测试上最好 seed。联合训练与逐任务训练分别命名；不拿作者逐任务 best-of-10 结果作为本项目联合训练单次结果的可直接公平对比。

原文及 EntNet 作者代码支持小型模型的有监督评测可行性，但本项目的现代 baseline、native scorer replay、完整样本覆盖和 RTX 2080 Ti 资源占用仍须实际验收。论文 95% 描述性阈值不是本项目所有 baseline 的任意强制准入阈值。

## 6. LAMBADA OpenAI English 原生合同

固定文件优先使用 data/lambada_test.jsonl：
- 1,819,752 bytes；
- SHA-256 **4aa8d02cd17c719165fc8a7887fddd641f43fcafa4b1c806ca8abc31fabdb226**；
- data/lambada_test_en.jsonl 的 hash 与大小完全相同；不需要下载两份。
- en/test/en.parquet 另有 1,157,764 bytes、SHA-256 99d8a9e54cda761c6340ddd4fa6feda7f846ffb0e716afa52968dea75495eea7，但选择 JSONL 即可，不混换转换版本。

来源：[文件 API](https://huggingface.co/api/datasets/EleutherAI/lambada_openai/tree/900124bf3b8235c6daf21033af9948b3f07346c4/data?expand=false)；
[真实 row 预览](https://datasets-server.huggingface.co/rows?dataset=EleutherAI%2Flambada_openai&config=en&split=test&offset=0&length=1)。
每行 schema 仅 text:string；5,153 passages。row 0 的最后一个词为 signs。原数据无稳定 UUID；使用固定文件 SHA-256 + 零基行号作为不可变样本身份。

[harness 原生 YAML](https://github.com/EleutherAI/lm-evaluation-harness/blob/d6de81643928d653435c431bae19945d41d32520/lm_eval/tasks/lambada/lambada_openai.yaml) 选择 dataset_name=default（英文），不是译文变体。原生 context 为 text.split(' ')[:-1] 再用空格 join；target 为单个前导空格加 text.split(' ')[-1]。不能改成随意 strip 后的最后 token，不能删目标标点或使用不一致 tokenizer。

还须忠实复现 [TemplateLM._encode_pair](https://github.com/EleutherAI/lm-evaluation-harness/blob/d6de81643928d653435c431bae19945d41d32520/lm_eval/api/model.py) 的 causal tokenizer 边界：先以 len(context)−len(context.rstrip()) 计末尾空白并移到 continuation 开头；编码 context+continuation 得 whole_enc，再独立编码 context 得 context_enc；continuation_enc=whole_enc[len(context_enc):]。不能把单独编码 target 的结果当作目标 suffix。原生 empty-context 分支由 loglikelihood 调用方使用 prefix_token_id 处理，_encode_pair 本身断言 context 非空。完整 LAMBADA adapter parity 要覆盖这些已读来源语义。

output_type=loglikelihood，num_fewshot=0，无 chat template，无外部工具/检索/模型评判，完整 5,153 样本一次。原生模型输出为 (ll, is_greedy)：
- ll 是整个目标末词的全部 tokenizer 子 token 条件 log probabilities 之和。
- is_greedy 要求每个目标子 token 都等于相应条件下的 argmax。
- ConfigurableTask.process_results 返回 perplexity=ll、acc=int(is_greedy)。
- metrics.mean 聚合 acc；metrics.perplexity 返回 exp(−mean(ll))。
- **字段名称是 perplexity，不是 word_perplexity**。后者在 harness 中属于 loglikelihood_rolling，不能替代本任务。也不能按子 token 数归一化末词 ll 再冒充 native perplexity。

每篇 reset 状态，完整输入上下文；不得与相邻篇共享记忆。优先保证完整上下文且不静默左截断；Local 记录最大 tokenizer 长度和模型可处理长度，任何截断须计数并先解决。未来推理 adapter 要与官方 HFLM 的 tokenizer boundary、target alignment、softmax 与 greedy 判定做真实原生样本 parity。源码阅读不能代替此项。

LAMBADA 没有本次选择的开发 split；不能在其测试集调参。预训练 FineWeb validation 用于 checkpoint 选择，预训练 checkpoint 在适配 bAbI 前单独保存并评估 LAMBADA。公布全部 checkpoint 测试曲线须标为开发性反复查看，不能再把同一测试结果叫前瞻独立确认。

## 7. Local 获取与原生准备命令（均未执行）

所有执行命令应由 Local 放进已有 run_harness.py 管理的 GPU 主机任务；下载/准备/scorer 用 0 GPU，模型推断另作 GPU 任务。本文件不给不存在的 SSH alias、Conda 路径或训练 entry point。以下 cwd 是 Local 实际交付 checkout；相对 paths 是拟冻结的项目缓存布局，不能把 Web scratch 路径当作 GPU 主机路径。先使用项目环境锁，不在本文件临时升级整套依赖。

### 7.1 tokenizer 与 FineWeb 文件

~~~bash
set -euo pipefail
mkdir -p assets/tokenizer/gpt2 assets/fineweb-edu/sample/10BT assets/provenance
for name in config.json merges.txt tokenizer.json tokenizer_config.json vocab.json; do
  curl --fail --location --retry 3 --max-time 300 --max-filesize 2000000 \
    "https://huggingface.co/openai-community/gpt2/resolve/607a30d783dfa663caf39e06633721c8d4cfcd7e/$name" \
    -o "assets/tokenizer/gpt2/$name"
done
git hash-object assets/tokenizer/gpt2/config.json assets/tokenizer/gpt2/merges.txt \
  assets/tokenizer/gpt2/tokenizer.json assets/tokenizer/gpt2/tokenizer_config.json \
  assets/tokenizer/gpt2/vocab.json
~~~

逐行必须等于第 4 节 Git blob ID，并把实际 SHA-256/字节数写入 input manifest。上述文件过滤不会下载任何 GPT-2 weights。

下面命令获取第一、二个 shard；如不足，按第 3 节表用同一 URL/bytes/hash 追加下一行。支持中断下载续传；每次消费前必须完整通过内容校验：

~~~bash
set -euo pipefail
while read -r name bytes digest; do
  curl --fail --location --retry 3 --max-time 7200 --continue-at - \
    --max-filesize "$bytes" \
    "https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu/resolve/87f09149ef4734204d70ed1d046ddc9ca3f2b8f9/sample/10BT/$name" \
    -o "assets/fineweb-edu/sample/10BT/$name"
  printf '%s  %s\n' "$digest" "assets/fineweb-edu/sample/10BT/$name" | sha256sum --check -
done <<'FINEWEB'
000_00000.parquet 2152819114 b1ba7b2ce4cb5ea6ef42dca40263eabb85f37700d01693a68e9b30a31d78e871
001_00000.parquet 2152222432 3fcf2dc69cd52503986276d3d2d26a8c356d0f2ea28a0de4fdbda8cf87755693
FINEWEB
~~~

所需 preprocessing 可直接用项目已锁定的 pyarrow.parquet.ParquetFile.iter_batches(columns=["id","text"]) 与 tokenizers.Tokenizer.from_file("assets/tokenizer/gpt2/tokenizer.json")；逐条执行第 4 节规则。当前已实际读到 src/lwm/data.py 的 CorpusWriter(directory, provenance).add(document_id, ids, loss_start=0, metadata=None)；准备器应把目标 token 文档流交给它，输出 tokens.bin（little-endian uint16）、index.jsonl，并最后发布 manifest.json。代码支持目标数和文件 hash；输出目录非空会拒绝，不能覆盖已有合格语料。

~~~python
from tokenizers import Tokenizer
from lwm.data import CorpusWriter

tokenizer = Tokenizer.from_file("assets/tokenizer/gpt2/tokenizer.json")
tokenizer.encode_special_tokens = True
body_ids = tokenizer.encode(raw_text, add_special_tokens=False).ids
if 50256 in body_ids:
    raise ValueError("Text-body EOS must not become a stream control event")
target_ids = body_ids + [50256]
# 对预算末篇先取 remaining_targets 前缀，并在 metadata 标记 truncated_tail。
writer.add(document_id, target_ids, loss_start=0, metadata=source_metadata)
~~~

特殊-token 行为的源码依据是 huggingface/tokenizers v0.20.3 的固定 commit b63262a481495453011bf7a3b27995d6611dfae7：[Python setter](https://github.com/huggingface/tokenizers/blob/b63262a481495453011bf7a3b27995d6611dfae7/bindings/python/src/tokenizer.rs) 和 [AddedVocabulary 的 matching 跳过规则](https://github.com/huggingface/tokenizers/blob/b63262a481495453011bf7a3b27995d6611dfae7/tokenizers/src/tokenizer/added_vocabulary.rs)。已读源码，没有运行验证。

若正式准备器改用 Hugging Face fast tokenizer，不能只设置 backend_tokenizer.encode_special_tokens。transformers==4.46.3（commit 052e652d6d53c2b26ffde87e039b723949a53493）的 [PreTrainedTokenizerFast._batch_encode_plus](https://github.com/huggingface/transformers/blob/052e652d6d53c2b26ffde87e039b723949a53493/src/transformers/tokenization_utils_fast.py) 每次都会用 split_special_tokens 参数改写 backend 该值。因此 FineWeb 普通文本调用应显式 tokenizer.encode(raw_text, add_special_tokens=False, split_special_tokens=True)。原生 benchmark 保持官方默认 split_special_tokens=False、add_prefix_space=False、无自动 BOS；不能因正文出现特殊-token 字面串改变原生内容或悄悄删行。两类调用的特殊 token 处理差异须写入 manifest。

**FineWeb 准备 CLI 仍待数据实现接入；这里不伪造已存在的 entry point。** 主实现交付时必须在 Local guide 填入真实 100M/1B 准备 argv；下列验收是硬要求：target 数等于预算，100M 前缀等同，reset/offset 一致、无跨 split 内容 hash、所有 shards 校验、来源字节总量未超 cap。CorpusCursor 默认 shuffle=True；若主协议冻结前述源顺序/前缀，运行必须显式 shuffle=False、repeat=False。若另选 deterministic document shuffle，应同时改变两预算的 source-order 约定并审查前缀关系，不能无记录启用默认 shuffle。只写本文件不能宣称完整代码交付。

### 7.2 pin 原生 scorer 源码与 bAbI archive

~~~bash
set -euo pipefail
git init external/ParlAI
git -C external/ParlAI remote add origin https://github.com/facebookresearch/ParlAI.git
git -C external/ParlAI fetch --depth 1 origin a29567f7ce76992fd1f03c51ba9e3b155a37ea51
git -C external/ParlAI checkout --detach FETCH_HEAD
git init external/lm-evaluation-harness
git -C external/lm-evaluation-harness remote add origin https://github.com/EleutherAI/lm-evaluation-harness.git
git -C external/lm-evaluation-harness fetch --depth 1 origin d6de81643928d653435c431bae19945d41d32520
git -C external/lm-evaluation-harness checkout --detach FETCH_HEAD
git -C external/ParlAI rev-parse HEAD
git -C external/lm-evaluation-harness rev-parse HEAD
mkdir -p assets/parlai/bAbI assets/babi/native
curl --fail --location --retry 3 --max-time 600 --max-filesize 67108864 \
  https://parl.ai/downloads/babi/babi.tar.gz -o assets/parlai/bAbI/babi.tar.gz
printf '%s  %s\n' \
  f7f0bee187efca0d81c3daac1b162cda4eb7f9505dee5ad6846eabbed3dbf92e \
  assets/parlai/bAbI/babi.tar.gz | sha256sum --check -
tar -tzf assets/parlai/bAbI/babi.tar.gz
tar -xzf assets/parlai/bAbI/babi.tar.gz -C assets/parlai/bAbI
test -d assets/parlai/bAbI/tasks_1-20_v1-2/en-valid-10k-nosf
~~~

已有相同 commit 的 checkout 则复用，不重复 git init/remote add。解压前检查所有成员没有绝对路径或父目录逃逸，并累加声明大小不超过 512 MiB。下载完整不等于 scorer 可用。采用 NATIVE_ENVIRONMENT.md 的独立环境卡并保留实际依赖解析/安装回执；ParlAI 与 harness 的完整依赖存在冲突，不能放进同一环境或用 --no-deps 跳过。以下裸 python 命令须放在已资格化的完整 ParlAI teacher 环境，完整调用前缀见该环境卡。

标记已按官方 hash 获取并解压，防止 builder 重新下载同一份：

~~~bash
python - <<'PY'
from parlai.core import build_data
build_data.mark_done("assets/parlai/bAbI", version_string="None")
PY
for task in $(seq 1 20); do
  for split in train valid test; do
    dtype="$split"
    if [ "$split" = train ]; then dtype='train:ordered'; fi
    python -m parlai.scripts.convert_data_to_parlai_format \
      --task "babi:Task10k:$task" --datatype "$dtype" \
      --datapath assets/parlai --num-examples -1 --ignore-fields '' \
      --outfile "assets/babi/native/task-$task-$split.txt"
  done
done
~~~

这是已读作者 entry point 的确切命令，导出全部原生题目；不是用 RepeatLabelAgent 的伪模型高分作 baseline。每题 ID 取 (archive SHA, task, split, 该 task/split 的零基原生题序号)，另存 episode/turn/native source-line。保留原文件与 dump 的 SHA-256；确认第 5 节总数。

### 7.3 LAMBADA 获取、数据定位与原生命令

~~~bash
set -euo pipefail
mkdir -p assets/lambada-openai
curl --fail --location --retry 3 --max-time 300 --max-filesize 1819752 \
  https://huggingface.co/datasets/EleutherAI/lambada_openai/resolve/900124bf3b8235c6daf21033af9948b3f07346c4/data/lambada_test.jsonl \
  -o assets/lambada-openai/lambada_test.jsonl
printf '%s  %s\n' \
  4aa8d02cd17c719165fc8a7887fddd641f43fcafa4b1c806ca8abc31fabdb226 \
  assets/lambada-openai/lambada_test.jsonl | sha256sum --check -
wc -l assets/lambada-openai/lambada_test.jsonl
~~~

期望 5153 行且每行仅需合法 text:string；任何空文本/额外字段都保留并审查，不悄悄删除。正式任务配置应复制固定原生 YAML，仅把 dataset_path 改为 json、dataset_name 设为 null，并把 dataset_kwargs.data_files.test 指向上述固定本地 JSONL；也可继续原生 HF 路径并在 dataset_kwargs 指定固定 revision。不得修改 doc_to_text、doc_to_target、output_type、metric_list 或样本行序。

当前交付使用已经实现的 `lwm.evaluate` 生成全部原生样本预测，再由 `lwm.scoring replay` 调用下面第 8 节的原生 scorer；确切调用见 LOCAL_AGENT_RUNBOOK。以下保留的是来源审查时读到的另一种原生 CLI 形状，并非当前交付命令：

~~~text
python -m lm_eval run --model MODEL_BACKEND --model_args CHECKPOINT_ARGS \
  --tasks PINNED_LOCAL_LAMBADA_TASK --include_path PINNED_TASK_DIRECTORY \
  --num_fewshot 0 --batch_size 1 --device cuda:0 \
  --seed 0,1234,1234,1234 --log_samples --output_path RUN_OUTPUT_DIRECTORY
~~~

若未来切换到该原生 CLI 路线，MODEL_BACKEND 必须是真正注册并验收的自有 recurrent LM adapter；不能填写不存在的注册名。当前薄 replay 路线不需要这个占位后端，也不宣称完成了该路线的 qualification。

完成全部 60 个原生导出后，使用 `lwm.native_parity` 对全部 220,000 问题逐行比较；完整环境、命令、字段/分母与失败记录规则见 [NATIVE_ENVIRONMENT.md](NATIVE_ENVIRONMENT.md#compare-all-60-author-exports-with-prepared-records)。该程序使用固定作者的 `str_to_msg`，不靠自制解析或几条样例宣称原生一致。实际执行和 teacher 环境资格仍待 Local。

## 8. scorer replay 的可实现调用合同

主交付应提供薄 replay adapter，而不是重写评分公式。以下是源代码已确认的原生函数调用，可作为代码作者的精确接口；**它们没有在 Web 运行**。

bAbI 的已导出原生行使用 parlai.utils.misc.str_to_msg 解码，不能简单按空格或制表符猜分隔规则。每个 task 独立建立 TeacherMetrics；逐题先检查预测 ID/输入 hash/无重复，再调用：

~~~python
from parlai.core.message import Message
from parlai.core.metrics import TeacherMetrics, aggregate_named_reports

metric = TeacherMetrics(metrics_list="accuracy")
metric.evaluate_response(Message({"text": prediction_text}), native_labels)
task_report = metric.report()
# 对完整 20 个 task 的 task_report：
report = aggregate_named_reports(reports_by_task, micro_average=False)
~~~

prediction_text 必须始终是字符串，空/非法答案转换为空字符串并计错，不能传 None 让指标跳过。输出 native report 中 accuracy 与 exs；全部 20 tasks 和全分母必须存在。原论文 failed-task count 只是从这 20 个已确认 native accuracy 得出的 summary。切勿通过 homemade 正误函数替代原生调用。Local 的 live replay 要保留 scorer commit、实际 argv/cwd、预测/原生 labels bytes、stdout/stderr、原生 report 和实际运行时间。

LAMBADA 用同一固定本地 JSONL 构造原生 ConfigurableTask；薄 adapter 只包装自有模型提供的 ll/is_greedy：

~~~python
from lm_eval.api.task import ConfigurableTask

task = ConfigurableTask(config=pinned_lambada_config)
native_per_example = task.process_results(
    native_document, [(float(log_likelihood), bool(is_greedy))]
)
aggregators = task.aggregation()
# 取这两个已注册的原生 aggregation，覆盖完整 5153 条：
accuracy = aggregators["acc"](all_native_acc_values)
perplexity = aggregators["perplexity"](all_native_ll_values)
~~~

实际 adapter 应严格验证输入 is_greedy 本来就是 bool、ll 是有限数，不能把字符串 "false" 或 NaN 强制转换成合格值。记录每题 context/target 与其 tokenizer ID、各目标 token logprob、argmax ID、ll/is_greedy 及完整 sample_id。这样 Local 可检验累加与 native HFLM parity，避免漂亮 aggregate 掩盖 target 对齐错误。无限/溢出 perplexity 原样保留为错误/非有限，不截断成可比较的漂亮数字。

仅重新聚合缓存 ll 不能证明模型 forward、state reset 或 target alignment 正确；必须先在真实原生数据上验收推断 adapter。没有这些回执时，不标记 faithful_harness verified。

## 9. Local 冻结前待办与限制

- 选择的所有数据/代码 bytes 完整获取、hash 通过；预处理 entry point、scorer replay CLI 与实际环境锁完成并读回。
- 原生 bAbI all20 全分母、episode 边界、task8/19 标签处理、标签隔离和候选泄漏检查；不可造几个例子充作 native qualification。
- LAMBADA 5153 全覆盖、末词多子 token、context/target 对齐与每篇 reset；同一真实输入对官方 scorer/adapter replay 的零容差 parity。
- FineWeb 文档语义、100M/1B 精确 token 计数、状态跨 chunk 延续/跨文档清空、同预算所有 arms 同文档流、split 交集与近重复/污染审计。
- 预训练与 bAbI 适配预算分开报告；所有 baseline/control 有公平训练机会和同原生输入。EntNet 或其他重叠功能的强基线不能只用历史论文数字冒充本地合格比较。
- RTX 2080 Ti 上实测单作业峰值显存、tokens/s、每任务推断/scoring 时间、内存/磁盘；没有实测前不给 1B 在一个窗口完成的保证。将所有方法/seed/控制/适配的累计 GPU 小时计入预算。
- 原生样本/推断/错误/重试/选择日志保留；通过实现检查 ≠ 科学有效；主方案的 G01、方法选择、统计精度和 prospective confirmation 仍独立存在。
- bAbI 多问题共享故事，统计重采样至少按 episode 聚类，不能把所有问题假设为独立；所有 task 同时作声称还需处理多重比较。LAMBADA 每篇为配对单位。这里不伪造已验证置信区间。
- 文本保留和得分只支持任务内能力，不证明可辨识的概率后验、外部世界动力学、意识或通用理解。

## 10. 已调查但不选入本轮的来源

LongMemEval 保持 SOURCE_AUDIT.md 的“候选、未冻结”状态：作者 scorer 用模型评判，多会话长历史与本轮从头训练小模型的可学能力/费用不匹配；本轮不以字符串 EM 偷换其 native judge。

CLUTRR 检查了 facebookresearch/clutrr@d045fae289d3746503677ceed7631c999202501e 和作者 koustuvsinha/clutrr-baselines@303ed9a48f82a59b4eb34ac5bd5866f0d82c5552。HF CLUTRR/v1@a8158d1fac10864c3424d53662fe63bf7d82dd87 的实际 live test row id=a44d478f-c68e-4557-8750-1b2f6f17d705，query=(Jason,Lewis)，target_text=grandson，证明看过真实 schema。**但该 pinned builder 的外部 CSV URL 仍指向第三方 kliang5/CLUTRR_huggingface_dataset/main**，仅 pin HF builder 不 pin 数据；作者 baseline 还动态形成类别映射，且 batch 均值聚合须检查分母。这些阻碍未关闭，不把它列入选中比较，不用新生成的 CLUTRR 数据填补。本轮两个原生 benchmark 已由 bAbI + LAMBADA 满足，CLUTRR 留待未来明确需要的扩展。
