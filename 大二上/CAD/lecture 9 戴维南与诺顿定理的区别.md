
# Thevenin vs Norton 速查（兼容性优先版）

**一句话总结**
- **Thevenin 等效**：理想电压源 $V_{th}$ 串联电阻 $R_{th}$
- **Norton 等效**：理想电流源 $I_N$ 并联电阻 $R_N$
- **结论**：二者对外完全等价（源模型不同而已）

---

## 核心区别

### 1. 等效形式
- **Thevenin**: 电压源 + 串联电阻 $\rightarrow (V_{th}, R_{th})$
- **Norton**: 电流源 + 并联电阻 $\rightarrow (I_N, R_N)$

### 2. 标称参数
- **Thevenin**: 
	- $V_{th} = V_{oc}$ （端口开路电压 Open Circuit Voltage）
	- $R_{th}$ 为端口等效电阻
- **Norton**: 
	- $I_N = I_{sc}$ （端口短路电流 Short Circuit Current）
	- $R_N$ 为端口等效电阻

### 3. 互换关系（源等效变换）
$$
\begin{aligned}
R_{th} &= R_N \\
V_{th} &= I_N \cdot R_N \\
I_N &= \frac{V_{th}}{R_{th}}
\end{aligned}
$$

---

## 计算步骤（线性两端口）

### 第一步：求等效电阻 $R_{eq}$ 
*(注：$R_{eq} = R_{th} = R_N$)*

1. **仅含独立源**：使用**置零法**
   - 电压源 $\rightarrow$ **短路** (Short, $V=0$)
   - 电流源 $\rightarrow$ **开路** (Open, $I=0$)
2. **含受控源**：使用**测试源法**
   - 端口加 $1\text{V}$ 电压源或 $1\text{A}$ 电流源
   - 计算 $R_{eq} = \frac{V_{test}}{I_{test}}$

### 第二步：求幅值
- **Thevenin**: 求端口开路电压 $\rightarrow V_{oc} \Rightarrow V_{th}$
- **Norton**: 求端口短路电流 $\rightarrow I_{sc} \Rightarrow I_N$

---

## 何时更顺手？
* **用 Thevenin 直观**：当负载很大 ($R_L \uparrow$) 或关心端口**电压**时。
* **用 Norton 直观**：当负载很小 ($R_L \downarrow$) 或关心端口**电流**时。
* **通用情况**：做匹配/扫描负载时，任选其一（二者严格等价）。

---

> [!EXAMPLE] 小例子
> **已知**：$V_{th} = 12 \text{ V}$， $R_{th} = 3 \ \Omega$
> **则 Norton 参数为**：
> $$I_N = \frac{V_{th}}{R_{th}} = \frac{12}{3} = 4 \text{ A}$$
> $$R_N = R_{th} = 3 \ \Omega$$

---

## 变换速查表

| 形式 | 源参数 | 等效电阻 | 互换关系 |
| :--- | :--- | :--- | :--- |
| **Thevenin** | $V_{th} = V_{oc}$ | $R_{th}$ | $I_N = \frac{V_{th}}{R_{th}}$ |
| **Norton** | $I_N = I_{sc}$ | $R_N$ | $V_{th} = I_N \cdot R_N$ |
| **公共** | — | $R_{th} = R_N$ | — |

---

> [!WARNING] 注意事项
> 1. **适用范围**：只对**线性**两端口严格成立；非线性电路需在工作点线性化后使用。
> 2. **置零规则**：仅对**独立源**有效（电压源短路、电流源开路）。**受控源必须保留**，且 $R_{eq}$ 必须用测试源法求解。
> 3. **工程安全**：短路计算 ($I_{sc}$) 仅作理论分析或仿真手段，实物电路直接短接需谨慎，防止烧毁元件。

---

## 等效验证（对任意负载 $R_L$）

我们可以通过计算流过负载 $R_L$ 的电流 $I_L$ 来验证等效性：

1. **Thevenin 电路** (分压定律)：
   $$I_L = \frac{V_{th}}{R_{th} + R_L}$$

2. **Norton 电路** (分流定律)：
   $$I_L = I_N \cdot \left( \frac{R_N}{R_N + R_L} \right)$$

**证明**：
将 $I_N = \frac{V_{th}}{R_{th}}$ 和 $R_N = R_{th}$ 代入 Norton 公式：
$$ 
I_L = \left( \frac{V_{th}}{R_{th}} \right) \cdot \left( \frac{R_{th}}{R_{th} + R_L} \right) = \frac{V_{th}}{R_{th} + R_L} 
$$
**结论**：两式完全相同，故对任意 $R_L$ 等效成立。