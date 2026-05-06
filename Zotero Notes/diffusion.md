---
title: "TFCDiff: Robust ECG Denoising via Time-Frequency Complementary Diffusion"
citekey: ""
doi: "10.48550/arXiv.2511.16627"
year: 2025
journal: ""
created: 2026-05-06
tags: [zotero, paper-note]
---

# TFCDiff: Robust ECG Denoising via Time-Frequency Complementary Diffusion

## 一、扩散模型的核心思想

扩散模型受热力学中的**扩散过程**启发：

```
正向过程（加噪）：  干净数据 → 加一点噪声 → 再加一点 → ... → 纯噪声
反向过程（去噪）：  纯噪声 → 去一点噪声 → 再去一点 → ... → 干净数据
```

## 二、前向扩散过程

给定一个干净信号 $x_0$，逐步添加高斯噪声，经过 $T$ 步后得到近似纯噪声 $x_T$。

**定义：** 对于 $t = 1, 2, ..., T$：

$$q(x_t|x_{t-1}) = \mathcal{N}(x_t; \sqrt{1-\beta_t} x_{t-1}, \beta_t I)$$

其中 $\beta_t \in (0, 1)$ 是噪声调度（noise schedule）。

**关键性质：** 可以一步从 $x_0$ 直接跳到 $x_t$：

$$q(x_t|x_0) = \mathcal{N}(x_t; \sqrt{\bar{\alpha}_t} x_0, (1-\bar{\alpha}_t) I)$$

重参数化形式：

$$x_t = \sqrt{\bar{\alpha}_t} x_0 + \sqrt{1-\bar{\alpha}_t} \varepsilon, \quad \varepsilon \sim \mathcal{N}(0, I) \tag{3}$$

其中：
- $\alpha_t = 1 - \beta_t$
- $\bar{\alpha}_t = \prod_{s=1}^t \alpha_s$
- 当 $t \to T$ 时，$\bar{\alpha}_t \to 0$，$x_T \to \varepsilon$（纯噪声）

(Li et al., 2025)

## 三、反向去噪过程

用神经网络 $\varepsilon_\theta$ 来近似反向过程。论文使用**条件扩散模型**——以带噪观测 $\tilde{x}$ 为条件：

$$p_\theta(x_{t-1}|x_t, \tilde{x}) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t, \tilde{x}), \sigma_\theta(x_t, t, \tilde{x}) \cdot I) \tag{5}$$

**均值公式：**

$$\mu_\theta(x_t, t, \tilde{x}) = \frac{1}{\sqrt{\alpha_t}} \left( x_t - \frac{1 - \alpha_t}{\sqrt{1 - \bar{\alpha}_t}} \varepsilon_\theta(x_t, t, \tilde{x}) \right) \tag{6}$$

**标准差公式：**

$$\sigma_\theta(x_t, t, \tilde{x}) = \begin{cases} \frac{1 - \bar{\alpha}_{t-1}}{1 - \bar{\alpha}_t} \beta_t, & t \geq 1 \\ \beta_1, & t = 1 \end{cases} \tag{7}$$

(Li et al., 2025)

**直观理解：**
- $\varepsilon_\theta$ 是一个 U-Net，输入 $x_t$（当前噪声信号）、$t$（时间步）、$\tilde{x}$（条件/带噪观测），输出预测的噪声
- 从 $x_t$ 中减去预测的噪声，就得到 $x_{t-1}$

## 四、训练目标

训练 $\varepsilon_\theta$ 使其预测的噪声尽可能接近真实噪声：

$$\mathcal{L}(\theta) = \mathbb{E}_{x_0, \tilde{x}, t, \varepsilon} \left[ \| \varepsilon - \varepsilon_\theta(x_t, t, \tilde{x}) \|_1 \right] \tag{8}$$

(Li et al., 2025)

## 五、噪声调度与 SNR

**二次方差保持调度：**

$$\beta_t = \left( \sqrt{\beta_1} + (t-1)\frac{\sqrt{\beta_T} - \sqrt{\beta_1}}{T-1} \right)^2 \tag{10}$$

参数：$\beta_1 = 10^{-4}$，$\beta_T = 0.5$，$T = 50$

$$\alpha_t = 1 - \beta_t, \quad \bar{\alpha}_t = \prod_{s=1}^t \alpha_s \tag{11}$$

**信噪比 (SNR)：**

$$SNR(t) = \frac{\bar{\alpha}_t}{1 - \bar{\alpha}_t} \tag{12}$$

| $t$ | $\bar{\alpha}_t$ | $SNR(t)$ |
|:---:|:---:|:---:|
| $t=0$ | 1 | $\infty$（纯信号） |
| $t=25$ | 约 0.5 | 1（信号=噪声） |
| $t=50$ | $\approx 0$ | $\approx 0$（纯噪声） |

**SNR 缩放：** 论文引入缩放因子 $c = 150$：

$$SNR'(t) = c \cdot SNR(t)$$

$$\bar{\gamma}_t = \frac{SNR'(t)}{1 + SNR'(t)} \tag{13}$$

(Li et al., 2025)

## 六、DCT 系数分布偏斜问题

### 6.1 问题描述

DCT 系数的分布高度偏斜：

```
D(0)  ┃███████████████████████████████████   ≈ 10² ~ 10³  （DC 分量，巨大）
D(1)  ┃███████                               ≈ 10¹ ~ 10²
D(2)  ┃████                                  ≈ 10¹
...    ┃...
D(10) ┃█                                     ≈ 10⁰
...    ┃...
D(100)┃▏                                    ≈ 10⁻¹
...    ┃...
D(1000)┃▏                                   ≈ 10⁻² ~ 10⁻³ （接近零）
```

DC 分量 $D(0)$ 与高频系数相差 5~6 个数量级。

### 6.2 为什么是问题

扩散模型的噪声 $\varepsilon \sim \mathcal{N}(0, I)$，每个元素方差为 1：

```
D(0) = 500,  噪声 ε₀ ≈ 1    → SNR ≈ 250000（噪声几乎无影响）
D(500) = 0.01, 噪声 ε₅₀₀ ≈ 1 → SNR ≈ 0.0001（信号完全被噪声淹没）
```

高频系数在扩散过程中直接被噪声吞没，模型无法学习到任何高频信息。

### 6.3 解决方案：系数缩放

$$\eta = \max(|P_\tau|, |P_{100-\tau}|), \quad \tau = 1.75, \quad \eta \approx 3$$

$$x_0 \leftarrow x_0 / \eta, \quad \tilde{x} \leftarrow \tilde{x} / \eta$$

(Li et al., 2025)

将所有 DCT 系数除以 3，使大部分系数落在 $[-1, 1]$ 范围内。

## 七、$\alpha_t$ 与 $\bar{\alpha}_t$ 的含义

| 符号 | 公式 | 物理意义 |
|:---:|:---|:---|
| $\beta_t$ | 噪声调度参数 | 第 $t$ 步添加的噪声量 |
| $\alpha_t$ | $1 - \beta_t$ | 第 $t$ 步的信号保留比例 |
| $\bar{\alpha}_t$ | $\prod_{s=1}^t \alpha_s$ | 累积信号保留比例，从 1 衰减到 0 |
| $SNR(t)$ | $\bar{\alpha}_t / (1 - \bar{\alpha}_t)$ | 第 $t$ 步的信噪比 |

## 八、推理（采样）过程

训练完成后，从纯噪声 $x_T \sim \mathcal{N}(0, I)$ 开始，逐步去噪：

```
x_T → x_{T-1} → x_{T-2} → ... → x_1 → x_0
```

每一步：

$$x_{t-1} = \frac{1}{\sqrt{\alpha_t}} \left( x_t - \frac{1 - \alpha_t}{\sqrt{1 - \bar{\alpha}_t}} \varepsilon_\theta(x_t, t, \tilde{x}) \right) + \sigma_t z, \quad z \sim \mathcal{N}(0, I)$$

其中最后一项 $\sigma_t z$ 是随机噪声项，使生成结果具有多样性。

## 九、完整流程总结

```
训练阶段：
  干净 DCT 系数 x₀ ← 缩放归一化到 [-1, 1]
  带噪 DCT 系数 x̃ ← 对 x₀ 加噪声
  随机采样 t ∈ [1, T]
  计算 x_t = √ᾱ_t · x₀ + √(1-ᾱ_t) · ε
  U-Net ε_θ 预测噪声 → 计算 L1 损失 → 反向传播

推理阶段：
  输入带噪 ECG → DCT → 截断 → 缩放
  x_T ~ N(0, I)（纯噪声）
  for t = T down to 1:
    预测噪声 ε_θ(x_t, t, x̃)
    计算 x_{t-1}（去一步噪声）
  x₀ → 逆缩放 → 零填充 → IDCT → 时域去噪信号
```

## 十、总结

| 概念 | 解释 |
|------|------|
| **分布偏斜** | DC 分量（$10^2$）和 AC 分量（$10^{-3}$）相差 5~6 个数量级 |
| **为什么有问题** | 扩散噪声 $\varepsilon \sim \mathcal{N}(0,1)$ 方差为 1，高频系数会被噪声淹没 |
| **$\alpha_t$** | $1 - \beta_t$，第 $t$ 步的信号保留比例 |
| **$\bar{\alpha}_t$** | $\prod \alpha_s$，累积信号保留比例，从 1 衰减到 0 |
| **扩散模型本质** | 正向逐步加噪 → 学习反向逐步去噪 → 从噪声恢复干净信号 |
| **条件扩散** | 以带噪观测 $\tilde{x}$ 为条件，使去噪过程知道目标是什么 |

## References

Li, P., Zhou, Y., Min, J., Wang, Y., Liang, W., & Li, W. (2025). *TFCDiff: Robust ECG Denoising via Time-Frequency Complementary Diffusion*. arXiv:2511.16627 [eess]. https://doi.org/10.48550/arXiv.2511.16627

---

Written by LLM-for-Zotero.
