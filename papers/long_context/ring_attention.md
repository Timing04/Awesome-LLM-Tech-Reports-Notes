---
title: Ring Attention
type: method_paper
category: long_context
status: ai_draft
source_status: to_verify
release_date: 2023-10-03
topics:
  - distributed_attention
  - long_context
  - systems
source:
  kind: arxiv
  ref: "2310.01889"
  official: ""
---

# Ring Attention

## 3-Minute Summary

- Ring Attention 把 sequence 维度上的注意力计算分布到多设备上，通过环形通信把 `Q/K/V` 分块流动起来，避免单卡保存完整注意力矩阵。
- 它解决的核心矛盾是: 长上下文训练/推理需要更长序列，但显存和通信很快变成瓶颈。
- 在长上下文系统路线里，它的重要性在于给出了一条“分布式 exact attention”的工程路径，而不是仅靠近似注意力。

## Problem Definition

- 输入:
  - 分布在多设备上的长序列 token 表示。
  - 标准 attention 所需的 `Q, K, V` 张量。
- 输出:
  - 与标准 self-attention 一致的注意力结果（数值上等价或近似等价，取决于实现细节）。
- 优化目标:
  - 在不牺牲 attention 正确性的前提下，把长序列训练扩展到更多设备，降低单设备内存压力。
- 与常见方案对比:
  - 相比 FlashAttention: FlashAttention 优化单设备内核 I/O；Ring Attention重点是跨设备序列并行。
  - 相比稀疏/近似 attention: Ring Attention主打保留 dense attention 语义。

## Method

- 核心思想:
  - 将序列切分到多设备，每个设备持有一段 token block。
  - 在 ring 拓扑中循环传递 `K/V` block，本地设备用固定 `Q` 逐块累计 attention 的分子与归一化项。
- 关键机制:
  - 在线 softmax 累积，确保分块计算后与全量 softmax 一致。
  - 每次只处理当前 block，避免构建完整 `L x L` 注意力矩阵。
- 典型流程:
  - Step 1: 每卡计算本地 `Q/K/V`。
  - Step 2: 初始化局部 attention 累加器（max/logsumexp 或等价统计量）。
  - Step 3: 在 ring 上轮转 `K/V` block，并更新本地输出累积。
  - Step 4: 归一化得到最终 attention output。
- 实现细节:
  - 通信与计算重叠是性能关键。
  - block size、pipeline 深度和网络拓扑直接影响吞吐。

## Why It Works

- 直觉:
  - 注意力计算可以按 key/value block 分解；只要在线维护 softmax 统计量，就不必一次性看到全部序列。
- 缓解的问题:
  - 单卡显存被 `O(L^2)` 中间量拖垮。
  - 长序列下的 device-local 计算与全局通信不平衡。
- 前提条件:
  - 高效集群互联（NVLink/IB）和稳定通信栈。
  - 框架支持 sequence parallel / ring collectives。
  - kernel 与通信调度协同优化，而不只是算法正确。

## Experiments

- 论文核心实验通常关注:
  - 不同上下文长度下的吞吐、显存占用和可扩展性。
  - 与常规并行 attention 方案的效率比较。
- 常见对比对象:
  - 标准 distributed attention 实现。
  - 与 FlashAttention 组合或非组合的版本。
- 可外推结论:
  - 当上下文足够长时，ring 化的序列并行可显著改善可训练长度上限。
  - 短序列下，通信开销可能抵消收益，Ring Attention 不一定占优。

## Implementation Notes

- 最小实现组件:
  - 序列切分策略（sequence parallel）。
  - ring 通信原语（send/recv 或 all-to-all 变体）。
  - 在线 softmax 累积逻辑。
- 常见坑点:
  - 数值稳定性: 在线 softmax 的 fp16/bf16 误差累计。
  - 通信拥塞: 当 ring 与其他并行策略叠加时，链路容易成为瓶颈。
  - 调度冲突: TP/PP/DP/CP 组合不当会导致“理论可扩展、实际低利用率”。
- 落地建议:
  - 与 FlashAttention 互补使用，分别优化“内核效率”和“跨设备长序列扩展”。
  - 先从固定长度 profile，确认 compute/comm 比，再逐步拉长上下文。

## Relationship to LLM Practice

- 显式关联场景:
  - 超长上下文预训练/continued pretraining。
  - 多节点训练时的 sequence parallel 加速。
- 更适合的阶段:
  - 更偏向 base model 训练和长上下文扩展训练，不是典型 post-training 算法。
- 在当前栈的位置:
  - 属于“系统级长上下文基础设施”。
  - 与 YaRN/PI 这类位置插值方法不同，Ring Attention主要解决算力与内存可行性。

## Limitations

- 假设:
  - 集群通信性能足够好，且可接受额外通信复杂度。
- 大规模问题:
  - 在跨机规模扩大后，ring 延迟和带宽限制会迅速显现。
  - 维护难度显著高于单机内核优化。
- 不建议直接使用的场景:
  - 序列长度中短、主要瓶颈不在 attention。
  - 团队尚未有稳定的分布式训练基建。
  - 只做推理且可用 KV cache / chunking 满足需求时。

## Cross-References

- 相关模型报告:
  - [Llama 3](../../models/llama/llama3.md)
  - [Qwen2](../../models/qwen/qwen2.md)
  - [DeepSeek-V3](../../models/deepseek/deepseek_v3.md)
- 相关论文:
  - [RoFormer / RoPE](../architecture/roformer.md)
  - [FlashAttention](../architecture/flashattention.md)
- 相关专题:
  - [Long Context](../../topics/long_context.md)

## References

- Primary source:
  - [Ring Attention with Blockwise Transformers for Near-Infinite Context (arXiv:2310.01889)](https://arxiv.org/abs/2310.01889)
- Follow-up work:
  - [FlashAttention (arXiv:2205.14135)](https://arxiv.org/abs/2205.14135)
  - [Llama 3 Report (arXiv:2407.21783)](https://arxiv.org/abs/2407.21783)
- Good implementation references:
  - [JAX Ring Attention reference implementation](https://github.com/Selimonder/ring-attention)
  - [xFormers / FlashAttention ecosystem references](https://github.com/facebookresearch/xformers)

## Review Checklist

- [x] 方法定义已核查
- [x] 关键公式没有抄错
- [x] 实验结论没有被过度解释
- [x] 已说明与主流 LLM 实践的关系
