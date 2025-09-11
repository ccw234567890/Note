# 算法：费雪向量 (Fisher Vector, FV)

**标签**: #ComputerVision #ImageRetrieval #FeatureEncoding #Statistics

> [!info] 核心思想
> 费雪向量（FV）是一种极其强大的特征聚合方法。如果说 [[VLAD]] 描述了特征与聚类中心的“一阶”差异（均值偏差），那么 FV 则更进一步，它同时描述了特征分布的“一阶”和“二阶”统计信息（即**均值偏差**和**方差偏差**）。
>
> 我们可以用一个更生动的比喻来理解这三者的递进关系：
> - **[[Bag of Visual Words (BoVW)]]**: 像一个简单的**人口普查**，只统计每个地区（视觉词汇）有多少人（特征数量）。
> - **[[VLAD]]**: 像一次**社会调查**，不仅统计各地区人数，还调查每个地区居民的平均观点与该地区主流观点的**平均偏离程度**（一阶信息）。
> - **Fisher Vector**: 像一次**深度社会分析**，不仅调查平均偏离程度，还分析该地区居民观点的**多样性或一致性**（二阶信息，即方差）。
>
> FV 通过对一个预先训练好的概率模型（GMM）进行求导，来捕捉这种更丰富、更具判别力的信息。

---

## 1. 核心前提：高斯混合模型 (GMM)

要理解 FV，必须先理解高斯混合模型（Gaussian Mixture Model, GMM）。

- **GMM 是什么？**
    - 它是一个强大的概率密度模型，假设所有的数据点都是从 $K$ 个不同的高斯分布（正态分布）中混合生成的。
    - 任何一个数据点 $\mathbf{x}$ 的概率可以表示为这 $K$ 个高斯分布的加权和：
    $$ p(\mathbf{x} | \lambda) = \sum_{k=1}^{K} \pi_k \mathcal{N}(\mathbf{x} | \mu_k, \Sigma_k) $$
- **GMM 的参数 $\lambda$**:
    - **混合权重 $\pi_k$**: 第 $k$ 个高斯分布被选中的概率，且 $\sum_{k=1}^K \pi_k = 1$。
    - **均值 $\mu_k$**: 第 $k$ 个高斯分布的中心。
    - **协方差矩阵 $\Sigma_k$**: 第 $k$ 个高斯分布的形状和范围。为了简化，通常假设 $\Sigma_k$ 是对角矩阵，其对角线元素为方差 $\sigma_{k,j}^2$。

在 FV 中，我们首先在海量的特征描述子（如 SIFT）上训练一个 GMM，得到一组能够描述“通用视觉世界”的全局参数 $\lambda = \{\pi_k, \mu_k, \Sigma_k\}_{k=1}^K$。

---

## 2. Fisher Vector 的理论与推导

FV 的理论根基是 **Fisher Kernel**。其核心思想是：一个对象的特征向量，可以通过计算该对象对一个生成模型参数的**梯度**来得到。

这个梯度向量描述了**我们应该如何调整模型的参数，才能更好地描述当前这个对象（图像）**。这个“调整的方向和幅度”本身，就成了一种极具代表性的特征。

对于一张包含 $T$ 个局部特征 $X = \{\mathbf{x}_1, \dots, \mathbf{x}_T\}$ 的图像，其对 GMM 模型 $\lambda$ 的对数似然函数为：
$$ \mathcal{L}(X|\lambda) = \sum_{t=1}^{T} \log \left( \sum_{k=1}^{K} \pi_k \mathcal{N}(\mathbf{x}_t | \mu_k, \Sigma_k) \right) $$

**Fisher Vector 就是这个对数似然函数关于模型参数 $\lambda$ 的梯度**，并乘以一个特定的矩阵（Fisher Information Matrix 的逆的平方根）进行归一化。

$$ \mathcal{G}_{\lambda}^X = \frac{1}{T} \nabla_{\lambda} \mathcal{L}(X|\lambda) $$

我们主要关心对均值 $\mu_k$ 和标准差 $\sigma_k$ 的梯度（通常忽略权重 $\pi_k$ 的梯度）。

### 算法流程与公式

#### **第一步：软分配 (Soft Assignment)**

- 对于图像中的每一个特征 $\mathbf{x}_t$，计算它属于第 $k$ 个高斯分布的后验概率（也称为“软分配”或“责任”）。我们用 $\gamma_t(k)$ 表示：
$$ \gamma_t(k) = \frac{\pi_k \mathcal{N}(\mathbf{x}_t | \mu_k, \Sigma_k)}{\sum_{j=1}^{K} \pi_j \mathcal{N}(\mathbf{x}_t | \mu_j, \Sigma_j)} $$
- $\gamma_t(k)$ 表示特征 $\mathbf{x}_t$ 有多大的可能性是由第 $k$ 个高斯分布生成的。这与 VLAD 的“硬分配”（只选最近的）不同。

#### **第二步：计算梯度**

- **对均值 $\mu_k$ 的梯度（一阶统计量）**:
    - 它捕捉了所有特征在第 $k$ 个高斯分量上的**加权平均残差**。
    $$ \mathcal{G}_{\mu_k}^X = \frac{1}{T\sqrt{\pi_k}} \sum_{t=1}^{T} \gamma_t(k) \left( \frac{\mathbf{x}_t - \mu_k}{\sigma_k} \right) $$
    - 这个形式和 [[VLAD]] 非常相似，但权重从 0/1 的硬分配变成了 $\gamma_t(k)$ 的软分配，并且有归一化因子。

- **对标准差 $\sigma_k$ 的梯度（二阶统计量）**:
    - 它捕捉了特征在第 $k$ 个高斯分量上的**方差偏差信息**。
    $$ \mathcal{G}_{\sigma_k}^X = \frac{1}{T\sqrt{2\pi_k}} \sum_{t=1}^{T} \gamma_t(k) \left[ \frac{(\mathbf{x}_t - \mu_k)^2}{\sigma_k^2} - 1 \right] $$
    - 这是 VLAD 所不具备的，也是 FV 性能更强的关键所在。

#### **第三步：拼接 (Concatenation)**

- 将所有高斯分量的梯度向量拼接起来，形成最终的 Fisher Vector。
$$ FV = [\dots, (\mathcal{G}_{\mu_k}^X)^T, \dots, (\mathcal{G}_{\sigma_k}^X)^T, \dots]^T $$
- **维度**:
    - 假设特征维度为 $d$，GMM 有 $K$ 个分量。
    - 均值梯度的总维度是 $K \times d$。
    - 标准差梯度的总维度也是 $K \times d$。
    - 最终 FV 的维度是 $D_{FV} = 2Kd$，维度非常高。

#### **第四步：后处理 (Normalization)**

- 与 VLAD 类似，FV 同样需要进行**幂律归一化 (SSR)** 和 **L2 归一化**来提升性能。

---

## 3. 与 BoVW 和 VLAD 的关系

| 特征 | [[Bag of Visual Words (BoVW)]] | [[VLAD]] | Fisher Vector (FV) |
| :--- | :--- | :--- | :--- |
| **分配方式** | 硬分配 (Hard) | 硬分配 (Hard) | **软分配 (Soft)** |
| **统计阶数** | 0 阶 (计数) | 1 阶 (均值残差) | **1 阶 + 2 阶 (均值和方差残差)** |
| **理论基础** | 启发式 | 启发式 (可视为简化的 FV) | **统计理论 (Fisher Kernel)** |
| **性能** | 好 | 更好 | **最好** |
| **复杂度** | 低 | 中 | **高** |

---

## 4. 优缺点总结

### 优点
- **性能强大**: 在深度学习方法成熟前，是图像检索领域的顶尖方法。
- **理论完备**: 基于坚实的统计学基础（Fisher Kernel），模型解释性强。
- **信息丰富**: 同时编码了一阶和二阶统计信息，描述能力非常强。

### 缺点
- **维度极高**: $2Kd$ 的维度带来了巨大的存储和计算开销，降维（如 PCA）几乎是必须的。
- **计算复杂**: 涉及 GMM 训练、概率计算、梯度计算等，实现和计算都比 VLAD 复杂得多。
- **对 GMM 敏感**: GMM 的训练质量直接决定了 FV 的最终性能。