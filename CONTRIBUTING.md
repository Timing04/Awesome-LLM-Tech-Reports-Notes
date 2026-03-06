# CONTRIBUTING

欢迎为这个仓库补充内容、修正错误和优化结构。为了保证仓库长期可维护，请遵守以下约定。

## 贡献目标

优先贡献以下内容:

- 可学习价值高的开源模型 technical report / system report / model card
- LLM 核心算法和高频方法论文
- 跨模型、跨论文的专题总结
- 错误修正、事实核查和链接补全

## 写作原则

- 一篇材料只维护一份正文，不要复制到多个目录
- 明确区分“事实摘录”和“技术解读”
- 不要只复述摘要，尽量解释技术动机、方法设计和工程含义
- 引用原始材料时尽量给出来源链接、章节或图表位置
- 如果内容由 AI 起草，请明确保留 `status: ai_draft`

## 目录约定

- `models/`: 模型报告主笔记
- `papers/`: 方法论文主笔记
- `topics/`: 横向专题总结
- `indexes/`: 索引页和学习路径
- `data/`: 待收录条目与元数据

## 新增内容流程

1. 先在 `data/models.yaml` 或 `data/papers.yaml` 补充条目
2. 选择合适模板:
   - `templates/model_note_template.md`
   - `templates/paper_note_template.md`
   - `templates/topic_template.md`
3. 生成 Markdown 文件并填写 frontmatter
4. 根据完成度设置 `status`
5. 在相关 `indexes/` 或 `topics/` 页面中补充导航

## Frontmatter 建议字段

```yaml
---
title: Qwen2 Technical Report
type: model_report
family: qwen
status: ai_draft
source_status: to_verify
release_date: 2024-00-00
topics:
  - dense_transformer
  - multilingual
  - post_training
source:
  kind: arxiv
  ref: "2407.10671"
  official: ""
---
```

## 质量标准

- `seeded`: 只有条目，没有正文
- `ai_draft`: 模板结构完整，但事实和结论还未充分核查
- `reviewed`: 已人工校对主要事实、术语、链接和结构
- `polished`: 已形成高质量学习笔记，能支持复盘和横向比较

## Pull Request 建议

- 一个 PR 只做一类事情
- 内容新增和结构改造尽量分开
- 如果你修正了事实错误，请在描述里说明修正依据
- 如果你新增专题页，请说明它关联了哪些模型或论文
