---
title: "RLHF架构图"
created: 2025-07-17
tags: [zotero, rlhf, architecture]
---

# RLHF 完整架构图

> 基于 Rafailov et al., *Direct Preference Optimization: Your Language Model is Secretly a Reward Model* (NeurIPS 2023)

---

## 一、RLHF 三阶段总览

```mermaid
flowchart TB
    subgraph Phase1["阶段一：监督微调（SFT）"]
        A1["预训练语言模型<br/>π_pretrain"] --> A2["高质量下游任务数据<br/>（对话/摘要等）"]
        A2 --> A3["监督微调<br/>π_SFT"]
    end

    subgraph Phase2["阶段二：奖励建模"]
        B1["π_SFT 生成回答对<br/>(y1, y2) ~ π_SFT(y|x)"] --> B2["人类标注偏好<br/>y_w ≻ y_l | x"]
        B2 --> B3["训练奖励模型 r_φ<br/>Bradley-Terry 模型"]
    end

    subgraph Phase3["阶段三：RL 微调（PPO）"]
        C1["π_SFT 作为 π_ref<br/>（参考策略）"] --> C2["策略 π_θ 生成回答"]
        C2 --> C3["奖励模型 r_φ 打分"]
        C3 --> C4["PPO 优化<br/>最大化奖励 + KL 约束"]
        C4 --> C2
    end

    Phase1 --> Phase2
    Phase2 --> Phase3
```

---

## 二、阶段一：监督微调（SFT）详解

```mermaid
flowchart LR
    A["预训练语言模型<br/>GPT / LLaMA / Pythia"] --> B["高质量标注数据<br/>（对话、摘要等）"]
    B --> C["标准交叉熵损失<br/>L = -∑ log π(y|x)"]
    C --> D["π_SFT<br/>（基础对齐模型）"]

    style A fill:#e1f5fe,stroke:#0288d1
    style D fill:#e8f5e9,stroke:#388e3c
```

**数学公式：**

$$L_{SFT}(\theta) = -\mathbb{E}_{(x,y)\sim D_{SFT}} \left[ \log \pi_\theta(y|x) \right]$$

---

## 三、阶段二：奖励建模详解

```mermaid
flowchart TB
    subgraph Data["数据收集"]
        D1["提示 x"] --> D2["π_SFT 生成<br/>回答 y1, y2"]
        D2 --> D3["人类标注者<br/>选择偏好 y_w ≻ y_l"]
    end

    subgraph Model["奖励模型训练"]
        D3 --> E1["奖励模型 r_φ(x, y)<br/>（通常从 π_SFT 初始化）"]
        E1 --> E2["Bradley-Terry 偏好模型<br/>p(y_w ≻ y_l|x) = σ(r_φ(x,y_w) - r_φ(x,y_l))"]
        E2 --> E3["最大似然估计（MLE）<br/>L_R = -log σ(r_φ(x,y_w) - r_φ(x,y_l))"]
        E3 --> E1
    end

    subgraph Output["输出"]
        E1 --> F["训练好的奖励模型 r_φ"]
    end

    style Data fill:#fff3e0,stroke:#ff9800
    style Model fill:#e3f2fd,stroke:#1976d2
    style Output fill:#e8f5e9,stroke:#388e3c
```

### Bradley-Terry 偏好模型

$$p^*(y_1 \succ y_2 | x) = \frac{\exp(r^*(x, y_1))}{\exp(r^*(x, y_1)) + \exp(r^*(x, y_2))}$$

### 奖励模型损失函数

$$L_R(r_\phi, D) = -\mathbb{E}_{(x,y_w,y_l)\sim D} \left[ \log \sigma(r_\phi(x, y_w) - r_\phi(x, y_l)) \right]$$

其中 $\sigma$ 是 logistic 函数：$\sigma(z) = \frac{1}{1 + e^{-z}}$

---

## 四、阶段三：RL 微调（PPO）详解

```mermaid
flowchart TB
    subgraph Init["初始化"]
        I1["π_θ ← π_SFT<br/>（策略网络）"] 
        I2["π_ref ← π_SFT<br/>（参考策略，冻结）"]
        I3["r_φ ← 训练好的奖励模型"]
    end

    subgraph Rollout["采样"]
        R1["从 π_θ(y|x) 采样回答 y"] --> R2["奖励模型 r_φ(x, y) 打分"]
        R2 --> R3["计算优势函数 A"]
    end

    subgraph Update["PPO 更新"]
        R3 --> U1["PPO 裁剪目标<br/>L_CLIP + L_value + L_entropy"]
        U1 --> U2["更新 π_θ"]
        U2 --> R1
    end

    subgraph Constraint["KL 约束"]
        C1["KL 散度惩罚<br/>β·D_KL(π_θ || π_ref)"]
        C1 -.-> U1
    end

    Init --> Rollout
    Constraint -.-> Update

    style Init fill:#e8f5e9,stroke:#388e3c
    style Rollout fill:#fff3e0,stroke:#ff9800
    style Update fill:#e3f2fd,stroke:#1976d2
    style Constraint fill:#fce4ec,stroke:#d32f2f
```

### RL 优化目标

$$\max_{\pi_\theta} \mathbb{E}_{x\sim D, y\sim\pi_\theta(y|x)} \left[ r_\phi(x, y) \right] - \beta \cdot D_{KL}\left( \pi_\theta(y|x) \parallel \pi_{\text{ref}}(y|x) \right)$$

### PPO 实际使用的奖励函数

$$r(x, y) = r_\phi(x, y) - \beta(\log \pi_\theta(y|x) - \log \pi_{\text{ref}}(y|x))$$

其中：
- $r_\phi(x, y)$：奖励模型的分数
- $\beta(\log \pi_\theta(y|x) - \log \pi_{\text{ref}}(y|x))$：KL 惩罚项（每个 token 的即时惩罚）
- $\beta$：控制偏离参考策略的程度

---

## 五、完整数学公式流程

```mermaid
flowchart LR
    A["偏好数据<br/>(x, y_w, y_l)"] --> B["Bradley-Terry 模型<br/>p(y_w ≻ y_l|x) = σ(r(x,y_w) - r(x,y_l))"]
    B --> C["MLE 训练奖励模型<br/>L_R = -log σ(r_φ(x,y_w) - r_φ(x,y_l))"]
    C --> D["奖励模型 r_φ"]
    D --> E["KL 约束 RL 目标<br/>max E[r_φ] - β·KL(π_θ || π_ref)"]
    E --> F["PPO 算法<br/>策略梯度 + 裁剪"]
    F --> G["对齐后的策略 π_θ"]

    style A fill:#fff3e0,stroke:#ff9800
    style B fill:#f3e5f5,stroke:#9c27b0
    style C fill:#e3f2fd,stroke:#1976d2
    style D fill:#e8f5e9,stroke:#388e3c
    style E fill:#fce4ec,stroke:#d32f2f
    style F fill:#fff8e1,stroke:#f57f17
    style G fill:#e8f5e9,stroke:#388e3c
```

### 完整公式链

**Step 1 — Bradley-Terry 偏好模型：**

$$p^*(y_w \succ y_l | x) = \frac{\exp(r^*(x, y_w))}{\exp(r^*(x, y_w)) + \exp(r^*(x, y_l))}$$

**Step 2 — 奖励模型 MLE 损失：**

$$L_R(r_\phi, D) = -\mathbb{E}_{(x,y_w,y_l)\sim D} \left[ \log \sigma(r_\phi(x, y_w) - r_\phi(x, y_l)) \right]$$

**Step 3 — KL 约束的 RL 目标：**

$$\max_{\pi_\theta} \mathbb{E}_{x\sim D, y\sim\pi_\theta(y|x)} \left[ r_\phi(x, y) \right] - \beta \cdot D_{KL}\left( \pi_\theta(y|x) \parallel \pi_{\text{ref}}(y|x) \right)$$

**Step 4 — PPO 实际优化目标（含裁剪）：**

$$L^{CLIP}(\theta) = \mathbb{E} \left[ \min\left( \frac{\pi_\theta(y|x)}{\pi_{\text{old}}(y|x)} A, \text{clip}\left( \frac{\pi_\theta(y|x)}{\pi_{\text{old}}(y|x)}, 1-\epsilon, 1+\epsilon \right) A \right) \right]$$

---

## 六、DPO vs RLHF 对比架构

```mermaid
flowchart TB
    subgraph RLHF["传统 RLHF 流程"]
        direction TB
        R1["偏好数据<br/>(x, y_w, y_l)"] --> R2["训练奖励模型 r_φ<br/>（MLE on BT 模型）"]
        R2 --> R3["从 π_θ 采样回答"]
        R3 --> R4["PPO 优化<br/>最大化奖励 + KL 约束"]
        R4 --> R3
    end

    subgraph DPO["DPO 流程（本文）"]
        direction TB
        D1["偏好数据<br/>(x, y_w, y_l)"] --> D2["重参数化<br/>r(x,y) = β log(π_θ/π_ref)"]
        D2 --> D3["直接优化策略<br/>L_DPO = -log σ(β log(π_θ(y_w)/π_ref(y_w)) - β log(π_θ(y_l)/π_ref(y_l)))"]
        D3 --> D4["对齐后的策略 π_θ"]
    end

    RLHF -.-> |"无需奖励模型<br/>无需 RL"| DPO

    style RLHF fill:#fce4ec,stroke:#d32f2f
    style DPO fill:#e8f5e9,stroke:#388e3c
```

### DPO 损失函数

$$L_{DPO}(\pi_\theta; \pi_{\text{ref}}) = -\mathbb{E}_{(x,y_w,y_l)\sim D} \left[ \log \sigma\left( \beta \log\frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta \log\frac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)} \right) \right]$$

---

## 七、关键符号说明

| 符号 | 含义 | 说明 |
|------|------|------|
| $\pi_{\text{pretrain}}$ | 预训练语言模型 | 无监督训练的基座模型 |
| $\pi_{\text{SFT}}$ | 监督微调后的模型 | 在高质量数据上 SFT 后的基础模型 |
| $\pi_{\text{ref}}$ | 参考策略 | 通常 = $\pi_{\text{SFT}}$，在 RL 阶段冻结 |
| $\pi_\theta$ | 正在优化的策略 | RL 阶段被训练的模型 |
| $r^*(x, y)$ | 真实奖励函数 | 人类心目中的理想评分（不可观测） |
| $r_\phi(x, y)$ | 参数化的奖励模型 | 从偏好数据中学习到的近似奖励 |
| $\beta$ | KL 散度系数 | 控制策略偏离参考策略的程度 |
| $y_w$ | 偏好回答 | 人类标注者更喜欢的回答 |
| $y_l$ | 非偏好回答 | 人类标注者不喜欢的回答 |
| $D_{KL}$ | KL 散度 | 衡量两个概率分布之间的差异 |
| $\sigma$ | Logistic 函数 | $\sigma(z) = 1/(1+e^{-z})$ |

---

## 八、RLHF 各阶段计算成本对比

| 阶段 | 所需资源 | 训练时间 | 稳定性 |
|------|---------|---------|-------|
| **SFT** | 标准 GPU 训练 | 较短 | 稳定 |
| **奖励建模** | 标准 GPU 训练 | 较短 | 稳定 |
| **PPO RL 微调** | 需要从 LM 采样 + 价值函数网络 | 较长 | 不稳定，需大量调参 |
| **DPO（替代方案）** | 仅需前向传播计算 log-prob | 较短 | 稳定，几乎无需调参 |

---

*基于 Rafailov et al., "Direct Preference Optimization: Your Language Model is Secretly a Reward Model", NeurIPS 2023.*

---

Written by LLM-for-Zotero.
