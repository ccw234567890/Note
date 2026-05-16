
# $π_{0.7}$: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities

## VLM 骨干和动作专家的输入输出

### 一、整体架构

π₀.₇ 是一个两阶段架构：

```
输入观测 + 上下文
        │
        ▼
┌─────────────────────────────────────┐
│         VLM 骨干网络 (4B)            │
│  ┌───────────────────────────────┐  │
│  │ 视觉编码器 (400M) + Gemma3 LLM │  │
│  └──────────┬────────────────────┘  │
└─────────────┼───────────────────────┘
              │ VLM 骨干的激活值 (activations)
              ▼
┌─────────────────────────────────────┐
│         动作专家 (860M)              │
│  ┌───────────────────────────────┐  │
│  │ 轻量级 Transformer + 流匹配    │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
              │
              ▼
          50 步动作块 [a₀, ..., a₄₉]
```

### 二、VLM 骨干的输入

论文原文（Section VI-B）：

> "The model takes as input up to four camera images (front view, two wrist views, and optionally rear view), each with up to six history frames, and up to three subgoal images (omitting the rear view)."

VLM 骨干接收**所有输入**，包括：

#### 1. 多视角观测图像（Multi-view Observations）

| 视角 | 数量 | 说明 |
|------|------|------|
| **前视摄像头** | 1 个 | 场景全局视角 |
| **腕部摄像头** | 2 个 | 左右手腕，近距离操作视角 |
| **后视摄像头** | 1 个（可选） | 移动机器人后方视角，30% 概率被丢弃 |
| **每视角历史帧** | 最多 6 帧 | 采样步长 1 秒，30% 概率全部丢弃 |

所有图像先缩放到 **448×448 像素**，然后通过视觉编码器处理。

#### 2. 子目标图像（Subgoal Images）

最多 **3 张**（前视 + 左右腕部，不含后视），与观测图像使用**相同的视觉编码器**。

#### 3. 本体感知状态（Proprioceptive State）

$$q_t = \text{关节角度 / 末端执行器位姿}$$

- 与 π₀.6 不同（用离散文本 token 表示），π₀.₇ 使用**线性投影**将状态向量映射到骨干网络维度
- 每个历史状态作为一个独立的 token
- 如果历史帧被丢弃，对应的状态 token 也被掩码

#### 4. 文本上下文（Text Context）

论文中的完整 prompt 示例（Section V-E）：

```
<Multi-view observation><Multi-view subgoals>
Task: peel vegetables.
Subtask: pick up the peeler.
Speed: 8000.
Quality: 5.
Mistake: false.
Control Mode: joint.
<Proprioception>
```

具体包括：

| 文本组件 | 示例 | 说明 |
|---------|------|------|
| **任务描述 $l_t$** | "peel vegetables" | 整体任务目标 |
| **子任务指令 $\hat{l}_t$** | "pick up the peeler" | 当前语义子任务，30% 概率被丢弃（有子目标图像时） |
| **速度元数据** | "Speed: 8000" | 片段长度（时间步数），离散化为 500 步区间 |
| **质量元数据** | "Quality: 5" | 1-5 分任务执行质量 |
| **错误标记** | "Mistake: false" | 是否在动作段中犯错 |
| **控制模式** | "Control Mode: joint" | joint（关节级）或 ee（末端执行器） |

**训练时丢弃策略**：
- 子目标图像：仅 25% 的 batch 样本包含
- 元数据：15% 概率全部丢弃，每个组件额外 5% 概率单独丢弃
- 控制模式：不丢弃

### 三、VLM 骨干的输出

VLM 骨干的输出是**中间层的激活值（hidden states / activations）**，这些激活值被动作专家通过交叉注意力读取。

同时，VLM 骨干还通过 **FAST token** 输出离散动作预测，使用交叉熵损失训练。

### 四、动作专家的输入

论文原文（Section VI-B）：

> "The more lightweight 'action expert' is a 860M-parameter transformer that is trained to predict continuous actions using flow matching objective... The 50 tokens attend bidirectionally to each other and **can also attend to the VLM backbone activations**."

动作专家的输入**不是原始观测或文本**，而是：

#### 1. VLM 骨干的激活值（Activations）

```
VLM 骨干处理完所有输入后，输出中间层的激活值（hidden states）
         │
         ▼
动作专家通过交叉注意力（cross-attention）关注这些激活值
         │
         ▼
动作专家从中提取与动作相关的语义信息
```

**关键**：动作专家**不直接看到**图像、文本或本体感知状态。它只看到 VLM 骨干对这些输入处理后产生的**表示（representations）**。

#### 2. 动作 token（Action Tokens）

- 固定 **50 个 token**，对应一个 50 步的动作块
- 这些 token 之间使用**双向注意力**（bidirectional attention）
- 初始化为**纯噪声**（流匹配的去噪起点）
- 通过流匹配逐步去噪，最终输出 50 步连续动作

#### 3. 去噪时间步信息（Timestep）

- 通过**自适应 RMSNorm** 注入
- 告诉动作专家当前处于去噪的哪个阶段（t ∈ [0, 1]）

### 五、动作专家的输出

动作专家输出 **50 步连续动作块**：

$$a_{t:t+H} = [a_t, a_{t+1}, ..., a_{t+49}]$$

其中每个 $a_t$ 可以是：
- **关节级（joint）控制**：所有关节角度
- **末端执行器（end-effector）控制**：末端执行器位姿 + 夹爪状态

### 六、对比总结

| 维度 | VLM 骨干 (4B) | 动作专家 (860M) |
|------|--------------|----------------|
| **输入来源** | 原始传感器 + 文本 | VLM 骨干的激活值 |
| **图像** | ✅ 多视角观测 + 子目标图像（448×448） | ❌ 不直接看图像 |
| **本体感知** | ✅ 线性投影嵌入 | ❌ 不直接看状态 |
| **文本指令** | ✅ 任务 + 子任务 + 元数据 | ❌ 不直接看文本 |
| **VLM 激活值** | ❌ 自身就是生成者 | ✅ **通过交叉注意力读取** |
| **动作 token** | ❌ 通过 FAST token 间接预测 | ✅ **50 个可学习 token**（从噪声去噪） |
| **时间步信息** | ❌ 不需要 | ✅ 通过自适应 RMSNorm 注入 |
| **输出** | FAST token 的离散预测 + 中间激活值 | 50 步连续动作块 |

### 七、一句话总结

> **VLM 骨干**接收所有原始输入（多视角图像、子目标图像、本体感知状态、文本指令和元数据），将其编码为丰富的语义表示；**动作专家**不直接看任何原始输入，而是通过交叉注意力读取 VLM 骨干的激活值，结合 50 个动作 token 和去噪时间步信息，用流匹配生成连续动作。

## References

Intelligence, P., Ai, B., Amin, A., Aniceto, R., Balakrishna, A., Balke, G., Black, K., Bokinsky, G., Cao, S., Charbonnier, T., Choudhary, V., Collins, F., Conley, K., Connors, G., Darpinian, J., Dhabalia, K., Dhaka, M., DiCarlo, J., Driess, D., … Zhilinsky, U. (2026). *$π_{0.7}$: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities*. arXiv. https://doi.org/10.48550/arXiv.2604.15483

---

Written by LLM-for-Zotero.
