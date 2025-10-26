# 实验详情：杨氏模量 (Young's Modulus) 测量

## 1. 实验目的 (Objectives)
1.  研究固体的弹性并测定其杨氏模量。
2.  正确使用精密测量仪器（如游标卡尺、螺旋测微器）来测量微小长度。
3.  理解在特定情况下用于消除系统误差的方法。

## 2. 核心原理与公式 (Core Principles & Formulas)

### A. 基本定义
- **应力 (Stress):** 单位面积上所受的力。
    - $stress = \frac{F}{A}$
    - $F$ 是施加的力， $A$ 是材料的横截面积。
- **应变 (Strain):** 材料的形变，即长度变化量与原始长度之比。
    - $strain = \frac{\Delta L}{L}$
    - $L$ 是原始长度， $\Delta L$ 是长度变化量。应变是无量纲的。
- **杨氏模量 (Young's Modulus, E):** 在弹性形变中，应力与应变之比的常数。
    - $E = \frac{Stress}{Strain} = \frac{F \times L}{A \times \Delta L}$

### B. 测量方法：光杠杆法 (Optical Lever)
- **挑战:** $\Delta L$（线的伸长量）通常非常小，难以精确测量。
- **解决方案:** 使用光杠杆 (Optical lever) 来放大并测量这个微小的伸长量。
- **核心部件:**
    - **$b$ (光杠杆长度):** 后金属足尖到两前足尖连线的距离。
    - **$D$ (镜尺距离):** 平面镜到测量标尺（米尺）之间的距离。
- **放大原理:**
    1.  当线伸长 $\Delta L$ 时，光杠杆的后足下降，导致平面镜倾斜一个角度 $\alpha$。
    2.  几何关系: $tan~\alpha = \frac{\Delta L}{b}$。
    3.  根据光的反射定律，望远镜中看到的标尺读数会从 $n_0$ 变为 $n_1$，标尺上的变化量为 $\Delta n = |n_1 - n_0|$。
    4.  光学关系: $tan~2\alpha = \frac{\Delta n}{D}$。
- **小角度近似:**
    - 由于 $\Delta L$ 非常小， $tan~\alpha \cong \alpha \cong \frac{\Delta L}{b}$。
    - 同样， $tan~2\alpha \cong 2\alpha \cong \frac{\Delta n}{D}$。
- **推导:**
    - $2 \times (\frac{\Delta L}{b}) \cong \frac{\Delta n}{D}$
    - $\Delta L = \frac{b \cdot \Delta n}{2D}$

### C. 最终计算公式
- 将 $A = \pi d^2 / 4$ 和 $\Delta L = \frac{b \cdot \Delta n}{2D}$ 代入 $E = \frac{F \times L}{A \times \Delta L}$ 中。
- **计算公式 (来自教材计算部分):**
    - $\overline{E} = \frac{8FL D}{\pi \overline{d}^2 b \overline{\Delta n}}$
    - *注意：教材P6的公式 似乎遗漏了 $b$，应以P13的计算公式 为准。*

## 3. 实验仪器 (Required Equipment)
- 垂直支架 (Vertical stand)
- 光杠杆 (Optical lever)
- 一组千克砝码 (Set of kilogram weights)
- 游标卡尺 (Vernier caliper)
- 望远镜 (Telescope)
- 螺旋测微器 (Micrometer screw gauge)
- 钢卷尺 (Steel tape)

## 4. 实验步骤 (Experimental Procedure)
1.  **准备:** 在砝码架上加 ==两个砝码==。
2.  **测量 $d$ (钢丝直径):**
    - 使用 ==螺旋测微器 (micrometer caliper)==。
    - 在钢丝的 ==上、中、下== 三个点，每个点 ==三个不同方向== (共9次测量)。
    - 记录螺旋测微器的“零点读数 (zero reading)”。
    - 记录在 Data Table 3.4-1。
3.  **测量 $L_0$ (钢丝原长):**
    - 使用 ==钢卷尺 (steel tape)==。
    - 记录在 Data Table 3.4-1。
4.  **安装光杠杆:**
    - 两个前足放入平槽的凹槽中。
    - ==后足放在夹具 (clamp) 表面==。
    - *注意：后足==不能==放入夹具和平槽的缝隙中*。
5.  **测量 $\Delta n$ (标尺读数变化):**
    - 调整望远镜，直到能清晰看到标尺图像。
    - **加载 (Loading):** 每次增加 1kg 砝码，==最多加到 9kg==。每次==系统静止后==读取望远镜读数 $n_i'$。记录在 Data Table 3.4-2。
    - **卸载 (Unloading):** 再加一个砝码（总重 10kg），此时==不读数==。然后每次==卸载 1kg==，并读取读数 $n_i''$。记录在 Data Table 3.4-2。
6.  **测量 $D$ (镜尺距离):**
    - 使用 ==钢卷尺 (steel tape)== 测量光杠杆平面镜到钢尺的距离 $D_0$。
    - 记录在 Data Table 3.4-1。
7.  **测量 $b$ (光杠杆长度):**
    - 使用 ==游标卡尺 (vernier caliper)==。
    - 将光杠杆按在一张白纸上，得到三个压痕。
    - 测量后足压痕到两前足压痕连线的距离 $b_0$。
    - 记录在 Data Table 3.4-1。

## 5. 关键仪器使用 (Instrument Usage)

### A. 螺旋测微器 (Micrometer Caliper)
- **读数:** 主尺（桶）读数 + 副尺（套管）读数。
- **精度:** 套管刻度为 0.01 mm。
- **示例:** 主尺读到 16.5 mm，套管读到 0.161 mm，最终读数为 $16.500 + 0.161 = 16.661$ mm。
- **零点修正:** ==必须==进行零点检查。
    - **$Corrected~reading = actual~reading - zero~reading$ (修正读数 = 实际读数 - 零点读数)**。

### B. 游标卡尺 (Vernier Caliper)
- **精度 (示例中):** 50 分度，精度为 0.02 mm。
- **读数:** 主尺读数 + 游标尺对齐刻度读数。
- **示例 (50分度):** $3~cm$ (主尺) + $0.3~cm$ (主尺) + $(0.002 \times 16)~cm$ (游标尺) = $3.332~cm = 33.32~mm$。
- **零点修正:** 同样需要检查零点。
    - **$Corrected~reading = actual~reading - zero~reading$ (修正读数 = 实际读数 - 零点读数)**。

## 6. 数据处理 (Calculations)
1.  **计算平均直径 $\overline{d}$:**
    - $\overline{d} = \frac{1}{9}(d_1 + d_2 + ... + d_9)$ (使用9次测量的平均值)。
2.  **计算平均读数差 $\overline{\Delta n}$:**
    - 对应于 $F = 4 \times g$ (N) 的力。
    - 采用 ==逐差法== (Successive difference method) 计算平均值:
    - $\overline{\Delta n} = \frac{1}{4}[|n_7 - n_3| + |n_6 - n_2| + |n_5 - n_1| + |n_4 - n_0|]$。
    - *注意: $n_0$ 到 $n_7$ 对应的是 Data Table 3.4-2 中 2.00kg 到 9.00kg 的读数均值*。
3.  **计算杨氏模量 $\overline{E}$:**
    - $\overline{E} = \frac{8FL D}{\pi \overline{d}^2 b \overline{\Delta n}}$ (使用 $F = 4 \times g$)。
4.  **计算不确定度 $\sigma_E$:**
    - 使用不确定度传播公式：
    - $\sigma_E = \overline{E} \times \sqrt{(\frac{\sigma_L}{L})^2 + (\frac{\sigma_D}{D})^2 + (2\frac{\sigma_d}{d})^2 + (\frac{\sigma_b}{b})^2 + (\frac{\sigma_{\overline{\Delta n}}}{\overline{\Delta n}})^2}$
    - 必须先确定 $\sigma_L, \sigma_D, \sigma_d, \sigma_b, \sigma_{\overline{\Delta n}}$ 这些直接测量量的不确定度。
5.  **报告最终结果:**
    - $\overline{E} = \overline{E} \pm \sigma_E~(N/m^2)$。

## 7. 思考题 (Study Questions)

### A. 预习题 (Prelab Assignment)
- (1) 0.02mm 游标卡尺的仪器误差和读数误差？
- (2) 杨氏模量的定义？实验中需要测量哪些量？ 在最终公式 (3.4-5) 中，哪个量最关键？为什么？
- (3) 光杠杆的主要功能是什么？ 它的放大倍数是多少？

### B. 课后问题 (Post Lab Questions)
- (1) 哪个测量更关键：线的长度 ($L$) 还是线的伸长量 ($\Delta L$)？为什么？ 为什么 $L$ 用米尺测量，而 $\Delta L$ 需要用非常敏感的设备测量？
- (2) 为什么初始的负载（砝码架+2kg砝码）没有包含在我们的计算中？ 我们可以使用不同的初始负载吗？解释。