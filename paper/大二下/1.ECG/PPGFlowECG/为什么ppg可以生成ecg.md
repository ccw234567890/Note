---
title: "PPGFlowECG: Latent Rectified Flow with Cross-Modal Encoding for PPG-Guided ECG Generation and Cardiovascular Disease Detection"
citekey: ""
doi: "10.48550/arXiv.2509.19774"
year: 2026
journal: ""
created: 2026-04-16
tags: [zotero, paper-note]
---

# PPGFlowECG: Latent Rectified Flow with Cross-Modal Encoding for PPG-Guided ECG Generation and Cardiovascular Disease Detection

## 一、PPG 是什么？

**PPG（Photoplethysmography，光电容积脉搏波）** 是一种光学检测技术，通过测量血管中血容量随心跳的周期性变化来获取脉搏信号。

**工作原理**：
- 用LED光照射皮肤（通常指尖或手腕）
- 光电探测器测量反射/透射光的强度变化
- 每次心跳时血管扩张→血容量增加→光吸收增加→信号变化

**特点**：
- ✅ **可穿戴友好**：智能手表、手环、指夹式设备都能采集
- ✅ **无创、低成本**
- ❌ **信息量有限**：只反映外周血管的容积变化，不直接反映心脏电活动

## 二、为什么可以从 PPG 生成 ECG？

PPG 和 ECG 之间存在**生理上的耦合关系**：

### 2.1 生理耦合

> ECG and PPG signals are physiologically coupled through the cardiac cycle. Each heartbeat triggers both electrical depolarization (ECG) and mechanical blood ejection (PPG).

(Fang et al., 2026)

每次心跳产生两个信号：
1. **ECG**：心脏的电活动（P波→QRS波群→T波）
2. **PPG**：血液被泵出后到达外周血管的机械效应

### 2.2 映射关系

```
心脏电活动（ECG）→ 心肌收缩 → 血液泵出 → 血管扩张（PPG）
```

两者通过**同一个心动周期**耦合，因此理论上存在一个映射函数 $f: \text{PPG} \to \text{ECG}$。

### 2.3 为什么难？

虽然存在生理耦合，但这个映射**不是简单的函数**：

| 挑战 | 原因 |
|------|------|
| **非线性** | 电→机械的转换涉及复杂的生理过程 |
| **个体差异** | 不同人的心率、血管弹性、信号形态不同 |
| **噪声干扰** | 运动伪影、基线漂移等 |
| **时间错位** | ECG 的 QRS 波群与 PPG 的峰值之间有延迟（脉搏传输时间，PTT） |

这就是为什么需要深度学习模型来学习这个映射，而不是简单的公式。

## 三、什么是映射关系？

**映射**（Mapping）简单说就是**一个输入对应一个输出的规则**：

$$f: X \to Y$$

- 输入 $X$ → 通过规则 $f$ → 输出 $Y$
- 每个输入 $x$ 对应一个输出 $y = f(x)$

### 3.1 论文中的映射

论文要学习的就是这个映射：

$$f: \text{PPG波形} \to \text{ECG波形}$$

**输入**：一段10秒的PPG信号（128Hz，共1280个采样点）
**输出**：对应的10秒ECG信号（同样1280个采样点）

### 3.2 映射的复杂性

| 映射类型 | 例子 | 难度 |
|---------|------|------|
| **简单映射** | $y = 2x + 1$ | 一个公式搞定 |
| **中等映射** | 身份证号→个人信息 | 查表即可 |
| **复杂映射** | 照片→照片中的人名 | 需要深度学习 |
| **PPG→ECG** | 脉搏波→心电图 | **非常复杂** |

> The mapping from PPG to ECG is highly nonlinear, subject-dependent, and corrupted by motion artifacts.

(Fang et al., 2026)

### 3.3 两阶段映射

论文把 PPG→ECG 这个复杂映射拆成两个阶段：

```
Stage 1: PPG → 潜在空间 ← ECG（对齐映射）
Stage 2: 噪声 + PPG条件 → ECG潜在（生成映射）
```

**Stage 1 的映射**（CardioAlign Encoder）：

$$E_{CA}: \text{PPG} \to z_{ppg}, \quad E_{CA}: \text{ECG} \to z_{ecg}$$

把两个信号映射到同一个潜在空间，让 $z_{ppg} \approx z_{ecg}$。

**Stage 2 的映射**（Latent Rectified Flow）：

$$v_\theta: (x_t, t, c) \to \text{方向向量}$$

学习从噪声到目标潜在表示的**直线路径**。

### 3.4 三层次对齐确保映射质量

| 损失 | 作用 | 类比 |
|------|------|------|
| **全局分布对齐** $L_{GDA}$ | 让PPG和ECG的潜在分布整体接近 | 让两个人的身高体重分布相似 |
| **局部实例判别** $L_{LID}$ | 保持个体身份信息 | 确保张三的PPG→张三的ECG，不是李四的 |
| **语义可解码性** $L_{SDC}$ | 确保潜在表示能还原回信号 | 压缩后的照片还能解压回原图 |

## 四、流匹配（Rectified Flow）在这里是怎么用的？

### 4.1 核心思想

流匹配是一种**生成模型**，它的目标是将一个简单的分布（高斯噪声）**逐步变形**为目标数据分布。

**关键创新**：修正流让这个变形路径是**直线**，而不是像扩散模型那样的弯曲路径。

### 4.2 在论文中的具体用法

论文使用**两阶段框架**，流匹配用在 **Stage 2**：

#### Stage 1：CardioAlign Encoder（对齐）

先把 PPG 和 ECG 映射到**共享的潜在空间**，让两者的表示在语义上对齐。

#### Stage 2：Latent Rectified Flow（生成）

在潜在空间中，从高斯噪声 $z$ 生成 ECG 潜在表示 $y$，以 PPG 潜在表示 $c$ 为条件：

**线性插值路径**（$t \in [0, 1]$）：

$$x_t = (1 - t)z + t y$$

- $t=0$：纯噪声 $z$
- $t=1$：目标 ECG 潜在 $y$
- 中间时刻：两者的线性混合

**学习目标**：训练一个神经网络 $v_\theta$ 来预测**最优漂移方向**：

$$\mathcal{L}(\theta) = \mathbb{E}_{z, y, t} \left\| v_\theta(x_t, t, c) - (y - z) \right\|_2^2$$

**直观理解**：网络学习"从当前位置指向目标位置的方向向量"。

### 4.3 推理过程

训练好后，生成 ECG 的过程是：

```
1. 采样高斯噪声 z ~ N(0, I)
2. 从 t=0 到 t=1，用 ODE 求解器逐步更新：
   x_{k+1} = x_k + Δt · v_θ(x_k, t_k, c)
3. 最终 x_T 就是生成的 ECG 潜在表示
4. 通过解码器重建为 ECG 波形
```

### 4.4 为什么用流匹配而不是扩散模型？

> When $\bar{\kappa} \to 0$, the optimal drift approaches a spatially invariant field, i.e., $\nabla_x v^* \to 0$.

(Fang et al., 2026)

**翻译成人话**：
- Stage 1 的对齐使得 PPG 和 ECG 在潜在空间中**已经很接近**
- 因此从噪声到目标的路径**接近直线**
- 直线路径可以用**很少的步数**（论文中 T=5 到 10 步）精确求解
- 相比之下，扩散模型通常需要 50-1000 步

### 4.5 一个直观类比

```
扩散模型：从山顶到山脚，走一条弯弯曲曲的小路（很多步）
修正流：  从山顶到山脚，直接坐缆车直线下降（很少步）
```

Stage 1 的对齐相当于把"山顶"和"山脚"拉近，让缆车线路更短更直。

## 五、数学形式化

论文中的映射最终可以写成：

$$x_{ecg} = D_{ECG}\left(\text{ODE}_{\text{solve}}\left(v_\theta(\cdot, \cdot, E_{CA}(x_{ppg})), z \sim \mathcal{N}(0,I)\right)\right)$$

**翻译成人话**：

1. 把PPG $x_{ppg}$ 编码到潜在空间 → $c = E_{CA}(x_{ppg})$
2. 从噪声 $z$ 开始，用流模型 $v_\theta$ 逐步生成 → ECG潜在表示
3. 解码成ECG波形 → $x_{ecg}$

整个流程就是一个**复合映射**：PPG波形 → ECG波形。

## 六、总结

| 概念 | 一句话理解 |
|------|-----------|
| **PPG** | 用光照皮肤测脉搏，可穿戴设备常用 |
| **PPG→ECG 可行** | 两者通过心动周期生理耦合，存在映射关系 |
| **映射关系** | 输入对应输出的规则，PPG→ECG是复杂非线性映射 |
| **流匹配** | 学习从噪声到目标的直线路径，用很少步数生成高质量ECG |
| **为什么有效** | Stage 1 对齐让路径变直 → Stage 2 用很少步就能精确生成 |

## References

Fang, X., Jin, J., Wang, H., Liu, C., Cai, J., Xiao, Y., Nie, G., Liu, B., Huang, S., Li, H., & Hong, S. (2026). *PPGFlowECG: Latent Rectified Flow with Cross-Modal Encoding for PPG-Guided ECG Generation and Cardiovascular Disease Detection*. arXiv:2509.19774. https://doi.org/10.48550/arXiv.2509.19774

---

Written by LLM-for-Zotero.
