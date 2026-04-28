
# MedSpaformer: A Transferable Transformer with Multi-Granularity Token Sparsification for Medical Time Series Classification

## 一、实验设计

### 1. 数据集（7个数据集，3个医学领域）

| 领域 | 数据集 | 类别数 | 样本数 | 通道数 | 时间步长 |
|------|--------|--------|--------|--------|----------|
| **阿尔茨海默症 (EEG)** | APAVA | 2类 | 5,967 | 16 | 256 |
| | ADFTD | 3类 | 69,752 | 19 | 256 |
| **癫痫 (EEG)** | TUSZ (粗粒度) | 2类 | 22,040 | 19 | 6,000 |
| | TUSZ (细粒度) | 4类 | 2,891 | 19 | 6,000 |
| **心脏病 (ECG)** | PTB | 2类 | 64,356 | 15 | 300 |
| | PTB-XL (粗粒度) | 4类 | 17,110 | 12 | 1,000 |
| | PTB-XL (细粒度) | 5类 | 17,110 | 12 | 1,000 |

### 2. 对比基线（13个）

- **非Transformer模型**：MultiRocket、DLinear、LightTS、TimesNet
- **非多粒度Transformer**：PatchTST、Autoformer、Crossformer、ETSformer、FEDformer、Informer
- **多粒度Transformer**：PathFormer、Medformer、MTST

### 3. 评估指标

采用 **macro-F1** 为主指标（因数据不平衡），同时报告 macro-AUROC、macro-AUPRC 和准确率。10个随机种子（41-50）取均值±标准差。

### 4. 超参数配置

- 多粒度窗口：$S = [25, 50, 100, 150]$
- TSDA 块数：$K = 3$，层级 token 数：$\{O_1, O_2, O_3\} = [128, 64, 32]$
- 粒度间编码输出：$O_{inter} = 10$
- 跨通道编码输出：$U = 5$
- 隐藏维度：$D = 128$
- 冻结语言模型：ClinicalBERT
- 优化器：AdamW，Cosine 学习率调度
- 早停：验证集 F1 连续 7 轮无提升则停止，最多 60 轮

### 5. 实验设置

**监督学习**：在全部7个数据集上训练并测试。

**小样本学习 (Few-shot)**：在源数据集预训练，然后在目标数据集上用 {5, 10, 20, 30, 40, 50} 个样本微调。选择通道数和长度匹配的数据集对：TUSZ(2类)→TUSZ(4类)，PTB-XL(4类)→PTB-XL(5类)。

**零样本学习 (Zero-shot)**：
- **域内迁移**：同一医学领域内跨数据集（如阿尔茨海默症域内 APAVA↔ADFTD）
- **跨域迁移**：跨医学领域（如用癫痫数据训练的模型直接测试心脏病数据）

---

## 二、结果与结论

### 1. 监督学习结果（F1分数）

| 数据集 | 最佳基线 | MedSpaformer | 提升 |
|--------|---------|-------------|------|
| APAVA (2类) | FEDformer 0.742 | **0.821** | +7.9% |
| ADFTD (3类) | TimesNet 0.463 | **0.468** | +0.5% |
| TUSZ (2类) | Medformer 0.821 | **0.852** | +3.1% |
| TUSZ (4类) | PatchTST/MTST 0.855 | **0.901** | +4.6% |
| PTB-XL (4类) | Medformer 0.575 | **0.583** | +0.8% |
| PTB-XL (5类) | MTST 0.532 | **0.562** | +3.0% |
| PTB (2类) | Medformer 0.814 | **0.843** | +2.9% |

**结论**：MedSpaformer 在 **全部7个数据集上取得最优**，证明了其强大的泛化能力。

### 2. 小样本学习

- 在所有 shot 设置下，MedSpaformer 几乎全部最优
- Transformer 模型普遍优于非 Transformer 模型
- 在 PTB-XL 上的优势比 TUSZ 更显著

### 3. 零样本学习

- **域内迁移**表现优于跨域迁移（4个最佳 vs 3个最佳）
- MedSpaformer 的零样本性能 **超过 DLinear 的 50-shot 微调结果**
- 在 APAVA、ADFTD、PTB-XL(4类) 上，零样本甚至 **超过 DLinear 的完整监督学习结果**

### 4. 消融实验

| 配置 | APAVA | TUSZ(2类) | PTB(2类) |
|------|-------|-----------|----------|
| 去掉多粒度 | 0.727 | 0.771 | 0.753 |
| 去掉通道注意力 | 0.766 | 0.794 | 0.787 |
| 去掉稀疏注意力 | 0.752 | 0.788 | 0.767 |
| 去掉标签编码器 | 0.796 | 0.828 | 0.820 |
| **完整模型** | **0.821** | **0.852** | **0.843** |

各模块贡献度：多粒度（~7%）> 稀疏注意力（~6%）> 通道注意力（~5%）> 标签编码器（~2%）

### 5. 效率分析

MedSpaformer 参数量 840万，训练速度排名第三，但 F1 分数最高，在效率与效果之间取得最佳平衡。

---

## 三、数学原理与公式推导

### 1. 问题形式化

给定医学时间序列数据集 $\mathcal{D} = \{(X_i, y_i)\}_{i=1}^N$，其中：

- $X_i \in \mathbb{R}^{L \times C}$：$L$ 个时间步，$C$ 个通道
- $y_i \in \{1, 2, \ldots, M\}$：类别标签，由文本 $T_{y_i}$ 描述

目标是学习一个框架，将时序信号和标签文本对齐到统一的 $D$ 维隐空间，得到：
- $h_i^{(x)} \in \mathbb{R}^D$：时序信号表示
- $h_i^{(y)} \in \mathbb{R}^D$：标签语义表示

优化目标：**最大化时序-标签对的相似度**。

---

### 2. Token-Sparse Dual Attention (TSDA) 块

TSDA 是核心组件，模拟医生的两阶段诊断过程：先整体把握症状，再聚焦分析特定生物标志物。

#### 第一阶段：自注意力（全局上下文建模）

给定输入序列 $H \in \mathbb{R}^{L \times D}$：

$$H_{self} \leftarrow \text{Attn}_{self}(H, H, H)$$

其中 $H_{self} \in \mathbb{R}^{L \times D}$，标准的 Transformer 自注意力。

#### 第二阶段：Token-Sparse 注意力（动态特征精炼）

引入 $Q$ 个可学习的查询向量 $Q \in \mathbb{R}^{Q \times D}$，用领域先验知识增强：

$$Q_{aug} = f(Q, e_{prior})$$

其中 $e_{prior} = f_{LM}(T_{data})$ 是冻结语言模型根据数据集描述生成的领域嵌入，$f$ 是融合函数（本文用拼接）。

稀疏注意力公式：

$$H_{sparse} \leftarrow \text{Attn}_{sparse}(Q_{aug}, H_{self}, H_{self})$$

展开为：

$$H_{sparse} = \text{Softmax}\left(\frac{Q_{aug} W_Q (H_{self} W_K)^\top}{\sqrt{D}}\right) (H_{self} W_V)$$

其中 $H_{sparse} \in \mathbb{R}^{Q \times D}$，且 $Q \ll L$。

**关键特性**：TSDA 块将变长序列 $L$ 映射为固定长度 $Q$，参数量仅取决于 $Q$ 和 $D$，与输入长度无关，实现了**输入长度无关性**。

---

### 3. 多粒度层次化稀疏编码

#### 多粒度分割

对每个通道独立处理，使用不同窗口大小 $S = \{s_1, s_2, \ldots, s_G\}$ 将序列分割为非重叠的 patches：

- 粒度 $s_i$ 产生 patches：$\{p_1^{(i)}, p_2^{(i)}, \ldots\}$，其中 $p_j^{(i)} \in \mathbb{R}^{s_i}$
- patch 数量：$L_i = \lceil L / s_i \rceil$（零填充保证整除）
- 线性投影到统一隐空间：$P_i = [\hat{p}_1^{(i)}, \hat{p}_2^{(i)}, \ldots, \hat{p}_{L_i}^{(i)}] \in \mathbb{R}^{L_i \times D}$

#### 粒度内层次化稀疏编码

每个粒度独立通过 $K$ 个 TSDA 块进行层次化特征精炼：

$$H_k = \text{TSDA}_k(H_{k-1}; \Theta_k, O_k)$$

其中 $H_0 = P_i$，$H_k \in \mathbb{R}^{O_k \times D}$，且 $O_k < O_{k-1}$（逐层压缩）。最终输出 $H_{intra} = H_K \in \mathbb{R}^{O_K \times D}$。

#### 粒度间稀疏编码

将所有粒度的表示拼接：

$$H_{intra}^S = [H_{intra}^{s_1}; H_{intra}^{s_2}; \cdots; H_{intra}^{s_G}] \in \mathbb{R}^{(G \cdot O_K) \times D}$$

通过一个 TSDA 块建模粒度间关系：

$$H_{inter} \in \mathbb{R}^{O_{inter} \times D} = \text{TSDA}(H_{intra}^S; \Theta, O_{inter})$$

其中 $O_{inter} \ll G \cdot O_K$。

---

### 4. 跨通道稀疏编码

将所有通道的粒度间表示拼接：

$$H_C = [H_{inter}^1; H_{inter}^2; \cdots; H_{inter}^C] \in \mathbb{R}^{(C \cdot O_{inter}) \times D}$$

通过 TSDA 块建模通道间依赖：

$$H_C^{self} \in \mathbb{R}^{(C \cdot O_{inter}) \times D} \leftarrow \text{Attn}_{self}(H_C, H_C, H_C)$$

$$H_C^{sparse} \in \mathbb{R}^{U \times D} \leftarrow \text{Attn}_{sparse}(Q_{aug}^C, H_C^{self}, H_C^{self})$$

最终时序嵌入：

$$h_i^{(x)} \in \mathbb{R}^D = \text{MLP}(\text{Flatten}(H_C^{sparse}))$$

**关键特性**：该模块参数量与通道数 $C$ 无关，支持异构数据集（如 6 通道 ICU 监护仪 vs 12 通道可穿戴设备）。

---

### 5. 自适应标签编码器

利用冻结语言模型 $f_{LM}$ 将标签文本 $T_{y_i}$ 映射到隐空间，再通过可学习投影器精炼：

$$h_i^{(y)} \in \mathbb{R}^D = W_1 \cdot (\text{ReLU}(W_2 \cdot f_{LM}(T_{y_i}) + b))$$

这解决了传统 one-hot 编码无法适应异构标签空间的问题，使模型能泛化到未见过的类别。

---

### 6. 损失函数与推理

**训练损失**（交叉熵）：

$$\mathcal{L} = -\sum_{i=1}^N \log \frac{\exp\left(\text{sim}(h_i^{(x)}, h_i^{(y)})\right)}{\sum_{j=1}^M \exp\left(\text{sim}(h_i^{(x)}, h_j^{(y)})\right)}$$

其中 $\text{sim}(\cdot, \cdot)$ 是相似度函数（本文用点积）。

**推理预测**：

$$y'_i = \arg\max_j \text{sim}(h_i^{(x)}, h_j^{(y)}) \quad | \quad j \in \{1, \ldots, M\}$$

即选择与时间序列表示最相似的类别标签作为预测结果。

---

## 总结

MedSpaformer 的核心创新在于：

1. **TSDA 块**：自注意力（全局建模）+ Token-Sparse 注意力（动态特征筛选），$Q \ll L$ 的稀疏化设计实现输入长度无关
2. **多粒度层次化编码**：不同窗口大小捕获多尺度时间模式，粒度内逐层压缩 + 粒度间融合
3. **跨通道稀疏编码**：通道数无关的参数量设计，支持异构传感器配置
4. **自适应标签编码器**：利用冻结 LLM 将标签文本映射到统一语义空间，实现跨数据集零样本迁移

## References

Ye, J., Zhang, W., Li, Z., Li, J., & Tsung, F. (2026). *MedSpaformer: A Transferable Transformer with Multi-Granularity Token Sparsification for Medical Time Series Classification*. Proceedings of the AAAI Conference on Artificial Intelligence, 40(33), 27791-27799. https://doi.org/10.1609/aaai.v40i33.40001

---

Written by LLM-for-Zotero.
