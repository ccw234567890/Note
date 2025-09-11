![](https://cc-407-1376569927.cos.ap-guangzhou.myqcloud.com/cc-407-1376569927/images-obsidian/202509111157950.png)
# 架构解析：DenseNet 的详细网络配置

**标签**: #DeepLearning #DenseNet #CNN #NetworkArchitecture #ImageNet

这张表格（表1）是 DenseNet 论文中用于 ImageNet 实验的四种不同深度模型的详细“施工图”。它清晰地展示了[[架构：DenseNet中的“密集块”与“过渡层”|“密集块” (Dense Block) 和“过渡层” (Transition Layer)]]是如何被组装成一个完整的、非常深的网络架构的。

---

## 1. 如何阅读此表格 - 表头与注释解析

在看具体结构前，先理解表头和表注的关键信息：

- **Columns (列)**:
    - `Layers`: 结构层的名称。
    - `Output Size`: 经过该层后，特征图的**空间尺寸（高度 x 宽度）**。
    - `DenseNet-121` 至 `DenseNet-264`: 四个具体的模型配置。表格单元格内的内容，描述了该模型在该结构层中的具体实现。

- **Key Information in Caption (表注关键信息)**:
    - **`growth rate (k) = 32`**: 这是整张表的“金科玉律”。对于这四个模型，**增长率 k 始终为 32**。这意味着，在密集块中，**每一个 `3x3 conv` 层都会新产生 32 个通道**的特征图。
    - **`BN-ReLU-Conv`**: 表格中写的每一个 `conv` 层，其**真实顺序**是 `批量归一化 (BN) -> ReLU激活 -> 卷积 (Conv)`。这是一种“预激活”（pre-activation）的形式，被证明效果很好。

---

## 2. 网络流程详解 (从上到下)

我们来追踪一下数据从输入到输出的完整旅程。

1.  **`Convolution` (初始卷积层)**
    - **操作**: `7 x 7 conv, stride 2`
    - **作用**: 这是一个标准的初始卷积层，用于对输入图像（通常是 224x224）进行初步的特征提取和下采样。步长为2，使得输出尺寸直接减半。
    - **`Output Size`**: `112 x 112`

2.  **`Pooling` (初始池化层)**
    - **操作**: `3 x 3 max pool, stride 2`
    - **作用**: 紧接着初始卷积，再次进行一次下采样，进一步缩小特征图尺寸，减少计算量。
    - **`Output Size`**: `56 x 56`

3.  **`Dense Block (1)` (第一个密集块)**
    - **`Output Size`**: `56 x 56` (在密集块内部，空间尺寸保持不变)。
    - **结构**: `[1x1 conv; 3x3 conv] x 6`
        - `[...]` 括号代表这是一个**[[Bottleneck Layer|瓶颈块]]**结构。数据先经过一个 `1x1` 卷积（降维），再经过一个 `3x3` 卷积（核心特征提取）。
        - `x 6`: 表示这个 `[1x1 -> 3x3]` 的瓶颈结构，被**重复了 6 次**。
    - **所有四个模型**在这个块中的结构都是一样的。

4.  **`Transition Layer (1)` (第一个过渡层)**
    - **作用**: 连接第一个和第二个密集块，并执行**下采样**。
    - **操作**: `1 x 1 conv` + `2 x 2 average pool, stride 2`。
        - `1x1 conv`: 用于[[原文 (Original): We adopt a standard data augmentation scheme (mirroring/shifting) that is widely used for these two datasets.|压缩]]通道数。
        - `2x2 pool`: 将空间尺寸减半。
    - **`Output Size`**: `28 x 28`

5.  **`Dense Block (2)` (第二个密集块)**
    - **`Output Size`**: `28 x 28`
    - **结构**: `[1x1 conv; 3x3 conv] x 12`
    - **所有四个模型**在这个块中都重复了 **12 次**瓶颈结构。

6.  **`Transition Layer (2)`**
    - **作用**: 再次下采样。
    - **`Output Size`**: `14 x 14`

7.  **`Dense Block (3)` (第三个密集块)**
    - **`Output Size`**: `14 x 14`
    - **结构**: `[1x1 conv; 3x3 conv] x N`
    - **区别开始出现**: 在这个最核心的块中，不同模型的**重复次数（深度）**开始不同：
        - `DenseNet-121`: 重复 **24** 次
        - `DenseNet-169`: 重复 **32** 次
        - `DenseNet-201`: 重复 **48** 次
        - `DenseNet-264`: 重复 **64** 次

8.  **`Transition Layer (3)`**
    - **作用**: 最后一次下采样。
    - **`Output Size`**: `7 x 7`

9.  **`Dense Block (4)` (第四个密集块)**
    - **`Output Size`**: `7 x 7`
    - **结构**: 不同模型再次展现出深度的差异：
        - `DenseNet-121`: 重复 **16** 次
        - `DenseNet-169`: 重复 **32** 次
        - `DenseNet-201`: 重复 **32** 次
        - `DenseNet-264`: 重复 **48** 次

10. **`Classification Layer` (分类层)**
    - **操作**: `7 x 7 global average pool` + `1000D fully-connected, softmax`
    - **作用**: 使用[[全局平均池化 (Global Average Pooling, GAP)]]将每个通道的 `7x7` 特征图转换为一个值，然后通过一个1000个神经元的全连接层，最终输出对应 ImageNet 1000个类别的概率。

---

## 3. 模型深度的计算

模型名称中的数字（如121）代表了**卷积层**和**全连接层**的总数。我们以 **`DenseNet-121`** 为例来验证：
- **初始卷积**: 1 层
- **Dense Block (1)**: `6 reps * 2 convs/rep` = 12 层
- **Transition Layer (1)**: `1 conv` = 1 层
- **Dense Block (2)**: `12 reps * 2 convs/rep` = 24 层
- **Transition Layer (2)**: `1 conv` = 1 层
- **Dense Block (3)**: `24 reps * 2 convs/rep` = 48 层
- **Transition Layer (3)**: `1 conv` = 1 层
- **Dense Block (4)**: `16 reps * 2 convs/rep` = 32 层
- **最终分类层**: `1` 个全连接层

**总层数**: `1 + 12 + 1 + 24 + 1 + 48 + 1 + 32 + 1 = 121` 层。
其他模型的深度也是同理计算得出。

### 总结
这张表格是 DenseNet 架构的“食谱”。它告诉我们，通过在一个标准化的“**初始层 → [密集块-过渡层]循环 → 分类层**”的框架下，仅需改变**密集块中瓶颈结构的重复次数**，就可以灵活地构建出不同深度和容量的 DenseNet 模型家族。