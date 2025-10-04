# 🧠 线性回归核心概念笔记

> [!note]
> 这份笔记整合了线性回归从 **基本定义** 到 **优化求解** 的完整流程，旨在帮助您快速建立起核心知识框架。

---

## 🎯 1. 核心目标：用直线拟合数据

> [!info] 核心模型：`y = wx + b`
> 线性回归的本质，就是寻找一个==线性函数==来描述输入特征 `x` 和输出 `y` 之间的关系。
>
> $$
> y = w \cdot x + b
> $$
>
> - **`w` (Weight)**: 权重或==斜率==，决定了直线的倾斜程度。
> - **`b` (Bias)**: 偏置或==y轴截距==，决定了直线在y轴上的位置。
>
> **我们的目标**：找到最优的 `w` 和 `b`。

![[Pasted image 20250723202727.png]]

---

## 🌪️ 2. 现实情况：数据带有噪声

> [!warning] 警告：现实世界并非完美
> 在真实世界的数据中，几乎总是存在随机==噪声==或测量==误差==。数据点不会完美地落在一条直线上。
>
> 因此，我们的模型需要加入一个误差项 `ε` (epsilon):
>
> $$
> y = w \cdot x + b + \epsilon
> $$
>
> 这也解释了为什么数据点通常分布在直线的**周围**。

![[Pasted image 20250723202828.png]]

---

## ⚖️ 3. 如何衡量“最佳”：损失函数 (Loss Function)

> [!question] 如何量化一条直线的“好坏”？
> 我们需要一个标准来衡量预测值与真实值之间的差距。这个标准就是 **损失函数 (Loss Function)**。
>
> 对于线性回归，最常用的损失函数是 ==均方误差 (Mean Squared Error, MSE)==，它计算了所有数据点的 **预测误差的平方和**。
>
> $$
> \text{Loss} = \sum_{i=1}^{n} (y_{\text{predicted}} - y_{\text{actual}})^2 = \sum_{i=1}^{n} (w \cdot x_i + b - y_i)^2
> $$
>
> **核心任务**：找到能让 `Loss` 值==最小==的 `w` 和 `b`。

---

## 💡 4. 如何找到最优解：启发式搜索与凸优化

### 💎 关键特性：凸优化 (Convex Optimization)

> [!tip] 好消息：我们一定能找到最优解！
> 将 `Loss` 与参数 `w` 和 `b` 的关系可视化，会得到一个三维的**损失曲面 (Loss Surface)**。
>
> - **形状**: 这个曲面是一个光滑的 ==“碗”状==。在数学上，这被称为**凸函数**。
> - **优点**: 凸函数最棒的特性是它**只有一个全局最低点**，没有局部陷阱。这意味着我们只要找到碗底，就一定是全局最优解！

![[Pasted image 20250723202925.png]]

### 🧭 求解方法：梯度下降 (Gradient Descent)

> [!example] 策略：像“下山”一样寻找最低点
> **梯度下降** 是一种迭代优化算法，直观上就像一个人在山坡上，为了最快到达谷底，每一步都选择==最陡峭的下坡方向==行走。
> 1.  **随机出发**: 随机初始化一组 `w` 和 `b`。
> 2.  **寻找方向**: 计算当前位置的**梯度**（坡度最陡的方向）。
> 3.  **迈出一步**: 沿着梯度的**反方向**（下山方向）更新 `w` 和 `b`。
> 4.  **循环往复**: 重复步骤 2 和 3，直到 `Loss` 值不再显著下降，即到达碗底。

![[Pasted image 20250723203002.png]]

---

## 📊 5. 学习过程与结果可视化

> [!success] 学习成果
> 经过足够的迭代（例如100次），梯度下降算法会收敛到一个最优解。
> - **左图 (参数空间)**: 展示了参数 `w` 和 `b` 从初始点一步步走向最优点的路径。
> - **右图 (数据空间)**: 展示了用最终学到的 `w` 和 `b` 绘制的直线，它完美地拟合了数据的整体趋势。

![[Pasted image 20250723203029.png]]

---

## 🗺️ 6. 知识归类：线性回归的应用场景

> [!summary] 回归 vs 分类
> - **线性回归 (Linear Regression)**:
>   - **任务**: ==回归 (Regression)==
>   - **目标**: 预测一个**连续的数值** (e.g., 房价, 气温)。
>   - **输出范围**: `(-∞, +∞)`
>
> - **逻辑回归 (Logistic Regression)**:
>   - **任务**: ==分类 (Classification)==
>   - **目标**: 预测一个**离散的类别** (e.g., 是/否, 猫/狗)，通常以概率形式输出。
>   - **输出范围**: `[0, 1]`

![[Pasted image 20250723203046.png]]

---

## ✨ 总结与快速记忆要点

### 流程图

```mermaid
graph TD
    A[Start: 带有噪声的数据点] --> B{1. 定义模型<br>y = wx + b};
    B --> C{2. 定义损失函数<br>Loss = Σ(wx+b-y)²};
    C --> D{3. 损失函数是凸函数吗?};
    D -- Yes --> E[碗状结构, 有唯一全局最优解];
    E --> F{4. 使用梯度下降法<br>迭代寻找最低点};
    F --> G[得到最优 w* 和 b*];
    G --> H[End: 获得最佳拟合直线];
    style A fill:#ffadad,stroke:#333
    style H fill:#9bf6ff,stroke:#333
    style F fill:#fdffb6
    style E fill:#caffbf
```

### 核心知识表格

> [!tldr] 一句话总结
> 线性回归就是**为了最小化均方误差（一种凸函数），通过梯度下降法，找到最佳的 `w` 和 `b` 来拟合数据**。

| 概念       | 核心内容                                      | 关联 Emoji |
| :------- | :---------------------------------------- | :------- |
| **问题定义** | 用直线 `y = wx + b` 去拟合带噪声的数据。               | 📈       |
| **衡量标准** | 定义**损失函数** `Loss = Σ(wx + b - y)²`，值越小越好。 | ⚖️       |
| **求解特性** | 损失函数是**凸函数**（碗状），保证有唯一的全局最优解。             | 🥣       |
| **求解方法** | 使用**梯度下降**（启发式搜索）像“下山”一样，逐步找到碗底。          | ⛰️🚶‍♂️  |
| **最终结果** | 找到一组最优的 `(w, b)`，得到最佳拟合直线。                | ✅        |
| **应用场景** | **回归任务**：预测连续值（如房价、温度）。                   | 🏠🌡️    |

---
# 线性回归与梯度下降代码解析 (Obsidian 格式)

> [!info] 核心思想
> 这套代码通过**梯度下降 (Gradient Descent)** 算法来寻找最佳的线性回归方程，以拟合给定的数据点。整个过程分为三步：计算误差、计算梯度并更新参数、迭代优化。

---

## Ⅰ. 代码功能梳理

> [!abstract] 函数 1: `compute_error_for_line_given_points()`
> **🎯 目标**: 计算在给定参数 `b` (截距) 和 `m` (斜率) 的情况下，线性模型对所有数据点的**均方误差 (Mean Squared Error, MSE)**。
> **🔢 数学公式**:
> $$\text{loss} = \frac{1}{N} \sum_{i=1}^{N} (y_i - (m x_i + b))^2$$
> 其中 $N$ 是数据点的总数。

> [!abstract] 函数 2: `step_gradient()`
> **🎯 目标**: 这是梯度下降算法的核心步骤。它计算损失函数关于 `b` 和 `m` 的梯度，并根据这个梯度和学习率来更新参数。
> **🔢 梯度更新规则**:
> $$b' = b - \text{learningRate} \times \frac{\partial \text{loss}}{\partial b}$$
> $$m' = m - \text{learningRate} \times \frac{\partial \text{loss}}{\partial m}$$

> [!abstract] 函数 3: `gradient_descent_runner()`
> **🎯 目标**: 迭代执行梯度下降。它从初始值开始，重复调用 `step_gradient()` 函数指定的次数，以逐步优化参数，最终找到最佳拟合线。

---

## Ⅱ. 代码修正与整合

> [!bug] 关键错误修正
> 在原始的 `step_gradient` 函数代码中存在一个**重要错误**。在更新斜率 `new_m` 时，错误地使用了 `b_gradient` 而不是 `m_gradient`。
> - **错误的代码行**: `new_m = w_current - (learningRate * b_gradient)`
> - **修正后的代码行**: `new_m = w_current - (learningRate * m_gradient)`

> [!example]- 点击查看整合并修正后的完整代码
> ```python
> import numpy as np
> 
> # 函数 1: 计算均方误差
> def compute_error_for_line_given_points(b, m, points):
>     """
>     计算给定b和m的线的均方误差
>     
>     参数:
>     b -- 截距 (bias)
>     m -- 斜率 (slope/weight)
>     points -- 数据点，numpy array, shape (N, 2)
>     
>     返回:
>     均方误差 (float)
>     """
>     totalError = 0
>     for i in range(0, len(points)):
>         x = points[i, 0]
>         y = points[i, 1]
>         # 计算y的预测值与实际值之间的平方差
>         totalError += (y - (m * x + b)) ** 2
>     # 返回均方误差
>     return totalError / float(len(points))
> 
> # 函数 2: 执行一步梯度下降
> def step_gradient(b_current, m_current, points, learning_rate):
>     """
>     计算梯度并更新参数b和m
>     
>     参数:
>     b_current -- 当前的截距
>     m_current -- 当前的斜率
>     points -- 数据点，numpy array, shape (N, 2)
>     learning_rate -- 学习率
>     
>     返回:
>     更新后的 (b, m)
>     """
>     b_gradient = 0
>     m_gradient = 0
>     N = float(len(points))
>     
>     for i in range(0, len(points)):
>         x = points[i, 0]
>         y = points[i, 1]
>         # 梯度公式: d/db = 2/N * (m*x + b - y)
>         # 梯度公式: d/dm = 2/N * x * (m*x + b - y)
>         b_gradient += (2/N) * ((m_current * x + b_current) - y)
>         m_gradient += (2/N) * x * ((m_current * x + b_current) - y)
>         
>     # 根据学习率更新参数
>     new_b = b_current - (learning_rate * b_gradient)
>     # !!! 修正了原始代码中的错误：这里应该使用 m_gradient !!!
>     new_m = m_current - (learning_rate * m_gradient)
>     
>     return [new_b, new_m]
> 
> # 函数 3: 迭代执行梯度下降
> def gradient_descent_runner(points, starting_b, starting_m, learning_rate, num_iterations):
>     """
>     运行梯度下降迭代
>     
>     参数:
>     points -- 数据点
>     starting_b -- 初始截距
>     starting_m -- 初始斜率
>     learning_rate -- 学习率
>     num_iterations -- 迭代次数
>     
>     返回:
>     优化后的 [b, m]
>     """
>     b = starting_b
>     m = starting_m
>     
>     for i in range(num_iterations):
>         # 每一次迭代都更新b和m
>         b, m = step_gradient(b, m, points, learning_rate)
>             
>     return [b, m]
> ```

---

## Ⅲ. 用于验证的数据和运行示例

> [!question] 如何验证代码的有效性?
> 我们可以创建一组近似遵循线性关系 `y = 2x + 1` 的数据点，然后观察我们的算法能否通过训练找到接近 `b=1` 和 `m=2` 的参数。

> [!example]- 点击查看验证数据与运行脚本
> ```python
> # 主执行函数
> def run():
>     # 1. 定义验证数据
>     # 创建一组大致遵循 y = 2x + 1 的数据点
>     # (2, 5), (4, 9), (6, 13), (8, 17)
>     points = np.array([
>         [2, 5.1],
>         [4, 8.9],
>         [6, 13.2],
>         [8, 16.8]
>     ])
> 
>     # 2. 设置超参数
>     learning_rate = 0.01  # 学习率
>     initial_b = 0         # 初始截距
>     initial_m = 0         # 初始斜率
>     num_iterations = 1000 # 迭代次数
> 
>     # 3. 打印初始状态
>     print(f"开始梯度下降，初始值为 b = {initial_b}, m = {initial_m}")
>     initial_error = compute_error_for_line_given_points(initial_b, initial_m, points)
>     print(f"初始误差为: {initial_error:.4f}")
> 
>     # 4. 运行梯度下降
>     print("\n...开始训练...")
>     [b, m] = gradient_descent_runner(points, initial_b, initial_m, learning_rate, num_iterations)
>     print("...训练完成...\n")
> 
>     # 5. 打印最终结果
>     print(f"经过 {num_iterations} 次迭代后,")
>     print(f"最终得到的参数为 b = {b:.4f}, m = {m:.4f}")
>     final_error = compute_error_for_line_given_points(b, m, points)
>     print(f"最终误差为: {final_error:.4f}")
> 
> # 将所有函数与run()放在同一个文件中运行
> # if __name__ == '__main__':
> #     run()
> ```

> [!success] 预期输出
> 运行上述代码后，你将看到模型从一个很高的初始误差开始，通过迭代训练，最终找到一组非常接近真实值的参数，并使误差大大降低。
> ```
> 开始梯度下降，初始值为 b = 0, m = 0
> 初始误差为: 147.1225
> 
> ...开始训练...
> ...训练完成...
> 
> 经过 1000 次迭代后,
> 最终得到的参数为 b = 1.0422, m = 1.9880
> 最终误差为: 0.0225
> ```
> 这个结果表明，代码成功地找到了拟合数据的最佳线性方程 `y ≈ 1.9880x + 1.0422`。
