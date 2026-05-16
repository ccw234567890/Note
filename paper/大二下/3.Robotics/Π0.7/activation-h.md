
# $π_{0.7}$: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities

## 激活值 h 的计算流程

激活值 $h$ 是 VLM 骨干网络（Gemma3 4B）的**最后一层输出**，动作专家通过 cross-attention 读取这些激活值。

### 完整计算流程

```
输入处理
    │
    ├── 多视角观测图像（最多 4 个摄像头 × 6 帧历史）
    │   └── 缩放至 448×448 → 视觉编码器（400M）→ 时空压缩 → 固定数量 token
    │
    ├── 子目标图像（最多 3 张）
    │   └── 缩放至 448×448 → 同一视觉编码器 → token
    │
    ├── 本体感知状态 q_t（关节角度等）
    │   └── 线性投影 → 嵌入到骨干维度 → 每个历史状态 = 1 个 token
    │
    ├── 文本上下文（任务描述、子任务指令、元数据、控制模式）
    │   └── 文本分词器 → token
    │
    ▼
┌─────────────────────────────────────┐
│      VLM 骨干网络（Gemma3 4B）       │
│  ┌───────────────────────────────┐  │
│  │ 视觉编码器 → 图像 token       │  │
│  │ 文本嵌入 → 文本 token         │  │
│  │ 本体感知投影 → 状态 token     │  │
│  │                               │  │
│  │  Transformer 层（块因果掩码）  │  │
│  │  ┌─────────────────────────┐  │  │
│  │  │ 自注意力 + FFN × N 层   │  │  │
│  │  └─────────────────────────┘  │  │
│  └──────────────┬────────────────┘  │
└─────────────────┼──────────────────┘
                  │
                  ▼
           激活值 h（所有 token 的最终隐藏状态）
                  │
                  ├──→ FAST token 头 → 交叉熵损失（离散动作预测）
                  │
                  ▼
          ┌──────────────────┐
          │  动作专家 (860M)  │
          │  cross-attention  │  ← 读取 h 中的激活值
          │  + 流匹配         │
          └──────────────────┘
```

## 注意力掩码机制（Attention Mask）

论文 Section VI-B 明确描述了注意力掩码方案：

> "We employ a block-causal masking scheme, such that the observation tokens and the subgoal image tokens use bidirectional attention within themselves, and goal-image tokens can additionally attend the observations. The following text tokens use causal attention."

| Token 类型 | 注意力范围 |
|-----------|-----------|
| **观测图像 token**（历史帧） | 双向注意力（彼此可见） |
| **子目标图像 token** | 双向注意力 + 可关注观测 token |
| **文本 token**（任务描述、子任务、元数据等） | 因果注意力（只能看前面的 token） |
| **本体感知状态 token** | 与对应历史帧一起被掩码处理 |

## 图像和语言令牌的 KV 缓存是否共享？

**答案是：是的，它们共享同一个 VLM 骨干的 KV 缓存，但注意力模式不同。**

### 共享的 Transformer 骨干

图像 token 和文本 token 都通过**同一个 VLM 骨干网络**（Gemma3 4B）处理。这意味着：

- 它们共享**同一组 Transformer 层**的权重
- 它们共享**同一个 KV 缓存**（在自注意力计算中，所有 token 的 Key 和 Value 都存储在同一个缓存中）
- 但它们的**注意力模式（attention mask）不同**——图像 token 之间是双向的，文本 token 之间是因果的

### 为什么这样设计？

在标准的 VLM 中，输入序列被拼接成一个单一的序列送入 Transformer：

```
输入序列 = [图像 token_1, 图像 token_2, ..., 文本 token_1, 文本 token_2, ...]
                    ↑ 共享同一个 Transformer 骨干 ↑
                    ↑ 共享同一个 KV 缓存 ↑
```

所有 token 的 K 和 V 都存储在同一个缓存中，但注意力掩码控制哪些 token 可以互相看到。

### 视觉编码器的角色

图像 token 在进入 VLM 骨干之前，先经过一个 **400M 参数的视觉编码器**（也是从 Gemma3 初始化的），将图像压缩为固定数量的 token。这个视觉编码器**不处理文本**，只处理图像。

```
图像 → 视觉编码器（400M）→ 图像 token（固定数量）
文本 → 分词器 → 文本 token

然后将两者拼接：
[图像 token_1, ..., 图像 token_N, 文本 token_1, ..., 文本 token_M]
                              ↓
                     VLM 骨干 Transformer
                              ↓
                      激活值 h（所有 token）
```

### 动作专家如何读取 h？

动作专家（860M Transformer）通过 **cross-attention** 读取 VLM 骨干的激活值 $h$：

> "The 50 tokens attend bidirectionally to each other and can also attend to the VLM backbone activations."

动作专家的 50 个动作 token 之间是**双向注意力**，并且它们可以**关注 VLM 骨干的所有激活值**（包括图像 token、文本 token、状态 token 的输出）。

## 总结

| 问题 | 答案 |
|------|------|
| **激活值 h 怎么算的？** | 所有输入（图像、文本、状态）拼接成单一序列，通过 Gemma3 4B Transformer 的前向传播得到最后一层隐藏状态 |
| **图像和语言 token 的 KV 缓存共享吗？** | **✅ 共享** — 它们在同一个 Transformer 骨干中处理，共享同一组 KV 缓存 |
| **注意力模式一样吗？** | **❌ 不一样** — 图像 token 之间是双向注意力，文本 token 之间是因果注意力（块因果掩码） |
| **动作专家怎么用 h？** | 通过 **cross-attention** 关注 VLM 骨干的所有激活值 |
| **视觉编码器处理什么？** | 只处理图像（观测帧和子目标图像），不处理文本 |

## References

Intelligence, P., Ai, B., Amin, A., Aniceto, R., Balakrishna, A., Balke, G., Black, K., Bokinsky, G., Cao, S., Charbonnier, T., Choudhary, V., Collins, F., Conley, K., Connors, G., Darpinian, J., Dhabalia, K., Dhaka, M., DiCarlo, J., Driess, D., … Zhilinsky, U. (2026). *$π_{0.7}$: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities*. arXiv:2604.15483. https://doi.org/10.48550/arXiv.2604.15483

---

Written by LLM-for-Zotero.
