


# 三个真机 RL Proposal

## 总体说明

提出三个面向真机 RL / VLA 后训练的研究方向：

1. **Explainable Counterfactual Human-Intervention Routing**
   可解释反事实人类干预调度
2. **Intervention-Quality-Aware Diffusion Latent Steering**
   人类干预质量感知的 Diffusion Latent Steering
3. **Failure-Aware RL Token**
   面向 VLA 后训练的失败感知 RL Token


**第一个是可解释反事实人类干预调度**，核心是训练 intervention value critic，估计不同人类帮助方式的反事实收益，并在推理时根据 human cost 选择是否请求人类帮助。该方向强调 decision-level interpretability，但完整系统较重。

**第二个是人类干预质量感知的 Diffusion Latent Steering**，核心是在 DSRL 的 action critic、latent critic、latent actor 框架上加入 human intervention constraint。人类干预不作为简单 imitation loss，而是作为 latent actor 的约束，并通过 intervention quality 控制约束强度。

**第三个是 Failure-Aware RL Token**，核心是参考 RLT 的两阶段训练方式：第一阶段用 reconstruction loss 学 RL token，同时加入一个统一 risk prediction loss，让 token 显式编码未来 failure / intervention 风险；第二阶段用 actor-critic loss 训练小 RL policy，并用 VLA reference action anchor 防止 actor 偏离 VLA prior。该方向最可执行，因为它不需要从零训练 VLA，只是在 pretrained VLA 和 RLT 框架上改造 RL token 的目标。



这三个方向都围绕：
- sample-efficient real-world robot RL
- human intervention
- failure modeling
- VLA / diffusion policy post-training
- decision-level interpretability

其中，**Proposal 3：Failure-Aware RL Token** 当前最适合作为短期主线，因为它可以直接从 pretrained VLA / RLT 框架开始，不需要从零训练大模型，只需要训练轻量 token、actor-critic 和 risk head，试错成本相对较低。 meeting 中也提到，从别人训练好的 VLA 开始做，比较适合当前阶段。

---

## Proposal 1: 可解释反事实人类干预调度
**Explainable Counterfactual Human-Intervention Routing for Real-World Robot RL**

### 1. 研究动机
现有真机 RL 方法中，很多工作已经使用了 human intervention。例如 HIL-SERL 使用人类介入帮助机器人更快、更安全地学习；SiLRI 进一步指出人类介入可能是次优的，因此不能盲目模仿；SOP 则把 human intervention signals 放进多机器人在线后训练系统中。

但是，现有方法大多关注的是：**人类介入之后，机器人怎么学习？**
而没有充分回答：
- 机器人什么时候应该请求人类？
- 应该请求哪一种人类帮助？
- 如果不请求人类，会发生什么？
- 这次人类介入到底值不值？
- 机器人能不能解释为什么请求人类？

因此，这个 proposal 的核心是：
**把 human intervention 从一种被动使用的数据，变成一个主动决策、可解释、可优化的过程。**

这个方向也对应 meeting 中提出的第一个 idea：希望模型能够解释什么时候人要介入、怎么介入、不介入会发生什么，以及一次 intervention 对当前学习有什么改变。

### 2. 核心问题
真实机器人训练中，人类时间是昂贵资源。不是所有不确定状态都应该让人 full takeover。例如插孔任务中，机器人可以选择：
1. **no help**：继续自主执行
2. **label**：请求一个简单判断，例如“现在对不对”
3. **short correction**：请求人类短暂修正
4. **full takeover**：请求人类完全接管

关键问题是：什么时候不需要人？什么时候只需要 short correction？什么时候必须 full takeover？每种选择对成功率的提升是多少？

### 3. 核心想法
训练一个 **Intervention Value Critic**。
它输入当前状态，预测不同人类帮助方式下的未来成功价值：
- $V_{\text{none}}(s)$ = 不请求人类时的预期 return / success probability
- $V_{\text{label}}(s)$ = 请求 label 后的预期 return / success probability
- $V_{\text{correction}}(s)$ = 请求 short correction 后的预期 return / success probability
- $V_{\text{takeover}}(s)$ = 请求 full takeover 后的预期 return / success probability

模型最后不是直接输出“叫不叫人”，而是根据反事实价值差来决策。

### 4. 方法框架
```text
Observation + Task + Robot State
        ↓
Robot Policy π
        ↓
Candidate Action / Action Chunk
        ↓
Intervention Value Critic V_h(s)
        ↓
计算不同帮助方式的反事实收益
        ↓
选择：no help / label / short correction / full takeover
        ↓
Robot execution / Human intervention
        ↓
收集 transition，更新 policy 和 value critic
````

**输入：**

视觉观测 $o_t$、机器人状态 $s_t$、任务语言 instruction、当前 policy 输出的 action / action chunk、历史 success / failure / intervention 信息。

**输出：**

不同 intervention 方式下的成功概率、推荐 intervention 类型、不介入时的失败风险、解释信息。

### 5. 损失函数设计

这个 proposal 的 loss 参考 SiLRI 和 HIL-SERL/SAC 的风格：不要为每一种解释、每一种 intervention 单独设计 loss，而是只学习一个 value model。

#### 5.1 Intervention Value Critic Loss

对于实际执行过的帮助方式 $h$，观察到 return 或 success label $G_h$，训练：

$$L_{IVC} = \mathbb{E}[(V_h(s) - G_h)^2]$$

其中：

- $h \in \{\text{none, label, correction, takeover}\}$
    
- $G_h$ = 执行该帮助方式后的 return / success outcome
    

这是一个 value regression，形式上接近 critic 的 Bellman / TD regression，只是 value 不是单一策略价值，而是不同 intervention choice 的反事实价值。

### 6. 决策公式

训练时只学 value，不把 human cost 写进 loss。推理时使用：

$$\text{Score}(h) = V_h(s) - V_{\text{none}}(s) - \beta \text{Cost}(h)$$

选择：

$$h^* = \arg\max_h \text{Score}(h)$$

其中：

- $\text{Cost}(h)$ = 人类帮助成本
    
- $\beta$ = human cost 权重
    

这样 loss 里没有额外 cost loss，只在决策阶段考虑人类成本，调参更简单。第一阶段可以只做二分类（$h \in \{\text{none, short correction}\}$），等跑通后再扩展到多种帮助方式。

### 7. 可解释性

该方法的解释直接来自 value critic，而不是额外加 explanation loss。

例如：

> 当前状态不请求人类的成功率：18%
> 
> short correction 后成功率：63%
> 
> full takeover 后成功率：82%
> 
> 但 full takeover 人类成本更高，因此推荐 short correction。

还可以解释：

- **为什么请求人类**：当前状态接近历史 misalignment failure prototype。
    
- **为什么不是 full takeover**：当前任务还没完全失败，只需要短暂姿态修正。
    
- **如果不介入会发生什么**：critic 预测会发生 stuck-contact failure。
    

### 8. 实验设计

- **适合任务**：peg insertion, USB insertion, plug insertion, drawer opening, button pressing, cable routing
    
- **对比方法**：No intervention, Random intervention, Uncertainty-triggered intervention, Always full takeover, HIL-SERL-style intervention, Ours (intervention value routing)
    
- **评价指标**：最终成功率，达到 80% / 90% 成功率需要的 episodes，人类介入总时长，full takeover 次数，训练过程失败次数，intervention efficiency (成功率提升 / 人类时间)
    

### 9. 创新点

1. 把 human intervention 建模成一个有成本的决策，而不是简单训练数据。
    
2. 用 intervention value critic 估计不同人类帮助方式的反事实收益。
    
3. 训练 loss 保持简单，只做 value regression，cost 放在决策公式中。
    
4. 提供 decision-level explanation，解释为什么请求人类、请求哪种帮助、不请求会怎样。
    

### 10. 风险与简化版本

风险是这个 idea 偏系统，完整做多种 intervention 方式会比较复杂。

**最小可行版本**：

只做 no help vs short correction；只预测 $V_{\text{none}}$ 和 $V_{\text{correction}}$；只在插入类任务中验证。

## Proposal 2: 人类干预质量感知的 Diffusion Latent Steering

**Intervention-Quality-Aware Diffusion Latent Steering**

### 1. 研究动机

DSRL 的核心思想是：冻结 diffusion policy，不直接更新 diffusion policy 权重，而是在 diffusion 的 latent-noise space 中训练一个 RL policy，让它选择更好的 latent noise，从而 steer diffusion policy 输出更好的动作。

另一方面，HIL-SERL / SiLRI 这条线说明 human intervention 对真机 RL 很重要。人类介入能够指出：什么时候机器人快失败了；当前行为哪里不对；应该往哪个方向修正。

但现有 DSRL 主要依赖 reward 来训练 latent steering，human intervention 没有被显式用于 latent-noise policy。新的问题是能不能把 human intervention 变成 diffusion steering 的训练信号。

### 2. 核心问题

真实机器人任务中，reward 往往很稀疏，而失败前的人类 intervention 很有价值。

例如插 USB 时，机器人快要插偏，人类接管并修正。这个 intervention 说明：当前状态是 high-risk state；当前 latent noise 可能诱导 diffusion policy 生成失败动作；人类修正方向包含有价值的信息。

但是，人类 intervention 也可能是次优的、有噪声的。所以核心问题不是“直接让 diffusion policy 模仿人类动作”，而是：**如何把 human intervention 转换成 latent actor 的约束或引导信号？**

### 3. 核心想法

提出 **Intervention-Quality-Aware Diffusion Latent Steering**。

基本思路：

- 冻结 pretrained diffusion policy $\pi_{dp}$；
    
- 保留 DSRL 的 action-space critic $Q^A$；
    
- 保留 DSRL 的 latent-noise critic $Q^w$；
    
- 训练 latent-noise actor $\pi^w$；
    
- **在人类介入状态下，对 latent actor 加一个 human intervention constraint。**
    

整体仍然是 DSRL 框架，只是把 human intervention 作为 latent actor 的约束信号，而不是另起一套复杂 loss。

### 4. 方法框架

Plaintext

```
State s
  ↓
Latent-noise actor π^w(s)
  ↓
latent noise w
  ↓
Frozen diffusion policy π_dp(s, w)
  ↓
action a
  ↓
Robot execution
  ↓
reward / next state / human intervention
  ↓
Update Q^A, Q^w, π^w
```

如果发生 intervention：

- robot action: $a_{\text{robot}} = \pi_{dp}(s, w)$
    
- human correction: $a_{\text{human}}$
    
- intervention quality: $q(s)$
    

则在 latent actor 更新时，让生成动作不要偏离可信 human correction 太远。

### 5. 损失函数设计

直接参考 DSRL 的三部分，然后参考 SiLRI 把 human intervention 作为约束项加入 latent actor。

#### 5.1 Action-Space Critic

$$L_{Q^A} = \mathbb{E}[(Q^A(s, a) - y)^2]$$

其中 TD target 为：$y = r + \gamma Q^A(s', a')$

#### 5.2 Latent-Noise Critic

$$L_{Q^w} = \mathbb{E}[(Q^w(s, w) - Q^A(s, \pi_{dp}(s, w)))^2]$$

含义是：latent noise $w$ 的价值 = 它经过 frozen diffusion policy 生成 action 后，该 action 在 $Q^A$ 中的价值。

#### 5.3 Latent-Noise Actor with Human Constraint

原始 DSRL 的 latent actor 目标是：$L_{\pi^w} = \mathbb{E}[-Q^w(s, \pi^w(s))]$

我们的改法是在 intervention 样本上加入约束：

$$L_{\pi^w} = \mathbb{E} \left[ -Q^w(s, \pi^w(s)) + \lambda \cdot I_{\text{int}} \cdot q(s) \cdot d(\pi_{dp}(s, \pi^w(s)), a_{\text{human}}) \right]$$

其中：

- $I_{\text{int}} = 1$ 表示该样本发生 human intervention
    
- $q(s)$ = intervention quality（作为样本权重，不是超参数）
    
- $a_{\text{human}}$ = 人类修正动作
    
- $d(\cdot)$ = action / action chunk 距离
    
- $\lambda$ = human constraint 权重
    

$q(s)$ 可以由：intervention 后是否成功、return/critic value 是否提高、人类动作是否稳定等信息估计。它是数据中估计的 sample weight。

### 6. 这和原始 DSRL 的区别

创新点不是重新设计 DSRL，而是：**把 human intervention 作为 latent actor 的约束信号。**

### 7. 可解释性

该方法可以解释：当前 latent noise 被修改，是因为类似状态曾触发 human intervention；这次 intervention quality 较高，因为修正后任务成功；latent actor 在保证 $Q^w$ 高的同时，也靠近人类修正方向。

可输出：$Q^w$ score, intervention quality $q(s)$, latent noise shift magnitude, human constraint strength。

### 8. 实验设计

- **适合任务**：peg / USB / plug insertion, cable routing, drawer opening
    
- **对比方法**：Frozen diffusion policy, Original DSRL, DSRL + naive human imitation, DSRL + intervention constraint without quality, Ours
    
- **评价指标**：success rate, sample efficiency, failures, human intervention frequency, noisy intervention 下的鲁棒性, latent shift magnitude
    

### 9. 创新点

1. 保留 DSRL 的原始框架。
    
2. 将 human intervention 建模为 latent actor 的约束，而不是单独设计复杂 imitation loss。
    
3. 使用 intervention quality 作为样本权重，避免被次优人类操作误导。
    
4. 将 human intervention 从 action-level correction 转换为 latent-noise steering 的训练信号。
    

### 10. 风险与简化版本

这个方向工程相对更重，涉及 human intervention 如何转换成 latent signal。

**最小可行版本**：

第一阶段使用 scripted expert 代替真实人类；第二阶段只使用 high-quality correction；第三阶段再加入 intervention quality weighting。

## Proposal 3: 面向 VLA 后训练的 Failure-Aware RL Token

**Failure-Aware RL Token for Sample-Efficient VLA Post-Training**

### 1. 研究动机

RLT / RL Token 提出了一种轻量化的 VLA 后训练方式：冻结大的 VLA backbone；让 VLA 输出 compact RL token；用 token 作为小 actor-critic 的输入；在真实机器人上做 sample-efficient online RL。

但是，原始 RL Token 主要目标是提取 VLA 中对任务有用的表征。它不一定显式编码：failure risk, intervention likelihood, contact instability, value uncertainty, failure mode。

可以让 RL token 显式学习失败风险和 intervention likelihood，使小 actor-critic 更快知道哪些状态应该保守修正。

### 2. 核心问题

VLA 本身不是天然带有 failure mode 标签的。failure mode 是 VLA policy 在真实环境 rollout 中反复暴露出来的失败行为模式（如最后几毫米角度偏、接触后没有后退重试、stuck contact）。这些需要通过真实 rollout、失败轨迹、人类 intervention 等信号学出来。

### 3. 核心想法

提出 **Failure-Aware RL Token**。

基本思路：

- 冻结 pretrained VLA backbone；
    
- 训练 RL token 时，不仅重构 VLA hidden representation，还让 token 预测未来是否会失败 / 是否需要 intervention；
    
- 用该 token 训练小 actor-critic。
    

该 token 不再只是普通的 task representation，而是成为：**VLA → online RL 的 risk-aware interface**。

### 4. 方法框架

Plaintext

```
Image + Language + Robot State
        ↓
Frozen VLA Transformer Backbone
        ↓
Failure-Aware RL Token z_RL
        ↓
--------------------------------
| Critic Q_ψ                   |
| Actor π_θ                    |
| Risk Head ρ                  |
--------------------------------
        ↓
Action Chunk + Risk Explanation
```

不需要从零训练大模型，试错成本相对更低。

### 5. 损失函数设计

分两个阶段，直接参考 RL Token 结构。

#### Stage 1：训练 Failure-Aware RL Token

保留核心重构目标，加一个统一的 risk prediction 目标。

$$L_{\text{stage1}} = L_{\text{recon}} + \lambda L_{\text{risk}}$$

**Reconstruction Loss** (参考原始 RL Token)：

$$L_{\text{recon}}(\phi) = \mathbb{E}_{\mathcal{D}} \left[ \sum_{i=1}^{M} || h_\phi(d_\phi([z_{RL}, z_{i-1}]))_i - z_i ||^2 \right]$$

保证 $z_{RL}$ 保留 VLA 中已有的 task-relevant representation。

**Risk Prediction Loss**：

只预测一个 scalar risk $p_{\text{risk}} = \rho(z_{RL})$

标签 $y_{\text{risk}} = 1$ (如果未来 N 步内发生 failure 或 human intervention)，否则为 $0$。

$$L_{\text{risk}} = \text{BCE}(p_{\text{risk}}, y_{\text{risk}})$$

这同时覆盖 failure probability, intervention likelihood, high-risk contact state，不需要独立写 $L_{\text{success}}, L_{\text{intervention}}$ 等。

_(主版本设定：冻结 VLA backbone，不 fine-tune VLA，不使用原始 RLT 的 $\alpha L_{\text{vla}}$ 以降低工程复杂度。)_

#### Stage 2：训练 Actor-Critic

输入：$x_t = (z_{RL}(s_t), s_t^p)$

VLA reference action chunk：$\bar{a}_{t:t+C-1} \sim \pi_{VLA}(s_t)$

Actor action chunk：$a_{t:t+C-1} \sim \pi_\theta(x_t, \bar{a}_{t:t+C-1})$

**Critic Loss** (学习 action chunk 价值)：

$$L_Q(\psi) = \mathbb{E}_b[(\hat{Q} - Q_\psi(x, a))^2]$$

其中 $\hat{Q} = \sum_{t'=1}^{C} \gamma^{t'-1} r_{t'} + \gamma^C \mathbb{E}_{a' \sim \pi_\theta}[Q_\psi(x', a')]$

**Actor Loss** (保留 action anchor)：

$$L_\pi(\theta) = \mathbb{E}_b[-Q_\psi(x, a) + \beta ||a - \bar{a}||^2]$$

### 6. 为什么这样设计 loss？

不堆砌零散的辅助 loss（不符合真机 RL 文章风格），而是：

- Stage 1: $L_{\text{stage1}} = L_{\text{recon}} + \lambda L_{\text{risk}}$
    
- Stage 2: $L_Q$ = TD critic loss, $L_\pi = -Q + \beta$ action anchor
    
    每个阶段最多只有一个额外权重，调参简单。
    

### 7. 可解释性

可输出 $p_{\text{risk}}$ (当前状态未来 N 步内失败或需要 intervention 的概率)。

例如：当前 risk = 0.78。原因：当前状态接近历史 intervention 状态。actor 选择保守 action，因为直接执行 VLA reference action 可能导致 stuck contact。

### 8. 实验设计

- **适合任务**：USB / plug / peg / screw insertion, cable routing
    
- **对比方法**：Frozen VLA only, Original RLT, Actor-critic without risk token, Risk prediction without actor-critic, Ours
    
- **评价指标**：success rate, sample efficiency, episodes to target success rate, training failures, intervention frequency, risk prediction accuracy & calibration
    

### 9. 创新点

1. 将 RL Token 从普通 representation bottleneck 改造成 failure-aware RL interface。
    
2. 采用两阶段训练，不破坏原始 RL Token 框架。
    
3. 在 token learning 阶段加入统一 scalar risk prediction，不堆多个 auxiliary loss。
    
4. 在 actor-critic 阶段保留 VLA reference action anchor，策略不偏离 VLA prior。
    
5. 让小 actor-critic 显式知道哪些状态更容易失败或需要介入。
    

### 10. 最小可行版本

第一版只做：

- Stage 1: 训练 $z_{RL}$ 重构 VLA representation，同时预测未来 N 步 $y_{\text{risk}}$。
    
- Stage 2: 冻结 VLA 和 $z_{RL}$，训练 actor-critic，保留 VLA action anchor。
    
    暂时不做：failure type 分类、value uncertainty prediction、复杂 intervention 类型、full VLA fine-tuning。

