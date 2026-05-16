
# A Comprehensive Benchmark for Electrocardiogram Time-Series

## Ground Truth、MSE、FFD 详解

---

### 1️⃣ Ground Truth（真实值/金标准）

**是什么：**
Ground Truth 指的是在模型训练和评估中使用的**真实、正确的参考信号或标签**。在本文中，它出现在多个任务中：

- **生成任务**：`yi` 是时间点 `i` 的 **ground truth ECG**，即期望模型输出的干净/真实心电信号
- **预训练阶段**：`si` 是第 `i` 个被掩码 token 的 **ground truth**，即被遮盖部分的原始真实信号
- **检测任务**：`y` 是**二值标签**，标注了每个时间点是否为关键波形（如 QRS 波群）

> yi is the ground truth ECG at time i of y

(Tang 等, 2025)

**作用：** 作为模型输出的"标准答案"，用于计算损失函数（衡量模型预测与真实值之间的差距）和评估指标。

---

### 2️⃣ MSE（Mean Squared Error，均方误差）

**是什么：**
逐点计算预测值与真实值之间差值的平方，再取平均。公式为：

$$ L_{gen} = \frac{1}{t} \sum_{i=1}^{t} \| y_i - e_i w \|^2 $$

其中 `yi` 是 ground truth，`e_i w` 是模型预测值。

**作用：** 最常用的时序信号评估指标，简单高效。但论文指出它在 ECG 评估中有**两个严重缺陷**：

> (1) it fails to capture the semantic fidelity of ECG (e.g., the quasiperiodic characteristics), and (2) it is sensitive to extreme values (e.g., the R-wave).

(Tang 等, 2025)

**具体问题：** 如图 1(b) 所示，当生成的 ECG 波形仅发生**微小时间偏移**时，波形形态完全符合临床特征，但 MSE 反而比一条毫无意义的平直线更高。这是因为 ECG 的极值（如 R 波峰值）与 ground truth 的极值错位，导致平方误差被放大。

> Minor temporal shifts in generated ECGs can cause misalignment between generated maxima and true minima, artificially inflating MSE. Thus, MSE alone is misleading.

(Tang 等, 2025)

---

### 3️⃣ FFD（Feature-based Fréchet Distance，特征弗雷歇距离）

**是什么：**
受图像生成领域 **FID（Fréchet Inception Distance）** 启发，论文提出的**新指标**，用于弥补 MSE 的不足。它不是在逐点层面比较信号，而是在**特征空间**中比较两组信号的整体分布。

**数学定义：**

$$ \text{FFD}(e, \hat{e}) = \sqrt{\frac{1}{k} \left( \| \mu - \hat{\mu} \|^2 + \text{Tr}\left( \Sigma + \hat{\Sigma} - 2(\Sigma \hat{\Sigma})^{\frac{1}{2}} \right) \right)} $$

其中：
- `μ, Σ` — 真实 ECG 特征向量的均值向量和协方差矩阵
- `μ̂, Σ̂` — 生成 ECG 特征向量的均值向量和协方差矩阵
- `Tr` — 矩阵的迹（trace operator）
- `k` — 特征维度

**实际计算时**，均值和协方差通过样本估计：

$$ \tilde{\mu} = \frac{1}{N} \sum_{i=1}^{N} e_i, \quad \tilde{\Sigma} = \frac{1}{N-1} \sum_{i=1}^{N} (e_i - \tilde{\mu})^\top (e_i - \tilde{\mu}) $$

**作用：** 评估生成 ECG 的**语义保真度**，即波形是否保留了临床诊断上有意义的模式。

**核心优势：** 对时间偏移鲁棒。实验表明：

> FFD shows robustness in evaluating the semantics of generated ECGs. ... ECGs preserve diagnostic semantics under temporal shifts ... with FFD remaining stable at 0.022 despite perturbations. In contrast, the MSE sharply increases from 0.281 to 1.579 under the same shifts.

(Tang 等, 2025)

---

### 三者关系总结

| 概念 | 本质 | 作用 | 局限 |
|------|------|------|------|
| **Ground Truth** | 真实参考信号/标签 | 作为"标准答案"衡量模型好坏 | 本身不是指标 |
| **MSE** | 逐点平方误差均值 | 简单衡量信号数值接近程度 | 对时间偏移敏感，无法评估语义质量 |
| **FFD** | 特征空间分布距离（Wasserstein-2） | 评估生成 ECG 的整体形态和临床语义保真度 | 需要额外特征提取器，计算更复杂 |

**一句话概括：** Ground Truth 是标准答案，MSE 逐点比较数值差异但容易误判，FFD 在特征空间比较整体分布，能正确反映临床有效波形的质量，是 MSE 的**关键互补指标**。

## References
Tang, Z., Qi, J., Zheng, Y., & Huang, J. (2025). *A Comprehensive Benchmark for Electrocardiogram Time-Series*. Proceedings of the 33rd ACM International Conference on Multimedia, 6490–6499. DOI: 10.1145/3746027.3754729.

---

Written by LLM-for-Zotero.
