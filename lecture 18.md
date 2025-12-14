# Lecture 18: RLC Filter Circuits (RLC 滤波器电路)

## 0. 课程概览与复习 (Agenda & Review)
**核心概念**：
* **滤波器 (Filter)**：想象成一个筛子，只允许特定频率的信号通过，阻挡其他频率。
* **传递函数 (Transfer Function)** $H(\omega)$：这是描述滤波器“性格”的数学公式。
    * $H(\omega) = \frac{\text{输出 (Output)}}{\text{输入 (Input)}}$
    * **幅度响应 (Magnitude/Gain)** $|H(\omega)|$：信号被放大了还是缩小了？
    * **相位响应 (Phase)** $\angle H(\omega)$：信号的时间延迟或偏移。

> [!NOTE] 复习：元件阻抗
> * 电阻 $R$：不随频率变化。
> * 电感 $Z_L = j\omega L$：频率越高，阻碍越大（高频开路）。
> * 电容 $Z_C = \frac{1}{j\omega C}$：频率越高，阻碍越小（高频短路）。

![[Lecture 18.pdf#page=1]]
![[Lecture 18.pdf#page=2]]
![[Lecture 18.pdf#page=3]]

---

## 1. 谐振基础 (Resonance Basics)
这部分是理解RLC电路的核心。为什么叫“二阶”？因为电路里有两个储能元件（L和C）。

### 1.1 串联谐振 (Series Resonance)
当 L 和 C 串联时，它们的作用是**相反**的。
* **谐振频率 $\omega_0$**：在这个特定频率下，电感的感抗 ($j\omega L$) 和电容的容抗 ($\frac{1}{j\omega C}$) 大小相等，符号相反，互相抵消。
* **结果**：总阻抗 $Z = R$（纯电阻性），电路阻抗最小，电流最大。相当于 L 和 C 连在一起变成了一根导线（短路）。

$$\omega_0 = \frac{1}{\sqrt{LC}}$$

![[Lecture 18.pdf#page=4]]
![[Lecture 18.pdf#page=5]]

### 1.2 并联谐振 (Parallel Resonance)
当 L 和 C 并联时：
* **谐振时**：并联部分的等效阻抗无穷大 ($\infty$)。
* **结果**：L 和 C 这一坨并联结构相当于**开路**（断路）。外部电流进不去，但在 L 和 C 内部有巨大的循环电流。

![[Lecture 18.pdf#page=6]]

---

## 2. 串联 RLC 滤波器详解 (Series RLC Filters)
利用串联分压原理：$V_{out} = V_{in} \times \frac{Z_{output}}{Z_{total}}$。

### 2.1 低通滤波器 (LPF) - 输出取自电容 C
* **直觉理解**：
    * 低频时：电容阻抗极大（断路），分压分到几乎所有电压 $\rightarrow$ 通。
    * 高频时：电容阻抗极小（短路），电压几乎为0 $\rightarrow$ 阻。
* **关键点**：$\omega_0$ 是截止频率。

![[Lecture 18.pdf#page=8]]

### 2.2 高通滤波器 (HPF) - 输出取自电感 L
* **直觉理解**：
    * 低频时：电感阻抗极小（短路），输出为0 $\rightarrow$ 阻。
    * 高频时：电感阻抗极大，分得大部分电压 $\rightarrow$ 通。

![[Lecture 18.pdf#page=9]]
![[Lecture 18.pdf#page=10]]

### 2.3 带通滤波器 (BPF) - 输出取自电阻 R
* **直觉理解**：
    * 只有在**谐振频率**附近，L和C相互抵消（短路），电路总阻抗最小，电流最大，电阻上的电压 $V_R = I \times R$ 也就最大。
    * 远离谐振频率，阻抗变大，电流变小，输出降低。
* **重要参数**：
    * **带宽 (Bandwidth, BW/$\omega_{3dB}$)**：信号能通过的频率范围宽度。 $BW = \frac{R}{L}$。
    * **品质因数 (Q Factor)**：描述滤波器有多“挑剔”。Q值越高，带宽越窄，滤波器选频越准。
    * 公式：$Q = \frac{\omega_0}{BW}$。

![[Lecture 18.pdf#page=11]]
![[Lecture 18.pdf#page=12]]

### 2.4 带阻滤波器 (BSF/Notch) - 输出取自 L+C
* **直觉理解**：
    * 在谐振频率时，串联的 L+C 阻抗为0（短路）。
    * 因为输出是并联在 L+C 两端的，所以输出电压被拉低到0 $\rightarrow$ 阻止该频率。
    * 其他频率 L+C 阻抗很大，信号可以通过。

![[Lecture 18.pdf#page=13]]
![[Lecture 18.pdf#page=14]]

---

## 3. 并联 RLC 滤波器详解 (Parallel RLC Filters)
这里的电路结构通常是：信号源串联一个元件，然后输出端并联其他元件。分析方法多用节点电压法 (Nodal Analysis)。

### 3.1 并联 RLC 低通 (LPF)
* 结构：输入经过 $L$，输出端是 $R$ 和 $C$ 并联。
* **直觉**：高频时，并联的电容 $C$ 变成短路，把输出电压“短路”掉了，所以高频不过。

![[Lecture 18.pdf#page=15]]

### 3.2 并联 RLC 高通 (HPF)
* 结构：输入经过 $C$，输出端是 $R$ 和 $L$ 并联。
* **直觉**：低频时，输入端的电容 $C$ 阻挡信号进入；同时输出端的电感 $L$ 短路掉电压。只有高频能通过 $C$ 且不被 $L$ 短路。

![[Lecture 18.pdf#page=16]]

### 3.3 并联 RLC 带通 (BPF)
* 结构：输入经过 $R$，输出端是 $L$ 和 $C$ 并联。
* **直觉**：
    * 谐振时，并联的 L+C 阻抗无穷大（开路）。
    * 此时输出电压最大（没有电流分流到地）。
    * 非谐振时，L或C总有一个阻抗比较小，把电压拉低。

![[Lecture 18.pdf#page=17]]
![[Lecture 18.pdf#page=18]]

### 3.4 并联 RLC 带阻 (BSF)
* 结构：输入经过并联的 L+C 组合，输出在电阻 R 上。
* **直觉**：
    * 谐振时，串联在主路上的 L+C 并联组合阻抗无穷大（断路）。
    * 信号过不去，输出为0。

![[Lecture 18.pdf#page=19]]
![[Lecture 18.pdf#page=20]]

---

## 4. 综合分析案例 (Example Analysis)

这里给出了一个稍微复杂的电路（梯形网络），教你如何判断它是什么滤波器。
**方法**：
1.  **极值法**：分析 $\omega=0$ (DC) 和 $\omega=\infty$ (高频) 时的电路状态。
    * $\omega=0$：电容断路，电感短路。计算 $V_{out}$。
    * $\omega=\infty$：电容短路，电感断路。计算 $V_{out}$。
2.  **推导**：通过节点电压法写出传递函数。

在这个例子中（图10.63）：
* $\omega=0$ 时，$H(0)=0.5$（有输出）。
* $\omega=\infty$ 时，$H(\infty)=0$（电容短路接地了，无输出）。
* **结论**：低频通，高频断 $\rightarrow$ **低通滤波器 (LPF)**。

![[Lecture 18.pdf#page=21]]
![[Lecture 18.pdf#page=22]]

---

## 5. 滤波器设计与计算 (Filter Design)

这部分教你如何根据要求的参数（如中心频率、带宽）反推 R, L, C 的值。

### 关键公式总结
无论是串联还是并联，以下关系恒成立：
$$Q \cdot BW = \omega_0$$

**公式差异表**：

| 参数 | 串联电路 (Series) | 并联电路 (Parallel) |
| :--- | :--- | :--- |
| **带宽 (BW)** | $\frac{R}{L}$ | $\frac{1}{RC}$ |
| **品质因数 (Q)** | $\frac{\omega_0 L}{R}$ | $\omega_0 RC$ |

**设计案例 (Page 23-25)**：
题目要求改变 L 和 C 的值，使得 Q 值翻倍，但保持中心频率 $\omega_0$ 和电阻 R 不变。
* **思路**：
    1.  $Q_{new} = 2 Q_{old}$。
    2.  对于串联电路 $Q = \frac{\omega_0 L}{R}$。
    3.  既然 $\omega_0$ 和 $R$ 不变，要让 Q 翻倍，**L 必须翻倍**。
    4.  又因为 $\omega_0 = \frac{1}{\sqrt{LC}}$ 必须不变，L 翻倍了，**C 必须减半**。

![[Lecture 18.pdf#page=23]]
![[Lecture 18.pdf#page=24]]
![[Lecture 18.pdf#page=25]]
![[Lecture 18.pdf#page=26]]

---

## 6. 总结 (Summary)
1.  **传递函数** $H(\omega)$ 是核心。
2.  实际滤波器无法做到完美的“矩形”切断，总是有过渡带。
3.  **一阶滤波器**用 RC 或 RL。
4.  **二阶滤波器**用 RLC（串联或并联），具有谐振特性，可以做更窄的带通/带阻。

![[Lecture 18.pdf#page=27]]
![[Lecture 18.pdf#page=28]]