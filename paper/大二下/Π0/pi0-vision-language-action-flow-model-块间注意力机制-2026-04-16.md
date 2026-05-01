---
title: "$π_0$: A Vision-Language-Action Flow Model for General Robot Control"
citekey: ""
doi: "10.48550/arXiv.2410.24164"
year: 2026
journal: ""
created: 2026-04-16
tags: [zotero, paper-note]
---

# $π_0$: A Vision-Language-Action Flow Model for General Robot Control

## 分块因果注意力掩码的设计

论文附录 B 明确给出了注意力掩码的定义和设计理由：

> π0 uses a blockwise causal attention mask with 3 blocks: [It1, ..., Itn, lt], [qt], and [atτ, ..., aτt+H−1]. Within each block, there is full bidirectional attention, whereas the tokens in each block cannot attend to the tokens in future blocks.

(Black 等, 2026, 附录 B)

三个块之间的注意力是**因果单向的**（只能看前面的块，不能看后面的块），但**块内部是双向的**。

### 原因 1：保护 VLM 预训练表示（块 1 → 块 2、块 3 被屏蔽）

> The first block includes the input modalities from PaliGemma's VLM pre-training, which are prevented from attending to future blocks (which include new inputs) to minimize distribution shift from said pre-training.

(Black 等, 2026, 附录 B)

**图像令牌和语言令牌**（块 1）在 PaliGemma 预训练时从未见过 $q_t$（状态）和 $a_t^\tau$（动作）。如果允许它们去注意这些新令牌，它们的表示会被"污染"，偏离预训练学到的语义知识。所以块 1 只能注意自己，不能注意块 2 和块 3。

### 原因 2：KV 缓存优化（块 2 → 块 3 被屏蔽）

> The robot state qt is its own block because it does not change with each flow matching integration step; preventing it from attending to the final block allows its corresponding keys and values to be cached during sampling.

(Black 等, 2026, 附录 B)

Flow Matching 需要 **10 步积分**，每一步都要重新跑动作令牌（块 3）的前向传播。但 $q_t$（状态令牌）在 10 步积分中**保持不变**。如果 $q_t$ 可以注意动作令牌，那么每一步 $q_t$ 的 KV 缓存都会因为动作令牌的变化而失效，必须重新计算。

通过让 $q_t$ **不能注意**动作令牌，$q_t$ 的 KV 值在 10 步积分中完全不变，可以**一次性计算并缓存**，大幅加速推理。

### 原因 3：动作令牌需要全局信息（块 3 可以注意所有块）

> The final block corresponds to the noisy actions Atτ, which can attend to the full input sequence.

(Black 等, 2026, 附录 B)

动作令牌（块 3）是唯一一个**可以注意整个序列**的块。这是合理的，因为动作生成需要依赖所有输入信息：图像（看到场景）、语言（理解指令）、状态（知道当前位姿）。所以块 3 的注意力是**非因果的**——它能看到前面所有块的全部内容。

### 注意力掩码矩阵

```
                   块 1 (图像+语言)    块 2 (状态)    块 3 (动作)
                    I1...In, lt          qt           a1...a50
                   ┌─────────────────┬─────────────┬─────────────────┐
块 1 (图像+语言)   │  ✅ 双向注意     │   ❌ 屏蔽    │   ❌ 屏蔽        │
                   │  (块内全连接)    │             │                  │
                   ├─────────────────┼─────────────┼─────────────────┤
块 2 (状态)        │  ✅ 可注意       │  ✅ 双向    │   ❌ 屏蔽        │
                   │  (单向因果)      │  (块内自身) │                  │
                   ├─────────────────┼─────────────┼─────────────────┤
块 3 (动作)        │  ✅ 可注意       │  ✅ 可注意  │  ✅ 双向注意     │
                   │  (全局可见)      │  (全局可见) │  (块内全连接)    │
                   └─────────────────┴─────────────┴─────────────────┘
```

### 总结

| 设计选择 | 原因 |
|---------|------|
| 块 1 → 块 2、块 3 屏蔽 | **保护 VLM 预训练表示**，避免新输入破坏图像/语言令牌的语义 |
| 块 2 → 块 3 屏蔽 | **KV 缓存优化**，$q_t$ 的键值在 10 步积分中可复用，无需重复计算 |
| 块 3 → 所有块可见 | **动作生成需要全局信息**，必须同时看到图像、语言和状态 |
| 块内双向注意 | 同类令牌之间需要充分交互（如图像 patches 之间、动作令牌之间） |

### 电子信息工程视角的类比

从电子信息工程的角度看，这类似于一个**多级信号处理流水线**：

- **前级（VLM）**：处理高维语义信号时被隔离保护，避免被后续信号干扰
- **中间级（状态）**：作为参考信号被缓存复用，不参与动态信号的迭代
- **后级（动作生成器）**：有权访问所有前级信息以合成最终的控制指令

这种精心设计的"信号流向"既保证了信号质量（不破坏预训练表示），又优化了计算效率（KV 缓存复用）。

## References
Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., Jakubczak, S., Jones, T., Ke, L., Levine, S., Li-Bell, A., Mothukuri, M., Nair, S., Pertsch, K., Shi, L. X., … Zhilinsky, U. (2026). *$π_0$: A Vision-Language-Action Flow Model for General Robot Control*. arXiv:2410.24164 [cs].

---

Written by LLM-for-Zotero.
