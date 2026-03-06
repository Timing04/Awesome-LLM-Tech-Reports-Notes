---
title: ChatGLM3
type: model_report
family: chatglm
status: ai_draft
source_status: to_verify
release_date: 2023-00-00
model_scope: bilingual chat + tool-use model
params: 6B (main open variant)
topics:
  - chinese_llm
  - tool_use
  - instruction_following
source:
  kind: technical_report
  ref: ""
  official: ""
---

# ChatGLM3

## TL;DR

- ChatGLM3 是中文开源助手模型中的高频基线，主打中英双语、工具调用和实用对话能力。
- 对学习者价值在于：它代表了“中等参数规模 + 强工程可用性”的路线。

## Problem Setting

- 目标:
  - 在较低部署成本下提供稳定对话与工具能力。
- 典型场景:
  - 企业私有化中文助手、知识库问答、轻量 agent 原型。

## Architecture and Training (High-level)

- 延续 GLM/ChatGLM 系列主干并做对话与工具能力强化。
- 重点在后训练:
  - instruction data
  - tool-use alignment
  - 安全行为控制

## Tool-use Perspective

```mermaid
flowchart LR
    A["User Query"] --> B["Planner / Prompting"]
    B --> C["ChatGLM3"]
    C --> D["Tool Call or Direct Answer"]
    D --> E["Final Response"]
```

## Evaluation Lens

- 中文复杂指令遵循。
- 工具调用成功率和错误恢复能力。
- 多轮对话一致性与幻觉率。

## What Learners Should Focus On

- 中英双语数据配比对行为差异的影响。
- tool-use 不是“会调用 API”而是“知道何时调用”。

## Cross-References

- [GLM-4](../zhipu/glm4.md)
- [Qwen2](../qwen/qwen2.md)
- [Post-training](../../topics/post_training.md)

## References

- Official materials / report: to verify

## Review Checklist

- [ ] 关键事实已核查
- [x] 术语和缩写已统一
- [x] 横向对比没有偷换结论
- [ ] 已补齐主要链接
