# Chapter 6: Large Random Samples (大样本理论与中心极限定理)

> [!abstract] **本章核心目标**
> 本笔记整合了概率论中关于**大样本 (Large Random Samples)** 分析的核心内容。
> * **核心思想**：引入一系列**近似结果 (Approximation Results)**，旨在简化分析。当样本量 $n$ 足够大时，我们可以利用极限理论来估算复杂的概率，而不需要计算精确的组合数。
> * **关键定理**：重点讲解 **大数定律 (LLN)** 和 **中心极限定理 (CLT)**。
> * **实际应用**：利用正态分布表估算各种分布（如二项、泊松、均匀分布）的概率。

---

## 1. 理论基础：概率不等式 (Inequalities)

在进入大数定律之前，我们需要两个强大的工具来界定随机变量的尾部概率。

### 1.1 马尔可夫不等式 (Markov Inequality)
这是最基础的不等式，用于非负随机变量。

> [!def] **定理 6.2.1: Markov Inequality**
> 假设 $X$ 是一个**非负**随机变量（即 $Pr(X \ge 0) = 1$）。对于任意实数 $t > 0$，有：
> $$Pr(X \ge t) \le \frac{E(X)}{t}$$
> 
> *直观理解：* 如果平均值很小，那么数值变得极大的概率一定很小。均值限制了尾部概率。

> [!example] **详细证明 (Proof)**
> 假设 $X$ 是离散型随机变量（连续型同理，用积分代替求和）：
> 
> $$
> \begin{aligned}
> E(X) &= \sum_{x} x f(x) \\
> &= \sum_{x < t} x f(x) + \sum_{x \ge t} x f(x) 
> \end{aligned}
> $$
> 
> 由于 $X$ 只能取非负值，第一部分 $\sum_{x < t} x f(x) \ge 0$。因此：
> 
> $$
> \begin{aligned}
> E(X) &\ge \sum_{x \ge t} x f(x) \\
> &\ge \sum_{x \ge t} t f(x) \quad (\text{因为在这个求和范围内 } x \ge t) \\
> &= t \sum_{x \ge t} f(x) \\
> &= t \cdot Pr(X \ge t)
> \end{aligned}
> $$
> 
> 移项即得：$Pr(X \ge t) \le \frac{E(X)}{t}$。$\blacksquare$

### 1.2 切比雪夫不等式 (Chebyshev Inequality)
利用方差来衡量数据偏离均值的程度。

> [!def] **定理 6.2.2: Chebyshev Inequality**
> 设 $X$ 是一个随机变量，其方差 $Var(X)$ 存在。对于任意 $t > 0$：
> $$Pr(|X - E(X)| \ge t) \le \frac{Var(X)}{t^2}$$

> [!tip] **推导过程 (利用 Markov 不等式)**
> 令 $Y = [X - E(X)]^2$。
> 1.  显然 $Y$ 是非负的 ($Y \ge 0$)。
> 2.  $Y$ 的期望就是 $X$ 的方差：$E(Y) = E[(X-\mu)^2] = Var(X)$。
> 3.  事件 $\{|X - E(X)| \ge t\}$ 等价于 事件 $\{Y \ge t^2\}$。
> 
> 对 $Y$ 应用 Markov 不等式：
> $$Pr(|X - E(X)| \ge t) = Pr(Y \ge t^2) \le \frac{E(Y)}{t^2} = \frac{Var(X)}{t^2}$$

**应用示例：**
如果取 $t = 3\sigma$（3倍标准差），则偏离均值超过3倍标准差的概率为：
$$Pr(|X - \mu| \ge 3\sigma) \le \frac{\sigma^2}{(3\sigma)^2} = \frac{1}{9}$$
这说明无论什么分布，数据落在 $3\sigma$ 之外的概率不超过 $1/9$。

---

## 2. 样本均值与方差的基础性质

在讨论极限定理之前，必须明确样本均值本身就是一个随机变量。
假设 $X_1, X_2, \dots, X_n$ 来自同一个总体分布（i.i.d.），均值为 $\mu$，方差为 $\sigma^2$。

### 2.1 核心定义与公式
* **样本均值 (Sample Mean)**: $\bar{X}_n = \frac{1}{n} \sum_{i=1}^{n} X_i$
* **样本总和 (Sample Sum)**: $T_n = \sum_{i=1}^{n} X_i = n \cdot \bar{X}_n$

> [!important] **关键性质 (必须熟记)**
> 无论 $X_i$ 服从什么分布，只要独立同分布：
> 
> **1. 关于样本均值 $\bar{X}_n$：**
> * 期望：$E[\bar{X}_n] = \mu$
> * 方差：$Var(\bar{X}_n) = \frac{\sigma^2}{n}$  *(注意分母是 $n$，样本越大，方差越小)*
> * 标准差 (Standard Error)：$SD(\bar{X}_n) = \frac{\sigma}{\sqrt{n}}$
> 
> **2. 关于样本总和 $T_n$：**
> * 期望：$E[T_n] = n\mu$
> * 方差：$Var(T_n) = n\sigma^2$
> * 标准差：$SD(T_n) = \sqrt{n}\sigma$

---

## 3. 大数定律 (The Law of Large Numbers)

大数定律描述了当试验次数无限增加时，频率收敛于概率的现象。

### 3.1 切比雪夫不等式的应用
将 Chebyshev 不等式应用于样本均值：
$$Pr(|\overline{X}_n - \mu| \ge \epsilon) \le \frac{Var(\overline{X}_n)}{\epsilon^2} = \frac{\sigma^2}{n\epsilon^2}$$

### 3.2 弱大数定律 (Weak Law of Large Numbers, WLLN)

> [!thm] **定理 6.2.4: WLLN**
> 假设 $X_1, \dots, X_n$ i.i.d，均值为 $\mu$，方差为 $\sigma^2$。对于任意 $\epsilon > 0$：
> $$\lim_{n \to \infty} Pr(|\overline{X}_n - \mu| < \epsilon) = 1$$
> 
> *通俗解释：* 当样本量 $n$ 趋于无穷大时，样本均值 $\overline{X}_n$ **依概率收敛 (Converges in Probability)** 于真实均值 $\mu$。

**直观例子（伯努利分布）：**
若 $X_i$ 为 Bernoulli 试验（1=成功，0=失败），概率为 $p$。根据 LLN，频率 $\overline{X}_n$ 会收敛于概率 $p$。

**样本量计算示例：**
假设我们要估计硬币正面的概率。要求误差在 $0.1$ 以内的概率至少是 $0.99$。
已知 $\sigma^2 = p(1-p) \le 0.25$ (因为 $p=0.5$ 时方差最大)。
根据 Chebyshev：
$$Pr(|\overline{X}_n - p| \ge 0.1) \le \frac{\sigma^2}{n(0.1)^2} \le \frac{0.25}{0.01n} = \frac{25}{n}$$
我们希望这个错误概率 $\le 0.01$：
$$\frac{25}{n} \le 0.01 \Rightarrow n \ge 2500$$
*(注：Chebyshev 给出的界限通常比较保守，实际可能不需要这么多样本)*

### 3.3 强大数定律 (Strong Law of Large Numbers)
> [!info] **WLLN vs SLLN 区别**
> * **弱大数定律**: $P(|\overline{X}_n - \mu| > \epsilon) \to 0$。（依概率收敛）
> * **强大数定律**: $Pr(\lim_{n \to \infty} \overline{X}_n = \mu) = 1$。（几乎处处收敛 / With Probability 1）

---

## 4. 依分布收敛 (Convergence in Distribution)

* **定义**：设 $X_n$ 是一列随机变量，$F_n(x)$ 是它们的累积分布函数（CDF）。如果对于任意 $F^*(x)$ 的连续点 $x$，都有 $\lim_{n \to \infty} F_n(x) = F^*(x)$，则称 $X_n$ **依分布收敛**于 $F^*$。
* **意义**：当 $n$ 很大时，我们可以用极限分布 $F^*$ 来**近似**计算 $X_n$ 的概率。

---

## 5. 中心极限定理 (Central Limit Theorem, CLT)

大数定律告诉我们均值会**去哪里**（收敛到 $\mu$），而中心极限定理告诉我们它是**怎么分布的**（形状）。这是本学期最重要的定理。

### 5.1 核心定义

> [!important] **定理 6.3: Central Limit Theorem**
> 设 $X_1, \dots, X_n$ 为独立同分布随机变量，均值为 $\mu$，方差为 $\sigma^2$。
> 当 $n$ **足够大**时，样本均值 $\overline{X}_n$ 的分布近似服从**正态分布**：
> 
> $$\overline{X}_n \approx N\left(\mu, \frac{\sigma^2}{n}\right)$$
> 
> 或者对其进行**标准化 (Standardization)** 后：
> $$Z_n = \frac{\overline{X}_n - \mu}{\sigma / \sqrt{n}} \xrightarrow{d} N(0, 1)$$

### 5.2 "Bell-Shaped Curve" 直观理解
以二项分布为例，当 $n$ 很小时，分布是离散的柱状图。当 $n$ 变大，连接柱状图顶点的连线会形成一条平滑的曲线，形状像一口钟（Bell），这就是正态分布曲线。
**意义**：我们可以用连续的正态分布面积积分，来近似离散分布的概率求和。

---

## 6. 计算技巧与实战 (Calculation Skills)

考试中通常需要将非标准正态分布转化为标准正态分布 $Z$，然后查表。

### 6.1 标准化步骤
如果要计算 $P(a \le \bar{X}_n \le b)$：
1.  **中心化**：减去均值 $\mu$。
2.  **缩放**：除以标准差（注意是 $\frac{\sigma}{\sqrt{n}}$）。
3.  **公式**：
    $$P\left( \frac{a - \mu}{\sigma/\sqrt{n}} \le Z \le \frac{b - \mu}{\sigma/\sqrt{n}} \right)$$

### 6.2 查表与对称性
标准正态分布表（Standard Normal Table）给出的是 $\Phi(z) = P(Z \le z)$（即 $z$ 左侧面积）。
* $\Phi(-z) = 1 - \Phi(z)$ （对称性）
* $P(Z \ge z) = 1 - \Phi(z)$
* 区间概率：$P(z_1 \le Z \le z_2) = \Phi(z_2) - \Phi(z_1)$

---

## 7. 典型应用案例详解 (Comprehensive Examples)

### 案例 A：均匀分布 (Uniform Distribution)

**题目**: 设 $X_1, \dots, X_{12}$ 是来自均匀分布 $U(0, 1)$ 的随机样本，样本量 $n=12$。求 $P(|\bar{X}_{12} - \frac{1}{2}| \le 0.1)$ 的近似值。

**解析**:
1.  **确定参数**:
    * $U(0,1)$ 的均值 $\mu = 0.5$。
    * 方差 $\sigma^2 = \frac{(1-0)^2}{12} = \frac{1}{12}$。
    * **样本均值的标准差**: $SD(\bar{X}) = \frac{\sigma}{\sqrt{n}} = \frac{\sqrt{1/12}}{\sqrt{12}} = \frac{1}{12}$。
2.  **转化不等式**:
    $$|\overline{X} - 0.5| \le 0.1 \Rightarrow -0.1 \le \overline{X} - 0.5 \le 0.1$$
3.  **标准化**:
    $$Z = \frac{\overline{X} - \mu}{SD(\overline{X})} = \frac{\overline{X} - 0.5}{1/12}$$
    边界值转化：$\frac{\pm 0.1}{1/12} = \pm 1.2$。
4.  **计算**:
    $$Pr(|Z| \le 1.2) = \Phi(1.2) - \Phi(-1.2) = 2\Phi(1.2) - 1$$
    查表知 $\Phi(1.2) \approx 0.8849$。
    $$= 2(0.8849) - 1 = \mathbf{0.7698}$$

> [!success] **Note**
> 此题设计巧妙，利用 $n=12$ 正好消去了分母，展示了 CLT 的典型应用。

### 案例 B：泊松分布 (Poisson Distribution)

**题目**: 设 $X_i \sim Poisson(\theta)$。利用 CLT 写出 $\bar{X}_n$ 与 $\theta$ 接近的概率公式。

**解析**:
1.  **参数**: $\mu = \theta$, $\sigma^2 = \theta$。
2.  **样本均值分布**: $\bar{X}_n \sim N(\theta, \frac{\theta}{n})$。
3.  **概率公式**:
    要计算 $Pr(|\overline{X}_n - \theta| < c)$：
    $$
    \begin{aligned}
    Pr\left( \frac{|\overline{X}_n - \theta|}{\sqrt{\theta/n}} < \frac{c}{\sqrt{\theta/n}} \right) &= Pr\left(|Z| < \frac{c\sqrt{n}}{\sqrt{\theta}}\right) \\
    &\approx 2\Phi\left(\frac{c\sqrt{n}}{\sqrt{\theta}}\right) - 1
    \end{aligned}
    $$

### 案例 C：二项分布 - 总和与均值的区别 (Sum vs Mean)

**题目**: 投掷硬币 900 次 ($n=900$)，$X_i \sim Bernoulli(0.5)$。求正面次数 $T$ 超过 495 次的概率。

> [!warning] **重要提示**
> 这里计算的是**总数 $T$**，而不是均值 $\bar{X}$。分母（标准差）计算方式不同！

**解析**:
1.  **确定参数**:
    * 单次试验：$\mu = 0.5$, $\sigma^2 = p(1-p) = 0.25$。
    * **总和 $T$ 的参数**:
        * 均值 $\mu_T = n\mu = 900 \times 0.5 = 450$。
        * 方差 $\sigma^2_T = n\sigma^2 = 900 \times 0.25 = 225$。
        * 标准差 $\sigma_T = \sqrt{225} = 15$。
2.  **标准化**:
    $$Z = \frac{T - \mu_T}{\sigma_T} = \frac{T - 450}{15}$$
3.  **计算概率**:
    $$Pr(T > 495) = Pr\left(\frac{T - 450}{15} > \frac{495 - 450}{15}\right)$$
    $$= Pr(Z > \frac{45}{15}) = Pr(Z > 3)$$
    $$= 1 - \Phi(3) \approx 1 - 0.9987 = \mathbf{0.0013}$$

---

## 8. 总结与对比 (Summary)

| 概念 | 关注对象 | 核心公式 | 含义 |
| :--- | :--- | :--- | :--- |
| **Markov Inequality** | 非负变量 | $P(X \ge t) \le \frac{E(X)}{t}$ | 均值限制了尾部概率 |
| **Chebyshev Inequality** | 任意变量 | $P(\lvert X-\mu \rvert \ge t) \le \frac{\sigma^2}{t^2}$ | 方差越小，数据越集中 |
| **Weak LLN** | 样本均值 $\overline{X}_n$ | $\lim P(\lvert \overline{X}_n - \mu \rvert < \epsilon) = 1$ | 样本量越大，均值越准 |
| **CLT** | 分布形状 | $Z = \frac{\overline{X}_n - \mu}{\sigma/\sqrt{n}} \sim N(0,1)$ | 大样本均值总是近似正态分布 |

> [!tip] **Takeaway**
> 1.  **CLT 的威力**: 只要样本量 $n$ 足够大（通常 $n \ge 30$），我们可以忽略原始分布的形状，直接用正态分布来计算概率。
> 2.  **公式记忆**:
>     * $\mu_{\bar{x}} = \mu$
>     * $\sigma_{\bar{x}} = \frac{\sigma}{\sqrt{n}}$ （如果是 Sum，则乘以 $\sqrt{n}$）
> 3.  **作答技巧**: 记得画图（Bell Curve），标记阴影区域，利用对称性计算。

