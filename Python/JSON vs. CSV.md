# 📊 数据格式双雄：JSON vs. CSV

> [!TIP] 核心印象
> - **<span style="color:#0984e3;">JSON</span>** 就像一份详尽的、有层级的**个人档案** (Key-Value)。
> - **<span style="color:#27ae60;">CSV</span>** 就像一张简洁明了的**电子表格** (Row-Column)。

---

## <span style="color:#0984e3;">① JSON (JavaScript Object Notation) - 详细的档案</span>

> [!QUOTE] 定义
> **JSON** 是一种轻量级的数据交换格式，它使用**人类可读的文本**来表示**键值对 (Key-Value)** 形式的数据。尽管源于 JavaScript，但它是一种独立于语言的通用格式。

### <span style="color:#74b9ff;">核心结构</span>
- **对象 (Object)**: 使用花括号 `{}` 包裹的一系列无序的键值对。
- **数组 (Array)**: 使用方括号 `[]` 包裹的一系列有序的值。
- **键 (Key)**: 必须是<span style="color:#e17055;">**字符串**</span>，用双引号 `""` 包裹。
- **值 (Value)**: 可以是<span style="color:#e84393;">字符串, 数字, 布尔值 (`true`/`false`), 数组, 或另一个对象</span>。

### <span style="color:#74b9ff;">示例：一组用户信息</span>
这展示了 JSON 如何轻松表示**层级关系**（`address` 是一个嵌套对象）和**列表**（`skills` 是一个数组）。

```json
[
  {
    "id": 101,
    "name": "爱丽丝",
    "email": "alice@example.com",
    "isPremium": true,
    "address": {
      "city": "北京",
      "street": "科技路1号"
    },
    "skills": ["Python", "Web开发"]
  },
  {
    "id": 102,
    "name": "鲍勃",
    "email": "bob@example.com",
    "isPremium": false,
    "address": {
      "city": "上海",
      "street": "创新道22号"
    },
    "skills": ["平面设计", "UI/UX"]
  }
]
```

### <span style="color:#74b9ff;">优缺点</span>
- 👍 **优点**:
  - **结构清晰**: 能够完美表示复杂的**层级**和**嵌套**数据。
  - **可读性强**: 对人类非常友好，易于理解。
  - **数据类型支持**: 原生支持<span style="color:#e84393;">字符串、数字、布尔值、数组</span>等多种类型。
  - **通用性**: 是现代 Web API 数据交换的**事实标准**。

- 👎 **缺点**:
  - **冗余信息**: 语法（引号、括号）比 CSV 多，文件体积通常更大。
---
# 🐍 Python `json` 模块核心函数解析

> [!TIP] 核心记忆技巧：关键看末尾的 "s"
> - `dump` & `load` ➡️ 操作**文件 (File)** 读写。
> - `dump**s**` & `load**s**` ➡️ 操作**字符串 (String)** 转换，`s` 代表 `String`。

---

## <span style="color:#a29bfe;">第一类：在内存中操作字符串 (String)</span>

### <span style="color:#74b9ff;">1. `json.dumps()` - 将 Python 对象编码为 JSON 字符串</span>

> [!NOTE] 定义
> 将一个 <span style="color:#fd79a8;">Python 对象</span> (如 `dict`, `list`) **编码 (Encode)** 成一个 <span style="color:#55efc4;">JSON 格式的字符串</span>。这个过程也叫**序列化 (Serialization)**。

#### <span style="color:#81ecec;">代码示例</span>
```python
import json

# 准备一个 Python 字典对象
python_dict = {
    "name": "卡片笔记",
    "version": 1.2,
    "tags": ["知识管理", "Obsidian"],
    "is_active": True
}

# 使用 dumps() 将字典转换为 JSON 字符串
# indent=4 让输出的字符串有4个空格的缩进，更美观
# ensure_ascii=False 保证中文字符能正常显示
json_string = json.dumps(python_dict, indent=4, ensure_ascii=False)

# 打印转换后的字符串
print("--- 转换后的 JSON 字符串 ---")
print(json_string)
print("\n字符串的类型是:", type(json_string))
```
- **输出结果**：一个格式化的字符串，可以被发送到网络或存储在任何文本字段中。

---

### <span style="color:#74b9ff;">2. `json.loads()` - 将 JSON 字符串解码为 Python 对象</span>
> [!NOTE] 定义
> 将一个 <span style="color:#55efc4;">JSON 格式的字符串</span> **解码 (Decode)** 成一个 <span style="color:#fd79a8;">Python 对象</span> (通常是 `dict` 或 `list`)。这个过程也叫**反序列化 (Deserialization)**。

#### <span style="color:#81ecec;">代码示例</span>
```python
import json

# 这是一个从 API 或其他地方获取的 JSON 字符串
json_string_from_api = """
{
    "name": "卡片笔记",
    "version": 1.2,
    "tags": [
        "知识管理",
        "Obsidian"
    ],
    "is_active": true
}
"""

# 使用 loads() 将字符串转换回 Python 字典
python_object_restored = json.loads(json_string_from_api)

# 打印恢复后的 Python 对象
print("--- 恢复后的 Python 字典 ---")
print(python_object_restored)
print("\n对象的类型是:", type(python_object_restored))

# 可以像操作普通字典一样访问数据
print("笔记的标签:", python_object_restored['tags'])
```

---

## <span style="color:#a29bfe;">第二类：直接操作文件 (File)</span>

### <span style="color:#74b9ff;">3. `json.dump()` - 将 Python 对象写入 JSON 文件</span>
> [!NOTE] 定义
> 功能与 `dumps()` 类似，但它不返回字符串，而是直接将**编码后的结果**写入到一个**文件对象 (file object)** 中。

#### <span style="color:#81ecec;">代码示例</span>
```python
import json

# 准备一个 Python 字典对象
python_dict_to_save = {
    "name": "项目配置",
    "author": "张三",
    "settings": {
        "theme": "dark",
        "autosave": True
    }
}

# 使用 'w' (写入模式) 打开一个文件
# with 语句能确保文件操作后自动关闭
with open('config.json', 'w', encoding='utf-8') as file:
    # 直接将字典 python_dict_to_save 写入到 file 文件中
    json.dump(python_dict_to_save, file, indent=4, ensure_ascii=False)

print("数据已成功写入 config.json 文件！")
```
- **操作结果**：项目目录下会生成一个名为 `config.json` 的文件，内容是格式化的 JSON。

---

### <span style="color:#74b9ff;">4. `json.load()` - 从 JSON 文件中读取并解码为 Python 对象</span>
> [!NOTE] 定义
> 功能与 `loads()` 类似，但它不是从字符串读取，而是直接从一个**文件对象 (file object)** 中读取数据并**解码**。

#### <span style="color:#81ecec;">代码示例</span>
```python
import json

# 假设 config.json 文件已存在
# 使用 'r' (读取模式) 打开文件
with open('config.json', 'r', encoding='utf-8') as file:
    # 从 file 文件中读取数据并自动转换成 Python 字典
    loaded_config = json.load(file)

print("--- 从文件读取并恢复的 Python 字典 ---")
print(loaded_config)
print("\n配置的类型是:", type(loaded_config))

# 同样可以轻松访问数据
print("当前主题设置:", loaded_config['settings']['theme'])
```

---

## <span style="color:#ff7675;">🧠 总结与对比</span>

| 函数名称 | 输入 (Input) | 输出 (Output) | 场景 | 记忆技巧 (Mnemonic) |
| :--- | :--- | :--- | :--- | :--- |
| <span style="color:#74b9ff;">`json.dump**s**(obj)`</span> | <span style="color:#fd79a8;">Python 对象</span> | <span style="color:#55efc4;">JSON 字符串</span> | 网络传输, 存入数据库文本字段 | `s` = **S**tring |
| <span style="color:#74b9ff;">`json.load**s**(s)`</span> | <span style="color:#55efc4;">JSON 字符串</span> | <span style="color:#fd79a8;">Python 对象</span> | 解析 API 返回的文本数据 | `s` = **S**tring |
| <span style="color:#74b9ff;">`json.dump(obj, file)`</span> | <span style="color:#fd79a8;">Python 对象</span> + `file` | <span style="color:#ffeaa7;">写入文件</span> | 生成 `.json` 配置文件 | `dump` 到文件里 |
| <span style="color:#74b9ff;">`json.load(file)`</span> | `file` | <span style="color:#fd79a8;">Python 对象</span> | 读取本地 `.json` 配置文件 | `load` from 文件 |

---

## <span style="color:#27ae60;">② CSV (Comma-Separated Values) - 简洁的表格</span>

> [!QUOTE] 定义
> **CSV** 是一种非常简单的文本格式，用**逗号**作为分隔符，将数据组织成**表格**形式（行和列）。任何电子表格软件（如 Excel, Google Sheets）都能轻松打开和处理它。

### <span style="color:#55efc4;">核心结构</span>
- **行 (Row)**: 每一行代表一条记录，以换行符分隔。
- **列 (Column)**: 每一行中的数据由逗号 `,` 分隔成不同的字段。
- **表头 (Header)**: 通常文件的**第一行**用作表头，定义每一列的名称。

### <span style="color:#55efc4;">示例：同样的一组用户信息</span>
与 JSON 不同，CSV 无法直接表示层级关系。`address` 被拆分成了两列。`skills` 也很难表示，通常会用另一种分隔符（如分号 `;`）放在一个单元格里。

```csv
id,name,email,isPremium,city,street,skills
101,爱丽丝,alice@example.com,true,北京,科技路1号,"Python;Web开发"
102,鲍勃,bob@example.com,false,上海,创新道22号,"平面设计;UI/UX"
```
*注意：当数据本身包含逗号时，通常会用双引号 `""` 将该字段包起来。*

### <span style="color:#55efc4a;">优缺点</span>
- 👍 **优点**:
  - **极其紧凑**: 语法简单，没有冗余字符，文件体积小。
  - **非常直观**: 对于表格数据来说，一目了然。
  - **兼容性极佳**: 几乎所有数据分析和电子表格工具都原生支持。
  - **易于生成和解析**: 处理简单，速度快。

- 👎 **缺点**:
  - **无数据类型**: 所有数据本质上都是**字符串**，需要程序自己去转换（`"true"` vs. `true`）。
  - **无层级结构**: 难以表示嵌套数据，所有数据都是扁平的。
  - **标准不统一**: 对于逗号、引号、换行符的处理，存在不同的方言。

---

## <span style="color:#d63031;">⚔️ JSON vs. CSV: 一图流对比</span>

| 特性 (Feature) | <span style="color:#0984e3;">JSON</span> | <span style="color:#27ae60;">CSV</span> |
| :--- | :--- | :--- |
| **结构 (Structure)** | **层级式 (Key-Value)** | **表格 (行/列)** |
| **数据类型** | ✅ **原生支持** (数字, 布尔值等) | ❌ **不支持** (全是字符串) |
| **人类可读性** | **非常高** (结构清晰) | **高** (对于简单表格) |
| **文件大小** | **较大** (语法冗余) | **非常小** (紧凑) |
| **复杂数据** | ✅ **非常适合** (嵌套、数组) | ❌ **不适合** (扁平化) |
| **最佳应用场景** | **Web APIs, 配置文件, NoSQL数据库** | **Excel数据导入/导出, 数据分析, 机器学习数据集** |

> [!SUCCESS] 总结
> - 当你需要传输**结构复杂**的数据，或者在**Web应用**之间通信时，选择 **JSON**。
> - 当你需要处理**大量表格数据**，或者需要与 **Excel** 等工具交互时，选择 **CSV**。