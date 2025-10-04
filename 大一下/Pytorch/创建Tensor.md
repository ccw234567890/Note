> [!abstract] PyTorch Tensor 创建方法核心笔记 📖
> 本笔记汇总了 PyTorch 中创建 Tensor (张量) 的所有核心方法。Tensor 是 PyTorch 的基础，掌握这些创建技巧是高效学习和应用 PyTorch 的关键。

> [!note] 1. 从现有数据创建 (Create from Existing Data)
> 这是最基础和直接的创建方式，可以将 Python 列表或 NumPy 数组等已有数据直接转换为 Tensor。
> 
> ---
> 
> #### **从 Python 列表 (List) 创建**
> 使用 `torch.tensor()` 函数，PyTorch 会自动推断数据类型。
> ```python
> # 从一维列表创建
> torch.tensor([2., 3.2])
> # >> tensor([2.0000, 3.2000])
> 
> # 从二维列表创建
> torch.tensor([[2., 3.2], [1., 22.3]])
> # >> tensor([[ 2.0000,  3.2000], [ 1.0000, 22.3000]])
> ```
> 
> #### **从 NumPy 数组 (Array) 创建**
> 使用 `torch.from_numpy()` 函数，它会继承 NumPy 数组的数据类型。
> > [!danger] 核心注意：共享内存
> > 通过 `from_numpy()` 创建的 Tensor 与原始的 NumPy 数组 **共享内存**。这意味着修改其中一个，另一个也会随之改变！
> ```python
> import numpy as np
> 
> a = np.array([2, 3.3])
> t = torch.from_numpy(a)
> # >> tensor([2.0000, 3.3000], dtype=torch.float64)
> ```

> [!success] 2. 创建特定值的张量 (Tensors with Specific Values)
> 用于创建具有特定形状和固定值的 Tensor，非常适合用于初始化权重、标签或掩码。
> 
> ---
> 
> - **`torch.ones(*size)`**: 创建全为 **1** 的 Tensor。
> - **`torch.zeros(*size)`**: 创建全为 **0** 的 Tensor。
> - **`torch.full(size, value)`**: 创建一个用指定 `value` 填充的 Tensor。
> - **`torch.eye(n)`**: 创建一个 **单位矩阵** (对角线为1，其余为0)。
> - **`..._like(input)`**: 例如 `torch.ones_like(a)`，可以快速创建一个与 `a` 形状相同的新 Tensor。
> 
> ```python
> # 2x3 且填充值为 7 的张量
> torch.full((2, 3), 7)
> # >> tensor([[7., 7., 7.],
> #           [7., 7., 7.]])
> 
> # 3x3 的单位矩阵
> torch.eye(3)
> # >> tensor([[1., 0., 0.],
> #           [0., 1., 0.],
> #           [0., 0., 1.]])
> ```

> [!tip] 3. 创建序列张量 (Tensors with Sequences)
> 用于生成有规律的数值序列，在数据可视化和生成坐标时非常有用。
> 
> ---
> 
> - **`torch.arange(start, end, step)`**: 在 `[start, end)` 半开区间内，按 `step` 生成等差序列。
> - **`torch.linspace(start, end, steps)`**: 在 `[start, end]` 闭区间内，生成 `steps` 个**线性等分**的点。
> - **`torch.logspace(start, end, steps)`**: 在 $[10^{start}, 10^{end}]$ 区间内，生成 `steps` 个**对数等分**的点。
> 
> ```python
> # 在 [0, 10] 区间内生成 5 个线性等分的点
> torch.linspace(0, 10, steps=5)
> # >> tensor([ 0.0000,  2.5000,  5.0000,  7.5000, 10.0000])
> ```

> [!example] 4. 创建随机值的张量 (Random Tensors)
> 随机数在机器学习中至关重要，例如用于初始化模型参数、数据增强或创建随机掩码。
> 
> ---
> 
> #### **均匀分布**
> - **`torch.rand(*size)`**: `[0, 1)` 区间的均匀分布。
> - **`torch.randint(low, high, size)`**: `[low, high)` 区间的随机整数。
> 
> #### **正态分布 (高斯分布)**
> - **`torch.randn(*size)`**: **标准正态分布** ($N(0, 1)$)。
> - **`torch.normal(mean, std)`**: 指定均值和标准差的正态分布。
> 
> #### **随机排序**
> - **`torch.randperm(n)`**: 生成一个 0 到 `n-1` 的随机整数排列，常用于打乱数据集索引。
> 
> ```python
> # 3x3 的标准正态分布张量
> torch.randn(3, 3)
> 
> # 用 randperm 打乱 tensor 的行顺序
> a = torch.tensor([[1,1],[2,2],[3,3]])
> idx = torch.randperm(3) # e.g., tensor([2, 0, 1])
> a[idx] 
> # >> tensor([[3, 3], [1, 1], [2, 2]])
> ```

> [!caution] 5. 创建未初始化的张量 (Uninitialized Tensors)
> 为了极致性能，可以只分配内存而不初始化。这在需要覆盖所有元素时可以节省时间。
> 
> ---
> 
> - **`torch.empty(*size)`**: 创建一个未初始化的张量，其值是内存中残留的“垃圾值”。
> 
> > [!warning] 核心区别：`Tensor()` vs `tensor()`
> > - `torch.Tensor(2, 3)` (大写T): 创建一个 **2x3 的未初始化** 张量。
> > - `torch.tensor([2, 3])` (小写t): 创建一个 **包含 `[2, 3]` 两个元素** 的已初始化张量。

> [!info] 6. 设置默认数据类型 (Default Data Type)
> 可以全局更改创建浮点数 Tensor 时的默认类型（默认为 32位 `float`）。
> 
> ---
> 
> - **`torch.set_default_tensor_type(t)`**: 设置默认的浮点张量类型。
> 
> ```python
> # 默认是 FloatTensor (float32)
> torch.tensor([1.2, 3]).type()
> # >> 'torch.FloatTensor'
> 
> # 将默认类型改为 DoubleTensor (float64)
> torch.set_default_tensor_type(torch.DoubleTensor)
> 
> # 再次创建，默认类型已改变
> torch.tensor([1.2, 3]).type()
> # >> 'torch.DoubleTensor'
> ```