# Chapter 1: Signals and Amplifiers 学习笔记

## 课程与背景介绍 (Introduction)

![[BAO_Ch1_introduction _ 20260301.pdf#page=1]]
![[BAO_Ch1_introduction _ 20260301.pdf#page=2]]
这是《模拟电路基础》(Fundamentals of Analogue Circuits) 的课程封面和介绍页。课程由鲍景富 (BAO JINGFU) 教授讲授，主要教材是经典的 Sedra/Smith 编写的《Microelectronic Circuits》。

![[BAO_Ch1_introduction _ 20260301.pdf#page=3]]
![[BAO_Ch1_introduction _ 20260301.pdf#page=4]]
这里提出了一句发人深省的话：“如果你不能用电池和导线点亮一个灯泡，那么建立在这些概念之上的所有东西都会有问题”。这强调了掌握最基础的物理和电路直觉的重要性。随后介绍了为了提升学习效果，课程会采用主动学习、翻转课堂、项目导向等教学方法。

![[BAO_Ch1_introduction _ 20260301.pdf#page=5]]
![[BAO_Ch1_introduction _ 20260301.pdf#page=6]]
![[BAO_Ch1_introduction _ 20260301.pdf#page=7]]
这几页简述了电子元件的发展史：
* **1904年**：真空管 (Vacuum Tube) 时代。
* **1947年**：第一只晶体管 (Transistor) 诞生（由贝尔实验室的 John Bardeen, William Shockley 和 Walter Brattain 发明，1956年获诺奖）。
* **1958年**：第一块集成电路 (IC) 诞生（由德州仪器的 Jack Kilby 发明，2000年获诺奖）。
* 集成度遵循摩尔定律指数级增长，至今电子技术仍处于快速发展之中。

![[BAO_Ch1_introduction _ 20260301.pdf#page=8]]
这里展示了一个典型电子系统 (Electronic System) 的功能框图：
外界物理量 $\rightarrow$ 传感器/接收器 $\rightarrow$ 信号获取 $\rightarrow$ 预处理 (如滤波/放大) $\rightarrow$ 模数转换 (A/D) $\rightarrow$ 计算机运算处理 $\rightarrow$ 数模转换 (D/A) $\rightarrow$ 驱动与执行机构。
**重点**：模拟电路主要用于系统的前端（信号获取与放大）和后端（功率驱动），而数字电路负责中间的逻辑运算。

![[BAO_Ch1_introduction _ 20260301.pdf#page=9]]
![[BAO_Ch1_introduction _ 20260301.pdf#page=10]]
详细列出了课程的预期学习成果，包括理论分析（二极管、BJT/MOSFET 工作原理及建模、频率响应、反馈）和实践操作（实验测试、放大器设计、使用 CAD 软件）。

![[BAO_Ch1_introduction _ 20260301.pdf#page=11]]
![[BAO_Ch1_introduction _ 20260301.pdf#page=12]]
![[BAO_Ch1_introduction _ 20260301.pdf#page=13]]
给出了学习这门课的建议与考核方式：
* 强调工程实践，理论分析必须得到实践验证。
* 考核：10% 平时作业，15% 实验与项目，75% 期末开卷考试。
* 严禁学术不端（抄袭直接0分）。

---

## 1.1 信号与等效模型 (Signals)

![[BAO_Ch1_introduction _ 20260301.pdf#page=14]]
![[BAO_Ch1_introduction _ 20260301.pdf#page=15]]
![[BAO_Ch1_introduction _ 20260301.pdf#page=16]]
正式进入第一章内容。本章目标是：了解信号的电学表示、戴维南/诺顿等效、模拟与数字的区别、信号的频谱，以及最核心的信号处理功能：**放大器 (Amplifier)** 的建模与表征。

![[BAO_Ch1_introduction _ 20260301.pdf#page=17]]
* **信号 (Signal)**：携带信息的物理量（例如播音员读新闻的声音）。
* **换能器 (Transducer)**：将非电学信号（如声音、温度）转换为电信号的器件，比如麦克风。

![[BAO_Ch1_introduction _ 20260301.pdf#page=18]]
![[BAO_Ch1_introduction _ 20260301.pdf#page=19]]
信号源在电路中有两种等效表示方式：
1.  **戴维南等效 (Thevenin form)**：一个理想电压源 $\upsilon_s(t)$ 串联一个源电阻 $R_s$。当 $R_s$ 较低时，这种模型更直观。
2.  **诺顿等效 (Norton form)**：一个理想电流源 $i_s(t)$ 并联一个源电阻 $R_s$。当 $R_s$ 较高时更适用。

---

## 1.2 模拟与数字信号 (Analog and Digital Signals)

![[BAO_Ch1_introduction _ 20260301.pdf#page=20]]
![[BAO_Ch1_introduction _ 20260301.pdf#page=21]]
![[BAO_Ch1_introduction _ 20260301.pdf#page=22]]
* **模拟信号 (Analog Signal)**：在数值（幅值）和时间上都是连续的。
* **离散时间信号 (Discrete-time Signal)**：数值上连续，但在离散的时间点上进行采样 (sampling)。
* **数字信号 (Digital Signal)**：不仅在时间上离散采样，其幅值也被**量化 (quantized)** 成了有限的离散值（0和1）。

---

## 1.3 信号的频谱 (Frequency Spectrum of Signals)

![[BAO_Ch1_introduction _ 20260301.pdf#page=23]]
![[BAO_Ch1_introduction _ 20260301.pdf#page=24]]
* **频谱 (Frequency Spectrum)**：用一组谐波分量的强度来定义一个时域信号。
* **傅里叶级数 (Fourier Series)**：任何周期函数都可以分解为无限多个频率成谐波关系的正弦波/余弦波的叠加。
  公式：$f(x) = \frac{a_0}{2} + \sum_{k=1}^{\infty} [a_k \cos(kx) + b_k \sin(kx)]$

![[BAO_Ch1_introduction _ 20260301.pdf#page=25]]
* 对于**非周期信号**，我们使用傅里叶变换 (Fourier Transform)，它会得到一个连续的频率谱 (continuous frequency spectrum)，而不是离散的频谱线。

---

## 1.4 放大器概念 (Amplifiers)

![[BAO_Ch1_introduction _ 20260301.pdf#page=26]]
![[BAO_Ch1_introduction _ 20260301.pdf#page=27]]
* **为什么要放大？** 因为很多换能器输出的信号功率极低（通常在毫瓦级别 mW），不足以驱动后续的系统。
* **线性度 (Linearity)**：放大器应该只放大信号，而不改变信号的形状。
* **失真 (Distortion)**：对输出信号造成的任何非预期改变。
* **电压放大器 (Voltage Amplifier)** 提升电压幅度；**功率放大器 (Power Amplifier)** 提升电流和功率强度。
* 关系式：$\upsilon_o(t) = A_v \cdot \upsilon_i(t)$，其中 $A_v$ 是**电压增益 (voltage gain)**。

![[BAO_Ch1_introduction _ 20260301.pdf#page=28]]
放大器的电路符号通常是一个三角形，信号从平的一端输入，从尖的一端输出。

![[BAO_Ch1_introduction _ 20260301.pdf#page=29]]
![[BAO_Ch1_introduction _ 20260301.pdf#page=30]]
* **放大器与变压器的区别**：变压器只能改变电压/电流的比例，而**不能增加总功率**；但放大器可以借助直流电源的能量，实实在在地提升信号的功率。
* **功率增益 (Power Gain)**: $A_p = \frac{\text{load power } (P_L)}{\text{input power } (P_I)}$。
* **分贝表示法 (Decibels, dB)**: 
  * 电压增益 $= 20 \log|A_v|$ dB
  * 电流增益 $= 20 \log|A_i|$ dB
  * 功率增益 $= 10 \log(A_p)$ dB

---

## 1.5 放大器的电路模型 (Circuit Models for Amplifiers)

![[BAO_Ch1_introduction _ 20260301.pdf#page=31]]
模型 (Model) 是描述器件端口行为特性的工具，它忽略了放大器内部复杂的晶体管级电路。

![[BAO_Ch1_introduction _ 20260301.pdf#page=32]]
![[BAO_Ch1_introduction _ 20260301.pdf#page=33]]
![[BAO_Ch1_introduction _ 20260301.pdf#page=34]]
**电压放大器模型**：
* **输入端**：用一个输入电阻 $R_i$ 等效。根据分压原理，实际进入放大器的电压 $\upsilon_i = \upsilon_s \frac{R_i}{R_i + R_s}$。
* **输出端**：用一个受控电压源 $A_{vo}\upsilon_i$ 串联一个输出电阻 $R_o$ 等效。根据分压原理，实际输出电压 $\upsilon_o = A_{vo}\upsilon_i \frac{R_L}{R_L + R_o}$。
* **总增益**：$\frac{\upsilon_o}{\upsilon_s} = A_{vo} \left(\frac{R_i}{R_i + R_s}\right) \left(\frac{R_L}{R_L + R_o}\right)$。
* **非理想特性**：可以看出，实际增益不再是一个常数，它会受到信号源内阻 $R_s$ 和负载电阻 $R_L$ 的严重影响。

![[BAO_Ch1_introduction _ 20260301.pdf#page=35]]
**理想电压放大器 (Ideal Voltage Amplifier)**：
为了不让信号在输入输出端被损耗，理想的电压放大器必须满足：
* $R_i = \infty$ （无穷大的输入电阻，不抽取源电流）
* $R_o = 0$ （零输出电阻，不怕负载变化拖低电压）
此时总增益 $\upsilon_o / \upsilon_s = A_{vo}$。

![[BAO_Ch1_introduction _ 20260301.pdf#page=36]]
![[BAO_Ch1_introduction _ 20260301.pdf#page=37]]
![[BAO_Ch1_introduction _ 20260301.pdf#page=38]]
**级联放大器 (Cascaded Amplifiers)**：
现实中很难用单个放大器做到既有极高 $R_i$ 又有极低 $R_o$ 且增益很大。解决办法是将多级放大器串联。比如：第一级侧重高 $R_i$，最后一级侧重低 $R_o$（充当缓冲器），中间级负责提供主要增益。

![[BAO_Ch1_introduction _ 20260301.pdf#page=39]]
![[BAO_Ch1_introduction _ 20260301.pdf#page=40]]
![[BAO_Ch1_introduction _ 20260301.pdf#page=41]]
**四种基础放大器类型及理想条件**：
1.  **电压放大器 (Voltage Amp)**: $v_i \rightarrow v_o$。理想条件：$R_i = \infty$, $R_o = 0$。
2.  **电流放大器 (Current Amp)**: $i_i \rightarrow i_o$。理想条件：$R_i = 0$, $R_o = \infty$。
3.  **跨导放大器 (Transconductance Amp)**: $v_i \rightarrow i_o$。理想条件：$R_i = \infty$, $R_o = \infty$。
4.  **跨阻放大器 (Transresistance Amp)**: $i_i \rightarrow v_o$。理想条件：$R_i = 0$, $R_o = 0$。
这四种模型是等效的，可以通过互相转换来描述同一个放大电路。

![[BAO_Ch1_introduction _ 20260301.pdf#page=42]]
![[BAO_Ch1_introduction _ 20260301.pdf#page=43]]
**如何测试计算 $R_i$ 和 $R_o$？**
* **求 $R_i$**：在输入端加上电压 $v_i$，测量流入的电流 $i_i$，则 $R_i = \frac{v_i}{i_i}$。
* **求 $R_o$**：将输入源置零（短路电压源/开路电流源，保证受控源为0），然后在输出端外加一个测试电压 $v_x$，测量反向流入放大器的电流 $i_x$，则 $R_o = \frac{v_x}{i_x}$。

![[BAO_Ch1_introduction _ 20260301.pdf#page=44]]
![[BAO_Ch1_introduction _ 20260301.pdf#page=45]]
![[BAO_Ch1_introduction _ 20260301.pdf#page=46]]
![[BAO_Ch1_introduction _ 20260301.pdf#page=47]]
![[BAO_Ch1_introduction _ 20260301.pdf#page=48]]
**Example 1.5 讲解 (带输入电容的放大器频率响应)**
当放大器输入端存在寄生电容 $C_i$ 时，电路变成了一个**单时间常数低通滤波器 (Low-pass STC network)**。
* 输入电压变为：$V_i = V_s \frac{1}{1 + \frac{R_s}{R_i} + sC_i R_s}$。
* 它引入了一个截止频率极点，时间常数 $\tau = C_i (R_s || R_i)$。
* 3-dB 截止频率 $\omega_0 = \frac{1}{\tau} = \frac{1}{C_i (R_s || R_i)}$。
这意味着输入信号频率越高，进入放大器的电压幅值就越低，并伴随着相位滞后。

---

## 课后习题详细解答 (Homework Solutions)

### **Homework 1.43**
**题目：** ![[BAO_Ch1_introduction _ 20260301.pdf#page=52]] 
考虑图示的电压放大器模型，开路增益 $A_{vo} = 10 \text{ V/V}$。计算以下三种情况下的实际增益 $\frac{v_o}{v_s}$：
(a) $R_i = 10R_s, R_L = 10R_o$
(b) $R_i = R_s, R_L = R_o$
(c) $R_i = R_s/10, R_L = R_o/10$

**解答：**
电压放大器的总增益公式为：
$$A_v = \frac{v_o}{v_s} = A_{vo} \cdot \left( \frac{R_i}{R_i + R_s} \right) \cdot \left( \frac{R_L}{R_L + R_o} \right)$$
* **(a)** 代入条件：
    $$A_v = 10 \cdot \left( \frac{10R_s}{11R_s} \right) \cdot \left( \frac{10R_o}{11R_o} \right) = 10 \cdot \frac{10}{11} \cdot \frac{10}{11} = \frac{1000}{121} \approx 8.26 \text{ V/V}$$
* **(b)** 代入条件：
    $$A_v = 10 \cdot \left( \frac{R_s}{2R_s} \right) \cdot \left( \frac{R_o}{2R_o} \right) = 10 \cdot 0.5 \cdot 0.5 = 2.5 \text{ V/V}$$
* **(c)** 代入条件：
    $$A_v = 10 \cdot \left( \frac{0.1R_s}{1.1R_s} \right) \cdot \left( \frac{0.1R_o}{1.1R_o} \right) = 10 \cdot \frac{1}{11} \cdot \frac{1}{11} = \frac{10}{121} \approx 0.0826 \text{ V/V}$$
*(注：这说明了为什么我们需要高输入电阻和低输出电阻，否则增益衰减严重)*

---

### **Homework 1.44**
**题目：** ![[BAO_Ch1_introduction _ 20260301.pdf#page=52]] 
一个放大器的小信号开路电压增益为 $40 \text{ dB}$，输入电阻 $R_i = 1 \text{ M}\Omega$，输出电阻 $R_o = 10 \text{ }\Omega$。现在接上 $R_L = 100 \text{ }\Omega$ 的负载。
1. 计算接上负载后的电压增益和功率增益（以 dB 表示）。
2. 如果放大器的峰值输出电流限制为 $100 \text{ mA}$，为了保证输出不失真，输入正弦波的最大有效值 (rms) 是多少？
3. 对应的最大输出功率是多少？

**解答：**
1. 首先将 $40 \text{ dB}$ 开路增益转换为线性倍数：$20\log_{10}(A_{vo}) = 40 \Rightarrow A_{vo} = 100 \text{ V/V}$。
   接上负载后的实际电压增益为：
   $$A_v = \frac{v_o}{v_i} = A_{vo} \cdot \frac{R_L}{R_L + R_o} = 100 \cdot \frac{100}{110} \approx 90.9 \text{ V/V}$$
   换算为 dB：$20\log_{10}(90.9) \approx 39.17 \text{ dB}$。
   功率增益 $A_p$ 为输出功率与输入功率之比：
   $$A_p = \frac{P_L}{P_i} = \frac{v_o^2 / R_L}{v_i^2 / R_i} = \left( \frac{v_o}{v_i} \right)^2 \cdot \frac{R_i}{R_L} = 90.9^2 \cdot \frac{10^6}{100} \approx 8.26 \times 10^7$$
   换算为 dB：$10\log_{10}(8.26 \times 10^7) \approx 79.17 \text{ dB}$。
2. 最大输出电流峰值为 $I_{o,peak} = 100 \text{ mA} = 0.1 \text{ A}$。
   此时负载上的最大电压峰值为：$V_{o,peak} = I_{o,peak} \cdot R_L = 0.1 \cdot 100 = 10 \text{ V}$。
   根据电压增益，输入电压的峰值为：$V_{i,peak} = \frac{V_{o,peak}}{A_v} = \frac{10}{90.9} \approx 0.11 \text{ V}$。
   转化为有效值 (rms)：$V_{i,rms} = \frac{V_{i,peak}}{\sqrt{2}} = \frac{0.11}{1.414} \approx 0.0778 \text{ V} = 77.8 \text{ mV}$。
3. 可获取的最大输出功率（有效功率）：
   $$P_{L,max} = \frac{V_{o,rms}^2}{R_L} = \frac{(10 / \sqrt{2})^2}{100} = \frac{50}{100} = 0.5 \text{ W}$$

---

### **Homework 1.48**
**题目：** ![[BAO_Ch1_introduction _ 20260301.pdf#page=53]] 
你有两个放大器 A 和 B，需要级联连接在信号源（$10\text{mV}, R_s = 100 \text{ k}\Omega$）和负载（$R_L = 100 \text{ }\Omega$）之间。
A 参数: $A_{vo} = 100 \text{ V/V}, R_i = 10 \text{ k}\Omega, R_o = 10 \text{ k}\Omega$。
B 参数: $A_{vo} = 1 \text{ V/V}, R_i = 100 \text{ k}\Omega, R_o = 100 \text{ }\Omega$。
比较两种连接方式（S-A-B-L 和 S-B-A-L）的整体电压增益（比值及 dB），并判断哪种最好。

**解答：**
**方式 1：S-A-B-L (源 $\rightarrow$ A $\rightarrow$ B $\rightarrow$ 负载)**
$$\frac{v_o}{v_s} = \left( \frac{R_{iA}}{R_{iA} + R_s} \right) \cdot A_{voA} \cdot \left( \frac{R_{iB}}{R_{iB} + R_{oA}} \right) \cdot A_{voB} \cdot \left( \frac{R_L}{R_L + R_{oB}} \right)$$
$$\frac{v_o}{v_s} = \left( \frac{10\text{k}}{10\text{k} + 100\text{k}} \right) \cdot 100 \cdot \left( \frac{100\text{k}}{100\text{k} + 10\text{k}} \right) \cdot 1 \cdot \left( \frac{100}{100 + 100} \right)$$
$$\frac{v_o}{v_s} = \left( \frac{10}{110} \right) \cdot 100 \cdot \left( \frac{100}{110} \right) \cdot 1 \cdot 0.5 \approx 0.0909 \cdot 100 \cdot 0.909 \cdot 0.5 \approx 4.13 \text{ V/V}$$
换算为 dB：$20\log_{10}(4.13) \approx 12.3 \text{ dB}$。

**方式 2：S-B-A-L (源 $\rightarrow$ B $\rightarrow$ A $\rightarrow$ 负载)**
$$\frac{v_o}{v_s} = \left( \frac{R_{iB}}{R_{iB} + R_s} \right) \cdot A_{voB} \cdot \left( \frac{R_{iA}}{R_{iA} + R_{oB}} \right) \cdot A_{voA} \cdot \left( \frac{R_L}{R_L + R_{oA}} \right)$$
$$\frac{v_o}{v_s} = \left( \frac{100\text{k}}{100\text{k} + 100\text{k}} \right) \cdot 1 \cdot \left( \frac{10\text{k}}{10\text{k} + 100} \right) \cdot 100 \cdot \left( \frac{100}{100 + 10\text{k}} \right)$$
$$\frac{v_o}{v_s} = 0.5 \cdot 1 \cdot \left( \frac{10000}{10100} \right) \cdot 100 \cdot \left( \frac{100}{10100} \right) \approx 0.5 \cdot 0.99 \cdot 100 \cdot 0.0099 \approx 0.49 \text{ V/V}$$
换算为 dB：$20\log_{10}(0.49) \approx -6.2 \text{ dB}$。

**结论：** S-A-B-L 方式更好。放大器 B 虽然没有增益（$1 \text{ V/V}$），但由于其输入电阻大、输出电阻小，作为一个完美的**缓冲器 (Buffer)** 级，极大地减小了级间负载效应。

---

### **Homework 1.53**
**题目：** ![[BAO_Ch1_introduction _ 20260301.pdf#page=54]] 
电流放大器 $R_i = 1 \text{ k}\Omega, R_o = 10 \text{ k}\Omega, A_{is} = 100 \text{ A/A}$。信号源 $v_s = 100 \text{ mV}, R_s = 100 \text{ k}\Omega$，负载 $R_L = 1 \text{ k}\Omega$。求电流增益 $i_o / i_i$、电压增益 $v_o / v_s$ 以及功率增益。

**解答：**
* **电流增益**：
    根据输出端的分流公式：
    $$\frac{i_o}{i_i} = A_{is} \cdot \frac{R_o}{R_o + R_L} = 100 \cdot \frac{10\text{k}}{10\text{k} + 1\text{k}} = 100 \cdot \frac{10}{11} \approx 90.9 \text{ A/A}$$
* **电压增益**：
    输入端电流：$i_i = \frac{v_s}{R_s + R_i} = \frac{v_s}{101\text{k}}$
    输出端电压：$v_o = i_o \cdot R_L = (90.9 \cdot i_i) \cdot 1\text{k} = 90.9 \cdot \left(\frac{v_s}{101\text{k}}\right) \cdot 1\text{k} = \frac{90.9}{101} \cdot v_s \approx 0.9 \cdot v_s$
    因此，电压增益 $\frac{v_o}{v_s} = 0.9 \text{ V/V}$。
* **功率增益**：
    $$A_p = \frac{P_L}{P_i} = \frac{i_o^2 R_L}{i_i^2 R_i} = \left( \frac{i_o}{i_i} \right)^2 \cdot \frac{R_L}{R_i} = (90.9)^2 \cdot \frac{1\text{k}}{1\text{k}} \approx 8264$$
    换算为 dB：$10\log_{10}(8264) \approx 39.17 \text{ dB}$。

---

### **Homework 1.54**
**题目：** ![[BAO_Ch1_introduction _ 20260301.pdf#page=54]] 
跨导放大器 (Transconductance amplifier)，参数为 $R_i = 2 \text{ k}\Omega, G_m = 40 \text{ mA/V}, R_o = 20 \text{ k}\Omega$。连接内阻 $R_s = 2 \text{ k}\Omega$ 的电压源，负载 $R_L = 1 \text{ k}\Omega$。求实现的电压增益 $\frac{v_o}{v_s}$。

**解答：**
在输入端：
$$v_i = v_s \cdot \frac{R_i}{R_i + R_s} = v_s \cdot \frac{2\text{k}}{2\text{k} + 2\text{k}} = 0.5 v_s$$
在输出端，受控电流源产生 $G_m \cdot v_i$ 的电流，该电流流过 $R_o$ 与 $R_L$ 的并联网络以产生输出电压：
$$v_o = (G_m \cdot v_i) \cdot (R_o || R_L)$$
计算并联电阻：$R_o || R_L = \frac{20\text{k} \cdot 1\text{k}}{20\text{k} + 1\text{k}} = \frac{20}{21} \text{ k}\Omega \approx 0.952 \text{ k}\Omega = 952 \text{ }\Omega$。
代入前面的数据：
$$v_o = \left( 40 \times 10^{-3} \text{ A/V} \cdot 0.5 v_s \right) \cdot 952 \text{ }\Omega = 20 \times 10^{-3} \cdot 952 \cdot v_s \approx 19.04 v_s$$
因此，实现的电压增益 $\frac{v_o}{v_s} \approx 19.04 \text{ V/V}$。

---

### **Homework 1.57**
**题目：** ![[BAO_Ch1_introduction _ 20260301.pdf#page=55]] 
设计一个放大器用来检测换能器的开路输出电压。
1. 换能器源电阻 $R_s$ 变化范围 $1 \text{ k}\Omega \sim 10 \text{ k}\Omega$。
2. 负载 $R_L$ 变化范围 $1 \text{ k}\Omega \sim 10 \text{ k}\Omega$。
3. 对应 $R_s$ 变化，输出电压最大变化不能超过 10%。
4. 对应 $R_L$ 变化，输出电压最大变化也不能超过 10%。
5. 换能器输出 $10 \text{ mV}$ 时，负载端应至少有 $1 \text{ V}$ 的电压。
需要选择哪种类型的放大器？请确定 $R_i, R_o$（以 $1 \times 10^m \text{ }\Omega$ 格式）和增益参数。

**解答：**
输入端是电压，输出端也是要求维持电压比例，所以我们需要一个**电压放大器 (Voltage Amplifier)**。

1. **确定 $R_i$：**
   为了减弱 $R_s$ 变化对系统的影响，必须要求 $R_i \gg R_s$。
   输入分压系数最差的情况发生在 $R_s = 10\text{k}$。
   按题意要求：$\frac{R_i}{R_i + 10\text{k}} \ge 0.9 \cdot \frac{R_i}{R_i + 1\text{k}}$
   化简得到：$R_i + 1\text{k} \ge 0.9 (R_i + 10\text{k}) \Rightarrow 0.1 R_i \ge 8\text{k} \Rightarrow R_i \ge 80 \text{ k}\Omega$。
   按照要求的格式，取 $R_i = 1 \times 10^5 \text{ }\Omega$ ($100 \text{ k}\Omega$)。

2. **确定 $R_o$：**
   为了减弱 $R_L$ 变化对输出电压的拉低效应，必须要求 $R_o \ll R_L$。
   输出分压系数最差的情况发生在 $R_L$ 最小时，即 $R_L = 1\text{k}$。
   按题意要求，当 $R_L$ 从 $10\text{k}$ 降到 $1\text{k}$ 时，电压衰减不得低于 $10\text{k}$ 时的 90%（为保守计算，也可以直接让 $1\text{k}$ 时的分压比 $\ge 0.9$）：
   $\frac{1\text{k}}{1\text{k} + R_o} \ge 0.9 \Rightarrow 1\text{k} \ge 900 + 0.9 R_o \Rightarrow 0.9 R_o \le 100 \Rightarrow R_o \le 111 \text{ }\Omega$。
   按照要求的格式，取 $R_o = 1 \times 10^2 \text{ }\Omega$ ($100 \text{ }\Omega$) 或 $1 \times 10^1 \text{ }\Omega$ ($10 \text{ }\Omega$)。这里取 $R_o = 1 \times 10^2 \text{ }\Omega$ 即可满足。

3. **确定 $A_{vo}$：**
   最小整体增益要求：$\frac{1 \text{ V}}{10 \text{ mV}} = 100 \text{ V/V}$。
   整体增益最小的情况发生在 $R_s = 10\text{k}$ 且 $R_L = 1\text{k}$ 时：
   $$100 \le A_{vo} \cdot \left(\frac{100\text{k}}{100\text{k} + 10\text{k}}\right) \cdot \left(\frac{1\text{k}}{1\text{k} + 100}\right)$$
   $$100 \le A_{vo} \cdot \frac{10}{11} \cdot \frac{10}{11} \Rightarrow A_{vo} \cdot \frac{100}{121} \ge 100 \Rightarrow A_{vo} \ge 121 \text{ V/V}$$
   所以，应设计 $A_{vo} \ge 121 \text{ V/V}$。