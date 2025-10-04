# 🐍 Python `time` 模块核心函数速查

> [!NOTE] 使用前必读：三种时间表示形式
> 要想掌握`time`模块，必须先理解它处理时间的三种“格式”。所有核心函数基本都是在这三者之间进行转换。
> 
> > [!tip] 1. 时间戳 (Timestamp)
> > - **格式**: 一个浮点数，如 `1720971000.123`
> > - **含义**: 从1970年1月1日至今的总**秒数**。
> > - **特点**: **计算机友好**，便于计算和存储。
> 
> > [!info] 2. 时间元组 (struct_time)
> > - **格式**: 一个包含9个元素的元组对象，如 `time.struct_time(tm_year=2025, ...)`
> > - **含义**: 将时间分解为年、月、日、时、分、秒等独立部分。
> > - **特点**: **程序员友好**，便于访问时间的特定部分（如年份、小时）。
> 
> > [!success] 3. 格式化时间字符串 (Formatted String)
> > - **格式**: 人类可读的字符串，如 `"2025-07-14 12:30:00"`
> > - **含义**: 用于显示给用户或从用户输入中解析。
> > - **特点**: **用户友好**，可读性最强。
> 
> > [!quote] 核心转换流程图
> > 时间戳 `--- localtime() --->` 时间元组 `--- strftime() --->` 字符串
> > 字符串 `--- strptime() --->` 时间元组 `--- mktime() --->` 时间戳

---

> [!example]- `time()` - 获取当前时间戳
> 
> **🎯 输入与输出**
> - **输入**: 无
> - **输出**: **时间戳** (浮点数)
> 
> **💻 代码示例**
> ```python
> import time
> 
> # 获取当前的时间戳
> current_timestamp = time.time()
> print(f"当前的时间戳是: {current_timestamp}")
> # 输出: 当前的时间戳是: 1720971047.1234567
> ```

---

> [!tip]- `localtime(sec)` - 时间戳转时间元组
> 
> **🎯 输入与输出**
> - **输入**: **时间戳** (可选，省略则为当前时间)
> - **输出**: **时间元组** (`struct_time`)
> 
> **💻 代码示例**
> ```python
> import time
> 
> local_time_struct = time.localtime() 
> print(f"当前时间元组: {local_time_struct}")
> 
> # 可以方便地访问任意部分
> print(f"今年是: {local_time_struct.tm_year} 年")
> print(f"现在是: {local_time_struct.tm_hour} 点")
> ```

---

> [!info]- `ctime(sec)` - 时间戳转标准字符串
> 
> **🎯 输入与输出**
> - **输入**: **时间戳** (可选，省略则为当前时间)
> - **输出**: **格式固定的时间字符串**
> - **💡 关键点**: 一个快捷函数，但格式无法自定义。
> 
> **💻 代码示例**
> ```python
> import time
> 
> # 获取当前时间的易读字符串
> current_time_str = time.ctime()
> print(f"当前时间的易读字符串是: {current_time_str}")
> # 输出: Mon Jul 14 08:30:47 2025
> ```

---

> [!success]- `strftime(format, t)` - 时间元组转自定义字符串
> 
> **🎯 输入与输出**
> - **输入**: `format` (格式字符串), `t` (**时间元组**)
> - **输出**: **自定义格式的时间字符串**
> - **💡 关键点**: **str**ing **f**ormat **time**，最强大的格式化工具。
> 
> **💻 代码示例**
> ```python
> import time
> 
> now_struct = time.localtime()
> formatted_str = time.strftime("%Y年%m月%d日 %H:%M:%S", now_struct)
> print(f"自定义格式化后的时间: {formatted_str}")
> # 输出: 自定义格式化后的时间: 2025年07月14日 08:30:47
> ```
> > [!faq] 常用格式代码
> > - `%Y`: 四位年份 (2025)
> > - `%y`: 两位年份 (25)
> > - `%m`: 月份 (01-12)
> > - `%d`: 日期 (01-31)
> > - `%H`: 24小时制 (00-23)
> > - `%I`: 12小时制 (01-12)
> > - `%M`: 分钟 (00-59)
> > - `%S`: 秒 (00-59)
> > - `%A`: 完整星期名 (Monday)
> > - `%a`: 星期名缩写 (Mon)

---

> [!bug]- `strptime(string, format)` - 字符串转时间元组
> 
> **🎯 输入与输出**
> - **输入**: `string` (时间字符串), `format` (对应的格式)
> - **输出**: **时间元组** (`struct_time`)
> - **💡 关键点**: **str**ing **p**arse **time**，`strftime` 的逆操作。
> 
> > [!danger] ‼️ 注意
> > `format` 参数必须与输入的 `string` **格式完全一致**，否则会报错！
> 
> **💻 代码示例**
> ```python
> import time
> 
> time_string = "2025-07-14 21:00:00"
> format_pattern = "%Y-%m-%d %H:%M:%S"
> 
> parsed_struct = time.strptime(time_string, format_pattern)
> print(f"从字符串解析出的时间元组: {parsed_struct}")
> print(f"解析出的年份是: {parsed_struct.tm_year}")
> ```

---

> [!warning]- `sleep(sec)` - 程序休眠
> 
> **🎯 输入与输出**
> - **输入**: `sec` (要休眠的秒数，可为小数)
> - **输出**: 无
> - **💡 关键点**: 这是一个**命令**，不是格式转换。它会**阻塞**程序，让程序暂停执行。
> 
> **💻 代码示例**
> ```python
> import time
> 
> print("开始倒计时...")
> time.sleep(1)
> print("3")
> time.sleep(1)
> print("2")
> time.sleep(1)
> print("1")
> print("发射！🚀")
> ```