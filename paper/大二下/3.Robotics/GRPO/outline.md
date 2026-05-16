---
title: "DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models"
citekey: ""
doi: "10.48550/arXiv.2402.03300"
year: 2024
journal: ""
created: 2025-07-18
tags: [zotero, paper-note]
---

# DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models

## Summary
GRPO（Group Relative Policy Optimization）是一种去除了价值模型（Critic）的 PPO 变体，通过组内相对比较来计算 Advantage，大幅降低显存开销的同时提升了数学推理能力。

## Key Findings
- GRPO 完全抛弃价值模型（Critic），仅保留策略模型 + 奖励模型 + 参考模型
- 组内归一化 Advantage 计算方式与奖励模型的 pairwise 训练范式天然一致
- 省去一个与策略模型等大的价值模型，训练资源大幅降低
- DeepSeekMath 7B 在 MATH 上达到 51.7%（Top-1），逼近 Gemini-Ultra 和 GPT-4

## Methodology
### 背景：PPO 的问题
- PPO 是 Actor-Critic 算法，需要策略模型 + 价值模型
- 价值模型与策略模型规模相当，显存消耗巨大
- LLM 场景中奖励模型只给最后一个 token 打分，价值模型训练困难

### GRPO 核心创新
- **去掉价值模型**：用组内相对比较替代 GAE + Value Model
- **Advantage 计算**：对同一问题采样 G 个输出，组内归一化奖励：
  $$\hat{A}_{i,t} = \frac{r_i - \text{mean}(\mathbf{r})}{\text{std}(\mathbf{r})}$$
- **Process Supervision**：每个步骤的 Advantage 等于后续所有步骤的归一化奖励之和
- **KL 正则化**：直接加到损失中，使用无偏估计器：
  $$D_{\text{KL}}(\pi_\theta || \pi_{\text{ref}}) = \frac{\pi_{\text{ref}}}{\pi_\theta} - \log\frac{\pi_{\text{ref}}}{\pi_\theta} - 1$$

### 目标函数
$$J_{\text{GRPO}}(\theta) = \mathbb{E}\left[ \frac{1}{G} \sum_{i=1}^G \frac{1}{|o_i|} \sum_{t=1}^{|o_i|} \left( \min\left( \frac{\pi_\theta}{\pi_{\theta_{\text{old}}}} \hat{A}_{i,t},\; \text{clip}(\cdots) \hat{A}_{i,t} \right) - \beta D_{\text{KL}}(\pi_\theta || \pi_{\text{ref}}) \right) \right]$$

### 梯度系数对比
| 方法 | 梯度系数 | 需要价值模型？ |
|------|---------|:------------:|
| SFT | $1$ | ❌ |
| RFT | $I(o) \in \{0,1\}$ | ❌ |
| DPO | $\sigma(\beta\log\frac{\pi_\theta(o^-)}{\pi_{\text{ref}}(o^-)} - \beta\log\frac{\pi_\theta(o^+)}{\pi_{\text{ref}}(o^+)})$ | ❌ |
| PPO | $A_t$（GAE + 价值模型） | ✅ |
| GRPO | $\hat{A}_{i,t} + \beta(\frac{\pi_{\text{ref}}}{\pi_\theta} - 1)$（组内归一化） | ❌ |

### 训练配置
- 策略模型学习率：$1 \times 10^{-6}$
- KL 系数 $\beta$：$0.04$
- 每组采样数 $G$：$64$
- 最大序列长度：$1024$

## My Notes
GRPO 的核心洞察在于：奖励模型本身就是通过比较同一问题的不同输出来训练的（pairwise preference data），因此组内 Advantage 计算方式与奖励模型的训练范式天然一致。GRPO 的梯度系数是连续值——好的输出获得更大的正梯度，差的输出获得负梯度（被惩罚），这与 RFT 的二值化处理形成鲜明对比。

## References
Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X., Zhang, H., Zhang, M., Li, Y. K., Wu, Y., & Guo, D. (2024). *DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models*. arXiv:2402.03300 [cs]. https://doi.org/10.48550/arXiv.2402.03300

---

Written by LLM-for-Zotero.
