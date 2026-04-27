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

"""Train Vision Transformer on ImageNet for cat-dog classification."""

import time
from mindspore import Tensor, nn
from mindspore.nn.optim.momentum import Momentum
from mindspore.nn.loss import SoftmaxCrossEntropyWithLogits
from mindspore.common import set_seed

from src.dataset import extract_features
from src.lr_generator import get_lr
from src.config import set_config
from src.args import train_parse_args
from src.utils import context_device_init, export_mindir, predict_from_net, get_samples_from_eval_dataset
from src.models import CrossEntropyWithLabelSmooth, define_net_vit, load_ckpt, get_networks, train

set_seed(1)

if __name__ == '__main__':
    # 解析命令行参数
    args_opt = train_parse_args()
    config = set_config(args_opt)
    
    # 设置ViT特定配置
    config.model_name = "vit"
    config.lr_max = 0.0001  # ViT需要更小的学习率
    config.warmup_epochs = 10
    config.batch_size = 16  # ViT显存需求更大
    
    start = time.time()

    # 设置运行环境和设备初始化
    context_device_init(config)

    # 定义ViT网络结构
    backbone_net, head_net, net = define_net_vit(config, activation="Softmax")

    # 加载预训练权重到骨干网络
    load_ckpt(backbone_net, args_opt.pretrain_ckpt, trainable=False)

    # 训练前测试推理
    test_list = get_samples_from_eval_dataset(args_opt.dataset_path)
    predict_from_net(net, test_list, config, show_title="ViT pre training")

    # 提取特征并缓存
    data, step_size = extract_features(backbone_net, args_opt.dataset_path, config)

    # 定义损失函数
    if config.label_smooth > 0:
        loss = CrossEntropyWithLabelSmooth(
            smooth_factor=config.label_smooth, 
            num_classes=config.num_classes
        )
    else:
        loss = SoftmaxCrossEntropyWithLogits(sparse=True, reduction='mean')

    # 获取学习率调度
    lr = Tensor(get_lr(global_step=0,
                       lr_init=config.lr_init,
                       lr_end=config.lr_end,
                       lr_max=config.lr_max,
                       warmup_epochs=config.warmup_epochs,
                       total_epochs=config.epoch_size,
                       steps_per_epoch=step_size))

    # 获取优化器（仅训练分类头参数）
    opt = Momentum(filter(lambda x: x.requires_grad, head_net.get_parameters()), 
                   lr, config.momentum, config.weight_decay)

    # 定义训练和评估网络并开始训练
    train_net, eval_net = get_networks(head_net, loss, opt)
    train(train_net, eval_net, net, data, config)
    
    print("ViT training total cost {:5.4f} s".format(time.time() - start))

    # 训练后测试推理
    predict_from_net(net, test_list, config, show_title="ViT after training")

    # 导出模型文件
    export_mindir(net, "vit_base")
