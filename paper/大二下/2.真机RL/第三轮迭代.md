

---

# 1 Explainable Human-Intervention Routing

## 题目可以叫

**Explainable Counterfactual Human-Intervention Routing for Real-World Robot RL**

中文：

**面向真机 RL 的可解释反事实人类干预调度**

---

## 核心问题

现在 HIL-SERL、SiLRI、SOP 这类方法都用了 human intervention，但大多只回答：

> 人类介入之后，机器人怎么学？

但没有很好回答：

> 为什么这个时候需要人类介入？  
> 为什么需要 full takeover，而不是只要一个 label？  
> 如果不让人介入，会发生什么？  
> 这次 intervention 对学习到底有多大价值？

这正好可以变成可解释性。

---

## 核心 idea

机器人不只是学一个 policy，还学一个 **intervention value model**。

它对当前状态输出几个可解释量：

```text
P_success_without_help
P_success_with_help
Expected improvement
Human cost
Failure reason
Recommended help type
```

比如机器人在插孔任务里快失败时，它不是直接叫人，而是输出：

```text
当前失败风险：高
主要风险原因：插头角度偏差过大
如果不介入：成功率约 18%
如果请求短 correction：成功率预计提升到 63%
如果 full teleoperation：成功率预计提升到 82%，但人类成本更高
推荐：请求 short correction
```

这个解释非常自然，而且和决策绑定，不是后处理可视化。

---

## 方法框架

```text
Observation
   ↓
Robot Policy
   ↓
Intervention Value Critic
   ↓
输出：
  1. 当前成功概率
  2. 当前失败类型
  3. 是否需要人类介入
  4. 应该请求哪种人类帮助
  5. 反事实解释：如果不介入会怎样
   ↓
Robot execution / Human intervention
   ↓
Update policy + intervention critic
```

---

## 这里的可解释性是什么？

不是简单说“attention map 看哪里”，而是 **decision-level explanation**：

### 第一，解释为什么请求人类

例如：

```text
机器人请求人类介入，因为当前状态和过去的 misalignment failure prototype 很接近。
```

### 第二，解释请求哪种帮助

例如：

```text
当前不是完全失败，只需要方向修正，因此请求 short correction，而不是 full takeover。
```

### 第三，解释反事实结果

例如：

```text
如果继续自主执行，critic 预测会发生插入卡住；如果人类调整末端角度，成功概率会显著提高。
```

### 第四，解释人类干预价值

例如：

```text
这次 intervention 的预计收益高，因为它位于任务成功/失败分界附近。
```

---

## 为什么这个 idea 比原版更强？

原版是：

> 什么时候叫人介入？

现在变成：

> 什么时候叫人介入，并且机器人能解释为什么叫人、叫人做什么、不叫人会怎样。

这就同时有：

```text
sample efficiency
human cost reduction
safety
interpretability
```



---
# 
# 2 用人类干预信号去指导 diffusion policy 的 latent steering



---

## 现有工作怎么做？

**DSRL** 冻结 diffusion policy，不改原来的 policy 权重，而是在 diffusion 的 latent-noise space 上训练一个 RL policy，让它选择更好的 latent noise，从而 steer diffusion policy 输出更好的动作。([arXiv](https://arxiv.org/abs/2506.15799?utm_source=chatgpt.com "Steering Your Diffusion Policy with Latent Space ..."))

**HIL-SERL / SiLRI** 这条线主要研究 human intervention。HIL-SERL 用人类介入帮助真机 RL 更快更安全；SiLRI 进一步指出，人类 intervention 不是总是最优的，所以要处理 suboptimal intervention。([arXiv](https://arxiv.org/abs/2512.24288?utm_source=chatgpt.com "Real-world Reinforcement Learning from Suboptimal Interventions"))

但是这两条线还可以产生一个结合点：

```text
DSRL：在 diffusion latent-noise space 里做 RL
HIL-SERL / SiLRI：利用 human intervention/correction
        ↓
新的问题：
能不能把 human intervention 变成 diffusion steering 的训练信号？
```

---

## 你可以提出的问题

现有 DSRL 主要依赖 reward 来学 latent steering，但真实机器人里 sparse reward 很慢，而且失败前的状态很有价值。人类 intervention 恰好指出了：

> policy 在什么状态下快失败了，以及应该往哪个方向修正。

但是，如果直接模仿 human intervention，又会遇到 SiLRI 提到的问题：人类干预可能是次优的、有噪声的。([arXiv](https://arxiv.org/abs/2512.24288?utm_source=chatgpt.com "Real-world Reinforcement Learning from Suboptimal Interventions"))

所以可以提出：

> 能否学习一个 **intervention-aware latent steering policy**，在 diffusion policy 的 latent-noise space 里利用人类干预信号，同时根据 intervention 的不确定性决定它对 RL 更新的影响强度？

---

## 方法可以怎么设计？

核心结构：

```text
Frozen Diffusion Policy
        ↓
latent noise z
        ↓
Steering Policy π_s(z | obs, task, intervention confidence)
        ↓
Diffusion denoising
        ↓
action
        ↓
robot rollout
        ↓
reward + intervention signal + failure signal
```

关键不是简单加 human data，而是设计三个信号：

### 1. Intervention trigger signal

什么时候人类介入？  
这个状态可以被标记为 **high-risk state**。

### 2. Intervention quality signal

人类介入不一定最优，所以不能直接全权模仿。可以参考 SiLRI 的思路，用 intervention uncertainty / critic disagreement / action consistency 来估计这次 intervention 的可信度。([arXiv](https://arxiv.org/abs/2512.24288?utm_source=chatgpt.com "Real-world Reinforcement Learning from Suboptimal Interventions"))

### 3. Latent steering loss

不是直接让最终 action 模仿人类，而是让 latent noise steering 产生更安全、更接近成功轨迹的 action distribution。

---

## 这个 idea 的一句话版本

> Existing DSRL steers diffusion policies with RL in latent-noise space, but it does not explicitly use human intervention signals. Existing HIL-SERL and SiLRI use human corrections, but not at the diffusion latent interface. We propose intervention-aware diffusion steering, where human intervention marks high-risk states and guides latent-noise RL with uncertainty-aware weighting.

中文可以说：

> 现有 DSRL 是 reward-driven latent steering，但没有充分利用人类干预；HIL-SERL 和 SiLRI 有人类干预，但没有把干预用在 diffusion latent space 上。我们想做人类干预感知的 diffusion steering，让人类干预既能指出失败区域，又不会因为人类次优操作而限制 RL 的最终性能。

---

## 这个 idea 的优点

它能把你读过的几条线连起来：

```text
DSRL：diffusion latent-noise RL
HIL-SERL：human-in-the-loop real-world RL
SiLRI：suboptimal intervention
RL-100：diffusion policy + real-world RL
```

这个方向比较像一个真正的“交叉点”，不是简单 A+B。

---

## 风险

风险是：你需要确认有没有已经有人把 human intervention 和 DSRL 直接结合。现在从公开结果看，DSRL 强调的是 latent-noise RL，SiLRI 强调的是 suboptimal human intervention，但二者的结合还不是主线。这个方向值得继续查重。([arXiv](https://arxiv.org/abs/2506.15799?utm_source=chatgpt.com "Steering Your Diffusion Policy with Latent Space ..."))

---
# 3 Failure-Aware RL Token

## 让 RL Token 不只压缩 VLA 表征，还显式编码失败风险

这个方向也很适合你，因为你刚刚读了 RLT / RL Token。

---

## 现有工作怎么做？

RLT 的核心是：冻结大的 VLA，让 VLA 输出一个 compact **RL token**，再用这个 token 作为小 actor-critic 的输入做在线 RL。这样可以避免直接 fine-tune 大 VLA，几分钟到几小时内提升精密操作。([物理智能](https://www.pi.website/research/rlt?utm_source=chatgpt.com "Precise Manipulation with Efficient Online RL"))

但是它有一个潜在问题：

> RL token 是为了保留 VLA 内部 task-relevant representation，但它不一定专门编码“失败风险”“接触状态”“什么时候需要人类介入”。

也就是说，RLT 的 token 可能对任务语义很强，但对真机 RL 中最关键的 **failure mode** 不一定足够敏感。

---

## 你可以提出的问题

精密操作的失败通常不是因为 VLA 完全不知道任务，而是因为最后几毫米的 contact、alignment、force、slippage、occlusion 等细节处理不好。

所以可以问：

> 能不能训练一个 **failure-aware RL token**，让 token 显式包含失败风险、intervention likelihood、critic uncertainty，而不仅仅是压缩 VLA embedding？

---

## 方法可以怎么设计？

在原来的 RL token 之外，加入一个 failure-aware auxiliary head：

```text
VLA backbone
    ↓
RL Token
    ↓
actor-critic

同时加辅助预测：
    1. success probability
    2. intervention probability
    3. failure type
    4. value uncertainty
```

训练信号可以来自：

```text
successful rollout
failed rollout
human intervention segment
critic TD error
contact-rich transition
```

这样 actor-critic 不只是知道“现在看到什么”，还知道：

> 这个状态是不是快失败了？  
> 失败大概率是哪一类？  
> 需不需要更保守地跟随 VLA prior？  
> 还是可以大胆探索？

---

## 一句话版本

> RLT uses an RL token as a compact interface for online RL, but the token is not explicitly optimized for failure prediction or intervention awareness. We propose a failure-aware RL token that encodes success probability, intervention risk, and value uncertainty to improve sample-efficient real-world fine-tuning.

中文可以说：

> RLT 的 token 是 VLA 到 RL 的接口，但这个接口不一定知道机器人什么时候快失败。我们想让 RL token 显式学习失败风险和 intervention likelihood，使小 actor-critic 在真实机器人精密操作中更快知道哪些状态值得探索，哪些状态应该保守修正。

---

## 和已有工作的区别

它不是重新做 RLT，而是改 RLT 的 bottleneck 目标：

```text
原 RLT：
RL token reconstructs useful VLA representations

你的 idea：
RL token also predicts failure/intervention/value-risk information
```

---

## 风险

这个方向的风险是：如果只是“加一个 failure prediction head”，可能显得太小。要让它更像论文，需要强调：

> token design 决定了 frozen VLA 能否被小 RL head 有效利用。

也就是说，贡献不是一个 auxiliary loss，而是：

**面向真实机器人后训练的 RL interface design。**

---
