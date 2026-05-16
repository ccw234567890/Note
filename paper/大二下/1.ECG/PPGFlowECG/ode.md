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

## ODE 的生成机制

在 Stage 2 的潜在修正流（Latent Rectified Flow）中，生成 ECG 潜在表示的过程就是解一个一阶常微分方程（ODE）：

\[
\frac{dx_t}{dt} = v_\theta(x_t, t, c), \qquad t \in [0, 1]
\]

其中：
- \(x_t\) 是当前时刻 \(t\) 的潜在状态
- \(c = z_{ppg}\) 是 PPG 的潜在表示（条件）
- \(v_\theta\) 是学到的条件速度场（vector field）

直觉上，这个 ODE 描述了"从噪声起点 \(x_0 = z\) 沿着速度场逐渐移动，最后到达 ECG 潜在向量 \(y\)"的动力学轨迹。

## ODE 的数值求解方法

理论上，任何标准 ODE 求解器都能用：

- **显式欧拉法（Euler）** — 论文选用的方法
- **隐式欧拉法**
- **Runge–Kutta 系列**（RK2, RK4）
- **Adams–Bashforth**
- **Dormand–Prince**（自适应步长）
- 其他自适应步长求解器

论文为了效率，选用了**显式欧拉法**，迭代公式为：

\[
x_{k+1} = x_k + \Delta t \cdot v_\theta(x_k, t_k, c), \quad k = 0, 1, \ldots, T-1
\]

其中 \(\Delta t = 1/T\)，\(t_k = k \cdot \Delta t\)，\(x_0 = z \sim \mathcal{N}(0, I)\)。只需跑 \(T\) 步（论文中 \(T\) 取 5~10），就能得到 \(x_T \approx y\)，再通过冻结的 ECG 解码器重建为波形。

## 解 ODE 与流匹配的关系

Stage 2 包含两个阶段：

1. **训练（流匹配，Flow Matching）**：在潜在空间里学习条件速度场 \(v_\theta\)，让它逼近"理想漂移" \(y - z\)：

\[
\mathcal{L}(\theta) = \mathbb{E}_{z \sim \mathcal{N}(0,I), y, t \sim U(0,1)} \left\| v_\theta(x_t, t, c) - (y - z) \right\|_2^2
\]

2. **推理（解 ODE，ODE Solve）**：利用已经学好的 \(v_\theta\)，从噪声 \(z\) 出发积分到 \(t=1\)，得到 ECG 潜在表示。

因此，**解 ODE 的过程就是流匹配将噪声推理为 ECG 的过程**。流匹配负责学出速度场，解 ODE 则执行这个速度场，把噪声逐渐运输成 ECG 潜在表示。

## 为什么可以用很少的步数

由于 Stage 1（CardioAlign Encoder）使 \(y\) 和 \(c\) 在潜在空间中接近，学习到的动力学近似线性，轨迹曲率 \(x_t^{(2)} \approx 0\)，从而大幅降低数值误差，支持仅用 5-10 步 ODE 求解即可稳定生成。

## References

Fang, X., Jin, J., Wang, H., Liu, C., Cai, J., Xiao, Y., Nie, G., Liu, B., Huang, S., Li, H., & Hong, S. (2026). *PPGFlowECG: Latent Rectified Flow with Cross-Modal Encoding for PPG-Guided ECG Generation and Cardiovascular Disease Detection*. arXiv:2509.19774.

---

Written by LLM-for-Zotero.
