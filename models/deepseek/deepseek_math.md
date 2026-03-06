---
title: DeepSeekMath
type: model_report
family: deepseek
status: ai_draft
source_status: verified
release_date: 2024-02-06
model_scope: base + instruct + RL-enhanced math
params: 7B
topics:
  - math_reasoning
  - grpo
  - verifiable_rewards
source:
  kind: arxiv
  ref: "2402.03300"
  official: ""
---

# DeepSeekMath

## TL;DR

- DeepSeekMath 的关键贡献不是“再做一个数学模型”，而是系统展示了可验证数学任务中 `GRPO` 的有效性。
- 报告核心思想是把数学推理任务转成高可验证奖励场景，减少对主观偏好奖励的依赖。
- 对学习者最有价值的是：如何把 `SFT -> RL` 串成可落地的 reasoning 训练管线。

## 3-Minute Summary

- 模型基于开源 7B 底座，针对数学语料与推理训练做专项优化。
- 在数学 benchmark 上相较同规模模型取得明显增益。
- 方法层面突出 `Group Relative Policy Optimization`，为后续 reasoning RL 路线提供了实证基础。

## Problem Setting

- 目标问题:
  - 如何在开源中等参数模型上显著提升数学推理能力。
- 核心挑战:
  - 数学任务需要长程推理与严格正确性，普通 SFT 容易在“看起来合理”处失败。

## Architecture

- 主干架构:
  - 延续主流 decoder-only Transformer。
- 贡献重点:
  - 不是新 block 结构，而是数据与后训练策略。

## Data and Pre-training

- 数学语料构建是基础，强调质量与领域覆盖。
- 公开信息表明其数据工程对能力上限影响很大，但完整细节未全部公开。

## Post-training and Alignment

- 训练流程可概括为:
  - 数学 SFT 预热。
  - 基于可验证奖励的 RL 强化（GRPO）。

### GRPO 目标直觉

```text
adv_i = r_i - mean(r_group)
loss ~ - E[ min(ratio_i * adv_i, clip(ratio_i)*adv_i) ]
```

- 重点是“组内相对比较”，减少绝对奖励标定难度。
- 这在数学可验证任务上尤其有效，因为正确性信号更清晰。

### 流程图（重绘）

```mermaid
flowchart LR
    A["Base Model"] --> B["Math SFT"]
    B --> C["Group Sampling"]
    C --> D["Rule-based Verification Reward"]
    D --> E["GRPO Update"]
    E --> F["Math Reasoning Model"]
```

## Evaluation

- 报告在数学 benchmark（如 GSM8K、MATH 等）上展示了显著改进趋势。
- 阅读结论时应关注:
  - 是否是 `pass@1` 还是 `pass@k`。
  - 是否使用了外部工具或采样增强。

## Engineering Takeaways

- 可验证奖励是 reasoning RL 的强信号来源。
- 组内相对优化降低了 value function 依赖，有利于训练稳定性。
- 数学能力提升依赖“数据 + RL”组合，而非单点 trick。

## What Is Actually Worth Learning

- 值得抄作业:
  - 用可验证任务优先打通 RL 管线。
- 工程折中:
  - 过度优化数学任务可能牺牲通用对话体验。
- 难复用:
  - 大规模高质量数学数据清洗与验证系统。

## Cross-References

- 相关模型:
  - [DeepSeek-R1](deepseek_r1.md)
  - [DeepSeek-V3](deepseek_v3.md)
- 相关论文:
  - [GRPO](../../papers/alignment/grpo.md)
  - [PPO](../../papers/alignment/ppo.md)
  - [DPO](../../papers/alignment/dpo.md)
- 相关专题:
  - [Reasoning RL](../../topics/reasoning_rl.md)
  - [Post-training](../../topics/post_training.md)

## Open Questions

- 数学专项 RL 收益向通用复杂推理任务迁移的边界在哪里。
- 奖励设计中“格式奖励 vs 正确性奖励”的最优平衡如何选。

## References

- Primary source:
  - [DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models (arXiv:2402.03300)](https://arxiv.org/abs/2402.03300)
- Related reading:
  - [DeepSeek-R1 (arXiv:2501.12948)](https://arxiv.org/abs/2501.12948)

## Review Checklist

- [x] 关键事实已核查
- [x] 术语和缩写已统一
- [x] 横向对比没有偷换结论
- [x] 已补齐主要链接
