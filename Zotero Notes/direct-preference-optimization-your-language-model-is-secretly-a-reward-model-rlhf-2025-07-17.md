
# Direct Preference Optimization: Your Language Model is Secretly a Reward Model

## Summary
RLHF（Reinforcement Learning from Human Feedback，基于人类反馈的强化学习）是一种将人类偏好融入语言模型训练的技术框架。其核心目标是让语言模型的行为与人类偏好对齐——使模型更有帮助、更无害、更诚实。

## Key Findings

### 传统 RLHF 的两阶段流程

**阶段 1：训练奖励模型（Reward Model）**

1. **收集偏好数据**：让人类标注员比较模型对同一提示的不同回答，标记哪个更好（$y_w$）和哪个更差（$y_l$）
2. **训练奖励模型**：使用 Bradley-Terry 模型来建模人类偏好：

$$p^*(y_1 \succ y_2 | x) = \frac{\exp(r^*(x, y_1))}{\exp(r^*(x, y_1)) + \exp(r^*(x, y_2))}$$

奖励模型 $r_\phi(x, y)$ 通过最大似然估计训练，损失函数为：

$$L_R(r_\phi, D) = -\mathbb{E}_{(x,y_w,y_l)\sim D} \left[ \log \sigma(r_\phi(x, y_w) - r_\phi(x, y_l)) \right]$$

**阶段 2：强化学习微调**

用学到的奖励函数 $r_\phi$ 来优化语言模型策略 $\pi_\theta$：

$$\max_{\pi_\theta} \mathbb{E}_{x\sim D, y\sim\pi_\theta(y|x)} \left[ r_\phi(x, y) \right] - \beta \cdot D_{KL}\left( \pi_\theta(y|x) \parallel \pi_{\text{ref}}(y|x) \right)$$

其中：
- 第一项最大化奖励模型的评分
- 第二项（KL 散度）防止模型偏离初始的 SFT 模型太远，保持生成多样性
- $\beta$ 控制两者的平衡

这个优化目标通常用 **PPO（Proximal Policy Optimization）** 算法来求解。

### RLHF 的主要痛点

1. **流程复杂**：需要先训练奖励模型，再用 RL 微调，两阶段相互依赖
2. **训练不稳定**：PPO 需要大量超参数调优（学习率、裁剪范围、KL 系数等）
3. **计算成本高**：RL 训练需要从当前策略中反复采样，计算开销大
4. **实现难度大**：需要同时维护策略网络、价值网络、奖励模型等多个组件

### DPO 的改进

DPO 的核心洞察是：**语言模型本身就可以"秘密地"充当奖励模型**。通过数学重参数化，将奖励函数表示为策略比率：

$$r(x, y) = \beta \log\frac{\pi^*(y|x)}{\pi_{\text{ref}}(y|x)} + \beta \log Z(x)$$

代入 Bradley-Terry 模型后，配分函数 $Z(x)$ 抵消，得到直接优化策略的损失函数：

$$L_{DPO}(\pi_\theta; \pi_{\text{ref}}) = -\mathbb{E}_{(x,y_w,y_l)\sim D} \left[ \log \sigma\left( \beta \log\frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta \log\frac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)} \right) \right]$$

这样就完全不需要训练奖励模型和 RL 了——只需要一个简单的二元交叉熵损失。

## Methodology

### DPO vs RLHF（PPO）对比

| 方面 | RLHF (PPO) | DPO |
|------|-----------|-----|
| **训练流程** | ①训练奖励模型 → ②RL微调（两阶段） | 一步直接优化（单阶段） |
| **计算成本** | 高：需要奖励模型 + RL采样 + 价值函数 | 低：仅需一个分类损失 |
| **稳定性** | 不稳定：需要大量超参数调优 | 稳定：几乎无需调参 |
| **数学复杂度** | 复杂：策略梯度、优势函数、裁剪 | 简单：二元交叉熵 |
| **Reward-KL效率** | 较低 | 更高（严格支配PPO） |
| **温度鲁棒性** | 差 | 好 |
| **分布外泛化** | 一般 | 更好 |

## My Notes

RLHF 是当前大语言模型对齐技术的核心框架。DPO 论文通过巧妙的数学重参数化，揭示了语言模型与奖励模型之间的深层联系——"你的语言模型秘密地就是一个奖励模型"。这一发现将原本复杂的两阶段 RLHF 流程简化为一个简单的分类损失，大幅降低了计算复杂度和实现难度，同时保持了理论上的完整性和表示能力。

## References
Rafailov, R., Sharma, A., Mitchell, E., Ermon, S., Manning, C. D., & Finn, C. (2024). *Direct Preference Optimization: Your Language Model is Secretly a Reward Model*. arXiv:2305.18290 [cs]. https://doi.org/10.48550/arXiv.2305.18290

---

Written by LLM-for-Zotero.
