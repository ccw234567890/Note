
# A Comprehensive Benchmark for Electrocardiogram Time-Series

## ECG 四类下游任务的区别

论文将 ECG 下游应用划分为 **分类（Classification）、检测（Detection）、预测（Forecasting）、生成（Generation）** 四类任务，它们的核心区别在于 **输入输出形式、目标用途和损失函数** 各不相同。

---

### 1️⃣ 分类（Classification）—— 疾病诊断与事件预测

> ECG can be used to classify diseases, such as atrial fibrillation and hyperkalemia classification, based on distinct ECG patterns from different patients.

(Tang 等, 2025)

- **输入**：单个患者的一段完整 ECG 信号 `x`
- **输出**：一个离散的**类别标签** `y`（如房颤、高钾血症、正常）
- **目标**：根据整体波形模式判断患者属于哪一类疾病
- **损失函数**：交叉熵损失
  $$ L_{cls} = -y \log\left(\frac{\exp(\bar{e} w)}{\sum_k \exp(\bar{e} w)_k}\right) $$
  其中 `ē` 是所有时间步特征 `e₁...eₙ` 的平均值，`w` 是线性分类层
- **本质**：**全局序列 → 单个标签**，关注整体模式

---

### 2️⃣ 检测（Detection）—— 关键波形定位

> ECG can be used to calculate cardiovascular metrics (e.g., heart rate variability) by detecting key waveform positions.

(Tang 等, 2025)

- **输入**：一段 ECG 信号 `x`
- **输出**：与输入**同时间长度的二值标签** `y ∈ {0,1}^t`，标记每个时间点是否为关键波形（如 P 波、QRS 波群、T 波）
- **目标**：逐点定位波形位置，用于计算心率变异性等心血管指标
- **损失函数**：逐点二分类交叉熵（Binary Cross-Entropy）
  $$ L_{det} = -y \log(\sigma(ew)) - (1-y) \log(1-\sigma(ew)) $$
  其中 `σ` 是 sigmoid 函数，输出维度需 reshape 为 `R^{t×1}` 以匹配标签
- **本质**：**全局序列 → 同长度逐点标签**，关注局部波形边界

---

### 3️⃣ 预测（Forecasting）—— ECG 动态预测

> ECG enables early risk alerts and facilitates personalized treatment by predicting its changes.

(Tang 等, 2025)

- **输入**：ECG 信号的前 `n` 个 token `x = {s₁, s₂, ..., sₙ}`
- **输出**：后续 `n'` 个 token 的 ECG 信号 `x' = {sₙ₊₁, sₙ₊₂, ..., sₙ₊ₙ'}`
- **目标**：根据已知波形预测未来一段时间的 ECG 变化，用于早期预警
- **损失函数**：均方误差（MSE），与预训练中的 next-token prediction 一致
  $$ L_{forecast} = \frac{1}{n'-1} \sum_{i=n}^{n+n'-1} \frac{1}{m} \| s_{i+1} - e_i w \|^2 $$
- **本质**：**已知序列 → 未来序列**，关注时序延续性

---

### 4️⃣ 生成（Generation）—— 信号去噪与分离

> In clinical practice, acquired ECGs often contain noise or require invasive acquisition (e.g., fetal ECG). Therefore, we define the generation task.

(Tang 等, 2025)

- **输入**：一段容易获取的 ECG 信号 `x`（如含噪声的母体 ECG，或体表混合信号）
- **输出**：与输入对齐的**干净/目标 ECG 信号** `y`（如去噪后的 ECG，或分离出的胎儿 ECG）
- **目标**：从有噪/混合信号中重建出干净的临床可用信号
- **损失函数**：逐点均方误差
  $$ L_{gen} = \frac{1}{t} \sum_{i=1}^{t} \| y_i - e_i w \|^2 $$
- **本质**：**输入序列 → 对齐的输出序列**（序列到序列），关注信号形态重建

---

### 对比总结

| 维度 | 分类 | 检测 | 预测 | 生成 |
|------|------|------|------|------|
| **输出形式** | 单个类别标签 | 逐点二值标签（同长度） | 未来连续信号 | 对齐的干净信号 |
| **输出长度** | 1 | t（与输入相同） | n'（未来段） | t（与输入相同） |
| **核心目标** | 判断疾病类型 | 定位波形位置 | 预测未来变化 | 重建/分离信号 |
| **损失函数** | 交叉熵 | 二分类交叉熵 | MSE | MSE |
| **典型应用** | 房颤分类、高钾血症诊断 | P波/QRS检测、心率变异性计算 | 心血管事件早期预警 | 胎儿ECG分离、信号去噪 |
| **关注重点** | 全局波形模式 | 局部波形边界 | 时序延续性 | 形态保真度 |

简单来说：**分类**看"是什么病"，**检测**看"波形在哪"，**预测**看"接下来怎样"，**生成**看"能不能还原干净信号"。

## References
Tang, Z., Qi, J., Zheng, Y., & Huang, J. (2025). *A Comprehensive Benchmark for Electrocardiogram Time-Series*. Proceedings of the 33rd ACM International Conference on Multimedia, 6490–6499. DOI: 10.1145/3746027.3754729.

---

Written by LLM-for-Zotero.
