# LLM-Tech-Reports-Notes

一个面向大模型算法学习的开源仓库，重点整理:

- 开源模型的 technical report / system report / model card 阅读笔记
- LLM 常用算法与关键论文的技术分析
- 跨模型、跨论文的横向专题总结

这个仓库的目标不是“收录最多”，而是尽量把每篇材料变成可学习、可复盘、可对比的笔记。

## 仓库定位

- 主要关注可学习价值高、技术细节相对充分的开源模型
- 优先收录能够帮助理解训练、架构、后训练、评测和工程取舍的材料
- 保留两条主线:
  - 纵向: 按模型家族整理，如 Llama、Qwen、DeepSeek、Mistral
  - 横向: 按技术主题整理，如 MoE、长上下文、后训练、Reasoning RL

## 收录原则

- 正文只保留一份，避免同一篇材料在多个目录重复维护
- `models/` 存放模型报告主笔记
- `papers/` 存放方法论文主笔记
- `topics/` 存放跨材料的专题总结，不重复正文
- `indexes/` 提供学习路径、难度分级和分类导航

## 内容状态

- `seeded`: 已建条目和元数据，尚未生成正文
- `ai_draft`: 已由 AI 生成初稿，待人工校对
- `reviewed`: 已经过人工校对，内容基本可用
- `polished`: 已完成高质量精读和结构化总结

## 仓库结构

```text
LLM-Tech-Reports-Notes/
├── README.md
├── ROADMAP.md
├── CONTRIBUTING.md
├── models/
├── papers/
├── topics/
├── indexes/
├── templates/
├── data/
├── scripts/
├── assets/
└── .github/
```

## 建议使用方式

1. 从 [indexes/by_learning_path.md](indexes/by_learning_path.md) 选择一条学习路线
2. 用 [indexes/by_family.md](indexes/by_family.md) 或 [indexes/by_topic.md](indexes/by_topic.md) 定位材料
3. 在 [ROADMAP.md](ROADMAP.md) 查看当前收录范围和状态
4. 优先阅读 `reviewed` / `polished` 内容，再把 `ai_draft` 当作辅助草稿

## AI 初稿工作流

1. 在 `data/models.yaml` 或 `data/papers.yaml` 中补充条目
2. 使用 `templates/` 中的模板生成 Markdown 骨架
3. 将内容状态标记为 `ai_draft`
4. 逐步人工修订为 `reviewed` 或 `polished`

AI 生成的内容只作为加速器，不作为最终质量标准。这个仓库会显式区分“事实摘录”和“技术解读”，避免把未经验证的总结直接当结论。

## 第一阶段目标

- 先完成一批代表性模型家族的种子清单
- 先覆盖一批高频技术主题: 架构、数据、后训练、长上下文、Reasoning RL
- 先建立统一模板和元数据，保证后续可以自动扩展

## 近期重点

- 模型主线: Llama / Qwen / DeepSeek / Mistral / Gemma
- 技术主线: MoE / Post-training / Long Context / Synthetic Data / Reasoning RL
- 论文主线: PPO / DPO / GRPO / FlashAttention / RoPE / Ring Attention

## 贡献方式

贡献前请先读 [CONTRIBUTING.md](CONTRIBUTING.md)。

欢迎以下类型的贡献:

- 补充缺失的技术报告或关键论文
- 修正事实错误、补充实验或训练细节
- 增加跨模型的专题总结
- 优化目录、索引和学习路径

## License

本仓库代码与文档采用 [MIT License](LICENSE)。
