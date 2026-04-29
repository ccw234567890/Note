
# $π_{0.7}$: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities

## 动作专家的结构

### 一、概述

动作专家（Action Expert）是 π₀.₇ 模型中负责预测连续动作的轻量级组件，参数量为 **860M**。它使用**流匹配（Flow Matching）**目标进行训练，能够建模多模态动作分布。动作专家通过 **cross-attention** 读取 VLM 骨干（Gemma3 4B）最后一层的激活值 $h$，但**梯度不回流**到 VLM 骨干（知识隔离 KI 训练策略）。

### 二、动作专家的输入

动作专家的输入包含**两部分**：

| 输入来源 | 说明 |
|---------|------|
| **① VLM 骨干的激活值 $h$** | 通过 **cross-attention** 读取 VLM 骨干最后一层的所有 token 激活值（图像 token + 文本 token + 状态 token） |
| **② 流匹配的时间步信息（timestep）** | 通过 **adaptive RMSNorm** 注入去噪时间步信息，这是流匹配/扩散模型的必要输入 |

**动作专家不接收以下信息**：
- ❌ 原始图像（已通过 VLM 骨干处理为激活值）
- ❌ 原始文本（已通过 VLM 骨干处理为激活值）
- ❌ 本体感知状态（已通过 VLM 骨干处理为激活值）
- ❌ 子目标图像（已通过 VLM 骨干处理为激活值）

所有原始输入都先经过 VLM 骨干处理，动作专家只通过 cross-attention 读取 VLM 骨干的输出激活值。

### 三、动作专家的内部结构

```
动作专家（860M Transformer）
┌────────────────────────────────────────────┐
│                                            │
│  50 个动作 token（可学习的查询 token）       │
│  ┌──────────────────────────────────────┐  │
│  │ token_1, token_2, ..., token_50      │  │
│  │                                      │  │
│  │ 自注意力（双向）←── 彼此可见           │  │
│  │                                      │  │
│  │ Cross-attention ──→ 关注 VLM 骨干的 h  │  │
│  │                                      │  │
│  │ Adaptive RMSNorm ←── 注入时间步信息    │  │
│  │                                      │  │
│  │ FFN（前馈网络）                        │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  输出：50 步连续动作（流匹配预测）           │
└────────────────────────────────────────────┘
```

#### 1. 50 个动作 token（可学习查询 token）

动作专家内部有 50 个固定的可学习 token，它们：
- **彼此之间**使用**双向注意力**（50 个 token 互相可见）
- **通过 cross-attention** 关注 VLM 骨干的所有激活值 $h$
- 每个 token 最终输出对应时间步的动作预测

> "The 50 tokens attend bidirectionally to each other and can also attend to the VLM backbone activations."
> (Intelligence 等, 2026)

#### 2. Adaptive RMSNorm 注入时间步信息

流匹配（Flow Matching）是一个去噪过程，需要知道当前处于去噪的哪个时间步。这个信息通过 **adaptive RMSNorm** 注入：

```
adaptive RMSNorm(h, t) = RMSNorm(h) * (1 + α·t) + β·t
```

其中 $t$ 是流匹配的时间步，$\alpha$ 和 $\beta$ 是可学习的缩放/偏移参数。

> "We use adaptive RMSNorm to inject timestep information for flow matching."
> (Intelligence 等, 2026)

#### 3. 输出：50 步连续动作

动作专家输出一个长度为 50 的动作块（action chunk），代表未来 50 个时间步的连续动作。推理时，实际执行其中的 $\hat{H} \in \{15, 25\}$ 步。

### 四、梯度隔离（知识隔离 KI）

论文 Section III 明确说明：

> "while the action expert attends to all of the activations in the VLM backbone, gradients from the action expert do not flow into the VLM backbone"

这意味着：
- **前向传播**：动作专家可以读取 VLM 骨干的所有激活值 $h$
- **反向传播**：动作专家的梯度**被截断**，不更新 VLM 骨干的参数
- VLM 骨干只通过 FAST token 的**交叉熵损失**训练

### 五、实时动作分块（RTC）

π₀.₇ 采用了训练时的实时动作分块（Real-Time Action Chunking, RTC）技术：

> "π0.7 also employs the training-time version of real-time action chunking (RTC) for generating smooth action trajectories in the presence of inference delay."

训练时模拟 0 到 12 个时间步的延迟（对应 50Hz 机器人上最大 240ms 推理延迟），使模型在推理时能生成平滑的动作轨迹。

### 六、推理流程

推理时，动作专家使用 **5 个去噪步** 生成 50 步动作块。同时支持**无分类器引导（CFG）**：

```
∇a log πθ(at:t+H |ot, Ct) +
β(∇a log πθ(at:t+H |ot, Ct) − ∇a log πθ(at:t+H |ot, Cuncond_t))
```

其中 CFG 权重 $\beta \in \{1.3, 1.7, 2.2\}$，应用于片段元数据以在灵巧任务中引出强性能。

### 七、总结

| 方面 | 说明 |
|------|------|
| **参数量** | 860M |
| **主要输入** | VLM 骨干最后一层的激活值 $h$（通过 cross-attention 读取） |
| **额外输入** | 流匹配去噪时间步（通过 adaptive RMSNorm 注入） |
| **动作 token** | 50 个可学习的查询 token |
| **注意力模式** | 50 个 token 之间双向注意力，可关注 VLM 骨干所有激活值 |
| **训练目标** | 流匹配（Flow Matching） |
| **梯度回流** | ❌ 不回流（知识隔离 KI） |
| **去噪步数** | 5 步 |
| **执行步数** | $\hat{H} \in \{15, 25\}$ |
| **RTC 延迟模拟** | 0-12 时间步（最大 240ms） |

## References
Physical Intelligence et al. (2026). *π₀.₇: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities*. arXiv:2604.15483.

---

Written by LLM-for-Zotero.
