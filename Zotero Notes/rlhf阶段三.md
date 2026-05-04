---
title: "Direct Preference Optimization: Your Language Model is Secretly a Reward Model"
citekey: ""
doi: "10.48550/arXiv.2305.18290"
year: 2024
journal: ""
created: 2025-07-17
tags: [zotero, paper-note]
---

# RLHF 中的 RL Optimization（PPO 阶段）详解

## 一、RL Optimization 在 RLHF 中的位置

RLHF 的完整三阶段流程：

```
阶段 1: SFT                   阶段 2: 奖励建模                    阶段 3: RL 优化
╔═══════════════════╗    ╔════════════════════════════╗    ╔═══════════════════════════╗
║ 预训练模型         ║    ║ π^SFT 采样回答对           ║    ║ 奖励模型 r_φ(x, y)        ║
║   ↓               ║    ║   ↓                       ║    ║   ↓                      ║
║ SFT 微调           ║ →  ║ 人类标注偏好 (y_w ≻ y_l)  ║ →  ║ PPO 优化策略 π_θ          ║
║   ↓               ║    ║   ↓                       ║    ║   ↓                      ║
║ π^SFT = π_ref     ║    ║ 训练奖励模型 r_φ           ║    ║ π_θ (最终对齐策略)        ║
╚═══════════════════╝    ╚════════════════════════════╝    ╚═══════════════════════════╝
```

论文原文（Rafailov et al., 2024, Section 3）：

> *"RL Fine-Tuning Phase: During the RL phase, the learned reward function is used to provide feedback to the language model."*

## 二、RL 优化的核心目标函数

### 2.1 KL 约束的奖励最大化

论文原文（Eq. 3）：

> *"Following prior works, the optimization is formulated as:*

$$\max_{\pi_\theta} \mathbb{E}_{x \sim D, y \sim \pi_\theta(y|x)} \left[ r_\phi(x, y) \right] - \beta \, D_{KL}\left( \pi_\theta(y|x) \parallel \pi_{\text{ref}}(y|x) \right)$$

其中：
- $\pi_\theta$ = 当前正在优化的语言模型策略（policy）
- $\pi_{\text{ref}}$ = 参考策略（reference policy），即**初始的 SFT 模型** $\pi^{\text{SFT}}$
- $r_\phi(x, y)$ = 阶段 2 训练好的奖励模型
- $\beta$ = 控制偏离参考策略程度的超参数
- $D_{KL}$ = KL 散度（Kullback-Leibler divergence）

### 2.2 目标函数的两项解读

**第一项：奖励期望**

$$\mathbb{E}_{x \sim D, y \sim \pi_\theta(y|x)} [r_\phi(x, y)]$$

- 从当前策略 $\pi_\theta$ 中采样回答 $y$
- 用奖励模型 $r_\phi$ 给回答打分
- 目标是让策略生成**高奖励的回答**

**第二项：KL 散度约束**

$$-\beta \, D_{KL}(\pi_\theta(y|x) \parallel \pi_{\text{ref}}(y|x))$$

- 惩罚策略 $\pi_\theta$ 偏离参考策略 $\pi_{\text{ref}}$（即 SFT 模型）
- $\beta$ 越大，约束越强，策略变化越小

### 2.3 为什么需要 KL 约束？

论文原文：

> *"The added constraint is important, as it prevents the model from deviating too far from the distribution on which the reward model is accurate, as well as maintaining the generation diversity and preventing mode-collapse to single high-reward answers."*

**三个关键作用：**

1. **保持奖励模型的准确性** — 奖励模型只在 $\pi^{\text{SFT}}$ 的分布附近是准确的，偏离太远会导致奖励模型给出不可靠的评分
2. **维持生成多样性** — 防止模型坍缩到只生成少数几个高奖励的回答
3. **防止模式坍缩（mode-collapse）** — 避免模型只学会一种"套路"来获取高奖励

## 三、为什么需要强化学习？

### 3.1 不可微性

论文原文：

> *"Due to the discrete nature of language generation, this objective is not differentiable and is typically optimized with reinforcement learning."*

**核心问题：** 语言生成是离散的 token 采样过程。目标函数中的 $\mathbb{E}_{y \sim \pi_\theta(y|x)}[r_\phi(x, y)]$ 对 $\theta$ 的梯度无法直接计算，因为采样操作不可微。

### 3.2 标准解决方案：PPO

论文原文：

> *"The standard approach has been to construct the reward function $r(x, y) = r_\phi(x, y) - \beta(\log \pi_\theta(y|x) - \log \pi_{\text{ref}}(y|x))$, and maximize using PPO."*

PPO（Proximal Policy Optimization）通过以下方式解决不可微问题：
1. 使用**策略梯度**（policy gradient）来估计梯度
2. 引入**裁剪机制**（clipping）来稳定训练
3. 使用**价值函数**（value function）来降低方差

## 四、PPO 的数学原理与公式推导

### 4.1 从 KL 约束到奖励塑造（Reward Shaping）

论文中提到的标准做法是将 KL 散度约束**融入奖励函数本身**，构造一个"修正后的奖励"：

$$r(x, y) = r_\phi(x, y) - \beta(\log \pi_\theta(y|x) - \log \pi_{\text{ref}}(y|x))$$

**推导过程：**

原始目标：

$$\max_{\pi_\theta} \mathbb{E}_{x \sim D, y \sim \pi_\theta} [r_\phi(x, y)] - \beta D_{KL}(\pi_\theta \parallel \pi_{\text{ref}})$$

展开 KL 散度：

$$D_{KL}(\pi_\theta \parallel \pi_{\text{ref}}) = \mathbb{E}_{y \sim \pi_\theta} \left[ \log \frac{\pi_\theta(y|x)}{\pi_{\text{ref}}(y|x)} \right]$$

代入：

$$\max_{\pi_\theta} \mathbb{E}_{x \sim D, y \sim \pi_\theta} \left[ r_\phi(x, y) - \beta \log \frac{\pi_\theta(y|x)}{\pi_{\text{ref}}(y|x)} \right]$$

定义**修正奖励**：

$$r(x, y) = r_\phi(x, y) - \beta(\log \pi_\theta(y|x) - \log \pi_{\text{ref}}(y|x))$$

于是目标简化为：

$$\max_{\pi_\theta} \mathbb{E}_{x \sim D, y \sim \pi_\theta} [r(x, y)]$$

### 4.2 PPO 的核心机制

PPO 使用**重要性采样**（importance sampling）来利用旧策略 $\pi_{\theta_{\text{old}}}$ 采样的数据更新当前策略 $\pi_\theta$。

**重要性采样比率：**

$$r_t(\theta) = \frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{\text{old}}}(a_t|s_t)}$$

在语言模型语境中，$a_t$ 是生成的 token，$s_t$ 是当前的上下文（prompt + 已生成的 tokens）。

**PPO 的裁剪目标函数：**

$$L^{\text{CLIP}}(\theta) = \mathbb{E}_t \left[ \min\left( r_t(\theta) \hat{A}_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t \right) \right]$$

其中：
- $\hat{A}_t$ = 优势函数估计（advantage estimate）
- $\epsilon$ = 裁剪范围（通常 0.2）
- $\text{clip}$ 将比率限制在 $[1-\epsilon, 1+\epsilon]$ 内

**裁剪的作用：** 当 $r_t(\theta)$ 超出范围时，梯度被裁剪，防止单次更新步长过大导致策略崩溃。

### 4.3 优势函数估计

PPO 使用**广义优势估计**（GAE, Generalized Advantage Estimation）：

$$\hat{A}_t = \delta_t + (\gamma\lambda)\delta_{t+1} + (\gamma\lambda)^2\delta_{t+2} + ...$$

其中：
- $\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)$ = TD 误差
- $V(s_t)$ = 价值函数（critic），估计状态 $s_t$ 的期望回报
- $\gamma$ = 折扣因子
- $\lambda$ = GAE 参数

### 4.4 PPO 在 RLHF 中的完整损失函数

PPO 在 RLHF 中的总损失包含三部分：

$$L^{\text{PPO}}(\theta) = L^{\text{CLIP}}(\theta) - c_1 L^{\text{VF}}(\theta) + c_2 S[\pi_\theta]$$

其中：
- $L^{\text{CLIP}}(\theta)$ = 策略损失（裁剪后的策略梯度）
- $L^{\text{VF}}(\theta) = \mathbb{E}_t[(V_\theta(s_t) - V_t^{\text{target}})^2]$ = 价值函数损失（MSE）
- $S[\pi_\theta]$ = 策略熵奖励（鼓励探索）
- $c_1, c_2$ = 各项的权重系数

## 五、RLHF 中 PPO 的完整训练流程

### 5.1 训练循环

```
对于每个 PPO 迭代：
  1. 从提示集 D 中采样一批提示 x
  2. 从当前策略 π_θ 中采样回答 y ~ π_θ(y|x)
  3. 用奖励模型 r_φ 计算每个回答的奖励 r_φ(x, y)
  4. 计算修正奖励：r(x,y) = r_φ(x,y) - β(log π_θ(y|x) - log π_ref(y|x))
  5. 用价值函数 V 计算优势估计 Â
  6. 计算 PPO 裁剪损失并更新 π_θ
  7. 更新价值函数 V 以拟合实际回报
  8. 重复直到收敛
```

### 5.2 初始化

论文原文：

> *"In practice, the language model policy $\pi_\theta$ is also initialized to $\pi^{\text{SFT}}$."*

- 策略 $\pi_\theta$ 初始化为 SFT 模型 $\pi^{\text{SFT}}$
- 参考策略 $\pi_{\text{ref}}$ 也固定为 $\pi^{\text{SFT}}$
- 这意味着训练开始时 $\pi_\theta = \pi_{\text{ref}}$，KL 散度为 0

## 六、PPO 在 RLHF 中的挑战

### 6.1 计算复杂度

论文指出 PPO 在 RLHF 中的主要问题：

> *"The RLHF pipeline is considerably more complex than supervised learning, involving training multiple LMs and sampling from the LM policy in the loop of training, incurring significant computational costs."*

**具体开销：**
- 需要同时维护策略网络 $\pi_\theta$ 和价值网络 $V$
- 每个 PPO 步骤都需要从策略中采样（自回归生成，非常慢）
- 需要计算每个 token 的 log 概率
- 需要存储旧策略的 log 概率用于重要性采样

### 6.2 训练不稳定性

论文在 Section 5.2 中分析了 PPO 的不稳定性来源：

> *"We can interpret the normalization term in $f(r_\phi, \pi_{\text{ref}}, \beta)$ as the soft value function of the reference policy $\pi_{\text{ref}}$. While this term does not affect the optimal solution, without it, the policy gradient of the objective could have high variance, making learning unstable."*

**核心问题：** 配分函数 $Z(x) = \sum_y \pi_{\text{ref}}(y|x) \exp(\frac{1}{\beta} r_\phi(x, y))$ 难以计算，导致策略梯度方差大。

**现有解决方案：**
- 使用学习到的价值函数来估计归一化项
- 使用人类完成基线（human completion baseline）作为蒙特卡洛估计
- 奖励归一化

### 6.3 超参数敏感性

PPO 需要调优大量超参数：
- $\beta$（KL 惩罚系数）
- 学习率
- 裁剪范围 $\epsilon$
- GAE 参数 $\lambda$
- 折扣因子 $\gamma$
- 价值函数损失权重 $c_1$
- 熵奖励权重 $c_2$
- 批次大小
- PPO epochs 数

## 七、PPO 与 DPO 的对比

论文的核心贡献正是**用 DPO 替代 PPO**：

| 方面 | PPO（传统 RLHF） | DPO |
|------|-----------------|-----|
| **训练流程** | 奖励建模 → PPO 优化（两阶段） | 一步直接优化（单阶段） |
| **梯度来源** | 策略梯度 + 重要性采样 | 二元交叉熵的解析梯度 |
| **采样需求** | 训练中反复从策略采样 | 仅需静态偏好数据集 |
| **价值函数** | 需要训练 critic 网络 | 不需要 |
| **超参数** | 多（$\beta, \epsilon, \gamma, \lambda, c_1, c_2$ 等） | 少（仅 $\beta$） |
| **稳定性** | 不稳定，需裁剪和归一化 | 稳定，标准分类训练 |
| **计算成本** | 高 | 低 |

## 八、完整数学流程总结

### 8.1 输入 → 输出

| | 内容 |
|------|------|
| **输入** | 奖励模型 $r_\phi(x, y)$ + SFT 模型 $\pi^{\text{SFT}} = \pi_{\text{ref}}$ |
| **目标函数** | $\max_{\pi_\theta} \mathbb{E}_{x\sim D, y\sim\pi_\theta}[r_\phi(x, y)] - \beta D_{KL}(\pi_\theta \parallel \pi_{\text{ref}})$ |
| **修正奖励** | $r(x, y) = r_\phi(x, y) - \beta(\log \pi_\theta(y\|x) - \log \pi_{\text{ref}}(y\|x))$ |
| **优化算法** | PPO（策略梯度 + 重要性采样 + 裁剪） |
| **输出** | 对齐后的语言模型策略 $\pi_\theta$ |

### 8.2 核心公式一览

| 公式 | 含义 |
|------|------|
| $\max_{\pi_\theta} \mathbb{E}_{x\sim D, y\sim\pi_\theta}[r_\phi(x, y)] - \beta D_{KL}(\pi_\theta \parallel \pi_{\text{ref}})$ | KL 约束的奖励最大化目标 |
| $r(x, y) = r_\phi(x, y) - \beta(\log \pi_\theta(y\|x) - \log \pi_{\text{ref}}(y\|x))$ | 将 KL 约束融入奖励 |
| $r_t(\theta) = \frac{\pi_\theta(a_t\|s_t)}{\pi_{\theta_{\text{old}}}(a_t\|s_t)}$ | PPO 重要性采样比率 |
| $L^{\text{CLIP}}(\theta) = \mathbb{E}_t[\min(r_t(\theta)\hat{A}_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t)]$ | PPO 裁剪目标 |
| $\hat{A}_t = \delta_t + (\gamma\lambda)\delta_{t+1} + (\gamma\lambda)^2\delta_{t+2} + ...$ | 广义优势估计（GAE） |

## 九、一句话总结

> **RL Optimization（PPO 阶段）= 在 KL 散度约束下，通过 PPO 算法（策略梯度 + 重要性采样 + 裁剪）最大化奖励模型 $r_\phi$ 给出的期望奖励，将语言模型策略 $\pi_\theta$ 从 SFT 模型 $\pi^{\text{SFT}}$ 优化为与人类偏好对齐的最终模型，同时通过 $\beta$ 控制偏离程度以防止模式坍缩和奖励模型失效。**

## References

Rafailov, R., Sharma, A., Mitchell, E., Ermon, S., Manning, C. D., & Finn, C. (2024). *Direct Preference Optimization: Your Language Model is Secretly a Reward Model*. arXiv. DOI: 10.48550/arXiv.2305.18290.

---

Written by LLM-for-Zotero.
