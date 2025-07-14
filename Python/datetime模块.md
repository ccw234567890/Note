# 🐍 Python `datetime` 模块核心类速查

> [!NOTE] 模块简介
> `datetime` 模块是 Python 中处理日期和时间的**主力军**。相比于 `time` 模块，它提供了更面向对象、更直观的工具，尤其在**日期计算**方面极为强大。
> **使用前，请务必在文件顶部 `import datetime`**。

---

> [!example]- `datetime.datetime` - 日期时间的“完全体”
> 
> **🎯 核心理解**
> - 这是最常用的类，代表一个**精确到微秒的特定时间点**，包含年月日时分秒等所有信息。
> 
> **🛠️ 如何创建**
> - `datetime.datetime.now()`: 获取本地当前日期和时间。
> - `datetime.datetime(年, 月, 日, 时, 分, 秒)`: 创建一个指定的日期时间。
> 
> **💻 代码示例**
> ```python
> import datetime
> 
> # 获取当前完整时间
> now = datetime.datetime.now()
> print(f"当前完整时间: {now}")
> 
> # 访问对象的属性
> print(f"当前年份: {now.year}, 当前小时: {now.hour}")
> 
> # 使用 strftime() 方法进行格式化
> print(f"格式化输出: {now.strftime('%Y-%m-%d %H:%M')}")
> ```

---

> [!abstract]- `datetime.date` - 只关心“日期”
> 
> **🎯 核心理解**
> - 一个只表示**日期**（年月日）的对象，不包含时分秒信息。非常适合处理生日、纪念日等场景。
> 
> **🛠️ 如何创建**
> - `datetime.date.today()`: 获取今天的日期。
> - `datetime.date(年, 月, 日)`: 创建一个指定的日期。
> 
> **💻 代码示例**
> ```python
> import datetime
> 
> today = datetime.date.today()
> print(f"今天的日期是: {today}")
> 
> new_year_day = datetime.date(2026, 1, 1)
> print(f"2026年的元旦是: {new_year_day}")
> ```

---

> [!tip]- `datetime.time` - 只关心“时间”
> 
> **🎯 核心理解**
> - 一个只表示**当天内时间**（时分秒）的对象，不包含年月日信息。非常适合处理闹钟、日程时间等场景。
> 
> **🛠️ 如何创建**
> - `datetime.time(时, 分, 秒, 微秒)`: 创建一个指定的时间。
> 
> **💻 代码示例**
> ```python
> import datetime
> 
> # 设置一个上午9:30的会议时间
> meeting_time = datetime.time(9, 30)
> print(f"会议时间是: {meeting_time}")
> print(f"会议小时: {meeting_time.hour}")
> ```

---

> [!success]- `datetime.timedelta` - 时间计算的“魔法棒”
> 
> **🎯 核心理解**
> - 它不代表一个时间点，而是代表一个**时间段**或**时间差**，是进行日期时间加减运算的**唯一工具**。
> 
> **🛠️ 如何创建**
> - `datetime.timedelta(days=, hours=, minutes=, seconds=, weeks=)`
> 
> **💻 代码示例 (最强大的功能！)**
> ```python
> import datetime
> 
> now = datetime.datetime.now()
> print(f"现在: {now.strftime('%Y-%m-%d %H:%M')}")
> 
> # 1. 日期加减：计算100天后的日期
> delta_100_days = datetime.timedelta(days=100)
> future_date = now + delta_100_days
> print(f"100天后: {future_date.strftime('%Y-%m-%d %H:%M')}")
> 
> # 2. 日期相减：计算两个日期相差多久
> independence_day = datetime.datetime(2025, 7, 4)
> time_diff = now - independence_day
> print(f"今天距离2025年7月4日已经过去了 {time_diff.days} 天")
> ```

---

> [!warning]- `datetime.tzinfo` - 处理“时区”（进阶）
> 
> **🎯 核心理解**
> - 这是一个与**时区信息**相关的抽象基类。
> - `datetime` 对象默认是“天真”的（naive, 不带时区），`tzinfo` 可以让它变得“感知”（aware），从而能正确处理不同时区的时间转换。
> 
> > [!INFO] 实用建议
> > 直接操作 `tzinfo` 比较复杂。在实际项目中，如果需要处理时区，强烈建议使用更方便的第三方库，如 `pytz` 或 `dateutil`。

---

> [!summary] 一图流总结
> - `datetime.datetime`: **全能选手** (年月日时分秒)
> - `datetime.date`: **日期专家** (年月日)
> - `datetime.time`: **时间专家** (时分秒)
> - `datetime.timedelta`: **计算利器** (一个时间段，用于加减)
> - `datetime.tzinfo`: **时区专家** (高级，通常用第三方库代替)