---
title: The Llama 3 Herd of Models
type: model_report
family: llama
status: ai_draft
source_status: verified
release_date: 2024-07-23
model_scope: dense base + instruct + multimodal experiments
params: 8B, 70B, 405B
topics:
  - dense_transformer
  - multilingual
  - post_training
  - long_context
  - tool_use
source:
  kind: arxiv
  ref: "2407.21783"
  official: "https://llama.meta.com/"
---

# The Llama 3 Herd of Models

## TL;DR

- 核心创新点不是某个“炫技模块”，而是 Meta 明确把 `data + scale + managing complexity` 作为三根主线，最后选择了 `dense Transformer + 15T 级数据 + 六轮 SFT/RS/DPO` 这条更稳的路线。
- 这篇报告在开源生态里的位置非常明确: 它不是最激进的架构论文，而是“大厂如何把开源 dense LLM 做到旗舰级”的方法论报告。
- 最值得先读的部分是 `Section 3 Pre-Training`、`Section 4 Post-Training`、`Table 3`、`Table 4`、`Table 7`。

## 3-Minute Summary

- Llama 3 这篇报告描述的是一整套模型族，而不是单一 checkpoint。核心成员是 `8B / 70B / 405B` 三个 dense 模型，覆盖 `base` 和 `instruct`，并进一步延伸到长上下文、工具使用和多模态实验。
- 这篇报告最值得学习的地方有三个:
  - 为什么 Meta 在 `2024` 依然选择 `dense`，而不是 `MoE`
  - 数据工程如何从“海量抓取”升级为“可控的高质量数据混合系统”
  - post-training 如何通过 `SFT + Rejection Sampling + DPO` 的迭代流程，把通用 base model 变成更强的 assistant
- 如果你把它只看成“Llama 3 benchmark 很强”，会错过真正值钱的东西。真正值钱的是它公开了大量 recipe 级别的判断: 数据配比、parser 设计、去重策略、annealing、4D parallelism、以及为什么复杂度管理本身就是模型设计的一部分。

## 这篇报告解决什么问题

- Meta 在这篇报告里要解决的核心问题不是“如何在某一项评测上赢一次”，而是“如何把一个公开可用的通用大模型家族推进到旗舰水平，同时不把训练复杂度推到无法管理”。
- 这在 `2024` 非常关键。因为当时开源生态有两条明显路线:
  - 一条是更激进的架构路线，例如 `MoE`
  - 另一条是更系统化的 dense recipe 路线
- Llama 3 选择的是后者。报告里直接写到，他们选择 `standard dense Transformer with minor adaptations`，而不是 `Mixture-of-Experts`，目的就是 `maximize training stability`。
- 这意味着 Llama 3 的方法论不是“我有一个神秘模块”，而是“我用更稳定的架构，把数据、训练和对齐每一步都做到更成熟”。

## 核心技术拆解

### Model Architecture

> Paper pointers: Table 3, Section 3.3, Figure 1.

- Llama 3 的主干仍然是标准自回归 dense Transformer。
- 公开配置如下:
  - `8B`: 32 层，model dim 4096，FFN dim 14336，32 个 attention heads，8 个 KV heads
  - `70B`: 80 层，model dim 8192，FFN dim 28672，64 个 attention heads，8 个 KV heads
  - `405B`: 126 层，model dim 16384，FFN dim 53248，128 个 attention heads，8 个 KV heads
- 结构上的关键点:
  - 使用 `GQA`，所有规模都统一为 `8` 个 KV heads。报告明确说这样做是为了提升 inference speed，并减小 decoding 阶段的 KV cache。
  - 激活函数是 `SwiGLU`。
  - 位置编码是 `RoPE`。
  - 继续预训练长上下文时，引入 document mask，避免同一 sequence 内不同 document 互相注意。
- 这套结构最重要的信号不是“新”，而是“收敛”。Meta 明确没有把架构当成主要创新点，而是有意识地减少架构复杂度，把复杂度预算留给数据和训练。
- 和 Llama 2 相比，能明确看到的变化有:
  - 数据规模极大扩大: 从 `1.8T` 到 `15T+`
  - 最大模型扩大到 `405B`
  - 上下文从标准预训练阶段的 `8K` 扩展到 continued pretraining 后的 `128K`
  - 全家族更加明确地服务于 multilingual、coding、reasoning 和 tool use
- 关于 Norm 位置:
  - 这篇报告没有像一些系统论文那样把完整 block diagram 里的 norm placement 写成 checklist，因此不要擅自把它写成“某种精确 pre/post norm 变体”。
  - 可以确认的是它延续了现代 decoder-only LLM 的优化 Transformer 路线，但 paper 本身没有把 norm placement 当作核心贡献展开。

### Data Engineering

> Paper pointers: Section 3.1, especially 3.1.1-3.1.3.

- Llama 3 把数据工程写得比很多技术报告都更系统，这一点非常值得学。
- 报告明确披露:
  - 预训练语料覆盖知识截止到 `2023` 年末
  - 训练总 token 量约 `15T`，旗舰 `405B` 模型的文字描述里进一步写到 `15.6T`
  - 最终数据混合 roughly 为:
    - `50%` general knowledge
    - `25%` mathematics and reasoning
    - `17%` code
    - `8%` multilingual
- 这个配比非常重要。它说明 Llama 3 并不是“通用 web 文本 + 少量代码”这种早期开源 recipe，而是明显把数学、推理、代码抬升到了主干地位。
- 清洗流水线方面，报告给出了好几条很有参考价值的细节:
  - 先做 `PII / unsafe / adult domain` 过滤
  - 自研 HTML parser，而不是直接依赖通用 third-party article parser
  - 对 code / math 页面保留结构信息
  - 保留图片的 `alt` 文本，因为数学内容经常以图片形式出现
  - 报告明确写到: 对主要基于 web 数据训练的模型来说，`markdown is harmful`，所以他们移除了 markdown 标记
- 去重策略是分层做的:
  - URL-level deduplication
  - document-level global MinHash deduplication
  - line-level deduplication
- 另一个非常值钱的点是“数据混合不是拍脑袋定的”。Meta 明确写到他们用 scaling-law experiments 来寻找 data mix，先在小模型上试 mix，再外推预测大模型效果。
- 数据课程方面，报告里有两个值得单独记住的动作:
  - `annealing data`: 在训练后段额外上采样高质量 code 和 math 数据
  - `continued pretraining for long context`: 先标准 8K 预训练，再继续预训练扩展到 128K
- 报告还强调 annealing 不使用常见 benchmark 训练集，目的是保留 few-shot 和 OOD 能力评估的可信度。

### Training Infrastructure

> Paper pointers: Table 4, Figure 5, system sections around large-scale training.

- Llama 3 报告里最容易被低估的部分是训练基础设施。它没有像 DeepSeek-V3 那样给出特别细的 kernel 级优化，但已经把大规模 dense 训练的很多核心信息说清楚了。
- 公开的并行配置显示:
  - 标准 8K 预训练阶段可用 `8,192` GPU，配置为 `TP=8, CP=1, PP=16, DP=64`
  - 更大规模阶段扩展到 `16,384` GPU，配置为 `TP=8, CP=1, PP=16, DP=128`
  - 128K continued pretraining 阶段使用 `16,384` GPU，并开启 `CP=16`
- BF16 MFU 公开为:
  - `43%` on 8,192 GPUs
  - `41%` on 16,384 GPUs
  - `38%` on 16,384 GPUs with `128K` context and context parallelism
- 这几个数字非常有含金量，因为它们告诉你:
  - dense 405B 的大规模训练不是靠极端黑科技“撑住”的
  - 而是靠扎实的 parallelism design 和较高但不过分夸张的 MFU 跑出来的
- 报告里还明确提到，`16K GPU training` 的复杂度和潜在故障场景远高于更大的 CPU cluster；而同步训练对单点故障很敏感，一个 GPU 故障就可能导致整 job 重启。
- 关于 loss spike 和稳定性:
  - 论文没有像 DeepSeek-V3 那样直接写“无 irrecoverable loss spike”，所以这里不能虚构结论
  - 但它明显把 fault handling、并行配置和可管理复杂度作为训练成功的重要前提

### Key Insights and Hidden Tricks

- 最反直觉的结论之一是: 在一个已经出现大量 `MoE` 尝试的时代，Meta 仍然明确选择 `dense`，理由不是“MoE 不强”，而是 `managing complexity` 和 `training stability`。
- 第二个很值钱的点是数据 parser。很多学习者会把数据工程理解成“抓网页 + 去重”，但 Llama 3 说明了 parser 质量会直接影响数学习题、代码和长文内容的保真度。
- 第三个点是 `markdown is harmful` 这类细节。它不像新算法那样吸睛，但它非常像真实 production pipeline 里决定效果的细小开关。
- 第四个点是 post-training 的稳定性做法。Llama 3 并没有直接跳到复杂 RL，而是把 `SFT -> RM -> rejection sampling -> DPO -> model averaging -> iterative rounds` 做得很系统。

## 训练与数据

- 旗舰模型 `405B` 使用 `15.6T` token、`8K` context 做标准预训练，然后 continued pretraining 到 `128K`。
- tokenizer / vocabulary:
  - vocabulary size `128,000`
- 数据处理重点:
  - 自研 parser
  - PII / adult / harmful domain filtering
  - URL / document / line 多层去重
  - code / math 结构保留
  - annealing 的高质量 code 和 math 数据
- 报告公开了混合比例和清洗逻辑，但没有公开完整数据源清单、逐语种比例、以及每一类数据的精确采样权重变化曲线。
- 这意味着 Llama 3 是“对外公开了方法论，但没有公开足以完全复现的数据细账”。

## 后训练 / 对齐

### SFT

> Paper pointers: Section 4.2, Table 7.

- Llama 3 的 post-training 数据是非常系统化的。
- Preference data 采集流程:
  - 每轮部署多个模型参与 annotation
  - 每个 prompt 从两个模型采两个回答
  - annotator 用四档强度标注偏好: `significantly better / better / slightly better / marginally better`
  - 对 chosen response 还加入 editing step，形成 `edited > chosen > rejected` 的更细粒度排序
- SFT 数据的 broad mix 公开得很细:
  - `General English 52.66%`
  - `Code 14.89%`
  - `Multilingual 3.01%`
  - `Exam-like 8.14%`
  - `Reasoning and tools 21.19%`
  - `Long context 0.11%`
- 这个表对学习非常重要。它说明 Llama 3 的 assistant 能力不是单纯靠“通用聊天数据”堆出来，而是明确在 SFT 阶段给 reasoning / tools 留了很高配额。

### Preference Optimization / RL

- Llama 3 的 post-training 主线不是 PPO，而是 `SFT + RM + RS + DPO`。
- rejection sampling 细节非常值得记:
  - 每个 prompt 通常采样 `10-30` 个回答
  - 用 reward model 选择最优 candidate
- DPO 稳定化手段也公开了:
  - 在 DPO 目标之外，额外加 chosen sequence 的 `NLL regularization`
  - 目标是稳住格式、避免 chosen response 的概率下降
- 另一个大厂级技巧是 `model averaging`
  - 在 RM / SFT / DPO 阶段，对不同数据版本和超参版本的模型做平均
- 整个迭代流程执行了 `6` 轮
  - 每轮都重新收集 preference data 和 SFT data
  - synthetic data 则从最新模型中继续采样
- 这一点说明 Llama 3 的 post-training 不是一个静态单次作业，而是一个持续滚动的 alignment pipeline。

## 评测与对比

- 代表性结果显示 Llama 3.1 405B Instruct 已经是非常强的公开 dense 模型:
  - `MMLU 87.3`
  - `MMLU-Pro 73.3`
  - `IFEval 88.6`
  - `HumanEval 89.0`
  - `GSM8K 96.8`
  - `MATH 73.8`
  - `GPQA 51.1`
  - `BFCL 88.5`
  - `MGSM 91.6`
- 长上下文指标也被明确纳入主表:
  - `ZeroSCROLLS/QuALITY 95.2`
  - `InfiniteBench/En.MC 83.4`
  - `NIH/Multi-needle 98.1`
- 对比对象包括 `GPT-4`, `GPT-4o`, `Claude 3.5 Sonnet`, `Nemotron 4 340B`, `Mixtral 8x22B` 等。
- 需要谨慎看的部分:
  - human eval 和 open-ended eval 仍然高度依赖内部流程
  - tool-use 任务的评测依赖具体 API 设定与 execution harness
- 但总体趋势非常明确:
  - Llama 3 的旗舰公开模型已经不只是“开源里最好之一”
  - 它在多个主流维度上都进入了可以直接和闭源前线模型横向比较的区间

## 相关代码 / 复现

- 官方站点: [Llama 官网](https://llama.meta.com/)
- 官方仓库: [meta-llama/llama3](https://github.com/meta-llama/llama3)
- 官方 Hugging Face: [meta-llama/Llama-3.1-70B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-70B-Instruct)
- 说明:
  - 官方仓库更偏“最小加载示例”
  - 真正的训练 recipe 并未完整开源
  - 所以这篇报告更适合做“方法论复盘”，不适合被误解成“可一键复刻”

## 真正值得学的点

- 值得抄作业的部分:
  - 用 scaling laws 选 data mix
  - 自研高质量 parser，而不是盲信通用抽取工具
  - post-training 中把 RS 和 DPO 迭代成多轮闭环
  - 在长上下文阶段引入 document mask
- 只适合大厂 / 大集群的部分:
  - 16K GPU dense 405B 训练
  - 大规模人类偏好标注和后续编辑流程
  - 多轮模型平均和大规模 reward model 体系
- 对个人学习者最有价值的部分:
  - 数据工程比想象中重要得多
  - dense 模型并没有“过时”，关键是 recipe 是否成熟
  - 简洁且可管理的系统设计，本身就是竞争力

## 局限与疑问

- 报告没有公开足够多的数据源细节，无法支持严格复现。
- architecture 层面的很多微观实现没有像系统论文那样完全展开，因此读者需要结合模型卡和推理实现继续确认。
- 它虽然给出大量评测，但仍有不少结论依赖内部 harness、human eval 流程或专有对比接口。
- 论文强调 dense 的稳定性优势，但没有在公开材料里给出与同等级 MoE 方案的系统性成本对照，因此“为什么没有用 MoE”目前更多是工程判断，而不是严格 controlled experiment。

## 延伸阅读

- 前置材料: [Llama 2](llama2.md)
- 同路线报告: [Qwen2](../qwen/qwen2.md), [DeepSeek-V3](../deepseek/deepseek_v3.md)
- 应该一起读的方法论文:
  - [DPO](../../papers/alignment/dpo.md)
  - [FlashAttention](../../papers/architecture/flashattention.md)

## Review Checklist

- [x] 关键事实已核查
- [x] 公开信息和个人推断已分开
- [x] 关键图表和结论已对应到原文位置
- [x] 已补充官方仓库 / 权重 / 复现链接
