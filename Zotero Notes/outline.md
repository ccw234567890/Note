
# Direct Preference Optimization: Your Language Model is Secretly a Reward Model

## Summary
DPO 提出了一种新的重参数化方法，将 RLHF 中奖励模型与最优策略的关系用闭式解表达，从而将两阶段的 RLHF（奖励建模 + RL 优化）简化为一个简单的分类损失，无需强化学习即可实现人类偏好对齐。

## Key Findings
- DPO 通过数学推导发现，Bradley-Terry 偏好模型中的奖励函数可以用最优策略与参考策略的对数比率来表示，从而消除了显式奖励建模和 RL 训练的需要。
- 在可控情感生成任务中，DPO 在所有 KL 散度值下都实现了最高的期望奖励，严格支配 PPO，甚至超过了使用真实奖励的 PPO-GT。
- 在 Reddit TL;DR 摘要任务中，DPO 在温度 0.0 时胜率约 61%，超过 PPO 的 57%，且对采样温度更鲁棒。
- 在 Anthropic HH 单轮对话任务中，DPO 是唯一显著改进超过数据集中偏好回答的方法。
- DPO 在分布外数据（CNN/DailyMail）上显著优于 PPO，尽管没有使用额外的无标签提示。
- DPO 训练稳定、计算轻量，无需从 LM 采样或进行大量超参数调优。

## Methodology
### 数学框架
1. **Bradley-Terry 偏好模型**：$p^*(y_1 \succ y_2 | x) = \frac{\exp(r^*(x, y_1))}{\exp(r^*(x, y_1)) + \exp(r^*(x, y_2))}$
2. **KL 约束下的最优策略闭式解**：$\pi_r(y|x) = \frac{1}{Z(x)} \pi_{\text{ref}}(y|x) \exp\left(\frac{1}{\beta} r(x, y)\right)$
3. **重参数化**：$r(x, y) = \beta \log\frac{\pi^*(y|x)}{\pi_{\text{ref}}(y|x)} + \beta \log Z(x)$
4. **DPO 损失函数**：$L_{DPO}(\pi_\theta; \pi_{\text{ref}}) = -\mathbb{E}_{(x,y_w,y_l)\sim D} \left[ \log \sigma\left( \beta \log\frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta \log\frac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)} \right) \right]$

### 实验设置
- **可控情感生成**：IMDb 电影评论，GPT-2-large，自动情感分类器标注
- **摘要生成**：Reddit TL;DR，GPT-J (6B)，人类标注
- **单轮对话**：Anthropic HH，Pythia-2.8B，人类标注
- 对比方法：PPO、PPO-GT、Preferred-FT、Unlikelihood、Best of N、Zero-shot
- 评估：Reward-KL 前沿曲线（情感任务）、GPT-4 自动评估 + 人类验证（摘要/对话）

## My Notes
DPO 的核心洞察在于"语言模型秘密地就是一个奖励模型"——通过巧妙的数学重参数化，将奖励函数表示为策略比率的形式，使得配分函数在偏好比较中抵消，最终得到一个简单的二元交叉熵损失。这一方法在理论上保持了与标准 RLHF 相同的表示能力（定理 1），同时大幅降低了计算复杂度和实现难度。

## References
Rafailov, R., Sharma, A., Mitchell, E., Ermon, S., Manning, C. D., & Finn, C. (2024). *Direct Preference Optimization: Your Language Model is Secretly a Reward Model*. arXiv:2305.18290 [cs]. https://doi.org/10.48550/arXiv.2305.18290

---

Written by LLM-for-Zotero.
