
# $π_0$: A Vision-Language-Action Flow Model for General Robot Control

## Summary
π₀ 模型使用分块因果掩码（blockwise causal mask）将输入划分为 3 个块，通过缓存 VLM 骨干的 Key-Value 来大幅加速流匹配推理。

## KV 缓存共享机制

### 注意力掩码结构

π₀ 使用一个分块因果掩码，包含 3 个块：

```
块 1: [图像令牌, 语言指令]  ← 双向注意力（块内）
块 2: [本体状态 qt]         ← 独立块（块内双向）
块 3: [带噪动作 Atτ]        ← 可关注全部前序块
```

### 各块的 KV 缓存行为

| 块 | 内容 | 注意力范围 | 是否缓存 KV |
|----|------|-----------|------------|
| **块 1** | 图像令牌 $[I_{t1},...,I_{tn}]$ + 语言指令 $l_t$ | 块内双向，不能关注块 2、块 3 | ✅ 缓存 |
| **块 2** | 本体状态 $q_t$ | 块内双向，不能关注块 3 | ✅ 缓存 |
| **块 3** | 带噪动作 $A_t^\tau$（H=50 个令牌） | 可关注全部前序块（块 1 + 块 2 + 块 3 内） | ❌ 每次流匹配步更新 |

### 为什么块 1 和块 2 的 KV 被缓存

论文原文解释：

> The robot state qt is its own block because it does not change with each flow matching integration step; preventing it from attending to the final block allows its corresponding keys and values to be cached during sampling.

(Black 等, 2026)

**推理流程：**

1. **Observation forward pass（32 ms）**：一次性编码图像 $I_{t1..tn}$、语言指令 $l_t$ 和本体状态 $q_t$，计算并缓存块 1 和块 2 的 Key 和 Value
2. **10 步流匹配（27 ms）**：在每一步中，动作令牌 $A_t^\tau$ 通过自注意力层时，复用已缓存的块 1 + 块 2 的 KV，只需计算块 3（动作令牌）自身的 KV 和注意力

### 动作专家与 VLM 骨干的共享机制

π₀ 实现为一个单 Transformer 模型，包含两组权重（专家），每个令牌被路由到其中一个专家：

| 令牌类型 | 路由到 | 权重 |
|----------|--------|------|
| 图像 $[I_{t1},...,I_{tn}]$ + 语言 $l_t$ | **VLM 骨干**（PaliGemma 2B） | width=2048, depth=18 |
| 本体状态 $q_t$ + 带噪动作 $A_t^\tau$ | **动作专家**（300M） | width=1024, mlp_dim=4096 |

两个专家共享**同一个自注意力层**（self-attention layers），但 MLP 权重是独立的（VLM 骨干的 MLP dim=16384，动作专家的 MLP dim=4096）。

### 总结

**被缓存的 KV 来自：**
1. ✅ 图像令牌（ViT 编码后的 patch tokens）
2. ✅ 语言指令令牌（tokenized text）
3. ✅ 本体状态令牌（$q_t$，线性投影后的 1 个令牌）

**不被缓存（每次流步重新计算）：**
4. ❌ 带噪动作令牌（$A_t^\tau$，H=50 个令牌）

这种设计使得 10 步流匹配推理中，**73 ms 总推理时间**中有 32 ms 用于一次性 observation 前向传播（含 KV 缓存），而 10 步动作前向传播仅需 27 ms（因为复用了缓存的 KV）。

## References
Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., Jakubczak, S., Jones, T., Ke, L., Levine, S., Li-Bell, A., Mothukuri, M., Nair, S., Pertsch, K., Shi, L. X., … Zhilinsky, U. (2026). *π₀: A Vision-Language-Action Flow Model for General Robot Control*. arXiv:2410.24164.

---

Written by LLM-for-Zotero.
