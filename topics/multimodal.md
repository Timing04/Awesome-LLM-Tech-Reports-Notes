---
title: Multimodal LLM
type: topic_overview
status: ai_draft
topics:
  - multimodal
  - architecture
---

# Multimodal LLM

## Scope

这个专题关注视觉、音频与文本统一建模，重点看模态接入方式、训练阶段和评测设计。

## Key Questions

- 多模态模型通常如何接入视觉/音频信息。
- 模态对齐和 instruction tuning 如何协同。
- 多模态评测如何避免只看“表面分数”。

## Architecture Patterns

| 路线 | 典型做法 | 优点 | 风险 |
|---|---|---|---|
| Projector-based | Vision encoder + LLM + projector | 成本低、可复用强 LLM | 模态深融合能力有限 |
| Adapter-based | 在 LLM 中插入跨模态适配层 | 参数效率高 | 训练与部署复杂度上升 |
| End-to-End | 统一 backbone 联合训练 | 上限高 | 数据和算力需求极高 |

## Training Stages

```mermaid
flowchart LR
    A["Modality Encoder Pretraining"] --> B["Cross-modal Alignment"]
    B --> C["Instruction Tuning"]
    C --> D["Safety and Policy Tuning"]
```

- 阶段切分很重要:
  - 先解决“看得懂/听得懂”，再解决“会回答”。
- instruction tuning 若过强，可能损伤细粒度感知能力。

## Evaluation Lens

- 任务要拆开评估:
  - 感知（OCR/ASR/grounding）
  - 推理（跨模态推断）
  - 交互（多轮工具与对话）
- 多模态 benchmark 分数很依赖数据分布和提示词，必须看失败样例。

## Canonical References

- LLaVA
- Qwen2.5-VL
- Qwen2-Audio

## In-Repo Reading Order

1. [Qwen2.5](../models/qwen/qwen2_5.md)
2. [Llama 3](../models/llama/llama3.md)
3. [Post-training](post_training.md)
4. [Evaluation](evaluation.md)

## Common Pitfalls

- 把多模态问题简化成“加图像输入就行”。
- 只看开放问答分数，忽略 grounding 错误和安全问题。
- 忽略模态数据标注噪声和版权/合规风险。
