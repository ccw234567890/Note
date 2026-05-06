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

## 一、为什么选择 DCT 而非 DFT？

论文选择 DCT（离散余弦变换）而非 DFT（离散傅里叶变换）有三个核心原因：

1. **实值系数** — DCT 通过将实信号延拓为偶函数，只产生实值频率系数，计算复杂度更低
2. **能量集中性** — DCT 的能量集中度优于 DFT，可以用更少的系数表示信号
3. **正交可逆性** — DCT 是正交变换，保证完美可逆

(Li 等, 2025)

---

## 二、DCT 正变换与逆变换（公式 1-2）

### 2.1 一维 Type-II DCT 正变换

给定一个 ECG 时域信号 $L \in \mathbb{R}^N$（长度为 $N$ 的实向量），其 DCT 系数 $D(k)$ 为：

$$D(k) = c(k) \sum_{n=0}^{N-1} L(n) \cos\left(\frac{(2n+1)k\pi}{2N}\right) \tag{1}$$

### 2.2 一维 Type-III DCT 逆变换（IDCT）

从频域恢复时域信号：

$$L(n) = \sum_{k=0}^{N-1} c(k) D(k) \cos\left(\frac{(2n+1)k\pi}{2N}\right) \tag{2}$$

### 2.3 归一化系数

$$c(k) = \begin{cases} \sqrt{1/N}, & k = 0 \\ \sqrt{2/N}, & k \neq 0 \end{cases}$$

**物理意义：** $k=0$ 对应 DC 分量（直流分量，即信号均值），$k>0$ 对应 AC 分量（交流分量，即不同频率成分）。余弦基函数 $\cos\left(\frac{(2n+1)k\pi}{2N}\right)$ 构成一组正交基，将时域信号投影到频域。

(Li 等, 2025)

---

## 三、DCT 系数截断策略

### 3.1 截断原理

ECG 的诊断信息主要分布在 **0.5–50 Hz** 范围内。DCT 系数的高频部分接近零，贡献可忽略。

**频率分辨率公式：**

$$\Delta f = \frac{f_s}{2N}$$

其中 $f_s$ 是采样率，$N$ 是信号长度。

**第 $k$ 个系数对应的频率：**

$$f_k = k \cdot \frac{f_s}{2N}$$

### 3.2 具体计算

论文中：$f_s = 360$ Hz，$N = 3600$（10 秒信号）

$$\Delta f = \frac{360}{2 \times 3600} = 0.05 \text{ Hz}$$

要保留 50 Hz 以下成分，保留的系数个数为：

$$\left[\frac{50}{\Delta f}\right] = \left[\frac{50}{0.05}\right] = 1000$$

即只保留前 **1000 个 DCT 系数**，其余截断为零。

### 3.3 截断保真度验证

论文对 37590 个 10 秒 ECG 片段进行验证：原始信号 → DCT → 截断 → 零填充 → IDCT 重建，重建信号与原始信号的 SSD（平方距离和）仅为：

$$(1.66 \pm 3.30) \times 10^{-3}$$

证明截断几乎无损。

(Li 等, 2025)

---

## 四、DCT 系数缩放（公式 9）

### 4.1 问题背景

扩散模型的扰动噪声 $\varepsilon \sim \mathcal{N}(0, I)$，要求输入归一化到 $[-1, 1]$。但 DCT 系数的分布高度偏斜，跨越多个数量级——DC 分量和 AC 分量的分布差异巨大。

### 4.2 基于 DC 分量的缩放策略

作者提出仅基于 DC 分量（$k=0$ 的系数）的分布来估计缩放边界：

$$\eta = \max\left(|P_\tau|, |P_{100-\tau}|\right) \tag{9}$$

其中 $P_\tau$ 是 DC 分量分布的第 $\tau$ 百分位数。

**选择 $\tau = 1.75$**，得到 $\eta \approx 3$。

### 4.3 缩放操作

将干净信号和带噪观测都除以 $\eta$：

$$x_0 \leftarrow \frac{x_0}{\eta}, \quad \tilde{x} \leftarrow \frac{\tilde{x}}{\eta}$$

**为什么只基于 DC 分量？** AC 分量虽然集中在零附近，但由于偶尔的极端值，范围远大于 DC 分量。如果基于 AC 分量的全局范围来缩放，DC 分量会被过度压缩，导致训练不稳定。

(Li 等, 2025)

---

## 五、DCT 域的条件扩散模型（公式 3-8）

### 5.1 前向扩散过程

给定一对信号 $\{x_0, \tilde{x}\}$，其中 $x_0$ 是干净 DCT 系数，$\tilde{x}$ 是带噪 DCT 系数。对于离散时间步 $t \in \{1, 2, ..., T\}$：

$$x_t = \sqrt{\bar{\alpha}_t} x_0 + \sqrt{1 - \bar{\alpha}_t} \varepsilon, \quad \varepsilon \sim \mathcal{N}(0, I) \tag{3}$$

前向扰动核为高斯分布：

$$q(x_t|x_0) = \mathcal{N}\left(x_t; \sqrt{\bar{\alpha}_t} x_0, \sqrt{1 - \bar{\alpha}_t} I\right) \tag{4}$$

其中 $\bar{\alpha}_t \in (0, 1]$ 由噪声调度决定。当 $t = T$ 时，$x_T$ 近似为各向同性高斯噪声。

### 5.2 反向去噪过程

反向过程以带噪观测 $\tilde{x}$ 为条件，也建模为高斯分布：

$$p(x_{t-1}|x_t, \tilde{x}) = \mathcal{N}\left(x_{t-1}; \mu_\theta(x_t, t, \tilde{x}), \sigma_\theta(x_t, t, \tilde{x}) \cdot I\right) \tag{5}$$

**均值公式（核心去噪步骤）：**

$$\mu_\theta(x_t, t, \tilde{x}) = \frac{1}{\sqrt{\alpha_t}} \left( x_t - \frac{1 - \alpha_t}{\sqrt{1 - \bar{\alpha}_t}} \varepsilon_\theta(x_t, t, \tilde{x}) \right) \tag{6}$$

**标准差公式：**

$$\sigma_\theta(x_t, t, \tilde{x}) = \begin{cases} \frac{1 - \bar{\alpha}_{t-1}}{1 - \bar{\alpha}_t} \beta_t, & t \geq 1 \\ \beta_1, & t = 1 \end{cases} \tag{7}$$

其中 $\varepsilon_\theta(x_t, t, \tilde{x})$ 是基于 U-Net 的噪声预测器。

### 5.3 训练损失

通过最小化变分下界（ELBO），简化为预测噪声与真实噪声的 L1 距离：

$$\mathcal{L}(\theta) = \mathbb{E}_{x_0, \tilde{x}, t, \varepsilon} \left[ \| \varepsilon - \varepsilon_\theta(x_t, t, \tilde{x}) \|_1 \right] \tag{8}$$

**关键点：** 所有信号都是**截断后的 DCT 系数**。去噪完成后，将输出系数零填充回原始长度 $N$，再通过 1D IDCT 变换回时域，得到最终的去噪 ECG 信号。

### 5.4 k-generation 集成策略

由于扩散采样本质上是随机的，进行 $k$ 次独立采样并取平均，可以显著降低方差、提高保真度：

$$\hat{x} = \frac{1}{k} \sum_{i=1}^k \hat{x}^{(i)}$$

(Li 等, 2025)

---

## 六、噪声调度与 SNR 缩放（公式 10-13）

### 6.1 二次方差保持噪声调度

标准二次方差保持（variance-preserving）噪声调度：

$$\beta_t = \left( \sqrt{\beta_1} + (t-1)\frac{\sqrt{\beta_T} - \sqrt{\beta_1}}{T-1} \right)^2 \tag{10}$$

其中 $\beta_1 = 10^{-4}$，$\beta_T = 0.5$，$T = 50$。

$$\alpha_t = 1 - \beta_t, \quad \bar{\alpha}_t = \prod_{s=1}^t \alpha_s \tag{11}$$

### 6.2 信噪比 (SNR)

$$SNR(t) = \frac{\bar{\alpha}_t}{1 - \bar{\alpha}_t} \tag{12}$$

### 6.3 SNR 缩放

**问题：** DCT 域中高频系数能量接近零，容易被噪声淹没。标准时域噪声调度在 DCT 域中会导致高频成分过早被破坏。

**解决方案：** 引入缩放因子 $c$：

$$SNR'(t) = c \cdot SNR(t)$$

代入公式 (12) 得到新的噪声调度参数：

$$\bar{\gamma}_t = \frac{SNR'(t)}{1 + SNR'(t)} \tag{13}$$

**物理意义：** 当 $c > 1$ 时，$SNR'(t) > SNR(t)$，意味着在每个时间步 $t$，信号成分保留更多，噪声添加更慢。论文通过实验确定 $c = 150$ 时性能最佳。

**效果：** 当 $c = 150$ 时，在 $t < 35$ 的时间步内，DCT 域的退化程度比时域更温和，使模型能更好地学习噪声分布。

此外，论文还采用**分层均匀采样**（hierarchical uniform sampling），使噪声预测器能够泛化到连续的噪声水平。

(Li 等, 2025)

---

## 七、完整 DCT 去噪流程总结

```
训练阶段：
  原始 ECG (时域) ──DCT──→ DCT系数 ──截断──→ 截断DCT系数 ──缩放──→ 归一化系数
                                                                      │
  带噪 ECG (时域) ──DCT──→ DCT系数 ──截断──→ 截断DCT系数 ──缩放──→ 归一化系数
                                                                      │
  前向扩散: x_t = √ᾱ_t·x₀ + √(1-ᾱ_t)·ε                              │
  损失: L = E[||ε - ε_θ(x_t, t, x̃)||₁] ◄──── U-Net + TFEM ◄─────────┘

采样/去噪阶段：
  带噪 ECG (时域) ──DCT──→ DCT系数 ──截断──→ 截断DCT系数 ──缩放──→ 归一化系数 x̃
                                                                      │
  反向去噪: x_{t-1} = μ_θ(x_t, t, x̃) + σ_θ·z  (迭代50步)              │
  输出: 去噪后的DCT系数 ◄──── U-Net + TFEM ◄──────────────────────────┘
      │
      ├──反缩放 (×η) ──零填充──→ IDCT ──→ 去噪ECG (时域)
      └──k次独立采样取平均 ──→ 最终结果
```

## 核心创新总结

TFCDiff 将扩散模型从时域搬到了 DCT 频域，利用 DCT 的能量集中性降低计算量，同时通过截断策略去除冗余高频信息。但纯频域建模会丢失时域细节，因此引入 TFEM 模块作为"中介"，动态整合时域和频域表征，实现时频互补的最优去噪效果。

## References

Li, P., Zhou, Y., Min, J., Wang, Y., Liang, W., & Li, W. (2025). *TFCDiff: Robust ECG Denoising via Time-Frequency Complementary Diffusion*. arXiv:2511.16627 [eess]. https://doi.org/10.48550/arXiv.2511.16627

---

Written by LLM-for-Zotero.
