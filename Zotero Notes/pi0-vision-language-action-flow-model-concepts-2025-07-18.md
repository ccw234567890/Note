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

## 核心概念讲解

本文整理了关于 π₀ 模型中几个关键概念的详细讲解，涵盖 Flow Matching、PaliGemma、跨形态训练与动作分块架构。

---

### 1. Flow Matching（流匹配）

**核心作用**：直接对机器人的连续动作分布进行建模与生成，输出高精度、高频的连续动作指令，而非将动作离散化为文本令牌。

> Flow matching provides our model with high precision and multimodal modeling capability, making it especially well suited to high-frequency dexterous tasks.

(Black et al., 2026)

**技术原理**：
- 训练一个向量场 $v_\theta$，将简单噪声分布 $A_t^0 \sim \mathcal{N}(0, I)$ 沿概率路径逐步演变到目标动作块 $A_t = [a_t, a_{t+1}, \dots, a_{t+H-1}]$ 的分布。
- 训练损失函数：$L_\tau(\theta) = \mathbb{E}_{p(A_t|o_t), q(A_t^\tau | A_t)} \left\| v_\theta(A_t^\tau, o_t) - u(A_t^\tau | A_t) \right\|^2$
- 推断时从纯噪声出发，通过解常微分方程逐步积分向量场，积分步长 $\delta=0.1$（10步积分），以 **50 Hz** 频率控制机器人。

**从电子信息工程视角理解**：
- **离散输入**：图像令牌（ViT 编码）、语言令牌、本体感知状态 $q_t$（线性投影至嵌入空间）。
- **连续输出生成器**：动作专家（action expert）将自身视为连续函数逼近器，输入噪声动作 $A_t^\tau$ 和观测 $o_t$，输出向量场 $v_\theta$，全程在实数域 $\mathbb{R}^d$ 内运行。
- **从噪声到指令的"数-模转换"**：纯高斯噪声 → 数值积分 $A_t^{\tau+\delta} = A_t^\tau + \delta\, v_\theta(A_t^\tau, o_t)$ → 连续关节角度/末端位姿指令。
- 相当于将传统数字通信系统中的"信源编码+调制"反向应用：从高维离散语义"信源"出发，直接"调制"出物理世界的连续控制波形。

---

### 2. PaliGemma 作为多模态 LLM

PaliGemma 是一个典型的**多模态 LLM（视觉语言模型，VLM）**，其核心架构包括：
- **视觉编码器**：从图像提取视觉特征。
- **大语言模型解码器**：处理视觉和文本令牌，生成语言输出。

> Our model, which we describe in Section IV, is based on the PaliGemma vision-language model [5], which we then further train with our data mixture.

(Black et al., 2026)

多模态 LLM 的定义是**基于大型语言模型，并导入视觉信号以进行图像理解、视频分析、视觉问答等多模态任务**的模型。PaliGemma 通过互联网规模的图文对进行预训练，具备强大的语言生成与视觉理解能力，符合"多模态 + LLM"的结构。

---

### 3. 跨形态训练（Cross-Embodiment Training）

**定义**：将来自多种不同机器人形态的数据混合在一起，共同训练同一个模型，而不为每种机器人单独训练。

> In order to make it feasible to utilize a variety of diverse robot data sources, we employ cross-embodiment training, where data from many robot types is combined into the same model. These different robot types have different configuration spaces and action representations, including single and dual-arm systems, as well as mobile manipulators.

(Black et al., 2026)

**关键概念拆解**：

**（a）机器人形态（embodiment）的多样性**
- 机器人构型：单臂、双臂、移动机械臂等。
- 动作空间：不同自由度（6轴 vs 7轴）、不同控制模式（关节角度 vs 末端位姿）、不同维度和数值范围。
- 观测空间：相机数量、安装位置、传感器类型各异。

**（b）跨形态训练的做法**
- 所有图像输入缩放、切块后送入统一视觉编码器。
- 本体感知状态通过投影层映射到统一维度嵌入向量。
- 动作输出采用统一维度的动作分块，不同机器人填充自己需控制的维度，其余用掩码占位。
- 模型通过动作专家学习不同机器人动作空间的映射关系。

**（c）为什么要跨形态训练？**
- **扩大数据规模**：单一机器人数据有限，混合后可达上万小时演示。
- **学习通用物理交互**：不同机器人在"抓取""推动""折叠"等操作中的物理规律共通。
- **实现零样本或多任务学习**：单一模型可控制未见过的机器人构型。

**（d）面临的挑战**
不同机器人动作空间的差异需要模型具备处理多分布的能力，π₀ 通过 Flow Matching 建模连续、多模态的动作分布来解决。

---

### 4. 动作分块架构（Action Chunking Architecture）+ Flow Matching

> Additionally, in order to make it possible to perform highly dexterous and intricate physical tasks, we use an action chunking architecture [57] with flow matching (a variant of diffusion) to represent complex continuous action distributions.

(Black et al., 2026)

**动作分块架构（Action Chunking）**
- 模型输出不是当前单个动作，而是未来一段时间内的一系列连续动作（动作块，chunk）。
- 每次预测接下来 $H$ 个时间步的动作序列 $\mathbf{a}_{t:t+H}$，实际执行前 $k$ 个后重新预测。
- **作用**：提供时间上下文与平滑性，适应高频控制（50 Hz），将决策从"一步预测"转变为"轨迹预测"。

**Flow Matching（流匹配）**
- 生成模型（diffusion 变体），学习向量场将噪声分布变换为目标动作分布。
- **高精度**：避免离散化量化误差，适合微米级/毫弧度级控制。
- **多模态建模**：对同一指令可采样出多条合理动作轨迹。
- **适应高维动作空间**：有效处理 $H \times D$ 维的动作块向量。

**二者如何结合实现复杂连续动作分布？**
1. 输出动作块 $\mathbf{a}_{t:t+H}$，将动作建模为连续序列。
2. 用 Flow Matching 生成整个动作块：从噪声出发，以当前观测和指令为条件，通过迭代去噪生成完整、平滑的动作序列。
3. 整个系统以 50 Hz 运行，完成洗衣折叠、叠蛋盒等高度灵巧任务。

---

## References

Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., Jakubczak, S., Jones, T., Ke, L., Levine, S., Li-Bell, A., Mothukuri, M., Nair, S., Pertsch, K., Shi, L. X., … Zhilinsky, U. (2026). *$π_0$: A Vision-Language-Action Flow Model for General Robot Control*. arXiv. https://doi.org/10.48550/arXiv.2410.24164

---

Written by LLM-for-Zotero.
