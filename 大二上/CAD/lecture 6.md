# Lecture 6 — Mesh Analysis & Supermesh （精讲笔记）

---

## 封面
![[Lecture 6.pdf#page=1]]

课程：Circuit Analysis and Design（2025/2026 S1）  
讲次：Lecture 6  
主题：Mesh Analysis，Supermesh

---

## 议程
![[Lecture 6.pdf#page=2]]

- Mesh Analysis（网孔分析）  
- Supermesh（超网孔）  
- 小结与要点

---

## Mesh Analysis 概念与依据
![[Lecture 6.pdf#page=3]]

- 目标：直接求**网孔电流**（每个 mesh 里假定顺时针电流）。  
- 依据：  
  1) **KVL**：一周电压降代数和为 0。  
  2) **Ohm 定律**：电阻压降 $V_R=R\,I$。  
- 已知网孔电流后：可求任意支路电流、结点电压与功率。

---

## Mesh 定义与示例
![[Lecture 6.pdf#page=4]]

- **网孔（Mesh）**：内部不再含更小回路的闭合回路。  
- 共 2 个 Mesh（示意图），分别定义电流 $I_1, I_2$（顺时针）。

---

## Mesh vs. Nodal 对照
![[Lecture 6.pdf#page=5]]

- **Nodal**：未知量是**结点电压**，基于 **KCL**。  
- **Mesh**：未知量是**网孔电流**，基于 **KVL**。  
- 电压源连地 → **已知结点电压**（Nodal 的“已知节点”）；  
  电流源只在某一个 Mesh 内 → **已知网孔电流**（Mesh 的“已知网孔”）。  
- 电压源跨两个未知节点 → **Supernode**；  
  电流源跨两个未知网孔 → **Supermesh**。

---

## Mesh 分析要点（文字版）
![[Lecture 6.pdf#page=6]]

- 每个网孔取**顺时针**电流 $I_k$。  
- 网孔中若有**电流源**且**仅属于该网孔**：该网孔电流**已知**（方向注意正负）。  
- **共享支路**的真实支路电流 = 两网孔电流之差（按假定方向）。  

---

## Mesh 分析要点（KVL 细节）
![[Lecture 6.pdf#page=7]]

- 每个网孔按顺时针走一圈：  
  $$\sum \text{(电压降)} = 0$$
- 单独电阻支路：$V=R\,I_\text{mesh}$。  
- 共享电阻支路：$V=R\,(I_\text{this}-I_\text{other})$。  
- 电压源：从“+”到“−”记 $+V_s$，从“−”到“+”记 $-V_s$。

---

## Mesh 四步法（操作流程）
![[Lecture 6.pdf#page=8]]

1) **识别网孔**（不含内回路的闭合环）。  
2) **标注网孔电流**（顺时针 $I_1,I_2,\dots$），并标电阻压降方向。  
3) **对未知网孔写 KVL**，电阻用 $V=RI$（共享支路用差流）。  
4) **解线性方程组**，得到各 $I_k$；再回代求支路电流、元件电压、功率。

---

## 例题 A：三网孔（其中一只电流源已知）
![[Lecture 6.pdf#page=9]]

- 设三网孔电流：$I_1,I_2,I_3$（顺时针）。  
- 题给：右侧电流源为 $I_s=3\,\text{mA}$，且与 $I_3$方向相反 ⇒  
  $$I_3=-\,3\ \text{mA}$$
- 未知仅 $I_1,I_2$，对 Mesh 1、Mesh 2 写 KVL 即可。

---

### 例题 A：Mesh 1 的 KVL
![[Lecture 6.pdf#page=10]]

按顺时针：
$$
(2000)I_1\;+\;2000(I_1 - I_3)\;+\;1000(I_1 - I_2)=0
$$
代入 $I_3=-3\ \text{mA}$ 并两边除以 $1000$：
$$
5I_1 - I_2 = -0.006\quad\text{(1)}
$$

---

### 例题 A：Mesh 2 的 KVL
![[Lecture 6.pdf#page=11]]

含电压源 $10\ \text{V}$：
$$
-10 + 1000(I_2 - I_1) + 2000(I_2 - I_3) = 0
$$
化简、除以 $1000$：
$$
-\,I_1 + 3I_2 = 0.004\quad\text{(2)}
$$

---

### 例题 A：联立求解与物理意义
![[Lecture 6.pdf#page=12]]

联立 (1)(2) 得：
$$
I_2=1\ \text{mA},\qquad I_1=-1\ \text{mA}.
$$
- $I_1<0$ 表示**实际方向**与假定顺时针相反。  
- 三网孔电流（单位 mA）：  
  $$I_1=-1,\quad I_2=+1,\quad I_3=-3.$$

---

### 例题 A：支路电流与元件电压
![[Lecture 6.pdf#page=13]]
![[Lecture 6.pdf#page=14]]

- 共享支路电流（按箭头方向）：  
  - 通过 $R_2$（左右共享）：$I_{R2}=I_2 - I_1 = 2\ \text{mA}$  
  - 通过 $R_3$（1 与 3 共享）：$I_{R3}=I_1 - I_3 = 2\ \text{mA}$  
  - 通过 $R_4$（2 与 3 共享）：$I_{R4}=I_2 - I_3 = 4\ \text{mA}$  
- 元件电压（“电压降方向”与上式同向）：  
  $$
  V_{R1}=R_1(-I_1)=2\ \text{V},\quad
  V_{R2}=R_2(I_2-I_1)=2\ \text{V},
  $$
  $$
  V_{R3}=R_3(I_1-I_3)=4\ \text{V},\quad
  V_{R4}=R_4(I_2-I_3)=8\ \text{V}.
  $$

---

## 例题 B（Example 3.12）：三未知网孔
![[Lecture 6.pdf#page=15]]
![[Lecture 6.pdf#page=16]]
![[Lecture 6.pdf#page=17]]

- 写三条 KVL（Mesh 1/2/3），遇共享支路用差流。  
- 代数整理（单位化后）：  
  $$
  \begin{aligned}
  17I_1-3I_2-4I_3&=0\quad (1)\\
  -3I_1+15I_2-12I_3&=0.009\quad (2)\\
  -4I_1-12I_2+17I_3&=-0.003\quad (3)
  \end{aligned}
  $$
- 消元（讲义演算）：  
  $$
  I_1=0.5\ \text{mA},\quad I_2=1.5\ \text{mA},\quad I_3=1.0\ \text{mA}.
  $$
- 由差流求支路电流，再得  
  $$
  V_1=R_4(I_2-I_3)=6\ \text{V},\quad
  V_2=R_5(I_3-I_4)=4\ \text{V}.
  $$

---

## 课堂练习（Mesh）
![[Lecture 6.pdf#page=18]]

提示：按“四步法”写 KVL，解未知网孔电流，再回代出指定电压/电流。

---

## 例题 C（Example 3.13）：电压控制电流源（VCCS）
![[Lecture 6.pdf#page=21]]
![[Lecture 6.pdf#page=22]]
![[Lecture 6.pdf#page=23]]

- 受控源：$I_3=-0.006\,V_1$，且 $V_1=v$ 与网孔电流满足关系。  
- 由依赖关系推出 $I_3=\dfrac{12}{11}I_2$，再与两条 KVL 联立：  
  $$
  \begin{aligned}
  12I_1-3I_2-4I_3&=0,\\
  3I_1+5I_2-2I_3&=0.006.
  \end{aligned}
  $$
- 解得（讲义数值）：
  $$
  I_1=3.767\,\text{mA},\ 
  I_2=6.140\,\text{mA},\ 
  I_3=6.698\,\text{mA}.
  $$
- 电压：
  $$
  V_1=R_4(I_2-I_3)\approx -1.116\ \text{V},\quad
  V_2=V_1+R_3(I_1-I_3)\approx -12.837\ \text{V}.
  $$
- 功率校核：$\sum P_\text{电阻}+P_\text{源}=0$（讲义给出平衡成立）。

---

## Supermesh 概念
![[Lecture 6.pdf#page=24]]
![[Lecture 6.pdf#page=25]]
![[Lecture 6.pdf#page=26]]
![[Lecture 6.pdf#page=27]]

- **电流源**若位于**两个网孔公共支路**，该支路电压未知，单独写两个 KVL 都会含未知源电压 $v$。  
- **做法**：把这两个网孔合并成**Supermesh**，**绕开电流源**写**一条** KVL：  
  $$
  \sum V_R = 0\quad (\text{把电流源那一枝跳过})
  $$
- 还需**额外一条方程**：来自电流源的电流约束（两网孔电流差等于源电流）：  
  $$
  I_\text{同向} - I_\text{反向} = I_s.
  $$

---

## 小测（识别 Supermesh）
![[Lecture 6.pdf#page=28]]

- 若电流源位于 Mesh 2 与 Mesh 3 的公共支路 → **Supermesh = {Mesh 2, Mesh 3}**。  
- 先写 supermesh 的 KVL，再配上 $I_3-I_2=I_s$。

---

## 例题 D（Example 3.15）：Supermesh 求解
![[Lecture 6.pdf#page=29]]
![[Lecture 6.pdf#page=30]]

- 由电流源：$I_3=I_2+0.002$。  
- Supermesh KVL（跳过电流源支路）：  
  $$
  -3I_1+2I_2+2.75I_3=0.
  $$
- Mesh 1 KVL：  
  $$
  3I_1 - I_2 - 2I_3 = 0.005.
  $$
- 联立得：  
  $$
  I_2=2\ \text{mA},\quad I_1=5\ \text{mA},\quad I_3=4\ \text{mA}.
  $$
- 受控支路电压（示例）：$v=1\ \text{V}$（按图公式计算）。

---

## 例题 E（Example 3.17）：含受控关系的 Supermesh
![[Lecture 6.pdf#page=31]]
![[Lecture 6.pdf#page=32]]

- 受控关系：$I_3-I_2=0.0005\,v$，且 $v=6000\,I_1$ ⇒ $I_3=3I_1+I_2$。  
- Supermesh KVL：  
  $$
  -1.8I_1 + 4.9I_2 = 0.008.
  $$
- Mesh 1 KVL：  
  $$
  I_2 = 2I_1.
  $$
- 解得：  
  $$
  I_1=1\ \text{mA},\quad I_2=2\ \text{mA},\quad I_3=5\ \text{mA}.
  $$
- 电压：$V_2=R_4 I_3=2\ \text{V}$，  
  $V_1=V_s - R_2(I_2-I_1)=4\ \text{V}$。

---

## Summary（要点回顾）
![[Lecture 6.pdf#page=33]]

- 网孔电流法：每个网孔一条 **KVL**，共享支路用差流。  
- 电流源在单一网孔内 → 该网孔电流已知。  
- 电流源位于两网孔公共支路 → **Supermesh**：  
  - 超网孔写**一条** KVL（跳过电流源支路），  
  - 再加**电流源约束**（两网孔电流之差）。  
- 解出网孔电流后即可求任意支路电流、电压及功率。
