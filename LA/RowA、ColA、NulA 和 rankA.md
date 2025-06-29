### 1. RowA (行空间，Row Space of A)

* **是什么？**
    矩阵 $A$ 的行空间是由 $A$ 的行向量的所有线性组合构成的集合 。如果矩阵 $A$ 是 $m \times n$ 维的，其行向量在 $\mathbb{R}^n$ 中。行空间是 $\mathbb{R}^n$ 的一个子空间。
* **怎么求？**
    1.  将矩阵 $A$ 进行行化简，得到其阶梯形（Echelon Form）或简化阶梯形（Reduced Echelon Form）矩阵 $B$。
    2.  矩阵 $B$ 中所有的非零行向量构成 $A$ 的行空间的一个基 。
    3.  行空间的维数 (dim RowA) 等于矩阵的秩 (rank A) 。

### 2. ColA (列空间，Column Space of A)

* **是什么？**
    矩阵 $A$ 的列空间是由 $A$ 的列向量的所有线性组合构成的集合 。如果矩阵 $A$ 是 $m \times n$ 维的，其列向量在 $\mathbb{R}^m$ 中。列空间是 $\mathbb{R}^m$ 的一个子空间。矩阵方程 $Ax=b$ 有解当且仅当 $b$ 在 $A$ 的列空间中 。
* **怎么求？**
    1.  将矩阵 $A$ 进行行化简，得到其阶梯形矩阵 $B$。
    2.  找出矩阵 $B$ 中的主元（pivot）位置 。
    3.  回到原始矩阵 $A$，对应于 $B$ 中主元位置的列向量构成 $A$ 的列空间的一个基 。
    4.  列空间的维数 (dim ColA) 等于矩阵的秩 (rank A) 。

### 3. NulA (零空间，Null Space of A)

* **是什么？**
    矩阵 $A$ 的零空间是齐次线性方程 $Ax=0$ 的所有解的集合 。如果矩阵 $A$ 是 $m \times n$ 维的，零空间是 $\mathbb{R}^n$ 的一个子空间。
* **怎么求？**
    1.  将增广矩阵 $[A | 0]$ 进行行化简，得到其简化阶梯形矩阵 。
    2.  写出 $Ax=0$ 的通解，将基本变量（对应主元列的变量）用自由变量（对应非主元列的变量）表示 。
    3.  将通解写成参数向量形式，解向量可以表示为自由变量的线性组合。这些组成线性组合的向量构成 $A$ 的零空间的一个基 。
    4.  零空间的维数 (dim NulA) 等于 $Ax=0$ 中自由变量的个数 。

### 4. rankA (秩，Rank of A)

* **是什么？**
    矩阵 $A$ 的秩是其列空间（或行空间）的维数 。它表示矩阵的“有效”维度，即矩阵所能张成空间的维数。
* **怎么求？**
    1.  将矩阵 $A$ 进行行化简，得到其阶梯形矩阵 。
    2.  阶梯形矩阵中主元（pivot）位置的个数就是矩阵 $A$ 的秩 。
    3.  秩与零度定理 (Rank Theorem)：对于一个 $m \times n$ 维矩阵 $A$，有 $rank A + \text{dim Nul } A = n$ (列数) 。这个定理可以用于相互推导秩和零空间的维数。


矩阵的秩（rank A）与 RowA（行空间）和 ColA（列空间）的维数是相等的。

具体来说：
* 矩阵 $A$ 的秩 ($rank A$) 等于其列空间的维数 ($dim \text{Col}A$)。
* 矩阵 $A$ 的秩 ($rank A$) 也等于其行空间的维数 ($dim \text{Row}A$)。

这意味着 $rank A = dim \text{Col}A = dim \text{Row}A$。