## 第 18 页：单位阶跃函数与 Dirac δ 的积分关系
![[Lecture 2 slides.pdf#page=18]]

**本页目标**：说明为什么
$$
u(t)=\int_{-\infty}^{t}\delta(\tau)\,d\tau,
\qquad\text{以及}\qquad
\frac{d}{dt}u(t)=\delta(t).
$$

---

### 1) 单位阶跃函数（Step Function）$u(t)$
**定义**（Heaviside）：
$$
u(t)=
\begin{cases}
1, & t>0,\\
0, & t<0.
\end{cases}
$$

> 关于 $t=0$ 的取值：在工程中常直接用 $u(0)=1$ 或 $0$；更严谨的分布论里可取 $u(0)=\tfrac12$，不影响绝大多数计算结果（只在与奇异项相乘时才可能相关）。

**物理含义**：$u(t)$ 表示“**在 $t=0$ 时刻被打开**”的开关。$x(t)u(t)$ 就是把任意信号 $x(t)$ 的“负时间部分”全部截断、只保留 $t\ge0$ 的**单边信号**。

---

### 2) Dirac δ 的基本性质（直觉版）
- **抽样（筛选）性质**：
  $$
  \int_{-\infty}^{\infty}x(\tau)\,\delta(\tau-a)\,d\tau=x(a).
  $$
- **“面积为 1” 的冲击**：$\displaystyle \int_{-\infty}^{\infty}\delta(t)\,dt=1$，但 $\delta$ **不是**通常意义的函数，而是广义函数/分布。
- **移位**：$\delta(t-a)$ 在 $t=a$ 处“冲击”。

---

### 3) 为什么 $\displaystyle u(t)=\int_{-\infty}^{t}\delta(\tau)\,d\tau$
把积分上限当作变量 $t$。当 $t<0$ 时，积分区间没有覆盖 $\tau=0$，于是
$$
\int_{-\infty}^{t}\delta(\tau)\,d\tau=0.
$$
当 $t>0$ 时，积分区间跨过 $\tau=0$，根据 δ 的面积性质得到
$$
\int_{-\infty}^{t}\delta(\tau)\,d\tau=1.
$$
这正好与 $u(t)$ 的定义一致。因此
$$
\boxed{~u(t)=\int_{-\infty}^{t}\delta(\tau)\,d\tau~}.
$$

> 这是“**微分—积分互逆**”的一个典型例子：δ 是阶跃的导数，阶跃是 δ 的积分。

---

### 4) 由此得到 $\dfrac{d}{dt}u(t)=\delta(t)$
由牛顿—莱布尼茨（上限是自变量）的链式规则可知
$$
\frac{d}{dt}\Big[\int_{-\infty}^{t}\delta(\tau)\,d\tau\Big]=\delta(t),
$$
也就是
$$
\boxed{~\frac{d}{dt}u(t)=\delta(t)~}.
$$
直观理解：$u(t)$ 在 $t=0$ 处有一个“高度从 $0$ 瞬间跳到 $1$”的不连续点，**导数**在该点表现为一个**无限尖锐、面积为 1** 的冲击，正是 $\delta(t)$。

---

### 5) 平移与缩放（常考变换）
- **平移**：
  $$
  u(t-t_0)=\int_{-\infty}^{t}\delta(\tau-t_0)\,d\tau,\qquad 
  \frac{d}{dt}u(t-t_0)=\delta(t-t_0).
  $$
  物理意义：在 $t=t_0$ 的时刻开关被“打开”。
- **缩放**（$a>0$）：
  $$
  u(at)=u(t),\qquad \delta(at)=\frac{1}{|a|}\delta(t).
  $$

---

### 6) 与常见基元的关系
- **斜坡函数**：$r(t)=t\,u(t)$，且
  $$
  \frac{d}{dt}r(t)=u(t),\qquad
  r(t)=\int_{-\infty}^{t}u(\tau)\,d\tau.
  $$
  级联起来就是：$\displaystyle r(t)=\iint \delta(\cdot)\,d\cdot\,d\cdot$（对 δ 积分两次得到斜坡）。
- **矩形/三角脉冲**：都能通过 $u(\cdot)$ 的差构造，例如宽度为 $\tau$、起点 $t_0$ 的矩形：
  $$
  \text{rect}_{[t_0,\,t_0+\tau]}(t)=u(t-t_0)-u\!\big(t-(t_0+\tau)\big).
  $$

---

### 7) 拉普拉斯变换（速记）
$$
\mathcal{L}\{u(t)\}=\frac{1}{s},\qquad
\mathcal{L}\{\delta(t)\}=1,\qquad
\mathcal{L}\{u(t-t_0)\}=e^{-t_0 s}\frac{1}{s}\ (t_0>0).
$$
这说明在 $s$ 域里，$u(t)$ 相当于“**积分算子**”，而 $\delta$ 相当于“**单位激励**”。

---

### 8) 典型运算与易错点
- **乘以一般函数**：$x(t)\,u(t-a)$ 表示“从 $t=a$ 起保留 $x(t)$”；在写 KCL/KVL 分段方程时很有用。
- **分段积分**：遇到 $\displaystyle \int x(t)\delta(t-a)\,dt$，要先把自变量一致化（多用 $\tau$ 作积分变量），然后一行写成 $x(a)$。
- **$t=0$ 处的值**：除非题目特别强调，否则 $u(0)$ 的取值不会影响积分/微分与系统响应的正确性；若出现 $\delta(t)\cdot u(t)$ 这类奇异乘积，需遵循题目或教材的约定。

---

### 9) 小练习（可选）
1. 证明：$\displaystyle \int_{-\infty}^{t}\delta(\tau-a)\,d\tau=u(t-a)$。  
2. 计算：$\displaystyle \frac{d}{dt}[u(t-a)-u(t-b)]=\delta(t-a)-\delta(t-b)$，并给出其物理图像解释。  
3. 用 $u(t)$ 表示一个**幅度 $A$、起点 $t_0$、宽度 $\tau$** 的矩形脉冲。

> 结论速记：**δ 是阶跃的导数；阶跃是 δ 的积分**。这组关系在分析开关电路、构造分段信号、以及做卷积/拉普拉斯变换时极其重要。
