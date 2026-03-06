---
title: {{TITLE}}
type: model_report
family: {{FAMILY}}
status: seeded
source_status: {{SOURCE_STATUS}}
release_date: {{RELEASE_DATE}}
model_scope: {{MODEL_SCOPE}}
params: {{PARAMS}}
topics:
{{TOPICS_BLOCK}}
source:
  kind: {{SOURCE_KIND}}
  ref: "{{SOURCE_REF}}"
  official: "{{OFFICIAL_URL}}"
---

# {{TITLE}}

## TL;DR

- 核心创新点:
- 这篇报告在开源 LLM 生态里的位置:
- 最值得先读的章节 / 图表:

## 3-Minute Summary

- 这篇报告主要做了什么:
- 相比上一代 / 同代模型，最重要的变化是什么:
- 读完之后你应该带走哪 3 个结论:

## 这篇报告解决什么问题

- 作者要解决的核心矛盾是什么:
- 为什么这个问题在当时重要:
- 它更偏“研究突破”还是“系统工程整合”:

## 核心技术拆解

### Model Architecture

- 参数规模、层数、隐藏维度:
- 注意力设计: 是否使用 GQA / MQA / MLA / SWA / RoPE / YaRN:
- FFN / MoE 设计:
- 激活函数、Norm、残差与特殊结构:
- 和 Llama / Qwen / DeepSeek / Mistral 等主流架构相比，具体改了什么:
- 如果报告没有公开某项细节，也要明确写出来，不要猜。

### Data Engineering

- 数据规模与主要来源:
- 数据配比: Web / Code / Math / Multilingual / Synthetic:
- 清洗流水线: dedup / filtering / parser / PII / contamination:
- 合成数据策略:
- 数据课程 / annealing / curriculum:
- 哪些数据细节公开了，哪些没有公开:

### Training Infrastructure

- 硬件规模、GPU 型号、训练时长:
- 并行策略: TP / PP / DP / EP / ZeRO / Offload / CP:
- 训练吞吐 / MFU / 成本:
- 稳定性挑战: loss spike / fault tolerance / checkpoint / rollback:
- 哪些系统优化值得单独学:

### Key Insights and Hidden Tricks

- 报告中最反直觉的结论:
- 真正影响结果但容易被忽略的 trick:
- 这些 trick 属于“普适方法”，还是“该团队/该集群专属方法”:

## 训练与数据

- 预训练 recipe:
- tokenizer / vocabulary:
- sequence length 设计:
- 训练阶段拆分:
- 是否做 continued pretraining / context extension / domain annealing:
- 如果有关键超参，记录公开部分；如果没有公开，明确标注“未披露”。

## 后训练 / 对齐

### SFT

- 数据来源:
- 数据筛选标准:
- 数据量级:
- 是否区分 reasoning / non-reasoning / tools / safety:

### Preference Optimization / RL

- 使用了什么方法: PPO / DPO / GRPO / 其他:
- reward 设计:
- RM 是否公开:
- 关键超参和训练 trick:
- 对齐阶段最关键的工程选择:

## 评测与对比

- 报告重点 benchmark:
- 关键对比对象:
- 哪些结果最值得信:
- 哪些结果需要谨慎读:
- 评测有没有 hidden caveat: judge model / internal eval / majority voting / long-CoT:

## 相关代码 / 复现

- 官方仓库:
- Hugging Face / ModelScope / 官方权重:
- 可参考的开源复现:
- 如果没有官方代码，要写清楚。

## 真正值得学的点

- 值得抄作业的部分:
- 只适合大厂 / 大集群的部分:
- 对个人学习者最有价值的部分:

## 局限与疑问

- 报告刻意没有说的:
- 目前无法从公开材料判断的:
- 我对这篇报告仍然保留怀疑的地方:

## 延伸阅读

- 前置材料:
- 同路线报告:
- 应该一起读的方法论文:

## Review Checklist

- [ ] 关键事实已核查
- [ ] 公开信息和个人推断已分开
- [ ] 关键图表和结论已对应到原文位置
- [ ] 已补充官方仓库 / 权重 / 复现链接
