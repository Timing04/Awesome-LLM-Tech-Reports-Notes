---
title: MiniCPM-V 2.6
type: model_report
family: modelbest
status: ai_draft
source_status: to_verify
release_date: 2024-00-00
model_scope: compact multimodal model
params: to_verify
topics:
  - multimodal
  - on_device
  - efficiency
source:
  kind: technical_report
  ref: ""
  official: ""
---

# MiniCPM-V 2.6

## TL;DR

- MiniCPM-V 2.6 代表“轻量多模态 + 高部署效率”路线，强调边缘侧可用性。
- 对学习者的价值是理解“多模态能力与模型体量”的折中设计。

## Problem Setting

- 目标:
  - 在更小模型体量下实现可用的视觉理解与对话能力。
- 典型场景:
  - 端侧应用、低成本多模态助手、轻量文档理解。

## Architecture (Learning View)

```mermaid
flowchart LR
    A["Image"] --> B["Vision Encoder"]
    B --> C["Lightweight Connector"]
    C --> D["Compact LLM"]
    D --> E["Answer / Reasoning"]
```

## What to Learn

- 小模型多模态的关键在于数据与训练策略，而不是盲目堆参数。
- 评估时要同时看:
  - 质量（任务准确率）
  - 成本（延迟、显存、吞吐）

## Cross-References

- [Qwen2.5-VL](../qwen/qwen2_5_vl.md)
- [Qwen2-Audio](../qwen/qwen2_audio.md)
- [Multimodal LLM](../../topics/multimodal.md)

## References

- Official materials / report: to verify

## Review Checklist

- [ ] 关键事实已核查
- [x] 术语和缩写已统一
- [x] 横向对比没有偷换结论
- [ ] 已补齐主要链接
