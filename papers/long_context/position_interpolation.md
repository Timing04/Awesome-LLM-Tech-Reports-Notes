---
title: Extending Context Window via Position Interpolation
type: method_paper
category: long_context
status: ai_draft
source_status: verified
release_date: 2023-06-27
topics:
  - rope_scaling
  - long_context
  - interpolation
source:
  kind: arxiv
  ref: "2306.15595"
  official: ""
---

# Position Interpolation

## 3-Minute Summary

- Position Interpolation（PI）提出通过缩放位置索引，把长序列位置映射回训练分布内，从而扩展 RoPE 模型的可用上下文。
- 它解决的问题是：RoPE 模型在超出训练长度时相位外推失真。
- PI 的意义在于改动小、兼容已有 RoPE 模型，常用于长上下文扩展微调。

## Problem Definition

- 输入:
  - 原始位置索引 `pos` 与目标长度 `L_target`。
- 输出:
  - 插值后位置索引 `pos'`，用于 RoPE 计算。
- 目标:
  - 让超长推理时的位置分布更接近训练分布，减少性能崩塌。

## Method

- 核心做法:
  - 对位置进行线性插值缩放，再喂给 RoPE。

```text
pos' = pos * (L_train / L_target)
```

- 当 `L_target > L_train` 时，插值把高位置压缩到可学习区域。

### 结构图（重绘）

```mermaid
flowchart LR
    A["Original Position pos"] --> B["Interpolation Scaling"]
    B --> C["Scaled Position pos'"]
    C --> D["RoPE(q,k,pos')"]
    D --> E["Attention"]
```

## Why It Works

- RoPE 的角频率对位置值敏感，直接外推会带来相位失配。
- PI 通过位置压缩减少这种失配，提升超长长度稳定性。

## Experiments

- 论文展示了对 LLaMA 等 RoPE 模型的上下文扩展效果。
- 关键趋势:
  - 在较少额外训练成本下，PI 可显著提高长上下文任务表现。

## Implementation Notes

- 常见做法:
  - PI + 少量长上下文 continued training / finetune。
- 风险:
  - 压缩过强时，短距离分辨率可能受损。
  - 不同任务对长度缩放超参敏感。

## Relationship to LLM Practice

- PI 是 RoPE 长度扩展的经典基础方法。
- 后续 YaRN、NTK-aware scaling 等通常可视为 PI 思路的进一步优化。

## Limitations

- PI 不能替代系统层优化（KV cache、attention kernel、并行通信）。
- 极端长上下文下仍需额外训练与评估保障。

## Cross-References

- 相关模型报告:
  - [Llama 3](../../models/llama/llama3.md)
  - [Qwen2.5](../../models/qwen/qwen2_5.md)
- 相关论文:
  - [RoFormer](../architecture/roformer.md)
  - [ALiBi](alibi.md)
  - [Ring Attention](ring_attention.md)
- 相关专题:
  - [Long Context](../../topics/long_context.md)

## References

- Primary source:
  - [Extending Context Window of Large Language Models via Positional Interpolation (arXiv:2306.15595)](https://arxiv.org/abs/2306.15595)
- Follow-up work:
  - [YaRN](https://arxiv.org/abs/2309.00071)

## Review Checklist

- [x] 方法定义已核查
- [x] 关键公式没有抄错
- [x] 实验结论没有被过度解释
- [x] 已说明与主流 LLM 实践的关系
