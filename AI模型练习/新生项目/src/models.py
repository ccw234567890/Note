# Copyright 2020 Huawei Technologies Co., Ltd
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

"""Model definitions for image classification."""

import mindspore as ms
import mindspore.nn as nn
from mindspore import Tensor
from mindspore.ops import operations as P
from mindspore.train.callback import Callback
from mindspore.train.serialization import load_checkpoint, load_param_into_net
from mindcv.models import create_model

class CrossEntropyWithLabelSmooth(nn.Cell):
    """Cross entropy with label smoothing."""
    
    def __init__(self, smooth_factor=0.1, num_classes=1000):
        super(CrossEntropyWithLabelSmooth, self).__init__()
        self.onehot = P.OneHot()
        self.on_value = Tensor(1.0 - smooth_factor, mindspore.float32)
        self.off_value = Tensor(1.0 * smooth_factor / (num_classes - 1), mindspore.float32)
        self.ce = nn.SoftmaxCrossEntropyWithLogits()
        self.mean = P.ReduceMean(False)
        self.cast = P.Cast()

    def construct(self, logits, label):
        if label.size == 1:
            label = self.cast(label, mindspore.int32)
            one_hot_label = self.onehot(label, logits.shape[1], self.on_value, self.off_value)
        else:
            one_hot_label = label
        loss_logits = self.ce(logits, one_hot_label)
        loss_logits = self.mean(loss_logits, 0)
        return loss_logits


class Monitor(Callback):
    """Monitor training process."""
    
    def __init__(self, lr_init=None, lr_end=None, warmup_epochs=0, 
                 total_epochs=0, steps_per_epoch=0, ckpt_dir=None):
        super(Monitor, self).__init__()
        self.lr_init = lr_init
        self.lr_end = lr_end
        self.warmup_epochs = warmup_epochs
        self.total_epochs = total_epochs
        self.steps_per_epoch = steps_per_epoch
        self.ckpt_dir = ckpt_dir

    def begin(self, run_context):
        self.lr_init = self.lr_init
        self.lr_end = self.lr_end
        self.warmup_epochs = self.warmup_epochs
        self.total_epochs = self.total_epochs
        self.steps_per_epoch = self.steps_per_epoch

    def epoch_begin(self, run_context):
        cb_params = run_context.original_args()
        epoch_num = cb_params.cur_epoch_num
        if epoch_num > self.warmup_epochs:
            lr = self.lr_end + (self.lr_init - self.lr_end) * \
                 (1 + P.Cos()(P.Pi() * (epoch_num - self.warmup_epochs) / 
                             (self.total_epochs - self.warmup_epochs))) / 2
        else:
            lr = self.lr_init * epoch_num / self.warmup_epochs
        print("epoch: %s, lr: %s" % (epoch_num, lr))


def acc_fn(logits, labels):
    """Calculate accuracy."""
    labels = labels.asnumpy()
    logits = logits.asnumpy()
    labels = labels.reshape(-1)
    logits = logits.reshape(-1, logits.shape[-1])
    pred = logits.argmax(axis=1)
    correct = (pred == labels).sum()
    return correct / len(labels)


def define_net(config, activation="None"):
    """Define network using MindCV models."""
    print("Using backbone: MobileNetV2 from mindcv")
    
    # 使用MindCV创建MobileNetV2模型
    net = create_model("mobilenet_v2_100_224", 
                      pretrained=True, 
                      num_classes=config.num_classes)
    
    # 分离backbone和head
    backbone_net = nn.SequentialCell(*list(net.cells())[:-1])  # 去掉最后的分类层
    head_net = nn.Dense(1280, config.num_classes)  # MobileNetV2最后一层输出1280维
    
    # 重新组合网络
    net = nn.SequentialCell(backbone_net, head_net)
    if activation == "Softmax":
        net = nn.SequentialCell(net, nn.Softmax())
    
    return backbone_net, head_net, net


def define_net_resnet(config, activation="None"):
    """Define ResNet network using MindCV models."""
    print("Using backbone: ResNet18 from mindcv")
    
    # 使用MindCV创建ResNet18模型
    net = create_model("resnet18", 
                      pretrained=True, 
                      num_classes=config.num_classes)
    
    # 分离backbone和head
    backbone_net = nn.SequentialCell(*list(net.cells())[:-1])  # 去掉最后的分类层
    head_net = nn.Dense(512, config.num_classes)  # ResNet18最后一层输出512维
    
    # 重新组合网络
    net = nn.SequentialCell(backbone_net, head_net)
    if activation == "Softmax":
        net = nn.SequentialCell(net, nn.Softmax())
    
    return backbone_net, head_net, net


def define_net_vit(config, activation="None"):
    """Define Vision Transformer network using MindCV models."""
    print("Using backbone: ViT-Base from mindcv")
    
    # 使用MindCV创建ViT-Base模型
    net = create_model("vit_base_patch16_224", 
                      pretrained=True, 
                      num_classes=config.num_classes)
    
    # 分离backbone和head
    backbone_net = nn.SequentialCell(*list(net.cells())[:-1])  # 去掉最后的分类层
    head_net = nn.Dense(768, config.num_classes)  # ViT-Base最后一层输出768维
    
    # 重新组合网络
    net = nn.SequentialCell(backbone_net, head_net)
    if activation == "Softmax":
        net = nn.SequentialCell(net, nn.Softmax())
    
    return backbone_net, head_net, net


def load_ckpt(network, pretrain_ckpt_path, trainable=False):
    """Load checkpoint into network."""
    if pretrain_ckpt_path:
        param_dict = load_checkpoint(pretrain_ckpt_path)
        load_param_into_net(network, param_dict)
        print(f"Load pretrain checkpoint from {pretrain_ckpt_path}")
    
    # 设置参数是否可训练
    for param in network.get_parameters():
        param.requires_grad = trainable


def get_networks(network, loss, opt):
    """Get training and evaluation networks."""
    train_net = nn.TrainOneStepCell(network, opt)
    eval_net = nn.Model(network, loss, metrics={"Accuracy": acc_fn})
    return train_net, eval_net


def train(train_net, eval_net, net, data, config):
    """Training function."""
    print("Starting training...")
    
    # 解包数据
    train_features, train_labels, eval_features, eval_labels = data
    
    # 创建数据集
    train_dataset = mindspore.dataset.GeneratorDataset(
        lambda: zip(train_features, train_labels), 
        ["data", "label"]
    )
    eval_dataset = mindspore.dataset.GeneratorDataset(
        lambda: zip(eval_features, eval_labels), 
        ["data", "label"]
    )
    
    # 训练循环
    for epoch in range(config.epoch_size):
        print(f"Epoch {epoch+1}/{config.epoch_size}")
        
        # 训练
        train_net.set_train()
        for step, (data, label) in enumerate(train_dataset):
            loss = train_net(data, label)
            if step % 100 == 0:
                print(f"Step {step}, Loss: {loss}")
        
        # 评估
        eval_net.set_train(False)
        result = eval_net.eval(eval_dataset)
        print(f"Epoch {epoch+1} - Accuracy: {result['Accuracy']}")
    
    print("Training completed!")
