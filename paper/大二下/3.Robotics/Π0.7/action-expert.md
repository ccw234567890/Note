
# $π_{0.7}$: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities

## 动作专家（Action Expert）关键技术详解

### 一、自适应 RMSNorm（Adaptive RMSNorm）注入时间步信息

论文原文（Section VI-B）：

> "We use adaptive RMSNorm to inject timestep information for flow matching."

**工作原理**：

流匹配（Flow Matching）是一个去噪过程，需要知道当前处于去噪的哪个时间步（timestep）。自适应 RMSNorm 的做法是：

- 标准 RMSNorm：$y = \frac{x}{\text{RMS}(x)} \odot \gamma$，其中 $\gamma$ 是固定可学习参数
- 自适应 RMSNorm：$\gamma(t) = \text{MLP}(t)$，根据去噪时间步 $t$ 动态生成缩放参数
- 去噪早期（$t \approx 1$，纯噪声）：$\gamma(t)$ 让模型关注全局结构
- 去噪后期（$t \approx 0$，接近干净动作）：$\gamma(t)$ 让模型关注精细细节

**RMSNorm 数学原理**（Zhang & Sennrich, 2019）：

$$\text{RMSNorm}(x) = \frac{x}{\sqrt{\frac{1}{d}\sum_{i=1}^{d} x_i^2 + \epsilon}} \odot \gamma$$

相比 LayerNorm，RMSNorm 去掉了均值中心化步骤，只保留均方根归一化。LayerNorm 的成功主要来自缩放（除以标准差），而不是中心化（减去均值）。

**自适应 RMSNorm 完整流程**：

1. 计算 RMS：$\text{RMS}(x) = \sqrt{\text{mean}(x^2) + \epsilon}$
2. 归一化：$x_{\text{norm}} = x / \text{RMS}(x)$
3. 生成自适应参数：$\gamma(t) = \text{MLP}(\text{embed}(t))$
4. 应用：$y = \gamma(t) \odot x_{\text{norm}}$

---

### 二、实时动作分块（Real-Time Chunking, RTC）

论文原文（Section VI-B）：

> "π0.7 also employs the training-time version of real-time action chunking (RTC) for generating smooth action trajectories in the presence of inference delay."

**问题背景**：动作专家一次性预测 50 步的动作块，但推理需要时间（~240ms），直接执行旧的动作块会导致不连贯。

**RTC 核心思想**：训练时模拟推理延迟，让模型学会在有延迟的情况下仍然生成平滑的动作序列。新预测的动作块与已执行动作平滑衔接，避免跳跃。

---

### 三、训练时模拟 0-12 步延迟

论文原文（Section VI-B）：

> "During training, we simulate delays of 0 to 12 timesteps, corresponding to a maximum inference latency of 240ms on a 50Hz robot."

**具体做法**：

- 每个训练样本随机选择一个延迟 $d \in [0, 12]$
- 输入观测：$o_{t-d}$（模型看到的是 $d$ 步前的观测）
- 目标动作：$a_t, a_{t+1}, ..., a_{t+49}$（预测未来的 50 步动作）
- 模型必须学会从"过时的观测"预测"正确的未来动作"

**数值对应**：
- 50Hz 机器人：1 步 = 20ms
- 0-12 步延迟 = 0-240ms，覆盖实际推理中可能遇到的各种延迟情况

**目的**：
- 模拟推理延迟（实际推理需要 ~240ms）
- 增强鲁棒性，模型学会容忍观测延迟
- 结合 RTC，生成与已执行动作平滑衔接的新动作块

---

### 四、推理时执行 15-25 步，5 步去噪生成

论文原文（Section VII）：

> "For all experiments we use 5 denoising steps to generate the 50-step action chunks and execute Ĥ ∈ {15, 25} steps out of the chunk."

**5 步去噪的原因**：
- 流匹配比扩散模型更高效，步数更少
- 50 步动作块是低维连续空间，不需要大量去噪步数
- 5 步在质量和速度之间取得平衡

**执行 15-25 步的原因**：
- 预测 50 步动作块 $[a_0, a_1, ..., a_{49}]$
- 只执行前 $\hat{H}$ 步（$\hat{H} \in \{15, 25\}$）
- 丢弃剩余的 $50-\hat{H}$ 步
- 基于新观测重新预测下一个 50 步动作块

**完整推理流程**（Algorithm 1）：
1. 用 5 步去噪生成 50 步动作块
2. 执行前 $\hat{H}$ 步（15 或 25 步）
3. 等待执行完成
4. 获取最新观测
5. 回到步骤 1

**折中考虑**：
- 执行太少步（如 5 步）→ 计算开销大
- 执行太多步（如 50 步）→ 动作过时
- 15-25 步是经验上最优的折中

---

### 五、总结表格

| 技术 | 作用 | 具体实现 |
|------|------|---------|
| **自适应 RMSNorm** | 向动作专家注入去噪时间步信息 | 根据时间步 $t$ 生成 $\gamma(t)$，对 RMSNorm 输出做仿射变换 |
| **RTC（实时动作分块）** | 在推理延迟下生成平滑动作轨迹 | 训练时模拟延迟，让模型学会基于已执行动作历史预测新动作块 |
| **模拟 0-12 步延迟** | 训练模型容忍推理延迟 | 每个样本随机选 $d \in [0,12]$，用 $o_{t-d}$ 作为输入，预测 $a_t...a_{t+49}$ |
| **5 步去噪** | 从噪声生成 50 步动作块 | 流匹配只需 5 步即可收敛到高质量动作 |
| **执行 15-25 步** | 平衡反应速度与计算效率 | 预测 50 步，只执行前 $\hat{H}$ 步，然后基于新观测重新预测 |

---

## References

Intelligence, P., Ai, B., Amin, A., et al. (2026). *π₀.₇: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities*. arXiv:2604.15483.

---

Written by LLM-for-Zotero.
