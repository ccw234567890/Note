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

## Summary
本文提出 PPGFlowECG，一个两阶段框架，通过 CardioAlign Encoder 在共享潜在空间中对齐 PPG 和 ECG，然后使用潜在修正流（Latent Rectified Flow）合成 ECG。该方法解决了现有生成方法中生理语义错位和高维信号建模复杂性的问题，在四个数据集上实现了最先进的合成保真度和下游诊断性能。

## Key Findings
- **重建质量**：在 MCMED 数据集上 MAE 0.73（↓22.3% vs 最佳基线）、FID 12.84（↓38.3%）
- **心率估计**：合成 ECG 的心率估计 MAE 为 1.80，比直接从 PPG 估计降低 16.7%
- **疾病检测**：MCMED 多标签分类 Macro-AUROC 0.631（比最强 PPG 基线提升 19.1%）；MIMIC-AFib 检测 Acc=0.82, F1=0.87
- **临床图灵测试**：5 位心脏病专家无法可靠区分合成与真实 ECG（识别准确率接近随机水平）
- **诊断实用性**：PPG + 合成 ECG 的诊断准确率（0.87）接近 PPG + 真实 ECG（0.89）

## Methodology
- **Stage 1 — CardioAlign Encoder**：共享编码器输出均值和标准差，通过重参数化技巧采样潜在变量；三层次对齐损失（全局分布对齐 L_GDA + 局部实例判别 L_LID + 语义可解码性约束 L_SDC）
- **Stage 2 — Latent Rectified Flow**：在潜在空间中学习条件向量场，将高斯噪声通过直线路径传输到 ECG 潜在表示；使用显式欧拉求解器，仅需 5-10 步 ODE 求解
- **理论贡献**：证明 Stage 1 的对齐直接降低 Stage 2 流学习的不可约贝叶斯风险下界，并提高数值稳定性

## My Notes
- 两阶段耦合的形式化分析是本文最重要的理论贡献——证明了 CardioAlign Encoder 对稳定合成是必要的
- 潜在空间中的修正流比原始波形空间更有效，因为对齐后的潜在空间流形更平滑、更线性
- T=5 时性能最佳，说明直线路径的数值误差极小
- 零样本迁移实验（MCMED→MIMIC-AFib）支持实际部署可行性

## References
Fang, X., Jin, J., Wang, H., Liu, C., Cai, J., Xiao, Y., Nie, G., Liu, B., Huang, S., Li, H., & Hong, S. (2026). *PPGFlowECG: Latent Rectified Flow with Cross-Modal Encoding for PPG-Guided ECG Generation and Cardiovascular Disease Detection*. arXiv:2509.19774 [cs]. DOI: 10.48550/arXiv.2509.19774.

---

Written by LLM-for-Zotero.
