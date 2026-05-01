
# Transformer Hawkes Process

## Summary
THP 首次将 Transformer 的自注意力机制引入点过程建模，解决了传统 RNN-based 点过程模型无法捕获长程依赖的问题。模型在多个真实数据集上显著优于 NHP、RMTPP 等基线方法，并可扩展集成图结构信息。

## Key Findings
- THP 在所有数据集上对数似然显著优于所有基线（Retweets: -2.04 vs NHP -5.60; MemeTrack: 0.68 vs NHP -6.23）
- 事件类型预测准确率最高（Financial 62.64%, MIMIC-II 85.3%, StackOverflow 47.0%）
- 事件时间预测 RMSE 大幅领先（MIMIC-II: 0.82 vs SAHP 3.89）
- 自注意力机制可同时捕获短程和长程依赖，且支持并行计算

## Methodology
- **时间编码**：将连续时间戳编码为 Transformer 可感知的位置编码形式
- **多头自注意力**：捕获任意时间距离的历史事件依赖关系
- **条件强度函数**：由当前项（线性插值）、历史项（隐状态映射）和基础项组成，通过 softplus 函数保证强度为正
- **训练**：最大化对数似然，积分近似采用蒙特卡洛或数值积分（梯形法则）
- **Structured-THP 扩展**：引入图注意力机制和顶点嵌入，建模多个相关事件序列

## My Notes
### 数学原理要点
1. **时间编码**：$[z(t_j)]_i = \cos(t_j / 10000^{(i-1)/M})$ 或 $\sin(t_j / 10000^{i/M})$，将连续时间映射到高维空间
2. **自注意力**：$S = \text{Softmax}(QK^\top / \sqrt{M_K})V$，注意力权重自动学习历史事件的重要性
3. **强度函数**：$\lambda_k(t|\mathcal{H}_t) = f_k(\alpha_k (t-t_j)/t_j + w_k^\top h(t_j) + b_k)$
4. **对数似然**：$\ell(S) = \sum \log \lambda(t_j|\mathcal{H}_j) - \int \lambda(t|\mathcal{H}_t)dt$

### 实验设计
- 7 个数据集覆盖长序列（Retweets 平均 109 步）和极短序列（MemeTrack 平均 3 步）
- 对比 RMTPP、NHP、TSES、SAHP 四个基线
- 评估指标：对数似然、事件类型准确率、时间预测 RMSE

### 关键洞察
- 浅层注意力头倾向于关注单个事件，深层注意力头关注更复杂的模式
- THP 在极短序列（MemeTrack）上表现优异，说明深层网络可捕获潜在属性
- 时间编码使模型能建模转发间隔逐渐变大的动态模式

## References
Zuo, S., Jiang, H., Li, Z., Zhao, T., & Zha, H. (2020). *Transformer Hawkes Process*. ICML 2020. arXiv:2002.09291v5.

---

Written by LLM-for-Zotero.
