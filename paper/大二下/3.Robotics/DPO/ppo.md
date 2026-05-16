---
title: "Direct Preference Optimization: Your Language Model is Secretly a Reward Model"
citekey: ""
doi: "10.48550/arXiv.2305.18290"
year: 2024
journal: ""
created: 2025-07-17
tags: [zotero, paper-note]
---

# PPO（Proximal Policy Optimization）详解

## 一、PPO 是什么？

PPO（Proximal Policy Optimization）是一种**强化学习算法**，由 OpenAI 在 2017 年提出。在 RLHF 的上下文中，PPO 是**阶段 2（RL 优化阶段）** 的标准算法，用于微调语言模型以最大化奖励模型的评分，同时不偏离参考策略太远。

## 二、为什么 RLHF 需要 PPO？

语言模型生成文本是**离散的**——模型输出的是一个个 token（词元），而不是连续值。这意味着：

1. **不可微问题**：奖励模型 $r_\phi(x, y)$ 的输入是离散的文本 $y$，无法直接对语言模型参数 $\theta$ 求导
2. **解决方案**：使用**策略梯度（Policy Gradient）** 方法，通过采样来估计梯度

PPO 正是策略梯度方法中最流行的一种。

## 三、PPO 在 RLHF 中的优化目标

RLHF 的 RL 阶段目标函数（论文 Eq. 3）：

$$\max_{\pi_\theta} \mathbb{E}_{x\sim D, y\sim\pi_\theta(y|x)} \left[ r_\phi(x, y) \right] - \beta \cdot D_{KL}\left( \pi_\theta(y|x) \parallel \pi_{\text{ref}}(y|x) \right)$$

其中：
- $r_\phi(x, y)$ 是阶段 1 训练好的奖励模型
- $\pi_\theta$ 是当前正在优化的语言模型策略
- $\pi_{\text{ref}}$ 是参考策略（初始 SFT 模型）
- $\beta$ 控制 KL 散度惩罚的强度

## 四、PPO 的核心机制

### 4.1 重要性采样（Importance Sampling）

PPO 使用**重要性采样比率**来复用旧策略采样的数据：

$$r_t(\theta) = \frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{\text{old}}}(a_t|s_t)}$$

在语言模型语境中，$a_t$ 是生成的 token，$s_t$ 是已生成的上下文。

### 4.2 PPO 的裁剪目标（Clipped Objective）

PPO 的核心创新是**裁剪（clipping）**，防止更新步长过大导致训练崩溃：

$$L^{CLIP}(\theta) = \mathbb{E}_t \left[ \min\left( r_t(\theta) \hat{A}_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t \right) \right]$$

其中：
- $\hat{A}_t$ 是**优势函数**（Advantage Function）的估计值，衡量当前动作相对于平均水平的优势
- $\epsilon$ 是裁剪阈值（通常 0.2）
- $\text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)$ 将比率限制在 $[1-\epsilon, 1+\epsilon]$ 范围内

**裁剪的作用：**
- 当 $r_t(\theta)$ 超出 $[1-\epsilon, 1+\epsilon]$ 范围时，梯度被裁剪为 0
- 防止单次更新步长过大，保证训练稳定性

### 4.3 优势函数的估计

PPO 使用**广义优势估计（GAE, Generalized Advantage Estimation）**：

$$\hat{A}_t = \sum_{l=0}^{\infty} (\gamma\lambda)^l \delta_{t+l}$$

其中 $\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)$ 是 TD 误差，$V(s)$ 是**价值函数**（Value Function）的估计。

在 RLHF 中，这需要一个额外的**价值网络**（通常与策略网络共享部分参数），增加了模型复杂度。

## 五、PPO 在 RLHF 中的完整训练流程

```
每个 PPO 迭代:
  1. 从当前策略 π_θ 采样一批回答 y ~ π_θ(y|x)
  2. 用奖励模型 r_φ 给每个回答打分
  3. 计算 KL 散度惩罚（与 π_ref 比较）
  4. 计算优势函数 A_t（需要价值网络 V_ψ）
  5. 计算 PPO 裁剪损失
  6. 更新策略参数 θ
  7. 更新价值网络参数 ψ
```

## 六、PPO 的痛点（为什么 DPO 要替代它）

论文在 Section 3 中指出了 PPO 的多个问题：

> *"While RLHF produces proficient models, its procedure is **notably unstable**, requiring significant hyperparameter tuning, and computationally expensive to train."*

具体问题包括：

| 问题 | 说明 |
|------|------|
| **训练不稳定** | PPO 对超参数（学习率、裁剪阈值、KL 系数等）非常敏感 |
| **需要在线采样** | 每个 PPO 迭代都需要从当前策略采样新回答，计算成本高 |
| **需要价值网络** | 需要额外训练一个价值函数 $V_\psi$，增加模型规模和复杂度 |
| **高方差梯度** | 策略梯度方法的固有缺陷，需要大量样本来降低方差 |
| **奖励模型误差传播** | 阶段 1 奖励模型的误差会在 PPO 训练中被放大 |

## 七、DPO 如何绕过 PPO

DPO 通过重参数化，**完全绕过了 PPO**：

| 方面 | PPO (RLHF) | DPO |
|------|-----------|-----|
| 是否需要奖励模型 | ✅ 是 | ❌ 否 |
| 是否需要在线采样 | ✅ 是 | ❌ 否（完全离线） |
| 是否需要价值网络 | ✅ 是 | ❌ 否 |
| 损失函数 | 复杂的裁剪 + KL + 价值损失 | 简单的二元交叉熵 |
| 超参数数量 | 多 | 少（主要是 $\beta$） |
| 训练稳定性 | 不稳定 | 稳定 |

## 八、总结

> **PPO 是传统 RLHF 中用于优化语言模型的强化学习算法，它通过重要性采样和裁剪机制来稳定策略更新，但需要在线采样、额外价值网络和大量超参数调优——DPO 通过重参数化技巧完全绕过了 PPO，将整个 RLHF 流程简化为一个简单的分类损失。**

## 参考文献

Rafailov, R., Sharma, A., Mitchell, E., Ermon, S., Manning, C. D., & Finn, C. (2024). *Direct Preference Optimization: Your Language Model is Secretly a Reward Model*. arXiv. https://doi.org/10.48550/arXiv.2305.18290

---

Written by LLM-for-Zotero.
