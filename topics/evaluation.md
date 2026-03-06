---
title: Evaluation and Benchmark Reading
type: topic_overview
status: ai_draft
topics:
  - evaluation
  - benchmark
---

# Evaluation and Benchmark Reading

## Scope

这个专题关注如何读懂模型报告里的 benchmark：不仅看分数，还看任务构成、污染风险、可比性和统计稳定性。

## Key Questions

- benchmark 分数为什么经常不能直接横比。
- 通用 benchmark 与真实任务表现的关系是什么。
- 应该如何读懂报告里的“胜负结论”。

## Evaluation Lens

| 维度 | 要问的问题 |
|---|---|
| Task Fit | 评测任务是否真的对应你的业务任务 |
| Data Leakage | 训练数据是否可能污染 benchmark |
| Protocol | 评测协议是否统一（shot 数、解码、工具） |
| Cost | 为了这个分数付出了多少 token/时间/推理成本 |
| Robustness | 换 prompt 或换子集后结果是否稳定 |

## Score != Capability

```text
Observed Score = Model Capability + Prompting Gain + Evaluation Bias
```

- 同一模型在不同 prompt 模板下可能差距很大。
- judge-model 评测会引入额外模型偏差。
- 工具增强（tool-augmented）场景下，评测的是“系统”而非纯模型。

## Canonical References

- MMLU
- GPQA
- MT-Bench
- SWE-bench

## In-Repo Reading Order

1. [Llama 3](../models/llama/llama3.md)
2. [Qwen2](../models/qwen/qwen2.md)
3. [DeepSeek-V3](../models/deepseek/deepseek_v3.md)
4. [Post-training](post_training.md)

## Benchmark Reading Checklist

- 明确是否 closed-book、是否允许外部工具。
- 检查是否多次采样（`pass@k`）而非单次采样（`pass@1`）。
- 关注方差、置信区间或复现实验，而非只看单点最优。
- 对“全面领先”结论先找失败类目和边界条件。
