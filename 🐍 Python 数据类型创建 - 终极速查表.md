

#python #cheatsheet #syntax

> [!tip] 目标
> 
> 当你忘记具体语法时，此笔记让你在5秒内找到答案，无需阅读长篇大论。

---

### 🛍️ 列表 `List` - `[ ]`

**特点**：有序、可变、可重复。

Python

```
# 空列表
my_list = []

# 带元素的列表
my_list = [1, "hello", True]

# 从可迭代对象创建 (例如 range 或字符串)
my_list = list(range(5))  # -> [0, 1, 2, 3, 4]
my_list = list("abc")     # -> ['a', 'b', 'c']

# 列表推导式 (最常用)
squares = [x**2 for x in range(5)] # -> [0, 1, 4, 9, 16]
```

---

### 💎 元组 `Tuple` - `( )`

**特点**：有序、**不可变**、可重复。

Python

```
# 空元组
my_tuple = ()

# 带元素的元组
my_tuple = (1, "hello", True)

# 省略括号 (元组打包)
my_tuple = 1, "hello", True

# !!!【重点】单元素元组，必须有逗号
single_tuple = (1,)  # 正确
wrong_tuple = (1)    # 错误, 这是一个整数

# 从可迭代对象创建
my_tuple = tuple([1, 2, 3]) # -> (1, 2, 3)
```

---

### 📚 字典 `Dict` - `{key: value}`

**特点**：键值对、键唯一、可变。

Python

```
# 空字典
my_dict = {}

# 带元素的字典
my_dict = {"name": "Alice", "age": 25}

# 使用 dict() 构造函数
my_dict = dict(name="Bob", age=30)

# 从键列表创建 (值默认为 None)
my_dict = dict.fromkeys(['a', 'b', 'c']) # -> {'a': None, 'b': None, 'c': None}

# 从键列表创建 (指定默认值)
my_dict = dict.fromkeys(['a', 'b', 'c'], 0) # -> {'a': 0, 'b': 0, 'c': 0}

# 字典推导式 (最常用)
squares_dict = {x: x**2 for x in range(3)} # -> {0: 0, 1: 1, 2: 4}
```

---

### 🎟️ 集合 `Set` - `{ }` 或 `set()`

**特点**：无序、**元素唯一**、可变。

Python

```
# !!!【重点】空集合，必须用 set()
empty_set = set()
wrong_empty = {}  # 错误, 这是空字典

# 带元素的集合 (自动去重)
my_set = {1, 2, "hello", 2} # -> {1, 2, 'hello'}

# 从可迭代对象创建 (常用于去重)
unique_numbers = set([1, 2, 3, 2, 1]) # -> {1, 2, 3}

# 集合推导式
squares_set = {x**2 for x in [1, 2, 1, 3]} # -> {1, 4, 9}
```