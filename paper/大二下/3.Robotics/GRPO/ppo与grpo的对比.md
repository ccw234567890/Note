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
本文详细对比了 PPO（Proximal Policy Optimization）和 GRPO（Group Relative Policy Optimization）两种强化学习算法在 LLM 数学推理微调中的应用。PPO 是传统 RLHF 的标准算法，需要 Actor-Critic 架构（策略模型 + 价值模型）；GRPO 是 DeepSeekMath 提出的改进变体，完全去掉了价值模型，改用组内归一化计算 Advantage。

## Key Findings

### 一、核心架构差异

| 维度 | PPO | GRPO |
|------|-----|------|
| **架构** | Actor-Critic（策略 + 价值模型） | 仅策略模型 |
| **价值模型** | ✅ 需要，与策略等大 | ❌ 不需要 |
| **Advantage 计算** | GAE：$A_t = \sum(\gamma\lambda)^l\delta_{t+l}$ | 组内归一化：$\hat{A}_t = (r_i - \mu)/\sigma$ |
| **采样方式** | 每次迭代采 **1 个**输出 | 每次迭代采 **G 个**输出（一组） |
| **KL 处理** | 混入每个 token 的奖励中 | 直接加入损失函数 |
| **显存需求** | 高（策略 + 价值 + 奖励 + 参考 ≈ 4×模型） | 低（策略 + 奖励 + 参考 ≈ 3×模型） |

### 二、目标函数对比

**PPO 目标函数：**

$$J_{\text{PPO}}(\theta) = \mathbb{E}_{q, o \sim \pi_{\theta_{\text{old}}}} \left[ \frac{1}{|o|} \sum_{t=1}^{|o|} \min\left( \frac{\pi_\theta(o_t)}{\pi_{\theta_{\text{old}}}(o_t)} A_t,\; \text{clip}\left( \frac{\pi_\theta(o_t)}{\pi_{\theta_{\text{old}}}(o_t)}, 1-\varepsilon, 1+\varepsilon \right) A_t \right) \right]$$

其中 $A_t$ 来自 GAE，依赖价值模型 $V_\psi$。

**GRPO 目标函数：**

$$J_{\text{GRPO}}(\theta) = \mathbb{E}_{q, \{o_i\}_{i=1}^G \sim \pi_{\theta_{\text{old}}}} \left[ \frac{1}{G} \sum_{i=1}^G \frac{1}{|o_i|} \sum_{t=1}^{|o_i|} \left( \min\left( \frac{\pi_\theta(o_{i,t})}{\pi_{\theta_{\text{old}}}(o_{i,t})} \hat{A}_{i,t},\; \text{clip}(\cdots) \hat{A}_{i,t} \right) - \beta D_{\text{KL}}(\pi_\theta || \pi_{\text{ref}}) \right) \right]$$

其中 $\hat{A}_{i,t}$ 来自组内归一化，**不依赖任何价值模型**。

### 三、KL 散度处理方式

- **PPO**：将 KL 惩罚混入每个 token 的即时奖励 $r_t = r_\phi(q, o_{\leq t}) - \beta \log\frac{\pi_\theta}{\pi_{\text{ref}}}$，再进入 GAE 计算 Advantage
- **GRPO**：将 KL 散度直接加入损失函数，使用 Schulman (2020) 的无偏估计器，避免干扰 Advantage 计算

### 四、梯度系数对比

- **PPO**：$\text{GC}_{\text{PPO}} = A_t$（来自 GAE，依赖价值模型）
- **GRPO**：$\text{GC}_{\text{GRPO}} = \hat{A}_{i,t} + \beta\left( \frac{\pi_{\text{ref}}(o_t)}{\pi_\theta(o_t)} - 1 \right)$（来自组内归一化，不依赖价值模型）

### 五、GRPO 的核心优势

1. **组内比较 vs 绝对评分**：奖励模型本身就是通过比较同一问题的不同输出来训练的，GRPO 的组内 Advantage 与奖励模型的训练范式天然一致
2. **差异化梯度系数**：好的输出获得更大的正梯度，差的输出获得负梯度（被惩罚），而非 RFT 的 0/1 二值化
3. **显存节省约 25%**：去掉价值模型，可在同样硬件上训练更大模型或使用更大 batch size
4. **过程监督的自然扩展**：GRPO+PS 可对每个推理步骤计算 Advantage，无需为每个步骤训练价值模型

## Methodology

PPO 使用重要性采样比率 $r_t(\theta) = \pi_\theta(a_t|s_t)/\pi_{\theta_{\text{old}}}(a_t|s_t)$ 复用旧策略数据，通过裁剪（clipping）防止更新步长过大。GRPO 在此基础上，对每个问题采样 G 个输出，在组内进行归一化得到 Advantage，完全去掉价值模型。

## My Notes

PPO 是通用 RL 算法，适用于游戏、机器人等连续控制场景；GRPO 专为 LLM 文本生成设计，利用"奖励模型只在最后 token 打分"的特性，用组内比较替代价值模型，更简单、更省资源、更稳定。

## References

Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X., Zhang, H., Zhang, M., Li, Y. K., Wu, Y., & Guo, D. (2024). *DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models*. arXiv. https://doi.org/10.48550/arXiv.2402.03300

---

Written by LLM-for-Zotero.
