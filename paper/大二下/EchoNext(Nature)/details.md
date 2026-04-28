
# Detecting structural heart disease from electrocardiograms using AI

## 一、关键术语解析

### 1. SHD（Structural Heart Disease，结构性心脏病）

> SHD encompasses pathologies that affect the valves, walls or chambers of the heart, including valvular heart disease (VHD), right- and left-sided heart failure, pulmonary hypertension and left ventricular hypertrophy.

(Poterucha 等, 2025)

**表征**：SHD 是一个复合临床概念，涵盖一系列影响心脏瓣膜、心肌壁或心腔的结构性异常。在当前研究中，SHD 的操作性定义是以下任一条件存在：

> LV ejection fraction (LVEF) ≤ 45%; maximum LV wall thickness ≥ 1.3 cm; moderate or severe right ventricular dysfunction; pulmonary hypertension (PASP ≥ 45 mmHg or TR jet velocity ≥ 3.2 m/s); moderate or severe aortic stenosis, aortic regurgitation, mitral regurgitation, tricuspid regurgitation, or pulmonary regurgitation; or a moderate or large pericardial effusion.

(Poterucha 等, 2025)

**临床意义**：SHD 是进展性、高负担的疾病，在美国每年直接和间接成本超过 1000 亿美元，心衰和 VHD 分别影响约 6400 万和 7500 万人，且严重未诊断。例如，在 65 岁以上人群中，VHD 的诊断率仅为 4.9%，而实际患病率超过 11%。

### 2. VHD（Valvular Heart Disease，瓣膜性心脏病）

**表征**：VHD 是 SHD 的一个子集，特指心脏瓣膜的结构或功能异常，包括主动脉瓣狭窄（AS）、主动脉瓣反流（AR）、二尖瓣反流（MR）、三尖瓣反流（TR）、肺动脉瓣反流（PR）等中度及以上程度的病变。本文中，VHD 被包含在 SHD 的复合标签中，也是 DISCOVERY 试验的主要终点。

### 3. AUROC（Area Under the Receiver Operating Characteristic Curve，受试者工作特征曲线下面积）

**表征**：AUROC 衡量模型在所有可能阈值下将正样本（患病）排在负样本（未患病）前面的概率，反映模型**整体区分能力**。AUROC 越接近 1 表示区分度越好，0.5 为随机猜测。

数学定义：

$$AUROC = \int_{0}^{1} TPR(FPR^{-1}(t)) dt$$

其中：
- $TPR = Sensitivity = \frac{TP}{TP + FN}$
- $FPR = 1 - Specificity = \frac{FP}{FP + TN}$

**优势**：对类别不平衡不敏感，适合全局评估。

### 4. AUPRC（Area Under the Precision-Recall Curve，精确率-召回率曲线下面积）

**表征**：AUPRC 在 Precision-Recall 平面上计算曲线下面积，特别关注**正样本（患病）的预测准确性**。当正样本很少时，AUPRC 比 AUROC 更能反映模型真实性能。

$$AUPRC = \int_{0}^{1} Precision(Recall^{-1}(t)) dt$$

其中：
- $Precision = \frac{TP}{TP + FP}$
- $Recall = TPR$

**本文中**：因为某些 SHD 子类（如肺动脉反流、心包积液）患病率极低，AUPRC 随患病率变化显著，所以论文强调 AUPRC 的评估。

### 5. DOR（Diagnostic Odds Ratio，诊断优势比）

**表征**：DOR 是衡量模型区分能力的单一指标，表示正样本被正确诊断的几率与负样本被误诊的几率之比。DOR 越大，模型区分度越好。

$$DOR = \frac{TP/FP}{FN/TN} = \frac{TP \times TN}{FP \times FN}$$

**本文中**：模型在阈值为 0.5 时，DOR = 12.8，表示真阳性患者的阳性几率是假阳性几率的 12.8 倍。

---

## 二、Fig.2 – 多中心 EchoNext 性能

### 实验设计
Fig.2 展示了 EchoNext 在内部和外部测试集上的性能。内部测试集来自纽约长老会系统八家医院（NYP test set），外部测试集包括三个地理上独立的数据集：蒙特利尔心脏研究所、西达赛奈医疗中心和加州大学旧金山分校。

### 结果

**(a) 内部和外部验证的 AUROC：**

> The model had high performance in detection of SHD in the internal eight-hospital NYP system test set and three geographically distinct external test sets

(Poterucha 等, 2025)

四个测试集的 AUROC 分别为：
- EchoNext test (NYP): 约 85%
- Montreal: 约 84%
- Cedars-Sinai: 约 82%
- UCSF: 约 79%

**(b) 内部和外部验证的 AUPRC：**
AUPRC 分别为：
- EchoNext test: 78.5
- Montreal: 80.4
- Cedars-Sinai: 79.8
- UCSF: 77.7

**(c) 各 SHD 子类的 AUROC：**
分别展示了下列疾病状态的 AUROC：

| 疾病 | AUROC (约) |
|------|------------|
| LVEF ≤ 45% | 90.4 |
| 右心室功能障碍 | 90.8 |
| 主动脉瓣狭窄 | 86.4 |
| 三尖瓣反流 | 86.7 |
| 二尖瓣反流 | 85.4 |
| PASP ≥ 45mmHg | 82.7 |
| TR_vmax ≥ 3.2 m/s | 84.8 |
| 心包积液 | 79.9 |
| 主动脉瓣反流 | 77.7 |
| 肺动脉反流 | 78.5 |
| LV 壁厚度 ≥ 13 mm | 77.2 |

**(d) 各子类的 AUPRC：**
由于患病率差异，AUPRC 波动较大：
- LVEF ≤ 45%: 64.7
- 右心室功能障碍: 40.5
- PASP ≥ 45: 43.6
- 主动脉瓣狭窄: 26.3
- 二尖瓣反流: 28.2
- 三尖瓣反流: 34.2
- 主动脉瓣反流: 5.6
- 肺动脉反流: 2.4
- 心包积液: 3.0

### 结论
EchoNext 在不同人群和医疗系统中表现一致，对左心和右心收缩功能障碍的检测能力最强，对低患病率的瓣膜病 AUPRC 较低但 AUROC 仍保持良好。外部验证证明了模型的泛化能力。

---

## 三、Fig.3 – DISCOVERY 前瞻性临床试验结果

### 实验设计

> To test the model's ability to detect clinically significant cardiac disease, we designed the DISCOVERY trial, which was a 100-patient open-label stratified sampling prospective trial recruiting patients on the basis of their ValveNet risk score.

(Poterucha 等, 2025)

纳入标准：成年患者，曾在哥伦比亚大学进行数字化 12 导联 ECG，近 3 年无超声心动图记录，无左心 VHD 病史，无预期寿命 < 1 年的严重非心脏疾病。
按 ValveNet 评分预定义三等分位（低、中、高），排除极低风险组。最终纳入 100 名患者，进行超声心动图检查。

主要终点：检测中度及以上主动脉瓣狭窄、主动脉瓣反流或二尖瓣反流（左心 VHD）。
次要终点：检测全部临床显著 SHD（使用与 EchoNext 相同的定义）。

### 结果
**按风险组分层：**
- 高风险组 (n=33)：左心 VHD 检出率 24%，SHD 检出率 73%
- 中等风险组 (n=50)：左心 VHD 检出率 2%，SHD 检出率 28%
- 低风险组 (n=17)：左心 VHD 检出率 0%，SHD 检出率 6%

### 结论
AI-ECG 风险分层能够有效识别没有近期心脏影像检查的患者中的未诊断结构性心脏病。高风险组中有近四分之三的患者存在 SHD，验证了模型在真实世界前瞻性环境中的临床应用潜力。

---

## 四、Fig.4 – 与心脏病专家的对比及人机合作

### 实验设计

> A set of 150 ECGs was abstracted from the NYP multicentre test set... Each cardiologist was presented with a block of 50 ECGs and were asked to answer... whether the patient was likely to have SHD... After completion... they were given the same 50 ECGs with the addition of the AI model analysis.

(Poterucha 等, 2025)

150 份 ECG（SHD 患病率 41%，平均年龄 67 岁），13 名心脏病专家分两轮解读：第一轮无 AI 辅助，第二轮有 AI 提供模型输出分数和解释。

### 结果

| 组别 | 准确率 | 灵敏度 | 特异度 |
|------|--------|--------|--------|
| 心脏病专家（无 AI） | 64.0% | 61.1% | 66.1% |
| 心脏病专家（有 AI） | 69.2% | 64.7% | 72.4% |
| EchoNext 模型单独 | 77.3% | 72.6% | 80.7% |

### 结论
AI 模型的独立表现优于心脏病专家，且 AI 辅助能显著提高心脏病专家的诊断准确性和特异度，证实了人机协同的增益效果。

---

## 五、EchoNext 模型架构

EchoNext 是一个**多任务卷积神经网络**，输入为原始 ECG 波形和少量结构化特征。

### 1. 输入
- **ECG 波形**：12 导联 × 250 Hz × 10 秒 = 12 × 2500 = 30,000 个采样点，作为一维或二维数组输入 CNN。
- **标准 ECG 测量值**：心室率、PR 间期、QRS 时限、QTc 间期、电轴等，以及年龄（截断至 90 岁以上设为 90）、性别。

### 2. 网络结构
> EchoNext was trained as a multitask classifier such that separate terminal branches of the model predict the presence of the SHD composite label and the presence of an individual component label.

(Poterucha 等, 2025)

具体结构未在提供的片段中详细描述，但基于前身 ValveNet 和典型设计，推测为：
- 特征提取器：堆叠的一维或二维卷积层 + 池化层，从波形中自动学习局部/全局模式。
- 全连接层：将提取的波形特征与 ECG 测量值和人口学特征拼接后输入。
- 输出层：多个 sigmoid 二分类头，分别对应：
  - SHD 复合标签
  - LVEF ≤ 45%
  - LV 壁厚度 ≥ 13 mm
  - 中度或重度 AS、AR、MR、TR、PR
  - 右心室功能障碍
  - 心包积液
  - PASP ≥ 45 mmHg (TR jet velocity ≥ 3.2 m/s)

### 3. 多任务学习策略
共享底层表示，每个任务有独立的分类头，共同优化多任务损失函数。

---

## 六、数学原理及推导

### 1. 多任务损失函数

假设有 $K$ 个任务，每个任务的二元标签为 $y_k \in \{0,1\}$，模型预测为 $\hat{y}_k \in [0,1]$。

**单任务二元交叉熵损失**：

$$\mathcal{L}_k = -[y_k \log(\hat{y}_k) + (1-y_k) \log(1-\hat{y}_k)]$$

**多任务总损失**为各任务损失的加权和：

$$\mathcal{L}_{total} = \sum_{k=1}^{K} w_k \cdot \mathcal{L}_k$$

权重 $w_k$ 可通过等权、根据样本数量或训练中动态调整（如不确定性加权）。本文可能对所有任务采用等权或基于类别平衡的调整。

### 2. AUROC 的数学推导

给定分类阈值 $\tau$，定义：
- $TPR(\tau) = \frac{TP}{P}$  （P 为正样本总数）
- $FPR(\tau) = \frac{FP}{N}$  （N 为负样本总数）

ROC 曲线是以 $FPR$ 为横坐标，$TPR$ 为纵坐标，遍历 $\tau$ 从 1 到 0 的所有点连线。

AUROC 可表示为 Wilcoxon-Mann-Whitney 统计量：

$$AUROC = \frac{1}{P \cdot N} \sum_{i \in \text{Pos}} \sum_{j \in \text{Neg}} \mathbb{I}(s_i > s_j)$$

其中 $\mathbb{I}$ 是指示函数，$s_i, s_j$ 为模型对正负样本的分数。此公式意味着 AUROC 等于随机抽取一对正负样本，模型给正样本打分高于负样本打分的概率。

### 3. AUPRC 的数学推导

对于每个可能召回率水平 $r \in [0,1]$，Precision 作为召回率的函数 $Prec(r)$。AUPRC 为：

$$AUPRC = \int_{0}^{1} Prec(r) dr$$

由于 Precision 和 Recall 都是基于排序阈值的离散点，实际计算常用平均精确率（Average Precision, AP）：

$$AP \approx \sum_{k=1}^{n} (Recall_k - Recall_{k-1}) \cdot \max_{i \ge k} Precision_i$$

这里 $n$ 是所有预测分数排序后的唯一分数点，$Recall_k$ 和 $Precision_k$ 是第 $k$ 个阈值点对应的值。该方法计算曲线下面积的插值近似，避免小阈值波动影响。

### 4. DOR 的推导

DOR 直接由混淆矩阵定义：

$$DOR = \frac{TP/FN}{FP/TN} = \frac{TP \cdot TN}{FP \cdot FN}$$

其对数值与 ROC 曲线下某些点对应。DOR 不依赖患病率，可综合灵敏度和特异度。置信区间通过 bootstrap 重采样 1000 次获得：

$$\text{CI} = \text{Percentile}_{2.5\% \sim 97.5\%} \text{ of bootstrap DOR distribution}$$

### 5. PPV 估计的贝叶斯框架（静默部署）

在静默部署中，未行超声的患者无法直接计算 PPV，但可利用已知的灵敏度和特异度，结合假定的不同患病率（prevalence）估计：

$$PPV = \frac{Sensitivity \times Prevalence}{Sensitivity \times Prevalence + (1 - Specificity) \times (1 - Prevalence)}$$

此公式衍生自贝叶斯定理。论文中通过变化患病率假设，给出了模型在不同筛查场景下的 PPV 范围（见 Table 3），以评估临床效用。

---

## 七、总结

| 要素 | 说明 |
|------|------|
| **AUROC** | 测量模型整体区分能力，不受患病率影响 |
| **AUPRC** | 突出对阳性患者的预测精度，对罕见病更敏感 |
| **DOR** | 单一比值指标综合灵敏度和特异度 |
| **VHD** | 瓣膜性心脏病，SHD 的重要子集 |
| **SHD** | 结构性心脏病，本研究的复合预测目标，涵盖心衰、瓣膜病、肺高压等 |
| **Fig.2** | 内部和外部多中心验证，模型跨系统稳定 |
| **Fig.3** | DISCOVERY 前瞻性试验，AI 分层有效发现未诊断 SHD |
| **Fig.4** | 人机对比，AI 独立优于专家，辅助后显著提升专家表现 |
| **架构** | 多任务 CNN，输入原始 12 导联 ECG + 结构化特征，多个 sigmoid 分类头 |
| **数学原理** | 多任务二元交叉熵、AUROC/AUPRC 积分与插值、DOR 及其 Bootstrap CI、贝叶斯 PPV 估计 |

## References
Poterucha, T. J., Jing, L., Ricart, R. P., et al. (2025). Detecting structural heart disease from electrocardiograms using AI. *Nature*, 644(8075), 221–230. https://doi.org/10.1038/s41586-025-09227-0

---

Written by LLM-for-Zotero.
