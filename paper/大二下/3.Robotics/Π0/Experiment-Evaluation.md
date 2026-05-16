
# $π_0$: A Vision-Language-Action Flow Model for General Robot Control

## Experiment Evaluation — 实验设计总纲

论文实验部分明确提出了**四个核心研究问题**，每个问题对应一组实验：

### 研究问题 1：预训练后的零样本能力

> How well does π0 perform after pre-training on a variety of tasks that are present in the pre-training data? We study this question by directly evaluating π0, with comparisons to other robot foundation models.

(Black et al., 2026)

**含义**：π₀ 在预训练后，不经过任何微调，直接执行预训练数据中出现过的任务，效果如何？

**评估方法**：开箱即用（out of box）评估，对比其他机器人基础模型（OpenVLA、Octo）。

**对应图表**：Figure 7

---

### 研究问题 2：语言指令跟随能力

> How well does π0 follow language commands? These experiments compare π0 to π0-small, a smaller version of our model without VLM initialization, to evaluate its performance on following language commands. We evaluate with both human-provided commands and commands specified by a high-level VLM policy, as discussed in Section V-B.

(Black et al., 2026)

**含义**：π₀ 能否准确理解并执行语言指令？

**评估方法**：
- 对比 **π₀** vs **π₀-small**（无 VLM 预训练的小模型）
- 两种指令来源：**人类提供**的中间指令 vs **高层 VLM 自动生成**的指令

**对应图表**：Figure 9

---

### 研究问题 3：与专用灵巧操作方法的对比

> How does π0 compare to methods that have been proposed specifically for addressing dexterous manipulation tasks? These experiments study downstream tasks for which we can either fine-tune our model from the pre-trained initialization, or train it from scratch on task-specific data, comparing to prior methods that were proposed for dexterous manipulation.

(Black et al., 2026)

**含义**：与专门为灵巧操作设计的**专用方法**（如 ACT、Diffusion Policy）相比，π₀ 表现如何？

**评估方法**：
- **π₀（fine-tune）**：从预训练权重微调
- **π₀（scratch）**：从零训练
- 对比基线：ACT、Diffusion Policy 等

**对应图表**：Figure 11

---

### 研究问题 4：复杂多阶段任务的适应能力

> Can π0 be adapted to complex, multi-stage tasks? In our final set of experiments, we fine-tune π0 to a set of particularly complex tasks, including folding laundry and bussing a table. These tasks take between 5 and 20 minutes to complete.

(Black et al., 2026)

**含义**：π₀ 能否处理需要多个步骤、长时间执行的复杂任务？

**评估方法**：微调 π₀ 到**叠衣服**和**收拾餐桌**等任务，每个任务耗时 **5~20 分钟**。

**对应图表**：Figure 12

---

## 实验设计总图

| 研究问题 | 评估方式 | 对比基线 | 对应图表 |
|----------|----------|----------|----------|
| ① 零样本能力 | 开箱即用（out of box） | OpenVLA、Octo | Figure 7 |
| ② 语言跟随 | π₀ vs π₀-small | 人类指令 vs VLM 指令 | Figure 9 |
| ③ 灵巧操作 | fine-tune vs scratch | ACT、Diffusion Policy | Figure 11 |
| ④ 复杂多阶段 | 微调后执行 | 叠衣服、收拾餐桌 | Figure 12 |

## 实验方法概述

论文的实验方法分为两个层面：

1. **直接提示对比（direct prompting）**：对替代模型设计进行开箱即用评估
2. **详细微调实验（detailed fine-tuning experiments）**：在具有挑战性的下游任务上评估模型，对比其他专为灵巧操作提出的方法

## 参考文献

Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., Jakubczak, S., Jones, T., Ke, L., Levine, S., Li-Bell, A., Mothukuri, M., Nair, S., Pertsch, K., Shi, L. X., … Zhilinsky, U. (2026). *$π_0$: A Vision-Language-Action Flow Model for General Robot Control*. arXiv:2410.24164 [cs].

---

Written by LLM-for-Zotero.
