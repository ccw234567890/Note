## Problem 2.52 — 用分压法求 V1（并求各关键节点电压）
![[Lecture 4.pdf#page=20]]

**电路识别与吸收思路**
- 把每个“主链节点上的并联支路”先吸收成一个等效电阻（并联等效），主链从左到右依次得到三段：
  - 左段：$R_a = R_1 \parallel R_2$
  - 中段：$R_b = R_3 \parallel R_4$
  - 右段：$R_c = R_5 \parallel R_6$
- 右端的 $R_7$ 与电源两端并联，仅改变总电流，不影响主链**节点电位的比例**；求主链节点电位时可先忽略 $R_7$（理想电源保持母线电压不变）。

**并联等效**
$$
R_a=\frac{R_1R_2}{R_1+R_2},\quad
R_b=\frac{R_3R_4}{R_3+R_4},\quad
R_c=\frac{R_5R_6}{R_5+R_6}.
$$

> 讲义示例给出的近似：$R_a=1.2\ \mathrm{k\Omega},\ R_b=1.5\ \mathrm{k\Omega},\ R_c\approx 2.3\ \mathrm{k\Omega}$  
> （若你按图上精确阻值计算，也可以代入精确的并联结果。）

**主链总电阻与电流**
$$
R_\text{chain}=R_a+R_b+R_c,\qquad
I_\text{chain}=\frac{V_s}{R_\text{chain}}.
$$

**三段分压（主链自左向右）**
- 左段两端电压（也是“左端节点到中间节点”的压降）：
$$
V_a^\Delta = I_\text{chain}\,R_a = V_s\frac{R_a}{R_a+R_b+R_c}.
$$
- 中段压降：
$$
V_b^\Delta = I_\text{chain}\,R_b = V_s\frac{R_b}{R_a+R_b+R_c}.
$$
- 右段压降：
$$
V_c^\Delta = I_\text{chain}\,R_c = V_s\frac{R_c}{R_a+R_b+R_c}.
$$

**主链节点电位（相对地）**
设电源正端母线为左端，最右端与母线相连。则
- 最右端节点（主链终点，对地）电位为：$V_\text{right}=V_s$；
- 中间节点（$R_b$ 与 $R_c$ 之间，对地）：
$$
V_c = V_\text{right} - V_c^\Delta = V_s\left(1-\frac{R_c}{R_a+R_b+R_c}\right)
= V_s\frac{R_a+R_b}{R_a+R_b+R_c}.
$$
- 左中节点（$R_a$ 与 $R_b$ 之间，对地）：
$$
V_b = V_c - V_b^\Delta
= V_s\frac{R_a}{R_a+R_b+R_c}.
$$
- 电源正端母线电位就是 $V_s$。

> 对照讲义的记号：上式中的节点 $V_b, V_c$ 分别对应图中标注的 $V_2, V_3$ 所在的母线节点电位；  
> 左侧 $V_1$ 是左段等效的**两端电压**（左母线 $\to$ 左中节点），其数值与 $V_a^\Delta$ 相同，方向与图示“左端 + 右端 −”一致：
> $$
> V_1 = V_a^\Delta = V_s\frac{R_a}{R_a+R_b+R_c}.
> $$

---

### 代数结果（通用）
$$
\begin{aligned}
V_1 &= V_s\frac{R_a}{R_a+R_b+R_c},\\[4pt]
V_2 &= V_b = V_s\frac{R_a}{R_a+R_b+R_c},\\[4pt]
V_3 &= V_c - 0 = V_s\frac{R_a+R_b}{R_a+R_b+R_c}.
\end{aligned}
$$
其中 $V_2$ 为图中右侧上半段的电压降（等同于左中节点电位），$V_3$ 为右侧下半段对地的电压（即中点电位）。

---

### 数值一：按讲义“示例等效”并取 $V_s=10\ \mathrm{V}$
（与你贴出的 $V_a=2.4\ \mathrm{V},\ V_b=3.0\ \mathrm{V},\ V_c=4.6\ \mathrm{V}$ 一致）

$$
R_a=1.2,\ R_b=1.5,\ R_c=2.3\ \ (\mathrm{k\Omega}),\quad
R_\text{chain}=5.0\ \mathrm{k\Omega},\ I_\text{chain}=2.0\ \mathrm{mA}.
$$
$$
V_1=V_s\frac{1.2}{5.0}=2.4\ \mathrm{V},\quad
V_2=2.4\ \mathrm{V},\quad
V_3=V_s\frac{1.2+1.5}{5.0}=4.6\ \mathrm{V}.
$$

---

### 数值二：若电源按截图为 $V_s=24\ \mathrm{V}$
同样的等效下：
$$
I_\text{chain}=\frac{24}{5.0\ \mathrm{k\Omega}}=4.8\ \mathrm{mA},
$$
$$
V_1=24\cdot\frac{1.2}{5.0}=5.76\ \mathrm{V},\quad
V_2=5.76\ \mathrm{V},\quad
V_3=24\cdot\frac{1.2+1.5}{5.0}=11.04\ \mathrm{V}.
$$

> 提醒  
> - 若你用图上的**精确阻值**去算并联（例如 $R_1=4\ \mathrm{k\Omega}$ 与 $R_2=40\ \mathrm{k\Omega}$ 得 $R_a=3.636\ \mathrm{k\Omega}$ 等），把这些精确值代入上面的**通用公式**即可得到一致的流程与结果。  
> - 右端的 $R_7$ 与理想电源并联，它只改变**电源供电电流**，不会改变主链分压得到的各**节点电位**；如果题目需要求总电流/功率，再把 $R_7$ 的支路电流 $V_s/R_7$ 加上即可。
