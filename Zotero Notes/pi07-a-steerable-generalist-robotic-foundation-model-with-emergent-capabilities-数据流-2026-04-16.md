---
title: "$\pi_{0.7}$: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities"
citekey: ""
doi: "10.48550/arXiv.2604.15483"
year: 2026
journal: ""
created: 2026-04-16
tags: [zotero, paper-note]
---

# $\pi_{0.7}$: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities

## 数据流总览

```mermaid
flowchart TD
    subgraph Input["输入层"]
        A1["多视角观测<br/>ot = [I₁ᵗ,...,Iₙᵗ, qᵗ]<br/>最多4摄像头×6帧历史<br/>448×448像素"]
        A2["本体感知状态<br/>qᵗ（关节位置）<br/>线性投影→token"]
        A3["提示上下文 Cᵗ<br/>语言指令 + 子任务<br/>+ 元数据 + 子目标图像"]
    end

    subgraph Encoding["编码层"]
        B1["MEM风格视频历史编码器<br/>时空压缩<br/>固定token数输出"]
        B2["视觉编码器<br/>400M参数<br/>Gemma3初始化"]
        B3["子目标图像编码器<br/>同视觉编码器<br/>最多3张（不含后视）"]
    end

    subgraph VLM["VLM骨干网络 4B<br/>Gemma3初始化"]
        C1["块因果注意力掩码<br/>观测token↔双向自注意力<br/>子目标token→可关注观测<br/>文本token→因果注意力"]
        C2["FAST token<br/>离散交叉熵损失<br/>知识隔离（KI）训练"]
    end

    subgraph ActionExpert["动作专家 860M"]
        D1["流匹配（Flow Matching）<br/>连续动作生成<br/>50步动作块"]
        D2["自适应RMSNorm<br/>注入流匹配时间步信息"]
        D3["实时动作分块（RTC）<br/>模拟0-12步推理延迟<br/>50Hz→240ms"]
    end

    subgraph Output["输出层"]
        E1["50步动作块 aₜ:ₜ₊ₕ<br/>关节级/末端执行器"]
        E2["PD控制器<br/>数值逆运动学<br/>执行Ĥ∈{15,25}步"]
    end

    A1 --> B1 --> B2 --> C1
    A2 --> C1
    A3 --> B3 --> C1
    C1 --> C2
    C1 -.->|"梯度隔离（不回流）"| D1
    C2 -->|"VLM激活"| D1
    D1 --> D2 --> D3 --> E1 --> E2
```

---

## 训练数据流

```mermaid
flowchart LR
    subgraph DataSources["数据源"]
        D1["演示数据<br/>高质量人类遥操作"]
        D2["自主数据<br/>策略评估rollout<br/>含失败/次优轨迹"]
        D3["人类干预数据<br/>策略rollout中<br/>人类接管记录"]
        D4["开源机器人数据集<br/>跨本体数据"]
        D5["π₀*.6 RL专家数据<br/>RL训练期间收集"]
        D6["自我中心人类视频<br/>第一人称操作视频"]
        D7["网络非机器人数据<br/>目标定位/VQA/文本"]
    end

    subgraph Annotation["标注层"]
        A1["子任务指令 l̂ᵗ<br/>语义子任务标注"]
        A2["片段元数据 m<br/>速度/质量(1-5)/错误标记"]
        A3["控制模式 c<br/>joint / end-effector"]
        A4["子目标图像 gᵗ<br/>真实未来帧 + 世界模型生成"]
    end

    subgraph Training["训练目标"]
        T1["VLM骨干<br/>max_θ E_D[log π_θ(FAST|o,C)]<br/>离散交叉熵"]
        T2["动作专家<br/>max_θ E_D[log π_θ(aₜ:ₜ₊ₕ|oₜ₋ₜ:ₜ, Cₜ)]<br/>流匹配近似下界"]
    end

    D1 --> A1 --> T1
    D2 --> A2 --> T1
    D3 --> A2 --> T1
    D4 --> A1 --> T1
    D5 --> A2 --> T1
    D6 --> A4 --> T1
    D7 --> A1 --> T1

    D1 --> A1 --> T2
    D2 --> A2 --> T2
    D3 --> A2 --> T2
    D4 --> A1 --> T2
    D5 --> A2 --> T2
    D6 --> A4 --> T2
    D7 --> A1 --> T2

    T1 -.->|"梯度隔离"| T2
```

---

## 推理数据流

```mermaid
sequenceDiagram
    participant HP as 高层策略
    participant WM as 世界模型 BAGEL 14B
    participant VLA as π₀.₇ VLA 模型
    participant Robot as 机器人

    Note over HP,Robot: 初始化
    HP->>VLA: 任务指令 l + 子任务指令 l̂ᵗ
    HP->>WM: 初始观测 o₀ + 子任务 l̂ᵗ + 元数据 m
    WM->>VLA: 子目标图像 g⋆ ~ p_ψ(g⋆|o₀, l̂ᵗ, m)
    VLA->>VLA: 组合上下文 C = {l, l̂ᵗ, g⋆, m, c}

    loop 每Ĥ步执行
        VLA->>VLA: 流匹配5步去噪<br/>生成50步动作块 aₜ:ₜ₊ₕ
        VLA->>VLA: CFG引导 β∈{1.3,1.7,2.2}<br/>∇logπ + β(∇logπ - ∇logπ_uncond)
        VLA->>Robot: 执行Ĥ∈{15,25}步动作
        Robot->>VLA: 新观测 oₜ
    end

    loop 每∆=4秒或子任务变化
        HP->>WM: 新子任务 l̂ᵗ（异步线程）
        WM->>VLA: 刷新子目标图像 g⋆（异步）
        VLA->>VLA: 更新上下文 C
    end
```

---

## 提示上下文组合数据流

```mermaid
flowchart TD
    subgraph Prompt["完整提示示例"]
        P1["<多视角观测>"]
        P2["<多视角子目标图像>"]
        P3["Task: peel vegetables."]
        P4["Subtask: pick up the peeler."]
        P5["Speed: 8000."]
        P6["Quality: 5."]
        P7["Mistake: false."]
        P8["Control Mode: joint."]
        P9["<本体感知>"]
    end

    subgraph Dropout["训练时随机丢弃策略"]
        D1["子目标图像：仅25%批次包含"]
        D2["子任务指令：有子目标时30%丢弃"]
        D3["元数据整体：15%丢弃"]
        D4["速度/质量/错误：各5%单独丢弃"]
        D5["控制模式：不丢弃"]
        D6["历史帧：30%丢弃"]
        D7["后视摄像头：30%丢弃"]
    end

    subgraph Runtime["推理时配置"]
        R1["速度：任务15百分位"]
        R2["质量：固定5（最高）"]
        R3["错误：固定false"]
        R4["子目标：子任务变化或每4秒刷新"]
        R5["CFG：对元数据应用β引导"]
    end

    P1 --> D6
    P2 --> D1 --> D2
    P3 --> D1
    P4 --> D2
    P5 --> D3 --> D4
    P6 --> D3 --> D4
    P7 --> D3 --> D4
    P8 --> D5

    D1 --> R4
    D2 --> R4
    D3 --> R1 & R2 & R3
    D4 --> R1 & R2 & R3
    D5 --> R5
```

---

## 子目标图像生成数据流

```mermaid
flowchart TD
    subgraph WorldModel["世界模型训练"]
        W1["训练数据 D_g<br/>高质量子任务标注片段"]
        W2["真实未来帧 g⋆ = o_end<br/>段末帧作为真值"]
        W3["网络数据<br/>视频编辑/图像生成"]
        W4["人类自我中心视频"]
    end

    subgraph Gen["子目标图像生成"]
        G1["输入：观测 oₜ + 子任务 l̂ᵗ + 元数据 m"]
        G2["BAGEL 14B<br/>Mixture-of-Transformers"]
        G3["流匹配目标<br/>max_ψ E[L_CFM(g⋆, g_ψ(o,l̂,m))]"]
        G4["输出：多视角子目标图像 g⋆"]
    end

    subgraph Sampling["训练时采样策略"]
        S1["25%概率：段末帧"]
        S2["75%概率：0-4秒随机未来帧"]
        S3["世界模型生成图像<br/>缓解训练-测试不匹配"]
    end

    subgraph Usage["推理时使用"]
        U1["异步生成<br/>独立线程"]
        U2["子任务变化时刷新"]
        U3["每∆=4秒刷新"]
        U4["VLA使用最新可用子目标"]
    end

    W1 --> W2 --> G2
    W3 --> G2
    W4 --> G2
    G1 --> G2 --> G3 --> G4
    G4 --> S1 & S2 & S3
    S1 & S2 & S3 -->|"训练π₀.₇"| U1
    U1 --> U2 & U3 --> U4
```

---

## 注意力掩码数据流

```mermaid
flowchart TD
    subgraph Tokens["Token序列"]
        T1["观测token<br/>多视角×多帧<br/>双向自注意力"]
        T2["子目标图像token<br/>最多3张<br/>双向自注意力"]
        T3["文本token<br/>任务+子任务+元数据<br/>因果注意力"]
        T4["动作token<br/>50步动作块<br/>双向自注意力"]
    end

    subgraph Attention["注意力流向"]
        A1["观测↔观测：✅ 双向"]
        A2["子目标→观测：✅ 可关注"]
        A3["观测→子目标：❌ 不可关注"]
        A4["子目标↔子目标：✅ 双向"]
        A5["文本→文本：✅ 因果（只看前面）"]
        A6["文本→观测/子目标：✅ 可关注"]
        A7["动作→全部VLM激活：✅ 可关注"]
        A8["动作↔动作：✅ 双向"]
    end

    T1 --> A1
    T2 --> A2 & A4
    T1 --> A3
    T3 --> A5 & A6
    T4 --> A7 & A8
```

---

## 关键参数汇总

| 参数 | 值 | 说明 |
|------|-----|------|
| VLM骨干 | 4B | Gemma3初始化 |
| 视觉编码器 | 400M | 含在VLM内 |
| 动作专家 | 860M | 流匹配Transformer |
| 总参数量 | ~5B | — |
| 输入摄像头 | 最多4个 | 前视+2腕部+后视 |
| 历史帧数 | 最多6帧/视角 | 步长1秒 |
| 子目标图像 | 最多3张 | 不含后视 |
| 图像分辨率 | 448×448 | — |
| 动作块长度 | 50步 | 固定 |
| 执行步数 Ĥ | 15-25步 | 可配置 |
| 推理延迟模拟 | 0-12步 | 240ms@50Hz |
| 去噪步数 | 5步 | 流匹配 |
| CFG权重 β | 1.3/1.7/2.2 | 元数据引导 |
| 子目标刷新间隔 ∆ | 4秒 | 或子任务变化时 |
| 控制模式 | joint / ee | 关节级/末端执行器 |
| 机器人频率 | 50Hz / 20Hz | UR5e为20Hz |

---

Written by LLM-for-Zotero.
