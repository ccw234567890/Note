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

## DCT 系数是什么？

### 一、一句话定义

**DCT 系数** $D(k)$ 是信号经过离散余弦变换后得到的**频域表示**。它告诉你原始信号中**每个频率成分的"含量"**。

$$D(k) = c(k) \sum_{n=0}^{N-1} L(n) \cos\left(\frac{(2n+1)k\pi}{2N}\right) \tag{1}$$

(Li et al., 2025)

---

### 二、直观理解：用"秤"称频率

想象你有一碗混合果汁（原始信号 $L(n)$），你想知道里面每种水果（不同频率）各有多少。

**DCT 系数 $D(k)$ 就是每种水果的"重量"：**

| 概念 | 类比 | 数学 |
|------|------|------|
| 原始信号 $L(n)$ | 混合果汁 | 时域采样点 |
| 余弦基函数 $\cos(\frac{(2n+1)k\pi}{2N})$ | 每种水果的"标准样本" | 第 $k$ 个频率的余弦波 |
| **DCT 系数 $D(k)$** | **每种水果的重量** | **信号与第 $k$ 个余弦基函数的"相似度"** |

**$k$ 的含义：** 频率索引。$k=0$ 是直流分量（DC），$k=1$ 是最低频率，$k$ 越大频率越高。

---

### 三、DCT 系数的物理意义

#### 3.1 每个系数对应一个特定频率

论文中明确给出：

> "the frequency corresponding to the k-th coefficient D(k) is given by $f_k = k \cdot f_s / 2N$"

(Li et al., 2025)

其中：
- $f_s$ = 采样率（360 Hz）
- $N$ = 信号长度（3600 个采样点，对应 10 秒）
- $k$ = 系数索引

**举例：** 对于论文中的配置 $f_s = 360$ Hz，$N = 3600$：

| 系数索引 $k$ | 对应频率 $f_k$ | 含义 |
|:---:|:---:|:---|
| $k=0$ | 0 Hz | **DC 分量**（信号的直流偏置/平均值） |
| $k=1$ | $360/7200 = 0.05$ Hz | 极低频（呼吸引起的基线漂移） |
| $k=10$ | 0.5 Hz | ECG 诊断信息的下限 |
| $k=1000$ | 50 Hz | ECG 诊断信息的上限 |
| $k=3599$ | 180 Hz | 奈奎斯特频率（最高可表示频率） |

#### 3.2 系数的数值含义

- **$|D(k)|$ 越大** → 信号中该频率成分越强
- **$|D(k)| \approx 0$** → 信号中几乎没有该频率成分

论文中 Fig. 2 展示了这一点：

> "the high-frequency portion of D is near zero and contributes negligible useful information"

(Li et al., 2025)

---

### 四、DCT 系数的数学本质

#### 4.1 它是"内积"（投影）

$$D(k) = c(k) \cdot \langle L, \phi_k \rangle$$

其中 $\phi_k(n) = \cos\left(\frac{(2n+1)k\pi}{2N}\right)$ 是第 $k$ 个余弦基函数。

**这本质上是一个内积运算**——衡量信号 $L$ 与基函数 $\phi_k$ 的"相似度"。

#### 4.2 类比：三维空间中的坐标

```
三维空间：                        函数空间（DCT）：

向量 v = (v_x, v_y, v_z)         信号 L(n)
坐标轴 x̂, ŷ, ẑ                    余弦基函数 φ₀, φ₁, φ₂, ...
v_x = v · x̂                      D(0) = ⟨L, φ₀⟩
v_y = v · ŷ                      D(1) = ⟨L, φ₁⟩
v_z = v · ẑ                      D(2) = ⟨L, φ₂⟩
```

**DCT 系数 $D(k)$ 就是信号在"余弦坐标系"中的坐标值。**

---

### 五、DCT 系数的关键特性

#### 5.1 实值性

> "produces real-valued frequency coefficients by extending a real input signal to an even function"

(Li et al., 2025)

DFT 的系数是复数（有实部和虚部），而 DCT 的系数全是**实数**。这是因为 DCT 先对信号做偶延拓，使得正弦项全部消失。

#### 5.2 能量集中性

> "DCT to represent signals with fewer coefficients than DFT, offering superior energy compaction in the frequency domain"

(Li et al., 2025)

ECG 信号的能量几乎全部集中在前 1000 个系数中（对应 0–50 Hz），后面的系数接近零。

#### 5.3 截断无损性

论文验证：保留前 1000 个系数，其余置零，重建后的误差仅为：

$$SSD = (1.66 \pm 3.30) \times 10^{-3}$$

(Li et al., 2025)

---

### 六、论文中 DCT 系数的具体应用

#### 6.1 截断（Truncation）

```
原始 DCT 系数:  D(0), D(1), D(2), ..., D(999), D(1000), ..., D(3599)
                    ↓ 保留前 1000 个 ↓
截断后:         D(0), D(1), D(2), ..., D(999), 0, 0, ..., 0
                    ↓ 零填充回原长度 ↓
重建输入:       D(0), D(1), D(2), ..., D(999), 0, 0, ..., 0
                    ↓ 1D IDCT ↓
重建时域信号:   L̂(0), L̂(1), ..., L̂(3599)  ≈ 原始 L(n)
```

#### 6.2 作为扩散模型的输入

论文将**截断后的 DCT 系数**作为扩散模型的输入，而不是直接在时域上做扩散。这样做的好处：

1. **维度降低：** 3600 维 → 1000 维，计算量减少约 72%
2. **能量集中：** 模型只需学习有信息的部分，忽略接近零的高频噪声
3. **频域去噪：** 噪声在频域中更容易与信号分离

#### 6.3 系数缩放

由于 DC 分量（$D(0)$）远大于 AC 分量（$D(k), k>0$），论文对系数做了缩放：

$$\eta = \max(|P_\tau|, |P_{100-\tau}|), \quad \tau = 1.75, \quad \eta \approx 3$$

$$x_0 \leftarrow x_0 / \eta, \quad \tilde{x} \leftarrow \tilde{x} / \eta$$

(Li et al., 2025)

---

### 七、总结

| 问题 | 答案 |
|------|------|
| **DCT 系数是什么？** | 信号在余弦基函数上的"投影值"，即频域表示 |
| **$D(k)$ 代表什么？** | 第 $k$ 个频率成分的强度，对应频率 $f_k = k \cdot f_s / 2N$ |
| **为什么是实数？** | 偶延拓使正弦项消失，只剩余弦项 |
| **为什么前几个系数最重要？** | ECG 能量集中在低频（0.5–50 Hz），高频系数接近零 |
| **论文中怎么用？** | 截断保留前 1000 个系数 → 缩放 → 作为扩散模型的输入 |

## References
Li, P., Zhou, Y., Min, J., Wang, Y., Liang, W., & Li, W. (2025). *TFCDiff: Robust ECG Denoising via Time-Frequency Complementary Diffusion*. arXiv:2511.16627 [eess]. https://doi.org/10.48550/arXiv.2511.16627

---

Written by LLM-for-Zotero.
