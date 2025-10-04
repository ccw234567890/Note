# 🐍 Python `random` 模块核心函数速查

> [!NOTE] 模块简介
> `random` 模块是 Python 的标准库，专门用于生成伪随机数，可用于游戏、模拟、抽样等多种场景。
> **使用前，请务必在文件顶部 `import random`**。

---

> [!abstract]- `seed(x)` - 设定随机数种子
> 
> **🎯 核心理解**
> - 设定随机数算法的“**起点**”或“**种子**”。
> - 计算机的随机数是“伪随机”，由一个确定的算法从种子开始计算。
> - **用途**: 如果你需要可复现的随机结果（例如科学实验或调试代码），请使用相同的种子。如果省略，Python会使用当前时间等不可预测的值作为种子。
> 
> **💻 代码示例**
> ```python
> import random
> 
> random.seed(42) # 设定种子为42
> print(random.random()) # 输出: 0.6394...
> print(random.randint(1, 10)) # 输出: 2
> 
> random.seed(42) # 重新设定相同的种子
> print(random.random()) # 输出: 0.6394... (和上面完全一样)
> print(random.randint(1, 10)) # 输出: 2 (和上面完全一样)
> ```

---

> [!example]- `random()` - 生成0到1的随机小数
> 
> **🎯 核心理解**
> - 生成一个 `[0.0, 1.0)` 范围内的随机**浮点数（小数）**。
> - 结果包含 `0.0`，但**不包含** `1.0`。
> 
> **💻 代码示例**
> ```python
> import random
> 
> # 生成一个基础的随机小数
> value = random.random()
> print(f"一个0到1的随机小数: {value}")
> ```

---

> [!tip]- `randint(a, b)` - 生成范围内的随机整数
> 
> **🎯 核心理解**
> - 生成一个 `[a, b]` 范围内的随机**整数**。
> - **关键点**: 这是一个**闭区间**，意味着结果**包含** `a` 和 `b`。
> - **最佳比喻**: 模拟扔一个从 `a` 点到 `b` 点的骰子。
> 
> **💻 代码示例**
> ```python
> import random
> 
> # 模拟扔一个1到6点的骰子
> dice_roll = random.randint(1, 6)
> print(f"扔出的骰子点数是: {dice_roll}")
> ```

---

> [!question]- `randrange(m, n, k)` - 按步长生成随机整数
> 
> **🎯 核心理解**
> - 从 `range(m, n, k)` 所代表的序列中，随机选择一个整数。
> - `m`: 起始值（包含）。
> - `n`: 结束值（**不包含**）。
> - `k`: 步长（默认为1）。
> 
> > [!INFO] `randint` vs `randrange`
> > `random.randint(a, b)` 等价于 `random.randrange(a, b + 1)`。
> 
> **💻 代码示例**
> ```python
> import random
> 
> # 从 [10, 12, 14, ..., 98, 100] 中随机选一个偶数
> even_num = random.randrange(10, 101, 2)
> print(f"10到100之间的一个随机偶数: {even_num}")
> ```

---

> [!example]- `uniform(a, b)` - 生成范围内的随机小数
> 
> **🎯 核心理解**
> - `randint()` 的**浮点数版本**。
> - 生成一个 `[a, b]` 范围内的随机**浮点数（小数）**。通常 `a` 和 `b` 都有可能被取到。
> 
> **💻 代码示例**
> ```python
> import random
> 
> # 随机生成一个体温
> temperature = random.uniform(36.5, 37.5)
> print(f"随机生成的体温是: {temperature:.2f}℃")
> ```

---

> [!success]- `choice(seq)` - 随机选择一个元素
> 
> **🎯 核心理解**
> - 从一个**序列（sequence）**中随机抽取一个元素。
> - 这个序列可以是**列表 (list)**、**元组 (tuple)** 或**字符串 (string)**。
> 
> **💻 代码示例**
> ```python
> import random
> 
> winners = ['爱丽丝', '鲍勃', '查理']
> lucky_one = random.choice(winners)
> print(f"恭喜中奖者: {lucky_one}!")
> 
> random_char = random.choice("Python")
> print(f"随机抽取的字母是: {random_char}")
> ```

---

> [!warning]- `shuffle(seq)` - 原地打乱序列
> 
> **🎯 核心理解**
> - 将一个序列（通常是列表）中的元素**原地**随机打乱。
> 
> > [!danger] ‼️ 最重要的警告
> > - **原地 (in-place)**: 这个函数会**直接修改你传入的原始列表**！
> > - **返回值为 `None`**: 这个函数**没有返回值**！
> > - **常见错误**: `new_list = random.shuffle(my_list)` 是**错误**的，`new_list` 会变成 `None`。
> 
> **💻 代码示例**
> ```python
> import random
> 
> cards = ['A', 'K', 'Q', 'J', '10']
> print(f"洗牌前: {cards}")
> 
> # 直接在原列表上操作，不需要赋值
> random.shuffle(cards) 
> 
> print(f"洗牌后: {cards}")
> ```