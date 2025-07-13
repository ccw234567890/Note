
#### 🎯 核心功能

当你循环时，需要同时得到**索引**和**元素值**。

---

#### 🛠️ 基础用法 (从 0 开始)

Python

```
my_list = ['a', 'b', 'c']

for index, value in enumerate(my_list):
    # index 会是 0, 1, 2
    # value 会是 'a', 'b', 'c'
    print(f"{index}: {value}")
```

**输出:**

```
0: a
1: b
2: c
```

---

#### ✨ 进阶用法 (自定义起始点)

使用 `start` 参数，让索引从 `1` 或任何你想要的数字开始。

Python

```
my_list = ['a', 'b', 'c']

for count, value in enumerate(my_list, start=1):
    # count 会是 1, 2, 3
    print(f"第 {count} 项: {value}")
```

**输出:**

```
第 1 项: a
第 2 项: b
第 3 项: c
```

---

#### ⚡ 高效用法 (与推导式结合)

快速创建“索引-值”对应的字典。

Python

```
my_list = ['a', 'b', 'c']

my_dict = {index: value for index, value in enumerate(my_list)}
# -> {0: 'a', 1: 'b', 2: 'c'}
```

---

#### 🤔 忘了为什么要用它？看这里！

|👎 **旧方法 (不推荐)**|👍 **`enumerate` (推荐)**|
|---|---|
|` python|`python|
|i = 0|my_list = ['a', 'b', 'c']|
|for item in my_list:||
|print(i, item)|for i, item in enumerate(my_list):|
|i += 1|print(i, item)|
|`|`|

**一句话总结：`for` 循环要索引，就用 `enumerate`。**