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
本文提出 PPGFlowECG，两阶段框架解决 PPG→ECG 生成中的语义错位与高维流形不平滑问题。Stage 1 的 CardioAlign Encoder 通过共享编码器与三类约束（全局分布对齐、局部实例判别、跨模态解码）把 PPG 与 ECG 映射到统一潜在空间；Stage 2 的 Latent Rectified Flow 在该潜在空间里，以 PPG 潜在表示为条件，从高斯噪声沿直线轨迹生成 ECG 潜在向量，再由冻结解码器还原波形，实现更稳定、更具生理语义的合成。

## Key Findings
- CardioAlign Encoder 利用重参数化采样 (式 1) 和分布对齐损失 $L_{GDA}$ (式 3) 使 $z_{ppg}$ 与 $z_{ecg}$ 在统计上接近，同时 InfoNCE 风格的 $L_{LID}$ 保留受试者判别性，语义可解码损失 $L_{SDC}$ 则强制跨模态互译。
- 潜在修正流通过线性插值路径 $x_t=(1-t)z+ty$ (式 7) 学习条件速度场 $v_\theta$，训练目标 (式 8) 直接回归最优漂移 $y-z$，推理时解显式 ODE (式 9–10) 即可得到 ECG 潜在表示。
- 形式化分析表明 Stage 1 降低条件分散度 $\bar{\kappa}$ (式 11)，进而压低 Stage 2 的贝叶斯风险下界 $R_{min}\le \bar{\kappa}$ (式 12)；当 $\bar{\kappa}\to 0$ 时，轨迹曲率 $x_t^{(2)}$ 近零，允许极少的 ODE 步数仍保持稳定生成。

## Methodology
Stage 1：对任意模态 $x_m$，共享编码器输出 $(\mu_m,\sigma_m)$ 并按式 (1) 进行重参数化采样；$L_{GDA}$ 拉近均值并对称匹配后验分布，$L_{LID}$ 采用双向 InfoNCE 限制正负样本距离，$L_{SDC}$ 以跨模态重建误差确保潜在表示具备互译语义，整体损失如式 (6)。Stage 2：将条件 $c=z_{ppg}$ 输入条件化 Transformer 向量场，采样 $z\sim\mathcal{N}(0,I)$，构造直线路径 $x_t$ 并最小化式 (8) 中的 MSE。推理时采用步长 $\Delta t=1/T$ 的显式欧拉法更新式 (10)，得到 $x_T$ 后用 ECG 解码器重建。

## My Notes
- CardioAlign Encoder 实质类似跨模态 VAE+对比学习混合体，在保持跨模态语义的同时避免 collapse；其中 $L_{SDC}$ 让共享潜在空间具备“即插即用”的条件语义。
- Rectified Flow 的优势在于最优漂移恒定，避免扩散模型需大量时间步的噪声调度；理论分析强调 Stage 1 减小条件方差以保障 Stage 2 的线性可传输性。
- 实践中，只需少量 ODE 步即可逼近线性轨迹，说明在 CardioAlign 之后潜在流形确实被“平滑化”。未来可尝试把 Stage 1 的潜在对齐用于其它跨模态生理信号（如 PPG→脉搏波速度）。

## References
Fang, X., Jin, J., Wang, H., Liu, C., Cai, J., Xiao, Y., Nie, G., Liu, B., Huang, S., Li, H., & Hong, S. (2026). *PPGFlowECG: Latent Rectified Flow with Cross-Modal Encoding for PPG-Guided ECG Generation and Cardiovascular Disease Detection*. arXiv preprint arXiv:2509.19774. https://doi.org/10.48550/arXiv.2509.19774

---

Written by LLM-for-Zotero.
