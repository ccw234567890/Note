---
title: "PPGFlowECG: Latent Rectified Flow with Cross-Modal Encoding for PPG-Guided ECG Generation and Cardiovascular Disease Detection"
citekey: ""
doi: "10.48550/arXiv.2509.19774"
year: 2026
journal: ""
created: 2026-04-16
tags: [zotero, paper-note]
---

# PPGFlowECG: Latent Rectified Flow with Cross-Modal Encoding for PPG-Guided ECG Generation and Cardiovascular Disease Detection

## Stage 1 — CardioAlign Encoder：语义对齐的共享潜在空间

### 核心目标

Stage 1 的目标是构建一个 **PPG 与 ECG 语义对齐的共享潜在空间**，使得两个模态的潜在表示在几何上接近、在语义上可互相解码。它**完全不涉及速度场 \(v_\theta\)，也不涉及噪声训练**，输入是**成对的对齐 PPG 和 ECG 信号** \((x_{ppg}, x_{ecg})\)。

### 网络结构

给定输入波形 \(x_m \in \mathbb{R}^{L \times 1}\)（\(m \in \{ppg, ecg\}\)），共享编码器 \(E_{CA}(\cdot)\) 输出均值 \(\mu_m\) 和标准差 \(\sigma_m\)，通过**重参数化技巧**采样潜在变量 \(z_m\)：

\[
z_m = \mu_m + \sigma_m \odot \varepsilon, \quad \varepsilon \sim \mathcal{N}(0, I) \tag{1}
\]

重参数化技巧将随机采样转化为确定性操作 + 噪声，使得梯度可以通过采样层反向传播，这是变分自编码器（VAE）的标准技术。

两个交叉模态解码器：
- \(D_{ECG}\)：从 PPG 潜在 \(z_{ppg}\) 重建 ECG 信号
- \(D_{PPG}\)：从 ECG 潜在 \(z_{ecg}\) 重建 PPG 信号

### 三层次对齐损失

#### (1) 全局分布对齐损失 \(L_{GDA}\)

将各模态的后验分布建模为高斯分布：

\[
q_m = \mathcal{N}\left(\mu_m, \text{diag}(\sigma_m^2)\right), \quad m \in \{ppg, ecg\} \tag{2}
\]

全局对齐损失：

\[
L_{GDA} = \|\mu_{ecg} - \mu_{ppg}\|_2^2 + \frac{1}{2}\left[D_{KL}(q_{ecg} \| q_{ppg}) + D_{KL}(q_{ppg} \| q_{ecg})\right] \tag{3}
\]

- **第一项**：均值对齐 — 鼓励两个模态的潜在表示均值接近
- **第二项**：对称 KL 散度 — 匹配两个后验分布的分散程度

#### (2) 局部实例判别损失 \(L_{LID}\)

使用对比学习（InfoNCE 损失）保持受试者级别的判别性：

\[
L_{LID} = -\frac{1}{2}\left[\log\frac{e^{\langle \bar{z}_{ecg}, \bar{z}_{ppg} \rangle / \tau}}{\sum_j e^{\langle \bar{z}_{ecg}, \bar{z}_{ppg}^{(j)} \rangle / \tau}} + \log\frac{e^{\langle \bar{z}_{ppg}, \bar{z}_{ecg} \rangle / \tau}}{\sum_j e^{\langle \bar{z}_{ppg}, \bar{z}_{ecg}^{(j)} \rangle / \tau}}\right] \tag{4}
\]

其中 \(\bar{z}\) 是均值池化后的潜在表示，\(\tau\) 是温度系数。

**直观理解**：同一受试者的 PPG 和 ECG 潜在表示（正样本对）在嵌入空间中应靠近，不同受试者的表示（负样本对）应远离。这防止了分布对齐导致的"表示过平滑"问题。

#### (3) 语义可解码性约束 \(L_{SDC}\)

要求一个模态的潜在表示能解码出另一个模态的信号：

\[
L_{SDC} = \|D_{ECG}(z_{ppg}) - x_{ecg}\|_2^2 + \|D_{PPG}(z_{ecg}) - x_{ppg}\|_2^2 \tag{5}
\]

**意义**：\(z_{ppg}\) 必须包含足够的信息来重建 ECG，\(z_{ecg}\) 也必须能重建 PPG。这迫使潜在空间捕获跨模态可翻译的生理因子。

#### 总损失

\[
L_{CA} = L_{GDA} + L_{LID} + L_{SDC} \tag{6}
\]

### Stage 1 的流程总结

1. 输入一对对齐的 PPG 和 ECG 信号 \((x_{ppg}, x_{ecg})\)
2. 共享编码器 \(E_{CA}\) 分别输出各自的均值 \(\mu_{ppg}, \sigma_{ppg}\) 和 \(\mu_{ecg}, \sigma_{ecg}\)
3. 通过重参数化技巧采样潜在变量 \(z_{ppg}, z_{ecg}\)
4. 用三层次对齐损失 \(L_{CA}\) 优化编码器和解码器

### Stage 1 与 Stage 2 的关系

| 阶段 | 输入 | 训练目标 | 输出 |
|------|------|---------|------|
| **Stage 1** | 成对真实 PPG + 真实 ECG | 对齐潜在空间（三损失） | 编码器 \(E_{CA}\) + 解码器 |
| **Stage 2** | 对齐后的 \(z_{ppg}, z_{ecg}\) + 高斯噪声 | 学习速度场 \(v_\theta\) | 条件速度场 \(v_\theta\) |

**Stage 1 是"对齐"，Stage 2 才是"生成"。** 速度场是 Stage 2 的产物，不是 Stage 1 的。

### Stage 1 对 Stage 2 的理论意义

Stage 1 的对齐直接降低了 Stage 2 流学习的不可约噪声下界。定义平均条件方差：

\[
\bar{\kappa} = \mathbb{E}_c\left[\text{tr}\left(\text{Cov}(y | c)\right)\right]
\]

Stage 2 修正流回归的不可约贝叶斯风险满足 \(R_{\min} \leq \bar{\kappa}\)。Stage 1 通过 \(L_{CA}\) 优化减小 \(\bar{\kappa}\)，使得 Stage 2 能恢复更精细的 ECG 形态，且学习到的动力学近似线性，支持仅用 5-10 步 ODE 求解即可稳定生成。

## References
Fang, X., Jin, J., Wang, H., Liu, C., Cai, J., Xiao, Y., Nie, G., Liu, B., Huang, S., Li, H., & Hong, S. (2026). *PPGFlowECG: Latent Rectified Flow with Cross-Modal Encoding for PPG-Guided ECG Generation and Cardiovascular Disease Detection*. arXiv:2509.19774 [cs]. https://doi.org/10.48550/arXiv.2509.19774

---

Written by LLM-for-Zotero.
