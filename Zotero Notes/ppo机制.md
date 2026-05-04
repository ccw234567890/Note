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

## 一、PPO（Proximal Policy Optimization）详解

### 1.1 PPO 是什么？

PPO（Proximal Policy Optimization）是一种**强化学习算法**，由 OpenAI 在 2017 年提出。在 RLHF 的上下文中，PPO 是**阶段 2（RL 优化阶段）** 的标准算法，用于微调语言模型以最大化奖励模型的评分，同时不偏离参考策略太远。

### 1.2 PPO 的 Actor-Critic 架构

PPO 需要**两个模型**同时参与训练：

| 组件 | 作用 | 数学表达 |
|:----|:-----|:---------|
| **策略模型（Actor）** $\pi_\theta$ | 生成文本，决定"做什么" | 被优化 |
| **价值模型（Critic）** $V_\psi$ | 估计状态价值，计算 Advantage | $A_t = r_t + \gamma V(s_{t+1}) - V(s_t)$ |

### 1.3 PPO 的目标函数

PPO 的核心创新是**裁剪（clipping）** 机制，防止策略更新过大：

$$
J_{\text{PPO}}(\theta) = \mathbb{E}_{q \sim P(Q),\; o \sim \pi_{\theta_{\text{old}}}(O|q)} \left[ \frac{1}{|o|} \sum_{t=1}^{|o|} \min\left( \frac{\pi_\theta(o_t|q,o_{<t})}{\pi_{\theta_{\text{old}}}(o_t|q,o_{<t})} A_t,\; \text{clip}\left( \frac{\pi_\theta(o_t|q,o_{<t})}{\pi_{\theta_{\text{old}}}(o_t|q,o_{<t})}, 1-\varepsilon, 1+\varepsilon \right) A_t \right) \right]
$$

其中：
- $\frac{\pi_\theta}{\pi_{\theta_{\text{old}}}}$ 是**重要性采样比率**（importance sampling ratio）
- $\varepsilon$ 是裁剪阈值（通常为 0.2）
- $A_t$ 是 Advantage（优势函数）

**裁剪机制的作用**：当 $A_t > 0$（好动作）时，鼓励增大该动作的概率，但不超过 $1+\varepsilon$ 倍；当 $A_t < 0$（差动作）时，鼓励减小该动作的概率，但不低于 $1-\varepsilon$ 倍。

### 1.4 Advantage 的计算：GAE

PPO 使用 **GAE（Generalized Advantage Estimation）** 来计算 Advantage：

$$
\hat{A}_t = \sum_{l=0}^{\infty} (\gamma\lambda)^l \delta_{t+l}
$$

其中 TD 误差 $\delta_t$ 为：

$$
\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)
$$

- $\gamma$：折扣因子（通常 0.99）
- $\lambda$：GAE 参数（通常 0.95），控制偏差-方差权衡
- $V(s_t)$：价值网络对状态 $s_t$ 的估计

### 1.5 PPO 的完整训练流程

```
1. 初始化策略网络 π_θ 和价值网络 V_ψ
2. for each iteration:
3.   用当前策略 π_θ 采样一批轨迹
4.   用奖励模型给每个完整回答打分
5.   用价值网络 V_ψ 估计每个 token 的状态价值
6.   用 GAE 计算每个 token 的 Advantage A_t
7.   通过 PPO 裁剪目标更新策略网络 π_θ（多次）
8.   通过最小化 TD 误差更新价值网络 V_ψ（多次）
```

### 1.6 PPO 的三大问题

**问题 1：显存开销巨大**

价值网络通常和策略网络规模相当。在 PPO 中，你需要同时加载：

| 模型 | 参数量（以 7B 模型为例） |
|:----|:---------------------:|
| 策略网络 $\pi_\theta$ | 7B |
| 价值网络 $V_\psi$ | 7B |
| 奖励模型 $r_\phi$ | 7B |
| 参考模型 $\pi_{\text{ref}}$ | 7B |
| **总计** | **28B 参数** |

> 论文原话："As the value function employed in PPO is typically another model of comparable size as the policy model, it brings a substantial memory and computational burden."

**问题 2：价值网络训练困难**

在 LLM 场景中，奖励模型通常只给**最后一个 token** 打分（即完整回答的好坏），但价值网络需要在**每个 token 位置**都输出一个价值估计。这意味着价值网络必须从稀疏的奖励信号中学习推断中间状态的价值——这是一个非常困难的任务。

**问题 3：额外的误差源**

价值网络的估计本身就有误差，这个误差会传播到 Advantage 的计算中，进而影响策略网络的更新质量。

---

## 二、Token 是什么？

### 2.1 基本概念

**Token（词元）** 是语言模型处理文本的最小单位。它不是字母，也不是完整的单词，而是介于两者之间的"子词"。

举个例子，句子 "I love mathematics" 可能被分词为：

```
"I"      → 1 个 token
" love"  → 1 个 token
" math"  → 1 个 token
"ematics" → 1 个 token
```

**总计：4 个 token**

中文例子，"我喜欢数学"：

```
"我"     → 1 个 token
"喜欢"   → 1 个 token
"数学"   → 1 个 token
```

**总计：3 个 token**

### 2.2 Token 在 RL 中的角色

在 RLHF 中，**每个 token 就是一个"动作"（action）**。策略网络每生成一个 token，就相当于在 RL 中执行了一个动作。一个完整的回答 $o = \{o_1, o_2, \cdots, o_{|o|}\}$ 就是一个**动作序列**（轨迹）。

语言模型预测的是"下一个 token 是什么"的概率：

$$\pi_\theta(o_t | q, o_{<t})$$

---

## 三、奖励模型（Reward Model）如何打分？

### 3.1 奖励模型是什么

奖励模型 $r_\phi$ 是一个**独立的神经网络**（通常和策略模型规模相当），它的任务是：**给一个完整的回答打一个分数**。

### 3.2 奖励模型的训练方式

奖励模型通过**成对比较（pairwise comparison）** 来训练：

**Step 1**：对同一个问题 $q$，让模型生成两个回答 $y_1$ 和 $y_2$

**Step 2**：让人类标注员（或规则判断）比较哪个回答更好：$y_w \succ y_l$

**Step 3**：奖励模型学习预测这种偏好。损失函数是 Bradley-Terry 偏好模型：

$$\mathcal{L}(r_\phi) = -\mathbb{E}_{(q, y_w, y_l) \sim D} \left[ \log \sigma(r_\phi(q, y_w) - r_\phi(q, y_l)) \right]$$

其中 $\sigma$ 是 sigmoid 函数。

**直观理解**：奖励模型学习给"更好的回答"打更高的分，给"更差的回答"打更低的分。它关注的是**相对排序**，而不是绝对分数。

### 3.3 奖励模型的打分方式

奖励模型**只打一个分**——给**整个完整回答**一个标量分数：

$$r = r_\phi(q, o) \in \mathbb{R}$$

比如：
- 回答 "x = 5" → 奖励模型打分：$r = 2.3$
- 回答 "x = 7" → 奖励模型打分：$r = -1.5$

**关键点**：奖励模型只在**最后一个 token**（即回答结束时）给出一个分数，而不是在每个 token 都打分。

### 3.4 DeepSeekMath 中的两种奖励方式

| 方式 | 说明 | 例子 |
|:---|:-----|:-----|
| **Rule（规则）** | 根据答案是否正确直接判断 | 答案正确 → $r=1$，错误 → $r=-1$ |
| **Model（模型）** | 训练一个神经奖励模型打分 | 基于规则判断的结果作为训练数据训练奖励模型 |

> 论文原话："Rule refers to judging the quality of a response based on the correctness of the answer, and Model denotes that we train a reward model to score each response. The training data of the reward model is based on the rule judgment."

---

## 四、价值模型（Value Model / Critic）如何估计价值？

### 4.1 价值模型是什么

价值模型 $V_\psi$ 也是一个神经网络，它的任务是：**在每个 token 位置，估计"从当前位置开始，未来能获得多少累积奖励"**。

### 4.2 价值模型的数学定义

$$V_\psi(s_t) = \mathbb{E}\left[ \sum_{l=0}^{\infty} \gamma^l r_{t+l} \;\big|\; s_t \right]$$

其中：
- $s_t$ 是"状态"——在 LLM 中就是已生成的上下文 $(q, o_{<t})$
- $r_t$ 是第 $t$ 个 token 的即时奖励
- $\gamma$ 是折扣因子（通常接近 1）

### 4.3 价值模型 vs 奖励模型：核心区别

| 维度 | 奖励模型 $r_\phi$ | 价值模型 $V_\psi$ |
|:----|:----------------|:-----------------|
| **输入** | 问题 + **完整回答** $(q, o)$ | 问题 + **部分回答** $(q, o_{<t})$ |
| **输出** | **一个标量分数**（整个回答的质量） | **每个 token 位置一个标量**（未来期望回报） |
| **何时打分** | 只在回答**结束时** | 在**每个 token 位置** |
| **训练数据** | 人类偏好对（pairwise） | TD 误差（自举学习） |
| **作用** | 告诉策略"这个回答好不好" | 告诉策略"当前状态好不好，下一步该不该冒险" |

### 4.4 一个具体的例子

假设模型在解数学题，生成过程如下：

```
Token 1: "Let"     → V(s₁) = 0.3  （刚开始，不确定）
Token 2: " x"      → V(s₂) = 0.3  （还在开头）
Token 3: " ="      → V(s₃) = 0.3
Token 4: " 5"      → V(s₄) = 0.8  （看起来方向对了！）
Token 5: " +"      → V(s₅) = 0.7  （还在继续）
Token 6: " 2"      → V(s₆) = 0.6  （有点不确定）
Token 7: " ="      → V(s₇) = 0.5
Token 8: " 7"      → V(s₈) = 0.9  （快完成了，看起来正确）
```

而奖励模型只在最后打分：$r_\phi(q, o) = 1.0$（答案正确！）

### 4.5 价值模型如何训练

价值模型通过**最小化 TD 误差**来训练：

$$\mathcal{L}(V_\psi) = \mathbb{E}_t \left[ \left( V_\psi(s_t) - (r_t + \gamma V_\psi(s_{t+1})) \right)^2 \right]$$

这本质上是一个**自举（bootstrapping）** 过程——价值模型用自己的预测来更新自己。

---

## 五、PPO 中三者如何协同工作

```
问题 q
  │
  ▼
策略网络 π_θ ──逐个 token 生成──→ 完整回答 o = {o₁, o₂, ..., oₙ}
                                      │
                                      ├──→ 奖励模型 r_φ → 一个分数 r（只在最后）
                                      │
                                      └──→ 价值模型 V_ψ → 每个 token 一个价值 V(s_t)
                                                              │
                                                              ▼
                                                     GAE 计算 Advantage A_t
                                                              │
                                                              ▼
                                                    更新策略网络 π_θ
```

---

## 六、总结对比

| 概念 | 是什么 | 输入 | 输出 | 训练方式 |
|:----|:------|:----|:----|:--------|
| **Token** | 文本的最小处理单元，也是 RL 中的"动作" | — | — | — |
| **奖励模型** $r_\phi$ | 给**完整回答**打分的模型 | $(q, o)$ | **1 个标量** | 成对偏好比较（Bradley-Terry） |
| **价值模型** $V_\psi$ | 给**每个 token 位置**估计未来回报的模型 | $(q, o_{<t})$ | **每个 token 1 个标量** | TD 误差自举学习 |
| **策略网络** $\pi_\theta$ | 语言模型本身，生成 token | $(q, o_{<t})$ | 下一个 token 的概率分布 | PPO 裁剪目标 |

## References

Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X., Zhang, H., Zhang, M., Li, Y. K., Wu, Y., & Guo, D. (2024). *DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models*. arXiv:2402.03300. https://doi.org/10.48550/arXiv.2402.03300

---

Written by LLM-for-Zotero.
