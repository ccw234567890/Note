---
title: "Transformer Hawkes Process"
citekey: ""
doi: ""
year: 2020
journal: ""
created: 2025-07-20
tags: [zotero, paper-note]
---

# Transformer Hawkes Process

## Summary
RMSE（Root Mean Square Error，均方根误差）是衡量预测值与真实值之间偏差的常用指标，在 Transformer Hawkes Process 论文中用于评估下一个事件发生时间的预测精度。

## Key Findings
- THP 在所有数据集上的 RMSE 均显著低于所有基线模型
- 在 MIMIC-II 数据集上，THP 的 RMSE = 0.82，而最佳基线 SAHP = 3.89，降低了近 5 倍
- RMSE 对离群的大误差特别敏感，THP 不仅平均误差小，而且几乎没有严重偏离的预测

## Methodology

### RMSE 公式

$$\text{RMSE} = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(\hat{y}_i - y_i)^2}$$

其中：
- $\hat{y}_i$ = 第 $i$ 个样本的预测值
- $y_i$ = 第 $i$ 个样本的真实值
- $n$ = 样本总数

### 计算步骤
1. **求差**：计算每个预测值与真实值的差值 $(\hat{y}_i - y_i)$
2. **平方**：消除正负号抵消的问题，同时放大较大误差
3. **求平均**：取所有平方误差的平均值
4. **开根号**：将结果恢复到与原始数据相同的量纲

### 在 THP 中的具体应用

模型预测下一个事件发生的时间：

$$\hat{t}_{j+1} = \int_{t_j}^\infty t \cdot p(t|\mathcal{H}_t)dt$$

将预测时间 $\hat{t}_{j+1}$ 与真实时间 $t_{j+1}$ 比较，计算 RMSE。

### 论文中的 RMSE 结果

| 模型 | Financial | MIMIC-II | StackOverflow |
|:----:|:---------:|:--------:|:-------------:|
| RMTPP | 1.56 | 6.12 | 9.78 |
| NHP | 1.56 | 6.13 | 9.83 |
| TSES | 1.50 | 4.70 | 8.00 |
| SAHP | — | 3.89 | 5.57 |
| **THP** | **0.93** | **0.82** | **4.99** |

### RMSE 与其他指标的区别

| 指标 | 公式 | 特点 |
|:----:|:----:|:----:|
| **MAE** | $\frac{1}{n}\sum\|\hat{y} - y\|$ | 平均绝对误差，对异常值不敏感 |
| **MSE** | $\frac{1}{n}\sum(\hat{y} - y)^2$ | 均方误差，量纲是原始数据的平方 |
| **RMSE** | $\sqrt{\text{MSE}}$ | 量纲与原始数据一致，对较大误差惩罚更重 |

论文使用 RMSE 而非 MAE 的原因：RMSE 对大误差更敏感——在事件时间预测中，偶尔出现一个严重偏离的预测比多个小误差更糟糕，RMSE 能更好地反映这种"稳定性"要求。

## My Notes
RMSE 是回归任务中最常用的评估指标之一，其平方再开方的特性使得它在量纲上与原始数据一致，便于直观理解预测误差的大小。

## References
Zuo, S., Jiang, H., Li, Z., Zhao, T., & Zha, H. (2020). *Transformer Hawkes Process*. arXiv:2002.09291v5.

---

Written by LLM-for-Zotero.
