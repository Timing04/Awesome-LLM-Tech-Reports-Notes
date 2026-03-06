---
title: Proximal Policy Optimization Algorithms
type: method_paper
category: alignment
status: ai_draft
source_status: verified
release_date: 2017-07-20
topics:
  - reinforcement_learning
  - policy_optimization
  - on_policy
source:
  kind: arxiv
  ref: "1707.06347"
  official: ""
---

# Proximal Policy Optimization Algorithms

## 3-Minute Summary

- `PPO` 用一个“限制策略更新幅度”的目标函数，解决了经典 policy gradient 容易训练不稳定、超参敏感的问题。
- 它的核心不是追求最强理论最优，而是用 `clipping` 做一个工程上稳定、实现简单、泛化好的近似优化器。
- 在 LLM 训练里，`PPO` 的历史意义是把早期 `RLHF`（尤其是 InstructGPT 路线）变成可执行流程。

## Problem Definition

- 输入:
  - 当前策略 `pi_theta(a|s)`
  - 由旧策略采样得到的轨迹和优势估计 `A_t`
- 输出:
  - 一次或多次 epoch 后更新的策略参数 `theta`
- 优化目标:
  - 最大化策略改进，同时限制新旧策略比值 `r_t(theta)` 偏离过大。
- 与 TRPO 相比:
  - TRPO 用硬 KL 约束 + 二阶近似，理论漂亮但实现复杂。
  - PPO 用一阶优化 + clipped surrogate objective，训练更“傻瓜化”。

## Method

- 核心思想:
  - 不让单步更新太激进。即使某个 batch 的优势估计很大，也要限制它对策略的推动。
- 关键目标函数:
```text
L^CLIP(theta) = E_t[min(r_t(theta) A_t, clip(r_t(theta), 1-eps, 1+eps) A_t)]
```
  - 其中 `r_t(theta) = pi_theta(a_t|s_t) / pi_theta_old(a_t|s_t)`。
  - `eps` 常见取值在 `0.1 ~ 0.2`。
- 算法流程:
  - 用旧策略采样 rollout。
  - 用 GAE 估计优势，计算 value target。
  - 对同一批样本做多轮 minibatch SGD（policy loss + value loss + entropy bonus）。
  - 更新后把当前策略作为下一轮 `old policy`。
- 稳定性细节:
  - `advantage normalization` 常常是必须项。
  - value loss 系数过大时，策略学习会被 critic 拖慢。
  - minibatch epoch 太多时，会出现过拟合 old batch 的问题。

## Why It Works

- 直觉:
  - policy gradient 的痛点是“估计噪声 + 更新过大”。PPO 通过 clip 把灾难性大步更新直接截断。
- 缓解的问题:
  - 相比 REINFORCE，方差更低（借助 advantage / critic）。
  - 相比 vanilla actor-critic，策略崩塌概率更低。
  - 相比 TRPO，工程复杂度显著降低。
- 成功前提:
  - 优势估计不能太差（GAE 参数和 critic 质量关键）。
  - rollout 分布和目标任务分布不能严重错位。
  - reward 设计至少能提供稳定梯度信号。

## Experiments

- 原论文主要覆盖 Atari、MuJoCo、Roboschool 等强化学习基准。
- 对比基线包括 TRPO、A2C 等常见策略优化方法。
- 关键结论:
  - PPO 在多任务上能以更低实现复杂度达到接近或优于 TRPO 的效果。
  - 对超参有一定鲁棒性，但不是“免调参”。
- 对 LLM 的外推价值:
  - 论文本身不是为 LLM 写的，外推成立依赖于“把 token 级生成视作序列决策”这一建模假设。
  - 在大模型后训练里，PPO 更像“可工作的默认 RL optimizer”，不是完整对齐方案。

## Implementation Notes

- 最小实现组件:
  - actor policy
  - value model（可与 policy 部分共享骨干）
  - advantage 估计（通常 GAE）
  - reward 来源（环境奖励或 RM 奖励）
- 常见踩坑:
  - KL 爆炸: policy 太快偏离 reference。
  - reward hacking: 模型学会“骗分”而非真实提升。
  - 长序列 credit assignment 差，导致训练噪声很大。
- 在 LLM 后训练落地:
  - 常见流程是 `SFT -> RM -> PPO`。
  - 实际训练常附加 KL penalty 到 reference model，抑制风格漂移和模式塌缩。
  - 算力成本通常显著高于 DPO/ORPO 这类离线偏好优化。

## Relationship to LLM Practice

- 明确使用/影响路径:
  - InstructGPT 是最经典的 `PPO + RM` 路线。
  - 许多对齐框架（如 TRL）都保留 PPO 作为标准算法。
- 适用位置:
  - 主要用于 post-training，而不是 base model 预训练。
- 在当前 LLM 栈的位置:
  - 如果奖励可学习但难以直接写成离线 pairwise 目标，PPO 仍然有效。
  - 当工程成本敏感且有高质量偏好对时，许多团队会优先 DPO，再按需引入 PPO/GRPO。

## Limitations

- 论文层面假设:
  - on-policy 采样可持续进行，且环境反馈可获得。
- 大规模系统问题:
  - 采样和训练闭环昂贵，吞吐低于纯监督目标。
  - 奖励模型偏差会被策略放大。
  - 多目标对齐（helpfulness/harmlessness/格式）时 reward 设计复杂。
- 不建议直接上 PPO 的场景:
  - 没有稳定 reward 来源。
  - 只有离线偏好数据且算力预算有限。
  - 团队缺少 RL 训练和诊断经验。

## Cross-References

- 相关模型报告:
  - [Llama 3](../../models/llama/llama3.md)
  - [Qwen2](../../models/qwen/qwen2.md)
  - [DeepSeek-R1](../../models/deepseek/deepseek_r1.md)
- 相关论文:
  - InstructGPT / RLHF（条目待补充）
  - [DPO](dpo.md)
  - [GRPO](grpo.md)
- 相关专题:
  - [Post-training](../../topics/post_training.md)
  - [Reasoning RL](../../topics/reasoning_rl.md)

## References

- Primary source:
  - [Proximal Policy Optimization Algorithms (arXiv:1707.06347)](https://arxiv.org/abs/1707.06347)
- Follow-up work:
  - [InstructGPT (arXiv:2203.02155)](https://arxiv.org/abs/2203.02155)
  - [Direct Preference Optimization (arXiv:2305.18290)](https://arxiv.org/abs/2305.18290)
  - [DeepSeekMath / GRPO (arXiv:2402.03300)](https://arxiv.org/abs/2402.03300)
- Good implementation references:
  - [Hugging Face TRL PPOTrainer](https://huggingface.co/docs/trl/main/en/ppo_trainer)
  - [OpenAI Spinning Up: PPO](https://spinningup.openai.com/en/latest/algorithms/ppo.html)

## Review Checklist

- [x] 方法定义已核查
- [x] 关键公式没有抄错
- [x] 实验结论没有被过度解释
- [x] 已说明与主流 LLM 实践的关系
