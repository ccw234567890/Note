PTB-XL 下载下来之后，核心结构很清楚：**两个 CSV 元数据文件 + 两套 ECG 波形文件夹**。

官方页面给出的数据结构大概是这样：([PhysioNet](https://physionet.org/content/ptb-xl/1.0.3/ "PTB-XL, a large publicly available electrocardiography dataset v1.0.3"))

```text
ptb-xl/
├── ptbxl_database.csv
├── scp_statements.csv
├── records100/
│   ├── 00000/
│   │   ├── 00001_lr.dat
│   │   ├── 00001_lr.hea
│   │   ├── ...
│   │   ├── 00999_lr.dat
│   │   └── 00999_lr.hea
│   ├── ...
│   └── 21000/
│       ├── 21001_lr.dat
│       ├── 21001_lr.hea
│       ├── ...
│       └── 21837_lr.hea
└── records500/
    ├── 00000/
    │   ├── 00001_hr.dat
    │   ├── 00001_hr.hea
    │   ├── ...
    │   └── 00999_hr.hea
    ├── ...
    └── 21000/
        ├── 21001_hr.dat
        ├── 21001_hr.hea
        ├── ...
        └── 21837_hr.hea
```

---

## 1. `records100/` 和 `records500/` 是 ECG 波形

这两个文件夹里面放的是 ECG 原始波形，都是 **WFDB 格式**。

每条 ECG 一般对应两个文件：

```text
00001_lr.dat
00001_lr.hea
```

或者：

```text
00001_hr.dat
00001_hr.hea
```

含义是：

|文件|含义|
|---|---|
|`.dat`|真正的 ECG 波形二进制数据|
|`.hea`|header 文件，记录采样率、导联名、信号长度等信息|

区别是：

|文件夹|采样率|文件名后缀|建议用途|
|---|--:|---|---|
|`records100/`|100 Hz|`_lr`|先跑 baseline / prototype|
|`records500/`|500 Hz|`_hr`|后续正式实验 / 更高精度|

官方说明 `records500/` 是 500 Hz，`records100/` 是下采样到 100 Hz 的版本，波形是 16-bit precision、1μV/LSB。([PhysioNet](https://physionet.org/content/ptb-xl/1.0.3/ "PTB-XL, a large publicly available electrocardiography dataset v1.0.3"))

你现在第一版建议用：

```text
records100/
```

因为 10 秒 ECG 在 100 Hz 下是：

```text
12 leads × 1000 points
```

而 500 Hz 下是：

```text
12 leads × 5000 points
```

训练速度差很多。

---

## 2. 一条 ECG 读出来是什么 shape？

如果用 `wfdb` 读取一条 100Hz ECG：

```python
import wfdb

record = wfdb.rdsamp("ptb-xl/records100/00000/00001_lr")
signal = record[0]
meta = record[1]

print(signal.shape)
print(meta["sig_name"])
```

通常 `signal.shape` 是：

```text
(1000, 12)
```

意思是：

```text
1000 个时间点 × 12 个导联
```

如果你训练 PyTorch 模型，一般会转成：

```text
(12, 1000)
```

也就是：

```python
signal = signal.T
```

对于 `records500/`：

```text
(5000, 12)
```

转置后：

```text
(12, 5000)
```

---

## 3. 12 个导联有哪些？

PTB-XL 提供标准 12 导联 ECG，官方页面列出的是：I、II、III、AVL、AVR、AVF、V1 到 V6。([PhysioNet](https://physionet.org/content/ptb-xl/1.0.3/ "PTB-XL, a large publicly available electrocardiography dataset v1.0.3"))

一般代码里会看到：

```text
I, II, III, aVR, aVL, aVF, V1, V2, V3, V4, V5, V6
```

所以一条样本可以理解为：

```text
X ∈ R^{12 × 1000}   # records100
```

或者：

```text
X ∈ R^{12 × 5000}   # records500
```

---

## 4. `ptbxl_database.csv` 是最重要的元数据表

这个 CSV 是主表，**一行对应一条 ECG 记录**。官方说明它有 28 个 columns，每条记录用 `ecg_id` 标识，并包含路径、人口统计信息、诊断标签、信号质量和推荐划分 fold 等。([PhysioNet](https://physionet.org/content/ptb-xl/1.0.3/ "PTB-XL, a large publicly available electrocardiography dataset v1.0.3"))

最重要的字段有这些：

|字段|作用|
|---|---|
|`ecg_id`|每条 ECG 的唯一 ID|
|`patient_id`|患者 ID|
|`age`|年龄|
|`sex`|性别|
|`height`|身高|
|`weight`|体重|
|`scp_codes`|最核心标签字段，SCP-ECG 诊断 statement|
|`report`|原始诊断报告文本|
|`filename_lr`|100Hz 文件路径|
|`filename_hr`|500Hz 文件路径|
|`strat_fold`|官方推荐 10-fold 划分|
|`heart_axis`|心电轴|
|`infarction_stadium1/2`|心梗阶段信息|
|`static_noise`|静态噪声标注|
|`burst_noise`|突发噪声标注|
|`baseline_drift`|基线漂移标注|
|`electrodes_problems`|电极问题|
|`extra_beats`|额外搏动|
|`pacemaker`|起搏器相关标记|

对你这个项目最有用的是：

```text
scp_codes
filename_lr
filename_hr
strat_fold
static_noise
burst_noise
baseline_drift
electrodes_problems
```

尤其是后面几个 signal metadata，和你想做的 (z_n)、noise/domain prototype 很相关。官方说明 PTB-XL 的信号元数据包括噪声、baseline drifts、电极问题、额外搏动和 pacemaker 等。([PhysioNet](https://physionet.org/content/ptb-xl/1.0.3/ "PTB-XL, a large publicly available electrocardiography dataset v1.0.3"))

---

## 5. `scp_codes` 是标签，但不是直接可用的 5 类标签

`scp_codes` 长这样：

```text
{'NORM': 100.0, 'LVOLT': 0.0, ...}
```

它是一个字典，表示这条 ECG 有哪些 SCP-ECG statement，以及对应 likelihood。

PTB-XL 总共有 **71 个 SCP-ECG statements**，覆盖 diagnostic、form、rhythm 三类 statement。官方摘要也说明每条记录可能有多个 ECG statements，所以它天然是 multi-label 数据集。([PhysioNet](https://physionet.org/content/ptb-xl/1.0.3/ "PTB-XL, a large publicly available electrocardiography dataset v1.0.3"))

但是常见 ECG 分类不直接用 71 类，而是聚合成 5 个 diagnostic superclasses。

---

## 6. `scp_statements.csv` 是标签映射表

这个文件用于解释 `scp_codes` 里每个 statement 的含义。

它会告诉你：

|信息|作用|
|---|---|
|statement 描述|这个 code 是什么诊断/形态/节律|
|`diagnostic`|是否属于诊断标签|
|`form`|是否属于形态标签|
|`rhythm`|是否属于节律标签|
|`diagnostic_class`|诊断大类|
|`diagnostic_subclass`|诊断子类|

官方说明 `scp_statements.csv` 存储 annotation scheme，并提供 category，以及 diagnostic statement 的 `diagnostic_class` 和 `diagnostic_subclass` 层级组织。([PhysioNet](https://physionet.org/content/ptb-xl/1.0.3/ "PTB-XL, a large publicly available electrocardiography dataset v1.0.3"))

---

## 7. 常用的 5 个诊断大类

最常用的是 5 个 diagnostic superclass：

|类别|含义|官方记录数|
|---|---|--:|
|`NORM`|Normal ECG|9514|
|`MI`|Myocardial Infarction|5469|
|`STTC`|ST/T Change|5235|
|`CD`|Conduction Disturbance|4898|
|`HYP`|Hypertrophy|2649|

官方也提醒：这些数字相加会超过总记录数，因为一条 ECG 可以有多个标签。([PhysioNet](https://physionet.org/content/ptb-xl/1.0.3/ "PTB-XL, a large publicly available electrocardiography dataset v1.0.3"))

所以你做模型时，最好按 **multi-label classification** 处理，而不是普通 single-label softmax。

也就是输出：

```text
[NORM, MI, STTC, CD, HYP]
```

每一类一个 sigmoid。

---

## 8. 官方推荐 train / val / test 划分

`ptbxl_database.csv` 里有：

```text
strat_fold
```

官方提供 10-fold split，并且保证同一个 patient 的记录不会被分到不同 fold。官方建议：fold 1-8 做 train，fold 9 做 validation，fold 10 做 test。([PhysioNet](https://physionet.org/content/ptb-xl/1.0.3/ "PTB-XL, a large publicly available electrocardiography dataset v1.0.3"))

你第一版可以直接用：

```text
train: strat_fold 1-8
val:   strat_fold 9
test:  strat_fold 10
```

这样比较标准，也方便以后和 baseline 对比。

---

## 9. 这个数据集对你项目最有用的地方

对你的 **APT + Koopman ECG 分类** 项目来说，PTB-XL 可以这样用：

### 输入

```text
X = ECG waveform
shape = [12, 1000]  # records100
```

### 标签

先做 5 类 diagnostic superclass：

```text
NORM, MI, STTC, CD, HYP
```

### 噪声/域信息

可以先利用这些字段辅助分析 (z_n)：

```text
static_noise
burst_noise
baseline_drift
electrodes_problems
```

这对你验证 (z_n) 是否学到了 noise representation 很有帮助。

### 划分

```text
fold 1-8 train
fold 9 val
fold 10 test
```

---

## 10. 最小可用版本

你现在要快速开始，不要一上来处理所有字段。

最小版本只需要：

```text
records100/
ptbxl_database.csv
scp_statements.csv
```

然后从 `ptbxl_database.csv` 里取：

```text
filename_lr
scp_codes
strat_fold
```

构建：

```text
X: ECG waveform, [12, 1000]
y: 5-class multi-label vector, [5]
```

第一版任务：

```text
12-lead ECG → NORM / MI / STTC / CD / HYP
```

然后你再逐步加入：

```text
static_noise
burst_noise
baseline_drift
electrodes_problems
```

用来验证 (z_n) 和 prototype 是否真的对应噪声/信号质量。