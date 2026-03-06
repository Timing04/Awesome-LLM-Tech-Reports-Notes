---
title: Mixture of Experts
type: topic_overview
status: ai_draft
topics:
  - moe
  - architecture
---

# Mixture of Experts

## Scope

这个专题关注 LLM 中的 MoE 路线：路由、激活专家数、训练稳定性、推理效率与规模化收益。

## Key Questions

- 为什么需要 MoE，而不是继续堆稠密参数。
- 路由机制如何影响训练稳定性和吞吐。
- MoE 在训练成本与推理成本之间如何取舍。

## Core Idea

```text
h_out = sum_{i in TopK(h)} p_i(h) * Expert_i(h)
```

- 总参数可以很大，但每个 token 只激活少数专家（常见 `K=1` 或 `K=2`）。
- 目标是提高模型容量，同时控制每 token 的实际计算量。

## Typical Architectures

| 路线 | 特征 | 优点 | 风险 |
|---|---|---|---|
| Top-1 Router (Switch) | 每 token 激活 1 个专家 | 吞吐好、实现简单 | 容易专家负载不均 |
| Top-2 Router (Mixtral) | 每 token 激活 2 个专家 | 表达力更强、更稳 | 通信和融合开销更高 |
| Shared + Routed Experts | 部分参数共享 | 泛化更稳 | 设计复杂、调参成本高 |

## System View

```mermaid
flowchart LR
    A["Token States"] --> B["Router"]
    B --> C["Expert Parallel Compute"]
    C --> D["All-to-All Communication"]
    D --> E["Merge + Residual"]
```

- MoE 效率瓶颈经常从 `FLOPs` 转移到 `通信`。
- 实际吞吐取决于专家并行策略、网络拓扑和负载均衡质量。

## Canonical References

- Switch Transformer
- Mixtral 8x7B
- DeepSeek-V2 / V3

## In-Repo Reading Order

1. [Mixtral 8x7B](../models/mistral/mixtral_8x7b.md)
2. [DeepSeek-V3](../models/deepseek/deepseek_v3.md)
3. [FlashAttention](../papers/architecture/flashattention.md)
4. [Long Context](long_context.md)

## Practical Checklist

- 训练时监控专家负载熵与 token 分配均衡性。
- 推理时监控 all-to-all 延迟，而不只看理论 FLOPs。
- 评测要拆分“单位成本性能”和“绝对性能”。

## Common Pitfalls

- 把 MoE 理解成“免费性能提升”。
- 忽略路由不稳定导致的训练退化。
- 忽略部署侧网络瓶颈，导致纸面优势无法落地。
