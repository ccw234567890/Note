# 算法：VLAD (Vector of Locally Aggregated Descriptors)

**标签**: #ComputerVision #ImageRetrieval #FeatureEncoding

> [!info] 核心思想
> VLAD 是一种用于图像检索任务的、高效的特征聚合方法。它被设计为 [[Bag of Visual Words (BoVW)]] 模型的升级版。
> 
> 如果说 BoVW 模型像一个简单的投票系统，只统计每种“视觉词汇”在图像中出现了多少次；那么 VLAD 则更进一步，它不仅关心某个特征属于哪个“视觉词汇”，更关心这个特征与它所属的“视觉词汇”中心**有多大的差异**。
>
> VLAD 通过累加这些**差异（残差）**，来更精细地描述图像内容，从而获得远超 BoVW 的检索精度。

---

## 1. VLAD 与 BoVW 的对比

- **[[Bag of Visual Words (BoVW)]]**:
    - **过程**: 将图像中的每个局部特征（如 SIFT）分配给最近的视觉词汇（码本中心），然后统计每个视觉词汇的出现频率，形成一个直方图。
    - **缺点**: 只记录了词汇的**数量**信息，丢失了大量关于特征本身分布的细节信息。

- **VLAD**:
    - **过程**: 将图像中的每个局部特征分配给最近的视觉词汇，然后计算每个特征与其对应词汇中心之间的**残差向量（Residual Vector）**。最后，将属于同一个视觉词汇的所有残差向量**累加**起来。
    - **优点**: 不仅编码了特征的数量信息，还编码了特征相对于其聚类中心的**分布信息**，描述能力更强。

---

## 2. 算法流程与公式推导

VLAD 的构建过程可以分为以下几个步骤：

### A. 前期准备

1.  **提取局部特征**:
    - 对于一张图像，首先使用 SIFT、SURF 或其他特征提取器，提取出 $N$ 个 $d$ 维的局部特征描述子。
    - 我们将这些描述子表示为集合: $X = \{\mathbf{x}_1, \mathbf{x}_2, \dots, \mathbf{x}_N\}$, 其中每个 $\mathbf{x}_n \in \mathbb{R}^d$。

2.  **构建视觉码本 (Codebook)**:
    - 使用大量的特征描述子（从一个大的训练数据集中提取），通过 [[K-Means]] 等聚类算法进行聚类。
    - 最终得到 $K$ 个聚类中心，这些中心构成了我们的“视觉码本”。
    - 我们将码本表示为集合: $C = \{\mathbf{c}_1, \mathbf{c}_2, \dots, \mathbf{c}_K\}$, 其中每个 $\mathbf{c}_k \in \mathbb{R}^d$。

### B. 核心：VLAD 聚合过程

对于一张给定的图像（包含 $N$ 个特征 $X = \{\mathbf{x}_n\}$），其 VLAD 向量的计算如下：

#### **第一步：分配 (Assignment)**
- 对于图像中的每一个特征描述子 $\mathbf{x}_n$，找到码本 $C$ 中与它**距离最近**的那个聚类中心 $\mathbf{c}_k$。
- 这个过程可以用一个最近邻函数来表示：$NN(\mathbf{x}_n) = \mathbf{c}_k$。

#### **第二步：计算并累加残差 (Accumulation of Residuals)**
- 这是 VLAD 最核心的一步。
- 我们需要为码本中的**每一个**聚类中心 $\mathbf{c}_k$ 计算一个累加向量 $\mathbf{v}_k$。
- $\mathbf{v}_k$ 的计算方法是：将所有被分配到 $\mathbf{c}_k$ 的特征 $\mathbf{x}_n$ 与 $\mathbf{c}_k$ 本身的**差值（残差）**全部加起来。

**公式推导**:
$$
\mathbf{v}_k = \sum_{\{\mathbf{x}_n | NN(\mathbf{x}_n) = \mathbf{c}_k\}} (\mathbf{x}_n - \mathbf{c}_k)
$$
- **解释**:
    - 求和符号的下标 $\{\mathbf{x}_n | NN(\mathbf{x}_n) = \mathbf{c}_k\}$ 表示“遍历所有最近邻是 $\mathbf{c}_k$ 的那些特征 $\mathbf{x}_n$”。
    - $(\mathbf{x}_n - \mathbf{c}_k)$ 就是残差向量，它描述了特征 $\mathbf{x}_n$ 相对于其“视觉原型”$\mathbf{c}_k$ 的偏离方向和程度。
    - 如果没有任何特征被分配给中心 $\mathbf{c}_k$，那么对应的 $\mathbf{v}_k$ 就是一个零向量。

#### **第三步：拼接 (Concatenation)**
- 将前面计算出的 $K$ 个 $d$ 维的累加向量 $\mathbf{v}_1, \mathbf{v}_2, \dots, \mathbf{v}_K$ 按顺序拼接起来，形成一个巨大的向量。这个向量就是最终的 VLAD 描述子。

**公式**:
$$
V = [\mathbf{v}_1^T, \mathbf{v}_2^T, \dots, \mathbf{v}_K^T]^T
$$
- **维度**: 
    - 每个 $\mathbf{v}_k$ 的维度是 $d$。
    - 共有 $K$ 个这样的向量。
    - 因此，最终的 VLAD 向量 $V$ 的维度是 $D_{VLAD} = K \times d$。
    - 这是一个非常高的维度（例如，K=64, SIFT维度d=128，则 $D_{VLAD}=8192$），通常需要使用 [[PCA]] 等降维技术进行压缩。

### C. 后处理：归一化 (Normalization)

原始的 VLAD 向量存在“突发性”（burstiness）问题，即少数几个视觉词汇主导了整个向量的模长。为了使其更适合进行相似度比较，必须进行严格的归一化。

1.  **幂律归一化 (Power-Law Normalization)**:
    - 也称为 **符号开方 (Signed Square Rooting, SSR)**。对向量 $V$ 的每一个元素 $v_i$ 进行操作：
    $$
    v_i \leftarrow \text{sign}(v_i)\sqrt{|v_i|}
    $$
    - 这可以有效抑制那些值过大的元素，缓解突发性问题。

2.  **L2 归一化 (L2 Normalization)**:
    - 将经过 SSR 处理后的整个向量 $V$ 进行 L2 归一化，使其模长为 1。
    $$
    V \leftarrow \frac{V}{\|V\|_2}
    $$
    - 归一化后的向量非常适合使用欧氏距离或点积来进行高效的相似度计算。

---

## 3. 优缺点总结

### 优点
- **高判别力**: 相比 BoVW，VLAD 编码了特征的分布信息，检索性能显著提升。
- **概念清晰**: 是对 BoVW 的一个直观且有效的改进。
- **紧凑性 (降维后)**: 尽管原始维度很高，但通过 PCA 降维后可以得到一个非常紧凑且高效的图像表示。

### 缺点
- **高维度**: 原始 VLAD 维度非常高 ($K \times d$)，导致存储和计算成本巨大，通常必须配合降维。
- **对码本敏感**: K-Means 聚类结果的好坏直接影响 VLAD 的性能。
- **计算复杂度**: 相比 BoVW，计算残差和累加的过程更为复杂。

---
## 关联概念
- [[Bag of Visual Words (BoVW)]]
- [[Fisher Vector (FV)]] (VLAD 的进一步推广)
- [[SIFT]]
- [[K-Means]]
- [[PCA]]