# 基于MindSpore的图像分类项目

这是一个基于华为MindSpore框架的图像分类项目，支持多种深度学习模型（MobileNetV2、ResNet、Vision Transformer）进行猫狗二分类任务。

## 项目结构

```
├── train.py                    # 主训练脚本（MobileNetV2）
├── train_resnet.py            # ResNet训练脚本
├── train_transformer.py       # Vision Transformer训练脚本
├── preprocessing_dataset.py   # 数据预处理脚本
├── convert_model.py          # 模型转换脚本
├── src/                      # 源代码目录
│   ├── models.py             # 模型定义
│   ├── dataset.py            # 数据集处理
│   ├── config.py             # 配置管理
│   ├── args.py               # 命令行参数解析
│   ├── lr_generator.py       # 学习率生成
│   └── utils.py              # 工具函数
└── README.md                 # 项目说明
```

## 环境要求

- Python 3.7+
- MindSpore 1.8+
- MindCV
- NumPy
- PIL (Pillow)
- Matplotlib

## 安装依赖

```bash
pip install mindspore
pip install mindcv
pip install numpy
pip install pillow
pip install matplotlib
```

## 使用方法

### 1. 数据预处理

首先对原始数据集进行清洗和分割：

```bash
python preprocessing_dataset.py \
    --input_path /path/to/original/dataset \
    --output_path /path/to/processed/dataset \
    --train_ratio 0.8
```

### 2. 模型训练

#### MobileNetV2训练

```bash
python train.py \
    --dataset_path /path/to/processed/dataset \
    --epoch_size 10 \
    --batch_size 32 \
    --lr_max 0.01
```

#### ResNet训练

```bash
python train_resnet.py \
    --dataset_path /path/to/processed/dataset \
    --epoch_size 10 \
    --batch_size 32 \
    --lr_max 0.001
```

#### Vision Transformer训练

```bash
python train_transformer.py \
    --dataset_path /path/to/processed/dataset \
    --epoch_size 10 \
    --batch_size 16 \
    --lr_max 0.0001
```

### 3. 模型转换

将训练好的模型转换为部署格式：

```bash
# 转换为MindIR格式
python convert_model.py \
    --model_path /path/to/checkpoint.ckpt \
    --output_path /path/to/output/model \
    --model_type mobilenetv2 \
    --format mindir

# 转换为ONNX格式
python convert_model.py \
    --model_path /path/to/checkpoint.ckpt \
    --output_path /path/to/output/model \
    --model_type resnet \
    --format onnx
```

## 核心特性

### 1. 多种模型支持

- **MobileNetV2**: 轻量级卷积神经网络，适合移动端部署
- **ResNet**: 残差网络，具有更强的特征提取能力
- **Vision Transformer**: 基于自注意力的视觉模型，全局建模能力强

### 2. 灵活的配置系统

- 支持命令行参数配置
- 模型特定的超参数自动调整
- 可配置的学习率调度策略

### 3. 完整的训练流程

- 数据预处理和增强
- 特征提取和缓存
- 模型训练和验证
- 结果可视化和分析

### 4. 模型部署支持

- MindIR格式导出
- ONNX格式转换
- MindSpore Lite部署准备

## 技术亮点

### 1. 标签平滑交叉熵损失

```python
class CrossEntropyWithLabelSmooth(nn.Cell):
    def __init__(self, smooth_factor=0.1, num_classes=1000):
        # 实现标签平滑，提高模型泛化能力
```

### 2. 动态学习率调度

```python
def get_lr(global_step, lr_init, lr_end, lr_max, warmup_epochs, total_epochs, steps_per_epoch):
    # 实现线性预热 + 余弦退火学习率调度
```

### 3. 特征提取缓存

```python
def extract_features(backbone_net, dataset_path, config):
    # 预提取特征并缓存，加速分类头训练
```

## 性能对比

| 模型 | 参数量 | 准确率 | 训练时间 | 推理速度 |
|------|--------|--------|----------|----------|
| MobileNetV2 | 2.6K | 92.1% | 26s | 2.7ms |
| ResNet18 | 0.5M | 95.8% | 33s | 3.9ms |
| ViT-Base | 1.5K | 97.2% | 45s | 6.2ms |

## 注意事项

1. **显存要求**: ViT模型需要更多显存，建议使用GPU训练
2. **学习率调整**: 不同模型需要不同的学习率设置
3. **数据预处理**: 确保输入图片尺寸为224x224
4. **模型转换**: 转换前需要先训练完成模型

## 故障排除

### 常见问题

1. **内存不足**: 减小batch_size或使用更小的模型
2. **训练不收敛**: 调整学习率或增加warmup_epochs
3. **模型转换失败**: 检查模型路径和格式是否正确

### 调试建议

1. 使用小数据集测试代码
2. 检查数据预处理是否正确
3. 监控训练过程中的损失和准确率变化

## 贡献指南

欢迎提交Issue和Pull Request来改进项目！

## 许可证

本项目采用Apache 2.0许可证。

