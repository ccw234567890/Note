---
title: "DPO/GRPO/RL 详解：数学原理与区别"
citekey: ""
doi: "10.48550/arXiv.2604.15483"
year: 2026
journal: ""
created: 2026-04-16
tags: [zotero, paper-note]
---

# DPO/GRPO/RL 详解：数学原理与区别

## 一、基础：强化学习（RL）

### 1.1 标准 RL 框架

强化学习的核心是 **马尔可夫决策过程（MDP）**，定义为五元组 $(S, A, P, R, \gamma)$：

- $S$：状态空间
- $A$：动作空间
- $P(s'|s,a)$：状态转移概率
- $R(s,a)$：奖励函数
- $\gamma \in [0,1]$：折扣因子

**目标**：找到最优策略 $\pi^*(a|s)$，最大化**累积折扣奖励**：

$$J(\pi) = \mathbb{E}_{\tau \sim \pi} \left[ \sum_{t=0}^{T} \gamma^t R(s_t, a_t) \right]$$

其中 $\tau = (s_0, a_0, s_1, a_1, ..., s_T)$ 是一条轨迹。

### 1.2 RL 在 LLM 中的形式（RLHF）

在 LLM 对齐中，RL 被形式化为 **RLHF（Reinforcement Learning from Human Feedback）**：

**三步流程：**

1. **SFT**：在高质量数据上监督微调
2. **奖励建模**：训练一个奖励模型 $r_\phi(x, y)$ 来预测人类偏好
3. **RL 优化**：使用 PPO 等算法最大化奖励，同时约束与参考模型的 KL 散度

**优化目标**：

$$\max_{\pi_\theta} \mathbb{E}_{x \sim \mathcal{D}, y \sim \pi_\theta(y|x)} \left[ r_\phi(x, y) - \beta \cdot \text{KL}(\pi_\theta(y|x) \parallel \pi_{\text{ref}}(y|x)) \right]$$

其中：
- $r_\phi(x, y)$：奖励模型给出的分数
- $\beta$：KL 惩罚系数
- $\pi_{\text{ref}}$：参考模型（通常是 SFT 模型）
- $\text{KL}$ 项防止模型偏离太远

---

## 二、PPO（Proximal Policy Optimization）

PPO 是 RLHF 中最常用的 RL 算法。

### 2.1 核心思想

PPO 通过**裁剪（clipping）**来限制策略更新的幅度，避免一步更新过大导致训练不稳定。

### 2.2 数学原理

**目标函数**：

$$L^{\text{CLIP}}(\theta) = \mathbb{E}_t \left[ \min\left( r_t(\theta) \hat{A}_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t \right) \right]$$

其中：
- $r_t(\theta) = \frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{\text{old}}}(a_t|s_t)}$：**重要性采样比率**，衡量新旧策略在动作 $a_t$ 上的概率比
- $\hat{A}_t$：**优势函数**估计，表示动作 $a_t$ 相对于平均水平的优势
- $\epsilon$：裁剪阈值（通常 0.2）
- $\text{clip}(r, 1-\epsilon, 1+\epsilon)$：将比率限制在 $[1-\epsilon, 1+\epsilon]$ 内

**直观理解**：
- 当 $\hat{A}_t > 0$（好动作）：鼓励增加 $r_t$，但不超过 $1+\epsilon$
- 当 $\hat{A}_t < 0$（坏动作）：鼓励减少 $r_t$，但不低于 $1-\epsilon$

### 2.3 优势函数估计（GAE）

$$\hat{A}_t = \sum_{l=0}^{T-t-1} (\gamma\lambda)^l \delta_{t+l}$$

其中 $\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)$ 是 **TD 误差**，$\lambda$ 是 GAE 参数。

### 2.4 完整 PPO 损失

$$L^{\text{PPO}}(\theta) = L^{\text{CLIP}}(\theta) - c_1 L^{\text{VF}}(\theta) + c_2 S[\pi_\theta](s_t)$$

- $L^{\text{VF}}(\theta)$：价值函数（Value Function）的 MSE 损失
- $S[\pi_\theta](s_t)$：策略熵奖励，鼓励探索

### 2.5 PPO 的优缺点

| 优点 | 缺点 |
|------|------|
| 训练稳定，更新可控 | 需要同时维护策略网络和价值网络 |
| 样本效率较高 | 需要奖励模型（额外训练） |
| 广泛验证 | 实现复杂，超参数敏感 |

---

## 三、DPO（Direct Preference Optimization）

DPO 是 **2023 年**提出的方法，**不需要显式的奖励模型和 RL 训练**，直接通过偏好数据优化策略。

### 3.1 核心洞察

DPO 的关键洞察是：**RLHF 中的最优策略可以解析地表示为奖励函数的函数**，因此可以直接从偏好数据中学习策略，无需训练奖励模型。

### 3.2 数学推导

**Step 1**：RLHF 优化问题的闭式解

在 KL 约束下，最优策略为：

$$\pi^*(y|x) = \frac{1}{Z(x)} \pi_{\text{ref}}(y|x) \exp\left(\frac{1}{\beta} r(x, y)\right)$$

其中 $Z(x) = \sum_y \pi_{\text{ref}}(y|x) \exp(\frac{1}{\beta} r(x, y))$ 是配分函数。

**Step 2**：反解奖励函数

$$r(x, y) = \beta \log\frac{\pi^*(y|x)}{\pi_{\text{ref}}(y|x)} + \beta \log Z(x)$$

**Step 3**：代入 Bradley-Terry 偏好模型

Bradley-Terry 模型假设人类偏好概率为：

$$p^*(y_w \succ y_l | x) = \frac{\exp(r(x, y_w))}{\exp(r(x, y_w)) + \exp(r(x, y_l))}$$

代入 $r$ 的表达式，配分函数 $Z(x)$ 消去：

$$p^*(y_w \succ y_l | x) = \frac{1}{1 + \exp\left(\beta \log\frac{\pi(y_l|x)}{\pi_{\text{ref}}(y_l|x)} - \beta \log\frac{\pi(y_w|x)}{\pi_{\text{ref}}(y_w|x)}\right)}$$

### 3.3 DPO 损失函数

$$L_{\text{DPO}}(\pi_\theta; \pi_{\text{ref}}) = -\mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}} \left[ \log \sigma\left( \beta \log\frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta \log\frac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)} \right) \right]$$

其中：
- $y_w$：被偏好的（赢家）回答
- $y_l$：不被偏好的（输家）回答
- $\sigma$：sigmoid 函数
- $\beta$：控制对参考模型的偏离程度

**直观理解**：DPO 直接**增加偏好回答的相对概率**，减少非偏好回答的相对概率。

### 3.4 DPO vs PPO 对比

| 维度 | PPO（RLHF） | DPO |
|------|------------|-----|
| **奖励模型** | ✅ 需要额外训练 | ❌ **不需要** |
| **策略网络** | ✅ 需要 | ✅ 需要 |
| **价值网络** | ✅ 需要 | ❌ **不需要** |
| **在线采样** | ✅ 需要（on-policy） | ❌ **离线训练** |
| **实现复杂度** | 高 | 低 |
| **训练稳定性** | 中等 | 高 |
| **数学形式** | 数值优化 | **闭式解** |

---

## 四、GRPO（Group Relative Policy Optimization）

GRPO 是 **DeepSeek 在 2024-2025 年**提出的方法，是 PPO 的简化变体，**不需要价值网络**，通过**组内相对比较**来估计优势。

### 4.1 核心思想

GRPO 的核心洞察：**对于同一个 prompt，生成一组回答，用组内回答的相对表现来估计优势**，而不是训练一个价值网络。

### 4.2 数学原理

**Step 1**：对每个 prompt $x$，从旧策略中采样 $G$ 个回答 $\{y_1, y_2, ..., y_G\}$

**Step 2**：计算每个回答的奖励 $r(x, y_i)$

**Step 3**：**组内归一化**计算优势：

$$\hat{A}_i = \frac{r(x, y_i) - \mu_r}{\sigma_r}$$

其中 $\mu_r = \frac{1}{G}\sum_{j=1}^G r(x, y_j)$，$\sigma_r = \sqrt{\frac{1}{G}\sum_{j=1}^G (r(x, y_j) - \mu_r)^2}$

**Step 4**：GRPO 目标函数

$$L^{\text{GRPO}}(\theta) = -\frac{1}{G} \sum_{i=1}^G \left[ \min\left( \frac{\pi_\theta(y_i|x)}{\pi_{\theta_{\text{old}}}(y_i|x)} \hat{A}_i, \text{clip}\left( \frac{\pi_\theta(y_i|x)}{\pi_{\theta_{\text{old}}}(y_i|x)}, 1-\epsilon, 1+\epsilon \right) \hat{A}_i \right) \right] + \beta \cdot \text{KL}(\pi_\theta \parallel \pi_{\text{ref}})$$

### 4.3 GRPO 的关键创新

| 创新 | 说明 |
|------|------|
| **无价值网络** | 用组内归一化替代价值函数估计 |
| **组内相对比较** | 优势基于组内相对表现，而非绝对分数 |
| **天然去偏** | 组内归一化自动消除奖励模型的偏差 |
| **计算效率高** | 比 PPO 少一个网络，训练更快 |

### 4.4 GRPO vs PPO vs DPO

| 维度 | PPO | DPO | GRPO |
|------|-----|-----|------|
| **奖励模型** | ✅ 需要 | ❌ 不需要 | ✅ 需要（或规则奖励） |
| **价值网络** | ✅ 需要 | ❌ 不需要 | ❌ **不需要** |
| **在线采样** | ✅ 需要 | ❌ 不需要 | ✅ **需要** |
| **优势估计** | GAE（价值网络） | 无 | **组内归一化** |
| **偏好数据** | 需要成对偏好 | 需要成对偏好 | **只需要奖励分数** |
| **实现复杂度** | 高 | 低 | 中 |

---

## 五、三种方法的数学关系总结

### 5.1 统一视角

三种方法都可以看作是在优化同一个核心目标的不同近似：

$$\max_\pi \mathbb{E}[r(x,y)] - \beta \cdot \text{KL}(\pi \parallel \pi_{\text{ref}})$$

| 方法 | 如何近似这个目标 |
|------|----------------|
| **PPO** | 用价值网络估计优势 + 裁剪约束更新步长 |
| **DPO** | 解析推导出闭式损失，直接优化偏好概率 |
| **GRPO** | 用组内采样替代价值网络，组内归一化估计优势 |

### 5.2 关键公式对比

| 方法 | 核心损失函数 |
|------|-------------|
| **PPO** | $\mathbb{E}[\min(r_t(\theta)\hat{A}_t, \text{clip}(r_t(\theta), 1\pm\epsilon)\hat{A}_t)]$ |
| **DPO** | $-\mathbb{E}[\log\sigma(\beta\log\frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta\log\frac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)})]$ |
| **GRPO** | $-\frac{1}{G}\sum_i [\min(\frac{\pi_\theta(y_i|x)}{\pi_{\theta_{\text{old}}}(y_i|x)}\hat{A}_i, \text{clip}(\cdots)\hat{A}_i)] + \beta\text{KL}$ |

### 5.3 与 π₀.₇ 的关系

π₀.₇ **没有使用** DPO/GRPO/PPO 中的任何一种。它使用的是：

1. **流匹配（Flow Matching）**：用于动作预测的连续生成目标
2. **知识隔离（KI）训练**：VLM 通过离散交叉熵损失训练，动作专家通过流匹配训练
3. **元数据引导 + CFG**：推理时通过元数据（质量/速度/错误标记）引导模型输出最佳行为

π₀.₇ 的"对齐"方式是通过**元数据标注**实现的——在训练数据中标注质量评分，推理时设置高质量参数，模型自然学会输出高质量行为。这与 DPO/GRPO/PPO 的偏好对齐思路不同，但达到了类似的效果。

## References

Intelligence, P., Ai, B., Amin, A., Aniceto, R., Balakrishna, A., Balke, G., Black, K., Bokinsky, G., Cao, S., Charbonnier, T., Choudhary, V., Collins, F., Conley, K., Connors, G., Darpinian, J., Dhabalia, K., Dhaka, M., DiCarlo, J., Driess, D., … Zhang, Z. (2026). *π₀.₇: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities*. arXiv:2604.15483. https://doi.org/10.48550/arXiv.2604.15483

---

Written by LLM-for-Zotero.
