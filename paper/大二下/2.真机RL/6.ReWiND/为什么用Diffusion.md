这是一个很好的问题。从论文的数学框架来看，选择扩散模型（DDPM-based Diffusion Policy）而非流匹配（Flow Matching），主要有以下几个原因：

### 1. 历史背景与生态成熟度

论文发表于 2026 年，其核心方法 DPPO（Diffusion Policy Policy Optimization）直接继承自 **Diffusion Policy [6]** 这一开创性工作。扩散策略在机器人领域的应用（2023-2024）远早于流匹配在生成式策略中的普及。论文的基线对比中也使用了标准的 DiT（Diffusion Transformer）架构，说明整个实验体系建立在扩散模型生态之上。

### 2. 增强 MDP 框架的天然适配性

这是最关键的数学原因。DPPO 的核心创新是将去噪过程嵌入环境 MDP 中，构造**增强 MDP** $\bar{\mathcal{M}}$。这个构造依赖于去噪过程的**马尔可夫链结构**：

$$q(A_t^k | A_t^{k-1}) = \mathcal{N}\left(\sqrt{\alpha_k} A_t^{k-1}, (1-\alpha_k)I\right) \tag{1}$$

这个前向过程是一个**离散时间马尔可夫链**，其反向过程 $p_\theta(A_t^{k-1} | A_t^k, S_t)$ 也是高斯分布，因此：

- **转移概率可解析计算**：增强 MDP 中 $k > 0$ 的转移是确定性的 Dirac 分布 $\delta_{S_t, A_t^k}$，因为去噪步的转移分布是已知的高斯形式
- **对数似然可求**：$\log \bar{\pi}_\theta(\bar{a}_{\bar{t}} | \bar{s}_{\bar{t}}) = \log p_\theta(A_t^k | A_t^{k+1}, S_t)$ 可以直接计算，这是策略梯度方法（公式 6）的核心要求

流匹配虽然也能生成动作，但其**概率路径（probability path）**通常通过连续常微分方程（ODE）定义：

$$\frac{dA_t}{dt} = v_\theta(A_t, t)$$

在流匹配中，从 $A_0$ 到 $A_1$ 的路径是连续的、确定性的（给定噪声），其条件概率 $p_\theta(A_{t-\Delta t} | A_t)$ 不像扩散模型那样有解析的高斯形式。这意味着在增强 MDP 中，去噪步的转移概率 $\bar{\pi}_\theta(\bar{a}_{\bar{t}} | \bar{s}_{\bar{t}})$ 无法直接计算，**PPO 所需的似然比（likelihood ratio）就无法获得**。

### 3. 离散去噪步与 MDP 时间步的自然对齐

扩散模型的去噪过程天然是**离散的**（$K$ 步），这与 MDP 的离散时间步结构完美对齐。增强 MDP 的统一时间步索引为：

$$\bar{t}(t, k) = tK + (K - 1 - k)$$

每个环境时间步 $t$ 内部嵌入 $K$ 个去噪步。流匹配的连续时间路径需要离散化才能嵌入 MDP，这会引入额外的近似误差和实现复杂度。

### 4. 噪声预测目标的简洁性

扩散模型的训练目标（公式 2）极其简洁：

$$\mathcal{L}_{\text{diff}}(\theta) = \mathbb{E}_{A_t^0, S_t, k, \varepsilon}\left[ \|\varepsilon - \varepsilon_\theta(A_t^k, S_t, k)\|^2 \right] \tag{2}$$

这个 L2 噪声预测损失在微调阶段与 DPPO 的策略梯度目标（公式 6）可以无缝衔接——DP 的参数 $\theta$ 既通过噪声预测损失预训练，又通过策略梯度微调，两种优化共享同一个网络结构 $\varepsilon_\theta$。

流匹配的损失函数通常涉及**速度场回归**：

$$\mathcal{L}_{\text{FM}}(\theta) = \mathbb{E}_{t, A_0, A_1}\left[ \|v_\theta(A_t, t) - (A_1 - A_0)\|^2 \right]$$

虽然形式上也类似，但流匹配的推理需要通过 ODE 求解器进行数值积分，这在 RL 微调的 rollout 过程中会引入额外的计算开销和数值误差。

### 5. 总结：核心原因

|维度|扩散模型 (DDPM)|流匹配|
|---|---|---|
|**转移概率**|解析高斯分布，可计算 $log pi_theta$|连续 ODE，概率密度难解析计算|
|**时间结构**|离散 $K$ 步，天然对齐 MDP|连续时间，需离散化|
|**DPPO 适配**|✅ 增强 MDP 的似然比可直接计算|❌ 无法直接计算策略梯度所需的对数似然|
|**生态成熟度**|Diffusion Policy 已是机器人领域标准|在策略微调中尚未建立类似 DPPO 的框架|

**一句话总结**：扩散模型的离散马尔可夫链结构使得增强 MDP 中的每个去噪步的转移概率可解析计算，这是 DPPO 能够将 PPO 应用于隐式策略的核心前提。流匹配的连续 ODE 路径不具备这一性质，因此无法直接套用 DPPO 框架。