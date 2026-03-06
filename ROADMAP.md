# ROADMAP

这个文件用于维护仓库的收录边界、优先级和状态，避免仓库演化成无结构的资料堆。

## 状态说明

- `seeded`: 已列入计划，待生成初稿
- `ai_draft`: AI 初稿已生成，待人工修订
- `reviewed`: 人工校对完成
- `polished`: 高质量精读完成

## 优先级说明

- `P0`: 优先启动，适合作为第一批内容
- `P1`: 第二阶段补充
- `P2`: 有学习价值，但可以后置

## 模型报告计划

### Llama

- `P0` `seeded` `models/llama/llama2.md` Llama 2
- `P0` `ai_draft` `models/llama/llama3.md` Llama 3
- `P1` `seeded` `models/llama/llama3_1.md` Llama 3.1

### Qwen

- `P0` `seeded` `models/qwen/qwen1_5.md` Qwen1.5
- `P0` `ai_draft` `models/qwen/qwen2.md` Qwen2
- `P0` `seeded` `models/qwen/qwen2_5.md` Qwen2.5
- `P1` `seeded` `models/qwen/qwen2_5_coder.md` Qwen2.5-Coder
- `P1` `seeded` `models/qwen/qwen2_5_vl.md` Qwen2.5-VL
- `P1` `seeded` `models/qwen/qwen2_audio.md` Qwen2-Audio
- `P1` `seeded` `models/qwen/qwen3.md` Qwen3
- `P1` `seeded` `models/qwen/qwen3_embedding.md` Qwen3-Embedding

### DeepSeek

- `P0` `seeded` `models/deepseek/deepseek_v2.md` DeepSeek-V2
- `P0` `ai_draft` `models/deepseek/deepseek_v3.md` DeepSeek-V3
- `P0` `ai_draft` `models/deepseek/deepseek_r1.md` DeepSeek-R1
- `P1` `seeded` `models/deepseek/deepseek_coder.md` DeepSeek-Coder
- `P1` `seeded` `models/deepseek/deepseek_math.md` DeepSeekMath

### Mistral

- `P0` `seeded` `models/mistral/mistral_7b.md` Mistral 7B
- `P0` `seeded` `models/mistral/mixtral_8x7b.md` Mixtral 8x7B
- `P1` `seeded` `models/mistral/mixtral_8x22b.md` Mixtral 8x22B

### Gemma

- `P1` `seeded` `models/gemma/gemma2.md` Gemma 2
- `P1` `seeded` `models/gemma/gemma3.md` Gemma 3

### Yi / 其他中文开源模型

- `P2` `seeded` `models/yi/yi_34b.md` Yi-34B
- `P2` `seeded` `models/yi/yi_1_5.md` Yi-1.5
- `P2` `seeded` `models/internlm/internlm2_5.md` InternLM2.5

## 方法论文计划

### Alignment / Preference Optimization

- `P0` `seeded` `papers/alignment/instructgpt.md` InstructGPT / RLHF
- `P0` `seeded` `papers/alignment/ppo.md` PPO
- `P0` `ai_draft` `papers/alignment/dpo.md` DPO
- `P1` `seeded` `papers/alignment/ipo.md` IPO
- `P1` `seeded` `papers/alignment/orpo.md` ORPO
- `P1` `seeded` `papers/alignment/simpo.md` SimPO
- `P0` `ai_draft` `papers/alignment/grpo.md` GRPO
- `P1` `seeded` `papers/alignment/gspo.md` GSPO

### Architecture

- `P0` `seeded` `papers/architecture/transformer.md` Attention Is All You Need
- `P0` `seeded` `papers/architecture/switch_transformer.md` Switch Transformer
- `P0` `seeded` `papers/architecture/roformer.md` RoFormer / RoPE
- `P0` `ai_draft` `papers/architecture/flashattention.md` FlashAttention
- `P1` `seeded` `papers/architecture/gqa.md` Grouped-Query Attention
- `P1` `seeded` `papers/architecture/mla.md` Multi-head Latent Attention
- `P1` `seeded` `papers/architecture/multi_token_prediction.md` Multi-Token Prediction

### Data Engineering

- `P0` `seeded` `papers/data/self_instruct.md` Self-Instruct
- `P1` `seeded` `papers/data/orca.md` Orca
- `P1` `seeded` `papers/data/textbooks_are_all_you_need.md` Textbooks Are All You Need
- `P1` `seeded` `papers/data/synthetic_data.md` Synthetic Data Survey / Key References

### Long Context

- `P0` `seeded` `papers/long_context/alibi.md` ALiBi
- `P0` `seeded` `papers/long_context/position_interpolation.md` Position Interpolation
- `P0` `seeded` `papers/long_context/yarn.md` YaRN
- `P0` `seeded` `papers/long_context/ring_attention.md` Ring Attention

### Evaluation

- `P1` `seeded` `papers/evaluation/mmlu.md` MMLU
- `P1` `seeded` `papers/evaluation/gpqa.md` GPQA
- `P1` `seeded` `papers/evaluation/mt_bench.md` MT-Bench
- `P1` `seeded` `papers/evaluation/swe_bench.md` SWE-bench

## 横向专题计划

- `P0` `seeded` `topics/moe.md` MoE
- `P0` `seeded` `topics/post_training.md` Post-training
- `P0` `seeded` `topics/long_context.md` Long Context
- `P0` `seeded` `topics/reasoning_rl.md` Reasoning RL
- `P1` `seeded` `topics/synthetic_data.md` Synthetic Data
- `P1` `seeded` `topics/multimodal.md` Multimodal LLM
- `P1` `seeded` `topics/evaluation.md` Evaluation and Benchmark Reading

## 第一批落地建议

如果以“先让仓库可用”为目标，建议第一批先完成以下内容:

- 模型: Llama 2, Llama 3, Qwen2, Qwen2.5, DeepSeek-V3, DeepSeek-R1, Mixtral 8x7B
- 论文: PPO, DPO, GRPO, RoFormer, FlashAttention, Ring Attention
- 专题: MoE, Post-training, Long Context, Reasoning RL

## 维护原则

- 先建索引和元数据，再批量生成 AI 初稿
- AI 初稿不直接视作完成，需要进入人工修订流
- 同一篇材料只维护一份正文，专题页只做抽象总结和横向对比
