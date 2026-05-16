
# OpenECG: Benchmarking ECG Foundation Models with Public 1.2 Million Records

## 一、实验设计

### 1. 数据集构建

OpenECG 整合了来自 **9个中心** 的 **1,233,337 条 12导联 ECG 记录**（约 120 万条），来自 **483,837 名患者**，是迄今为止最大的公开 ECG 基准。

**有标签数据集（6个）**：

| 数据集 | 样本数 | 导联 | 采样率 | 时长 |
|--------|--------|------|--------|------|
| CPSC | 14,053 | 12 | 500Hz | 6-60s |
| Georgia | 10,344 | 12 | 500Hz | 10s |
| PTB | 549 | 12 | 1000Hz | 不定 |
| PTB-XL | 21,837 | 12 | 500Hz | 10s |
| St. Petersburg (INCART) | 75 | 12 | 257Hz | 1800s |
| Chapman | 45,152 | 12 | 500Hz | 10s |

**无标签数据集（2个）**：
- **MIMIC-IV-ECG**: ~800,000 条记录，160,000 名患者，500Hz，10秒
- **CODE-15**: 345,779 条记录，233,770 名患者，400Hz，7-10秒

### 2. 数据预处理

- 所有信号重采样至 **固定长度 1000 个采样点**
- 数据格式统一为 `(n, 12, 1000)` — n 个样本，12 导联，每导联 1000 点
- 按 **患者** 划分训练/验证/测试集，避免同患者数据泄露
- 标签系统基于 **SNOMED CT** 标准，选择 **24 种 ECG 相关疾病** 作为分类目标
- 五折交叉验证

### 3. 数据增强策略

- **时间掩码 (Temporal Masking)**: 随机掩盖 ECG 信号中连续的 100 个数据点，模拟信号中断
- **导联掩码 (Lead Masking)**: 同时在所有 12 导联上随机掩盖 100 个数据点，模拟多导联信号损坏

### 4. 模型架构

两种骨干网络：
- **ResNet-50**（用于 SimCLR 和 BYOL）
- **Vision Transformer (ViT)**（用于 MAE）

### 5. 三种自监督学习方法

| 方法 | 骨干网络 | 核心思想 |
|------|---------|---------|
| **SimCLR** | ResNet-50 | 对比学习：拉近正样本对，推远负样本对 |
| **BYOL** | ResNet-50 | 自举潜在表示：仅需正样本对，无负样本 |
| **MAE** | ViT | 掩码自编码器：随机掩盖并重建输入信号 |

### 6. 评估策略

**实验一：留一数据集排除法 (Leave-One-Dataset-Out, LODO)**
- 用除目标数据集外的所有数据预训练模型
- 在排除的数据集上测试
- 对比"包含目标数据集预训练 (w/)" vs "排除目标数据集预训练 (w/o)" 的性能差异

**实验二：数据规模缩放实验 (Data Scaling)**
- 训练数据从 **1% 逐步增加到 100%**
- 在固定测试集上评估 AUROC
- 寻找性能饱和点

---

## 二、实验结果与结论

### 1. 主要性能对比

在 PhysioNet Challenge 2020、PTB-XL、CPSC 2018、Chapman 等数据集上，OpenECG 模型与之前的工作（ECG-Chat、MERL、ESI 等）相比具有竞争力。

### 2. LODO 实验结果

| 目标数据集 | BYOL (△) | SimCLR (△) | MAE (△) |
|-----------|---------|-----------|---------|
| CPSC | **+3.6%** | +2.6% | +3.1% |
| PTB-XL | +0.8% | +0.9% | +0.8% |
| Chapman | +0.2% | +0.2% | +0.1% |
| PTB | +1.1% | +1.2% | +1.5% |
| Georgia | +1.2% | +1.2% | +2.4% |
| INCART | **+4.4%** | +3.2% | +2.9% |

**关键发现**：
- **INCART 和 CPSC**（高变异性数据集）从预训练中包含自身数据获益最大（△达 4.4%）
- **Chapman 和 PTB-XL**（同质性好、结构规整的数据集）获益最小（△ < 1%）
- **BYOL 和 MAE 整体优于 SimCLR**，尤其在变异性大的数据集上

### 3. 数据规模缩放结论

- **BYOL 和 MAE** 在 **60-70%** 数据量时达到性能饱和
- **SimCLR** 需要更多数据（超过 80% 仍持续提升）
- 说明：**特征一致性学习（BYOL）和生成式重建（MAE）比对比学习（SimCLR）更数据高效**

### 4. 核心结论

> **公开数据集经过精心整理和标准化后，可以媲美甚至超越专有数据集，训练出鲁棒的 ECG 基础模型。**

- 数据集**多样性**比单纯的数据量更重要
- BYOL 和 MAE 优于 SimCLR，说明**特征一致性和生成式学习**比对比学习更适合 ECG 表示学习
- 数据规模存在**饱和效应**，并非数据越多越好

---

## 三、数学原理与公式推导

### 1. SimCLR — 对比学习

**核心思想**：对同一 ECG 信号做两次不同的数据增强，得到正样本对 $(x_i, x_j)$，与其他样本构成负样本对。

**余弦相似度**：
$$\text{sim}(u, v) = \frac{u^\top v}{\|u\| \|v\|}$$

**InfoNCE 损失函数**（归一化交叉熵损失）：

$$\mathcal{L}_{\text{SimCLR}} = -\log \frac{\exp(\text{sim}(z_i, z_j)/\tau)}{\sum_{k=1}^{2N} \mathbb{1}_{[k \neq i]} \exp(\text{sim}(z_i, z_k)/\tau)}$$

其中：
- $z_i = g(f(\tilde{x}_i))$ — 编码器 $f$ 后接投影头 $g$ 得到的表示
- $\tau$ — 温度参数，控制分布的集中程度
- 分母对 batch 中所有 $2N$ 个样本求和（排除自身）

**数学直觉**：最大化正样本对的相似度（分子），同时最小化与所有负样本的相似度（分母）。这等价于一个 $(2N-1)$ 类的 softmax 分类问题。

### 2. BYOL — 自举潜在表示

**核心思想**：不使用负样本对，仅通过两个网络（在线网络和目标网络）之间的特征一致性来学习。

**架构**：
- **在线网络**：编码器 $f_\theta$ → 投影头 $g_\theta$ → 预测头 $q_\theta$
- **目标网络**：编码器 $f_\xi$ → 投影头 $g_\xi$（参数 $\xi$ 是 $\theta$ 的指数移动平均）

**损失函数**（均方误差的负余弦相似度）：

$$\mathcal{L}_{\text{BYOL}} = \left\| \frac{q_\theta(z_\theta)}{\|q_\theta(z_\theta)\|} - \frac{z_\xi'}{\|z_\xi'\|} \right\|^2_2 = 2 - 2 \cdot \frac{q_\theta(z_\theta)^\top z_\xi'}{\|q_\theta(z_\theta)\| \cdot \|z_\xi'\|}$$

其中：
- $z_\theta = g_\theta(f_\theta(\tilde{x}_1))$ — 在线网络对增强视图1的投影
- $z_\xi' = g_\xi(f_\xi(\tilde{x}_2))$ — 目标网络对增强视图2的投影
- $q_\theta$ — 预测头，防止表示坍塌

**目标网络更新**（指数移动平均）：

$$\xi \leftarrow \tau \xi + (1 - \tau) \theta$$

其中 $\tau \in [0,1]$ 是衰减率（通常接近1，如 0.996）。

**数学直觉**：BYOL 通过让在线网络预测目标网络的输出来学习表示。由于目标网络缓慢跟踪在线网络，这形成了一个自举式的学习循环。**关键创新**：即使没有负样本，通过预测头 $q_\theta$ 和 EMA 更新机制，也能避免表示坍塌（所有样本映射到同一向量）。

### 3. MAE — 掩码自编码器

**核心思想**：随机掩盖输入 ECG 信号的大部分（如 75%），训练模型重建原始信号。

**架构**：
- **编码器** $f_\phi$：仅处理未被掩盖的可见 patch
- **解码器** $g_\psi$：接收编码后的可见 patch + 可学习的掩码 token，重建完整信号

**损失函数**（均方误差，仅在掩码位置计算）：

$$\mathcal{L}_{\text{MAE}} = \frac{1}{|M|} \sum_{i \in M} (x_i - \hat{x}_i)^2$$

其中：
- $M$ — 被掩盖的位置集合
- $x_i$ — 原始 ECG 信号在第 $i$ 个位置的值
- $\hat{x}_i = g_\psi(f_\phi(x_{\text{visible}}), \text{mask\_tokens})_i$ — 重建值

**对于 ViT 的具体实现**：
1. 将 ECG 信号（12×1000）划分为不重叠的 patch（如每个 patch 为 12×16）
2. 随机选择 75% 的 patch 掩盖
3. 仅将 25% 的可见 patch 送入编码器
4. 解码器从编码特征 + 掩码 token 重建完整信号

**数学直觉**：MAE 迫使模型学习 ECG 信号的**全局结构和局部模式**。为了准确重建被掩盖的部分，模型必须理解 ECG 的形态学特征（P波、QRS波群、T波）以及它们之间的时序依赖关系。

### 4. 三种方法的数学对比总结

| 方法 | 损失函数类型 | 需要负样本 | 数学复杂度 | 数据效率 |
|------|------------|-----------|-----------|---------|
| **SimCLR** | InfoNCE (对比) | ✅ 是 | 中等 | 较低 |
| **BYOL** | 负余弦相似度 (MSE) | ❌ 否 | 中等 | 较高 |
| **MAE** | MSE (重建) | ❌ 否 | 较低 | 较高 |

### 5. 评估指标

**AUROC (Area Under the Receiver Operating Characteristic Curve)**：
- 衡量模型区分正负类的能力
- AUC = $P(\text{score}_{\text{positive}} > \text{score}_{\text{negative}})$
- 值域 [0, 1]，1 为完美分类，0.5 为随机

**F1 Score**：
$$F_1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

其中：
- $\text{Precision} = \frac{TP}{TP + FP}$
- $\text{Recall} = \frac{TP}{TP + FN}$

---

## References

Wan, Z., Yu, Q., Mao, J., Duan, W., & Ding, C. (2025). *OpenECG: Benchmarking ECG Foundation Models with Public 1.2 Million Records*. arXiv:2503.00711 [cs]. DOI: 10.48550/arXiv.2503.00711.

---

Written by LLM-for-Zotero.
