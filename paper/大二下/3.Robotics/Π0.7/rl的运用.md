---
title: "$\\pi_{0.7}$: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities"
citekey: ""
doi: "10.48550/arXiv.2604.15483"
year: 2026
journal: ""
created: 2026-04-16
tags: [zotero, paper-note]
---

# $\\pi_{0.7}$: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities

## RL 的数学原理

### 马尔可夫决策过程（MDP）

强化学习的数学基础是 **马尔可夫决策过程**，定义为五元组 $(S, A, P, R, \gamma)$：

- $S$：状态空间（机器人观测到的所有可能状态）
- $A$：动作空间（机器人可执行的所有动作）
- $P(s'|s,a)$：状态转移概率（执行动作后环境如何变化）
- $R(s,a)$：奖励函数（每个动作获得的即时奖励）
- $\gamma \in [0,1]$：折扣因子（权衡即时奖励与未来奖励）

**目标**：找到最优策略 $\pi^*(a|s)$，最大化累积折扣奖励：

$$J(\pi) = \mathbb{E}_{\tau \sim \pi} \left[ \sum_{t=0}^{T} \gamma^t R(s_t, a_t) \right]$$

### 策略梯度定理

$$\nabla_\theta J(\pi_\theta) = \mathbb{E}_{\tau \sim \pi_\theta} \left[ \sum_{t=0}^{T} \nabla_\theta \log \pi_\theta(a_t|s_t) \cdot \hat{A}_t \right]$$

其中 $\hat{A}_t$ 是优势函数，衡量动作 $a_t$ 相对于平均水平的优劣。

### PPO（Proximal Policy Optimization）

PPO 是机器人 RL 中最常用的算法，核心思想是裁剪策略更新幅度：

$$L^{\text{CLIP}}(\theta) = \mathbb{E}_t \left[ \min\left( r_t(\theta) \hat{A}_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t \right) \right]$$

其中 $r_t(\theta) = \frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{\text{old}}}(a_t|s_t)}$ 是新旧策略的概率比，$\epsilon$ 是裁剪阈值（通常 0.2）。

**GAE（Generalized Advantage Estimation）**：

$$\hat{A}_t = \sum_{l=0}^{T-t-1} (\gamma\lambda)^l \delta_{t+l}, \quad \delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)$$

### 流匹配（Flow Matching）—— π₀.₇ 使用的替代方案

π₀.₇ 没有使用 PPO/DPO/GRPO，而是使用流匹配来预测连续动作：

$$\mathcal{L}_{\text{CFM}}(\theta) = \mathbb{E}_{t \sim [0,1], x_0 \sim q, \epsilon \sim \mathcal{N}(0,1)} \left[ \| v_\theta(x_t, t) - u_t(x_t|x_0) \|^2 \right]$$

其中 $v_\theta$ 是学习的向量场，$u_t$ 是目标向量场（从噪声到数据的直线路径）。

---

## RL 在 π₀.₇ 实验中的作用

### π₀.₇ 本身没有用 RL 训练

π₀.₇ 的主训练流程是纯监督学习：

> "π0.7 achieves performance that is competitive with the RL specialists... **without any task-specific post-training**."
> (Intelligence 等, 2026)

具体训练目标：

$$\max_\theta \mathbb{E}_{\mathcal{D}} \left[ \log \pi_\theta(a_{t:t+H} | o_{t-T:t}, C_t) \right]$$

- **VLM 骨干**：通过 FAST token 的离散交叉熵损失训练
- **动作专家**：通过流匹配目标训练（连续生成模型）
- **梯度隔离（KI）**：动作专家的梯度不回流到 VLM 骨干

### 训练数据来自 RL 专家

这是 RL 在 π₀.₇ 中最关键的作用——π₀.₇ 的训练数据包含了 π₀*.6（RL 微调版本）在 RL 训练过程中收集的数据：

> "we make heavy use of suboptimal robot data in training... **data collected by the π0∗.6 model during RL training as additional examples**, effectively allowing π0.7 to distill their behavior."
> (Intelligence 等, 2026)

**蒸馏过程**：
1. **π₀*.6** 对每个任务单独进行 RL 微调 → 产生高质量 rollout 数据
2. 这些 rollout 数据被标注元数据（质量评分 1-5、速度、错误标记）
3. π₀.₇ 在训练时看到这些数据，通过元数据区分好坏
4. 推理时设置 `Quality: 5, Mistake: false` → 模型自然输出 RL 专家级别的行为

### 对比基准：RL 专家模型

论文中 π₀.₇ 对比的 **π₀*.6（RL Specialist）** 是经过 RL 微调的：

> "the RL-trained π0∗.6 models [50], where we can directly compare the speed and robustness of the single general-purpose π0.7 model to the individual **RL-finetuned specialist** π0∗.6 models."
> (Intelligence 等, 2026)

**对比结果**：

| 任务 | π₀.₇ vs RL 专家 |
|------|----------------|
| 衣物折叠（T恤/短裤） | 成功率相当，吞吐量更高 |
| 衣物折叠（最难物品） | 成功率相当，吞吐量更高 |
| 制作浓缩咖啡 | 成功率相当 |
| 折叠纸箱 | 成功率相当，吞吐量更高 |

> "π0.7 achieves performance that is competitive with the RL specialists... and even **outperform the specialists in throughput** in the difficult laundry and box building tasks."
> (Intelligence 等, 2026)

### 消融实验证明 RL 数据的重要性

| 变体 | 说明 | 效果 |
|------|------|------|
| **π₀.₇（完整）** | 包含 RL 专家的 rollout 数据 + 元数据 | ✅ 最佳性能 |
| **π₀.₇ (no eval data)** | 移除所有 RL 专家的 rollout 数据 | ❌ 所有任务性能显著下降 |
| **π₀.₇ (no metadata)** | 保留 RL 数据但移除元数据标注 | ❌ 吞吐量大幅下降 |

> "π0.7 significantly outperforms both π0.7 (no eval data) and π0.7 (no metadata) on all tasks."
> (Intelligence 等, 2026)

### 元数据蒸馏 vs 直接 RL 的对比

| 维度 | 传统 RL（π₀*.6） | 元数据蒸馏（π₀.₇） |
|------|-----------------|-------------------|
| 训练方式 | 在线 RL：策略 rollout → 奖励 → 更新 | 离线监督学习：标注数据 → 流匹配训练 |
| 数据需求 | 需要在线交互 + 奖励函数 | 需要已标注的 rollout 数据 |
| 泛化能力 | 任务特定，每个任务单独训练 | 一个模型覆盖所有任务 |
| 吞吐量 | 较低（RL 探索消耗时间） | 更高（直接输出高质量动作） |
| 数学本质 | $\max_\pi \mathbb{E}[R(s,a)] - \beta \cdot \text{KL}(\pi \parallel \pi_{\text{ref}})$ | $\max_\theta \mathbb{E}_{\mathcal{D}}[\log \pi_\theta(a|o,C)]$ 带元数据条件 |

### 未来方向：自主 RL

> "An exciting direction for future work is to leverage the high steerability of π0.7 to efficiently learn from data in the test task, for example with more detailed language coaching or even with **autonomous reinforcement learning**."
> (Intelligence 等, 2026)

---

## 总结：RL 在 π₀.₇ 中的完整角色

| 角色 | 是否用了 RL | 说明 |
|------|------------|------|
| π₀.₇ 主训练 | ❌ 否 | 纯监督学习（流匹配 + 交叉熵） |
| 训练数据来源 | ✅ 间接使用 | 使用了 π₀*.6 RL 专家的 rollout 数据，通过元数据蒸馏吸收能力 |
| 对比基准 | ✅ 是 | π₀*.6 是 RL 微调的专家模型，π₀.₇ 与之性能相当甚至更优 |
| 消融实验 | ✅ 证明必要性 | 移除 RL 数据后性能显著下降 |
| 未来方向 | ✅ 计划使用 | 论文提出未来可以用自主 RL 进一步提升 |

**核心洞察**：π₀.₇ 的贡献在于用监督学习的方式实现了 RL 级别的性能——通过元数据标注 + 多样化提示，将 RL 专家的能力蒸馏到通用模型中，既保留了 RL 的高性能，又获得了通用模型的泛化能力。

## References

Intelligence, P., Ai, B., Amin, A., Aniceto, R., Balakrishna, A., Balke, G., Black, K., Bokinsky, G., Cao, S., Charbonnier, T., Choudhary, V., Collins, F., Conley, K., Connors, G., Darpinian, J., Dhabalia, K., Dhaka, M., DiCarlo, J., Driess, D., … Zhilinsky, U. (2026). *$π_{0.7}$: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities*. arXiv:2604.15483. https://doi.org/10.48550/arXiv.2604.15483

---

Written by LLM-for-Zotero.
