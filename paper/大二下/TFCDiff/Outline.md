---
title: "TFCDiff: Robust ECG Denoising via Time-Frequency Complementary Diffusion"
citekey: ""
doi: "10.48550/arXiv.2511.16627"
year: 2025
journal: ""
created: 2026-05-06
tags: [zotero, paper-note]
---

# TFCDiff: Robust ECG Denoising via Time-Frequency Complementary Diffusion

## Summary
本文提出 TFCDiff，一种在离散余弦变换（DCT）域中运行的条件扩散模型，用于去除可穿戴设备采集的 ECG 信号中的混合运动噪声（基线漂移 BW、肌肉伪迹 MA、电极运动伪迹 EM）。通过引入时域特征增强机制（TFEM）动态整合时频表征，在五项评估指标上达到 SOTA，并展现出优异的跨数据集泛化能力。

## Key Findings
- TFCDiff-10（10次生成取平均）在所有五项指标上超越所有基准方法，SSD = 21.522 ± 57.303，CosSim = 0.957 ± 0.055，ImSNR = 14.100 ± 4.172
- TFCDiff-1（单次生成）已超越多数基准方法，SSD 比 DesCod-10 降低 52.25%
- 在最强噪声区间（λ=1.5–2.0）下，TFCDiff-10 的 SSD = 34.59，远优于 TCDAE 的 40.65
- 在 SimEMG 跨数据集测试中，TFCDiff-1 在所有指标上超越 DesCod-10，展现了极强的泛化能力
- TFCDiff-1（0.167s）仅需 DesCod-10（0.805s）约 1/5 的时间，即可达到更优性能

## Methodology
### 核心架构
1. **DCT 域扩散模型**：将 ECG 信号通过 DCT 变换到频域，截断保留前 1000 个系数（覆盖 0.5–50 Hz 诊断频段），在频域执行条件扩散去噪
2. **TFEM 时域特征增强机制**：
   - TFE（Temporal Feature Extraction）：DCT 域特征 → IDCT 转时域 → 残差块处理 → DCT 转回频域
   - TFF（Temporal Feature Fusion）：在编码器中间层通过跨域注意力融合时频异构表征
3. **fRMN 灵活随机混合噪声策略**：随机权重组合 BW、MA、EM 三种噪声，模拟真实运动场景

### 数学基础
- DCT Type-II 正/逆变换公式
- 条件扩散模型前向/反向过程（公式 3–8）
- DCT 系数缩放（公式 9）
- SNR 缩放与噪声调度（公式 10–13）
- FiLM 条件注入（公式 15）
- 五项评估指标：SSD、MAD、PRD、CosSim、ImSNR（公式 17–21）

### 实验设置
- 数据集：QT Database（干净 ECG）+ MIT-BIH NST（噪声源）+ SimEMG Database（跨数据集泛化测试）
- 输入长度：3600 采样点（10 秒，360 Hz）
- 对比方法：8 种基准（FIR、IIR、FCN-DAE、DRNN、DeepFilter、CBAM-DAE、TCDAE、DesCod）
- 训练：Adam 优化器，400 epoch，batch size 128

## My Notes
- 本文的核心创新在于将扩散模型从时域迁移到 DCT 频域，利用 DCT 的能量集中特性大幅降低计算量，同时通过 TFEM 弥补频域建模丢失的时域细节
- 处理 10 秒长序列而非单心跳，避免了手动分割标注的需求，更贴近实际应用场景
- 消融实验清晰展示了 DCT 扩散与 TFEM 的协同效应：纯 DCT 扩散能重建 T 波形态但产生伪迹，加入 TFEM 后大幅提升质量
- 跨数据集泛化能力是本文的一大亮点，在未见过的真实 EMG 污染数据上仍保持领先

## References
Li, P., Zhou, Y., Min, J., Wang, Y., Liang, W., & Li, W. (2025). *TFCDiff: Robust ECG Denoising via Time-Frequency Complementary Diffusion*. arXiv:2511.16627 [eess]. https://doi.org/10.48550/arXiv.2511.16627

---

Written by LLM-for-Zotero.
