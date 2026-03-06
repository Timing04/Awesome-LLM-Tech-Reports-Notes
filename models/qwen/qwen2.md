---
title: Qwen2 Technical Report
type: model_report
family: qwen
status: ai_draft
source_status: verified
release_date: 2024-07-15
model_scope: base + instruct + moe
params: 0.5B, 1.5B, 7B, 72B dense; 57B-A14B MoE
topics:
  - dense_transformer
  - multilingual
  - post_training
  - long_context
source:
  kind: arxiv
  ref: "2407.10671"
  official: "https://github.com/QwenLM/Qwen2"
---

# Qwen2 Technical Report

## TL;DR

`Qwen2` 的核心价值不是某一个爆点结构，而是一套非常完整、非常“产品化”的开源通用 LLM recipe: 用更强的数据筛选和多语言覆盖做预训练底座，用 `GQA + YaRN + DCA` 把长上下文拉起来，再把 `SFT + DPO + 在线偏好优化` 串成后训练闭环。它在开源生态中的位置很明确: 如果你想学习一个“不是只会刷榜，而是真的面向实际部署”的通用模型家族，`Qwen2` 是非常高价值的样本。

## 3-Minute Summary

- `Qwen2` 发布了完整的模型家族: `0.5B / 1.5B / 7B / 72B` 稠密模型，以及 `57B-A14B` 的 `MoE` 模型，同时提供 `Base` 和 `Instruct` 路线。
- 报告公开了很多真正有学习价值的细节: tokenizer、架构配置、长上下文做法、预训练数据扩展方向、以及后训练 recipe。
- 这篇报告最值得学的点不只是“Qwen2 达到了什么分数”，而是它明确展示了一条通用大模型的工程路径: `高质量预训练数据 -> 长上下文扩展 -> 自动化后训练数据构造 -> DPO + 在线偏好优化`。
- 同时，报告也有明显留白，尤其是算力基础设施、精确数据配比、reward model 细节没有完全公开。读这篇报告时，最好把“公开 recipe”与“未公开细节”区分开。

## 这篇报告解决什么问题

`Qwen2` 要解决的不是一个单任务问题，而是“如何做出一套真正能覆盖多语言、代码、数学、长上下文、对话场景的开源模型家族”。

相比前代 `Qwen1.5`，它强化了几条主线:

- 多语言覆盖更广
- 代码和数学能力更强
- 长上下文支持更完整
- 后训练更接近产品化闭环，而不只是做一次 SFT

从学习角度看，`Qwen2` 不是那种“结构很花哨但难复用”的论文。它更像一份通用 LLM 工程说明书，适合回答下面这些问题:

- 开源通用模型为什么普遍开始用 `GQA`？
- 长上下文不是只改 `RoPE` base，还要配什么？
- 预训练数据到底是“更多”更重要，还是“更干净”更重要？
- 后训练怎么把自动合成、规则验证、离线偏好优化和在线优化接起来？

## 核心技术拆解

### Model Architecture

`Qwen2` 的基础骨架仍然是 `decoder-only Transformer`，但它在几个关键点上已经非常接近今天主流高性能开源模型的默认配置。

#### 架构主干

- `RMSNorm`
- `pre-norm`
- `SwiGLU`
- `RoPE`
- `QKV bias`
- `Grouped Query Attention (GQA)`

如果你拿它和 `Llama` 系列比较，可以看到一个很清晰的共性: 大家都已经收敛到“`RoPE + RMSNorm + SwiGLU + GQA/类GQA`”这一套高性价比骨架。区别不在于大方向，而在于训练 recipe、长上下文处理和后训练细节。

#### 稠密模型配置

报告给出的主要 dense 配置是:

- `Qwen2-0.5B`: 24 层，hidden size `896`
- `Qwen2-1.5B`: 28 层，hidden size `1536`
- `Qwen2-7B`: 28 层，hidden size `3584`
- `Qwen2-72B`: 80 层，hidden size `8192`

从这里可以看出两点:

- 小模型并没有简单沿用大模型缩放，而是做了适合产品部署的分档
- `72B` 仍然走 dense 路线，说明 Qwen2 的主力通用旗舰并没有完全押注 `MoE`

#### MoE 版本

`Qwen2-57B-A14B` 的关键配置:

- 总参数约 `57B`
- 每 token 激活参数约 `14B`
- `64` 个 routed experts
- `8` 个 activated experts
- `8` 个 shared experts

这条设计路线和 `Mixtral 8x7B` 有相似处，但并不是简单复刻。Qwen2 明确强调使用 shared experts 来补足 routed experts 容易忽略的公共知识通道，这是一种很典型的 MoE 工程折中。

#### 长上下文设计

Qwen2 的长上下文不是单点技巧，而是组合拳:

- `RoPE` base 从 `10000` 改到 `1000000`
- 引入 `YaRN` 做位置外推
- 使用 `Dual Chunk Attention (DCA)`
- 在训练末期显式加入长文本数据，并把上下文从 `4K` 拉到 `32K`
- 报告给出最高支持 `128K+` 的结果展示

这一点很值得学。很多人把长上下文理解成“改个 RoPE 插值系数”，但 Qwen2 明确告诉你: 真正可用的长上下文能力至少涉及位置编码、attention 机制、数据分布和训练阶段安排四件事。

### Data Engineering

这是 `Qwen2` 最值钱的部分之一，也是最值得学习的部分。

#### 数据规模与分布

报告公开的核心事实包括:

- 主要高质量预训练数据规模超过 `7T` tokens
- 相比 `Qwen1.5` 的 `3T`，显著增强了代码、数学和多语言数据
- 覆盖约 `30` 种语言

但报告没有公开精确数据配比。这一点要明确写出来，因为很多二手总结会把“加强代码、数学、多语言”误写成某种精确比例。原报告给的是方向，不是完整 recipe。

#### 清洗与阈值控制

Qwen2 报告里非常有价值的一条结论是:

- 团队尝试过把筛选阈值放宽，构造约 `12T` tokens 的更大语料
- 但最终结果并没有显著优于 `7T` 的高质量版本
- 因此最终选择了更严格筛选后的 `7T` 路线

这条结论几乎可以单独写进仓库首页，因为它代表了一个非常重要的现代 LLM 数据观:

- 数据工程不是简单追求 token 数量最大化
- 在足够大规模后，分布质量和去噪质量往往比继续放量更重要

#### Synthetic Data 与 Instruction-like Data

Qwen2 报告明确提到，在预训练过程中混入了高质量多任务 instruction-like data，用来提升 in-context learning 和 instruction following。这个做法很值得注意，因为它说明:

- 预训练和后训练之间的边界正在变得模糊
- 有些“指令遵循能力”并不是完全留到 SFT 才学
- 高质量 synthetic / reformulated instruction data 已经被视作预训练数据工程的一部分

#### Curriculum Learning

Qwen2 并没有像一些论文那样给出非常显式的 curriculum 表格，但从报告透露的信息看，至少有两条课程式安排:

- 在训练末期单独进行长上下文扩展，说明序列长度扩展是 staged 而不是从头到尾一次性完成
- 将 instruction-like 数据和后续对齐数据分层引入，而不是一开始就用单一混合数据一锅炖

### Training Infrastructure

这里要诚实地写: `Qwen2` 报告没有像 `Llama 3` 或 `DeepSeek-V3` 那样充分公开硬件规模、并行策略、MFU 和训练时长。

这意味着你无法从原报告里学到完整的训练系统 recipe，例如:

- 总共用了多少 GPU
- 训练总时长是多少
- 使用了怎样的 `3D parallelism`
- 是否有特殊的 loss spike 恢复机制

但这并不意味着这一部分毫无价值。恰恰相反，`Qwen2` 给了一个很现实的信号: 对很多工业开源团队来说，愿意公开“模型如何训练”和“数据如何构造”，不等于愿意把最核心的系统基础设施全部公开。

因此读 `Qwen2` 时，最好的学习方式是:

- 架构和数据部分直接学
- 基础设施部分承认信息不完整，再拿 `Llama 3 / DeepSeek-V3` 补系统视角

### Key Insights 与“不传之秘”

#### 1. 7T 高质量数据优于 12T 放宽阈值数据

这不是一个小结论，而是通用 LLM 训练里的关键判断。很多团队真正拉不开差距的地方，往往不是参数量，而是数据筛选标准和分布控制。

#### 2. 长上下文不是一个参数，而是一条训练支线

Qwen2 的 `YaRN + DCA + RoPE base 调整 + 长文本数据 + staged extension` 非常值得抄。它告诉你长上下文能力来自系统设计，而不是单独某个 patch。

#### 3. 后训练的核心不是“用了 DPO”

很多人会把报告读成“Qwen2 用了 DPO，所以效果好”。这太浅了。真正关键的是它把:

- 自动数据构造
- 可执行反馈
- rejection sampling
- 离线 DPO
- 在线偏好优化

串成了一个闭环。这才是通用对齐系统最有价值的地方。

## 训练与数据

### Tokenizer

- 采用 `byte-level BPE`
- 词表规模 `151,646`

一个足够大的 tokenizer 在多语言和代码场景里很重要，因为它直接影响:

- 中文、阿拉伯文等非拉丁文字的分词效率
- 代码中的符号、缩进和长标识符表示方式
- 长上下文下 token 膨胀速度

### 预训练数据方向

报告明确强调增强了这些方向:

- 通用高质量网页文本
- 代码
- 数学
- 多语言语料

但没有公开精确配比。因此在笔记里应该坚持写“方向增强”，而不是编造具体比例。

### 长上下文阶段

Qwen2 在训练末期把上下文长度从 `4096` 扩到 `32768`，同时引入更多长文本数据，并配合 `YaRN` 与 `DCA`。这类 staged length extension 是很典型、也很值得学的做法，因为从头用超长序列训练通常成本过高。

## 后训练 / 对齐

### SFT 数据与筛选

报告公开的核心事实:

- `SFT` 数据规模超过 `500k`
- 覆盖 instruction following、coding、math、reasoning、role-play、multilingual、safety 等多个方向
- 使用 `32768` 序列长度训练 `2` 个 epoch

这个信息量其实不小。它说明 Qwen2 的 `SFT` 已经不是短指令问答级别的 recipe，而是明确支持长上下文、多任务和复杂推理的统一式后训练。

### 数据构造方法

Qwen2 的后训练数据构造大致包含这些模块:

- `Collaborative Data Annotation`
- `Automated Data Synthesis`
- `Rejection Sampling`
- `Execution Feedback`
- `Data Repurposing`
- `Constitutional Feedback`

这组模块非常值得学习，因为它几乎覆盖了现代开源对齐最常见的数据来源:

- 人工标注补高价值样本
- synthetic data 放大覆盖面
- rule / executor 用于提高正确性
- repurposing 降低数据获取成本
- constitutional feedback 补安全边界

### DPO 与在线偏好优化

报告明确写到所有模型都经历了 `SFT + DPO`。在此基础上，团队还做了在线偏好优化:

- 用 reward model 从多条采样回答中挑出更优和更差回答
- 继续进行 DPO 风格的偏好训练
- 使用 `Online Merging Optimizer` 缓解 alignment tax

这说明 `Qwen2` 的对齐路线不是“离线 DPO 一步到位”，而是:

```text
SFT -> Offline DPO -> Online preference optimization -> anti-alignment-tax adjustment
```

对学习者来说，这条链路比单独记住 `DPO` 这个词重要得多。

## 评测与对比

### Base 模型代表结果

`Qwen2-72B` 的代表指标包括:

- `MMLU 84.2`
- `MMLU-Pro 55.6`
- `GPQA 37.9`
- `HumanEval 64.6`
- `GSM8K 89.5`
- `BBH 82.4`
- `C-Eval 91.0`
- `CMMLU 90.1`

从这些分数能读出的重点不是“它每项都第一”，而是它在:

- 中文
- 多语言
- 数学
- 代码
- 通用知识

几条主线上都做到了相对均衡，没有明显短板。

### Instruct 模型代表结果

`Qwen2-72B-Instruct` 的代表指标包括:

- `MT-Bench 9.12`
- `Arena-Hard 48.1`
- `LiveCodeBench v1 35.7`
- `IFEval strict-prompt 77.6`
- `MATH 69.0`
- `GSM8K 93.2`

这组结果说明后训练并不是只把聊天体验变好，而是连代码、数学和指令遵循也一起拉升了。

### 长上下文与多语言

报告还给出了 `Needle in a Haystack`、`NeedleBench` 和 `LV-Eval` 等长上下文与长文档测试结果，并提供了多语言 human evaluation。这里最值得读的不是具体单项分数，而是两个趋势:

- Qwen2 把长上下文评测做得比很多只给单一 retrieval 图的报告更完整
- 它的多语言能力不是停留在 tokenization 层，而是在人工评估里也表现出较强竞争力

## 相关代码 / 复现

- 官方仓库: [Qwen2 GitHub](https://github.com/QwenLM/Qwen2)
- Hugging Face 模型页: [Qwen Organization](https://huggingface.co/Qwen)
- 技术报告: [Qwen2 Technical Report](https://arxiv.org/abs/2407.10671)
- HTML 阅读版: [ar5iv HTML](https://ar5iv.labs.arxiv.org/html/2407.10671v4)

如果你想找“较小规模可学习复现”，Qwen 系列没有像 `TinyLlama` 那样直接对应的官方全流程复现项目，所以更现实的做法通常是:

- 学它的数据与后训练 recipe
- 用更小模型在 `Transformers + TRL` 上复现 `SFT + DPO`
- 把 `YaRN / GQA / 长上下文 staged extension` 这些设计迁移到自己的实验设置里

## 真正值得学的点

- 高质量数据筛选比盲目扩 token 更重要，`7T > 12T` 是整篇报告最有价值的信号之一。
- 长上下文能力要通过“位置编码 + attention 机制 + 数据 + 训练阶段”联合设计。
- 通用模型的后训练不应该只理解成一个 loss，而应该理解成一套数据构造与优化闭环。
- 多语言、代码、数学、对话不是互相独立的四件事，Qwen2 的 recipe 本质上是在做统一式通用模型设计。

## 局限与疑问

- 精确数据配比没有公开，很多关于“为什么它在哪项上更强”的分析只能做到方向层。
- 硬件规模、训练时长、MFU、并行策略等基础设施细节披露不足，限制了系统层复盘。
- 在线偏好优化阶段的 reward model 架构与采样预算没有完全公开。
- MoE 版本的工程细节公开度明显低于 dense 版本，因此更适合作为补充阅读，而不是主线学习入口。

## 延伸阅读

- [Qwen2.5](qwen2_5.md)
- [DPO](../../papers/alignment/dpo.md)
- [RoFormer / RoPE](../../papers/architecture/roformer.md)
- [Long Context](../../topics/long_context.md)
- [Post-training](../../topics/post_training.md)
- [Synthetic Data](../../topics/synthetic_data.md)

## Review Checklist

- [x] 关键事实已核查
- [x] 术语和缩写已统一
- [x] 横向对比没有偷换结论
- [x] 已补齐主要链接
