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

"""Configuration utilities."""

import argparse
from mindspore import context

class Config:
    """Configuration class for training parameters."""
    
    def __init__(self):
        # 数据集配置
        self.num_classes = 2  # 猫狗二分类
        self.image_size = 224
        self.batch_size = 32
        self.num_parallel_workers = 4
        
        # 训练配置
        self.epoch_size = 10
        self.lr_init = 0.0
        self.lr_end = 0.0
        self.lr_max = 0.01
        self.warmup_epochs = 5
        self.momentum = 0.9
        self.weight_decay = 0.0001
        self.label_smooth = 0.1
        
        # 设备配置
        self.device_target = "CPU"
        self.device_id = 0
        self.mode = context.GRAPH_MODE
        
        # 模型配置
        self.model_name = "mobilenetv2"
        self.pretrain_ckpt = None


def set_config(args):
    """Set configuration from command line arguments."""
    config = Config()
    
    # 更新配置
    if hasattr(args, 'dataset_path'):
        config.dataset_path = args.dataset_path
    if hasattr(args, 'pretrain_ckpt'):
        config.pretrain_ckpt = args.pretrain_ckpt
    if hasattr(args, 'epoch_size'):
        config.epoch_size = args.epoch_size
    if hasattr(args, 'batch_size'):
        config.batch_size = args.batch_size
    if hasattr(args, 'lr_max'):
        config.lr_max = args.lr_max
    if hasattr(args, 'model'):
        config.model_name = args.model
    
    # 根据模型调整配置
    if config.model_name == "resnet":
        config.lr_max = 0.001  # ResNet需要更小的学习率
        config.warmup_epochs = 3
    elif config.model_name == "vit":
        config.lr_max = 0.0001  # ViT需要更小的学习率
        config.warmup_epochs = 10
        config.batch_size = 16  # ViT显存需求更大
    
    return config


def get_model_config(model_name):
    """Get model-specific configuration."""
    configs = {
        "mobilenetv2": {
            "backbone_dim": 1280,
            "lr_max": 0.01,
            "warmup_epochs": 5,
            "batch_size": 32
        },
        "resnet18": {
            "backbone_dim": 512,
            "lr_max": 0.001,
            "warmup_epochs": 3,
            "batch_size": 32
        },
        "resnet50": {
            "backbone_dim": 2048,
            "lr_max": 0.001,
            "warmup_epochs": 3,
            "batch_size": 16
        },
        "vit_base": {
            "backbone_dim": 768,
            "lr_max": 0.0001,
            "warmup_epochs": 10,
            "batch_size": 16
        },
        "swin_tiny": {
            "backbone_dim": 768,
            "lr_max": 0.0001,
            "warmup_epochs": 10,
            "batch_size": 16
        }
    }
    
    return configs.get(model_name, configs["mobilenetv2"])
