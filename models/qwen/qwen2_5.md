---
title: Qwen2.5 Technical Report
type: model_report
family: qwen
status: ai_draft
source_status: to_verify
release_date: 2024-09-19
model_scope: base + instruct
params: 0.5B-72B
topics:
  - instruction_following
  - coding
  - long_context
source:
  kind: technical_report
  ref: "TBD"
  official: ""
---

# Qwen2.5 Technical Report

## 3-Minute Summary

- Qwen2.5 的核心目标不是单点“刷榜”，而是把开源模型线从 Qwen2 推进到一个更均衡的版本: 更强指令遵循、更稳代码能力、更可用长上下文。
- 相比 Qwen2，这一代的价值在于“全栈配方升级”：数据、训练、后训练和模型产品线同时演进，而不是只改某个结构模块。
- 最值得学习的三点:
  - 如何在同一模型家族里维护多尺寸、同风格的能力分布。
  - 如何把长上下文与代码/数学能力作为主线能力而不是边缘特性。
  - 如何用一致的 post-training 流程提升可用性而不严重牺牲基础能力。

## Source Facts

- 原始材料类型:
  - technical report + official blog/model card（需在人工校对时逐条核验）。
- 发布时间:
  - 当前记录为 `2024-09-19`（待与官方原文发布时间再次核对）。
- 模型范围:
  - 覆盖 base 与 instruct，多尺寸参数段（`0.5B-72B`）。
- 已公开且可确认的方向性信息:
  - 系列化开源策略（多尺寸模型、统一产品线）。
  - 对 instruction following、coding、long-context 能力的重点强化。
- 未完整公开或需谨慎读取的部分:
  - 全量数据源细节与精确混合配比。
  - 全部训练超参与计算预算明细。
  - 某些能力提升背后的单因素贡献拆分。

## Problem Setting

- 目标任务:
  - 通用对话、代码生成、推理问答、长文档处理等高频 LLM 工作负载。
- 目标场景:
  - 开源社区模型二次开发、企业内私有部署、研究复现与评估。
- 相比 Qwen2 的重点提升:
  - 更稳定的多任务泛化。
  - 更高可用性的对齐表现（回答结构、遵循指令、输出一致性）。
  - 更强调长上下文与代码场景的综合可用性。

## Architecture

- 整体架构:
  - 仍基于 decoder-only Transformer 路线，延续家族内架构连续性。
- 关键模块:
  - 重点不在“颠覆式新结构”，而在已有结构的工程优化与训练配方升级。
- 关于 MoE/GQA/MLA/MTP/多模态:
  - 在当前条目中不对未核实细节做确定性断言，避免把二手信息写成结论。
  - 建议在人工校对时逐项补充“官方明确披露 vs 推断”标记。
- 核心设计动机:
  - 保持架构连续性，减少迁移成本，把创新预算更多投入到数据与后训练效果。

## Data and Pre-training

- 数据来源与规模:
  - 从公开信息看，Qwen2.5 延续了大规模多域数据训练，并强化代码、数学、指令相关数据比重。
- 数据清洗和配比:
  - 可确认存在质量过滤和多域配比优化，但精确配比通常未完整公开。
- tokenizer / vocabulary:
  - 延续 Qwen 家族 tokenizer 生态，具体词表和兼容策略需按官方文档逐项核查。
- 训练阶段:
  - 可按“base pretraining -> instruction/post-training -> 能力专项强化”理解。
- 关键 recipe 选择:
  - 不是单次训练后直接发布，而是通过多阶段训练把任务能力分布做均衡。

## Post-training and Alignment

- SFT:
  - 使用高质量 instruction 数据做能力与风格对齐，确保“可回答 + 可读 + 可执行”。
- Preference optimization / RL:
  - 公开资料通常强调偏好优化对输出质量的提升，但具体算法组合和超参需继续核验。
- Tool use / reasoning / instruction following:
  - 这一代明显强化了“可执行性”场景，尤其是 coding 与复杂指令遵循。
- 安全/对齐:
  - 与主流开源模型一致，采用多层安全与拒答策略；具体规则与覆盖范围仍需按官方说明核实。

## Evaluation

- 常见评测维度:
  - 通用知识、代码、数学、长上下文、指令遵循与对话体验。
- 常见对比基线:
  - 家族前代（Qwen2）与同期开源模型（Llama、Mistral、DeepSeek 等）。
- 最值得相信的部分:
  - 多任务长期一致改进趋势（而不是单 benchmark 最高分）。
  - 在代码和长上下文任务上的“可用性改善”反馈。
- 需谨慎解读:
  - 对 judge model 依赖较强的评测。
  - 多轮工具调用、代理式任务在不同 harness 下的不可比性。

## Engineering Takeaways

- 对训练:
  - 保持架构连续，重点投资数据与后训练，通常比盲目换架构更稳。
- 对部署:
  - 多尺寸统一能力风格，有利于从边缘设备到服务器集群的分层部署。
- 对数据工程:
  - 强化代码/推理/长文档数据是提升真实可用性的关键，而非可选项。
- 对后训练:
  - 指令遵循、格式一致性和工具可调用性需要共同优化，不能分割看待。

## What Is Actually Worth Learning

- 值得抄作业:
  - 用系列化产品线管理不同参数规模下的能力一致性。
  - 把“可用性指标”作为训练目标，而不仅是理论 benchmark。
- 工程折中:
  - 通用能力、代码能力、长上下文能力之间的配比一定存在 trade-off。
  - 推理效果与安全拒答策略之间要持续调平衡。
- 暂时难直接复用:
  - 大规模高质量数据闭环。
  - 高成本偏好数据采集和人类评估体系。

## Cross-References

- 相关模型:
  - [Qwen2](qwen2.md)
  - [Llama 3](../llama/llama3.md)
  - [DeepSeek-V3](../deepseek/deepseek_v3.md)
- 相关论文:
  - [DPO](../../papers/alignment/dpo.md)
  - [PPO](../../papers/alignment/ppo.md)
  - [RoFormer / RoPE](../../papers/architecture/roformer.md)
- 相关专题:
  - [Post-training](../../topics/post_training.md)
  - [Long Context](../../topics/long_context.md)
  - [Synthetic Data](../../topics/synthetic_data.md)

## Open Questions

- 未完全公开细节:
  - 数据配比、去重策略细粒度参数、完整训练预算。
- 可能依赖隐藏设置的结论:
  - 某些专项能力提升是否来自特定数据分布或特定后训练 trick。
- 后续追踪重点:
  - Qwen 后续版本在 reasoning/tool-use 上的持续迭代。
  - 开源实现与官方发布在推理稳定性上的差异。

## References

- Primary source:
  - [Qwen2.5 Technical Report (to verify)](https://arxiv.org/search/?query=qwen2.5&searchtype=all)
- Supplemental material:
  - [Qwen Official Organization on Hugging Face](https://huggingface.co/Qwen)
  - [QwenLM GitHub](https://github.com/QwenLM)
- Related reading:
  - [Qwen2 Technical Report](https://arxiv.org/abs/2407.10671)
  - [Llama 3 Report](https://arxiv.org/abs/2407.21783)
  - [DeepSeek-V3 Report](https://arxiv.org/abs/2412.19437)

## Review Checklist

- [ ] 关键事实已核查
- [x] 术语和缩写已统一
- [x] 横向对比没有偷换结论
- [ ] 已补齐主要链接
