这是一个很好的概念性问题，我来用论文中的具体设计来阐明这两个层次的区别和联系。

---

### 高层 DP（扩散策略） vs 底层 RL（强化学习控制器）

#### 一句话区分

||**高层 DP（Planner）**|**底层 RL（Controller）**|
|---|---|---|
|**角色**|大脑——**决定做什么**|小脑——**决定怎么做**|
|**输入**|任务目标 + 环境观测（物体位置、门把手姿态等）|高层 DP 输出的命令 + 机器人本体状态|
|**输出**|**低维命令**：基座线速度 + 期望手部姿态 + 夹爪状态|**全身关节位置偏移**（29 个自由度的目标值）|
|**训练方式**|先离线模仿学习（behavior cloning），再用 DPPO 微调|纯 RL（PPO），从仿真中通过 trial-and-error 学习|
|**更新频率**|较低（规划级，~10 Hz）|较高（控制级，~50-100 Hz）|

---

#### 具体拆解

##### 底层 RL 控制器 $\pi_{\text{loco-manip}}(a_t | s_t)$

这是论文**阶段 (a)** 中预训练好的全身控制策略。它的：

- **状态空间** $s_t = [s_t^{\text{lower}}; s_t^{\text{upper}}]$：包含下半身（腿、足）和上半身（躯干、手臂）的完整本体感知信息
- **动作空间** $a_t$：**29 个关节的位置偏移量**，相对于默认姿态 $q_{\text{def}}$
- **执行方式**：目标关节位置 $q_{\text{target}} = q_{\text{def}} + a_t$ 由 **PD 控制器**跟踪
- **训练方式**：纯 RL（PPO），通过精心设计的奖励函数从零开始学习全身协调

> "The combined loco-manipulation policy is $\pi_{\text{loco-manip}}(a_t|s_t)$, where $s_t = [s_t^{\text{lower}}; s_t^{\text{upper}}]$. The resulting target joint positions, $q_{\text{target}} = q_{\text{def}} + a_t$, are tracked by proportional-derivative (PD) control." (Gu 等, 2026)

**关键点**：这个底层控制器在预训练时，接收的是**独立采样的、静态的**速度/手部命令。它学会了如何将"往前走 0.2 m/s"这样的命令转化为全身关节的协调运动。

---

##### 高层 DP（扩散策略）$\bar{\pi}_\theta(A_t^0 | S_t)$

这是论文**阶段 (b)** 中训练的规划器。它的：

- **状态块** $S_t$：包含任务相关的观测——物体位置、门把手姿态、机器人手部/脚部姿态（body frame）等
- **动作块** $A_t^0$：输出一个**动作块（action chunk）**，包含未来多个时间步的：
- **基座线速度命令**（velocity command）
- **期望手部姿态**（hand pose）
- **夹爪状态**（gripper state）
- **训练方式**：先通过扩散模型（公式 2）在 1000 条演示轨迹上做行为克隆，再通过 DPPO（公式 6）用 RL 微调

> "The DP outputs low-dimensional commands: base linear velocity and hand poses." (Gu 等, 2026)

**关键点**：高层 DP 不直接控制关节，它只输出**高层命令**。这些命令通过一个 **velocity-to-footstep planner** 转换为足部步序，再由底层 RL 控制器执行。

---

#### 为什么需要分层？

论文给出了明确的理由：

> "Unlike the independently sampled, stationary commands used during controller pre-training, DP commands represent a moving target along a continuous trajectory, creating a distribution mismatch that degrades tracking performance." (Gu 等, 2026)

**翻译**：底层控制器预训练时，接收的命令是独立采样的、静态的（比如固定速度往前走）。但高层 DP 生成的命令是**连续的、动态变化的轨迹**（比如先慢走、再转向、再伸手）。这两种命令的分布不同，导致底层控制器跟踪不准。

---

#### 联合优化（Joint Optimization）解决了什么？

论文**阶段 (c)** 的核心创新就是让两者**同时微调**：

```
算法流程（简化）：
for each iteration:
    // 1. 更新底层控制器
    DP 生成命令 → 底层执行 → 收集数据 → PPO 更新 π_loco-manip
    
    // 2. 更新高层 DP
    DP 生成命令 → 底层执行 → 收集奖励 → DPPO 更新 π_θ
```

这样做的效果是：

1. **底层控制器**学会了跟踪 DP 生成的动态命令（不再是静态命令）
2. **高层 DP** 学会了生成底层控制器能准确执行的命令
3. 两者互相适应，消除了分布不匹配

> "Joint optimization alleviates this mismatch by exposing the controller to planner-generated commands, bringing them in-distribution and substantially improving tracking accuracy." (Gu 等, 2026)

---

#### 一个直观类比

想象你在教一个人跳舞：

|层次|类比|具体在本论文中|
|---|---|---|
|**高层 DP**|编舞师——决定"先向左迈两步，再转身，然后伸手"|输出基座速度 + 手部姿态|
|**底层 RL**|舞者——把编舞师的指令转化为具体的肌肉协调|输出 29 个关节的位置偏移|
|**velocity-to-footstep planner**|舞者的"步法转换器"——把"向左走"转化为具体的脚步序列|将速度命令转为足部步序|
|**联合优化**|编舞师和舞者一起排练——编舞师调整动作使其可执行，舞者学习适应编舞师的风格|两者同时微调，互相适应|

---

**总结**：高层 DP 是**决策层**（决定去哪、做什么动作），输出低维命令；底层 RL 是**执行层**（如何协调全身关节去执行命令），输出高维关节位置。两者通过联合优化互相适应，这是 REFINE-DP 从预训练的 50-70% 成功率提升到 97-99% 的关键原因。