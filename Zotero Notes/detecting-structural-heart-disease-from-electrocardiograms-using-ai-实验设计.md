
# Detecting structural heart disease from electrocardiograms using AI

## 一、研究目标

本文旨在开发并验证一个名为 **EchoNext** 的深度学习模型，通过12导联心电图（ECG）检测结构性心脏病（SHD），并评估其在临床实践中的应用潜力。

## 二、实验设计

### 1. 数据集构建

研究团队从纽约长老会医院（NYP）系统的8家附属医院收集了2008年12月至2022年间的数据：

> We curated a dataset comprising 1,245,273 ECG–echocardiogram pairs from 230,318 unique patients (aged 18 years or above) collected between December 2008 and 2022 at one of eight NewYork–Presbyterian (NYP) affiliated hospitals

(Poterucha 等, 2025)

**数据划分**：按患者级别分为训练集（149,819名患者，796,816对）、验证集（35,780名患者，35,780对）和测试集（44,719名患者，44,719对）。

### 2. SHD定义（复合标签）

SHD被定义为以下任一条件的复合：

> low LVEF less than or equal to 45%; maximum low left ventricular wall thickness greater than or equal to 1.3 cm; moderate or severe right ventricular dysfunction; pulmonary hypertension (PASP greater than or equal to 45 mm Hg or tricuspid regurgitation jet velocity greater than or equal to 3.2 m s−1); moderate or severe aortic stenosis, aortic regurgitation, mitral regurgitation, tricuspid regurgitation or pulmonary regurgitation, or a moderate or large pericardial effusion

(Poterucha 等, 2025)

### 3. 模型架构

EchoNext采用**卷积神经网络（CNN）**，输入包括：
- 12导联ECG波形（250 Hz采样，共30,000个数据点）
- 7个标准ECG特征（年龄、性别、心房率、心室率、PR间期、QRS时限、QTc间期）

模型采用**多任务学习（multitask classifier）**架构：

> Extending previous work3, we trained EchoNext as a multitask classifier such that separate terminal branches of the model predict the presence of the SHD composite label and the presence of an individual component label

(Poterucha 等, 2025)

### 4. 验证策略

**四个层次的验证**：

| 验证层次 | 方法 | 样本量 |
|---------|------|--------|
| 内部验证 | NYP系统内8家医院 | 44,719名患者 |
| 外部验证 | 3个外部医疗中心 | 27,145名患者 |
| 静默部署验证 | 2023年1-9月新患者 | 84,875名患者 |
| 前瞻性临床试验 | DISCOVERY试验 | 100名患者 |

### 5. 与心脏病专家的对比实验

> A set of 150 ECGs was abstracted from the NYP multicentre test set with a similar SHD prevalence (41%) and age distribution (mean 67.0 ± 19.6) as the entire dataset.

(Poterucha 等, 2025)

13名心脏病专家在无AI辅助和有AI辅助两种条件下进行解读，共完成3,200次ECG解读。

## 三、核心数学原理

### 1. 模型评估指标

#### (1) AUROC（受试者工作特征曲线下面积）

AUROC衡量模型区分正负样本的能力，取值范围[0.5, 1.0]。其数学定义为：

$$AUROC = \int_{0}^{1} TPR(FPR^{-1}(t)) dt$$

其中：
- $TPR = \frac{TP}{TP + FN}$（真阳性率，即灵敏度）
- $FPR = \frac{FP}{FP + TN}$（假阳性率）

#### (2) AUPRC（精确率-召回率曲线下面积）

对于不平衡数据集更为稳健，定义为：

$$AUPRC = \int_{0}^{1} Precision(Recall^{-1}(t)) dt$$

其中：
- $Precision = \frac{TP}{TP + FP}$（精确率，即阳性预测值）
- $Recall = \frac{TP}{TP + FN}$（召回率，即灵敏度）

#### (3) 诊断优势比（Diagnostic Odds Ratio）

$$DOR = \frac{TP/FP}{FN/TN} = \frac{TP \times TN}{FP \times FN}$$

### 2. 多任务学习损失函数

模型优化采用多任务损失函数，对各标签的损失进行加权求和：

$$\mathcal{L}_{total} = \sum_{i=1}^{N} w_i \cdot \mathcal{L}_i$$

其中 $\mathcal{L}_i$ 为每个子任务的二元交叉熵损失：
$$\mathcal{L}_i = -\frac{1}{M}\sum_{j=1}^{M}[y_{ij}\log(\hat{y}_{ij}) + (1-y_{ij})\log(1-\hat{y}_{ij})]$$

### 3. 置信区间估计

采用**Bootstrap重抽样法**（1,000次）计算95%置信区间：

> For each statistical test, 95% CIs were generated using 1,000 bootstrapped estimates.

(Poterucha 等, 2025)

### 4. 阳性预测值的估计

对于静默部署中未进行超声心动图检查的患者，研究团队通过贝叶斯方法估计不同患病率下的PPV：

$$PPV = \frac{Sensitivity \times Prevalence}{Sensitivity \times Prevalence + (1-Specificity) \times (1-Prevalence)}$$

表3展示了在不同患病率和灵敏度假设下的PPV估计值。

## 四、关键实验结果

### 1. 模型性能

| 指标 | 数值 | 95%置信区间 |
|------|------|------------|
| AUROC | 85.2% | 84.5–85.9% |
| AUPRC | 78.5% | 77.2–79.6% |
| 诊断优势比 | 12.8 | 11.6–14.1 |

### 2. 与心脏病专家对比

| 组别 | 准确率 | 灵敏度 | 特异度 |
|------|--------|--------|--------|
| 心脏病专家（无AI） | 64.0% | 61.1% | 66.1% |
| 心脏病专家（有AI） | 69.2% | 64.7% | 72.4% |
| EchoNext模型 | 77.3% | 72.6% | 80.7% |

### 3. 前瞻性试验结果

DISCOVERY试验中，EchoNext将患者分为三个风险等级：

> high risk (n = 33, 24% with left-sided VHD and 73% with SHD), moderate risk (n = 50, 2% with left-sided VHD, 28% with SHD) and low risk (n = 17, 0% with left-sided VHD and 6% with SHD)

(Poterucha 等, 2025)

## 五、研究创新点

1. **复合标签策略**：将多种SHD合并为一个预测目标，提高阳性预测值
2. **多任务学习**：同时预测复合标签和各个子标签，捕捉疾病间的共线性
3. **公开数据集**：发布10万份ECG数据及模型权重，促进可重复性研究
4. **多层次验证**：从回顾性到前瞻性，从内部到外部，全面评估模型泛化能力

## 六、12导联心电图（ECG）详解

### 1. 基本概念

**12导联心电图（12-lead Electrocardiogram, ECG）** 是一种无创的心脏电生理检查方法，通过放置在体表特定位置的电极，记录心脏电活动在时间轴上的变化。

### 2. 导联系统

**肢体导联（6个）**：
- **I导联**：左上肢（+）→ 右上肢（−）
- **II导联**：左下肢（+）→ 右上肢（−）
- **III导联**：左下肢（+）→ 左上肢（−）
- **aVR**：面向右心室
- **aVL**：面向左心室高侧壁
- **aVF**：面向左心室下壁

**胸前导联（6个）**：

| 导联 | 位置 | 主要观察区域 |
|------|------|------------|
| V1 | 胸骨右缘第4肋间 | 右心室、室间隔 |
| V2 | 胸骨左缘第4肋间 | 右心室、室间隔 |
| V3 | V2与V4连线中点 | 室间隔、前壁 |
| V4 | 左锁骨中线第5肋间 | 前壁 |
| V5 | 左腋前线与V4同一水平 | 侧壁 |
| V6 | 左腋中线与V4同一水平 | 侧壁 |

### 3. 波形组成

一个完整的心动周期在ECG上表现为P波（心房除极）、QRS波群（心室除极）和T波（心室复极）。

## 七、TP、TN、FP、FN 的含义

这四个术语是**混淆矩阵（Confusion Matrix）**的核心组成部分：

| 缩写 | 英文全称 | 中文含义 | 含义解释 |
|------|---------|---------|---------|
| **TP** | True Positive | 真阳性 | 模型预测为阳性，且真实标签也是阳性（正确） |
| **TN** | True Negative | 真阴性 | 模型预测为阴性，且真实标签也是阴性（正确） |
| **FP** | False Positive | 假阳性 | 模型预测为阳性，但真实标签是阴性（错误，即"误报"） |
| **FN** | False Negative | 假阴性 | 模型预测为阴性，但真实标签是阳性（错误，即"漏报"） |

### 混淆矩阵

以本文检测结构性心脏病（SHD）为例：

| 真实情况 \ 模型预测 | 预测为SHD（阳性） | 预测为无SHD（阴性） |
|-------------------|------------------|-------------------|
| **实际有SHD（阳性）** | **TP**（正确识别） | **FN**（漏诊） |
| **实际无SHD（阴性）** | **FP**（误诊） | **TN**（正确排除） |

### 衍生指标

| 指标 | 公式 | 含义 |
|------|------|------|
| **灵敏度（Recall/TPR）** | $TP/(TP+FN)$ | 阳性样本中被正确识别的比例 |
| **特异度（TNR）** | $TN/(TN+FP)$ | 阴性样本中被正确排除的比例 |
| **精确率（Precision/PPV）** | $TP/(TP+FP)$ | 阳性预测的可靠性 |
| **准确率（Accuracy）** | $(TP+TN)/(TP+TN+FP+FN)$ | 整体预测正确率 |
| **F1分数** | $2 \times (Precision \times Recall)/(Precision + Recall)$ | 精确率和召回率的调和平均数 |
| **诊断优势比（DOR）** | $(TP \times TN)/(FP \times FN)$ | 整体区分能力 |

## 八、混淆矩阵详解

**混淆矩阵（Confusion Matrix）** 是一个 $N \times N$ 的表格（$N$ 为分类类别数），用于直观展示**分类模型预测结果**与**真实标签**之间的对比关系。矩阵的行代表真实类别，列代表预测类别。

"混淆"（Confusion）一词来源于：矩阵中的**非对角线元素**（FP 和 FN）代表了模型**混淆**（即犯错）的情况——模型把一类样本错误地分到了另一类。

混淆矩阵是**所有分类评估指标的源头**，AUROC曲线正是通过**遍历所有可能的分类阈值**，在每个阈值下计算混淆矩阵，进而得到TPR和FPR，最终绘制曲线并计算曲线下面积。

## 参考文献

Poterucha, T. J., Jing, L., Ricart, R. P., et al. (2025). *Detecting structural heart disease from electrocardiograms using AI*. Nature, 644(8075), 221–230. DOI: 10.1038/s41586-025-09227-0.

---

Written by LLM-for-Zotero.
