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

"""Command line argument parsing."""

import argparse
import os

def train_parse_args():
    """Parse training arguments."""
    parser = argparse.ArgumentParser(description='Image Classification Training')
    
    # 数据集相关参数
    parser.add_argument('--dataset_path', type=str, default='./data',
                       help='Path to dataset directory')
    parser.add_argument('--pretrain_ckpt', type=str, default=None,
                       help='Path to pretrained checkpoint')
    
    # 训练相关参数
    parser.add_argument('--epoch_size', type=int, default=10,
                       help='Number of training epochs')
    parser.add_argument('--batch_size', type=int, default=32,
                       help='Batch size for training')
    parser.add_argument('--lr_max', type=float, default=0.01,
                       help='Maximum learning rate')
    parser.add_argument('--warmup_epochs', type=int, default=5,
                       help='Number of warmup epochs')
    parser.add_argument('--momentum', type=float, default=0.9,
                       help='Momentum for optimizer')
    parser.add_argument('--weight_decay', type=float, default=0.0001,
                       help='Weight decay for optimizer')
    parser.add_argument('--label_smooth', type=float, default=0.1,
                       help='Label smoothing factor')
    
    # 模型相关参数
    parser.add_argument('--model', type=str, default='mobilenetv2',
                       choices=['mobilenetv2', 'resnet', 'vit', 'swin'],
                       help='Model architecture to use')
    parser.add_argument('--num_classes', type=int, default=2,
                       help='Number of classes')
    parser.add_argument('--image_size', type=int, default=224,
                       help='Input image size')
    
    # 设备相关参数
    parser.add_argument('--device_target', type=str, default='CPU',
                       choices=['CPU', 'GPU', 'Ascend'],
                       help='Device target for training')
    parser.add_argument('--device_id', type=int, default=0,
                       help='Device ID')
    
    # 其他参数
    parser.add_argument('--num_parallel_workers', type=int, default=4,
                       help='Number of parallel workers for data loading')
    parser.add_argument('--save_checkpoint', action='store_true',
                       help='Save checkpoint during training')
    parser.add_argument('--checkpoint_path', type=str, default='./checkpoints',
                       help='Path to save checkpoints')
    
    args = parser.parse_args()
    
    # 验证参数
    if not os.path.exists(args.dataset_path):
        raise ValueError(f"Dataset path {args.dataset_path} does not exist")
    
    if args.pretrain_ckpt and not os.path.exists(args.pretrain_ckpt):
        raise ValueError(f"Pretrained checkpoint {args.pretrain_ckpt} does not exist")
    
    return args


def eval_parse_args():
    """Parse evaluation arguments."""
    parser = argparse.ArgumentParser(description='Image Classification Evaluation')
    
    # 模型相关参数
    parser.add_argument('--model_path', type=str, required=True,
                       help='Path to trained model')
    parser.add_argument('--dataset_path', type=str, required=True,
                       help='Path to evaluation dataset')
    parser.add_argument('--model', type=str, default='mobilenetv2',
                       choices=['mobilenetv2', 'resnet', 'vit', 'swin'],
                       help='Model architecture')
    
    # 设备相关参数
    parser.add_argument('--device_target', type=str, default='CPU',
                       choices=['CPU', 'GPU', 'Ascend'],
                       help='Device target for evaluation')
    parser.add_argument('--device_id', type=int, default=0,
                       help='Device ID')
    
    # 其他参数
    parser.add_argument('--batch_size', type=int, default=32,
                       help='Batch size for evaluation')
    parser.add_argument('--image_size', type=int, default=224,
                       help='Input image size')
    
    args = parser.parse_args()
    
    # 验证参数
    if not os.path.exists(args.model_path):
        raise ValueError(f"Model path {args.model_path} does not exist")
    
    if not os.path.exists(args.dataset_path):
        raise ValueError(f"Dataset path {args.dataset_path} does not exist")
    
    return args


def convert_parse_args():
    """Parse model conversion arguments."""
    parser = argparse.ArgumentParser(description='Model Conversion')
    
    # 模型相关参数
    parser.add_argument('--model_path', type=str, required=True,
                       help='Path to trained model')
    parser.add_argument('--output_path', type=str, required=True,
                       help='Path to save converted model')
    parser.add_argument('--model', type=str, default='mobilenetv2',
                       choices=['mobilenetv2', 'resnet', 'vit', 'swin'],
                       help='Model architecture')
    
    # 转换相关参数
    parser.add_argument('--input_format', type=str, default='NCHW',
                       help='Input format for conversion')
    parser.add_argument('--input_shape', type=str, default='1,3,224,224',
                       help='Input shape for conversion')
    parser.add_argument('--device_target', type=str, default='CPU',
                       choices=['CPU', 'GPU', 'Ascend'],
                       help='Target device for conversion')
    
    args = parser.parse_args()
    
    # 验证参数
    if not os.path.exists(args.model_path):
        raise ValueError(f"Model path {args.model_path} does not exist")
    
    return args
