---
title: "$π_0$: A Vision-Language-Action Flow Model for General Robot Control"
citekey: ""
doi: "10.48550/arXiv.2410.24164"
year: 2026
journal: ""
created: 2025-07-18
tags: [zotero, paper-note]
---

# $π_0$: A Vision-Language-Action Flow Model for General Robot Control

## Summary
π₀ 是一个基于流匹配（Flow Matching）的视觉-语言-动作（VLA）基础模型，建立在预训练的 PaliGemma VLM 之上。它通过引入"动作专家"（Action Expert）架构，让 VLM 继续处理视觉和语言理解，同时用一组专门的 Transformer 权重处理连续动作生成，实现了 50 Hz 的高频灵巧操控。

## Key Findings
- 在 10,000+ 小时、7 种机器人构型、68 个任务的数据上预训练，具备零样本泛化能力
- 在折叠衣物、清理桌面、组装盒子等 20+ 个灵巧操控任务上超越 OpenVLA 等基线模型
- 结合高层语义策略（π₀-HL）可完成复杂的长时域多步骤任务
- 流匹配架构相比自回归离散化架构具有更高的精度和多模态建模能力

## Methodology

### 核心架构：双专家 MoE Transformer

π₀ 在标准 VLM 基础上新增一组专门的 Transformer 权重（动作专家），形成双专家混合专家（MoE）架构：

- **专家 1（VLM 骨干）**：PaliGemma 2B，配置 `{width=2048, depth=18, mlp_dim=16384, num_heads=18, num_kv_heads=1, head_dim=256}`，处理图像和文本令牌
- **专家 2（动作专家）**：约 300M 参数，配置 `{width=1024, mlp_dim=4096}`，处理状态和动作令牌
- 两个专家在自注意力层中交互，但 FFN 层由各自专家独立计算

### 流匹配（Flow Matching）

训练时，从标准高斯分布采样噪声 $\epsilon \sim \mathcal{N}(0, I)$，构造带噪声动作 $A_t^\tau = \tau A_t + (1-\tau)\epsilon$，训练向量场 $v_\theta(A_t^\tau, o_t)$ 逼近去噪向量场 $u(A_t^\tau | A_t) = A_t - \epsilon$：

$$L_\tau(\theta) = \mathbb{E}_{p(A_t|o_t), q(A_t^\tau | A_t)} \left\| v_\theta(A_t^\tau, o_t) - (A_t - \epsilon) \right\|^2$$

推理时，从纯噪声 $A_t^0 \sim \mathcal{N}(0, I)$ 出发，通过 10 步欧拉积分逐步去噪：

$$A_t^{\tau+\delta} = A_t^\tau + \delta \cdot v_\theta(A_t^\tau, o_t), \quad \delta=0.1$$

### 动作分块（Action Chunking）

一次性预测未来 $H=50$ 个时间步的动作块 $A_t = [a_t, a_{t+1}, \dots, a_{t+H-1}]$，实现 50 Hz 高频控制。

### 分块因果注意力掩码

输入序列分为 3 个块：`[图像, 文本]`、`[状态]`、`[动作]`。块内全双向注意力，块间因果（只能看前面的块），最小化与 VLM 预训练的分布偏移。

### 三种评估方式

1. **开箱即用**：零样本，直接通过自然语言指令执行任务
2. **微调**：使用下游任务数据有监督微调
3. **高层语义策略（π₀-HL）**：结合独立的高层 VLM 将复杂任务分解为中间语言指令，由 π₀ 逐个执行

## My Notes

### 电子信息工程视角解读

1. **向量场 → 模拟电路微分方程**：向量场 $v_\theta$ 描述了噪声动作随流匹配时间步 $\tau$ 的"变化率"，类似于电容的电压-电流关系 $i = C\frac{dv}{dt}$。数值积分相当于用欧拉法求解常微分方程。

2. **噪声 → 通信系统中的热噪声**：流匹配过程相当于一个最优滤波器，从被噪声污染的"信号"中恢复出干净的原始信号，与维纳滤波或卡尔曼滤波思想相通。

3. **目标动作块 → 数字信号处理中的输出帧**：类似音频编码器一次处理一帧 PCM 数据，π₀ 一次生成一帧（50 个时间步）的动作指令，充分利用并行计算优势。

4. **数-模转换**：从离散的多模态符号（图像 patches、语言 tokens）到连续模拟量（动作向量）的直接映射通路，避免了离散动作空间带来的量化误差。

5. **FFN 层 → 非线性信号处理**：FFN 的"扩展-激活-压缩"结构类似于稀疏编码——先将输入投影到高维空间（16384 维），在高维空间中用 GeLU 激活进行稀疏激活，再投影回低维空间。

### 关键设计洞察

- **共享前缀 KV Cache**：流匹配推理需要 10 步积分，通过缓存图像和文本的 K/V 向量，后续 9 步只需处理动作令牌，推理速度提升约 5-10 倍
- **动作专家缩小化**：动作专家配置为 `{width=1024, mlp_dim=4096}`（约 300M 参数），远小于 VLM 骨干的 2B 参数，这是为了加速推理（需要多次前向传播）
- **VLM 理解世界 + 动作专家操控世界**：两者通过共享注意力层紧密耦合，但参数互不干扰

## References
Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., Jakubczak, S., Jones, T., Ke, L., Levine, S., Li-Bell, A., Mothukuri, M., Nair, S., Pertsch, K., Shi, L. X., … Zhilinsky, U. (2026). *$π_0$: A Vision-Language-Action Flow Model for General Robot Control*. arXiv:2410.24164 [cs]. https://doi.org/10.48550/arXiv.2410.24164

---

Written by LLM-for-Zotero.
