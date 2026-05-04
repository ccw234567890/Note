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

## DPO 中的 Sample Completions 详解

### 一、Sample Completions 在 DPO 中的位置

论文原文（Section 4, DPO outline）：

> *"The general DPO pipeline is as follows: 1) **Sample completions** $y_1, y_2 \sim \pi_{\text{ref}}(\cdot | x)$ for every prompt $x$, label with human preferences to construct the offline dataset of preferences $D = \{x^{(i)}, y_w^{(i)}, y_l^{(i)}\}_{i=1}^N$ and 2) optimize the language model $\pi_\theta$ to minimize $L_{DPO}$ for the given $\pi_{\text{ref}}$ and $D$ and desired $\beta$."*

DPO 的完整流程：

```
步骤 1: Sample Completions（偏好数据采集）
╔═══════════════════════════════════════════════════════════════╗
║ 提示 x ──→ π_ref (SFT 模型) ──→ 采样 y₁, y₂ ~ π_ref(·|x)    ║
║                                      ↓                       ║
║                             人类标注偏好 (y_w ≻ y_l)          ║
║                                      ↓                       ║
║                     构建静态偏好数据集 D = {x, y_w, y_l}     ║
╚═══════════════════════════════════════════════════════════════╝
                              ↓
步骤 2: DPO 训练
╔═══════════════════════════════════════════════════════════════╗
║ 用 DPO 损失函数直接优化 π_θ，无需 RL                        ║
╚═══════════════════════════════════════════════════════════════╝
```

### 二、为什么需要 Sample Completions？

#### 2.1 偏好数据的来源

论文 Section 3（Reward Modelling Phase）中明确写道：

> *"In the second phase the SFT model is prompted with prompts $x$ to produce pairs of answers $(y_1, y_2) \sim \pi^{\text{SFT}}(y | x)$. These are then presented to human labelers who express preferences for one answer, denoted as $y_w \succ y_l | x$ where $y_w$ and $y_l$ denotes the preferred and dispreferred completion amongst $(y_1, y_2)$ respectively."*

**关键点：** 偏好数据不是随便找的文本，而是**从 SFT 模型 $\pi^{\text{SFT}}$ 中采样**得到的回答对。

#### 2.2 为什么用 SFT 模型采样？

**原因 1：分布匹配**
SFT 模型 $\pi^{\text{SFT}}$ 是经过监督微调的模型，它的输出分布与人类标注者期望看到的回答分布最接近。如果从原始预训练模型采样，生成的回答质量可能太低，人类无法做出有意义的偏好判断。

**原因 2：奖励模型的准确性**
奖励模型只在 $\pi^{\text{SFT}}$ 的分布附近是准确的。如果偏好数据来自其他分布，训练出的奖励模型在 $\pi^{\text{SFT}}$ 附近的表现会不可靠。

**原因 3：复用现有数据集**
论文 Section 4 指出：

> *"In practice, one would like to reuse preference datasets publicly available, rather than generating samples and gathering human preferences. Since the preference datasets are sampled using $\pi^{\text{SFT}}$, we initialize $\pi_{\text{ref}} = \pi^{\text{SFT}}$ whenever available."*

即：大多数公开的偏好数据集（如 Anthropic HH、Reddit TL;DR）本身就是用 SFT 模型采样构建的，所以 DPO 可以直接复用。

### 三、Sample Completions 的数学表示

#### 3.1 采样过程的形式化

给定一个提示 $x$，从参考策略 $\pi_{\text{ref}}$（即 SFT 模型）中独立采样两个回答：

$$y_1 \sim \pi_{\text{ref}}(\cdot | x)$$
$$y_2 \sim \pi_{\text{ref}}(\cdot | x)$$

这两个回答构成一个**回答对** $(y_1, y_2)$。

#### 3.2 偏好标注

将 $(y_1, y_2)$ 呈现给人类标注者，标注者表达偏好：

$$y_w \succ y_l \;|\; x$$

其中：
- $y_w$ = preferred completion（人类偏好的回答）
- $y_l$ = dispreferred completion（人类不偏好的回答）

#### 3.3 偏好数据集的数学结构

经过采样和标注后，得到静态偏好数据集：

$$D = \{x^{(i)}, y_w^{(i)}, y_l^{(i)}\}_{i=1}^N$$

这是一个**离线（offline）数据集**——一旦构建完成，DPO 训练过程中不再需要从策略中采样。

#### 3.4 偏好分布的假设

论文假设人类偏好是由某个**潜在的真实奖励函数** $r^*(x, y)$ 生成的。在 Bradley-Terry 模型下：

$$p^*(y_1 \succ y_2 | x) = \frac{\exp(r^*(x, y_1))}{\exp(r^*(x, y_1)) + \exp(r^*(x, y_2))}$$

这意味着偏好数据 $D$ 是从这个分布中采样得到的：

$$D \sim p^*$$

### 四、三种实验任务中的具体采样方式

#### 4.1 可控情感生成（IMDb）

论文 Section 6：

> *"In controlled sentiment generation, $x$ is a prefix of a movie review from the IMDb dataset, and the policy must generate $y$ with positive sentiment. In order to perform a controlled evaluation, for this experiment we generate preference pairs over generations using a pre-trained sentiment classifier, where $p(\text{positive} | x, y_w) > p(\text{positive} | x, y_l)$."*

**采样过程：**
1. 从 IMDb 数据集中取电影评论前缀作为提示 $x$
2. 从 SFT 模型（GPT-2-large）中采样 4 个回答
3. 用预训练情感分类器自动标注偏好（代替人类）
4. 对每个前缀创建 6 个偏好对

论文附录 C.1 补充：

> *"We first use supervised fine-tuning on a subset of the IMDB data for 1 epoch. We then use this model to sample 4 completions for 25000 prefixes and create 6 preference pairs for each prefix using the ground-truth reward model."*

**数学表示：**
$$y_1, y_2, y_3, y_4 \sim \pi^{\text{SFT}}(\cdot | x)$$

从 4 个回答中，用情感分类器 $r_{\text{sentiment}}$ 打分，生成 6 个偏好对：

$$D = \{(x, y_w, y_l) \;|\; r_{\text{sentiment}}(x, y_w) > r_{\text{sentiment}}(x, y_l), \; y_w, y_l \in \{y_1, y_2, y_3, y_4\}\}$$

#### 4.2 摘要生成（Reddit TL;DR）

论文 Section 6：

> *"In summarization, $x$ is a forum post from Reddit; the policy must generate a summary $y$ of the main points in the post. Following prior work, we use the Reddit TL;DR summarization dataset along with human preferences gathered by Stiennon et al.."*

**采样过程：**
1. 提示 $x$ = Reddit 论坛帖子
2. 从 SFT 模型（GPT-J）中采样回答对
3. 人类标注者表达偏好

论文特别指出：

> *"The human preference dataset was gathered by Stiennon et al. on samples from a different, but similarly-trained, SFT model."*

这意味着偏好数据来自一个**不同但类似训练**的 SFT 模型，而不是实验用的那个 SFT 模型。

#### 4.3 单轮对话（Anthropic HH）

论文 Section 6：

> *"In single-turn dialogue, $x$ is a human query... we use the Anthropic Helpful and Harmless dialogue dataset, containing 170k dialogues between a human and an automated assistant. Each transcript ends with a pair of responses generated by a large (although unknown) language model along with a preference label denoting the human-preferred response."*

**采样过程：**
1. 提示 $x$ = 人类查询（从天文物理到关系建议）
2. 回答对来自一个**未知的**大型语言模型
3. 人类标注者标注偏好

论文特别指出：

> *"In this setting, no pre-trained SFT model is available; we therefore fine-tune an off-the-shelf language model on only the preferred completions to form the SFT model."*

即：当没有现成的 SFT 模型时，用偏好数据中的 $y_w$（偏好的回答）做监督微调来构建 $\pi^{\text{SFT}}$。

### 五、DPO 如何处理采样分布偏移？

#### 5.1 核心问题

论文 Section 4 指出：

> *"Since the preference datasets are sampled using $\pi^{\text{SFT}}$, we initialize $\pi_{\text{ref}} = \pi^{\text{SFT}}$ whenever available."*

但问题在于：偏好数据是用 $\pi^{\text{SFT}}$ 采样的，而 DPO 训练时 $\pi_\theta$ 会不断更新。如果 $\pi_\theta$ 偏离 $\pi_{\text{ref}}$ 太远，就会出现**分布偏移**。

#### 5.2 解决方案

**方案 1：初始化 $\pi_{\text{ref}} = \pi^{\text{SFT}}$**

当 SFT 模型可用时，直接将参考策略设为 SFT 模型：

$$\pi_{\text{ref}} = \pi^{\text{SFT}}$$

这样 $\pi_{\text{ref}}$ 的分布与采样偏好数据的分布一致。

**方案 2：用 Preferred-FT 构建 $\pi_{\text{ref}}$**

当 SFT 模型不可用时（如 Anthropic HH 任务）：

> *"When $\pi^{\text{SFT}}$ is not available, we initialize $\pi_{\text{ref}}$ by maximizing likelihood of preferred completions $(x, y_w)$, that is, $\pi_{\text{ref}} = \arg\max_\pi \mathbb{E}_{x,y_w\sim D} [\log \pi(y_w | x)]$."*

即：在偏好数据中的 $y_w$ 上做监督微调：

$$\pi_{\text{ref}} = \arg\max_\pi \sum_{(x, y_w) \in D} \log \pi(y_w | x)$$

论文解释道：

> *"This procedure helps mitigate the distribution shift between the true reference distribution which is unavailable, and $\pi_{\text{ref}}$ used by DPO."*

#### 5.3 KL 散度的保护作用

DPO 损失函数中的 $\beta$ 参数控制着 $\pi_\theta$ 偏离 $\pi_{\text{ref}}$ 的程度：

$$L_{DPO}(\pi_\theta; \pi_{\text{ref}}) = -\mathbb{E}_{(x,y_w,y_l)\sim D} \left[ \log \sigma\left( \beta \log\frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta \log\frac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)} \right) \right]$$

$\beta$ 越大，$\pi_\theta$ 越接近 $\pi_{\text{ref}}$，分布偏移越小。

### 六、Sample Completions 的完整数学流程总结

#### 6.1 输入 → 输出

| | 内容 |
|------|------|
| **输入** | 提示集 $\{x^{(i)}\}_{i=1}^N$ + SFT 模型 $\pi^{\text{SFT}}$ |
| **采样** | $y_1, y_2 \sim \pi^{\text{SFT}}(\cdot \| x)$，对每个提示 |
| **标注** | 人类标注偏好 $y_w \succ y_l \| x$ |
| **数据集** | $D = \{x^{(i)}, y_w^{(i)}, y_l^{(i)}\}_{i=1}^N$ |
| **参考策略** | $\pi_{\text{ref}} = \pi^{\text{SFT}}$（可用时）或 Preferred-FT |
| **输出** | 静态偏好数据集 $D$，供 DPO 训练使用 |

#### 6.2 核心公式一览

| 公式 | 含义 |
|------|------|
| $y_1, y_2 \sim \pi_{\text{ref}}(\cdot \| x)$ | 从参考策略采样回答对 |
| $y_w \succ y_l \| x$ | 人类偏好标注 |
| $D = \{x^{(i)}, y_w^{(i)}, y_l^{(i)}\}_{i=1}^N$ | 构建静态偏好数据集 |
| $p^*(y_1 \succ y_2 \| x) = \frac{\exp(r^*(x, y_1))}{\exp(r^*(x, y_1)) + \exp(r^*(x, y_2))}$ | Bradley-Terry 偏好模型 |
| $\pi_{\text{ref}} = \arg\max_\pi \mathbb{E}_{x,y_w\sim D} [\log \pi(y_w \| x)]$ | 无 SFT 时用 Preferred-FT 构建参考策略 |

### 七、一句话总结

> **Sample Completions = 从 SFT 模型 $\pi^{\text{SFT}}$ 中为每个提示 $x$ 采样两个回答 $(y_1, y_2)$，让人类标注偏好 $y_w \succ y_l$，构建静态离线偏好数据集 $D = \{x, y_w, y_l\}$，供 DPO 直接优化使用——整个过程只需一次采样，训练中不再需要在线生成。**

## References
Rafailov, R., Sharma, A., Mitchell, E., Ermon, S., Manning, C. D., & Finn, C. (2024). *Direct Preference Optimization: Your Language Model is Secretly a Reward Model*. arXiv. DOI: 10.48550/arXiv.2305.18290.

---

Written by LLM-for-Zotero.
