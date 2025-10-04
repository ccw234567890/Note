## 第 12 页：从微观关系推到宏观电阻公式
![[Lecture 3.pdf#page=12]]

**目标**：从材料的导电特性推出
$$
R=\frac{l}{\sigma A}, \qquad V=RI.
$$

### 1) 三个基本关系
- 电流密度（单位面积电流）：
$$
J=\frac{I}{A}
$$

- 材料本构关系（欧姆介质）：
$$
J=\sigma E
$$
其中 $\sigma$ 为电导率（单位：$\mathrm{S/m}$）。

- 均匀导体内平均电场与电压差：
$$
E=\frac{V}{l}
$$

### 2) 串联代入，得到宏观关系
把 $J=\frac{I}{A}$、$J=\sigma E$、$E=\frac{V}{l}$ 连起来：
$$
\frac{I}{A}=\sigma\frac{V}{l} \quad\Rightarrow\quad V=\frac{l}{\sigma A}\,I.
$$

**定义电阻**
$$
R=\frac{l}{\sigma A}\quad(\text{单位：}\mathrm{\Omega})
$$

**直觉**：导线越长（$l$ 大）电阻越大；截面积越大（$A$ 大）电阻越小；材料越“能导”（$\sigma$ 大）电阻越小。

---

## 第 13 页：用“电阻率”写法 & 欧姆定律
![[Lecture 3.pdf#page=13]]

电阻率与电导率互为倒数：
$$
\rho=\frac{1}{\sigma}\quad(\text{单位：}\mathrm{\Omega\cdot m})
$$

常用电阻公式：
$$
R=\frac{\rho\,l}{A}
$$

于是电压与电流的线性关系为欧姆定律：
$$
V=RI
$$

**量纲检查**：$\rho$ 的单位为 $\mathrm{\Omega\cdot m}$，乘以 $l$（$\mathrm{m}$）得 $\mathrm{\Omega\cdot m^2}$，再除以 $A$（$\mathrm{m^2}$）得到 $\mathrm{\Omega}$，正确。

---

## 第 14 页：数值例题（算出 63.662 Ω）
![[Lecture 3.pdf#page=14]]

**已知**：均匀圆柱导线  
$l=10\ \mathrm{m}$，$r=1.0\times10^{-3}\ \mathrm{m}$，$\sigma=5.0\times10^{4}\ \mathrm{S/m}$。  
**求**：$R$。

### 1) 先算截面积
$$
A=\pi r^2
=\pi\,(1.0\times10^{-3}\ \mathrm{m})^2
=\pi\times10^{-6}\ \mathrm{m^2}
\approx 3.14159\times10^{-6}\ \mathrm{m^2}
$$

### 2) 代入 $R=\frac{l}{\sigma A}$
先算分母：
$$
\sigma A=(5.0\times10^{4})\times(3.14159\times10^{-6})
=(5\times3.14159)\times10^{-2}
\approx 0.1570795
$$

于是
$$
R=\frac{10}{0.1570795}\ \mathrm{\Omega}\ \approx\ 63.662\ \mathrm{\Omega}
$$

### 3) 用电阻率再验算（可选）
$$
\rho=\frac{1}{\sigma}=2.0\times10^{-5}\ \mathrm{\Omega\cdot m}
$$
$$
R=\frac{\rho\,l}{A}
=\frac{(2.0\times10^{-5})\times10}{3.14159\times10^{-6}}
\approx 63.662\ \mathrm{\Omega}
$$

> [!warning] 常见易错点  
> 1) 半径/直径勿混：$A=\pi r^2$，若给直径 $d$，先换 $r=d/2$。  
> 2) 毫米到米要平方：$1\ \mathrm{mm}=10^{-3}\ \mathrm{m}\Rightarrow r^2=10^{-6}\ \mathrm{m^2}$。  
> 3) 单位统一：$\sigma$ 用 $\mathrm{S/m}$、$l$ 用 $\mathrm{m}$、$A$ 用 $\mathrm{m^2}$，最后 $R$ 为 $\mathrm{\Omega}$。
