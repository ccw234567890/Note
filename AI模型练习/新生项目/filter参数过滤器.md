
# 解析：“参数过滤器”的模拟流程

**标签**: #DeepLearning #Optimizer #FineTuning #MindSpore #Python

> [!quote] 您的原始分析
> `opt = Momentum(filter(lambda x: x.requires_grad, head_net.get_parameters()), …)`
> 这一小段其实做了两件事：
> 1. 用 `head_net.get_parameters()` 拿到分类头里所有 `Parameter` 对象
> 2. 用 Python 内置 `filter()`＋lambda 把 `requires_grad=False` 的剔除，只留下需要更新梯度的参数
> ... (完整分析)

---

## 1. 我们的目标
我们将模拟一个包含了**“冻结的”Backbone** 和 **“待训练的”Head Net** 的完整模型。然后，我们将像 `filter` 函数一样，对模型中所有的参数（表现为矩阵和向量）进行一次“安检”，看看最终哪些参数会被送进优化器。

## 2. 模拟开始：构建一个虚拟模型
在 MindSpore/PyTorch 中，每个权重和偏置都是一个 `Parameter` 对象，它既包含数据（矩阵/向量），也包含一个 `requires_grad` 布尔标记。我们就来手动创建这么一个虚拟的模型参数列表。

#### A. “冻结的” Backbone 参数
这些参数已经被预训练好，我们在微调（fine-tuning）时**不希望**更新它们。
```python
import numpy as np

# 模拟 Backbone 中的一个卷积层的权重和偏置
backbone_conv1_w = {
    "name": "backbone.conv1.weight",
    "data": np.random.rand(64, 3, 3, 3), # 形状为 [64, 3, 3, 3] 的权重矩阵
    "requires_grad": False  # <-- 关键点：被冻结
}
backbone_conv1_b = {
    "name": "backbone.conv1.bias",
    "data": np.zeros(64), # 形状为 [64] 的偏置向量
    "requires_grad": False # <-- 关键点：被冻结
}
````

#### B. “待训练的” Head Net 参数

这是我们新建的分类头，它的参数需要从零开始学习。

Python

```
# 模拟分类头的全连接层的权重和偏置 (使用我们熟悉的 4x2 矩阵)
head_dense_w = {
    "name": "head.dense.weight",
    "data": np.array([[10,2], [10,1], [-8,9], [1,10]], dtype=np.float32),
    "requires_grad": True # <-- 关键点：需要训练
}
head_dense_b = {
    "name": "head.dense.bias",
    "data": np.array([0.5, 0.5], dtype=np.float32), # 形状为 [2] 的偏置向量
    "requires_grad": True # <-- 关键点：需要训练
}
```

#### C. 获取整个模型的“参数列表”

在实际代码中，`head_net.get_parameters()` 只会获取头部的参数。为了模拟 `filter` 的筛选能力，我们假设有一个能获取模型**所有**参数的列表 `all_model_params`。

Python

```
all_model_params = [
    backbone_conv1_w,
    backbone_conv1_b,
    head_dense_w,
    head_dense_b
]
```

---

## 3. 执行过滤流程：模拟 `filter()` 的“安检”

现在，我们来手动执行 `filter(lambda x: x.requires_grad, all_model_params)` 这个操作。

Python

```
# 这是 filter 函数在内部做的事情
trainable_params = []
print("开始筛选需要训练的参数...")

for p in all_model_params:
    # lambda x: x.requires_grad 检查的就是这个布尔值
    is_trainable = p["requires_grad"]

    print(f"检查参数: {p['name']:<25} | requires_grad? -> {is_trainable}")

    if is_trainable:
        trainable_params.append(p)
        print(f"  └─ PASSED! 已加入待训练列表。")
    else:
        print(f"  └─ SKIPPED! 已被冻结。")

print("\n筛选完成！")
```

**模拟运行的输出**:

```
开始筛选需要训练的参数...
检查参数: backbone.conv1.weight    | requires_grad? -> False
  └─ SKIPPED! 已被冻结。
检查参数: backbone.conv1.bias     | requires_grad? -> False
  └─ SKIPPED! 已被冻结。
检查参数: head.dense.weight       | requires_grad? -> True
  └─ PASSED! 已加入待训练列表。
检查参数: head.dense.bias         | requires_grad? -> True
  └─ PASSED! 已加入待训练列表。

筛选完成！
```

---

## 4. 最终递交给优化器

经过“安检”后，最终被送到 `Momentum` 优化器的，只有通过了筛选的 `trainable_params` 列表。

**过滤后的列表 `trainable_params` 内容**:

Python

```
[
    {'name': 'head.dense.weight', 'data': array(...), 'requires_grad': True},
    {'name': 'head.dense.bias', 'data': array(...), 'requires_grad': True}
]
```

**最终的调用**:

Python

```
# 优化器只拿到了需要训练的 head_dense_w 和 head_dense_b
opt = Momentum(trainable_params, ...)
```

结论:

当后续的训练循环调用 opt.step() 时，优化器只会看到并更新 head_dense_w 和 head_dense_b 这两个参数的矩阵/向量数据。Backbone 的参数矩阵 backbone_conv1_w 和 backbone_conv1_b 从始至终都没有进入优化器的管辖范围，因此它们的值在整个微调过程中都保持不变，完美地实现了**“冻结主干，仅训头部”**的目标。

这个 `filter` 操作，就是连接“模型参数定义”和“优化器更新”之间的、一个至关重要且设计优雅的**“看门人”**。