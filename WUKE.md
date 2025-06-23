---
**Linear Algebra Review - 线性代数复习**

这份PDF文档提供了线性代数核心概念的总结，主要包括线性方程组求解、矩阵形式、向量空间、特征值/特征向量和正交性等。

---

### **1. 求解线性系统 $A\vec{x}=\vec{b}$**

**定义：矩形矩阵的阶梯形 (Echelon Form, REF)**
一个矩形矩阵是阶梯形（或行阶梯形），如果它满足以下三个性质:
1.  [cite_start]所有非零行都在全零行的上方 。
2.  [cite_start]每一行的首个非零元素（leading entry）所在的列，位于其上方行的首个非零元素的右侧 。
3.  [cite_start]首个非零元素所在列下方的所有元素都是零 。

**定义：简化阶梯形 (Reduced Row Echelon Form, RREF)**
[cite_start]如果阶梯形矩阵（REF）满足以下附加条件，则称为简化阶梯形（RREF） 。
* [cite_start]RREF 是唯一的，而 REF 不唯一 。

**例子 (REF 与 RREF):**
* **REF:**
    ```
    [x x x x]
    [0 x x x]
    [0 0 0 x]
    ```
* **RREF:**
    ```
    [1 0 0 x]
    [0 1 0 x]
    [0 0 1 x]
    ```

**定义：主元位置 (Pivot Position) 和主元列 (Pivot Column)**
* [cite_start]矩阵 $A$ 中的主元位置是指在简化阶梯形中对应的首个非零元素（leading 1）所在的位置 。
* [cite_start]主元列是矩阵 $A$ 中包含主元位置的列 。

**例子 (主元位置和主元列):**
![[Pasted image 20250623205543.png]]
上述矩阵中，第一列、第三列和第四列是主元列 。 
### **2. 线性系统解的存在性和唯一性 ($A\vec{x}=\vec{b}$)**

**定理：解的存在性和唯一性**
[cite_start]一个线性系统是**一致的**（consistent），当且仅当增广矩阵的最右列不是主元列 [cite: 258][cite_start]。也就是说，阶梯形矩阵中没有形如 $[0\ 0\ \dots\ 0\ |\ b]$ 且 $b$ 非零的行 。

如果一个线性系统是一致的，那么解集包含:
* [cite_start]**唯一解：** 当没有自由变量时 。
* [cite_start]**无穷多解：** 当至少有一个自由变量时 。

**例子 (解的存在性):**
* `[x x x x]`
  `[0 x x x]`
  [cite_start]`[0 0 0 5]` $\implies$ **无解** 
* `[x x x x]`
  `[0 x x x]`
  [cite_start]`[0 0 x x]` $\implies$ **唯一解** 
* `[x x x x]`
  `[0 x x x]`
  [cite_start]`[0 0 0 0]` $\implies$ **无穷多解** 

**应用示例：**
[cite_start]给定矩阵 $A = \begin{pmatrix} 1 & 1 & 2 \\ 2 & 3 & 7 \\ 0 & a & -a \\ \end{pmatrix}$，且 $A$ 与矩阵 $B = \begin{pmatrix} 1 & 0 & -1 \\ 0 & 1 & 1 \\ 2 & 1 & 1 \\ \end{pmatrix}$ 行等价 。
* **(a) 确定 $a$ 的值，使 $A\vec{x}=\vec{b}$ 有无穷多解。**
  [cite_start]方法：找到 $A$ 的 RREF，然后将其与 $B$ 相等，从而找到 $a$ 的值 。
* **(b) 找到可逆矩阵 $P$ 使得 $PA=B$。**
  [cite_start]方法：从 $PA=B$ 推出 $P=BA^{-1}$ 。

---

### **3. 向量的线性独立性与张成空间**

**定义：线性独立集**
[cite_start]一个向量集 $\{\vec{u}_1, \dots, \vec{v}_p\}$ 在 $\mathbb{R}^n$ 中被称为**线性独立**的，如果向量方程 $x_1\vec{u}_1 + x_2\vec{u}_2 + \dots + x_p\vec{v}_p = \vec{0}$ 只有平凡解 。
[cite_start]如果存在不全为零的权重 $c_1, c_2, \dots, c_p$ 使得 $c_1\vec{v}_1 + c_2\vec{v}_2 + \dots + c_p\vec{v}_p = \vec{0}$，则该集合被称为**线性相关**的 。

**判断线性独立性**:
* [cite_start]如果向量集 $\{\vec{u}_1, \dots, \vec{v}_p\}$ 是线性独立的，那么由这些向量组成的矩阵 $A = [\vec{u}_1\ \dots\ \vec{v}_p]$ 的每一列都应该是主元列 。
* 等价地，方程 $A\vec{x}=\vec{0}$ 只有平凡解。

**定义：张成空间 (Span)**
[cite_start]如果在 $\mathbb{R}^n$ 中有向量 $\vec{u}_1, \dots, \vec{u}_p$，那么它们的所有线性组合的集合，记作 $\text{Span}\{\vec{u}_1, \dots, \vec{u}_p\}$，被称为由这些向量**张成**（或**生成**）的子空间 。
[cite_start]也就是说，$\text{Span}\{\vec{u}_1, \dots, \vec{u}_p\}$ 是所有形如 $c_1\vec{u}_1 + c_2\vec{u}_2 + \dots + c_p\vec{u}_p$ 的向量的集合，其中 $c_i$ 是标量 。

**例子：如何判断向量是否线性独立？**
[cite_start]给定向量 $\vec{v}_1, \vec{v}_2, \vec{v}_3$ [cite: 265][cite_start]。要验证它们是否线性独立，可以设置方程 $c_1\vec{v}_1 + c_2\vec{v}_2 + c_3\vec{v}_3 = \vec{0}$，并将其写成矩阵形式 $A\vec{c} = \vec{0}$，其中 $A = [\vec{v}_1\ \vec{v}_2\ \vec{v}_3]$，$\vec{c} = \begin{pmatrix} c_1 \\ c_2 \\ c_3 \\ \end{pmatrix}$ 。如果此方程只有平凡解，则向量线性独立。

---

### **4. 列空间、零空间、基和秩**

**定义：基 (Basis)**
[cite_start]向量空间 $H$ 的一个基是一个线性独立集 $B = \{\vec{v}_1, \dots, \vec{v}_p\}$，并且它能够张成 $H$ 。
* [cite_start]如果 $B$ 是基，则 $c_1\vec{v}_1 + \dots + c_p\vec{v}_p = \vec{0} \implies c_1 = \dots = c_p = 0$（线性独立） 。
* [cite_start]任何在 $H$ 中的向量 $\vec{x}$ 都可以唯一地写成基向量的线性组合：$\vec{x} = c_1\vec{v}_1 + \dots + c_p\vec{v}_p$（张成且唯一表示） 。

**定义：列空间 (Column Space, Col($A$))**
[cite_start]矩阵 $A$ 的列空间是 $A$ 的列向量的所有线性组合的集合 。
[cite_start]如果 $A = [\vec{a}_1\ \vec{a}_2\ \dots\ \vec{a}_n]$ 且 $\vec{a}_j \in \mathbb{R}^m$，那么 $\text{Col}(A) = \text{Span}\{\vec{a}_1, \dots, \vec{a}_n\}$ 。

**求 Col($A$) 的基**:
1. [cite_start]将 $A$ 行化简到 REF 。
2. [cite_start]识别 REF 中的主元列 。
3. [cite_start]回到**原始矩阵 $A$**，主元列对应的列向量构成 Col($A$) 的基 。

**例子 (Col($A$) 的基和维数):**
[cite_start]$A = \begin{pmatrix} -3 & 6 & 4 & 1 & -7 \\ 1 & -2 & 2 & 3 & -1 \\ 2 & -4 & 5 & 8 & 4 \\ \end{pmatrix} \simeq \begin{pmatrix} 1 & -2 & 0 & -1 & 3 \\ 0 & 0 & 1 & 2 & -2 \\ 0 & 0 & 0 & 0 & 0 \\ \end{pmatrix}$ (REF) 
* [cite_start]主元在第一列和第三列 。
* [cite_start]Col($A$) 的基是 $A$ 的第一列和第三列：$\left\{ \begin{pmatrix} -3 \\ 1 \\ 2 \\ \end{pmatrix}, \begin{pmatrix} 4 \\ 2 \\ 5 \\ \end{pmatrix} \right\}$ 。
* [cite_start]$\text{dim Col}(A) = \text{Rank}(A) = 2$ 。

**定义：零空间 (Null Space, Nul($A$))**
[cite_start]矩阵 $A$ 的零空间是齐次方程 $A\vec{x}=\vec{0}$ 的所有解的集合 。

**求 Nul($A$) 的基**:
1. 通过对增广矩阵 $[A | [cite_start]\vec{0}]$ 进行行化简，得到简化阶梯形 。
2. 解 $A\vec{x}=\vec{0}$，写出通解，将基本变量表示为自由变量的线性组合。
3. [cite_start]通解的参数向量形式中的向量就是 Nul($A$) 的基向量 。

**秩与零度定理 (Rank Theorem)**
* [cite_start]$\text{dim Nul}(A) = (\text{A 的总列数}) - \text{Rank}(A)$ 。
* [cite_start]**例子：** 上述 $A$ 矩阵有 5 列，Rank($A$) = 2。所以 $\text{dim Nul}(A) = 5 - 2 = 3$ 。

---

### **5. 特征值、特征向量和相似变换**

**定义：特征值 (Eigenvalue) 和特征向量 (Eigenvector)**
[cite_start]矩阵 $A$ 的一个**特征向量**是一个非零向量 $\vec{x}$，使得 $A\vec{x}=\lambda\vec{x}$，其中 $\lambda$ 是一个标量 。
[cite_start]标量 $\lambda$ 被称为 $A$ 的一个**特征值**，如果存在一个非平凡解（即非零向量）$\vec{x}$ 满足 $A\vec{x}=\lambda\vec{x}$ [cite: 269][cite_start]。这个 $\vec{x}$ 就是对应于 $\lambda$ 的特征向量 。

**如何计算特征值和特征向量**:
1. [cite_start]**求特征值：** 将方程 $A\vec{x}=\lambda\vec{x}$ 改写为 $(A-\lambda I)\vec{x}=\vec{0}$ 。
   为了使这个齐次方程有非平凡解，系数矩阵 $(A-\lambda I)$ 必须是奇异的（不可逆），即 $\text{det}(A-\lambda I)=0$。解这个方程（特征方程）可以得到特征值 $\lambda$。
2. [cite_start]**求特征向量：** 一旦获得了特征值 $\lambda$，将其代入 $(A-\lambda I)\vec{x}=\vec{0}$，然后解这个齐次方程 [cite: 269][cite_start]。得到的非零解 $\vec{x}$ 就是对应于 $\lambda$ 的特征向量 。

[cite_start]**定理：** 对应于**不同特征值**的特征向量是线性独立的 。

**定义：相似变换 (Similarity Transformation)**
[cite_start]如果 $A$ 和 $B$ 是 $n \times n$ 矩阵，那么 $A$ 被称为**相似于** $B$，如果存在一个可逆矩阵 $P$ 使得 $P^{-1}AP=B$ 或 $A=PBP^{-1}$ 。

**定理：相似矩阵的性质**
[cite_start]如果 $A$ 和 $B$ 相似，那么它们具有相同的特征多项式，因此也具有相同的特征值（包括重数） 。
[cite_start]但反过来不一定成立（即具有相同特征值的矩阵不一定相似） 。

---

### **6. 特征值和特征向量的应用**

**对角化 (Diagonalization)**
[cite_start]如果一个 $n \times n$ 矩阵 $A$ 有 $n$ 个线性独立的特征向量 $\vec{v}_1, \dots, \vec{v}_n$，分别对应特征值 $\lambda_1, \dots, \lambda_n$ 。
* [cite_start]我们可以构造矩阵 $P = [\vec{v}_1\ \vec{v}_2\ \dots\ \vec{v}_n]$ 和对角矩阵 $D = \text{diag}(\lambda_1, \lambda_2, \dots, \lambda_n)$ 。
* [cite_start]此时，$A=PDP^{-1}$ 。

**对称矩阵的对角化 (Orthogonal Diagonalization)**
* [cite_start]如果矩阵 $A$ 是对称的（$A=A^T$），那么我们可以找到一组正交且规范化的特征向量 $\vec{u}_1, \dots, \vec{u}_n$ 。
* [cite_start]这些特征向量满足 $\vec{u}_i \cdot \vec{u}_j = 0$ (当 $i \ne j$) 且 $\vec{u}_i \cdot \vec{u}_i = 1$ (当 $i = j$) 。
* [cite_start]此时，$P$ 是一个正交矩阵（即 $P P^T = I$，或 $P^T = P^{-1}$） 。
* [cite_start]因此，对称矩阵的对角化形式为 $A=PDP^T$ 。

**重复特征值的情况**:
* [cite_start]如果特征值有重数（几何重数不是1），情况会更复杂 。
* [cite_start]如果一个 $3 \times 3$ 矩阵 $A$ 有特征值 $\lambda_1 = \lambda_2 = 5$ 和 $\lambda_3 = 6$，如果对应于 $\lambda=5$ 有两个线性独立的特征向量，则矩阵是可对角化的 。
* [cite_start]如果对应于 $\lambda=5$ 只有一个线性独立的特征向量，则矩阵不可对角化 。

**矩阵的高次幂计算**:
* [cite_start]如果 $A=PDP^{-1}$，那么 $A^k = PD^k P^{-1}$ 。
* [cite_start]$D^k$ 是一个对角矩阵，其对角线元素为 $\lambda_i^k$ 。这大大简化了矩阵高次幂的计算。

---

### **7. 正交投影 (Orthogonal Projection)**

**单向量的正交投影**:
[cite_start]向量 $\vec{y}$ 在向量 $\vec{u}$ 上的正交投影为 $\text{Proj}_{\vec{u}}\vec{y} = \frac{\vec{y} \cdot \vec{u}}{\vec{u} \cdot \vec{u}}\vec{u}$ 。

**定理：正交分解定理 (Orthogonal Decomposition Theorem)**
[cite_start]设 $W$ 是 $\mathbb{R}^n$ 的一个子空间 [cite: 275][cite_start]。那么 $\mathbb{R}^n$ 中的每个向量 $\vec{y}$ 都可以唯一地写成 $\vec{y} = \hat{y} + \vec{z}$ 的形式，其中 $\hat{y}$ 在 $W$ 中，$\vec{z}$ 在 $W^\perp$（$W$ 的正交补）中 。
* [cite_start]事实上，如果 $\{\vec{u}_1, \dots, \vec{u}_p\}$ 是 $W$ 的**正交基**，那么 $\hat{y} = \frac{\vec{y} \cdot \vec{u}_1}{\vec{u}_1 \cdot \vec{u}_1}\vec{u}_1 + \frac{\vec{y} \cdot \vec{u}_2}{\vec{u}_2 \cdot \vec{u}_2}\vec{u}_2 + \dots + \frac{\vec{y} \cdot \vec{u}_p}{\vec{u}_p \cdot \vec{u}_p}\vec{u}_p$ 。
* [cite_start]$\vec{z} = \vec{y} - \hat{y}$ 。
* [cite_start]$\hat{y}$ 被称为 $\vec{y}$ 在 $W$ 上的正交投影 。

**正交投影的性质 (最佳逼近定理)**:
* [cite_start]$\vec{z}$ 的长度 $\|\vec{z}\|$ 是从 $\vec{y}$ 到 $W$ 的距离 。
* [cite_start]$\hat{y}$ 是 $W$ 中最接近 $\vec{y}$ 的点 。
* [cite_start]$\hat{y}$ 是 $\vec{y}$ 在 $W$ 中的最佳近似 。

---

### **8. Gram-Schmidt 过程**

**定理：Gram-Schmidt 过程**
[cite_start]给定 $\mathbb{R}^n$ 中非零子空间 $W$ 的一个基 $\{\vec{x}_1, \vec{x}_2, \dots, \vec{x}_p\}$ 。定义:
[cite_start]$\vec{v}_1 = \vec{x}_1$ 
[cite_start]$\vec{v}_2 = \vec{x}_2 - \frac{\vec{x}_2 \cdot \vec{v}_1}{\vec{v}_1 \cdot \vec{v}_1}\vec{v}_1$ 
[cite_start]$\vec{v}_3 = \vec{x}_3 - \frac{\vec{x}_3 \cdot \vec{v}_1}{\vec{v}_1 \cdot \vec{v}_1}\vec{v}_1 - \frac{\vec{x}_3 \cdot \vec{v}_2}{\vec{v}_2 \cdot \vec{v}_2}\vec{v}_2$ 
...
[cite_start]$\vec{v}_p = \vec{x}_p - \frac{\vec{x}_p \cdot \vec{v}_1}{\vec{v}_1 \cdot \vec{v}_1}\vec{v}_1 - \frac{\vec{x}_p \cdot \vec{v}_2}{\vec{v}_2 \cdot \vec{v}_2}\vec{v}_2 - \dots - \frac{\vec{x}_p \cdot \vec{v}_{p-1}}{\vec{v}_{p-1} \cdot \vec{v}_{p-1}}\vec{v}_{p-1}$ 

[cite_start]那么 $\{\vec{v}_1, \vec{v}_2, \dots, \vec{v}_p\}$ 是 $W$ 的一个**正交基** 。
[cite_start]此外，对于每个 $k$ (从 $1$ 到 $p$)，$\text{Span}\{\vec{v}_1, \dots, \vec{v}_k\} = \text{Span}\{\vec{x}_1, \dots, \vec{x}_k\}$ 。
（若要得到标准正交基，还需将每个 $\vec{v}_i$ 单位化。）

---

### **9. 二次型 (Quadratic Form)**

**定义：二次型**
[cite_start]在 $\mathbb{R}^n$ 上的一个二次型函数 $Q$ 可以通过一个形如 $Q(\vec{x}) = \vec{x}^T A \vec{x}$ 的表达式来计算，其中 $A$ 是一个 $n \times n$ 对称矩阵 。
[cite_start]矩阵 $A$ 被称为二次型的矩阵 。

**例子**:
对于 $Q(\vec{x}) = 5x_1^2 + 3x_2^2 + 2x_3^2 - x_1x_2 + 8x_2x_3$，其矩阵形式为 $\vec{x}^T A \vec{x}$，其中:
[cite_start]$A = \begin{pmatrix} 5 & -1/2 & 0 \\ -1/2 & 3 & 4 \\ 0 & 4 & 2 \\ \end{pmatrix}$ 。
[cite_start]（注意：交叉项 $x_ix_j$ 的系数要除以 2 填入 $A$ 的 $a_{ij}$ 和 $a_{ji}$ 位置 。）

**二次型的变量代换 (Change of Variable in a Quadratic Form)**
[cite_start]为了消除二次型中的交叉项，可以使用正交对角化 。
1. [cite_start]将二次型写成 $\vec{x}^T A \vec{x}$ 的形式，其中 $A$ 是对称矩阵 。
2. [cite_start]对 $A$ 进行正交对角化：$A = P D P^T$ 。
3. [cite_start]进行变量代换：令 $\vec{x} = P\vec{y}$ 。
4. [cite_start]由于 $P$ 是正交矩阵，所以 $P^T \vec{x} = \vec{y}$ 。
5. [cite_start]代入二次型：$\vec{x}^T A \vec{x} = (P\vec{y})^T A (P\vec{y}) = \vec{y}^T P^T A P \vec{y}$ 。
   [cite_start]由于 $P^T A P = D$，所以 $\vec{y}^T D \vec{y}$ 。
6. [cite_start]新的二次型形式为 $\lambda_1 y_1^2 + \lambda_2 y_2^2 + \dots + \lambda_n y_n^2$，其中 $\lambda_i$ 是 $A$ 的特征值 。
   [cite_start]这种形式消除了所有交叉项 。