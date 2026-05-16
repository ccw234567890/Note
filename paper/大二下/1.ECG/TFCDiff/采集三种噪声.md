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

## 三种噪声的采集方法

论文中使用的噪声数据来自 **MIT-BIH NST Database (NSTDB)**，该数据库专门用于采集纯净的三种运动噪声。其采集方法如下：

### 电极放置位置

电极被放置在人体的**大腿和手臂**上，而非胸部标准 ECG 导联位置。这种远离心脏的放置方式使得 ECG 信号本身非常微弱。

### 导联轴配置

导联轴（lead axis）被配置为**抵消 ECG 成分**。通过调整电极之间的连线方向，使得心脏电活动在正负电极上产生的电位相互抵消（类似于共模抑制），从而只记录到纯净的噪声信号。

### 采集到的三种噪声

| 噪声类型 | 英文缩写 | 来源 | 频率特征 |
|---------|---------|------|---------|
| 基线漂移 | BW (Baseline Wander) | 呼吸和身体运动 | 低频 |
| 肌肉伪迹 | MA (Muscle Artifact / EMG) | 肌肉收缩产生的肌电干扰 | 高频 |
| 电极运动伪迹 | EM (Electrode Motion Artifact) | 电极与皮肤接触变化 | 中频（介于 BW 和 MA 之间） |

### 数据规格

- **记录长度：** 1800 秒
- **通道数：** 2 通道
- **采样率：** 360 Hz
- **噪声类型：** 三种噪声分别独立记录，均为纯净噪声（不含 ECG 成分）

### 在论文中的用途

这三种纯净噪声通过论文提出的 **fRMN（灵活随机混合噪声）策略** 以随机权重组合，叠加到干净的 QT Database ECG 信号上，用于训练和测试 TFCDiff 模型。此外，**SimEMG Database** 提供了真实 EMG 污染的 ECG 信号，用于跨数据集泛化测试。

## References

Li, P., Zhou, Y., Min, J., Wang, Y., Liang, W., & Li, W. (2025). *TFCDiff: Robust ECG Denoising via Time-Frequency Complementary Diffusion*. arXiv:2511.16627 [eess]. https://doi.org/10.48550/arXiv.2511.16627

---

Written by LLM-for-Zotero.
