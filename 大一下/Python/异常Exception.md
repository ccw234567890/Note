# 🐍 Python 常见内置异常 (Exception) 速查指南

> [!NOTE] 什么是异常 (Exception)？
> **异常**是在程序**运行时**发生的错误，它会中断程序的正常流程。Python 使用**异常对象**来表示这些错误。
> 
> > [!TIP] 如何应对？
> > 我们使用 `try...except` 语句块来“**捕获**”这些异常，这就像给我们的代码带上“安全帽”。当可能发生错误的代码块出现问题时，程序会跳转到 `except` 部分执行补救措施，而不是直接崩溃。

---

> [!example] 异常处理的完整结构：`try...except...else...finally`
> 
> 在深入了解各种异常前，先掌握这个强大的“四件套”结构。
> 
> ```python
> try:
>     # 1. 尝试执行的代码块
>     print("正在尝试打开文件...")
>     f = open('my_file.txt', 'r')
>     content = f.read()
> 
> except FileNotFoundError as e:
>     # 2. 如果 try 块中发生了 FileNotFoundError，执行这里的代码
>     print(f"捕获到错误：文件未找到！错误详情: {e}")
>     content = "默认内容"
> 
> except Exception as e:
>     # 捕获其他所有类型的异常，通常放在最后作为“兜底”
>     print(f"发生了其他未知错误！错误详情: {e}")
>     content = ""
> 
> else:
>     # 3. 如果 try 块中没有发生任何异常，执行这里的代码
>     print("文件读取成功，没有发生错误。")
>     print(f"文件内容是: {content}")
> 
> finally:
>     # 4. 无论是否发生异常，这里的代码最终总会被执行
>     # 通常用于释放资源，比如关闭文件
>     print("执行最终的清理工作...")
>     # if 'f' in locals() and not f.closed:
>     #     f.close()
> ```

---

### 常见的内置异常类型

## 📂 与文件和权限相关的错误

> [!abstract]- `FileNotFoundError` - 文件未找到错误
> 
> **🎯 发生原因**: 试图打开或操作一个不存在的文件。
> 
> **💻 失败示例**:
> ```python
> with open('non_existent_file.txt', 'r') as f:
>     content = f.read()
> # >> FileNotFoundError: [Errno 2] No such file or directory: 'non_existent_file.txt'
> ```
> 
> **⛑️ 处理方法**:
> ```python
> try:
>     with open('non_existent_file.txt', 'r') as f:
>         print(f.read())
> except FileNotFoundError:
>     print("处理：文件不存在，请检查路径或文件名。")
> ```

> [!abstract]- `PermissionError` - 权限错误
> 
> **🎯 发生原因**: 试图执行一个没有操作系统权限的操作，如读取受保护文件、向只读文件写入内容。
> 
> **💻 失败示例**:
> ```python
> # 假设 /root/secret.txt 是一个受保护的文件
> with open('/root/secret.txt', 'r') as f:
>     pass
> # >> PermissionError: [Errno 13] Permission denied: '/root/secret.txt'
> ```
> 
> **⛑️ 处理方法**:
> ```python
> try:
>     with open('read_only_file.txt', 'w') as f:
>         f.write("test")
> except PermissionError:
>     print("处理：权限不足，无法写入文件。")
> ```

## 🔢 与数据类型和值相关的错误

> [!failure]- `TypeError` - 类型错误
> 
> **🎯 发生原因**: 对不同或不兼容的类型进行了不支持的操作。
> 
> **💻 失败示例**:
> ```python
> result = 'hello' + 5
> # >> TypeError: can only concatenate str (not "int") to str
> ```
> 
> **⛑️ 处理方法**:
> ```python
> try:
>     result = 'hello' + 5
> except TypeError:
>     print("处理：字符串和数字不能直接相加，请检查数据类型。")
> ```

> [!failure]- `ValueError` - 值错误
> 
> **🎯 发生原因**: 参数的类型正确，但其**值**不合适或无法被正确处理。
> 
> **💻 失败示例**:
> ```python
> num = int('abc')
> # >> ValueError: invalid literal for int() with base 10: 'abc'
> ```
> 
> **⛑️ 处理方法**:
> ```python
> try:
>     num = int('abc')
> except ValueError:
>     print("处理：无法将'abc'转换成数字。")
> ```

> [!failure]- `AttributeError` - 属性错误
> 
> **🎯 发生原因**: 试图访问一个对象不存在的属性或方法。
> 
> **💻 失败示例**:
> ```python
> my_list = [1, 2, 3]
> my_list.push(4) # list没有push方法，应该是append
> # >> AttributeError: 'list' object has no attribute 'push'
> ```
> 
> **⛑️ 处理方法**:
> ```python
> try:
>     my_list.push(4)
> except AttributeError:
>     print("处理：该对象没有这个方法，你是不是想用 'append'？")
> ```

## ⛓️ 与数据集合（列表、字典）相关的错误

> [!bug]- `IndexError` - 索引错误
> 
> **🎯 发生原因**: 访问序列（如列表、元组）时，索引超出了范围（下标越界）。
> 
> **💻 失败示例**:
> ```python
> my_list = ['a', 'b']
> print(my_list[2]) # 只有索引0和1
> # >> IndexError: list index out of range
> ```
> 
> **⛑️ 处理方法**:
> ```python
> try:
>     print(my_list[2])
> except IndexError:
>     print("处理：索引超出列表范围！")
> ```

> [!bug]- `KeyError` - 键错误
> 
> **🎯 发生原因**: 访问字典时，使用了不存在的键 (key)。
> 
> **💻 失败示例**:
> ```python
> my_dict = {'name': 'Alice'}
> print(my_dict['age']) # 没有 'age' 这个键
> # >> KeyError: 'age'
> ```
> 
> **⛑️ 处理方法**:
> ```python
> try:
>     print(my_dict['age'])
> except KeyError:
>     print("处理：字典中不存在这个键。")
> 
> # 更好的方式是使用 .get() 方法
> age = my_dict.get('age', '未知') # 如果键不存在，返回默认值'未知'
> print(f"年龄是: {age}")
> ```

## ➗ 与变量名和逻辑相关的错误

> [!warning]- `NameError` - 名称错误
> 
> **🎯 发生原因**: 使用了一个从未被定义（赋值）过的变量名。
> 
> **💻 失败示例**:
> ```python
> print(undefined_variable)
> # >> NameError: name 'undefined_variable' is not defined
> ```
> 
> **⛑️ 处理方法**:
> 这通常是代码逻辑错误，应在编码时修复，确保变量先定义后使用，一般不建议用`try...except`来“掩盖”这个问题。

> [!warning]- `ZeroDivisionError` - 除零错误
> 
> **🎯 发生原因**: 在数学运算中，除数是零。
> 
> **💻 失败示例**:
> ```python
> result = 10 / 0
> # >> ZeroDivisionError: division by zero
> ```
> 
> **⛑️ 处理方法**:
> ```python
> try:
>     result = 10 / 0
> except ZeroDivisionError:
>     print("处理：数学上除数不能为零！")
> ```

---

> [!summary] 速查总表
| 异常名称 | 中文名 | 发生原因 | 一句话例子 |
| :--- | :--- | :--- | :--- |
| `TypeError` | 类型错误 | 对不同类型进行不支持的操作 | `'hello' + 5` |
| `ValueError` | 值错误 | 值的格式无法被函数处理 | `int('abc')` |
| `AttributeError`| 属性错误 | 对象没有这个属性或方法 | `[].bad_method()` |
| `IndexError` | 索引错误 | 列表/元组的索引超出范围 | `my_list[99]` |
| `KeyError` | 键错误 | 访问字典中不存在的键 | `my_dict['bad_key']`|
| `NameError` | 名称错误 | 使用了未定义的变量 | `print(undefined_var)` |
| `ZeroDivisionError`| 除零错误 | 除数是零 | `10 / 0` |
| `FileNotFoundError`| 文件未找到 | 试图打开不存在的文件 | `open('no_file.txt')`|
| `PermissionError`| 权限错误 | 没有权限读写文件/目录 | 写入只读文件 |