三个 Day4 split 实验都跑完了。

总体结论很清楚：

> `z_n` 确实能学到噪声类型；但 λ 越大，noise 分类越强，disease 分类会下降。当前最平衡的是 `λ=0.1`。

结果表：

| Model | Disease AUROC | Disease AUPRC | Disease F1 | Noise Acc | Noise Macro-F1 |
|---|---:|---:|---:|---:|---:|
| Baseline CNN | 0.9040 test / 0.9089 val | 0.7610 test | 0.6654 test | - | - |
| Split λ=0.05 | 0.9040 | 0.7596 | 0.6691 | 0.6853 | 0.6803 |
| Split λ=0.1 | 0.9012 | 0.7594 | 0.6686 | 0.9047 | 0.9020 |
| Split λ=0.2 | 0.8917 | 0.7373 | 0.6588 | 0.9409 | 0.9424 |

注意：split 这里是 validation 上的结果；baseline test/val 我都列出来方便对比。

我建议选 `λ=0.1` 作为 Day4 主结果。它的 disease AUROC 只从 baseline val `0.9089` 降到 `0.9012`，还能把 noise accuracy 做到 `0.9047`，说明 `z_n` 是有用的。

`λ=0.1` 的 confusion matrix 也很好：

```text
clean:             309 / 325 correct
baseline_wander:   373 / 380 correct
gaussian:          365 / 371 correct
muscle:            358 / 384 correct
lead_dropout:      308 / 358 correct
amplitude_scaling: 262 / 365 correct
```

主要混淆是：

```text
amplitude_scaling → clean
lead_dropout → clean
muscle ↔ gaussian 少量混淆
```

这个也合理：amplitude scaling 比较像 clean，只是幅值变了；部分轻度 lead dropout 也可能和 clean 接近。

可以给导师这样汇报：

> 我训练了 `z_p/z_n` split model，用 `z_p` 做疾病分类，用 `z_n` 预测人工噪声类型。λ=0.1 时 disease AUROC 为 0.9012，接近 baseline，同时 noise accuracy 达到 0.9047，noise macro-F1 为 0.9020。这说明在不显著破坏疾病分类的情况下，`z_n` 可以学习到噪声状态，初步回答了噪声能否被分出来的问题。