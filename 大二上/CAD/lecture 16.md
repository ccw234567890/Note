# Lecture 16: Analysis of Phasor Transformed Circuits (相量变换电路分析)

**课程信息**: Circuit Analysis and Design (Semester 1, 2025/2026)
**文件引用**: [[Lecture 16.pdf]]

---

## 1. 课程大纲与基础概念 (Page 1-2)
![[Lecture 16.pdf#page=2]]

### 核心议程
本节课主要解决如何分析交流（AC）电路。我们将从时间域（Time Domain）转换到频率域/相量域（Phasor Domain），这就像把微积分问题变成代数问题一样简单。
* **正弦信号 (Sinusoidal signals)**: 交流电的基础。
* **有效值 (RMS value)**: 如何衡量交流电的“大小”。
* **相量 (Phasors)**: 分析交流电路的核心数学工具。
* **阻抗与导纳 (Impedances and admittances)**: 电阻在交流电路中的推广。
* **电路分析**: 串并联与定律应用。

---

## 2. 正弦信号基础 (Page 3-6)

### 正弦波的数学表达
![[Lecture 16.pdf#page=3]]
> [!NOTE] 通俗讲解
> 交流电路在稳态下，电压和电流都是正弦波（或余弦波）。我们通常用余弦波（Cosine）作为标准形式。

公式：
$$v(t) = V_m \cos(\omega t + \phi)$$
* $V_m$: **振幅 (Amplitude)**，波形的最高点。
* $T$: **周期 (Period)**，波形重复一次所需的时间。
* $f$: **频率 (Frequency)**，1秒内重复的次数，$f=1/T$，单位 Hz。

### 角频率与相位移动
![[Lecture 16.pdf#page=4]]
* **角频率 ($\omega$)**: 表示旋转的速度，$\omega = 2\pi f = \frac{2\pi}{T}$，单位 rad/s。
* **相位 ($\phi$)**: 决定了 $t=0$ 时的起始位置。
    * 可以将 $\omega t + \phi$ 写成 $\omega(t + \frac{\phi}{\omega})$。
    * **左移/超前**: 如果 $\phi > 0$，波形向**左**移动（发生得更早）。
    * **右移/滞后**: 如果 $\phi < 0$，波形向**右**移动（发生得更晚）。

### 相位对比示例
![[Lecture 16.pdf#page=5]]
图示展示了三个波形：
1.  $\phi = 0^\circ$: 标准余弦波，峰值在 $t=0$。
2.  $\phi = 45^\circ$: 波形**左移**，峰值提前出现（超前）。
3.  $\phi = -45^\circ$: 波形**右移**，峰值延后出现（滞后）。

### Sine 与 Cosine 的转换 (重点)
![[Lecture 16.pdf#page=6]]
> [!Important] 考试易错点
> 在相量分析中，我们**必须**统一用 Cosine 作为标准。如果题目给的是 Sine，需要转换。

转换公式：
$$\sin(\omega t + \phi) = \cos(\omega t + \phi - 90^\circ)$$
* 几何理解：Sine 波形可以看作是 Cosine 波形向右平移了 $90^\circ$（即滞后 $90^\circ$）。

---

## 3. 有效值 (RMS Value) (Page 7-8)

### 定义与推导
![[Lecture 16.pdf#page=7]]
**RMS (Root Mean Square)** 均方根值。
* 物理意义：交流电的 RMS 值等于**产生相同热效应（功率）**的直流电（DC）数值。
* 推导过程利用了三角恒等式 $\cos^2(\theta) = \frac{1 + \cos(2\theta)}{2}$ 进行积分。

### 关键结论
![[Lecture 16.pdf#page=8]]
对于正弦波/余弦波：
$$V_{rms} = \frac{V_m}{\sqrt{2}} \approx 0.707 V_m$$
* **峰值 (Peak)**: $V_m$
* **峰峰值 (Peak-to-Peak)**: $2V_m$
* **平均值**: 正弦波一整个周期的平均值为 0。

---

## 4. 相量 (Phasors) 核心原理 (Page 9-11)

### 欧拉公式与旋转矢量
![[Lecture 16.pdf#page=9]]
欧拉公式是相量的基石：
$$e^{j\theta} = \cos(\theta) + j\sin(\theta)$$
我们可以把余弦波看作是一个在复平面上**逆时针旋转**的矢量在实轴（Real Axis）上的投影。
$$v(t) = \text{Re}[V_m e^{j(\omega t + \phi)}] = \text{Re}[V_m e^{j\phi} \cdot e^{j\omega t}]$$

### 相量的定义
![[Lecture 16.pdf#page=10]]
去掉旋转部分 $e^{j\omega t}$（因为全电路频率相同），剩下的部分就是**相量**：
$$\mathbf{V} = V_m e^{j\phi} = V_m \angle \phi$$
* 相量包含两个信息：**幅值 ($V_m$)** 和 **相位 ($\phi$)**。
* 它就像是在 $t=0$ 时刻给旋转矢量拍了一张照片。

![[Lecture 16.pdf#page=11]]
* 此页展示了不同相角的相量在复平面上的位置及其对应的时间轴波形。

### 标准化规则 (Standard Values)
![[Lecture 16.pdf#page=12]]
在写出相量之前，必须遵守两条规则：
1.  **幅值必须为正**: 如果是负数，例如 $-V_m \cos(...)$，需要加/减 $180^\circ$ 变成正值。
    * $- \cos(A) = \cos(A \pm 180^\circ)$
2.  **必须是 Cosine**: 如果是 Sine，减去 $90^\circ$。
    * $\sin(A) = \cos(A - 90^\circ)$
    * $-\sin(A) = \cos(A + 90^\circ)$

---

## 5. 实例练习 (Page 13-14)

### Example 9.4: 写出相量
![[Lecture 16.pdf#page=13]]
* (a) $v(t) = -110 \cos(2\pi 60t + 210^\circ)$
    * 处理负号：$210^\circ - 180^\circ = 30^\circ$
    * 结果：$\mathbf{V} = 110 \angle 30^\circ$ V
* (c) $v(t) = 220 \sin(2\pi 50t + 30^\circ)$
    * Sine 转 Cosine：$30^\circ - 90^\circ = -60^\circ$
    * 结果：$\mathbf{V} = 220 \angle -60^\circ$ V
* (f) $i(t) = -20 \sin(\dots + 120^\circ)$
    * 负 Sine 转 Cosine：$120^\circ + 90^\circ = 210^\circ$ 或 $120^\circ - 90^\circ \pm 180^\circ = -150^\circ$
    * 结果：$\mathbf{I} = 20 \angle -150^\circ$ A

### Example 9.5: 相量转回时间域
![[Lecture 16.pdf#page=14]]
已知 $f=60\text{Hz}$ ($\omega = 377 \text{rad/s}$)。
* (a) $\mathbf{V} = 110 \angle 120^\circ \Rightarrow v(t) = 110 \cos(377t + 120^\circ)$ V

---

## 6. 复数运算基础 (Page 15-19)

### 坐标转换
![[Lecture 16.pdf#page=15]]
* **直角坐标 (Rectangular)**: $z = a + jb$
* **极坐标 (Polar)**: $z = r \angle \phi$
* **转换公式**:
    * $r = \sqrt{a^2 + b^2}$
    * $\phi = \tan^{-1}(b/a)$ (注意象限！)
    * $a = r \cos \phi$, $b = r \sin \phi$

### 四则运算规则
![[Lecture 16.pdf#page=18]]
> [!Tip] 计算技巧
> * **加减法**: 用**直角坐标** ($a+jb$) 最方便。
> * **乘除法**: 用**极坐标** ($r \angle \phi$) 最方便。
>     * 乘法：模相乘，角相加。
>     * 除法：模相除，角相减。

### 同频率正弦波相加
![[Lecture 16.pdf#page=19]]
如果是两个不同相位的正弦波相加，直接在时间域很难算。
**方法**:
1.  把两个波形都转换成相量 ($\mathbf{V}_1, \mathbf{V}_2$)。
2.  在复平面上做加法 ($\mathbf{V}_{total} = \mathbf{V}_1 + \mathbf{V}_2$)。
3.  把结果转换回时间域。

---

## 7. 阻抗 (Impedance) 与 导纳 (Admittance) (Page 20-21)

### 定义
![[Lecture 16.pdf#page=20]]
* **阻抗 ($Z$)**: 相量电压与相量电流的比值。这是欧姆定律在交流电路的推广。
    $$Z = \frac{\mathbf{V}}{\mathbf{I}} = R + jX$$
    * $R$: 电阻 (Resistance)
    * $X$: 电抗 (Reactance)
* **导纳 ($Y$)**: 阻抗的倒数。
    $$Y = \frac{1}{Z} = G + jB$$
    * $G$: 电导 (Conductance)
    * $B$: 电纳 (Susceptance)

---

## 8. R, L, C 元件的阻抗 (Page 22-24)

### 1. 电阻 (Resistor)
![[Lecture 16.pdf#page=22]]
* 电压与电流**同相位** ($\phi_v = \phi_i$)。
* **阻抗**: $Z_R = R$ (实数)。
* 复平面上：$Z$ 在实轴上。

### 2. 电容 (Capacitor)
![[Lecture 16.pdf#page=23]]
* 电流**超前**电压 $90^\circ$ (Current leads Voltage by $90^\circ$)。
* 记忆口诀：**ICE** (Current I in Capacitor C is before E voltage).
* **阻抗**:
    $$Z_C = \frac{1}{j\omega C} = -j \frac{1}{\omega C} = \frac{1}{\omega C} \angle -90^\circ$$
* 复平面上：$Z$ 在虚轴负半轴。

### 3. 电感 (Inductor)
![[Lecture 16.pdf#page=24]]
* 电压**超前**电流 $90^\circ$ (Voltage leads Current by $90^\circ$)。
* 记忆口诀：**ELI** (Voltage E in Inductor L is before I current).
* **阻抗**:
    $$Z_L = j\omega L = \omega L \angle 90^\circ$$
* 复平面上：$Z$ 在虚轴正半轴。

---

## 9. 相量电路分析方法 (Page 25-29)

### 分析步骤 (Page 25)
1.  **变换**: 将时域电路转换为相量域电路。
    * 源 $v(t) \to \mathbf{V}$
    * 元件 $R, L, C \to Z_R, Z_L, Z_C$
2.  **计算**: 使用 KVL, KCL, 节点分析, 网孔分析等方法（和直流电路一样，只是变成了复数计算）。
3.  **反变换**: 将结果转回时域（如果需要）。

### Example 9.9: 画出相量模型
![[Lecture 16.pdf#page=26]]
* 给定 $\omega = 2\pi(60) \approx 377$ rad/s。
* 计算所有 $L$ 的 $j\omega L$ 和所有 $C$ 的 $1/j\omega C$。
* 画出用阻抗表示的电路图。

### Example 9.10: 完整计算
![[Lecture 16.pdf#page=27]]
* 这是一个 RL 串联电路。
* **总阻抗**: $Z_{eq} = Z_{R1} + Z_{L1} + Z_{R2} + Z_{L2}$
* **电流**: $\mathbf{I} = \frac{\mathbf{V}_s}{Z_{eq}}$
* **分压**: 计算各部分电压，如 $V_w = \mathbf{I} \cdot (Z_{R1} + Z_{L1})$。

### Example 9.11 & 9.12: 并联与混联
![[Lecture 16.pdf#page=28]]
![[Lecture 16.pdf#page=29]]
* 利用 KCL ($I = I_1 + I_2$) 和 KVL 分析复杂电路。
* 注意复数运算的准确性。

---

## 10. 阻抗的串并联 (Page 30-31)

### 串联 (Series)
![[Lecture 16.pdf#page=30]]
$$Z_{eq} = Z_1 + Z_2 + \dots + Z_n$$
就像直流电路的电阻串联一样，直接相加（复数相加）。

### 并联 (Parallel)
![[Lecture 16.pdf#page=31]]
$$\frac{1}{Z_{eq}} = \frac{1}{Z_1} + \frac{1}{Z_2} + \dots + \frac{1}{Z_n}$$
对于两个阻抗：
$$Z_{eq} = \frac{Z_1 Z_2}{Z_1 + Z_2}$$

### Example 9.13: 梯形网络分析
![[Lecture 16.pdf#page=32]]
这是一个典型的梯形电路，分析步骤是从最右侧开始向左进行等效：
1.  最右侧 $R_4$ 与 $L_2$ 串联。
2.  该组合与 $C_2$ 并联，得到 $Z_a$。
3.  $Z_a$ 与 $R_3$ 串联。
4.  该组合与中间支路 ($R_2 + L_1$) 并联，得到 $Z_b$。
5.  最后算出总阻抗和总电流，再一步步回推各点电压。

---

## 11. 总结 (Summary) (Page 33)
![[Lecture 16.pdf#page=33]]
1.  **相量**代表正弦波的幅值和相位。
2.  **阻抗 ($Z$)** 是频率的函数，是复数。
3.  **分析流程**: 时域 $\to$ 相量域 $\to$ 代数运算 $\to$ 时域。
4.  所有直流电路的定律 (KVL, KCL, Thévenin, Norton) 都适用于相量域。