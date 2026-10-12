# Delta CPU 验证阶段

已按用户2026-10-12授权切换到 rsi-simple0.3.0-simple.9。原后台暂停已被本次
“开始验证所有实验”的指令取代；保留同一任务和同一GitHub main，旧研究历史不删除。

首轮实际执行了65项不同的数值检查，另有1项来源完整性校验。R01–R20每条最新修复线
至少有一项代表性检查；另外覆盖了部分历史候选/控制，以及率失真、查询缓存和写前取证。
共15次成功数值命令和1次已修复的语法失败，runner累计命令wall time约9.62秒。
构造输入、检查项、种子与命令不是新方法数量，也不是独立语言模型实验数量。

## 已经获得的证据

- 完整state/updater反馈Jacobian与有限差分一致；冻结后续gate可能改变决策符号。
- 独立rollout、线性系统求解、优化器、有限域枚举及积分参考复现了声明条件下的公式。
- 两步例子中即时保护输出位移为0，后续位移平方为0.053388；局部保护不自动延伸到未来。
- 一个旧SPD存在性“iff”缺少零因子identity例外。修正的是假设范围，不是推翻整个方法。
- 独立审查推动了真实零分支、四个实际决策臂、系数与能量单位、线程和内存报告的修复。

最新不同检查ID在测试的有限案例中均通过。原始输出、具体误差和反例见
[RESULTS_SUMMARY.json](RESULTS_SUMMARY.json)，独立审查见
[INDEPENDENT_NUMERICAL_REVIEW.md](review/INDEPENDENT_NUMERICAL_REVIEW.md)。
进程峰值RSS最高约82.1MiB；资源记录是Linux child rusage，包含其声明的范围。
BLAS/OpenMP与HiGHS线程设置是请求，实际线程数未直接测量。256MiB限制针对data
allocation，不是硬RSS上限；共享宿主8GiB上限也不是本项目独占内存。

## 尚未完成的实验

完整范围见[coverage_inventory.json](coverage_inventory.json)与
[COVERAGE_REVIEW.md](review/COVERAGE_REVIEW.md)。70份来源已逐项映射，不能把
每条修复有代表性检查解释为每个定理分支都已覆盖。后续优先补旧控制/STEP2检查，
FP32与病态条件，以及包含构造/维护开销的同成本比较。

公开原生任务效果、SFT遗忘、部署中更新器学习效率和原13arms×2seeds模型矩阵仍待执行。
100M/1B是每次模型训练的target-token预算，不是参数量；全矩阵预训练合计2.6B/26B
targets，另有26M适应targets每tier。当前宿主没有PyTorch和已资格化的数据/模型，
也没有取得另一个GPU主机的运行接口。小矩阵结果不能填入这些任务的结果表。

## 接续执行

读取[CPU_CHECKPOINT.json](checkpoints/CPU_CHECKPOINT.json)和POLICY_TRANSITION.json，
恢复归档后先运行现有runner的status/inbox/health；已有尝试、源digest、deadline和用量
均须保留。不要重复init、重跑已完成种子或恢复旧20→15准入要求。

在恢复后的根目录，可以用已钉住的vendor入口读取状态：

```bash
python vendor/rsi-simple-0.3.0-simple.9/scripts/simple_runner.py --root . status
python vendor/rsi-simple-0.3.0-simple.9/scripts/simple_runner.py --root . inbox
```

新的诊断必须经同一runner提交，绑定真实代码、source_manifest和具体plan hashes；
小批次执行、读原始结果、修复具体问题、再决定下一项。持续报告实际异常，保留失败，
不安装收费服务或用定时触发冒充连续运行。整个验证目标仍开放。
