
# MEIT: Multimodal Electrocardiogram Instruction Tuning on Large Language Models for Report Generation

## Summary
MEIT 是首个将大语言模型（LLM）与多模态指令微调相结合用于自动 ECG 报告生成的工作。它提出了一种轻量级的拼接式 ECG-文本对齐融合方法，在超过 800,000 份 ECG 报告上验证了 9 种开源 LLM，在报告质量、零样本泛化、噪声鲁棒性和人类专家对齐方面均表现优异。

## Key Findings
- **拼接式融合（Concatenated-fusion）** 优于 LLaVA 的直接输入和 Flamingo 的可训练交叉注意力，且无需额外可训练参数
- **指令微调** 在所有指标上大幅优于直接微调
- **LLaMA-3-Instruct 8B** 取得最优：BLEU-4=0.610, METEOR=0.799, ROUGE-L=0.773, CIDEr-D=5.78, BERTScore F-1=0.771
- **零样本域迁移** 有效：MIMIC-IV-ECG 训练 → PTB-XL 测试仍能生成有效报告
- **诊断准确性评分** 达 3.98/5（GPT-4o 评估），接近人类专家水平
- **模型规模扩展** 7B→13B→70B 性能提升但边际收益递减
- **1D 时序卷积编码器**（20.4M 参数）性能与 SSL 预训练的 ViT 相当，优于 Vision Mamba 和 ViT

## Methodology

### 模型架构
1. **ECG 编码器**：1D 时序卷积块（Conv1D → BatchNorm → ReLU → 平均池化）+ 非线性投影层，输出维度与 LLM 注意力头维度一致
2. **ECG-文本对齐**：将 ECG 嵌入 $H_e$ 与 LLM 第 $(i-1)$ 层隐藏状态 $H_t^i$ 在序列维度拼接，通过多头自注意力融合：
   - $K_{m,j} = [K_{e,j}, K_{t,j}]^\top$, $V_{m,j} = [V_{e,j}, V_{t,j}]$
   - $\text{head}_j = \text{Softmax}(Q_{t,j} K_{m,j} / \sqrt{D_h}) V_{m,j}$
3. **LLM 骨干**：使用 LoRA（alpha=64, rank=128, dropout=0.1）高效微调，LLM 骨干冻结

### 数据集
- **MIMIC-IV-ECG**：800,035 份报告（80/10/10 划分）
- **PTB-XL**：21,837 份报告（70/10/20 划分）

### 训练
- 自回归损失：$\mathcal{L} = -\sum_{i=j}^{L} \log p_\theta(x_{t,i} | X_p, X_e, X_{t,<i})$
- 仅对 `<assistant>` 之后的 token 计算损失
- 256 个多样化指令提示（GPT-4 改写扩展）

### 评估
- 10 个指标：BLEU 1-4, METEOR, ROUGE-1/2/L, CIDEr-D, BERTScore (P/R/F-1)
- 4 个任务：报告质量、零样本泛化、信号扰动鲁棒性、人类专家对齐

## My Notes
- 拼接式融合的设计非常巧妙——将 ECG 嵌入作为前缀条件拼接到序列维度，利用 LLM 已有的因果注意力机制完成跨模态融合，无需新增任何可训练参数
- 1D 时序卷积（20.4M 参数）以极小代价达到与 SSL 预训练 ViT 相当的性能，说明对于 ECG 这种一维时序信号，简单的卷积结构已经足够
- 零样本域迁移的成功（美国→欧洲，不同设备）说明模型学到了 ECG 信号的通用特征而非设备特定的伪影
- 局限性：生成结果缺乏完全的可解释性和可控性，未来可结合 RAG 和外部医学知识库

## References
Wan, Z., Liu, C., Wang, X., Tao, C., Shen, H., Xiong, J., Arcucci, R., Yao, H., & Zhang, M. (2025). *MEIT: Multimodal Electrocardiogram Instruction Tuning on Large Language Models for Report Generation*. arXiv:2403.04945. https://doi.org/10.48550/arXiv.2403.04945

---

Written by LLM-for-Zotero.
