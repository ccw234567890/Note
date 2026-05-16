现在我已经掌握了论文中关于Koopman算子数学原理的全部内容。下面进行系统讲解。

---

## Koopman算子的数学原理详解

### 一、核心思想：非线性 → 线性的"升维"魔法

Koopman算子的核心思想可以用一句话概括：

> **把非线性系统"提升"到无限维函数空间，在这个空间中动力学变成线性的。**

这就像用不同的视角看同一个问题——虽然状态本身的演化是非线性的，但如果我们观察的是状态的某种"函数"，这些函数的演化可以是线性的。

---

### 二、数学定义

#### 2.1 基本设定

考虑一个离散时间的**非线性**动力系统：

$$x_t = T(x_{t-1})$$

其中：

- $\mathcal{M} \subset \mathbb{R}^n$ 是一个有限维流形（系统所有可能状态的集合）
- $T: \mathcal{M} \to \mathcal{M}$ 是一个**非线性**映射
- $x_t \in \mathcal{M}$ 是系统在时刻 $t$ 的状态

#### 2.2 Koopman算子的定义

> **定义 2.1 (Koopman算子)** Koopman算子 $\mathcal{K}: \mathcal{H} \to \mathcal{H}$ 是一个作用在可观测函数上的**线性**算子，定义为：
> 
> $$(\mathcal{K}\varphi)(x) = \varphi(T(x)), \quad \text{for } \varphi \in \mathcal{H}, x \in \mathcal{M}.$$

(Cheng 等, 2025)

其中：

- $\mathcal{H} = L^2(\mathcal{M}, \mu)$ 是平方可积的可观测函数构成的**Hilbert空间**（无限维）
- $\varphi: \mathcal{M} \to \mathbb{R}$ 是任意一个"可观测函数"——可以理解为对系统状态的某种测量或观察
- $\mu$ 是流形 $\mathcal{M}$ 上的一个测度

#### 2.3 为什么这是线性的？

**关键**：$\mathcal{K}$ 是**线性算子**，因为对任意两个函数 $\varphi_1, \varphi_2 \in \mathcal{H}$ 和任意标量 $a, b \in \mathbb{R}$：

$$\mathcal{K}(a\varphi_1 + b\varphi_2)(x) = (a\varphi_1 + b\varphi_2)(T(x)) = a\varphi_1(T(x)) + b\varphi_2(T(x)) = a(\mathcal{K}\varphi_1)(x) + b(\mathcal{K}\varphi_2)(x)$$

**线性性成立！** ✅

#### 2.4 核心对比

||状态空间|可观测函数空间|
|---|---|---|
|空间|$mathcal{M}$（有限维流形）|$mathcal{H} = L^2(mathcal{M}, mu)$（无限维Hilbert空间）|
|演化规则|$x_t = T(x_{t-1})$|$varphi_t = mathcal{K}varphi_{t-1}$|
|线性性|❌ 非线性|✅ **线性**|
|维度|有限维 $n$|无限维|

---

### 三、Koopman算子的谱分解

线性算子 $\mathcal{K}$ 有**特征值和特征函数**（称为Koopman特征值和Koopman特征函数）：

$$\mathcal{K}\phi_j = \lambda_j \phi_j, \quad j = 1, 2, \dots$$

其中 $\lambda_j \in \mathbb{C}$ 是特征值，$\phi_j \in \mathcal{H}$ 是对应的特征函数。

**谱分解**：任意可观测函数 $\varphi$ 可以展开为特征函数的线性组合：

$$\varphi(x) = \sum_{j=1}^\infty c_j \phi_j(x)$$

那么在Koopman算子作用下：

$$(\mathcal{K}\varphi)(x) = \sum_{j=1}^\infty c_j (\mathcal{K}\phi_j)(x) = \sum_{j=1}^\infty c_j \lambda_j \phi_j(x)$$

**经过 $t$ 步演化**：

$$\varphi(x_t) = (\mathcal{K}^t\varphi)(x_0) = \sum_{j=1}^\infty c_j \lambda_j^t \phi_j(x_0)$$

**这就是Koopman算子的核心威力**：非线性系统的长期演化被分解为**指数模式** $\lambda_j^t$ 的线性叠加！

---

### 四、谱的物理意义

特征值 $\lambda_j$ 的模长决定了对应模式的动力学行为：

| 特征值                    | 物理意义 | 信息传播 |                     |          |
| ---------------------- | ---- | ---- | ------------------- | -------- |
| $lambda_japprox 1$<br> |      |      | **时间相干模态**（保守/缓慢耗散） | 信息几乎无损传播 |
| $lambda_j< 1$          |      |      | **快速耗散模态**          | 信息指数级衰减  |
| $lambda_j> 1$          |      |      | **发散模态**（不稳定）       | 信息指数级增长  |


这正是论文**命题3**的核心发现：

> **Proposition 3 (信息解缠与谱性质)** 互信息 $I(z_t; x_t)$ 可以解缠为三个分量，每个分量都有谱解释：
> 
> - **时间相干信息** $I(z_{t-n}; z_t)$：对应 $|\lambda| \approx 1$ 的模态
> - **快速耗散信息** $I(z_t; x_{t-1}|z_{t-n})$：对应 $|\lambda| < 1$ 的模态
> - **残差信息** $I(z_t; x_t|x_{t-1})$：无谱对应（噪声/异常）

(Cheng 等, 2025)

---

### 五、概率视角下的Koopman表示

在实际深度学习中，Koopman表示被建模为一个概率生成过程。给定初始状态 $x_0$，轨迹分布为：

> $$p_{\text{KR}}(x_{1:t}|x_0) = \int p(z_0|x_0) \prod_{n=1}^t p(z_n|z_{n-1}) p(x_n|z_n) \, dz_0 dz_1 \cdots dz_t.$$

(Cheng 等, 2025)

其中三个关键组件：

| 组件      | 公式                                                        | 作用  |             |                               |
| ------- | --------------------------------------------------------- | --- | ----------- | ----------------------------- |
| **编码器** | $p(z_0x_0)$                                               |     | 将初始状态映射到潜变量 |                               |
| **潜转移** | $p(z_nz_{n-1}) = mathcal{N}(z_nmathcal{K}z_{n-1}, Sigma)$ |     |             | **线性高斯转移**——这就是Koopman算子的概率实现 |
| **解码器** | $p(x_nz_n)$                                               |     | 从潜变量重建状态    |                               |

**注意**：潜转移 $p(z_n|z_{n-1})$ 中的均值是 $\mathcal{K}z_{n-1}$，即Koopman算子 $\mathcal{K}$ 的**线性**作用——这正是"将非线性动力系统线性化"在实践中的体现。

---

### 六、信息论视角下的Koopman表示

#### 6.1 命题1：信息损失

> **Proposition 1** 在Koopman表示的信息传播路径 $x_{n-1} \to z_{n-1} \xrightarrow{\mathcal{K}} z_n \to x_n$ 中：
> 
> $$I(x_{n-1}; x_n) \geq I(z_{n-1}; x_n) \geq I(z_{n-1}; z_n).$$

(Cheng 等, 2025)

**含义**：每一步信息都在减少，$I(z_{n-1}; z_n)$ 设定了Koopman表示的信息极限。

#### 6.2 命题2：误差界

> **Proposition 2** 真实轨迹与Koopman诱导轨迹之间的误差被信息间隙所界定：
> 
> $$\left\|\mathbb{E}_{q_{\text{KR}}}[x_{1:t}|x_0] - \mathbb{E}_p[x_{1:t}|x_0]\right\|_2 \leq \bar{C} \sqrt{2\sum_{n=1}^t \left[I(x_{n-1}; x_n) - I(z_{n-1}; z_n)\right] + \mathcal{E}}.$$

(Cheng 等, 2025)

**含义**：预测误差由**步进式信息极限**控制——$I(x_{n-1}; x_n)$ 是原始系统的内在耦合，$I(z_{n-1}; z_n)$ 是Koopman表示保留的耦合，两者的差距就是信息损失。

#### 6.3 潜互信息的闭式解

> $$I(z_{t-n}; z_t) = \frac{1}{2} \log \det\left(I + M_n^{-\frac{1}{2}} \mathcal{K}^n C (\mathcal{K}^n)^\top M_n^{-\frac{1}{2}}\right)$$

(Cheng 等, 2025)

其中：

- $C := \text{Cov}(z_{t-n})$：潜变量协方差矩阵
- $M_n := \sum_{i=0}^{n-1} \mathcal{K}^i \Sigma (\mathcal{K}^i)^\top$：$n$步线性前向协方差
- $\det$：行列式

#### 6.4 注水效应（Water-filling）

最大化 $I(z_{t-n}; z_t)$ 会导致**注水效应**：方差沿着最大特征值方向分配。当谱高度偏斜时，解退化为低秩分配，信息被挤压到少数主导方向——这就是**模式坍缩**。

#### 6.5 冯·诺依曼熵与反坍缩

> $$S(\rho) = -\text{tr}(\rho \log \rho) = -\sum_{i=1}^d \lambda_i \log \lambda_i, \quad \rho = \frac{C}{\text{tr}(C)}.$$

(Cheng 等, 2025)

**有效维度**：$d_{\text{eff}}(\rho) = \exp(S(\rho))$

- 坍缩时：$d_{\text{eff}} \approx 1$
- 均匀分布时：$d_{\text{eff}} = d$

惩罚冯·诺依曼熵鼓励谱多样性，防止模式坍缩。

---

### 七、统一的信息论拉格朗日量

综合以上分析，论文提出了核心贡献——**信息论拉格朗日量**：

> $$\max \alpha \log I(z_{t-n}; z_t) - \beta I(z_t; x_t|z_{t-n}) + \gamma S\left(\frac{C}{\text{tr}(C)}\right) + \log p(x_t|z_t).$$

(Cheng 等, 2025)

| 项                           | 作用             | 对应需求        |           |
| --------------------------- | -------------- | ----------- | --------- |
| $alpha log I(z_{t-n}; z_t)$ | 保留时间相干信息       | **时间相干性**   |           |
| $-beta I(z_t; x_tz_{t-n})$  |                | 压缩快速耗散和残差信息 | **结构一致性** |
| $gamma S(C/text{tr}(C))$    | 冯·诺依曼熵正则化，防止坍缩 | **预测充分性**   |           |
| $log p(x_tz_t)$             |                | 从潜变量重建状态    | **重建质量**  |

---

### 八、一句话总结

**Koopman算子**是一个定义在无限维函数空间上的**线性算子**，它通过"将非线性系统提升到更高维的函数空间"来实现线性化。其核心公式：

$$(\mathcal{K}\varphi)(x) = \varphi(T(x))$$

虽然 $\mathcal{K}$ 本身是无限维的，但通过深度学习和信息论（互信息 + 冯·诺依曼熵）的指导，我们可以学习到一个好的**有限维近似**，使得非线性动力学的长期预测变得稳定、可解释且高效。