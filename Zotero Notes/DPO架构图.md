---
title: "DPO架构图"
created: 2025-07-17
tags: [zotero, paper-note]
---

# DPO 架构图

## 图 1：DPO 核心思想总览

```mermaid
flowchart TB
    subgraph Input["输入"]
        A["偏好数据集 D<br/>{x, y_w, y_l}"]
        B["参考策略 π_ref<br/>(初始 SFT 模型)"]
    end

    subgraph Core["DPO 核心：重参数化"]
        C["Bradley-Terry 偏好模型<br/>p*(y₁ ≻ y₂|x) = σ(r*(x,y₁) - r*(x,y₂))"]
        D["关键重参数化<br/>r(x,y) = β log(π_θ(y|x) / π_ref(y|x)) + β log Z(x)"]
        E["代入 BT 模型，Z(x) 抵消<br/>p(y_w ≻ y_l|x) = σ(β log(π_θ(y_w|x)/π_ref(y_w|x)) - β log(π_θ(y_l|x)/π_ref(y_l|x)))"]
    end

    subgraph Loss["DPO 损失函数"]
        F["L_DPO(π_θ; π_ref) = -E[log σ(β log(π_θ(y_w|x)/π_ref(y_w|x)) - β log(π_θ(y_l|x)/π_ref(y_l|x)))]"]
        G["= 二元交叉熵损失<br/>无需 RL，无需奖励模型"]
    end

    subgraph Gradient["梯度更新"]
        H["∇L_DPO = -β · E[ σ(r̂_θ(x,y_l) - r̂_θ(x,y_w)) · (∇log π(y_w|x) - ∇log π(y_l|x)) ]"]
        I["权重：隐式奖励估计错误越大，更新力度越大"]
        J["↑ 增加 y_w 概率"]
        K["↓ 降低 y_l 概率"]
    end

    A --> C
    B --> D
    C --> D
    D --> E
    E --> F
    F --> G
    F --> H
    H --> I
    H --> J
    H --> K
```

---

## 图 2：DPO 训练流程

```mermaid
flowchart LR
    subgraph Step1["步骤 1：准备偏好数据"]
        A1["SFT 模型 π_SFT"]
        A2["对每个提示 x<br/>采样 y₁, y₂ ~ π_SFT(·|x)"]
        A3["人类标注偏好<br/>y_w ≻ y_l"]
        A4["构建离线数据集<br/>D = {xⁱ, y_wⁱ, y_lⁱ}"]
    end

    subgraph Step2["步骤 2：DPO 训练"]
        B1["初始化 π_θ = π_SFT<br/>π_ref = π_SFT"]
        B2["对每个 batch<br/>(x, y_w, y_l) ~ D"]
        B3["计算隐式奖励<br/>r̂_θ(x,y) = β log(π_θ(y|x)/π_ref(y|x))"]
        B4["计算 DPO 损失<br/>L = -log σ(r̂_θ(x,y_w) - r̂_θ(x,y_l))"]
        B5["梯度下降更新 θ"]
    end

    subgraph Output["输出"]
        C1["对齐后的策略 π_θ"]
        C2["隐式奖励模型 r̂_θ"]
    end

    A1 --> A2 --> A3 --> A4 --> B1
    B1 --> B2 --> B3 --> B4 --> B5
    B5 -.->|"迭代"| B2
    B5 --> C1
    B5 --> C2
```

---

## 图 3：DPO vs RLHF（PPO）架构对比

```mermaid
flowchart TB
    subgraph RLHF["传统 RLHF（PPO）— 两阶段"]
        direction TB
        RLHF_Data["偏好数据集 D"]
        RLHF_RM["阶段 1：训练奖励模型 r_φ<br/>L_R = -E[log σ(r_φ(x,y_w) - r_φ(x,y_l))]"]
        RLHF_Policy["阶段 2：PPO RL 微调<br/>max E[r_φ(x,y)] - β·KL(π_θ || π_ref)<br/>需要：策略网络 + 价值网络 + 采样"]
        RLHF_Out["对齐策略 π_θ"]
        
        RLHF_Data --> RLHF_RM --> RLHF_Policy --> RLHF_Out
    end

    subgraph DPO["DPO（本文）— 单阶段"]
        direction TB
        DPO_Data["偏好数据集 D"]
        DPO_Loss["直接优化策略 π_θ<br/>L_DPO = -E[log σ(β log(π_θ(y_w|x)/π_ref(y_w|x)) - β log(π_θ(y_l|x)/π_ref(y_l|x)))]"]
        DPO_Out["对齐策略 π_θ<br/>+ 隐式奖励模型 r̂_θ"]
        
        DPO_Data --> DPO_Loss --> DPO_Out
    end

    RLHF -.->|"vs"| DPO
```

---

## 图 4：数学公式推导链

```mermaid
flowchart LR
    A["RLHF 目标<br/>max E[r(x,y)] - β·KL(π || π_ref)"]
    B["最优策略闭式解<br/>π*(y|x) = (1/Z(x))·π_ref(y|x)·exp((1/β)·r(x,y))"]
    C["重参数化：用策略表示奖励<br/>r(x,y) = β log(π*(y|x)/π_ref(y|x)) + β log Z(x)"]
    D["代入 Bradley-Terry 模型<br/>Z(x) 抵消"]
    E["偏好概率仅用策略表示<br/>p(y_w ≻ y_l|x) = σ(β log(π*(y_w|x)/π_ref(y_w|x)) - β log(π*(y_l|x)/π_ref(y_l|x)))"]
    F["DPO 最大似然目标<br/>L_DPO = -E[log σ(β log(π_θ(y_w|x)/π_ref(y_w|x)) - β log(π_θ(y_l|x)/π_ref(y_l|x)))]"]
    G["梯度<br/>∇L = -β·E[σ(r̂_l - r̂_w)·(∇log π(y_w) - ∇log π(y_l))]"]

    A -->|"推导"| B -->|"取对数"| C -->|"代入 BT"| D -->|"化简"| E -->|"MLE"| F -->|"求导"| G
```

---

## 图 5：DPO 梯度权重机制详解

```mermaid
flowchart TB
    subgraph Case1["情况 1：模型已正确排序"]
        A1["r̂_θ(x,y_w) >> r̂_θ(x,y_l)"]
        B1["σ(r̂_l - r̂_w) ≈ 0"]
        C1["梯度权重 ≈ 0"]
        D1["几乎不更新<br/>（模型已经做对了）"]
        A1 --> B1 --> C1 --> D1
    end

    subgraph Case2["情况 2：模型排序错误"]
        A2["r̂_θ(x,y_w) << r̂_θ(x,y_l)"]
        B2["σ(r̂_l - r̂_w) ≈ 1"]
        C2["梯度权重 ≈ β"]
        D2["大力更新<br/>（模型做错了，需要纠正）"]
        A2 --> B2 --> C2 --> D2
    end

    subgraph Case3["情况 3：模型不确定"]
        A3["r̂_θ(x,y_w) ≈ r̂_θ(x,y_l)"]
        B3["σ(r̂_l - r̂_w) ≈ 0.5"]
        C3["梯度权重 ≈ 0.5β"]
        D3["适度更新<br/>（模型分不清，需要学习）"]
        A3 --> B3 --> C3 --> D3
    end
```

---

## 图 6：DPO 实验设置与结果

```mermaid
flowchart TB
    subgraph Tasks["三个评估任务"]
        T1["可控情感生成<br/>IMDb 评论<br/>GPT-2 large<br/>自动情感分类器标注"]
        T2["摘要生成<br/>Reddit TL;DR<br/>GPT-J (6B)<br/>人类标注"]
        T3["单轮对话<br/>Anthropic HH<br/>Pythia 2.8B<br/>人类标注"]
    end

    subgraph Baselines["对比基线"]
        B1["PPO（标准 RLHF）"]
        B2["PPO-GT（使用真实奖励）"]
        B3["Preferred-FT（监督微调）"]
        B4["Unlikelihood"]
        B5["Best of N"]
        B6["Zero-shot / Few-shot"]
    end

    subgraph Results["关键结果"]
        R1["情感任务：DPO 的 Reward-KL 前沿<br/>严格支配 PPO，甚至超过 PPO-GT"]
        R2["摘要：DPO 胜率 61% > PPO 57%<br/>对采样温度更鲁棒"]
        R3["对话：DPO 唯一显著改进<br/>超过偏好回答本身"]
        R4["分布外泛化：DPO 0.36 > PPO 0.26<br/>（CNN/DailyMail 新闻摘要）"]
    end

    T1 --> R1
    T2 --> R2
    T3 --> R3
    T2 --> R4
    B1 --> Results
    B2 --> Results
    B3 --> Results
    B4 --> Results
    B5 --> Results
    B6 --> Results
```

---

## 图 7：DPO 与 RLHF 详细对比

```mermaid
flowchart TB
    subgraph Compare["DPO vs RLHF (PPO) 对比"]
        direction TB
        C1["┌──────────────────────────────────────┬──────────────────────┬──────────────────────┐
│              维度              │      RLHF (PPO)      │        DPO          │
├──────────────────────────────────────┼──────────────────────┼──────────────────────┤
│ 训练流程                           │ 两阶段：RM → RL     │ 单阶段：直接优化     │
│ 是否需要奖励模型                   │ 是                   │ 否（隐式奖励）       │
│ 是否需要 RL 算法                   │ 是（PPO）           │ 否（交叉熵损失）     │
│ 是否需要从 LM 采样                 │ 是                   │ 否                   │
│ 是否需要价值网络                   │ 是                   │ 否                   │
│ 超参数数量                         │ 多                   │ 少（仅 β）          │
│ 训练稳定性                         │ 不稳定               │ 稳定                 │
│ Reward-KL 效率                     │ 较低                 │ 更高                 │
│ 温度鲁棒性                         │ 差                   │ 好                   │
│ 分布外泛化                         │ 一般                 │ 更好                 │
│ 实现复杂度                         │ 高                   │ 低                   │
└──────────────────────────────────────┴──────────────────────┴──────────────────────┘"]
    end
```

---

## 关键符号说明

| 符号                                                                                  | 含义                                             |
| ----------------------------------------------------------------------------------- | ---------------------------------------------- |
| $$x$$                                                                               | 提示（prompt）                                     |
| $$y_w$$                                                                             | 人类偏好的回答（winning response）                      |
| $$y_l$$                                                                             | 人类不偏好的回答（losing response）                      |
| $$\pi_\theta$$                                                                      | 正在优化的策略（语言模型）                                  |
| $$\pi_{\text{ref}}$$                                                                | 参考策略（初始 SFT 模型）                                |
| $$r(x,y)$$                                                                          | 奖励函数                                           |
| $$\hat{r}_\theta(x,y) = \beta \log\frac{\pi_\theta(y\|x)}{\pi_{\text{ref}}(y\|x)}$$ | 隐式奖励（由策略定义）                                    |
| $$\beta$$                                                                           | KL 散度约束系数                                      |
| $$\sigma$$                                                                          | logistic 函数 $$\sigma(z) = \frac{1}{1+e^{-z}}$$ |
| $$Z(x)$$                                                                            | 配分函数（partition function）                       |
| $$D_{KL}$$                                                                          | KL 散度                                          |

---

## 核心公式总结

**Bradley-Terry 偏好模型：**

$$p^*(y_1 \succ y_2 | x) = \frac{\exp(r^*(x, y_1))}{\exp(r^*(x, y_1)) + \exp(r^*(x, y_2))} = \sigma(r^*(x, y_1) - r^*(x, y_2))$$

**RLHF 目标：**

$$\max_{\pi_\theta} \mathbb{E}_{x\sim D, y\sim\pi_\theta(y|x)}[r_\phi(x, y)] - \beta \cdot D_{KL}(\pi_\theta(y|x) \parallel \pi_{\text{ref}}(y|x))$$

**最优策略闭式解：**

$$\pi^*(y|x) = \frac{1}{Z(x)} \pi_{\text{ref}}(y|x) \exp\left(\frac{1}{\beta} r(x, y)\right)$$

**DPO 重参数化：**

$$r(x, y) = \beta \log\frac{\pi^*(y|x)}{\pi_{\text{ref}}(y|x)} + \beta \log Z(x)$$

**DPO 损失函数：**

$$L_{DPO}(\pi_\theta; \pi_{\text{ref}}) = -\mathbb{E}_{(x,y_w,y_l)\sim D} \left[ \log \sigma\left( \beta \log\frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta \log\frac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)} \right) \right]$$

**DPO 梯度：**

$$\nabla_\theta L_{DPO} = -\beta \cdot \mathbb{E}_{(x,y_w,y_l)\sim D} \left[ \sigma(\hat{r}_\theta(x, y_l) - \hat{r}_\theta(x, y_w)) \left( \nabla_\theta \log \pi(y_w|x) - \nabla_\theta \log \pi(y_l|x) \right) \right]$$

---

Written by LLM-for-Zotero.
