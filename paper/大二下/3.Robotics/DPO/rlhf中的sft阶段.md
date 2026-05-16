---
title: "Direct Preference Optimization: Your Language Model is Secretly a Reward Model"
citekey: ""
doi: "10.48550/arXiv.2305.18290"
year: 2024
journal: ""
created: 2025-07-17
tags: [zotero, paper-note]
---

# Direct Preference Optimization: Your Language Model is Secretly a Reward Model

## RLHF 中的 SFT（Supervised Fine-Tuning）详解

## 一、SFT 在 RLHF 中的位置

RLHF 的完整流程包含三个阶段：

> **阶段 1：SFT（监督微调）** → **阶段 2：奖励建模** → **阶段 3：RL 微调（PPO）**

论文原文（Rafailov et al., 2024, Section 3）：

> *"RLHF typically begins by fine-tuning a pre-trained LM with supervised learning on high-quality data for the downstream task(s) of interest (dialogue, summarization, etc.), to obtain a model π^SFT."*

**SFT 是 RLHF 的起点**，它的输出 $\pi^{\text{SFT}}$ 是后续所有阶段的基础。

---

## 二、SFT 的核心思想

### 2.1 为什么需要 SFT？

预训练语言模型（如 GPT-2、GPT-J、Pythia）是在大规模无监督语料上训练的，它们学会了语言建模（预测下一个 token），但**没有学会如何完成特定任务**。

SFT 的目的就是：**将通用语言模型转化为一个能完成特定下游任务的模型**。

### 2.2 SFT 的数据

SFT 使用**高质量的人工标注数据**，每个样本是：

$$D_{\text{SFT}} = \{(x^{(i)}, y^{(i)})\}_{i=1}^N$$

其中：
- $x^{(i)}$ = 提示（prompt），如对话中的用户问题、摘要任务中的帖子
- $y^{(i)}$ = 人工撰写的理想回答（demonstration）

**论文中的三个实验任务的 SFT 数据：**

| 任务 | 数据集 | SFT 数据来源 |
|------|--------|-------------|
| **可控情感生成** | IMDb 电影评论 | 从 IMDb 训练集取评论，用 GPT-2-large 微调 |
| **摘要生成** | Reddit TL;DR | 人工撰写的论坛帖子摘要 |
| **单轮对话** | Anthropic HH | 偏好数据中**仅取偏好回答** $y_w$ 微调 |

---

## 三、SFT 的数学公式与推导

### 3.1 目标函数

SFT 的优化目标是**最大化对数似然**（Maximum Likelihood Estimation, MLE）：

$$\theta_{\text{SFT}} = \arg\max_\theta \sum_{i=1}^N \log p_\theta(y^{(i)} | x^{(i)})$$

其中 $p_\theta(y|x)$ 是语言模型在参数 $\theta$ 下生成回答 $y$ 的概率。

### 3.2 等价于最小化交叉熵损失

上述最大化问题等价于最小化**负对数似然损失**（即交叉熵损失）：

$$L_{\text{SFT}}(\theta) = -\frac{1}{N} \sum_{i=1}^N \log p_\theta(y^{(i)} | x^{(i)})$$

### 3.3 逐 token 展开

对于每个回答 $y = (y_1, y_2, ..., y_T)$，语言模型的自回归分解为：

$$p_\theta(y|x) = \prod_{t=1}^T p_\theta(y_t | x, y_{<t})$$

代入损失函数：

$$L_{\text{SFT}}(\theta) = -\frac{1}{N} \sum_{i=1}^N \sum_{t=1}^{T^{(i)}} \log p_\theta(y_t^{(i)} | x^{(i)}, y_{<t}^{(i)})$$

**这就是标准的自回归语言模型训练损失**，与预训练阶段的损失形式完全相同，区别仅在于训练数据不同。

### 3.4 梯度更新

对参数 $\theta$ 求梯度：

$$\nabla_\theta L_{\text{SFT}}(\theta) = -\frac{1}{N} \sum_{i=1}^N \sum_{t=1}^{T^{(i)}} \nabla_\theta \log p_\theta(y_t^{(i)} | x^{(i)}, y_{<t}^{(i)})$$

使用随机梯度下降（或 Adam、RMSprop 等优化器）更新参数：

$$\theta \leftarrow \theta - \eta \cdot \nabla_\theta L_{\text{SFT}}(\theta)$$

其中 $\eta$ 是学习率。

---

## 四、SFT 在论文实验中的具体实现

### 4.1 IMDb 情感生成实验

论文附录 C.1 描述：

> *"We first use supervised fine-tuning on a subset of the IMDB data for 1 epoch."*

- **基础模型：** GPT-2-large（774M 参数）
- **数据：** IMDb 电影评论子集
- **训练轮数：** 1 个 epoch（防止过拟合）
- **输出：** $\pi^{\text{SFT}}$（用于后续采样偏好数据）

### 4.2 TL;DR 摘要实验

- **基础模型：** GPT-J（6B 参数）
- **数据：** Reddit TL;DR 数据集的人工撰写摘要
- **框架：** TRLX（用于 RLHF 的训练框架）
- **输出：** $\pi^{\text{SFT}}$（用于后续采样偏好数据）

### 4.3 Anthropic HH 对话实验

论文特别说明：

> *"In this setting, no pre-trained SFT model is available; we therefore fine-tune an off-the-shelf language model on only the preferred completions to form the SFT model."*

- **基础模型：** Pythia-2.8B
- **数据：** 从偏好数据集中**只取偏好回答** $y_w$ 做监督学习
- **原因：** 该数据集没有独立的 SFT 阶段，所以用偏好回答构造 SFT 模型

**数学上：**

$$\pi^{\text{SFT}} = \arg\max_\pi \mathbb{E}_{(x,y_w)\sim D} [\log \pi(y_w | x)]$$

这也是 DPO 论文中当 $\pi^{\text{SFT}}$ 不可用时，初始化参考策略 $\pi_{\text{ref}}$ 的方法。

---

## 五、SFT 在 RLHF 中的关键作用

### 5.1 SFT 的输出流向

```
预训练模型 (GPT-2/GPT-J/Pythia)
        ↓
   ╔═══════════════╗
   ║  SFT 微调     ║  ← 高质量人工标注数据 (x, y)
   ╚═══════════════╝
        ↓
   π^SFT (SFT 模型)
        ↓                    ↓
   ╔═══════════════╗    ╔═══════════════╗
   ║ 阶段2: 采样   ║    ║ 阶段3: 参考   ║
   ║ 偏好数据      ║    ║ 策略 π_ref   ║
   ╚═══════════════╝    ╚═══════════════╝
        ↓                    ↓
   奖励模型训练          PPO KL 约束
```

### 5.2 SFT 的两个关键角色

**角色 1：偏好数据生成器**

在阶段 2（奖励建模）中，用 $\pi^{\text{SFT}}$ 采样回答对：

$$y_1, y_2 \sim \pi^{\text{SFT}}(y|x)$$

然后让人类标注者选择偏好回答 $y_w \succ y_l$，构成偏好数据集：

$$D = \{(x^{(i)}, y_w^{(i)}, y_l^{(i)})\}_{i=1}^N$$

**角色 2：RL 阶段的参考策略**

在阶段 3（PPO）中，$\pi^{\text{SFT}}$ 作为参考策略 $\pi_{\text{ref}}$，用于 KL 散度约束：

$$\max_{\pi_\theta} \mathbb{E}_{x\sim D, y\sim\pi_\theta(y|x)} [r_\phi(x, y)] - \beta \cdot D_{KL}(\pi_\theta(y|x) \parallel \pi_{\text{ref}}(y|x))$$

这个约束防止 RL 微调后的模型偏离 SFT 模型太远。

---

## 六、SFT 的完整数学流程总结

### 6.1 输入输出

| | 内容 |
|------|------|
| **输入** | 预训练语言模型 $\pi_{\text{pretrain}}$ + 高质量数据集 $D_{\text{SFT}} = \{(x^{(i)}, y^{(i)})\}$ |
| **优化目标** | $\theta_{\text{SFT}} = \arg\min_\theta -\sum_i \log \pi_\theta(y^{(i)}|x^{(i)})$ |
| **损失函数** | $L_{\text{SFT}} = -\frac{1}{N}\sum_i \sum_t \log \pi_\theta(y_t^{(i)}|x^{(i)}, y_{<t}^{(i)})$ |
| **输出** | SFT 模型 $\pi^{\text{SFT}}$ |

### 6.2 与预训练的区别

| 方面 | 预训练 | SFT |
|------|--------|-----|
| **数据** | 大规模无监督语料（TB 级） | 高质量人工标注数据（万级） |
| **目标** | 学习通用语言知识 | 学习特定任务行为 |
| **损失** | 下一个 token 预测 | 同上，但数据不同 |
| **轮数** | 多轮（数万步） | 少轮（1-3 epoch） |

### 6.3 SFT 的局限性

SFT 本身只能让模型模仿人类示范，但**无法利用相对偏好信息**（即哪个回答更好）。这就是为什么 RLHF 需要在 SFT 之后增加奖励建模和 RL 微调两个阶段——SFT 只是对齐的第一步，它让模型"学会说话"，但 RLHF 让模型"学会说人话"。

---

## 七、一句话总结

> **SFT = 用高质量人工标注数据，通过标准的最大似然估计（交叉熵损失），将预训练语言模型微调为能完成特定下游任务的模型 $\pi^{\text{SFT}}$，为后续的偏好学习和 RL 优化提供起点和参考基准。**

## References

Rafailov, R., Sharma, A., Mitchell, E., Ermon, S., Manning, C. D., & Finn, C. (2024). *Direct Preference Optimization: Your Language Model is Secretly a Reward Model*. arXiv. https://doi.org/10.48550/arXiv.2305.18290

---

Written by LLM-for-Zotero.
