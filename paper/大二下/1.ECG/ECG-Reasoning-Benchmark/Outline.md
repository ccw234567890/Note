
# ECG-Reasoning-Benchmark: A Benchmark for Evaluating Clinical Reasoning Capabilities in ECG Interpretation

## Summary
本文提出了 ECG-Reasoning-Benchmark，一个包含 6,400+ 样本的多轮交互评估框架，用于系统评估多模态大语言模型（MLLMs）在心电图（ECG）解读中的逐步推理能力。覆盖 17 种核心 ECG 诊断。评估发现当前最先进模型在完整推理链上的完成率不足 6%，主要瓶颈在于模型无法将诊断标准锚定到 ECG 信号中的细粒度视觉证据上。

## Key Findings
- **完成率极低（< 6%）**：所有模型的完整推理链完成率均低于 6.3%，超过 94% 的样本中模型无法完成完整的临床推理。
- **推理瓶颈在 Stage 2-3**：模型能完成 Stage 1（Criterion Selection），但在 Stage 2（Finding Identification）和 Stage 3（ECG Grounding）处崩溃，Depth 指标几乎不超过 2.0。
- **ECG 专用模型的"性能崩塌"**：ECG-R1-RL 的 IDA 高达 85.41%，但 GT-RDA 仅 22.70%，说明模型靠表面模式匹配而非真正推理。相比之下，Hulu-Med (32B) 的 IDA 仅 57.49% 但 GT-RDA 达 99.42%，表明其具备真正的临床推理能力。
- **核心结论**：当前 MLLMs 绕过实际的视觉解读，暴露了现有训练范式的根本缺陷。

## Methodology
- **数据来源**：PTB-XL（21,837 份记录）和 MIMIC-IV-ECG（约 800,000 份记录），经严格人工审核筛选。
- **评估框架**：4 阶段多轮交互——Stage 1 Criterion Selection（标准选择）、Stage 2 Finding Identification（发现识别）、Stage 3 ECG Grounding（ECG 锚定）、Stage 4 Diagnosis Determination（诊断确定）。
- **评估指标**：IDA（初始诊断准确率）、Completion（完成率）、Depth（推理深度，0-4）、GT-RDA（基于金标准推理的诊断准确率）。
- **评估模型**：4 大类共 20 个模型，包括 ECG 专用模型（PULSE、GEM、ECG-R1）、医学领域模型（Hulu-Med、MedGemma）、通用视觉模型（Qwen3-VL、Llama-3.2-Vision）和闭源商业模型（Gemini、GPT 系列）。

## My Notes
这篇论文的核心贡献不在于提出新的数学模型，而在于设计了一个能够揭示模型"伪推理"本质的评估框架。GT-RDA 指标的设计非常巧妙——通过给模型提供正确的推理路径，分离了"知识"和"推理能力"两个维度。高 IDA + 低 GT-RDA 意味着模型只是学会了将 ECG 信号的全局特征直接映射到诊断标签的"捷径"。

## References
Oh, J., Chung, H., Lee, J., Kim, M.-G., Yoon, H., Lee, K. S., Lee, Y., Yeo, M., & Choi, E. (2026). *ECG-Reasoning-Benchmark: A Benchmark for Evaluating Clinical Reasoning Capabilities in ECG Interpretation*. arXiv. https://doi.org/10.48550/arXiv.2603.14326

---

Written by LLM-for-Zotero.
