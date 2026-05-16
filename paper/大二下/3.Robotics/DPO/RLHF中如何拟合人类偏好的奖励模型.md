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

## 一、核心问题

给定一个偏好数据集：

$$D = \{(x^{(i)}, y_w^{(i)}, y_l^{(i)})\}_{i=1}^N$$

其中：
- $x$：输入提示（prompt）
- $y_w$：人类认为**更好**的回答（winning/preferred）
- $y_l$：人类认为**更差**的回答（losing/dispreferred）

**目标：** 学到一个奖励函数 $r(x, y)$，使得对于任意 $(x, y_w, y_l)$，有 $r(x, y_w) > r(x, y_l)$。

---

## 二、Bradley-Terry 偏好模型

### 2.1 核心假设

Bradley-Terry 模型假设：**人类偏好是由某个潜在的奖励函数 $r^*(x, y)$ 决定的**，但人类的判断带有随机性（噪声）。

给定两个回答 $y_1$ 和 $y_2$，人类认为 $y_1$ 优于 $y_2$ 的概率为：

$$p^*(y_1 \succ y_2 | x) = \frac{\exp(r^*(x, y_1))}{\exp(r^*(x, y_1)) + \exp(r^*(x, y_2))}$$

### 2.2 等价形式

该公式等价于 logistic 回归形式：

$$p^*(y_1 \succ y_2 | x) = \sigma(r^*(x, y_1) - r^*(x, y_2))$$

其中 $\sigma(z) = \frac{1}{1 + e^{-z}}$ 是 sigmoid 函数。

| 奖励差 $r(x, y_1) - r(x, y_2)$ | $y_1$ 被偏好的概率 |
|:---:|:---:|
| +5（$y_1$ 明显更好） | $\sigma(5) \approx 0.993$ |
| +1（$y_1$ 略好） | $\sigma(1) \approx 0.731$ |
| 0（一样好） | $\sigma(0) = 0.5$ |
| -1（$y_2$ 略好） | $\sigma(-1) \approx 0.269$ |
| -5（$y_2$ 明显更好） | $\sigma(-5) \approx 0.007$ |

**关键洞察：** 模型不要求 $r(x, y_w)$ 永远大于 $r(x, y_l)$，而是说**差值越大，人类选择 $y_w$ 的概率越高**。这容忍了人类标注中的不一致性。

---

## 三、最大似然估计（MLE）拟合过程

### 3.1 似然函数

给定参数化的奖励模型 $r_\phi(x, y)$（$\phi$ 是神经网络参数），整个数据集的似然（likelihood）为：

$$\mathcal{L}(\phi; D) = \prod_{(x,y_w,y_l)\in D} p_\phi(y_w \succ y_l | x)$$

其中 $p_\phi(y_w \succ y_l | x) = \sigma(r_\phi(x, y_w) - r_\phi(x, y_l))$。

### 3.2 负对数似然损失

取负对数，将乘积变成求和：

$$L_R(r_\phi, D) = -\log \mathcal{L}(\phi; D) = -\sum_{(x,y_w,y_l)\in D} \log \sigma(r_\phi(x, y_w) - r_\phi(x, y_l))$$

写成期望形式：

$$L_R(r_\phi, D) = -\mathbb{E}_{(x,y_w,y_l)\sim D} \left[ \log \sigma(r_\phi(x, y_w) - r_\phi(x, y_l)) \right]$$

### 3.3 与二分类的关系

这实际上就是一个**二元交叉熵损失**：

| 组件 | 标准二分类 | 奖励模型训练 |
|------|-----------|-------------|
| **输入** | 样本 $x$ | 样本对 $(x, y_w, y_l)$ |
| **真实标签** | $y \in \{0, 1\}$ | $y_w$ 更好（标签=1） |
| **模型输出** | $\hat{p} = \sigma(f(x))$ | $\hat{p} = \sigma(r_\phi(x, y_w) - r_\phi(x, y_l))$ |
| **损失** | $-y\log\hat{p} - (1-y)\log(1-\hat{p})$ | $-\log\sigma(r_\phi(x, y_w) - r_\phi(x, y_l))$ |

因为 $y=1$（$y_w$ 总是更好的那个），所以损失简化为 $-\log\hat{p}$。

---

## 四、具体训练流程

### Step 1: 初始化奖励模型

奖励模型 $r_\phi(x, y)$ 通常是一个 Transformer 模型，在预训练 LM 的基础上加一个**线性层**将最后一层 hidden state 映射为标量分数。

### Step 2: 构造训练样本

对于每个偏好对 $(x, y_w, y_l)$：

```
输入: [CLS] x [SEP] y_w [SEP] → 奖励分数 r(x, y_w)
输入: [CLS] x [SEP] y_l [SEP] → 奖励分数 r(x, y_l)
```

两个回答共享同一个奖励模型参数，只是输入不同。

### Step 3: 前向传播

1. 分别计算 $r_\phi(x, y_w)$ 和 $r_\phi(x, y_l)$
2. 计算差值 $\Delta = r_\phi(x, y_w) - r_\phi(x, y_l)$
3. 计算偏好概率 $\hat{p} = \sigma(\Delta)$
4. 计算损失 $L = -\log\hat{p}$

### Step 4: 反向传播

梯度为：

$$\nabla_\phi L_R = -(1 - \sigma(r_\phi(x, y_w) - r_\phi(x, y_l))) \cdot (\nabla_\phi r_\phi(x, y_w) - \nabla_\phi r_\phi(x, y_l))$$

**直观理解：**
- 如果模型已经正确（$r_\phi(x, y_w) \gg r_\phi(x, y_l)$），则 $\sigma \approx 1$，梯度接近 0，**几乎不更新**
- 如果模型错误（$r_\phi(x, y_w) \ll r_\phi(x, y_l)$），则 $\sigma \approx 0$，梯度接近 $-(\nabla_\phi r_\phi(x, y_w) - \nabla_\phi r_\phi(x, y_l))$，**大幅更新**
- 梯度方向：**提高** $y_w$ 的奖励分数，**降低** $y_l$ 的奖励分数

---

## 五、数值示例

假设一个训练样本：

| 输入 $x$ | 回答 $y_w$（偏好） | 回答 $y_l$（不偏好） |
|----------|-------------------|-------------------|
| "如何杀死一个进程？" | "建议先用 tasklist 查看进程，然后用 taskkill /PID 正常关闭" | "用 taskkill /F /PID 强制杀死" |

**前向传播：**

| 计算步骤 | 数值 |
|----------|------|
| $r_\phi(x, y_w)$ | 2.5 |
| $r_\phi(x, y_l)$ | 0.8 |
| $\Delta = r_\phi(x, y_w) - r_\phi(x, y_l)$ | 1.7 |
| $\hat{p} = \sigma(1.7)$ | 0.846 |
| $L = -\log(0.846)$ | 0.167 |

**反向传播梯度：**
- $(1 - 0.846) = 0.154$ 的权重
- 提高 $r_\phi(x, y_w)$ 的梯度分量
- 降低 $r_\phi(x, y_l)$ 的梯度分量

---

## 六、训练完成后

训练好的奖励模型 $r_\phi(x, y)$ 可以给任何 $(x, y)$ 对打分：

```
输入: "如何杀死一个进程？" + "用 taskkill /PID 1234" → 分数: 3.2
输入: "如何杀死一个进程？" + "我不知道" → 分数: -1.5
输入: "如何杀死一个进程？" + "用 taskkill /F /PID 强制杀死" → 分数: 0.8
```

这个奖励分数随后被用于 RL 阶段（PPO）来微调语言模型。

---

## 七、DPO 的突破

DPO 的关键洞察是：**不需要显式地训练奖励模型**。通过数学推导，Bradley-Terry 模型中的奖励函数可以用策略比率来表示：

$$r(x, y) = \beta \log\frac{\pi_\theta(y|x)}{\pi_{\text{ref}}(y|x)} + \beta \log Z(x)$$

代入 Bradley-Terry 模型后，配分函数 $Z(x)$ 抵消，得到：

$$p(y_w \succ y_l | x) = \sigma\left( \beta \log\frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta \log\frac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)} \right)$$

**所以 DPO 的损失函数和奖励模型训练的损失函数在数学形式上是完全一样的**——只是把 $r_\phi(x, y)$ 替换成了 $\beta \log\frac{\pi_\theta(y|x)}{\pi_{\text{ref}}(y|x)}$。

| 方法 | 拟合对象 | 损失函数形式 |
|------|---------|-------------|
| **RLHF 奖励模型** | $r_\phi(x, y)$ | $-\log\sigma(r_\phi(x, y_w) - r_\phi(x, y_l))$ |
| **DPO** | $\pi_\theta(y\|x)$ | $-\log\sigma(\beta\log\frac{\pi_\theta(y_w\|x)}{\pi_{\text{ref}}(y_w\|x)} - \beta\log\frac{\pi_\theta(y_l\|x)}{\pi_{\text{ref}}(y_l\|x)})$ |

**两者都是最大化偏好回答的隐式奖励与不偏好回答的隐式奖励之间的差值**，只是隐式奖励的定义不同。

## References

Rafailov, R., Sharma, A., Mitchell, E., Ermon, S., Manning, C. D., & Finn, C. (2024). *Direct Preference Optimization: Your Language Model is Secretly a Reward Model*. arXiv. DOI: 10.48550/arXiv.2305.18290.

---

Written by LLM-for-Zotero.