Now I have comprehensive information. Let me compile a thorough answer.

---

## RL-100 论文深度解析

### 一、实验设计

#### 1.1 整体框架：三阶段训练流水线

RL-100 采用 **三阶段渐进式训练** 策略，从人类示范出发，逐步通过强化学习自我提升：

> **Stage 1 — 模仿学习 (Imitation Learning)** 通过行为克隆 (Behavior Cloning) 在人类遥操作轨迹上初始化策略。使用条件扩散模型 (conditional diffusion) 从视觉观测和机器人本体感知中学习鲁棒的视觉运动策略。

> **Stage 2 — 迭代离线 RL 后训练 (Iterative Offline RL Post-Training)** 在离线数据集上，使用统一的裁剪 PPO 代理目标 (clipped PPO surrogate objective) 保守地改进策略，配合渐进式数据扩展 (progressive data expansion) 来获取大部分性能增益。

> **Stage 3 — 在线微调 (Online Fine-Tuning)** 在真实机器人上短暂在线交互，消除残余的失败模式，最终达到完美性能。

#### 1.2 8 个真实机器人任务

RL-100 在 **8 个多样化真实操作任务** 上评估，覆盖了流体/颗粒、工具使用、可变形物体操作、动态非抓取操作和精密插入等多种场景：

|任务|描述|关键挑战|
|---|---|---|
|**Dynamic Push-T**|推动 T 形块到目标位置|动态接触、摩擦变化|
|**Agile Bowling**|敏捷保龄球投掷|动态释放、轨迹成形|
|**Pouring**|倒液体/颗粒物|容器倾斜控制、流体动力学|
|**Dynamic Unscrewing**|灵巧手动态拧螺丝|接触丰富、精密力控|
|**Soft-towel Folding**|双臂软毛巾折叠|可变形物体、双臂协调|
|**Orange Juicing — Placing**|橙汁榨取 — 放置|大角度倾斜插入|
|**Orange Juicing — Removal**|橙汁榨取 — 取出|狭窄腔体中的推出|
|**Box Folding**|双臂纸盒折叠|长时域、双臂协调、折痕对齐|

#### 1.3 奖励设计

奖励机制非常简洁：对于除 Dynamic Push-T 外的所有任务，人类操作员在任务成功完成时给予 **终端成功奖励 +1** 并结束回合；否则奖励为 0，回合在超时或安全停止时终止。这是一个 **稀疏奖励 (sparse reward)** 设置，增加了 RL 优化的难度。

#### 1.4 基线对比

论文设置了两个模仿学习基线：

- **DP-2D**：2D 扩散策略（平均成功率 45.3%）
- **DP3**：3D 点云扩散策略（平均成功率 67.8%）

---

### 二、结果与结论

#### 2.1 主要结果（Table 1）

|任务|DP-2D|DP3|迭代离线RL|在线RL (DDIM)|在线RL (CM)|
|---|---|---|---|---|---|
|Dynamic Push-T|40%|64%|90%|**100%**|**100%**|
|Agile Bowling|14%|80%|88%|**100%**|**100%**|
|Pouring|42%|48%|92%|**100%**|**100%**|
|Soft-towel Folding|46%|68%|94%|**100%**|**100%** (250/250)|
|Dynamic Unscrewing|82%|70%|94%|**100%**|**100%**|
|Orange Juicing — Placing|78%|88%|94%|**100%**|**100%**|
|Orange Juicing — Removal|48%|76%|86%|**100%**|—*|
|Box Folding|12%|48%|96%|**100%**|**100%**|
|**平均**|**45.3%**|**67.8%**|**91.8%**|**100.0%**|**100.0%†**|

> *Juicing-Removal 因 IK 导致的位姿不连续性，未在 CM 上评估。 †7 个任务的平均值。

**关键发现**：

- 迭代离线 RL 阶段带来了最大提升，平均成功率从 67.8% 跃升至 **91.8%**
- 最难任务上的提升最为显著：Box Folding +48 分 (48%→96%)，Pouring +44 分 (48%→92%)
- 最终在线微调后，**DDIM 策略 450/450 全部成功，CM 策略 550/550 全部成功**
- Soft-towel Folding 上 CM 策略连续 **250/250 次成功**

#### 2.2 泛化与鲁棒性（Table 2）

**零样本适应 (Zero-shot Adaptation)** — 平均 90.0%：

- 倒水（颗粒→液体）：90%
- Push-T 改变表面摩擦：100%
- Push-T 加入干扰物：80%
- 保龄球改变表面：100%
- 毛巾折叠未见形状：80%
- 纸盒折叠未见形状/方向：90%

**少样本适应 (Few-shot Adaptation)** — 仅 1-3 小时微调，平均 86.7%：

- 倒水换新容器：60%
- 折叠换不同物体：100%
- 保龄球倒置球瓶：100%

**抗物理干扰 (Robustness)** — 平均 96.0%：

- 毛巾折叠被拉拽：90%
- 拧螺丝时人手反向干扰：100%
- Push-T 被拖动：100%
- 纸盒折叠被推/拉/敲：100%

#### 2.3 与人类对比

- **保龄球**：RL-100 25/25 成功 vs 人类玩家 14/25
- **商场部署**：连续 7 小时无故障榨汁服务
- **Push-T 基准**：相同时间预算下，机器人 20 次成功 vs 专家遥操作员 17 次 vs 新手 13 次

#### 2.4 核心结论

> "Across eight real-world tasks... it achieves 100% success in 1000/1000 trials. The policy generalizes across initial object placements and tolerates shape/size variations, while matching or surpassing expert teleoperators in time-to-completion."

RL-100 证明了：从少量人类示范出发，通过统一的离线到在线 RL 微调框架，可以超越人类水平的可靠性和效率，实现部署级机器人操作。

---

### 三、数学原理与公式推导

#### 3.1 扩散策略 (Diffusion Policy)

##### 3.1.1 数据表示

每个回合提供同步元组：

$$(o_t, q_t, a_t)_{t=0}^{T-1}$$

其中 $o_t$ 是视觉观测（RGB 图像或 3D 点云），$q_t$ 是机器人本体感知（关节位置/速度、夹爪状态），$a_t$ 是单步动作或动作块。

##### 3.1.2 条件编码

将最近的观测融合为条件向量：

$$c_t = [\phi(o_{t-n_f+1}, q_{t-n_f+1})]_{t-n_f+1}^{t}$$

其中 $\phi(\cdot)$ 是感知编码器，处理最近 $n_f$ 帧（通常 $n_f=2$），$[\cdot]$ 是向量拼接操作。

扩散目标 $a_t^0$ 可以是单步动作 $a_t^0 = u_t \in \mathbb{R}^{d_a}$ 或动作块 $a_t^0 = [u_t, ..., u_{t+n_c-1}] \in \mathbb{R}^{n_c d_a}$，其中 $n_c$ 是块大小（通常 8-16）。

##### 3.1.3 扩散前向过程

给定干净动作 $a_t^0$，通过 **K 步噪声调度** $\tau_K > \tau_{K-1} > ...

> \tau_1$ 逐步加噪：

$$a_t^\tau = \sqrt{\alpha_\tau} a_t^0 + \sqrt{1-\alpha_\tau} \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)$$

其中 $\alpha_\tau$ 是噪声调度参数，$\tau$ 是扩散时间步索引。

##### 3.1.4 噪声预测目标 (BC 损失)

去噪器 $\epsilon_\theta(a^\tau, \tau, c_t)$ 通过 **噪声预测目标** 训练：

$$L_{IL}(\theta) = \mathbb{E}_{(a_t^0, c_t) \sim D, \tau, \epsilon} \left[ \|\epsilon - \epsilon_\theta(a^\tau, \tau, c_t)\|^2 \right] \tag{3}$$

这是标准的扩散模型训练损失：预测添加到动作上的噪声 $\epsilon$，通过最小化均方误差来学习从噪声到动作的去噪过程。

##### 3.1.5 DDIM 采样

在推理时，使用 **DDIM (Denoising Diffusion Implicit Models)** 进行确定性采样：

$$a_t^{\tau_{k-1}} \leftarrow \text{DDIM}(\epsilon_\theta(\cdot, \cdot, c_t))$$

DDIM 将 K 步去噪过程变为确定性映射，使得每一步都有良好定义的高斯子策略，从而可以计算对数似然用于 PPO 比率。

#### 3.2 两层 MDP 结构

RL-100 的核心创新是将扩散去噪过程建模为 **层次化两层 MDP**：

**① 环境层 MDP**：标准机器人控制

- 状态 $s_t$，动作 $a_t$，奖励 $R_t$
- 每个环境时间步 $t$ 执行一个动作

**② 去噪层 MDP**：嵌入在每个环境时间步内的 K 步扩散过程

- 从纯噪声 $a_t^{\tau_K}$ 开始，经过 K 步迭代去噪得到 $a_t^0$
- K 个去噪步产生一个环境动作

这种层次结构解决了关键问题：如果只在最终动作上施加奖励，去噪链中的中间步骤无法获得学习信号，导致 **稀疏信用分配 (sparse credit assignment)**。

#### 3.3 统一的裁剪 PPO 目标

##### 3.3.1 标准 PPO 回顾

PPO (Proximal Policy Optimization) 的核心思想是 **裁剪重要性采样比率** 来防止策略更新过大：

$$J^{PPO}(\pi) = \mathbb{E}_{s \sim \rho^\pi, a \sim \pi_i} \left[ \min\left(r(\pi)A, \text{clip}(r(\pi), 1-\epsilon, 1+\epsilon)A\right) \right]$$

其中重要性比率 $r(\pi) = \frac{\pi(a|s)}{\pi_i(a|s)}$，$\pi_i$ 是当前行为策略，$A$ 是优势函数。

##### 3.3.2 RL-100 的统一 PPO 目标

RL-100 将 PPO 扩展到扩散去噪过程的每一步：

$$J_i(\pi) = \mathbb{E}_{s \sim \rho^{\pi_i}, \tau_k \sim \text{schedule}} \left[ \sum_{k=1}^K \min\left(r_k(\pi)A_t, \text{clip}(r_k(\pi), 1-\epsilon, 1+\epsilon)A_t\right) \right] \tag{7}$$

损失函数为：

$$L_{RL} = -J_i(\pi) \tag{8}$$

**关键洞察**：同一个环境层优势 $A_t$ 被共享到所有 K 个去噪步，为整个去噪链提供密集的学习信号，同时与环境奖励结构保持一致。

其中 $r_k(\pi)$ 是第 k 个去噪步的重要性比率：

$$r_k(\pi) = \frac{\pi(a^{\tau_{k-1}} | s^{\tau_k}, c_t)}{\pi_i(a^{\tau_{k-1}} | s^{\tau_k}, c_t)}$$

##### 3.3.3 在线阶段的完整损失

在线阶段使用 **GAE (Generalized Advantage Estimation)** 计算优势：

$$A_t^{\text{on}} = \text{GAE}(\lambda, \gamma; R_t, V_\psi)$$

其中 $V_\psi$ 是价值函数（从离线评论家热启动后在线更新）。

在线总损失：

$$L_{\text{on}}^{RL} = -J_i(\pi) + \lambda_V \mathbb{E}\left[(V_\psi(s_t) - \hat{V}_t)^2\right] \tag{10}$$

其中 $\hat{V}_t = \sum_{l=0}^{T-t} \gamma^l R_{t+l}$ 是折扣回报，$\lambda_V$ 是价值函数损失权重。

#### 3.4 一致性模型蒸馏 (Consistency Distillation)

##### 3.4.1 动机

K 步扩散去噪过程引入延迟，限制了高频控制。为解决此问题，RL-100 联合训练一个 **一致性模型 (Consistency Model, CM)** $f_\phi$，学习直接从噪声到动作的单步映射。

##### 3.4.2 联合优化目标

在离线或在线 RL 训练期间，增强策略优化目标：

$$L_{\text{total}}(\phi) = L_{RL} + \lambda_{CD} \cdot L_{CD} \tag{11}$$

其中 $L_{CD}$ 是一致性蒸馏损失（论文中 Equation S12），教师策略是 K 步 DDIM 扩散策略 $\pi_\theta$，学生策略是单步 CM 策略 $f_\phi$。

**停止梯度 (stop-gradient)** 操作确保教师策略通过 RL 目标持续改进，同时作为蒸馏目标。

##### 3.4.3 控制模式

- **单步控制**：$u_t \leftarrow a_t^0$ 立即执行，适合反应性任务（如动态保龄球）
- **动作块控制**：$[u_t, ..., u_{t+n_c-1}] \leftarrow a_t^0$ 在后续 $n_c$ 个时间步执行，减少精确任务中的抖动（如装配）

两种模式共享同一架构，支持任务自适应部署。

#### 3.5 训练流程总结 (Algorithm 1)

1. **Stage 1 — 模仿学习**：在人类示范数据集上通过 Equation (3) 训练扩散策略
2. **Stage 2 — 迭代离线 RL**：使用 Equation (7) 的 PPO 目标 + IQL 风格的优势函数，在离线数据集上保守优化，逐步扩展数据集
3. **Stage 3 — 在线 RL**：在真实机器人上使用 Equation (10) 的在线 PPO 目标 + GAE 进行短暂微调
4. **蒸馏**：全程使用 Equation (11) 联合训练一致性模型，实现单步高频控制

---

### 总结

RL-100 的核心贡献在于：

1. **统一框架**：将模仿学习、离线 RL 和在线 RL 统一在同一个裁剪 PPO 代理目标下，实现平滑过渡
2. **两层 MDP**：将扩散去噪过程建模为层次化 MDP，解决稀疏信用分配问题
3. **一致性蒸馏**：将多步扩散策略蒸馏为单步一致性模型，实现高频控制
4. **实证突破**：在 8 个真实任务上达到 100% 成功率，超越人类水平，并在商场连续 7 小时无故障运行