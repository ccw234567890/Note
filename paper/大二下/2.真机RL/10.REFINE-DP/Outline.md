我已经在上一个回答中给出了完整的讲解。看起来你希望我重新组织或补充更多细节。让我基于已读取的证据，再做一个更系统、更深入的讲解。

---

## REFINE-DP 论文完整讲解

### 一、论文概述

**REFINE-DP**（Reinforcement Learning Fine-tuning of Diffusion Policy）发表于 IEEE Robotics and Automation Letters，核心贡献是提出了一套**分层人形机器人全身移动操作框架**，通过强化学习微调扩散策略，解决离线预训练策略与底层控制器之间的分布不匹配问题。

> "Humanoid loco-manipulation requires coordinated high-level motion plans with stable, low-level whole-body execution under complex robot-environment dynamics and long-horizon tasks." (Gu 等, 2026)

---

### 二、实验设计详解

#### 2.1 三阶段流水线

论文的整个框架分为三个阶段（Fig. 1）：

**阶段 (a) 数据收集**

- 使用一个**冻结的 RL 全身移动操作控制器** $\pi_{\text{loco-manip}}$ 在源环境中收集专家演示
- 数据来源：50条人工遥操作轨迹 + 启发式规划器自动生成，扩展至 **1000条成功轨迹**
- 状态包含：机器人手部/脚部姿态（body frame）、夹爪状态、物体信息
- 动作包含：期望手部姿态、夹爪状态、基座速度命令
- 使用 **velocity-to-footstep planner** 将速度命令转为足部步序

**阶段 (b) 扩散策略预训练**

- 用收集的演示数据训练 DP 作为**高层规划器**
- DP 输出低维命令（基座速度 + 手部姿态），而非直接控制 29 个关节

**阶段 (c) 联合优化（核心创新）**

- **同时微调**高层 DP 和底层 RL 控制器
- DP 通过 **DPPO** 更新，底层控制器通过 **PPO** 更新

#### 2.2 机器人平台与硬件

|项目|规格|
|---|---|
|机器人|Booster T1 人形机器人|
|自由度|29|
|计算平台|AMD 7945HX CPU + NVIDIA RTX 4060 GPU|
|控制频率|行走 ≤ 0.2 m/s，手部 ≤ 0.05 m/s|
|底层控制|PD 控制跟踪目标关节位置 $q_{text{target}} = q_{text{def}} + a_t$|

#### 2.3 四个实验任务

|任务|描述|关键挑战|
|---|---|---|
|**Task 1**|基础物体搬运|基础移动操作|
|**Task 2**|长时域物体运输|长时间执行，累积误差|
|**Task 3**|**开门并穿越**|首次将 DP 用于人形开门，需要协调推门+行走|
|**Task 4**|**台阶辅助物体取回**|不平地形 + 登高取物|

#### 2.4 基线方法设计

论文设计了4种对比方法，用于消融研究：

1. **DiT**（预训练 Diffusion Transformer）——标准 DP 基线
2. **MLP**（确定性多层感知器）——无不确定性建模，输出确定性动作
3. **MLP-FT**（MLP + RL 微调）——将 MLP 转为随机策略微调，作为骨干网络消融
4. **Residual RL**——在冻结 DP 上学习残差修正

> "Residual RL [23] improves a pre-trained DP by learning a lightweight corrective residual that is added to the output of the frozen DP" (Gu 等, 2026)

#### 2.5 分布外（OOD）测试设计

在物体运输任务上，通过域随机化扩展三个参数：

- **径向距离**：扩展到预训练范围的 **320%**
- **极角**：扩展到 **125%**
- **航向角**：扩展到 **600%**

采用**课程学习**策略：每次增加 10% 随机化范围，当策略在当前水平达到 90% 成功率时才推进。

---

### 三、数学原理与公式推导

#### 3.1 扩散策略（Diffusion Policy）的数学基础

##### 条件动作分布

扩散策略将动作生成建模为一个条件去噪扩散过程：

$$p_\theta(A_t^{0:K} | S_t) = p(A_t^K) \prod_{k=1}^K p_\theta(A_t^{k-1} | A_t^k, S_t)$$

其中：

- $A_t^k$：第 $k$ 个去噪步的动作块（action chunk）
- $S_t$：观测状态块
- $K$：总去噪步数

##### 前向扩散过程

在前向过程中，高斯噪声逐步添加到动作上：

$$q(A_t^k | A_t^{k-1}) = \mathcal{N}\left(\sqrt{\alpha_k} A_t^{k-1}, (1-\alpha_k)I\right) \tag{1}$$

其中 $\{\alpha_k\}_{k=1}^K$ 是预定义的递减系数序列（noise schedule）。

利用重参数化技巧，可以直接从闭合形式采样：

$$A_t^k = \sqrt{\bar{\alpha}_k} A_t^0 + \sqrt{1 - \bar{\alpha}_k} \varepsilon, \quad \varepsilon \sim \mathcal{N}(0, I)$$

其中 $\bar{\alpha}_k = \prod_{i=1}^k \alpha_i$。

##### 训练目标：噪声预测

给定数据集 $\mathcal{D} = \{(S_i, A_i^0)\}_{i=1}^N$，训练一个噪声预测网络 $\varepsilon_\theta$，最小化：

$$\mathcal{L}_{\text{diff}}(\theta) = \mathbb{E}_{A_t^0, S_t, k, \varepsilon}\left[ \|\varepsilon - \varepsilon_\theta(A_t^k, S_t, k)\|^2 \right] \tag{2}$$

**直观理解**：网络学习预测添加到动作上的噪声 $\varepsilon$，从而学会如何从噪声中恢复出干净动作。这是一个简单的 MSE 损失，但训练时需要在所有去噪步 $k$ 上采样。

##### 反向去噪过程（推理时）

推理时从纯噪声 $A_t^K \sim \mathcal{N}(0, I)$ 开始，逐步去噪：

$$p_\theta(A_t^{k-1} | A_t^k, S_t) = \mathcal{N}\left(A_t^{k-1}; \mu_\theta(A_t^k, S_t), \sigma_k\right) \tag{3}$$

其中均值由预测的噪声计算：

$$\mu_\theta(A_t^k, S_t) = \frac{1}{\sqrt{\alpha_k}} \left( A_t^k - \frac{1-\alpha_k}{\sqrt{1-\bar{\alpha}_k}} \varepsilon_\theta(A_t^k, S_t, k) \right)$$

方差为：

$$\sigma_k = \frac{1-\bar{\alpha}_{k-1}}{1-\bar{\alpha}_k} \cdot (1-\alpha_k)$$

**推导思路**：这个均值公式来自 DDPM 的去噪公式——给定 $A_t^k$，要预测 $A_t^{k-1}$，需要从 $A_t^k$ 中减去预测的噪声成分，再按系数缩放。

#### 3.2 DPPO：扩散策略的 RL 微调

##### 核心问题

标准 PPO 需要评估策略密度函数 $\bar{\pi}_\theta(A_t^0|S_t)$，但扩散策略是**隐式策略**，其密度不可直接计算。

##### 解决方案：增强 MDP

定义环境 MDP 为 $\mathcal{M}_{\text{ENV}} := (\mathcal{S}, \mathcal{A}, P_0, P, R)$。

构造**扩散过程增强 MDP** $\bar{\mathcal{M}} := (\bar{\mathcal{S}}, \bar{\mathcal{A}}, \bar{P}_0, \bar{P}, \bar{R})$，在每个环境时间步中插入完整的去噪过程。

**统一时间步索引**：

$$\bar{t}(t, k) = tK + (K - 1 - k)$$

其中 $K$ 是总去噪步数，$k \in [0, K-1]$。

**增强后的状态、动作和初始分布**：

$$\bar{s}_{\bar{t}(t,k)} = (S_t, A_t^{k+1}), \quad \bar{a}_{\bar{t}(t,k)} = A_t^k, \quad \bar{P}_0 = P_0 \otimes \mathcal{N}(0, I)$$

**关键洞察**：增强 MDP 将去噪过程的每一步都视为 MDP 中的一个决策步。状态包含当前环境状态 $S_t$ 和下一步的噪声动作 $A_t^{k+1}$，动作是当前步的噪声动作 $A_t^k$。

##### 转移动力学

$$\bar{P}(\bar{s}_{\bar{t}+1} | \bar{s}_{\bar{t}}, \bar{a}_{\bar{t}}) = 
\begin{cases}
(S_t, A_t^k) \sim \delta_{S_t, A_t^k}, & k > 0 \\
(S_{t+1}, A_{t+1}^K) \sim P(S_{t+1}|S_t, A_t^0) \otimes \mathcal{N}(0, I), & k = 0
\end{cases} \tag{4}$$

其中 $\delta$ 是 Dirac 分布。

**解释**：

- 当 $k > 0$（去噪中间步）：状态转移是确定性的——环境状态不变，只更新去噪步
- 当 $k = 0$（去噪完成）：动作 $A_t^0$ 真正执行到环境中，环境状态更新，并采样新的初始噪声

##### 奖励函数

$$\bar{R}_{\bar{t}(t,k)}(\bar{s}_{\bar{t}(t,k)}, \bar{a}_{\bar{t}(t,k)}) = 
\begin{cases}
0, & k > 0 \\
R_t(S_t, A_t^0), & k = 0
\end{cases} \tag{5}$$

**只有最终去噪动作获得奖励**，中间去噪步奖励为零。这符合直觉——只有真正执行到环境中的动作才产生效果。

##### 策略梯度目标

$$\nabla_\theta \bar{J}(\bar{\pi}_\theta) = \mathbb{E}_{\bar{\pi}_\theta, \bar{P}, \bar{P}_0} \left[ \sum_{\bar{t} \geq 0} \nabla_\theta \log \bar{\pi}_\theta(\bar{a}_{\bar{t}} | \bar{s}_{\bar{t}}) \cdot \bar{r}(\bar{s}_{\bar{t}}, \bar{a}_{\bar{t}}) \right] \tag{6}$$

其中折扣回报：

$$\bar{r}(\bar{s}_{\bar{t}}, \bar{a}_{\bar{t}}) := \sum_{\tau \geq \bar{t}} \gamma^{(\tau)} \bar{R}_\tau(\bar{s}_\tau, \bar{a}_\tau)$$

且 $\bar{\pi}_\theta(\bar{a}_{\bar{t}(t,k)} | \bar{s}_{\bar{t}(t,k)}) = p_\theta(A_t^k | A_t^{k+1}, S_t)$。

**实际实现**：使用 **GAE（Generalized Advantage Estimation）** 计算优势函数 $\hat{A}(\bar{s}_{\bar{t}}, \bar{a}_{\bar{t}})$，然后用 **PPO 的 clipped surrogate objective** 优化。

#### 3.3 联合优化算法

这是论文的核心创新——**同时微调高层 DP 和底层 RL 控制器**。

增强 MDP 产生**两组**状态和奖励：

- $(\bar{s}_t, \bar{R}_t)$：用于更新 DP $\bar{\pi}_\theta$，提升任务成功率
- $(s_t, \hat{R}_t)$：用于更新底层控制器 $\pi_{\text{loco-manip}}$，提升运动质量

**为什么需要联合优化？**

> "Unlike the independently sampled, stationary commands used during controller pre-training, DP commands represent a moving target along a continuous trajectory, creating a distribution mismatch that degrades tracking performance. Joint optimization alleviates this mismatch by exposing the controller to planner-generated commands" (Gu 等, 2026)

**算法伪代码（Algorithm 1）**：

```
输入: 预训练 DP π̄_θ, 底层控制器 π_loco-manip, 增强 MDP M̄
初始化: 回放缓冲区 D = D̄ = ∅

for iter = 0 to L:
    // === 内循环1: 更新底层控制器 ===
    for iter = 0 to M:
        从 DP 采样动作块 A_t^0 = π̄_θ(A_t^0|S_t)
        执行得到 (s_t, a_t, R̂_t) = M̄(A_t^0)
        D ← D ∪ {(s_t, a_t, R̂_t)}
        从 D 采样小批量 D_k
        用 PPO 更新 π_loco-manip

    // === 内循环2: 更新高层 DP ===
    for iter = 0 to N:
        从 DP 采样动作块 A_t^0 = π̄_θ(A_t^0|S_t)
        执行得到 (s̄_t, ā_t, R̄_t) = M̄(A_t^0)
        D̄ ← D̄ ∪ {(s̄_t, ā_t, R̄_t)}
        从 D̄ 采样小批量 D̄_k
        用 DPPO (公式6) 更新 π̄_θ
```

#### 3.4 MLP 微调的均值回归采样

对于 MLP 基线微调，将确定性 MLP 转为随机策略：

$$A_t^{k-1} = (1 - \lambda_k) A_t^k + \lambda_k \tilde{\mu}_\theta(S_t) + \tilde{\sigma}_k \varepsilon_k, \quad \varepsilon_k \sim \mathcal{N}(0, I)$$

其中：

- $\tilde{\mu}_\theta(S_t)$：MLP 均值预测
- $\lambda_k$：插值系数（线性调度），控制向均值回归的强度
- $\tilde{\sigma}_k$：探索幅度（递减调度），控制随机性

**设计思路**：早期去噪步（大 $k$）探索性强，后期去噪步（小 $k$）集中在均值附近，保证确定性结构的同时引入随机探索。

---

### 四、实验结果与结论

#### 4.1 仿真成功率对比

|方法|Task 1|Task 2|Task 3|Task 4|
|---|---|---|---|---|
|DiT Planner（预训练）|68%|64%|73%|56%|
|MLP Planner（预训练）|44%|24%|18%|57%|
|MLP-FT（微调）|81%|43%|45%|64%|
|Residual RL|86%|85%|91%|70%|
|**DiT-FT (Ours)**|**97%**|**98%**|**99%**|**98%**|
|**Joint Optimized (Ours)**|**97%**|**97%**|**99%**|**99%**|

#### 4.2 关键发现

**1. REFINE-DP 大幅超越所有基线**

- 预训练 DiT 仅 56-73%，微调后达到 **97-99%**
- 预训练 MLP 仅 18-57%，远差于 DiT——说明**概率建模能力至关重要**

**2. Transformer 骨干优于 MLP 骨干**

- DiT 预训练（56-73%）远优于 MLP 预训练（18-57%）
- DiT-FT（97-99%）远优于 MLP-FT（43-81%）
- 原因：扩散模型的多模态分布建模能力

**3. 联合优化提升运动质量而非成功率**

- DiT-FT 和 Joint Optimized 的成功率几乎相同
- 但联合优化显著提升**运动跟踪精度和动作平滑度**

**4. Residual RL 不如完整微调**

- Residual RL（70-91%）优于预训练但远不如 DiT-FT（97-99%）
- 说明**修改 DP 参数本身**比添加残差修正更有效

#### 4.3 分布外泛化结果

|条件|预训练 DP|直接微调（无课程）|课程微调（Ours）|
|---|---|---|---|
|最大随机化水平|**7%**|**30%**|**>90%**|

**课程学习至关重要**——直接在高难度下微调会导致策略崩溃（仅 30%），而逐步增加难度可达到 90%+。

#### 4.4 真实硬件实验结果

|任务|成功率|
|---|---|
|开门穿越（door traversal）|**>70%**|
|箱子搬运（box transport）|**>50%**|

Sim-to-real 差距主要来自：

1. 物体观测噪声（门把手位置、目标箱子姿态不准确）
2. 真实动力学与仿真的差异

#### 4.5 核心结论总结

1. **RL 微调是可靠人形移动操作的关键**——仅靠离线预训练不足以应对复杂动态环境
2. **分层架构有效**——高层 DP 输出低维命令 + 底层 RL 控制器负责全身执行，大幅降低学习难度
3. **联合优化消除分布不匹配**——让底层控制器暴露于 DP 生成的动态命令分布中
4. **课程学习对 OOD 泛化至关重要**——直接在高难度下微调会导致策略崩溃
5. **小数据集 + RL 微调可以超越大数据集预训练**——这是该方法的核心经济性优势
6. **扩散模型的概率建模能力优于确定性 MLP**——多模态动作分布对移动操作任务至关重要