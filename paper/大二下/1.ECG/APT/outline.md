---
title: "APT: Affine Prototype-Timestamp For Time Series Forecasting Under Distribution Shift"
citekey: ""
doi: "10.48550/arXiv.2511.12945"
year: 2025
journal: ""
created: 2026-05-06
tags: [zotero, paper-note]
---

# APT: Affine Prototype-Timestamp For Time Series Forecasting Under Distribution Shift

## Summary
APT 是一个轻量级即插即用模块，通过时间戳条件化的原型学习（Prototype Learning）动态生成仿射参数，将全局分布特征注入归一化-预测管线，解决时间序列预测中的分布偏移（Distribution Shift）问题。与 RevIN 等方法的静态仿射变换不同，APT 利用离散时间戳信息为不同子序列动态生成不同的仿射参数，显著提升在分布偏移强烈场景下的预测性能。

## Key Findings
- 在分布偏移强烈的数据集（ETTh1/ETTh2、Exchange）上，APT 带来 **4%–40% 的性能提升**，跨越多种 backbone-归一化组合
- 即使在稳定的数据集（如 ECL）上，APT 也能持续带来增益，几乎没有退化风险
- APT 与任意 backbone 和归一化策略兼容，仅引入 1.5K–5K 参数（backbone 通常超过 1M 参数）
- 原型学习使时间戳嵌入形成与"一周中的天"对应的清晰聚类（t-SNE 可视化验证）

## Methodology

### 整体框架
APT 位于归一化-预测-反归一化管线中：
- **前向变换（APT）**：在归一化之后、backbone 输入之前
- **反向变换（de-APT）**：在 backbone 输出之后、反归一化之前

### 数学原理

**时间戳编码（公式 4）**：将时间戳离散化为分类属性（TiD + DiW），每个时间戳由其属性嵌入之和表示：
$$T_t = T^{TiD}_t + T^{DiW}_t$$

**原型学习（公式 5-7）**：
1. 相似度计算：时间戳嵌入与原型库做内积
2. Top-k 选择 + Softmax：选取最相似的 k 个原型，计算权重
3. 加权聚合：最终时间戳表示为原型嵌入的加权和

**仿射参数生成（公式 8）**：通过两个 MLP 将聚合后的时间戳表示映射为通道级仿射参数：
$$\gamma_t, \beta_t = \text{MLP}_\gamma(\tilde{T}_t), \text{MLP}_\beta(\tilde{T}_t)$$

**完整前向-反向变换（公式 9）**：
$$y^{(i)}_{t+1:t+H} = \sigma^{(i)}_{h,t} \gamma^{(i)}_t \left( M\left( \gamma^{(i)}_t \frac{x^{(i)}_{t-L:t} - \mu^{(i)}_{l,t}}{\sigma^{(i)}_{l,t}} + \beta^{(i)}_t \right) - \beta^{(i)}_t \right) + \mu^{(i)}_{h,t}$$

### 训练策略
- **阶段一**：自监督预训练（冻结 backbone 和归一化），使用三个损失函数：
  - 正交损失（公式 10）：确保嵌入多样性
  - 负载均衡损失（公式 11）：防止原型坍缩
  - 仿射正则化损失（公式 12）：防止仿射参数不稳定
- **阶段二**：联合优化，APT 与 backbone、归一化模块一起在标准 MSE 下优化

### 实验设置
- **数据集**：ECL、ETTh1/ETTh2、Exchange、Traffic、Weather（6个基准）
- **Backbone**：CATS、Informer、iTransformer、SparseTSF（4种）
- **归一化策略**：RevIN、Dish-TS、SAN、FAN（4种）
- **预测长度**：H = {96, 192, 336, 720}

## My Notes
APT 的核心创新在于将时间戳信息通过原型学习转化为动态仿射参数，解决了 RevIN 静态仿射变换的局限。其对称的前向-反向结构保证了 backbone 可以专注于学习纯净的时序模式，而分布信息由 APT 模块管理。参数量极小（1.5K–5K）使其成为真正实用的即插即用方案。

## References
Li, Y., Shao, Z., Yu, C., Fu, Y., Sun, T., Xu, Y., & Wang, F. (2025). *APT: Affine Prototype-Timestamp For Time Series Forecasting Under Distribution Shift*. arXiv:2511.12945 [cs]. https://doi.org/10.48550/arXiv.2511.12945

---

Written by LLM-for-Zotero.
