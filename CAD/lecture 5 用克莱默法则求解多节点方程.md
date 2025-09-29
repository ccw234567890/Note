## 用克莱默法则求解第 9 页的两节点方程
![[Lecture 5.pdf#page=9]]

### 1) 由 KCL 得到的线性方程组
由前面推到的两式（单位一致，系数已化简）：
$$
\begin{cases}
2.25\,V_1 - 1\,V_2 = 3,\\
-1\,V_1 + 1.5\,V_2 = 6.
\end{cases}
$$

矩阵形式：
$$
\underbrace{\begin{bmatrix}
2.25 & -1\\
-1 & 1.5
\end{bmatrix}}_{\displaystyle A}
\underbrace{\begin{bmatrix}
V_1\\
V_2
\end{bmatrix}}_{\displaystyle \mathbf{V}}
=
\underbrace{\begin{bmatrix}
3\\
6
\end{bmatrix}}_{\displaystyle \mathbf{b}}.
$$

### 2) 克莱默法则（2×2 版）
设
$$
\Delta=\det(A)=a_{11}a_{22}-a_{12}a_{21}.
$$
分别把 $A$ 的第 1 列/第 2 列替换为常数列 $\mathbf{b}$，得
$$
\Delta_1=\det\!\begin{bmatrix}
b_1 & a_{12}\\
b_2 & a_{22}
\end{bmatrix},\qquad
\Delta_2=\det\!\begin{bmatrix}
a_{11} & b_1\\
a_{21} & b_2
\end{bmatrix}.
$$
解为
$$
V_1=\frac{\Delta_1}{\Delta},\qquad V_2=\frac{\Delta_2}{\Delta}.
$$

### 3) 代入本题系数并计算
系数矩阵
$$
A=\begin{bmatrix}
2.25 & -1\\
-1 & 1.5
\end{bmatrix},\quad
\mathbf{b}=\begin{bmatrix}
3\\
6
\end{bmatrix}.
$$

行列式
$$
\Delta=\det(A)=2.25\times1.5-(-1)\times(-1)=3.375-1=2.375.
$$

第一列替换：
$$
\Delta_1=\det\!\begin{bmatrix}
3 & -1\\
6 & 1.5
\end{bmatrix}
=3\times1.5-(-1)\times6=4.5+6=10.5.
$$

第二列替换：
$$
\Delta_2=\det\!\begin{bmatrix}
2.25 & 3\\
-1 & 6
\end{bmatrix}
=2.25\times6-3\times(-1)=13.5+3=16.5.
$$

求解
$$
V_1=\frac{\Delta_1}{\Delta}=\frac{10.5}{2.375}\ \mathrm{V}\approx 4.421\ \mathrm{V},
$$
$$
V_2=\frac{\Delta_2}{\Delta}=\frac{16.5}{2.375}\ \mathrm{V}\approx 6.947\ \mathrm{V}.
$$

### 4) 一行速记（通用 2×2）
若
$$
\begin{cases}
a_{11}x+a_{12}y=b_1,\\
a_{21}x+a_{22}y=b_2,
\end{cases}
$$
则
$$
\Delta=a_{11}a_{22}-a_{12}a_{21},\quad
x=\frac{b_1a_{22}-a_{12}b_2}{\Delta},\quad
y=\frac{a_{11}b_2-b_1a_{21}}{\Delta}.
$$
把 $x,y$ 分别替换成 $V_1,V_2$ 即可直接套用。
