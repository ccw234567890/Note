
# A Comprehensive Benchmark for Electrocardiogram Time-Series

## 实验设计

### 1. 四类下游评估任务

论文将心电图的临床应用系统性地归纳为**四个标准化的评估任务**，以全面衡量模型性能：

**(a) 分类（Classification）—— 疾病诊断与事件预测**
- 输入：个体 ECG 信号 x
- 输出：对应的疾病类别标签 y
- 损失函数（交叉熵）：
  $$ \mathcal{L}_{\text{cls}} = y \log\left(\frac{\exp(\bar{e} w)}{\sum_k \exp(\bar{e} w)_k}\right) $$
  其中 $\bar{e} \in \mathbb{R}^{1 \times d}$ 是模型提取的特征 e 的均值，$w \in \mathbb{R}^{d \times c}$ 为线性投影层，c 为类别数。

**(b) 检测（Detection）—— 关键波形定位**
- 输入：ECG 信号 x
- 输出：关键波形（如 P 波、QRS 波群）的位置
- 使用非极大值抑制（NMS）算法消除冗余输出，通过 Youden's J 指数选取阈值 ε

**(c) 预测（Forecasting）—— ECG 动态预测**
- 输入：历史 ECG 片段
- 输出：未来时间段的 ECG 波形
- 使用传统时序预测损失函数：
  $$ \mathcal{L}_{\text{NTP}} = \frac{1}{n-1} \sum_{i=1}^{n-1} \frac{1}{m} \| s_{i+1} - e_i w \|^2 $$
  其中 $s_{i+1} \in \mathbb{R}^{1 \times m}$ 为第 i+1 个 token 的真实值，$e_i \in \mathbb{R}^{1 \times d}$ 为模型提取的特征。

**(d) 生成（Generation）—— 信号去噪与分离**
- 包括母胎 ECG 分离、信号去噪等任务
- 通过添加噪声构造训练数据：
  $$ \tilde{x} = x + \sqrt{P_x / (P_n 10^{\gamma/10})} \cdot n $$
  其中 $P_x = \frac{1}{t}\|x\|^2$ 为信号功率，$P_n = \frac{1}{t}\|n\|^2$ 为噪声功率，γ 为目标信噪比。

### 2. 基准构建策略

- 整合多个公开 ECG 数据集（MITDB、PTBXL、CPSC2018、SST、FEPL 等）
- 在每个任务上对比现有最先进的时序模型（Timer、Informer、Medformer 等）
- 提出专用于 ECG 的新架构 PSSM 和新指标 FFD

---

## 结果与结论

### 核心定量结果

PSSM 在四个任务上均取得最优表现：

| 对比基线 | 分类 Accuracy | 检测 F1 Score | 预测 FFD | 生成 FFD | 平均提升 |
|---------|:-----------:|:-----------:|:-------:|:-------:|:-------:|
| vs Medformer（传统方法） | +23.6% | +151.2% | +80.9% | +80.9% | **+83.4%** |
| vs Timer（大规模时序模型） | +8.1% | +28.6% | +83.8% | +78.1% | **+49.6%** |
| vs GQRS（规则方法） | — | +151.2% | — | — | — |

### 关键结论

1. **基准的全面性与鲁棒性**：四类任务构成的评估体系能有效消除单一数据集上的异常表现（如 Informer 在 CPSC2018 分类上的偶然优势），确保评估结果的可靠性。

2. **FFD 的有效性**：FFD 能正确反映 ECG 的语义保真度。当生成波形存在时间偏移时，MSE 从 0.281 急剧上升至 1.579，而 FFD 稳定保持在 0.022，说明 FFD 仅与 ECG 语义相关，对时间波动具有鲁棒性。

3. **PSSM 的优越性**：层次化编码-解码结构比通用大规模时序模型（LTMs）更适合 ECG 分析。即使 Timer*（在 ECG 上进一步预训练）也只能排第二，说明需要专门为 ECG 设计的模型架构。

4. **通用时序模型的局限性**：Transformer 在 ECG 任务上约一半的注意力权重被浪费，无法充分利用 ECG 的周期模式。

---

## 数学原理与公式推导

### 1. FFD（Feature-based Fréchet Distance）

#### 动机
![image.png](https://cc-407-1376569927.cos.ap-guangzhou.myqcloud.com/cc-407-1376569927/images-obsidian/202604281936818.png)

传统 MSE 在 ECG 评估中存在根本性缺陷：如图 1(b) 所示，保留临床有效形态但存在微小时间偏移的生成 ECG，其 MSE 反而高于一条无意义的平直线。这是因为 ECG 具有准周期性和极值特性（P 波极小值、R 波极大值），微小偏移会导致生成波形的极值与真实波形的极值错位，人为放大 MSE。

#### 定义
受图像质量评估中 Fréchet Inception Distance (FID) 的启发，FFD 在特征空间中比较真实 ECG 与生成 ECG 的分布距离。

设映射 $f: \mathbb{R}^t \to \mathbb{R}^k$ 将 ECG 信号 x 投影到特征空间，且投影后的特征服从正态分布 $e \sim \mathcal{N}(\mu, \Sigma)$。

对于真实 ECG 特征分布 $(\mu, \Sigma)$ 和生成 ECG 特征分布 $(\hat{\mu}, \hat{\Sigma})$，FFD 定义为：

$$ \text{FFD}(e, \hat{e}) = \sqrt{\frac{1}{k}} \left( \|\mu - \hat{\mu}\|^2 + \operatorname{Tr}\left( \Sigma + \hat{\Sigma} - 2(\Sigma \hat{\Sigma})^{\frac{1}{2}} \right) \right) $$

其中：
- $\|\mu - \hat{\mu}\|^2$：均值向量的欧氏距离平方，衡量分布中心偏移
- $\operatorname{Tr}(\Sigma + \hat{\Sigma} - 2(\Sigma \hat{\Sigma})^{1/2})$：协方差矩阵的 Wasserstein-2 距离，衡量分布形状差异
- $\sqrt{1/k}$：归一化因子，消除特征维度影响

#### 经验估计
实际计算中，均值和协方差通过样本估计：

$$ \tilde{\mu} = \frac{1}{N} \sum_{i=1}^N e_i, \quad \tilde{\Sigma} = \frac{1}{N-1} \sum_{i=1}^N (e_i - \tilde{\mu})^\top (e_i - \tilde{\mu}) $$

其中 N 为样本数，$e_i = f(x_i)$ 为第 i 个 ECG 样本的特征。

#### 映射 f 的训练
映射 f 使用掩码 token 预测（Mask Token Prediction）目标进行预训练：

$$ \mathcal{L}_{\text{MTP}} = \frac{1}{k} \sum_i \frac{1}{m} \| s_i - e_i w \|^2 $$

其中 $s_i$ 为第 i 个掩码 token 的真实值，$e_i \in \mathbb{R}^{1 \times d}$ 为模型提取的特征，$w \in \mathbb{R}^{d \times m}$ 为线性投影层。

掩码数量 $n_m$ 的采样策略：
$$ n_m = \begin{cases} 0.5n & p \leq 0.5 \\ U(n/4, 3n/4) & p > 0.5 \end{cases} $$
其中 $p \sim U(0,1)$，即一半概率掩码 50% 的 token，另一半概率从 $n/4$ 到 $3n/4$ 均匀采样。

---

### 2. PSSM（Patch Step-by-Step Model）架构

PSSM 采用层次化编码器-解码器结构，专门为 ECG 信号的准周期特性设计。

#### 编码器（Patching Encoder）

ECG 信号 x 先经过嵌入层，再经过 l 层层次化 Patch 操作：

$$ e_1 = \text{Embedding}(x) $$
$$ e_{i+1} = \text{ConvBlock}_i(\text{Patch}(e_i)) $$

其中：
- 嵌入层将 $x \in \mathbb{R}^{t \times 1}$ 映射到 $e_1 \in \mathbb{R}^{t \times d}$
- Patch 层将 $e_i \in \mathbb{R}^{(t/2^{i-1}) \times (2^{i-1}d)}$ 分割为 patches：
  $$ \text{Patch}(e_i) = \{(e_i^{2k-1} + e_i^{2k})/2\} $$
  即相邻两个时间步的特征取平均，时间分辨率减半
- ConvBlock 将隐藏维度加倍，输出 $e_{i+1} \in \mathbb{R}^{(t/2^i) \times (2^i d)}$

#### 解码器（Unpatching Decoder）

解码器执行 l 层逆 Patch 操作：

$$ e_{i+1} = \text{ConvBlock}_i(\text{UnPatch}(e_i)) $$
$$ e = e_{2l+1} w $$

其中 $i = l+1, \ldots, 2l$ 为解码器层数，$w$ 为线性投影层。

**UnPatch 层** 通过可学习的加权复制实现上采样：

$$ (e_{i+1}^{2k-1}, e_{i+1}^{2k}) = (\text{ConvBlock}_i(c_1 e_i^k), \text{ConvBlock}_i(c_2 e_i^k)) $$

其中 $c_1, c_2$ 为可学习参数，ConvBlock 将隐藏维度减半。

**原理**：同一特征 $e_i^k$ 通过两条不同权重的分支 $(c_1, c_2)$ 分别经过卷积块，生成两个新的特征向量，从而将时间分辨率加倍。可学习参数 $c_1, c_2$ 使得上采样过程能自适应 ECG 信号的局部形态特征，而非简单的线性插值。

---

### 3. 检测任务中的 NMS 算法

检测任务使用非极大值抑制（NMS）来消除冗余的波形检测结果：

**输入**：波形概率序列 $S \in \mathbb{R}^t$，阈值 $\tau$
**输出**：保留的波形概率 $S_{\text{retain}}$

算法步骤：
1. 对 S 按降序排列，得到索引序列 I
2. 排除零概率位置
3. 循环选择当前最高概率位置，抑制其 $\tau$ 邻域内的所有候选
4. 最终输出保留位置集合

最终检测结果：
$$ \hat{y} = \{i \mid \text{NMS}(\sigma(e w))_i > \varepsilon\} $$
其中 $\sigma$ 为 sigmoid 函数，$\varepsilon$ 为通过 Youden's J 指数选取的阈值。

---

## 参考文献

Tang, Z., Qi, J., Zheng, Y., & Huang, J. (2025). *A Comprehensive Benchmark for Electrocardiogram Time-Series*. Proceedings of the 33rd ACM International Conference on Multimedia (MM '25), Dublin, Ireland, pp. 6490-6499. DOI: 10.1145/3746027.3754729.

---

Written by LLM-for-Zotero.
