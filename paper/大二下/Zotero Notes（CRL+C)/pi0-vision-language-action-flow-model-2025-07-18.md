---
title: "$π_0$: A Vision-Language-Action Flow Model for General Robot Control"
citekey: ""
doi: "10.48550/arXiv.2410.24164"
year: 2026
journal: ""
created: 2025-07-18
tags: [zotero, paper-note]
---

# $π_0$: A Vision-Language-Action Flow Model for General Robot Control

## Summary
π₀ 是一个通用的机器人基础模型（robot foundation model），由 Physical Intelligence 团队提出。它基于预训练的视觉-语言模型（VLM）PaliGemma 作为骨干网络，通过添加一个独立的"动作专家"（action expert）模块，利用 Flow Matching（流匹配）生成连续动作分布，从而实现对多种机器人形态（单臂、双臂、移动操作平台）的高频灵巧控制。模型在超过 10,000 小时的机器人数据上预训练，涵盖 7 种机器人配置和 68 个任务，并通过预训练/后训练（pre-training/post-training）两阶段策略实现从基础能力到高精度灵巧操作的迁移。

## Key Findings
- **Flow Matching 架构**：π₀ 使用条件流匹配（Conditional Flow Matching）对连续动作分布进行建模，避免了传统 VLA 模型将动作离散化为文本令牌带来的精度损失，能够以高达 50 Hz 的频率输出连续控制指令。
- **跨形态训练**：通过跨形态训练（cross-embodiment training），单一模型可以同时控制多种不同配置空间的机器人，包括单臂、双臂和移动操作平台。
- **预训练/后训练策略**：预训练阶段使用大规模多样化数据（含低质量数据）赋予模型广泛的基础能力和纠错行为；后训练阶段使用高质量精标数据微调，使模型在特定任务上达到高精度和高鲁棒性。
- **任务表现**：模型在折叠衣物、清理桌面、装盒、叠鸡蛋入盒等复杂灵巧操作任务上表现出色，能够执行长达数十分钟的多阶段任务。

## Methodology
π₀ 的模型架构基于 PaliGemma VLM，采用晚期融合（late fusion）方式将图像观测嵌入到语言令牌的同一语义空间中。模型的核心创新在于**动作专家（Action Expert）**模块：

1. **Flow Matching 动作生成**：动作专家使用条件流匹配来建模连续动作分布 $p(A_t|o_t)$。训练时，模型学习一个向量场 $v_\theta(A_t^\tau, o_t)$，该场将高斯噪声逐步变换为目标动作块 $A_t = [a_t, a_{t+1}, \dots, a_{t+H-1}]$。推断时从纯噪声出发，通过 10 步欧拉积分（步长 $\delta=0.1$）得到连续动作指令。
2. **动作分块（Action Chunking）**：模型一次性预测长度为 $H$ 的动作块，支持高频（50 Hz）控制。
3. **数据策略**：预训练数据混合了自有灵巧操作数据集和开源 OXE 数据集（共 22 种机器人数据），后训练使用高质量精标数据。

## My Notes
从电子信息工程的视角来看，π₀ 的 Flow Matching 机制可以类比为一个**端到端的连续信号发生器**：

- **离散→连续的转换**：传统 VLA 模型（如 OpenVLA）将动作空间离散化为有限类别，类似于数字信号处理中的量化过程，会引入量化误差。π₀ 的 Flow Matching 直接在实数域 $\mathbb{R}^d$ 中生成动作向量，避免了这一信息损失。
- **从噪声到控制波形的重建**：推断时，模型从高斯噪声（随机信号）出发，通过数值积分逐步"去噪"为有意义的连续动作序列。这类似于数字通信中的**信源解码+数模转换**过程：高维离散语义（视觉、语言令牌）作为"信源编码"，Flow Matching 作为"调制器"将其映射为物理世界的连续控制波形。
- **高频控制的意义**：50 Hz 的控制频率意味着每 20 毫秒输出一个动作指令，这对于折叠衣物等需要连续、平滑轨迹的灵巧操作至关重要。离散化架构由于自回归逐令牌生成，难以达到如此高的频率和精度。

## References
Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., Jakubczak, S., Jones, T., Ke, L., Levine, S., Li-Bell, A., Mothukuri, M., Nair, S., Pertsch, K., Shi, L. X., … Zhilinsky, U. (2026). *$π_0$: A Vision-Language-Action Flow Model for General Robot Control*. arXiv:2410.24164 [cs]. https://doi.org/10.48550/arXiv.2410.24164

---

Written by LLM-for-Zotero.

---
# 通用机器人基础模型：

通用机器人基础模型（generalist robot policies，即 robot foundation models）是π₀论文中所追求的核心目标。它指一种能够执行广泛、多样化机器人任务的通用策略模型，而非仅针对单一或窄域任务设计的专用控制器。其核心思想源自NLP和计算机视觉领域的“基础模型”范式：

    While such models have been shown to exhibit broad instruction-following and problem-solving abilities … they are not truly situated in a physical world … we will need to train them on physically situated data — that is, data from embodied robot agents. Flexible and general-purpose models that can be tasked to perform a variety of robot behaviors have tremendous practical ramifications.

Black 等, 2026, page 2

这意味着机器人基础模型是一个处在物理世界中的具身智能体，它通过大规模预训练在海量、多样化的机器人数据（来自不同任务、不同机器人、甚至非机器人数据）上习得丰富的视觉-语言-动作关联，从而获得以下能力：

    任务泛化：能够被自然语言指令提示（prompt），执行未曾在训练中出现过的全新任务，或经少量微调快速适应特定任务。
    行为鲁棒性：因见过高度多样的场景、干扰及错误恢复行为，它能在复杂物理交互中展现更强的纠正能力和泛化性。
    灵巧连续控制：能够输出高频（如50 Hz）、高精度的连续动作块，胜任折叠衣物、精密装配等复杂灵巧任务。

论文用π₀模型具体示范了这一概念：它基于预训练的VLM导入互联网级别的常识与语义推理，并加入流匹配动作专家产生高维连续动作，通过预训练+后训练的配方使模型同时具备广泛物理知识和高品质执行能力。因此，通用机器人基础模型并非专为“抓取鸟”或“开抽屉”而设计，而是一个可被重新赋值、覆盖家庭、车间等各种场景的通用操作平台。

---
# 开发generalist robotic model的三大瓶颈


根据π₀论文的论述，开发通用机器人基础模型（即“机器人基础模型”）面临的三大瓶颈具体如下：
1. 大规模训练的需求（Scale）

    While such models have been shown to exhibit broad instruction-following and problem-solving abilities, they are not truly situated in a physical world … we will need to train them on physically situated data — that is, data from embodied robot agents.

Black 等, 2026, page 2

问题：机器人学习领域长期面临数据稀缺、泛化性差、鲁棒性不足三大难题。若专门训练一个窄域任务模型（例如只针对“折叠衬衫”），往往只能获得几十到几百条演示轨迹，模型无法见识到足够多的场景、干扰、失败与恢复行为，泛化能力极其有限。而大规模预训练（类似于NLP和计算机视觉中的基础模型）有望解决这些问题，因为更多来源的数据（其他任务、其他机器人、甚至非机器人数据）都能被通用模型利用，从而覆盖更丰富的观察与动作分布。然而，大规模预训练的全部收益只有在足够大的规模下才会显现，小规模实验往往无法观察到这些收益（论文引用[54]）。因此，必须在海量机器人数据上进行大规模训练，这对数据采集、计算资源、工程架构都构成第一道瓶颈。
2. 合适的模型架构（Model Architecture）

    Second, it requires developing the right model architectures that can effectively make use of diverse data sources, while at the same time being able to represent the intricate and subtle behaviors necessary to interact with complex physical scenes.

Black 等, 2026, page 2

问题：机器人行为数据来源多样（不同机器人构型、不同传感器、不同动作空间），而且物理交互需要高度灵巧、高频、连续的控制（例如折叠衣物时需以50 Hz实时调整关节角度）。传统VLA模型（如OpenVLA）将动作离散化为文本令牌并自回归生成，无法支持动作分块和高频控制，导致灵巧任务表现崩溃。架构必须兼具以下能力：

    有效利用多源异构数据：整合不同机器人（单臂、双臂、移动机械臂）的观测和动作，实现跨形态训练。
    表征复杂连续动作分布：能够输出高维连续动作的多模态分布，并具备动作分块（action chunking） 来保持时序协调性。论文为此提出基于流匹配（Flow Matching） 的动作专家，将其附加在预训练的VLM之上，实现高频、连续、多模态动作生成。

因此，设计一个能够同时承载异质数据、并输出高精度连续动作的架构，是第二道瓶颈。
3. 正确的训练配方（Training Recipe）

    Third, it requires the right training recipe. This is perhaps the most important ingredient, as much of the recent progress with large models in NLP and computer vision has relied heavily on delicate strategies for curating pre-training and post-training data.

Black 等, 2026, page 2

问题：训练数据策展和训练阶段的划分直接决定模型行为。如果只在高质量干净数据上训练，模型学不会从错误中纠正和恢复（因为高质量数据中错误很少）；如果只在低质量多样数据上训练，模型虽然见过各种混乱场景，但表现不够高效、鲁棒和准确。正确的训练配方（recipe）需模仿大语言模型中的预训练+后训练两阶段策略：

    Intuitively, training only on high-quality data does not teach the model how to recover from mistakes, since mistakes are rarely seen in such data. Training on only lower-quality pre-training data does not teach the model to act efficiently and robustly. Combining both provides the desired behavior.

Black 等, 2026, page 3

    预训练阶段：在海量、多样性优先的混合数据（约10,000小时，包含大量复杂、噪声、错误恢复片段）上训练，赋予模型广泛的物理世界知识、恢复行为和纠正能力。
    后训练阶段：在高质量、精心策展的数据上微调，使模型的行为更加高效、稳定、符合预期，同时仍保留在错误出现时的恢复能力。

因此，如何划分训练阶段、策展预训练与后训练数据、平衡多样性与高质量，是最关键且最微妙的瓶颈。

总结：这三大瓶颈构成开发通用机器人基础模型的根本挑战——规模决定数据丰度与泛化潜力，架构决定能否融合异质数据并输出高精度连续动作，训练配方决定模型在真实物理任务中是否鲁棒、高效且具备错误恢复能力。

---
# 预训练，后训练：
在π₀模型（以及当代大模型训练范式中），预训练（pre-training） 和 后训练（post-training） 是两个连续的、目的不同的训练阶段，二者配合才能让模型既具备广泛的物理世界知识，又展现出高效、稳定的任务执行能力。
预训练（Pre-training）

预训练是指在大量、多样性优先的数据上对模型进行大规模初始训练，目标是赋予模型广泛的通用知识和基本能力。在π₀中：

    a pre-training phase endows our model with a broad base of knowledge, which is then refined in a post-training phase with higher-quality curated data to achieve the desired behavior.

Black 等, 2026, page 3

具体做法：

    使用约 10,000 小时的机器人演示数据（规模远超以往），混合多种来源、多种任务、甚至包含噪声和失败恢复片段。
    数据策展不追求完美质量，而是追求多样性：包含各种场景、错误、校正行为和恢复策略。
    预训练让模型学会从错误中恢复，因为错误在低质量数据中频繁出现，模型能够见识到“犯错→纠正”的完整链路。

直观理解：预训练相当于让模型通过海量经验的“通识教育”，建立对物理交互世界的普适认知，但还不一定精于某一具体任务的高效执行。
后训练（Post-training）

后训练是在预训练完成之后，使用高质量、精心策展的数据对模型进行进一步的微调或提示，目的是将模型的广泛能力聚焦并优化到期望的具体行为上。论文指出：

    Intuitively, training only on high-quality data does not teach the model how to recover from mistakes, since mistakes are rarely seen in such data. Training on only lower-quality pre-training data does not teach the model to act efficiently and robustly. Combining both provides the desired behavior.

Black 等, 2026, page 3

具体做法：

    使用高质量演示数据（例如由专家提供的流畅、高效的任务执行轨迹），这些数据中错误很少，行为规范。
    后训练使模型学习高效、稳定、符合任务的策略：在预训练赋予的恢复能力基础上，将行为“打磨”得更加精准、快速和可靠。
    后训练本质上是一种行为对齐过程，类似于LLM中的指令微调（instruction tuning）或RLHF。

直观理解：预训练好比一个见过大风大浪的学徒，知道如何应对各种意外；后训练则是一位精益求精的师傅，教会他如何干净利落地完成任务。二者结合，模型既能从容纠错，又能行云流水。

---

# Internet-scale pre-training

Internet-scale pre-training 指的是在互联网级别的大规模数据上对模型进行预训练——通常是海量的图像、文本、视频等多模态数据，数量级可达数十亿样本——使得模型能够学习到极其丰富和通用的视觉、语言概念及它们之间的关联。

在π₀模型中，internet-scale pre-training具体体现在它并非从零开始在机器人数据上训练，而是以一个预先在互联网规模数据上训练好的视觉语言模型（VLM） 为基础：

    Our model, which we describe in Section IV, is based on the PaliGemma vision-language model [5], which we then further train with our data mixture. To turn the base PaliGemma VLM into π0, we add action outputs that use flow matching [32, 28] to generate continuous action distributions.

Black 等, 2026, page 4

这里 PaliGemma 已经经历过海量网络图像和文本对的训练，因此它具备了：

    理解自然语言指令的能力；
    识别数千种物体、场景、材质的视觉理解能力；
    从图像到语言、从语言到概念的基础推理能力。

这些能力是在极其庞大、多样的互联网数据集上获得的，远远超出了任何机器人专用数据集所能覆盖的范围。π₀ 继承这个互联网预训练的知识，再通过机器人的动作数据（预训练+后训练）将视觉-语言能力接地到物理交互中。这样，机器人不仅能识别物体，还能理解“把易碎物品轻轻放下”这类抽象指令。

简而言之，internet-scale pre-training 就是让模型在遇到任何机器人任务之前，先成为一个“见过世面”的多模态理解模型，这为后续的机器人技能学习提供了强大的语义和视觉先验，使得用相对较少的机器人数据就能实现复杂行为的泛化。

互联网数据集（Internet-scale dataset），是指从互联网上大规模抓取、聚合而成的超大规模数据集，通常包含数以亿计甚至数十亿计的图像、文本、视频、音频等多种模态的数据样本。这些数据来源广泛，包括网页、社交媒体、百科、论坛、电商平台等，覆盖极其多样化的场景、概念和文化背景。
关键特征

    体量巨大：几十亿级别的样本，远超人手工标注的数据集。
    多模态：经常是图文对（如网页中图片与周围文字、alt标签），或视频-文本对（如视频配字幕）。
    弱/自监督标签：通常不是严格手工标注，而是利用互联网本身的共现关系形成“弱标签”（如图片与它的描述自然对齐）。
    覆盖面广：从自然风景、日常物品到抽象概念，几乎无所不包。

在π₀中的角色

π₀ 的基础模型 PaliGemma 就是在这样的互联网数据集上预训练的：

    Our model, which we describe in Section IV, is based on the PaliGemma vision-language model, which we then further train with our data mixture.

Black 等, 2026, page 4

正是借助在互联网数据集上获得的海量知识，π₀ 在遇到真实机器人数据之前就已经具备了：

    识别数千种物体与场景的视觉能力；
    理解复杂自然语言指令的语义能力；
    跨模态对齐的常识推理能力。

因此，互联网数据集相当于让模型先接受了“世界知识”的通识教育，使其在随后的机器人数据训练中能够事半功倍，将抽象概念落地为具体的物理动作。

---
# Cross-embodiment-training
在π₀模型中，跨形态训练（cross-embodiment training） 是一种核心策略，指将来自多种不同机器人形态的数据混合在一起，共同训练同一个模型，而不为每种机器人单独训练。论文是这样描述的：

    In order to make it feasible to utilize a variety of diverse robot data sources, we employ cross-embodiment training, where data from many robot types is combined into the same model. These different robot types have different configuration spaces and action representations, including single and dual-arm systems, as well as mobile manipulators.

Black 等, 2026, page 3

这一做法的关键概念可以拆解如下：
1. 机器人形态（embodiment）的多样性

    机器人构型：单臂、双臂、移动机械臂（带轮式底盘的机械臂）、甚至不同类型的夹爪等。
    动作空间：不同机器人有不同的自由度（例如6轴机械臂与7轴机械臂）、不同的控制模式（关节角度、末端笛卡尔位姿）以及不同的维度和数值范围。
    观测空间：相机数量和安装位置不同、是否提供深度传感器、本体感知维度各异。

传统方法通常为每种机器人单独训练策略，导致数据利用率极低，小量数据难以泛化。
2. 跨形态训练的做法

将所有不同机器人的数据统一为一种通用格式，然后注入同一个模型。具体而言：

    所有图像输入被缩放、切块后送入统一的视觉编码器。
    本体感知状态（关节角度、末端位姿等）通过投影层映射到统一维度的嵌入向量。
    动作输出也采用统一维度的动作分块（固定长度 HH 的序列），不同机器人只需填充自己需控制的部分维度，其余维度用掩码或固定值占位。
    模型通过附加的动作专家学习到不同机器人动作空间的映射关系，而不是为每个机器人单独训练独立的策略头。

这样，模型就可以在来自不同机器人的海量混合数据上进行联合训练，既提高了数据利用率，又允许知识在不同形态之间迁移与共享。
3. 为什么要跨形态训练？

    扩大数据规模：单一机器人的数据量非常有限（通常只有几十到几百条演示），混合多种机器人后可达上万小时演示，满足大规模训练的需求。
    学习通用物理交互：不同机器人在执行“抓取”、“推动”、“折叠”等操作时，物理规律是共通的。模型从多形态数据中抽取共性特征（如力与运动的关系、物体变化的视觉模式），使策略更具泛化性。
    实现零样本或多任务学习：单一模型可被用于控制未见过的机器人构型，只需提供少量的后训练数据便能快速适应新形态。

4. 面临的挑战

不同机器人动作空间的差异（如位置控制 vs. 速度控制）需要模型具备处理多分布的能力。π₀通过流匹配（Flow Matching）来建模连续、多模态的动作分布，天然适合表达不同机器人的复杂动作分布，这也是它们选择流匹配而非离散化的原因之一。

总结：跨形态训练的本质是用统一的模型结构吸收异构机器人数据，从而实现知识重用、数据增强和规模化训练，这是构建通用机器人基础模型的必经之路。

---
# 流匹配
这句话描述了 π₀ 模型能够执行高度灵巧、精细物理任务的核心技术：==动作分块架构==和==流匹配==，二者共同解决了复杂连续动作分布的建模问题。

    Additionally, in order to make it possible to perform highly dexterous and intricate physical tasks, we use an action chunking architecture with flow matching (a variant of diffusion) to represent complex continuous action distributions.

Black 等, 2026, page 3
1. 动作分块架构（Action Chunking Architecture）

动作分块 是指模型的输出不是当前的单个动作，而是未来一段时间内的一系列连续动作（一个动作块，chunk）。例如，模型每次预测接下来 H 个时间步的动作序列 at:t+H​，实际执行时可能只执行前 k 个，然后重新预测。

    作用一：提供时间上下文与平滑性

对于灵巧任务（如折叠衣物、插线），动作之间需要高度协调，连续动作块能让模型学习动作之间的时序关联，避免单步预测带来的抖动或突变。

    作用二：适应高频控制

π₀ 控制机器人频率高达 50 Hz，动作分块可以提前规划一小段轨迹，使控制更加稳定高效。

    本质

将决策从“一步预测”转变为“轨迹预测”，从而更好地表达长时间尺度的连续运动。
2. 流匹配（Flow Matching）

流匹配 是一种生成模型（diffusion 的变体），它学习一个向量场 vθvθ​，将简单噪声分布 x0∼N(0,I)x0​∼N(0,I) 沿着概率路径连续变换为目标动作分布 x1x1​。训练时，模型学习匹配这个向量场；推理时，从噪声开始，沿着学习到的向量场逐步积分，生成最终的动作。

    高精度：直接建模连续分布，避免了离散化导致的量化误差，非常适合需要微米级/毫弧度级控制的灵巧操作。
    多模态建模能力：对于同一个指令，可能存在多条合理动作轨迹（比如避开障碍物的不同方向），流匹配能够自然地采样出不同但都可行的动作序列。
    适应高维动作空间：π₀ 的动作块是一个 H×DH×D 维的向量，流匹配能够有效处理这种高维连续数据的生成。

    Flow matching provides our model with high precision and multimodal modeling capability, making it especially well suited to high-frequency dexterous tasks.

Black 等, 2026, page 4
3. 如何结合实现“复杂连续动作分布”

过去很多 VLA 模型将动作离散化成数字令牌，再用语言模型进行下一步预测。这种方式在处理高频、精细、多模态的动作时，表达能力有限，且容易产生不连续的动作。

π₀ 的做法：

    输出动作块：将动作建模为一个连续序列 at:t+Hat:t+H​。
    用流匹配生成整个动作块：以当前观测和指令为条件，从一个噪声向量出发，通过流匹配的迭代去噪生成完整、平滑的动作序列，而不是逐步自回归生成。
    整个系统以 50 Hz 运行：动作分块保证了时间连贯性，流匹配保证了每块内部动作的高精度和多模态合理性。

这样，π₀ 便可以完成如洗衣折叠、把盘子放进微波炉、叠蛋盒等需要高度灵巧和连续操控的任务，而这正是以前离散化 VLA 方法难以企及的。