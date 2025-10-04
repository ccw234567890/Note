hello
# 具有重特征值的矩阵的正交特征向量

假设我们有以下矩阵 $A$：

$A = \begin{pmatrix} 2 & 1 & 1 \\ 1 & 2 & 1 \\ 1 & 1 & 2 \end{pmatrix}$

---

## **步骤 1：找到特征值**

首先，我们需要找到矩阵 $A$ 的特征值。我们计算 $det(A - \lambda I) = 0$：

$det \begin{pmatrix} 2-\lambda & 1 & 1 \\ 1 & 2-\lambda & 1 \\ 1 & 1 & 2-\lambda \end{pmatrix} = 0$

通过计算，我们会发现特征方程是 $(1-\lambda)^2 (4-\lambda) = 0$。

因此，我们的特征值是：
* $\lambda_1 = 1$ (重数是 2)
* $\lambda_2 = 4$ (重数是 1)

---

## **步骤 2：找到特征向量**

**对于 $\lambda_1 = 1$：**

我们需要解 $(A - 1I)v = 0$：

$\begin{pmatrix} 1 & 1 & 1 \\ 1 & 1 & 1 \\ 1 & 1 & 1 \end{pmatrix} \begin{pmatrix} x \\ y \\ z \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \\ 0 \end{pmatrix}$

这简化为方程 $x + y + z = 0$。这个方程有两个自由变量，所以它将产生两个线性无关的特征向量。

我们可以选择：
* $v_1 = \begin{pmatrix} -1 \\ 1 \\ 0 \end{pmatrix}$
* $v_2 = \begin{pmatrix} -1 \\ 0 \\ 1 \end{pmatrix}$

检查一下，$v_1$ 和 $v_2$ 是线性无关的，但它们不是正交的，因为 $v_1 \cdot v_2 = (-1)(-1) + (1)(0) + (0)(1) = 1 \neq 0$。

---

**对于 $\lambda_2 = 4$：**

我们需要解 $(A - 4I)v = 0$：

$\begin{pmatrix} -2 & 1 & 1 \\ 1 & -2 & 1 \\ 1 & 1 & -2 \end{pmatrix} \begin{pmatrix} x \\ y \\ z \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \\ 0 \end{pmatrix}$

通过行简化，我们会得到一个特征向量，例如：
* $v_3 = \begin{pmatrix} 1 \\ 1 \\ 1 \end{pmatrix}$

我们可以验证 $v_3$ 与 $v_1$ 和 $v_2$ 都是正交的 (例如 $v_1 \cdot v_3 = (-1)(1) + (1)(1) + (0)(1) = 0$)。

---

## **步骤 3：对重特征值对应的特征向量应用 Gram-Schmidt 过程**

由于 $v_1$ 和 $v_2$ 不是正交的，我们需要对它们应用 **Gram-Schmidt 过程**来得到正交的特征向量。

1.  **设 $u_1 = v_1$：**
    $u_1 = \begin{pmatrix} -1 \\ 1 \\ 0 \end{pmatrix}$

2.  **计算 $u_2$：**
    $u_2 = v_2 - \text{proj}_{u_1} v_2 = v_2 - \frac{v_2 \cdot u_1}{u_1 \cdot u_1} u_1$

    首先计算点积：
    $v_2 \cdot u_1 = (-1)(-1) + (0)(1) + (1)(0) = 1$
    $u_1 \cdot u_1 = (-1)^2 + (1)^2 + (0)^2 = 2$

    所以：
    $u_2 = \begin{pmatrix} -1 \\ 0 \\ 1 \end{pmatrix} - \frac{1}{2} \begin{pmatrix} -1 \\ 1 \\ 0 \end{pmatrix} = \begin{pmatrix} -1 - (-1/2) \\ 0 - 1/2 \\ 1 - 0 \end{pmatrix} = \begin{pmatrix} -1/2 \\ -1/2 \\ 1 \end{pmatrix}$

现在我们有了正交的特征向量集：
* $u_1 = \begin{pmatrix} -1 \\ 1 \\ 0 \end{pmatrix}$
* $u_2 = \begin{pmatrix} -1/2 \\ -1/2 \\ 1 \end{pmatrix}$
* $v_3 = \begin{pmatrix} 1 \\ 1 \\ 1 \end{pmatrix}$

我们可以将 $u_2$ 乘以 2，使其更易于处理，得到 $u_2' = \begin{pmatrix} -1 \\ -1 \\ 2 \end{pmatrix}$。它仍然是正交的。

---

## **步骤 4：标准化特征向量 (可选但通常建议)**

为了得到**标准正交基**，我们可以将每个特征向量单位化（除以其长度）：

* 对于 $u_1$: $\|u_1\| = \sqrt{(-1)^2 + 1^2 + 0^2} = \sqrt{2}$
    $e_1 = \frac{1}{\sqrt{2}} \begin{pmatrix} -1 \\ 1 \\ 0 \end{pmatrix}$

* 对于 $u_2'$: $\|u_2'\| = \sqrt{(-1)^2 + (-1)^2 + 2^2} = \sqrt{1+1+4} = \sqrt{6}$
    $e_2 = \frac{1}{\sqrt{6}} \begin{pmatrix} -1 \\ -1 \\ 2 \end{pmatrix}$

* 对于 $v_3$: $\|v_3\| = \sqrt{1^2 + 1^2 + 1^2} = \sqrt{3}$
    $e_3 = \frac{1}{\sqrt{3}} \begin{pmatrix} 1 \\ 1 \\ 1 \end{pmatrix}$

最终，我们就得到了三个相互正交且长度为 1 的特征向量 $e_1, e_2, e_3$。

---

## **总结：**

当一个特征值具有重数时，它可能对应多个线性无关的特征向量。这些特征向量不一定是正交的。**Gram-Schmidt 过程**允许我们从这些线性无关的特征向量中构建一个等价的**正交基**，这在许多应用中（例如，矩阵的对角化、谱分解）非常重要。