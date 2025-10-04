# 🔐 Web Agent 安全攻击文献清单

**整理日期**: 2025-10-04  
**领域**: Web Agent Jailbreak & Security Attacks  
**筛选标准**: 2024年最新 + 高引用/高影响力

---

## 🌟 核心必读（Top 3）

### 1️⃣ WIPI: A New Web Threat for LLM-Driven Web Agents ⭐⭐⭐

**📅 发表时间**: 2024年2月  
**👥 作者**: Fangzhou Wu, Shutong Wu, Yulong Cao, Chaowei Xiao  
**🔗 链接**: https://arxiv.org/abs/2402.16965

**📝 核心贡献**:
- 提出**WIPI攻击**：通过在公开网页中嵌入恶意指令，间接控制Web Agent
- **攻击成功率**: 纯黑盒环境下超过**90%**
- **鲁棒性强**: 对不同用户前缀指令保持高成功率

**🎯 为什么必读**:
- ✅ 直接针对Web Agent的攻击
- ✅ 真实Web环境（网页内容注入）
- ✅ 高成功率，证明威胁性强
- ✅ 与您会议讨论的"Web内容误导Agent"高度相关

**💡 可复用点**:
- 网页内容注入的攻击模板
- 黑盒攻击策略
- 评测方法设计

---

### 2️⃣ AdvWeb: Controllable Black-box Attacks against VLM-powered Web Agents ⭐⭐⭐

**📅 发表时间**: 2024年10月  
**👥 作者**: Chejian Xu, Mintong Kang, Jiawei Zhang, Zeyi Liao, Lingbo Mo, Mengqi Yuan, Huan Sun, Bo Li  
**🔗 链接**: https://arxiv.org/abs/2410.17401

**📝 核心贡献**:
- 提出**AdvWeb框架**：针对VLM驱动Web Agent的黑盒攻击
- **训练对抗性提示模型**，自动生成恶意网页内容
- **可控攻击目标**：不当股票购买、错误银行交易等
- **隐蔽性强**：不改变网页外观

**🎯 为什么必读**:
- ✅ 最新研究（2024年10月）
- ✅ 针对**VLM-powered Agent**（多模态）
- ✅ 自动化攻击框架（可复现）
- ✅ 真实应用场景（金融、电商）

**💡 可复用点**:
- 对抗性提示模型训练方法
- VLM Agent攻击策略
- 隐蔽攻击设计思路

**🔥 与多语言攻击的结合点**:
```
AdvWeb的对抗性提示 + 低资源语言 = 更强攻击？
- 在网页中嵌入多语言恶意指令
- 降低检测系统识别率
- 提高攻击成功率
```

---

### 3️⃣ WASP: A Web Agent Safety Benchmark for Prompt Injection Attacks ⭐⭐⭐

**📅 发表时间**: 2024年  
**👥 作者**: Ivan Evtimov, Arman Zharmagambetov, Aaron Grattafiori, Chuan Guo, Kamalika Chaudhuri  
**🔗 链接**: https://arxiv.org/abs/2504.18575 *(注：此arXiv编号可能有误，请以实际为准)*

**📝 核心贡献**:
- 构建**WASP基准测试**，评估Web Agent安全性
- 系统性评测**提示注入攻击**
- 发现：即使先进模型也易受**低成本人为攻击**
- 强调需要更强的防御机制

**🎯 为什么必读**:
- ✅ **Benchmark**（可用于评测您的攻击方法）
- ✅ 提供baseline和评测标准
- ✅ 分析了现有防御的不足
- ✅ 为研究提供对比基准

**💡 可复用点**:
- 评测框架设计
- 攻击成功的定义标准
- 现有防御的weakness分析

---

## 📚 扩展阅读（相关领域）

### 4️⃣ Hide Your Malicious Goal Into Benign Narratives

**📅 发表时间**: 2024年8月  
**👥 作者**: 未列出  
**🔗 链接**: https://arxiv.org/abs/2408.11182

**📝 核心思想**:
- 将被禁止的查询嵌入到"**载体文章**"中
- 黑盒越狱方法
- 平均成功率**63%**

**🎯 可借鉴点**:
- 隐藏恶意意图的技巧
- 语义相关性利用
- 可用于Web页面内容设计

---

### 5️⃣ JailExpert: Building on Previous Attack Experience

**📅 发表时间**: 2024年  
**👥 作者**: 未列出  
**🔗 链接**: https://arxiv.org/abs/2508.19292 *(注：arXiv编号格式可能需要验证)*

**📝 核心思想**:
- 利用**先前攻击经验**自动化越狱
- 形式化表示经验结构
- 基于语义漂移分组经验

**🎯 可借鉴点**:
- 迭代优化攻击策略
- 经验复用框架
- 自动化攻击生成

---

## 🔍 搜索关键词推荐

如果您想深入搜索更多文献，建议使用以下关键词：

### 核心关键词
```
Primary:
- "web agent security"
- "web agent attack"
- "prompt injection" + "agent"
- "indirect prompt injection"

Secondary:
- "LLM agent safety"
- "autonomous agent attack"
- "tool misuse attack"
- "agent jailbreak"
```

### 组合搜索
```
- "VLM" + "web agent" + "adversarial"
- "multi-agent" + "security" + "attack"
- "web agent" + "red teaming"
- "agent" + "prompt injection" + "benchmark"
```

---

## 📊 论文对比分析

| 论文 | 攻击类型 | 场景 | 成功率 | 黑盒/白盒 | 多模态 |
|------|---------|------|--------|-----------|--------|
| WIPI | 内容注入 | Web浏览 | >90% | 黑盒 | ❌ |
| AdvWeb | 对抗性提示 | Web交互 | 未明确 | 黑盒 | ✅ VLM |
| WASP | Benchmark | 多场景 | - | - | - |
| 载体文章 | 语义隐藏 | 通用LLM | 63% | 黑盒 | ❌ |
| JailExpert | 经验学习 | 通用LLM | 提升显著 | 黑盒 | ❌ |

---

## 💡 与您研究的关联

### 结合点1: WIPI + 多语言攻击
```
WIPI的网页注入 × 低资源语言 = 新攻击方法

研究问题:
- 多语言恶意指令在网页中的检测难度？
- 低资源语言是否能提高WIPI的成功率？
- 自适应多语言攻击在Web Agent上的表现？
```

### 结合点2: AdvWeb + 跨模态多语言
```
AdvWeb的VLM攻击 × 图像OCR + 多语言 = 跨模态攻击

研究问题:
- 图像中的多语言文本能否绕过VLM的安全检测？
- 文本+图像的多语言组合攻击效果？
- 在真实Web环境中的可行性？
```

### 结合点3: WASP + MultiJail评测方法
```
WASP的评测框架 × MultiJail的多语言数据 = 新Benchmark

研究贡献:
- 构建多语言Web Agent安全Benchmark
- 评测现有Agent在多语言攻击下的脆弱性
- 对比不同语言资源的攻击成功率
```

---

## 🎯 推荐阅读顺序

### Phase 1: 快速了解（本周）
1. **WIPI** - 了解Web Agent最核心的攻击方法
2. **AdvWeb** - 了解最新的VLM Agent攻击
3. **WASP** - 了解评测标准和benchmark

### Phase 2: 深入研究（本月）
4. 精读WIPI的方法细节和实验设计
5. 分析AdvWeb的对抗性提示训练方法
6. 研究WASP的评测指标体系

### Phase 3: 拓展视野（长期）
7. 载体文章论文 - 学习隐藏恶意意图的技巧
8. JailExpert - 学习迭代优化攻击策略
9. 搜索更多相关领域的防御方法

---

## 📝 阅读笔记模板

为了系统整理这些论文，建议使用以下模板：

```markdown
# 论文标题

## 基本信息
- 发表时间:
- 作者:
- 会议/期刊:
- 链接:

## 一句话总结

## 核心贡献（3-5点）

## 方法概述
- 攻击链路:
- 关键技术:
- 实验设置:

## 主要结果
- 成功率:
- 关键发现:

## 与我研究的关联
- 可借鉴:
- 可改进:
- 可结合:

## 复现可行性
- 数据:
- 代码:
- 环境:

## 后续TODO
- [ ] 
```

---

## 🔗 相关资源

### 代码仓库（预期）
- WIPI GitHub: *（待论文发布后查找）*
- AdvWeb GitHub: *（待论文发布后查找）*
- WASP Benchmark: *（待论文发布后查找）*

### 相关会议与期刊
- **NeurIPS 2024**: AI安全专题
- **ICLR 2025**: Agent与安全
- **ACL 2024**: LLM安全
- **USENIX Security**: 系统安全
- **CCS**: 计算机安全

### 研究团队/机构
- **Michigan (Huan Sun组)**: AdvWeb作者所在
- **Meta AI**: WASP作者所在
- **UIUC (Bo Li组)**: AI安全知名团队

---

## ✅ 行动清单

### 本周行动
- [ ] 下载并阅读WIPI论文（重点关注方法和实验）
- [ ] 阅读AdvWeb论文摘要和方法部分
- [ ] 查看WASP benchmark的评测指标
- [ ] 与Polly讨论这些论文与研究方向的关系

### 本月行动
- [ ] 精读WIPI和AdvWeb的完整论文
- [ ] 尝试复现WIPI的攻击方法（如果有代码）
- [ ] 设计结合多语言的Web Agent攻击方案
- [ ] 准备research proposal初稿

### 长期计划
- [ ] 关注这些论文的后续工作和引用
- [ ] 参与相关会议（如果有机会）
- [ ] 构建自己的Web Agent安全数据集

---

## 🤔 思考题

阅读这些论文时，思考以下问题：

1. **攻击机制**: WIPI和AdvWeb的核心攻击机制有什么不同？
2. **成功率**: 为什么WIPI能达到>90%的成功率？关键因素是什么？
3. **防御挑战**: 为什么现有的安全机制对这些攻击无效？
4. **多语言结合**: 如何将多语言攻击融入这些方法？
5. **评测标准**: WASP的评测指标能否直接应用到多语言场景？

---

## 📞 下一步

### 与Polly讨论的问题
1. 这些论文中哪篇最接近您推荐的研究方向？
2. 我应该重点精读哪1-2篇？
3. 您认为多语言攻击能否有效结合到这些方法中？
4. 评测实验是否需要构建真实的Web环境？

---

**最后更新**: 2025-10-04  
**状态**: 📖 待阅读

**备注**: 部分arXiv编号可能需要验证，建议访问链接确认论文实际编号。某些论文可能正在投稿中，代码和数据集可能尚未公开。

