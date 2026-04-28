
# $π_0$: A Vision-Language-Action Flow Model for General Robot Control

## 概述

π₀ 的 Transformer 输入序列由**四种不同类型的令牌**拼接而成，形成一个**一维序列**送入 Transformer 处理。整个序列的结构为：

```
输入序列 = [图像令牌 | 语言令牌 | 状态令牌 | 动作令牌]
```

其中前三种令牌构成**观测 $o_t$**，动作令牌是**带噪声的动作块 $A_t^\tau$**。

> The standard PaliGemma architecture takes in a sequence of images $[I_{t1}, \dots, I_{tn}]$ followed by a language prompt $l_t$. We add an input $q_t$ for the robot's proprioceptive state, which is mapped to the transformer embedding dimension using a linear projection. The final set of input tokens correspond to the noisy action chunk $A_t^\tau = [a_t^\tau, \dots, a_{t+H-1}^\tau]$, with the number of tokens equal to the action horizon ($H=50$ for our tasks).

(Black 等, 2026)

---

## 一、图像令牌（Image Tokens）

### 原始数据

机器人搭载 $n$ 个摄像头（通常为 1~3 个），每个摄像头在时间步 $t$ 采集一张 RGB 图像 $I_{ti} \in \mathbb{R}^{H \times W \times 3}$。

### 编码过程

每张图像通过一个**预训练的 Vision Transformer（ViT）编码器**处理：

1. **图像分块（Patchify）**：将图像分割为固定大小的 patches，例如 $14 \times 14$ 像素。
2. **线性投影**：每个 patch 展平后通过线性投影映射到嵌入维度 $w$。
3. **ViT 编码**：经过多层 Transformer 编码器，输出一组图像 patch 令牌。

> 论文中使用的 ViT 编码器是 PaliGemma 架构中的预训练 ViT（主模型）或 R26-S-32 ResNet-ViT 混合编码器（π₀-small 基线模型）。

### 输出形状

每张图像产生 $P$ 个 patch 令牌，每个令牌维度为 $w$。$n$ 张图像共产生 $n \times P$ 个图像令牌。

### 向量变化

```
I_ti ∈ ℝ^(H×W×3)          ← 原始 RGB 图像
    ↓ 分块 (patchify)
[patches] ∈ ℝ^(P × (patch_size² × 3))
    ↓ 线性投影 + ViT 编码
[image_tokens] ∈ ℝ^(P × w)  ← 图像令牌嵌入
```

---

## 二、语言令牌（Language Tokens）

### 原始数据

自然语言指令 $l_t$，例如 "fold the towel" 或 "pick up the cup"。

### 编码过程

语言指令通过 **Gemma 语言模型的 tokenizer** 进行分词（tokenization），将文本转换为离散的 token ID 序列，然后通过**词嵌入层（embedding layer）**映射为连续向量。

> 论文遵循 PaliGemma VLM 设计，使用预训练的 Gemma 语言模型骨干网络来处理语言令牌。

### 输出形状

语言令牌的数量取决于指令的长度，通常为 $L$ 个令牌，每个维度为 $w$。

### 向量变化

```
l_t = "fold the towel"      ← 原始文本字符串
    ↓ Gemma tokenizer
[token_ids] ∈ ℤ^L           ← 离散 token ID 序列
    ↓ 词嵌入层
[lang_tokens] ∈ ℝ^(L × w)   ← 语言令牌嵌入
```

---

## 三、状态令牌（State Tokens）

### 原始数据

机器人本体感知状态向量 $q_t \in \mathbb{R}^d$，包含：
- 各关节角度
- 夹爪开合状态
- 移动底盘位姿
- 升降躯干高度

等 proprioceptive（本体感知）信息。

> 配置向量的维度取数据集中最大机器人的维度（论文中为 18 维，对应双臂 6-DoF × 2 + 2 夹爪 + 移动底座 + 升降躯干）。对于低维度的机器人，不足的维度用零填充。

### 编码过程

状态向量通过一个**线性投影层**直接映射到 Transformer 的嵌入维度：

$$e_q = W_q \cdot q_t$$

其中 $W_q \in \mathbb{R}^{w \times d}$ 是可学习的投影矩阵。

### 输出形状

**1 个**状态令牌，维度为 $w$。

### 向量变化

```
q_t ∈ ℝ^d                   ← 原始状态向量（d ≤ 18）
    ↓ 线性投影 W_q ∈ ℝ^(w×d)
state_token ∈ ℝ^w           ← 状态令牌嵌入
```

---

## 四、动作令牌（Action Tokens）

### 原始数据

带噪声的动作块 $A_t^\tau = [a_t^\tau, a_{t+1}^\tau, \dots, a_{t+H-1}^\tau]$，其中：
- $H = 50$：动作分块长度（action horizon）
- 每个 $a_{t'}^\tau \in \mathbb{R}^d$：第 $t'$ 个时间步的噪声动作向量
- $\tau \in [0, 1]$：流匹配时间步（$\tau=0$ 为纯噪声，$\tau=1$ 为干净动作）

### 编码过程

这是最复杂的令牌编码，因为需要同时融合**动作向量**和**流匹配时间步 $\tau$** 的信息。

对于每个噪声动作 $a_{t'}^\tau$，其嵌入的计算公式为：

$$e_{t'} = W_3 \cdot \text{swish}\left(W_2 \cdot \text{concat}\left(W_1 \cdot a_{t'}^\tau,\ \phi(\tau)\right)\right)$$

其中：
- $\phi: \mathbb{R} \to \mathbb{R}^w$：**正弦位置编码函数**，将标量 $\tau$ 编码为 $w$ 维向量
- $W_1 \in \mathbb{R}^{w \times d}$：将动作向量投影到嵌入维度 $w$
- $\text{concat}(W_1 \cdot a_{t'}^\tau,\ \phi(\tau)) \in \mathbb{R}^{2w}$：拼接动作嵌入和时间步编码
- $W_2 \in \mathbb{R}^{w \times 2w}$：将拼接向量压缩回 $w$ 维
- $\text{swish}$：Swish 激活函数，$\text{swish}(x) = x \cdot \sigma(x)$
- $W_3 \in \mathbb{R}^{w \times w}$：最终线性投影
- $e_{t'} \in \mathbb{R}^w$：最终输入 Transformer 的动作令牌嵌入

### 输出形状

**50 个**动作令牌，每个维度为 $w$。

### 向量变化

```
a_{t'}^τ ∈ ℝ^d              ← 第 t' 个时间步的噪声动作向量
τ ∈ [0, 1]                  ← 流匹配时间步

    ↓ W₁ · a_{t'}^τ           ↓ φ(τ) 正弦编码
W₁·a_{t'}^τ ∈ ℝ^w          φ(τ) ∈ ℝ^w
    ↓ concat
concat ∈ ℝ^(2w)
    ↓ W₂ · swish(·)
hidden ∈ ℝ^w
    ↓ W₃
e_{t'} ∈ ℝ^w                ← 动作令牌嵌入（送入 Transformer）
```

---

## 五、完整输入序列的向量维度变化

### 序列拼接

所有令牌按顺序拼接成一个一维序列：

```
输入序列 = [image_tokens_1, ..., image_tokens_n, lang_tokens, state_token, action_tokens_1, ..., action_tokens_50]
```

### 总序列长度

$$N_{\text{total}} = n \times P + L + 1 + 50$$

其中：
- $n$：摄像头数量（1~3）
- $P$：每张图像的 patch 数量（ViT 输出）
- $L$：语言指令的 token 数量
- $1$：状态令牌
- $50$：动作令牌（$H=50$）

### 完整的向量变化流程

```
步骤 1: 原始数据
──────────────────────────────────────────────────
图像 I_ti ∈ ℝ^(H×W×3)    语言 l_t (字符串)    状态 q_t ∈ ℝ^d    噪声动作 A_t^τ ∈ ℝ^(50×d)

步骤 2: 编码为令牌嵌入
──────────────────────────────────────────────────
图像: ViT 编码器 → [n×P 个令牌] ∈ ℝ^(n×P×w)
语言: Tokenizer + 词嵌入 → [L 个令牌] ∈ ℝ^(L×w)
状态: 线性投影 W_q → [1 个令牌] ∈ ℝ^w
动作: MLP(动作 + τ 编码) → [50 个令牌] ∈ ℝ^(50×w)

步骤 3: 拼接为输入序列
──────────────────────────────────────────────────
输入序列 ∈ ℝ^((n×P + L + 1 + 50) × w)

步骤 4: Transformer 处理（观测编码器 + 动作专家）
──────────────────────────────────────────────────
观测编码器处理图像/语言/状态令牌 → 输出 KV 缓存
动作专家处理动作令牌（交叉注意观测 KV）→ 输出 H 个向量

步骤 5: 解码为向量场
──────────────────────────────────────────────────
仅取动作令牌对应的输出 → 线性投影 → v_θ(A_t^τ, o_t) ∈ ℝ^(50×d)
```

---

## 六、分块因果注意力掩码（Chunked Causal Attention Mask）

Transformer 内部使用一种**分块因果注意力掩码**来控制令牌之间的信息流动：

```
序列分块:
┌─────────────────┬──────────────┬──────┬────────────────────┐
│  图像令牌 (n×P)  │ 语言令牌 (L)  │ 状态  │  动作令牌 (50)      │
│  块 1            │  块 2        │  块 2 │  块 3              │
│  双向注意力       │  因果注意力   │       │  双向注意力         │
└─────────────────┴──────────────┴──────┴────────────────────┘

注意力规则:
- 块 1（图像）：块内全连接（双向注意力）
- 块 2（语言 + 状态）：块内因果（从左到右）
- 块 3（动作）：块内全连接（双向注意力）
- 块间：后面的块可以看到前面所有块（因果）
  → 动作令牌可以看到所有观测令牌
  → 观测令牌看不到动作令牌
```

这种设计确保：
1. **动作令牌**可以充分关注所有观测信息（图像、语言指令、机器人状态）
2. **动作令牌之间**互相可见，可以学习 $H=50$ 个动作之间的时序相关性
3. **观测编码**不受动作令牌的干扰

---

## 七、动作专家（Action Expert）与观测编码器的分离

π₀ 采用类似**混合专家（Mixture of Experts）**的设计，使用两套独立的权重：

> Building on Transfusion, we additionally found that using a separate set of weights for the robotics-specific (action and state) tokens led to an improvement in performance. This design is analogous to a mixture of experts with two mixture elements, where the first element is used for image and text inputs, and the second element is used for action and state inputs.

(Black 等, 2026)

- **观测编码器（Observation Encoder）**：处理图像令牌和语言令牌，使用 Gemma 架构的权重（较大）
- **动作专家（Action Expert）**：处理状态令牌和动作令牌，使用一组更小的独立权重

推理时，观测令牌只需编码**一次**，其 KV 缓存被动作专家在 10 步流匹配迭代中**复用**：

> Each time we predict a new action chunk $A_t$, we must encode each of the images $I_{t1}, \dots, I_{tn}$, run a forward pass on the tokens corresponding to $o_t$, and then run 10 steps of flow matching, where each step requires running a forward pass on the tokens corresponding to $A_t^\tau$ (the keys and values corresponding to $o_t$ are cached).

(Black 等, 2026)

---

## 八、电子信息工程视角的解读

### 多路复用与帧结构

整个输入序列可以类比为**时分复用（TDM）通信帧**：

| 帧字段 | 对应令牌 | 类比 |
|--------|---------|------|
| 帧头（图像） | 图像令牌 | 环境感知信息，相当于"场景描述符" |
| 控制字（语言） | 语言令牌 | 任务指令，相当于"命令码" |
| 状态字（状态） | 状态令牌 | 系统当前状态反馈 |
| 数据载荷（动作） | 动作令牌 | 待发送的控制指令序列 |

### 数-模混合信号处理

π₀ 的输入序列是一个**数-模混合信号**：
- **离散信号**：语言令牌（离散 token ID）、图像 patch 令牌（离散化后的视觉特征）
- **连续信号**：状态令牌（连续实数向量）、动作令牌（连续实数向量，含噪声）

Transformer 作为一个统一的处理骨干，同时处理这两种信号类型，其中离散令牌通过交叉熵损失监督，连续令牌通过流匹配损失监督。

### 向量维度的"阻抗匹配"

从原始数据到 Transformer 嵌入的每一步映射，都可以看作**阻抗匹配**的过程：
- 图像：$\mathbb{R}^{H \times W \times 3} \to \mathbb{R}^{P \times w}$（空间维度 → 特征维度）
- 语言：字符串 $\to \mathbb{Z}^L \to \mathbb{R}^{L \times w}$（符号 → 连续嵌入）
- 状态：$\mathbb{R}^d \to \mathbb{R}^w$（低维物理量 → 高维特征空间）
- 动作：$\mathbb{R}^d \to \mathbb{R}^w$（含 $\tau$ 调制，动作向量 + 噪声水平编码）

所有模态最终被映射到**统一的嵌入空间 $\mathbb{R}^w$**，使得 Transformer 可以在同一表示空间中处理多模态信息。

## References
Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., Jakubczak, S., Jones, T., Ke, L., Levine, S., Li-Bell, A., Mothukuri, M., Nair, S., Pertsch, K., Shi, L. X., … Zhilinsky, U. (2026). *$π_0$: A Vision-Language-Action Flow Model for General Robot Control*. arXiv:2410.24164 [cs].

---

Written by LLM-for-Zotero.
