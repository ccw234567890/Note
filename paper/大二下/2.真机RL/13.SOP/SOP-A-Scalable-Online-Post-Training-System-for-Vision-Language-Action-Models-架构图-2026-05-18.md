---
title: "SOP: A Scalable Online Post-Training System for Vision-Language-Action Models"
citekey: ""
doi: "10.48550/arXiv.2601.03044"
year: 2026
journal: ""
created: 2026-05-18
tags: [zotero, paper-note, architecture]
---

# SOP: A Scalable Online Post-Training System for Vision-Language-Action Models

## SOP 系统架构图

```mermaid
graph TB
    subgraph "Robot Fleet (N Actors)"
        direction TB
        R1["Robot Actor 1<br/>边缘端客户端"]
        R2["Robot Actor 2<br/>边缘端客户端"]
        R3["Robot Actor ...<br/>边缘端客户端"]
        RN["Robot Actor N<br/>边缘端客户端"]
    end

    subgraph "Data Flow"
        direction LR
        EP["Episode 执行<br/>策略 πθ 收集 rollout τ_π<br/>人类干预 τ_H"]
        BUFF["本地缓冲<br/>episode 边界异步上传"]
    end

    subgraph "Cloud Infrastructure"
        direction TB
        OB["对象存储<br/>Object Storage"]
        B_ON["在线缓冲区 B_on(t)<br/>追加所有机器人上传的 episodes"]
        B_OFF["离线缓冲区 B_off<br/>静态人类示范数据"]
        SAMPLER["自适应采样器 S_j<br/>公式(3): 动态在线/离线比例"]
        LEARNER["云端学习器<br/>异步训练更新策略参数 θ"]
    end

    subgraph "Model Sync"
        PUBSUB["发布-订阅通道<br/>Pub-Sub Channel"]
    end

    R1 --> EP
    R2 --> EP
    R3 --> EP
    RN --> EP
    EP --> BUFF
    BUFF -->|"异步上传"| OB
    OB -->|"追加"| B_ON
    B_ON --> SAMPLER
    B_OFF --> SAMPLER
    SAMPLER -->|"训练批次 ξ_j"| LEARNER
    LEARNER -->|"更新后策略 θ"| PUBSUB
    PUBSUB -->|"流式同步"| R1
    PUBSUB -->|"流式同步"| R2
    PUBSUB -->|"流式同步"| R3
    PUBSUB -->|"流式同步"| RN

    style R1 fill:#4a90d9,color:#fff
    style R2 fill:#4a90d9,color:#fff
    style R3 fill:#4a90d9,color:#fff
    style RN fill:#4a90d9,color:#fff
    style LEARNER fill:#e67e22,color:#fff
    style PUBSUB fill:#27ae60,color:#fff
    style B_ON fill:#8e44ad,color:#fff
    style B_OFF fill:#95a5a6,color:#fff
    style SAMPLER fill:#d35400,color:#fff
```

## SOP 算法流程

```mermaid
flowchart TD
    START(["开始: 预训练策略 πθ₀"]) --> BROADCAST["广播 πθ₀ 到所有 N 个 Actor"]
    BROADCAST --> PARALLEL{"并行执行"}

    subgraph "Actor i (并行)"
        direction TB
        EXEC["执行当前策略 πθ<br/>收集 rollout τ_π^i"]
        CHECK{"人类是否干预?"}
        INTERV["收集人类干预 τ_H^i"]
        UPLOAD["上传 τ_π^i ∪ τ_H^i<br/>到在线缓冲区 B_on"]
        APPLY["在 episode 边界<br/>应用更新后的策略"]
    end

    subgraph "Cloud Learner (异步)"
        direction TB
        NOTIFY["收到新数据通知"]
        SAMPLE["自适应采样 S_j<br/>ξ_j = S_j(B_on ∪ B_off)"]
        UPDATE["策略更新<br/>θ ← argmin E[L_PT(πθ; s, a)]"]
        STREAM["流式传输更新后策略 πθ<br/>到所有 Actor"]
    end

    PARALLEL --> EXEC
    EXEC --> CHECK
    CHECK -->|"是"| INTERV
    CHECK -->|"否"| UPLOAD
    INTERV --> UPLOAD
    UPLOAD --> NOTIFY
    NOTIFY --> SAMPLE
    SAMPLE --> UPDATE
    UPDATE --> STREAM
    STREAM --> APPLY
    APPLY -->|"继续下一轮"| EXEC

    style START fill:#2c3e50,color:#fff
    style BROADCAST fill:#2980b9,color:#fff
    style EXEC fill:#4a90d9,color:#fff
    style INTERV fill:#e74c3c,color:#fff
    style UPLOAD fill:#8e44ad,color:#fff
    style LEARNER fill:#e67e22,color:#fff
    style SAMPLE fill:#d35400,color:#fff
    style UPDATE fill:#e67e22,color:#fff
    style STREAM fill:#27ae60,color:#fff
    style APPLY fill:#16a085,color:#fff
```

## 自适应采样策略

```mermaid
flowchart LR
    subgraph "任务 m 的采样决策"
        direction TB
        L_ON["在线损失均值<br/>l̄^m_on = 1/W Σ l^m,i_on"]
        L_OFF["离线损失均值<br/>l̄^m_off = 1/W Σ l^m,i_off"]
        FORMULA["在线采样比例<br/>ω^m_on = exp(α·l̄^m_on) / (exp(α·l̄^m_on) + exp(l̄^m_off))"]
        CLIP["裁剪到 [0.2, 0.8]"]
        DECISION{"采样来源"}
        B_ON_M["从 B^m_on 采样<br/>概率 = ω^m_on"]
        B_OFF_M["从 B^m_off 采样<br/>概率 = 1 - ω^m_on"]
    end

    L_ON --> FORMULA
    L_OFF --> FORMULA
    FORMULA --> CLIP
    CLIP --> DECISION
    DECISION -->|"ω^m_on"| B_ON_M
    DECISION -->|"1-ω^m_on"| B_OFF_M

    style L_ON fill:#3498db,color:#fff
    style L_OFF fill:#95a5a6,color:#fff
    style FORMULA fill:#d35400,color:#fff
    style CLIP fill:#f39c12,color:#fff
    style B_ON_M fill:#8e44ad,color:#fff
    style B_OFF_M fill:#7f8c8d,color:#fff
```

## 核心公式

### 公式 (1): 后训练优化目标

$$
\theta_{k+1} = \arg\min_{\theta} \mathbb{E}_{(s,a) \sim D_k} L_{PT}(\pi_\theta; s, a)
$$

### 公式 (2): 训练批次采样

$$
\xi_j := S_j(B_{on}(t_j) \cup B_{off})
$$

其中 $$B_{on}(t) = \bigcup_{i=1}^{N} \tau^i(t)$$

### 公式 (3): 自适应在线采样比例

$$
\omega^m_{on} = \frac{\exp(\alpha \cdot \bar{l}^m_{on})}{\exp(\alpha \cdot \bar{l}^m_{on}) + \exp(\bar{l}^m_{off})}
$$

### 公式 (4): RECAP 行为正则化策略改进

$$
\hat{\pi}(a|s) \propto \pi_{ref}(a|s) \left( \frac{\pi_{ref}(a|I, s)}{\pi_{ref}(a|s)} \right)^\beta
$$

### 行为克隆损失函数

$$
L_{BC}(\pi_\theta; s, a) = -\log \pi_\theta(a|s)
$$

## 系统组件说明

| 组件 | 角色 | 关键特性 |
|------|------|---------|
| **Robot Actor** | 边缘端执行策略，收集经验 | 本地缓冲 episodes，episode 边界异步上传 |
| **对象存储** | 接收并存储上传数据 | 异步、非阻塞上传 |
| **在线缓冲区 B_on** | 动态增长的在线经验池 | 随时间 t 不断增大 |
| **离线缓冲区 B_off** | 静态人类示范数据 | 训练开始前准备好 |
| **自适应采样器 S_j** | 动态混合在线/离线数据 | 按任务均匀 + 按损失动态调整 |
| **云端学习器** | 异步训练更新策略 | 通过通知按需检索数据 |
| **发布-订阅通道** | 轻量级模型同步 | 端到端延迟秒到数十秒级 |

## 参考文献

Pan, M., Feng, S., Zhang, Q., Li, X., Song, J., Qu, C., Wang, Y., Li, C., Xiong, Z., Chen, Z., Liu, Y., & Luo, J. (2026). *SOP: A Scalable Online Post-Training System for Vision-Language-Action Models*. arXiv:2601.03044 [cs.RO]. https://doi.org/10.48550/arXiv.2601.03044

---

Written by LLM-for-Zotero.
